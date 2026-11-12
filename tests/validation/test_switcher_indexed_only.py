#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Gate: indexed pages do not link to noindexed locales (D-3, option b).

On every page search engines may index, the language menu lists only the
locales in ``_data/seo/locale-indexing.json`` and ends with "More
languages" (``postbuild_lib.lang_switcher_scope``). The one indexed page
allowed to link every locale is ``/languages/``. Noindexed pages keep the
full menu. Checks the built ``public/`` tree.

Run from repo root: ``python3 tests/validation/test_switcher_indexed_only.py``.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
import _lang_registry as _lr
import _locale_indexing as _li

_ROBOTS_RE = re.compile(r'<meta\s+name="robots"\s+content="([^"]*)"', re.I)
_LANG_ITEM_RE = re.compile(r'<a class="ap-lang-item[^"]*"[^>]*\bdata-lang="([^"]+)"')
ALLOWED = {"languages/index.html"}


def page_defects(html: str, noindexed: frozenset[str]) -> list[str]:
    """Problems with one indexed page's language menu."""
    if "ap-lang-menu-grid" not in html:
        return []
    langs = _LANG_ITEM_RE.findall(html)
    out = [f"links noindexed locale {code}" for code in langs if code in noindexed]
    if "more" not in langs:
        out.append('no "More languages" item')
    return out


def is_indexed_page(html: str) -> bool:
    m = _ROBOTS_RE.search(html)
    return not (m and "noindex" in m.group(1).lower())


def main() -> int:
    if not PUBLIC.is_dir():
        print("switcher-indexed-only: public/ missing, run ./build.sh", file=sys.stderr)
        return 1
    noindexed = frozenset(_li.noindex_codes())
    active = {lang.code for lang in _lr.active()}
    bad: list[str] = []
    checked = 0
    for page in sorted(PUBLIC.rglob("index.html")):
        rel = page.relative_to(PUBLIC).as_posix()
        if rel.split("/", 1)[0] in noindexed or rel in ALLOWED:
            continue
        html = page.read_text(encoding="utf-8", errors="ignore")
        if not is_indexed_page(html):
            continue
        checked += 1
        bad += [f"{rel}: {d}" for d in page_defects(html, noindexed)]
    if bad:
        print(
            f"switcher-indexed-only: {len(bad)} problem(s) on {checked} indexed pages",
            file=sys.stderr,
        )
        for line in bad[:20]:
            print(f"  {line}", file=sys.stderr)
        return 1
    print(
        f"ok: {checked} indexed pages link only to the {len(active) - len(noindexed)} indexed locales"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
