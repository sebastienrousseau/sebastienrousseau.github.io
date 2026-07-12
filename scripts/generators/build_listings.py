#!/usr/bin/env python3
"""Paged article listing generator — `/articles/`, `/articles/page/N/`.

Runs after ssg, before build_translations + postbuild. Reads all
dated posts under ``_posts/`` (slug starts ``YYYY-MM-DD-``), sorts by
date descending, chunks into pages of 24, and writes:

  - ``public/articles/index.html``        — page 1 (rewritten from
                                            the ssg-produced cover)
  - ``public/articles/page/N/index.html`` — N >= 2

For each non-English locale, the same structure is replicated under
``public/<lang>/<localised-articles>/page/N/index.html``, using the
``static.articles`` slug from ``_data/i18n/<lang>/slugs.json``
(e.g. fr → articles, ja → kiji, ar → maqalat, …).

Each page renders:

  - Hero with title "Articles" + page-N-of-M label
  - Responsive card grid of 24 article cards
  - Pagination nav (Prev / numbered / Next)

Template skeleton comes from the ssg-emitted
``public/articles/index.html`` — the same approach
``build_tag_landings.py`` uses. The hero ``.ap-hero`` block is
stripped to keep exactly one ``<h1>`` per page (AAA).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore[assignment]

ROOT = Path(__file__).resolve().parents[2]
from listing_common import (
    _BANNER_FM_RE,
    _DEFAULT_BANNER,
    _DESC_FM_RE,
    _EXCERPT_FM_RE,
    _TITLE_FM_RE,
    PILLAR_ORDER,
    _alias_map,
    _load_locale_article_slugs,
    _load_locale_post_index,
    _post_pillars,
    _translate_chrome_for,
)

PUBLIC = ROOT / "public"
POSTS = ROOT / "_posts"
TAXONOMY = ROOT / "_data" / "taxonomy.yml"
TEMPLATE_PATH = PUBLIC / "articles" / "index.html"

PAGE_SIZE = 24
_BASE_URL = "https://sebastienrousseau.com"

_BANNER_ALT_FM_RE = re.compile(r'^banner_alt:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
from _core import DATED_SLUG_RE as _DATED_SLUG_RE  # canonical dated-slug matcher
from _svg_icons import (
    _CARD_SVG_EMAIL,
    _CARD_SVG_FB,
    _CARD_SVG_LI,
    _CARD_SVG_LINK,
    _CARD_SVG_WA,
    _CARD_SVG_X,
)

PILLAR_LABELS: dict[str, str] = {
    "ai": "Applied AI",
    "payments": "Payments & money",
    "infra": "Infra & cryptography",
    "policy": "Policy & resilience",
    "open-source": "Open source",
    "leadership": "Banking leadership",
}
_MAIN_RE = re.compile(r'(<main\b[^>]*>)([\s\S]*?)(</main>)', re.IGNORECASE)
_AP_HERO_BLOCK_RE = re.compile(
    r'<section class="ap-hero">[\s\S]*?</section>', re.IGNORECASE
)
_HTML_LANG_RE = re.compile(r'<html lang="[^"]*"', re.IGNORECASE)
_TITLE_RE = re.compile(r"<title>[^<]*</title>", re.IGNORECASE)
_DESC_RE = re.compile(r'<meta name="description" content="[^"]*"', re.IGNORECASE)
_CANONICAL_RE = re.compile(r'<link rel="canonical" href="[^"]*"', re.IGNORECASE)
_OG_TITLE_RE = re.compile(r'<meta property="og:title" content="[^"]*"', re.IGNORECASE)
_OG_DESC_RE = re.compile(r'<meta property="og:description" content="[^"]*"', re.IGNORECASE)
_OG_URL_RE = re.compile(r'<meta property="og:url" content="[^"]*"', re.IGNORECASE)
_INLANG_RE = re.compile(r'"inLanguage":\s*"(?:en|en-GB|en-US)"')
_HREFLANG_ARTICLE_RE = re.compile(r'href="/(\d{4}-\d{2}-\d{2}-[^/"]+)/"')

LOCALES_NON_EN = (
    "ar", "bn", "cs", "de", "es", "fil", "fr", "ha", "he", "hi", "hu",
    "id", "it", "ja", "ko", "nl", "pl", "pt-br", "ro", "ru", "sv",
    "th", "tr", "uk", "vi", "yo", "zh-hans", "zh-hant",
)


def _esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#x27;")
    )




def _load_taxonomy() -> tuple[dict, dict[str, str]]:
    """Return (taxonomy, alias→canonical-slug map). Empty when missing."""
    if yaml is None or not TAXONOMY.is_file():
        return {}, {}
    taxonomy = yaml.safe_load(TAXONOMY.read_text(encoding="utf-8")) or {}
    return taxonomy, _alias_map(taxonomy)






# Tiny per-card share rail — 5 monochrome SVG glyphs (X, LinkedIn, Facebook,
# WhatsApp, email). Shorter than the article-level rail (no Bluesky, no copy-
# link) because cards are dense and the 5 anchors fit 16px row at 44px touch
# target.


def _card_share_rail(url: str, title: str, desc: str) -> str:
    """Render a 6-icon per-card share rail (X / LinkedIn / Facebook /
    WhatsApp / email / copy-link). Anchors only — CSP-safe — and the
    copy-link button is a ``<button data-copy-link>`` that main.js
    wires to ``navigator.clipboard.writeText(href)`` with a textarea
    fallback for insecure contexts."""
    abs_url = url if url.startswith("http") else f"{_BASE_URL}{url}"
    x_text = f"{title}\n\n{abs_url}"
    li_text = "\n\n".join(p for p in (title, desc, abs_url) if p)
    wa_text = "\n\n".join(p for p in (title, desc, abs_url) if p)
    email_body = "\n\n".join(p for p in (desc, f"Read more: {abs_url}") if p)
    import urllib.parse as _u

    def q(s: str) -> str:
        return _u.quote(s, safe="")

    items = (
        f'<li><a href="https://twitter.com/intent/tweet?text={q(x_text)}" '
        f'rel="noopener noreferrer" aria-label="Share on X">{_CARD_SVG_X}</a></li>'
        f'<li><a href="https://www.linkedin.com/feed/?shareActive=true&text={q(li_text)}" '
        f'rel="noopener noreferrer" aria-label="Share on LinkedIn">{_CARD_SVG_LI}</a></li>'
        f'<li><a href="https://www.facebook.com/sharer/sharer.php?u={q(abs_url)}" '
        f'rel="noopener noreferrer" aria-label="Share on Facebook">{_CARD_SVG_FB}</a></li>'
        f'<li><a href="https://wa.me/?text={q(wa_text)}" '
        f'rel="noopener noreferrer" aria-label="Share on WhatsApp">{_CARD_SVG_WA}</a></li>'
        f'<li><a href="mailto:?subject={q(title)}&body={q(email_body)}" '
        f'aria-label="Share by email">{_CARD_SVG_EMAIL}</a></li>'
        f'<li><button type="button" data-copy-link="{_esc(abs_url)}" '
        f'aria-label="Copy link">{_CARD_SVG_LINK}</button></li>'
    )
    # `<div role="group">` instead of `<nav>` — every card emits a
    # share rail, so 24 `<nav aria-label="Share this article">` landmarks
    # per page would all share the same accessible name and trip
    # landmark-unique. role="group" carries semantic intent without
    # contributing a landmark to the page outline.
    return (
        f'<div class="card-share-rail" role="group" aria-label="Share this article">'
        f"<ul>{items}</ul></div>"
    )


def _post_card_fields(
    path: Path,
    taxonomy: dict,
    amap: dict[str, str],
) -> tuple[str, str, str, str, list[str], str, str] | None:
    """Read one dated post's frontmatter and return the tuple of card
    fields: (title, iso-date, slug, excerpt, pillars, banner-url,
    banner-alt). Returns None when the file isn't a dated article."""
    stem_m = _DATED_SLUG_RE.match(path.stem)
    if not stem_m:
        return None
    text = path.read_text(encoding="utf-8", errors="ignore")
    title_m = _TITLE_FM_RE.search(text)
    excerpt_m = _EXCERPT_FM_RE.search(text)
    desc_m = _DESC_FM_RE.search(text)
    banner_m = _BANNER_FM_RE.search(text)
    banner_alt_m = _BANNER_ALT_FM_RE.search(text)
    pillars = _post_pillars(text, taxonomy, amap) if taxonomy else []
    title = title_m.group(1) if title_m else path.stem
    # Excerpt > description > "" — most posts have only description.
    excerpt = (
        excerpt_m.group(1)
        if excerpt_m
        else (desc_m.group(1) if desc_m else "")
    )
    banner = banner_m.group(1) if banner_m else _DEFAULT_BANNER
    banner_alt = banner_alt_m.group(1) if banner_alt_m else title
    return (title, stem_m.group(1), path.stem, excerpt, pillars, banner, banner_alt)


def _walk_posts() -> list[tuple[str, str, str, str, list[str], str, str]]:
    """Return [(title, iso-date, slug, excerpt, pillars, banner,
    banner_alt), …] for every dated post, newest first. Pillars drive
    the filter data-category; banner + alt feed the FT-tier card."""
    taxonomy, amap = _load_taxonomy()
    out: list[tuple[str, str, str, str, list[str], str, str]] = []
    for path in sorted(POSTS.glob("*.md")):
        rec = _post_card_fields(path, taxonomy, amap)
        if rec is not None:
            out.append(rec)
    out.sort(key=lambda p: p[1], reverse=True)
    return out








def _load_static_slug(lang: str, key: str, default: str) -> str:
    """Return ``static.<key>`` from a locale's slugs.json, with default."""
    path = ROOT / "_data" / "i18n" / lang / "slugs.json"
    if not path.is_file():
        return default
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default
    return (data.get("static") or {}).get(key) or default




def _render_card(
    title: str,
    iso_date: str,
    slug: str,
    excerpt: str,
    pillars: list[str] | None = None,
    banner: str = _DEFAULT_BANNER,
    banner_alt: str = "",
    *,
    href_override: str | None = None,
    eyebrow_override: str | None = None,
    featured: bool = False,
) -> str:
    """Render one FT-tier ``article.tag-landing-card`` — image left,
    eyebrow + headline + date + excerpt right. Pillar-derived eyebrow
    is rendered in caps using the first pillar (or "Editorial" if the
    post has no canonical pillar). On locale forks, ``href_override``
    swaps the article URL to ``/<lang>/<locale-slug>/`` and
    ``eyebrow_override`` swaps the pillar caption to its translation."""
    excerpt_html = (
        f'<p class="card-excerpt">{_esc(excerpt)}</p>' if excerpt else ""
    )
    year_attr = f' data-year="{iso_date[:4]}"' if iso_date else ""
    cat_attr = f' data-category="{" ".join(pillars)}"' if pillars else ""
    eyebrow = eyebrow_override or (
        PILLAR_LABELS[pillars[0]] if pillars else "Editorial"
    )
    eyebrow_html = f'<p class="eyebrow card-eyebrow">{_esc(eyebrow).upper()}</p>'
    href = href_override or f"/{slug}/"
    safe_alt = banner_alt or title
    img_html = (
        f'<a class="card-media" href="{href}" tabindex="-1" aria-hidden="true">'
        f'<img src="{banner}" alt="{_esc(safe_alt)}" loading="lazy" '
        f'decoding="async" width="800" height="800" />'
        f"</a>"
    )
    share_html = _card_share_rail(href, title, excerpt)
    body_html = (
        f'<div class="card-body">'
        f"{eyebrow_html}"
        f'<h2><a href="{href}">{_esc(title)}</a></h2>'
        f'<time datetime="{iso_date}" class="card-date">{iso_date}</time>'
        f"{excerpt_html}"
        f"{share_html}"
        f"</div>"
    )
    featured_class = " tag-landing-card--featured" if featured else ""
    return (
        f'<article class="tag-landing-card tag-landing-card--ft{featured_class}"{year_attr}{cat_attr}>'
        f"{img_html}{body_html}"
        f"</article>"
    )


def _render_filter_form(
    pillar_options: list[tuple[str, str]],
    year_options: list[str],
    nav_base: str = "/articles",
) -> str:
    """Two native <select>s + an empty-state region. main.js wires the
    `change` event to update data-filter-* attributes on the list."""
    pillar_opts = '<option value="">All categories</option>' + "".join(
        f'<option value="{slug}">{_esc(label)}</option>'
        for slug, label in pillar_options
    )
    year_opts = '<option value="">All years</option>' + "".join(
        f'<option value="{year}">{year}</option>' for year in year_options
    )
    # `<div role="search">` rather than `<form>` — there's no submit
    # target (selects fire JS change events that mutate the list's
    # data attributes), and a form-without-submit-button trips
    # WCAG H32.2 AAA. The role keeps SR announcement as "search".
    #
    # The Year selector navigates rather than filtering in place: the
    # paged listing only shows the current page's 24 cards, so a
    # client-side year filter on page 1 would always miss the corpus's
    # older articles. `data-filter-mode="navigate"` tells main.js to
    # jump to `<nav_base>/<year>/` (the dedicated year archive) instead
    # of mutating data-filter-year. Category stays client-side because
    # categories are mixed across years on every page.
    return (
        '<div class="listing-filters" role="search" aria-label="Filter articles">'
        '<label>Category'
        f'<select data-filter-target="category" name="category">{pillar_opts}</select>'
        '</label>'
        '<label>Year'
        f'<select data-filter-target="year" data-filter-mode="navigate" '
        f'data-navigate-base="{nav_base}" '
        f'name="year">{year_opts}</select>'
        '</label>'
        '</div>'
    )


def _render_pagination(
    page: int, total_pages: int, base_path: str
) -> str:
    """Render a Prev/numbered/Next pagination nav. ``base_path`` is the
    URL prefix (no trailing slash) — e.g. ``/articles`` for EN or
    ``/fr/articles`` for FR locale. Page 1 lives at ``<base_path>/``;
    page N lives at ``<base_path>/page/N/``."""
    if total_pages <= 1:
        return ""

    def page_url(n: int) -> str:
        return f"{base_path}/" if n == 1 else f"{base_path}/page/{n}/"

    parts: list[str] = []
    if page > 1:
        parts.append(
            f'<a href="{page_url(page - 1)}" rel="prev" class="page-nav-prev">'
            "&larr; Previous"
            "</a>"
        )
    nums: list[str] = []
    for n in range(1, total_pages + 1):
        if n == page:
            nums.append(
                f'<span class="page-nav-num is-current" aria-current="page">{n}</span>'
            )
        else:
            nums.append(f'<a href="{page_url(n)}" class="page-nav-num">{n}</a>')
    parts.append(f'<span class="page-nav-pages">{"".join(nums)}</span>')
    if page < total_pages:
        parts.append(
            f'<a href="{page_url(page + 1)}" rel="next" class="page-nav-next">'
            "Next &rarr;"
            "</a>"
        )
    return (
        f'<nav class="page-nav" aria-label="Pagination">{"".join(parts)}</nav>'
    )


def _render_listing_body(
    page: int,
    total_pages: int,
    page_posts: list[tuple[str, str, str, str, list[str], str, str]],
    base_path: str,
    page_label: str,
    title: str,
    all_years: list[str],
) -> str:
    cards = "".join(
        _render_card(*p, featured=(page == 1 and i == 0))
        for i, p in enumerate(page_posts)
    )
    pagination = _render_pagination(page, total_pages, base_path)
    pillar_options = [(p, PILLAR_LABELS[p]) for p in PILLAR_ORDER]
    filter_form = _render_filter_form(pillar_options, all_years, nav_base=base_path)
    return (
        f'<div class="wrap report-wrap">'
        f'<header class="tag-landing-hero">'
        f'<p class="eyebrow">FEED</p>'
        f"<h1>{_esc(title)}</h1>"
        f'<p class="tag-landing-meta">{page_label} · '
        f'<span id="listing-count">{len(page_posts)}</span> visible</p>'
        f"</header>"
        f"{filter_form}"
        f'<section class="tag-landing-list" aria-label="Article cards">'
        f"{cards}"
        f"</section>"
        f'<p class="listing-empty" role="status">No articles match the current filters.</p>'
        f"{pagination}"
        f"</div>"
    )


def _swap_head(
    out: str,
    title: str,
    desc: str,
    canonical_url: str,
) -> str:
    out = _TITLE_RE.sub(f"<title>{_esc(title)}</title>", out, count=1)
    out = _DESC_RE.sub(
        f'<meta name="description" content="{_esc(desc)}"', out, count=1
    )
    out = _CANONICAL_RE.sub(
        f'<link rel="canonical" href="{canonical_url}"', out, count=1
    )
    out = _OG_TITLE_RE.sub(
        f'<meta property="og:title" content="{_esc(title)}"', out, count=1
    )
    out = _OG_DESC_RE.sub(
        f'<meta property="og:description" content="{_esc(desc)}"', out, count=1
    )
    out = _OG_URL_RE.sub(
        f'<meta property="og:url" content="{canonical_url}"', out, count=1
    )
    return out


def _render_page_html(
    template: str,
    page: int,
    total_pages: int,
    page_posts: list[tuple[str, str, str, str, list[str], str, str]],
    canonical_url: str,
    base_path: str,
    title: str,
    all_years: list[str],
) -> str:
    page_label = f"Page {page} of {total_pages}"
    desc = (
        f"Articles by Sebastien Rousseau on AI, payments, post-quantum "
        f"cryptography, and the technology of banking. {page_label}."
    )
    body = _render_listing_body(
        page, total_pages, page_posts, base_path, page_label, title, all_years
    )
    out = _swap_head(template, title, desc, canonical_url)
    out = _AP_HERO_BLOCK_RE.sub("", out, count=1)
    out = _MAIN_RE.sub(rf"\1{body}\3", out, count=1)
    return out




_TAG_LANDING_LIST_RE = re.compile(
    r'(<section class="tag-landing-list"[^>]*>)([\s\S]*?)(</section>)',
    re.IGNORECASE,
)


def _localised_card(
    card: tuple[str, str, str, str, list[str], str, str],
    lang: str,
    locale_index: dict[str, tuple[str, str, str, str]],
    featured: bool = False,
) -> str:
    """Render one card with locale-translated title + excerpt + URL +
    eyebrow when ``locale_index`` has a matching entry for the EN slug;
    fall back to EN content otherwise."""
    title, iso_date, slug, excerpt, pillars, banner, banner_alt = card
    locale_entry = locale_index.get(slug)
    if locale_entry is not None:
        locale_slug, locale_title, locale_excerpt, locale_banner = locale_entry
        title = locale_title
        excerpt = locale_excerpt or excerpt
        banner = locale_banner or banner
        href = f"/{lang}/{locale_slug}/"
    else:
        href = f"/{lang}/{slug}/"
    eyebrow = (
        PILLAR_LABELS[pillars[0]] if pillars else "Editorial"
    )
    return _render_card(
        title, iso_date, slug, excerpt, pillars, banner, banner_alt,
        href_override=href,
        eyebrow_override=eyebrow,
        featured=featured,
    )


def _swap_locale_cards(
    html: str,
    lang: str,
    page_posts: list[tuple[str, str, str, str, list[str], str, str]],
    locale_index: dict[str, tuple[str, str, str, str]],
    feature_first: bool = False,
) -> str:
    """Replace the EN card grid inside ``<section class="tag-landing-
    list">`` with the locale-translated card grid. Posts without a
    locale frontmatter fall back to the EN card (rendered with locale
    URL anyway). When ``feature_first`` is True, the newest card gets
    the featured (2-column-spanning) treatment — used on page-1 paged
    listings, not year archives."""
    body = "".join(
        _localised_card(card, lang, locale_index, featured=(feature_first and i == 0))
        for i, card in enumerate(page_posts)
    )
    return _TAG_LANDING_LIST_RE.sub(rf"\1{body}\3", html, count=1)


def _write_locale_page(
    en_html: str,
    lang: str,
    page: int,
    article_map: dict[str, str],
    locale_prefix: str,
    out_path: Path,
    page_posts: list[tuple[str, str, str, str, list[str], str, str]] | None = None,
    locale_index: dict[str, tuple[str, str, str, str]] | None = None,
) -> None:
    """Rewrite an EN page into one locale variant: <html lang>,
    canonical, internal links, og:url, JSON-LD inLanguage, chrome,
    and (when ``page_posts`` is supplied) the card grid translated
    via per-locale frontmatter."""
    out = en_html
    out = _HTML_LANG_RE.sub(f'<html lang="{lang}"', out, count=1)
    canonical = f"{_BASE_URL}/{lang}/{locale_prefix}/"
    if page > 1:
        canonical += f"page/{page}/"
    out = _CANONICAL_RE.sub(
        f'<link rel="canonical" href="{canonical}"', out, count=1
    )
    out = _OG_URL_RE.sub(
        f'<meta property="og:url" content="{canonical}"', out, count=1
    )

    def _swap_article(m: re.Match[str], _lang: str = lang, _amap: dict = article_map) -> str:
        en_slug = m.group(1)
        return f'href="/{_lang}/{_amap.get(en_slug, en_slug)}/"'

    out = _HREFLANG_ARTICLE_RE.sub(_swap_article, out)
    # The per-page pagination links (/articles/page/N/) → localised.
    out = out.replace('href="/articles/', f'href="/{lang}/{locale_prefix}/')
    out = _INLANG_RE.sub(f'"inLanguage":"{lang}"', out)
    if page_posts is not None and locale_index is not None:
        out = _swap_locale_cards(
            out, lang, page_posts, locale_index,
            feature_first=(page == 1),
        )
    out = _translate_chrome_for(lang, out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(out, encoding="utf-8")


def _chunk(seq: list, size: int) -> list[list]:
    return [seq[i : i + size] for i in range(0, len(seq), size)]


def _group_by_year(
    posts: list[tuple[str, str, str, str, list[str], str, str]],
) -> dict[str, list[tuple[str, str, str, str, list[str], str, str]]]:
    groups: dict[str, list[tuple[str, str, str, str, list[str], str, str]]] = {}
    for p in posts:
        year = p[1][:4]
        groups.setdefault(year, []).append(p)
    return groups


def _render_year_filter_form(
    pillar_options: list[tuple[str, str]],
    year_options: list[str],
    current_year: str,
    nav_base: str = "/articles",
) -> str:
    """Filter form for year archives. Year select defaults to the
    current archive's year and exposes "All articles" as the way out —
    picking it navigates back to ``<nav_base>/``."""
    pillar_opts = '<option value="">All categories</option>' + "".join(
        f'<option value="{slug}">{_esc(label)}</option>'
        for slug, label in pillar_options
    )
    year_opts = '<option value="">All years</option>' + "".join(
        f'<option value="{y}"{" selected" if y == current_year else ""}>{y}</option>'
        for y in year_options
    )
    return (
        '<div class="listing-filters" role="search" aria-label="Filter articles">'
        '<label>Category'
        f'<select data-filter-target="category" name="category">{pillar_opts}</select>'
        '</label>'
        '<label>Year'
        f'<select data-filter-target="year" data-filter-mode="navigate" '
        f'data-navigate-base="{nav_base}" '
        f'name="year">{year_opts}</select>'
        '</label>'
        '</div>'
    )


def _render_year_body(
    year: str,
    posts_for_year: list[tuple[str, str, str, str, list[str], str, str]],
    all_years: list[str],
) -> str:
    cards = "".join(_render_card(*p) for p in posts_for_year)
    n = len(posts_for_year)
    pillar_options = [(p, PILLAR_LABELS[p]) for p in PILLAR_ORDER]
    filter_form = _render_year_filter_form(pillar_options, all_years, year)
    return (
        f'<div class="wrap report-wrap">'
        f'<header class="tag-landing-hero">'
        f'<p class="eyebrow"><a href="/articles/">&larr; All articles</a></p>'
        f"<h1>Articles — {year}</h1>"
        f'<p class="tag-landing-meta">{n} article{"s" if n != 1 else ""}</p>'
        f"</header>"
        f"{filter_form}"
        f'<section class="tag-landing-list" aria-label="Articles published in {year}">'
        f"{cards}"
        f"</section>"
        f'<p class="listing-empty" role="status">No articles match the current filters.</p>'
        f"</div>"
    )


def _write_year_archives(
    template: str,
    posts: list[tuple[str, str, str, str, list[str], str, str]],
) -> tuple[int, int]:
    by_year = _group_by_year(posts)
    all_years = sorted(by_year.keys(), reverse=True)
    en_pages: list[tuple[str, str, list[tuple[str, str, str, str, list[str], str, str]]]] = []
    for year, year_posts in sorted(by_year.items(), reverse=True):
        canonical = f"{_BASE_URL}/articles/{year}/"
        title = f"Articles — {year}"
        desc = (
            f"All articles published by Sebastien Rousseau in {year}. "
            f"{len(year_posts)} articles on AI, payments, post-quantum "
            f"cryptography, and the technology of banking."
        )
        out = _swap_head(template, title, desc, canonical)
        out = _AP_HERO_BLOCK_RE.sub("", out, count=1)
        out = _MAIN_RE.sub(
            rf"\1{_render_year_body(year, year_posts, all_years)}\3", out, count=1
        )
        out_path = PUBLIC / "articles" / year / "index.html"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(out, encoding="utf-8")
        en_pages.append((year, out, year_posts))

    locale_written = 0
    article_maps = {lang: _load_locale_article_slugs(lang) for lang in LOCALES_NON_EN}
    locale_prefixes = {
        lang: _load_static_slug(lang, "articles", "articles") for lang in LOCALES_NON_EN
    }
    locale_indexes = {lang: _load_locale_post_index(lang) for lang in LOCALES_NON_EN}
    for year, en_html, year_posts in en_pages:
        for lang in LOCALES_NON_EN:
            prefix = locale_prefixes[lang]
            out_path = PUBLIC / lang / prefix / year / "index.html"
            out = en_html
            out = _HTML_LANG_RE.sub(f'<html lang="{lang}"', out, count=1)
            canonical = f"{_BASE_URL}/{lang}/{prefix}/{year}/"
            out = _CANONICAL_RE.sub(
                f'<link rel="canonical" href="{canonical}"', out, count=1
            )
            out = _OG_URL_RE.sub(
                f'<meta property="og:url" content="{canonical}"', out, count=1
            )
            amap = article_maps[lang]

            def _swap_article(m: re.Match[str], _lang: str = lang, _amap: dict = amap) -> str:
                en_slug = m.group(1)
                return f'href="/{_lang}/{_amap.get(en_slug, en_slug)}/"'

            out = _HREFLANG_ARTICLE_RE.sub(_swap_article, out)
            out = out.replace('href="/articles/', f'href="/{lang}/{prefix}/')
            out = _INLANG_RE.sub(f'"inLanguage":"{lang}"', out)
            out = _swap_locale_cards(out, lang, year_posts, locale_indexes[lang])
            out = _translate_chrome_for(lang, out)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(out, encoding="utf-8")
            locale_written += 1
    return len(en_pages), locale_written


def _write_en_paged(
    template: str,
    pages: list[list[tuple[str, str, str, str, list[str], str, str]]],
    all_years: list[str],
) -> list[tuple[int, str, list[tuple[str, str, str, str, list[str], str, str]]]]:
    """Write each English paged listing to /articles/[page/N/]index.html
    and return ``(page-number, rendered-html, page_posts)`` triples so
    the locale-fork pass can re-render the cards in each language."""
    total_pages = len(pages)
    out: list[tuple[int, str, list[tuple[str, str, str, str, list[str], str, str]]]] = []
    for idx, page_posts in enumerate(pages, start=1):
        canonical = (
            f"{_BASE_URL}/articles/"
            if idx == 1
            else f"{_BASE_URL}/articles/page/{idx}/"
        )
        page_html = _render_page_html(
            template,
            idx,
            total_pages,
            page_posts,
            canonical,
            "/articles",
            "Articles",
            all_years,
        )
        out_path = (
            PUBLIC / "articles" / "index.html"
            if idx == 1
            else PUBLIC / "articles" / "page" / str(idx) / "index.html"
        )
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(page_html, encoding="utf-8")
        out.append((idx, page_html, page_posts))
    return out


def _write_listings() -> tuple[int, int, int, int]:
    if not TEMPLATE_PATH.is_file():
        print(
            f"build_listings: missing template {TEMPLATE_PATH}",
            file=sys.stderr,
        )
        return 0, 0, 0, 0
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    posts = _walk_posts()
    year_en, year_locale = _write_year_archives(template, posts)
    pages = _chunk(posts, PAGE_SIZE)
    all_years = sorted({p[1][:4] for p in posts}, reverse=True)
    en_pages = _write_en_paged(template, pages, all_years)

    locale_written = 0
    article_maps = {lang: _load_locale_article_slugs(lang) for lang in LOCALES_NON_EN}
    locale_prefixes = {
        lang: _load_static_slug(lang, "articles", "articles") for lang in LOCALES_NON_EN
    }
    locale_indexes = {lang: _load_locale_post_index(lang) for lang in LOCALES_NON_EN}
    for idx, en_html, page_posts in en_pages:
        for lang in LOCALES_NON_EN:
            prefix = locale_prefixes[lang]
            out_path = (
                PUBLIC / lang / prefix / "index.html"
                if idx == 1
                else PUBLIC / lang / prefix / "page" / str(idx) / "index.html"
            )
            _write_locale_page(
                en_html, lang, idx, article_maps[lang], prefix, out_path,
                page_posts=page_posts,
                locale_index=locale_indexes[lang],
            )
            locale_written += 1
    return len(en_pages), locale_written, year_en, year_locale


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    en_written, locale_written, year_en, year_locale = _write_listings()
    print(
        f"build_listings: wrote {en_written} EN paged listing(s) + "
        f"{locale_written} locale fork(s); "
        f"{year_en} EN year archive(s) + {year_locale} locale fork(s) "
        f"across {len(LOCALES_NON_EN)} non-EN locales."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
