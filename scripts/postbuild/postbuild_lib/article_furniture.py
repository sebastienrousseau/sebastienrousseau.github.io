"""Article UI furniture + nav + hreflang lookups.

Owns every per-page transform applied AFTER the SEO + JSON-LD passes:

* tag badges + meta bar (author / dates / read time) after the H1
* anchor links on every H2/H3 inside <main>
* table-of-contents sidebar for posts with >= 5 H2 sections
* FAQ <p><strong>Q?</strong></p><p>A</p> → collapsible <details qa-item>
* citation graph as visible <ol> at the bottom of dated posts
* sources list extracted from outbound links
* mermaid block rendering
* prev/next nav with active-link marker
* speculation rules
* hoist body-level <link rel=stylesheet> into <head>

Plus the lang/slug helpers used by the hreflang pass:
* _all_active_non_en_langs / _slug_maps / _translated_slugs* /
  _resolve_en_slug / _alternates_for_en_slug.

Pure functions over HTML strings; module-level state is regex
constants + author identity constants only.
"""

from __future__ import annotations

import json as _json
import re
import sys
from html import escape as _esc
from html import unescape as _unesc
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

# _fr_slugs is deprecated
from postbuild_lib.seo import _keywords_re

PUBLIC = Path("public")


# ---------------------------------------------------------------------------
# 7. Article UI furniture
#    - tag badges + meta bar (author / dates / read time) after the H1
#    - anchor links on every H2/H3 inside <main>
#    - table-of-contents sidebar for posts with ≥5 H2 sections
#    - citation graph in BlogPosting JSON-LD for outbound links to known
#      authoritative domains
# ---------------------------------------------------------------------------

# Domains we accept as primary-source citations for AI grounding.

# Author meta shared across every dated post. Single source of truth.
AUTHOR_NAME = "Sebastien Rousseau"
AUTHOR_AVATAR = "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp"
AUTHOR_URL = "/about/index.html"

_HERO_RE = re.compile(
    r'(<section class="ap-hero">\s*'
    r'(?:<p class="eyebrow">[^<]*</p>\s*)?'
    r'<h1>[^<]*</h1>\s*'
    r'(?:<p class="sub[^"]*">[^<]*</p>\s*)?'
    r")(</section>)",
    re.IGNORECASE,
)
_MAIN_RE = re.compile(
    r'(<main\b[^>]*>\s*<div class="wrap[^"]*">)([\s\S]*?)(</div>\s*</main>)',
    re.IGNORECASE,
)
_BLOGPOSTING_DATES_RE = re.compile(
    r'"datePublished":"([^"]+)"[^"]*"dateModified":"([^"]+)"',
)
_WORDCOUNT_RE = re.compile(r'"wordCount":(\d+)')
_HEADING_RE = re.compile(r'<(h[23])(?:\s+id="[^"]*")?>([\s\S]*?)</\1>', re.IGNORECASE)
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from _core import DATED_SLUG_RE as _DATED_SLUG_RE  # canonical dated-slug matcher
from postbuild_lib._i18n import (  # noqa: F401 — i18n base; several are re-exports
    _HTML_LANG_DETECT_RE,
    _LABEL_CACHE,
    _SLUG_MAPS_CACHE,
    LABELS_EN,
    _all_active_non_en_langs,
    _detect_page_lang,
    _labels,
    _labels_for_lang,
    _slug_maps,
    _slug_maps_for,
)

_H1_RE = re.compile(
    r'<section class="ap-hero">\s*'
    r'(?:<p class="eyebrow">[^<]*</p>\s*)?'
    r"<h1>([^<]+)</h1>",
    re.IGNORECASE,
)


def _is_french(html: str) -> bool:
    m = _HTML_LANG_DETECT_RE.search(html)
    return bool(m and m.group(1).lower().startswith("fr"))


# Furniture string tables — labels emitted in <main>'s reader-facing chrome.
# English defaults stay verbatim; the French dict mirrors I18N_FR in
# build_translations.py.
LABELS_FR: dict[str, str] = {
    "Published": "Publié le",
    "Updated": "Mis à jour le",
    "min read": "min de lecture",
    "Previous": "Précédent",
    "Next": "Suivant",
    "Sources & references": "Sources et références",
    "Contents": "Sommaire",
    "Article pagination": "Pagination des articles",
    "Estimated read time": "Temps de lecture estimé",
    "Link to": "Lien vers",
    "Table of contents": "Table des matières",
    "Topics": "Sujets",
    "Home": "Accueil",
    "Breadcrumb": "Fil d'Ariane",
}










def slugify(s: str) -> str:
    import unicodedata as _ud

    s = re.sub(r"<[^>]+>", "", s).strip().lower()
    s = re.sub(r"&[a-z0-9#]+;", " ", s)
    # Fold accented letters to ASCII so "Références" -> "references", not
    # "r-f-rences". NFKD normalization decomposes é -> e + combining
    # acute; the combining mark is dropped by the [^a-z0-9]+ pass below.
    s = _ud.normalize("NFKD", s)
    s = s.encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:80]


_FR_MONTHS = {
    1: "janv.",
    2: "févr.",
    3: "mars",
    4: "avr.",
    5: "mai",
    6: "juin",
    7: "juil.",
    8: "août",
    9: "sept.",
    10: "oct.",
    11: "nov.",
    12: "déc.",
}


def _fmt_date(iso_or_rfc: str, french: bool = False) -> str:
    """Render a date string as 'D Mon YYYY' (English) or 'D mois YYYY'
    (French). Accepts ISO 8601 or RFC 822. Returns input unchanged on
    parse failure."""
    iso_or_rfc = iso_or_rfc.strip()
    from datetime import datetime as _dt

    for fmt in (
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%d",
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S %Z",
    ):
        try:
            dt = _dt.strptime(iso_or_rfc, fmt)
        except ValueError:
            continue
        if french:
            return f"{dt.day} {_FR_MONTHS[dt.month]} {dt.year}"
        return dt.strftime("%-d %b %Y")
    return iso_or_rfc


_TAGS_PATH_BY_LANG: dict[str, str] = {
    "en": "/tags",
    "ar": "/ar/wusum",
    "bn": "/bn/tag",
    "cs": "/cs/stitky",
    "de": "/de/etiketten",
    "es": "/es/etiquetas",
    "fil": "/fil/mga-tag",
    "fr": "/fr/etiquettes",
    "ha": "/ha/tags",
    "he": "/he/tagim",
    "hi": "/hi/tag",
    "id": "/id/label",
    "it": "/it/etichette",
    "ja": "/ja/tagu",
    "ko": "/ko/taegeu",
    "nl": "/nl/labels",
    "pl": "/pl/tagi",
    "pt-br": "/pt-br/etiquetas",
    "ro": "/ro/etichete",
    "ru": "/ru/tegi",
    "sv": "/sv/taggar",
    "th": "/th/thaek",
    "tr": "/tr/etiketler",
    "uk": "/uk/tegy",
    "vi": "/vi/the",
    "yo": "/yo/awon-ami",
    "zh-hans": "/zh-hans/biaoqian",
    "zh-hant": "/zh-hant/biaoqian-tw",
}


_LANDING_PUBLIC = Path(__file__).resolve().parents[3] / "public"


def _has_landing(slug: str, lang: str = "en") -> bool:
    """True iff ``public/<locale-tags-prefix>/<slug>/index.html`` exists
    on disk. Built by build_tag_landings.py only for canonical tags with
    at least ``_LANDING_THRESHOLD`` posts (currently 3), so this lets the
    chip strip skip the link wrapper for sub-threshold tags rather than
    emitting a /tags/<slug>/ link that would 404 the strict-internal
    link audit."""
    prefix = _TAGS_PATH_BY_LANG.get(lang, "/tags").lstrip("/")
    return (_LANDING_PUBLIC / prefix / slug / "index.html").is_file()


def _render_tag_badges(keywords: list[str], labels: dict[str, str], lang: str = "en") -> str:
    """Render the hero tag-chip strip. Links point at the per-tag
    landings ``/<locale-tags>/<slug>/`` (WS3) when one exists; tags
    with no landing (sub-threshold canonicals + non-canonical aliases)
    render as plain ``<span>`` chips so the audit doesn't flag a 404."""
    if not keywords:
        return ""
    prefix = _TAGS_PATH_BY_LANG.get(lang, "/tags")
    badges_html: list[str] = []
    for k in keywords:
        slug = slugify(k)
        if _has_landing(slug, lang):
            badges_html.append(
                f'<a href="{prefix}/{slug}/" class="article-tag" rel="tag">{k}</a>'
            )
        else:
            badges_html.append(f'<span class="article-tag">{k}</span>')
    aria = labels.get("Topics", "Topics")
    return f'<nav class="article-tags" aria-label="{aria}">{"".join(badges_html)}</nav>'


def _render_meta_bar(
    date_pub: str, date_mod: str, word_count: int | None, labels: dict[str, str], lang: str = "en"
) -> str:
    parts: list[str] = []
    french = labels is LABELS_FR
    author_url = "/fr/a-propos/index.html" if lang == "fr" else AUTHOR_URL
    alt_text = f"Portrait de {AUTHOR_NAME}" if lang == "fr" else f"Portrait of {AUTHOR_NAME}"
    parts.append(
        f'<a href="{author_url}" class="article-author" rel="author">'
        f'<img alt="{alt_text}" src="{AUTHOR_AVATAR}" '
        f'width="36" height="36" loading="lazy" decoding="async" />'
        f"<span>{AUTHOR_NAME}</span></a>"
    )
    if date_pub:
        parts.append(
            f'<time datetime="{date_pub}" class="meta-pub">'
            f'{labels["Published"]} {_fmt_date(date_pub, french)}</time>'
        )
    # Suppress "Updated" when the modification date is the same as or
    # earlier than the publication date — otherwise a post scheduled into
    # the future shows a nonsensical "Updated before Published" stamp.
    if date_mod and date_mod[:10] > date_pub[:10]:
        parts.append(
            f'<time datetime="{date_mod}" class="meta-rev">'
            f'{labels["Updated"]} {_fmt_date(date_mod, french)}</time>'
        )
    if word_count:
        read_min = max(1, round(word_count / 220))
        parts.append(
            f'<span class="meta-read" aria-label="{labels["Estimated read time"]}">'
            f'{read_min} {labels["min read"]}</span>'
        )
    return (
        '<div class="article-meta">' + ' <span aria-hidden="true">·</span> '.join(parts) + "</div>"
    )


# ---------------------------------------------------------------------------
# Sigstore attestation footer (gated on _data/sigstore/config.json)
# ---------------------------------------------------------------------------
#
# When ``scripts/sigstore_sign.py`` runs (which only happens if
# ``_data/sigstore/config.json`` exists), it writes a Sigstore bundle
# per article under ``public/sigstore/<slug>.bundle``. This injector
# adds a small footer attestation badge to articles that have a
# matching bundle. The badge links to the bundle + the public-key
# verify command so any reader can confirm the page bytes match what
# the author signed.

_SIGSTORE_CONFIG_PRESENT: bool = Path("_data/sigstore/config.json").is_file()


def inject_sigstore_attestation(html: str, slug: str) -> str:
    """Insert a 'Signed · cosign' badge near the article footer when a
    Sigstore bundle exists for this slug. No-op otherwise."""
    if not _SIGSTORE_CONFIG_PRESENT:
        return html
    if '"@type":"BlogPosting"' not in html:
        return html
    bundle = PUBLIC / "sigstore" / f"{slug}.bundle"
    if not bundle.is_file():
        return html
    if 'class="article-sigstore"' in html:
        return html  # idempotent
    is_fr = _is_french(html)
    label = (
        "Signature Sigstore · vérifiable avec cosign"
        if is_fr
        else "Sigstore signature · verifiable with cosign"
    )
    badge = (
        f'<aside class="article-sigstore" aria-label="{label}">'
        f'<a href="/sigstore/{slug}.bundle" rel="external" '
        f'type="application/vnd.dev.sigstore.bundle+json">'
        f"🔏 {label}</a></aside>"
    )
    # Insert just before the existing article furniture's end-of-main.
    return re.sub(r"(</main>)", badge + r"\1", html, count=1)


def _extract_article_metadata(html: str) -> tuple[list[str], str, str, int | None]:
    """Pull the inputs ``inject_article_furniture`` needs out of the page:
    keyword list, datePublished, dateModified, wordCount."""
    keywords: list[str] = []
    m = _keywords_re.search(html)
    if m and m.group(1):
        keywords = [k.strip() for k in m.group(1).split(",") if k.strip()]
    dm = _BLOGPOSTING_DATES_RE.search(html)
    date_pub, date_mod = (dm.group(1), dm.group(2)) if dm else ("", "")
    wm = _WORDCOUNT_RE.search(html)
    word_count = int(wm.group(1)) if wm else None
    return keywords, date_pub, date_mod, word_count


def inject_article_furniture(html: str) -> str:
    """Insert tag badges + meta bar between the H1 hero and the main body.

    Only fires when the page carries a BlogPosting JSON-LD graph — listing /
    static pages are left alone.
    """
    if '"@type":"BlogPosting"' not in html:
        return html
    # Don't double-inject if a previous postbuild run already added them.
    if 'class="article-tags"' in html:
        return html
    keywords, date_pub, date_mod, word_count = _extract_article_metadata(html)
    labels = _labels(html)
    lang = "fr" if _is_french(html) else "en"
    fragment = _render_tag_badges(keywords, labels, lang) + _render_meta_bar(
        date_pub, date_mod, word_count, labels, lang
    )
    if not fragment:
        return html
    return _HERO_RE.sub(rf"\1{fragment}\2", html, count=1)


_LDJSON_BLOCK_RE = re.compile(
    r'<script type="application/ld\+json"[^>]*>([\s\S]*?)</script>',
    re.IGNORECASE,
)
_BASE_URL = "https://sebastienrousseau.com"


def _relativize(url: str) -> str:
    if url.startswith(_BASE_URL):
        return url[len(_BASE_URL) :] or "/"
    return url


def _trail_from_node(node: object) -> list[tuple[str, str]]:
    """Extract a 3-level ``(name, root-relative href)`` trail from one
    JSON-LD node; empty list when the node isn't a well-formed
    ``BreadcrumbList``."""
    if not isinstance(node, dict) or node.get("@type") != "BreadcrumbList":
        return []
    raw = node.get("itemListElement")
    if not isinstance(raw, list) or len(raw) != 3:
        return []
    items: list[tuple[str, str]] = []
    for entry in raw:
        if not isinstance(entry, dict):
            return []
        name, url = entry.get("name"), entry.get("item")
        if not (isinstance(name, str) and isinstance(url, str)):
            return []
        items.append((name, _relativize(url)))
    return items


def _breadcrumb_items(html: str) -> list[tuple[str, str]]:
    """Return the article's ``BreadcrumbList`` as ``[(name, href), …]``
    with hrefs made root-relative. Empty list when no 3-level trail is
    found (listing / static pages) or the JSON-LD is malformed."""
    for m in _LDJSON_BLOCK_RE.finditer(html):
        if '"BreadcrumbList"' not in m.group(1):
            continue
        try:
            data = _json.loads(m.group(1))
        except ValueError:
            continue
        nodes = data.get("@graph", [data]) if isinstance(data, dict) else []
        for node in nodes:
            items = _trail_from_node(node)
            if items:
                return items
    return []




def inject_breadcrumbs(html: str) -> str:
    """Render a visible breadcrumb trail mirroring the page's 3-level
    ``BreadcrumbList`` JSON-LD (Home > Articles > Title), inserted
    directly above the H1 hero. Names and URLs come from the JSON-LD —
    already localized by build_translations — so the visible UI can
    never drift from the structured-data markup."""
    if '"@type":"BlogPosting"' not in html:
        return html
    if 'class="crumbs"' in html:
        return html
    items = _breadcrumb_items(html)
    if not items:
        return html
    aria = _esc(_labels(html).get("Breadcrumb", "Breadcrumb"), quote=True)
    parts = []
    for i, (name, url) in enumerate(items):
        current = ' aria-current="page"' if i == 2 else ""
        parts.append(f'<li><a href="{_esc(url, quote=True)}"{current}>{_esc(name)}</a></li>')
    nav = f'<nav class="crumbs" aria-label="{aria}"><ol>{"".join(parts)}</ol></nav>'
    return html.replace('<section class="ap-hero">', f'{nav}<section class="ap-hero">', 1)


_TABLE_BLOCK_RE = re.compile(r"<table\b[^>]*>[\s\S]*?</table>", re.IGNORECASE)
_THEAD_RE = re.compile(r"<thead\b[\s\S]*?</thead>", re.IGNORECASE)
_TH_TEXT_RE = re.compile(r"<th\b[^>]*>([\s\S]*?)</th>", re.IGNORECASE)
_TR_RE = re.compile(r"<tr\b[\s\S]*?</tr>", re.IGNORECASE)
_TD_OPEN_RE = re.compile(r"<td\b", re.IGNORECASE)
_TABLE_OPEN_RE = re.compile(r"<table\b([^>]*)>", re.IGNORECASE)
_TAG_STRIP_RE = re.compile(r"<[^>]+>")


def _card_label_table(table: str) -> str:
    """Stamp ``data-label="<column header>"`` on every body ``<td>`` and
    tag the table ``table--cards`` so CSS can collapse it into stacked
    cards below 48em. No-op for headerless tables or on re-runs."""
    if "data-label=" in table or "table--cards" in table:
        return table
    head_m = _THEAD_RE.search(table)
    if not head_m:
        return table
    # th text arrives entity-encoded from ssg; unescape before re-escaping
    # so CSS attr() renders "Q&A", not a raw "&amp;" entity.
    headers = [
        _esc(_unesc(_TAG_STRIP_RE.sub("", m.group(1)).strip()), quote=True)
        for m in _TH_TEXT_RE.finditer(head_m.group(0))
    ]
    if not any(headers):
        return table

    def label_row(row_m: re.Match[str]) -> str:
        cell = -1

        def label_td(td_m: re.Match[str]) -> str:
            nonlocal cell
            cell += 1
            if cell >= len(headers) or not headers[cell]:
                return td_m.group(0)
            return f'<td data-label="{headers[cell]}"'

        return _TD_OPEN_RE.sub(label_td, row_m.group(0))

    body = _TR_RE.sub(label_row, table[head_m.end() :])

    def add_class(open_m: re.Match[str]) -> str:
        attrs = open_m.group(1)
        if 'class="' in attrs:
            return f"<table{attrs}>".replace('class="', 'class="table--cards ', 1)
        return f'<table{attrs} class="table--cards">'

    head = _TABLE_OPEN_RE.sub(add_class, table[: head_m.end()], count=1)
    return head + body


def inject_table_labels(html: str) -> str:
    """Make every article table mobile-fluid: per-cell ``data-label``
    attributes (mirroring the column headers) + a ``table--cards``
    class for the card-collapse CSS. BlogPosting pages only."""
    if '"@type":"BlogPosting"' not in html:
        return html
    return _TABLE_BLOCK_RE.sub(lambda m: _card_label_table(m.group(0)), html)


# ---------------------------------------------------------------------------
# WS2 — FT-tier editorial composition
# ---------------------------------------------------------------------------
# Pure additive HTML — no <script> or <style> tags, CSP-safe. Each pass is
# BlogPosting-gated, idempotent, and only reads from data already in the
# built page (canonical URL, og:title, JSON-LD keywords). The translation
# pipeline's _strip_postbuild_furniture in build_translations/_article.py
# strips each tag from EN shells before locale re-render so locale pages
# get re-injected with locale-correct strings, not EN leaks.

_CANONICAL_RE = re.compile(r'<link\s+rel="canonical"\s+href="([^"]+)"', re.IGNORECASE)
_OG_TITLE_RE = re.compile(r'<meta\s+property="og:title"\s+content="([^"]+)"', re.IGNORECASE)
_DESCRIPTION_RE = re.compile(r'<meta\s+name="description"\s+content="([^"]+)"', re.IGNORECASE)
_AP_HERO_OPEN_RE = re.compile(r'(<section class="ap-hero">)(\s*)(<h1>)', re.IGNORECASE)
_LI_CONTENT_RE = re.compile(r'<li>(.*?)</li>', re.IGNORECASE | re.DOTALL)
_SUB_PARA_RE = re.compile(r'<p class="sub">', re.IGNORECASE)
_WRAP_CLOSE_RE = re.compile(r"(</div>\s*</main>)", re.IGNORECASE)

# 16x16 monochrome SVG glyphs — currentColor so .share-rail can theme them.
_SVG_WA = (
    '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false">'
    '<path d="M8 1C4.13 1 1 4.13 1 8c0 1.27.34 2.46.93 3.5L1 15l3.6-.93C5.62 14.66 6.79 15 8 15c3'
    '.87 0 7-3.13 7-7s-3.13-7-7-7zm0 12.7c-1.06 0-2.05-.29-2.9-.78l-.2-.12-2.13.56.57-2.08-.13-.21'
    'A5.69 5.69 0 012.3 8c0-3.14 2.56-5.7 5.7-5.7s5.7 2.56 5.7 5.7-2.56 5.7-5.7 5.7zm3.1-4.27c-.17'
    '-.08-1-.5-1.16-.55-.16-.06-.27-.08-.39.08-.11.17-.44.55-.54.66-.1.11-.2.13-.37.04-.17-.08-.71'
    '-.26-1.36-.83a5.04 5.04 0 01-.94-1.17c-.1-.17-.01-.26.07-.34.07-.07.17-.2.25-.3.08-.1.11-.17'
    '.16-.28.06-.11.03-.21-.01-.3-.05-.08-.39-.94-.53-1.28-.14-.34-.28-.29-.39-.3-.1-.01-.21-.01-'
    '.32-.01a.61.61 0 00-.45.21c-.15.17-.59.58-.59 1.4 0 .83.61 1.63.69 1.74.08.12 1.2 1.83 2.91 '
    '2.57.41.18.72.28.97.36.4.13.78.11 1.07.07.33-.05 1-.41 1.14-.8.14-.4.14-.74.1-.81-.04-.07-.16'
    '-.11-.32-.19z"/></svg>'
)
_SVG_BLUESKY = (
    '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false">'
    '<path d="M3.2 2.5c1.5.6 3.2 1.9 4.3 4.3c.3.7.6 1.5.8 2.1c.2-.7.5-1.4.8-2.1c1.1-2.4 2.8-3.7 4.3-4.3'
    'c1.7-.7 2.5.2 2.5 2.6c0 1.4-.5 4.2-.8 5.1c-.4 1.2-1.4 1.5-2.4 1.4c1.6.3 2 1.2 1 2.1c-1.9 1.7-2.7-.4-2.9'
    '-.9c0-.1-.1-.1-.1-.1c-.1 0-.1.1-.2.1c-.2.5-1.1 2.6-3 .9c-1-.9-.6-1.8 1-2.1c-1.1.1-2-.2-2.4-1.4c-.3'
    '-.9-.8-3.7-.8-5.1c0-2.4.8-3.3 2.5-2.6z"/></svg>'
)
def inject_eyebrow(html: str) -> str:
    """Render an FT-style eyebrow caption (``<p class="eyebrow">``)
    immediately above the H1 hero. The label is the article's first
    keyword, upper-cased — mirroring how the FT promotes a single
    editorial section per article (FEATURES / OPINION / ANALYSIS).
    BlogPosting pages only; idempotent."""
    if '"@type":"BlogPosting"' not in html:
        return html
    if 'class="eyebrow"' in html:
        return html
    keywords, _date_pub, _date_mod, _wc = _extract_article_metadata(html)
    if not keywords:
        return html
    section = keywords[0].upper()
    eyebrow = f'<p class="eyebrow">{_esc(section)}</p>'
    return _AP_HERO_OPEN_RE.sub(rf"\1\2{eyebrow}\3", html, count=1)


def inject_deck(html: str) -> str:
    """Promote the existing ``<p class="sub">`` hero excerpt to the
    FT-style ``.deck`` standfirst. The excerpt is already populated
    from the article's frontmatter; this pass just signals 'editorial
    standfirst' so the .deck CSS applies. BlogPosting pages only;
    idempotent."""
    if '"@type":"BlogPosting"' not in html:
        return html
    if 'class="sub deck"' in html:
        return html
    return _SUB_PARA_RE.sub('<p class="sub deck">', html, count=1)






























# ---------------------------------------------------------------------------
# WS2 — pull-quotes, section rules, footnotes
# ---------------------------------------------------------------------------

_PULL_BLOCKQUOTE_RE = re.compile(
    r'<blockquote\b[^>]*\bclass="[^"]*\bpull\b[^"]*"[^>]*>([\s\S]*?)</blockquote>',
    re.IGNORECASE,
)
# inject_anchor_links_and_toc stamps id="h2-..." on every PROSE h2
# (the ones with slugified anchors). The ToC / Lead / Sources asides
# use bare <h2> with no id, so this scoped regex naturally skips them.
_H2_WITH_ID_RE = re.compile(r'<h2\s+id="[^"]*"[^>]*>', re.IGNORECASE)
_MIN_H2_FOR_RULES = 6
_FOOTNOTE_MARKER_RE = re.compile(r"\[\^(\d+)\]")
_FOOTNOTE_DEF_RE = re.compile(r"\[\^(\d+)\]:\s*([^\n<]+)")


def inject_pullquotes(html: str) -> str:
    """Promote ``<blockquote class="pull">…</blockquote>`` blocks to
    ``<aside class="pull-quote">…</aside>`` so the FT-style serif italic
    + oversized opening-quote CSS (WS1 commit 2) applies. The marker
    class is opt-in — authors who don't want a pull-quote keep the
    plain blockquote. BlogPosting pages only; idempotent."""
    if '"@type":"BlogPosting"' not in html:
        return html
    if 'class="pull-quote"' in html:
        return html
    return _PULL_BLOCKQUOTE_RE.sub(
        lambda m: f'<aside class="pull-quote">{m.group(1)}</aside>',
        html,
    )


def inject_section_rules(html: str) -> str:
    """Insert ``<hr class="section-rule" aria-hidden="true">`` BEFORE
    every prose ``<h2 id="...">`` after the first, on long-read
    articles with at least 6 such headings. Targets the anchored body
    headings stamped by ``inject_anchor_links_and_toc`` — so the
    aside-only headings (Contents, Lead, Sources) are skipped, and
    short pieces don't get visually overloaded with rules. Skipping
    the first H2 preserves the natural break from the hero section.
    BlogPosting pages only; idempotent."""
    if '"@type":"BlogPosting"' not in html:
        return html
    if 'class="section-rule"' in html:
        return html
    headings = list(_H2_WITH_ID_RE.finditer(html))
    if len(headings) < _MIN_H2_FOR_RULES:
        return html
    rule = '<hr class="section-rule" aria-hidden="true">'
    out = html
    # Walk back-to-front so earlier offsets stay valid as we splice.
    for match in reversed(headings[1:]):
        start = match.start()
        out = out[:start] + rule + out[start:]
    return out


def _footnote_list_items(definitions: list[tuple[str, str]], labels: dict[str, str]) -> str:
    backref_label = labels.get("Footnotes.return", "Return to text")
    items = []
    for n, body in definitions:
        items.append(
            f'<li id="fn-{n}">{body} '
            f'<a class="footnote-back" href="#fnref-{n}" '
            f'aria-label="{_esc(backref_label, quote=True)}">↩</a></li>'
        )
    return "".join(items)


def inject_footnotes(html: str) -> str:
    """Convert literal markdown footnote markers (``[^n]`` in text and
    ``[^n]: …`` at the article foot) into HTML: each in-text marker
    becomes a numbered ``<sup><a>`` link, and the collected definitions
    surface as a ``<section class="footnotes">`` block immediately
    inside the wrap-div close. Static Site Generator (SSG) doesn't expand footnotes,
    so we do it at postbuild. BlogPosting pages only; idempotent."""
    if '"@type":"BlogPosting"' not in html:
        return html
    if 'class="footnotes"' in html:
        return html
    if "[^" not in html:
        return html
    definitions = _FOOTNOTE_DEF_RE.findall(html)
    if not definitions:
        return html
    # Strip the literal "[^n]: definition" lines from the body — they're
    # about to be moved into the <section class="footnotes"> block.
    body_no_defs = _FOOTNOTE_DEF_RE.sub("", html)
    # Wrap remaining "[^n]" markers in <sup><a> superscript links.
    def _sup(m: re.Match[str]) -> str:
        n = m.group(1)
        return (
            f'<sup class="footnote-ref"><a href="#fn-{n}" id="fnref-{n}">{n}</a></sup>'
        )

    body_marked = _FOOTNOTE_MARKER_RE.sub(_sup, body_no_defs)
    labels = _labels(html)
    heading = _esc(labels.get("Footnotes.heading", "Footnotes"), quote=True)
    items = _footnote_list_items(definitions, labels)
    section = (
        f'<section class="footnotes" aria-labelledby="footnotes-heading">'
        f'<h2 id="footnotes-heading">{heading}</h2>'
        f"<ol>{items}</ol></section>"
    )
    return _WRAP_CLOSE_RE.sub(section + r"\1", body_marked, count=1)


# ---------------------------------------------------------------------------
# WS2 — action rail, cite popover, reuse / republish panel
# ---------------------------------------------------------------------------

_LICENSE_DEFAULT = "CC-BY-4.0"
_LICENSE_URLS: dict[str, str] = {
    "CC-BY-4.0": "https://creativecommons.org/licenses/by/4.0/",
    "CC-BY-SA-4.0": "https://creativecommons.org/licenses/by-sa/4.0/",
    "CC-BY-NC-SA-4.0": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
    "CC-BY-ND-4.0": "https://creativecommons.org/licenses/by-nd/4.0/",
}

_AUTHOR_LAST = "Rousseau"
_AUTHOR_FIRST = "Sebastien"

# 14x14 monochrome SVG glyphs (currentColor fill) for the action rail.
_SVG_DOWNLOAD = (
    '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false">'
    '<path d="M7.3 1.5h1.4v6l1.95-1.95.99.99L8 9.18 4.36 5.54l.99-.99L7.3 6.5v-5zM2 13h12v1.5H2V13z"/>'
    "</svg>"
)


















_OG_IMAGE_RE = re.compile(
    r'<meta\s+property="og:image"\s+content="([^"]+)"',
    re.IGNORECASE,
)
_OG_IMAGE_ALT_RE = re.compile(
    r'<meta\s+(?:property|name)="og:image:alt"\s+content="([^"]+)"',
    re.IGNORECASE,
)
_BANNER_ALT_FRONTMATTER_RE = re.compile(
    r'<meta\s+name="twitter:image:alt"\s+content="([^"]+)"',
    re.IGNORECASE,
)
_OG_IMAGE_WIDTH_RE = re.compile(
    r'<meta\s+property="og:image:width"\s+content="(\d+)"',
    re.IGNORECASE,
)
_OG_IMAGE_HEIGHT_RE = re.compile(
    r'<meta\s+property="og:image:height"\s+content="(\d+)"',
    re.IGNORECASE,
)
# Fallback dimensions when the page has no og:image:width / og:image:height
# meta tags. Picked at 16:9 because that's the canonical hero aspect for
# CDN-transform URLs that don't carry a height. Used only as a last resort
# — every article since 2026-06-02 ships with explicit og:image dimensions.
_BANNER_FALLBACK_WIDTH = 1200
_BANNER_FALLBACK_HEIGHT = 675


def _banner_dimensions(html: str) -> tuple[int, int]:
    """Read og:image:width / og:image:height from the rendered HTML and
    return ``(width, height)`` as integers. Falls back to the canonical
    16:9 hero dims when either tag is absent or malformed.

    This is what fixes the lighthouse CLS regression: an article whose
    banner has a 2.5:1 natural ratio (e.g. 1425×571) needs a 2.5:1 box
    reservation. Hardcoding 16:9 attributes meant the browser reserved a
    16:9 box while CSS set ``aspect-ratio: 16/9``; when the natural image
    actually arrived, ``object-fit: cover`` cropped the strip but the box
    surrounding text still shifted by ~0.04 above the 0.1 CLS threshold.
    Reading the real og:image dimensions makes the reservation exact.
    """
    w_m = _OG_IMAGE_WIDTH_RE.search(html)
    h_m = _OG_IMAGE_HEIGHT_RE.search(html)
    # The og:image:width/height regexes only match \d+, so the int() cast
    # cannot fail — validation is the regex shape, not a runtime check.
    if w_m and h_m:
        w = int(w_m.group(1))
        h = int(h_m.group(1))
        if w > 0 and h > 0:
            return w, h
    return _BANNER_FALLBACK_WIDTH, _BANNER_FALLBACK_HEIGHT


def _banner_path(banner_url: str) -> str | None:
    """Return the on-CDN path component (e.g. ``/stocks/images/foo.webp``)
    of a banner URL, or ``None`` if the URL has no extractable path."""
    m = re.match(r"https?://[^/]+(/[^?#]+)", banner_url)
    return m.group(1) if m else None


def strip_legacy_inline_banner(html: str, banner_url: str) -> str:
    """Remove the legacy ``<p><img></p>`` wrapper that pre-2026 articles
    used to place the banner inline as the first body element.

    Pre-2026 articles routinely placed the banner as the first paragraph
    in the markdown source (``![alt](url)`` → ``<p><img></p>``). The
    article-banner figure injected by ``inject_hero_banner`` now carries
    that role at the top of every page, so the inline copy is a visible
    duplicate of the same image.

    Detection: find the first ``<p><img></p>`` after the article-banner
    figure (skipping ``langswitch`` aside + ``lead-start`` aside in
    between); if the img's src contains the og:image path as a substring,
    drop the entire ``<p>…</p>`` wrapper. The wrap_cdn_images postbuild
    pass may have rewritten the body img to a ``/api/transform?url=…``
    form, so substring match is used instead of URL equality.

    No-op if the page has no article-banner figure (e.g. listings,
    static pages) or the first body ``<p><img></p>`` doesn't match the
    banner.
    """
    og_path = _banner_path(banner_url)
    if og_path is None:
        return html
    # Anchor: the close of the auto-injected article-banner figure.
    anchor = re.search(r"</figure>", html, re.IGNORECASE)
    if not anchor:
        return html
    # Look at the first ~4 KB after </figure> for a `<p><img …></p>`
    # whose src contains the banner path. The langswitch + lead-start
    # asides come in between but are easy to skip — they're `<aside>`
    # tags that the regex skips over.
    start = anchor.end()
    window = html[start : start + 4000]
    m = re.search(
        r'<p>\s*<img\b[^>]*\bsrc="([^"]+)"[^>]*>\s*</p>',
        window,
        re.IGNORECASE,
    )
    if not m or og_path not in m.group(1):
        return html
    # Drop the matched <p>…</p>.
    abs_start = start + m.start()
    abs_end = start + m.end()
    return html[:abs_start] + html[abs_end:]


def inject_hero_banner(html: str) -> str:
    """Insert a hero ``<figure class="article-banner">`` right after the
    H1/byline ``<section class="ap-hero">`` on every BlogPosting page.

    Source: ``<meta property="og:image">`` (set by the SSG from the
    article's frontmatter ``banner:`` field).
    Alt:    ``<meta name="twitter:image:alt">`` (set by the SSG from
            ``banner_alt:``), falling back to the article's H1 title.

    Idempotent. Skips:
      - non-BlogPosting pages (listings / static pages)
      - pages already carrying ``class="article-banner"`` (re-runs)
      - legacy articles whose first body image already matches the
        og:image URL (``_body_starts_with_banner_image``); without this
        check we'd inject a duplicate, producing the banner-then-banner
        stack at the top of the article that the 2018 / 2023 series
        currently shows.
    """
    if '"@type":"BlogPosting"' not in html:
        return html
    if 'class="article-banner"' in html:
        return html
    og = _OG_IMAGE_RE.search(html)
    if not og:
        return html
    banner_url = og.group(1)
    banner_width, banner_height = _banner_dimensions(html)

    alt_m = _BANNER_ALT_FRONTMATTER_RE.search(html) or _OG_IMAGE_ALT_RE.search(html)
    if alt_m:
        alt_text = alt_m.group(1)
    else:
        # Fallback: derive from the H1 — better than nothing, screen-reader-safe.
        h1 = _H1_RE.search(html)
        alt_text = f"Banner for: {h1.group(1).strip()}" if h1 else ""

    figure = (
        f'<figure class="article-banner">'
        f'<img src="{banner_url}" alt="{alt_text}" '
        f'width="{banner_width}" height="{banner_height}" '
        f'fetchpriority="high" decoding="async" />'
        f"</figure>"
    )
    # Insert immediately after the closing </section> of the ap-hero block.
    # Same anchor _LANG_SWITCH_INSERT_RE uses, but we run BEFORE the lang
    # switcher so its insertion sees the banner already in place and slots
    # the langswitch aside after the banner.
    new_html, n = _HERO_BANNER_INSERT_RE.subn(
        lambda m: f"{m.group(1)}{figure}{m.group(2)}",
        html,
        count=1,
    )
    if not n:
        return html
    # Legacy authoring pattern: pre-2026 articles placed the banner image
    # inline as the first body element. The auto-injected figure above
    # now carries that role, so the inline copy is a visible duplicate.
    return strip_legacy_inline_banner(new_html, banner_url)


# Insertion anchor: the close of <section class="ap-hero"> immediately
# followed by the next sibling. Matches the same shape as the lang-switch
# anchor (which runs later in the pipeline).
_HERO_BANNER_INSERT_RE = re.compile(
    r'(</section>)(\s*<(?!figure class="article-banner")[a-z])',
    re.IGNORECASE,
)


# A previously-injected anchor link inside a heading. Matched once and
# stripped during text extraction so a re-run never picks up the "#" or
# its surrounding markup as part of the heading title.
_HEADING_ANCHOR_RE = re.compile(
    r'\s*<a\s+class="heading-anchor"[\s\S]*?</a>',
    re.IGNORECASE,
)


def inject_anchor_links_and_toc(html: str) -> str:
    """Add id="…" + a click-to-copy anchor link icon to every H2/H3 inside
    <main>. If the post has ≥5 H2 headings, build a table-of-contents card
    and insert it at the top of <main>.

    Idempotent: if a previous run already injected a ``.article-toc`` or
    any ``.heading-anchor`` link inside <main>, the function no-ops.
    Without this guard, re-running the pass (e.g. when a stale ``public/``
    tree carries last build's HTML) compounds anchors on each H2 and
    stacks N copies of the TOC — and because each rerun strips tags
    rather than the prior anchor's "#" text content, the TOC labels
    accumulate trailing " # # # #" tokens that contaminate every entry.
    """
    if '"@type":"BlogPosting"' not in html:
        return html
    m = _MAIN_RE.search(html)
    if not m:
        return html
    pre, body, post = m.group(1), m.group(2), m.group(3)
    # Idempotency guard — either marker means a previous run already
    # owned this <main>. Skipping returns the HTML untouched.
    if 'class="article-toc"' in body or 'class="heading-anchor"' in body:
        return html
    h2_titles: list[tuple[str, str]] = []
    labels = _labels(html)
    # Track slugs already emitted on this page; append -2, -3… on
    # collision. Non-ASCII scripts (Arabic, Cyrillic, CJK) often
    # slugify to the same Latin fragment (e.g. "FHE", "2026") for
    # multiple headings — without dedup, pa11y fails on duplicate ids.
    seen: dict[str, int] = {}

    def _unique(slug: str, idx: int) -> str:
        if not slug:
            slug = f"section-{idx}"
        n = seen.get(slug, 0) + 1
        seen[slug] = n
        return slug if n == 1 else f"{slug}-{n}"

    heading_idx = 0

    def patch_heading(hm: re.Match[str]) -> str:
        nonlocal heading_idx
        heading_idx += 1
        level = hm.group(1).lower()
        inner = hm.group(2)
        # Drop any prior anchor-link markup from the inner content
        # before computing the heading text. The top-level idempotency
        # guard makes this defensive rather than hot-path — kept so
        # narrow regression cases (e.g. tests that hand-craft a partial
        # state) still degrade safely.
        clean_inner = _HEADING_ANCHOR_RE.sub("", inner)
        text = re.sub(r"<[^>]+>", "", clean_inner).strip()
        if not text:
            return hm.group(0)
        slug = _unique(slugify(text), heading_idx)
        if level == "h2":
            h2_titles.append((slug, text))
        return (
            f'<{level} id="{slug}">{clean_inner} '
            f'<a class="heading-anchor" href="#{slug}" aria-label="{labels["Link to"]} {text}">#</a>'
            f'</{level}>'
        )

    new_body = _HEADING_RE.sub(patch_heading, body)
    toc_html = ""
    if len(h2_titles) >= 5:
        items = "".join(f'<li><a href="#{slug}">{text}</a></li>' for slug, text in h2_titles)
        toc_html = (
            f'<aside class="article-toc" aria-label="{labels["Table of contents"]}">'
            f'<h2>{labels["Contents"]}</h2>'
            f'<ol>{items}</ol></aside>'
        )
    return html[: m.start()] + pre + toc_html + new_body + post + html[m.end() :]


_BODY_H1_RE = re.compile(
    r'(<main\b[^>]*>\s*<div class="wrap[^"]*">[\s\S]*?' r"(?:</aside>\s*)*)<h1>([^<]+)</h1>\s*",
    re.IGNORECASE,
)


def strip_duplicate_body_h1(html: str) -> str:
    """Remove the first H1 inside <main> when it duplicates the hero H1
    that the layout template emits in ``<section class="ap-hero">``.

    Every dated article runs the markdown body through Static Site
    Generator with the H1 markdown ``# {{title}}`` at the top. The
    layout *also* emits ``<h1>{{title}}</h1>`` in the hero band. The
    rendered output therefore carries two H1s with identical text —
    WCAG 1.3.1 / 2.4.6 violation, plus a noisy duplicate above the
    article body.

    The fix is render-only: ``check_voice`` still requires exactly one
    H1 in the markdown source (so editors keep the canonical title at
    the top of the file), but the postbuild pass deletes the
    duplicate before the page is served.
    """
    hero_m = _H1_RE.search(html)
    if hero_m is None:
        return html
    hero_text = _html_unescape(hero_m.group(1)).strip()
    new_html, n = _BODY_H1_RE.subn(
        lambda m: m.group(1) if _html_unescape(m.group(2)).strip() == hero_text else m.group(0),
        html,
        count=1,
    )
    return new_html if n else html


def _html_unescape(s: str) -> str:
    """Thin indirection so the strip-duplicate-H1 helper can be patched
    (``article_furniture._unesc``) in tests if needed."""
    return _unesc(s)






def build_post_nav_index(
    pages: list[Path],
) -> dict[str, tuple[tuple[str, str] | None, tuple[str, str] | None]]:
    """Build a slug -> (prev, next) lookup over every dated post in pages.

    A dated post is one whose parent directory name matches ``YYYY-MM-DD-…``.
    Order is chronological (oldest first); 'prev' is older, 'next' is newer.
    Each entry is (slug, title) so the renderer can localize labels per
    target page.
    """
    dated: list[tuple[str, str, str]] = []
    for p in pages:
        slug = p.parent.name
        if not _DATED_SLUG_RE.match(slug):
            continue
        # Skip non-EN translations — they share the (EN-)slug with the English
        # original at the data level, but live under /<lang>/<lang-slug>/.
        # Including them would double-count and yield wrong nav.
        if p.parent.parent.name in _all_active_non_en_langs():
            continue
        html = p.read_text(encoding="utf-8", errors="ignore")
        if '"@type":"BlogPosting"' not in html:
            continue
        m = _H1_RE.search(html)
        title = m.group(1).strip() if m else slug
        dated.append((slug[:10], slug, title))
    dated.sort(key=lambda t: t[0])
    out: dict[str, tuple[tuple[str, str] | None, tuple[str, str] | None]] = {}
    for i, entry in enumerate(dated):
        prev_e = (dated[i - 1][1], dated[i - 1][2]) if i > 0 else None
        next_e = (dated[i + 1][1], dated[i + 1][2]) if i < len(dated) - 1 else None
        out[entry[1]] = (prev_e, next_e)
    return out




_FAQ_H2_RE = re.compile(
    r'<h2 id="(frequently-asked-questions|foire-aux-questions)"[^>]*>'
    r"([\s\S]+?)</h2>"
    r"([\s\S]+?)"
    r"(?=<h2|<aside|</main>|<hr|<footer)",
)


def _convert_faq_to_qa(html: str) -> str:
    """Convert the plain ``<p><strong>Q?</strong></p><p>A</p>…`` FAQ
    structure inside articles into the collapsible ``<details class="qa-item">``
    pattern used by ``/projects/`` and ``/papers/`` for UX/UI consistency.
    """
    is_fr = _is_french(html)
    headline = "Questions ?" if is_fr else "Questions?"
    soft = "Réponses." if is_fr else "Answers."

    def patch(m: re.Match[str]) -> str:
        faq_id = m.group(1)  # preserve original anchor so TOC links stay valid
        body = m.group(3)
        # Strip the trailing "<a class='heading-anchor'>#</a>" inside H2.
        # Walk for Q/A pairs: <p><strong>Q?</strong></p><p>A</p>
        qa_pairs: list[tuple[str, str]] = []
        # Capture Q + multiple following <p>…</p> until next <p><strong>...?</strong></p>.
        # Build a list of P-segments first, then pair Q with the answer chunk.
        segments: list[str] = [
            sm.group(1).strip() for sm in re.finditer(r"<p>([\s\S]*?)</p>", body)
        ]
        i = 0
        while i < len(segments):
            seg = segments[i]
            # Q heuristic: starts with <strong> and ends with ? (or French ?)
            qm = re.match(r"^<strong>([\s\S]+?)</strong>\s*$", seg)
            if qm:
                question = qm.group(1).strip()
                # Collect answer paragraphs until next strong-only paragraph
                ans_parts: list[str] = []
                j = i + 1
                while j < len(segments):
                    nxt = segments[j]
                    if re.match(r"^<strong>[\s\S]+?</strong>\s*$", nxt):
                        break
                    ans_parts.append(nxt)
                    j += 1
                qa_pairs.append((question, "</p><p>".join(ans_parts)))
                i = j
            else:
                i += 1

        if not qa_pairs:
            return m.group(0)

        new_h2 = (
            f'<h2 id="{faq_id}" class="qa-headline">{headline} '
            f'<span class="qa-headline-soft">{soft}</span></h2>'
        )
        out_parts: list[str] = [new_h2, f'<section class="qa-list" aria-labelledby="{faq_id}">']
        for q, a in qa_pairs:
            out_parts.append(
                f'<details class="qa-item" open><summary class="qa-q">{q}</summary>'
                f'<section class="qa-a"><p>{a}</p></section></details>'
            )
        out_parts.append("</section>")
        return "".join(out_parts)

    return _FAQ_H2_RE.sub(patch, html)


def _nav_target_for_en_page(top: str) -> str:
    """Map an EN top-level page slug to its nav-link href."""
    if _DATED_SLUG_RE.match(top):
        return "/articles/index.html"
    return f"/{top}/index.html"


def _nav_target_for_lang_page(lang: str, top: str) -> str:
    """Map a localised top-level page slug to its nav-link href."""
    articles_slug = _slug_maps(lang)["statics_en_to_lang"].get("articles", "articles")
    if _DATED_SLUG_RE.match(top):
        return f"/{lang}/{articles_slug}/index.html"
    return f"/{lang}/{top}/index.html"


def _nav_active_target(page: Path) -> str | None:
    """Return the nav-link href that should be marked active for this
    page, or ``None`` if there's no obvious match.

    Greedy by depth: ``/about/`` → ``/about/index.html``;
    ``/2026-05-12-…/`` → ``/articles/index.html``;
    ``/<lang>/<x>/`` → ``/<lang>/<x>/index.html``.
    """
    rel = page.relative_to(PUBLIC).as_posix()
    if rel == "index.html":
        return "/index.html"  # home
    parts = rel.split("/")
    if len(parts) == 2 and parts[1] == "index.html":
        return _nav_target_for_en_page(parts[0])
    if len(parts) == 3 and parts[2] == "index.html":
        lang, top = parts[0], parts[1]
        if lang not in _all_active_non_en_langs():
            return None
        return _nav_target_for_lang_page(lang, top)
    return None


def inject_nav_active(html: str, page: Path) -> str:
    """Add ``aria-current="page"`` + ``class="active"`` to the nav link
    matching this page. For home pages (/, /<lang>/), the brand link
    sitting outside the nav menu is the home indicator, so we mark it
    there. Idempotent — re-running doesn't double-mark."""
    target = _nav_active_target(page)
    if not target:
        return html

    # Always clear any pre-existing active markers in the header first.
    header_m = re.search(r"<header\b[^>]*>([\s\S]*?)</header>", html, re.IGNORECASE)
    if not header_m:
        return html
    header_body = header_m.group(1)
    header_clean = re.sub(r'\s+aria-current=["\']?[^"\'>]+["\']?', "", header_body)
    header_clean = re.sub(r'(<a\b[^>]*?)\s+class=["\']?active["\']?', r"\1", header_clean)

    pat = re.compile(
        r'(<a\s+(?:[^>]*?)href=["\']?)(' + re.escape(target) + r')(["\']?)([^>]*>)',
        re.IGNORECASE,
    )

    def repl(m: re.Match[str]) -> str:
        return (
            f'{m.group(1)}{m.group(2)}{m.group(3)} aria-current="page" class="active"{m.group(4)}'
        )

    new_body = pat.sub(repl, header_clean, count=1)
    open_tag = header_m.group(0)[: header_m.group(0).index(">") + 1]
    return html.replace(header_m.group(0), open_tag + new_body + "</header>", 1)


def inject_prev_next_nav(
    html: str,
    slug: str,
    nav_index: dict[str, tuple[tuple[str, str] | None, tuple[str, str] | None]],
    is_fr: bool = False,
    fr_titles: dict[str, str] | None = None,
    *,
    page_lang: str = "en",
) -> str:
    """Inject a ``<nav class="post-pagination">`` with prev/next links
    just before the closing ``</div></main>`` of any dated BlogPosting
    page. Localised via ``_labels(html)``; non-EN pages get translated
    labels and links pointing to the matching translation under
    ``/<lang>/<lang-slug>/``.
    """
    if '"@type":"BlogPosting"' not in html:
        return html
    # Resolve the EN slug regardless of which lang we're patching.
    if page_lang != "en":
        maps = _slug_maps(page_lang)
        lookup_slug = maps["articles_lang_to_en"].get(slug, slug)
    else:
        lookup_slug = slug
    if 'class="post-pagination"' in html:
        return html
    labels = _labels(html)
    # Pages that ship BlogPosting JSON-LD but aren't in the dated nav chain
    # (landing pages with frontmatter schema=Article, dateless reports) get
    # an empty stub block so validate_jsonld's furniture contract holds.
    if lookup_slug not in nav_index:
        stub = (
            f'<nav class="post-pagination" aria-label="{labels["Article pagination"]}">'
            f'<span class="post-pagination-stub" aria-hidden="true"></span>'
            f'<span class="post-pagination-stub" aria-hidden="true"></span>'
            f"</nav>"
        )
        return re.sub(
            r"(</div>)(\s*(?:<aside\b[^>]*>[\s\S]*?</aside>\s*)*</main>)",
            stub + r"\1\2",
            html,
            count=1,
        )
    prev_e, next_e = nav_index[lookup_slug]
    if not prev_e and not next_e:
        return html
    fr_titles = fr_titles or {}

    def render(entry: tuple[str, str] | None, direction: str, label: str) -> str:
        if not entry:
            return '<span class="post-pagination-stub" aria-hidden="true"></span>'
        s, t = entry
        if page_lang != "en":
            articles_map = _slug_maps(page_lang)["articles_en_to_lang"]
            if s in articles_map:
                href = f"/{page_lang}/{articles_map[s]}/"
                if page_lang == "fr":
                    t = fr_titles.get(s, t)
            else:
                href = f"/{s}/"
        else:
            href = f"/{s}/"
        return (
            f'<a class="post-pagination-{direction}" href="{href}">'
            f'<span class="post-pagination-label">{label}</span>'
            f'<span class="post-pagination-title">{t}</span>'
            f"</a>"
        )

    inner = render(prev_e, "prev", labels["Previous"]) + render(next_e, "next", labels["Next"])
    nav = f'<nav class="post-pagination" aria-label="{labels["Article pagination"]}">{inner}</nav>'
    # The anchor used to be `</div>\s*</main>` (the wrap-div directly closing
    # the main element). But the sigstore-attestation pass runs earlier and
    # may have inserted `<aside class="article-sigstore">...</aside>` between
    # `</div>` and `</main>`. Allow an optional aside (or chain of asides) in
    # between, so pagination still anchors against the wrap-div even after
    # sigstore has run. Without this, translated pages with sigstore bundles
    # silently lost prev/next nav.
    patched = re.sub(
        r"(</div>)(\s*(?:<aside\b[^>]*>[\s\S]*?</aside>\s*)*</main>)",
        nav + r"\1\2",
        html,
        count=1,
    )
    return patched




_MERMAID_BLOCK_RE = re.compile(
    r'<pre[^>]*>\s*<code\s+class="language-mermaid"[^>]*>([\s\S]*?)</code>\s*</pre>',
    re.IGNORECASE,
)

# Local copies of the CSP-meta regexes (kept in postbuild.py too — both
# modules patch the same tag from different injection passes).
_csp_tag_re = re.compile(
    r'<meta\b[^>]*?http-equiv=["\']?Content-Security-Policy["\']?[^>]*?>',
    re.IGNORECASE,
)
_content_attr_re = re.compile(
    r'(content=)(["\'])(.+?)(\2)',
    re.IGNORECASE | re.DOTALL,
)


def inject_mermaid(html: str) -> str:
    """Convert ```mermaid fenced blocks into <pre class="mermaid"> containers
    so main.js can lazy-load the Mermaid library and render them. Also
    widens the meta-CSP script-src to allow the cdn.jsdelivr.net import,
    but only on pages that actually contain a Mermaid block."""
    if "language-mermaid" not in html:
        return html

    def replace(m: re.Match[str]) -> str:
        # Strip <span> wrappers a syntax highlighter may have added,
        # then unescape entities — Mermaid wants the raw source.
        # Mermaid v10's run() reads via innerHTML, so emit `>` as a raw
        # char (not `&gt;`) — otherwise `->>` arrows fail to parse.
        # Still escape `<` and `&` to keep the surrounding HTML valid.
        inner = re.sub(r"<[^>]+>", "", m.group(1))
        raw = _unesc(inner)
        safe = raw.replace("&", "&amp;").replace("<", "&lt;")
        return f'<pre class="mermaid">{safe}</pre>'

    new_html = _MERMAID_BLOCK_RE.sub(replace, html)
    if new_html == html:
        return html

    # Widen the meta-CSP for this page so the dynamic import resolves.
    def patch_csp(tag_match: re.Match[str]) -> str:
        tag = tag_match.group(0)

        def patch_content(c: re.Match[str]) -> str:
            policy = c.group(3)
            new_policy = policy
            # Widen script-src so the Mermaid lib can be imported from jsDelivr.
            if "cdn.jsdelivr.net" not in new_policy:
                new_policy = re.sub(
                    r"(script-src)(\s+)",
                    r"\1 https://cdn.jsdelivr.net\2",
                    new_policy,
                    count=1,
                )
            # Widen style-src so Mermaid can set inline styles on the SVG it
            # generates (arrowhead fills, sequence-number colors, message-line
            # strokes are all set via element.style.X). Without 'unsafe-inline'
            # in style-src for these pages, those assignments are silently
            # blocked by CSP and the diagram renders with browser default fill
            # (black filled paths = teardrop blobs).
            #
            # CSP3 spec gotcha: 'unsafe-inline' is IGNORED if any hash or nonce
            # is also present in the same source list. So we strip the existing
            # 'sha256-…' tokens from the style-src clause when we add
            # 'unsafe-inline', otherwise the browser silently drops it.
            if "'unsafe-inline'" not in new_policy:
                # Match the whole style-src clause (up to the next ; or end of value)
                def widen_style_src(m: re.Match[str]) -> str:
                    clause = m.group(0)
                    # Drop any 'sha256-…' or 'sha384-…' / 'sha512-…' hashes
                    clause = re.sub(r"\s*'sha(?:256|384|512)-[A-Za-z0-9+/=]+'", "", clause)
                    # Insert 'unsafe-inline' right after the directive name
                    clause = re.sub(
                        r"^(style-src)(\s+)",
                        r"\1 'unsafe-inline'\2",
                        clause,
                        count=1,
                    )
                    return clause
                new_policy = re.sub(
                    r"style-src[^;]*",
                    widen_style_src,
                    new_policy,
                    count=1,
                )
            if new_policy == policy:
                return c.group(0)
            return c.group(1) + c.group(2) + new_policy + c.group(4)

        return _content_attr_re.sub(patch_content, tag, count=1)

    return _csp_tag_re.sub(patch_csp, new_html, count=1)




_HEAD_END_RE = re.compile(r"</head>", re.IGNORECASE)
# Match a <link rel="alternate" hreflang=…> tag with any attribute order
# and either HTML5 (``>``) or XHTML (``/>``) self-close. The previous form
# required ``[^/]*/>`` which can never match real URLs (every ``https://``
# contains ``/``) — so the strip never fired and duplicates accumulated.


# Speculation Rules API — prerender same-origin pages on hover so any
# navigation feels instant. The CSP allows it via 'inline-speculationrules'
# in script-src; no per-page hash needed.
SPECULATION_RULES_BLOCK = (
    '<script type="speculationrules">'
    '{"prerender":[{'
    '"where":{"and":['
    '{"href_matches":"/*"},'
    '{"not":{"href_matches":"/_csp/*"}},'
    '{"not":{"href_matches":"/*.xml"}},'
    '{"not":{"href_matches":"/*.json"}},'
    '{"not":{"href_matches":"/*.txt"}},'
    '{"not":{"href_matches":"/*.pdf"}},'
    '{"not":{"href_matches":"/manifest.json"}},'
    '{"not":{"href_matches":"/sw.js"}},'
    '{"not":{"href_matches":"/contact/*"}},'
    '{"not":{"href_matches":"/fr/contact/*"}}'
    "]},"
    '"eagerness":"moderate"'
    "}]}"
    "</script>"
)


_BODY_LINK_STYLESHEET_RE = re.compile(
    r'<link\b[^>]*\brel=(?:"stylesheet"|stylesheet)[^>]*>',
    re.IGNORECASE,
)
_BODY_END_RE = re.compile(r"</head>", re.IGNORECASE)


def _sanitize_link_tag(tag: str) -> str:
    """Strip the stray trailing double-quote SSG emits on the search-widget
    stylesheet (``crossorigin="anonymous""``). Browsers treat that as an
    attribute-value error and bail out of ``<head>`` parsing, which then
    cascades into pa11y flagging the legitimate ``<link rel=icon>`` etc.
    as "link in body"."""
    # Collapse any duplicate `crossorigin="anonymous"` runs into one.
    tag = re.sub(
        r'(crossorigin="anonymous")(\s+crossorigin="anonymous")+',
        r"\1",
        tag,
    )
    # Remove a trailing `"` immediately before the closing `>`.
    tag = re.sub(r'""(\s*/?>)', r'"\1', tag)
    return tag


def hoist_body_link_stylesheets(html: str) -> tuple[str, int]:
    """Hoist every in-body ``<link rel=stylesheet>`` into ``<head>`` and
    sanitize the tag (SSG ships one with a malformed double-quote attribute
    that breaks Chrome's head-parser). HTML5 forbids ``<link>`` in body, so
    pa11y AAA flags this on every page shipping the SSG search widget."""
    head_end_m = _BODY_END_RE.search(html)
    if not head_end_m:
        return html, 0
    head_end = head_end_m.start()
    head, body = html[:head_end], html[head_end:]

    # Also sanitize any in-head stylesheet tags that already have the malformed
    # attribute — a previous hoist pass may have moved them up without fixing.
    head = _BODY_LINK_STYLESHEET_RE.sub(lambda m: _sanitize_link_tag(m.group(0)), head)

    matches = list(_BODY_LINK_STYLESHEET_RE.finditer(body))
    if not matches:
        return head + body, 0
    extracted: list[str] = []
    new_body = body
    for m in reversed(matches):
        extracted.insert(0, _sanitize_link_tag(m.group(0)))
        new_body = new_body[: m.start()] + new_body[m.end() :]
    return head + "".join(extracted) + new_body, len(extracted)


def inject_speculation_rules(html: str) -> str:
    """Inject the Speculation Rules API block before </head>. Idempotent."""
    if 'type="speculationrules"' in html:
        return html
    return _HEAD_END_RE.sub(SPECULATION_RULES_BLOCK + "</head>", html, count=1)


# ---------------------------------------------------------------------------
# 8. Lang / slug helpers — used by the hreflang pass + various injectors
# ---------------------------------------------------------------------------


















# Per-locale lead-in for the inline language switcher rail. (visible-lead,
# aria-label). Visible-lead reads naturally before a comma-separated list of
# native-script language names; aria-label is the accessible name for the
# <aside> wrapper. Translations match the editorial register used elsewhere
# on the site — sub-agents that touch this file should not paraphrase.

# Curated rendering order — high-distribution markets first, then alphabetical
# by code for the long tail. Matches the publish-today dispatch order so the
# language rail visually mirrors the translation pipeline's priority.

# Match the closing </section> of the article hero followed by the opening
# <main>. Insertion target is exactly between them so the rail sits as a
# distinct band above the body — not competing with tag badges + meta bar
# inside the hero, not buried below the lead aside.








