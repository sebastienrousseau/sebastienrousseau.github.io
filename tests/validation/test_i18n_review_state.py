#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Gate: no machine-drafted string stays unreviewed for more than 60 days.

Plan A-3. Prints, per indexed locale, how many tag, author-card and patch
strings are still unreviewed (``scripts/i18n/review_sheet.py``), and fails
only when one of them was first exported (``drafted_on`` in
``_data/i18n/<lang>/review.json``) more than 60 days ago. A string never
exported has no clock yet: run ``review_sheet.py export`` to start it.

Run from repo root: ``python3 tests/validation/test_i18n_review_state.py``.
"""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "i18n"))
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
import _locale_indexing as _li
import review_sheet as rs

MAX_AGE_DAYS = 60


def overdue(lang: str, today: dt.date) -> tuple[int, list[str]]:
    """(unreviewed count, keys older than the limit) for one locale."""
    state = rs.load_state(lang)
    rows = rs.unreviewed(lang)
    late = []
    for r in rows:
        drafted = state.get(f"{r['file']}::{r['key']}", {}).get("drafted_on")
        if drafted and (today - dt.date.fromisoformat(drafted)).days > MAX_AGE_DAYS:
            late.append(f"{lang}: {r['file']}::{r['key']} (drafted {drafted})")
    return len(rows), late


def main() -> int:
    today = dt.date.today()
    late: list[str] = []
    for lang in sorted(_li.indexed_codes() - {"en"}):
        count, overdue_keys = overdue(lang, today)
        late += overdue_keys
        print(f"  {lang}: {count} unreviewed")
    if late:
        print(
            f"i18n-review-state: {len(late)} string(s) unreviewed for over {MAX_AGE_DAYS} days",
            file=sys.stderr,
        )
        for line in late[:20]:
            print(f"  {line}", file=sys.stderr)
        return 1
    print(f"ok: no unreviewed string older than {MAX_AGE_DAYS} days")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
