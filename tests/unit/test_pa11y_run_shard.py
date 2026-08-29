"""Chunked pa11y shard runner — scripts/seo_and_audit/pa11y_run_shard.py."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "seo_and_audit"))

import pa11y_run_shard as runner


def _config(tmp_path: Path, n: int) -> Path:
    cfg = tmp_path / "shard.json"
    cfg.write_text(
        json.dumps({"defaults": {"timeout": 20000}, "urls": [f"http://x/{i}" for i in range(n)]})
    )
    return cfg


def test_empty_shard_writes_a_zero_report(tmp_path):
    cfg = tmp_path / "shard.json"
    cfg.write_text(json.dumps({"urls": []}))
    out = tmp_path / "out.json"
    assert runner.run(cfg, out, chunk_size=8, timeout_s=1) == 0
    assert json.loads(out.read_text()) == {"total": 0, "passes": 0, "errors": 0, "results": {}}


def test_results_from_every_chunk_are_merged(tmp_path, monkeypatch):
    """Chunking must not lose results — the point is the other chunks survive."""
    seen = []

    def fake(cfg, timeout_s):
        urls = json.loads(cfg.read_text())["urls"]
        seen.append(len(urls))
        return 0, {"results": {u: [] for u in urls}}

    monkeypatch.setattr(runner, "_run_chunk", fake)
    out = tmp_path / "out.json"
    assert runner.run(_config(tmp_path, 10), out, chunk_size=4, timeout_s=1) == 0
    report = json.loads(out.read_text())
    assert seen == [4, 4, 2]
    assert report["total"] == 10
    assert report["passes"] == 10
    assert report["errors"] == 0


def test_errors_are_counted_not_swallowed(tmp_path, monkeypatch):
    def fake(cfg, timeout_s):
        urls = json.loads(cfg.read_text())["urls"]
        return 2, {"results": {u: ([{"code": "X"}] if u.endswith("0") else []) for u in urls}}

    monkeypatch.setattr(runner, "_run_chunk", fake)
    out = tmp_path / "out.json"
    runner.run(_config(tmp_path, 4), out, chunk_size=4, timeout_s=1)
    report = json.loads(out.read_text())
    assert report["errors"] == 1
    assert report["passes"] == 3


def test_a_wedged_chunk_is_retried_once(tmp_path, monkeypatch):
    calls = {"n": 0}

    def fake(cfg, timeout_s):
        calls["n"] += 1
        if calls["n"] == 1:
            return 124, {}
        urls = json.loads(cfg.read_text())["urls"]
        return 0, {"results": {u: [] for u in urls}}

    monkeypatch.setattr(runner, "_run_chunk", fake)
    monkeypatch.setattr(runner, "_kill_chrome", lambda: None)
    out = tmp_path / "out.json"
    assert runner.run(_config(tmp_path, 3), out, chunk_size=8, timeout_s=1) == 0
    assert calls["n"] == 2
    assert json.loads(out.read_text())["total"] == 3


def test_a_chunk_wedged_twice_fails_the_shard_but_keeps_the_rest(tmp_path, monkeypatch, capsys):
    """The whole point: one stuck chunk must not cost the other results."""

    def fake(cfg, timeout_s):
        urls = json.loads(cfg.read_text())["urls"]
        if any(u.endswith("/0") for u in urls):
            return 124, {}
        return 0, {"results": {u: [] for u in urls}}

    monkeypatch.setattr(runner, "_run_chunk", fake)
    monkeypatch.setattr(runner, "_kill_chrome", lambda: None)
    out = tmp_path / "out.json"
    assert runner.run(_config(tmp_path, 6), out, chunk_size=3, timeout_s=1) == 1
    report = json.loads(out.read_text())
    assert report["total"] == 3  # the surviving chunk still reported
    assert "unchecked" in capsys.readouterr().out


def test_sigkill_is_treated_as_a_wedge(tmp_path, monkeypatch):
    def fake(cfg, timeout_s):
        return 137, {}

    monkeypatch.setattr(runner, "_run_chunk", fake)
    monkeypatch.setattr(runner, "_kill_chrome", lambda: None)
    out = tmp_path / "out.json"
    assert runner.run(_config(tmp_path, 2), out, chunk_size=8, timeout_s=1) == 1


def test_unparseable_output_is_not_a_pass(tmp_path, monkeypatch):
    """A crashed pa11y-ci must not look like a clean shard."""

    def fake(cfg, timeout_s):
        return 3, {}

    monkeypatch.setattr(runner, "_run_chunk", fake)
    out = tmp_path / "out.json"
    assert runner.run(_config(tmp_path, 2), out, chunk_size=8, timeout_s=1) == 1


@pytest.mark.parametrize("code", [124, 137])
def test_timeout_codes_are_recognised(code):
    assert code in runner.TIMED_OUT


def test_shard_budget_stops_and_reports_the_rest(tmp_path, monkeypatch, capsys):
    """Every chunk wedging must still land inside the job's own timeout."""
    clock = {"t": 0.0}

    def fake(cfg, timeout_s):
        clock["t"] += 100.0
        urls = json.loads(cfg.read_text())["urls"]
        return 0, {"results": {u: [] for u in urls}}

    monkeypatch.setattr(runner, "_run_chunk", fake)
    monkeypatch.setattr(runner.time, "monotonic", lambda: clock["t"])
    out = tmp_path / "out.json"
    rc = runner.run(_config(tmp_path, 20), out, chunk_size=2, timeout_s=1, budget_s=250)
    assert rc == 1
    report = json.loads(out.read_text())
    assert 0 < report["total"] < 20  # stopped early, kept what it had
    assert "unchecked" in capsys.readouterr().out
