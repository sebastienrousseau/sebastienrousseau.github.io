# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Indexed pages link only to indexed locales (decision D-3, option b).

The header's language menu lists every active locale, 35 of them. On a page
search engines index, the 24 links into noindexed locales spend crawl budget
on pages that can never rank. This pass keeps, on indexed pages, only the
menu items for the locales in ``_data/seo/locale-indexing.json`` and ends the
menu with "More languages", which links to ``/languages/``: that page lists
every locale, so each translation stays one click from anywhere.

A noindexed page (a noindexed locale, or a utility page with its own
``noindex``) keeps the full menu, so readers of those languages navigate as
before. Runs from ``locale_indexing.apply_locale_indexing``, after the
robots meta has been merged, so the page's final robots value decides.
"""

from __future__ import annotations

import re

LANGUAGES_PATH = "/languages/"

# "More languages" in each indexed locale. The English is the source; the
# rest follow A-3's review flow like every other UI string.
MORE_LABEL = {
    "en": "More languages",
    "fr": "Autres langues",
    "de": "Weitere Sprachen",
    "es": "Más idiomas",
    "it": "Altre lingue",
    "cs": "Další jazyky",
    "ru": "Другие языки",
    "ja": "その他の言語",
    "ko": "다른 언어",
    "zh-hans": "更多语言",
    "zh-hant": "更多語言",
}

_ITEM_RE = re.compile(
    r'\s*<a class="ap-lang-item"[^>]*\bdata-lang="([^"]+)"[^>]*>.*?</a>', re.DOTALL
)
_GRID_RE = re.compile(r'(<div class="ap-lang-menu-grid">)(.*?)(</div>)', re.DOTALL)
_ROBOTS_RE = re.compile(r'<meta\s+name="robots"\s+content="([^"]*)"', re.IGNORECASE)


def is_noindex(html: str) -> bool:
    m = _ROBOTS_RE.search(html)
    return bool(m and "noindex" in m.group(1).lower())


def more_item(lang: str) -> str:
    label = MORE_LABEL.get(lang, MORE_LABEL["en"])
    return (
        # data-lang="more": main.js reads data-lang on every item, and no
        # hreflang alternate is named "more", so the href stays as written.
        f' <a class="ap-lang-item ap-lang-more" href="{LANGUAGES_PATH}" data-lang="more"'
        ' role="menuitem">'
        f'<span aria-hidden="true">🌐</span> {label}</a>'
    )


def scope_switcher(html: str, lang: str, indexed: frozenset[str]) -> str:
    """Drop menu items for locales outside ``indexed`` and add "More
    languages". Noindexed pages, pages without the menu and pages already
    scoped are returned unchanged."""
    if is_noindex(html) or "ap-lang-more" in html:
        return html

    def grid(m: re.Match[str]) -> str:
        kept = _ITEM_RE.sub(lambda i: i.group(0) if i.group(1) in indexed else "", m.group(2))
        return m.group(1) + kept.rstrip() + more_item(lang) + " " + m.group(3)

    return _GRID_RE.sub(grid, html, count=1)
