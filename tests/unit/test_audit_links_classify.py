# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""A bot block is not link rot.

The 2026-11-01 audit (#510) reported 10 broken links. Nine answered 401/403/
429 or dropped the connection: the target refusing a datacentre client, which
says nothing about the link. Only the 404 was rot. Those responses are now
reported as unverifiable, apart from the broken list the workflow counts.
"""

from __future__ import annotations

import http.client
import sys
import urllib.error
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "seo_and_audit"))

import audit_links

OK, UNVERIFIABLE, BROKEN = audit_links.OK, audit_links.UNVERIFIABLE, audit_links.BROKEN


@pytest.mark.parametrize("code", [200, 204, 301, 308])
def test_success_and_redirects_are_ok(code):
    assert audit_links.classify(code) == OK


@pytest.mark.parametrize("code", [401, 403, 429])
def test_bot_block_statuses_are_unverifiable(code):
    assert audit_links.classify(code) == UNVERIFIABLE


@pytest.mark.parametrize("code", [400, 404, 410, 500, 502, 503, 526])
def test_rot_and_server_errors_stay_broken(code):
    assert audit_links.classify(code) == BROKEN


@pytest.mark.parametrize(
    "code",
    ["ERR RemoteDisconnected", "ERR ConnectionResetError", "ERR URLError(ConnectionResetError)"],
)
def test_connection_reset_is_unverifiable(code):
    assert audit_links.classify(code) == UNVERIFIABLE


@pytest.mark.parametrize(
    "code",
    ["ERR URLError(gaierror)", "ERR TimeoutError", "ERR InvalidURL", "ERR URLError"],
)
def test_dns_and_other_failures_stay_broken(code):
    assert audit_links.classify(code) == BROKEN


def _raising(exc):
    def fake(_url, _method):
        raise exc

    return fake


def test_dns_failure_is_labelled_by_its_reason(monkeypatch):
    import socket

    exc = urllib.error.URLError(socket.gaierror(8, "nodename nor servname provided"))
    monkeypatch.setattr(audit_links, "_fetch", _raising(exc))
    _url, code = audit_links.check_external("https://nx.example.test/")
    assert code == "ERR URLError(gaierror)"
    assert audit_links.classify(code) == BROKEN


def test_remote_disconnect_is_unverifiable_end_to_end(monkeypatch):
    exc = http.client.RemoteDisconnected("Remote end closed connection")
    monkeypatch.setattr(audit_links, "_fetch", _raising(exc))
    _url, code = audit_links.check_external("https://pqcc.org/international-pqc-requirements/")
    assert audit_links.classify(code) == UNVERIFIABLE


@pytest.mark.parametrize(
    "url",
    [
        "https://chatgpt.com/?q=Summarise+this+page",
        "https://claude.ai/new?q=Summarise+this+page",
        "https://www.perplexity.ai/search/new?q=Summarise+this+page",
    ],
)
def test_ai_prompt_links_are_share_endpoints(url):
    assert audit_links.is_share_endpoint(url)


def _fake_results(monkeypatch, results):
    monkeypatch.setattr(audit_links, "check_external", lambda u: (u, results[u]))


def test_report_counts_only_broken(monkeypatch, capsys):
    results = {
        "https://a.test/": 200,
        "https://b.test/": 403,
        "https://c.test/": 429,
        "https://d.test/": 404,
        "https://e.test/": "ERR RemoteDisconnected",
    }
    _fake_results(monkeypatch, results)
    broken = audit_links._audit_external(sorted(results))
    out = capsys.readouterr().out
    assert broken == [("https://d.test/", 404)]
    # The workflow counts lines matching '^  \[' as broken; only one may match.
    counted = [ln for ln in out.splitlines() if ln.startswith("  [")]
    assert counted == ["  [404] https://d.test/"]
    assert "3 unverifiable (bot-blocked)" in out
    assert "  ? [403] https://b.test/" in out
    assert "  ? [ERR RemoteDisconnected] https://e.test/" in out
