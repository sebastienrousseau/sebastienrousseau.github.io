# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Offline tests for ``scripts/seo_and_audit/search_alert.py``: open or
update one ``search-alert`` issue, once per report week."""

from __future__ import annotations

import io
import json
import urllib.request
from typing import Any

import pytest
import search_alert as sa

REPO = "owner/site"
WEEK = "2026-11-01"


class FakeGitHub:
    """Records calls; answers GETs from ``issues`` and ``comments``."""

    def __init__(self, issues: list[dict[str, Any]], comments: list[dict[str, Any]] | None = None):
        self.issues = issues
        self.comments = comments or []
        self.calls: list[tuple[str, str, dict[str, Any] | None]] = []

    def call(self, method: str, path: str, body: dict[str, Any] | None = None) -> Any:
        self.calls.append((method, path, body))
        if method == "GET" and "/comments" in path:
            return self.comments
        if method == "GET":
            return self.issues
        return {"number": 99, "html_url": "https://github.com/owner/site/issues/99"}

    def posts(self) -> list[tuple[str, dict[str, Any] | None]]:
        return [(p, b) for m, p, b in self.calls if m == "POST"]


def test_no_open_issue_creates_one_with_the_label() -> None:
    gh = FakeGitHub([])
    assert sa.file_alert(gh, REPO, "Drop", "body", WEEK) == "created #99"
    ((path, body),) = gh.posts()
    assert path == f"/repos/{REPO}/issues"
    assert body is not None
    assert body["labels"] == ["search-alert"]
    assert sa.marker(WEEK) in body["body"]
    assert gh.calls[0][1] == f"/repos/{REPO}/issues?labels=search-alert&state=open&per_page=100"


def test_open_issue_gets_a_comment_not_a_second_issue() -> None:
    gh = FakeGitHub([{"number": 7, "body": sa.marker("2026-10-25")}])
    assert sa.file_alert(gh, REPO, "Drop", "body", WEEK) == "commented on #7"
    ((path, body),) = gh.posts()
    assert path == f"/repos/{REPO}/issues/7/comments"
    assert body is not None and sa.marker(WEEK) in body["body"]


def test_same_week_twice_is_a_no_op() -> None:
    in_body = FakeGitHub([{"number": 7, "body": "x " + sa.marker(WEEK)}])
    assert sa.file_alert(in_body, REPO, "Drop", "body", WEEK) == "already reported on #7"
    assert in_body.posts() == []
    in_comment = FakeGitHub([{"number": 7, "body": None}], [{"body": sa.marker(WEEK)}])
    assert sa.file_alert(in_comment, REPO, "Drop", "body", WEEK) == "already reported on #7"
    assert in_comment.posts() == []


def test_pull_requests_are_ignored_and_oldest_issue_wins() -> None:
    gh = FakeGitHub(
        [
            {"number": 12, "body": ""},
            {"number": 5, "body": "", "pull_request": {}},
            {"number": 9, "body": ""},
        ]
    )
    assert sa.file_alert(gh, REPO, "Drop", "body", WEEK) == "commented on #9"


class _Resp(io.BytesIO):
    def __enter__(self) -> _Resp:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


def test_rest_client_sends_token_and_json(monkeypatch: pytest.MonkeyPatch) -> None:
    sent: list[urllib.request.Request] = []

    def fake_urlopen(req: urllib.request.Request, timeout: float = 0) -> _Resp:
        sent.append(req)
        return _Resp(json.dumps({"ok": True}).encode())

    monkeypatch.setattr(sa.urllib.request, "urlopen", fake_urlopen)
    gh = sa.GitHub("tok")
    assert gh.call("POST", "/repos/o/r/issues", {"title": "t"}) == {"ok": True}
    req = sent[0]
    assert req.full_url == "https://api.github.com/repos/o/r/issues"
    assert req.get_method() == "POST"
    assert req.get_header("Authorization") == "Bearer tok"
    assert req.data == b'{"title": "t"}'
    gh.call("GET", "/x")
    assert sent[1].data is None
