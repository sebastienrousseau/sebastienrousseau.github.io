#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

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
    _posts/*.md       - post frontmatter (read directly)
    scripts/build_topics.py:TOPICS - topic taxonomy
    public/.../index.html - wordCount lifted from rendered BlogPosting JSON-LD

Must run AFTER postbuild.py so the wordCount stamped into each rendered
BlogPosting JSON-LD is populated on clean builds.
"""

from __future__ import annotations

import sys as _sys  # path bootstrap — scripts reorg (scripts/lib/ on sys.path)
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "lib"))

import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _profile
from build_topics import TOPICS, read_frontmatter

PUBLIC = Path("public")
POSTS = Path("_posts")
SIGSTORE = Path("sigstore-bundles")
OUT = PUBLIC / "api" / "agents"
BASE = "https://sebastienrousseau.com"

_WC_RE = re.compile(r'"wordCount":(\d+)')
_DATED_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-")


def _topic_index() -> dict[str, list[str]]:
    slug_to_topics: dict[str, list[str]] = {}
    for tslug, spec in TOPICS.items():
        for s in spec["slugs"]:  # type: ignore[index]
            slug_to_topics.setdefault(s, []).append(tslug)
    return slug_to_topics


def _word_count(stem: str) -> int | None:
    """Word count is added by postbuild — peek at the rendered page if
    it exists at this point in the pipeline."""
    rendered = PUBLIC / stem / "index.html"
    if not rendered.is_file():
        return None
    m = _WC_RE.search(rendered.read_text(encoding="utf-8", errors="ignore"))
    return int(m.group(1)) if m else None


def _content_sha256(md: Path) -> str:
    """Return the hex SHA-256 digest of a markdown source file for agent provenance."""
    return hashlib.sha256(md.read_bytes()).hexdigest()


def _sigstore_bundle_url(stem: str) -> str | None:
    """Return the public Sigstore bundle URL when a bundle exists for ``stem``."""
    bundle_name = f"{stem}.sigstore.json"
    if (SIGSTORE / bundle_name).is_file() or (PUBLIC / "sigstore" / bundle_name).is_file():
        return f"{BASE}/sigstore/{bundle_name}"
    return None


def _split_keywords(fm: dict[str, str]) -> list[str]:
    return [k.strip() for k in (fm.get("keywords") or "").split(",") if k.strip()]


def collect_posts() -> list[dict[str, object]]:
    """Walk _posts/, return one record per dated post."""
    out: list[dict[str, object]] = []
    slug_to_topics = _topic_index()

    for md in sorted(POSTS.glob("*.md")):
        stem = md.stem
        if not _DATED_RE.match(stem):
            continue
        fm = read_frontmatter(stem)
        if not fm:
            continue
        wc = _word_count(stem)
        sigstore_url = _sigstore_bundle_url(stem)
        record: dict[str, object] = {
            "slug": stem,
            "url": f"{BASE}/{stem}/",
            "date": stem[:10],
            "title": fm.get("title") or stem,
            "description": fm.get("description", ""),
            "keywords": _split_keywords(fm),
            "banner": fm.get("banner", ""),
            "topics": slug_to_topics.get(stem, []),
            "language": fm.get("language", "en-GB"),
            "content_sha256": _content_sha256(md),
        }
        if wc is not None:
            record["wordCount"] = wc
        if sigstore_url is not None:
            record["sigstore_bundle"] = sigstore_url
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
            "url": f"{BASE}/about/",
            "wikidata": None,
        },
        "endpoints": {
            "posts": {
                "url": f"{BASE}/api/agents/posts.json",
                "description": "All dated posts with metadata",
            },
            "topics": {
                "url": f"{BASE}/api/agents/topics.json",
                "description": "Curated topic clusters + slug lists",
            },
            "person": {
                "url": f"{BASE}/api/agents/person.json",
                "description": "Author profile (Person schema with ORCID + hasCredential + knowsAbout)",
            },
            "organization": {
                "url": f"{BASE}/api/agents/organization.json",
                "description": "Publisher organisation (Organization + Brand schema)",
            },
        },
        "see_also": {
            "llms_txt": f"{BASE}/llms.txt",
            "llms_full": f"{BASE}/llms-full.txt",
            "sitemap": f"{BASE}/sitemap.xml",
            "news_sitemap": f"{BASE}/news-sitemap.xml",
            "rss": f"{BASE}/rss.xml",
            "atom": f"{BASE}/atom.xml",
            "openapi": f"{BASE}/.well-known/openapi.json",
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


ORCID_ID = "0009-0005-1434-284X"


def build_person() -> dict[str, object]:
    """Person graph: ORCID identifier and knowsAbout as DefinedTerm objects
    with sameAs links to Wikipedia / standards-body URLs, plus the facts
    _data/profile.yml owns (title, bio, employer, schools, memberships,
    credentials), merged from _profile.person_fields as postbuild merges
    them into the layouts' @graph."""
    return {
        "@context": "https://schema.org",
        "@type": "Person",
        "@id": f"{BASE}/#person",
        "name": "Sebastien Rousseau",
        "givenName": "Sebastien",
        "familyName": "Rousseau",
        "url": BASE + "/",
        "image": "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp",
        "identifier": {
            "@type": "PropertyValue",
            "propertyID": "ORCID",
            "value": ORCID_ID,
            "url": f"https://orcid.org/{ORCID_ID}",
        },
        "knowsAbout": [
            {
                "@type": "DefinedTerm",
                "name": "Post-Quantum Cryptography",
                "sameAs": "https://en.wikipedia.org/wiki/Post-quantum_cryptography",
            },
            {
                "@type": "DefinedTerm",
                "name": "ML-KEM (FIPS 203)",
                "sameAs": "https://csrc.nist.gov/pubs/fips/203/final",
            },
            {
                "@type": "DefinedTerm",
                "name": "ML-DSA (FIPS 204)",
                "sameAs": "https://csrc.nist.gov/pubs/fips/204/final",
            },
            {
                "@type": "DefinedTerm",
                "name": "ISO 20022",
                "sameAs": "https://en.wikipedia.org/wiki/ISO_20022",
            },
            {
                "@type": "DefinedTerm",
                "name": "SWIFT gpi",
                "sameAs": "https://www.swift.com/our-solutions/swift-gpi",
            },
            {
                "@type": "DefinedTerm",
                "name": "SEPA Instant Payments",
                "sameAs": "https://www.ecb.europa.eu/paym/integration/retail/instant_payments/html/index.en.html",
            },
            {
                "@type": "DefinedTerm",
                "name": "FedNow Service",
                "sameAs": "https://www.federalreserve.gov/paymentsystems/fednow_about.htm",
            },
            {
                "@type": "DefinedTerm",
                "name": "Real-Time Payments (RTP)",
                "sameAs": "https://www.theclearinghouse.org/payment-systems/rtp",
            },
            {
                "@type": "DefinedTerm",
                "name": "Cross-border payments",
                "sameAs": "https://en.wikipedia.org/wiki/Cross-border_payments",
            },
            {
                "@type": "DefinedTerm",
                "name": "Wholesale banking",
                "sameAs": "https://en.wikipedia.org/wiki/Wholesale_banking",
            },
            {
                "@type": "DefinedTerm",
                "name": "Applied artificial intelligence in banking",
                "sameAs": "https://en.wikipedia.org/wiki/Applications_of_artificial_intelligence",
            },
            {
                "@type": "DefinedTerm",
                "name": "Generative artificial intelligence",
                "sameAs": "https://en.wikipedia.org/wiki/Generative_artificial_intelligence",
            },
        ],
        "sameAs": [
            f"https://orcid.org/{ORCID_ID}",
            "https://x.com/wwdseb",
            "https://www.linkedin.com/in/sebastienrousseau/",
            "https://medium.com/@BankingOnQuantum",
            "https://www.youtube.com/@BankingOnQuantum",
            "https://github.com/sebastienrousseau",
        ],
    } | _profile.person_fields(BASE)


def build_organization() -> dict[str, object]:
    """Site Organization graph node. Separate file so AI crawlers walking
    /api/agents/ can discover the publisher entity without parsing HTML."""
    return {
        "@context": "https://schema.org",
        "@type": ["Organization", "Brand"],
        "@id": f"{BASE}/#organization",
        "name": "Sebastien Rousseau",
        "alternateName": "Banking on Quantum",
        "url": BASE + "/",
        "logo": {
            "@type": "ImageObject",
            "@id": f"{BASE}/#logo",
            "url": "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp",
            "width": "512",
            "height": "512",
            "caption": "Sebastien Rousseau",
        },
        "founder": {"@id": f"{BASE}/#person"},
        "sameAs": [
            "https://github.com/sebastienrousseau",
            "https://x.com/wwdseb",
            "https://www.linkedin.com/in/sebastienrousseau/",
            "https://medium.com/@BankingOnQuantum",
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
    write_json(OUT / "organization.json", build_organization())
    print(
        f"build_agent_api: wrote {len(posts)} posts + {len(TOPICS)} topics "
        "+ person + organization + index",
    )


if __name__ == "__main__":
    main()
