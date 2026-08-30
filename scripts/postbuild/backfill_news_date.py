#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Backfill ``news_publication_date:`` into build-copy posts that lack one.

Why: ssg's news-sitemap generator reads ``news_publication_date`` and, when
the field is blank, falls back to **the current time** — stamping a build
timestamp onto an article as its publication date, which for a news sitemap
is precisely the wrong thing to get wrong (issue #433).

Measured on this corpus: 3,640 dated posts, of which only 141 declare the
field. The remaining 3,499 produced one warning each per build —

    news_sitemap: field 'news_publication_date' could not parse date ""

— 3,556 lines in a 6.3 MB log, which is enough noise to bury a real warning.

It causes no bad output *today* only because the sitemaps are recency-filtered
and currently empty; the moment anything publishes inside the 48-hour window
the fallback ships. Every one of those 3,499 posts already carries a ``date:``
to derive from, so nothing needs inventing.

Like ``backfill_permalink``, this runs on the build copy (``--dir
_posts_build``) rather than editing thousands of committed files, so source
stays untouched (ADR-0003).

Deterministic by construction: the value is a pure function of the post's own
``date:``, never of the clock. Two builds of one commit therefore produce
identical output, which the byte-identical rebuild gate requires. The time of
day is fixed at 00:00:00 +0000 because a long-form date carries none — an
honest floor rather than a fabricated hour.

Idempotent: a post that already declares the field is left exactly as-is.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import re
import sys
from pathlib import Path

# The corpus uses BOTH "July 1, 2026" and "Jul 01, 2026". They look alike
# enough that a survey regex counts them as one shape, and a parser accepting
# only the full name silently skips 539 posts — every one of which then keeps
# the build-time fallback this script exists to remove. The same full/short
# split is documented in fix_locale_date_frontmatter's MONTHS set.
# ISO and RFC 2822 are accepted too so a post that adopts either still works.
_LONG_FORM = "%B %d, %Y"
_SHORT_FORM = "%b %d, %Y"
_RFC2822_OUT = "%a, %d %b %Y %H:%M:%S +0000"

_DATE_FIELD = re.compile(r"^date:\s*(.+?)\s*$", re.MULTILINE)
_DATED_NAME = re.compile(r"^\d{4}-\d{2}-\d{2}-")


def _has_frontmatter(text: str) -> bool:
    return text.startswith("---\n") or text.startswith("---\r\n")


def _frontmatter_has_news_date(text: str) -> bool:
    """True if the first front-matter block declares the key."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return False
    for line in lines[1:]:
        if line.strip() == "---":
            return False
        if line.startswith("news_publication_date:"):
            return True
    return False


def parse_date(raw: str) -> _dt.datetime | None:
    """Parse a front-matter ``date:`` value, or ``None`` if unrecognised.

    Never guesses: an unparseable date leaves the post alone, so the worst
    case is the status quo rather than a wrong publication date.
    """
    value = raw.strip().strip('"').strip("'")
    if not value:
        return None
    for fmt in (_LONG_FORM, _SHORT_FORM, "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d", _RFC2822_OUT):
        try:
            return _dt.datetime.strptime(value, fmt).replace(tzinfo=_dt.UTC)
        except ValueError:
            continue
    return None


def _insert_news_date(text: str, stamp: str) -> str:
    """Insert the field immediately after the opening ``---``."""
    newline = "\r\n" if text.startswith("---\r\n") else "\n"
    marker = f"---{newline}"
    rest = text[len(marker) :]
    return f'{marker}news_publication_date: "{stamp}"{newline}{rest}'


def backfill(root: Path) -> tuple[int, int]:
    """Returns (added, skipped-because-undatable)."""
    added = unparsed = 0
    for md in sorted(root.rglob("*.md")):
        if md.name == "README.md" or not _DATED_NAME.match(md.name):
            continue
        text = md.read_text(encoding="utf-8")
        if not _has_frontmatter(text) or _frontmatter_has_news_date(text):
            continue
        m = _DATE_FIELD.search(text)
        parsed = parse_date(m.group(1)) if m else None
        if parsed is None:
            unparsed += 1
            continue
        md.write_text(_insert_news_date(text, parsed.strftime(_RFC2822_OUT)), encoding="utf-8")
        added += 1
    return added, unparsed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dir",
        default="_posts_build",
        help="Build directory to process (default: _posts_build).",
    )
    args = parser.parse_args()
    root = Path(args.dir)
    if not root.is_dir():
        print(f"backfill_news_date: {root} is not a directory", file=sys.stderr)
        return 1
    added, unparsed = backfill(root)
    tail = f", {unparsed} left alone (unparseable date)" if unparsed else ""
    print(f"backfill_news_date: stamped {added} post(s) in {root}{tail}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
