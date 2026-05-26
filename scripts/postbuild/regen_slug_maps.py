#!/usr/bin/env python3
"""Regenerate ``_data/i18n/<lang>/slugs.json`` from the actual locale
post filenames in ``_posts/<lang>/``.

Why: each article PR used to commit slug-map updates manually (one line
per locale × 27 = 27 modified JSON files per PR). With multiple articles
in flight on stacked PRs, those updates collide every time. By deriving
the article slug map from the on-disk locale filenames at build time,
PRs become additive-only — they ship only the new article source files
(EN + 27 translations) and the slug map regenerates itself.

Slug map shape:
    {
      "_comment": "EN → FR slug map. ...",
      "static": { "about": "a-propos", ... },        // preserved verbatim
      "articles": { "<en-slug>": "<locale-slug>", ... }  // regenerated
    }

Algorithm:
    1. Index every dated EN post at ``_posts/YYYY-MM-DD-*.md`` by its
       date prefix.
    2. For each language directory ``_posts/<lang>/``, scan its dated
       posts. Each locale file's stem is the locale slug; match it to
       the EN slug by date prefix and write the mapping.
    3. Preserve ``_comment`` and ``static`` from the existing
       ``slugs.json`` — those are hand-curated and the regen never owns
       them. Only the ``articles`` dict is rewritten.
    4. Write the result back with stable key ordering so diffs are
       deterministic when an article is added.

Run as part of ``build.sh`` before ``ssg`` so the rendered hreflang and
locale-alternative URLs always reflect the on-disk state.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POSTS = ROOT / "_posts"
I18N = ROOT / "_data" / "i18n"

_DATED_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-(.+)$")


def _index_en_slugs_by_date() -> dict[str, str]:
    """Return ``{YYYY-MM-DD: en-slug}`` for every top-level dated EN post."""
    out: dict[str, str] = {}
    if not POSTS.is_dir():
        return out
    for md in POSTS.glob("*.md"):
        m = _DATED_RE.match(md.stem)
        if m:
            out[m.group(1)] = md.stem
    return out


def _articles_map_for_language(
    lang_dir: Path,
    en_by_date: dict[str, str],
    previous: dict[str, str] | None = None,
) -> dict[str, str]:
    """Build ``{en-slug: locale-slug}`` for one locale by scanning its
    ``_posts/<lang>/*.md`` files and matching each on its date prefix.

    Conflict resolution when a date has multiple candidate files:
      1. The previously-mapped slug wins if its file still exists. This
         makes the regen sticky — once a translator chose a slug, a
         later stub file dropped into ``_posts/<lang>/`` for the same
         date can't silently steal the mapping.
      2. Otherwise, locale-named files (stem != EN slug) beat EN-named
         twins (stem == EN slug). EN-named twins are typically leftover
         stubs from an aborted translation pipeline and would regress
         the locale's hreflang / canonical / language-switcher URLs.
      3. Among multiple locale-named candidates, glob order decides
         (deterministic but arbitrary)."""
    out: dict[str, str] = {}
    previous = previous or {}
    if not lang_dir.is_dir():
        return out
    by_date: dict[str, list[str]] = {}
    for md in lang_dir.glob("*.md"):
        m = _DATED_RE.match(md.stem)
        if not m:
            continue
        date = m.group(1)
        if date not in en_by_date:
            continue
        by_date.setdefault(date, []).append(md.stem)
    for date, stems in by_date.items():
        en_slug = en_by_date[date]
        prior = previous.get(en_slug)
        if prior and prior in stems:
            out[en_slug] = prior
            continue
        locale_named = sorted(s for s in stems if s != en_slug)
        if locale_named:
            out[en_slug] = locale_named[0]
        else:
            out[en_slug] = stems[0]
    return out


def regen_one(lang: str, *, en_by_date: dict[str, str]) -> tuple[int, int]:
    """Regenerate ``_data/i18n/<lang>/slugs.json``. Returns
    ``(article_count, added_since_previous)``."""
    slugs_path = I18N / lang / "slugs.json"
    lang_dir = POSTS / lang
    if not slugs_path.exists():
        # Nothing to preserve — fresh write would lose hand-curated
        # `_comment`/`static`. Skip silently.
        return (0, 0)
    existing = json.loads(slugs_path.read_text(encoding="utf-8"))
    previous = existing.get("articles", {}) or {}
    articles = _articles_map_for_language(lang_dir, en_by_date, previous=previous)
    # Stable, deterministic ordering: oldest-first by EN slug (which
    # already starts with the date), matching what translate_post.py
    # produces.
    articles_sorted = dict(sorted(articles.items()))
    added = len(set(articles_sorted) - set(previous))
    existing["articles"] = articles_sorted
    slugs_path.write_text(
        json.dumps(existing, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return (len(articles_sorted), added)


def main() -> int:
    if not I18N.is_dir():
        print("regen_slug_maps: _data/i18n/ missing; nothing to do.")
        return 0
    en_by_date = _index_en_slugs_by_date()
    if not en_by_date:
        print("regen_slug_maps: no dated EN posts found; nothing to do.")
        return 0
    langs = sorted(p.name for p in I18N.iterdir() if p.is_dir())
    total_added = 0
    summary: list[str] = []
    for lang in langs:
        count, added = regen_one(lang, en_by_date=en_by_date)
        total_added += added
        summary.append(f"{lang}={count}" + (f"(+{added})" if added else ""))
    print(f"regen_slug_maps: {len(langs)} locale(s); {' '.join(summary)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
