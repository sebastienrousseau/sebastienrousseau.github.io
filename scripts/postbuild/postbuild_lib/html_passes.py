# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Standalone HTML finishing passes: Sigstore attestation badge, body-link
stylesheet hoisting, duplicate-H1 stripping, and data-table label wrapping.

Split from article_furniture (Phase 4.1). Imports shared constants + _is_french
from article_furniture (one-directional — article_furniture does not import this
module; the rest only calls the staying _is_french).
"""

from __future__ import annotations

import functools as _functools
import json as _json
import re
from html import escape as _esc
from html import unescape as _unesc
from pathlib import Path

import _lang_registry
from postbuild_lib.article_furniture import (
    _BODY_H1_RE,
    _H1_RE,
    _TABLE_OPEN_RE,
    _TAG_STRIP_RE,
    _TH_TEXT_RE,
    _TR_RE,
    PUBLIC,
    _is_french,
)

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


_TABLE_BLOCK_RE = re.compile(r"<table\b[^>]*>[\s\S]*?</table>", re.IGNORECASE)
_THEAD_RE = re.compile(r"<thead\b[\s\S]*?</thead>", re.IGNORECASE)
_TD_OPEN_RE = re.compile(r"<td\b", re.IGNORECASE)


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


def strip_duplicate_body_h1(html: str) -> str:
    """Remove the first H1 inside <main>: the hero H1 the layout emits in
    ``<section class="ap-hero">`` is the page's only H1.

    Every dated article runs the markdown body through Static Site
    Generator with an H1 at the top. The layout *also* emits
    ``<h1>{{title}}</h1>`` in the hero band. The rendered output
    therefore carries two H1s — WCAG 1.3.1 / 2.4.6 violation, plus a
    noisy duplicate headline directly above the article body.

    This used to strip the body H1 only when its text matched the hero
    exactly, to avoid deleting content that might differ on purpose.
    That left the drifted majority in place: ``title:`` is the short
    SEO form and the body H1 the long headline, so on 267 posts the two
    differ by wording alone and both survived. The duplicate is one of
    *role*, not of text — a second H1 is wrong whatever it says — so the
    match is now on position rather than on content.

    The fix stays render-only: the markdown keeps its full headline for
    editors (``check_voice`` still requires exactly one H1 in source),
    and only the served page drops the redundant second one.
    """
    if _H1_RE.search(html) is None:
        return html
    new_html, n = _BODY_H1_RE.subn(lambda m: m.group(1), html, count=1)
    return new_html if n else html


_LDJSON_RE = re.compile(
    r'(<script[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)',
    re.DOTALL | re.IGNORECASE,
)


def _decode_json_strings(node: object) -> object:
    """Recursively HTML-unescape every string *value* in a parsed JSON tree."""
    if isinstance(node, str):
        return _unesc(node)
    if isinstance(node, list):
        return [_decode_json_strings(v) for v in node]
    if isinstance(node, dict):
        return {k: _decode_json_strings(v) for k, v in node.items()}
    return node


def decode_entities_in_jsonld(html: str) -> str:
    """Strip HTML entities from JSON-LD payloads.

    A ``<script type="application/ld+json">`` body is *not* HTML-parsed, so an
    entity that arrives inside it is read literally: consumers see the six
    characters ``&amp;`` in a page name rather than ``&``. The layouts embed
    ``"name":"{{title}}"`` directly inside the JSON block, and the template
    layer fills variables with the HTML-escaped form — correct for the rest of
    the page, wrong here. Measured on this corpus: 1,528 of 26,001 blocks.

    The decode runs on parsed **string values only**, never on the raw text.
    Unescaping the block wholesale would turn a ``&quot;`` inside a value into
    a bare quote and break the JSON it was trying to fix — the naive version
    of this pass is worse than the bug.

    A block that does not parse is left exactly as found: this pass never
    rewrites what it cannot understand.
    """

    def _one(m: re.Match[str]) -> str:
        open_tag, body, close_tag = m.group(1), m.group(2), m.group(3)
        if "&" not in body:
            return m.group(0)
        try:
            parsed = _json.loads(body)
        except (ValueError, RecursionError):
            return m.group(0)
        decoded = _decode_json_strings(parsed)
        if decoded == parsed:
            return m.group(0)
        return (
            open_tag + _json.dumps(decoded, ensure_ascii=False, separators=(",", ":")) + close_tag
        )

    return _LDJSON_RE.sub(_one, html)


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


# ---------------------------------------------------------------------------
# Localised listing titles — 2154 of the 7004 non-EN pages served a <title>
# byte-identical to an English page's, from four templates repeated across all
# 34 locales: the article listing, its year archives, the six editorial-pillar
# pages and the tag landings. Each of those pages is self-canonical and
# declares its own language, so the strongest on-page signal a search engine
# has was in the wrong one, and up to 35 pages shared a single string.
#
# The frames live in labels.json and the pillar names already existed in
# listings.json; only the wiring was missing. Done here rather than in the
# four generators that emit these pages because each forks its locale
# variants separately, and a render pass covers all of them uniformly.
# ---------------------------------------------------------------------------

_EN_PILLARS = {
    "Applied AI": "ai",
    "Payments &amp; money": "payments",
    "Payments & money": "payments",
    "Infrastructure &amp; cryptography": "infra",
    "Infrastructure & cryptography": "infra",
    "Policy &amp; resilience": "policy",
    "Policy & resilience": "policy",
    "Open source": "open-source",
    "Banking leadership": "leadership",
}
_YEAR_TITLE_RE = re.compile(r"^Articles &mdash; (\d{4})$|^Articles — (\d{4})$")
_LISTINGS_CACHE: dict[str, dict] = {}


def _pillars_for(locale: str) -> dict[str, str]:
    if locale not in _LISTINGS_CACHE:
        path = Path("_data") / "i18n" / locale / "listings.json"
        try:
            _LISTINGS_CACHE[locale] = _json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            _LISTINGS_CACHE[locale] = {}
    return _LISTINGS_CACHE[locale].get("pillars", {})


def localised_listing_title(title: str, locale: str, labels: dict[str, str]) -> str:
    """Translate one of the four listing title templates, or return it as-is."""
    articles = labels.get("Articles")
    if not articles:
        return title
    if title == "Articles":
        return articles
    year = _YEAR_TITLE_RE.match(title)
    if year:
        return f"{articles} — {year.group(1) or year.group(2)}"
    for suffix, key in (
        (" — Editorial pillar", "Editorial pillar"),
        (" — Articles by topic", "Articles by topic"),
    ):
        if not title.endswith(suffix):
            continue
        frame = labels.get(key)
        if not frame:
            return title
        head = title[: -len(suffix)]
        if key == "Editorial pillar":
            # The pillar name is translated; a tag name is a canonical
            # taxonomy label and stays as it is.
            head = _pillars_for(locale).get(_EN_PILLARS.get(head, ""), head)
        return f"{head} — {frame}"
    return title


_LOCALE_LABELS_CACHE: dict[str, dict[str, str]] = {}
_PAGE_TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S)
_OG_TITLE_ATTR_RE = re.compile(r'(<meta[^>]+property="og:title"[^>]+content=")([^"]*)(")')
_TW_TITLE_ATTR_RE = re.compile(r'(<meta[^>]+name="twitter:title"[^>]+content=")([^"]*)(")')


def _labels_for(locale: str) -> dict[str, str]:
    if locale not in _LOCALE_LABELS_CACHE:
        path = Path("_data") / "i18n" / locale / "labels.json"
        try:
            _LOCALE_LABELS_CACHE[locale] = _json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            _LOCALE_LABELS_CACHE[locale] = {}
    return _LOCALE_LABELS_CACHE[locale]


@_functools.cache
def _active_locales() -> frozenset[str]:
    return frozenset(lang.code for lang in _lang_registry.LANGUAGES if lang.code != "en")


def localise_listing_titles(page: Path, html: str) -> str:
    """Put a locale listing page's title into its own language.

    Rewrites <title>, og:title, twitter:title and the hero H1 together, so the
    page cannot end up saying one thing to a reader and another to a crawler.
    """
    locales = _active_locales()
    locale = next((p for p in page.parts[:2] if p in locales), None)
    if locale is None:
        return html
    match = _PAGE_TITLE_RE.search(html)
    if match is None:
        return html
    old = match.group(1).strip()
    new = localised_listing_title(old, locale, _labels_for(locale))
    if new == old:
        return html
    out = _PAGE_TITLE_RE.sub(lambda _m: f"<title>{new}</title>", html, count=1)
    out = _OG_TITLE_ATTR_RE.sub(
        lambda m: m.group(1) + new + m.group(3) if m.group(2).strip() == old else m.group(0), out
    )
    out = _TW_TITLE_ATTR_RE.sub(
        lambda m: m.group(1) + new + m.group(3) if m.group(2).strip() == old else m.group(0), out
    )
    out = re.sub(
        r"(<h1[^>]*>)" + re.escape(old) + r"(</h1>)",
        lambda m: m.group(1) + new + m.group(2),
        out,
        count=1,
    )
    # A pillar page's H1 is the bare pillar name, not the full title, so the
    # rewrite above does not reach it: the title read Arabic while the visible
    # heading still read "Infrastructure &amp; cryptography".
    head = old.removesuffix(" — Editorial pillar")
    if head != old:
        translated = _pillars_for(locale).get(_EN_PILLARS.get(head, ""), head)
        if translated != head:
            out = re.sub(
                r"(<h1[^>]*>)" + re.escape(head) + r"(</h1>)",
                lambda m: m.group(1) + translated + m.group(2),
                out,
                count=1,
            )
    return out
