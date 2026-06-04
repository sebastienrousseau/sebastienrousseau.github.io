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

import re
import sys
from datetime import UTC, datetime
from pathlib import Path
import _lang_registry
from _core import read_frontmatter

PUBLIC = Path("public")
BASE = "https://sebastienrousseau.com"

_DATED_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-")
_AMP_RE = re.compile(r"&(?![a-zA-Z]+;|#\d+;|#x[0-9a-fA-F]+;)")

def xml_escape(s: str) -> str:
    s = _AMP_RE.sub("&amp;", s)
    return (
        s.replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )

def iso8601(d: datetime) -> str:
    return d.strftime("%Y-%m-%dT%H:%M:%S+00:00")

def build_news_sitemap() -> int:
    now = datetime.now(tz=UTC)
    entries = []

    # Process active languages (including 'en' which is English)
    for lang in _lang_registry.active():
        lang_code = lang.code
        
        # Determine source folder
        if lang_code == "en":
            src_dir = Path("_posts")
        else:
            src_dir = Path(f"_posts/{lang_code}")
            
        if not src_dir.is_dir():
            continue

        # For translations, we map translated slugs to original english slugs or vice versa
        if lang_code != "en":
            try:
                slugs = _lang_registry.load_slugs(lang_code).get("articles", {})
            except Exception:
                slugs = {}
            en_to_lang = slugs
            lang_to_en = {v: k for k, v in slugs.items()}
        else:
            slugs = {}
            en_to_lang = {}
            lang_to_en = {}

        for md in sorted(src_dir.glob("*.md")):
            m = _DATED_RE.match(md.stem)
            if not m:
                continue
            
            # Determine correct URL slug
            if lang_code == "en":
                slug = md.stem
            else:
                if md.stem in lang_to_en:
                    slug = md.stem
                elif md.stem in en_to_lang:
                    slug = en_to_lang[md.stem]
                else:
                    continue

            fm = read_frontmatter(md)
            if not fm.get("title"):
                continue

            # Filename is the canonical publication date (YYYY-MM-DD) at 06:06:06 UTC
            d = datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), 6, 6, 6, tzinfo=UTC)
            
            # Check 48h limit
            time_diff_seconds = (now - d).total_seconds()
            # Accept within 48h (allowing up to 2 hours of future timezone clock drift)
            if -7200 <= time_diff_seconds <= 48 * 3600:
                url = f"{BASE}/{slug}/" if lang_code == "en" else f"{BASE}/{lang_code}/{slug}/"
                
                # Fetch publication name (optionally localized, or default to "Sebastien Rousseau Research")
                pub_name = "Sebastien Rousseau Research"
                try:
                    strings = _lang_registry.load_strings(lang_code)
                    if strings.get("feeds.channelTitle"):
                        pub_name = strings.get("feeds.channelTitle")
                except Exception:
                    pass

                entries.append({
                    "url": url,
                    "title": fm.get("title", ""),
                    "keywords": fm.get("keywords", ""),
                    "date": d,
                    "lang_code": lang_code,
                    "pub_name": pub_name
                })

    # Sort entries by date desc
    entries.sort(key=lambda e: e["date"], reverse=True)

    # Render Google News Sitemap
    parts = []
    parts.append('<?xml version="1.0" encoding="UTF-8"?>')
    parts.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')
    parts.append('        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">')

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
        if e['keywords']:
            parts.append(f"      <news:keywords>{xml_escape(e['keywords'])}</news:keywords>")
        parts.append("    </news:news>")
        parts.append("  </url>")

    parts.append("</urlset>")
    parts.append("")

    PUBLIC.mkdir(parents=True, exist_ok=True)
    xml_path = PUBLIC / "news-sitemap.xml"
    xml_path.write_text("\n".join(parts), encoding="utf-8")
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
