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

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import _lang_registry as _lr  # type: ignore[import-not-found]


def _all_active_non_en_langs() -> list[str]:
    """Locally-scoped copy of the helper defined in postbuild.py — keeps
    this module independent of the orchestrator."""
    return [lg.code for lg in _lr.LANGUAGES if lg.active and lg.code != "en"]


# ---------------------------------------------------------------------------
# 6a. robots.txt — explicit per-category crawler stance
# ---------------------------------------------------------------------------
#
# Default robots.txt that SSG emits is just "User-agent: *" + Sitemap. We
# replace it with an explicit per-bot taxonomy so each crawler family
# (search / social preview / AI retrieval / AI training / SEO audit) can
# be addressed and reasoned about independently — and so the stance is
# legible to humans, not just bots.
#
# Current stance: ALLOW everywhere. Goal is broad LLM citation under the
# CC BY-4.0 license posted at /about/#bot-policy. Flip any block to
# `Disallow: /` to opt out per-bot — the categorisation makes the
# trade-off visible at the point of decision.
ROBOTS_BODY = """# Crawler policy for sebastienrousseau.com
# Human-readable version: https://sebastienrousseau.com/about/#bot-policy
# License of crawled content: CC BY-4.0 — attribution required.

User-agent: *
Allow: /

# -- Web search engines -----------------------------------------------------
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

# -- Social / link-preview --------------------------------------------------
User-agent: facebookexternalhit
Allow: /

User-agent: Twitterbot
Allow: /

User-agent: LinkedInBot
Allow: /

# -- SEO audit / link-graph crawlers ---------------------------------------
User-agent: AhrefsBot
Allow: /

User-agent: SemrushBot
Allow: /

# -- AI retrieval (cite-on-query) ------------------------------------------
# These crawlers fetch on user-query and surface citations. Highest-signal
# bots for the site's distribution strategy.
User-agent: ChatGPT-User
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: Claude-User
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: MistralAI-User
Allow: /

User-agent: YouBot
Allow: /

# -- AI training crawlers ---------------------------------------------------
# Broad-ingest model-training bots. Allowed under CC BY-4.0; attribution
# requested per /about/#bot-policy. Flip any line to `Disallow: /` to
# opt out of that specific corpus.
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: Google-Extended
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

User-agent: meta-externalagent
Allow: /

User-agent: meta-externalfetcher
Allow: /

User-agent: facebook-externalhit-llama
Allow: /

# -- Specialised indexers ---------------------------------------------------
User-agent: ImagesiftBot
Allow: /

User-agent: Diffbot
Allow: /

# -- Sitemaps ---------------------------------------------------------------
Sitemap: https://sebastienrousseau.com/sitemap.xml
Sitemap: https://sebastienrousseau.com/news-sitemap.xml
Sitemap: https://sebastienrousseau.com/fr/news-sitemap.xml

# -- Machine-readable surfaces ---------------------------------------------
# llms.txt        — navigation index for LLM ingestion (llmstxt.org)
# llms-ctx.txt    — compact agent-context format (URLs + one-line context)
# llms-full.txt   — full article corpus, navigation-stripped
# api/agents/     — JSON API: posts, topics, person, organization
# Bot policy      — https://sebastienrousseau.com/about/#bot-policy

# llms.txt:       https://sebastienrousseau.com/llms.txt
# llms-ctx.txt:   https://sebastienrousseau.com/llms-ctx.txt
# llms-full.txt:  https://sebastienrousseau.com/llms-full.txt
# Agent API:      https://sebastienrousseau.com/api/agents/index.json
"""


def write_robots(public: Path) -> bool:
    target = public / "robots.txt"
    cur = target.read_text(encoding="utf-8") if target.is_file() else ""
    if cur.strip() == ROBOTS_BODY.strip():
        return False
    target.write_text(ROBOTS_BODY, encoding="utf-8")
    return True


# ---------------------------------------------------------------------------
# 6a-ii. humans.txt + security.txt — copy the source files into public/
# ---------------------------------------------------------------------------
#
# Shokunin emits empty placeholder humans.txt + security.txt at the site root
# regardless of source. The canonical RFC-9116 disclosure file lives at
# /.well-known/security.txt and the human-readable colophon at /humans.txt
# — both authored in the repo root. This pass copies them through so they
# survive the SSG's auxiliary-file emission. Idempotent.

def _copy_through(public: Path, source_root: Path, name: str) -> bool:
    src = source_root / name
    dst = public / name
    if not src.is_file():
        return False
    src_body = src.read_text(encoding="utf-8")
    cur = dst.read_text(encoding="utf-8") if dst.is_file() else ""
    if cur == src_body:
        return False
    dst.write_text(src_body, encoding="utf-8")
    return True


def write_humans(public: Path, source_root: Path) -> bool:
    """Copy the repo-root humans.txt over the SSG's empty placeholder."""
    return _copy_through(public, source_root, "humans.txt")


def write_security_txt(public: Path, source_root: Path) -> bool:
    """Copy the repo-root security.txt over the SSG's empty placeholder so the
    RFC 9116 file is reachable at both `/security.txt` (root) and the canonical
    `/.well-known/security.txt`. Security scanners check both locations."""
    return _copy_through(public, source_root, "security.txt")


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


def build_llms_ctx_txt() -> str:
    """Render llms-ctx.txt — the compact "agent context" companion to
    llms.txt designed to drop directly into an LLM context window.

    Per the llmstxt.org convention, llms-ctx.txt strips marketing prose
    and groups the site's machine-readable surfaces into terse
    URL + one-line description pairs. The audience is a tool-using
    agent that wants to know "where do I look?" — not a human reader.

    Structure: site identity → primary content URLs → feeds / JSON
    endpoints → author profile → bot policy. Every line is either a
    URL or a one-line description tied to a URL.
    """
    base = "https://sebastienrousseau.com"
    out: list[str] = []
    out.append("# Sebastien Rousseau — agent context")
    out.append("")
    out.append(
        "Compact reference for LLM/agent ingestion. URLs + one-line "
        "descriptions; no marketing prose. Crawl policy: "
        "CC BY-4.0, attribution requested. See /about/#bot-policy."
    )
    out.append("")
    out.append("## Content")
    out.append(f"- {base}/                — Home: latest research and projects.")
    out.append(f"- {base}/about/          — Biography, credentials (ORCID 0009-0005-1434-284X).")
    out.append(f"- {base}/articles/       — Research notes: PQC, ISO 20022, payments, applied AI.")
    out.append(f"- {base}/papers/         — White papers, peer-reviewed analysis, regulatory submissions.")
    out.append(f"- {base}/projects/       — Open-source Python and Rust libraries.")
    out.append(f"- {base}/topics/         — Topic hubs: post-quantum, ISO 20022, applied AI, Rust, blockchain.")
    out.append(f"- {base}/contact/        — Professional contact form.")
    out.append("")
    out.append("## Feeds")
    out.append(f"- {base}/llms.txt        — Site directory (llmstxt.org navigation format).")
    out.append(f"- {base}/llms-full.txt   — Full article corpus, navigation-stripped.")
    out.append(f"- {base}/sitemap.xml     — All URLs, with hreflang per locale.")
    out.append(f"- {base}/news-sitemap.xml — Last 48 h news entries.")
    out.append(f"- {base}/rss.xml         — RSS feed.")
    out.append(f"- {base}/atom.xml        — Atom feed.")
    out.append(f"- {base}/feed.json       — JSON Feed 1.1.")
    out.append("")
    out.append("## JSON API")
    out.append(f"- {base}/api/agents/index.json        — Endpoint index + crawl policy.")
    out.append(f"- {base}/api/agents/posts.json        — Every dated post with metadata.")
    out.append(f"- {base}/api/agents/topics.json       — Curated topic clusters.")
    out.append(f"- {base}/api/agents/person.json       — Author (Person + ORCID + hasCredential).")
    out.append(f"- {base}/api/agents/organization.json — Publisher (Organization + Brand).")
    out.append("")
    out.append("## Author")
    out.append("- Sebastien Rousseau, London, UK.")
    out.append("- Senior payments leader, 20+ years at Tier-1 banks (HSBC, PayPal, Barclays).")
    out.append("- ORCID: https://orcid.org/0009-0005-1434-284X")
    out.append("- GitHub: https://github.com/sebastienrousseau")
    out.append("- LinkedIn: https://www.linkedin.com/in/sebastienrousseau/")
    out.append("")
    out.append("## Bot policy")
    out.append("- Allow: all categories (web search, social, AI retrieval, AI training, indexers).")
    out.append("- License: CC BY-4.0 — attribution required.")
    out.append(f"- Full text: {base}/about/#bot-policy")
    out.append("")
    return "\n".join(out)


def write_llms_ctx_txt(public: Path) -> bool:
    target = public / "llms-ctx.txt"
    new = build_llms_ctx_txt()
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


_TITLE_INSIDE_RE = re.compile(
    r'<(?:title|news:title)[^>]*>([\s\S]*?)</(?:title|news:title)>',
    re.IGNORECASE,
)
_RSS_ITEM_RE   = re.compile(r'<item>[\s\S]*?</item>', re.IGNORECASE)
_ATOM_ENTRY_RE = re.compile(r'<entry>[\s\S]*?</entry>', re.IGNORECASE)
_NEWS_URL_RE   = re.compile(r'<url>[\s\S]*?</url>', re.IGNORECASE)


def _build_title_index() -> dict[str, str]:
    """title -> canonical https://… URL, derived from _posts frontmatter.

    Walks both the top-level English ``_posts/*.md`` AND every
    per-language subtree ``_posts/<lang>/*.md`` so the per-entry rewrite
    in :func:`fix_xml_feed_urls` can find a URL for translated titles
    too. Without the per-language pass, Shokunin's atom feed would keep
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
    return (s.replace("&amp;", "&")
             .replace("&lt;", "<")
             .replace("&gt;", ">")
             .replace("&quot;", '"')
             .replace("&apos;", "'")
             .strip())


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
    # has /.meta/ anywhere in its path — that's the Shokunin bug signature.
    bad_url = (
        r'https?://'
        r'(?:'
        # localhost host (any path)
        r'(?:127\.0\.0\.1|localhost)(?::\d+)?[^<\s"]*'
        # OR any host with a /.meta/ path segment
        r'|[^<\s"]*?/\.meta(?:/[^<\s"]*)?'
        r')'
    )

    def rewrite_url(m: re.Match[str]) -> str:
        return m.group(1) + url + m.group(3)

    block = re.sub(rf'(>\s*)({bad_url})(\s*<)', rewrite_url, block)
    block = re.sub(rf'(="\s*)({bad_url})(\s*")', rewrite_url, block)
    return block


def fix_xml_feed_urls(public: Path) -> int:
    """Repair localhost/.meta/ URLs Shokunin sometimes bakes into the
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
        # dev-artefact /.meta/ path — those entries come from Shokunin
        # processing the nested _posts/fr/ directory and don't belong in
        # the news-sitemap.
        text = re.sub(
            r'<url>\s*<loc>[^<]*\/\.meta\/[^<]*</loc>[\s\S]*?</url>\s*',
            '',
            text,
        )

        # Top-of-feed cleanup: any residual localhost reference becomes the
        # production root. Done last so it doesn't shadow per-block matches.
        text = re.sub(
            r'https?://(?:127\.0\.0\.1|localhost)(?::\d+)?',
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


# Detect and strip duplicate <item>/<entry>/<url> blocks emitted by the upstream
# SSG when many translation files share the same publication date — the
# generator can collapse multiple locale files onto the same per-item URL
# instead of emitting distinct per-locale URLs, producing identical-by-link
# duplicates that fail xmlls/lib2-news validation downstream.
_RSS_ITEM_RE = re.compile(r'<item>[\s\S]*?</item>', re.IGNORECASE)
_ATOM_ENTRY_RE = re.compile(r'<entry>[\s\S]*?</entry>', re.IGNORECASE)
_SITEMAP_URL_RE = re.compile(r'<url>[\s\S]*?</url>', re.IGNORECASE)
_LINK_RE = re.compile(r'<link[^>]*>([\s\S]*?)</link>', re.IGNORECASE)
_ATOM_LINK_HREF_RE = re.compile(r'<link[^>]*\bhref="([^"]+)"', re.IGNORECASE)
_LOC_RE = re.compile(r'<loc>([\s\S]*?)</loc>', re.IGNORECASE)


def _dedupe_blocks(text: str, block_re: re.Pattern[str], key_fn) -> tuple[str, int]:
    """Walk ``block_re`` matches in order, keep the first occurrence of each
    ``key_fn(block)`` value, drop subsequent duplicates. Returns (new_text,
    dropped_count). Non-block content is preserved verbatim."""
    seen: set[str] = set()
    out: list[str] = []
    cursor = 0
    dropped = 0
    for m in block_re.finditer(text):
        out.append(text[cursor:m.start()])
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
        (public / "rss.xml",          _RSS_ITEM_RE,    _rss_key),
        (public / "atom.xml",         _ATOM_ENTRY_RE,  _atom_key),
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
_SITEMAP_EXCLUDE_TAILS = ("/404/", "/offline/", "/thanks/", "/fr/404/", "/fr/hors-ligne/", "/fr/merci/")
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
    return any(
        path.startswith(tail) or path == tail.rstrip("/")
        for tail in _SITEMAP_EXCLUDE_TAILS
    )


def _collect_sitemap_urls(text: str) -> set[str]:
    return {
        _normalise_url(m.group(1))
        for m in re.finditer(r'<loc>([^<]+)</loc>', text)
    }


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
    m = re.search(r'<lastmod>(\d{4}-\d{2}-\d{2})</lastmod>', text)
    today = m.group(1) if m else ""
    # `additions` already ends with `/` — the canonical pretty URL.
    block = "".join(
        f"\n<url>\n  <changefreq>weekly</changefreq>\n"
        f"  <lastmod>{today}</lastmod>\n  <loc>{u}</loc>\n</url>"
        for u in additions
    )
    new_text = re.sub(r'</urlset>\s*$', block + "\n</urlset>\n", text, count=1)
    sitemap.write_text(new_text, encoding="utf-8")
    return len(additions)


_URL_BLOCK_FOR_DEDUP_RE = re.compile(r'<url>[\s\S]*?</url>', re.MULTILINE)


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


_NEWS_TITLE_RE = re.compile(r'(<news:title>)([\s\S]*?)(</news:title>)', re.IGNORECASE)
_NEWS_KEYWORDS_RE = re.compile(r'(<news:keywords>)([\s\S]*?)(</news:keywords>)', re.IGNORECASE)


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
                "</loc>", f"</loc>\n  {new_lastmod}", 1,
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
    "about", "articles", "papers", "projects", "topics", "tags",
    "playlists", "contact", "accessibility", "privacy", "terms",
    "made-with-shokunin", "made-with-static-site-generator",
    "resources-pacs008-checklist",
)
_TOPIC_SLUGS = (
    "post-quantum-cryptography", "iso-20022-payments",
    "applied-ai-banking", "rust-open-source", "blockchain-digital-assets",
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


def _lang_sitemap_urls(
    code: str, lastmod_index: dict[str, str]
) -> list[tuple[str, str, str, str]]:
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
        (f"{_SITEMAP_BASE}/{code}/{lang_slug}/", "0.7", "monthly", lastmod_index.get(en_art_slug, ""))
        for en_art_slug, lang_slug in articles.items()
    )
    return out


def _splice_fr_urls(xml: str, lastmod_index: dict[str, str]) -> str:
    """Splice every missing EN + non-EN URL into Shokunin's sitemap.xml,
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
