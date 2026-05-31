"""Unit tests for scripts/seo_and_audit/pa11y_retry_flakes.py.

We don't actually exercise the subprocess retry here — that needs the
pa11y-ci binary, which only exists in CI. We do exercise the partition
between flaky and real failures, plus the exit-code semantics for the
edge cases the workflow depends on.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

import importlib.util

_HERE = Path(__file__).resolve().parent
_SCRIPT = _HERE.parent / "scripts" / "seo_and_audit" / "pa11y_retry_flakes.py"
_spec = importlib.util.spec_from_file_location("pa11y_retry_flakes", _SCRIPT)
assert _spec is not None and _spec.loader is not None
prf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(prf)


def _write_report(tmp_path: Path, payload: dict) -> Path:
    p = tmp_path / "pa11y.json"
    p.write_text(json.dumps(payload), encoding="utf-8")
    return p


def test_real_failure_blocks(tmp_path: Path) -> None:
    """A genuine WCAG violation must not be retried."""
    report = _write_report(tmp_path, {
        "results": {
            "http://x.example/a/": [
                {"code": "WCAG2AAA.Principle1.Guideline1_1.1_1_1.H37",
                 "message": "Img element missing an alt attribute."},
            ],
        },
    })
    assert prf.main(["pa11y_retry_flakes.py", str(report)]) == 1


def test_flake_only_triggers_retry(tmp_path: Path) -> None:
    """If the only error is the navigation race, attempt a retry."""
    report = _write_report(tmp_path, {
        "results": {
            "http://x.example/a/": [
                {"code": "?",
                 "message": "Execution context was destroyed, "
                            "most likely because of a navigation."},
            ],
        },
    })
    with patch.object(prf, "_retry_urls", return_value=0) as mock_retry:
        rc = prf.main(["pa11y_retry_flakes.py", str(report)])
    assert rc == 0
    mock_retry.assert_called_once()
    (urls,), _ = mock_retry.call_args
    assert urls == ["http://x.example/a/"]


def test_flake_retry_failure_propagates(tmp_path: Path) -> None:
    """If the retry still fails, propagate nonzero exit."""
    report = _write_report(tmp_path, {
        "results": {
            "http://x.example/a/": [
                {"code": "?", "message": "Execution context was destroyed."},
            ],
        },
    })
    with patch.object(prf, "_retry_urls", return_value=1):
        assert prf.main(["pa11y_retry_flakes.py", str(report)]) == 1


def test_mixed_flake_and_real_fails_without_retry(tmp_path: Path) -> None:
    """If any URL has a real failure, no retry runs even if other URLs
    are flakes."""
    report = _write_report(tmp_path, {
        "results": {
            "http://x.example/a/": [
                {"code": "?", "message": "Execution context was destroyed."},
            ],
            "http://x.example/b/": [
                {"code": "WCAG2AAA.X",
                 "message": "Real WCAG violation"},
            ],
        },
    })
    with patch.object(prf, "_retry_urls") as mock_retry:
        rc = prf.main(["pa11y_retry_flakes.py", str(report)])
    assert rc == 1
    mock_retry.assert_not_called()


def test_no_failures_with_nonzero_pa11y_exit(tmp_path: Path) -> None:
    """pa11y-ci exited nonzero but reported no failed URLs — bail
    rather than spuriously passing."""
    report = _write_report(tmp_path, {"results": {}})
    assert prf.main(["pa11y_retry_flakes.py", str(report)]) == 1


def test_missing_report_bails(tmp_path: Path) -> None:
    assert prf.main(["pa11y_retry_flakes.py", str(tmp_path / "nope")]) == 2


def test_url_with_no_issues_is_ignored(tmp_path: Path) -> None:
    """URLs that passed shouldn't show up in either bucket."""
    report = _write_report(tmp_path, {
        "results": {
            "http://x.example/ok/": [],
            "http://x.example/flake/": [
                {"code": "?", "message": "Execution context was destroyed."},
            ],
        },
    })
    with patch.object(prf, "_retry_urls", return_value=0) as mock_retry:
        rc = prf.main(["pa11y_retry_flakes.py", str(report)])
    assert rc == 0
    (urls,), _ = mock_retry.call_args
    assert urls == ["http://x.example/flake/"]
