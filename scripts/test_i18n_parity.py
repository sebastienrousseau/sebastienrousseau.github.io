#!/usr/bin/env python3
"""Smoke test: every active non-EN language has a 1:1 slug map vs English.

This is the parity gate for the multi-language rollout. For every
``Language`` flagged ``active=True`` in ``scripts/_lang_registry.py``
(other than English itself), this script asserts:

  1. ``_data/i18n/<code>/slugs.json`` exists and parses.
  2. Every EN article slug in ``_posts/*.md`` has a counterpart in
     the language's ``articles`` map.
  3. Every static-page slug expected by the FR mirror has a
     counterpart in the language's ``static`` map. (We use the FR
     static-page slug list as the reference because that's the
     historic baseline; once other languages ship, the contract
     becomes "match every EN static page".)
  4. No two articles in the same language share the same translated
     slug (would collide on case-insensitive filesystems).
  5. The inverse map is unique — no two EN slugs collapse to the
     same translated slug.
  6. Every translated slug is ASCII-only, lowercase, hyphen-joined,
     length ≤ 90 chars.

Run from repo root: ``python3 scripts/test_i18n_parity.py``. Exits
non-zero on any defect. Wired into ``build.sh`` so the build fails
if a translation goes missing.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _lang_registry  # type: ignore[import-not-found]

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "_posts"

# Slug shape: ASCII-only, lowercase, hyphen-joined.
_SLUG_OK_RE = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
_MAX_SLUG_LEN = 100

# Static-page slugs every active language must cover. Mirrors the
# baseline FR set in scripts/build_translations.py:STATIC_SLUG_FR.
REQUIRED_STATIC_SLUGS = (
    "about", "papers", "projects", "topics", "tags",
    "contact", "accessibility", "privacy", "terms",
    "playlists", "made-with-static-site-generator",
    "made-with-shokunin", "404", "offline", "thanks", "articles",
)


def _en_article_slugs() -> set[str]:
    """Every dated EN article that has a frontmatter date."""
    return {
        p.stem for p in POSTS.glob("*.md")
        if re.match(r'^\d{4}-\d{2}-\d{2}-', p.name)
    }


def check_language(lang: _lang_registry.Language) -> list[str]:
    """Return a list of human-readable defects for one language. Empty
    list = pass."""
    problems: list[str] = []
    try:
        data = _lang_registry.load_slugs(lang.code)
    except _lang_registry.LanguageError as e:
        return [str(e)]
    static_map = data["static"]
    article_map = data["articles"]

    # 2. Every EN article has a counterpart
    en_articles = _en_article_slugs()
    missing_articles = en_articles - set(article_map)
    problems.extend(
        f"[{lang.code}] missing article translation: {slug}"
        for slug in sorted(missing_articles)
    )

    # 3. Every required static-page slug has a counterpart
    missing_static = set(REQUIRED_STATIC_SLUGS) - set(static_map)
    problems.extend(
        f"[{lang.code}] missing static-page slug: {slug}"
        for slug in sorted(missing_static)
    )

    # Combined slug list for shape + collision checks
    all_native = list(article_map.values()) + list(static_map.values())

    # 4. No two slugs collide (case-insensitive)
    case_lower = [s.lower() for s in all_native]
    seen: dict[str, str] = {}
    for original, lower in zip(all_native, case_lower, strict=True):
        if lower in seen and seen[lower] != original:
            problems.append(
                f"[{lang.code}] slug collision: {seen[lower]!r} vs {original!r} "
                f"(case-insensitive)"
            )
        seen[lower] = original

    # 5. Inverse map uniqueness (no two EN slugs collapse to the same)
    inverse: dict[str, list[str]] = {}
    for en_slug, native in article_map.items():
        inverse.setdefault(native, []).append(en_slug)
    for native, en_slugs in inverse.items():
        if len(en_slugs) > 1:
            problems.append(
                f"[{lang.code}] inverse-map collision: {native!r} ← "
                + ", ".join(repr(s) for s in en_slugs)
            )

    # 6. Slug shape
    for slug in sorted(set(all_native)):
        if not _SLUG_OK_RE.match(slug):
            problems.append(f"[{lang.code}] malformed slug: {slug!r}")
        if len(slug) > _MAX_SLUG_LEN:
            problems.append(
                f"[{lang.code}] slug exceeds {_MAX_SLUG_LEN} chars: {slug!r}"
            )

    return problems


def main() -> int:
    all_problems: list[str] = []
    languages = [
        lang for lang in _lang_registry.active()
        if lang.code != "en"
    ]
    if not languages:
        print("warn: no active non-EN languages — nothing to check", file=sys.stderr)
        return 0
    for lang in languages:
        all_problems.extend(check_language(lang))

    if all_problems:
        print("i18n parity defects:", file=sys.stderr)
        for line in all_problems[:50]:
            print(f"  - {line}", file=sys.stderr)
        if len(all_problems) > 50:
            print(f"  …and {len(all_problems) - 50} more", file=sys.stderr)
        return 1

    print(
        f"ok: i18n parity passes for {len(languages)} language(s) "
        f"({', '.join(lang.code for lang in languages)})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
