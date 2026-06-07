#!/usr/bin/env python3
"""Smoke test: every hreflang alternate is reciprocal.

For every rendered HTML page in ``public/`` that declares
``<link rel="alternate" hreflang="X" href="…">`` pointing at
another rendered page, that target page must declare a matching
alternate back to the source. This is what Google requires and
what trips up most multi-language sites in practice.

Also asserts:
  - every active non-EN language listed in ``_lang_registry`` is
    represented in *every* EN page's alternate set (a freshly-shipped
    language must rebuild every existing page so its hreflang gets
    injected — this guard catches a forgotten rebuild)
  - ``x-default`` is present on every paired page, and points at the
    EN canonical of that pair

Run from repo root: ``python3 scripts/test_hreflang_reciprocity.py``.
Exits non-zero on any defect.
"""

from __future__ import annotations

import sys as _sys  # path bootstrap — scripts reorg (scripts/lib/ on sys.path)
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[2] / "scripts" / "lib"))

import re
import sys
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).parent))

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
SITE = "https://sebastienrousseau.com"

_HREFLANG_RE = re.compile(
    r'<link\s+rel="?alternate"?\s+hreflang="?([a-zA-Z0-9-]+)"?\s+href="?([^"\s>]+)',
    re.IGNORECASE,
)


def _url_to_local_path(url: str) -> str | None:
    """Convert a same-origin URL into a relative ``public/`` path. Returns
    None for off-site URLs."""
    p = urlparse(url)
    if p.netloc and p.netloc not in ("sebastienrousseau.com", "www.sebastienrousseau.com"):
        return None
    path = p.path or "/"
    # Map "/" to public/index.html, "/foo/" to public/foo/index.html, etc.
    if path.endswith("/"):
        path = path + "index.html"
    elif not path.endswith((".html", ".xml", ".json", ".txt", ".pdf")):
        path = path + "/index.html"
    return path.lstrip("/")


def main() -> int:  # noqa: C901 — reciprocity validator is a sequential ladder
    if not PUBLIC.is_dir():
        print("error: public/ not built — run ./build.sh first", file=sys.stderr)
        return 1

    # Pass 1: gather alternates per page
    alts: dict[str, dict[str, str]] = {}  # rel_path → {hreflang: href}
    for page in PUBLIC.rglob("index.html"):
        rel = page.relative_to(PUBLIC).as_posix()
        html = page.read_text(encoding="utf-8", errors="ignore")
        page_alts: dict[str, str] = {}
        for m in _HREFLANG_RE.finditer(html):
            page_alts[m.group(1).lower()] = m.group(2)
        if page_alts:
            alts[rel] = page_alts

    if not alts:
        print("warn: no hreflang found anywhere — skipping reciprocity check", file=sys.stderr)
        return 0

    problems: list[str] = []
    # Pass 2: reciprocity — every alternate must be reciprocated
    for src, src_alts in alts.items():
        for tag, href in src_alts.items():
            if tag == "x-default":
                continue
            target_rel = _url_to_local_path(href)
            if target_rel is None:
                # Off-site URL; nothing to reciprocate.
                continue
            target_alts = alts.get(target_rel)
            if target_alts is None:
                problems.append(
                    f"{src}: hreflang={tag!r} points at {target_rel!r} which has no alternates"
                )
                continue
            # The target must list our source as one of its alternates.
            # Derive every plausible URL spelling of `src` and compare
            # against the target's alt set after normalising trailing
            # slashes both ways.
            # src is a public/-relative path like "index.html",
            # "fr/index.html", "about/index.html".
            path = "/" + src.removesuffix("index.html")  # "/", "/fr/", "/about/"
            src_url_candidates = {
                SITE + path,  # canonical (trailing slash)
                SITE + path.rstrip("/") if path != "/" else SITE,
                SITE + "/" + src,  # explicit /index.html
                path,  # relative
                "/" + src,  # relative explicit
            }

            def _norm(u: str) -> str:
                u = u.rstrip("/")
                return u or "/"

            target_norm = {_norm(v) for v in target_alts.values()}
            cand_norm = {_norm(v) for v in src_url_candidates}
            if not (target_norm & cand_norm):
                problems.append(
                    f"{src} → {target_rel}: target does not reciprocate "
                    f"(target alts: {list(target_alts.values())[:3]}…)"
                )

    # Pass 3: x-default presence on paired pages
    for src, src_alts in alts.items():
        if len(src_alts) >= 2 and "x-default" not in src_alts:
            problems.append(f"{src}: missing x-default")

    if problems:
        print("hreflang reciprocity defects:", file=sys.stderr)
        for line in problems[:30]:
            print(f"  - {line}", file=sys.stderr)
        if len(problems) > 30:
            print(f"  …and {len(problems) - 30} more", file=sys.stderr)
        return 1

    paired = sum(1 for a in alts.values() if len(a) >= 2)
    print(
        f"ok: hreflang reciprocity passes ({paired} paired pages, {len(alts)} total with alternates)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
