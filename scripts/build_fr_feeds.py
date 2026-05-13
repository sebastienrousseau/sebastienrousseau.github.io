#!/usr/bin/env python3
"""Emit French-language XML feeds under ``public/fr/``.

Shokunin's main ``rss.xml`` / ``atom.xml`` / ``news-sitemap.xml`` only
cover the English ``_posts/*.md``. This script mirrors the same shape
for the French translations so feed readers and Google News see the
French corpus as a first-class language edition.

Inputs : ``_posts/fr/<en-slug>.md`` (frontmatter date + title +
         description + keywords) plus the canonical EN→FR slug map in
         :mod:`_fr_slugs`.

Outputs:
  * ``public/fr/rss.xml``
  * ``public/fr/atom.xml``
  * ``public/fr/news-sitemap.xml``

Must run AFTER ``build_translations.py`` (so the FR pages exist on
disk) and BEFORE ``postbuild.py`` (so the FR feeds get the SRI / CSP
hash treatment if needed, and so robots.txt picks them up).
"""
from __future__ import annotations

import re
import sys
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _fr_slugs import EN_TO_FR, FR_TO_EN

PUBLIC = Path("public")
SRC = Path("_posts/fr")
OUT = PUBLIC / "fr"
BASE = "https://sebastienrousseau.com"

_DATED_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-")
_FM_KEY_RE = re.compile(r'^([a-zA-Z_]+):\s*"((?:[^"\\]|\\.)*)"\s*$')

_FR_MONTHS = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12,
    "janvier": 1, "février": 2, "mars": 3, "avril": 4,
    "mai": 5, "juin": 6, "juillet": 7, "août": 8,
    "septembre": 9, "octobre": 10, "novembre": 11, "décembre": 12,
}


def parse_frontmatter(text: str) -> dict[str, str]:
    fm: dict[str, str] = {}
    sep = 0
    for line in text.splitlines():
        if line.strip() == "---":
            sep += 1
            if sep == 2:
                break
            continue
        if sep != 1:
            continue
        m = _FM_KEY_RE.match(line.strip())
        if m:
            fm[m.group(1)] = m.group(2)
    return fm


def parse_date(s: str) -> datetime:
    """Parse a frontmatter date string ('October 26, 2023' or '2023-10-26')
    to a tz-aware UTC datetime at 06:06:06 (mirrors Shokunin's RSS time)."""
    s = (s or "").strip()
    if not s:
        return datetime.now(tz=UTC)
    # Try ISO first
    try:
        d = datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        d = None
    if d is None:
        # English "Month DD, YYYY" / "Mon DD, YYYY"
        try:
            d = datetime.strptime(s, "%B %d, %Y")
        except ValueError:
            try:
                d = datetime.strptime(s, "%b %d, %Y")
            except ValueError:
                d = None
    if d is None:
        # Mixed-language fallback: "<Month> <day>, <year>"
        m = re.match(r"^([A-Za-zÀ-ÿ]+)\s+(\d{1,2}),?\s+(\d{4})$", s)
        if m:
            month = _FR_MONTHS.get(m.group(1)) or _FR_MONTHS.get(m.group(1).lower())
            if month:
                d = datetime(int(m.group(3)), month, int(m.group(2)))
    if d is None:
        return datetime.now(tz=UTC)
    return d.replace(hour=6, minute=6, second=6, tzinfo=UTC)


def collect_entries() -> list[dict[str, object]]:
    if not SRC.is_dir():
        return []
    entries: list[dict[str, object]] = []
    for md in sorted(SRC.glob("*.md")):
        if not _DATED_RE.match(md.stem):
            continue
        if md.stem in FR_TO_EN:
            slug_fr = md.stem
        elif md.stem in EN_TO_FR:
            slug_fr = EN_TO_FR[md.stem]
        else:
            continue
        fm = parse_frontmatter(md.read_text(encoding="utf-8"))
        if not fm.get("title"):
            continue
        d = parse_date(fm.get("date", ""))
        entries.append({
            "slug": slug_fr,
            "title": fm.get("title", ""),
            "description": fm.get("description", ""),
            "keywords": fm.get("keywords", ""),
            "banner": fm.get("banner", ""),
            "date": d,
            "url": f"{BASE}/fr/{slug_fr}/",
        })
    entries.sort(key=lambda e: e["date"], reverse=True)  # type: ignore[arg-type, return-value]
    return entries


_AMP_RE = re.compile(r"&(?![a-zA-Z]+;|#\d+;|#x[0-9a-fA-F]+;)")


def xml_escape(s: str) -> str:
    """Escape XML special characters. ``html.escape`` handles &, <, >, "
    but leaves existing entities untouched if we feed the raw string."""
    # Replace bare & first, then < > " '
    s = _AMP_RE.sub("&amp;", s)
    return s.replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")


def rfc822(d: datetime) -> str:
    return d.strftime("%a, %d %b %Y %H:%M:%S +0000")


def iso8601(d: datetime) -> str:
    return d.strftime("%Y-%m-%dT%H:%M:%S+00:00")


def render_rss(entries: list[dict[str, object]]) -> str:
    today = datetime.now(tz=UTC)
    parts: list[str] = []
    parts.append('<?xml version="1.0" encoding="UTF-8"?>')
    parts.append('<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">')
    parts.append("  <channel>")
    parts.append("    <title>Sebastien Rousseau — Édition française</title>")
    parts.append(f"    <link>{BASE}/fr/</link>")
    parts.append("    <description>Articles en français : IA appliquée, paiements ISO 20022, cryptographie post-quantique et transformation des paiements wholesale.</description>")
    parts.append(f'    <atom:link href="{BASE}/fr/rss.xml" rel="self" type="application/rss+xml"/>')
    parts.append("    <language>fr-FR</language>")
    parts.append(f"    <lastBuildDate>{rfc822(today)}</lastBuildDate>")
    parts.append("    <copyright>© Copyright 2024 - 2026 - Sebastien Rousseau. All rights reserved.</copyright>")
    for e in entries:
        parts.append("    <item>")
        parts.append(f"      <title>{xml_escape(e['title'])}</title>")  # type: ignore[arg-type]
        parts.append(f"      <link>{e['url']}</link>")
        parts.append(f"      <description>{xml_escape(e['description'])}</description>")  # type: ignore[arg-type]
        parts.append(f'      <guid isPermaLink="true">{e["url"]}</guid>')
        parts.append(f"      <pubDate>{rfc822(e['date'])}</pubDate>")  # type: ignore[arg-type]
        parts.append("      <author>contact@sebastienrousseau.com (Sebastien Rousseau)</author>")
        banner = e.get("banner") or ""
        if banner:
            parts.append(f'      <enclosure url="{banner}" type="image/webp" length="0"/>')
        keywords = (e.get("keywords") or "").split(",") if isinstance(e.get("keywords"), str) else []
        for k in (kw.strip() for kw in keywords if kw.strip()):
            parts.append(f"      <category>{xml_escape(k)}</category>")
        parts.append("    </item>")
    parts.append("  </channel>")
    parts.append("</rss>")
    parts.append("")
    return "\n".join(parts)


def render_atom(entries: list[dict[str, object]]) -> str:
    today = datetime.now(tz=UTC)
    parts: list[str] = []
    parts.append('<?xml version="1.0" encoding="UTF-8"?>')
    parts.append('<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="fr-FR">')
    parts.append("  <title>Sebastien Rousseau — Édition française</title>")
    parts.append(f'  <link href="{BASE}/fr/atom.xml" rel="self" type="application/atom+xml"/>')
    parts.append(f'  <link href="{BASE}/fr/"/>')
    parts.append(f"  <id>{BASE}/fr/</id>")
    parts.append(f"  <updated>{iso8601(today)}</updated>")
    for e in entries:
        parts.append("  <entry>")
        parts.append(f"    <title>{xml_escape(e['title'])}</title>")  # type: ignore[arg-type]
        parts.append(f'    <link href="{e["url"]}"/>')
        parts.append(f"    <id>{e['url']}</id>")
        parts.append(f"    <updated>{iso8601(e['date'])}</updated>")  # type: ignore[arg-type]
        parts.append(f"    <published>{iso8601(e['date'])}</published>")  # type: ignore[arg-type]
        parts.append(f"    <summary>{xml_escape(e['description'])}</summary>")  # type: ignore[arg-type]
        parts.append("    <author><name>contact@sebastienrousseau.com (Sebastien Rousseau)</name></author>")
        parts.append("  </entry>")
    parts.append("</feed>")
    parts.append("")
    return "\n".join(parts)


def render_news_sitemap(entries: list[dict[str, object]]) -> str:
    parts: list[str] = []
    parts.append('<?xml version="1.0" encoding="UTF-8"?>')
    parts.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')
    parts.append('        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">')
    for e in entries:
        parts.append("<url>")
        parts.append(f"  <loc>{e['url']}</loc>")
        parts.append("  <news:news>")
        parts.append("    <news:publication>")
        parts.append("      <news:name>contact@sebastienrousseau.com (Sebastien Rousseau)</news:name>")
        parts.append("      <news:language>fr-FR</news:language>")
        parts.append("    </news:publication>")
        parts.append(f"    <news:publication_date>{iso8601(e['date'])}</news:publication_date>")  # type: ignore[arg-type]
        parts.append(f"    <news:title>{xml_escape(e['title'])}</news:title>")  # type: ignore[arg-type]
        kw = e.get("keywords") or ""
        if isinstance(kw, str) and kw:
            parts.append(f"    <news:keywords>{xml_escape(kw)}</news:keywords>")
        parts.append("  </news:news>")
        parts.append("</url>")
    parts.append("</urlset>")
    parts.append("")
    return "\n".join(parts)


def main() -> None:
    entries = collect_entries()
    if not entries:
        print("build_fr_feeds: no French entries found — nothing to do")
        return
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "rss.xml").write_text(render_rss(entries), encoding="utf-8")
    (OUT / "atom.xml").write_text(render_atom(entries), encoding="utf-8")
    (OUT / "news-sitemap.xml").write_text(render_news_sitemap(entries), encoding="utf-8")
    print(f"build_fr_feeds: wrote {len(entries)} entry feeds (rss.xml + atom.xml + news-sitemap.xml)")


if __name__ == "__main__":
    main()
