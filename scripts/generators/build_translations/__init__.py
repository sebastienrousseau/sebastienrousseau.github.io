#!/usr/bin/env python3
"""Render manual French translations under ``public/fr/{slug}/``.

Translation sources live in ``_posts/fr/*.md``. For each translation,
this package:

  1. Parses YAML frontmatter (title, description, banner, dates, …).
  2. Renders the markdown body to HTML via markdown-it-py.
  3. Loads the rendered English page at ``public/{slug}/index.html`` and
     uses it as a shell — same nav, footer, head meta, CSS — so the
     French version inherits every layout fix automatically.
  4. Swaps the English body for the French body and patches every
     language-bearing attribute (html lang, meta description, og:*,
     canonical, JSON-LD inLanguage / headline / description).
  5. Writes ``public/fr/{slug}/index.html``.

Also emits ``public/fr/index.html`` — the French articles hub.

Hreflang reciprocity (English ↔ French) is wired in postbuild.py so
the link tags survive subsequent rebuilds.

Must run AFTER ``ssg`` and ``build_topics.py``, BEFORE
``build_agent_api.py`` and ``postbuild.py`` (so the French pages enter
the same SRI / CSP / sitemap pipeline as the English originals).

Package layout (was a single 2,500-line module):

  _state.py   — per-language mutable globals + ``bind_lang()``
  _fm.py      — frontmatter re-export + markdown renderer
  _chrome.py  — head/meta/JSON-LD/breadcrumb chrome rewriting
  _maps.py    — EN→FR title/description/excerpt/eyebrow/url maps
  _article.py — per-article renderer (lead, takeaways, author card)
  _pages.py   — articles hub, home, static mirrors, topic sub-pages
  _search.py  — per-language search index
  _run.py     — per-language driver + ``main()``
"""

from __future__ import annotations

import sys as _sys  # path bootstrap — scripts reorg (scripts/lib/ on sys.path)
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[2] / "lib"))
_sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))  # generators dir

from ._article import render_translation
from ._chrome import (
    _localize_inlanguage_globally,
    _swap_breadcrumb,
    localize_en_dates,
    localize_feed_links,
    rewrite_static_links,
    translate_chrome,
)
from ._fm import parse_frontmatter, render_markdown
from ._maps import (
    rewrite_en_descs_in_text,
    rewrite_en_titles_in_text,
    rewrite_en_urls,
    rewrite_fr_link_titles,
    rewrite_newsroom_card_titles,
    rewrite_related_card_titles,
)
from ._pages import (
    render_articles_hub,
    render_home,
    render_static_translation,
    write_static_translations,
)
from ._run import _render_one_lang, main
from ._search import _build_fr_search_index
from ._state import (
    BASE,
    CHROME_PATCHES,
    EN_TO_FR,
    FR_TO_EN,
    I18N_FR,
    PUBLIC,
    STATIC_SLUG_EN,
    STATIC_SLUG_FR,
    bind_lang,
    fr_slug,
)

# Legacy private name — the monolith called this ``_bind_lang``.
_bind_lang = bind_lang

__all__ = [
    "BASE",
    "CHROME_PATCHES",
    "EN_TO_FR",
    "FR_TO_EN",
    "I18N_FR",
    "PUBLIC",
    "STATIC_SLUG_EN",
    "STATIC_SLUG_FR",
    "_bind_lang",
    "_build_fr_search_index",
    "_localize_inlanguage_globally",
    "_render_one_lang",
    "_swap_breadcrumb",
    "bind_lang",
    "fr_slug",
    "localize_en_dates",
    "localize_feed_links",
    "main",
    "parse_frontmatter",
    "render_articles_hub",
    "render_home",
    "render_markdown",
    "render_static_translation",
    "render_translation",
    "rewrite_en_descs_in_text",
    "rewrite_en_titles_in_text",
    "rewrite_en_urls",
    "rewrite_fr_link_titles",
    "rewrite_newsroom_card_titles",
    "rewrite_related_card_titles",
    "rewrite_static_links",
    "translate_chrome",
    "write_static_translations",
]
