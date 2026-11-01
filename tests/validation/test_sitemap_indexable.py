#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Gate: every sitemap URL is an indexable page, and error pages are noindex.

``test_sitemap_completeness`` checks the other direction (every page is
listed). This one checks that nothing listed should be absent: a ``<loc>``
must render in ``public/``, must not be a meta-refresh redirect page, must
not carry ``noindex``, and must canonicalise to itself. It also asserts that
every ``/404/`` page, EN and locale, carries ``noindex`` so a crawler that
reaches one through a 200 response does not file it as a Soft 404.

Run from repo root: ``python3 tests/validation/test_sitemap_indexable.py``.
Exits non-zero listing the first offenders.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
SITE = "https://sebastienrousseau.com"

_LOC_RE = re.compile(r"<loc>([^<]+)</loc>")
_NOINDEX_RE = re.compile(r'<meta\s+name=["\']robots["\']\s+content=["\'][^"\']*noindex', re.I)
_REFRESH_RE = re.compile(r'<meta\s+http-equiv=["\']?refresh', re.I)
_CANONICAL_RE = re.compile(
    r'<link\b[^>]*\brel=["\']?canonical["\']?[^>]*\bhref=["\']?([^"\'\s>]+)', re.I
)


def _norm(url: str) -> str:
    url = unquote(url.strip()).removesuffix("index.html")
    return url.rstrip("/")


def _head(page: Path) -> str:
    with page.open("r", encoding="utf-8", errors="ignore") as fh:
        return fh.read(65536)


def loc_problem(loc: str) -> str | None:
    """Return why ``loc`` does not belong in a sitemap, or None."""
    if not loc.startswith(SITE):
        return "off-site"
    rel = unquote(loc[len(SITE) :]).lstrip("/")
    page = PUBLIC / (rel + "index.html" if rel == "" or rel.endswith("/") else rel)
    if not page.is_file():
        return "not rendered"
    if page.suffix != ".html":
        return None
    head = _head(page)
    if _REFRESH_RE.search(head):
        return "redirect page"
    if _NOINDEX_RE.search(head):
        return "noindex"
    m = _CANONICAL_RE.search(head)
    if m and _norm(m.group(1)) != _norm(loc):
        return f"canonical is {m.group(1)}"
    return None


def main() -> int:
    if not PUBLIC.is_dir():
        print("error: public/ not built, run ./build.sh first", file=sys.stderr)
        return 1
    sitemaps = sorted(PUBLIC.glob("*sitemap*.xml")) + sorted(PUBLIC.glob("*/news-sitemap.xml"))
    bad: list[str] = []
    checked = 0
    for sm in sitemaps:
        for loc in _LOC_RE.findall(sm.read_text(encoding="utf-8", errors="ignore")):
            checked += 1
            why = loc_problem(loc)
            if why:
                bad.append(f"{sm.relative_to(PUBLIC)}: {loc.strip()} ({why})")
    error_pages = [PUBLIC / "404" / "index.html", *PUBLIC.glob("*/404/index.html")]
    bad.extend(
        f"{page.relative_to(PUBLIC)}: error page without noindex"
        for page in error_pages
        if page.is_file() and not _NOINDEX_RE.search(_head(page))
    )
    if bad:
        print(f"FAIL: {len(bad)} sitemap/indexability problem(s):", file=sys.stderr)
        for line in bad[:40]:
            print(f"  {line}", file=sys.stderr)
        return 1
    print(f"OK: {checked} sitemap URL(s) across {len(sitemaps)} sitemap(s) are indexable")
    return 0


if __name__ == "__main__":
    sys.exit(main())
