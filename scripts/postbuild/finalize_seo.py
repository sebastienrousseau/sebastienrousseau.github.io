#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Last SEO pass over ``public/``: locale indexing, unique head metadata,
sitemap pruning and real ``<lastmod>`` dates.

Runs in build.sh after ``fix_lang_switcher.py`` (which reads the hreflang
links this pass strips from the noindex locales) and after every sitemap
writer, so nothing later re-adds what it removes. Order inside the pass:

1. ``locale_indexing``: noindex + hreflang removal for the locales outside
   ``_data/seo/locale-indexing.json``.
2. ``indexability.prune_sitemaps``: drops every ``<loc>`` that is now
   noindex (the whole of each of those locales).
3. ``unique_meta``: titles and descriptions, unique among the pages that
   are still indexable.
4. ``sitemap_lastmod``: the real modification date of each remaining URL.

Idempotent: a second run changes nothing.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
sys.path.insert(0, str(ROOT / "scripts" / "postbuild"))

import _lang_registry as _lr
from postbuild_lib.indexability import is_indexable, prune_sitemaps
from postbuild_lib.locale_indexing import apply_locale_indexing, page_locale
from postbuild_lib.sitemap_lastmod import refresh_lastmod
from postbuild_lib.unique_meta import make_unique
from postbuild_transforms import build_comprehensive_lastmod_index

PUBLIC = Path("public")
SITE = "https://sebastienrousseau.com"


def _entries(public: Path) -> list[tuple[Path, str, str, bool]]:
    """``(path, rel, locale, indexable)`` for every ``index.html`` page."""
    codes = frozenset(lang.code for lang in _lr.active())
    out = []
    for page in sorted(public.rglob("index.html")):
        rel = page.relative_to(public).as_posix()
        loc = f"{SITE}/{rel.removesuffix('index.html')}"
        out.append((page, rel, page_locale(rel, codes), is_indexable(loc, public)))
    return out


def main(public: Path = PUBLIC) -> int:
    if not (public / "index.html").is_file():
        print("finalize_seo: public/ not built", file=sys.stderr)
        return 1
    noindexed, hreflang_removed = apply_locale_indexing(public)
    pruned = prune_sitemaps(public)
    rewritten = make_unique(_entries(public))
    dated, undated = refresh_lastmod(public, build_comprehensive_lastmod_index())
    print(
        f"finalize_seo: {noindexed} page(s) set noindex, {hreflang_removed} hreflang link(s) "
        f"removed, {pruned} sitemap entrie(s) pruned, {rewritten} page(s) given unique "
        f"title/description, lastmod on {dated} URL(s) ({undated} without a real date)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
