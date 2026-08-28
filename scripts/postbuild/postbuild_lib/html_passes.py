"""Standalone HTML finishing passes: Sigstore attestation badge, body-link
stylesheet hoisting, duplicate-H1 stripping, and data-table label wrapping.

Split from article_furniture (Phase 4.1). Imports shared constants + _is_french
from article_furniture (one-directional — article_furniture does not import this
module; the rest only calls the staying _is_french).
"""

from __future__ import annotations

import json as _json
import re
from html import escape as _esc
from html import unescape as _unesc
from pathlib import Path

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
