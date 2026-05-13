#!/usr/bin/env python3
"""Lightweight structured-data + feed validator for the built tree.

Two passes, both surfacing the exact failure modes we've already hit on
this site (so the next regression fails CI instead of shipping).

Pass 1 — Schema.org JSON-LD inside *.html
  - malformed JSON inside <script type="application/ld+json">
  - missing required fields on the @types we use
  - broken URLs (empty href="" / src="" leaking back in)
  - duplicate @id collisions across the graph
  - unresolved {{template}} placeholders that escaped the SSG pass

Pass 2 — XML feeds (*.xml)
  - XML well-formedness via xml.etree (catches bare `&` regressions, the
    Shokunin RSS double-escape, malformed nesting, etc.)
  - RSS feeds: every channel has title + link + description, every item
    has title + link
  - Atom feeds: feed-level id + title + updated; every entry has id +
    title + updated
  - Sitemap: every <url> has a <loc>; every <loc> is a parseable URL
  - News sitemap: every <url> has a <news:news> child

This is not a full spec validator — for that, Google's Rich Results
Test and the W3C Feed Validation Service exist as web tools.

Run:
    python3 scripts/validate_jsonld.py [--base-dir public|docs]

Exits non-zero if any page or feed has a hard error; warnings are
reported but don't fail the build.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

JSONLD_RE = re.compile(
    r'<script[^>]*type=["\']?application/ld\+json["\']?[^>]*>([\s\S]*?)</script>',
    re.IGNORECASE,
)
COMMENT_RE = re.compile(r'<!--[\s\S]*?-->')

# Required-property table per @type. Keep narrow — false positives are
# more expensive than missing a real issue, and the Rich Results Test
# covers the wider spec.
REQUIRED: dict[str, set[str]] = {
    "BlogPosting":      {"headline", "author", "datePublished"},
    "Article":          {"headline", "author", "datePublished"},
    "NewsArticle":      {"headline", "author", "datePublished"},
    "Person":           {"name"},
    "Organization":     {"name"},
    "WebSite":          {"name", "url"},
    "WebPage":          {"name"} ,
    "ImageObject":      {"url"},
    "BreadcrumbList":   {"itemListElement"},
    "ListItem":         {"position", "name"},
    "ItemList":         {"itemListElement"},
    "FAQPage":          {"mainEntity"},
    "Question":         {"name", "acceptedAnswer"},
    "Answer":           {"text"},
    "ProfilePage":      {"mainEntity"},
    "SpeakableSpecification": {"cssSelector"},
}


def iter_typed_nodes(obj, parent_key=None):
    """Yield (type_str, node) tuples for every Schema.org node we can find,
    recursing into @graph arrays and child objects."""
    if isinstance(obj, dict):
        t = obj.get("@type")
        if isinstance(t, str):
            yield t, obj
        elif isinstance(t, list):
            for s in t:
                if isinstance(s, str):
                    yield s, obj
        for k, v in obj.items():
            yield from iter_typed_nodes(v, parent_key=k)
    elif isinstance(obj, list):
        for item in obj:
            yield from iter_typed_nodes(item, parent_key=parent_key)


def validate_page(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    html = path.read_text(encoding="utf-8", errors="ignore")
    # Strip HTML comments first — they can contain literal
    # <script type="application/ld+json"> text (documentation) that we
    # don't want the regex to match as a real script block.
    html = COMMENT_RE.sub('', html)
    blocks = JSONLD_RE.findall(html)
    if not blocks:
        return errors, warnings

    ids_seen: set[str] = set()
    for i, raw in enumerate(blocks):
        body = raw.strip()
        # Unresolved templating leaking through.
        if "{{" in body or "}}" in body and not body.count("}") == body.count("{"):
            errors.append(f"block#{i}: unresolved template token ({'{{' if '{{' in body else '}}'} found)")
        try:
            data = json.loads(body)
        except json.JSONDecodeError as e:
            errors.append(f"block#{i}: invalid JSON ({e.msg} at line {e.lineno} col {e.colno})")
            continue

        for type_str, node in iter_typed_nodes(data):
            # Skip pure @id references — these are pointers to a node
            # defined elsewhere (in the same graph or another page), not
            # full node definitions.
            keys_no_at = {k.lstrip("@") for k in node.keys()}
            if keys_no_at <= {"type", "id"}:
                continue
            required = REQUIRED.get(type_str)
            if required:
                present = set(node.keys()) | keys_no_at
                missing = required - present
                if missing:
                    errors.append(f"{type_str}: missing required {sorted(missing)}")
            # @id uniqueness within the page.
            nid = node.get("@id")
            if isinstance(nid, str):
                if nid in ids_seen:
                    warnings.append(f"{type_str}: duplicate @id {nid!r}")
                ids_seen.add(nid)
            # Empty url/href detection.
            for key in ("url", "href", "image", "sameAs"):
                val = node.get(key)
                if isinstance(val, str) and val.strip() == "":
                    errors.append(f"{type_str}.{key} is empty string")
                elif isinstance(val, list):
                    if any(isinstance(x, str) and x.strip() == "" for x in val):
                        errors.append(f"{type_str}.{key}[] contains empty string")

    return errors, warnings


# ---------------------------------------------------------------------------
# Pass 2 — XML feed validation
# ---------------------------------------------------------------------------

# Atom namespace. RSS doesn't use a namespace; news-sitemap uses several.
_ATOM_NS = "http://www.w3.org/2005/Atom"
_SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
_NEWS_NS = "http://www.google.com/schemas/sitemap-news/0.9"


def _localname(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def validate_feed(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        errors.append(f"XML parse failed: {e}")
        return errors, warnings

    root = tree.getroot()
    root_local = _localname(root.tag)
    name = path.name

    if root_local == "rss":
        # RSS 2.0 layout: <rss><channel>...<item>*</channel></rss>
        channel = root.find("channel")
        if channel is None:
            errors.append("rss: missing <channel>")
            return errors, warnings
        for required in ("title", "link", "description"):
            if channel.find(required) is None:
                errors.append(f"rss: channel missing <{required}>")
        for i, item in enumerate(channel.findall("item")):
            for required in ("title", "link"):
                if item.find(required) is None:
                    errors.append(f"rss: item[{i}] missing <{required}>")

    elif root_local == "feed":
        # Atom layout (namespaced).
        for required in ("id", "title", "updated"):
            if root.find(f"{{{_ATOM_NS}}}{required}") is None:
                errors.append(f"atom: feed missing <{required}>")
        for i, entry in enumerate(root.findall(f"{{{_ATOM_NS}}}entry")):
            for required in ("id", "title", "updated"):
                if entry.find(f"{{{_ATOM_NS}}}{required}") is None:
                    errors.append(f"atom: entry[{i}] missing <{required}>")

    elif root_local == "urlset":
        # sitemap.xml or news-sitemap.xml
        is_news = root.find(f"{{{_SITEMAP_NS}}}url/{{{_NEWS_NS}}}news") is not None
        for i, url in enumerate(root.findall(f"{{{_SITEMAP_NS}}}url")):
            loc = url.find(f"{{{_SITEMAP_NS}}}loc")
            if loc is None or not (loc.text and loc.text.strip()):
                errors.append(f"sitemap: url[{i}] missing <loc>")
                continue
            if not loc.text.strip().startswith(("http://", "https://")):
                errors.append(f"sitemap: url[{i}] <loc> is not an absolute URL: {loc.text!r}")
            lastmod = url.find(f"{{{_SITEMAP_NS}}}lastmod")
            if lastmod is not None and lastmod.text:
                # Basic ISO-ish shape check.
                if not re.match(r"^\d{4}-\d{2}-\d{2}", lastmod.text.strip()):
                    warnings.append(
                        f"sitemap: url[{i}] <lastmod> not ISO 8601: {lastmod.text!r}"
                    )
            if is_news:
                news = url.find(f"{{{_NEWS_NS}}}news")
                if news is None:
                    errors.append(f"news-sitemap: url[{i}] missing <news:news>")

    else:
        warnings.append(f"unknown root element <{root_local}>; skipped feed-specific checks")

    return errors, warnings


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--base-dir", default="public",
                   help="HTML tree to validate (default: public)")
    args = p.parse_args()
    base = Path(args.base_dir)
    if not base.is_dir():
        print(f"ERROR: {base} not found", file=sys.stderr)
        return 2

    pages = sorted(base.rglob("*.html"))
    total_errors = 0
    total_warnings = 0
    failed_pages = 0
    for page in pages:
        errs, warns = validate_page(page)
        if errs or warns:
            rel = page.relative_to(base).as_posix()
            for e in errs:
                print(f"ERROR  {rel}: {e}")
            for w in warns:
                print(f"WARN   {rel}: {w}")
            total_errors += len(errs)
            total_warnings += len(warns)
            if errs:
                failed_pages += 1

    feeds = sorted(base.glob("*.xml"))
    failed_feeds = 0
    feed_errors = 0
    feed_warnings = 0
    for feed in feeds:
        errs, warns = validate_feed(feed)
        if errs or warns:
            rel = feed.relative_to(base).as_posix()
            for e in errs:
                print(f"ERROR  {rel}: {e}")
            for w in warns:
                print(f"WARN   {rel}: {w}")
            feed_errors += len(errs)
            feed_warnings += len(warns)
            if errs:
                failed_feeds += 1

    print()
    print(
        f"validate: {len(pages)} HTML pages, "
        f"{failed_pages} with structured-data errors "
        f"({total_errors} err, {total_warnings} warn). "
        f"{len(feeds)} XML feeds, "
        f"{failed_feeds} with errors "
        f"({feed_errors} err, {feed_warnings} warn)."
    )
    return 1 if (total_errors or feed_errors) else 0


if __name__ == "__main__":
    sys.exit(main())
