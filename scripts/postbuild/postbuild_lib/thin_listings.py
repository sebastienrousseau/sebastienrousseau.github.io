# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Keep thin listing pages out of the index.

Tag and category term pages (``[<lang>/]tags/<term>/``,
``[<lang>/]categories/<term>/``) and every page after the first of a
paginated listing (``.../page/<N>/`` with N >= 2) repeat excerpts of
articles that are indexed in their own right. Search Console filed most
of them as "Crawled - currently not indexed", and a site with many such
pages reads as thin. They stay published for readers and keep
``follow``, so crawlers still reach the articles they list, but they
carry ``noindex``; ``indexability.prune_sitemaps`` then drops them from
every sitemap.

The hubs stay indexable: the ``tags/`` and ``categories/`` indexes, the
first page of each listing and the curated ``topics/`` pages.
"""

from __future__ import annotations

import re
from pathlib import Path

from postbuild_lib.locale_indexing import merge_noindex

_TERM_RE = re.compile(r"^(?:tags|categories)/[^/]+/index\.html$")
_PAGED_RE = re.compile(r"/page/(\d+)/index\.html$")


def _strip_locale(rel: str, codes: frozenset[str]) -> str:
    first, _, rest = rel.partition("/")
    return rest if rest and first in codes else rel


def is_thin_listing(rel: str, codes: frozenset[str]) -> bool:
    """True for a tag or category term page, or page 2+ of a listing."""
    m = _PAGED_RE.search(rel)
    if m:
        return int(m.group(1)) >= 2
    return bool(_TERM_RE.match(_strip_locale(rel, codes)))


def apply_thin_noindex(public: Path, codes: frozenset[str]) -> int:
    """Merge ``noindex`` into every thin listing page. Returns pages changed."""
    changed = 0
    for page in sorted(public.rglob("index.html")):
        if not is_thin_listing(page.relative_to(public).as_posix(), codes):
            continue
        html = page.read_text(encoding="utf-8")
        out = merge_noindex(html)
        if out != html:
            page.write_text(out, encoding="utf-8")
            changed += 1
    return changed
