# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Unit coverage for fetch_metrics — Phase 1.3.

fetch_metrics.py aggregates public download/star metrics for the project cards
(with fail-soft fallbacks). Network is mocked; these cover the JSON fetch, the
per-source parsers/fallbacks, compact formatting, and the date math.
"""

from __future__ import annotations

import datetime as _dt
import urllib.error

import fetch_metrics as fm


class _Resp:
    def __init__(self, payload, status=200):
        import json

        self._b = json.dumps(payload).encode()
        self.status = status

    def read(self):
        return self._b

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


# --- _format_compact -------------------------------------------------------


def test_format_compact() -> None:
    assert fm._format_compact(500) == "500"
    assert fm._format_compact(1000) == "1K"  # .0 stripped
    assert fm._format_compact(12345) == "12.3K"
    assert fm._format_compact(1_000_000) == "1M"
    assert fm._format_compact(1_234_567) == "1.2M"


# --- _http_get_json --------------------------------------------------------


def test_http_get_json_ok(monkeypatch) -> None:
    monkeypatch.setattr(fm.urllib.request, "urlopen", lambda *a, **k: _Resp({"x": 1}))
    assert fm._http_get_json("http://u") == {"x": 1}


def test_http_get_json_non_200_is_none(monkeypatch) -> None:
    monkeypatch.setattr(fm.urllib.request, "urlopen", lambda *a, **k: _Resp({}, status=503))
    assert fm._http_get_json("http://u") is None


def test_http_get_json_exception_is_none(monkeypatch) -> None:
    def _boom(*a, **k):
        raise urllib.error.URLError("down")

    monkeypatch.setattr(fm.urllib.request, "urlopen", _boom)
    assert fm._http_get_json("http://u") is None


# --- per-source parsers ----------------------------------------------------


def test_pypi_downloads(monkeypatch) -> None:
    monkeypatch.setattr(fm, "_http_get_json", lambda url: {"data": {"last_month": 4200}})
    assert fm._pypi_downloads("pain001") == 4200


def test_pypi_downloads_failure_is_zero(monkeypatch) -> None:
    monkeypatch.setattr(fm, "_http_get_json", lambda url: None)
    assert fm._pypi_downloads("pain001") == 0


def test_github_repos_sums(monkeypatch) -> None:
    repos = [{"stargazers_count": 10, "forks_count": 2}, {"stargazers_count": 5, "forks_count": 1}]
    monkeypatch.setattr(fm, "_http_get_json", lambda url: repos)
    assert fm._github_repos() == (15, 3)


def test_github_repos_non_list_is_zeros(monkeypatch) -> None:
    monkeypatch.setattr(fm, "_http_get_json", lambda url: {"message": "rate limited"})
    assert fm._github_repos() == (0, 0)


def test_crates_downloads_sums(monkeypatch) -> None:
    def fake(url):
        if "users/" in url:
            return {"user": {"id": 99}}
        return {"crates": [{"downloads": 100}, {"downloads": 250}]}

    monkeypatch.setattr(fm, "_http_get_json", fake)
    assert fm._crates_downloads_all() == 350


def test_crates_downloads_no_uid_is_zero(monkeypatch) -> None:
    monkeypatch.setattr(fm, "_http_get_json", lambda url: {})
    assert fm._crates_downloads_all() == 0


# --- _years_active ---------------------------------------------------------


def test_years_active() -> None:
    assert fm._years_active() == _dt.date.today().year - 2007
