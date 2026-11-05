#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Query Cloudflare Analytics Engine SQL API for weekly conversion and Core Web Vitals counts.

Requires environment variables:
  CLOUDFLARE_ACCOUNT_ID - Cloudflare account identifier
  CLOUDFLARE_API_TOKEN  - API token with Account Analytics Read permission
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any

DATASET = "sebastien_pageviews"
API_TEMPLATE = "https://api.cloudflare.com/client/v4/accounts/{account_id}/analytics_engine/sql"

EVENTS_BY_NAME_SQL = """
SELECT
    blob1 AS event_name,
    SUM(_sample_interval) AS total_events
FROM sebastien_pageviews
WHERE timestamp >= NOW() - INTERVAL '{days}' DAY
  AND blob1 != ''
GROUP BY event_name
ORDER BY total_events DESC
"""

EVENTS_BY_PAGE_SQL = """
SELECT
    blob1 AS event_name,
    blob2 AS page_path,
    blob3 AS event_key,
    SUM(_sample_interval) AS total_events
FROM sebastien_pageviews
WHERE timestamp >= NOW() - INTERVAL '{days}' DAY
  AND blob1 != ''
GROUP BY event_name, page_path, event_key
ORDER BY total_events DESC
LIMIT 50
"""

VITALS_SQL = """
SELECT
    blob1 AS vital_name,
    blob3 AS rating,
    COUNT() AS samples,
     quantileWeighted(0.75)(double1, _sample_interval) AS p75_value
FROM sebastien_pageviews
WHERE timestamp >= NOW() - INTERVAL '{days}' DAY
  AND blob1 IN ('vital_lcp', 'vital_inp', 'vital_cls')
GROUP BY vital_name, rating
ORDER BY vital_name ASC, rating ASC
"""


def run_sql_query(
    account_id: str,
    api_token: str,
    sql: str,
    timeout: int = 20,
) -> list[dict[str, Any]]:
    """Execute a SQL query against Cloudflare Analytics Engine and return rows."""
    if not account_id or not api_token:
        raise ValueError("CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN must be set")
    url = API_TEMPLATE.format(account_id=account_id.strip())
    req = urllib.request.Request(
        url,
        data=sql.strip().encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_token.strip()}",
            "Content-Type": "text/plain; charset=utf-8",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8", errors="replace")
    parsed = json.loads(body)
    rows = parsed.get("data", [])
    return rows if isinstance(rows, list) else []


def format_report(
    by_event: list[dict[str, Any]],
    by_page: list[dict[str, Any]],
    vitals: list[dict[str, Any]],
    days: int,
) -> str:
    """Format the queried rows into a human-readable markdown/text report."""
    lines: list[str] = [f"# Analytics Engine Report (last {days} days)", ""]
    lines.append("## Counts by Event")
    if not by_event:
        lines.append("No events recorded in window.")
    else:
        for row in by_event:
            name = row.get("event_name", "?")
            total = int(float(row.get("total_events", 0)))
            lines.append(f"- {name}: {total}")
    lines.append("")
    lines.append("## Top Events by Page & Key")
    if not by_page:
        lines.append("No page-level events recorded in window.")
    else:
        for row in by_page:
            name = row.get("event_name", "?")
            path = row.get("page_path", "/")
            key = row.get("event_key", "")
            total = int(float(row.get("total_events", 0)))
            suffix = f" [{key}]" if key else ""
            lines.append(f"- {path} :: {name}{suffix}: {total}")
    lines.append("")
    lines.append("## Core Web Vitals (p75)")
    if not vitals:
        lines.append("No Core Web Vitals samples recorded in window.")
    else:
        for row in vitals:
            vname = row.get("vital_name", "?")
            rating = row.get("rating", "?")
            samples = int(float(row.get("samples", 0)))
            p75 = float(row.get("p75_value", 0.0))
            lines.append(f"- {vname} ({rating}): p75={p75:.1f} (n={samples})")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Lookback window in days (default: 7)",
    )
    args = parser.parse_args(argv)
    days = max(1, min(args.days, 90))

    account_id = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "").strip()
    api_token = os.environ.get("CLOUDFLARE_API_TOKEN", "").strip()
    if not account_id or not api_token:
        print(
            "events_report: CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN must be set",
            file=sys.stderr,
        )
        return 1

    try:
        by_event = run_sql_query(account_id, api_token, EVENTS_BY_NAME_SQL.format(days=days))
        by_page = run_sql_query(account_id, api_token, EVENTS_BY_PAGE_SQL.format(days=days))
        vitals = run_sql_query(account_id, api_token, VITALS_SQL.format(days=days))
    except (urllib.error.URLError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"events_report: query failed: {exc}", file=sys.stderr)
        return 1

    print(format_report(by_event, by_page, vitals, days))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
