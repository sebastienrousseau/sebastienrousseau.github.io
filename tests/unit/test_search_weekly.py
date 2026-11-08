# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Offline tests for ``scripts/seo_and_audit/search_weekly.py``: the API
call and its paging, the Markdown and CSV output, the no-secret no-op and
the alert hand-off. No request leaves the machine."""

from __future__ import annotations

import csv
import datetime as dt
import json
import sys
import types
from pathlib import Path
from typing import Any

import pytest
import search_weekly as sw

FIXTURE = Path(__file__).parent / "fixtures" / "search_weekly" / "searchanalytics.json"
END = "2026-11-01"
CODES = ["en", "fr", "de", "nl"]


class FakeResponse:
    def __init__(self, payload: dict[str, Any]) -> None:
        self.payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict[str, Any]:
        return self.payload


class FakeSession:
    def __init__(self, pages: list[list[dict[str, Any]]]) -> None:
        self.pages = pages
        self.bodies: list[dict[str, Any]] = []
        self.urls: list[str] = []

    def post(self, url: str, json: dict[str, Any]) -> FakeResponse:
        self.urls.append(url)
        self.bodies.append(json)
        return FakeResponse({"rows": self.pages[len(self.bodies) - 1]} if self.pages else {})


def test_fetch_rows_pages_until_a_short_page(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sw, "ROW_LIMIT", 2)
    session = FakeSession([[{"a": 1}, {"a": 2}], [{"a": 3}]])
    rows = sw.fetch_rows(
        session, "sc-domain:example.com", dt.date(2026, 10, 5), dt.date(2026, 11, 1)
    )
    assert rows == [{"a": 1}, {"a": 2}, {"a": 3}]
    assert [b["startRow"] for b in session.bodies] == [0, 2]
    body = session.bodies[0]
    assert body["dimensions"] == ["page", "date"]
    assert (body["startDate"], body["endDate"]) == ("2026-10-05", "2026-11-01")
    assert session.urls[0].endswith("/sites/sc-domain%3Aexample.com/searchAnalytics/query")


def test_fetch_rows_handles_no_rows() -> None:
    assert sw.fetch_rows(FakeSession([]), "s", dt.date(2026, 1, 1), dt.date(2026, 1, 2)) == []


def test_authorized_session_uses_the_read_only_scope(monkeypatch: pytest.MonkeyPatch) -> None:
    seen: dict[str, Any] = {}

    class Creds:
        @staticmethod
        def from_service_account_info(info: dict[str, Any], scopes: list[str]) -> str:
            seen["info"], seen["scopes"] = info, scopes
            return "creds"

    google = types.ModuleType("google")
    oauth2 = types.ModuleType("google.oauth2")
    sa_mod = types.ModuleType("google.oauth2.service_account")
    sa_mod.Credentials = Creds  # type: ignore[attr-defined]
    transport = types.ModuleType("google.auth.transport.requests")
    transport.AuthorizedSession = lambda creds: ("session", creds)  # type: ignore[attr-defined]
    for name, mod in {
        "google": google,
        "google.oauth2": oauth2,
        "google.oauth2.service_account": sa_mod,
        "google.auth": types.ModuleType("google.auth"),
        "google.auth.transport": types.ModuleType("google.auth.transport"),
        "google.auth.transport.requests": transport,
    }.items():
        monkeypatch.setitem(sys.modules, name, mod)
    oauth2.service_account = sa_mod  # type: ignore[attr-defined]
    assert sw.authorized_session('{"client_email": "x"}') == ("session", "creds")
    assert seen == {"info": {"client_email": "x"}, "scopes": [sw.SCOPE]}


def _run(tmp_path: Path, *extra: str) -> tuple[int, Path]:
    summary = tmp_path / "summary.md"
    rc = sw.main(
        [
            "--fixture",
            str(FIXTURE),
            "--end",
            END,
            "--out-dir",
            str(tmp_path / "out"),
            "--summary",
            str(summary),
            "--codes",
            ",".join(CODES),
            "--kept",
            "en,fr,de",
            *extra,
        ]
    )
    return rc, summary


def test_fixture_run_writes_markdown_csv_and_summary(tmp_path: Path) -> None:
    rc, summary = _run(tmp_path)
    assert rc == 0
    md = (tmp_path / "out" / "search-weekly.md").read_text(encoding="utf-8")
    assert summary.read_text(encoding="utf-8") == md
    assert "2026-10-26 to 2026-11-01" in md
    assert "| en | yes | 700 | 1,000 | -30.0% |" in md
    assert "| de | yes | 40 | 0 | new |" in md
    assert "| nl | no |" in md
    assert "`/iso20022-mcp/`" in md
    assert "Alert: impressions fell 30% or more" in md
    with (tmp_path / "out" / "search-weekly.csv").open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    en = next(r for r in rows if r["scope"] == "locale" and r["key"] == "en")
    assert (en["impressions"], en["impressions_previous"], en["impressions_28d"]) == (
        "700",
        "1000",
        "1750",
    )
    assert {r["scope"] for r in rows} == {"locale", "page"}


def test_no_drop_says_so(tmp_path: Path) -> None:
    rc, summary = _run(tmp_path, "--kept", "fr")
    assert rc == 0
    assert "No kept locale fell 30% or more" in summary.read_text(encoding="utf-8")


def test_missing_secret_is_a_clear_no_op(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.delenv("GSC_SERVICE_ACCOUNT_JSON", raising=False)
    summary = tmp_path / "summary.md"
    rc = sw.main(["--out-dir", str(tmp_path / "out"), "--summary", str(summary)])
    assert rc == 0
    text = summary.read_text(encoding="utf-8")
    assert "GSC_SERVICE_ACCOUNT_JSON is not set" in text
    assert "GSC_SERVICE_ACCOUNT_JSON is not set" in capsys.readouterr().out
    assert not (tmp_path / "out" / "search-weekly.csv").exists()


def test_secret_drives_the_live_fetch(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    rows = json.loads(FIXTURE.read_text(encoding="utf-8"))["rows"]
    monkeypatch.setenv("GSC_SERVICE_ACCOUNT_JSON", "{}")
    monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)
    monkeypatch.setattr(sw, "authorized_session", lambda info: FakeSession([rows]))
    rc = sw.main(["--end", END, "--out-dir", str(tmp_path / "out"), "--codes", ",".join(CODES)])
    assert rc == 0
    assert (tmp_path / "out" / "search-weekly.csv").is_file()


def test_alert_files_an_issue_when_asked(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    filed: list[tuple[str, str, str]] = []

    def fake_file_alert(gh: object, repo: str, title: str, body: str, week: str) -> str:
        filed.append((repo, title, week))
        assert "Pages that lost the most" in body
        return "created #1"

    monkeypatch.setattr(sw.search_alert, "file_alert", fake_file_alert)
    monkeypatch.setenv("GITHUB_TOKEN", "tok")
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/site")
    rc, _ = _run(tmp_path, "--file-issue")
    assert rc == 0
    assert filed == [
        ("owner/site", "Search impressions fell 30% or more: en (week to 2026-11-01)", END)
    ]


def test_file_issue_without_token_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    rc, _ = _run(tmp_path, "--file-issue")
    assert rc == 1


def test_default_end_leaves_room_for_late_data() -> None:
    assert sw.default_end(dt.date(2026, 11, 2)) == dt.date(2026, 10, 30)


def test_default_codes_and_kept_come_from_the_registry_and_policy() -> None:
    codes, kept = sw.locale_sets(None, None)
    assert "en" in kept and kept <= codes
    assert "nl" in codes and "nl" not in kept


def test_format_helpers() -> None:
    assert sw.pct(None) == "new"
    assert sw.pct(0.5) == "+50.0%"
    assert sw.pct(-0.3) == "-30.0%"
    assert sw.change_label(0, 0) == "n/a"
    assert sw.change_label(5, 0) == "new"
    assert sw.change_label(7, 10) == "-30.0%"
