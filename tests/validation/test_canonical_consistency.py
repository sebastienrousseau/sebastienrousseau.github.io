#!/usr/bin/env python3
"""Gate: one canonical URL form per page.

A page used to advertise three different URLs for itself: ``<link
rel="canonical">`` = ".../slug/index.html", ``og:url`` = ".../slug" (no
slash), and the sitemap ``<loc>`` = ".../slug/". Search engines read all
three as canonicalisation signals, so the disagreement is a defect.
``postbuild_lib.seo.normalize_canonical`` collapses canonical + og:url
onto the trailing-slash form the sitemap uses. This gate asserts they
agree, and match the page's own path.

Run from repo root:
``python3 tests/validation/test_canonical_consistency.py``.
Exits non-zero on the first page whose canonical / og:url disagree.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
BASE = "https://sebastienrousseau.com"

_CANONICAL_RE = re.compile(
    r'<link\b[^>]*\brel=["\']?canonical["\']?[^>]*>', re.IGNORECASE
)
_OGURL_RE = re.compile(
    r'<meta\b[^>]*\bproperty=["\']?og:url["\']?[^>]*>', re.IGNORECASE
)
_HREF_RE = re.compile(r'href=["\']?([^"\'\s>]+)', re.IGNORECASE)
_CONTENT_RE = re.compile(r'content=["\']?([^"\'\s>]+)', re.IGNORECASE)
# Redirect pages (legacy URLs converted by postbuild_lib.redirects, e.g.
# /papers/ -> /research/) carry an instant meta refresh and canonicalise to
# their TARGET, not to themselves — that is the whole point of the page.
_META_REFRESH_RE = re.compile(
    r'<meta\s+http-equiv=["\']?refresh["\']?[^>]*content=["\']?\s*0;\s*url=([^"\'>\s]+)',
    re.IGNORECASE,
)


def _expected(page: Path) -> str:
    rel = page.relative_to(PUBLIC)
    if rel.name != "index.html":
        return f"{BASE}/{rel.as_posix()}"
    parent = rel.parent.as_posix()
    return f"{BASE}/" if parent in ("", ".") else f"{BASE}/{parent}/"


def main() -> int:
    if not PUBLIC.is_dir():
        print("error: public/ not built — run ./build.sh first", file=sys.stderr)
        return 1

    bad: list[str] = []
    scanned = 0
    for page in PUBLIC.rglob("index.html"):
        html = page.read_text(encoding="utf-8", errors="ignore")
        cm = _CANONICAL_RE.search(html)
        if not cm:
            continue  # pages without a canonical (e.g. error pages) are exempt
        scanned += 1
        canon_m = _HREF_RE.search(cm.group(0))
        canon = canon_m.group(1) if canon_m else ""
        expected = _expected(page)
        rel = str(page.relative_to(PUBLIC))
        refresh_m = _META_REFRESH_RE.search(html)
        if refresh_m:
            # Redirect page: canonical must agree with the refresh target
            # (self-canonical would contradict the redirect).
            target = refresh_m.group(1)
            if canon != target:
                bad.append(
                    f"{rel}: redirect page canonical={canon!r} != refresh target={target!r}"
                )
            continue
        if canon != expected:
            bad.append(f"{rel}: canonical={canon!r} expected={expected!r}")
            continue
        om = _OGURL_RE.search(html)
        if om:
            og_m = _CONTENT_RE.search(om.group(0))
            og = og_m.group(1) if og_m else ""
            if og != expected:
                bad.append(f"{rel}: og:url={og!r} != canonical={expected!r}")

    if bad:
        print("canonical / og:url inconsistencies:", file=sys.stderr)
        for line in bad[:30]:
            print(f"  {line}", file=sys.stderr)
        if len(bad) > 30:
            print(f"  …and {len(bad) - 30} more", file=sys.stderr)
        return 1

    print(f"ok: canonical / og:url consistent — {scanned} pages checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
