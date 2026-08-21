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


def _index_en_slugs_by_date() -> dict[str, list[str]]:
    """Return ``{YYYY-MM-DD: [en-slug, ...]}`` for every top-level dated
    EN post. A date may host multiple EN articles (e.g. a Saturday
    publishing two pieces) — earlier versions of this script kept only
    one stem per date, which silently dropped one EN article from every
    locale's slug map. The list form preserves all of them."""
    out: dict[str, list[str]] = {}
    if not POSTS.is_dir():
        return out
    for md in POSTS.glob("*.md"):
        m = _DATED_RE.match(md.stem)
        if m:
            out.setdefault(m.group(1), []).append(md.stem)
    for date in out:
        out[date].sort()
    return out


def _articles_map_for_language(
    lang_dir: Path,
    en_by_date: dict[str, list[str]],
    previous: dict[str, str] | None = None,
) -> dict[str, str]:
    """Build ``{en-slug: locale-slug}`` for one locale by scanning its
    ``_posts/<lang>/*.md`` files and pairing each EN article with the
    best-matching locale file on the same date.

    Per-date pairing rules, applied in order:

      1. **Sticky preference** — the slug already in the existing
         ``slugs.json`` wins if its source file still exists. Once a
         translator chose a slug, a later stub dropped in for the same
         date can't silently steal the mapping.
      2. **Exact stem match** — if a locale stem matches the EN stem
         exactly (the locale uses the EN-named filename, common in
         languages that haven't translated the URL yet), pair them.
      3. **Sorted residual pairing** — after sticky + exact have
         claimed their pairs, the remaining EN slugs and remaining
         locale stems for the same date are paired up in sorted order.
         This is deterministic but order-coupled; if a date has, say,
         two EN articles "magnifica" and "stablecoins" and two locale
         files "magnifica-quantique" and "stablecoins-vs-tokenise",
         sorted-order pairing produces the right answer because the
         locale slugs preserve the lexicographic order of the EN
         slugs. When that assumption breaks the publisher should set
         the locale filename to the EN stem (triggering rule 2) or
         commit the desired mapping to ``slugs.json`` once (triggering
         rule 1 on every later regen)."""
    out: dict[str, str] = {}
    previous = previous or {}
    if not lang_dir.is_dir():
        return out
    for date, en_slugs in _locale_stems_by_date(lang_dir, en_by_date).items():
        _pair_one_date(out, en_by_date[date], en_slugs, previous)
    return out


def _locale_stems_by_date(
    lang_dir: Path, en_by_date: dict[str, list[str]]
) -> dict[str, list[str]]:
    """``{date: [locale stems]}`` for dates that also have an EN article.

    A locale file on a date with no English counterpart has nothing to pair
    with, so it is dropped here rather than confusing the pairing passes.
    """
    by_date: dict[str, list[str]] = {}
    for md in lang_dir.glob("*.md"):
        m = _DATED_RE.match(md.stem)
        if m and m.group(1) in en_by_date:
            by_date.setdefault(m.group(1), []).append(md.stem)
    return by_date


def _pair_one_date(
    out: dict[str, str],
    en_slugs: list[str],
    locale_stems: list[str],
    previous: dict[str, str],
) -> None:
    """Pair one date's EN slugs to its locale stems, in three passes.

    Order is the whole design (see the caller's docstring): sticky wins first
    so a translator's choice cannot be stolen by a later stub, exact stem
    match second, and only the leftovers are paired positionally.
    """
    locale_stems = list(locale_stems)
    en_remaining = list(en_slugs)

    def claim(en_slug: str, locale_stem: str) -> None:
        out[en_slug] = locale_stem
        locale_stems.remove(locale_stem)
        en_remaining.remove(en_slug)

    # Pass 1: sticky preference — the slug already committed to slugs.json.
    for en_slug in list(en_remaining):
        prior = previous.get(en_slug)
        if prior and prior in locale_stems:
            claim(en_slug, prior)

    # Pass 2: exact stem match — the locale kept the EN filename.
    for en_slug in list(en_remaining):
        if en_slug in locale_stems:
            claim(en_slug, en_slug)

    # Pass 3: sorted residual pairing — deterministic, order-coupled.
    en_remaining.sort()
    locale_stems.sort()
    out.update(zip(en_remaining, locale_stems, strict=False))


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
