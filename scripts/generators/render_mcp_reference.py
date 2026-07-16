#!/usr/bin/env python3
"""Render the ISO 20022 MCP tool catalog into ``_posts/iso20022-mcp-reference.md``.

The catalog between the ``BEGIN GENERATED: mcp-tool-catalog`` and
``END GENERATED: mcp-tool-catalog`` markers is generated verbatim from the
captured ``tools/list`` snapshots under ``_data/mcp/`` (one JSON per server,
each captured live over MCP stdio JSON-RPC), so the published reference can
never drift from what the servers actually expose.

Regenerate after re-capturing a snapshot:

    python3 scripts/generators/render_mcp_reference.py

Drift check (CI / unit tests, exits 1 when the committed page is stale):

    python3 scripts/generators/render_mcp_reference.py --check

Every tool is rendered Alpha-Vantage style: name, description, and a full
parameter table (name, type, required/optional, description, defaults and
enums) pulled straight from the captured ``inputSchema``. Interactivity is
CSS-only (``<details>``/``<summary>``); no inline styles, no scripts, and no
em dashes are emitted (the odd em dash inside a captured docstring is
normalised to a plain hyphen for house style; the JSON snapshots keep the
verbatim capture).
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "_data" / "mcp"
PAGE = ROOT / "_posts" / "iso20022-mcp-reference.md"

BEGIN = "<!-- BEGIN GENERATED: mcp-tool-catalog. Do not edit by hand. -->"
END = "<!-- END GENERATED: mcp-tool-catalog -->"
REGEN_NOTE = (
    "<!-- Regenerated from _data/mcp/*.json by "
    "scripts/generators/render_mcp_reference.py -->"
)

# Curated presentation per server, in catalog order. Everything below the
# header (tool names, descriptions, parameters) comes from the capture.
SERVERS = [
    {
        "file": "tool_schemas.json",
        "id": "gateway",
        "pkg": "iso20022-mcp",
        "kicker": "iso20022-mcp · THE GATEWAY",
        "headline": "One surface, all families.",
        "role": "Routes search, describe, validate, generate and parse to whichever family server the job needs.",
    },
    {
        "file": "pain001-mcp.tools.json",
        "id": "pain001",
        "pkg": "pain001-mcp",
        "kicker": "pain001-mcp · INITIATE",
        "headline": "Customer credit transfers.",
        "role": "pain.001 initiation: discovery, IBAN/BIC and XSD validation, generation, migration and MT101 conversion.",
    },
    {
        "file": "pacs008-mcp.tools.json",
        "id": "pacs008",
        "pkg": "pacs008-mcp",
        "kicker": "pacs008-mcp · SETTLE",
        "headline": "FI-to-FI transfers, returns, status.",
        "role": "pacs.008 interbank settlement plus pacs.004 returns, pacs.002 status, MT103 conversion and the structured-address toolkit.",
    },
    {
        "file": "camt053-mcp.tools.json",
        "id": "camt053",
        "pkg": "camt053-mcp",
        "kicker": "camt053-mcp · READ STATEMENTS",
        "headline": "Bank-to-customer statements.",
        "role": "camt.053/camt.052 parsing, entry queries, MT94x conversion, reversals and CBPR+ readiness.",
    },
    {
        "file": "reconcile-mcp.tools.json",
        "id": "reconcile",
        "pkg": "reconcile-mcp",
        "kicker": "reconcile-mcp · RECONCILE",
        "headline": "Statements against expected payments.",
        "role": "Explainable matching of observed statement entries against expected payments, with a zero-data sandbox.",
    },
    {
        "file": "camt-exceptions.tools.json",
        "id": "camt-exceptions",
        "pkg": "camt-exceptions",
        "entrypoint": "camt-exceptions-mcp",
        "kicker": "camt-exceptions · RESOLVE",
        "headline": "Cancellation &amp; investigation.",
        "role": "camt.056 payment cancellation and camt.029 resolution of investigation, XSD-checked.",
    },
    {
        "file": "ap2-iso20022.tools.json",
        "id": "ap2",
        "pkg": "ap2-iso20022",
        "entrypoint": "ap2-iso20022-mcp",
        "kicker": "ap2-iso20022 · BRIDGE",
        "headline": "Agent mandate to bank rail.",
        "role": "Normalises AP2/x402 agent mandates, checks guardrails, and emits pain.001/pacs.008-ready records. Never moves money.",
    },
    {
        "file": "acmt001-mcp.tools.json",
        "id": "acmt001",
        "pkg": "acmt001-mcp",
        "kicker": "acmt001-mcp · ACCOUNTS",
        "headline": "Account management.",
        "role": "acmt.001 account opening, maintenance and verification, validated against the bundled schema.",
    },
    {
        "file": "bankstatementparser-mcp.tools.json",
        "id": "bankstatementparser",
        "pkg": "bankstatementparser-mcp",
        "kicker": "bankstatementparser-mcp · PARSE STATEMENTS",
        "headline": "Legacy statements, structured.",
        "role": "Format detection and parsing for camt.053, pain.001, MT940, CSV, OFX and QFX statements.",
    },
]

# Docstring sections that duplicate the parameter table or describe returns;
# the catalog cuts the prose there.
_CUT_AT = re.compile(r"^\s*(Args|Arguments|Returns|Raises|Yields|Examples?)\s*:\s*$")
_RST_ROLE = re.compile(r":(?:func|class|meth|mod|attr|data|obj|exc):`~?([^`]+)`")
_DOUBLE_TICK = re.compile(r"``([^`]+)``")
_EMPH = re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)")


def _strip_em_dashes(text: str) -> str:
    """House style bans em dashes; captured docstrings occasionally carry
    them. Normalise to a plain hyphen without touching the JSON snapshots."""
    return text.replace(" — ", " - ").replace("—", "-")


def _paragraphs(description: str) -> list[str]:
    """Split a captured docstring into display paragraphs, cutting at
    Args:/Returns:-style sections (the parameter table covers those)."""
    lines: list[str] = []
    for line in description.splitlines():
        if _CUT_AT.match(line):
            break
        lines.append(line)
    paras: list[str] = []
    buf: list[str] = []
    for line in lines:
        if line.strip():
            buf.append(line.strip())
        elif buf:
            paras.append(" ".join(buf))
            buf = []
    if buf:
        paras.append(" ".join(buf))
    return paras


def _inline_html(text: str) -> str:
    """Escape captured prose for HTML, then re-apply its lightweight markup
    (``code``, :func:`roles`, *emphasis*) as real tags."""
    out = html.escape(_strip_em_dashes(text), quote=False)
    out = _RST_ROLE.sub(lambda m: f"<code>{m.group(1)}</code>", out)
    out = _DOUBLE_TICK.sub(lambda m: f"<code>{m.group(1)}</code>", out)
    out = _EMPH.sub(lambda m: f"<em>{m.group(1)}</em>", out)
    return out


def _schema_type(prop: dict) -> str:
    """Human-readable type for a JSON Schema property."""
    if "type" in prop:
        t = prop["type"]
        if t == "array":
            items = prop.get("items", {})
            inner = items.get("type")
            return f"array of {inner}" if inner else "array"
        return str(t)
    if "anyOf" in prop:
        parts: list[str] = []
        for alt in prop["anyOf"]:
            alt_t = _schema_type(alt) if isinstance(alt, dict) else "any"
            if alt_t not in parts:
                parts.append(alt_t)
        # "x | null" reads better as "x (nullable)".
        if "null" in parts and len(parts) == 2:
            parts.remove("null")
            return f"{parts[0]}, nullable"
        return " | ".join(parts) if parts else "any"
    return "any"


def _param_notes(prop: dict) -> list[str]:
    notes: list[str] = []
    if "enum" in prop:
        vals = " · ".join(f"<code>{html.escape(str(v))}</code>" for v in prop["enum"])
        notes.append(f"One of: {vals}.")
    if "default" in prop and prop["default"] not in (None, ""):
        notes.append(f"Default: <code>{html.escape(json.dumps(prop['default']))}</code>.")
    return notes


def _render_params(tool: dict, server_id: str) -> list[str]:
    schema = tool.get("inputSchema") or {}
    props: dict = schema.get("properties") or {}
    required = set(schema.get("required") or [])
    if not props:
        return ['<p class="ref-noparams">This tool takes no parameters.</p>']
    out = [
        '<div class="ref-params-wrap">',
        '<table class="ref-params">',
        f'<caption class="visually-hidden">Parameters of {html.escape(tool["name"])}</caption>',
        "<thead>",
        "<tr>",
        '<th scope="col">Parameter</th>',
        '<th scope="col">Type</th>',
        '<th scope="col">Required</th>',
        '<th scope="col">Description</th>',
        "</tr>",
        "</thead>",
        "<tbody>",
    ]
    for name, prop in props.items():
        desc_bits: list[str] = []
        if prop.get("description"):
            desc_bits.append(_inline_html(str(prop["description"])))
        desc_bits.extend(_param_notes(prop))
        req = "Required" if name in required else "Optional"
        out += [
            "<tr>",
            f"<td><code>{html.escape(name)}</code></td>",
            f"<td>{html.escape(_schema_type(prop))}</td>",
            f'<td><span class="ref-req ref-req-{req.lower()}">{req}</span></td>',
            f"<td>{' '.join(desc_bits)}</td>",
            "</tr>",
        ]
    out += ["</tbody>", "</table>", "</div>"]
    return out


def _render_tool(tool: dict, server_id: str) -> list[str]:
    name = html.escape(tool["name"])
    paras = _paragraphs(tool.get("description") or "")
    brief = _inline_html(paras[0]) if paras else ""
    schema = tool.get("inputSchema") or {}
    n_params = len(schema.get("properties") or {})
    n_req = len(schema.get("required") or [])
    if n_params == 0:
        meta = "No parameters"
    else:
        meta = f"{n_params} parameter{'s' if n_params != 1 else ''} · {n_req} required"
    out = [
        f'<details class="ref-tool" id="{server_id}-{name}">',
        "<summary>",
        f'<span class="ref-tool-name"><code>{name}</code></span>',
        f'<span class="ref-tool-brief">{brief}</span>',
        f'<span class="ref-tool-meta">{meta}</span>',
        "</summary>",
        '<div class="ref-tool-body">',
    ]
    for para in paras[1:]:
        out.append(f'<p class="ref-tool-desc">{_inline_html(para)}</p>')
    out += _render_params(tool, server_id)
    out += ["</div>", "</details>"]
    return out


def _render_index(loaded: list[tuple[dict, dict]]) -> list[str]:
    out = [
        '<nav class="ref-index" aria-label="Servers in this reference">',
        '<ol class="ref-index-list">',
    ]
    for meta, doc in loaded:
        n = len(doc["tools"])
        version = doc["_meta"]["server"].get("version", "")
        out += [
            '<li class="ref-index-item">',
            f'<a class="ref-index-link" href="#{meta["id"]}">',
            f'<span class="ref-index-name"><code>{meta["pkg"]}</code></span>',
            f'<span class="ref-index-role">{meta["role"]}</span>',
            f'<span class="ref-index-count">{n} tools · v{html.escape(version)}</span>',
            "</a>",
            "</li>",
        ]
    out += ["</ol>", "</nav>"]
    return out


def _render_server(meta: dict, doc: dict) -> list[str]:
    tools = doc["tools"]
    cap = doc["_meta"]
    version = cap["server"].get("version", "")
    captured = cap.get("captured", "")
    command = _strip_em_dashes(cap.get("command", ""))
    out = [
        f'<section class="newsroom ref-server" id="{meta["id"]}">',
        '<header class="cat-section-head">',
        f'<p class="cat-kicker">{meta["kicker"]}</p>',
        f'<h2 class="cat-headline">{meta["headline"]}</h2>',
        f'<p class="cat-lede">{meta["role"]}</p>',
        "</header>",
        f'<p class="ref-capture">{len(tools)} tools · v{html.escape(version)} · '
        f"captured live over MCP stdio on {html.escape(captured)} with "
        f"<code>{html.escape(command)}</code></p>",
        '<div class="ref-tools">',
    ]
    for tool in tools:
        out += _render_tool(tool, meta["id"])
    out += ["</div>", "</section>"]
    return out


def render_catalog() -> str:
    """The full generated block, marker line to marker line inclusive."""
    loaded: list[tuple[dict, dict]] = []
    expected = {m["file"] for m in SERVERS}
    on_disk = {
        p.name for p in DATA.glob("*.json") if p.name.endswith((".tools.json",))
    } | {"tool_schemas.json"}
    extra = sorted(on_disk - expected)
    if extra:
        raise SystemExit(
            f"render_mcp_reference: captured snapshots not in the catalog: {extra} "
            "(add them to SERVERS so the reference stays complete)"
        )
    for meta in SERVERS:
        path = DATA / meta["file"]
        if not path.is_file():
            raise SystemExit(f"render_mcp_reference: missing capture {path}")
        doc = json.loads(path.read_text(encoding="utf-8"))
        if not doc.get("tools"):
            raise SystemExit(f"render_mcp_reference: no tools in {path}")
        loaded.append((meta, doc))
    total = sum(len(doc["tools"]) for _, doc in loaded)
    lines: list[str] = [BEGIN, REGEN_NOTE]
    lines.append(
        f'<p class="ref-totals">{len(loaded)} servers · {total} tools. '
        "Every entry below is generated from a live <code>tools/list</code> "
        "capture over MCP stdio; nothing is hand-written.</p>"
    )
    lines += _render_index(loaded)
    for meta, doc in loaded:
        lines.append("")
        lines += _render_server(meta, doc)
    lines.append("")
    lines.append(END)
    out = "\n".join(lines)
    if "—" in out:
        raise SystemExit("render_mcp_reference: em dash escaped into output")
    return out


def apply(page_text: str) -> str:
    """Replace the generated block inside the page, markers included."""
    try:
        head, rest = page_text.split(BEGIN, 1)
        _, tail = rest.split(END, 1)
    except ValueError:
        raise SystemExit(
            f"render_mcp_reference: markers not found in {PAGE} "
            f"(need both {BEGIN!r} and {END!r})"
        )
    return head + render_catalog() + tail


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    check = "--check" in args
    current = PAGE.read_text(encoding="utf-8")
    updated = apply(current)
    if check:
        if updated != current:
            print(
                f"DRIFT: {PAGE.relative_to(ROOT)} is stale; run "
                "python3 scripts/generators/render_mcp_reference.py",
                file=sys.stderr,
            )
            return 1
        print("render_mcp_reference: catalog is in sync")
        return 0
    if updated == current:
        print("render_mcp_reference: no changes")
        return 0
    PAGE.write_text(updated, encoding="utf-8")
    print(f"render_mcp_reference: wrote {PAGE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
