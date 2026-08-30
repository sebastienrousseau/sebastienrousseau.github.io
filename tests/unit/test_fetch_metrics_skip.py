# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""``fetch_metrics`` must be able to leave the committed snapshot alone.

Every figure in _data/proof/metrics.json is fetched live — pypistats,
crates.io, the GitHub API. The reproducible-build CI job builds twice and
requires byte-identical output, so any counter moving between the two
builds broke it: github_stars and github_forks render in `plain` format,
so a single star was enough to rewrite the KPI on /, /about/, /projects/
and /speaking/ plus all 34 locale forks, and search-index.json with them.
Two runs seconds apart were observed at 44,651,836 and 44,664,070
downloads.

That made a job whose purpose is "catch a build pass that is not
idempotent" measure the network instead. SKIP_METRICS_FETCH lets the job
build twice against one snapshot.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
_SPEC = importlib.util.spec_from_file_location(
    "fetch_metrics", ROOT / "scripts" / "seo_and_audit" / "fetch_metrics.py"
)
fetch_metrics = importlib.util.module_from_spec(_SPEC)
sys.modules["fetch_metrics"] = fetch_metrics
_SPEC.loader.exec_module(fetch_metrics)


@pytest.fixture
def snapshot(tmp_path, monkeypatch):
    """Point the module at a throwaway metrics.json."""
    out = tmp_path / "metrics.json"
    out.write_text(
        '{"$generated_at":"2026-01-01T00:00:00+00:00",'
        '"stats":[{"key":"github_stars","label":"Stars","value":672,'
        '"format":"plain","source":"api.github.com"}]}\n',
        encoding="utf-8",
    )
    monkeypatch.setattr(fetch_metrics, "OUT_PATH", out)
    return out


def test_skip_leaves_the_snapshot_byte_identical(snapshot, monkeypatch, capsys):
    monkeypatch.setenv(fetch_metrics.SKIP_ENV, "1")
    before = snapshot.read_bytes()

    def _boom(*_a, **_k):  # any network call is a bug in this mode
        raise AssertionError("fetch_metrics hit the network with the skip flag set")

    monkeypatch.setattr(fetch_metrics, "_pypi_downloads", _boom)
    monkeypatch.setattr(fetch_metrics, "_crates_downloads_all", _boom)
    monkeypatch.setattr(fetch_metrics, "_github_repos", _boom)

    assert fetch_metrics.main() == 0
    assert snapshot.read_bytes() == before
    assert "keeping committed snapshot" in capsys.readouterr().out


def test_skip_is_reported_when_there_is_no_snapshot(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(fetch_metrics, "OUT_PATH", tmp_path / "absent.json")
    monkeypatch.setenv(fetch_metrics.SKIP_ENV, "1")
    assert fetch_metrics.main() == 0
    assert "no committed snapshot" in capsys.readouterr().out


def test_unset_flag_still_fetches(snapshot, monkeypatch):
    """The default path must be untouched — the flag is opt-in only."""
    monkeypatch.delenv(fetch_metrics.SKIP_ENV, raising=False)
    called: list[str] = []
    monkeypatch.setattr(fetch_metrics, "_pypi_downloads", lambda *_a: called.append("pypi") or 1)
    monkeypatch.setattr(
        fetch_metrics, "_crates_downloads_all", lambda: called.append("crates") or 2
    )
    monkeypatch.setattr(fetch_metrics, "_github_repos", lambda: called.append("gh") or (3, 4))
    monkeypatch.setattr(fetch_metrics, "_articles_count", lambda: 5)
    monkeypatch.setattr(fetch_metrics, "_years_active", lambda: 6)
    assert fetch_metrics.main() == 0
    assert {"pypi", "crates", "gh"} <= set(called)
