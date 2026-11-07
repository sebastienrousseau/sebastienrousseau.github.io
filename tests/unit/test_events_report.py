# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Unit tests for scripts/seo_and_audit/events_report.py."""

from __future__ import annotations

import json
from typing import Any
from urllib.error import URLError

import pytest

from scripts.seo_and_audit import events_report


class _FakeResp:
    def __init__(self, payload: dict[str, Any]) -> None:
        self._raw = json.dumps(payload).encode("utf-8")

    def read(self) -> bytes:
        return self._raw

    def __enter__(self) -> _FakeResp:
        return self

    def __exit__(self, *args: object) -> None:
        return None


def test_run_sql_query_rejects_missing_credentials() -> None:
    with pytest.raises(ValueError, match="CLOUDFLARE_ACCOUNT_ID"):
        events_report.run_sql_query("", "tok", "SELECT 1")
    with pytest.raises(ValueError, match="CLOUDFLARE_API_TOKEN"):
        events_report.run_sql_query("acc", "", "SELECT 1")


def test_run_sql_query_parses_data_rows(monkeypatch: pytest.MonkeyPatch) -> None:
    def _fake_urlopen(req: Any, timeout: int = 20) -> _FakeResp:
        assert "acc123" in req.full_url
        assert req.headers["Authorization"] == "Bearer tok456"
        return _FakeResp({"data": [{"event_name": "copy_config", "total_events": 12}]})

    monkeypatch.setattr(events_report.urllib.request, "urlopen", _fake_urlopen)
    rows = events_report.run_sql_query("acc123", "tok456", "SELECT 1")
    assert rows == [{"event_name": "copy_config", "total_events": 12}]


def test_format_report_handles_empty_and_populated_rows() -> None:
    empty_txt = events_report.format_report([], [], [], 7)
    assert "No events recorded in window." in empty_txt
    assert "No page-level events recorded in window." in empty_txt
    assert "No Core Web Vitals samples recorded in window." in empty_txt

    pop_txt = events_report.format_report(
        [{"event_name": "copy_config", "total_events": 5}],
        [
            {
                "event_name": "copy_config",
                "page_path": "/iso20022-mcp/",
                "event_key": "claude-desktop",
                "total_events": 5,
            }
        ],
        [{"vital_name": "vital_lcp", "rating": "good", "samples": 10, "p75_value": 1240.0}],
        7,
    )
    assert "- copy_config: 5" in pop_txt
    assert "- /iso20022-mcp/ :: copy_config [claude-desktop]: 5" in pop_txt
    assert "- vital_lcp (good): p75=1240.0 (n=10)" in pop_txt


def test_main_missing_env_returns_1(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CLOUDFLARE_ACCOUNT_ID", raising=False)
    monkeypatch.delenv("CLOUDFLARE_API_TOKEN", raising=False)
    assert events_report.main(["--days", "7"]) == 1


def test_main_success_and_error(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("CLOUDFLARE_ACCOUNT_ID", "acc123")
    monkeypatch.setenv("CLOUDFLARE_API_TOKEN", "tok456")
    monkeypatch.setattr(
        events_report,
        "run_sql_query",
        lambda acc, tok, sql: [{"event_name": "cta_click", "total_events": 3}],
    )
    assert events_report.main(["--days", "14"]) == 0
    out = capsys.readouterr().out
    assert "Analytics Engine Report (last 14 days)" in out

    def _fail(acc: str, tok: str, sql: str) -> list[dict[str, Any]]:
        raise URLError("network down")

    monkeypatch.setattr(events_report, "run_sql_query", _fail)
    assert events_report.main(["--days", "7"]) == 1
