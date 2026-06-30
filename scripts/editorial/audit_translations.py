#!/usr/bin/env python3
"""Audit locale posts for translation placeholders and draft leakage.

This is intentionally conservative: it reports hard evidence that a page is
not a completed localisation, rather than trying to score translation quality.
"""

from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POSTS = ROOT / "_posts"

HARD_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("stub_marker", re.compile(r"translation-stub", re.I)),
    ("translation_pending", re.compile(r"Translation pending", re.I)),
    ("draft_translation", re.compile(r"DRAFT translation", re.I)),
    ("english_body_stub", re.compile(r"Body text is intentionally left in English", re.I)),
    ("native_review_stub", re.compile(r"native reviewer signs off", re.I)),
    ("editorial_note", re.compile(r"Editorial note:\s*replace this block", re.I)),
    ("draft_title", re.compile(r"\[[A-Z]{2,}(?:-[A-Z]+)? DRAFT\]")),
    ("canonical_fallback_id", re.compile(r"halaman kanonis artikel", re.I)),
    ("canonical_fallback_uk", re.compile(r"канонічн\w+ сторінц\w+ статті", re.I)),
)


def iter_locale_posts() -> list[Path]:
    return sorted(
        path
        for lang_dir in POSTS.iterdir()
        if lang_dir.is_dir()
        for path in lang_dir.glob("*.md")
    )


def scan(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    return [name for name, pattern in HARD_PATTERNS if pattern.search(text)]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fail", action="store_true", help="exit non-zero when defects are found")
    parser.add_argument("--summary-only", action="store_true", help="print counts without file details")
    args = parser.parse_args()

    by_locale: dict[str, Counter[str]] = defaultdict(Counter)
    by_file: list[tuple[Path, list[str]]] = []

    for path in iter_locale_posts():
        kinds = scan(path)
        if not kinds:
            continue
        locale = path.parent.name
        by_locale[locale].update(kinds)
        by_file.append((path, kinds))

    if by_locale:
        print("Translation audit defects by locale:")
        for locale in sorted(by_locale):
            counts = ", ".join(f"{kind}={count}" for kind, count in sorted(by_locale[locale].items()))
            print(f"  {locale}: {counts}")
    else:
        print("Translation audit defects by locale: none")

    if by_file and not args.summary_only:
        print("\nFiles:")
        for path, kinds in by_file:
            rel = path.relative_to(ROOT)
            print(f"  {rel}: {', '.join(kinds)}")

    return 1 if args.fail and by_file else 0


if __name__ == "__main__":
    raise SystemExit(main())
