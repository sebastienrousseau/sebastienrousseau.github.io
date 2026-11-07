# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Offline tests for ``scripts/seo_and_audit/check_live_redirects.py``.

No request leaves the machine: the opener is a fake that answers from a
table, so the 301 assertion, the sample and the CLI are all exercised
without touching the live site.
"""

from __future__ import annotations

import email.message
import io
import json
import urllib.error
import urllib.request
from pathlib import Path

import check_live_redirects as clr
import pytest

BASE = "https://sebastienrousseau.com"


def _headers(location: str | None) -> email.message.Message:
    msg = email.message.Message()
    if location is not None:
        msg["Location"] = location
    return msg


class FakeOpener:
    """Answers ``open()`` from ``{url: (status, location)}``, recording calls."""

    def __init__(self, table: dict[str, tuple[int, str | None]]) -> None:
        self.table = table
        self.calls: list[tuple[str, str]] = []

    def open(self, req: urllib.request.Request, timeout: float = 0) -> io.BytesIO:
        self.calls.append((req.get_method(), req.full_url))
        status, location = self.table[req.full_url]
        if status == 200:
            return io.BytesIO(b"")
        raise urllib.error.HTTPError(req.full_url, status, "x", _headers(location), None)


def test_sample_is_spread_and_bounded() -> None:
    sources = [f"/p{i:03d}/" for i in range(100)]
    picks = clr.sample(sources, 20, seed=0)
    assert len(picks) == 20
    assert picks[0] == "/p000/" and picks[1] == "/p005/"
    assert clr.sample(sources, 20, seed=3)[0] == "/p003/"
    assert clr.sample(sources[:4], 20, seed=7) == sources[:4]


def test_probe_reads_status_and_location_without_following() -> None:
    url = f"{BASE}/old/"
    opener = FakeOpener({url: (301, f"{BASE}/new/")})
    assert clr.probe(url, opener) == (301, f"{BASE}/new/")
    assert opener.calls == [("HEAD", url)]


def test_probe_200_has_no_location() -> None:
    url = f"{BASE}/live/"
    assert clr.probe(url, FakeOpener({url: (200, None)})) == (200, None)


def test_check_redirect_passes_on_single_hop_301() -> None:
    opener = FakeOpener({f"{BASE}/old/": (301, f"{BASE}/new/")})
    assert clr.check_redirect(BASE, "/old/", "/new/", opener) is None


def test_check_redirect_fails_on_302_and_wrong_target() -> None:
    opener = FakeOpener(
        {
            f"{BASE}/a/": (302, f"{BASE}/new/"),
            f"{BASE}/b/": (301, f"{BASE}/elsewhere/"),
            f"{BASE}/c/": (200, None),
        }
    )
    assert clr.check_redirect(BASE, "/a/", "/new/", opener) == f"{BASE}/a/: HTTP 302, expected 301"
    assert clr.check_redirect(BASE, "/b/", "/new/", opener) == (
        f"{BASE}/b/: 301 to {BASE}/elsewhere/, expected {BASE}/new/"
    )
    assert clr.check_redirect(BASE, "/c/", "/new/", opener) == f"{BASE}/c/: HTTP 200, expected 301"


def test_non_ascii_paths_are_encoded_and_compared_decoded() -> None:
    src, dst = "/zh-hans/旧/", "/zh-hans/新/"
    url = f"{BASE}/zh-hans/%E6%97%A7/"
    opener = FakeOpener({url: (301, f"{BASE}/zh-hans/%E6%96%B0/")})
    assert clr.check_redirect(BASE, src, dst, opener) is None


def test_unreachable_is_a_problem() -> None:
    class Down:
        def open(self, req: urllib.request.Request, timeout: float = 0) -> None:
            raise urllib.error.URLError("dns")

    problem = clr.check_redirect(BASE, "/old/", "/new/", Down())
    assert problem is not None and "unreachable" in problem


def test_no_redirect_handler_refuses_to_follow() -> None:
    handler = clr.NoRedirect()
    req = urllib.request.Request(f"{BASE}/old/")
    assert handler.redirect_request(req, None, 301, "x", _headers(None), f"{BASE}/new/") is None


def _map_file(tmp_path: Path, redirects: dict[str, str]) -> Path:
    path = tmp_path / "redirects.json"
    path.write_text(json.dumps({"version": 1, "redirects": redirects}), encoding="utf-8")
    return path


def test_main_runs_sequentially_and_reports(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    redirects = {f"/old{i}/": f"/new{i}/" for i in range(30)}
    table: dict[str, tuple[int, str | None]] = {
        f"{BASE}{s}": (301, f"{BASE}{t}") for s, t in redirects.items()
    }
    table[f"{BASE}/old0/"] = (302, f"{BASE}/new0/")
    opener = FakeOpener(table)
    monkeypatch.setattr(clr, "build_opener", lambda: opener)
    rc = clr.main(["--map", str(_map_file(tmp_path, redirects)), "--seed", "0", "--delay", "0"])
    assert rc == 1
    assert len(opener.calls) == 20
    err = capsys.readouterr().err
    assert "1 of 20" in err and "HTTP 302" in err


def test_main_ok(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    redirects = {"/old/": "/new/"}
    opener = FakeOpener({f"{BASE}/old/": (301, f"{BASE}/new/")})
    monkeypatch.setattr(clr, "build_opener", lambda: opener)
    monkeypatch.setattr(clr.time, "sleep", lambda _s: None)
    assert clr.main(["--map", str(_map_file(tmp_path, redirects))]) == 0
    assert "OK: 1 sampled" in capsys.readouterr().out


def test_build_opener_does_not_follow_redirects() -> None:
    opener = clr.build_opener()
    assert any(isinstance(h, clr.NoRedirect) for h in opener.handlers)
