"""`update_last_modified_date` is what made the rebuild non-identical.

A page with a `last_reviewed` date in frontmatter gets that date. A page
without one — the category, topic, case-study and speaking listings — fell
back to `date.today()`, so two builds either side of midnight UTC stamped
different days and the byte-identical diff failed (CI run 33281416595).

The fallback still exists; it is now read through the build clock, so a
build that pins SOURCE_DATE_EPOCH stamps the same date whenever it runs.
This function had no test at all before.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field

import pytest
from postbuild_transforms import PUBLIC, update_last_modified_date

META = '<meta itemprop="dateModified" content="1970-01-01" id="last-modified" />'
EPOCH = "1750000000"  # 2025-06-15T15:06:40Z


@dataclass
class _Ctx:
    last_reviewed_index: dict[str, str] = field(default_factory=dict)
    translated_per_lang: dict[str, object] = field(default_factory=dict)


def _stamp(html: str, rel: str, ctx: _Ctx) -> str:
    return update_last_modified_date(html, PUBLIC / rel, ctx)


def test_frontmatter_date_wins(monkeypatch: pytest.MonkeyPatch) -> None:
    """An article with a real reviewed date never touched the clock."""
    monkeypatch.delenv("SOURCE_DATE_EPOCH", raising=False)
    out = _stamp(META, "some-article/index.html", _Ctx({"some-article": "2024-03-01"}))
    assert 'content="2024-03-01"' in out


def test_listing_without_a_reviewed_date_uses_the_build_clock(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The regression path: no frontmatter date, so the clock decides."""
    monkeypatch.setenv("SOURCE_DATE_EPOCH", EPOCH)
    out = _stamp(META, "categories/index.html", _Ctx())
    assert 'content="2025-06-15"' in out


def test_two_builds_at_different_times_agree_when_pinned(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The failure shape, reproduced and then fixed.

    Unpinned, a listing page stamped either side of midnight differs — that
    is exactly what broke the byte-identical diff. Pinned, it does not.
    """
    before = dt.datetime(2026, 8, 29, 23, 37, 39, tzinfo=dt.UTC)
    after = dt.datetime(2026, 8, 30, 0, 9, 41, tzinfo=dt.UTC)

    class _Clock(dt.datetime):
        moment = before

        @classmethod
        def now(cls, tz: dt.tzinfo | None = None) -> dt.datetime:
            return cls.moment

    monkeypatch.setattr("_build_clock.datetime", _Clock)

    monkeypatch.delenv("SOURCE_DATE_EPOCH", raising=False)
    _Clock.moment = before
    first = _stamp(META, "categories/index.html", _Ctx())
    _Clock.moment = after
    second = _stamp(META, "categories/index.html", _Ctx())
    assert first != second, "unpinned, the two builds disagree — the original bug"
    assert 'content="2026-08-29"' in first
    assert 'content="2026-08-30"' in second

    monkeypatch.setenv("SOURCE_DATE_EPOCH", EPOCH)
    _Clock.moment = before
    first_pinned = _stamp(META, "categories/index.html", _Ctx())
    _Clock.moment = after
    second_pinned = _stamp(META, "categories/index.html", _Ctx())
    assert first_pinned == second_pinned
    assert 'content="2025-06-15"' in first_pinned
