#!/usr/bin/env python3
"""Generate /api/agents/ — a structured, robots-friendly JSON API for AI
crawlers and downstream agent toolchains.

The site already publishes JSON-LD on every page, an RSS feed, and an
llms.txt. The agent API complements those by exposing the *post + topic
graph* as plain JSON over a stable URL surface, with no rate limit and
no auth — pure static files served from the CDN.

Outputs (all under public/api/agents/):
    index.json        — entry point: links to other endpoints + meta
    posts.json        — every dated post with title, url, date, topics,
                        keywords, description, wordCount when known
    topics.json       — every curated topic cluster + its post slugs
    person.json       — author profile (Person + Organization)

Inputs:
    _posts/*.md       — post frontmatter (read directly)
    scripts/build_topics.py:TOPICS — topic taxonomy
    public/.../index.html — wordCount lifted from rendered BlogPosting JSON-LD

Must run AFTER ssg + build_topics + before postbuild (so the API is
fingerprinted into the build artefacts).
"""
from __future__ import annotations

import sys as _sys  # path bootstrap — scripts reorg (scripts/lib/ on sys.path)
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "lib"))

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_topics import TOPICS, read_frontmatter

PUBLIC = Path("public")
POSTS = Path("_posts")
OUT = PUBLIC / "api" / "agents"
BASE = "https://sebastienrousseau.com"

_WC_RE = re.compile(r'"wordCount":(\d+)')
_DATED_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-")


def collect_posts() -> list[dict[str, object]]:
    """Walk _posts/, return one record per dated post."""
    out: list[dict[str, object]] = []
    slug_to_topics: dict[str, list[str]] = {}
    for tslug, spec in TOPICS.items():
        for s in spec["slugs"]:  # type: ignore[index]
            slug_to_topics.setdefault(s, []).append(tslug)

    for md in sorted(POSTS.glob("*.md")):
        stem = md.stem
        if not _DATED_RE.match(stem):
            continue
        fm = read_frontmatter(stem)
        if not fm:
            continue
        # Word count is added by postbuild — peek at the rendered page
        # if it exists at this point in the pipeline.
        wc: int | None = None
        rendered = PUBLIC / stem / "index.html"
        if rendered.is_file():
            m = _WC_RE.search(rendered.read_text(encoding="utf-8", errors="ignore"))
            if m:
                wc = int(m.group(1))
        record: dict[str, object] = {
            "slug": stem,
            "url": f"{BASE}/{stem}/index.html",
            "date": stem[:10],
            "title": fm.get("title") or stem,
            "description": fm.get("description", ""),
            "keywords": [k.strip() for k in (fm.get("keywords") or "").split(",") if k.strip()],
            "banner": fm.get("banner", ""),
            "topics": slug_to_topics.get(stem, []),
            "language": fm.get("language", "en-GB"),
        }
        if wc is not None:
            record["wordCount"] = wc
        out.append(record)
    # Newest first.
    out.sort(key=lambda r: str(r["date"]), reverse=True)
    return out


def build_index() -> dict[str, object]:
    return {
        "name": "Sebastien Rousseau — Agent API",
        "description": (
            "Structured JSON access to the post + topic graph. Designed for AI "
            "crawlers, RAG indexers, and downstream agent toolchains. No auth, "
            "no rate limit, no tracking. Served as static files from CDN."
        ),
        "version": 1,
        "base_url": f"{BASE}/api/agents/",
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "author": {
            "name": "Sebastien Rousseau",
            "url": f"{BASE}/about/index.html",
            "wikidata": None,
        },
        "endpoints": {
            "posts":   {"url": f"{BASE}/api/agents/posts.json",   "description": "All dated posts with metadata"},
            "topics":  {"url": f"{BASE}/api/agents/topics.json",  "description": "Curated topic clusters + slug lists"},
            "person":  {"url": f"{BASE}/api/agents/person.json",  "description": "Author profile (Person schema)"},
        },
        "see_also": {
            "llms_txt":     f"{BASE}/llms.txt",
            "llms_full":    f"{BASE}/llms-full.txt",
            "sitemap":      f"{BASE}/sitemap.xml",
            "news_sitemap": f"{BASE}/news-sitemap.xml",
            "rss":          f"{BASE}/rss.xml",
            "atom":         f"{BASE}/atom.xml",
            "ai_plugin":    f"{BASE}/.well-known/ai-plugin.json",
            "openapi":      f"{BASE}/.well-known/openapi.json",
        },
        "robots_policy": "Permitted: crawl, index, train. Attribution requested via citation in your output.",
    }


def build_topics_payload() -> dict[str, object]:
    return {
        "count": len(TOPICS),
        "topics": [
            {
                "slug": tslug,
                "title": spec["title"],
                "description": spec["lede"],
                "url": f"{BASE}/topics/{tslug}/",
                "post_count": len(spec["slugs"]),  # type: ignore[arg-type]
                "post_slugs": list(spec["slugs"]),  # type: ignore[arg-type]
            }
            for tslug, spec in TOPICS.items()
        ],
    }


def build_person() -> dict[str, object]:
    return {
        "@context": "https://schema.org",
        "@type": "Person",
        "@id": f"{BASE}/#person",
        "name": "Sebastien Rousseau",
        "givenName": "Sebastien",
        "familyName": "Rousseau",
        "url": BASE,
        "jobTitle": "Senior Product Manager",
        "worksFor": {"@type": "Organization", "name": "HSBC Commercial & Investment Bank", "url": "https://www.hsbc.com/"},
        "knowsAbout": [
            "Post-quantum cryptography",
            "ISO 20022",
            "Wholesale payments",
            "Applied artificial intelligence in banking",
            "Generative AI for financial services",
            "CRYSTALS-Kyber",
            "SEPA Instant Payments",
            "SWIFT gpi",
        ],
        "memberOf": {
            "@type": "ProgramMembership",
            "programName": "Quantum-Safe Cryptography Working Group",
            "hostingOrganization": {
                "@type": "Organization",
                "name": "Emerging Payments Association Asia",
                "url": "https://emergingpaymentsasia.org/",
            },
        },
        "sameAs": [
            "https://twitter.com/wwdseb",
            "https://www.linkedin.com/in/sebastienrousseau/",
            "https://medium.com/@BankingOnQuantum",
            "https://www.youtube.com/@BankingOnQuantum",
            "https://github.com/sebastienrousseau",
        ],
    }


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    posts = collect_posts()
    write_json(OUT / "index.json", build_index())
    write_json(OUT / "posts.json", {"count": len(posts), "posts": posts})
    write_json(OUT / "topics.json", build_topics_payload())
    write_json(OUT / "person.json", build_person())
    print(f"build_agent_api: wrote {len(posts)} posts + {len(TOPICS)} topics + person + index")


if __name__ == "__main__":
    main()
