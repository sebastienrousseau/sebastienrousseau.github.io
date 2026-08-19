#!/usr/bin/env python3
"""Emit per-language XML + JSON Feed 1.1 feeds under ``public/<lang>/``.

Static Site Generator's main ``rss.xml`` / ``atom.xml`` / ``news-sitemap.xml`` only
cover the English ``_posts/*.md``. This script mirrors the same shape
for every non-English language whose ``active=True`` Language entry
lives in :mod:`_lang_registry`, so feed readers and Google News see
each translated corpus as a first-class language edition.

Channel-level metadata (title, description, copyright, JSON-Feed
title) comes from ``_data/i18n/<lang>/strings.json`` under the
``feeds.channel*`` / ``feeds.jsonFeedTitle`` keys. Item titles +
descriptions come from each post's frontmatter.

Inputs : ``_posts/<lang>/<lang-slug>.md`` (frontmatter) + the
         EN→<lang> slug map and BCP-47 tag from
         :mod:`_lang_registry`.

Outputs (per active language ≠ EN):
  * ``public/<lang>/rss.xml``
  * ``public/<lang>/atom.xml``
  * ``public/<lang>/news-sitemap.xml``
  * ``public/<lang>/feed.json``

Must run AFTER ``build_translations.py`` (so the translated pages
exist on disk) and BEFORE ``postbuild.py`` (so the feeds get SRI/CSP
treatment if needed and robots.txt picks them up).
"""

from __future__ import annotations

import sys as _sys  # path bootstrap — scripts reorg (scripts/lib/ on sys.path)
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "lib"))

import contextlib
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _lang_registry  # type: ignore[import-not-found]  # script-mode sibling import

PUBLIC = Path("public")
BASE = "https://sebastienrousseau.com"

_DATED_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-")
_FM_KEY_RE = re.compile(r'^([a-zA-Z_]+):\s*(?:"((?:[^"\\]|\\.)*)"|\'((?:[^\'\\]|\\.)*)\')\s*$')


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
            fm[m.group(1)] = m.group(2) if m.group(2) is not None else m.group(3)
    return fm


_DATE_FORMATS = ("%Y-%m-%d", "%B %d, %Y", "%b %d, %Y")


def _parse_date_strptime(s: str) -> datetime | None:
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None


def parse_date(s: str) -> datetime:
    """Parse a frontmatter date string ('October 26, 2023' or '2023-10-26')
    to a tz-aware UTC datetime at 06:06:06 (mirrors Static Site Generator's RSS time)."""
    s = (s or "").strip()
    d = _parse_date_strptime(s) if s else None
    if d is None:
        # Previously this returned datetime.now(), which stamped every
        # unparseable date with the build time and said nothing. That is how
        # 467 posts across 27 locale feeds came to advertise themselves as
        # published at build time, undetected: the <pubDate> was always
        # present and always plausible. A localised-date fallback existed but
        # its regex was month-first while the dates it targeted are day-first
        # ("28 juin 2026"), so it never fired — a silent fallback behind a
        # silent fallback. Raise instead; the build should stop rather than
        # publish a date it had to invent.
        raise ValueError(
            f"unparseable frontmatter date {s!r}; expected ISO 8601 or an "
            "English month name (locale posts inherit the English date — see "
            "scripts/maintenance/fix_locale_date_frontmatter.py)"
        )
    return d.replace(hour=6, minute=6, second=6, tzinfo=UTC)


def collect_entries(lang_code: str) -> list[dict[str, object]]:
    src = Path(f"_posts/{lang_code}")
    if not src.is_dir():
        return []
    slugs = _lang_registry.load_slugs(lang_code).get("articles", {})
    en_to_lang = slugs
    lang_to_en = {v: k for k, v in slugs.items()}
    entries: list[dict[str, object]] = []
    for md in sorted(src.glob("*.md")):
        if not _DATED_RE.match(md.stem):
            continue
        if md.stem in lang_to_en:
            slug = md.stem
        elif md.stem in en_to_lang:
            slug = en_to_lang[md.stem]
        else:
            continue
        fm = parse_frontmatter(md.read_text(encoding="utf-8"))
        if not fm.get("title"):
            continue
        d = parse_date(fm.get("date", ""))
        entries.append(
            {
                "slug": slug,
                "title": fm.get("title", ""),
                "description": fm.get("description", ""),
                "keywords": fm.get("keywords", ""),
                "banner": fm.get("banner", ""),
                "date": d,
                "url": f"{BASE}/{lang_code}/{slug}/",
            }
        )
    entries.sort(key=lambda e: e["date"], reverse=True)  # type: ignore[arg-type, return-value]
    return entries


_AMP_RE = re.compile(r"&(?![a-zA-Z]+;|#\d+;|#x[0-9a-fA-F]+;)")


def xml_escape(s: str) -> str:
    s = _AMP_RE.sub("&amp;", s)
    return s.replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")


def rfc822(d: datetime) -> str:
    return d.strftime("%a, %d %b %Y %H:%M:%S +0000")


def iso8601(d: datetime) -> str:
    return d.strftime("%Y-%m-%dT%H:%M:%S+00:00")


def render_rss(
    entries: list[dict[str, object]], lang_code: str, bcp47: str, strings: dict[str, str]
) -> str:
    today = datetime.now(tz=UTC)
    parts: list[str] = []
    parts.append('<?xml version="1.0" encoding="UTF-8"?>')
    parts.append('<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">')
    parts.append("  <channel>")
    parts.append(f"    <title>{xml_escape(strings.get('feeds.channelTitle', ''))}</title>")
    parts.append(f"    <link>{BASE}/{lang_code}/</link>")
    parts.append(
        f"    <description>{xml_escape(strings.get('feeds.channelDescription', ''))}</description>"
    )
    parts.append(
        f'    <atom:link href="{BASE}/{lang_code}/rss.xml" rel="self" type="application/rss+xml"/>'
    )
    parts.append(f"    <language>{bcp47}</language>")
    parts.append(f"    <lastBuildDate>{rfc822(today)}</lastBuildDate>")
    parts.append(
        f"    <copyright>{xml_escape(strings.get('feeds.channelCopyright', ''))}</copyright>"
    )
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
        keywords = (
            (e.get("keywords") or "").split(",") if isinstance(e.get("keywords"), str) else []
        )
        parts.extend(
            f"      <category>{xml_escape(k)}</category>" for kw in keywords if (k := kw.strip())
        )
        parts.append("    </item>")
    parts.append("  </channel>")
    parts.append("</rss>")
    parts.append("")
    return "\n".join(parts)


def render_atom(
    entries: list[dict[str, object]], lang_code: str, bcp47: str, strings: dict[str, str]
) -> str:
    today = datetime.now(tz=UTC)
    parts: list[str] = []
    parts.append('<?xml version="1.0" encoding="UTF-8"?>')
    parts.append(f'<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="{bcp47}">')
    parts.append(f"  <title>{xml_escape(strings.get('feeds.channelTitle', ''))}</title>")
    parts.append(
        f'  <link href="{BASE}/{lang_code}/atom.xml" rel="self" type="application/atom+xml"/>'
    )
    parts.append(f'  <link href="{BASE}/{lang_code}/"/>')
    parts.append(f"  <id>{BASE}/{lang_code}/</id>")
    parts.append(f"  <updated>{iso8601(today)}</updated>")
    for e in entries:
        parts.append("  <entry>")
        parts.append(f"    <title>{xml_escape(e['title'])}</title>")  # type: ignore[arg-type]
        parts.append(f'    <link href="{e["url"]}"/>')
        parts.append(f"    <id>{e['url']}</id>")
        parts.append(f"    <updated>{iso8601(e['date'])}</updated>")  # type: ignore[arg-type]
        parts.append(f"    <published>{iso8601(e['date'])}</published>")  # type: ignore[arg-type]
        parts.append(f"    <summary>{xml_escape(e['description'])}</summary>")  # type: ignore[arg-type]
        parts.append(
            "    <author><name>contact@sebastienrousseau.com (Sebastien Rousseau)</name></author>"
        )
        parts.append("  </entry>")
    parts.append("</feed>")
    parts.append("")
    return "\n".join(parts)


# A Google News sitemap must contain only articles published in the last 48
# hours (plus a little forward tolerance for timezone skew); anything older is
# a spec violation Search Console reports as an error. The per-locale feeds
# emitted every article ever published — /fr/news-sitemap.xml shipped 84 KB of
# months-old entries — because this renderer reused the unfiltered feed entry
# list. Mirror the window build_news_sitemap.py already applies to the root.
_NEWS_WINDOW_PAST_S = 48 * 3600
_NEWS_WINDOW_FUTURE_S = -7200  # 2 h of forward timezone skew

# Fallback when a locale's strings.json carries no feeds.channelTitle. Same
# constant as build_news_sitemap.py: a publication NAME, never a contact
# address. Every locale news sitemap previously named the publication
# "contact@sebastienrousseau.com (Sebastien Rousseau)" — the author
# front-matter string — which is what Google News would have displayed.
_DEFAULT_PUB_NAME = "Sebastien Rousseau Research"


def _resolve_pub_name(lang_code: str) -> str:
    """Localised publication name from ``feeds.channelTitle`` if present, else
    the canonical English brand string. Tolerates a missing or partial
    strings.json — a syndication surface must not fail the build."""
    with contextlib.suppress(Exception):
        strings = _lang_registry.load_strings(lang_code)
        if strings.get("feeds.channelTitle"):
            return str(strings["feeds.channelTitle"])
    return _DEFAULT_PUB_NAME


def _within_news_window(entry: dict[str, object], now: datetime) -> bool:
    date = entry.get("date")
    if not isinstance(date, datetime):
        return False
    delta = (now - date).total_seconds()
    return _NEWS_WINDOW_FUTURE_S <= delta <= _NEWS_WINDOW_PAST_S


def render_news_sitemap(
    entries: list[dict[str, object]],
    bcp47: str,
    pub_name: str = _DEFAULT_PUB_NAME,
    now: datetime | None = None,
) -> str:
    now = now or datetime.now(tz=UTC)
    entries = [e for e in entries if _within_news_window(e, now)]
    parts: list[str] = []
    parts.append('<?xml version="1.0" encoding="UTF-8"?>')
    parts.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')
    parts.append('        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">')
    for e in entries:
        parts.append("<url>")
        parts.append(f"  <loc>{e['url']}</loc>")
        parts.append("  <news:news>")
        parts.append("    <news:publication>")
        parts.append(f"      <news:name>{xml_escape(pub_name)}</news:name>")
        parts.append(f"      <news:language>{bcp47}</news:language>")
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


def render_json_feed(
    entries: list[dict[str, object]], lang_code: str, bcp47: str, strings: dict[str, str]
) -> str:
    """JSON Feed 1.1 (https://www.jsonfeed.org/version/1.1/)."""
    items = []
    for e in entries:
        d = e["date"]
        item: dict[str, object] = {
            "id": e["url"],
            "url": e["url"],
            "title": e["title"],
            "summary": e["description"],
            "date_published": iso8601(d) if isinstance(d, datetime) else "",
            "language": bcp47,
            "author": {"name": "Sebastien Rousseau"},
        }
        banner = e.get("banner")
        if banner:
            item["image"] = banner
        tags_raw = e.get("keywords")
        if isinstance(tags_raw, str) and tags_raw.strip():
            item["tags"] = [t.strip() for t in tags_raw.split(",") if t.strip()]
        items.append(item)
    # Author URL uses the localized "about" slug when known, falls back to /<lang>/.
    static_slugs = _lang_registry.load_slugs(lang_code).get("static", {})
    about_slug = static_slugs.get("about", "")
    author_url = f"{BASE}/{lang_code}/{about_slug}/" if about_slug else f"{BASE}/{lang_code}/"
    feed: dict[str, object] = {
        "version": "https://jsonfeed.org/version/1.1",
        "title": strings.get("feeds.jsonFeedTitle", strings.get("feeds.channelTitle", "")),
        "home_page_url": f"{BASE}/{lang_code}/",
        "feed_url": f"{BASE}/{lang_code}/feed.json",
        "language": bcp47,
        "icon": "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp",
        "favicon": "https://cloudcdn.pro/clients/sebastienrousseau/favicon.ico",
        "authors": [{"name": "Sebastien Rousseau", "url": author_url}],
        "items": items,
    }
    return json.dumps(feed, separators=(",", ":"), ensure_ascii=False)


def build_for_lang(lang_code: str) -> int:
    """Build all four feed artefacts for the given language. Returns the
    number of items emitted. No-op (returns 0) if no posts exist."""
    lang = next((lg for lg in _lang_registry.LANGUAGES if lg.code == lang_code), None)
    if lang is None or lang.code == "en":
        return 0
    entries = collect_entries(lang_code)
    if not entries:
        return 0
    strings = _lang_registry.load_strings(lang_code)
    out = PUBLIC / lang_code
    out.mkdir(parents=True, exist_ok=True)
    (out / "rss.xml").write_text(
        render_rss(entries, lang_code, lang.bcp47, strings), encoding="utf-8"
    )
    (out / "atom.xml").write_text(
        render_atom(entries, lang_code, lang.bcp47, strings), encoding="utf-8"
    )
    (out / "news-sitemap.xml").write_text(
        render_news_sitemap(entries, lang.bcp47, _resolve_pub_name(lang_code)),
        encoding="utf-8",
    )
    (out / "feed.json").write_text(
        render_json_feed(entries, lang_code, lang.bcp47, strings), encoding="utf-8"
    )
    return len(entries)


def main() -> None:
    total_entries = 0
    built: list[str] = []
    for lang in _lang_registry.LANGUAGES:
        if not lang.active or lang.code == "en":
            continue
        n = build_for_lang(lang.code)
        if n:
            total_entries += n
            built.append(f"{lang.code}={n}")
    if not built:
        print("build_lang_feeds: no non-EN active languages with posts — nothing to do")
        return
    print(
        f"build_lang_feeds: wrote feeds for {len(built)} language(s) "
        f"({', '.join(built)}); {total_entries} total entries "
        f"(rss.xml + atom.xml + news-sitemap.xml + feed.json each)"
    )


if __name__ == "__main__":
    main()
