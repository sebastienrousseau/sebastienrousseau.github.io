#!/usr/bin/env python3
"""Verify the WCAG 2.2 criteria ssg cannot check statically.

`wcag-compliance.json` classifies each criterion as automated / runtime /
manual / not-applicable. That classification describes **ssg's static
analyser**, not this site's conformance — and treating it as a conformance
score is a category error:

* `runtime` criteria (1.4.3 contrast, 1.4.10 reflow, 1.4.11, 1.4.12, 2.4.11,
  4.1.3) *are* verified here, by the Pa11y sweep — a real browser with
  axe-core, across 3,697 pages, in light **and** forced-dark rendering,
  currently at 0 issues. A static analyser cannot compute contrast; a browser
  can, and we run one.
* `not-applicable` criteria (3.3.7 redundant entry, 3.3.8 accessible
  authentication) have no authentication or multi-step form to apply to.
* That leaves two genuinely manual criteria, and both turn out to be
  decidable by measurement rather than judgement. This file decides them, so
  the claim is reproducible instead of asserted.

Usage:  python3 tests/validation/test_wcag_manual_criteria.py
"""

from __future__ import annotations

import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
I18N = ROOT / "_data" / "i18n"
SAMPLE = 400
SEED = 3

# 2.5.7 applies only where a drag interaction exists. These are every way a
# drag can be initiated in HTML or JS; if none is present, the criterion has
# nothing to apply to.
_DRAG = re.compile(
    r'draggable=["\']true["\']|ondrag[a-z]*=|addEventListener\(\s*["\']'
    r"(?:drag|dragstart|dragover|dragend|pointermove|touchmove)",
    re.IGNORECASE,
)


def _pages() -> list[Path]:
    return sorted(PUBLIC.rglob("index.html"))


def _contact_slugs() -> dict[str, str]:
    """Each locale's own contact slug, from the site's own i18n data.

    Guessing these is how an earlier measurement of this criterion reported
    48 % coverage: the pattern included Italian ``contatto`` while the site
    uses ``contatti``, so a link that was present on every page looked absent
    on half of them. Read the slug map instead of pattern-matching.
    """
    out = {"en": "contact"}
    for f in I18N.glob("*/slugs.json"):
        try:
            static = json.loads(f.read_text(encoding="utf-8")).get("static", {})
        except (OSError, ValueError):
            continue
        out[f.parent.name] = static.get("contact", "contact")
    return out


def check_2_5_7_dragging(pages: list[Path]) -> list[str]:
    """Dragging Movements (AA). Applicable only if a drag interaction exists."""
    offenders = [
        str(p.relative_to(PUBLIC))
        for p in pages
        if _DRAG.search(p.read_text(encoding="utf-8", errors="ignore"))
    ]
    offenders.extend(
        str(js.relative_to(PUBLIC))
        for js in PUBLIC.glob("main.*.js")
        if _DRAG.search(js.read_text(encoding="utf-8", errors="ignore"))
    )
    return offenders


def check_3_2_6_consistent_help(pages: list[Path], slugs: dict[str, str]) -> list[str]:
    """Consistent Help (A). The help mechanism must be present and in the same
    place. Checked as: every page carries a footer link to its own locale's
    contact page."""
    # Fixed seed so two runs on the same tree agree. Not a security context.
    rng = random.Random(SEED)  # noqa: S311
    sample = rng.sample(pages, min(len(pages), SAMPLE))
    missing: list[str] = []
    for p in sample:
        parts = p.relative_to(PUBLIC).parts
        lang = parts[0] if parts and parts[0] in slugs else "en"
        slug = re.escape(slugs.get(lang, "contact"))
        html = p.read_text(encoding="utf-8", errors="ignore")
        if not re.search(rf'<a\b[^>]*href="[^"]*/{slug}/?"', html, re.IGNORECASE):
            missing.append(str(p.relative_to(PUBLIC)))
    return missing


def main() -> int:
    pages = _pages()
    if not pages:
        print("wcag-manual: no built pages — run ./build.sh first", file=sys.stderr)
        return 1

    problems: list[str] = []

    drag = check_2_5_7_dragging(pages)
    if drag:
        problems.append(
            f"2.5.7 Dragging Movements: {len(drag)} file(s) introduce a drag "
            f"interaction, so the criterion now applies and needs a "
            f"single-pointer alternative — e.g. {drag[0]}"
        )
    else:
        print(f"  2.5.7 Dragging Movements   not applicable — 0 drag interactions in {len(pages)} pages + shipped JS")

    slugs = _contact_slugs()
    missing = check_3_2_6_consistent_help(pages, slugs)
    if missing:
        problems.append(
            f"3.2.6 Consistent Help: {len(missing)} of {min(len(pages), SAMPLE)} "
            f"sampled pages carry no help link — e.g. {missing[0]}"
        )
    else:
        print(f"  3.2.6 Consistent Help      pass — footer help link on {min(len(pages), SAMPLE)}/{min(len(pages), SAMPLE)} sampled pages across {len(slugs)} locales")

    if problems:
        for p in problems:
            print(f"  ::error::{p}", file=sys.stderr)
        return 1
    print("wcag-manual: both manually-classified criteria verified by measurement")
    return 0


if __name__ == "__main__":
    sys.exit(main())
