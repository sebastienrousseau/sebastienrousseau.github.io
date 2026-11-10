#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Generate ``/tools/``: free browser tools, presented like a product (G-4).

Three tools run entirely in the reader's browser, from same-origin ES
modules in ``assets/js/tools/`` (copied to ``public/_csp/tools/`` by
build.sh and tested by ``tests/unit/tools/tools.test.mjs``):

* the structured-address checker (CBPR+ structured-address rules),
* the ISO 20022 message identifier,
* the PQC sizing calculator (FIPS 203 and FIPS 204 sizes).

A card links the ISO 20022 MCP suite. Each tool carries
``SoftwareApplication`` JSON-LD (free, operating system "Web"). English
only, same shell and slot as ``build_trust.py``.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
from build_case_studies import _swap_into_shell

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
SHELL_SRC = PUBLIC / "articles" / "index.html"
BASE = "https://sebastienrousseau.com"
URL = f"{BASE}/tools/"
TITLE = "Free ISO 20022 and PQC tools | Sebastien Rousseau"
DESC = (
    "Free browser tools for payments teams: check structured addresses, identify ISO 20022 "
    "messages and size post-quantum keys. Nothing you paste leaves the page."
)
ADDRESS_ARTICLE = "/2026-05-12-iso-20022-pacs008-structured-address-deadline/index.html"
BOE_DELAY = "https://www.bankofengland.co.uk/news/2026/august/delay-to-the-november-2026-rtgs-standards-release"
_ALT_RE = re.compile(r'[ \t]*<link\s+rel="alternate"\s+hreflang="[^"]*"\s+href="[^"]*"\s*/?>\n?')

TOOLS = (
    ("tool-address", "Structured-address checker",
     "Paste a pacs.008 or pain.001 party element and see whether its postal address meets the "
     "CBPR+ structured-address rules: structured, hybrid or unstructured, and why."),
    ("tool-message", "ISO 20022 message identifier",
     "Paste any ISO 20022 XML and get the message, version and business area from its namespaces."),
    ("tool-pqc", "PQC sizing calculator",
     "Compare ML-KEM and ML-DSA key, ciphertext and signature sizes with RSA, ECDSA and X25519, "
     "and estimate the extra bytes per message and per day."),
)  # fmt: skip


def _form(form_id: str, inner: str, button: str) -> str:
    return (
        f'<form id="{form_id}" class="tool-form" novalidate>{inner}'
        f'<p><button class="pill no-chev" type="submit">{button}</button></p>'
        f'<output aria-live="polite" for="{form_id}"></output></form>'
    )


def _textarea(form_id: str, label: str, placeholder: str) -> str:
    return (
        f'<label for="{form_id}-xml">{label}</label>'
        f'<textarea id="{form_id}-xml" name="xml" rows="8" spellcheck="false" '
        f'placeholder="{placeholder}"></textarea>'
    )


def _select(sel_id: str, name: str, label: str) -> str:
    return f'<p><label for="{sel_id}">{label}</label> <select id="{sel_id}" name="{name}"></select></p>'


def tool_sections() -> str:
    address = _form(
        "tool-address",
        _textarea("tool-address", "XML fragment", "<Cdtr><Nm>…</Nm><PstlAdr>…</PstlAdr></Cdtr>"),
        "Check the address",
    ) + (
        f'<p class="tool-note">Rules: Town name and Country required, at most two address lines in hybrid '
        f'form, no address held in free-text lines alone (<a href="{ADDRESS_ARTICLE}">the structured-address '
        "requirements</a>). Swift planned to stop accepting unstructured addresses in November 2026 and "
        f'delayed that release on 27 August 2026 (<a href="{BOE_DELAY}" rel="external noopener">Bank of '
        "England</a>).</p>"
    )
    message = _form(
        "tool-message",
        _textarea("tool-message", "ISO 20022 XML", '<Document xmlns="urn:iso:std:iso:20022:…">'),
        "Identify",
    )
    pqc = _form(
        "tool-pqc",
        _select("pqc-from", "from", "Signature today")
        + _select("pqc-to", "to", "Signature after migration")
        + '<p><label for="pqc-volume">Signed messages per day</label> '
        '<input id="pqc-volume" name="volume" type="number" min="0" step="1" value="100000" /></p>'
        + _select("kem-from", "kemFrom", "Key exchange today")
        + _select("kem-to", "kemTo", "Key exchange after migration"),
        "Calculate",
    ) + (
        '<p class="tool-note">Sizes in bytes from NIST FIPS 203 (ML-KEM, Table 3) and FIPS 204 '
        "(ML-DSA, Table 2); RSA and ECDSA P-256 shown as raw public keys and signatures.</p>"
    )
    bodies = {"tool-address": address, "tool-message": message, "tool-pqc": pqc}
    return "".join(
        f'<section class="narrative-section" aria-labelledby="{tid}-h"><div class="narrative-wrap"><div>'
        f'<h2 id="{tid}-h" class="narrative-head">{name}</h2><p>{lede}</p>{bodies[tid]}</div></div></section>'
        for tid, name, lede in TOOLS
    )


def render_body() -> str:
    return (
        '<div class="tools-page">'
        '<section class="story-cta" aria-labelledby="tools-h1"><header class="story-head">'
        '<p class="story-eyebrow">Free tools</p>'
        '<h1 id="tools-h1" class="story-title">Tools for ISO 20022 and post-quantum migration.</h1>'
        "<p>Each tool runs in your browser. Nothing you paste is sent anywhere: there is no "
        "server behind these forms.</p></header></section>"
        + tool_sections()
        + '<section class="narrative-section alt" aria-labelledby="tools-mcp"><div class="narrative-wrap"><div>'
        '<h2 id="tools-mcp" class="narrative-head">ISO 20022 MCP suite</h2>'
        "<p>Nine open, vendor-neutral servers that let AI agents generate, validate, reconcile "
        'and settle bank payments from plain language. <a class="offer-link" '
        'href="/iso20022-mcp/index.html">Install the suite</a></p>'
        "</div></div></section>"
        '<script type="module" src="/_csp/tools/tools.js"></script>' + jsonld() + "</div>"
    )


def jsonld() -> str:
    graph = [
        {
            "@type": "SoftwareApplication",
            "@id": f"{URL}#{tid}",
            "name": name,
            "description": lede,
            "applicationCategory": "DeveloperApplication",
            "operatingSystem": "Web",
            "url": f"{URL}#{tid}-h",
            "offers": {"@type": "Offer", "price": 0, "priceCurrency": "GBP"},
            "author": {"@id": f"{BASE}/#person"},
        }
        for tid, name, lede in TOOLS
    ]
    payload = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    return f'<script type="application/ld+json">{payload}</script>'


def main() -> int:
    if not SHELL_SRC.is_file():
        print(f"build_tools: shell missing at {SHELL_SRC}", file=sys.stderr)
        return 1
    out = _ALT_RE.sub(
        "", _swap_into_shell(SHELL_SRC.read_text(encoding="utf-8"), render_body(), TITLE, DESC, URL)
    )
    target = PUBLIC / "tools" / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(out, encoding="utf-8")
    print(f"build_tools: wrote {target.relative_to(ROOT)} ({len(TOOLS)} tools)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
