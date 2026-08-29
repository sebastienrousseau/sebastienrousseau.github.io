"""Detection rules of the URL-integrity gate."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tests" / "validation"))

import test_url_integrity as gate


def test_a_clean_url_passes():
    assert gate.offences("see https://en.wikipedia.org/wiki/Quantum_computing here") == []


def test_devanagari_in_a_url_fails():
    """andrea-de-santis became andrea-का-santis — a broken image."""
    out = gate.offences("https://cloudcdn.pro/stocks/images/andrea-का-santis-x.webp")
    assert len(out) == 1
    assert "non-ASCII" in out[0]


def test_a_translated_host_fails():
    assert gate.offences("https://em.wikipedia.org/wiki/X")[0].startswith("host rewritten")
    assert gate.offences("https://devblogs.microsvaak.com/x")[0].startswith("host rewritten")


def test_punycode_is_never_legitimate_here():
    assert gate.offences("https://xn--p2br8c.archive.org/x")


def test_a_linkedin_profile_is_not_an_offence():
    """linkedin.com/in/<profile> is a real path; a naive /in/ rule broke it."""
    assert gate.offences("https://www.linkedin.com/in/sebastienrousseau/") == []


def test_trailing_punctuation_is_not_part_of_the_url():
    assert gate.offences("see https://en.wikipedia.org/wiki/X.") == []


def test_the_allow_list_exempts_a_url():
    url = "https://example.test/café"
    assert gate.offences(url)
    gate.ALLOW = frozenset({url})
    try:
        assert gate.offences(url) == []
    finally:
        gate.ALLOW = frozenset()
