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
    "mcp-band-img-tall": (1920, 1080),
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


def _imgband(name: str, alt: str, cls: str = "mcp-band-img") -> str:
    """A full-bleed-within-wrap image band that breaks up the text sections.
    ``cls`` picks the crop: the default 16/6 strip, or the 16/9
    ``mcp-band-img-tall`` for photos whose subject a 16/6 crop beheads
    (the wall-clock band; its face just fits a centred 16/9)."""
    return (
        '<section><div class="spk-wrap">'
        + _img(name, alt, cls, "(max-width:1120px) 100vw, 1120px")
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
    "mcp-what": ["alert", "globe", "grid", "layers"],
    "mcp-arc": ["layers", "grid", "link"],
    "mcp-safety": ["check", "shield", "eye", "lock"],
    "mcp-security": ["lock", "check", "globe", "shield"],
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


# Shared install strings. One source so the tabs, client cards and tests can
# never drift apart. The uvx command is the one proven against the live
# gateway (stdio JSON-RPC initialize / tools/list / tools/call, 2026-07-15).
UVX_ARGS = '"--from", "iso20022-mcp[pain,pacs,acmt]", "iso20022-mcp"'
UVX_CMD = 'uvx --from "iso20022-mcp[pain,pacs,acmt]" iso20022-mcp'
_JSON_BODY = (
    '    "iso20022": {\n'
    '      "command": "uvx",\n'
    f"      \"args\": [{UVX_ARGS}]\n"
    "    }"
)
MCPSERVERS_JSON = '{\n  "mcpServers": {\n' + _JSON_BODY + "\n  }\n}"
VSCODE_JSON = (
    '{\n  "servers": {\n'
    '    "iso20022": {\n'
    '      "type": "stdio",\n'
    '      "command": "uvx",\n'
    f"      \"args\": [{UVX_ARGS}]\n"
    "    }\n  }\n}"
)
AGENTS_SDK_PY = (
    "async with MCPServerStdio(\n"
    '    name="iso20022",\n'
    '    params={\n'
    '        "command": "uvx",\n'
    f"        \"args\": [{UVX_ARGS}],\n"
    "    },\n"
    ") as server:\n"
    "    ..."
)

# Where the captured gateway tool schemas live. Recorded once from a running
# server (tools/list over stdio JSON-RPC) and committed; the build renders
# them verbatim, and skips the section gracefully when the file is absent.
SCHEMAS_SRC = ROOT / "_data" / "mcp" / "tool_schemas.json"


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
            {
                "eyebrow": "THE OUTCOME",
                "title": "Build the next era of your enterprise.",
                "body": (
                    "Agents that act across your whole payment stack: "
                    "initiate, reconcile, migrate and resolve, on an open, "
                    "vendor-neutral standard you can run anywhere."
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
                "eyebrow": "READ-ONLY",
                "title": "Read-only where it counts.",
                "body": (
                    "Reconciliation is pure matching, and every tool is "
                    "marked read-only, idempotent and closed-world, so "
                    "clients can reason about safety."
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
    # Trust pack: how a payment flows, with the human approval wall.
    # Every claim below is verified: the gateway's tools/list annotations mark
    # all seven meta-tools readOnlyHint / idempotentHint / closed-world, the
    # installed suite packages contain no outbound network calls, and every
    # generator XSD-validates before returning (test-driven 2026-07-15).
    "flow": {
        "eyebrow": "TRUST, BY ARCHITECTURE",
        "headline": "Money never moves without a human.",
        "lede": (
            "The servers produce and check messages. Sending them stays "
            "behind your approval, in your own systems."
        ),
        "steps": [
            {
                "num": "01",
                "title": "Generate locally.",
                "body": (
                    "Your records become a pain.001 or pacs.008 on your own "
                    "machine, over stdio. Nothing is uploaded anywhere."
                ),
                "gate": False,
            },
            {
                "num": "02",
                "title": "Validate locally.",
                "body": (
                    "Output is checked against the bundled official XSD "
                    "before it returns. Deterministic, offline, the same "
                    "answer every run."
                ),
                "gate": False,
            },
            {
                "num": "03",
                "title": "A human approves.",
                "body": (
                    "Every meta-tool is annotated read-only and idempotent. "
                    "The message is a file; a person decides whether it "
                    "becomes a payment."
                ),
                "gate": True,
            },
            {
                "num": "04",
                "title": "Your rails dispatch.",
                "body": (
                    "Submission to SWIFT, SEPA or FedNow happens in your own "
                    "banking channel. The servers hold no credentials and "
                    "never move money."
                ),
                "gate": False,
            },
        ],
    },
    # Security strip. "No outbound network calls" is asserted from source:
    # the installed suite packages (iso20022_mcp, pain001(-mcp), pacs008(-mcp),
    # acmt001(-mcp)) contain no requests/httpx/urllib/socket network code.
    "security": {
        "eyebrow": "SECURITY POSTURE",
        "headline": "Your payment data stays yours.",
        "cards": [
            {
                "eyebrow": "LOCAL-FIRST",
                "title": "Zero data retention.",
                "body": (
                    "The stdio servers run inside your environment and make "
                    "no outbound network calls. Nothing is sent, nothing is "
                    "stored, nothing phones home."
                ),
            },
            {
                "eyebrow": "DETERMINISTIC",
                "title": "Validated on your machine.",
                "body": (
                    "Every generated message is checked against the bundled "
                    "official ISO 20022 XSD locally, before you ever see it."
                ),
            },
            {
                "eyebrow": "OPEN",
                "title": "Apache-2.0, in the open.",
                "body": (
                    "Every server is open source on PyPI and the official "
                    "MCP registry. Read the code before you trust it."
                ),
            },
            {
                "eyebrow": "TESTED",
                "title": "100% branch-tested.",
                "body": (
                    "Full branch coverage across the suite, so the paths an "
                    "agent exercises are the paths the tests exercise."
                ),
            },
        ],
    },
    # Multi-client integration. Config shapes verified against each client's
    # official documentation on 2026-07-15; see the docs page for sources.
    "clients": {
        "eyebrow": "WORKS WITH YOUR STACK",
        "headline": "Works with every MCP client.",
        "lede": (
            "One standard stdio server, so the setup is one small block in "
            "your client's own config. Remote-first platforms connect to "
            "hosted MCP servers instead."
        ),
        "stdio": [
            {
                "name": "Claude Code",
                "slug": "claude-code",
                "where": "One command, from any directory.",
                "code": f"claude mcp add iso20022 -- {UVX_CMD}",
            },
            {
                "name": "Claude Desktop",
                "slug": "claude-desktop",
                "where": "Settings, Developer, Edit Config: claude_desktop_config.json.",
                "code": MCPSERVERS_JSON,
            },
            {
                "name": "Cursor",
                "slug": "cursor",
                "where": ".cursor/mcp.json in the project, or ~/.cursor/mcp.json.",
                "code": MCPSERVERS_JSON,
            },
            {
                "name": "Windsurf",
                "slug": "windsurf",
                "where": "~/.codeium/windsurf/mcp_config.json.",
                "code": MCPSERVERS_JSON,
            },
            {
                "name": "VS Code + GitHub Copilot",
                "slug": "vscode",
                "where": '.vscode/mcp.json. The top-level key is "servers".',
                "code": VSCODE_JSON,
            },
            {
                "name": "Google Gemini CLI",
                "slug": "gemini",
                "where": '"mcpServers" inside ~/.gemini/settings.json.',
                "code": MCPSERVERS_JSON,
            },
        ],
        "remote": [
            {
                "name": "OpenAI",
                "slug": "openai",
                "body": (
                    "The Agents SDK spawns the suite locally over stdio "
                    "through its MCPServerStdio class, with the same command "
                    "and args. ChatGPT connectors and the Responses API "
                    "connect to remote MCP servers over Streamable HTTP or "
                    "HTTP/SSE only, so they pair with a hosted deployment, "
                    "not a local process."
                ),
                "code": AGENTS_SDK_PY,
            },
            {
                "name": "Microsoft Copilot Studio",
                "body": (
                    "Adds MCP servers to agents as tools through Power "
                    "Platform connectors, over the Streamable HTTP transport "
                    "only; it does not run local stdio servers."
                ),
            },
            {
                "name": "Zapier MCP",
                "body": (
                    "A Zapier-hosted remote MCP endpoint: you create a "
                    "dedicated server at mcp.zapier.com and point your "
                    "client at the generated URL. It connects clients to "
                    "Zapier actions, not to local servers like this suite."
                ),
            },
        ],
    },
    # CSS-only tabbed install block (radio-input tabs, strict-CSP safe).
    "install": {
        "eyebrow": "INSTALL",
        "headline": "Install it your way.",
        "lede": (
            "Run it with uvx and nothing to install, pin it with pip, or "
            "drop one block of JSON into Claude Desktop."
        ),
        "tabs": [
            {
                "id": "uvx",
                "label": "uvx",
                "code": UVX_CMD,
                "note": (
                    "No install, no account, no key. Add camt053-mcp the "
                    "same way for bank statements."
                ),
            },
            {
                "id": "pip",
                "label": "pip",
                "code": (
                    'pip install "iso20022-mcp[pain,pacs,acmt]"\n'
                    "iso20022-mcp"
                ),
                "note": (
                    "Installed with pip, the client config is just the "
                    "iso20022-mcp command, no args."
                ),
            },
            {
                "id": "json",
                "label": "Claude Desktop",
                "code": MCPSERVERS_JSON,
                "note": (
                    "Settings, Developer, Edit Config, then restart. The "
                    "tools appear under the tools icon in the chat box."
                ),
            },
            {
                "id": "cursor",
                "label": "Cursor",
                "code": MCPSERVERS_JSON,
                "note": (
                    ".cursor/mcp.json in the project, or ~/.cursor/mcp.json "
                    "to make the suite available everywhere."
                ),
            },
            {
                "id": "vscode",
                "label": "VS Code",
                "code": VSCODE_JSON,
                "note": (
                    '.vscode/mcp.json, for GitHub Copilot. The top-level '
                    'key is "servers", not "mcpServers".'
                ),
            },
            {
                "id": "agents",
                "label": "OpenAI Agents SDK",
                "code": AGENTS_SDK_PY,
                "note": (
                    "The Python Agents SDK spawns the server itself over "
                    "stdio through MCPServerStdio."
                ),
            },
        ],
    },
    "schemas": {
        "eyebrow": "THE GATEWAY, VERBATIM",
        "headline": "Seven meta-tools, captured live.",
        "lede": (
            "Recorded from a running gateway over stdio JSON-RPC "
            "(tools/list), not written by hand. Expand a tool to see its "
            "real description and input schema."
        ),
        "note": (
            "Captured from iso20022-mcp 0.0.2 on 15 July 2026. Every tool "
            "is annotated read-only, idempotent and closed-world."
        ),
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
        (
            "STEP 4",
            "Keep humans in the loop.",
            "The agent can search, generate and validate complex ISO 20022 "
            "XML, but by design it never moves money directly. Have it "
            "output the XSD-valid payload, or route it to your bank's SFTP, "
            "API gateway or treasury queue for final human approval and "
            "settlement. Generation stays separate from execution, so the "
            "AI can draft, reconcile and migrate with no risk of "
            "unauthorised funds leaving accounts.",
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


def _flow(d: dict) -> str:
    """The trust flow: generation and validation are local, dispatch sits
    behind a human approval wall. Rendered as an ordered list so assistive
    tech announces the four stages in sequence."""
    steps = []
    for s in d["steps"]:
        gate = " mcp-step-gate" if s["gate"] else ""
        badge = (
            '<span class="mcp-gate-badge">Approval wall</span>' if s["gate"] else ""
        )
        steps.append(
            f'<li class="mcp-step{gate}">'
            f'<span class="mcp-step-num" aria-hidden="true">{_esc(s["num"])}</span>'
            f"{badge}"
            f'<h3>{_esc(s["title"])}</h3><p>{_rich(s["body"])}</p></li>'
        )
    return (
        '<section id="mcp-flow"><div class="spk-wrap">'
        + _head(d["eyebrow"], d["headline"], d["lede"])
        + f'<ol class="mcp-flow">{"".join(steps)}</ol></div></section>'
    )


def _security(d: dict) -> str:
    """Four-up security strip: local-first, deterministic, open, tested."""
    cells = []
    for i, it in enumerate(d["cards"]):
        cells.append(
            '<div class="mcp-sec-cell">'
            + _icon("mcp-security", i)
            + f'<span class="spk-eyebrow">{_esc(it["eyebrow"])}</span>'
            f'<h3>{_esc(it["title"])}</h3><p>{_rich(it["body"])}</p></div>'
        )
    return (
        '<section class="spk-band" id="mcp-security"><div class="spk-wrap">'
        + _head(d["eyebrow"], d["headline"])
        + f'<div class="mcp-sec">{"".join(cells)}</div></div></section>'
    )


def _code_block(code: str, block_id: str = "", copy: bool = False) -> str:
    """A literal code block, plus an optional copy button riding main.js's
    site-wide [data-copy] delegate (no inline JS; CSP-safe)."""
    id_attr = f' id="{block_id}"' if block_id else ""
    btn = ""
    if copy and block_id:
        btn = (
            f'<button type="button" class="mcp-copy" data-copy="#{block_id}" '
            f'aria-label="Copy to clipboard">Copy</button>'
        )
    return f'<pre class="mcp-code"{id_attr}><code>{_esc(code)}</code></pre>{btn}'


def _clients(d: dict) -> str:
    """The multi-client grid. Local-stdio clients get their documented config
    shape verbatim; remote-first platforms get one honest sentence."""
    cards = [
        '<div class="mcp-client">'
        f'<h3>{_esc(it["name"])}</h3>'
        f'<p class="mcp-client-where">{_esc(it["where"])}</p>'
        + _code_block(it["code"], f'mcp-code-client-{it["slug"]}', copy=True)
        + "</div>"
        for it in d["stdio"]
    ]
    remote = []
    for it in d["remote"]:
        code = (
            _code_block(it["code"], f'mcp-code-client-{it["slug"]}', copy=True)
            if it.get("code")
            else ""
        )
        remote.append(
            '<div class="mcp-client mcp-client-remote">'
            f'<h3>{_esc(it["name"])}</h3><p>{_rich(it["body"])}</p>{code}</div>'
        )
    return (
        '<section id="mcp-clients"><div class="spk-wrap">'
        + _head(d["eyebrow"], d["headline"], d["lede"])
        + f'<div class="mcp-clients">{"".join(cards)}</div>'
        '<p class="mcp-clients-label">Remote-first platforms</p>'
        f'<div class="mcp-clients mcp-clients-3">{"".join(remote)}</div>'
        '<p class="mcp-clients-foot">Config shapes checked against each '
        "client's official documentation, July 2026. "
        '<a href="/iso20022-mcp-docs/index.html#clients" class="spk-textlink">'
        "Full per-client setup</a></p>"
        "</div></section>"
    )


def _install_tabs(d: dict) -> str:
    """CSS-only tabbed install block. Radio inputs drive which panel shows
    (:checked ~ sibling selectors in the stylesheet); no JS, no inline style,
    and the radios stay keyboard-focusable."""
    tabs = d["tabs"]
    radios, labels, panels = [], [], []
    for i, t in enumerate(tabs):
        tid = f'mcp-tab-{t["id"]}'
        checked = " checked" if i == 0 else ""
        radios.append(
            f'<input type="radio" name="mcp-install-tab" id="{tid}" '
            f'class="mcp-tab-in"{checked}>'
        )
        labels.append(f'<label for="{tid}">{_esc(t["label"])}</label>')
        panels.append(
            f'<div class="mcp-tab-panel" id="mcp-panel-{t["id"]}">'
            + _code_block(t["code"], f'mcp-code-{t["id"]}', copy=True)
            + f'<p class="mcp-tab-note">{_rich(t["note"])}</p></div>'
        )
    return (
        '<section id="mcp-install"><div class="spk-wrap">'
        + _head(d["eyebrow"], d["headline"], d["lede"])
        + '<div class="mcp-tabs">'
        + "".join(radios)
        + f'<div class="mcp-tab-labels">{"".join(labels)}</div>'
        + "".join(panels)
        + "</div></div></section>"
    )


def _schema_props(schema: dict) -> str:
    """Render an inputSchema's properties as a definition list."""
    props = schema.get("properties") or {}
    if not props:
        return '<p class="mcp-props-none">Takes no arguments.</p>'
    required = set(schema.get("required") or [])
    items = []
    for name, spec in props.items():
        kind = _esc(str(spec.get("type", "any")))
        req = "required" if name in required else "optional"
        desc = spec.get("description", "")
        desc_html = f'<span class="mcp-prop-desc">{_esc(desc)}</span>' if desc else ""
        items.append(
            '<li><code class="spk-mono">'
            + _esc(name)
            + f'</code><span class="mcp-prop-type">{kind}, {req}</span>{desc_html}</li>'
        )
    return f'<ul class="mcp-props">{"".join(items)}</ul>'


def _schemas(d: dict) -> str:
    """Collapsible viewer over the captured gateway tool schemas. Reads the
    committed tools/list snapshot at build time; if the file is missing the
    section is skipped rather than failing the build."""
    if not SCHEMAS_SRC.is_file():
        print(
            f"build_iso20022_mcp: {SCHEMAS_SRC} missing; skipping schema viewer",
            file=sys.stderr,
        )
        return ""
    data = json.loads(SCHEMAS_SRC.read_text(encoding="utf-8"))
    tools = data.get("tools") or []
    if not tools:
        return ""
    blocks = [
        '<details class="mcp-schema">'
        '<summary><code class="spk-mono">'
        + _esc(t["name"])
        + '</code><span class="mcp-schema-sum">'
        + _esc(t.get("description", ""))
        + '</span><span class="spk-ic" aria-hidden="true">+</span></summary>'
        '<div class="mcp-schema-body">'
        f'<p>{_esc(t.get("description", ""))}</p>'
        + _schema_props(t.get("inputSchema") or {})
        + "</div></details>"
        for t in tools
    ]
    return (
        '<section id="mcp-schemas"><div class="spk-wrap">'
        + _head(d["eyebrow"], d["headline"], d["lede"])
        + f'<div class="mcp-schemas">{"".join(blocks)}</div>'
        f'<p class="mcp-schema-note">{_esc(d["note"])}</p>'
        "</div></section>"
    )


def _render_body(d: dict) -> str:
    sections = [
        _hero(d),
        _hero_image(),
        _cards(d["benefits"], "mcp-benefits", bullets=False),
        _imgband(
            "majed-swan-RBEv0VyNi2U",
            "A grid of blue and white cubes with one cube glowing, evoking a validated message among structured blocks.",
        ),
        _cards(d["what"], "mcp-what", bullets=False),
        _cards(d["arc"], "mcp-arc", bullets=True),
        _flow(d["flow"]),
        _security(d["security"]),
        _imgband(
            "ocean-ng-L0xOtAnv94Y",
            "A minimalist wall clock, evoking payment operations measured in seconds.",
            cls="mcp-band-img-tall",
        ),
        _clients(d["clients"]),
        _install_tabs(d["install"]),
        _start(),
        _schemas(d["schemas"]),
        _cards(d["safety"], "mcp-safety", bullets=False),
    ]
    return (
        '<div class="speaking-page iso20022-mcp-page">' + "".join(sections) + "</div>"
    )


def _nav(shell: str) -> str:
    """Rebuild the primary nav as the site-wide 5-item dropdown structure.
    Idempotent, and robust to a stale shell that still carries a different
    nav (the regex consumes everything up to the </ul> that closes
    ap-menu, i.e. the one directly followed by </nav>, so nested ap-sub
    lists are handled).

    Active-state policy (nav re-architecture, deliberate): no marker is
    baked here. /iso20022-mcp/ is itself a nav sub-item under Suite, so
    postbuild's inject_nav_active marks that sub-item with
    aria-current="page" on the final page.
    """
    chev = (
        '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
        '<path d="M6 9l6 6 6-6"/></svg>'
    )

    def _toggle(item_id: str, label: str) -> str:
        return (
            '<button type="button" class="ap-sub-toggle" aria-expanded="false" '
            f'aria-controls="sub-{item_id}" aria-label="Toggle {label} submenu">'
            f"{chev}</button>"
        )

    items = (
        '<li class="has-sub"><a href="/about/index.html">About</a>'
        + _toggle("about", "About")
        + '<ul id="sub-about" class="ap-sub">'
        '<li><a href="/trust/index.html">Trust &amp; Compliance</a></li>'
        '<li><a href="/speaking/index.html">Public Speaking</a></li>'
        '<li><a href="/contact/index.html">Contact</a></li>'
        "</ul></li>"
        '<li><a href="/articles/index.html">Articles</a></li>'
        '<li class="has-sub"><a href="/library/index.html">Library</a>'
        + _toggle("library", "Library")
        + '<ul id="sub-library" class="ap-sub">'
        '<li><a href="/topics/index.html">Browse by Topic</a></li>'
        '<li><a href="/projects/index.html">Open Source Projects</a></li>'
        '<li><a href="/playlists/index.html">Video Playlists</a></li>'
        "</ul></li>"
        '<li class="has-sub"><a href="/research/index.html">Research</a>'
        + _toggle("research", "Research")
        + '<ul id="sub-research" class="ap-sub">'
        '<li><a href="/research/index.html">Whitepapers &amp; Reports</a></li>'
        '<li><a href="/case-studies/index.html">Real-World Case Studies</a></li>'
        "</ul></li>"
        '<li class="has-sub"><a href="/suite/index.html">Suite</a>'
        + _toggle("suite", "Suite")
        + '<ul id="sub-suite" class="ap-sub">'
        '<li><a href="/iso20022-mcp/index.html">ISO 20022 MCP Suite</a></li>'
        '<li><a href="/iso20022-mcp-docs/index.html">Documentation</a></li>'
        '<li><a href="/iso20022-mcp-reference/index.html">API Reference</a></li>'
        '<li><a href="/iso20022-mcp-recipes/index.html">Integration Recipes</a></li>'
        "</ul></li>"
    )
    out, n = re.subn(
        r'(<ul class="ap-menu">)[\s\S]*?(</ul>)(?=\s*</nav>)',
        lambda m: m.group(1) + items + m.group(2),
        shell,
        count=1,
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
