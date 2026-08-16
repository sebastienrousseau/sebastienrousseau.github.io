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

import sys as _sys  # path bootstrap — scripts reorg (scripts/lib/ on sys.path)
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[2] / "scripts" / "lib"))

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
SITE = "https://sebastienrousseau.com"

# Paths excluded from sitemap by convention.
_EXCLUDE_TAILS = (
    "/404/",
    "/offline/",
    "/thanks/",
    # FR localised
    "/fr/404/",
    "/fr/hors-ligne/",
    "/fr/merci/",
)

# Prefixes excluded from sitemap by convention. WASM lab demos are
# `<meta name="robots" content="noindex,nofollow">` by design — they're
# experimental playgrounds linked from articles, not canonical content
# that should rank in search.
_EXCLUDE_PREFIXES = ("/labs/",)

_LOC_RE = re.compile(r"<loc>([^<]+)</loc>")


def _norm(url: str) -> str:
    """Normalise: strip trailing /index.html and trailing slash so the
    canonical form (`/foo/`) and the path form (`/foo/index.html`)
    compare equal."""
    url = url.rstrip()
    if url.endswith("/index.html"):
        url = url[: -len("/index.html")]
    return url.rstrip("/")


def _index_targets(locs: list[str]) -> list[Path]:
    """Map <loc> entries of a <sitemapindex> onto files under public/."""
    out: list[Path] = []
    for loc in locs:
        rel = loc.split("//", 1)[-1] if "//" in loc else loc
        rel = rel.split("/", 1)[-1] if "/" in rel else ""
        if rel:
            out.append(PUBLIC / rel.lstrip("/"))
    return out


def collect_sitemap_urls() -> set[str]:
    """Return every ``<loc>`` in the root sitemap, following sitemap indexes.

    Deliberately *not* a tree-wide ``rglob``. ssg emits a full copy of the
    sitemap into every output directory, and each copy prefixes its URLs
    with the containing directory — yielding malformed double-slash
    entries like ``/made-with-static-site-generator//2018-01-01-…``. On
    this site that is 3,635 files, 13.5 GB and ~49.8 M ``<loc>`` entries,
    of which ~1.8 M are that junk. Reading them turned a one-second gate
    into a multi-minute one (minutes more when the page cache is cold)
    while contributing nothing: the root sitemap already covers every
    rendered page.
    """
    urls: set[str] = set()
    seen: set[Path] = set()
    queue: list[Path] = [PUBLIC / "sitemap.xml"]
    while queue:
        sm = queue.pop()
        resolved = sm.resolve()
        if resolved in seen or not sm.is_file():
            continue
        seen.add(resolved)
        text = sm.read_text(encoding="utf-8", errors="ignore")
        locs = _LOC_RE.findall(text)
        if "<sitemapindex" in text:
            queue.extend(_index_targets(locs))
        else:
            urls.update(_norm(u) for u in locs)
    return urls


def _is_redirect_page(page: Path) -> bool:
    """Redirect pages (legacy URLs converted by postbuild_lib.redirects,
    e.g. /papers/ -> /research/) canonicalise to their target and are
    deliberately purged from the sitemap — a non-canonical URL does not
    belong there. The meta refresh lives in <head>, so sniffing the first
    few KB is sufficient — read just that, instead of pulling whole pages
    into memory only to slice the front off them."""
    with page.open("r", encoding="utf-8", errors="ignore") as fh:
        head = fh.read(4096)
    return 'http-equiv="refresh"' in head


def collect_rendered_pages() -> set[str]:
    """Walk public/ for index.html files; return normalised canonical URLs.
    Excludes pages that shouldn't appear in a sitemap by convention
    (error/offline/post-submit pages, labs, redirect pages)."""
    urls: set[str] = set()
    for page in PUBLIC.rglob("index.html"):
        rel = page.relative_to(PUBLIC).as_posix()
        if rel == "index.html":
            canonical = SITE + "/"
        else:
            canonical = SITE + "/" + rel.removesuffix("index.html")
        if any(canonical.endswith(tail) for tail in _EXCLUDE_TAILS):
            continue
        path = canonical[len(SITE) :]
        if any(path.startswith(prefix) for prefix in _EXCLUDE_PREFIXES):
            continue
        if _is_redirect_page(page):
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
        print(
            "sitemap completeness defects (pages rendered but absent from any sitemap):",
            file=sys.stderr,
        )
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
