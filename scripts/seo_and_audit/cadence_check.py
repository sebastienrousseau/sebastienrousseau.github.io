#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Warn when English articles bunch up in one week (plan B-3).

More than two English articles dated in the same ISO week blurs what the
site is about and spreads its authority thin. This prints a warning per
crowded week since ``--since`` (default: 90 days ago) and never fails the
build: the editorial calendar (``_data/editorial/calendar.yml``) is where
publication dates are planned.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAX_PER_WEEK = 2
_DATED_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-")


def crowded_weeks(names: list[str], since: dt.date) -> dict[str, list[str]]:
    """``{"2026-W41": [slugs]}`` for weeks over the limit, from file names."""
    weeks: dict[str, list[str]] = defaultdict(list)
    for name in names:
        m = _DATED_RE.match(name)
        if not m:
            continue
        day = dt.date.fromisoformat(m.group(1))
        if day >= since:
            year, week, _ = day.isocalendar()
            weeks[f"{year}-W{week:02d}"].append(name.removesuffix(".md"))
    return {w: sorted(s) for w, s in sorted(weeks.items()) if len(s) > MAX_PER_WEEK}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--since", type=dt.date.fromisoformat, default=dt.date.today() - dt.timedelta(days=90)
    )
    args = parser.parse_args(argv)
    names = [p.name for p in (ROOT / "_posts").glob("*.md")]
    crowded = crowded_weeks(names, args.since)
    for week, slugs in crowded.items():
        print(
            f"cadence warning: {week} has {len(slugs)} English articles (max {MAX_PER_WEEK}): {', '.join(slugs)}"
        )
    if not crowded:
        print(f"ok: no week since {args.since} has more than {MAX_PER_WEEK} English articles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
