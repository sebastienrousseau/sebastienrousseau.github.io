#!/usr/bin/env python3
"""Repair entity-escaped HTML that some local ssg builds emit.

Two artifacts, both local-only (production/CI verified clean against the
deployed site; observed locally on ssg 0.0.46):

1. Head metas: a run of ``<meta>``/``<link>`` tags entity-escaped right
   after ``<title>``. Browsers treat text content inside <head> as the
   start of <body>, so the escaped tags render as visible prose above the
   site header on every ssg-built page. Generator-owned pages (/speaking/,
   /iso20022-mcp/) repaired their own heads via the shared
   ``_unescape_head_metas`` helper while every other page bled raw
   metadata in local previews.

2. Body enrich blocks on story-layout pages (about, papers, projects,
   homepage, the ISO 20022 MCP subpages): the frontmatter enrich/lead HTML
   fragments ship entity-escaped and render as raw markup prose mid-page.
   Every such fragment starts with an escaped ``<div lang="...">`` wrapper,
   which is the gate: pages without that escaped marker (all articles) are
   never body-touched, and <pre>/<code> zones are skipped, so quoted markup
   in article prose or code samples can never be turned into live tags.

This pass runs right after the ssg compile in build.sh, BEFORE the page
generators fork the /articles shell and before postbuild's SRI/CSP passes,
so every downstream consumer sees a sane page. Idempotent and a no-op when
nothing is escaped (i.e. on CI).
"""

from __future__ import annotations

import html as _html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"

# Terminator: fully escaped tags end in &gt; but minified pages carry a
# half-escaped variant ending in a literal > (escaped opener only).
_ESCAPED_META_RE = re.compile(r"&lt;(?:meta|link)\b.*?(?:&gt;|>)", re.DOTALL)

# Marker that gates the body pass: only the ssg-escaped enrich/lead
# fragments carry it. Articles never do.
_BODY_MARKER = "&lt;div lang="

_PRE_CODE_RE = re.compile(r"<(pre|code)\b[\s\S]*?</\1>", re.IGNORECASE)

_META_TAG_RE = re.compile(r"<meta\b[^>]*>")
_META_NAME_RE = re.compile(r'name=["\']?([A-Za-z0-9_.:-]+)')

# The escaped head run is always this fixed set. Only these names are
# deduped (keep-first, matching the single copy CI produces) so
# legitimately repeating metas — the light/dark theme-color pair,
# og:*/twitter:* property metas — are never touched.
_LEAKED_NAMES = frozenset(
    {
        "author",
        "description",
        "keywords",
        "viewport",
        "apple-mobile-web-app-capable",
        "apple-mobile-web-app-status-bar-style",
        "apple-mobile-web-app-title",
    }
)


def _repair_head(head: str) -> str:
    head = _ESCAPED_META_RE.sub(lambda m: _html.unescape(m.group(0)), head)
    # The escaped run duplicates metas the head already carries for real
    # (sometimes byte-identical, sometimes with generic site-bio copy).
    # Keep the first tag per leaked name so the local head matches the
    # single-copy shape CI produces — production keeps the page-specific
    # meta, which always precedes the revived generic one.
    seen: set[str] = set()

    def _dedupe(m: re.Match) -> str:
        tag = m.group(0)
        name_m = _META_NAME_RE.search(tag)
        if not name_m or name_m.group(1) not in _LEAKED_NAMES:
            return tag
        name = name_m.group(1)
        if name in seen:
            return ""
        seen.add(name)
        return tag

    return _META_TAG_RE.sub(_dedupe, head)


def _repair_body(body: str) -> str:
    """Unescape each contiguous escaped enrich fragment wholesale.

    The escaped blob was escaped exactly once by ssg, so a single
    ``html.unescape`` over the whole region restores the authored bytes
    byte-for-byte — including text entities like the ``&quot;`` JSON inside
    the embedded JSON-LD script some enrich blocks carry (editorial,
    glossary). Tag-by-tag unescaping is NOT enough there: it revives the
    ``<script>`` shell while leaving the escaped JSON inside, producing a
    malformed JSON-LD block.

    Region bounds: from the ``&lt;div lang=`` marker to the next literal
    ``<`` — the blob contains no real tags, so the first raw ``<`` is where
    normal markup resumes. Everything outside these regions (article prose
    quoting markup, <pre>/<code> samples) is untouched by construction.
    """
    if _BODY_MARKER not in body:
        return body
    # Never touch <pre>/<code> zones: escaped markup there is content.
    zones = [(m.start(), m.end()) for m in _PRE_CODE_RE.finditer(body)]

    def _in_zone(pos: int) -> bool:
        return any(a <= pos < b for a, b in zones)

    out: list[str] = []
    pos = 0
    while True:
        start = body.find(_BODY_MARKER, pos)
        if start < 0:
            out.append(body[pos:])
            break
        if _in_zone(start):
            out.append(body[pos : start + len(_BODY_MARKER)])
            pos = start + len(_BODY_MARKER)
            continue
        end = body.find("<", start)
        if end < 0:
            end = len(body)
        out.append(body[pos:start])
        out.append(_html.unescape(body[start:end]))
        pos = end
    return "".join(out)


def repair(html_text: str) -> str:
    end = html_text.find("</head>")
    if end < 0:
        return html_text
    return _repair_head(html_text[:end]) + _repair_body(html_text[end:])


def main() -> int:
    if not PUBLIC.is_dir():
        print("fix_escaped_ssg_html: public/ missing; nothing to do.")
        return 0
    touched = 0
    for page in PUBLIC.rglob("*.html"):
        text = page.read_text(encoding="utf-8", errors="ignore")
        fixed = repair(text)
        if fixed != text:
            page.write_text(fixed, encoding="utf-8")
            touched += 1
    print(f"fix_escaped_ssg_html: repaired {touched} page(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
