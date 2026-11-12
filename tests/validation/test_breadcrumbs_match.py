#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Gate: a visible breadcrumb has a BreadcrumbList that says the same.

Plan F-3. On every built page with ``nav[aria-label=Breadcrumb]``, the
JSON-LD ``BreadcrumbList`` must exist and list the same crumbs, in order,
with the same names (whitespace and entities normalised). Search engines
show the structured crumbs; a mismatch shows readers a path the page does
not have.

Run from repo root: ``python3 tests/validation/test_breadcrumbs_match.py``.
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
_NAV_RE = re.compile(r'<nav[^>]*aria-label="Breadcrumb"[^>]*>(.*?)</nav>', re.S | re.I)
_CRUMB_RE = re.compile(r"<li[^>]*>(.*?)</li>", re.S)
_INLINE_CRUMB_RE = re.compile(r"<(?:a|span)\b[^>]*>(.*?)</(?:a|span)>", re.S)
_TAG_RE = re.compile(r"<[^>]+>")
_LD_RE = re.compile(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', re.S | re.I)


def _norm(text: str) -> str:
    return " ".join(html.unescape(_TAG_RE.sub("", text)).split())


def visible_crumbs(page_html: str) -> list[str] | None:
    nav = _NAV_RE.search(page_html)
    if not nav:
        return None
    crumbs = _CRUMB_RE.findall(nav.group(1)) or _INLINE_CRUMB_RE.findall(nav.group(1))
    return [_norm(c) for c in crumbs]


def _walk(node: object) -> list[dict]:
    if isinstance(node, dict):
        return [node, *(n for v in node.values() for n in _walk(v))]
    if isinstance(node, list):
        return [n for v in node for n in _walk(v)]
    return []


def schema_crumbs(page_html: str) -> list[str] | None:
    for block in _LD_RE.findall(page_html):
        try:
            data = json.loads(block)
        except json.JSONDecodeError:
            continue
        for node in _walk(data):
            if node.get("@type") == "BreadcrumbList":
                items = sorted(node.get("itemListElement", []), key=lambda i: i.get("position", 0))
                return [_norm(str(i.get("name", ""))) for i in items]
    return None


def page_problem(page_html: str) -> str | None:
    shown = visible_crumbs(page_html)
    if shown is None:
        return None
    marked = schema_crumbs(page_html)
    if marked is None:
        return "visible breadcrumb but no BreadcrumbList"
    if marked != shown:
        return f"BreadcrumbList {marked} differs from the visible {shown}"
    return None


def main() -> int:
    if not PUBLIC.is_dir():
        print("breadcrumbs: public/ missing, run ./build.sh", file=sys.stderr)
        return 1
    bad, checked = [], 0
    for page in sorted(PUBLIC.rglob("index.html")):
        text = page.read_text(encoding="utf-8", errors="ignore")
        problem = page_problem(text)
        checked += visible_crumbs(text) is not None
        if problem:
            bad.append(f"{page.relative_to(PUBLIC).as_posix()}: {problem}")
    if bad:
        print(f"breadcrumbs: {len(bad)} page(s) out of step", file=sys.stderr)
        for line in bad[:20]:
            print(f"  {line}", file=sys.stderr)
        return 1
    print(f"ok: {checked} visible breadcrumbs match their BreadcrumbList")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
