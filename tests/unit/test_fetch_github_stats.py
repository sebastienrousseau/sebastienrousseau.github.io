"""Unit coverage for fetch_github_stats — Phase 1.3.

fetch_github_stats.py fetches per-repo GitHub metrics into gh-stats.json
(consumed by postbuild to render project cards). The network call is mocked;
these cover the response-slimming, defaults/fallbacks, error tolerance, and
the load_existing cache reader.
"""

from __future__ import annotations

import io
import json
import urllib.error
from pathlib import Path

import fetch_github_stats as fgs


class _FakeResp:
    def __init__(self, payload: dict) -> None:
        self._b = json.dumps(payload).encode("utf-8")

    def read(self) -> bytes:
        return self._b

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


# --- fetch_repo ------------------------------------------------------------


def test_fetch_repo_maps_and_defaults(monkeypatch) -> None:
    payload = {
        "name": "hsh",
        "stargazers_count": 42,
        "forks_count": 7,
        "subscribers_count": 3,
        "language": "Rust",
        "license": {"spdx_id": "Apache-2.0"},
        "pushed_at": "2026-06-01T00:00:00Z",
        # description/homepage omitted → default to ""
    }
    monkeypatch.setattr(fgs.urllib.request, "urlopen", lambda *a, **k: _FakeResp(payload))
    out = fgs.fetch_repo("sebastienrousseau/hsh", token=None)
    assert out["slug"] == "sebastienrousseau/hsh"
    assert out["stars"] == 42 and out["forks"] == 7 and out["watchers"] == 3
    assert out["language"] == "Rust"
    assert out["license"] == "Apache-2.0"
    assert out["description"] == ""  # missing → ""
    assert out["default_branch"] == "main"  # missing → default
    assert out["html_url"] == "https://github.com/sebastienrousseau/hsh"


def test_fetch_repo_null_license_becomes_empty(monkeypatch) -> None:
    monkeypatch.setattr(
        fgs.urllib.request, "urlopen", lambda *a, **k: _FakeResp({"name": "x", "license": None})
    )
    out = fgs.fetch_repo("o/x", token=None)
    assert out["license"] == ""


def test_fetch_repo_httperror_returns_none(monkeypatch) -> None:
    def _raise(*a, **k):
        raise urllib.error.HTTPError("u", 404, "Not Found", {}, io.BytesIO(b""))

    monkeypatch.setattr(fgs.urllib.request, "urlopen", _raise)
    assert fgs.fetch_repo("o/missing", token=None) is None


def test_fetch_repo_urlerror_returns_none(monkeypatch) -> None:
    def _raise(*a, **k):
        raise urllib.error.URLError("boom")

    monkeypatch.setattr(fgs.urllib.request, "urlopen", _raise)
    assert fgs.fetch_repo("o/x", token=None) is None


# --- load_existing ---------------------------------------------------------


def test_load_existing_missing_file(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(fgs, "OUTPUT", tmp_path / "nope.json")
    assert fgs.load_existing() == {}


def test_load_existing_indexes_by_slug(monkeypatch, tmp_path: Path) -> None:
    p = tmp_path / "gh-stats.json"
    p.write_text(
        json.dumps({"repos": [{"slug": "o/a", "stars": 1}, {"stars": 2}]}),  # 2nd lacks slug
        encoding="utf-8",
    )
    monkeypatch.setattr(fgs, "OUTPUT", p)
    out = fgs.load_existing()
    assert out == {"o/a": {"slug": "o/a", "stars": 1}}  # slugless entry skipped


def test_load_existing_bad_json(monkeypatch, tmp_path: Path) -> None:
    p = tmp_path / "gh-stats.json"
    p.write_text("{not json", encoding="utf-8")
    monkeypatch.setattr(fgs, "OUTPUT", p)
    assert fgs.load_existing() == {}
