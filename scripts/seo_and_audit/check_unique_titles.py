#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Fail when more than one indexable page in a locale shares a <title> or description.

Walks ``public/**/index.html`` (skipping ``/labs/``, redirect stubs with
``http-equiv="refresh"``, non-self-canonical pages, and ``noindex`` pages),
collects ``<title>`` and ``<meta name="description">`` grouped by locale, and
exits 1 if any title or description is shared by more than one URL.
"""

from __future__ import annotations

import argparse
import collections
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

import _lang_registry  # type: ignore[import-not-found]

_TITLE_RE = re.compile(r"<title>([^<]*)</title>", re.IGNORECASE)
_DESC_RE = re.compile(
    r'<meta\b[^>]*\bname=["\']?description["\']?[^>]*\bcontent="([^"]*)"',
    re.IGNORECASE,
)
_ROBOTS_RE = re.compile(
    r'<meta\b[^>]*\bname=["\']?robots["\']?[^>]*\bcontent="([^"]*)"',
    re.IGNORECASE,
)
_REFRESH_RE = re.compile(r'<meta\b[^>]*\bhttp-equiv=["\']?refresh["\']?', re.IGNORECASE)
_CANON_RE = re.compile(
    r'<link\b[^>]*\brel=["\']?canonical["\']?[^>]*\bhref="([^"]*)"',
    re.IGNORECASE,
)
_BASE_URL = "https://sebastienrousseau.com"
_NON_EN_LOCALES: frozenset[str] = frozenset(
    lang.code for lang in _lang_registry.LANGUAGES if lang.code != "en"
)


def _is_indexable_canonical(html: str, rel_url: str) -> bool:
    """Return True if the page is indexable, not a meta-refresh redirect, and self-canonical."""
    robots_m = _ROBOTS_RE.search(html)
    if robots_m and "noindex" in robots_m.group(1).lower():
        return False
    if _REFRESH_RE.search(html):
        return False
    canon_m = _CANON_RE.search(html)
    if canon_m:
        canon_path = canon_m.group(1).removeprefix(_BASE_URL)
        if not canon_path.endswith("/"):
            canon_path += "/"
        if canon_path != rel_url:
            return False
    return True


def _locale_for(rel_parts: tuple[str, ...]) -> str:
    """Return the locale code for a relative path tuple under ``public/``."""
    if len(rel_parts) > 1 and rel_parts[0] in _NON_EN_LOCALES:
        return rel_parts[0]
    return "en"


def _first_group(pattern: re.Pattern[str], html: str) -> str:
    """Stripped first group of ``pattern`` in ``html``, or ``""``."""
    m = pattern.search(html)
    return m.group(1).strip() if m else ""


def _page_record(base_dir: Path, page: Path) -> tuple[str, str, str, str] | None:
    """``(locale, url, title, description)`` for an indexable page, else None."""
    rel_parts = page.relative_to(base_dir).parts
    if rel_parts and rel_parts[0] == "labs":
        return None
    rel_dir = "/" + "/".join(rel_parts[:-1])
    rel_url = "/" if rel_dir == "/" else f"{rel_dir}/"
    html = page.read_text(encoding="utf-8", errors="ignore")
    if not _is_indexable_canonical(html, rel_url):
        return None
    return (
        _locale_for(rel_parts),
        rel_url,
        _first_group(_TITLE_RE, html),
        _first_group(_DESC_RE, html),
    )


def _duplicates(label: str, seen: dict[tuple[str, str], list[str]]) -> list[str]:
    """One error line per ``(locale, value)`` shared by more than one URL."""
    return [
        f"duplicate {label} [{locale}] {val!r}: {', '.join(urls)}"
        for (locale, val), urls in sorted(seen.items())
        if len(urls) > 1
    ]


def scan_tree(base_dir: Path) -> list[str]:
    """Scan ``base_dir`` and return human-readable duplicate-metadata error lines."""
    titles: dict[tuple[str, str], list[str]] = collections.defaultdict(list)
    descs: dict[tuple[str, str], list[str]] = collections.defaultdict(list)
    for page in sorted(base_dir.rglob("index.html")):
        record = _page_record(base_dir, page)
        if record is None:
            continue
        locale, rel_url, title, desc = record
        if title:
            titles[(locale, title)].append(rel_url)
        if desc:
            descs[(locale, desc)].append(rel_url)
    return _duplicates("<title>", titles) + _duplicates("description", descs)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-dir", type=Path, default=ROOT / "public")
    args = parser.parse_args(argv)
    errors = scan_tree(args.base_dir)
    if errors:
        for err in errors:
            print(f"FAIL: {err}", file=sys.stderr)
        return 1
    print(f"OK: unique <title> and meta descriptions across {args.base_dir}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
