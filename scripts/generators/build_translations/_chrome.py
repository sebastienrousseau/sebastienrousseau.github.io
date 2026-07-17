"""Page-level chrome / HTML rewriting.

Everything here transforms a rendered English shell in place: head-meta
regex patches, ``<html lang>`` swapping, nav/footer chrome translation,
date localisation, static-link rewriting, and the JSON-LD parse +
mutate + re-serialise passes.
"""

from __future__ import annotations

import json as _json
import re
import sys
from collections.abc import Callable

from . import _state as st

# ---------------------------------------------------------------------------
# Head / meta regexes
# ---------------------------------------------------------------------------

_MAIN_BODY_RE = re.compile(
    r'(<main\b[^>]*>\s*<div class="wrap[^"]*">)([\s\S]*?)(</div>\s*</main>)',
    re.IGNORECASE,
)
_HERO_RE = re.compile(
    r'(<section class="ap-hero">\s*<h1>)[^<]*(</h1>\s*<p class="sub">)[^<]*(</p>)',
    re.IGNORECASE,
)
_TITLE_RE = re.compile(r"<title>[^<]*</title>", re.IGNORECASE)
_DESC_META_RE = re.compile(r'(<meta\s+name="description"\s+content=")[^"]*(")', re.IGNORECASE)
_KW_META_RE = re.compile(r'(<meta\s+name="keywords"\s+content=")[^"]*(")', re.IGNORECASE)
_HTML_LANG_RE = re.compile(r'(<html\b[^>]*\blang=)"?[^"\s>]*"?', re.IGNORECASE)
_HTML_DIR_RE = re.compile(r'(<html\b[^>]*?)\s+dir="[^"]*"', re.IGNORECASE)
_HTML_OPEN_RE = re.compile(r"(<html\b[^>]*?)(>)", re.IGNORECASE)

_OG_TITLE_RE = re.compile(r'(<meta\s+property="og:title"\s+content=")[^"]*(")', re.IGNORECASE)
_OG_DESC_RE = re.compile(r'(<meta\s+property="og:description"\s+content=")[^"]*(")', re.IGNORECASE)
_OG_URL_RE = re.compile(r'(<meta\s+property="og:url"\s+content=")[^"]*(")', re.IGNORECASE)
_OG_LOCALE_RE = re.compile(r'(<meta\s+property="og:locale"\s+content=")[^"]*(")', re.IGNORECASE)
_TW_TITLE_RE = re.compile(r'(<meta\s+name="twitter:title"\s+content=")[^"]*(")', re.IGNORECASE)
_TW_DESC_RE = re.compile(r'(<meta\s+name="twitter:description"\s+content=")[^"]*(")', re.IGNORECASE)
_CANONICAL_RE = re.compile(r'(<link\s+rel="canonical"\s+href=")[^"]*(")', re.IGNORECASE)


def _set_html_lang(shell: str) -> str:
    """Patch the ``<html>`` element: set the lang attribute to the
    current BCP-47 tag, and add/strip ``dir="rtl"`` based on the
    language's RTL flag. Drops any existing dir before re-adding the
    right one — idempotent across re-runs."""
    shell = _HTML_LANG_RE.sub(rf'\g<1>"{st.LANG_BCP47}"', shell, count=1)
    shell = _HTML_DIR_RE.sub(r"\g<1>", shell, count=1)
    if st._is_current_rtl():
        shell = _HTML_OPEN_RE.sub(r'\g<1> dir="rtl"\g<2>', shell, count=1)
    return shell


def _date_today() -> str:
    from datetime import datetime as _dt

    return _dt.now().strftime("%Y-%m-%d")


def translate_chrome(html: str) -> str:
    """Apply all CHROME_PATCHES to localize nav / footer / search / social
    strings on a French page. Anchored regexes — no false positives in
    article body."""
    for pat, repl in st._CHROME_PATCHES_COMPILED:
        html = pat.sub(repl, html)
    html = rewrite_static_links(html)
    html = localize_en_dates(html)
    return html


# ---------------------------------------------------------------------------
# Date localisation
# ---------------------------------------------------------------------------

_DATE_FULL_RE = re.compile(
    r"\b("
    + "|".join(m for m in st._LANG_MONTHS["fr"] if len(m) > 4)
    + r")\s+(\d{1,2}),\s+(\d{4})\b"
)
_DATE_SHORT_RE = re.compile(
    r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\s+(\d{1,2}),\s+(\d{4})\b"
)
_DATE_YEAR_MONTH_RE = re.compile(
    r"\b(" + "|".join(m for m in st._LANG_MONTHS["fr"] if len(m) > 4) + r")\s+(\d{4})\b"
)


def localize_en_dates(html: str) -> str:
    """Rewrite English `Month DD, YYYY` and `Mon DD, YYYY` to the French
    equivalent. Skips inside <time datetime="…"> attribute values."""

    # Replace only inside visible text — protect <time datetime="…"> values.
    # Substitutions inside attribute values are safe because we only swap
    # the visible-month words — ISO datetime attributes use numbers
    # (YYYY-MM-DD), not month names.
    # Every lookup uses ``.get(month, month)`` so a locale with no month
    # glossary (empty map) leaves the English month word intact instead of
    # raising KeyError — a clean no-op for those languages, which is what
    # keeps un-glossaried locales from getting French month names stamped
    # on them. The active-language map is read once via the tracked
    # accessor (bind_lang has already run for this page's language).
    month_map = st.current_month_map()

    def full_repl(m: re.Match[str]) -> str:
        month = month_map.get(m.group(1), m.group(1))
        return f"{int(m.group(2))} {month} {m.group(3)}"

    def short_repl(m: re.Match[str]) -> str:
        month = month_map.get(m.group(1), m.group(1))
        return f"{int(m.group(2))} {month} {m.group(3)}"

    def ym_repl(m: re.Match[str]) -> str:
        month = month_map.get(m.group(1), m.group(1))
        return f"{month} {m.group(2)}"

    html = _DATE_FULL_RE.sub(full_repl, html)
    html = _DATE_SHORT_RE.sub(short_repl, html)
    html = _DATE_YEAR_MONTH_RE.sub(ym_repl, html)
    return html


# ---------------------------------------------------------------------------
# Static-page link rewriting
# ---------------------------------------------------------------------------

# Static pages we mirror under /fr/. Keys are the EN slugs. Built once
# from the FR registry at import — the EN slug set is identical across
# languages, so the compiled regexes are language-independent.
_STATIC_FR_PAGES = tuple(st.STATIC_SLUG_FR.keys())
_STATIC_LINK_RE = re.compile(
    r'(href=)(["\']?)(?:https?://sebastienrousseau\.com)?/('
    + "|".join(re.escape(s) for s in _STATIC_FR_PAGES)
    + r")(/(?:index\.html)?)?\2(?=[\s>])",
)
# Also catch links to ALREADY-FR slugs like /fr/privacy/ that should be /fr/confidentialite/
_LEGACY_FR_LINK_RE = re.compile(
    r'(href=)(["\']?)(?:https?://sebastienrousseau\.com)?/fr/('
    + "|".join(re.escape(s) for s in _STATIC_FR_PAGES)
    + r")(/(?:index\.html)?)?\2(?=[\s>])",
)
_TOPIC_SUBPAGE_RE = re.compile(
    r'(href=)(["\']?)(?:https?://sebastienrousseau\.com)?/(?:fr/)?topics/([a-z0-9-]+)(/(?:index\.html)?)\2(?=[\s>])',
)


def rewrite_static_links(html: str) -> str:
    """Rewrite every internal anchor on a FR page that still points at a
    top-level EN (or EN-slug FR) static page so it lands on the
    correctly-localised FR slug under /fr/. Handles both quoted and
    unquoted href attributes."""

    def repl_top_level(m: re.Match[str]) -> str:
        en_slug = m.group(3)
        fr_slug_str = st.STATIC_SLUG_FR.get(en_slug, en_slug)
        tail = m.group(4) or "/"
        if not tail.startswith("/"):  # defensive: group(4) always starts with "/"
            tail = "/" + tail  # pragma: no cover
        return f'{m.group(1)}"/{st.LANG_CODE}/{fr_slug_str}{tail}"'

    def repl_legacy_fr(m: re.Match[str]) -> str:
        en_slug = m.group(3)
        fr_slug_str = st.STATIC_SLUG_FR.get(en_slug, en_slug)
        if fr_slug_str == en_slug:
            return m.group(0)  # nothing to change
        tail = m.group(4) or "/"
        if not tail.startswith("/"):  # defensive: group(4) always starts with "/"
            tail = "/" + tail  # pragma: no cover
        return f'{m.group(1)}"/{st.LANG_CODE}/{fr_slug_str}{tail}"'

    def repl_topic_sub(m: re.Match[str]) -> str:
        topics_slug_lang = st.STATIC_SLUG_FR.get("topics", "topics")
        return f'{m.group(1)}"/{st.LANG_CODE}/{topics_slug_lang}/{m.group(3)}{m.group(4)}"'

    html = _STATIC_LINK_RE.sub(repl_top_level, html)
    html = _LEGACY_FR_LINK_RE.sub(repl_legacy_fr, html)
    html = _TOPIC_SUBPAGE_RE.sub(repl_topic_sub, html)
    return html


def localize_feed_links(html: str) -> str:
    """Point the page's feed links at the current language's feed
    shadows. Covers absolute, root-relative, and any prod/preview host
    variants Static Site Generator may have emitted into the shell."""
    html = re.sub(
        r'href="(?:https?://[^/"]+)?/atom\.xml"',
        f'href="/{st.LANG_CODE}/atom.xml"',
        html,
    )
    return re.sub(
        r'href="(?:https?://[^/"]+)?/rss\.xml"',
        f'href="/{st.LANG_CODE}/rss.xml"',
        html,
    )


# ---------------------------------------------------------------------------
# JSON-LD patch passes
# ---------------------------------------------------------------------------

_LDJSON_SCRIPT_RE = re.compile(r'<script type="application/ld\+json">([\s\S]+?)</script>')


def _patch_jsonld_scripts(
    html: str,
    patch_node: Callable[[dict], bool],
    *,
    require: str | None = None,
    warn_context: str | None = None,
) -> str:
    """Walk every ``<script type="application/ld+json">`` block, parse
    the JSON content, apply ``patch_node`` to the top-level dict and to
    every dict inside an ``@graph`` list, and re-serialise the block if
    anything changed. Avoids brittle non-greedy regex over nested ``}``
    characters.

    ``require`` short-circuits blocks that don't contain the substring.
    ``warn_context`` names the page in the stderr warning emitted when
    a block's JSON is malformed (the block is left untouched — a broken
    breadcrumb must not break the build, but it must be visible in
    build logs)."""

    def fix(m: re.Match[str]) -> str:
        raw = m.group(1)
        if require is not None and require not in raw:
            return m.group(0)
        try:
            data = _json.loads(raw)
        except _json.JSONDecodeError:
            if warn_context:
                print(
                    f"build_translations: WARNING — malformed JSON-LD on {warn_context}; "
                    "block left untouched",
                    file=sys.stderr,
                )
            return m.group(0)
        changed = False
        if isinstance(data, dict):
            if patch_node(data):
                changed = True
            graph = data.get("@graph")
            if isinstance(graph, list):
                for node in graph:
                    if isinstance(node, dict) and patch_node(node):
                        changed = True
        if not changed:
            return m.group(0)
        return (
            '<script type="application/ld+json">'
            + _json.dumps(data, separators=(",", ":"), ensure_ascii=False)
            + "</script>"
        )

    return _LDJSON_SCRIPT_RE.sub(fix, html)


def _swap_breadcrumb(html: str, slug: str, title: str) -> str:
    """Patch the BreadcrumbList JSON-LD on the page to point at /fr/{slug}/
    and localize the labels (Home → labels.json "Home", Articles → Articles)."""

    def patch_node(node: dict) -> bool:
        if node.get("@type") != "BreadcrumbList":
            return False
        items = node.get("itemListElement")
        if not isinstance(items, list):
            return False
        for item in items:
            if not isinstance(item, dict):
                continue
            pos = item.get("position")
            if pos == 1:
                item["name"] = st.I18N_FR.get("Home", "Home")
                item["item"] = f"{st.BASE}/"
            elif pos == 2:
                item["name"] = "Articles"
                item["item"] = f"{st.BASE}/{st.LANG_CODE}/"
            elif pos == 3:
                item["name"] = title
                item["item"] = f"{st.BASE}/{st.LANG_CODE}/{slug}/"
        return True

    return _patch_jsonld_scripts(
        html,
        patch_node,
        require='"BreadcrumbList"',
        warn_context=f"/{st.LANG_CODE}/{slug}/ (breadcrumb)",
    )


def _patch_blogposting_jsonld(
    html: str,
    *,
    title: str,
    description: str,
    keywords: str,
    url_fr: str,
    banner: str,
    banner_alt: str,
) -> str:
    """Walk every JSON-LD script block; for each BlogPosting node,
    rewrite headline / description / inLanguage / url / mainEntityOfPage /
    image / keywords / isPartOf so the FR page advertises itself as a
    French resource."""

    def patch_node(node: dict) -> bool:
        t = node.get("@type")
        if t != "BlogPosting":
            return False
        node["headline"] = title
        node["description"] = description
        node["inLanguage"] = st.LANG_CODE
        node["url"] = url_fr
        if keywords:
            node["keywords"] = keywords
        if banner:
            node["image"] = {
                "@type": "ImageObject",
                "url": banner,
                "width": "100vw",
                "height": "100vh",
                "caption": banner_alt or title,
            }
        mep = node.get("mainEntityOfPage")
        if isinstance(mep, dict):
            mep["@id"] = url_fr
        elif isinstance(mep, str):
            node["mainEntityOfPage"] = url_fr
        # isPartOf — point at the FR articles hub.
        ipo = node.get("isPartOf")
        if isinstance(ipo, dict):
            ipo["@id"] = "https://sebastienrousseau.com/fr/#blog"
            ipo["name"] = "Sebastien Rousseau — Articles (français)"
            ipo["url"] = "https://sebastienrousseau.com/fr/"
            ipo["inLanguage"] = st.LANG_CODE
        return True

    return _patch_jsonld_scripts(html, patch_node, require='"BlogPosting"')


def _localize_inlanguage_globally(html: str, lang: str = "fr") -> str:
    """Walk EVERY JSON-LD block on the page and set ``inLanguage`` to
    ``lang`` on every node that has the field.

    The targeted patchers (BlogPosting, AboutPage, ContactPage, …) only
    touch nodes they recognise — the secondary blocks that ship
    ``WebSite`` and ``ProfilePage`` graphs from the EN layout get left
    behind, so the FR page ends up advertising ``inLanguage="en-GB"``
    on its WebSite node even though everything else is French. This
    is what ``scripts/test_jsonld_localized.py`` was built to catch.
    """

    def walk(node: object) -> None:
        if isinstance(node, dict):
            if "inLanguage" in node and isinstance(node["inLanguage"], str):
                node["inLanguage"] = lang
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    def fix(m: re.Match[str]) -> str:
        raw = m.group(1)
        if "inLanguage" not in raw:
            return m.group(0)
        try:
            data = _json.loads(raw)
        except _json.JSONDecodeError:
            return m.group(0)
        walk(data)
        return (
            '<script type="application/ld+json">'
            + _json.dumps(data, separators=(",", ":"), ensure_ascii=False)
            + "</script>"
        )

    # Quote-tolerant match — the minifier sometimes strips the quotes
    # around the type attribute (`<script type=application/ld+json>`).
    return re.sub(
        r'<script\b[^>]*type=["\']?application/ld\+json["\']?[^>]*>([\s\S]+?)</script>',
        fix,
        html,
    )
