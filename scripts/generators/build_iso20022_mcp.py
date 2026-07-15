#!/usr/bin/env python3
# =============================================================================
# Build the premium /iso20022-mcp/ hub page.
#
# Mirrors build_speaking.py: clone the built ``public/articles/index.html``
# shell (typography, CSP, SRI, a11y chrome, primary nav) and swap in a body of
# ``spk-``-prefixed editorial sections. Business-benefit led, in the spirit of
# business.apple.com: what you can do, a friendly "What is MCP?" explainer, the
# suite, and a concrete "Get started in three steps".
#
# All copy lives in this file's CONTENT dict; the spk- CSS is already
# AAA-contrast-compliant. English-only for now; locale forks can be added later
# exactly as build_speaking does.
#
# Input:  public/articles/index.html   (shell template, built by ssg first)
# Output: public/iso20022-mcp/index.html
# =============================================================================
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "generators"))

from build_case_studies import _swap_into_shell, _unescape_head_metas
from build_speaking import _esc, _rich

PUBLIC = ROOT / "public"
SHELL_SRC = PUBLIC / "articles" / "index.html"
OUT = PUBLIC / "iso20022-mcp" / "index.html"
URL = "https://sebastienrousseau.com/iso20022-mcp"
GH = "https://github.com/sebastienrousseau/iso20022-mcp"
KEYWORDS = (
    "ISO 20022 MCP, Model Context Protocol, AI agent payments, pain.001, "
    "pacs.008, camt.053, reconciliation, AP2, x402, agentic payments, fintech"
)


CDN = "https://cloudcdn.pro/stocks/images"


def _mono(s: str) -> str:
    """Wrap a literal command/code snippet in the site's mono style.
    ``<code>`` (not a bare span) so assistive tech announces it as code."""
    return f'<code class="spk-mono">{_esc(s)}</code>'


# Intrinsic width/height per image class. Must stay consistent with the CSS
# aspect-ratio the classes carry in _layouts/articles.html (.mcp-hero-img is
# 16/8, .mcp-band-img is 16/6) so the browser reserves the right box before
# the bytes arrive and CLS stays at zero.
_IMG_DIMS: dict[str, tuple[int, int]] = {
    "mcp-hero-img": (1920, 960),
    "mcp-band-img": (1920, 720),
}


def _img(name: str, alt: str, cls: str, sizes: str, eager: bool = False) -> str:
    """A responsive CDN image (webp srcset). Styled by CLASS, never inline --
    the site's CSP forbids inline styles, which would be stripped on deploy.
    """
    prio = 'fetchpriority="high"' if eager else 'loading="lazy"'
    width, height = _IMG_DIMS[cls]
    return (
        f'<img src="{CDN}/{name}-1920.webp" '
        f'srcset="{CDN}/{name}-640.webp 640w, {CDN}/{name}-1200.webp 1200w, '
        f'{CDN}/{name}-1920.webp 1920w" sizes="{sizes}" '
        f'alt="{_esc(alt)}" class="{cls}" width="{width}" height="{height}" '
        f'{prio} decoding="async">'
    )


def _imgband(name: str, alt: str) -> str:
    """A full-bleed-within-wrap image band that breaks up the text sections."""
    return (
        '<section><div class="spk-wrap">'
        + _img(name, alt, "mcp-band-img", "(max-width:1120px) 100vw, 1120px")
        + "</div></section>"
    )


# Apple-style line icons (24x24, currentColor stroke) keyed per card slot.
_ICON_SVG = {
    "send": '<path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4 20-7z"/>',
    "check": '<path d="M22 11.1V12a10 10 0 1 1-5.9-9.1"/><path d="m9 11 3 3L22 4"/>',
    "swap": (
        '<path d="M17 1l4 4-4 4"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/>'
        '<path d="M7 23l-4-4 4-4"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/>'
    ),
    "link": (
        '<path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/>'
        '<path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/>'
    ),
    "alert": (
        '<path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h16.9a2 2 0 0 0 1.7-3L13.7 3.9a2 2 '
        '0 0 0-3.4 0z"/><path d="M12 9v4"/><path d="M12 17h.01"/>'
    ),
    "globe": (
        '<circle cx="12" cy="12" r="10"/><path d="M2 12h20"/>'
        '<path d="M12 2a15 15 0 0 1 4 10 15 15 0 0 1-4 10 15 15 0 0 1-4-10 15 15 0 0 1 4-10z"/>'
    ),
    "grid": (
        '<rect x="3" y="3" width="7" height="7" rx="1"/>'
        '<rect x="14" y="3" width="7" height="7" rx="1"/>'
        '<rect x="14" y="14" width="7" height="7" rx="1"/>'
        '<rect x="3" y="14" width="7" height="7" rx="1"/>'
    ),
    "layers": (
        '<path d="M12 2 2 7l10 5 10-5-10-5z"/><path d="m2 17 10 5 10-5"/>'
        '<path d="m2 12 10 5 10-5"/>'
    ),
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    "lock": (
        '<rect x="3" y="11" width="18" height="11" rx="2"/>'
        '<path d="M7 11V7a5 5 0 0 1 10 0v4"/>'
    ),
    "eye": '<path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/>',
}
_ICONS = {
    "mcp-benefits": ["send", "check", "swap", "link"],
    "mcp-what": ["alert", "globe", "grid"],
    "mcp-arc": ["layers", "grid", "link"],
    "mcp-safety": ["check", "shield", "lock"],
}


def _icon(section_id: str, i: int) -> str:
    keys = _ICONS.get(section_id, [])
    if i >= len(keys):
        return ""
    svg = _ICON_SVG[keys[i]]
    # Presentation attributes on the <svg> itself (not only CSS) so the icons
    # stay small line-drawings even if the stylesheet is cached/stale.
    return (
        '<span class="mcp-icon" aria-hidden="true"><svg viewBox="0 0 24 24" '
        'width="34" height="34" fill="none" stroke="currentColor" '
        f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{svg}'
        "</svg></span>"
    )


# --- Content (single source of copy) ----------------------------------------
C: dict = {
    "meta_title": "ISO 20022 MCP Suite: let AI agents make bank payments",
    "meta_description": (
        "The open ISO 20022 layer for AI agents. Nine vendor-neutral MCP "
        "servers to generate, validate, reconcile and settle bank payments "
        "from natural language. Apache-2.0, on PyPI and the MCP registry."
    ),
    "hero": {
        "eyebrow": "OPEN SOURCE · APACHE-2.0 · ON PYPI + THE MCP REGISTRY",
        "headline": "Let your AI agent make real bank payments.",
        "lede": (
            "Nine open MCP servers that turn plain language into validated ISO "
            "20022 bank messages: initiate, settle, reconcile and resolve. "
            "Vendor-neutral, runs anywhere, installed in one line."
        ),
    },
    # What you can do — benefit-led, business.apple.com "Run / Grow" style.
    "benefits": {
        "eyebrow": "WHAT YOU CAN DO",
        "headline": "Payment operations, from a sentence.",
        "lede": (
            "Give an agent the jobs a treasury team does by hand. Every result "
            "is schema-valid before it is returned."
        ),
        "cards": [
            {
                "eyebrow": "INITIATE",
                "title": "Pay from plain language.",
                "body": (
                    "“Pay this supplier €4,200” becomes a "
                    "validated pain.001 or pacs.008, IBAN- and XSD-checked, "
                    "ready for the rail."
                ),
            },
            {
                "eyebrow": "RECONCILE",
                "title": "Match a statement in seconds.",
                "body": (
                    "Reconcile a camt.053 statement against what you expected, "
                    "with an explainable reason for every match, partial and "
                    "split payment."
                ),
            },
            {
                "eyebrow": "MIGRATE",
                "title": "Get off SWIFT MT in time.",
                "body": (
                    "Convert MT103/MT101/MT94x to ISO 20022 and fix structured "
                    "addresses before the 2026–2028 deadlines, one message "
                    "at a time."
                ),
            },
            {
                "eyebrow": "BRIDGE",
                "title": "Turn a mandate into a wire.",
                "body": (
                    "Take a signed AP2 or x402 agent mandate and produce a "
                    "wire-valid pain.001, with spending-cap and expiry "
                    "guardrails."
                ),
            },
        ],
    },
    "what": {
        "eyebrow": "NEW TO MCP?",
        "headline": "What is the Model Context Protocol?",
        "lede": (
            "MCP is an open standard that lets AI assistants use real tools "
            "safely, a universal port between an assistant and your systems."
        ),
        "cards": [
            {
                "eyebrow": "THE PROBLEM",
                "title": "Agents talk, but can't act.",
                "body": (
                    "A model can describe a payment, but not produce the exact "
                    "bank message that moves it. Every integration was bespoke "
                    "glue code."
                ),
            },
            {
                "eyebrow": "THE STANDARD",
                "title": "One protocol, any tool.",
                "body": (
                    "MCP gives assistants a common way to discover and call "
                    "tools, from Claude, Cursor or your own agent. Build a "
                    "capability once; every client can use it."
                ),
            },
            {
                "eyebrow": "THIS SUITE",
                "title": "Payments as MCP tools.",
                "body": (
                    "These servers expose ISO 20022 as MCP tools. Ask in plain "
                    "terms, get back XSD-validated messages. No translator "
                    "between your systems and the rails."
                ),
            },
        ],
    },
    "arc": {
        "eyebrow": "THE SUITE",
        "headline": "Nine servers, one payment lifecycle.",
        "lede": (
            "Install the gateway and let it route, or install just the server "
            "for the job. Each is one pip install, on the MCP registry."
        ),
        "cards": [
            {
                "eyebrow": "DISCOVER + GENERATE",
                "title": "The gateway.",
                "body": (
                    "One surface across pain, pacs, camt and acmt: search, "
                    "generate XSD-valid XML, validate and parse, through seven "
                    "meta-tools."
                ),
                "bullets": ["iso20022-mcp", "pain001-mcp", "pacs008-mcp"],
                "cta_label": "Read the docs",
                "cta_href": "/iso20022-mcp-docs/index.html",
            },
            {
                "eyebrow": "RECONCILE + RESOLVE",
                "title": "Close the loop.",
                "body": (
                    "Match statements to expected payments, explainably. When "
                    "one goes wrong, cancel and resolve it with camt.056 and "
                    "camt.029."
                ),
                "bullets": ["reconcile-mcp", "camt053-mcp", "camt-exceptions"],
                "cta_label": "See the recipes",
                "cta_href": "/iso20022-mcp-recipes/index.html",
            },
            {
                "eyebrow": "BRIDGE + ACCOUNTS",
                "title": "The frontier.",
                "body": (
                    "Bridge AP2 / x402 agent mandates to a wire-valid message, "
                    "guardrailed, and open or verify accounts with acmt.001."
                ),
                "bullets": ["ap2-iso20022", "acmt001-mcp", "bankstatementparser-mcp"],
                "cta_label": "Tool reference",
                "cta_href": "/iso20022-mcp-reference/index.html",
            },
        ],
    },
    "safety": {
        "eyebrow": "SAFE BY DESIGN",
        "headline": "Built to hand to an agent.",
        "cards": [
            {
                "eyebrow": "VALIDATED",
                "title": "Checked before it returns.",
                "body": (
                    "Every generator validates output against the official "
                    "bundled XSD before handing it back. Malformed messages "
                    "never leave the tool."
                ),
            },
            {
                "eyebrow": "GUARDED",
                "title": "Never moves money.",
                "body": (
                    "The bridge only transforms and validates. Producing a "
                    "message stays separate from sending it, so payment is a "
                    "human-guarded step."
                ),
            },
            {
                "eyebrow": "OPEN",
                "title": "Owned by no bank.",
                "body": (
                    "Apache-2.0, 100% branch-tested, on your own "
                    "infrastructure, tied to no balance sheet."
                ),
            },
        ],
    },
}


# --- Section renderers (spk- components, matching /speaking) -----------------
def _head(eyebrow: str, headline: str, lede: str = "") -> str:
    lede_html = f'<p class="spk-lede">{_rich(lede)}</p>' if lede else ""
    # Left-aligned heads (no spk-center) to match the Apple Partner Network look.
    return (
        '<div class="spk-head">'
        f'<span class="spk-eyebrow">{_esc(eyebrow)}</span>'
        f"<h2>{_esc(headline)}</h2>{lede_html}</div>"
    )


def _hero(d: dict) -> str:
    h = d["hero"]
    return (
        '<header class="spk-hero" id="spk-top"><div class="spk-hero-grid"><div>'
        f'<span class="spk-eyebrow">{_esc(h["eyebrow"])}</span>'
        f'<h1>{_esc(h["headline"])}</h1>'
        f'<p class="spk-lede">{_rich(h["lede"])}</p>'
        '<div class="spk-cta-row">'
        '<a href="#mcp-start" class="spk-btn spk-btn-primary">Get started '
        '<span class="spk-arw" aria-hidden="true">&#8594;</span></a>'
        '<a href="#mcp-benefits" class="spk-btn spk-btn-ghost">See what it '
        "does</a></div>"
        '<p class="spk-microproof"><strong>9</strong> servers, live on PyPI '
        "&middot; <strong>100%</strong> branch-tested &middot; "
        "<strong>vendor-neutral</strong>, Apache-2.0</p>"
        "</div></div></header>"
    )


def _hero_image() -> str:
    """The big rounded hero photo below the headline, Partner-Network style."""
    return (
        '<section class="mcp-hero-media"><div class="spk-wrap">'
        + _img(
            "modern-corporate-office-with-technological-displays",
            "A modern financial operations floor with technology displays.",
            "mcp-hero-img",
            "(max-width:1120px) 100vw, 1120px",
            eager=True,
        )
        + "</div></section>"
    )


def _cards(
    section: dict, section_id: str, band: bool = False, bullets: bool = False
) -> str:
    items = []
    for i, it in enumerate(section["cards"]):
        primary = "spk-btn-primary" if i == 0 else "spk-btn-ghost"
        extra = ""
        if bullets:
            lis = "".join(f"<li>{_esc(b)}</li>" for b in it.get("bullets", []))
            # aria-label carries the card name so repeated CTA phrasings stay
            # distinguishable when a screen reader lists the page's links.
            cta = (
                f'<a href="{_esc(it["cta_href"])}" class="spk-btn {primary}" '
                f'aria-label="{_esc(it["cta_label"])}: {_esc(it["title"].rstrip("."))}">'
                f'{_esc(it["cta_label"])}</a>'
            )
            extra = f"<ul>{lis}</ul>{cta}"
        items.append(
            '<div class="spk-path">'
            + _icon(section_id, i)
            + f'<span class="spk-eyebrow">{_esc(it["eyebrow"])}</span>'
            f'<h3>{_esc(it["title"])}</h3><p>{_rich(it["body"])}</p>{extra}</div>'
        )
    cls = "spk-band" if band else ""
    return (
        f'<section class="{cls}" id="{section_id}"><div class="spk-wrap">'
        + _head(section["eyebrow"], section["headline"], section.get("lede", ""))
        + f'<div class="spk-paths">{"".join(items)}</div></div></section>'
    )


def _start() -> str:
    steps = [
        (
            "STEP 1",
            "Run it, no install.",
            "Start the gateway with one command, no account, no key: "
            + _mono('uvx --from "iso20022-mcp[pain,pacs,acmt]" iso20022-mcp'),
        ),
        (
            "STEP 2",
            "Ask in plain terms.",
            "Try " + _mono('search "cancel a payment"') + " and it points you "
            "at the right message, then "
            + _mono("generate")
            + " returns XSD-valid XML.",
        ),
        (
            "STEP 3",
            "Connect your agent.",
            "Add " + _mono("iso20022-mcp") + " as a command in your MCP client "
            "(Claude Desktop, Cursor) and your assistant can pay, reconcile "
            "and migrate.",
        ),
    ]
    cards = "".join(
        '<div class="spk-path">'
        f'<span class="spk-eyebrow">{_esc(eyebrow)}</span>'
        f"<h3>{_esc(title)}</h3><p>{body}</p></div>"
        for eyebrow, title, body in steps
    )
    return (
        '<section class="spk-band" id="mcp-start"><div class="spk-wrap">'
        + _head("GET STARTED", "Live in under a minute.")
        + f'<div class="spk-paths">{cards}</div>'
        '<div class="spk-cta-row mcp-start-cta">'
        f'<a href="{GH}" class="spk-btn spk-btn-primary">Get started on GitHub '
        '<span class="spk-arw" aria-hidden="true">&#8594;</span></a>'
        '<a href="/iso20022-mcp-docs/index.html" class="spk-btn spk-btn-ghost">'
        "Read the quickstart</a>"
        '<a href="/iso20022-mcp-reference/index.html" class="spk-btn spk-btn-ghost">'
        "Tool reference</a></div></div></section>"
    )


def _render_body(d: dict) -> str:
    sections = [
        _hero(d),
        _hero_image(),
        _cards(d["benefits"], "mcp-benefits", bullets=False),
        _imgband(
            "circuit_board_cityscape",
            "A circuit board rendered as a city, evoking payment rails.",
        ),
        _cards(d["what"], "mcp-what", bullets=False),
        _cards(d["arc"], "mcp-arc", bullets=True),
        _imgband(
            "digital-nodes",
            "A network of connected nodes, evoking agents calling MCP tools.",
        ),
        _start(),
        _cards(d["safety"], "mcp-safety", bullets=False),
    ]
    return (
        '<div class="speaking-page iso20022-mcp-page">' + "".join(sections) + "</div>"
    )


def _nav(shell: str) -> str:
    """Rebuild the primary nav as the site-wide 9-item structure, with Suite
    (this page) active. Idempotent, and robust to a stale shell that still
    carries a different nav.
    """
    items = (
        '<li><a href="/about/index.html">About</a></li>'
        '<li><a href="/articles/index.html">Articles</a></li>'
        '<li><a href="/papers/index.html">Papers</a></li>'
        '<li><a href="/case-studies/index.html">Case studies</a></li>'
        '<li><a href="/topics/index.html">Topics</a></li>'
        '<li><a href="/projects/index.html">Projects</a></li>'
        '<li><a href="/playlists/index.html">Playlists</a></li>'
        '<li><a href="/speaking/index.html">Speaking</a></li>'
        '<li><a href="/iso20022-mcp/index.html" aria-current="page" '
        'class="active">Suite</a></li>'
    )
    out, n = re.subn(
        r'(<ul class="ap-menu">).*?(</ul>)',
        lambda m: m.group(1) + items + m.group(2),
        shell,
        count=1,
        flags=re.DOTALL,
    )
    if n == 0:
        raise SystemExit(
            'build_iso20022_mcp: primary nav (<ul class="ap-menu">) not found in shell'
        )
    return out


# In-page language-switcher items, e.g.
#   <a class="ap-lang-item" href="/fr/articles/" data-lang="fr" role="menuitem">
_SWITCHER_ITEM_RE = re.compile(
    r'(<a\s+class="ap-lang-item"\s+)href="[^"]*"(\s+data-lang="([^"]+)")'
)


def _lang_switcher_home(html: str) -> str:
    """Point every language-switcher item at its locale homepage.

    This page is EN-only: its hreflang alternates are stripped by _fix_metas,
    and scripts/postbuild/fix_lang_switcher.py rewires switcher items from a
    page's *own* hreflang links, returning early when there are none. Left
    alone, the switcher would keep the articles shell's misleading
    ``/<lang>/articles-segment/`` links — so degrade it here to the locale
    homepages (``/`` for EN).
    """

    def repl(m: re.Match) -> str:
        lang = m.group(3)
        home = "/" if lang == "en" else f"/{lang}/"
        return f'{m.group(1)}href="{home}"{m.group(2)}'

    out, n = _SWITCHER_ITEM_RE.subn(repl, html)
    if n == 0:
        raise SystemExit(
            "build_iso20022_mcp: no .ap-lang-item switcher links found in shell"
        )
    return out


HERO_OG_IMAGE = f"{CDN}/modern-corporate-office-with-technological-displays-1920.webp"
# Intrinsic size of the hero webp above (checked against the served asset),
# stamped into og:image:width/height so link-preview crops are computed right.
HERO_OG_SIZE = (1920, 1076)


def _sub_required(html: str, pattern: str, rep: str, what: str, count: int = 1) -> str:
    """Targeted single-tag swap that fails the build if the anchor tag is
    missing from the shell — a silent no-op ships the articles metadata."""
    out, n = re.subn(pattern, lambda m: rep, html, count=count)
    if n == 0:
        raise SystemExit(f"build_iso20022_mcp: _fix_metas anchor missing: {what}")
    return out


def _upsert_head_tag(html: str, pattern: str, tag: str, what: str) -> str:
    """Replace ``pattern`` with ``tag`` if present, else insert ``tag`` just
    before ``</head>``. Never a silent no-op: the tag ends up on the page
    either way."""
    out, n = re.subn(pattern, lambda m: tag, html, count=1)
    if n == 1:
        return out
    idx = html.find("</head>")
    if idx < 0:
        raise SystemExit(f"build_iso20022_mcp: no </head> to insert {what}")
    return html[:idx] + tag + "\n" + html[idx:]


def _keep_first_tag(html: str, pattern: str) -> str:
    """Keep only the first tag matching ``pattern``, dropping later repeats
    even when their content differs. Used for viewport: the local shell can
    carry a second, entity-escaped viewport meta that _unescape_head_metas
    revives — a page must ship exactly one."""
    seen = False

    def repl(m: re.Match) -> str:
        nonlocal seen
        if seen:
            return ""
        seen = True
        return m.group(0)

    return re.sub(pattern, repl, html)


def _dedupe_exact_tags(html: str, pattern: str) -> str:
    """Drop byte-identical repeats of a head tag, keeping the first. The two
    theme-color tags with different ``media`` attrs are distinct and kept."""
    seen: set[str] = set()

    def repl(m: re.Match) -> str:
        if m.group(0) in seen:
            return ""
        seen.add(m.group(0))
        return m.group(0)

    return re.sub(pattern, repl, html)


def _jsonld_script(payload: dict) -> str:
    """Serialise JSON-LD for embedding in a <script> element. ``</`` must be
    escaped as ``<\\/`` so no value can close the script element early."""
    return (
        '<script type="application/ld+json">\n'
        + json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace(
            "</", "<\\/"
        )
        + "\n    </script>"
    )


def _hub_jsonld() -> str:
    """WebPage + BreadcrumbList for the hub — replaces the articles shell's
    CollectionPage block."""
    payload = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "name": C["meta_title"],
                "description": C["meta_description"],
                "url": URL,
                "inLanguage": "en-GB",
                "isPartOf": {"@id": "https://sebastienrousseau.com/#website"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": "https://sebastienrousseau.com/",
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "ISO 20022 MCP Suite",
                        "item": URL,
                    },
                ],
            },
        ],
    }
    return _jsonld_script(payload)


# The articles shell's page-level JSON-LD: a @graph of CollectionPage +
# BreadcrumbList describing /articles/. Wrong for this page — swapped out
# wholesale for the hub's WebPage graph.
_COLLECTION_LD_RE = re.compile(
    r'<script type="application/ld\+json">\s*\{"@context":"https://schema\.org",'
    r'"@graph":\[\{"@type":"CollectionPage"[\s\S]*?</script>'
)


def _fix_metas(html: str) -> str:
    """Swap the article-shell metas _swap_into_shell misses, by exact tag only.

    Targeted regex per meta tag -- never a global string replace, which would
    also corrupt nav links / breadcrumbs / aria-labels that share the text.
    Every swap either verifies its anchor matched or upserts the tag; a shell
    drift can no longer silently ship /articles metadata on this page.
    """
    title, desc = _esc(C["meta_title"]), _esc(C["meta_description"])

    # Exactly one meta description: replace every copy the shell carries with
    # the hub one, then drop all but the first of the now-identical tags.
    desc_tag = f'<meta name="description" content="{desc}">'
    html = _sub_required(
        html, r'<meta name="description"[^>]*>', desc_tag, "meta description", count=0
    )
    first_end = html.find(desc_tag) + len(desc_tag)
    html = html[:first_end] + html[first_end:].replace(desc_tag, "")

    # Social cards: the hub hero photo, not the shell's X share icon.
    og_w, og_h = HERO_OG_SIZE
    for pattern, rep, what in (
        (
            r'<meta property="og:image" content="[^"]*"',
            f'<meta property="og:image" content="{HERO_OG_IMAGE}"',
            "og:image",
        ),
        (
            r'<meta property="og:image:width" content="[^"]*"',
            f'<meta property="og:image:width" content="{og_w}"',
            "og:image:width",
        ),
        (
            r'<meta property="og:image:height" content="[^"]*"',
            f'<meta property="og:image:height" content="{og_h}"',
            "og:image:height",
        ),
        (
            r'<meta name="twitter:image"[^>]*>',
            f'<meta name="twitter:image" content="{HERO_OG_IMAGE}">',
            "twitter:image",
        ),
        (
            r'<meta name="twitter:title"[^>]*>',
            f'<meta name="twitter:title" content="{title}">',
            "twitter:title",
        ),
        (
            r'<meta name="twitter:description"[^>]*>',
            f'<meta name="twitter:description" content="{desc}">',
            "twitter:description",
        ),
    ):
        html = _sub_required(html, pattern, rep, what)

    # twitter:card only if the shell carries that key (it does today); a full
    # photo warrants the large-image card.
    html = re.sub(
        r'<meta name="twitter:card"[^>]*>',
        lambda m: '<meta name="twitter:card" content="summary_large_image">',
        html,
        count=1,
    )

    # These aren't in every shell build — upsert so the page always has them.
    for pattern, tag, what in (
        (
            r'<meta name="keywords"[^>]*>',
            f'<meta name="keywords" content="{_esc(KEYWORDS)}">',
            "meta keywords",
        ),
        (
            r'<meta name="apple-mobile-web-app-title"[^>]*>',
            '<meta name="apple-mobile-web-app-title" content="ISO 20022 MCP">',
            "apple-mobile-web-app-title",
        ),
        (
            r'<meta name="application-name"[^>]*>',
            '<meta name="application-name" content="ISO 20022 MCP">',
            "application-name",
        ),
    ):
        html = _upsert_head_tag(html, pattern, tag, what)

    # EN-only page: the copied /articles hreflang alternates are wrong here
    # and a page with no alternates is valid (test_hreflang_reciprocity).
    # Removal is conditional: the raw ssg shell carries no hreflang links at
    # all (postbuild injects them), so in a fresh build there is nothing to
    # strip and that is normal, not an error.
    html, _ = re.subn(
        r'[ \t]*<link\s+rel="alternate"\s+hreflang="[^"]*"\s+href="[^"]*"\s*/?>\n?',
        "",
        html,
    )

    # Page JSON-LD: the articles CollectionPage graph → hub WebPage graph.
    html, n = _COLLECTION_LD_RE.subn(lambda m: _hub_jsonld(), html, count=1)
    if n == 0:
        raise SystemExit(
            "build_iso20022_mcp: _fix_metas anchor missing: CollectionPage JSON-LD"
        )

    # Never ship duplicate viewport / theme-color tags. Viewport dedupes by
    # name (the unescaped shell can carry a second, differing copy);
    # theme-color only drops byte-identical repeats, keeping the intentional
    # light/dark media pair.
    html = _keep_first_tag(html, r'<meta name="viewport"[^>]*>')
    return _dedupe_exact_tags(html, r'<meta name="theme-color"[^>]*>')


def main() -> int:
    if not SHELL_SRC.is_file():
        print(f"build_iso20022_mcp: shell missing at {SHELL_SRC}", file=sys.stderr)
        return 1
    # Unescape first so every meta is a real tag (no-op on CI).
    shell = _unescape_head_metas(_nav(SHELL_SRC.read_text(encoding="utf-8")))
    body = _render_body(C)
    out = _swap_into_shell(shell, body, C["meta_title"], C["meta_description"], URL)
    out = _fix_metas(out)
    out = _lang_switcher_home(out)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(out, encoding="utf-8")
    rel = OUT.relative_to(ROOT) if OUT.is_relative_to(ROOT) else OUT
    print(f"build_iso20022_mcp: wrote {rel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
