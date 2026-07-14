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

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "generators"))

from build_case_studies import _swap_into_shell
from build_speaking import _esc, _rich, _unescape_head_metas

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
    """Wrap a literal command/code snippet in the site's mono style."""
    return f'<span class="spk-mono">{_esc(s)}</span>'


def _img(name: str, alt: str, style: str, sizes: str, eager: bool = False) -> str:
    """A responsive CDN image (webp srcset), styled inline to avoid CSS risk."""
    prio = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (
        f'<img src="{CDN}/{name}-1920.webp" '
        f'srcset="{CDN}/{name}-640.webp 640w, {CDN}/{name}-1200.webp 1200w, '
        f'{CDN}/{name}-1920.webp 1920w" sizes="{sizes}" '
        f'alt="{_esc(alt)}" {prio} decoding="async" style="{style}">'
    )


def _imgband(name: str, alt: str) -> str:
    """A full-bleed-within-wrap image band that breaks up the text sections."""
    style = (
        "width:100%;border-radius:16px;aspect-ratio:16/6;object-fit:cover;"
        "display:block"
    )
    return (
        '<section><div class="spk-wrap">'
        + _img(name, alt, style, "(max-width:1120px) 100vw, 1120px")
        + "</div></section>"
    )


# --- Content (single source of copy) ----------------------------------------
C: dict = {
    "meta_title": "ISO 20022 MCP Suite: let AI agents make bank payments",
    "meta_description": (
        "The open ISO 20022 layer for AI agents. Eight vendor-neutral MCP "
        "servers to generate, validate, reconcile and settle bank payments "
        "from natural language. Apache-2.0, on PyPI and the MCP registry."
    ),
    "hero": {
        "eyebrow": "OPEN SOURCE · APACHE-2.0 · ON PYPI + THE MCP REGISTRY",
        "headline": "Let your AI agent make real bank payments.",
        "lede": (
            "Eight open MCP servers that turn plain language into validated ISO "
            "20022 bank messages: initiate, settle, reconcile and resolve. "
            "Vendor-neutral, runs anywhere, installed in one line.",
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
        "headline": "Eight servers, one payment lifecycle.",
        "lede": (
            "Install the gateway and let it route, or install just the server "
            "for the job. Each is one `pip install`, on the MCP registry."
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
    lede = h["lede"][0] if isinstance(h["lede"], (list, tuple)) else h["lede"]
    return (
        '<header class="spk-hero" id="spk-top"><div class="spk-hero-grid"><div>'
        f'<span class="spk-eyebrow">{_esc(h["eyebrow"])}</span>'
        f'<h1>{_esc(h["headline"])}</h1>'
        f'<p class="spk-lede">{_rich(lede)}</p>'
        '<div class="spk-cta-row">'
        '<a href="#mcp-start" class="spk-btn spk-btn-primary">Get started '
        '<span class="spk-arw">&#8594;</span></a>'
        '<a href="#mcp-benefits" class="spk-btn spk-btn-ghost">See what it '
        "does</a></div>"
        '<p class="spk-microproof"><strong>8</strong> servers, live on PyPI '
        "&middot; <strong>100%</strong> branch-tested &middot; "
        "<strong>vendor-neutral</strong>, Apache-2.0</p>"
        "</div></div></header>"
    )


def _hero_image() -> str:
    """The big full-bleed-within-wrap hero photo, Partner-Network style."""
    style = (
        "width:100%;border-radius:18px;aspect-ratio:16/8;object-fit:cover;"
        "display:block"
    )
    return (
        '<section><div class="spk-wrap" style="margin-block-start:clamp(24px,4vw,44px)">'
        + _img(
            "modern-corporate-office-with-technological-displays",
            "A modern financial operations floor with technology displays.",
            style,
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
            cta = (
                f'<a href="{_esc(it["cta_href"])}" class="spk-btn {primary}">'
                f'{_esc(it["cta_label"])}</a>'
            )
            extra = f"<ul>{lis}</ul>{cta}"
        items.append(
            '<div class="spk-path">'
            f'<span class="spk-eyebrow">{_esc(it["eyebrow"])}</span>'
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
            + _mono('uvx --from "iso20022-mcp[all]" iso20022-mcp'),
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
        '<div class="spk-cta-row" style="margin-block-start:1.8rem">'
        f'<a href="{GH}" class="spk-btn spk-btn-primary">Get started on GitHub '
        '<span class="spk-arw">&#8594;</span></a>'
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
    """Rebuild the primary nav as the 5-item Apple-Partner-Network structure,
    with Suite (this page) active. Idempotent, and robust to a stale shell that
    still carries the old 9-item nav.
    """
    items = (
        '<li><a href="/iso20022-mcp/index.html" aria-current="page" '
        'class="active">Suite</a></li>'
        '<li><a href="/papers/index.html">Research</a></li>'
        '<li><a href="/case-studies/index.html">Case Studies</a></li>'
        '<li><a href="/projects/index.html">Resources</a></li>'
        '<li><a href="/about/index.html">About</a></li>'
    )
    return re.sub(
        r'(<ul class="ap-menu">).*?(</ul>)',
        lambda m: m.group(1) + items + m.group(2),
        shell,
        count=1,
        flags=re.DOTALL,
    )


def _fix_metas(html: str) -> str:
    """Swap the article-shell metas _swap_into_shell misses, by exact tag only.

    Targeted regex per meta tag -- never a global string replace, which would
    also corrupt nav links / breadcrumbs / aria-labels that share the text.
    """
    title, desc = _esc(C["meta_title"]), _esc(C["meta_description"])
    # The shell can carry more than one name="description" (a page one and an
    # articles-listing one); replace every copy with the MCP description.
    html = re.sub(
        r'<meta name="description"[^>]*>',
        f'<meta name="description" content="{desc}">',
        html,
    )
    swaps = [
        (
            r'<meta name="keywords"[^>]*>',
            f'<meta name="keywords" content="{_esc(KEYWORDS)}">',
        ),
        (
            r'<meta name="apple-mobile-web-app-title"[^>]*>',
            '<meta name="apple-mobile-web-app-title" content="ISO 20022 MCP">',
        ),
        (
            r'<meta name="application-name"[^>]*>',
            '<meta name="application-name" content="ISO 20022 MCP">',
        ),
        (
            r'<meta name="twitter:title"[^>]*>',
            f'<meta name="twitter:title" content="{title}">',
        ),
        (
            r'<meta name="twitter:description"[^>]*>',
            f'<meta name="twitter:description" content="{desc}">',
        ),
    ]
    for pat, rep in swaps:
        html = re.sub(pat, rep, html, count=1)
    return html


def main() -> int:
    if not SHELL_SRC.is_file():
        print(f"build_iso20022_mcp: shell missing at {SHELL_SRC}", file=sys.stderr)
        return 1
    # Unescape first so every meta is a real tag (no-op on CI).
    shell = _unescape_head_metas(_nav(SHELL_SRC.read_text(encoding="utf-8")))
    body = _render_body(C)
    out = _swap_into_shell(shell, body, C["meta_title"], C["meta_description"], URL)
    out = _fix_metas(out)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(out, encoding="utf-8")
    print(f"build_iso20022_mcp: wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
