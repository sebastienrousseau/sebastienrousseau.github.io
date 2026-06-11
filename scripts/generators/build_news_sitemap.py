#!/usr/bin/env python3
"""Generate a Google News XML sitemap at ``public/news-sitemap.xml``.

Google News sitemaps must only contain articles published in the last 48 hours.
This script scans all active language posts under ``_posts/`` (including English
in the root directory), filters for publication dates within the last 48 hours,
and writes a compliant XML document using the Google News namespace.
"""

from __future__ import annotations

import sys as _sys
from pathlib import Path as _Path

# Bootstrapping scripts/lib onto sys.path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "lib"))

import contextlib
import re
import sys
from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path

import _lang_registry
from _core import read_frontmatter

PUBLIC = Path("public")
BASE = "https://sebastienrousseau.com"

_DATED_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-")
_AMP_RE = re.compile(r"&(?![a-zA-Z]+;|#\d+;|#x[0-9a-fA-F]+;)")
_DEFAULT_PUB_NAME = "Sebastien Rousseau Research"
_WINDOW_PAST_S = 48 * 3600
_WINDOW_FUTURE_S = -7200  # 2h of forward timezone skew


def xml_escape(s: str) -> str:
    s = _AMP_RE.sub("&amp;", s)
    return s.replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")


def iso8601(d: datetime) -> str:
    return d.strftime("%Y-%m-%dT%H:%M:%S+00:00")


def _resolve_pub_name(lang_code: str) -> str:
    """Localised publication name from `feeds.channelTitle` if present;
    fall back to the canonical English brand string. Tolerates a missing
    or partial strings.json — the news sitemap is a syndication surface,
    not a place to fail the build."""
    with contextlib.suppress(Exception):
        strings = _lang_registry.load_strings(lang_code)
        if strings.get("feeds.channelTitle"):
            return strings["feeds.channelTitle"]
    return _DEFAULT_PUB_NAME


def _slug_for_locale(
    stem: str, lang_code: str, en_to_lang: dict[str, str], lang_to_en: dict[str, str]
) -> str | None:
    """Return the URL slug for this post under this locale, or None if
    the locale's slug-map disowns it."""
    if lang_code == "en":
        return stem
    if stem in lang_to_en:
        return stem
    if stem in en_to_lang:
        return en_to_lang[stem]
    return None


def _iter_locale_entries(lang_code: str, now: datetime) -> Iterator[dict]:
    """Yield one entry dict per dated post in `lang_code` that falls
    inside the rolling 48 h news window."""
    src_dir = Path("_posts") if lang_code == "en" else Path(f"_posts/{lang_code}")
    if not src_dir.is_dir():
        return

    if lang_code == "en":
        en_to_lang: dict[str, str] = {}
        lang_to_en: dict[str, str] = {}
    else:
        slugs: dict[str, str] = {}
        with contextlib.suppress(Exception):
            slugs = _lang_registry.load_slugs(lang_code).get("articles", {})
        en_to_lang = slugs
        lang_to_en = {v: k for k, v in slugs.items()}

    pub_name = _resolve_pub_name(lang_code)

    for md in sorted(src_dir.glob("*.md")):
        m = _DATED_RE.match(md.stem)
        if not m:
            continue
        slug = _slug_for_locale(md.stem, lang_code, en_to_lang, lang_to_en)
        if slug is None:
            continue

        fm = read_frontmatter(md)
        if not fm.get("title"):
            continue

        d = datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), 6, 6, 6, tzinfo=UTC)
        delta = (now - d).total_seconds()
        if not (_WINDOW_FUTURE_S <= delta <= _WINDOW_PAST_S):
            continue

        url = f"{BASE}/{slug}/" if lang_code == "en" else f"{BASE}/{lang_code}/{slug}/"
        yield {
            "url": url,
            "title": fm.get("title", ""),
            "keywords": fm.get("keywords", ""),
            "date": d,
            "lang_code": lang_code,
            "pub_name": pub_name,
        }


def _render_xml(entries: list[dict]) -> str:
    parts: list[str] = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">',
    ]
    for e in entries:
        parts.append("  <url>")
        parts.append(f"    <loc>{e['url']}</loc>")
        parts.append("    <news:news>")
        parts.append("      <news:publication>")
        parts.append(f"        <news:name>{xml_escape(e['pub_name'])}</news:name>")
        parts.append(f"        <news:language>{e['lang_code']}</news:language>")
        parts.append("      </news:publication>")
        parts.append(f"      <news:publication_date>{iso8601(e['date'])}</news:publication_date>")
        parts.append(f"      <news:title>{xml_escape(e['title'])}</news:title>")
        if e["keywords"]:
            parts.append(f"      <news:keywords>{xml_escape(e['keywords'])}</news:keywords>")
        parts.append("    </news:news>")
        parts.append("  </url>")
    parts.append("</urlset>")
    parts.append("")
    return "\n".join(parts)


def build_news_sitemap() -> int:
    now = datetime.now(tz=UTC)
    entries: list[dict] = []
    for lang in _lang_registry.active():
        entries.extend(_iter_locale_entries(lang.code, now))
    entries.sort(key=lambda e: e["date"], reverse=True)

    PUBLIC.mkdir(parents=True, exist_ok=True)
    xml_path = PUBLIC / "news-sitemap.xml"
    xml_path.write_text(_render_xml(entries), encoding="utf-8")
    print(f"build_news_sitemap: wrote {len(entries)} entries to {xml_path}")
    return len(entries)


def main() -> int:
    try:
        build_news_sitemap()
        return 0
    except Exception as exc:
        print(f"error: failed to build news sitemap: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
