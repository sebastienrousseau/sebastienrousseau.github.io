#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

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
        '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>'
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
# gateway (stdio JSON-RPC initialize / tools/list, 2026-07-16): the [all]
# extra resolves cleanly since camt053 0.0.14 and acmt001 0.0.3.
UVX_ARGS = '"--from", "iso20022-mcp[all]", "iso20022-mcp"'
UVX_CMD = 'uvx --from "iso20022-mcp[all]" iso20022-mcp'
_JSON_BODY = f'    "iso20022": {{\n      "command": "uvx",\n      "args": [{UVX_ARGS}]\n    }}'
MCPSERVERS_JSON = '{\n  "mcpServers": {\n' + _JSON_BODY + "\n  }\n}"
VSCODE_JSON = (
    '{\n  "servers": {\n'
    '    "iso20022": {\n'
    '      "type": "stdio",\n'
    '      "command": "uvx",\n'
    f'      "args": [{UVX_ARGS}]\n'
    "    }\n  }\n}"
)
AGENTS_SDK_PY = (
    "async with MCPServerStdio(\n"
    '    name="iso20022",\n'
    "    params={\n"
    '        "command": "uvx",\n'
    f'        "args": [{UVX_ARGS}],\n'
    "    },\n"
    ") as server:\n"
    "    ..."
)
# Codex CLI stdio shape: a [mcp_servers.<name>] table in ~/.codex/config.toml
# with command/args keys. Verified against OpenAI's official Codex MCP docs
# (developers.openai.com/codex/mcp) on 2026-07-16.
CODEX_TOML = f'[mcp_servers.iso20022]\ncommand = "uvx"\nargs = [{UVX_ARGS}]'

# Where the captured gateway tool schemas live. Recorded once from a running
# server (tools/list over stdio JSON-RPC) and committed; the build renders
# them verbatim, and skips the section gracefully when the file is absent.
SCHEMAS_SRC = ROOT / "_data" / "mcp" / "tool_schemas.json"

# Live-verified evidence data, committed next to the schema snapshot:
# * hub_transcripts.json — prompt/result transcripts captured over stdio
#   JSON-RPC (the proof blocks render the excerpts verbatim);
# * verified_metrics.json — measured timings and adoption figures, each
#   carrying its as-of date and collection method.
# Same policy as the schema viewer: a missing file skips its section with
# a stderr note instead of failing the build.
TRANSCRIPTS_SRC = ROOT / "_data" / "mcp" / "hub_transcripts.json"
METRICS_SRC = ROOT / "_data" / "mcp" / "verified_metrics.json"


def _load_data(path: Path, what: str) -> dict | None:
    """Read one committed evidence file, or None (with a stderr note)."""
    if not path.is_file():
        print(
            f"build_iso20022_mcp: {path} missing; skipping {what}",
            file=sys.stderr,
        )
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _tool_count() -> int | None:
    """Suite-wide tool count, computed from the committed tools/list
    captures (the gateway snapshot plus every per-server capture) so the
    published figure can never drift from the evidence."""
    if not SCHEMAS_SRC.is_file():
        return None
    total = len(json.loads(SCHEMAS_SRC.read_text(encoding="utf-8"))["tools"])
    for f in sorted(SCHEMAS_SRC.parent.glob("*.tools.json")):
        total += len(json.loads(f.read_text(encoding="utf-8"))["tools"])
    return total


# Audience lens tags per section id (PR #338 "Read as…" pattern, extended
# to the hub). Every rendered section carries one of these so main.js can
# reorder without ever hiding content; the hero header and the selector
# itself stay untagged.
ALL_AUD = "boards engineers regulators"
AUDIENCES: dict[str, str] = {
    "mcp-board": "boards",
    "mcp-benefits": ALL_AUD,
    "mcp-simulator": ALL_AUD,
    "mcp-band-1": ALL_AUD,
    "mcp-capability": ALL_AUD,
    "mcp-what": ALL_AUD,
    "mcp-arc": "engineers",
    "mcp-flow": "boards regulators",
    "mcp-security": "boards regulators",
    "mcp-regulators": "regulators",
    "mcp-band-2": ALL_AUD,
    "mcp-proof": ALL_AUD,
    "mcp-free": ALL_AUD,
    "mcp-clients": "engineers",
    "mcp-install": "engineers",
    "mcp-start": "engineers",
    "mcp-prompts": "boards",
    "mcp-sandbox": "boards engineers",
    "mcp-adoption": "boards regulators",
    "mcp-schemas": "engineers regulators",
    "mcp-safety": "boards regulators",
}


def _aud(html: str, section_id: str) -> str:
    """Stamp a rendered block's first <section> tag with its audience lens
    tags. Empty blocks (a skipped section) pass through untouched."""
    if not html:
        return html
    tags = AUDIENCES[section_id]
    return html.replace("<section", f'<section data-audience="{tags}"', 1)


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
    # For the board: the three questions a board asks, answered without
    # figures we cannot source. Qualitative only, no invented savings.
    "board": {
        "eyebrow": "FOR THE BOARD",
        "headline": "Three questions, answered up front.",
        "lede": (
            "What agentic payments cost, what they risk and what they "
            "replace, before anyone books a meeting about it."
        ),
        "cards": [
            {
                "eyebrow": "WHAT IT COSTS",
                "title": "Free. Apache-2.0.",
                "body": (
                    "No licence, no account, no procurement. The whole suite "
                    "is open source on public PyPI, so adopting it is an "
                    "engineering decision, not a contract negotiation."
                ),
            },
            {
                "eyebrow": "WHAT IT RISKS",
                "title": "Money never moves without a human.",
                "body": (
                    "The servers generate and check messages; sending them "
                    "stays behind your own approval wall, in your own "
                    "systems. Every gateway tool is read-only and idempotent."
                ),
            },
            {
                "eyebrow": "WHAT IT REPLACES",
                "title": "Bespoke ISO 20022 integration work.",
                "body": (
                    "The message generation, validation and reconciliation "
                    "plumbing a team would otherwise build by hand against "
                    "the schemas, maintained in the open instead."
                ),
            },
        ],
    },
    # Capability contrast strip. Counts are computed at build time from the
    # committed tools/list captures; the zero-network and coverage claims
    # restate the verified security strip.
    "capability": {
        "eyebrow": "CAPABILITY, NOT BROCHURE",
        "headline": "An MCP server that does the work, not just the docs.",
        "lede": (
            "Ask for a payment and get the validated message itself. These "
            "servers generate, validate, parse, convert and reconcile ISO "
            "20022 on your machine; they do not stop at telling you how."
        ),
        "foot": (
            "Tool count computed at build time from the committed "
            "tools/list captures in this site's repository, recorded over "
            "stdio JSON-RPC from the running servers."
        ),
    },
    # Regulators & compliance: every claim below restates a captured tool
    # description (_data/mcp/camt053-mcp.tools.json, pacs008-mcp.tools.json)
    # or a live session run on 2026-07-16. The DORA paragraph is careful
    # control-mapping, never a certification claim.
    "regulators": {
        "eyebrow": "FOR REGULATORS AND COMPLIANCE",
        "headline": "Evidence a supervisor can check.",
        "lede": (
            "Tools that cite their sources, dates they enforce, and "
            "validation an auditor can rerun and get the same answer."
        ),
    },
    "free": {
        "eyebrow": "FREE, THREE WAYS",
        "headline": "Free means free.",
        "cards": [
            {
                "eyebrow": "BOARDS",
                "title": "Free to adopt.",
                "body": (
                    "Nothing to procure: no licence, no contract, no vendor "
                    "negotiation. Apache-2.0, tied to no balance sheet."
                ),
            },
            {
                "eyebrow": "ENGINEERS",
                "title": "Free to run.",
                "body": (
                    "No account, no API key, no metering. One uvx command "
                    "and the suite is running on your own machine."
                ),
            },
            {
                "eyebrow": "REGULATORS",
                "title": "Free to audit.",
                "body": (
                    "Every line public on GitHub and PyPI. Read the exact "
                    "code that validates the message before you rely on it."
                ),
            },
        ],
    },
    "prompts": {
        "eyebrow": "PASTE-AND-SEE",
        "headline": "Three prompts, three receipts.",
        "lede": (
            "Each prompt is limited to what the suite actually does, and "
            "each result excerpt is from a real tool session driven over "
            "stdio JSON-RPC. Paste the prompt into any connected client; "
            "the same ask becomes the same tool call."
        ),
    },
    "sandbox": {
        "eyebrow": "ZERO REAL DATA",
        "headline": "Try it with zero real data.",
    },
    "proof": {
        "eyebrow": "TIMED, NOT ESTIMATED",
        "headline": "Under a minute, with a stopwatch on it.",
    },
    "adoption": {
        "eyebrow": "ADOPTION, MEASURED",
        "headline": "Real numbers, dated.",
    },
    # Multi-client integration. Config shapes verified against each client's
    # official documentation on 2026-07-15 (Codex CLI: 2026-07-16); see the
    # docs page for sources.
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
            {
                "name": "OpenAI Codex CLI",
                "slug": "codex",
                "where": (
                    "~/.codex/config.toml, or one command: codex mcp add iso20022 -- uvx ..."
                ),
                "code": CODEX_TOML,
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
                    "No install, no account, no key. The [all] extra covers "
                    "every family, bank statements included."
                ),
            },
            {
                "id": "pip",
                "label": "pip",
                "code": ('pip install "iso20022-mcp[all]"\niso20022-mcp'),
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
                    ".vscode/mcp.json, for GitHub Copilot. The top-level "
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
    """Split hero: copy (eyebrow, h1, lede, CTA row) left, the animated
    terminal right at >=1100px (stacked below, terminal directly under the
    CTA row). The stats band (spk-microproof) sits after the split grid so
    it never pushes the terminal out of the initial viewport."""
    h = d["hero"]
    return (
        '<header class="spk-hero" id="spk-top">'
        '<div class="spk-hero-grid"><div class="mcp-hero-copy">'
        f'<span class="spk-eyebrow">{_esc(h["eyebrow"])}</span>'
        f"<h1>{_esc(h['headline'])}</h1>"
        f'<p class="spk-lede">{_rich(h["lede"])}</p>'
        '<div class="spk-cta-row">'
        '<a href="#mcp-start" class="spk-btn spk-btn-primary">Get started '
        '<span class="spk-arw" aria-hidden="true">&#8594;</span></a>'
        '<a href="#mcp-benefits" class="spk-btn spk-btn-ghost">See what it '
        "does</a></div>"
        "</div>"
        f'<div class="mcp-hero-term">{_hero_terminal()}</div>'
        "</div>"
        '<div class="spk-wrap"><p class="spk-microproof"><strong>9</strong> '
        "servers, live on PyPI &middot; <strong>100%</strong> branch-tested "
        "&middot; <strong>vendor-neutral</strong>, Apache-2.0</p></div>"
        "</header>"
    )


# Hero terminal session (corral-README style, CSS-only animation). Every
# line reuses content verified elsewhere on this site: the one-line install
# is the command proven against public PyPI (docs Chapter 1), `claude mcp
# list` reporting iso20022 as connected is documented in the same chapter,
# and the pain.001 ask/result mirrors the docs' tested prompt template
# (schema-valid pain.001.001.03, XSD-checked before return).
#
# (kind, timing-class, prompt-glyph, text). Typed lines carry --tw/--ts ch
# counts in articles.html CSS (gen_layouts.SPEAKING_MCP_HUB_CSS) that MUST
# equal len(glyph + text): t1=72ch, t2=17ch, t3b=8ch, t4=83ch.
# The ask line is typed INSIDE the Claude session opened by '$ claude' -
# a reader pasting it into a shell would get 'command not found'.
_TERM_LINES: list[tuple[str, str, str, str]] = [
    (
        "cmd",
        "mcp-tl-typed mcp-tl-t1",
        "$ ",
        'claude mcp add iso20022 -- uvx --from "iso20022-mcp[all]" iso20022-mcp',
    ),
    ("cmd", "mcp-tl-typed mcp-tl-t2", "$ ", "claude mcp list"),
    ("out", "mcp-tl-fade mcp-tl-f3", "", "iso20022 · connected"),
    ("cmd", "mcp-tl-typed mcp-tl-t3b", "$ ", "claude"),
    (
        "ask",
        "mcp-tl-typed mcp-tl-t4",
        "> ",
        "Generate a pain.001 credit transfer paying Acme GmbH EUR 4,200, executing Friday.",
    ),
    ("out", "mcp-tl-fade mcp-tl-f5", "", "generate · records validated against the official XSD"),
    ("ok", "mcp-tl-fade mcp-tl-f6", "", "✓ schema-valid pain.001.001.03 returned"),
]


def _hero_terminal() -> str:
    """The animated terminal session figure, embedded by _hero() as the
    second hero-grid cell so it is above the fold on first load (replaces
    the former 1920w hero webp: the demo is real selectable markup, so
    nothing is fetched, the reserved box cannot shift (zero CLS), and the
    LCP candidate stays the h1 headline instead of a hero image)."""
    lines = []
    for kind, timing, glyph, text in _TERM_LINES:
        ps = f'<span class="mcp-tl-ps" aria-hidden="true">{_esc(glyph)}</span>' if glyph else ""
        lines.append(f'<span class="mcp-tl mcp-tl-{kind} {timing}">{ps}{_esc(text)}</span>')
    caret = '<span class="mcp-tl mcp-tl-caret" aria-hidden="true"></span>'
    return (
        '<figure class="mcp-term">'
        '<figcaption class="mcp-term-bar">'
        '<span class="mcp-term-dot" aria-hidden="true"></span>'
        '<span class="mcp-term-dot" aria-hidden="true"></span>'
        '<span class="mcp-term-dot" aria-hidden="true"></span>'
        '<span class="mcp-term-title">Terminal · claude</span></figcaption>'
        f'<pre class="mcp-term-body"><code>{"".join(lines)}{caret}</code></pre>'
        "</figure>"
    )


def _cards(section: dict, section_id: str, band: bool = False, bullets: bool = False) -> str:
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
                f"{_esc(it['cta_label'])}</a>"
            )
            extra = f"<ul>{lis}</ul>{cta}"
        items.append(
            '<div class="spk-path">'
            + _icon(section_id, i)
            + f'<span class="spk-eyebrow">{_esc(it["eyebrow"])}</span>'
            f"<h3>{_esc(it['title'])}</h3><p>{_rich(it['body'])}</p>{extra}</div>"
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
            "at the right message, then " + _mono("generate") + " returns XSD-valid XML.",
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
        badge = '<span class="mcp-gate-badge">Approval wall</span>' if s["gate"] else ""
        steps.append(
            f'<li class="mcp-step{gate}">'
            f'<span class="mcp-step-num" aria-hidden="true">{_esc(s["num"])}</span>'
            f"{badge}"
            f"<h3>{_esc(s['title'])}</h3><p>{_rich(s['body'])}</p></li>"
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
            f"<h3>{_esc(it['title'])}</h3><p>{_rich(it['body'])}</p></div>"
        )
    return (
        '<section class="spk-band" id="mcp-security"><div class="spk-wrap">'
        + _head(d["eyebrow"], d["headline"])
        + f'<div class="mcp-sec">{"".join(cells)}</div></div></section>'
    )


def _read_as() -> str:
    """The "Read as…" audience selector, mirroring the homepage control
    (PR #338): ships [hidden] so a JS-off reader never sees an inert
    widget; main.js reveals it and re-orders the [data-audience] sections.
    A lens, not a filter — nothing is ever removed."""
    buttons = "".join(
        f'<button type="button" class="read-as-btn" data-read="{val}" '
        f'aria-pressed="{"true" if val == "" else "false"}">{label}</button>'
        for val, label in (
            ("", "Everyone"),
            ("boards", "Boards"),
            ("engineers", "Engineers"),
            ("regulators", "Regulators"),
        )
    )
    return (
        '<section class="read-as" data-announce="Now showing content for" '
        'aria-labelledby="read-as-label" hidden>'
        '<div class="read-as-inner">'
        '<span class="read-as-label" id="read-as-label">Read as…</span>'
        '<div class="read-as-group" role="group" '
        'aria-label="Choose your reading lens">'
        f"{buttons}</div></div>"
        '<p class="visually-hidden" data-read-status role="status" '
        'aria-live="polite"></p></section>'
    )


def _stat_cells(cells: list[tuple[str, str]]) -> str:
    return "".join(
        f'<div><p class="spk-num">{_esc(num)}</p><p class="spk-lbl">{_esc(lbl)}</p></div>'
        for num, lbl in cells
    )


def _capability(d: dict) -> str:
    """Capability contrast strip: servers/tools counted from the committed
    captures, plus the two verified posture claims. Skipped if the gateway
    snapshot is absent (same policy as the schema viewer)."""
    count = _tool_count()
    if count is None:
        print(
            "build_iso20022_mcp: tool captures missing; skipping capability strip",
            file=sys.stderr,
        )
        return ""
    cells = _stat_cells(
        [
            ("9", "servers on PyPI"),
            (str(count), "tools, captured live"),
            ("0", "outbound network calls"),
            ("100%", "branch coverage"),
        ]
    )
    return (
        '<section class="spk-band" id="mcp-capability"><div class="spk-wrap">'
        + _head(d["eyebrow"], d["headline"], d["lede"])
        + f'<div class="spk-stats mcp-cap-stats">{cells}</div>'
        f'<p class="spk-stats-foot">{_rich(d["foot"])}</p>'
        "</div></section>"
    )


def _regulators(d: dict) -> str:
    """The regulators & compliance section. Four cards, each restating a
    captured tool description, then the DORA note: control-mapping raw
    material only, with the no-certification caveat stated outright."""
    cards = [
        (
            "CITED, NOT ASSERTED",
            "Rulebook clauses with sources.",
            _mono("cite_rulebook")
            + " and "
            + _mono("list_rulebook_clauses")
            + " return curated SEPA, CBPR+ and HVPS+ clauses, versioned, "
            "each with its canonical source URL, so a compliance claim can "
            "be traced to the official document.",
        ),
        (
            "THE 2026 CUTOVER",
            "November 2026, encoded.",
            _mono("get_cbpr_cutover_date")
            + " returns 2026-11-16, and "
            + _mono("check_cbpr_readiness")
            + " audits a camt.053 statement against the CBPR+ acceptance "
            "rules that take effect at the 14-16 November 2026 cutover, "
            "structured postal addresses included.",
        ),
        (
            "STRUCTURED ADDRESSES",
            "The address cliff, tool by tool.",
            _mono("classify_address")
            + ", "
            + _mono("validate_address")
            + ", "
            + _mono("repair_address")
            + " and "
            + _mono("validate_addresses")
            + " classify, police and repair party addresses against the "
            "14 November 2026 rule that rejects unstructured-only addresses.",
        ),
        (
            "AUDIT EVIDENCE",
            "Deterministic, offline validation.",
            "Every generated message is checked against the bundled "
            "official XSD on your machine: same input, same answer, no "
            "network. A validation run can be reproduced by an auditor, "
            "line for line.",
        ),
    ]
    items = "".join(
        '<div class="spk-path">'
        f'<span class="spk-eyebrow">{_esc(eyebrow)}</span>'
        f"<h3>{_esc(title)}</h3><p>{body}</p></div>"
        for eyebrow, title, body in cards
    )
    dora = (
        "<strong>A note on DORA.</strong> This suite is not certified "
        "against DORA, and no such product certification exists. What the "
        "architecture offers is raw material for your own control mapping: "
        "local execution reduces reliance on external ICT providers for "
        "message validation, deterministic offline validation produces "
        "repeatable testing evidence, and open source means your auditors "
        "can read every line they depend on. Whether these properties "
        "satisfy your DORA obligations is your assessment to make."
    )
    return (
        '<section id="mcp-regulators"><div class="spk-wrap">'
        + _head(d["eyebrow"], d["headline"], d["lede"])
        + f'<div class="spk-paths">{items}</div>'
        f'<p class="mcp-note">{dora}</p></div></section>'
    )


def _free(d: dict) -> str:
    """The free-three-ways strip: one cell per audience, reusing the
    security-strip cell anatomy on a three-column grid."""
    cells = "".join(
        '<div class="mcp-sec-cell">'
        f'<span class="spk-eyebrow">{_esc(it["eyebrow"])}</span>'
        f"<h3>{_esc(it['title'])}</h3><p>{_rich(it['body'])}</p></div>"
        for it in d["cards"]
    )
    return (
        '<section class="spk-band" id="mcp-free"><div class="spk-wrap">'
        + _head(d["eyebrow"], d["headline"])
        + f'<div class="mcp-sec mcp-3col">{cells}</div></div></section>'
    )


def _proof(d: dict, metrics: dict | None) -> str:
    """The timed proof: real measured numbers from verified_metrics.json,
    published with machine, method and date. Skipped when unmeasured."""
    if not metrics or "timed_proof" not in metrics:
        print(
            "build_iso20022_mcp: no timed_proof metrics; skipping proof strip",
            file=sys.stderr,
        )
        return ""
    tp = metrics["timed_proof"]
    cold, warm = tp["cold_seconds"], tp["warm_seconds"]
    lede = (
        f"From a completely empty package cache to a schema-valid pain.001 "
        f"in {cold} seconds, downloads included. We measured it, on "
        f"{tp['date_human']}, instead of promising it."
    )
    cells = _stat_cells(
        [
            (f"{cold}s", "cold cache to validated pain.001"),
            (f"{warm}s", "warm cache, same session"),
            ("1", "call, first try"),
            ("0", "accounts, keys or sign-ups"),
        ]
    )
    foot = f"Method: {tp['method']} Machine: {tp['machine']}."
    return (
        '<section id="mcp-proof"><div class="spk-wrap">'
        + _head(d["eyebrow"], d["headline"], lede)
        + f'<div class="spk-stats">{cells}</div>'
        f'<p class="spk-stats-foot">{_rich(foot)}</p>'
        "</div></section>"
    )


def _prompts(d: dict, data: dict | None) -> str:
    """Board-pasteable prompts, each backed by a committed transcript
    captured over stdio JSON-RPC. The excerpt is rendered verbatim from
    the capture file; nothing here is written by hand at build time."""
    if not data or not data.get("prompts"):
        print(
            "build_iso20022_mcp: no hub transcripts; skipping prompts section",
            file=sys.stderr,
        )
        return ""
    captured = data.get("_meta", {}).get("captured", "")
    blocks = []
    for p in data["prompts"]:
        pid = p["id"]
        meta = f"{p['server']} · tool: {p['tool']} · stdio JSON-RPC · captured {captured}"
        blocks.append(
            '<article class="mcp-prompt">'
            f'<span class="spk-eyebrow">{_esc(p["eyebrow"])}</span>'
            f"<h3>{_esc(p['title'])}</h3>"
            f'<p class="mcp-prompt-meta">{_esc(meta)}</p>'
            '<p class="mcp-prompt-label">The prompt</p>'
            + _code_block(p["prompt"], f"mcp-prompt-{pid}", copy=True)
            + '<p class="mcp-prompt-label">What came back</p>'
            + _code_block(p["excerpt"])
            + f'<p class="mcp-prompt-note">{_rich(p["note"])}</p>'
            "</article>"
        )
    return (
        '<section id="mcp-prompts"><div class="spk-wrap">'
        + _head(d["eyebrow"], d["headline"], d["lede"])
        + f'<div class="mcp-prompts">{"".join(blocks)}</div>'
        '<p class="mcp-clients-foot">Excerpts are drawn from the committed '
        "capture file; elisions are marked with an ellipsis and nothing is "
        "reworded.</p></div></section>"
    )


def _sandbox(d: dict) -> str:
    """The zero-real-data card: names the three sandbox tools exactly as
    captured in _data/mcp/reconcile-mcp.tools.json and points at the docs
    reconciliation chapter."""
    body = (
        _mono("reconcile-mcp")
        + " ships deterministic sandbox fixtures: "
        + _mono("list_sandbox_scenarios")
        + " shows the scenarios, "
        + _mono("load_sandbox_scenario")
        + " opens one for inspection and "
        + _mono("run_sandbox_scenario")
        + " reconciles it in one call. Watch a full, explainable "
        "reconciliation, exact matches, short payments, splits and "
        "unmatched residuals, before any real statement touches the tools."
    )
    return (
        '<section id="mcp-sandbox"><div class="spk-wrap">'
        + _head(d["eyebrow"], d["headline"])
        + f'<p class="mcp-note">{body}</p>'
        '<div class="spk-cta-row mcp-start-cta">'
        '<a href="/iso20022-mcp-docs/index.html#chapter-3" '
        'class="spk-btn spk-btn-primary">Open the reconciliation chapter '
        '<span class="spk-arw" aria-hidden="true">&#8594;</span></a>'
        '<a href="/iso20022-mcp-reference/index.html#reconcile" '
        'class="spk-btn spk-btn-ghost">reconcile-mcp tool reference</a>'
        "</div></div></section>"
    )


def _adoption(d: dict, metrics: dict | None) -> str:
    """Adoption signals: pypistats last-30-day downloads for the nine suite
    packages and the live registry listing count, baked as static verified
    figures with their as-of date."""
    if not metrics or "adoption" not in metrics:
        print(
            "build_iso20022_mcp: no adoption metrics; skipping adoption strip",
            file=sys.stderr,
        )
        return ""
    ad = metrics["adoption"]
    total = ad["suite_last_month_total"]
    cells = _stat_cells(
        [
            (f"{total:,}", "downloads, last 30 days"),
            (str(ad["registry_listed"]), "servers on the official registry"),
            ("9", "of them are this suite"),
        ]
    )
    foot = (
        f"Downloads: pypistats.org last-30-day counts for the nine suite "
        f"packages, summed, fetched {ad['date_human']}. Registry: live "
        f"listing count for this account on "
        f"registry.modelcontextprotocol.io, checked "
        f"{ad['registry_checked_human']}. No projections, no all-time "
        f"totals."
    )
    return (
        '<section class="spk-band" id="mcp-adoption"><div class="spk-wrap">'
        + _head(d["eyebrow"], d["headline"])
        + f'<div class="spk-stats mcp-stats-3">{cells}</div>'
        f'<p class="spk-stats-foot">{_rich(foot)}</p>'
        "</div></section>"
    )


def _code_block(code: str, block_id: str = "", copy: bool = False) -> str:
    """A literal code block, plus an optional copy button riding main.js's
    site-wide [data-copy] delegate (no inline JS; CSP-safe)."""
    id_attr = f' id="{block_id}"' if block_id else ""
    btn = ""
    if copy and block_id:
        btn = (
            f'<button type="button" class="ap-cta-mini mcp-copy" '
            f'data-copy="#{block_id}" '
            f'aria-label="Copy to clipboard">Copy</button>'
        )
    return f'<pre class="mcp-code"{id_attr}><code>{_esc(code)}</code></pre>{btn}'


def _clients(d: dict) -> str:
    """The multi-client grid. Local-stdio clients get their documented config
    shape verbatim; remote-first platforms get one honest sentence."""
    cards = [
        '<div class="mcp-client">'
        f"<h3>{_esc(it['name'])}</h3>"
        f'<p class="mcp-client-where">{_esc(it["where"])}</p>'
        + _code_block(it["code"], f"mcp-code-client-{it['slug']}", copy=True)
        + "</div>"
        for it in d["stdio"]
    ]
    remote = []
    for it in d["remote"]:
        code = (
            _code_block(it["code"], f"mcp-code-client-{it['slug']}", copy=True)
            if it.get("code")
            else ""
        )
        remote.append(
            '<div class="mcp-client mcp-client-remote">'
            f"<h3>{_esc(it['name'])}</h3><p>{_rich(it['body'])}</p>{code}</div>"
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
        tid = f"mcp-tab-{t['id']}"
        checked = " checked" if i == 0 else ""
        radios.append(
            f'<input type="radio" name="mcp-install-tab" id="{tid}" class="mcp-tab-in"{checked}>'
        )
        labels.append(f'<label for="{tid}">{_esc(t["label"])}</label>')
        panels.append(
            f'<div class="mcp-tab-panel" id="mcp-panel-{t["id"]}">'
            + _code_block(t["code"], f"mcp-code-{t['id']}", copy=True)
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
        '<details class="qa-item mcp-schema">'
        '<summary class="qa-q"><code class="spk-mono">'
        + _esc(t["name"])
        + '</code><span class="mcp-schema-sum">'
        + _esc(t.get("description", ""))
        + "</span></summary>"
        '<div class="qa-a mcp-schema-body">'
        f"<p>{_esc(t.get('description', ''))}</p>"
        + _schema_props(t.get("inputSchema") or {})
        + "</div></details>"
        for t in tools
    ]
    return (
        '<section id="mcp-schemas"><div class="spk-wrap">'
        + _head(d["eyebrow"], d["headline"], d["lede"])
        + f'<div class="qa-list mcp-schemas">{"".join(blocks)}</div>'
        f'<p class="mcp-schema-note">{_esc(d["note"])}</p>'
        "</div></section>"
    )


def _simulator() -> str:
    """Interactive simulator mount (progressive enhancement, mirroring the
    index-scorecard pattern): an inert <iso20022-simulator> carrying a static
    fallback paragraph, upgraded client-side by /_csp/iso20022-simulator.js.
    Everything the component shows is baked into its data module from real
    MCP stdio transcripts at authoring time (see assets/js/mcp-simulator/);
    it makes no network calls, and postbuild stamps SRI on the module
    script."""
    fallback = (
        "This interactive demo lets you pick a payment sentence and see the "
        "exact MCP tool call an assistant makes, plus the validated ISO "
        "20022 XML the gateway returned, captured live over stdio. Enable "
        "JavaScript to explore the transcripts."
    )
    return (
        '<section id="mcp-simulator-section"><div class="spk-wrap">'
        + _head(
            "SEE IT WORK",
            "From a sentence to a validated message.",
            "Pick a real payment sentence and watch it become an exact MCP "
            "tool call and schema-valid ISO 20022 XML. Every transcript "
            "shown was captured from a live server, not mocked.",
        )
        + '<div id="mcp-simulator-mount">'
        "<iso20022-simulator>"
        f'<p class="mcp-sim-fallback">{_esc(fallback)}</p>'
        "</iso20022-simulator></div>"
        '<script type="module" src="/_csp/iso20022-simulator.js"></script>'
        "</div></section>"
    )


def _render_body(d: dict) -> str:
    metrics = _load_data(METRICS_SRC, "verified-metrics sections")
    transcripts = _load_data(TRANSCRIPTS_SRC, "prompts section")
    sections = [
        _hero(d),
        _read_as(),
        _aud(_cards(d["board"], "mcp-board", bullets=False), "mcp-board"),
        _aud(_cards(d["benefits"], "mcp-benefits", bullets=False), "mcp-benefits"),
        _aud(_simulator(), "mcp-simulator"),
        _aud(
            _imgband(
                "majed-swan-RBEv0VyNi2U",
                "A grid of blue and white cubes with one cube glowing, evoking a validated message among structured blocks.",
            ),
            "mcp-band-1",
        ),
        _aud(_capability(d["capability"]), "mcp-capability"),
        _aud(_cards(d["what"], "mcp-what", bullets=False), "mcp-what"),
        _aud(_cards(d["arc"], "mcp-arc", bullets=True), "mcp-arc"),
        _aud(_flow(d["flow"]), "mcp-flow"),
        _aud(_security(d["security"]), "mcp-security"),
        _aud(_regulators(d["regulators"]), "mcp-regulators"),
        _aud(
            _imgband(
                "ocean-ng-L0xOtAnv94Y",
                "A minimalist wall clock, evoking payment operations measured in seconds.",
                cls="mcp-band-img-tall",
            ),
            "mcp-band-2",
        ),
        _aud(_proof(d["proof"], metrics), "mcp-proof"),
        _aud(_free(d["free"]), "mcp-free"),
        _aud(_clients(d["clients"]), "mcp-clients"),
        _aud(_install_tabs(d["install"]), "mcp-install"),
        _aud(_start(), "mcp-start"),
        _aud(_prompts(d["prompts"], transcripts), "mcp-prompts"),
        _aud(_sandbox(d["sandbox"]), "mcp-sandbox"),
        _aud(_adoption(d["adoption"], metrics), "mcp-adoption"),
        _aud(_schemas(d["schemas"]), "mcp-schemas"),
        _aud(_cards(d["safety"], "mcp-safety", bullets=False), "mcp-safety"),
    ]
    return '<div class="speaking-page iso20022-mcp-page">' + "".join(sections) + "</div>"


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
        '<li><a href="/playlists/index.html">Playlists</a></li>'
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
        raise SystemExit("build_iso20022_mcp: no .ap-lang-item switcher links found in shell")
    return out


# Social-card image only: the on-page hero is now the animated terminal
# (real markup, nothing to fetch), but link previews still need a large
# image, so og:image keeps the verified CDN photo.
HERO_OG_IMAGE = f"{CDN}/modern-corporate-office-with-technological-displays-1920.webp"
# Intrinsic size of the og webp above (checked against the served asset),
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
        + json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
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
        raise SystemExit("build_iso20022_mcp: _fix_metas anchor missing: CollectionPage JSON-LD")

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
