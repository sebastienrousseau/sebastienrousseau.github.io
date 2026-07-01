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
import _lang_registry as _lr


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
# Static Site Generator emits empty placeholder humans.txt + security.txt at the site root
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
    out.append(
        f"- [About]({base}/about/) — full biography, professional history, areas of expertise."
    )
    out.append(
        f"- [Articles]({base}/articles/) — research notes on quantum-safe cryptography, ISO 20022, applied AI, wholesale payments."
    )
    out.append(
        f"- [Papers]({base}/papers/) — industry white papers, peer-reviewed analysis, regulatory submissions."
    )
    out.append(
        f"- [Projects]({base}/projects/) — open-source Python and Rust libraries for payments, post-quantum crypto, AI tooling."
    )
    out.append(
        f"- [Topics]({base}/topics/) — topic hubs: post-quantum, ISO 20022, applied AI, Rust, blockchain."
    )
    out.append(
        f"- [Playlists]({base}/playlists/) — curated music libraries for deep work and engineering flow."
    )
    out.append(
        f"- [Contact]({base}/contact/) — professional contact form for consulting, speaking, advisory engagements."
    )
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
    out.append("## RAG corpus + oEmbed (machine-readable surfaces)")
    out.append("")
    out.append(
        f"- [/feed.jsonl]({base}/feed.jsonl) — full editorial corpus, "
        f"newline-delimited JSON, one record per article with title, "
        f"summary, body_markdown, body_text, tags, pillars, license."
    )
    out.append(
        f"- [/tags/<slug>/feed.jsonl]({base}/tags/iso-20022/feed.jsonl) — "
        f"per-canonical-tag subsets (51 tags today; substitute any "
        f"canonical slug from taxonomy.yml)."
    )
    out.append(
        f"- [/oembed/<slug>.json]({base}/oembed/2026-06-12-kyberlib-post-quantum-banking-migration-standards-code-2026.json) — "
        f"static oEmbed metadata per article. Notion / Discord / Slack / "
        f"WordPress / Atlassian consume this directly."
    )
    out.append(
        "- [/tags/](https://sebastienrousseau.com/tags/) — curated "
        "6-pillar editorial cover with featured tags and per-tag "
        "collapsible article lists."
    )
    out.append(
        f"- [/categories/<pillar>/]({base}/categories/ai/) — per-pillar "
        f"landing pages (ai, payments, infra, policy, open-source, "
        f"leadership) with the tags + recent articles in each."
    )
    out.append(
        f"- [/.well-known/ai.txt]({base}/.well-known/ai.txt) — AI usage "
        f"policy (attribution + license terms)."
    )
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


def build_ai_txt() -> str:
    """Render `/.well-known/ai.txt` — AI usage policy. Format follows
    the emerging ai.txt convention used by Substack, GitHub, and
    several IETF drafts. Tells AI clients what they can and can't do
    with the content, while keeping the corpus broadly available for
    summarisation + citation under CC-BY-4.0.
    """
    base = "https://sebastienrousseau.com"
    lines = [
        "# AI usage policy for sebastienrousseau.com",
        "# Format: emerging ai.txt convention (ai.txt @ /.well-known/).",
        "# Last reviewed: 2026-06-13",
        "",
        "Author: Sebastien Rousseau",
        f"Site: {base}/",
        "License: CC-BY-4.0",
        "",
        "## Allow",
        "",
        "- Indexing for AI search (Perplexity, You.com, ChatGPT Search,",
        "  Bing Copilot, Google AI Overviews, Brave Leo).",
        "- Summarisation in answers to user questions.",
        "- Citation in generative AI output, provided the canonical URL",
        "  is preserved in the citation.",
        "- Use in RAG pipelines, vector stores, and MCP servers (see",
        f"  the RAG-ready corpus at {base}/feed.jsonl).",
        "- Training of derivative AI models, provided each training",
        "  example carries the canonical URL and CC-BY-4.0 attribution",
        "  in metadata, AND the resulting model's documentation lists",
        "  this domain as a training source.",
        "",
        "## Require",
        "",
        "- Attribution: include the canonical article URL in answers,",
        "  summaries, and any derived content (CC-BY-4.0 §3.a.A).",
        "- Attribution: include the author name (Sebastien Rousseau)",
        "  in cited material (CC-BY-4.0 §3.a.B).",
        "- License: indicate CC-BY-4.0 when material is republished",
        "  or used in derivative works (CC-BY-4.0 §3.a.D).",
        "",
        "## Do not",
        "",
        "- Strip the canonical URL or author attribution from derived",
        "  content.",
        "- Misrepresent the editorial position by selectively quoting",
        "  out of context.",
        "- Use the content for ad-targeting profile-building unrelated",
        "  to the editorial subject matter.",
        "",
        "## Contact",
        "",
        "Sebastien Rousseau (London, UK)",
        f"- Site: {base}/contact/",
        "- LinkedIn: https://www.linkedin.com/in/sebastienrousseau/",
        "",
        "## Machine-readable surfaces",
        "",
        f"- {base}/feed.jsonl                    — full editorial corpus, RAG-ready",
        f"- {base}/tags/<slug>/feed.jsonl        — per-canonical-tag subsets",
        f"- {base}/oembed/<slug>.json            — per-article oEmbed metadata",
        f"- {base}/.well-known/llm.txt           — LLM site index",
        f"- {base}/llms.txt                      — same content at root for crawler compat",
        f"- {base}/llms-ctx.txt                  — terse agent-context companion",
        f"- {base}/llms-full.txt                 — full corpus dump as plain text",
        "",
    ]
    return "\n".join(lines)


def write_ai_txt(public: Path) -> bool:
    target = public / ".well-known" / "ai.txt"
    new = build_ai_txt()
    target.parent.mkdir(parents=True, exist_ok=True)
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
    out.append(
        f"- {base}/papers/         — White papers, peer-reviewed analysis, regulatory submissions."
    )
    out.append(f"- {base}/projects/       — Open-source Python and Rust libraries.")
    out.append(
        f"- {base}/topics/         — Topic hubs: post-quantum, ISO 20022, applied AI, Rust, blockchain."
    )
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

