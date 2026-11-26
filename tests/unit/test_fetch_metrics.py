# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Unit coverage for fetch_metrics — Phase 1.3.

fetch_metrics.py takes the download, package and star figures from the GitHub
profile's profile.json, so the homepage and the profile agree, and keeps the
committed snapshot when that fetch fails. Network is mocked.
"""

from __future__ import annotations

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


def test_github_forks_sums_owned_repos(monkeypatch) -> None:
    repos = [{"forks_count": 2}, {"forks_count": 1}, {"forks_count": 9, "fork": True}]
    monkeypatch.setattr(fm, "_http_get_json", lambda url: repos)
    assert fm._github_forks() == 3


def test_github_forks_non_list_is_zero(monkeypatch) -> None:
    monkeypatch.setattr(fm, "_http_get_json", lambda url: {"message": "rate limited"})
    assert fm._github_forks() == 0


_NUMBERS = {
    "all_time_downloads": 54_661_183,
    "recent_downloads": 2_518_481,
    "window_days": 30,
    "github_stars": 760,
    "packages": 199,
    "as_of": "2026-11-24",
}


def test_profile_numbers_reads_the_profile_json(monkeypatch) -> None:
    seen: list[str] = []
    monkeypatch.setattr(
        fm, "_http_get_json", lambda url: seen.append(url) or {"numbers": dict(_NUMBERS)}
    )
    assert fm._profile_numbers() == _NUMBERS
    assert seen == [fm.PROFILE_JSON_URL]


def test_profile_numbers_rejects_a_partial_answer(monkeypatch) -> None:
    for bad in (
        None,
        {},
        {"numbers": {**_NUMBERS, "packages": 0}},
        {"numbers": {k: v for k, v in _NUMBERS.items() if k != "recent_downloads"}},
    ):
        monkeypatch.setattr(fm, "_http_get_json", lambda url, bad=bad: bad)
        assert fm._profile_numbers() is None


def _run_main(tmp_path, monkeypatch, numbers):
    out = tmp_path / "metrics.json"
    out.write_text(
        '{"stats":[{"key":"downloads_30d","value":3700000},'
        '{"key":"packages_published","value":179},'
        '{"key":"downloads_total","value":53927032},'
        '{"key":"github_stars","value":761},{"key":"github_forks","value":114}]}',
        encoding="utf-8",
    )
    monkeypatch.setattr(fm, "OUT_PATH", out)
    monkeypatch.delenv(fm.SKIP_ENV, raising=False)
    monkeypatch.setattr(fm, "_profile_numbers", lambda: numbers)
    monkeypatch.setattr(fm, "_github_forks", lambda: 115)
    monkeypatch.setattr(fm, "_articles_count", lambda: 132)
    assert fm.main() == 0
    import json

    return {s["key"]: s["value"] for s in json.loads(out.read_text())["stats"]}


def test_main_takes_the_profile_figures_even_when_lower(tmp_path, monkeypatch) -> None:
    """The GitHub profile and the homepage show the same four numbers.

    A 30-day window falls as well as rises; the old max() against the
    committed snapshot froze it at 3.7M while the profile read 2.5M.
    """
    got = _run_main(tmp_path, monkeypatch, dict(_NUMBERS))
    assert got["downloads_total"] == 54_661_183
    assert got["downloads_30d"] == 2_518_481
    assert got["packages_published"] == 199
    assert got["github_stars"] == 760
    assert got["github_forks"] == 115


def test_main_keeps_the_snapshot_when_the_profile_is_unreachable(tmp_path, monkeypatch) -> None:
    got = _run_main(tmp_path, monkeypatch, None)
    assert got["downloads_total"] == 53_927_032
    assert got["downloads_30d"] == 3_700_000
    assert got["packages_published"] == 179
    assert got["github_stars"] == 761


# --- _years_active ---------------------------------------------------------


def test_years_active() -> None:
    assert fm._years_active() == "20+"


_DISPLAY = {
    "all_time_downloads": "54.7M",
    "recent_downloads": "2.5M",
    "github_stars": "760",
    "packages": "199",
}


def _run_main_stats(tmp_path, monkeypatch, numbers):
    _run_main(tmp_path, monkeypatch, numbers)
    import json

    return {s["key"]: s for s in json.loads((tmp_path / "metrics.json").read_text())["stats"]}


def test_main_records_the_profile_display_strings(tmp_path, monkeypatch) -> None:
    """The profile's printed figures travel with the values, so the build
    prints exactly what the profile's numbers panel prints."""
    got = _run_main_stats(tmp_path, monkeypatch, {**_NUMBERS, "display": dict(_DISPLAY)})
    assert got["downloads_total"]["display"] == "54.7M"
    assert got["downloads_30d"]["display"] == "2.5M"
    assert got["github_stars"]["display"] == "760"
    assert got["packages_published"]["display"] == "199"
    assert "display" not in got["github_forks"]


def test_main_ignores_malformed_display_strings(tmp_path, monkeypatch) -> None:
    for bad in (
        None,
        "54.7M",
        {**_DISPLAY, "packages": 199},
        {**_DISPLAY, "github_stars": "<b>760</b>"},
    ):
        got = _run_main_stats(tmp_path, monkeypatch, {**_NUMBERS, "display": bad})
        assert all("display" not in s for s in got.values()), bad


def test_main_keeps_the_snapshot_display_when_the_profile_is_unreachable(
    tmp_path, monkeypatch
) -> None:
    _run_main(tmp_path, monkeypatch, {**_NUMBERS, "display": dict(_DISPLAY)})
    out = tmp_path / "metrics.json"
    snapshot = out.read_text()
    monkeypatch.setattr(fm, "_profile_numbers", lambda: None)
    assert fm.main() == 0
    import json

    stats = {s["key"]: s for s in json.loads(out.read_text())["stats"]}
    assert stats["packages_published"]["display"] == "199"
    assert json.loads(snapshot)["stats"] != []
