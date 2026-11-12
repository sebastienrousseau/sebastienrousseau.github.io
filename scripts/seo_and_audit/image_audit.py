#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Audit every image on the built site (plan F-1).

Errors (exit 1):
* an ``<img>`` without both ``width`` and ``height`` (layout shift);
* the first large image in the body (declared width 300px or more: the
  likely LCP element; avatars and icons come first on articles) marked
  ``loading="lazy"``, which delays it;
* that image without ``fetchpriority="high"``.

Warnings (printed only):
* an image that is not WebP, AVIF or SVG;
* a CDN width variant (``-1920``) more than twice the declared width
  without a ``srcset`` to let the browser pick a smaller one.

    image_audit.py public
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

_BODY_RE = re.compile(r"<body\b[^>]*>(.*)</body>", re.S | re.I)
_IMG_RE = re.compile(r"<img\b[^>]*>", re.I)
_ATTR_RE = r"""\b{0}=["']?([^"'\s>]+)"""
_MODERN = (".webp", ".avif", ".svg")
_VARIANT_RE = re.compile(r"-(320|640|1200|1920)\.webp")
LARGE = 300


def attr(tag: str, name: str) -> str | None:
    m = re.search(_ATTR_RE.format(name), tag, re.I)
    return m.group(1) if m else None


def _is_large(tag: str) -> bool:
    width = attr(tag, "width") or ""
    return width.isdigit() and int(width) >= LARGE


def _first_image_problems(tag: str) -> list[str]:
    out = []
    if (attr(tag, "loading") or "").lower() == "lazy":
        out.append('first large image is loading="lazy"')
    if (attr(tag, "fetchpriority") or "").lower() != "high":
        out.append('first large image lacks fetchpriority="high"')
    return out


def _warnings(tag: str, src: str) -> list[str]:
    out = []
    path = src.split("?", 1)[0].lower()
    if not path.endswith(_MODERN) and not path.startswith("data:"):
        out.append(f"not WebP/AVIF/SVG: {src[:80]}")
    m, width = _VARIANT_RE.search(path), attr(tag, "width")
    if (
        m
        and width
        and width.isdigit()
        and int(m.group(1)) > 2 * int(width)
        and not attr(tag, "srcset")
    ):
        out.append(f"-{m.group(1)} variant for a {width}px image without srcset: {src[:80]}")
    return out


def audit_page(page_html: str) -> tuple[list[str], list[str]]:
    """(errors, warnings) for one page."""
    body = _BODY_RE.search(page_html)
    tags = _IMG_RE.findall(body.group(1) if body else page_html)
    errors: list[str] = []
    warnings: list[str] = []
    seen_large = False
    for tag in tags:
        src = attr(tag, "src") or ""
        if not (attr(tag, "width") and attr(tag, "height")):
            errors.append(f"no width/height: {src[:80]}")
        if not seen_large and _is_large(tag):
            seen_large = True
            errors += _first_image_problems(tag)
        warnings += _warnings(tag, src)
    return errors, warnings


def main(argv: list[str]) -> int:
    root = Path(argv[0] if argv else "public")
    errors, warnings = [], []
    for page in sorted(root.rglob("index.html")):
        e, w = audit_page(page.read_text(encoding="utf-8", errors="ignore"))
        rel = page.relative_to(root).as_posix()
        errors += [f"{rel}: {x}" for x in e]
        warnings += [f"{rel}: {x}" for x in w]
    print(f"image audit: {len(errors)} error(s), {len(warnings)} warning(s)")
    for line in errors[:30]:
        print(f"  error: {line}")
    for line in warnings[:10]:
        print(f"  warning: {line}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
