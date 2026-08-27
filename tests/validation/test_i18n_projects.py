#!/usr/bin/env python3
"""The /projects/ body catalogue must stay aligned with the English page.

``build_translations/_projects.py`` reads its English reference from the
*built* page rather than from a source module, so the reference cannot
drift out of date. The cost of that choice is the opposite failure: a
copy change on /projects/ silently changes the reference while all 34
catalogues still hold the old counts.

The catalogues are positional arrays — repeating 29 long English
excerpts in 34 files would add 200 KB of duplication — so a length
mismatch is not a small problem. Add one project card to the English
page and, without this gate, every catalogue from that point on would
describe the wrong project: 28 confidently mislabelled cards per locale.

The localiser already refuses to shift a section whose length no longer
matches, and prints why. That keeps a bad build correct but quiet. This
gate makes it loud, at the point where it is cheap to fix.

Also checked:

* ``{age}`` survives in ``gh_pushed_template``. The commit age comes
  from the GitHub push date and changes between builds, so it is
  templated rather than pinned; a translation that drops the
  placeholder would print one stale age on all 29 cards.
* no entry is left as the English string, which is what a
  half-finished catalogue looks like.

Usage:  python3 tests/validation/test_i18n_projects.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
sys.path.insert(0, str(ROOT / "scripts" / "generators"))

import _lang_registry  # type: ignore[import-not-found]
from build_translations._projects import reference  # type: ignore[import-not-found]

EN_PAGE = ROOT / "public" / "projects" / "index.html"

# Fields whose English is a bare standard or product name, where an
# identical translation is correct rather than a gap.
NAME_LIKE = {"more"}


def check(code: str, ref: dict[str, list[str]]) -> list[str]:
    """Defects in one locale's catalogue, as human-readable lines."""
    try:
        cat = _lang_registry.load_projects(code)
    except _lang_registry.LanguageError as exc:
        return [f"{code}: {exc}"]

    problems: list[str] = []
    for key, en_values in ref.items():
        got = cat.get(key)
        if got is None:
            problems.append(f"{code}/{key}: missing")
            continue
        if len(got) != len(en_values):
            problems.append(
                f"{code}/{key}: has {len(got)} entries, the English page has {len(en_values)}"
            )
            continue
        for i, (en, tr) in enumerate(zip(en_values, got, strict=True)):
            if not tr.strip():
                problems.append(f"{code}/{key}[{i}]: empty")
            elif tr == en and key not in NAME_LIKE and len(en.split()) > 2:
                problems.append(f"{code}/{key}[{i}]: still English — {en[:60]!r}")

    template = cat.get("gh_pushed_template")
    if not template:
        problems.append(f"{code}: missing gh_pushed_template")
    elif "{age}" not in template:
        problems.append(
            f"{code}: gh_pushed_template drops the {{age}} placeholder — "
            f"every card would show the same commit age ({template!r})"
        )
    return problems


def main() -> int:
    if not EN_PAGE.is_file():
        print("public/projects/index.html not built — run ./build.sh first", file=sys.stderr)
        return 0

    ref = reference(EN_PAGE.read_text(encoding="utf-8", errors="ignore"))
    codes = [lg.code for lg in _lang_registry.active() if lg.code != "en"]
    problems: list[str] = []
    for code in codes:
        problems.extend(check(code, ref))

    if problems:
        print("projects catalogue defects:", file=sys.stderr)
        for line in problems[:60]:
            print(f"  - {line}", file=sys.stderr)
        if len(problems) > 60:
            print(f"  …and {len(problems) - 60} more", file=sys.stderr)
        return 1

    total = sum(len(v) for v in ref.values())
    print(
        f"ok: /projects/ catalogue complete for {len(codes)} language(s) "
        f"({total} strings across {len(ref)} sections each)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
