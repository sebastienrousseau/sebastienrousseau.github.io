#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Weekly Search Console report, with an issue when impressions drop.

Run every Monday by ``.github/workflows/search-weekly.yml``. It calls
``searchAnalytics.query`` once (paged) for the trailing 28 days with
dimensions ``page`` and ``date``, then reports three windows from those
rows: the last 7 complete days, the 7 before them, and the 28 days. Rows
are grouped by locale (path prefix, ``en`` for the root) and by page;
``search_stats.py`` does the arithmetic.

Outputs, in ``--out-dir``:

* ``search-weekly.md``: impressions, clicks, CTR and average position per
  locale, the top 20 English pages with week-on-week change, and the alert
  section. Also appended to the run summary (``$GITHUB_STEP_SUMMARY``).
* ``search-weekly.csv``: the same figures for every locale and every page.

Alert: when English or any kept locale (``_data/seo/locale-indexing.json``)
loses 30% or more of its impressions week on week, ``--file-issue`` opens
or updates the ``search-alert`` issue (``search_alert.py``) with the 10
pages that lost the most.

Credentials: the service-account key JSON in ``GSC_SERVICE_ACCOUNT_JSON``.
When it is unset the script writes a one-line summary saying so and exits
0, so the schedule stays green until the secret exists. ``--fixture`` reads
a saved API response instead, for offline runs.

"Complete" days: Search Console's final data lags by about two days, so the
report ends ``LAG_DAYS`` before today (UTC) unless ``--end`` is given.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import sys
from pathlib import Path
from typing import Any, Protocol
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import _lang_registry as registry
import search_alert
import search_stats as ss
from _locale_indexing import indexed_codes

SITE = os.environ.get("GSC_SITE_URL") or "sc-domain:sebastienrousseau.com"
SCOPE = "https://www.googleapis.com/auth/webmasters.readonly"
API = "https://searchconsole.googleapis.com/webmasters/v3/sites/{site}/searchAnalytics/query"
ROW_LIMIT = 25000
LAG_DAYS = 3
TOP_PAGES = 20
TOP_LOSERS = 10
GSC_ENV = "GSC_SERVICE_ACCOUNT_JSON"
CSV_FIELDS = (
    "scope",
    "key",
    "locale",
    "kept",
    "impressions",
    "impressions_previous",
    "change",
    "clicks",
    "clicks_previous",
    "ctr",
    "position",
    "impressions_28d",
    "clicks_28d",
    "ctr_28d",
    "position_28d",
)


class Session(Protocol):
    def post(self, url: str, json: dict[str, Any]) -> Any:
        """POST ``json`` to ``url`` and return the response."""


def authorized_session(info_json: str) -> Any:
    """A ``requests`` session that signs calls with the service account."""
    from google.auth.transport.requests import AuthorizedSession
    from google.oauth2 import service_account

    creds = service_account.Credentials.from_service_account_info(
        json.loads(info_json), scopes=[SCOPE]
    )
    return AuthorizedSession(creds)


def fetch_rows(session: Session, site: str, start: dt.date, end: dt.date) -> list[dict[str, Any]]:
    """Every ``page``/``date`` row between ``start`` and ``end`` inclusive."""
    url = API.format(site=quote(site, safe=""))
    rows: list[dict[str, Any]] = []
    while True:
        resp = session.post(
            url,
            json={
                "startDate": start.isoformat(),
                "endDate": end.isoformat(),
                "dimensions": ["page", "date"],
                "type": "web",
                "dataState": "final",
                "rowLimit": ROW_LIMIT,
                "startRow": len(rows),
            },
        )
        resp.raise_for_status()
        batch = resp.json().get("rows", [])
        rows.extend(batch)
        if len(batch) < ROW_LIMIT:
            return rows


def default_end(today: dt.date) -> dt.date:
    return today - dt.timedelta(days=LAG_DAYS)


def locale_sets(codes: str | None, kept: str | None) -> tuple[set[str], set[str]]:
    """Active locale codes and kept (indexed) codes, overridable for tests."""

    def split(value: str) -> set[str]:
        return {c.strip() for c in value.split(",") if c.strip()}

    all_codes = split(codes) if codes else {lang.code for lang in registry.active()}
    kept_codes = split(kept) if kept else set(indexed_codes())
    return all_codes, kept_codes


# -- rendering -------------------------------------------------------------------


def pct(value: float | None) -> str:
    return "new" if value is None else f"{value:+.1%}"


def change_label(current: int, previous: int) -> str:
    """Week-on-week change; ``n/a`` when both weeks are empty."""
    return "n/a" if current == previous == 0 else pct(ss.change(current, previous))


def _totals(table: dict[str, ss.Totals], period: str) -> ss.Totals:
    return table.get(period) or ss.Totals()


def _locale_order(report: ss.Report, kept: set[str]) -> list[str]:
    codes = set(report.locales) | kept
    return sorted(codes, key=lambda c: (-ss.impressions(report.locales.get(c, {}), "current"), c))


def _locale_table(report: ss.Report, kept: set[str]) -> list[str]:
    lines = [
        "## By locale",
        "",
        "| Locale | Kept | Impressions | Last week | Change | Clicks | CTR | Position "
        + "| Impressions 28 d | Clicks 28 d | CTR 28 d | Position 28 d |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for code in _locale_order(report, kept):
        table = report.locales.get(code, {})
        cur, prev, t28 = (_totals(table, p) for p in ss.PERIODS)
        lines.append(
            f"| {code} | {'yes' if code in kept else 'no'} | {cur.impressions:,} "
            f"| {prev.impressions:,} | {change_label(cur.impressions, prev.impressions)} "
            f"| {cur.clicks:,} | {cur.ctr:.1%} | {cur.position:.1f} | {t28.impressions:,} "
            f"| {t28.clicks:,} | {t28.ctr:.1%} | {t28.position:.1f} |"
        )
    return lines


def _pages_table(report: ss.Report) -> list[str]:
    lines = [
        f"## Top {TOP_PAGES} English pages",
        "",
        "| Page | Impressions | Last week | Change | Clicks | CTR | Position |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for path in ss.top_pages(report, "en", TOP_PAGES):
        cur, prev = _totals(report.pages[path], "current"), _totals(report.pages[path], "previous")
        lines.append(
            f"| `{path}` | {cur.impressions:,} | {prev.impressions:,} "
            f"| {change_label(cur.impressions, prev.impressions)} | {cur.clicks:,} "
            f"| {cur.ctr:.1%} | {cur.position:.1f} |"
        )
    return lines


def _alert_section(report: ss.Report, alerts: list[str]) -> list[str]:
    if not alerts:
        return ["## Alerts", "", "No kept locale fell 30% or more week on week."]
    lines = ["## Alert: impressions fell 30% or more", ""]
    for code in alerts:
        table = report.locales[code]
        cur, prev = ss.impressions(table, "current"), ss.impressions(table, "previous")
        lines.append(f"- **{code}**: {cur:,} against {prev:,} ({pct(ss.change(cur, prev))})")
    lines += [
        "",
        f"### Pages that lost the most ({TOP_LOSERS})",
        "",
        "| Page | Impressions | Last week | Lost |",
        "| --- | ---: | ---: | ---: |",
    ]
    for path, cur, prev in ss.top_losers(report, alerts, TOP_LOSERS):
        lines.append(f"| `{path}` | {cur:,} | {prev:,} | {prev - cur:,} |")
    return lines


def render_markdown(report: ss.Report, kept: set[str], site: str) -> str:
    w = report.windows
    header = [
        "# Search Console weekly report",
        "",
        f"Property `{site}`. This week {w.current[0]} to {w.current[1]}; "
        f"last week {w.previous[0]} to {w.previous[1]}; "
        f"28 days {w.trailing[0]} to {w.trailing[1]}. "
        "CTR and position are impression-weighted over pages.",
    ]
    sections = [
        header,
        _locale_table(report, kept),
        _pages_table(report),
        _alert_section(report, ss.alert_locales(report, kept)),
    ]
    return "\n\n".join("\n".join(s) for s in sections) + "\n"


def _csv_row(
    scope: str, key: str, locale: str, kept: bool, table: dict[str, ss.Totals]
) -> list[Any]:
    cur, prev, t28 = (_totals(table, p) for p in ss.PERIODS)
    change = ss.change(cur.impressions, prev.impressions)
    return [
        scope,
        key,
        locale,
        "yes" if kept else "no",
        cur.impressions,
        prev.impressions,
        "" if change is None else f"{change:.4f}",
        cur.clicks,
        prev.clicks,
        f"{cur.ctr:.4f}",
        f"{cur.position:.2f}",
        t28.impressions,
        t28.clicks,
        f"{t28.ctr:.4f}",
        f"{t28.position:.2f}",
    ]


def write_csv(path: Path, report: ss.Report, kept: set[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        out = csv.writer(fh)
        out.writerow(CSV_FIELDS)
        for code in _locale_order(report, kept):
            out.writerow(_csv_row("locale", code, code, code in kept, report.locales.get(code, {})))
        for path_ in sorted(report.pages):
            loc = report.page_locale[path_]
            out.writerow(_csv_row("page", path_, loc, loc in kept, report.pages[path_]))


# -- orchestration ---------------------------------------------------------------


def _parse(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--site", default=SITE, help="Search Console property")
    parser.add_argument("--end", type=dt.date.fromisoformat, help="last day (default: today - 3)")
    parser.add_argument("--out-dir", type=Path, default=Path("search-report"))
    parser.add_argument("--summary", type=Path, default=os.environ.get("GITHUB_STEP_SUMMARY"))
    parser.add_argument("--fixture", type=Path, help="saved searchAnalytics.query response")
    parser.add_argument("--codes", help="comma-separated active locales (default: registry)")
    parser.add_argument("--kept", help="comma-separated kept locales (default: policy)")
    parser.add_argument("--file-issue", action="store_true", help="open/update search-alert")
    return parser.parse_args(argv)


def _summarise(path: Path | None, text: str) -> None:
    if path:
        with Path(path).open("a", encoding="utf-8") as fh:
            fh.write(text)


def load_rows(args: argparse.Namespace, windows: ss.Windows) -> list[dict[str, Any]] | None:
    """API rows (or fixture rows); None when there are no credentials."""
    if args.fixture:
        rows: list[dict[str, Any]] = json.loads(args.fixture.read_text(encoding="utf-8"))["rows"]
        return rows
    secret = os.environ.get(GSC_ENV, "").strip()
    if not secret:
        return None
    return fetch_rows(authorized_session(secret), args.site, *windows.trailing)


def file_issue(report: ss.Report, alerts: list[str], markdown: str) -> int:
    token, repo = os.environ.get("GITHUB_TOKEN"), os.environ.get("GITHUB_REPOSITORY")
    if not token or not repo:
        print(
            "search_weekly: --file-issue needs GITHUB_TOKEN and GITHUB_REPOSITORY", file=sys.stderr
        )
        return 1
    week = report.windows.current[1].isoformat()
    title = f"Search impressions fell 30% or more: {', '.join(alerts)} (week to {week})"
    outcome = search_alert.file_alert(search_alert.GitHub(token), repo, title, markdown, week)
    print(f"search_weekly: search-alert issue {outcome}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = _parse(argv)
    codes, kept = locale_sets(args.codes, args.kept)
    end = args.end or default_end(dt.datetime.now(dt.UTC).date())
    windows = ss.Windows.ending(end)
    rows = load_rows(args, windows)
    if rows is None:
        note = (
            f"Search Console report skipped: {GSC_ENV} is not set, so there is nothing to query.\n"
        )
        print(note, end="")
        _summarise(args.summary, note)
        return 0
    report = ss.aggregate(rows, windows, codes)
    markdown = render_markdown(report, kept, args.site)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "search-weekly.md").write_text(markdown, encoding="utf-8")
    write_csv(args.out_dir / "search-weekly.csv", report, kept)
    _summarise(args.summary, markdown)
    alerts = ss.alert_locales(report, kept)
    print(f"search_weekly: {len(rows)} rows, alerts: {', '.join(alerts) or 'none'}")
    if args.file_issue and alerts:
        return file_issue(report, alerts, markdown)
    return 0


if __name__ == "__main__":
    sys.exit(main())
