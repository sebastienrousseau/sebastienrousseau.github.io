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
        "banner": "https://cloudcdn.pro/stocks/images/leo_visions-Q_y8ZzhQ2_s-unsplash.webp",
        "lede": (
            "Lattice-based cryptography, NIST PQC standards, quantum-safe payments, "
            "and the harvest-now-decrypt-later threat. Research notes, open-source "
            "libraries, and migration playbooks for financial-services security teams."
        ),
        "slugs": [
            "2026-06-04-quantum-safe-banking-index-pqc-qkd-crypto-agility-2026",
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
            "2026-07-08-global-corporate-standard-iso-20022-swift-2026",
            "2026-07-07-corporate-banking-api-standard-agentic-mcp-2026",
            "2026-06-06-wholesale-payments-index-iso20022-tokenised-deposits-cross-border-2026",
            "2026-05-30-uk-wholesale-digital-markets-tokenised-gilts-settlement-2026",
            "2026-05-29-iso-20022-after-migration-payment-data-banking-products-2026",
            "2026-05-24-uk-payments-forward-plan-stablecoins-open-banking-tokenised-payments-2026",
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
        "banner": "https://cloudcdn.pro/stocks/images/alis-po-IdVNRv-5wJo.webp",
        "lede": (
            "Kubernetes-based platform engineering for regulated institutions: "
            "DORA-tested operational resilience, VM and container convergence, "
            "sovereign cloud, exit strategy, and the architecture that lets banks "
            "ship critical services under supervision."
        ),
        "slugs": [
            "2026-06-05-cloud-native-banking-index-dora-resilience-platform-engineering-2026",
            "2026-05-20-cloud-native-banking-financial-institutions-2026",
            "2026-05-16-best-cloud-infrastructure-architecture-2026",
        ],
    },
    "applied-ai-banking": {
        "title": "Applied AI in Banking",
        "banner": "https://cloudcdn.pro/stocks/images/hector-j-rivas-1FxMET2U5dU-unsplash.webp",
        "lede": (
            "Generative AI, multimodal LLMs, voice, and speech models, and how they "
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
            "2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap",
            "2024-03-08-rustlogs-advanced-logging-library-for-rust-applications",
            "2023-12-04-mastering-date-and-time-in-rust-with-the-dtt-library",
            "2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats",
            "2023-11-05-mathematical-and-cryptographic-constants-for-rust-security",
            "2023-10-26-libmake-a-code-generator-to-reduce-repetitive-tasks-and-build-high-quality-rust-libraries",
            "2023-10-16-protecting-data-in-the-quantum-age-the-hash-library-hsh",
            "2023-10-09-the-fastest-rust-based-static-site-generator",
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
            "2026-05-28-digital-assets-tokenisation-stablecoins-bank-strategy-infrastructure-transition-2026",
            "2026-05-15-blackrock-brsrv-bstbl-genius-act-tokenised-mmf",
            "2018-02-15-the-making-of-the-express-transaction-credits-platform",
            "2018-02-04-unveiling-a-new-cryptocurrency-and-offering-future-faster-payment-solution",
            "2018-01-24-the-erc-20-token-standard",
            "2018-01-09-understanding-the-technology-behind-blockchain",
            "2018-01-02-blockchain-the-technology-that-matters-in-2018",
            "2018-01-01-bitcoin-the-year-in-review",
        ],
    },
    "agentic-ai-banking": {
        "title": "Agentic AI in Banking",
        "banner": "https://cloudcdn.pro/stocks/images/digital-nodes.webp",
        "lede": (
            "Agent control planes, deterministic semantic routing, OPA policy "
            "gates, immutable WORM audit logs, and the SR 11-7 / SS1/23 model-risk "
            "lens that turns autonomous workflows into supervisory-ready evidence."
        ),
        "slugs": [
            "2026-07-01-agentic-ai-index-banks-measuring-autonomy-2026",
            "2026-06-03-agentic-ai-index-banks-autonomy-governance-auditability-2026",
            "2026-06-02-banking-infrastructure-index-agentic-ai-quantum-cloud-wholesale-payments-2026",
            "2026-05-27-ai-operating-system-payments-fraud-routing-resilience-compliance-2026",
            "2026-05-23-agentic-payments-banking-consent-liability-new-payment-ux-2026",
            "2026-05-17-agentic-engineering-banks-blueprint-2026",
        ],
    },
    "treasury-automation": {
        "title": "Treasury Automation",
        "banner": "https://cloudcdn.pro/stocks/images/tyler-prahm-lmV3gJSAgbo.webp",
        "lede": (
            "Programmable liquidity, autonomous treasury, ISO 20022 payment "
            "engines, and the open-source toolkits that turn CAMT / pacs.008 / "
            "MT940 / pain.001 into auditable, board-grade transaction "
            "intelligence for corporate treasury teams."
        ),
        "slugs": [
            "2026-06-15-pacs008-automation-iso-20022-interbank-payments-2026",
            "2026-06-14-bankstatementparser-transaction-intelligence-treasury-open-source-2026",
            "2026-06-07-autonomous-treasury-index-programmable-liquidity-tokenised-deposits-2026",
            "2026-05-25-programmable-liquidity-ai-tokenised-deposits-real-time-treasury-2026",
            "2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001",
        ],
    },
    "operational-resilience-dora": {
        "title": "Operational Resilience & DORA",
        "banner": "https://cloudcdn.pro/stocks/images/simone-hutsch-oqlh6RsrYB0.webp",
        "lede": (
            "DORA Article 5 board accountability, BCBS 239 risk-data aggregation, "
            "third-party concentration risk, exit testing, and the engineering "
            "controls that turn operational resilience from a compliance project "
            "into a supervisor-ready scoreboard."
        ),
        "slugs": [
            "2026-06-08-banking-resilience-index-ai-cloud-quantum-payments-third-party-risk-2026",
            "2026-06-05-cloud-native-banking-index-dora-resilience-platform-engineering-2026",
            "2026-05-28-dora-ai-act-data-sovereignty-banking-compliance-stack-2026",
            "2026-05-16-best-cloud-infrastructure-architecture-2026",
        ],
    },
    "stablecoins-tokenisation": {
        "title": "Stablecoins & Tokenisation",
        "banner": "https://cloudcdn.pro/stocks/images/christopher-burns-Kj2SaNHG-hg.webp",
        "lede": (
            "Tokenised deposits, money-market funds, wholesale CBDC pilots, "
            "BlackRock's BRSRV/BSTBL, the GENIUS Act, and the engineering choices "
            "behind making programmable money work inside regulated balance "
            "sheets."
        ),
        "slugs": [
            "2026-05-30-uk-wholesale-digital-markets-tokenised-gilts-settlement-2026",
            "2026-05-28-digital-assets-tokenisation-stablecoins-bank-strategy-infrastructure-transition-2026",
            "2026-05-26-stablecoins-vs-tokenised-deposits-bank-strategy-2026",
            "2026-05-25-programmable-liquidity-ai-tokenised-deposits-real-time-treasury-2026",
            "2026-05-24-uk-payments-forward-plan-stablecoins-open-banking-tokenised-payments-2026",
            "2026-05-21-tokenised-deposits-banking-services-status-2026",
            "2026-05-15-blackrock-brsrv-bstbl-genius-act-tokenised-mmf",
        ],
    },
    "generative-ai-llms": {
        "title": "Generative AI & LLMs",
        "banner": "https://cloudcdn.pro/stocks/images/mm1-visual.webp",
        "lede": (
            "Foundation models, multimodal LLMs (Gemini, Gemma, Mistral, MM1), "
            "prompt engineering, and the open-source releases that shape what "
            "banks can build inside their own data perimeter."
        ),
        "slugs": [
            "2024-03-18-advancing-ai-with-multimodal-llms-insights-from-mm1",
            "2024-03-04-le-chat-by-mistral-ai-a-new-era-in-conversational-ai",
            "2024-02-26-google-gemma-ai-transforming-open-source-ai-development",
            "2024-02-19-unlocking-gemini-google-ai-revolution-explained",
            "2024-01-23-advancements-in-ai-prompt-engineering",
            "2024-01-01-ai-trends-2024-insights-and-predictions-for-the-future",
            "2023-11-12-exploring-generative-ai",
        ],
    },
    "voice-speech-ai": {
        "title": "Voice & Speech AI",
        "banner": "https://cloudcdn.pro/stocks/images/akande-voice-assistant-office.webp",
        "lede": (
            "Voice cloning, real-time speech recognition (Whisper), executive "
            "voice assistants, and the audio-intelligence stack reshaping the "
            "private-banking client experience."
        ),
        "slugs": [
            "2024-04-01-openvoice-leading-innovation-in-voice-cloning-technology",
            "2024-03-12-revolutionising-real-time-speech-recognition-on-macos-with-openai-whisper",
            "2024-02-12-akande-voice-assistant-revolutionising-personal-and-executive-assistance",
            "2024-01-29-ai-powered-audio-insights-analysis-translations",
        ],
    },
    "ai-governance-regulation": {
        "title": "AI Governance & Regulation",
        "banner": "https://cloudcdn.pro/stocks/images/getty-images-LaU3HadwEeE-unsplash.webp",
        "lede": (
            "EU AI Act conformity, SR 11-7 model risk, board-level accountability, "
            "auditability of autonomous workflows, and the regulatory frame for "
            "AI inside Tier-1 banks."
        ),
        "slugs": [
            "2026-07-01-agentic-ai-index-banks-measuring-autonomy-2026",
            "2026-06-03-agentic-ai-index-banks-autonomy-governance-auditability-2026",
            "2026-05-28-dora-ai-act-data-sovereignty-banking-compliance-stack-2026",
            "2024-02-13-eus-ai-act-shaping-the-future-of-global-ai-regulation",
        ],
    },
    "wholesale-payments-rails": {
        "title": "Wholesale Payments Rails",
        "banner": "https://cloudcdn.pro/stocks/images/viktor-forgacs-KxVRDiFdTVo.webp",
        "lede": (
            "Multi-rail strategy across cards, A2A, RTP, FedNow, open banking, "
            "and stablecoin corridors. Wholesale economics, settlement finality, "
            "and the BIS Project Agorá cross-border atomicity model."
        ),
        "slugs": [
            "2026-07-24-global-payments-outlook-operating-model-risk-revenue",
            "2026-06-06-wholesale-payments-index-iso20022-tokenised-deposits-cross-border-2026",
            "2026-06-01-multi-rail-bank-cards-a2a-stablecoins-rtp-fednow-open-banking-2026",
            "2026-05-31-post-quantum-payments-infrastructure-replace-rather-than-retrofit-2026",
            "2026-05-24-uk-payments-forward-plan-stablecoins-open-banking-tokenised-payments-2026",
            "2026-05-19-global-wholesale-payments-economics-2026",
        ],
    },
}


# Pillar grouping for the /topics/ hub. Each pillar has a name + one-line
# lede; the 14 topics fall under exactly one pillar. Apple-HIG principle:
# selective, well-grouped choices reduce hesitation. Edit the mapping
# below when the taxonomy shifts.
PILLARS: list[dict[str, object]] = [
    {
        "slug": "cryptography-resilience",
        "name": "Cryptography & resilience",
        "lede": "Post-quantum migration, DORA-grade operational resilience, and the governance framework around AI in financial services.",
        "topics": [
            "post-quantum-cryptography",
            "operational-resilience-dora",
            "ai-governance-regulation",
        ],
    },
    {
        "slug": "payments-money",
        "name": "Payments & money",
        "lede": "ISO 20022 migration, wholesale settlement, stablecoins, tokenised deposits, and the corporate treasury function around them.",
        "topics": [
            "iso-20022-payments",
            "wholesale-payments-rails",
            "stablecoins-tokenisation",
            "treasury-automation",
        ],
    },
    {
        "slug": "ai-cloud",
        "name": "AI & cloud",
        "lede": "Applied AI, agentic systems, generative models, voice and speech AI, and the cloud-native banking platforms that host them.",
        "topics": [
            "applied-ai-banking",
            "agentic-ai-banking",
            "generative-ai-llms",
            "voice-speech-ai",
            "cloud-native-banking",
        ],
    },
    {
        "slug": "open-source-craft",
        "name": "Open source & craft",
        "lede": "Rust libraries, blockchain primitives, and the open-source engineering discipline behind them.",
        "topics": [
            "rust-open-source",
            "blockchain-digital-assets",
        ],
    },
]


def read_frontmatter(slug: str) -> dict[str, str]:
    """Parse a post's YAML frontmatter into a flat dict. Returns {} if
    the slug doesn't resolve to a file — callers warn/exit on that case."""
    return _core_read_frontmatter(POSTS / f"{slug}.md")


_DATED_FILE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-.+\.md$")


def _dated_post_frontmatter() -> list[tuple[str, str, dict[str, str]]]:
    """All dated ``_posts/`` entries as ``(date, slug, frontmatter)``
    rows, skipping files without parseable frontmatter."""
    dated: list[tuple[str, str, dict[str, str]]] = []
    if not POSTS.is_dir():
        return dated
    for md in POSTS.iterdir():
        if not _DATED_FILE_RE.match(md.name):
            continue
        fm = _core_read_frontmatter(md)
        if not fm:
            continue
        dated.append((md.stem[:10], md.stem, fm))
    return dated


def _discover_frontmatter_topic_assignments() -> dict[str, list[str]]:
    """Scan ``_posts/<date>-*.md`` for ``topic_clusters:`` frontmatter
    entries and return ``{cluster_key: [slug, ...]}`` (slugs in
    date-descending order so they sit at the top of each cluster after
    merging).

    Why: each article PR used to add itself to the relevant cluster(s)
    by hand-editing the ``TOPICS`` dict in this file. Multiple stacked
    PRs collided every time on those edits. Articles now self-assign
    via frontmatter (``topic_clusters: "iso-20022-payments, applied-ai-banking"``)
    and the merge happens at build time. PRs that don't set the field
    just don't appear in any topic page — same as before.
    """
    out: dict[str, list[str]] = {}
    dated = _dated_post_frontmatter()
    # Latest article first.
    dated.sort(key=lambda r: r[0], reverse=True)
    for _date, slug, fm in dated:
        raw = (fm.get("topic_clusters") or "").strip()
        if not raw:
            continue
        for cluster in (c.strip() for c in raw.split(",")):
            if cluster:
                out.setdefault(cluster, []).append(slug)
    return out


def _merge_frontmatter_assignments_into_topics() -> None:
    """Prepend each cluster's discovered slugs (already date-descending)
    onto the front of its hand-curated ``TOPICS[cluster]["slugs"]`` list,
    deduping while preserving order so a slug never appears twice in the
    same topic page."""
    assignments = _discover_frontmatter_topic_assignments()
    unknown_clusters: list[str] = []
    for cluster, slugs in assignments.items():
        if cluster not in TOPICS:
            unknown_clusters.append(cluster)
            continue
        existing: list[str] = list(TOPICS[cluster]["slugs"])  # type: ignore[arg-type]
        merged: list[str] = []
        seen: set[str] = set()
        for s in slugs + existing:
            if s in seen:
                continue
            seen.add(s)
            merged.append(s)
        TOPICS[cluster]["slugs"] = merged
    if unknown_clusters:
        # Don't hard-fail — an article referencing an unknown cluster
        # is recoverable (drop the bad reference at merge time). But
        # surface it so the typo gets caught.
        for c in sorted(set(unknown_clusters)):
            print(
                f"build_topics: warning — article frontmatter references "
                f"unknown topic_cluster '{c}'; skipping.",
                file=sys.stderr,
            )


_merge_frontmatter_assignments_into_topics()


def _format_date(iso_like: str) -> str:
    """Render a post 'date' frontmatter value as YYYY-MM-DD for <time>."""
    from datetime import datetime as _dt

    for fmt in ("%b %d, %Y", "%B %d, %Y", "%Y-%m-%d"):
        try:
            return _dt.strptime(iso_like, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return iso_like


def _field(fm: dict[str, str], key: str, default: str = "") -> str:
    return fm.get(key) or default


def _human_date(date_iso: str) -> str:
    from datetime import datetime as _dt

    try:
        return _dt.strptime(date_iso, "%Y-%m-%d").strftime("%b %-d, %Y")
    except ValueError:
        return date_iso


def render_card(slug: str, fm: dict[str, str]) -> str:
    """Render a single newsroom-card for the given post slug + frontmatter."""
    title = _field(fm, "title", slug)
    desc = _field(fm, "description")
    banner = _field(fm, "banner", "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp")
    banner_alt = _field(fm, "banner_alt", title)
    keywords = _field(fm, "keywords")
    eyebrow = " · ".join(k.strip().title() for k in keywords.split(",")[:3] if k.strip())
    date_iso = _format_date(_field(fm, "date", slug[:10]))
    date_human = _human_date(date_iso)

    url = f"/{slug}/index.html"
    e_title = html.escape(title, quote=True)
    e_desc = html.escape(desc)
    e_alt = html.escape(banner_alt, quote=True)
    e_eyebrow = html.escape(eyebrow)
    return (
        '<article class="newsroom-card">'
        f'<a class="newsroom-card-media" href="{url}" title="{e_title}">'
        f'<img alt="{e_alt}" src="{banner}" loading="lazy" decoding="async" width="600" height="600" />'
        "</a>"
        '<div class="newsroom-card-body">'
        f'<span class="newsroom-eyebrow">{e_eyebrow}</span>'
        f'<h3><a href="{url}" title="{e_title}">{e_title}</a></h3>'
        f'<p class="newsroom-meta"><time datetime="{date_iso}">{date_human}</time> · Sebastien Rousseau</p>'
        f'<p class="newsroom-excerpt">{e_desc}</p>'
        "</div>"
        "</article>"
    )


_TITLE_RE = re.compile(r"<title>([^<]*)</title>", re.IGNORECASE)
_DESC_RE = re.compile(r'<meta\s+name="description"\s+content="([^"]*)"', re.IGNORECASE)
_OG_TITLE_RE = re.compile(r'(<meta\s+property="og:title"\s+content=")[^"]*(")', re.IGNORECASE)
_OG_DESC_RE = re.compile(r'(<meta\s+property="og:description"\s+content=")[^"]*(")', re.IGNORECASE)
_OG_URL_RE = re.compile(r'(<meta\s+property="og:url"\s+content=")[^"]*(")', re.IGNORECASE)
_CANONICAL_RE = re.compile(r'(<link\s+rel="canonical"\s+href=")[^"]*(")', re.IGNORECASE)
_NEWSROOM_RE = re.compile(r'<section class="newsroom">[\s\S]*?</section>', re.IGNORECASE)
# After the editorial-overhaul, /articles/ no longer has `<section class="newsroom">`.
# Instead its <main> body is a `<div class="wrap report-wrap">…</div>` containing
# the FT-tier hero + filter form + card list. The topics generator swaps the
# whole wrap-div in that case so topics don't end up cloning the articles
# listing wholesale.
_MAIN_WRAP_RE = re.compile(
    r'(<main\b[^>]*>\s*)<div class="wrap[^"]*">[\s\S]*?</div>(\s*</main>)',
    re.IGNORECASE,
)


def _swap_main_body(shell: str, body: str) -> str:
    """Swap the listing body inside the shell's <main>. Tries the legacy
    `<section class="newsroom">` swap first (no-op now since /articles/
    moved off newsroom markup), then falls back to replacing the entire
    `<main>`'s wrap-div with the topics body."""
    out, n = _NEWSROOM_RE.subn(body, shell, count=1)
    if n:
        return out
    return _MAIN_WRAP_RE.sub(rf'\1<div class="wrap report-wrap">{body}</div>\2', shell, count=1)
_LDJSON_BLOCKS_RE = re.compile(
    r'<script type="application/ld\+json">[\s\S]*?</script>', re.IGNORECASE
)
# The forked /articles/ shell carries the site-wide `ap-hero` band whose
# <h1> is the author's name. Topic pages emit their own page-scoped <h1>
# ("Topics" on the hub, the cluster title on each pillar page), so keeping
# the shell hero would ship two <h1>s, the first one naming the wrong
# thing. Strip it and let the topic header be the page's only <h1>.
_AP_HERO_RE = re.compile(r'<section class="ap-hero">[\s\S]*?</section>\s*', re.IGNORECASE)


def _strip_shell_hero(shell: str) -> str:
    """Remove the shell's `ap-hero` section so each topic page has
    exactly one <h1>, the topic's own."""
    return _AP_HERO_RE.sub("", shell, count=1)


def _strip_extra_jsonld(shell: str) -> str:
    """The articles shell ships an ItemList JSON-LD block listing every
    article. Strip it — the topic page emits its own ItemList scoped to
    the cluster."""
    blocks = _LDJSON_BLOCKS_RE.findall(shell)
    if not blocks:
        return shell
    for b in blocks:
        if '"ItemList"' in b or '"itemListElement"' in b:
            shell = shell.replace(b, "", 1)
    return shell


def _build_topic_body(title: str, lede: str, cards: list[str], slug: str) -> str:
    return (
        '<section class="newsroom">'
        '<nav aria-label="Breadcrumb" class="topic-breadcrumb">'
        '<a href="/">Home</a> &middot; '
        '<a href="/topics/index.html">Topics</a> &middot; '
        f"<span>{html.escape(title)}</span>"
        "</nav>"
        '<header class="newsroom-section-head">'
        f'<p class="newsroom-kicker">TOPIC</p>'
        f"<h1>{html.escape(title)}</h1>"
        f'<p class="topic-lede">{html.escape(lede)}</p>'
        "</header>"
        '<h2 class="visually-hidden">Articles in this topic</h2>'
        '<div class="newsroom-grid">' + "".join(cards) + "</div>"
        "</section>"
    )


def _build_topic_jsonld(
    slug: str, title: str, lede: str, slugs: list[str], post_titles: list[str]
) -> str:
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
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Topics",
                        "item": f"{base}/topics/",
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": title,
                        "item": f"{base}/topics/{slug}/",
                    },
                ],
            },
        ],
    }
    return (
        '<script type="application/ld+json">'
        + _json.dumps(graph, separators=(",", ":"), ensure_ascii=False)
        + "</script>"
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
    out = _strip_shell_hero(out)
    out = _swap_main_body(out, body)

    page_title = f"{title} — Sebastien Rousseau"
    out = _TITLE_RE.sub(f"<title>{html.escape(page_title)}</title>", out, count=1)
    out = _DESC_RE.sub(
        f'<meta name="description" content="{html.escape(lede, quote=True)}"',
        out,
        count=1,
    )
    out = _OG_TITLE_RE.sub(rf"\1{html.escape(page_title, quote=True)}\2", out, count=1)
    out = _OG_DESC_RE.sub(rf"\1{html.escape(lede, quote=True)}\2", out, count=1)
    out = _OG_URL_RE.sub(rf"\1https://sebastienrousseau.com/topics/{slug}/\2", out, count=1)
    out = _CANONICAL_RE.sub(rf"\1https://sebastienrousseau.com/topics/{slug}/\2", out, count=1)

    # Inject our scoped JSON-LD just before </body>.
    out = re.sub(r"(</body>)", ldjson + r"\1", out, count=1)

    return f"topics/{slug}/index.html", out


def _render_topic_card(topic_slug: str) -> str:
    """Render a single topic card for the hub. Returns empty string if
    the slug is missing from TOPICS — surfaces a build warning instead."""
    spec = TOPICS.get(topic_slug)
    if not spec:
        sys.stderr.write(f"build_topics: PILLARS references unknown topic {topic_slug!r}\n")
        return ""
    title = html.escape(str(spec["title"]))
    lede = html.escape(str(spec["lede"]))
    banner = html.escape(str(spec.get("banner") or ""))
    count = len(spec["slugs"])  # type: ignore[arg-type]
    url = f"/topics/{topic_slug}/index.html"
    if banner:
        media = (
            f'<a class="newsroom-card-media" href="{url}" aria-label="{title}">'
            f'<img src="{banner}" alt="{title} topic banner" '
            f'loading="lazy" decoding="async" '
            f'width="800" height="800"></a>'
        )
    else:
        media = (
            f'<a class="newsroom-card-media" href="{url}" aria-label="{title}" '
            'style="background:linear-gradient(135deg,var(--cl-grey-100,#f1f3f7),var(--cl-grey-200,#e3e6ed));aspect-ratio:1/1"></a>'
        )
    return (
        '<article class="newsroom-card">' + media + '<div class="newsroom-card-body">'
        '<span class="newsroom-eyebrow">PILLAR · TOPIC</span>'
        f'<h3><a href="{url}">{title}</a></h3>'
        f'<p class="newsroom-excerpt">{lede}</p>'
        f'<p class="newsroom-meta">{count} article(s)</p>'
        "</div>"
        "</article>"
    )


def render_hub(shell: str) -> tuple[str, str]:
    """Topic-hub page: /topics/index.html grouped by pillar."""
    total_topics = sum(len(p["topics"]) for p in PILLARS)  # type: ignore[arg-type]
    total_articles = sum(len(spec["slugs"]) for spec in TOPICS.values())  # type: ignore[arg-type]

    # Pillar groups — each pillar gets a header + a 3-up card grid.
    pillar_sections: list[str] = []
    for pillar in PILLARS:
        pillar_slug = html.escape(str(pillar["slug"]))
        pillar_name = html.escape(str(pillar["name"]))
        pillar_lede = html.escape(str(pillar["lede"]))
        cards = "".join(_render_topic_card(t) for t in pillar["topics"])  # type: ignore[arg-type]
        pillar_sections.append(
            f'<section class="topic-pillar" id="pillar-{pillar_slug}" data-reveal>'
            '<header class="topic-pillar-head">'
            f'<p class="newsroom-kicker">PILLAR</p>'
            f'<h2>{pillar_name}</h2>'
            f'<p class="topic-pillar-lede">{pillar_lede}</p>'
            '</header>'
            f'<div class="newsroom-grid">{cards}</div>'
            "</section>"
        )

    # Pillar quick-nav (chips). Anchor links into each section — Apple-HIG
    # selective navigation, no full filter UI for 14 items.
    chips = "".join(
        f'<a class="topic-chip" href="#pillar-{html.escape(str(p["slug"]))}">{html.escape(str(p["name"]))}</a>'
        for p in PILLARS
    )

    body = (
        '<section class="newsroom topic-hub">'
        '<nav aria-label="Breadcrumb" class="topic-breadcrumb">'
        '<a href="/">Home</a> &middot; <span>Topics</span></nav>'
        '<header class="newsroom-section-head topic-hub-head" data-reveal>'
        '<p class="newsroom-kicker">PILLARS</p>'
        "<h1>Topics</h1>"
        '<p class="topic-lede">Four pillars, fourteen topic clusters, every dated article. '
        'Pick a thread and follow it through the archive.</p>'
        f'<nav class="topic-chips" aria-label="Jump to pillar">{chips}</nav>'
        "</header>"
        '<section class="proof-rail topic-proof" aria-label="Topics at a glance">'
        f'<div class="kpi-cell"><span class="kpi-cell-value">{len(PILLARS)}</span><span class="kpi-cell-label">Pillars</span></div>'
        f'<div class="kpi-cell"><span class="kpi-cell-value">{total_topics}</span><span class="kpi-cell-label">Topic clusters</span></div>'
        f'<div class="kpi-cell"><span class="kpi-cell-value">{total_articles}</span><span class="kpi-cell-label">Articles indexed</span></div>'
        '</section>'
        + "".join(pillar_sections)
        + "</section>"
    )
    out = _strip_extra_jsonld(shell)
    out = _strip_shell_hero(out)
    out = _swap_main_body(out, body)
    title = "Topics — Sebastien Rousseau"
    desc = "Curated topic clusters covering post-quantum cryptography, ISO 20022, applied AI in banking, Rust open source, and digital assets."
    out = _TITLE_RE.sub(f"<title>{html.escape(title)}</title>", out, count=1)
    out = _DESC_RE.sub(
        f'<meta name="description" content="{html.escape(desc, quote=True)}"', out, count=1
    )
    out = _OG_TITLE_RE.sub(rf"\1{html.escape(title, quote=True)}\2", out, count=1)
    out = _OG_DESC_RE.sub(rf"\1{html.escape(desc, quote=True)}\2", out, count=1)
    out = _OG_URL_RE.sub(r"\1https://sebastienrousseau.com/topics/\2", out, count=1)
    out = _CANONICAL_RE.sub(r"\1https://sebastienrousseau.com/topics/\2", out, count=1)
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
