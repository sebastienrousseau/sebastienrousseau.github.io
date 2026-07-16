"""XML feed / sitemap post-processing for the built site.

Repairs and de-duplicates the ssg-emitted RSS/Atom/JSON feeds, the news-
sitemap, and the sitemap index; splices rendered + per-language URLs. Split
out of postbuild_lib.output (Phase 4.1); imports the two shared helpers it
needs from that module.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from datetime import datetime
from pathlib import Path

from postbuild_lib.output import _all_active_non_en_langs, _lr, _parse_frontmatter

# ---------------------------------------------------------------------------
# 6c. XML feed URL rewrite — repair Static Site Generator RSS/Atom/news-sitemap output
# ---------------------------------------------------------------------------


_TITLE_INSIDE_RE = re.compile(
    r"<(?:title|news:title)[^>]*>([\s\S]*?)</(?:title|news:title)>",
    re.IGNORECASE,
)
_RSS_ITEM_RE = re.compile(r"<item>[\s\S]*?</item>", re.IGNORECASE)
_ATOM_ENTRY_RE = re.compile(r"<entry>[\s\S]*?</entry>", re.IGNORECASE)
_NEWS_URL_RE = re.compile(r"<url>[\s\S]*?</url>", re.IGNORECASE)


def _build_title_index() -> dict[str, str]:
    """title -> canonical https://… URL, derived from _posts frontmatter.

    Walks both the top-level English ``_posts/*.md`` AND every
    per-language subtree ``_posts/<lang>/*.md`` so the per-entry rewrite
    in :func:`fix_xml_feed_urls` can find a URL for translated titles
    too. Without the per-language pass, Static Site Generator's atom feed would keep
    `<link href=".meta/<lang>/">` placeholders for every translation.
    """
    idx: dict[str, str] = {}
    posts_dir = Path("_posts")
    if not posts_dir.is_dir():
        return idx
    # English: _posts/*.md (top level)
    for md in posts_dir.glob("*.md"):
        fm = _parse_frontmatter(md)
        title = fm.get("title")
        url = fm.get("url")
        if title and url:
            _index_title(idx, title, url.strip())
    # Per-language: _posts/<lang>/<slug>.md. Frontmatter `url:` is
    # frequently the EN URL (translators copy from source) — so we
    # synthesise the per-language URL from the post's filesystem path
    # instead of trusting frontmatter. That avoids feed-entry guid
    # collisions where multiple translations all point at the EN URL.
    for md in posts_dir.glob("*/*.md"):
        fm = _parse_frontmatter(md)
        title = fm.get("title")
        if not title:
            continue
        lang = md.parent.name
        slug = md.stem
        url = f"https://sebastienrousseau.com/{lang}/{slug}/index.html"
        _index_title(idx, title, url)
    return idx


def _index_title(idx: dict[str, str], title: str, url: str) -> None:
    """Insert title → url under the title's plain form plus the two
    XML-escaped variants (``&amp;`` for ampersand, ``&apos;`` for
    apostrophe) so feed-entry lookups hit regardless of escape style."""
    t = title.strip()
    idx[t] = url
    idx[t.replace("&", "&amp;")] = url
    idx[t.replace("'", "&apos;")] = url
    # Both substitutions can co-occur if a title carries both characters.
    idx[t.replace("&", "&amp;").replace("'", "&apos;")] = url


def _decode_entities(s: str) -> str:
    return (
        s.replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
        .replace("&apos;", "'")
        .strip()
    )


def _patch_block(block: str, title_index: dict[str, str]) -> str:
    tm = _TITLE_INSIDE_RE.search(block)
    if not tm:
        return block
    title_raw = tm.group(1)
    title_clean = _decode_entities(title_raw)
    url = title_index.get(title_clean) or title_index.get(title_raw.strip())
    if not url:
        return block

    # Replace any URL inside this block that either has a localhost host or
    # has /.meta/ anywhere in its path — that's the Static Site Generator bug signature.
    bad_url = (
        r"https?://"
        r"(?:"
        # localhost host (any path)
        r'(?:127\.0\.0\.1|localhost)(?::\d+)?[^<\s"]*'
        # OR any host with a /.meta/ path segment
        r'|[^<\s"]*?/\.meta(?:/[^<\s"]*)?'
        r")"
    )

    def rewrite_url(m: re.Match[str]) -> str:
        return m.group(1) + url + m.group(3)

    block = re.sub(rf"(>\s*)({bad_url})(\s*<)", rewrite_url, block)
    block = re.sub(rf'(="\s*)({bad_url})(\s*")', rewrite_url, block)
    return block


def fix_xml_feed_urls(public: Path) -> int:
    """Repair localhost/.meta/ URLs Static Site Generator sometimes bakes into the
    RSS / Atom / news-sitemap output."""
    title_index = _build_title_index()
    if not title_index:
        return 0
    patched = 0
    for xml in public.glob("*.xml"):
        original = xml.read_text(encoding="utf-8", errors="ignore")
        text = original

        # Per-item / per-entry / per-url URL rewrites.
        if "<item>" in text.lower():
            text = _RSS_ITEM_RE.sub(lambda m: _patch_block(m.group(0), title_index), text)
        if "<entry>" in text.lower():
            text = _ATOM_ENTRY_RE.sub(lambda m: _patch_block(m.group(0), title_index), text)
        if "<news:" in text.lower():
            text = _NEWS_URL_RE.sub(lambda m: _patch_block(m.group(0), title_index), text)

        # Strip any residual <url>…</url> block whose <loc> still has the
        # dev-artefact /.meta/ path — those entries come from Static Site Generator
        # processing the nested _posts/fr/ directory and don't belong in
        # the news-sitemap.
        text = re.sub(
            r"<url>\s*<loc>[^<]*\/\.meta\/[^<]*</loc>[\s\S]*?</url>\s*",
            "",
            text,
        )

        # Top-of-feed cleanup: any residual localhost reference becomes the
        # production root. Done last so it doesn't shadow per-block matches.
        text = re.sub(
            r"https?://(?:127\.0\.0\.1|localhost)(?::\d+)?",
            "https://sebastienrousseau.com",
            text,
        )

        if text != original:
            xml.write_text(text, encoding="utf-8")
            patched += 1
    return patched


# ---------------------------------------------------------------------------
# 6d. XML feed entity-escape pass — scrub bare ampersands in titles
# ---------------------------------------------------------------------------


_VALID_ENTITY_RE = re.compile(r"&(amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);")
_DOUBLE_ESCAPE_RE = re.compile(r"&amp;(amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);")


def escape_xml_ampersands(text: str) -> str:
    """Repair XML feed ampersands two ways:

    1. Un-double-escape ``&amp;<entity>;`` back to ``&<entity>;``
       (Static Site Generator's bug on the RSS channel-level <title>).
    2. Replace bare ``&`` with ``&amp;``, leaving valid entity
       references alone.

    Walks the string in one pass after the double-escape repair.
    """
    text = _DOUBLE_ESCAPE_RE.sub(r"&\1;", text)
    out: list[str] = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch == "&":
            m = _VALID_ENTITY_RE.match(text, i)
            if m:
                out.append(m.group(0))
                i = m.end()
                continue
            out.append("&amp;")
            i += 1
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def fix_xml_feeds(public: Path) -> int:
    """Scrub bare ``&`` inside RSS / Atom / news-sitemap titles."""
    n = 0
    for xml in [public / "rss.xml", public / "atom.xml", public / "news-sitemap.xml"]:
        if not xml.is_file():
            continue
        text = xml.read_text(encoding="utf-8")
        new = escape_xml_ampersands(text)
        if new != text:
            xml.write_text(new, encoding="utf-8")
            n += 1
    return n


# Detect and strip duplicate <item>/<entry>/<url> blocks emitted by the upstream
# SSG when many translation files share the same publication date — the
# generator can collapse multiple locale files onto the same per-item URL
# instead of emitting distinct per-locale URLs, producing identical-by-link
# duplicates that fail xmlls/lib2-news validation downstream.
_RSS_ITEM_RE = re.compile(r"<item>[\s\S]*?</item>", re.IGNORECASE)
_ATOM_ENTRY_RE = re.compile(r"<entry>[\s\S]*?</entry>", re.IGNORECASE)
_SITEMAP_URL_RE = re.compile(r"<url>[\s\S]*?</url>", re.IGNORECASE)
_LINK_RE = re.compile(r"<link[^>]*>([\s\S]*?)</link>", re.IGNORECASE)
_ATOM_LINK_HREF_RE = re.compile(r'<link[^>]*\bhref="([^"]+)"', re.IGNORECASE)
_LOC_RE = re.compile(r"<loc>([\s\S]*?)</loc>", re.IGNORECASE)


def _dedupe_blocks(
    text: str, block_re: re.Pattern[str], key_fn: Callable[[str], str]
) -> tuple[str, int]:
    """Walk ``block_re`` matches in order, keep the first occurrence of each
    ``key_fn(block)`` value, drop subsequent duplicates. Returns (new_text,
    dropped_count). Non-block content is preserved verbatim."""
    seen: set[str] = set()
    out: list[str] = []
    cursor = 0
    dropped = 0
    for m in block_re.finditer(text):
        out.append(text[cursor : m.start()])
        block = m.group(0)
        key = key_fn(block)
        if key and key in seen:
            dropped += 1
        else:
            if key:
                seen.add(key)
            out.append(block)
        cursor = m.end()
    out.append(text[cursor:])
    return "".join(out), dropped


def _rss_key(block: str) -> str:
    m = _LINK_RE.search(block)
    return m.group(1).strip() if m else ""


def _atom_key(block: str) -> str:
    # Prefer the self/alternate <link href="…"> form used in Atom entries.
    for m in _ATOM_LINK_HREF_RE.finditer(block):
        href = m.group(1).strip()
        if href:
            return href
    return ""


def _sitemap_key(block: str) -> str:
    m = _LOC_RE.search(block)
    return m.group(1).strip() if m else ""


def dedupe_xml_feeds(public: Path) -> int:
    """Drop duplicate <item>/<entry>/<url> blocks from RSS / Atom /
    news-sitemap. Dedup key is the canonical URL (link/href/loc). Returns
    the count of files actually rewritten."""
    n = 0
    targets = [
        (public / "rss.xml", _RSS_ITEM_RE, _rss_key),
        (public / "atom.xml", _ATOM_ENTRY_RE, _atom_key),
        (public / "news-sitemap.xml", _SITEMAP_URL_RE, _sitemap_key),
    ]
    for xml, block_re, key_fn in targets:
        if not xml.is_file():
            continue
        text = xml.read_text(encoding="utf-8")
        new, dropped = _dedupe_blocks(text, block_re, key_fn)
        if dropped:
            xml.write_text(new, encoding="utf-8")
            n += 1
    return n


_SITE = "https://sebastienrousseau.com"

# Pages excluded from sitemap by convention. Keep in sync with
# scripts/test_sitemap_completeness.py.
_SITEMAP_EXCLUDE_TAILS = (
    "/404/",
    "/offline/",
    "/thanks/",
    "/fr/404/",
    "/fr/hors-ligne/",
    "/fr/merci/",
)
_SITEMAP_EXCLUDE_PREFIXES = ("/labs/",)


def _normalise_url(url: str) -> str:
    url = url.rstrip()
    if url.endswith("/index.html"):
        url = url[: -len("/index.html")]
    return url.rstrip("/")


def _path_excluded_from_sitemap(path: str) -> bool:
    """Mirror the exclude policy used by test_sitemap_completeness."""
    if any(path.startswith(p) for p in _SITEMAP_EXCLUDE_PREFIXES):
        return True
    return any(path.startswith(tail) or path == tail.rstrip("/") for tail in _SITEMAP_EXCLUDE_TAILS)


def _collect_sitemap_urls(text: str) -> set[str]:
    return {_normalise_url(m.group(1)) for m in re.finditer(r"<loc>([^<]+)</loc>", text)}


def _missing_rendered_urls(public: Path, existing: set[str]) -> list[str]:
    """Walk ``public/`` for index.html files; return canonical URLs not
    yet in the sitemap and not in the exclude policy."""
    additions: list[str] = []
    for html in sorted(public.rglob("index.html")):
        rel = html.relative_to(public).as_posix()
        path = "/" + rel[: -len("index.html")]  # always ends with '/'
        if _path_excluded_from_sitemap(path):
            continue
        url = f"{_SITE}{path}"
        if _normalise_url(url) in existing:
            continue
        additions.append(url)
        existing.add(_normalise_url(url))
    return additions


def augment_sitemap_with_rendered_pages(public: Path) -> int:
    """Append any rendered ``public/**/index.html`` page that is not yet
    listed in ``public/sitemap.xml``.

    Why this exists: the upstream SSG generates sitemap.xml before our
    Python post-pipeline runs. Topic-cluster pages and per-locale topic
    forks are written *after* ssg, so they're absent from the initial
    sitemap. Without this pass, ``test_sitemap_completeness`` fails on
    every new cluster.

    Emits the canonical pretty URL (``/<slug>/``) — the ``/index.html``
    form is a search-engine duplicate that hurts crawl budget.

    Returns the count of `<url>` entries appended."""
    sitemap = public / "sitemap.xml"
    if not sitemap.is_file():
        return 0
    text = sitemap.read_text(encoding="utf-8")
    additions = _missing_rendered_urls(public, _collect_sitemap_urls(text))
    if not additions:
        return 0
    m = re.search(r"<lastmod>(\d{4}-\d{2}-\d{2})</lastmod>", text)
    today = m.group(1) if m else ""
    # `additions` already ends with `/` — the canonical pretty URL.
    block = "".join(
        f"\n<url>\n  <changefreq>weekly</changefreq>\n"
        f"  <lastmod>{today}</lastmod>\n  <loc>{u}</loc>\n</url>"
        for u in additions
    )
    new_text = re.sub(r"</urlset>\s*$", block + "\n</urlset>\n", text, count=1)
    sitemap.write_text(new_text, encoding="utf-8")
    return len(additions)


_URL_BLOCK_FOR_DEDUP_RE = re.compile(r"<url>[\s\S]*?</url>", re.MULTILINE)


def dedupe_sitemap_index_html(sitemap_path: Path) -> int:
    """Normalise every ``<loc>`` in the sitemap to the canonical pretty
    URL form (``/<path>/``), dropping the legacy ``/<path>/index.html``
    variant.

    Why this exists: the upstream SSG ships every page as
    ``<loc>...slug/index.html</loc>`` with a generic homepage-stub
    ``<lastmod>``. Postbuild's ``_splice_fr_urls`` adds the canonical
    pretty URL (``/<slug>/``) with the article's actual last-reviewed
    date. The two coexist until this pass cleans them up — Google
    treats them as separate URLs and the stale lastmod tells the
    crawler the page hasn't changed since 2024.

    Two cases:

    - **Twin exists** (both ``/<path>/`` and ``/<path>/index.html`` are
      present): drop the ``/index.html`` block. The pretty form already
      carries the right ``lastmod`` and ``priority``.
    - **Orphan** (only ``/<path>/index.html`` is present): rewrite its
      ``<loc>`` to the pretty form in place. Preserves the block's
      other metadata (``lastmod``, ``changefreq``, ``priority``).

    Returns the count of ``<url>`` blocks rewritten or removed."""
    if not sitemap_path.is_file():
        return 0
    text = sitemap_path.read_text(encoding="utf-8")
    pretty_urls: set[str] = set()
    for m in _LOC_RE.finditer(text):
        loc = m.group(1).strip()
        if loc.endswith("/") and not loc.endswith("/index.html"):
            pretty_urls.add(loc)
    touched = 0

    def _patch(m: re.Match[str]) -> str:
        nonlocal touched
        block = m.group(0)
        loc_m = _LOC_RE.search(block)
        if not loc_m:
            return block
        loc = loc_m.group(1).strip()
        if not loc.endswith("/index.html"):
            return block
        pretty = loc[: -len("index.html")]
        if pretty in pretty_urls:
            # Twin exists — drop the duplicate /index.html block entirely.
            touched += 1
            return ""
        # Orphan — rewrite this block's <loc> to the pretty URL in place.
        touched += 1
        pretty_urls.add(pretty)
        return block.replace(f"<loc>{loc}</loc>", f"<loc>{pretty}</loc>", 1)

    new_text = _URL_BLOCK_FOR_DEDUP_RE.sub(_patch, text)
    # Collapse the blank lines left behind by dropped blocks.
    new_text = re.sub(r"\n{3,}", "\n\n", new_text)
    if touched > 0:
        sitemap_path.write_text(new_text, encoding="utf-8")
    return touched


_NEWS_TITLE_RE = re.compile(r"(<news:title>)([\s\S]*?)(</news:title>)", re.IGNORECASE)
_NEWS_KEYWORDS_RE = re.compile(r"(<news:keywords>)([\s\S]*?)(</news:keywords>)", re.IGNORECASE)


def _truncate_news_title(title: str, limit: int = 80) -> str:
    """Google News recommends news:title ≤ 80 chars. Truncate at the
    last word boundary inside the limit; append a single ``…`` so the
    reader sees the title was clipped."""
    if len(title) <= limit:
        return title
    cut = title[: limit - 1]
    # Back up to the last space so we don't split a word mid-syllable.
    sp = cut.rfind(" ")
    if sp > limit // 2:
        cut = cut[:sp]
    return cut.rstrip(" ,;:.") + "…"


def _limit_news_keywords(kws: str, limit: int = 10) -> str:
    """Google News recommends news:keywords ≤ 10 items."""
    items = [k.strip() for k in kws.split(",") if k.strip()]
    if len(items) <= limit:
        return kws
    return ", ".join(items[:limit])


def shrink_news_sitemap(public: Path) -> int:
    """Bring news-sitemap.xml within Google News' recommended bounds:
    ``news:title`` ≤ 80 chars and ``news:keywords`` ≤ 10 items.

    Returns the count of files actually rewritten (0 or 1)."""
    xml = public / "news-sitemap.xml"
    if not xml.is_file():
        return 0
    text = xml.read_text(encoding="utf-8")
    original = text
    text = _NEWS_TITLE_RE.sub(
        lambda m: m.group(1) + _truncate_news_title(m.group(2)) + m.group(3), text
    )
    text = _NEWS_KEYWORDS_RE.sub(
        lambda m: m.group(1) + _limit_news_keywords(m.group(2)) + m.group(3), text
    )
    if text == original:
        return 0
    xml.write_text(text, encoding="utf-8")
    return 1


# ---------------------------------------------------------------------------
# 6e. Sitemap lastmod refresh + per-language splice
# ---------------------------------------------------------------------------


def build_lastmod_index() -> dict[str, str]:
    """Walk _posts/, return ``{slug: last_reviewed}`` (falling back to
    the post's date if last_reviewed isn't set)."""
    out: dict[str, str] = {}
    posts_dir = Path("_posts")
    if not posts_dir.is_dir():
        return out
    for md in posts_dir.glob("2*-*-*.md"):
        fm = _parse_frontmatter(md)
        last = fm.get("last_reviewed") or ""
        if not last:
            try:
                last = datetime.strptime(fm.get("date", ""), "%b %d, %Y").strftime("%Y-%m-%d")
            except ValueError:
                continue
        out[md.stem] = last
    return out


_URL_BLOCK_RE = re.compile(r"<url>[\s\S]*?</url>", re.IGNORECASE)
_LOC_RE = re.compile(r"<loc>([^<]+)</loc>", re.IGNORECASE)
_LASTMOD_RE = re.compile(r"<lastmod>[^<]+</lastmod>", re.IGNORECASE)


def refresh_sitemap_lastmod(sitemap_path: Path, index: dict[str, str]) -> int:
    """Rewrite ``<lastmod>`` for every dated post in the sitemap to
    its ``last_reviewed`` value. Also splices missing per-lang URLs
    so every active non-EN language's full slug tree is present."""
    if not sitemap_path.is_file():
        return 0
    xml = sitemap_path.read_text(encoding="utf-8")
    n = 0

    def _patch(m: re.Match[str]) -> str:
        nonlocal n
        block = m.group(0)
        loc_m = _LOC_RE.search(block)
        if not loc_m:
            return block
        loc = loc_m.group(1).strip()
        slug_m = re.search(r"/(2\d{3}-\d{2}-\d{2}-[a-z0-9-]+)/?$", loc)
        if not slug_m:
            return block
        slug = slug_m.group(1)
        if slug not in index:
            return block
        new_lastmod = f"<lastmod>{index[slug]}</lastmod>"
        if _LASTMOD_RE.search(block):
            new_block = _LASTMOD_RE.sub(new_lastmod, block, count=1)
        else:
            new_block = block.replace(
                "</loc>",
                f"</loc>\n  {new_lastmod}",
                1,
            )
        if new_block != block:
            n += 1
        return new_block

    xml = _URL_BLOCK_RE.sub(_patch, xml)
    xml = _splice_fr_urls(xml, index)
    sitemap_path.write_text(xml, encoding="utf-8")
    return n


_SITEMAP_BASE = "https://sebastienrousseau.com"
_STATIC_SLUGS = (
    "about",
    "articles",
    # "papers" is deliberately absent: it is a redirect page to /research
    # (postbuild_lib.redirects) and must not be spliced into the sitemap.
    "suite",
    "research",
    "library",
    "projects",
    "topics",
    "tags",
    "playlists",
    "contact",
    "accessibility",
    "privacy",
    "terms",
    "made-with-static-site-generator",
    "made-with-static-site-generator",
    "resources-pacs008-checklist",
)
_TOPIC_SLUGS = (
    "post-quantum-cryptography",
    "iso-20022-payments",
    "applied-ai-banking",
    "rust-open-source",
    "blockchain-digital-assets",
)


def _url_block(url: str, priority: str, changefreq: str, lastmod: str = "") -> str:
    lm_line = f"\n  <lastmod>{lastmod}</lastmod>" if lastmod else ""
    return (
        f"<url>\n  <loc>{url}</loc>{lm_line}\n"
        f"  <changefreq>{changefreq}</changefreq>\n"
        f"  <priority>{priority}</priority>\n</url>"
    )


def _en_sitemap_urls(lastmod_index: dict[str, str]) -> list[tuple[str, str, str, str]]:
    """Return ``(url, priority, changefreq, lastmod)`` tuples for the EN tree."""
    out: list[tuple[str, str, str, str]] = [(f"{_SITEMAP_BASE}/", "1.0", "daily", "")]
    out.extend((f"{_SITEMAP_BASE}/{slug}/", "0.6", "monthly", "") for slug in _STATIC_SLUGS)
    out.extend((f"{_SITEMAP_BASE}/topics/{topic}/", "0.6", "monthly", "") for topic in _TOPIC_SLUGS)
    posts_dir = Path("_posts")
    if posts_dir.is_dir():
        out.extend(
            (f"{_SITEMAP_BASE}/{md.stem}/", "0.8", "weekly", lastmod_index.get(md.stem, ""))
            for md in sorted(posts_dir.glob("2*.md"))
        )
    return out


def _lang_sitemap_urls(code: str, lastmod_index: dict[str, str]) -> list[tuple[str, str, str, str]]:
    """Return ``(url, priority, changefreq, lastmod)`` tuples for a single
    non-EN language tree (home + statics + topics + articles)."""
    slugs = _lr.load_slugs(code)
    statics = slugs.get("static", {})
    articles = slugs.get("articles", {})
    topics_slug = statics.get("topics", "topics")
    articles_slug = statics.get("articles", "articles")
    out: list[tuple[str, str, str, str]] = [
        (f"{_SITEMAP_BASE}/{code}/", "0.8", "weekly", ""),
        (f"{_SITEMAP_BASE}/{code}/{articles_slug}/", "0.7", "weekly", ""),
    ]
    out.extend(
        (f"{_SITEMAP_BASE}/{code}/{lang_static}/", "0.5", "monthly", "")
        for en_static, lang_static in statics.items()
        if en_static not in ("articles", "topics")
    )
    out.append((f"{_SITEMAP_BASE}/{code}/{topics_slug}/", "0.5", "monthly", ""))
    out.extend(
        (f"{_SITEMAP_BASE}/{code}/{topics_slug}/{topic}/", "0.6", "monthly", "")
        for topic in _TOPIC_SLUGS
    )
    out.extend(
        (
            f"{_SITEMAP_BASE}/{code}/{lang_slug}/",
            "0.7",
            "monthly",
            lastmod_index.get(en_art_slug, ""),
        )
        for en_art_slug, lang_slug in articles.items()
    )
    return out


def _splice_fr_urls(xml: str, lastmod_index: dict[str, str]) -> str:
    """Splice every missing EN + non-EN URL into Static Site Generator's sitemap.xml,
    which ships empty. Idempotent — re-runs don't dupe."""
    existing_locs = {m.group(1).strip() for m in _LOC_RE.finditer(xml)}
    seen: set[str] = set()
    new_blocks: list[str] = []

    candidates: list[tuple[str, str, str, str]] = _en_sitemap_urls(lastmod_index)
    for code in _all_active_non_en_langs():
        candidates.extend(_lang_sitemap_urls(code, lastmod_index))

    for url, priority, changefreq, lastmod in candidates:
        if url in existing_locs or url in seen:
            continue
        seen.add(url)
        new_blocks.append(_url_block(url, priority, changefreq, lastmod))

    if not new_blocks:
        return xml
    insertion = "\n" + "\n".join(new_blocks) + "\n"
    return xml.replace("</urlset>", insertion + "</urlset>", 1)
