"""Frozen-page model of the localised-title gate."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tests" / "validation"))

import test_localised_titles as gate


def test_a_frozen_page_is_accepted():
    failures, stale = gate.evaluate({"ar/x/index.html": "Articles"}, {"ar/x/index.html"})
    assert failures == []
    assert stale == []


def test_a_new_english_title_fails():
    failures, stale = gate.evaluate({"fr/new/index.html": "Articles"}, set())
    assert len(failures) == 1
    assert "fr/new/index.html" in failures[0]
    assert "Articles" in failures[0]
    assert stale == []


def test_a_translated_page_must_leave_the_frozen_set():
    """Otherwise the backlog never shrinks and stale entries accumulate."""
    failures, stale = gate.evaluate({}, {"ar/x/index.html"})
    assert failures == []
    assert stale == ["ar/x/index.html"]


def test_a_clean_site_is_clean():
    assert gate.evaluate({}, set()) == ([], [])


def test_offenders_are_reported_in_a_stable_order():
    failures, _ = gate.evaluate({"z/index.html": "Articles", "a/index.html": "Articles"}, set())
    assert failures[0].startswith("a/index.html")


def test_a_template_whose_translation_is_identical_is_not_an_offence():
    """ "Articles" is the correct French word.

    Matching an English title is not proof of being untranslated, and fr
    listing pages were reported as offenders for using the right word.
    """
    assert gate._is_template("Articles")
    assert gate._is_template("Articles — 2018")
    assert gate._is_template("Research — Articles by topic")
    assert gate._is_template("Applied AI — Editorial pillar")


def test_a_title_the_pass_does_not_recognise_is_never_excused():
    """The narrow exemption matters: excusing every unrecognised title would
    quietly pardon the locale home pages, which really are English."""
    assert not gate._is_template("Sebastien Rousseau: AI, Payments & Quantum Cryptography")
    assert not gate._is_template("Topics — Sebastien Rousseau")
    assert not gate._is_template("Rust & Open Source — Sebastien Rousseau")
