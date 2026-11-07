# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Offline tests for ``scripts/seo_and_audit/search_stats.py``: windows,
grouping by locale and page, and the 30% drop rule, against a fixture
``searchAnalytics.query`` response."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import pytest
import search_stats as ss

FIXTURE = Path(__file__).parent / "fixtures" / "search_weekly" / "searchanalytics.json"
CODES = frozenset({"en", "fr", "de", "nl"})
KEPT = frozenset({"en", "fr", "de"})
END = dt.date(2026, 11, 1)


@pytest.fixture
def report() -> ss.Report:
    rows = json.loads(FIXTURE.read_text(encoding="utf-8"))["rows"]
    return ss.aggregate(rows, ss.Windows.ending(END), CODES)


def test_windows_are_seven_seven_and_twenty_eight_days() -> None:
    w = ss.Windows.ending(END)
    assert w.current == (dt.date(2026, 10, 26), END)
    assert w.previous == (dt.date(2026, 10, 19), dt.date(2026, 10, 25))
    assert w.trailing == (dt.date(2026, 10, 5), END)
    assert w.periods(dt.date(2026, 10, 25)) == ("previous", "trailing")
    assert w.periods(dt.date(2026, 10, 26)) == ("current", "trailing")
    assert w.periods(dt.date(2026, 10, 4)) == ()


def test_locale_comes_from_the_path_prefix() -> None:
    assert ss.locale_of("https://sebastienrousseau.com/", CODES) == "en"
    assert ss.locale_of("https://sebastienrousseau.com/fr/x/", CODES) == "fr"
    assert ss.locale_of("https://sebastienrousseau.com/fr", CODES) == "fr"
    assert ss.locale_of("https://sebastienrousseau.com/frog/", CODES) == "en"
    assert ss.path_of("https://sebastienrousseau.com/a/b/?q=1") == "/a/b/"


def test_grouping_by_locale(report: ss.Report) -> None:
    en = report.locales["en"]
    assert (en["current"].impressions, en["previous"].impressions) == (700, 1000)
    assert (en["current"].clicks, en["previous"].clicks) == (32, 50)
    assert en["trailing"].impressions == 1750
    assert report.locales["fr"]["current"].impressions == 150
    assert report.locales["nl"]["previous"].impressions == 100
    assert "previous" not in report.locales["de"]


def test_grouping_by_page(report: ss.Report) -> None:
    home = report.pages["/"]
    assert (home["current"].impressions, home["previous"].impressions) == (500, 600)
    assert report.page_locale["/fr/"] == "fr"
    assert report.page_locale["/iso20022-mcp/"] == "en"


def test_ctr_and_position_are_impression_weighted(report: ss.Report) -> None:
    cur = report.locales["en"]["current"]
    assert cur.ctr == pytest.approx(32 / 700)
    assert cur.position == pytest.approx((5.0 * 500 + 11.0 * 200) / 700)
    empty = ss.Totals()
    assert (empty.ctr, empty.position) == (0.0, 0.0)


@pytest.mark.parametrize(
    ("current", "previous", "alert"),
    [
        (700, 1000, True),  # exactly 30%: "30% or more"
        (701, 1000, False),  # 29.9%
        (699, 1000, True),
        (0, 1000, True),
        (7, 10, True),
        (1000, 1000, False),
        (5, 0, False),  # no previous impressions: nothing to fall from
        (0, 0, False),
    ],
)
def test_thirty_percent_rule(current: int, previous: int, alert: bool) -> None:
    assert ss.dropped(current, previous) is alert


def test_alerts_only_for_kept_locales(report: ss.Report) -> None:
    # en falls exactly 30%; nl falls 90% but is not kept; de had no previous week.
    assert ss.alert_locales(report, KEPT) == ["en"]


def test_zero_impression_previous_week_never_alerts(report: ss.Report) -> None:
    assert ss.change(40, 0) is None
    assert "de" not in ss.alert_locales(report, KEPT)


def test_change_is_relative() -> None:
    assert ss.change(700, 1000) == pytest.approx(-0.3)
    assert ss.change(150, 100) == pytest.approx(0.5)


def test_top_losers_are_ranked_by_lost_impressions(report: ss.Report) -> None:
    losers = ss.top_losers(report, ["en"], 10)
    assert [p for p, _, _ in losers] == ["/iso20022-mcp/", "/"]
    assert losers[0] == ("/iso20022-mcp/", 200, 400)
    assert ss.top_losers(report, ["en"], 1) == [("/iso20022-mcp/", 200, 400)]
    assert ss.top_losers(report, ["fr"], 10) == []


def test_top_pages_by_current_impressions(report: ss.Report) -> None:
    assert ss.top_pages(report, "en", 20) == ["/", "/iso20022-mcp/", "/about/"]
    assert ss.top_pages(report, "en", 1) == ["/"]


def test_rows_outside_the_windows_are_ignored() -> None:
    row = {"keys": ["https://sebastienrousseau.com/", "2026-09-01"], "clicks": 9, "impressions": 99}
    report = ss.aggregate([row], ss.Windows.ending(END), CODES)
    assert not report.locales and not report.pages
