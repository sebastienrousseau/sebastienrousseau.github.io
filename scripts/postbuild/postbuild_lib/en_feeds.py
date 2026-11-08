# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""The English root feeds: one item set for rss.xml, atom.xml and feed.json.

Static Site Generator writes the root rss.xml and atom.xml from every
``_posts/**/*.md``, translations included, and keeps the 50 newest. Each
article has 35 language editions sharing one date, so the root feed held
one or two English items among dozens of translations, and which edition
came first depended on ssg's file-walk order (ssg 0.0.73 changed it). The
translations already have their own feeds under ``/<lang>/`` (see
``scripts/generators/build_lang_feeds.py``), so the root feeds carry the
English articles only.

The item set is every dated ``_posts/*.md`` with a title. Links and guids
keep the values ssg emitted (the front matter ``url``), so a reader that
has already seen an English item does not see it again.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from _frontmatter import parse_frontmatter

BASE = "https://sebastienrousseau.com"
AUTHOR = "contact@sebastienrousseau.com (Sebastien Rousseau)"

# Front matter spells the month in full ("October 28, 2026") or short
# ("Oct 28, 2026"). feed.json once parsed the short form only and dropped
# 61 of 120 articles, silently, including the newest.
_DATE_FORMATS = ("%B %d, %Y", "%b %d, %Y", "%Y-%m-%d")
_DATED_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-")
_RSS_ITEM_RE = re.compile(r"\s*<item>[\s\S]*?</item>", re.IGNORECASE)
_ATOM_ENTRY_RE = re.compile(r"\s*<entry>[\s\S]*?</entry>", re.IGNORECASE)
_AMP_RE = re.compile(r"&(?![a-zA-Z]+;|#\d+;|#x[0-9a-fA-F]+;)")


@dataclass(frozen=True)
class Entry:
    """One English article as the root feeds describe it."""

    stem: str
    url: str
    title: str
    description: str
    banner: str
    keywords: tuple[str, ...]
    date: datetime


def parse_post_date(value: str, source: Path) -> datetime:
    """Midnight UTC on the front matter date. An unparseable date stops
    the build: dropping the post would hide it from every subscriber."""
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(value.strip(), fmt).replace(tzinfo=UTC)
        except ValueError:
            continue
    raise ValueError(f"{source}: unparseable front matter date {value!r}")


def _keywords(raw: str) -> tuple[str, ...]:
    """Comma-separated keywords, trimmed, first occurrence kept."""
    seen: dict[str, None] = {}
    for word in raw.split(","):
        if word.strip():
            seen.setdefault(word.strip(), None)
    return tuple(seen)


def _entry(md: Path) -> Entry | None:
    fm, _body = parse_frontmatter(md.read_text(encoding="utf-8"))
    if not fm.get("title"):
        return None
    return Entry(
        stem=md.stem,
        url=(fm.get("url") or f"{BASE}/{md.stem}").strip(),
        title=fm["title"],
        description=fm.get("description", ""),
        banner=fm.get("banner", ""),
        keywords=_keywords(fm.get("keywords", "")),
        date=parse_post_date(fm.get("date", ""), md),
    )


def english_entries(posts_dir: Path) -> list[Entry]:
    """Every dated English article, newest first; same-day articles in
    reverse file-name order, so the order never depends on a file walk."""
    entries = [
        e
        for md in sorted(posts_dir.glob("*.md"))
        if _DATED_RE.match(md.stem) and (e := _entry(md)) is not None
    ]
    entries.sort(key=lambda e: (e.date, e.stem), reverse=True)
    return entries


def xml_escape(s: str) -> str:
    """Escape text for XML, leaving existing entity references alone."""
    s = _AMP_RE.sub("&amp;", s)
    return s.replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")


def _rfc822(d: datetime) -> str:
    return d.strftime("%a, %d %b %Y %H:%M:%S +0000")


def _iso8601(d: datetime) -> str:
    return d.strftime("%Y-%m-%dT%H:%M:%S+00:00")


def render_rss_item(e: Entry) -> str:
    """One <item>, in the shape ssg emitted for English articles."""
    lines = [
        "    <item>",
        f"      <title>{xml_escape(e.title)}</title>",
        f"      <link>{e.url}</link>",
        f"      <description>{xml_escape(e.description)}</description>",
        f'      <guid isPermaLink="true">{e.url}</guid>',
        f"      <pubDate>{_rfc822(e.date)}</pubDate>",
        f"      <author>{AUTHOR}</author>",
    ]
    if e.banner:
        lines.append(f'      <enclosure url="{e.banner}" type="image/webp" length="0"/>')
    lines.extend(f"      <category>{xml_escape(k)}</category>" for k in e.keywords)
    lines.append("    </item>")
    return "\n".join(lines)


def render_atom_entry(e: Entry) -> str:
    """One <entry> for atom.xml."""
    return "\n".join(
        [
            "  <entry>",
            f"    <title>{xml_escape(e.title)}</title>",
            f'    <link href="{e.url}"/>',
            f"    <id>{e.url}</id>",
            f"    <updated>{_iso8601(e.date)}</updated>",
            f"    <published>{_iso8601(e.date)}</published>",
            f"    <summary>{xml_escape(e.description)}</summary>",
            f"    <author><name>{AUTHOR}</name></author>",
            "  </entry>",
        ]
    )


def replace_blocks(text: str, block_re: re.Pattern[str], close_tag: str, blocks: list[str]) -> str:
    """ssg's feed with its item blocks swapped for ``blocks``. The channel
    header and footer ssg wrote (title, description, self link) stay."""
    stripped = block_re.sub("", text)
    at = stripped.rfind(close_tag)
    if at < 0:
        raise ValueError(f"feed has no {close_tag}")
    body = "".join("\n" + b for b in blocks)
    return stripped[:at].rstrip() + body + "\n" + stripped[at:].lstrip(" ")


def write_en_xml_feeds(public: Path, entries: list[Entry]) -> int:
    """Rewrite the root rss.xml and atom.xml with ``entries``. Returns the
    number of files rewritten (a feed ssg did not write is skipped)."""
    targets = (
        (public / "rss.xml", _RSS_ITEM_RE, "</channel>", render_rss_item),
        (public / "atom.xml", _ATOM_ENTRY_RE, "</feed>", render_atom_entry),
    )
    written = 0
    for path, block_re, close_tag, render in targets:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        blocks = [render(e) for e in entries]
        path.write_text(replace_blocks(text, block_re, close_tag, blocks), encoding="utf-8")
        written += 1
    return written


def write_json_feed(public: Path, entries: list[Entry] | None = None) -> bool:
    """Emit JSON Feed 1.1 at public/feed.json from EN dated posts.

    Same item set as rss.xml / atom.xml (:func:`english_entries`)
    in the JSON Feed format (https://www.jsonfeed.org/version/1.1/). Ids
    and urls keep the trailing-slash form this feed has always published,
    so readers do not see old items again."""
    base = "https://sebastienrousseau.com"
    items: list[dict] = []
    for e in entries if entries is not None else english_entries(Path("_posts")):
        item: dict = {
            "id": f"{base}/{e.stem}/",
            "url": f"{base}/{e.stem}/",
            "title": e.title,
            "summary": e.description,
            "date_published": e.date.isoformat(),
            "language": "en-GB",
            "author": {"name": "Sebastien Rousseau"},
        }
        if e.banner:
            item["image"] = e.banner
        if e.keywords:
            item["tags"] = list(e.keywords)
        items.append(item)
    feed = {
        "version": "https://jsonfeed.org/version/1.1",
        "title": "Sebastien Rousseau — Articles",
        "home_page_url": f"{base}/",
        "feed_url": f"{base}/feed.json",
        "language": "en-GB",
        "icon": "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp",
        "favicon": "https://cloudcdn.pro/clients/sebastienrousseau/favicon.ico",
        "authors": [{"name": "Sebastien Rousseau", "url": f"{base}/about/"}],
        "items": items,
    }
    target = public / "feed.json"
    target.write_text(
        json.dumps(feed, separators=(",", ":"), ensure_ascii=False),
        encoding="utf-8",
    )
    return True


def write_en_feeds(public: Path) -> None:
    """Write the root rss.xml, atom.xml and feed.json from one item set."""
    entries = english_entries(Path("_posts"))
    write_json_feed(public, entries)
    write_en_xml_feeds(public, entries)
