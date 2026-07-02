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

import re
import sys
from html import escape as _esc
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












_TH_TEXT_RE = re.compile(r"<th\b[^>]*>([\s\S]*?)</th>", re.IGNORECASE)
_TR_RE = re.compile(r"<tr\b[\s\S]*?</tr>", re.IGNORECASE)
_TABLE_OPEN_RE = re.compile(r"<table\b([^>]*)>", re.IGNORECASE)
_TAG_STRIP_RE = re.compile(r"<[^>]+>")






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

# inject_anchor_links_and_toc stamps id="h2-..." on every PROSE h2
# (the ones with slugified anchors). The ToC / Lead / Sources asides
# use bare <h2> with no id, so this scoped regex naturally skips them.
_MIN_H2_FOR_RULES = 6
_FOOTNOTE_DEF_RE = re.compile(r"\[\^(\d+)\]:\s*([^\n<]+)")










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


















_OG_IMAGE_ALT_RE = re.compile(
    r'<meta\s+(?:property|name)="og:image:alt"\s+content="([^"]+)"',
    re.IGNORECASE,
)
_BANNER_ALT_FRONTMATTER_RE = re.compile(
    r'<meta\s+name="twitter:image:alt"\s+content="([^"]+)"',
    re.IGNORECASE,
)
# Fallback dimensions when the page has no og:image:width / og:image:height
# meta tags. Picked at 16:9 because that's the canonical hero aspect for
# CDN-transform URLs that don't carry a height. Used only as a last resort
# — every article since 2026-06-02 ships with explicit og:image dimensions.
_BANNER_FALLBACK_WIDTH = 1200
_BANNER_FALLBACK_HEIGHT = 675










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




_BODY_H1_RE = re.compile(
    r'(<main\b[^>]*>\s*<div class="wrap[^"]*">[\s\S]*?' r"(?:</aside>\s*)*)<h1>([^<]+)</h1>\s*",
    re.IGNORECASE,
)































# Local copies of the CSP-meta regexes (kept in postbuild.py too — both
# modules patch the same tag from different injection passes).
_csp_tag_re = re.compile(
    r'<meta\b[^>]*?http-equiv=["\']?Content-Security-Policy["\']?[^>]*?>',
    re.IGNORECASE,
)






_HEAD_END_RE = re.compile(r"</head>", re.IGNORECASE)
# Match a <link rel="alternate" hreflang=…> tag with any attribute order
# and either HTML5 (``>``) or XHTML (``/>``) self-close. The previous form
# required ``[^/]*/>`` which can never match real URLs (every ``https://``
# contains ``/``) — so the strip never fired and duplicates accumulated.


# Speculation Rules API — prerender same-origin pages on hover so any
# navigation feels instant. The CSP allows it via 'inline-speculationrules'
# in script-src; no per-page hash needed.










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








