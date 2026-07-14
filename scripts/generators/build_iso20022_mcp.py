#!/usr/bin/env python3
# =============================================================================
# Build the premium /iso20022-mcp/ hub page.
#
# Mirrors build_speaking.py: clone the built ``public/articles/index.html``
# shell (typography, CSP, SRI, a11y chrome, primary nav) and swap in a body of
# ``spk-``-prefixed editorial sections. This keeps the ISO 20022 MCP hub at the
# same Apple-caliber presentation as /speaking, with a friendly, Google-style
# "What is MCP?" explainer for newcomers.
#
# All copy lives in this file's CONTENT dict (no separate data file yet); the
# spk- CSS is already AAA-contrast-compliant. English-only for now; locale
# forks can be added later exactly as build_speaking does.
#
# Input:  public/articles/index.html   (shell template, built by ssg first)
# Output: public/iso20022-mcp/index.html
# =============================================================================
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "generators"))

from build_case_studies import _swap_into_shell  # noqa: E402
from build_speaking import _esc, _rich  # noqa: E402

PUBLIC = ROOT / "public"
SHELL_SRC = PUBLIC / "articles" / "index.html"
OUT = PUBLIC / "iso20022-mcp" / "index.html"
URL = "https://sebastienrousseau.com/iso20022-mcp"
GH = "https://github.com/sebastienrousseau/iso20022-mcp"

# --- Content (single source of copy) ----------------------------------------
C: dict = {
    "meta_title": "ISO 20022 MCP Suite: payments for AI agents",
    "meta_description": (
        "The open ISO 20022 layer for AI agents. Eight vendor-neutral MCP "
        "servers to generate, validate, reconcile and settle ISO 20022 "
        "payments from natural language. Apache-2.0, on PyPI and the MCP "
        "registry."
    ),
    "hero": {
        "eyebrow": "OPEN SOURCE · APACHE-2.0 · ON PYPI + THE MCP REGISTRY",
        "headline": "The open ISO 20022 layer for AI agents.",
        "lede": (
            "Eight vendor-neutral MCP servers that let an AI agent generate, "
            "validate, reconcile and settle ISO 20022 payments from natural "
            "language. Runs anywhere, owned by no bank, installed in one line."
        ),
        "microproof": [
            "8 servers, live on PyPI",
            "100% branch-test coverage",
            "Vendor-neutral, Apache-2.0",
        ],
    },
    "what": {
        "eyebrow": "START HERE",
        "headline": "What is the Model Context Protocol?",
        "lede": (
            "MCP is an open standard that lets AI assistants use real tools "
            "safely. Think of it as a universal port between an assistant and "
            "the systems it needs to act on."
        ),
        "cards": [
            {
                "eyebrow": "THE PROBLEM",
                "title": "Agents can talk, but not act.",
                "body": (
                    "A language model can describe a SEPA payment, but it can't "
                    "produce the exact, schema-valid bank message that actually "
                    "moves it. Every integration used to be bespoke glue code."
                ),
            },
            {
                "eyebrow": "THE STANDARD",
                "title": "One protocol, any tool.",
                "body": (
                    "MCP gives assistants a common way to discover and call "
                    "tools, from any client (Claude, Cursor, your own agent). "
                    "Write a capability once; every MCP-aware assistant can use "
                    "it, with the client deciding what to allow."
                ),
            },
            {
                "eyebrow": "THIS SUITE",
                "title": "Payments as MCP tools.",
                "body": (
                    "These servers expose ISO 20022 as MCP tools: ask in plain "
                    "terms, get back XSD-validated messages. The bank-message "
                    "layer, made callable by an agent, without a bespoke "
                    "translator between your systems and the rails."
                ),
            },
        ],
    },
    "arc": {
        "eyebrow": "ONE SUITE, THE WHOLE LIFECYCLE",
        "headline": "Discover, settle, reconcile, resolve.",
        "lede": (
            "Install the gateway and let it route, or install just the server "
            "for the job in front of you. Each is `pip install`-able and on the "
            "official MCP registry."
        ),
        "cards": [
            {
                "eyebrow": "DISCOVER + GENERATE",
                "title": "The gateway.",
                "body": (
                    "One agent-friendly surface across pain, pacs, camt and "
                    "acmt. Search for a message, generate XSD-valid XML, parse "
                    "an inbound one, all through seven meta-tools."
                ),
                "bullets": ["iso20022-mcp", "pain001-mcp", "pacs008-mcp"],
                "cta_label": "Read the docs",
                "cta_href": "/iso20022-mcp-docs/index.html",
            },
            {
                "eyebrow": "RECONCILE + RESOLVE",
                "title": "Close the loop.",
                "body": (
                    "Match a camt.053 statement against expected pain.001 "
                    "payments, explainably. When a payment goes wrong, cancel "
                    "and resolve it with camt.056 and camt.029, XSD-valid."
                ),
                "bullets": ["reconcile-mcp", "camt053-mcp", "camt-exceptions"],
                "cta_label": "See the recipes",
                "cta_href": "/iso20022-mcp-recipes/index.html",
            },
            {
                "eyebrow": "BRIDGE AGENT PAYMENTS",
                "title": "Mandate to bank rail.",
                "body": (
                    "Turn a signed Google AP2 or Coinbase x402 agent mandate "
                    "into a wire-valid pain.001, with spending-cap and expiry "
                    "guardrails. It transforms and validates; it never moves "
                    "money."
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
                    "Every generator validates its output against the official "
                    "bundled XSD before it hands it back. Malformed messages "
                    "never leave the tool."
                ),
            },
            {
                "eyebrow": "GUARDED",
                "title": "Never moves money.",
                "body": (
                    "The AP2 bridge only transforms and validates; producing a "
                    "message is deliberately separate from sending it, so the "
                    "money-movement step stays a human-guarded action."
                ),
            },
            {
                "eyebrow": "OPEN",
                "title": "Owned by no bank.",
                "body": (
                    "Apache-2.0, 100% branch-tested, on your own "
                    "infrastructure, tied to no balance sheet. The message "
                    "engine everyone else has to build."
                ),
            },
        ],
    },
    "faq": {
        "eyebrow": "QUICKSTART",
        "headline": "Start in under a minute.",
        "items": [
            {
                "q": "How do I try it right now?",
                "a": (
                    "Run the gateway with no install and no account: "
                    "`uvx --from \"iso20022-mcp[all]\" iso20022-mcp`. Ask it to "
                    "search \"cancel a payment\" and it points you at camt.056; "
                    "ask it to generate and you get XSD-valid XML back."
                ),
            },
            {
                "q": "Which server do I need?",
                "a": (
                    "Start with the gateway and let it route, or install just "
                    "one: pain001-mcp to initiate, pacs008-mcp to settle, "
                    "camt053-mcp to read statements, reconcile-mcp to "
                    "reconcile, camt-exceptions to cancel or resolve, "
                    "ap2-iso20022 to bridge an agent mandate."
                ),
            },
            {
                "q": "Is it safe to give an agent?",
                "a": (
                    "Yes, by design. Generators validate against the official "
                    "XSD before returning; the AP2 bridge never moves money; "
                    "reconciliation is read-only. Producing a message is "
                    "deliberately separate from sending it."
                ),
            },
            {
                "q": "Does it help with the ISO 20022 migration?",
                "a": (
                    "Directly. MT retires between 2025 and 2028 and structured "
                    "addresses become mandatory in November 2026. The suite "
                    "ships the MT to MX converters and the structured-address "
                    "toolkit, so you migrate one message at a time."
                ),
            },
        ],
    },
    "final": {
        "headline": "The bank rail for AI agents is open. Build on it.",
        "lede": (
            "Eight servers, the whole ISO 20022 payment lifecycle, "
            "vendor-neutral and installable in one line."
        ),
    },
}


# --- Section renderers (spk- components, matching /speaking) -----------------
def _head(eyebrow: str, headline: str, lede: str = "") -> str:
    lede_html = f'<p class="spk-lede">{_rich(lede)}</p>' if lede else ""
    return (
        '<div class="spk-head spk-center">'
        f'<span class="spk-eyebrow">{_esc(eyebrow)}</span>'
        f"<h2>{_esc(headline)}</h2>{lede_html}</div>"
    )


def _hero(d: dict) -> str:
    h = d["hero"]
    micro = " · ".join(
        f"<strong>{_esc(m.split(' ', 1)[0])}</strong> {_esc(m.split(' ', 1)[1])}"
        if " " in m else _esc(m)
        for m in h["microproof"]
    )
    return (
        '<header class="spk-hero" id="spk-top"><div class="spk-hero-grid"><div>'
        f'<span class="spk-eyebrow">{_esc(h["eyebrow"])}</span>'
        f'<h1>{_esc(h["headline"])}</h1>'
        f'<p class="spk-lede">{_esc(h["lede"])}</p>'
        '<div class="spk-cta-row">'
        f'<a href="{GH}" class="spk-btn spk-btn-primary">Get started '
        '<span class="spk-arw">&#8594;</span></a>'
        '<a href="#mcp-docs" class="spk-btn spk-btn-ghost">Read the docs</a>'
        "</div>"
        f'<p class="spk-microproof">{micro}</p>'
        "</div></div></header>"
    )


def _cards(section: dict, section_id: str, with_bullets: bool) -> str:
    cards = []
    for i, it in enumerate(section["cards"]):
        primary = "spk-btn-primary" if i == 0 else "spk-btn-ghost"
        bullets = cta = ""
        if with_bullets:
            lis = "".join(f"<li>{_esc(b)}</li>" for b in it.get("bullets", []))
            bullets = f"<ul>{lis}</ul>"
            cta = (
                f'<a href="{_esc(it["cta_href"])}" class="spk-btn {primary}">'
                f'{_esc(it["cta_label"])}</a>'
            )
        cards.append(
            '<div class="spk-path">'
            f'<span class="spk-eyebrow">{_esc(it["eyebrow"])}</span>'
            f'<h3>{_esc(it["title"])}</h3>'
            f'<p>{_rich(it["body"])}</p>{bullets}{cta}</div>'
        )
    return (
        f'<section id="{section_id}"><div class="spk-wrap">'
        + _head(section["eyebrow"], section["headline"], section.get("lede", ""))
        + f'<div class="spk-paths">{"".join(cards)}</div></div></section>'
    )


def _safety(d: dict) -> str:
    s = d["safety"]
    cards = "".join(
        '<div class="spk-path">'
        f'<span class="spk-eyebrow">{_esc(it["eyebrow"])}</span>'
        f'<h3>{_esc(it["title"])}</h3><p>{_rich(it["body"])}</p></div>'
        for it in s["cards"]
    )
    return (
        '<section class="spk-band" id="mcp-safety"><div class="spk-wrap">'
        + _head(s["eyebrow"], s["headline"])
        + f'<div class="spk-paths">{cards}</div></div></section>'
    )


def _faq(d: dict) -> str:
    f = d["faq"]
    rows = "".join(
        "<details><summary>"
        f'{_esc(it["q"])} <span class="spk-ic">+</span></summary>'
        f'<div class="spk-ans">{_rich(it["a"])}</div></details>'
        for it in f["items"]
    )
    return (
        '<section class="spk-band" id="mcp-docs"><div class="spk-wrap">'
        + _head(f["eyebrow"], f["headline"])
        + f'<div class="spk-faq">{rows}</div>'
        '<div class="spk-cta-row" style="margin-block-start:1.8rem">'
        '<a href="/iso20022-mcp-docs/index.html" class="spk-btn spk-btn-ghost">'
        "Full quickstart</a>"
        '<a href="/iso20022-mcp-reference/index.html" class="spk-btn spk-btn-ghost">'
        "Tool reference</a>"
        '<a href="/iso20022-mcp-recipes/index.html" class="spk-btn spk-btn-ghost">'
        "Recipes</a></div></div></section>"
    )


def _final(d: dict) -> str:
    c = d["final"]
    return (
        '<section class="spk-band spk-finalcta"><div class="spk-wrap">'
        f'<h2>{_esc(c["headline"])}</h2>'
        f'<p class="spk-lede">{_esc(c["lede"])}</p>'
        '<div class="spk-cta-row">'
        f'<a href="{GH}" class="spk-btn spk-btn-primary">Get started on GitHub '
        '<span class="spk-arw">&#8594;</span></a>'
        '<a href="/iso20022-mcp-docs/index.html" class="spk-btn spk-btn-ghost">'
        "Read the docs</a></div></div></section>"
    )


def _render_body(d: dict) -> str:
    sections = [
        _hero(d),
        _cards(d["what"], "mcp-what", with_bullets=False),
        _cards(d["arc"], "mcp-arc", with_bullets=True),
        _safety(d),
        _faq(d),
        _final(d),
    ]
    return '<div class="speaking-page iso20022-mcp-page">' + "".join(sections) + "</div>"


def _nav(shell: str) -> str:
    """Mark the ISO 20022 nav item active (idempotent).

    Drops the Articles active state, then either activates an existing ISO
    20022 nav item (once the layouts carry it) or injects one after Projects
    (so this still works against a shell built before the layout change).
    """
    shell = shell.replace(
        '<a href="/articles/index.html" aria-current="page" class="active">Articles</a>',
        '<a href="/articles/index.html">Articles</a>',
        1,
    )
    plain = '<a href="/iso20022-mcp/index.html">ISO 20022</a>'
    active = '<a href="/iso20022-mcp/index.html" aria-current="page" class="active">ISO 20022</a>'
    if plain in shell:
        return shell.replace(plain, active, 1)
    return shell.replace(
        '<li><a href="/projects/index.html">Projects</a></li>',
        f'<li><a href="/projects/index.html">Projects</a></li><li>{active}</li>',
        1,
    )


def main() -> int:
    if not SHELL_SRC.is_file():
        print(f"build_iso20022_mcp: shell missing at {SHELL_SRC}", file=sys.stderr)
        return 1
    shell = _nav(SHELL_SRC.read_text(encoding="utf-8"))
    body = _render_body(C)
    out = _swap_into_shell(shell, body, C["meta_title"], C["meta_description"], URL)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(out, encoding="utf-8")
    print(f"build_iso20022_mcp: wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
