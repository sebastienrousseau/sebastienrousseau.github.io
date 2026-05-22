#!/usr/bin/env python3
"""Generate topic-cluster pillar pages under ``public/topics/{slug}/``.

A pillar page bundles a curated set of dated posts under a named topic
(e.g. "Post-Quantum Cryptography") with a hand-written lede + a card
grid of the cluster's posts. The page is a full standalone HTML
document sharing the same shell (nav, footer, head meta, CSS) as the
existing /articles/ listing — we fork the rendered shell rather than
re-implementing it, so layout drift can't happen.

Inputs:
    - TOPICS         curated map (this file)
    - _posts/*.md    source of truth for each cluster member's metadata
    - public/articles/index.html  shell template (must exist; build.sh
                                  runs `ssg` before this script)

Outputs:
    - public/topics/{slug}/index.html   one per topic
    - public/topics/index.html          hub listing every topic
"""
from __future__ import annotations

import sys as _sys  # path bootstrap — scripts reorg (scripts/lib/ on sys.path)
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "lib"))

import html
import re
import sys
from pathlib import Path

from _core import read_frontmatter as _core_read_frontmatter

PUBLIC = Path("public")
POSTS = Path("_posts")
SHELL_SRC = PUBLIC / "articles" / "index.html"
OUT = PUBLIC / "topics"

# Curated topic clusters. Slug -> {title, lede, slugs[]}. Edit here when
# you reshape the taxonomy or add new posts.
TOPICS: dict[str, dict[str, object]] = {
    "post-quantum-cryptography": {
        "title": "Post-Quantum Cryptography",
        "banner": "https://cloudcdn.pro/stocks/images/getty-images-LaU3HadwEeE-unsplash.webp",
        "lede": (
            "Lattice-based cryptography, NIST PQC standards, quantum-safe payments, "
            "and the harvest-now-decrypt-later threat. Research notes, open-source "
            "libraries, and migration playbooks for financial-services security teams."
        ),
        "slugs": [
            "2026-05-18-quantum-cryptography-standards-developments-2026",
            "2026-05-14-securing-the-ledger-post-quantum-migration-corporate-finance",
            "2026-04-11-quantum-thresholds-are-moving-again",
            "2025-09-01-quantum-safe-payments-epaa",
            "2024-04-22-bug-discovered-in-quantum-algorithm-for-lattice-based-crypto",
            "2024-04-15-quantum-algorithm-challenges-lattice-based-cryptography",
            "2024-03-25-fully-homomorphic-encryption-in-a-banking-quantum-era",
            "2023-12-25-revolutionising-finance-with-ai-enhanced-quantum-algorithms",
            "2023-12-18-state-of-ai-and-quantum-computing-in-banking-a-2023-review",
            "2023-12-11-quantum-key-distribution-revolutionising-security-in-banking",
            "2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats",
            "2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age",
            "2023-10-16-protecting-data-in-the-quantum-age-the-hash-library-hsh",
        ],
    },
    "iso-20022-payments": {
        "title": "ISO 20022 & Payments",
        "banner": "https://cloudcdn.pro/stocks/images/alev-takil-7ojyp-IXW7w-unsplash.webp",
        "lede": (
            "Cross-border message migration, structured-address compliance, "
            "SEPA Instant, SWIFT gpi, and the wholesale-payments rails carrying "
            "it all. Tools, playbooks, and the regulatory clock."
        ),
        "slugs": [
            "2026-05-23-agentic-payments-banking-consent-liability-new-payment-ux-2026",
            "2026-05-19-global-wholesale-payments-economics-2026",
            "2026-05-15-blackrock-brsrv-bstbl-genius-act-tokenised-mmf",
            "2026-05-12-iso-20022-pacs008-structured-address-deadline",
            "2025-09-01-quantum-safe-payments-epaa",
            "2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001",
            "2018-02-15-the-making-of-the-express-transaction-credits-platform",
            "2018-02-04-unveiling-a-new-cryptocurrency-and-offering-future-faster-payment-solution",
        ],
    },
    "cloud-native-banking": {
        "title": "Cloud Native Banking",
        "banner": "https://cloudcdn.pro/stocks/images/freeman-zhou-oV9hp8wXkPE.webp",
        "lede": (
            "Kubernetes-based platform engineering for regulated institutions: "
            "DORA-tested operational resilience, VM and container convergence, "
            "sovereign cloud, exit strategy, and the architecture that lets banks "
            "ship critical services under supervision."
        ),
        "slugs": [
            "2026-05-20-cloud-native-banking-financial-institutions-2026",
            "2026-05-16-best-cloud-infrastructure-architecture-2026",
        ],
    },
    "applied-ai-banking": {
        "title": "Applied AI in Banking",
        "banner": "https://cloudcdn.pro/stocks/images/hector-j-rivas-1FxMET2U5dU-unsplash.webp",
        "lede": (
            "Generative AI, multimodal LLMs, voice, and speech models — and how they "
            "reshape banking operations, customer service, and product engineering "
            "at Tier-1 institutions."
        ),
        "slugs": [
            "2026-05-23-agentic-payments-banking-consent-liability-new-payment-ux-2026",
            "2026-05-17-agentic-engineering-banks-blueprint-2026",
            "2026-05-11-lucy-besson-knowledge-transfer-ai-quantum",
            "2024-04-01-openvoice-leading-innovation-in-voice-cloning-technology",
            "2024-03-18-advancing-ai-with-multimodal-llms-insights-from-mm1",
            "2024-03-12-revolutionising-real-time-speech-recognition-on-macos-with-openai-whisper",
            "2024-03-04-le-chat-by-mistral-ai-a-new-era-in-conversational-ai",
            "2024-02-26-google-gemma-ai-transforming-open-source-ai-development",
            "2024-02-19-unlocking-gemini-google-ai-revolution-explained",
            "2024-02-13-eus-ai-act-shaping-the-future-of-global-ai-regulation",
            "2024-02-12-akande-voice-assistant-revolutionising-personal-and-executive-assistance",
            "2024-02-08-revolutionising-advertising-how-ai-shapes-the-future",
            "2024-01-29-ai-powered-audio-insights-analysis-translations",
            "2024-01-23-advancements-in-ai-prompt-engineering",
            "2024-01-15-alien-studio-revolutionising-art-with-ai-photography",
            "2024-01-01-ai-trends-2024-insights-and-predictions-for-the-future",
            "2023-11-12-exploring-generative-ai",
        ],
    },
    "rust-open-source": {
        "title": "Rust & Open Source",
        "banner": "https://cloudcdn.pro/stocks/images/rustlogs.webp",
        "lede": (
            "Open-source Rust libraries I author and maintain: logging, code "
            "generation, date-time, cryptographic primitives, Kyber-based KEM, "
            "and a Rust static site generator."
        ),
        "slugs": [
            "2024-03-08-rustlogs-advanced-logging-library-for-rust-applications",
            "2023-12-04-mastering-date-and-time-in-rust-with-the-dtt-library",
            "2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats",
            "2023-11-05-mathematical-and-cryptographic-constants-for-rust-security",
            "2023-10-26-libmake-a-code-generator-to-reduce-repetitive-tasks-and-build-high-quality-rust-libraries",
            "2023-10-16-protecting-data-in-the-quantum-age-the-hash-library-hsh",
            "2023-10-09-shokunin-the-fastest-rust-based-static-site-generator",
        ],
    },
    "blockchain-digital-assets": {
        "title": "Blockchain & Digital Assets",
        "banner": "https://cloudcdn.pro/stocks/images/traxer-AIKjbZdNOlw.webp",
        "lede": (
            "Bitcoin, blockchain fundamentals, ERC-20 tokens, stablecoins, and the "
            "regulatory frame around digital-asset-backed payment rails."
        ),
        "slugs": [
            "2026-05-15-blackrock-brsrv-bstbl-genius-act-tokenised-mmf",
            "2018-02-15-the-making-of-the-express-transaction-credits-platform",
            "2018-02-04-unveiling-a-new-cryptocurrency-and-offering-future-faster-payment-solution",
            "2018-01-24-the-erc-20-token-standard",
            "2018-01-09-understanding-the-technology-behind-blockchain",
            "2018-01-02-blockchain-the-technology-that-matters-in-2018",
            "2018-01-01-bitcoin-the-year-in-review",
        ],
    },
}


def read_frontmatter(slug: str) -> dict[str, str]:
    """Parse a post's YAML frontmatter into a flat dict. Returns {} if
    the slug doesn't resolve to a file — callers warn/exit on that case."""
    return _core_read_frontmatter(POSTS / f"{slug}.md")


def _format_date(iso_like: str) -> str:
    """Render a post 'date' frontmatter value as YYYY-MM-DD for <time>."""
    from datetime import datetime as _dt
    for fmt in ("%b %d, %Y", "%B %d, %Y", "%Y-%m-%d"):
        try:
            return _dt.strptime(iso_like, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return iso_like


def render_card(slug: str, fm: dict[str, str]) -> str:
    """Render a single newsroom-card for the given post slug + frontmatter."""
    title = fm.get("title") or slug
    desc = fm.get("description") or ""
    banner = fm.get("banner") or "https://cloudcdn.pro/stocks/images/sebastien-rousseau.png"
    banner_alt = fm.get("banner_alt") or title
    keywords = fm.get("keywords") or ""
    eyebrow = " · ".join(k.strip().title() for k in keywords.split(",")[:3] if k.strip())
    date_iso = _format_date(fm.get("date") or slug[:10])
    date_human = ""
    try:
        from datetime import datetime as _dt
        date_human = _dt.strptime(date_iso, "%Y-%m-%d").strftime("%b %-d, %Y")
    except ValueError:
        date_human = date_iso

    url = f"/{slug}/index.html"
    e_title = html.escape(title, quote=True)
    e_desc = html.escape(desc)
    e_alt = html.escape(banner_alt, quote=True)
    e_eyebrow = html.escape(eyebrow)
    return (
        '<article class="newsroom-card">'
        f'<a class="newsroom-card-media" href="{url}" title="{e_title}">'
        f'<img alt="{e_alt}" src="{banner}" loading="lazy" decoding="async" width="600" height="600" />'
        '</a>'
        '<div class="newsroom-card-body">'
        f'<span class="newsroom-eyebrow">{e_eyebrow}</span>'
        f'<h3><a href="{url}" title="{e_title}">{e_title}</a></h3>'
        f'<p class="newsroom-meta"><time datetime="{date_iso}">{date_human}</time> · Sebastien Rousseau</p>'
        f'<p class="newsroom-excerpt">{e_desc}</p>'
        '</div>'
        '</article>'
    )


_TITLE_RE = re.compile(r'<title>([^<]*)</title>', re.IGNORECASE)
_DESC_RE = re.compile(r'<meta\s+name="description"\s+content="([^"]*)"', re.IGNORECASE)
_OG_TITLE_RE = re.compile(r'(<meta\s+property="og:title"\s+content=")[^"]*(")', re.IGNORECASE)
_OG_DESC_RE = re.compile(r'(<meta\s+property="og:description"\s+content=")[^"]*(")', re.IGNORECASE)
_OG_URL_RE = re.compile(r'(<meta\s+property="og:url"\s+content=")[^"]*(")', re.IGNORECASE)
_CANONICAL_RE = re.compile(r'(<link\s+rel="canonical"\s+href=")[^"]*(")', re.IGNORECASE)
_NEWSROOM_RE = re.compile(r'<section class="newsroom">[\s\S]*?</section>', re.IGNORECASE)
_LDJSON_BLOCKS_RE = re.compile(r'<script type="application/ld\+json">[\s\S]*?</script>', re.IGNORECASE)


def _strip_extra_jsonld(shell: str) -> str:
    """The articles shell ships an ItemList JSON-LD block listing every
    article. Strip it — the topic page emits its own ItemList scoped to
    the cluster."""
    blocks = _LDJSON_BLOCKS_RE.findall(shell)
    if not blocks:
        return shell
    for b in blocks:
        if '"ItemList"' in b or '"itemListElement"' in b:
            shell = shell.replace(b, '', 1)
    return shell


def _build_topic_body(title: str, lede: str, cards: list[str], slug: str) -> str:
    return (
        '<section class="newsroom">'
        '<nav aria-label="Breadcrumb" class="topic-breadcrumb">'
        '<a href="/">Home</a> &middot; '
        '<a href="/topics/index.html">Topics</a> &middot; '
        f'<span>{html.escape(title)}</span>'
        '</nav>'
        '<header class="newsroom-section-head">'
        f'<p class="newsroom-kicker">TOPIC</p>'
        f'<h1>{html.escape(title)}</h1>'
        f'<p class="topic-lede">{html.escape(lede)}</p>'
        '</header>'
        '<h2 class="visually-hidden">Articles in this topic</h2>'
        '<div class="newsroom-grid">' + "".join(cards) + '</div>'
        '</section>'
    )


def _build_topic_jsonld(slug: str, title: str, lede: str, slugs: list[str], post_titles: list[str]) -> str:
    import json as _json
    base = "https://sebastienrousseau.com"
    items = [
        {
            "@type": "ListItem",
            "position": i + 1,
            "url": f"{base}/{s}/index.html",
            "name": t,
        }
        for i, (s, t) in enumerate(zip(slugs, post_titles, strict=False))
    ]
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "@id": f"{base}/topics/{slug}/",
                "url": f"{base}/topics/{slug}/",
                "name": title,
                "description": lede,
                "isPartOf": {"@id": f"{base}/#website"},
                "about": {"@id": f"{base}/#person"},
                "inLanguage": "en-GB",
                "mainEntity": {
                    "@type": "ItemList",
                    "numberOfItems": len(items),
                    "itemListElement": items,
                },
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{base}/"},
                    {"@type": "ListItem", "position": 2, "name": "Topics", "item": f"{base}/topics/"},
                    {"@type": "ListItem", "position": 3, "name": title, "item": f"{base}/topics/{slug}/"},
                ],
            },
        ],
    }
    return (
        '<script type="application/ld+json">'
        + _json.dumps(graph, separators=(",", ":"), ensure_ascii=False)
        + '</script>'
    )


def render_topic(slug: str, spec: dict[str, object], shell: str) -> tuple[str, str]:
    """Return (path-relative-to-PUBLIC, html) for one topic page."""
    title = str(spec["title"])
    lede = str(spec["lede"])
    slugs: list[str] = list(spec["slugs"])  # type: ignore[arg-type]
    cards: list[str] = []
    post_titles: list[str] = []
    missing: list[str] = []
    for s in slugs:
        fm = read_frontmatter(s)
        if not fm:
            missing.append(s)
            continue
        cards.append(render_card(s, fm))
        post_titles.append(fm.get("title") or s)
    if missing:
        # Hard fail — silently dropping cards from a topic page lets a
        # typo in TOPICS[].slugs ship to production unnoticed. Surface
        # the bad slugs so the editor fixes the typo before the build
        # completes.
        print(
            f"build_topics: ERROR — topic '{slug}' references unknown slug(s):",
            file=sys.stderr,
        )
        for s in missing:
            print(f"  - {s}", file=sys.stderr)
        raise SystemExit(1)

    body = _build_topic_body(title, lede, cards, slug)
    ldjson = _build_topic_jsonld(slug, title, lede, slugs, post_titles)

    out = _strip_extra_jsonld(shell)
    out = _NEWSROOM_RE.sub(body, out, count=1)

    page_title = f"{title} — Sebastien Rousseau"
    out = _TITLE_RE.sub(f"<title>{html.escape(page_title)}</title>", out, count=1)
    out = _DESC_RE.sub(
        f'<meta name="description" content="{html.escape(lede, quote=True)}"',
        out,
        count=1,
    )
    out = _OG_TITLE_RE.sub(rf'\1{html.escape(page_title, quote=True)}\2', out, count=1)
    out = _OG_DESC_RE.sub(rf'\1{html.escape(lede, quote=True)}\2', out, count=1)
    out = _OG_URL_RE.sub(rf'\1https://sebastienrousseau.com/topics/{slug}/\2', out, count=1)
    out = _CANONICAL_RE.sub(rf'\1https://sebastienrousseau.com/topics/{slug}/\2', out, count=1)

    # Inject our scoped JSON-LD just before </body>.
    out = re.sub(r'(</body>)', ldjson + r'\1', out, count=1)

    return f"topics/{slug}/index.html", out


def render_hub(shell: str) -> tuple[str, str]:
    """Topic-hub page: /topics/index.html listing every topic."""
    cards: list[str] = []
    for slug, spec in TOPICS.items():
        title = html.escape(str(spec["title"]))
        lede = html.escape(str(spec["lede"]))
        banner = html.escape(str(spec.get("banner") or ""))
        count = len(spec["slugs"])  # type: ignore[arg-type]
        url = f"/topics/{slug}/index.html"
        if banner:
            media = (
                f'<a class="newsroom-card-media" href="{url}" aria-label="{title}">'
                f'<img src="{banner}" alt="{title} — topic banner" '
                f'loading="lazy" decoding="async" '
                f'width="800" height="800"></a>'
            )
        else:
            media = (
                f'<a class="newsroom-card-media" href="{url}" aria-label="{title}" '
                'style="background:linear-gradient(135deg,var(--cl-grey-100,#f1f3f7),var(--cl-grey-200,#e3e6ed));aspect-ratio:1/1"></a>'
            )
        cards.append(
            '<article class="newsroom-card">'
            + media +
            '<div class="newsroom-card-body">'
            '<span class="newsroom-eyebrow">PILLAR · TOPIC</span>'
            f'<h3><a href="{url}">{title}</a></h3>'
            f'<p class="newsroom-excerpt">{lede}</p>'
            f'<p class="newsroom-meta">{count} article(s)</p>'
            '</div>'
            '</article>'
        )
    body = (
        '<section class="newsroom">'
        '<nav aria-label="Breadcrumb" class="topic-breadcrumb">'
        '<a href="/">Home</a> &middot; <span>Topics</span></nav>'
        '<header class="newsroom-section-head">'
        '<p class="newsroom-kicker">PILLARS</p>'
        '<h1>Topics</h1>'
        '<p class="topic-lede">Curated topic clusters — pick a thread and follow it through the archive.</p>'
        '</header>'
        '<h2 class="visually-hidden">All topics</h2>'
        '<div class="newsroom-grid">' + "".join(cards) + '</div>'
        '</section>'
    )
    out = _strip_extra_jsonld(shell)
    out = _NEWSROOM_RE.sub(body, out, count=1)
    title = "Topics — Sebastien Rousseau"
    desc = "Curated topic clusters covering post-quantum cryptography, ISO 20022, applied AI in banking, Rust open source, and digital assets."
    out = _TITLE_RE.sub(f"<title>{html.escape(title)}</title>", out, count=1)
    out = _DESC_RE.sub(f'<meta name="description" content="{html.escape(desc, quote=True)}"', out, count=1)
    out = _OG_TITLE_RE.sub(rf'\1{html.escape(title, quote=True)}\2', out, count=1)
    out = _OG_DESC_RE.sub(rf'\1{html.escape(desc, quote=True)}\2', out, count=1)
    out = _OG_URL_RE.sub(r'\1https://sebastienrousseau.com/topics/\2', out, count=1)
    out = _CANONICAL_RE.sub(r'\1https://sebastienrousseau.com/topics/\2', out, count=1)
    return "topics/index.html", out


def main() -> None:
    if not SHELL_SRC.is_file():
        raise SystemExit(f"shell template missing: {SHELL_SRC} — run ssg first")
    shell = SHELL_SRC.read_text(encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    count = 0
    for slug, spec in TOPICS.items():
        rel, body = render_topic(slug, spec, shell)
        dst = PUBLIC / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(body, encoding="utf-8")
        count += 1
    rel, body = render_hub(shell)
    (PUBLIC / rel).write_text(body, encoding="utf-8")
    print(f"build_topics: wrote {count} topic page(s) + 1 hub")


if __name__ == "__main__":
    main()
