#!/usr/bin/env python3
"""Per-PR JSON-LD diff.

Walks two build outputs (base, head), extracts every
``<script type="application/ld+json">`` block from every HTML page, and
prints a Markdown report summarising added / removed / changed schemas
per page. Designed to run inside a GitHub Action that posts the output
as a PR comment so reviewers see structured-data drift without opening
the diff.

Usage:
    python3 scripts/jsonld_diff.py BASE_DIR HEAD_DIR [--max-pages N]

Exit status:
    0 — always (informational; never fails the build).
"""

from __future__ import annotations

import sys as _sys  # path bootstrap — scripts reorg (scripts/lib/ on sys.path)
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "lib"))

import argparse
import json
import re
import sys
from pathlib import Path

_JSONLD_RE = re.compile(
    r'<script type="application/ld\+json">\s*([\s\S]*?)\s*</script>',
    re.IGNORECASE,
)
_COMMENT_RE = re.compile(r"<!--[\s\S]*?-->")


def extract_blocks(path: Path) -> list[object]:
    """Return parsed JSON-LD blocks from an HTML file. Bad JSON is
    skipped (the validator catches those). Each block is a dict or list
    matching the schema graph."""
    html = path.read_text(encoding="utf-8", errors="ignore")
    html = _COMMENT_RE.sub("", html)
    out: list[object] = []
    for raw in _JSONLD_RE.findall(html):
        try:
            out.append(json.loads(raw.strip()))
        except json.JSONDecodeError:
            continue
    return out


def index(root: Path) -> dict[str, list[object]]:
    """Build a relative-path -> JSON-LD block list map over root."""
    out: dict[str, list[object]] = {}
    if not root.is_dir():
        return out
    for p in root.rglob("*.html"):
        rel = str(p.relative_to(root))
        out[rel] = extract_blocks(p)
    return out


def summarise_block(block: object) -> str:
    """Render a one-line summary of a JSON-LD block (or list of blocks).
    For @graph blocks, list each node's @type. Otherwise list @type."""
    if isinstance(block, dict):
        graph = block.get("@graph")
        if isinstance(graph, list):
            types = [str(n.get("@type", "?")) for n in graph if isinstance(n, dict)]
            return f"@graph[{', '.join(types)}]"
        return f"@type:{block.get('@type', '?')}"
    if isinstance(block, list):
        return f"list[{len(block)} blocks]"
    return "?"


def diff_pages(base: dict[str, list[object]], head: dict[str, list[object]]) -> str:
    base_keys = set(base.keys())
    head_keys = set(head.keys())
    added = sorted(head_keys - base_keys)
    removed = sorted(base_keys - head_keys)
    changed: list[str] = [k for k in sorted(base_keys & head_keys) if base[k] != head[k]]

    if not (added or removed or changed):
        return "✅ **No structured-data changes** vs. base.\n"

    lines = ["## Structured-data diff vs. base\n"]
    if added:
        lines.append(f"### ➕ {len(added)} page(s) added\n")
        for k in added[:25]:
            sig = ", ".join(summarise_block(b) for b in head[k]) or "(empty)"
            lines.append(f"- `{k}` — {sig}")
        if len(added) > 25:
            lines.append(f"- … and {len(added) - 25} more")
        lines.append("")
    if removed:
        lines.append(f"### ➖ {len(removed)} page(s) removed\n")
        lines.extend(f"- `{k}`" for k in removed[:25])
        if len(removed) > 25:
            lines.append(f"- … and {len(removed) - 25} more")
        lines.append("")
    if changed:
        lines.append(f"### 🔁 {len(changed)} page(s) with schema changes\n")
        for k in changed[:25]:
            base_sig = ", ".join(summarise_block(b) for b in base[k]) or "(empty)"
            head_sig = ", ".join(summarise_block(b) for b in head[k]) or "(empty)"
            if base_sig == head_sig:
                # Same shape, different content — count BlogPosting prop deltas.
                lines.append(f"- `{k}` — content changed ({base_sig})")
            else:
                lines.append(f"- `{k}`\n  - was: {base_sig}\n  - now: {head_sig}")
        if len(changed) > 25:
            lines.append(f"- … and {len(changed) - 25} more")
        lines.append("")

    lines.append(f"_Compared {len(base_keys)} base pages against {len(head_keys)} head pages._")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("base", type=Path, help="Path to base-build directory")
    ap.add_argument("head", type=Path, help="Path to head-build directory")
    args = ap.parse_args()

    base = index(args.base)
    head = index(args.head)
    sys.stdout.write(diff_pages(base, head))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
