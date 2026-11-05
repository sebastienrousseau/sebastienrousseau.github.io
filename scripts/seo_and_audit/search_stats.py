# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Pure aggregation for the weekly Search Console report.

``search_weekly.py`` fetches ``searchAnalytics.query`` rows (dimensions
``page`` and ``date``) and hands them here. Nothing in this module does I/O,
so the grouping and the alert rule are tested offline against a fixture.

* Windows: the 7 days ending on the report date (``current``), the 7 before
  them (``previous``) and the 28 ending on the report date (``trailing``).
* Grouping: by locale (the first path segment when it is an active locale
  code, ``en`` otherwise) and by page path.
* CTR and average position are impression-weighted over the rows summed,
  which is how Search Console itself combines them.
* Alert rule: a locale has dropped when its impressions this week are 30% or
  more below last week's. A locale with no impressions last week cannot
  drop.
"""

from __future__ import annotations

import datetime as dt
from collections import defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlsplit

PERIODS = ("current", "previous", "trailing")
# 30% or more, as integers: current <= previous * (1 - 0.30). Integer maths
# keeps the boundary exact; a float ratio would put 700/1000 on either side
# of 0.7 depending on rounding.
DROP_NUM, DROP_DEN = 7, 10


@dataclass
class Totals:
    """Summed clicks and impressions, with impression-weighted position."""

    clicks: int = 0
    impressions: int = 0
    _position_sum: float = 0.0

    def add(self, clicks: int, impressions: int, position: float) -> None:
        self.clicks += clicks
        self.impressions += impressions
        self._position_sum += position * impressions

    @property
    def ctr(self) -> float:
        return self.clicks / self.impressions if self.impressions else 0.0

    @property
    def position(self) -> float:
        return self._position_sum / self.impressions if self.impressions else 0.0


@dataclass(frozen=True)
class Windows:
    """Inclusive ``(start, end)`` date ranges of the three periods."""

    current: tuple[dt.date, dt.date]
    previous: tuple[dt.date, dt.date]
    trailing: tuple[dt.date, dt.date]

    @classmethod
    def ending(cls, end: dt.date) -> Windows:
        day = dt.timedelta(days=1)
        return cls(
            current=(end - 6 * day, end),
            previous=(end - 13 * day, end - 7 * day),
            trailing=(end - 27 * day, end),
        )

    def periods(self, day: dt.date) -> tuple[str, ...]:
        """The period names whose range contains ``day``."""
        return tuple(name for name in PERIODS if _within(day, getattr(self, name)))


def _within(day: dt.date, span: tuple[dt.date, dt.date]) -> bool:
    return span[0] <= day <= span[1]


def _period_table() -> defaultdict[str, dict[str, Totals]]:
    return defaultdict(dict)


@dataclass
class Report:
    """Totals per locale and per page, each keyed by period name."""

    windows: Windows
    locales: defaultdict[str, dict[str, Totals]] = field(default_factory=_period_table)
    pages: defaultdict[str, dict[str, Totals]] = field(default_factory=_period_table)
    page_locale: dict[str, str] = field(default_factory=dict)


def path_of(url: str) -> str:
    return urlsplit(url).path or "/"


def locale_of(url: str, codes: Iterable[str]) -> str:
    """``fr`` for ``/fr/...``; ``en`` for the root and anything else."""
    first = path_of(url).strip("/").split("/", 1)[0]
    return first if first and first != "en" and first in codes else "en"


def _add(table: dict[str, Totals], periods: tuple[str, ...], row: Mapping[str, Any]) -> None:
    for name in periods:
        table.setdefault(name, Totals()).add(
            int(row.get("clicks", 0)), int(row.get("impressions", 0)), float(row.get("position", 0))
        )


def aggregate(rows: Iterable[Mapping[str, Any]], windows: Windows, codes: Iterable[str]) -> Report:
    """Group ``page``/``date`` rows into per-locale and per-page totals."""
    codes = frozenset(codes)
    report = Report(windows)
    for row in rows:
        url, day = row["keys"][0], dt.date.fromisoformat(row["keys"][1])
        periods = windows.periods(day)
        if not periods:
            continue
        path, locale = path_of(url), locale_of(url, codes)
        report.page_locale[path] = locale
        _add(report.locales[locale], periods, row)
        _add(report.pages[path], periods, row)
    return report


def impressions(table: Mapping[str, Totals], period: str) -> int:
    totals = table.get(period)
    return totals.impressions if totals else 0


def dropped(current: int, previous: int) -> bool:
    """True when ``current`` is 30% or more below a non-zero ``previous``."""
    return previous > 0 and current * DROP_DEN <= previous * DROP_NUM


def change(current: int, previous: int) -> float | None:
    """Relative week-on-week change; None when there was nothing last week."""
    return (current - previous) / previous if previous else None


def alert_locales(report: Report, kept: Iterable[str]) -> list[str]:
    """Kept locales whose impressions fell 30% or more week on week."""
    return [
        code
        for code in sorted(kept)
        if dropped(
            impressions(report.locales.get(code, {}), "current"),
            impressions(report.locales.get(code, {}), "previous"),
        )
    ]


def top_losers(report: Report, locales: Iterable[str], n: int) -> list[tuple[str, int, int]]:
    """``(path, current, previous)`` of the ``n`` pages that lost the most
    impressions in ``locales``, largest loss first."""
    wanted = set(locales)
    rows = [
        (path, impressions(table, "current"), impressions(table, "previous"))
        for path, table in report.pages.items()
        if report.page_locale[path] in wanted
    ]
    losing = [r for r in rows if r[2] > r[1]]
    losing.sort(key=lambda r: (r[1] - r[2], r[0]))
    return losing[:n]


def top_pages(report: Report, locale: str, n: int) -> list[str]:
    """The ``n`` pages of ``locale`` with most impressions this week."""
    paths = [p for p, loc in report.page_locale.items() if loc == locale]
    paths.sort(
        key=lambda p: (
            -impressions(report.pages[p], "current"),
            -impressions(report.pages[p], "previous"),
            p,
        )
    )
    return paths[:n]
