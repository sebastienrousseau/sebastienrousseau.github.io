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

# CSP delivery is a defence-in-depth contract: the HTTP response carries a
# permissive header (with 'unsafe-inline') for the securityheaders.com
# grader, and EVERY page additionally carries a strict per-page meta CSP
# with hash-pinned inline script tokens. Browsers enforce the intersection,
# so the strict meta is what actually matters. If the meta CSP is ever
# accidentally removed from the build, the HTTP header alone would silently
# permit inline scripts site-wide. This pass turns that into a build error.
META_CSP_RE = re.compile(
    r'<meta\b[^>]*?http-equiv\s*=\s*["\']?Content-Security-Policy["\']?'
    r'[^>]*?\bcontent\s*=\s*"([^"]+)"',
    re.IGNORECASE,
)
META_CSP_RE_ALT = re.compile(
    r'<meta\b[^>]*?\bcontent\s*=\s*"([^"]+)"'
    r'[^>]*?http-equiv\s*=\s*["\']?Content-Security-Policy["\']?',
    re.IGNORECASE,
)
SCRIPT_SRC_RE = re.compile(r'script-src\s+([^;]+)', re.IGNORECASE)


def _extract_meta_csp(html: str) -> str | None:
    """Return the meta CSP value if present, else None. Tolerates attribute
    order (http-equiv before/after content) and minifier variations."""
    m = META_CSP_RE.search(html) or META_CSP_RE_ALT.search(html)
    return m.group(1) if m else None


def validate_meta_csp(html: str) -> list[str]:
    """Assert the per-page meta CSP exists, has a script-src directive,
    that directive has at least one sha256-* token (hash-pinned inline),
    and does NOT contain 'unsafe-inline' (which would defeat the
    hash-pinning point). Returns a list of error strings — empty if OK."""
    errors: list[str] = []
    csp = _extract_meta_csp(html)
    if csp is None:
        errors.append("meta CSP missing — site relies on it for hash-pinned inline-script enforcement")
        return errors
    m = SCRIPT_SRC_RE.search(csp)
    if m is None:
        errors.append("meta CSP has no script-src directive")
        return errors
    script_src = m.group(1)
    if "'unsafe-inline'" in script_src:
        errors.append("meta CSP script-src contains 'unsafe-inline' — defeats hash-only enforcement")
    if "sha256-" not in script_src:
        errors.append("meta CSP script-src has no sha256-* hash tokens — inline JSON-LD would fail to load")
    return errors

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


_EMPTYABLE_URL_FIELDS = ("url", "href", "image", "sameAs")


def _check_template_leak(body: str, i: int, errors: list[str]) -> None:
    """Flag unresolved {{template}} tokens that escaped the SSG pass."""
    if "{{" in body:
        errors.append(f"block#{i}: unresolved template token ('{{{{' found)")
    elif "}}" in body and body.count("}") != body.count("{"):
        errors.append(f"block#{i}: unresolved template token ('}}}}' found)")


def _check_node_required(type_str: str, node: dict, errors: list[str]) -> None:
    """Assert any required Schema.org properties for this @type are present."""
    required = REQUIRED.get(type_str)
    if not required:
        return
    keys_no_at = {k.lstrip("@") for k in node}
    present = set(node.keys()) | keys_no_at
    missing = required - present
    if missing:
        errors.append(f"{type_str}: missing required {sorted(missing)}")


def _check_node_id_unique(
    type_str: str,
    node: dict,
    ids_seen: set[str],
    warnings: list[str],
) -> None:
    """Track @id values within a page and warn on collisions."""
    nid = node.get("@id")
    if not isinstance(nid, str):
        return
    if nid in ids_seen:
        warnings.append(f"{type_str}: duplicate @id {nid!r}")
    ids_seen.add(nid)


def _check_node_empty_urls(type_str: str, node: dict, errors: list[str]) -> None:
    """Catch the empty-href / empty-src regression that bit us on the Lucy
    post — Schema.org url-shaped fields must never be the literal empty
    string."""
    for key in _EMPTYABLE_URL_FIELDS:
        val = node.get(key)
        if isinstance(val, str) and val.strip() == "":
            errors.append(f"{type_str}.{key} is empty string")
        elif isinstance(val, list) and any(
            isinstance(x, str) and x.strip() == "" for x in val
        ):
            errors.append(f"{type_str}.{key}[] contains empty string")


def _validate_jsonld_block(
    body: str,
    i: int,
    ids_seen: set[str],
    errors: list[str],
    warnings: list[str],
) -> None:
    """Validate a single inline <script type="application/ld+json"> body."""
    _check_template_leak(body, i, errors)
    try:
        data = json.loads(body)
    except json.JSONDecodeError as e:
        errors.append(
            f"block#{i}: invalid JSON ({e.msg} at line {e.lineno} col {e.colno})"
        )
        return
    for type_str, node in iter_typed_nodes(data):
        # Skip pure @id references — pointers to nodes defined elsewhere,
        # not full node definitions.
        keys_no_at = {k.lstrip("@") for k in node}
        if keys_no_at <= {"type", "id"}:
            continue
        _check_node_required(type_str, node, errors)
        _check_node_id_unique(type_str, node, ids_seen, warnings)
        _check_node_empty_urls(type_str, node, errors)


def validate_page(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    raw_html = path.read_text(encoding="utf-8", errors="ignore")
    # Meta-CSP defence check runs against the RAW html — comments shouldn't
    # affect attribute extraction, and the meta tag isn't inside one anyway.
    errors.extend(validate_meta_csp(raw_html))
    # Strip HTML comments first — they can contain literal
    # <script type="application/ld+json"> text (documentation) that we
    # don't want the regex to match as a real script block.
    html = COMMENT_RE.sub('', raw_html)
    blocks = JSONLD_RE.findall(html)
    if not blocks:
        return errors, warnings
    ids_seen: set[str] = set()
    for i, raw in enumerate(blocks):
        _validate_jsonld_block(raw.strip(), i, ids_seen, errors, warnings)
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


# A URL is "tainted" if it's the kind of regression Shokunin keeps shipping:
# localhost host, IPv4 loopback, or a `/.meta/` artefact path. These are the
# exact patterns the postbuild URL-repair pass rewrites — this check is the
# loud failure surface for when that repair stops working.
TAINTED_URL_RE = re.compile(
    r'(?:'
    r'https?://(?:127\.0\.0\.1|localhost)'   # local dev host
    r'|/\.meta(?:/|$)'                       # SSG internal path
    r')',
    re.IGNORECASE,
)

# RFC 822 date used by RSS 2.0 (e.g. "Mon, 11 May 2026 06:06:06 +0000").
# We accept the "Day, DD Mon YYYY HH:MM:SS ±HHMM" shape — Google + most
# feed readers reject anything looser.
RFC822_RE = re.compile(
    r'^(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun), '
    r'\d{2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{4} '
    r'\d{2}:\d{2}:\d{2} (?:[+-]\d{4}|GMT|UTC)$'
)
# RFC 3339 / ISO 8601 date used by Atom + sitemaps
# (e.g. "2026-05-11T06:06:06+00:00" or just "2026-05-11").
RFC3339_RE = re.compile(
    r'^\d{4}-\d{2}-\d{2}'
    r'(?:T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2}))?$'
)


def _check_url_taint(label: str, url: str | None, errors: list[str]) -> None:
    if not url:
        return
    if TAINTED_URL_RE.search(url):
        errors.append(f"{label} contains dev artefact (.meta/ or localhost): {url!r}")


def _check_url_seo(label: str, url: str | None, warnings: list[str]) -> None:
    if not url:
        return
    if url.startswith("http://"):
        warnings.append(f"{label} uses http:// not https:// (mixed-content risk): {url!r}")
    if len(url) > 2048:
        warnings.append(f"{label} exceeds Google's 2048-char URL limit ({len(url)}c)")


def _validate_rss_item(
    item: ET.Element,
    i: int,
    seen_guids: dict[str, int],
    seen_links: dict[str, int],
    errors: list[str],
    warnings: list[str],
) -> None:
    for required in ("title", "link"):
        if item.find(required) is None:
            errors.append(f"rss: item[{i}] missing <{required}>")
    link = (item.findtext("link") or "").strip()
    _check_url_taint(f"rss: item[{i}] <link>", link, errors)
    _check_url_seo(f"rss: item[{i}] <link>", link, warnings)
    guid_el = item.find("guid")
    guid = (guid_el.text or "").strip() if guid_el is not None else ""
    if guid_el is not None:
        _check_url_taint(f"rss: item[{i}] <guid>", guid, errors)
        if guid_el.attrib.get("isPermaLink", "true").lower() != "false":
            _check_url_seo(f"rss: item[{i}] <guid>", guid, warnings)
    # Uniqueness — duplicate guid breaks subscriber-state machinery.
    if guid:
        if guid in seen_guids:
            errors.append(f"rss: item[{i}] duplicate <guid> (also at item[{seen_guids[guid]}])")
        seen_guids[guid] = i
    if link:
        if link in seen_links:
            warnings.append(f"rss: item[{i}] duplicate <link> (also at item[{seen_links[link]}])")
        seen_links[link] = i
    d = (item.findtext("description") or "").strip()
    if d and len(d) < 10:
        warnings.append(f"rss: item[{i}] <description> too short ({len(d)}c, ideal ≥10)")
    pd = (item.findtext("pubDate") or "").strip()
    if pd and not RFC822_RE.match(pd):
        warnings.append(f"rss: item[{i}] <pubDate> not RFC 822: {pd!r}")
    t = (item.findtext("title") or "").strip()
    if len(t) > 200:
        warnings.append(f"rss: item[{i}] <title> very long ({len(t)}c, ideal ≤200)")


def _validate_rss(root: ET.Element, errors: list[str], warnings: list[str]) -> None:
    channel = root.find("channel")
    if channel is None:
        errors.append("rss: missing <channel>")
        return
    for required in ("title", "link", "description"):
        if channel.find(required) is None:
            errors.append(f"rss: channel missing <{required}>")
    desc = channel.findtext("description", "")
    if desc and len(desc.strip()) < 30:
        warnings.append(f"rss: channel description is very short ({len(desc.strip())}c, ideal ≥30)")
    seen_guids: dict[str, int] = {}
    seen_links: dict[str, int] = {}
    for i, item in enumerate(channel.findall("item")):
        _validate_rss_item(item, i, seen_guids, seen_links, errors, warnings)


def _validate_atom_entry(
    entry: ET.Element,
    i: int,
    seen_ids: dict[str, int],
    errors: list[str],
    warnings: list[str],
) -> None:
    for required in ("id", "title", "updated"):
        if entry.find(f"{{{_ATOM_NS}}}{required}") is None:
            errors.append(f"atom: entry[{i}] missing <{required}>")
    eid = (entry.findtext(f"{{{_ATOM_NS}}}id") or "").strip()
    _check_url_taint(f"atom: entry[{i}] <id>", eid, errors)
    if eid:
        if eid in seen_ids:
            errors.append(f"atom: entry[{i}] duplicate <id> (also at entry[{seen_ids[eid]}])")
        seen_ids[eid] = i
    for j, ln in enumerate(entry.findall(f"{{{_ATOM_NS}}}link")):
        href = ln.attrib.get("href", "")
        _check_url_taint(f"atom: entry[{i}] <link>[{j}] href", href, errors)
        _check_url_seo(f"atom: entry[{i}] <link>[{j}] href", href, warnings)
    upd = (entry.findtext(f"{{{_ATOM_NS}}}updated") or "").strip()
    if upd and not RFC3339_RE.match(upd):
        warnings.append(f"atom: entry[{i}] <updated> not RFC 3339: {upd!r}")
    if entry.find(f"{{{_ATOM_NS}}}summary") is None:
        warnings.append(f"atom: entry[{i}] missing <summary> (recommended)")


def _validate_atom(root: ET.Element, errors: list[str], warnings: list[str]) -> None:
    for required in ("id", "title", "updated"):
        if root.find(f"{{{_ATOM_NS}}}{required}") is None:
            errors.append(f"atom: feed missing <{required}>")
    feed_updated = (root.findtext(f"{{{_ATOM_NS}}}updated") or "").strip()
    if feed_updated and not RFC3339_RE.match(feed_updated):
        warnings.append(f"atom: feed <updated> not RFC 3339: {feed_updated!r}")
    seen_ids: dict[str, int] = {}
    for i, entry in enumerate(root.findall(f"{{{_ATOM_NS}}}entry")):
        _validate_atom_entry(entry, i, seen_ids, errors, warnings)


def _validate_news_extension(
    news: ET.Element | None,
    i: int,
    errors: list[str],
    warnings: list[str],
) -> None:
    if news is None:
        errors.append(f"news-sitemap: url[{i}] missing <news:news>")
        return
    title_el = news.find(f"{{{_NEWS_NS}}}title")
    pub = news.find(f"{{{_NEWS_NS}}}publication")
    pubdate = news.find(f"{{{_NEWS_NS}}}publication_date")
    if title_el is None:
        errors.append(f"news-sitemap: url[{i}] news:news missing <news:title>")
    elif title_el.text and len(title_el.text) > 80:
        warnings.append(
            f"news-sitemap: url[{i}] <news:title> exceeds Google's 80-char "
            f"recommendation ({len(title_el.text)}c)"
        )
    if pub is None:
        errors.append(f"news-sitemap: url[{i}] missing <news:publication>")
    else:
        if pub.find(f"{{{_NEWS_NS}}}name") is None:
            errors.append(f"news-sitemap: url[{i}] publication missing <news:name>")
        if pub.find(f"{{{_NEWS_NS}}}language") is None:
            errors.append(f"news-sitemap: url[{i}] publication missing <news:language>")
    if pubdate is None:
        errors.append(f"news-sitemap: url[{i}] missing <news:publication_date>")
    elif pubdate.text and not RFC3339_RE.match(pubdate.text.strip()):
        warnings.append(
            f"news-sitemap: url[{i}] <news:publication_date> not ISO 8601: "
            f"{pubdate.text!r}"
        )
    kw_el = news.find(f"{{{_NEWS_NS}}}keywords")
    if kw_el is not None and kw_el.text:
        kws = [k.strip() for k in kw_el.text.split(",") if k.strip()]
        if len(kws) > 10:
            warnings.append(
                f"news-sitemap: url[{i}] <news:keywords> has {len(kws)} items "
                f"(Google recommends ≤10)"
            )


def _validate_sitemap_url(
    url: ET.Element,
    i: int,
    is_news: bool,
    seen_locs: dict[str, int],
    errors: list[str],
    warnings: list[str],
) -> None:
    loc = url.find(f"{{{_SITEMAP_NS}}}loc")
    loc_text = (loc.text or "").strip() if (loc is not None and loc.text) else ""
    if not loc_text:
        errors.append(f"sitemap: url[{i}] missing <loc>")
        return
    if not loc_text.startswith(("http://", "https://")):
        errors.append(f"sitemap: url[{i}] <loc> is not an absolute URL: {loc_text!r}")
    _check_url_taint(f"sitemap: url[{i}] <loc>", loc_text, errors)
    _check_url_seo(f"sitemap: url[{i}] <loc>", loc_text, warnings)
    if loc_text in seen_locs:
        warnings.append(f"sitemap: url[{i}] duplicate <loc> (also at url[{seen_locs[loc_text]}])")
    seen_locs[loc_text] = i

    lastmod = url.find(f"{{{_SITEMAP_NS}}}lastmod")
    if lastmod is not None and lastmod.text and not RFC3339_RE.match(lastmod.text.strip()):
        warnings.append(f"sitemap: url[{i}] <lastmod> not ISO 8601: {lastmod.text!r}")
    cf = url.findtext(f"{{{_SITEMAP_NS}}}changefreq", "").strip()
    if cf and cf not in {"always", "hourly", "daily", "weekly", "monthly", "yearly", "never"}:
        warnings.append(f"sitemap: url[{i}] <changefreq> not in spec: {cf!r}")
    pr = url.findtext(f"{{{_SITEMAP_NS}}}priority", "").strip()
    if pr:
        try:
            pf = float(pr)
            if not (0.0 <= pf <= 1.0):
                warnings.append(f"sitemap: url[{i}] <priority> outside 0.0–1.0: {pr!r}")
        except ValueError:
            warnings.append(f"sitemap: url[{i}] <priority> not numeric: {pr!r}")
    if is_news:
        _validate_news_extension(url.find(f"{{{_NEWS_NS}}}news"), i, errors, warnings)


def _validate_sitemap(
    root: ET.Element,
    path: Path,
    errors: list[str],
    warnings: list[str],
) -> None:
    is_news = root.find(f"{{{_SITEMAP_NS}}}url/{{{_NEWS_NS}}}news") is not None
    urls = root.findall(f"{{{_SITEMAP_NS}}}url")
    if len(urls) > 50000:
        errors.append(f"sitemap: {len(urls)} URLs exceeds Google's 50,000 limit")
    if path.stat().st_size > 50 * 1024 * 1024:
        errors.append("sitemap: file size exceeds 50MB limit")
    seen_locs: dict[str, int] = {}
    for i, url in enumerate(urls):
        _validate_sitemap_url(url, i, is_news, seen_locs, errors, warnings)


_FEED_HANDLERS = {
    "rss": lambda root, path, errs, warns: _validate_rss(root, errs, warns),
    "feed": lambda root, path, errs, warns: _validate_atom(root, errs, warns),
    "urlset": _validate_sitemap,
}


def validate_feed(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        errors.append(f"XML parse failed: {e}")
        return errors, warnings
    root = tree.getroot()
    handler = _FEED_HANDLERS.get(_localname(root.tag))
    if handler is None:
        warnings.append(f"unknown root element <{_localname(root.tag)}>; skipped feed-specific checks")
        return errors, warnings
    handler(root, path, errors, warnings)
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
