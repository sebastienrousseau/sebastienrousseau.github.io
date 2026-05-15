#!/usr/bin/env python3
"""Smoke test: every rendered HTML page has a sitemap entry.

Walks ``public/`` for ``index.html`` files, derives the canonical URL,
and asserts each is present in ``public/sitemap.xml`` (or any
per-language sitemap referenced from a sitemap index). Excludes
URLs that don't belong in a sitemap by convention:

  - ``/404/`` and per-language equivalents — error pages
  - ``/offline/`` and per-language equivalents — service-worker fallbacks
  - ``/thanks/`` and per-language equivalents — post-submit pages

Normalises URLs both ways: ``/foo/`` and ``/foo/index.html`` compare
equal, so the gate doesn't false-fail on canonical-form variation.

Run from repo root: ``python3 scripts/test_sitemap_completeness.py``.
Exits non-zero on any rendered page that is missing.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
SITE = "https://sebastienrousseau.com"

# Paths excluded from sitemap by convention.
_EXCLUDE_TAILS = (
    "/404/", "/offline/", "/thanks/",
    # FR localised
    "/fr/404/", "/fr/hors-ligne/", "/fr/merci/",
)

_LOC_RE = re.compile(r'<loc>([^<]+)</loc>')


def _norm(url: str) -> str:
    """Normalise: strip trailing /index.html and trailing slash so the
    canonical form (`/foo/`) and the path form (`/foo/index.html`)
    compare equal."""
    url = url.rstrip()
    if url.endswith("/index.html"):
        url = url[: -len("/index.html")]
    return url.rstrip("/")


def collect_sitemap_urls() -> set[str]:
    """Read every sitemap.xml under public/ (root + per-language indexes)
    and return the normalised set of every ``<loc>`` entry."""
    urls: set[str] = set()
    for sm in PUBLIC.rglob("sitemap.xml"):
        text = sm.read_text(encoding="utf-8", errors="ignore")
        urls.update(_norm(u) for u in _LOC_RE.findall(text))
    return urls


def collect_rendered_pages() -> set[str]:
    """Walk public/ for index.html files; return normalised canonical URLs.
    Excludes pages that shouldn't appear in a sitemap by convention."""
    urls: set[str] = set()
    for page in PUBLIC.rglob("index.html"):
        rel = page.relative_to(PUBLIC).as_posix()
        if rel == "index.html":
            canonical = SITE + "/"
        else:
            canonical = SITE + "/" + rel.removesuffix("index.html")
        if any(canonical.endswith(tail) for tail in _EXCLUDE_TAILS):
            continue
        urls.add(_norm(canonical))
    return urls


def main() -> int:
    if not PUBLIC.is_dir():
        print("error: public/ not built — run ./build.sh first", file=sys.stderr)
        return 1
    sitemap = collect_sitemap_urls()
    rendered = collect_rendered_pages()

    missing = rendered - sitemap
    if missing:
        print("sitemap completeness defects (pages rendered but absent from any sitemap):",
              file=sys.stderr)
        for url in sorted(missing)[:30]:
            print(f"  - {url}", file=sys.stderr)
        if len(missing) > 30:
            print(f"  …and {len(missing) - 30} more", file=sys.stderr)
        return 1

    print(
        f"ok: sitemap completeness — {len(rendered)} non-excluded rendered pages, "
        f"all present in sitemap ({len(sitemap)} total entries)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
