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
from datetime import datetime as _datetime
from html import escape as _esc
from html import unescape as _unesc
from pathlib import Path
from urllib.parse import quote as _url_quote

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import _lang_registry as _lr

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
CITATION_AUTHORITIES = (
    "iso20022.org",
    "swift.com",
    "iso.org",
    "ietf.org",
    "w3.org",
    "nist.gov",
    "csrc.nist.gov",
    "bis.org",
    "ecb.europa.eu",
    "imf.org",
    "wikipedia.org",
    "wikidata.org",
    "arxiv.org",
    "ieee.org",
    "acm.org",
    "doi.org",
    "blackrock.com",
    "sec.gov",
    "treasury.gov",
    "ofac.treasury.gov",
    "hsbc.com",
    "jpmorgan.com",
    "santander.com",
    "bmo.com",
    "google.com",
    "openai.com",
    "anthropic.com",
    "deepmind.com",
    "github.com",
    "emergingpaymentsasia.org",
)

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
_OUTBOUND_LINK_RE = re.compile(r'<a\b[^>]*\bhref="(https?://[^"]+)"', re.IGNORECASE)
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from _core import DATED_SLUG_RE as _DATED_SLUG_RE  # canonical dated-slug matcher
from _svg_icons import (  # shared share-rail glyphs (Phase 4.2 dedup)
    _CARD_SVG_EMAIL as _SVG_EMAIL,
)
from _svg_icons import (
    _CARD_SVG_FB as _SVG_FB,
)
from _svg_icons import (
    _CARD_SVG_LI as _SVG_LI,
)
from _svg_icons import (
    _CARD_SVG_X as _SVG_X,
)
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


def inject_oembed_link(html: str) -> str:
    """Inject the `<link rel="alternate" type="application/json+oembed">`
    discovery link in the article's `<head>`. The href points at the
    static `/oembed/<slug>.json` file generated by
    `scripts/generators/build_oembed.py`. BlogPosting pages only;
    idempotent."""
    if '"@type":"BlogPosting"' not in html:
        return html
    if 'application/json+oembed' in html:
        return html
    canonical_m = _CANONICAL_RE.search(html)
    title_m = _OG_TITLE_RE.search(html)
    if not (canonical_m and title_m):
        return html
    url = canonical_m.group(1)
    # Strip /index.html, then drop the leading site domain to get the
    # bare slug. Canonicals look like https://sebastienrousseau.com/
    # <slug>/index.html or https://…/<slug>/.
    if url.endswith("/index.html"):
        url = url[: -len("/index.html")] + "/"
    bare = url.rstrip("/").rsplit("/", 1)[-1] or None
    if not bare:
        return html
    title = _unesc(title_m.group(1))
    oembed_href = f"{_BASE_URL}/oembed/{bare}.json"
    link = (
        f'<link rel="alternate" type="application/json+oembed" '
        f'href="{_esc(oembed_href, quote=True)}" '
        f'title="{_esc(title, quote=True)}">'
    )
    return html.replace("</head>", f"{link}</head>", 1)


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
_LEAD_TAKEAWAYS_RE = re.compile(
    r'<ul\s+class="post-lead-takeaways">(.*?)</ul>', re.IGNORECASE | re.DOTALL
)
_LI_CONTENT_RE = re.compile(r'<li>(.*?)</li>', re.IGNORECASE | re.DOTALL)
_HTML_TAGS_RE = re.compile(r'<[^>]+>')
_BODY_QUESTION_RE = re.compile(r'<p(?:\s[^>]*)?>([^<]{50,300}?\?)\s*</p>', re.IGNORECASE)
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


def _byline_role(is_fr: bool) -> str:
    return "FONDATEUR · INGÉNIEUR" if is_fr else "FOUNDER · ENGINEER"


def inject_byline_strap(html: str) -> str:
    """Render an FT-style byline strap (``NAME · ROLE`` in caps) at the
    foot of the article body, INSIDE the wrap-div so it ends up
    immediately before the prev/next pagination (which the later
    ``inject_prev_next_nav`` pass anchors on ``</div>\\s*</main>``).
    The strap signals the editorial credit attached to the foregoing
    piece — the same gesture FT Professional uses to close a Features
    post. BlogPosting pages only; idempotent."""
    if '"@type":"BlogPosting"' not in html:
        return html
    if 'class="byline-strap"' in html:
        return html
    labels = _labels(html)
    is_fr = _is_french(html)
    author_url = "/fr/a-propos/index.html" if is_fr else AUTHOR_URL
    role = _byline_role(is_fr)
    aria = _esc(labels.get("Byline", "Byline"), quote=True)
    strap = (
        f'<p class="byline-strap" aria-label="{aria}">'
        f'<a href="{author_url}">{_esc(AUTHOR_NAME.upper())}</a>'
        f' <span class="sep" aria-hidden="true">·</span> '
        f"<span>{_esc(role)}</span></p>"
    )
    return _WRAP_CLOSE_RE.sub(strap + r"\1", html, count=1)


def _share_li(href: str, label: str, glyph: str) -> str:
    return (
        f'<li><a href="{_esc(href, quote=True)}" rel="noopener noreferrer" '
        f'aria-label="{_esc(label, quote=True)}">{glyph}</a></li>'
    )


def _strip_html_tags(text: str) -> str:
    return _unesc(_HTML_TAGS_RE.sub("", text)).strip()


def _extract_lead_takeaways_text(html: str) -> list[str]:
    """Return plain-text bullet strings from the lead block takeaways list."""
    m = _LEAD_TAKEAWAYS_RE.search(html)
    if not m:
        return []
    items = []
    for li in _LI_CONTENT_RE.findall(m.group(1)):
        text = _strip_html_tags(li)
        if text:
            items.append(text)
    return items[:5]


def _extract_body_question(html: str) -> str:
    """Return the first short question-paragraph found in the article body."""
    for m in _BODY_QUESTION_RE.finditer(html):
        text = _strip_html_tags(m.group(1)).strip()
        if text.endswith("?"):
            return text
    return ""


def _keywords_to_hashtags(html: str, max_n: int = 5) -> list[str]:
    """Convert JSON-LD BlogPosting keywords to #CamelCase hashtags."""
    m = _keywords_re.search(html)
    if not m or not m.group(1):
        return []
    seen: set[str] = set()
    result: list[str] = []
    for tag in m.group(1).split(","):
        tag = tag.strip()
        if not tag:
            continue
        words = tag.replace("-", " ").replace("_", " ").replace("/", " ").split()
        hashtag = "#" + "".join(w.capitalize() for w in words)
        if hashtag not in seen:
            seen.add(hashtag)
            result.append(hashtag)
        if len(result) >= max_n:
            break
    return result


def _generate_linkedin_post(
    payload: dict[str, str], html: str, labels: dict[str, str]
) -> str:
    """Build a copy-ready LinkedIn post from article metadata and lead block.

    Structure (mirrors the Readable Framework the editorial team uses):
      Hook      — article title on its own line
      Opening   — first 1-2 sentences of the meta description
      Takeaways — bullet list extracted from the lead block (3-5 items)
      CTA       — engagement question found in the body or a locale fallback
      Link note — placeholder for the first-comment link
      Footer    — canonical URL + CC-BY-4.0 attribution
      Hashtags  — up to 5 #CamelCase tags from JSON-LD keywords
    """
    url, title, desc = payload["url"], payload["title"], payload["desc"]

    # Opening: first two short sentences of the description, max ~220 chars
    sentences = desc.replace("—", "-").split(". ")
    opening = sentences[0].rstrip(".")
    if len(sentences) > 1 and len(opening) < 120:
        second = sentences[1].rstrip(".")
        if len(opening) + len(second) + 2 < 220:
            opening = f"{opening}. {second}"
    opening = opening.rstrip(".") + "."

    # Bullet takeaways from lead block
    takeaways = _extract_lead_takeaways_text(html)
    intro = labels.get("Syndicate.linkedin_intro", "Here are the key strategic takeaways:")
    bullets = "\n".join(f"- {t}" for t in takeaways)

    # Engagement question: first short question-paragraph in body, else label fallback
    question = _extract_body_question(html) or labels.get(
        "Syndicate.linkedin_question",
        "What is your organisation's approach to the challenges outlined in this piece?",
    )

    hashtags = " ".join(_keywords_to_hashtags(html))

    parts: list[str] = [title, "", opening]
    if takeaways:
        parts += ["", intro, "", bullets]
    parts += ["", question, "", f"→ {url}"]
    if hashtags:
        parts += ["", hashtags]
    parts += ["", "Sebastien Rousseau | CC-BY-4.0"]
    return "\n".join(parts)


def _share_payload(html: str) -> dict[str, str] | None:
    """Extract canonical URL + og:title + meta description and return
    the per-platform pre-fill strings the share rail needs. Returns
    None if canonical or title is missing."""
    url_m = _CANONICAL_RE.search(html)
    title_m = _OG_TITLE_RE.search(html)
    if not (url_m and title_m):
        return None
    url = url_m.group(1)
    # Strip the /index.html canonical suffix so previews carry a clean
    # trailing-slash URL — browsers resolve either.
    if url.endswith("/index.html"):
        url = url[: -len("/index.html")] + "/"
    title = _unesc(title_m.group(1))
    desc_m = _DESCRIPTION_RE.search(html)
    desc = _unesc(desc_m.group(1)) if desc_m else ""
    return {
        "url": url,
        "title": title,
        "desc": desc,
    }


def _share_rail_items(payload: dict[str, str], labels: dict[str, str]) -> str:
    """Render the 5 share-rail <li> anchors. Per-platform pre-fill
    strategy (the richer the prompt, the more likely the reader
    actually shares — empty share dialogs get closed):

    * **X** — 280 char limit; title + URL fits, description usually
      doesn't, so it's omitted and the OG meta card carries the
      visual preview.
    * **LinkedIn** — the share-offsite dialog ignores ``?text=`` today,
      so we open the feed composer (``?shareActive=true``) with
      title + description + URL pre-filled. That's the
      "Share your thoughts…" prompt the FT pattern lives in.
    * **Facebook** — stripped all ``?quote=`` support in 2017. Only
      the URL gets through; OG meta drives the preview card.
    * **WhatsApp + email** — no length cap, so they get the full
      title + description + URL share-card payload.
    """
    url, title, desc = payload["url"], payload["title"], payload["desc"]
    x_text = f"{title}\n\n{url}"
    wa_text = "\n\n".join(p for p in (title, desc, url) if p)
    email_body = "\n\n".join(p for p in (desc, f"Read more: {url}") if p)
    li_text = "\n\n".join(p for p in (title, desc, url) if p)
    enc_url = _url_quote(url, safe="")
    enc_title = _url_quote(title, safe="")
    return (
        _share_li(
            f"https://twitter.com/intent/tweet?text={_url_quote(x_text, safe='')}",
            labels.get("Share.x", "Share on X"),
            _SVG_X,
        )
        + _share_li(
            f"https://www.linkedin.com/feed/?shareActive=true&text={_url_quote(li_text, safe='')}",
            labels.get("Share.linkedin", "Share on LinkedIn"),
            _SVG_LI,
        )
        + _share_li(
            f"https://www.facebook.com/sharer/sharer.php?u={enc_url}",
            labels.get("Share.facebook", "Share on Facebook"),
            _SVG_FB,
        )
        + _share_li(
            f"https://wa.me/?text={_url_quote(wa_text, safe='')}",
            labels.get("Share.whatsapp", "Share on WhatsApp"),
            _SVG_WA,
        )
        + _share_li(
            f"mailto:?subject={enc_title}&body={_url_quote(email_body, safe='')}",
            labels.get("Share.email", "Share by email"),
            _SVG_EMAIL,
        )
        + _share_li(
            # Bluesky's compose intent accepts ?text= with title+URL —
            # 300 char post limit so we send title + URL like X.
            f"https://bsky.app/intent/compose?text={_url_quote(x_text, safe='')}",
            labels.get("Share.bluesky", "Share on Bluesky"),
            _SVG_BLUESKY,
        )
    )


def _syndication_payloads(
    payload: dict[str, str], html: str, labels: dict[str, str]
) -> dict[str, str]:
    """Return pre-formatted text payloads for platforms that don't
    accept ?text= compose intents — Medium (markdown import), Mastodon
    (no universal share URL across instances), LinkedIn (structured
    thought-leadership post). The reader copies and pastes into the
    platform of their choice."""
    url, title, desc = payload["url"], payload["title"], payload["desc"]
    # Medium import-style markdown — Medium's web importer reads the
    # first H1 + body. The canonical link goes at the top so the
    # Medium copy preserves the canonical URL.
    medium_md = "\n\n".join(
        p
        for p in (
            f"# {title}",
            f"> Originally published at [{url}]({url})",
            desc,
            f"Read the full article on sebastienrousseau.com: {url}",
        )
        if p
    )
    # Mastodon toot — 500 char limit on mastodon.social. Title +
    # truncated description + URL.
    desc_trunc = desc[:300].rstrip()
    if len(desc) > 300:
        desc_trunc += "…"
    mastodon = "\n\n".join(p for p in (title, desc_trunc, url) if p)
    linkedin = _generate_linkedin_post(payload, html, labels)
    return {"medium": medium_md, "mastodon": mastodon, "linkedin": linkedin}


def _render_syndication_panel(
    payload: dict[str, str], labels: dict[str, str], html: str
) -> str:
    """Inline collapsible at the article foot with copy buttons for
    Medium, Mastodon, and LinkedIn. Each pre block has a stable id so
    main.js's existing [data-copy] handler wires the clipboard."""
    payloads = _syndication_payloads(payload, html, labels)
    blocks = []
    label_map = {
        "medium": labels.get("Syndicate.medium", "Format for Medium"),
        "mastodon": labels.get("Syndicate.mastodon", "Format for Mastodon"),
        "linkedin": labels.get("Syndicate.linkedin", "Copy formatted for LinkedIn"),
    }
    copy_label = _esc(labels.get("Cite.copy", "Copy"))
    for key, body in payloads.items():
        target_id = f"syndicate-{key}"
        blocks.append(
            f'<div class="cite-format">'
            f"<h3>{_esc(label_map[key])}</h3>"
            f'<pre id="{target_id}">{_esc(body)}</pre>'
            f'<button type="button" class="copy-btn" data-copy="#{target_id}" '
            f'aria-label="{_esc(label_map[key], quote=True)} — {copy_label}">'
            f"{copy_label}</button>"
            f"</div>"
        )
    heading = _esc(labels.get("Syndicate.heading", "Syndicate this article"))
    return (
        f'<details class="cite-popover" id="syndicate-popover">'
        f"<summary>{heading}</summary>"
        + "".join(blocks)
        + "</details>"
    )


def inject_syndication_panel(html: str) -> str:
    """Append a syndication payload panel at the wrap-div close —
    pre-formatted blocks for Medium import, Mastodon, and LinkedIn,
    each with a copy button. Bluesky has a compose-intent URL so it
    joins the share rail directly; Medium, Mastodon, and LinkedIn have
    no universal share URL so the panel is the only path. BlogPosting
    pages only; idempotent."""
    if '"@type":"BlogPosting"' not in html:
        return html
    if 'id="syndicate-popover"' in html:
        return html
    payload = _share_payload(html)
    if payload is None:
        return html
    panel = _render_syndication_panel(payload, _labels(html), html)
    return _WRAP_CLOSE_RE.sub(panel + r"\1", html, count=1)


def inject_share_rail(html: str) -> str:
    """Render an FT-style vertical share rail (X / LinkedIn / Facebook
    / WhatsApp / email / Bluesky) at the top of the article body. CSS
    makes it ``position: sticky`` on >=64em and flows it inline on
    mobile. Anchors only — no inline JavaScript, CSP-safe.
    Medium / Mastodon payloads ship via inject_syndication_panel at
    the wrap-div close (no universal share URL). BlogPosting pages
    only; idempotent."""
    if '"@type":"BlogPosting"' not in html:
        return html
    if 'class="share-rail share-rail--sticky"' in html:
        return html
    payload = _share_payload(html)
    if payload is None:
        return html
    items = _share_rail_items(payload, _labels(html))
    aria = _esc(_labels(html).get("Share", "Share"), quote=True)
    rail = (
        f'<nav class="share-rail share-rail--sticky" aria-label="{aria}">'
        f"<ul>{items}</ul></nav>"
    )
    return _MAIN_RE.sub(rf"\1{rail}\2\3", html, count=1)


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

_LICENSE_RE = re.compile(r'<meta\s+name="license"\s+content="([^"]+)"', re.IGNORECASE)
_LICENSE_DEFAULT = "CC-BY-4.0"
_LICENSE_LABELS: dict[str, str] = {
    "CC-BY-4.0": "Creative Commons Attribution 4.0 International",
    "CC-BY-SA-4.0": "Creative Commons Attribution-ShareAlike 4.0 International",
    "CC-BY-NC-SA-4.0": "Creative Commons Attribution-NonCommercial-ShareAlike 4.0",
    "CC-BY-ND-4.0": "Creative Commons Attribution-NoDerivatives 4.0 International",
    "All-Rights-Reserved": "All rights reserved",
}
_LICENSE_URLS: dict[str, str] = {
    "CC-BY-4.0": "https://creativecommons.org/licenses/by/4.0/",
    "CC-BY-SA-4.0": "https://creativecommons.org/licenses/by-sa/4.0/",
    "CC-BY-NC-SA-4.0": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
    "CC-BY-ND-4.0": "https://creativecommons.org/licenses/by-nd/4.0/",
}

_AUTHOR_LAST = "Rousseau"
_AUTHOR_FIRST = "Sebastien"
_AUTHOR_INITIAL = "S."

# 14x14 monochrome SVG glyphs (currentColor fill) for the action rail.
_SVG_DOWNLOAD = (
    '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false">'
    '<path d="M7.3 1.5h1.4v6l1.95-1.95.99.99L8 9.18 4.36 5.54l.99-.99L7.3 6.5v-5zM2 13h12v1.5H2V13z"/>'
    "</svg>"
)
_SVG_QUOTE = (
    '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false">'
    '<path d="M3 4.5h3.5v3.5H5c0 1.5.5 2.5 1.5 3v1c-2 0-3.5-2-3.5-4V4.5zm6.5 0H13v3.5h-1.5'
    'c0 1.5.5 2.5 1.5 3v1c-2 0-3.5-2-3.5-4V4.5z"/>'
    "</svg>"
)


def _slug_from_canonical(html: str) -> str | None:
    """Return the bare slug from the canonical URL. Canonical URLs on
    this site always end with ``/<slug>/index.html``; strip that suffix
    before taking the last path segment so PDF / oEmbed routes get
    ``/api/pdf/<slug>.pdf`` and not ``/api/pdf/index.html.pdf``."""
    m = _CANONICAL_RE.search(html)
    if not m:
        return None
    url = m.group(1)
    for suffix in ("/index.html", "/"):
        if url.endswith(suffix):
            url = url[: -len(suffix)]
            break
    return url.rsplit("/", 1)[-1] or None


def _license_id(html: str) -> str:
    m = _LICENSE_RE.search(html)
    if m:
        candidate = m.group(1).strip()
        if candidate in _LICENSE_LABELS:
            return candidate
    return _LICENSE_DEFAULT


def inject_action_rail(html: str) -> str:
    """Render the floating ``.action-rail--sticky`` with Save PDF + Cite
    at the top of the article body. The CSS positions it on the right
    edge on >=64em viewports and as a sticky bottom bar on <48em.

    Save PDF is an anchor to ``/api/pdf/<slug>.pdf`` — the Cloudflare
    Worker (workers/pdf-proxy.js) forwards to the Fly.io WeasyPrint
    service and Edge-caches the response immutable for 24h. The
    ``download`` attribute hints the browser to save rather than
    navigate. A ``data-print-fallback`` hook on the same anchor lets
    main.js fall back to ``window.print()`` if the route ever 503s
    (e.g. local dev without the Worker).

    Cite jumps to the popover. BlogPosting pages only; idempotent."""
    if '"@type":"BlogPosting"' not in html:
        return html
    if 'class="action-rail action-rail--sticky"' in html:
        return html
    slug = _slug_from_canonical(html)
    if not slug:
        return html
    labels = _labels(html)
    aria = _esc(labels.get("Action.aria", "Article actions"), quote=True)
    pdf_href = f"/api/pdf/{slug}.pdf"
    items = (
        f'<li><a href="{pdf_href}" download="{slug}.pdf" '
        f'data-print-fallback rel="alternate" type="application/pdf">'
        f'{_SVG_DOWNLOAD}'
        f'<span>{_esc(labels.get("Action.savePdf", "Save PDF"))}</span></a></li>'
        f'<li><a href="#cite-popover">{_SVG_QUOTE}'
        f'<span>{_esc(labels.get("Action.cite", "Cite"))}</span></a></li>'
    )
    rail = (
        f'<nav class="action-rail action-rail--sticky" aria-label="{aria}">'
        f"<ul>{items}</ul></nav>"
    )
    return _MAIN_RE.sub(rf"\1{rail}\2\3", html, count=1)


def _parse_iso_date(date_str: str) -> _datetime | None:
    if not date_str:
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%d"):
        try:
            return _datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def _first_word(title: str) -> str:
    m = re.search(r"\w+", title)
    return m.group(0).lower() if m else "post"


def _citation_blocks(title: str, url: str, date_str: str) -> dict[str, str]:
    """Render the 5 academic citation formats from article metadata."""
    dt = _parse_iso_date(date_str)
    year = str(dt.year) if dt else "n.d."
    month_short = dt.strftime("%b") if dt else ""
    month_long = dt.strftime("%B") if dt else ""
    day = str(dt.day) if dt else ""
    author_lastfirst = f"{_AUTHOR_LAST}, {_AUTHOR_FIRST}"
    author_vancouver = f"{_AUTHOR_LAST} {_AUTHOR_INITIAL[0]}"
    author_apa = f"{_AUTHOR_LAST}, {_AUTHOR_INITIAL}"
    bib_key = f"{_AUTHOR_LAST.lower()}{year}{_first_word(title)}"
    bibtex = (
        f"@online{{{bib_key},\n"
        f"  author  = {{{author_lastfirst}}},\n"
        f"  title   = {{{{{title}}}}},\n"
        f"  year    = {{{year}}},\n"
        f"  url     = {{{url}}},\n"
        f"  urldate = {{{year}}}\n"
        f"}}"
    )
    ris = (
        f"TY  - GEN\n"
        f"AU  - {author_lastfirst}\n"
        f"TI  - {title}\n"
        f"PY  - {year}\n"
        f"UR  - {url}\n"
        f"ER  -"
    )
    vancouver = (
        f"{author_vancouver}. {title}. sebastienrousseau.com. "
        f"{year} {month_short} {day}. Available from: {url}"
    )
    chicago = f'{author_lastfirst}. "{title}." sebastienrousseau.com. {month_long} {day}, {year}. {url}.'
    apa = f"{author_apa} ({year}, {month_long} {day}). {title}. sebastienrousseau.com. {url}"
    return {
        "BibTeX": bibtex,
        "RIS": ris,
        "Vancouver": vancouver,
        "Chicago": chicago,
        "APA": apa,
    }


def inject_cite_popover(html: str) -> str:
    """Append a zero-JS ``<details class="cite-popover" id="cite-popover">``
    block at the wrap-div close, with one ``<pre>`` per citation format
    (BibTeX / RIS / Vancouver / Chicago / APA). The action-rail's
    "Cite" button jumps here. WS5 will wire copy-to-clipboard
    buttons + main.js handlers; for now readers select-all + copy
    from the <pre>. BlogPosting pages only; idempotent.

    Idempotency gates on the ``id="cite-popover"`` anchor rather than
    the class — `inject_syndication_panel` runs first and also uses
    ``class="cite-popover"`` for shared FT styling (with
    ``id="syndicate-popover"``). Without the ID-based gate, the
    syndicate-popover's class match short-circuits this injector and
    the action-rail's ``href="#cite-popover"`` resolves to no target
    (pa11y WCAG2AAA NoSuchID)."""
    if '"@type":"BlogPosting"' not in html:
        return html
    if 'id="cite-popover"' in html:
        return html
    url_m = _CANONICAL_RE.search(html)
    title_m = _OG_TITLE_RE.search(html)
    if not (url_m and title_m):
        return html
    url = url_m.group(1)
    title = _unesc(title_m.group(1))
    _kw, date_pub, _dm, _wc = _extract_article_metadata(html)
    formats = _citation_blocks(title, url, date_pub)
    labels = _labels(html)
    copy_label = _esc(labels.get("Cite.copy", "Copy"))
    # Meta header — title + description give the reader context before
    # they commit to a citation format. Description comes from the
    # canonical <meta name="description"> the article already carries.
    desc_m = _DESCRIPTION_RE.search(html)
    desc = _unesc(desc_m.group(1)) if desc_m else ""
    # Heading-skip-safe: the cite popover is a <details> disclosure
    # widget whose <summary> already serves as the accessible name.
    # An <h3> here under the article's body <h2>s would still parse,
    # but inside a closed <details> the screen-reader heading tree
    # gets confusing. Use a <p class="cite-title"> with strong text
    # — same visual weight, no heading-skip claim.
    meta_block = (
        f'<header class="cite-meta">'
        f'<p class="cite-title"><strong>{_esc(title)}</strong></p>'
        + (f"<p>{_esc(desc)}</p>" if desc else "")
        + "</header>"
    )
    blocks = []
    for name, body in formats.items():
        target_id = f"cite-{name.lower()}"
        blocks.append(
            f'<div class="cite-format"><h3>{_esc(name)}</h3>'
            f'<pre id="{target_id}">{_esc(body)}</pre>'
            f'<button type="button" class="copy-btn" data-copy="#{target_id}" '
            f'aria-label="{_esc(name, quote=True)} — {copy_label}">{copy_label}</button>'
            f"</div>"
        )
    popover = (
        f'<details class="cite-popover" id="cite-popover">'
        f'<summary>{_esc(labels.get("Cite.heading", "Cite this article"))}</summary>'
        + meta_block
        + "".join(blocks)
        + "</details>"
    )
    return _WRAP_CLOSE_RE.sub(popover + r"\1", html, count=1)


def inject_reuse_panel(html: str) -> str:
    """Append a republish / reuse panel at the wrap-div close: licence
    statement, machine-readable ``rel="license"`` link, attribution
    snippet in a ``<pre>``. License id comes from
    ``<meta name="license">`` (or defaults to CC-BY-4.0) and must be
    on the allow-list; unknown ids fall back to the default rather
    than emitting a broken licence URL. BlogPosting pages only;
    idempotent."""
    if '"@type":"BlogPosting"' not in html:
        return html
    if 'class="reuse"' in html:
        return html
    url_m = _CANONICAL_RE.search(html)
    title_m = _OG_TITLE_RE.search(html)
    if not (url_m and title_m):
        return html
    url = url_m.group(1)
    title = _unesc(title_m.group(1))
    license_id = _license_id(html)
    license_label = _LICENSE_LABELS[license_id]
    license_url = _LICENSE_URLS.get(license_id)
    labels = _labels(html)
    if license_url:
        license_a = f'<a rel="license" href="{license_url}">{_esc(license_label)}</a>'
    else:
        license_a = _esc(license_label)
    # Description for the visible share-card preview AND the multi-line
    # attribution payload. Falls back to "" when the article has no
    # meta description (rare; default articles do).
    desc_m = _DESCRIPTION_RE.search(html)
    desc = _unesc(desc_m.group(1)) if desc_m else ""
    # Same heading-skip-safe pattern as the cite popover: the panel's
    # <h2 id="reuse-heading"> ("Republish this article") IS the
    # section heading; the title preview is a strong paragraph, not
    # another h-level inside it.
    meta_block = (
        f'<header class="reuse-meta">'
        f'<p class="reuse-title"><strong>{_esc(title)}</strong></p>'
        + (f"<p>{_esc(desc)}</p>" if desc else "")
        + "</header>"
    )
    # Richer multi-line attribution so the pasted block reads as a
    # complete share card, not a one-liner. Title + description give
    # republishers immediate context; URL + author + licence carry
    # the legal attribution requirement. The visible URL drops the
    # /index.html canonical suffix so the share payload reads
    # naturally — browsers resolve either form.
    share_url = url[: -len("/index.html")] + "/" if url.endswith("/index.html") else url
    attribution_lines = [title]
    if desc:
        attribution_lines.extend(["", desc])
    attribution_lines.extend(
        [
            "",
            f"Originally published at {share_url} by {_AUTHOR_FIRST} {_AUTHOR_LAST}.",
            f"Licensed under {license_id}.",
        ]
    )
    attribution = "\n".join(attribution_lines)
    copy_label = _esc(labels.get("Reuse.copy", "Copy attribution"))
    panel = (
        f'<section class="reuse" aria-labelledby="reuse-heading">'
        f'<h2 id="reuse-heading">'
        f'{_esc(labels.get("Reuse.heading", "Republish this article"))}</h2>'
        + meta_block
        + f"<p>{_esc(labels.get('Reuse.license', 'This article is licensed under'))} "
        + f"{license_a}. "
        + f"{_esc(labels.get('Reuse.attribution', 'Republication requires attribution to the canonical URL.'))}</p>"
        + f'<pre id="reuse-attribution">{_esc(attribution)}</pre>'
        + '<button type="button" class="copy-btn" data-copy="#reuse-attribution" '
        + f'aria-label="{copy_label}">{copy_label}</button>'
        + "</section>"
    )
    return _WRAP_CLOSE_RE.sub(panel + r"\1", html, count=1)


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


_NON_BODY_ASIDE_RE = re.compile(
    r'<aside\s+class="(?:author-card|related-posts|post-lead|article-sources|article-toc)\b[^"]*"[\s\S]*?</aside>',
    re.IGNORECASE,
)


def _extract_citations(html: str) -> list[dict[str, str]]:
    """Return at most 12 distinct authoritative outbound links from the
    article body. Strips author-card / related-posts / post-lead / ToC /
    article-sources asides first so the author's own profile links and
    nav chrome don't pollute the citation graph."""
    main_m = _MAIN_RE.search(html)
    if not main_m:
        return []
    body = _NON_BODY_ASIDE_RE.sub("", main_m.group(2))
    seen: set[str] = set()
    out: list[dict[str, str]] = []
    for lm in _OUTBOUND_LINK_RE.finditer(body):
        url = lm.group(1)
        if url in seen:
            continue
        seen.add(url)
        host = url.split("/", 3)[2].lower() if url.count("/") >= 2 else ""
        if not any(host == d or host.endswith("." + d) for d in CITATION_AUTHORITIES):
            continue
        out.append({"@type": "CreativeWork", "url": url})
        if len(out) >= 12:
            break
    return out


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


def build_fr_title_index(pages: list[Path]) -> dict[str, str]:
    """Walk rendered FR pages, return ``en_slug -> FR H1 title`` so the
    prev/next nav on a FR page can advertise the FR title for the
    neighbouring article instead of the English H1.
    """
    out: dict[str, str] = {}
    fr_articles_map = _lr.load_slugs("fr").get("articles", {})
    fr_to_en = {v: k for k, v in fr_articles_map.items()}
    for p in pages:
        if p.parent.parent.name != "fr":
            continue
        slug = p.parent.name  # FR slug
        if not _DATED_SLUG_RE.match(slug):
            continue
        en = fr_to_en.get(slug, slug)
        if en == slug:  # not in slug map
            continue
        html = p.read_text(encoding="utf-8", errors="ignore")
        m = _H1_RE.search(html)
        if m:
            out[en] = m.group(1).strip()
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


def inject_citations(html: str) -> str:
    """Append a "citation" array to the BlogPosting JSON-LD listing the
    authoritative outbound URLs the post references. AI engines extract
    citation graphs from this property to build provenance chains."""
    if '"@type":"BlogPosting"' not in html:
        return html
    cites = _extract_citations(html)
    if not cites:
        return html
    fragment = ',"citation":' + _json.dumps(cites, separators=(",", ":"))
    # Insert just before the "speakable" key in the BlogPosting object.
    return re.sub(
        r'(,"speakable":)',
        fragment + r"\1",
        html,
        count=1,
    )


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


def inject_sources_list(html: str) -> str:
    """Mirror the JSON-LD citation array as a human-visible <aside> so the
    primary-source references are visible to readers, not just AI crawlers.
    Inserted just before the prev/next nav so it sits at the foot of every
    dated post. Idempotent."""
    if '"@type":"BlogPosting"' not in html:
        return html
    if 'class="article-sources"' in html:
        return html
    cites = _extract_citations(html)
    if not cites:
        return html
    items: list[str] = []
    for c in cites:
        url = c["url"]
        parts = url.split("/", 3)
        host = parts[2] if len(parts) > 2 else url
        path = "/" + parts[3] if len(parts) > 3 else ""
        display = path if len(path) <= 80 else path[:77] + "…"
        items.append(
            f'<li><a href="{url}" rel="external noopener nofollow">'
            f'<span class="source-host">{host}</span>'
            f'<span class="source-path">{display}</span>'
            f"</a></li>"
        )
    heading = _labels(html)["Sources & references"]
    fragment = (
        '<aside class="article-sources" aria-labelledby="sources-heading">'
        f'<h2 id="sources-heading" class="article-sources-heading">{heading}</h2>'
        f'<ol class="article-sources-list">{"".join(items)}</ol>'
        '</aside>'
    )
    # Insert before the prev/next nav if it's already there, else before
    # the closing </div></main>.
    if 'class="post-pagination"' in html:
        return re.sub(r'(<nav class="post-pagination")', fragment + r"\1", html, count=1)
    return re.sub(r"(</div>\s*</main>)", fragment + r"\1", html, count=1)


_HEAD_END_RE = re.compile(r"</head>", re.IGNORECASE)
# Match a <link rel="alternate" hreflang=…> tag with any attribute order
# and either HTML5 (``>``) or XHTML (``/>``) self-close. The previous form
# required ``[^/]*/>`` which can never match real URLs (every ``https://``
# contains ``/``) — so the strip never fired and duplicates accumulated.
_HREFLANG_RE = re.compile(
    r'<link\b(?=[^>]*\brel=["\']?alternate["\']?)(?=[^>]*\bhreflang=)[^>]*/?>',
    re.IGNORECASE,
)


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










def _translated_slugs_per_lang() -> dict[str, set[str]]:
    """Return ``{code: set_of_rendered_slugs}`` for every active non-EN
    language whose output dir exists under ``public/``."""
    out: dict[str, set[str]] = {}
    for code in _all_active_non_en_langs():
        d = PUBLIC / code
        if not d.is_dir():
            continue
        out[code] = {p.parent.name for p in d.glob("*/index.html")}
    return out


def _translated_slugs() -> tuple[set[str], set[str]]:
    """Legacy FR-only helper. Returns ``(en_slugs_with_fr,
    fr_slugs_with_en)`` for the call sites that haven't yet moved to
    the lang-keyed API."""
    fr_dir = PUBLIC / "fr"
    if not fr_dir.is_dir():
        return set(), set()
    rendered_fr = {p.parent.name for p in fr_dir.glob("*/index.html")}
    fr_articles_map = _lr.load_slugs("fr").get("articles", {})
    en_with_fr = {en for en, fr in fr_articles_map.items() if fr in rendered_fr}
    fr_to_en = {v: k for k, v in fr_articles_map.items()}
    fr_with_en = rendered_fr & set(fr_to_en.keys())
    return en_with_fr, fr_with_en


def _resolve_en_slug(slug: str, lang: str) -> str | None:
    """Reverse-map any language's slug to its EN counterpart."""
    if lang == "en":
        return slug
    maps = _slug_maps(lang)
    return maps["articles_lang_to_en"].get(slug) or maps["statics_lang_to_en"].get(slug)


def _alternates_for_en_slug(
    en_slug: str,
    translated_per_lang: dict[str, set[str]],
) -> list[tuple[str, str]]:
    """Build the full ``[(lang_code, absolute_url), …]`` alternate list
    for an EN slug."""
    alts: list[tuple[str, str]] = [
        ("en", f"https://sebastienrousseau.com/{en_slug}/"),
    ]
    for code in _all_active_non_en_langs():
        maps = _slug_maps(code)
        lang_slug = maps["articles_en_to_lang"].get(en_slug) or maps["statics_en_to_lang"].get(
            en_slug
        )
        if not lang_slug:
            continue
        if lang_slug not in translated_per_lang.get(code, set()):
            continue
        alts.append((code, f"https://sebastienrousseau.com/{code}/{lang_slug}/"))
    return alts


# Per-locale lead-in for the inline language switcher rail. (visible-lead,
# aria-label). Visible-lead reads naturally before a comma-separated list of
# native-script language names; aria-label is the accessible name for the
# <aside> wrapper. Translations match the editorial register used elsewhere
# on the site — sub-agents that touch this file should not paraphrase.
_LANG_SWITCH_STRINGS: dict[str, tuple[str, str]] = {
    "en": ("This post is also available in", "Available languages"),
    "fr": ("Cet article est aussi disponible en", "Langues disponibles"),
    "es": ("Este artículo también está disponible en", "Idiomas disponibles"),
    "de": ("Dieser Artikel ist auch verfügbar auf", "Verfügbare Sprachen"),
    "it": ("Questo articolo è disponibile anche in", "Lingue disponibili"),
    "pt-br": ("Este artigo também está disponível em", "Idiomas disponíveis"),
    "nl": ("Dit artikel is ook beschikbaar in", "Beschikbare talen"),
    "ja": ("この記事は次の言語でもご覧いただけます", "対応言語"),
    "zh-hans": ("本文亦提供以下语言版本", "可用语言"),
    "zh-hant": ("本文亦提供以下語言版本", "可用語言"),
    "ko": ("이 글은 다음 언어로도 제공됩니다", "지원 언어"),
    "ar": ("هذه المقالة متوفرة أيضًا باللغات", "اللغات المتوفرة"),
    "ru": ("Эта статья также доступна на", "Доступные языки"),
    "pl": ("Ten artykuł jest również dostępny w", "Dostępne języki"),
    "cs": ("Tento článek je k dispozici také v", "Dostupné jazyky"),
    "uk": ("Ця стаття також доступна", "Доступні мови"),
    "ro": ("Acest articol este disponibil și în", "Limbi disponibile"),
    "tr": ("Bu makale şu dillerde de mevcuttur", "Mevcut diller"),
    "he": ("מאמר זה זמין גם בשפות", "שפות זמינות"),
    "hi": ("यह लेख इन भाषाओं में भी उपलब्ध है", "उपलब्ध भाषाएँ"),
    "bn": ("এই নিবন্ধটি এই ভাষাগুলিতেও উপলব্ধ", "উপলব্ধ ভাষাসমূহ"),
    "id": ("Artikel ini juga tersedia dalam", "Bahasa yang tersedia"),
    "vi": ("Bài viết này cũng có sẵn bằng", "Ngôn ngữ có sẵn"),
    "th": ("บทความนี้มีให้ในภาษาต่อไปนี้ด้วย", "ภาษาที่ใช้ได้"),
    "fil": ("Available rin ang artikulong ito sa", "Mga available na wika"),
    "ha": ("Wannan labarin yana samuwa kuma a cikin", "Harsunan da ake samu"),
    "yo": ("Àpilẹ̀kọ yìí tún wà ní", "Àwọn èdè tó wà"),
    "sv": ("Den här artikeln finns även på", "Tillgängliga språk"),
}

# Curated rendering order — high-distribution markets first, then alphabetical
# by code for the long tail. Matches the publish-today dispatch order so the
# language rail visually mirrors the translation pipeline's priority.
_LANG_SWITCH_ORDER: tuple[str, ...] = (
    "fr",
    "es",
    "de",
    "it",
    "pt-br",
    "nl",
    "ja",
    "zh-hans",
    "zh-hant",
    "ko",
    "ar",
    "ru",
    "pl",
    "cs",
    "uk",
    "ro",
    "tr",
    "he",
    "hi",
    "bn",
    "id",
    "vi",
    "th",
    "fil",
    "ha",
    "yo",
    "sv",
    "en",
)

# Match the closing </section> of the article hero followed by the opening
# <main>. Insertion target is exactly between them so the rail sits as a
# distinct band above the body — not competing with tag badges + meta bar
# inside the hero, not buried below the lead aside.
_LANG_SWITCH_INSERT_RE = re.compile(
    r"(</section>)(\s*<main\b)",
    re.IGNORECASE,
)


def _render_lang_switch_item(
    code: str,
    href: str,
) -> str:
    """One <li><a> for the lang rail. Sets lang + hreflang + dir=rtl when
    appropriate so screen readers pronounce the native label correctly."""
    lang_obj = _lr.get(code)
    rtl_attr = ' dir="rtl"' if lang_obj.rtl else ""
    return (
        f'<li><a href="{href}" lang="{lang_obj.bcp47}" hreflang="{lang_obj.bcp47}"'
        f' rel="alternate"{rtl_attr}>{lang_obj.long_label}</a></li>'
    )


def _lang_switch_others(
    en_slug: str,
    lang: str,
    translated_per_lang: dict[str, set[str]],
) -> list[tuple[str, str]]:
    """Return ``[(code, relative_href), …]`` for every locale this article
    is available in, excluding the current page's lang, in the
    :data:`_LANG_SWITCH_ORDER` priority order."""
    alts = _alternates_for_en_slug(en_slug, translated_per_lang)
    by_code = {code: url.replace("https://sebastienrousseau.com", "", 1) for code, url in alts}
    return [
        (code, by_code[code]) for code in _LANG_SWITCH_ORDER if code in by_code and code != lang
    ]


def inject_lang_switcher(
    html: str,
    slug: str,
    lang: str,
    translated_per_lang: dict[str, set[str]],
) -> str:
    """Insert an inline per-article language switcher between the hero
    and the article body.

    Surfaces the 28-locale advantage to readers as content, not chrome.
    Different from the site-wide ``.ap-lang-item`` dropdown — that's nav
    furniture; this is editorial. Both can coexist on the same page.

    Idempotent. Skips:
      - pages without the BlogPosting JSON-LD anchor (listing / static)
      - pages already carrying a ``.article-langswitch`` block
      - articles available in fewer than two locales (no rail needed)
    """
    if '"@type":"BlogPosting"' not in html:
        return html
    if 'class="article-langswitch"' in html:
        return html
    en_slug = _resolve_en_slug(slug, lang)
    if en_slug is None:
        return html
    others = _lang_switch_others(en_slug, lang, translated_per_lang)
    if not others:
        return html

    lead_text, aria_label = _LANG_SWITCH_STRINGS.get(
        lang,
        _LANG_SWITCH_STRINGS["en"],
    )
    items = "".join(_render_lang_switch_item(c, h) for c, h in others)
    aside = (
        f'<aside class="article-langswitch" aria-label="{aria_label}">'
        f'<span class="article-langswitch-lead">{lead_text}</span> '
        f'<ul class="article-langswitch-list">{items}</ul>'
        f"</aside>"
    )

    new_html, n = _LANG_SWITCH_INSERT_RE.subn(
        lambda m: f"{m.group(1)}{aside}{m.group(2)}",
        html,
        count=1,
    )
    return new_html if n else html


def inject_hreflang(
    html: str,
    slug: str,
    lang: str,
    translated_per_lang: dict[str, set[str]] | None = None,
    *,
    en_with_fr: set[str] | None = None,
    fr_with_en: set[str] | None = None,
) -> str:
    """Inject reciprocal hreflang links so search crawlers + the
    language-selector JS pair every translated version of a page."""
    if translated_per_lang is None:
        translated_per_lang = {}
        if fr_with_en:
            translated_per_lang["fr"] = fr_with_en
    en_slug = _resolve_en_slug(slug, lang)
    if en_slug is None:
        return html
    alts = _alternates_for_en_slug(en_slug, translated_per_lang)
    if len(alts) < 2:
        return html
    en_url = alts[0][1]
    html = _HREFLANG_RE.sub("", html)
    links = "".join(
        f'<link rel="alternate" hreflang="{code}" href="{url}" />' for code, url in alts
    )
    links += f'<link rel="alternate" hreflang="x-default" href="{en_url}" />'
    return _HEAD_END_RE.sub(links + "</head>", html, count=1)
