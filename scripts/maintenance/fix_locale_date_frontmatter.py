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


def main() -> int:
    apply = "--apply" in sys.argv
    converted: list[tuple[pathlib.Path, str, str]] = []
    manual: list[tuple[pathlib.Path, str]] = []
    skipped = 0

    for p in sorted((ROOT / "_posts").glob("*/*.md")):
        m = DATED.match(p.stem)
        if not m:
            continue
        slug_date = datetime.date.fromisoformat(m.group(1))
        text = p.read_text(encoding="utf-8")
        cur = field(text, "date")
        if cur is None or parseable(cur):
            skipped += 1
            continue

        en = en_counterpart(p)
        if not en.is_file():
            manual.append((p, "no English counterpart"))
            continue
        src = field(en.read_text(encoding="utf-8"), "date")
        if not src or not parseable(src):
            manual.append((p, f"English counterpart date unusable: {src!r}"))
            continue

        # Assertion 1: the source resolves to a real calendar date.
        d = to_date(src)
        if d is None:
            manual.append((p, f"English date did not round-trip: {src!r}"))
            continue
        # Assertion 2: it agrees with the slug, which is the URL and is not
        # being changed here. Anything outside the window is a real editorial
        # difference (backdated repost, corrected date) and is not guessed at.
        if abs((d - slug_date).days) > SLUG_WINDOW_DAYS:
            manual.append((p, f"English date {d} vs slug {slug_date}"))
            continue

        new = re.sub(r'^date:\s*".*?"\s*$', f'date: "{src}"', text, count=1, flags=re.M)
        if new == text:
            manual.append((p, "date: line did not rewrite"))
            continue
        converted.append((p, cur, src))
        if apply:
            p.write_text(new, encoding="utf-8")

    print(f"  already parseable / skipped : {skipped}")
    print(f"  converted                   : {len(converted)}")
    print(f"  MANUAL REVIEW               : {len(manual)}")
    for p, why in manual[:20]:
        print(f"    {p.parent.name}/{p.stem[:40]}  <- {why}")
    print(f"  ({'APPLIED' if apply else 'dry run — no files written'})")
    return 1 if manual else 0


if __name__ == "__main__":
    raise SystemExit(main())
