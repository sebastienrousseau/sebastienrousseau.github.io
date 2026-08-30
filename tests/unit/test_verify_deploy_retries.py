# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""A post-deploy probe must not race the CDN.

`verify_deploy` runs immediately after the deploy step. GitHub Pages answers
200 with the PREVIOUS build for a short window, so a single fetch can assert
against content that is already superseded. That is not hypothetical: this
gate failed `main` with

    ::error::home page has no <meta name="description">

while https://sebastienrousseau.com was serving exactly such a tag.

Retrying turns the race into a real signal — a genuine regression fails every
attempt, a propagation lag resolves on a later one. These tests pin both
directions, plus the property that a clean first attempt costs no delay.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "seo_and_audit"))

import verify_deploy as vd


def _patch(monkeypatch, sequences, sleeps):
    """Drive main() with scripted per-attempt outcomes and record sleeps."""
    monkeypatch.setattr(vd, "advertised_paths", lambda base: set())
    monkeypatch.setattr(vd, "check_paths", lambda base, paths: [])
    monkeypatch.setattr(vd, "check_csp", lambda base: [])
    state = {"n": 0}

    def home(base):
        i = min(state["n"], len(sequences) - 1)
        state["n"] += 1
        return list(sequences[i])

    monkeypatch.setattr(vd, "check_home_description", home)
    monkeypatch.setattr(vd.time, "sleep", lambda s: sleeps.append(s))
    return state


def test_transient_failure_then_success_is_not_a_failure(monkeypatch):
    """The stale-build window: attempt 1 sees the old page, attempt 2 the new."""
    sleeps: list[int] = []
    state = _patch(monkeypatch, [['home page has no <meta name="description">'], []], sleeps)
    rc = vd.main(["--base", "https://example.com", "--retries", "3", "--retry-delay", "1"])
    assert rc == 0, "a problem that clears on retry must not fail the deploy"
    assert state["n"] == 2, "should have stopped as soon as it was clean"
    assert sleeps == [1], f"exactly one backoff expected, got {sleeps}"


def test_persistent_failure_still_fails(monkeypatch):
    """The guarantee retrying must not weaken: a real regression fails."""
    sleeps: list[int] = []
    state = _patch(monkeypatch, [['home page has no <meta name="description">']], sleeps)
    rc = vd.main(["--base", "https://example.com", "--retries", "3", "--retry-delay", "1"])
    assert rc == 1, "a problem present on every attempt must fail"
    assert state["n"] == 3, "should have used every attempt before giving up"
    assert sleeps == [1, 1], f"backoff between attempts only, got {sleeps}"


def test_clean_first_attempt_costs_no_delay(monkeypatch):
    """The common case must not add minutes to every deploy."""
    sleeps: list[int] = []
    state = _patch(monkeypatch, [[]], sleeps)
    rc = vd.main(["--base", "https://example.com", "--retries", "5", "--retry-delay", "20"])
    assert rc == 0
    assert state["n"] == 1
    assert sleeps == [], "a clean run must not sleep"
