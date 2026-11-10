#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Gate: indexable pages have titles and descriptions search can show whole.

Plan F-2. For every indexable page in ``public/`` (no ``noindex``):

* ``<title>``: 30-60 characters in Latin and other alphabetic scripts,
  12-30 in Chinese and Japanese, 12-35 in Korean;
* ``meta[name=description]``: 120-160 characters (Latin), 50-80 (Chinese,
  Japanese), 60-100 (Korean), and unique across indexable pages.

Prints the 20 worst offenders. ``--strict`` fails the build on any; without
it the gate reports and passes.

Run from repo root: ``python3 tests/validation/test_title_description_lengths.py [--strict]``.
"""

from __future__ import annotations

import html
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
_ROBOTS_RE = re.compile(r'<meta\s+name="robots"\s+content="([^"]*)"', re.I)
_TITLE_RE = re.compile(r"<title>([\s\S]*?)</title>", re.I)
_DESC_RE = re.compile(r'<meta\s+name="description"\s+content="([^"]*)"', re.I)
_LANG_RE = re.compile(r'<html[^>]*\blang="([^"]+)"', re.I)
_REDIRECT_RE = re.compile(r'http-equiv="refresh"', re.I)


def limits(lang: str) -> tuple[tuple[int, int], tuple[int, int]]:
    """((title min, max), (description min, max)) for a BCP-47 tag."""
    primary = lang.lower().split("-")[0]
    if primary in ("zh", "ja"):
        return (12, 30), (50, 80)
    if primary == "ko":
        return (12, 35), (60, 100)
    return (30, 60), (120, 160)


def page_problems(page_html: str) -> tuple[list[tuple[int, str]], str]:
    """([(distance outside the range, message)], description)."""
    lang_m = _LANG_RE.search(page_html)
    (t_lo, t_hi), (d_lo, d_hi) = limits(lang_m.group(1) if lang_m else "en")
    title_m, desc_m = _TITLE_RE.search(page_html), _DESC_RE.search(page_html)
    title = html.unescape(title_m.group(1).strip()) if title_m else ""
    desc = html.unescape(desc_m.group(1).strip()) if desc_m else ""
    out: list[tuple[int, str]] = []
    for name, value, lo, hi in (("title", title, t_lo, t_hi), ("description", desc, d_lo, d_hi)):
        n = len(value)
        if not lo <= n <= hi:
            out.append((max(lo - n, n - hi), f"{name} {n} chars (want {lo}-{hi})"))
    return out, desc


def is_indexable(page_html: str) -> bool:
    m = _ROBOTS_RE.search(page_html)
    return not (m and "noindex" in m.group(1).lower()) and not _REDIRECT_RE.search(page_html)


def main(argv: list[str]) -> int:
    strict = "--strict" in argv
    if not PUBLIC.is_dir():
        print("title-description-lengths: public/ missing, run ./build.sh", file=sys.stderr)
        return 1
    problems: list[tuple[int, str]] = []
    by_desc: dict[str, list[str]] = defaultdict(list)
    checked = 0
    for page in sorted(PUBLIC.rglob("index.html")):
        text = page.read_text(encoding="utf-8", errors="ignore")
        if not is_indexable(text):
            continue
        checked += 1
        rel = page.relative_to(PUBLIC).as_posix()
        found, desc = page_problems(text)
        problems += [(d, f"{rel}: {msg}") for d, msg in found]
        if desc:
            by_desc[desc].append(rel)
    dupes = [
        (len(v), f"{v[0]}: description shared by {len(v)} pages")
        for v in by_desc.values()
        if len(v) > 1
    ]
    problems += dupes
    if not problems:
        print(f"ok: titles and descriptions within limits on {checked} indexable pages")
        return 0
    label = "error" if strict else "warning"
    print(
        f"title-description-lengths {label}: {len(problems)} problem(s) on {checked} pages; worst 20:"
    )
    for _, line in sorted(problems, reverse=True)[:20]:
        print(f"  {line}")
    return 1 if strict else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
