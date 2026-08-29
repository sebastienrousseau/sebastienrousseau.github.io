"""A 4xx from HEAD is a question, not an answer.

Plenty of servers answer HEAD with 4xx and GET with 200 — csrc.nist.gov and
gleif.org both do. Reporting those as broken is how a link checker loses the
reader's trust, and it hid the real dead links among false ones.
"""

from __future__ import annotations

import sys
import urllib.error
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "seo_and_audit"))

import audit_links


def _stub(monkeypatch, behaviour):
    calls = []

    def fake(url, method):
        calls.append(method)
        result = behaviour(method)
        if isinstance(result, int) and result >= 400:
            raise urllib.error.HTTPError(url, result, "err", {}, None)
        return url, result

    monkeypatch.setattr(audit_links, "_fetch", fake)
    return calls


def test_head_405_is_retried_with_get(monkeypatch):
    calls = _stub(monkeypatch, lambda m: 200 if m == "GET" else 405)
    assert audit_links.check_external("https://example.test/x") == ("https://example.test/x", 200)
    assert calls == ["HEAD", "GET"]


def test_head_403_is_retried_with_get(monkeypatch):
    calls = _stub(monkeypatch, lambda m: 200 if m == "GET" else 403)
    _url, status = audit_links.check_external("https://example.test/x")
    assert status == 200
    assert calls == ["HEAD", "GET"]


def test_a_genuinely_dead_url_stays_dead(monkeypatch):
    """The retry must not paper over a real 404."""
    calls = _stub(monkeypatch, lambda _m: 404)
    _url, status = audit_links.check_external("https://example.test/gone")
    assert status == 404
    assert calls == ["HEAD", "GET"]


def test_a_working_head_is_not_retried(monkeypatch):
    calls = _stub(monkeypatch, lambda _m: 200)
    _url, status = audit_links.check_external("https://example.test/x")
    assert status == 200
    assert calls == ["HEAD"]


def test_a_5xx_is_not_retried(monkeypatch):
    """Only a 4xx suggests the method is the problem; a 5xx is the server."""
    calls = _stub(monkeypatch, lambda _m: 503)
    _url, status = audit_links.check_external("https://example.test/x")
    assert status == 503
    assert calls == ["HEAD"]
