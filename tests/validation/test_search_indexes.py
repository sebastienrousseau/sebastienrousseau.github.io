#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Smoke test: EN + FR search indexes must have the same entry shape.

Regression we are guarding: the search widget reads
``e.headings.length`` — if any entry is missing the ``headings``
array, the widget silently aborts and returns zero results. This
test catches that before the build ships.

Run from repo root: ``python3 scripts/test_search_indexes.py``.
Exits non-zero on any defect; CI/Makefile should treat that as a
build failure.
"""

from __future__ import annotations

import sys as _sys  # path bootstrap — scripts reorg (scripts/lib/ on sys.path)
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[2] / "scripts" / "lib"))

import json
import sys
from pathlib import Path

REQUIRED_KEYS = ("title", "url", "content", "headings")
INDEXES = (
    Path("public/search-index.json"),
    Path("public/fr/search-index.json"),
)


def check(path: Path) -> list[str]:
    if not path.is_file():
        return [f"{path}: file missing"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"{path}: JSON parse error — {e}"]
    entries = data.get("entries")
    if not isinstance(entries, list) or not entries:
        return [f"{path}: no entries"]
    problems: list[str] = []
    for i, e in enumerate(entries):
        problems.extend(
            f"{path} entry {i} ({e.get('url', '?')}): missing '{k}'"
            for k in REQUIRED_KEYS
            if k not in e
        )
        if "headings" in e and not isinstance(e["headings"], list):
            problems.append(
                f"{path} entry {i} ({e.get('url', '?')}): "
                f"'headings' is {type(e['headings']).__name__}, expected list"
            )
    return problems


def main() -> int:
    all_problems: list[str] = []
    for p in INDEXES:
        all_problems.extend(check(p))
    if all_problems:
        print("search-index defects:", file=sys.stderr)
        for line in all_problems[:20]:
            print(f"  - {line}", file=sys.stderr)
        if len(all_problems) > 20:
            print(f"  …and {len(all_problems) - 20} more", file=sys.stderr)
        return 1
    print(f"ok: {len(INDEXES)} search-index file(s) pass shape check")
    return 0


if __name__ == "__main__":
    sys.exit(main())
