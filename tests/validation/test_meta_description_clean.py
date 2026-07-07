#!/usr/bin/env python3
"""Gate: no rendered page ships corrupted description metadata.

The SSG derives ``<meta name="description">``, ``og:description`` and
``twitter:description`` by scraping the rendered ``<body>``, which used
to leave double-escaped markup ("&amp;lt;div lang=&quot;en&quot; …") in
the social-share card — the exact string that renders when someone
shares the URL. ``postbuild_lib.seo.clean_meta_description`` rewrites the
three tags with a clean, attribute-escaped summary. This gate asserts the
fix held: every page's description tags are free of HTML markup and
entity-encoded markup.

Run from repo root: ``python3 tests/validation/test_meta_description_clean.py``.
Exits non-zero on the first page that still carries corrupted markup.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"

# The three description-bearing meta tags (name= or property=).
_DESC_META_RE = re.compile(
    r'<meta\b[^>]*\b(?:name|property)='
    r'"(description|og:description|twitter:description)"[^>]*>',
    re.IGNORECASE,
)
_CONTENT_RE = re.compile(r'content="([^"]*)"', re.IGNORECASE)

# Markers of a leaked / escaped tag inside a description. A clean summary
# never contains a literal angle bracket or an entity-encoded one.
_CORRUPT_MARKERS = ("<", "&lt;", "&amp;lt;", "&amp;amp;")


def _defects(html: str) -> list[str]:
    out: list[str] = []
    for tag in _DESC_META_RE.finditer(html):
        cm = _CONTENT_RE.search(tag.group(0))
        content = cm.group(1) if cm else ""
        if any(marker in content for marker in _CORRUPT_MARKERS):
            out.append(f'{tag.group(1)}: {content[:80]}')
    return out


def main() -> int:
    if not PUBLIC.is_dir():
        print("error: public/ not built — run ./build.sh first", file=sys.stderr)
        return 1

    bad: dict[str, list[str]] = {}
    scanned = 0
    for page in PUBLIC.rglob("index.html"):
        scanned += 1
        defects = _defects(page.read_text(encoding="utf-8", errors="ignore"))
        if defects:
            bad[str(page.relative_to(PUBLIC))] = defects

    if bad:
        print(
            "corrupted description metadata (markup leaked into "
            "description / og:description / twitter:description):",
            file=sys.stderr,
        )
        for rel, defects in sorted(bad.items())[:30]:
            print(f"  {rel}", file=sys.stderr)
            for d in defects:
                print(f"      {d}", file=sys.stderr)
        if len(bad) > 30:
            print(f"  …and {len(bad) - 30} more pages", file=sys.stderr)
        return 1

    print(f"ok: description metadata clean — {scanned} pages scanned")
    return 0


if __name__ == "__main__":
    sys.exit(main())
