"""Site-level output emitters: robots.txt, llms.txt, llms-full.txt,
JSON Feed, XML feed URL fix, XML feed entity-escape, sitemap lastmod
refresh + per-language sitemap splice.

This module owns everything that runs once at the end of postbuild
(after the per-page injection loop). Each public entry-point takes
``PUBLIC`` as a parameter so the orchestrator doesn't have to set a
module-level constant.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import _lang_registry as _lr  # type: ignore[import-not-found]


def _all_active_non_en_langs() -> list[str]:
    """Locally-scoped copy of the helper defined in postbuild.py — keeps
    this module independent of the orchestrator."""
    return [lg.code for lg in _lr.LANGUAGES if lg.active and lg.code != "en"]


# ---------------------------------------------------------------------------
# 6a. robots.txt — explicit AI crawler rules
# ---------------------------------------------------------------------------
#
# Default robots.txt that SSG emits is just "User-agent: *" + Sitemap. The
# spec for major AI crawlers is to keep separate User-agent blocks rather
# than rely on the wildcard, so each ML team can be addressed independently
# in future without rewriting the whole file. We allow all AI crawlers
# because the goal is broad LLM citation; flip any line to `Disallow: /`
# to opt out of that specific bot.
ROBOTS_BODY = """User-agent: *
Allow: /

# Web search + general-purpose crawlers
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: DuckDuckBot
Allow: /

User-agent: Slurp
Allow: /

User-agent: Yandex
Allow: /

User-agent: Baiduspider
Allow: /

User-agent: Applebot
Allow: /

User-agent: AhrefsBot
Allow: /

User-agent: SemrushBot
Allow: /

User-agent: facebookexternalhit
Allow: /

User-agent: Twitterbot
Allow: /

User-agent: LinkedInBot
Allow: /

# AI / LLM crawlers — broad citation rather than blanket block. Flip any
# block to `Disallow: /` to opt out per-bot.
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: Amazonbot
Allow: /

User-agent: AmazonbotCommerce
Allow: /

User-agent: Bytespider
Allow: /

User-agent: cohere-ai
Allow: /

User-agent: CCBot
Allow: /

User-agent: ImagesiftBot
Allow: /

User-agent: Diffbot
Allow: /

User-agent: meta-externalagent
Allow: /

User-agent: meta-externalfetcher
Allow: /

User-agent: facebook-externalhit-llama
Allow: /

User-agent: MistralAI-User
Allow: /

User-agent: YouBot
Allow: /

Sitemap: https://sebastienrousseau.com/sitemap.xml
Sitemap: https://sebastienrousseau.com/news-sitemap.xml
Sitemap: https://sebastienrousseau.com/fr/news-sitemap.xml

# llms.txt: https://sebastienrousseau.com/llms.txt
# llms-full: https://sebastienrousseau.com/llms-full.txt
"""


def write_robots(public: Path) -> bool:
    target = public / "robots.txt"
    cur = target.read_text(encoding="utf-8") if target.is_file() else ""
    if cur.strip() == ROBOTS_BODY.strip():
        return False
    target.write_text(ROBOTS_BODY, encoding="utf-8")
    return True


# ---------------------------------------------------------------------------
# 6b. llms.txt — structured directory for AI crawlers
# ---------------------------------------------------------------------------


def build_llms_txt() -> str:
    """Render llms.txt — a curated index designed for LLM consumption.
    Format: H1 site name + summary, then bulleted sections for the
    canonical entry points (home, articles, papers, projects, topics,
    about, contact).
    """
    base = "https://sebastienrousseau.com"
    out: list[str] = []
    out.append("# Sebastien Rousseau")
    out.append("")
    out.append(
        "AI, banking and financial services expert. Senior payments leader "
        "at HSBC Commercial & Investment Bank. Twenty years across Tier-1 "
        "banks (HSBC, PayPal, Barclays) and consumer technology (Shazam, "
        "AKQA, Virgin Group). Applied AI, ISO 20022 migration, wholesale "
        "payments and post-quantum cryptography for financial services."
    )
    out.append("")
    out.append("## Canonical entry points")
    out.append("")
    out.append(f"- [Home]({base}/) — landing page with the latest research and projects.")
    out.append(f"- [About]({base}/about/) — full biography, professional history, areas of expertise.")
    out.append(f"- [Articles]({base}/articles/) — research notes on quantum-safe cryptography, ISO 20022, applied AI, wholesale payments.")
    out.append(f"- [Papers]({base}/papers/) — industry white papers, peer-reviewed analysis, regulatory submissions.")
    out.append(f"- [Projects]({base}/projects/) — open-source Python and Rust libraries for payments, post-quantum crypto, AI tooling.")
    out.append(f"- [Topics]({base}/topics/) — topic hubs: post-quantum, ISO 20022, applied AI, Rust, blockchain.")
    out.append(f"- [Playlists]({base}/playlists/) — curated music libraries for deep work and engineering flow.")
    out.append(f"- [Contact]({base}/contact/) — professional contact form for consulting, speaking, advisory engagements.")
    out.append("")
    out.append("## Feeds")
    out.append("")
    out.append(f"- [RSS feed]({base}/rss.xml)")
    out.append(f"- [Atom feed]({base}/atom.xml)")
    out.append(f"- [JSON Feed 1.1]({base}/feed.json)")
    out.append(f"- [News sitemap]({base}/news-sitemap.xml)")
    out.append(f"- [Sitemap]({base}/sitemap.xml)")
    out.append(f"- [French RSS]({base}/fr/rss.xml)")
    out.append(f"- [French sitemap]({base}/fr/news-sitemap.xml)")
    out.append("")
    out.append("## Areas of expertise")
    out.append("")
    out.append("- Applied artificial intelligence in banking")
    out.append("- Generative AI for financial services")
    out.append("- Wholesale payments")
    out.append("- ISO 20022 migration")
    out.append("- SWIFT gpi")
    out.append("- SEPA Instant Payments")
    out.append("- Cross-border payments")
    out.append("- Post-quantum cryptography for financial services")
    out.append("- CRYSTALS-Kyber, CRYSTALS-Dilithium")
    out.append("- Quantum-safe payment authentication")
    out.append("")
    out.append("## Contact")
    out.append("")
    out.append("Sebastien Rousseau (London, UK)")
    out.append("")
    out.append("- LinkedIn: https://www.linkedin.com/in/sebastienrousseau/")
    out.append("- Twitter / X: https://twitter.com/wwdseb")
    out.append("- Medium: https://medium.com/@BankingOnQuantum")
    out.append("- YouTube: https://www.youtube.com/@BankingOnQuantum")
    out.append("- GitHub: https://github.com/sebastienrousseau")
    out.append("- Newsletter: https://news.bankingonquantum.com")
    out.append("")
    return "\n".join(out)


def write_llms_txt(public: Path) -> bool:
    target = public / "llms.txt"
    new = build_llms_txt()
    cur = target.read_text(encoding="utf-8") if target.is_file() else ""
    if cur == new:
        return False
    target.write_text(new, encoding="utf-8")
    return True


def build_llms_full_txt(public: Path) -> str:
    """Render llms-full.txt — the full text of every article concatenated
    in chronological (newest-first) order. Drops navigation furniture so
    LLM ingestion gets just the substantive prose.
    """
    posts_dir = Path("_posts")
    if not posts_dir.is_dir():
        return ""
    posts: list[tuple[str, Path, dict[str, str], str]] = []
    for md in sorted(posts_dir.glob("2*-*-*.md"), reverse=True):
        fm = _parse_frontmatter(md)
        if not fm.get("title"):
            continue
        text = md.read_text(encoding="utf-8")
        # Strip frontmatter
        sep_count = 0
        body_start = 0
        for i, line in enumerate(text.splitlines(keepends=True)):
            if line.strip() == "---":
                sep_count += 1
                if sep_count == 2:
                    body_start = i + 1
                    break
        body = "".join(text.splitlines(keepends=True)[body_start:])
        # Drop the enrich block (Last reviewed + Related grid)
        body = re.sub(r"<!-- enrich-start -->[\s\S]*?<!-- enrich-end -->", "", body)
        body = re.sub(r"<aside\b[\s\S]*?</aside>", "", body)
        body = body.strip()
        posts.append((md.stem, md, fm, body))

    lines: list[str] = []
    lines.append("# Sebastien Rousseau — full article corpus")
    lines.append("")
    lines.append(
        "Every article on sebastienrousseau.com, newest-first, with "
        "navigation furniture stripped. Provided for LLM ingestion under "
        "Apache-2.0 attribution. See https://sebastienrousseau.com/ for "
        "the canonical formatting."
    )
    lines.append("")
    for stem, _md, fm, body in posts:
        title = fm.get("title", stem)
        url = f"https://sebastienrousseau.com/{stem}/"
        date = fm.get("date", "")
        lines.append(f"## {title}")
        lines.append("")
        if date:
            lines.append(f"_{date}_  ·  [{url}]({url})")
            lines.append("")
        lines.append(body)
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append("")
    return "\n".join(lines)


def write_json_feed(public: Path) -> bool:
    """Emit JSON Feed 1.1 at public/feed.json from EN dated posts.

    Mirrors the data in rss.xml / atom.xml but in the modern JSON
    Feed format (https://www.jsonfeed.org/version/1.1/). Most modern
    feed-reader clients prefer this — same item set, smaller payload,
    easier to parse than XML."""
    items: list[dict] = []
    posts_dir = Path("_posts")
    base = "https://sebastienrousseau.com"
    for md in sorted(posts_dir.glob("2*-*-*.md")):
        fm = _parse_frontmatter(md)
        if not fm.get("title"):
            continue
        date_str = fm.get("date", "")
        try:
            parsed = datetime.strptime(date_str, "%b %d, %Y").replace(tzinfo=UTC)
        except ValueError:
            continue
        item: dict = {
            "id": f"{base}/{md.stem}/",
            "url": f"{base}/{md.stem}/",
            "title": fm.get("title", ""),
            "summary": fm.get("description", ""),
            "date_published": parsed.isoformat(),
            "language": "en-GB",
            "author": {"name": "Sebastien Rousseau"},
        }
        banner = fm.get("banner", "")
        if banner:
            item["image"] = banner
        keywords = fm.get("keywords", "")
        if keywords:
            item["tags"] = [t.strip() for t in keywords.split(",") if t.strip()]
        items.append(item)
    items.sort(key=lambda i: i["date_published"], reverse=True)
    feed = {
        "version": "https://jsonfeed.org/version/1.1",
        "title": "Sebastien Rousseau — Articles",
        "home_page_url": f"{base}/",
        "feed_url": f"{base}/feed.json",
        "language": "en-GB",
        "icon": "https://cloudcdn.pro/stocks/images/sebastien-rousseau.png",
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


def _parse_frontmatter(md: Path) -> dict[str, str]:
    """Minimal YAML-style frontmatter parser. Same shape as the FR
    feeds helper."""
    out: dict[str, str] = {}
    text = md.read_text(encoding="utf-8")
    lines = text.splitlines()
    inside = False
    sep = 0
    for line in lines:
        s = line.strip()
        if s == "---":
            sep += 1
            inside = sep == 1
            if sep == 2:
                break
            continue
        if not inside:
            continue
        m = re.match(r'^([a-z_-]+):\s*"((?:[^"\\]|\\.)*)"\s*$', s)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def write_llms_full_txt(public: Path) -> bool:
    target = public / "llms-full.txt"
    new = build_llms_full_txt(public)
    if not new:
        return False
    cur = target.read_text(encoding="utf-8") if target.is_file() else ""
    if cur == new:
        return False
    target.write_text(new, encoding="utf-8")
    return True


# ---------------------------------------------------------------------------
# 6c. XML feed URL rewrite — repair Shokunin RSS/Atom/news-sitemap output
# ---------------------------------------------------------------------------


_FEED_URL_FIX_RE = re.compile(
    r"https?://(?:127\.0\.0\.1(?::\d+)?|localhost(?::\d+)?)"
    r"(?:/[^\"<\s]*)?",
)


def _build_title_index() -> dict[str, str]:
    """Walk _posts/ once; return ``{slug: title}`` for every dated post."""
    out: dict[str, str] = {}
    posts_dir = Path("_posts")
    if not posts_dir.is_dir():
        return out
    for md in posts_dir.glob("2*-*-*.md"):
        fm = _parse_frontmatter(md)
        if "title" in fm:
            out[md.stem] = fm["title"]
    return out


def _decode_entities(s: str) -> str:
    """Decode the handful of XML entities we encounter in Shokunin's
    feed output."""
    return (
        s.replace("&amp;amp;", "&amp;")
        .replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
        .replace("&apos;", "'")
    )


def _patch_block(block: str, title_index: dict[str, str]) -> str:
    """Rewrite localhost / .meta/ URLs inside a single <item> /
    <entry> / <url> XML block."""

    def _fix_url(m: re.Match[str]) -> str:
        bad = m.group(0)
        # Look for a /<dated-slug>/ component in the URL
        slug_m = re.search(r"/(2\d{3}-\d{2}-\d{2}-[a-z0-9-]+)(?:/|$)", bad)
        if not slug_m:
            return "https://sebastienrousseau.com/"
        return f"https://sebastienrousseau.com/{slug_m.group(1)}/"

    return _FEED_URL_FIX_RE.sub(_fix_url, block)


def fix_xml_feed_urls(public: Path) -> int:
    """Repair localhost/.meta/ URLs Shokunin sometimes bakes into the
    RSS / Atom / news-sitemap output."""
    title_index = _build_title_index()
    n = 0
    for xml in [public / "rss.xml", public / "atom.xml", public / "news-sitemap.xml"]:
        if not xml.is_file():
            continue
        text = xml.read_text(encoding="utf-8")
        new = _patch_block(text, title_index)
        if new != text:
            xml.write_text(new, encoding="utf-8")
            n += 1
    return n


# ---------------------------------------------------------------------------
# 6d. XML feed entity-escape pass — scrub bare ampersands in titles
# ---------------------------------------------------------------------------


_VALID_ENTITY_RE = re.compile(r'&(amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);')
_DOUBLE_ESCAPE_RE = re.compile(r'&amp;(amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);')


def escape_xml_ampersands(text: str) -> str:
    """Repair XML feed ampersands two ways:

    1. Un-double-escape ``&amp;<entity>;`` back to ``&<entity>;``
       (Shokunin's bug on the RSS channel-level <title>).
    2. Replace bare ``&`` with ``&amp;``, leaving valid entity
       references alone.

    Walks the string in one pass after the double-escape repair.
    """
    text = _DOUBLE_ESCAPE_RE.sub(r'&\1;', text)
    out: list[str] = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch == '&':
            m = _VALID_ENTITY_RE.match(text, i)
            if m:
                out.append(m.group(0))
                i = m.end()
                continue
            out.append('&amp;')
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
                "</loc>", f"</loc>\n  {new_lastmod}", 1,
            )
        if new_block != block:
            n += 1
        return new_block

    xml = _URL_BLOCK_RE.sub(_patch, xml)
    xml = _splice_fr_urls(xml, index)
    sitemap_path.write_text(xml, encoding="utf-8")
    return n


def _splice_fr_urls(xml: str, lastmod_index: dict[str, str]) -> str:  # noqa: C901 — multi-lang sitemap splicer touches every static + article slug per active lang
    """Ensure the sitemap contains every EN + FR article + the static
    landing pages. Shokunin's sitemap.xml ships empty (regression) so we
    splice the missing URLs in here. Idempotent — re-runs don't dupe."""
    base = "https://sebastienrousseau.com"
    existing_locs = {m.group(1).strip() for m in _LOC_RE.finditer(xml)}
    new_blocks: list[str] = []
    seen: set[str] = set()

    def _add(url: str, priority: str, changefreq: str, lastmod: str = "") -> None:
        if url in existing_locs or url in seen:
            return
        seen.add(url)
        lm_line = f"\n  <lastmod>{lastmod}</lastmod>" if lastmod else ""
        new_blocks.append(
            f"<url>\n  <loc>{url}</loc>{lm_line}\n"
            f"  <changefreq>{changefreq}</changefreq>\n"
            f"  <priority>{priority}</priority>\n</url>"
        )

    _add(f"{base}/", "1.0", "daily")
    for slug in (
        "about", "articles", "papers", "projects", "topics", "tags",
        "playlists", "contact", "accessibility", "privacy", "terms",
        "made-with-shokunin", "made-with-static-site-generator",
        "resources-pacs008-checklist",
    ):
        _add(f"{base}/{slug}/", "0.6", "monthly")

    for topic in (
        "post-quantum-cryptography", "iso-20022-payments",
        "applied-ai-banking", "rust-open-source", "blockchain-digital-assets",
    ):
        _add(f"{base}/topics/{topic}/", "0.6", "monthly")

    posts_dir = Path("_posts")
    if posts_dir.is_dir():
        for md in sorted(posts_dir.glob("2*.md")):
            stem = md.stem
            lastmod = lastmod_index.get(stem, "")
            _add(f"{base}/{stem}/", "0.8", "weekly", lastmod)

    for _code in _all_active_non_en_langs():
        _slugs = _lr.load_slugs(_code)
        _statics = _slugs.get("static", {})
        _articles = _slugs.get("articles", {})
        _topics_slug = _statics.get("topics", "topics")
        _articles_slug = _statics.get("articles", "articles")
        _add(f"{base}/{_code}/", "0.8", "weekly")
        _add(f"{base}/{_code}/{_articles_slug}/", "0.7", "weekly")
        for _en_static, _lang_static in _statics.items():
            if _en_static in ("articles", "topics"):
                continue
            _add(f"{base}/{_code}/{_lang_static}/", "0.5", "monthly")
        _add(f"{base}/{_code}/{_topics_slug}/", "0.5", "monthly")
        for topic in (
            "post-quantum-cryptography", "iso-20022-payments",
            "applied-ai-banking", "rust-open-source", "blockchain-digital-assets",
        ):
            _add(f"{base}/{_code}/{_topics_slug}/{topic}/", "0.6", "monthly")
        for _en_art_slug, _lang_slug in _articles.items():
            _add(f"{base}/{_code}/{_lang_slug}/", "0.7", "monthly", lastmod_index.get(_en_art_slug, ""))

    if not new_blocks:
        return xml
    insertion = "\n" + "\n".join(new_blocks) + "\n"
    return xml.replace("</urlset>", insertion + "</urlset>", 1)
