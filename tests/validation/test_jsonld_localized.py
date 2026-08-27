#!/usr/bin/env python3
"""Smoke test: JSON-LD inLanguage matches the page's <html lang>.

Per Google Search Central guidance, every JSON-LD block's
``inLanguage`` field should be a BCP-47 tag consistent with the
page's declared ``<html lang>``. This gate enforces the *base
language* match — ``inLanguage: "en"`` on a page with
``<html lang="en-GB">`` is fine (en is the base of en-GB), but
``inLanguage: "fr"`` on the same page is an error.

Strict tag-equality is **not** required. ``en`` and ``en-GB`` are
both valid BCP-47 and Schema.org accepts the less-specific form.
What matters is that we never claim a page is in a language it
isn't — that misleads search engines and AI crawlers.

Run from repo root: ``python3 scripts/test_jsonld_localized.py``.
Exits non-zero on any base-language mismatch.
"""

from __future__ import annotations

import sys as _sys  # path bootstrap — scripts reorg (scripts/lib/ on sys.path)
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[2] / "scripts" / "lib"))

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"

_HTML_LANG_RE = re.compile(r'<html\b[^>]*\blang=["\']?([a-zA-Z0-9-]+)', re.IGNORECASE)
_JSONLD_RE = re.compile(
    r'<script[^>]*type=["\']?application/ld\+json["\']?[^>]*>([\s\S]*?)</script>',
    re.IGNORECASE,
)


def _base_lang(tag: str) -> str:
    """Strip BCP-47 subtags. ``en-GB`` → ``en``, ``zh-Hans`` → ``zh``."""
    return tag.split("-", 1)[0].lower()


def _walk_inlanguage(node: object, out: list[str]) -> None:
    """Walk a JSON-LD node tree and collect every ``inLanguage`` value
    encountered."""
    if isinstance(node, dict):
        if "inLanguage" in node and isinstance(node["inLanguage"], str):
            out.append(node["inLanguage"])
        for v in node.values():
            _walk_inlanguage(v, out)
    elif isinstance(node, list):
        for v in node:
            _walk_inlanguage(v, out)


def check_page(path: Path) -> list[str]:
    """Return defects for one HTML page. Empty list = pass."""
    rel = path.relative_to(PUBLIC).as_posix()
    html = path.read_text(encoding="utf-8", errors="ignore")
    lang_m = _HTML_LANG_RE.search(html)
    if not lang_m:
        return []  # No <html lang>; nothing to validate against.
    page_lang = _base_lang(lang_m.group(1))

    problems: list[str] = []
    for jm in _JSONLD_RE.finditer(html):
        body = jm.group(1)
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            continue  # JSON-LD parse errors are caught by validate_jsonld.py
        seen: list[str] = []
        _walk_inlanguage(data, seen)
        problems.extend(
            f"{rel}: inLanguage={tag!r} (base {_base_lang(tag)!r}) ≠ <html lang> base {page_lang!r}"
            for tag in seen
            if _base_lang(tag) != page_lang
        )
    return problems


def main() -> int:
    if not PUBLIC.is_dir():
        print("error: public/ not built — run ./build.sh first", file=sys.stderr)
        return 1
    pages = sorted(PUBLIC.rglob("index.html"))
    all_problems: list[str] = []
    for page in pages:
        all_problems.extend(check_page(page))

    if all_problems:
        print("JSON-LD inLanguage defects:", file=sys.stderr)
        for line in all_problems[:30]:
            print(f"  - {line}", file=sys.stderr)
        if len(all_problems) > 30:
            print(f"  …and {len(all_problems) - 30} more", file=sys.stderr)
        return 1

    print(f"ok: JSON-LD inLanguage matches <html lang> on all {len(pages)} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
