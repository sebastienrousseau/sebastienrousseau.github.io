"""The build clock is what makes a rebuild byte-identical.

The `Reproducible build` CI job builds twice and diffs. It failed once, on
run 33281416595, which built from 23:37:39Z to 00:09:41Z — across midnight.
Every page that stamps today's date differed. The same branch had passed the
same job twice that day; only the hour had changed.

These tests fix the wall clock as a variable: with SOURCE_DATE_EPOCH set,
the date a build stamps must not depend on when the build runs.
"""

from __future__ import annotations

import datetime as dt

import pytest
from _build_clock import build_now, build_today, build_today_iso

# 2025-06-15T15:06:40Z — an arbitrary fixed instant.
EPOCH = "1750000000"


def test_unset_uses_the_wall_clock(monkeypatch: pytest.MonkeyPatch) -> None:
    """A normal build is unaffected: no env var, no behaviour change."""
    monkeypatch.delenv("SOURCE_DATE_EPOCH", raising=False)
    assert build_today() == dt.date.today()


def test_set_pins_the_date(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SOURCE_DATE_EPOCH", EPOCH)
    assert build_today_iso() == "2025-06-15"
    assert build_now() == dt.datetime(2025, 6, 15, 15, 6, 40, tzinfo=dt.UTC)


def test_empty_value_falls_back(monkeypatch: pytest.MonkeyPatch) -> None:
    """An empty var is 'unset', not 'malformed' — CI can export a blank."""
    monkeypatch.setenv("SOURCE_DATE_EPOCH", "")
    assert build_today() == dt.date.today()


@pytest.mark.parametrize("bad", ["not-a-number", "2026-08-30", "1e9", "9" * 40])
def test_malformed_raises(monkeypatch: pytest.MonkeyPatch, bad: str) -> None:
    """A typo in CI must fail loudly, not silently restore the flake."""
    monkeypatch.setenv("SOURCE_DATE_EPOCH", bad)
    with pytest.raises(ValueError, match="SOURCE_DATE_EPOCH"):
        build_today()


def test_pinned_date_survives_a_midnight_crossing(monkeypatch: pytest.MonkeyPatch) -> None:
    """The regression itself.

    Two reads of the clock either side of midnight — the exact shape of the
    CI failure — must agree when the epoch is pinned. Without the pin they
    are two different days, which is what broke the byte-identical diff.
    """
    before = dt.datetime(2026, 8, 29, 23, 37, 39, tzinfo=dt.UTC)
    after = dt.datetime(2026, 8, 30, 0, 9, 41, tzinfo=dt.UTC)
    assert before.date() != after.date(), "the two builds really were on different days"

    class _Clock(dt.datetime):
        moment = before

        @classmethod
        def now(cls, tz: dt.tzinfo | None = None) -> dt.datetime:
            return cls.moment

    monkeypatch.setattr("_build_clock.datetime", _Clock)

    monkeypatch.delenv("SOURCE_DATE_EPOCH", raising=False)
    _Clock.moment = before
    unpinned_first = build_today()
    _Clock.moment = after
    unpinned_second = build_today()
    assert unpinned_first != unpinned_second, "wall clock differs across midnight"

    monkeypatch.setenv("SOURCE_DATE_EPOCH", EPOCH)
    _Clock.moment = before
    pinned_first = build_today()
    _Clock.moment = after
    pinned_second = build_today()
    assert pinned_first == pinned_second == dt.date(2025, 6, 15)
