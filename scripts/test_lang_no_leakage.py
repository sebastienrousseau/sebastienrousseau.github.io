#!/usr/bin/env python3
"""Smoke test: no EN UI strings leak into non-EN page chrome.

When a translation pipeline misses an edge case, English UI strings
end up on translated pages — visitor sees ``Subscribe`` on the FR
newsletter pill, ``Latest`` on the FR home eyebrow, or
``Get in touch`` in the FR footer. These are exactly the regressions
that hit FR during early rollout (``1× Latest``, ``1× Get in touch``).

This gate cross-references ``_data/i18n/en/strings.json`` (the
canonical EN UI strings) against every non-EN page's chrome content.
A hit means a string the EN reference treats as UI chrome surfaced
verbatim on a translated page — almost certainly a translation gap.

We scope the search to chrome content only (everything outside
``<main>``) so legitimate quoted English text in article bodies
(e.g. an article that QUOTES a Beatles lyric, or a domain term that
isn't translated) is ignored.

Run from repo root: ``python3 scripts/test_lang_no_leakage.py``.
Exits non-zero on any leakage. Wired into ``build.sh`` so the build
fails if a future translation gap silently slips through.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _lang_registry  # type: ignore[import-not-found]

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"

# We only scan chrome content (outside <main>). The page lang is read
# from <html lang=…>.
_HTML_LANG_RE = re.compile(r'<html\b[^>]*\blang=["\']?([a-zA-Z0-9-]+)', re.IGNORECASE)
_MAIN_RE = re.compile(r'<main\b[\s\S]*?</main>', re.IGNORECASE)
_SCRIPT_RE = re.compile(r'<script\b[\s\S]*?</script>', re.IGNORECASE)
_STYLE_RE = re.compile(r'<style\b[\s\S]*?</style>', re.IGNORECASE)
_COMMENT_RE = re.compile(r'<!--[\s\S]*?-->')
_LINK_LANG_MENU_RE = re.compile(r'<div class=["\']?ap-lang-menu[\s\S]*?</div>', re.IGNORECASE)

# Strings that legitimately appear in EN form in every language's
# chrome — brand names, technical terms, proper nouns. These are
# whitelisted so the gate doesn't flag them.
_GLOBAL_WHITELIST = (
    "Sebastien Rousseau", "Banking On Quantum",
    "RSS", "Atom", "Spotify", "GitHub", "LinkedIn", "Twitter",
    "X", "YouTube", "Medium", "Apple", "Cloudflare",
    "ISO 20022", "PQC", "AI", "API",
)


def _base_lang(tag: str) -> str:
    """``en-GB`` → ``en``, ``zh-Hans`` → ``zh``."""
    return tag.split("-", 1)[0].lower()


_META_DESC_RE = re.compile(
    r'<meta\s+(?:name|property)=["\']?(?:description|og:description|twitter:description)[^>]*>',
    re.IGNORECASE,
)
_META_KEYWORDS_RE = re.compile(
    r'<meta\s+name=["\']?keywords[^>]*>', re.IGNORECASE,
)
_TITLE_TAG_RE = re.compile(r'<title>[\s\S]*?</title>', re.IGNORECASE)
_OG_TITLE_RE = re.compile(
    r'<meta\s+(?:name|property)=["\']?(?:og:title|twitter:title)[^>]*>',
    re.IGNORECASE,
)


def _strip_chrome_noise(html: str) -> str:
    """Remove <main>, <script>, <style>, the lang switcher menu, and
    per-page content metadata (title, description, keywords) — these
    are content-driven and can legitimately contain EN technical
    terms ("Large Language Models", "Post-Quantum Cryptography", …)
    as substrings of phrases."""
    html = _MAIN_RE.sub("", html)
    html = _SCRIPT_RE.sub("", html)
    html = _STYLE_RE.sub("", html)
    html = _COMMENT_RE.sub("", html)
    html = _LINK_LANG_MENU_RE.sub("", html)
    # Strip per-page content metadata
    html = _META_DESC_RE.sub("", html)
    html = _META_KEYWORDS_RE.sub("", html)
    html = _TITLE_TAG_RE.sub("", html)
    html = _OG_TITLE_RE.sub("", html)
    return html


def _en_chrome_strings() -> list[str]:
    """Return the EN UI strings worth checking for leakage. Filter out
    very short strings (likely false positives) and globally-OK terms."""
    try:
        en = _lang_registry.load_strings("en")
    except _lang_registry.LanguageError:
        return []
    out: list[str] = []
    for v in en.values():
        if not isinstance(v, str):
            continue
        v = v.strip()
        if len(v) < 6:
            # Too short — risk of matching incidentally in unrelated copy.
            continue
        if v in _GLOBAL_WHITELIST:
            continue
        out.append(v)
    return out


def check_page(path: Path, en_strings: list[str]) -> list[str]:
    """Return defects for one page.

    Each EN string is searched with word boundaries either side so it
    doesn't false-positive on substring matches inside legitimate
    technical-term content (e.g. "Language" in "Large Language Models"
    inside a description meta is the article's topic, not chrome).
    """
    html = path.read_text(encoding="utf-8", errors="ignore")
    lang_m = _HTML_LANG_RE.search(html)
    if not lang_m or _base_lang(lang_m.group(1)) == "en":
        return []
    chrome = _strip_chrome_noise(html)
    rel = path.relative_to(PUBLIC).as_posix()
    defects: list[str] = []
    for s in en_strings:
        escaped = re.escape(s)
        pat = rf"(?<![A-Za-z\-]){escaped}(?![A-Za-z\-])"
        if re.search(pat, chrome):
            defects.append(f"{rel}: EN string leaked into chrome: {s!r}")
    return defects


def main() -> int:
    if not PUBLIC.is_dir():
        print("error: public/ not built — run ./build.sh first", file=sys.stderr)
        return 1
    en_strings = _en_chrome_strings()
    if not en_strings:
        print("warn: no EN reference strings — skipping leakage check", file=sys.stderr)
        return 0

    all_problems: list[str] = []
    for page in sorted(PUBLIC.rglob("index.html")):
        all_problems.extend(check_page(page, en_strings))

    if all_problems:
        print(f"lang-leakage: {len(all_problems)} EN-string leak(s) into non-EN chrome:",
              file=sys.stderr)
        for line in all_problems[:30]:
            print(f"  - {line}", file=sys.stderr)
        if len(all_problems) > 30:
            print(f"  …and {len(all_problems) - 30} more", file=sys.stderr)
        return 1

    print(
        f"ok: no EN UI strings leak into non-EN page chrome "
        f"(checked {len(en_strings)} reference strings)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
