# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Keep the locales outside ``_data/seo/locale-indexing.json`` out of search.

Every active locale stays published for readers, but only the locales in
that policy file may be indexed. For every other locale this pass:

* merges ``noindex`` into the page's single robots meta (``follow`` stays,
  so link equity still flows to the indexed pages they link to);
* strips every hreflang alternate from its pages: a noindex page must not
  sit in a hreflang cluster, because Google requires every member of a
  cluster to be indexable and to link back;
* strips, from every other page, each hreflang alternate that targets one
  of those locales.

Sitemap removal follows from ``noindex``: ``indexability.prune_sitemaps``
already drops any ``<loc>`` whose page is noindex.

Runs after ``fix_lang_switcher.py``, which rewrites the in-page language
switcher from each page's hreflang links: running earlier would leave the
switcher entries for these locales pointing at the locale home instead of
the translation of the current page.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import _lang_registry as _lr
import _locale_indexing as _li

_ROBOTS_META_RE = re.compile(r'<meta\s+(?=[^>]*\bname=["\']?robots["\']?[\s/>])[^>]*>', re.I)
_CONTENT_RE = re.compile(r'\bcontent=(?:"([^"]*)"|\'([^\']*)\'|([^\s>]+))', re.I)
_HEAD_OPEN_RE = re.compile(r"<head\b[^>]*>", re.I)
_HREFLANG_LINK_RE = re.compile(
    r'<link\b(?=[^>]*\brel=["\']?alternate["\']?)'
    r'(?=[^>]*\bhreflang=["\']?([^"\'\s>]+))'
    r'(?=[^>]*\bhref=["\']?([^"\'\s>]+))[^>]*>',
    re.I,
)
# Directives the merged tag decides itself; every other one (max-snippet and
# friends) is carried over unchanged.
_INDEX_DIRECTIVES = {"index", "noindex", "follow", "all", "none"}


def _robots_content(tag: str) -> str:
    m = _CONTENT_RE.search(tag)
    return next((g for g in m.groups() if g is not None), "") if m else ""


def merge_noindex(html: str) -> str:
    """Return ``html`` with exactly one robots meta that says ``noindex``.

    Existing directives are kept (``nofollow`` wins over ``follow``, the
    snippet controls survive); further robots metas are dropped.
    """
    tags = _ROBOTS_META_RE.findall(html)
    kept: list[str] = []
    for tag in tags:
        for raw in _robots_content(tag).split(","):
            d = raw.strip()
            if d and d.lower() not in _INDEX_DIRECTIVES and d not in kept:
                kept.append(d)
    follow = [] if any(d.lower() == "nofollow" for d in kept) else ["follow"]
    meta = f'<meta name="robots" content="{", ".join(["noindex", *follow, *kept])}">'
    if tags:
        first = [True]

        def repl(_m: re.Match[str]) -> str:
            if first[0]:
                first[0] = False
                return meta
            return ""

        return _ROBOTS_META_RE.sub(repl, html)
    m = _HEAD_OPEN_RE.search(html)
    return html if m is None else html[: m.end()] + meta + html[m.end() :]


def page_locale(rel: str, codes: frozenset[str]) -> str:
    """Locale of a ``public/``-relative path: its first segment, or ``en``."""
    first = rel.split("/", 1)[0]
    return first if "/" in rel and first in codes else "en"


def _targets_dropped(hreflang: str, href: str, dropped: tuple[str, ...]) -> bool:
    if hreflang.lower() in _li.noindex_hreflangs():
        return True
    segments = re.sub(r"^https?://[^/]+", "", href).split("/")
    return len(segments) > 1 and segments[1] in dropped


def strip_hreflang(html: str, *, drop_all: bool, dropped: tuple[str, ...]) -> tuple[str, int]:
    """Remove hreflang alternates (all of them, or those for ``dropped``)."""
    removed = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal removed
        if drop_all or _targets_dropped(m.group(1), m.group(2), dropped):
            removed += 1
            return ""
        return m.group(0)

    return _HREFLANG_LINK_RE.sub(repl, html), removed


def apply_locale_indexing(public: Path) -> tuple[int, int]:
    """Apply the policy to every HTML page. Returns (noindexed, hreflang links removed)."""
    dropped = _li.noindex_codes()
    codes = frozenset(lang.code for lang in _lr.active())
    noindexed = removed = 0
    for page in sorted(public.rglob("*.html")):
        html = page.read_text(encoding="utf-8")
        is_dropped = page_locale(page.relative_to(public).as_posix(), codes) in dropped
        out, n = strip_hreflang(html, drop_all=is_dropped, dropped=dropped)
        removed += n
        if is_dropped:
            merged = merge_noindex(out)
            noindexed += merged != out
            out = merged
        if out != html:
            page.write_text(out, encoding="utf-8")
    return noindexed, removed
