#!/usr/bin/env python3
"""Restore locale `date:` frontmatter from its English counterpart.

An earlier translation pass localised the `date:` field ("28 juin 2026",
"2026年6月27日"). Three consumers parse that field and every one of them
falls back silently when it cannot:

  * ssg's news-sitemap generator      -> entry stamped with build time
  * build_lang_feeds.parse_date       -> <pubDate> stamped with build time
  * feeds.py's last-modified map      -> post skipped

Measured before the fix: 467 affected posts, 467 build-stamped RSS items
across 27 locale feeds, and 17 build-stamped news-sitemap entries in fr
(the only advertised locale sitemap).

Parse-don't-guess. The localised string is never parsed: a wrong-but-parseable
date is worse than an unparseable one, because it stops triggering the
fallback and starts looking correct. The English counterpart is the source —
every locale post was scaffolded from one, and `date` is not in the
translation allow-list, so the English value is the original this field was
copied from before being overwritten.

Copying it verbatim (rather than reformatting to ISO) keeps one format across
the corpus: after this runs, every locale post's `date` equals its English
counterpart's, which is an invariant a test can assert. Introducing ISO here
would leave two formats and a weaker check ("parses" rather than "matches").

Usage: fix_locale_date_frontmatter.py [--apply]
"""

from __future__ import annotations

import datetime
import json
import pathlib
import re
import sys
from typing import NamedTuple

ROOT = pathlib.Path(__file__).resolve().parents[2]
DATED = re.compile(r"^(\d{4}-\d{2}-\d{2})-")
# Both full and abbreviated English month names parse in every consumer.
# Verified empirically: ar has 32 abbreviated + 16 localised dates and exactly
# 16 build-stamped sitemap entries; bn has 38 + 15 and exactly 15. Treating
# abbreviations as broken would rewrite 676 healthy files.
MONTHS = {
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
    "jan",
    "feb",
    "mar",
    "apr",
    "jun",
    "jul",
    "aug",
    "sep",
    "sept",
    "oct",
    "nov",
    "dec",
}
SLUG_WINDOW_DAYS = 2


def field(text: str, name: str) -> str | None:
    # Frontmatter uses both quote styles; parts of the corpus are
    # single-quoted (date: 'January 1, 2018'). Stripping only double quotes
    # leaves the value unparseable and invents a defect that is not there.
    m = re.search(rf"^{name}:\s*(.*?)\s*$", text, re.M)
    if not m:
        return None
    v = m.group(1)
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        v = v[1:-1]
    return v


def parseable(v: str) -> bool:
    low = v.lower()
    return bool(
        any(re.search(rf"\b{m}\b", low) for m in MONTHS) or re.match(r"^\d{4}-\d{2}-\d{2}", v)
    )


def to_date(v: str) -> datetime.date | None:
    for fmt in ("%Y-%m-%d", "%B %d, %Y", "%b %d, %Y"):
        try:
            return datetime.datetime.strptime(v, fmt).date()
        except ValueError:
            continue
    return None


def en_counterpart(p: pathlib.Path) -> pathlib.Path:
    """Locale slugs may be localised; map back via the slug registry."""
    reg = ROOT / "_data" / "i18n" / p.parent.name / "slugs.json"
    stem = p.stem
    if reg.is_file():
        articles = json.loads(reg.read_text(encoding="utf-8")).get("articles", {})
        stem = {v: k for k, v in articles.items()}.get(p.stem, p.stem)
    return ROOT / "_posts" / f"{stem}.md"


def _english_source_date(p: pathlib.Path) -> tuple[str | None, str | None]:
    """The English counterpart's usable ``date:`` value, or a reason it isn't.

    Returns ``(date, None)`` on success and ``(None, why)`` when the locale
    file has to go to manual review.
    """
    en = en_counterpart(p)
    if not en.is_file():
        return None, "no English counterpart"
    src = field(en.read_text(encoding="utf-8"), "date")
    if not src or not parseable(src):
        return None, f"English counterpart date unusable: {src!r}"
    return src, None


class _Plan(NamedTuple):
    """What to do with one locale file: rewrite to ``new_text``, or defer."""

    new_text: str | None
    src: str = ""
    why: str = ""


def _plan_one(p: pathlib.Path, text: str, slug_date: datetime.date) -> _Plan:
    """Decide what to do with one unparseable locale date.

    Nothing here guesses: a date is only adopted when it round-trips to a real
    calendar date *and* agrees with the slug, which is the URL and is not being
    changed. Anything outside that window is a real editorial difference
    (backdated repost, corrected date) and goes to a human instead.
    """
    src, why = _english_source_date(p)
    if src is None:
        return _Plan(None, why=why or "unknown")

    d = to_date(src)
    if d is None:
        return _Plan(None, why=f"English date did not round-trip: {src!r}")

    if abs((d - slug_date).days) > SLUG_WINDOW_DAYS:
        return _Plan(None, why=f"English date {d} vs slug {slug_date}")

    new = re.sub(r'^date:\s*".*?"\s*$', f'date: "{src}"', text, count=1, flags=re.M)
    if new == text:
        return _Plan(None, why="date: line did not rewrite")
    return _Plan(new, src=src)


def _report(
    skipped: int,
    converted: list[tuple[pathlib.Path, str, str]],
    manual: list[tuple[pathlib.Path, str]],
    apply: bool,
) -> None:
    """Print the run summary, capped at 20 manual-review lines."""
    print(f"  already parseable / skipped : {skipped}")
    print(f"  converted                   : {len(converted)}")
    print(f"  MANUAL REVIEW               : {len(manual)}")
    for p, why in manual[:20]:
        print(f"    {p.parent.name}/{p.stem[:40]}  <- {why}")
    print(f"  ({'APPLIED' if apply else 'dry run — no files written'})")


def main() -> int:
    apply = "--apply" in sys.argv
    converted: list[tuple[pathlib.Path, str, str]] = []
    manual: list[tuple[pathlib.Path, str]] = []
    skipped = 0

    for p in sorted((ROOT / "_posts").glob("*/*.md")):
        m = DATED.match(p.stem)
        if not m:
            continue
        text = p.read_text(encoding="utf-8")
        cur = field(text, "date")
        if cur is None or parseable(cur):
            skipped += 1
            continue

        plan = _plan_one(p, text, datetime.date.fromisoformat(m.group(1)))
        if plan.new_text is None:
            manual.append((p, plan.why))
            continue
        converted.append((p, cur, plan.src))
        if apply:
            p.write_text(plan.new_text, encoding="utf-8")

    _report(skipped, converted, manual, apply)
    return 1 if manual else 0


if __name__ == "__main__":
    raise SystemExit(main())
