"""Frozen-exception model of the slug-derivable gate."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tests" / "validation"))

import test_slug_derivable as gate


def test_a_frozen_post_is_accepted():
    failures, stale = gate.evaluate({"ar": ["2018-01-01-old"]}, {"ar": {"2018-01-01-old"}})
    assert failures == []
    assert stale == []


def test_a_post_outside_the_frozen_set_fails():
    failures, stale = gate.evaluate({"ar": ["2018-01-01-new"]}, {"ar": {"2018-01-01-old"}})
    assert len(failures) == 1
    assert "2018-01-01-new" in failures[0]
    assert stale == ["ar/2018-01-01-old.md"]


def test_compensation_no_longer_hides_a_regression():
    """The hole in the old count model: one post breaks, another heals.

    Counting derivable posts per locale left the total level, so the gate
    passed. Naming the exceptions means both halves are reported.
    """
    current = {"ar": ["2018-01-01-broke"]}
    frozen = {"ar": {"2018-01-02-healed"}}
    failures, stale = gate.evaluate(current, frozen)
    assert any("2018-01-01-broke" in f for f in failures)
    assert stale == ["ar/2018-01-02-healed.md"]


def test_a_healed_entry_is_stale_and_must_be_removed():
    failures, stale = gate.evaluate({}, {"ar": {"2018-01-01-old"}})
    assert failures == []
    assert stale == ["ar/2018-01-01-old.md"]


def test_clean_tree_is_clean():
    assert gate.evaluate({}, {}) == ([], [])


def test_locales_are_independent():
    failures, _ = gate.evaluate({"ar": ["x"], "he": ["y"]}, {"ar": {"x"}})
    assert len(failures) == 1
    assert failures[0].startswith("he/y.md")
