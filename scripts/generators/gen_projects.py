#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Rewrite the body of _posts/projects.md into Apple-Newsroom-style markup.

Featured project at the top, then category sections (AI, Quantum, Rust, …) each as
its own Newsroom grid of cards.
"""

from __future__ import annotations

import sys as _sys  # path bootstrap — scripts reorg (scripts/lib/ on sys.path)
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "lib"))

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


# (eyebrow, title, image, image_alt, summary, href)
def P(*a):
    return a


CATEGORIES = [
    {
        "kicker": "AUTOMATED FINANCIAL INFRASTRUCTURE",
        "title": "Financial data, untangled.",
        "lede": "Payment files and bank statements, without the friction. These tools generate the full ISO 20022 message lifecycle and parse messy real-world statements with deterministic precision. Bring your CSVs, PDFs, or databases. The data just flows.",
        "items": [
            P(
                "Featured · Python · ISO 20022",
                "pain001",
                "https://cloudcdn.pro/clients/pain001/v1/logos/pain001.svg",
                "Banner for the pain001 open-source payments library",
                "Generates ISO 20022 pain.001 files from CSV or SQLite. Banks and payment providers use it to produce structured credit-transfer messages without rebuilding existing systems.",
                "https://pain001.com",
            ),
            P(
                "Python · ISO 20022",
                "pacs008",
                "https://cloudcdn.pro/clients/pacs008/v1/logos/pacs008.svg",
                "Banner for the pacs008 ISO 20022 toolkit",
                "Generates, validates, and delivers ISO 20022 pacs.008 messages for bank-to-bank customer credit transfers. Includes JSON Schema and XSD validation, IBAN checks across 75 countries, and PII masking for GDPR and PCI-DSS.",
                "https://pacs008.com/",
            ),
            P(
                "Python · ISO 20022 suite",
                "camt053",
                "https://cloudcdn.pro/clients/camt053/v1/logos/camt053.svg",
                "Logo for the camt053 bank-statement suite",
                "Reads ISO 20022 camt.053 bank-to-customer statements and extracts balances, entries, and transaction detail into structured data. Includes MT940 loading, XLSX export, and editor and AI-assistant integrations.",
                "https://github.com/sebastienrousseau/camt053",
            ),
            P(
                "Python · ISO 20022 suite",
                "acmt001",
                "https://cloudcdn.pro/clients/acmt001/v1/logos/acmt001.svg",
                "Logo for the acmt001 account-management suite",
                "ISO 20022 account-management messaging. Opens, maintains, closes, switches, and verifies bank accounts from plain data files, with editor and AI-assistant tooling.",
                "https://github.com/sebastienrousseau/acmt001",
            ),
            P(
                "Python · Finance",
                "Bank Statement Parser",
                "https://cloudcdn.pro/clients/bankstatementparser/v1/logos/bankstatementparser.svg",
                "Banner for Bank Statement Parser",
                "A Python toolkit that turns bank statements in several formats into structured data. Built for messy real-world files and for audit requirements.",
                "https://bankstatementparser.com/",
            ),
            P(
                "Rust · Treasury · AI",
                "NaluFX",
                "https://cloudcdn.pro/clients/nalufx/v1/logos/nalufx.svg",
                "Logo for NaluFX, AI-driven cash allocation in Rust",
                "A Rust application for cash allocation across fund structures, using forecasting to inform the split. Aimed at treasury, fund accounting, and asset allocation.",
                "https://github.com/sebastienrousseau/nalufx",
            ),
            P(
                "Rust · Payments QR",
                "QRC",
                "https://cloudcdn.pro/clients/qrc/v1/logos/qrc.svg",
                "Logo for QRC, a Rust QR-code library",
                "A Rust library for generating and reading QR codes in several formats. Payment uses include EPC QR codes for SEPA credit transfers, payment links for merchant collection, and step-up authentication.",
                "https://github.com/sebastienrousseau/qrc",
            ),
        ],
    },
    {
        "kicker": "POST-QUANTUM FINANCIAL SECURITY",
        "title": "Quantum-safe. Enterprise ready.",
        "lede": "Security built for the quantum era, applied today. These libraries track the NIST standards for key encapsulation and hashing, so you can future-proof financial infrastructure long before the threat lands.",
        "items": [
            P(
                "Rust · Quantum",
                "KyberLib",
                "https://cloudcdn.pro/clients/kyberlib/v1/logos/kyberlib.svg",
                "Banner for KyberLib",
                "A Rust implementation of CRYSTALS-Kyber, the NIST FIPS 203 standard for post-quantum key encapsulation.",
                "https://kyberlib.com/",
            ),
            P(
                "Rust · Security",
                "Hash (HSH)",
                "https://cloudcdn.pro/clients/hsh/v1/logos/hsh.svg",
                "Banner for the Hash (HSH) Rust library",
                "Hash and digest algorithms for password storage and verification, written with a quantum-resistant posture in mind.",
                "https://github.com/sebastienrousseau/hsh",
            ),
            P(
                "Rust · Security",
                "Password Generator Pro",
                "https://cloudcdn.pro/clients/password-generator-pro/v1/logos/password-generator-pro.svg",
                "Banner for Password Generator Pro",
                "A cross-platform command-line tool for generating random passwords, backed by audited cryptographic primitives.",
                "https://password-generator.pro",
            ),
        ],
    },
    {
        "kicker": "APPLIED AI & EXECUTIVE INTELLIGENCE",
        "title": "Ask a question. Get the briefing.",
        "lede": "AI put to work on everyday operations. Scan code for vulnerabilities, turn a question into a structured briefing, and work by voice. On your terms, without vendor lock-in.",
        "items": [
            P(
                "AI · Security",
                "Euxis",
                "https://cloudcdn.pro/clients/euxis/v1/logos/euxis.svg",
                "Banner for Euxis, an open-source code security scanner",
                "A code security scanner for eight languages that pairs static and taint analysis with LLM verification to cut false positives. Outputs Sigstore-signed SARIF, SBOM, and OpenVEX bundles for supply-chain review.",
                "https://github.com/sebastienrousseau/euxis",
            ),
            P(
                "AI · Voice",
                "Àkàndé",
                "https://cloudcdn.pro/clients/akande/v1/logos/akande.svg",
                "Banner for Àkàndé, an advanced AI voice assistant",
                "A voice assistant built on OpenAI's GPT models, with PDF summaries and response caching. Suitable for personal and executive use.",
                "https://akande.co/",
            ),
            P(
                "AI · Speech",
                "Audio Analyser",
                "https://cloudcdn.pro/clients/audioanalyser/v1/logos/audioanalyser.svg",
                "Banner for Audio Analyser",
                "Converts audio to text in real time using AI speech recognition. Aimed at analysing recorded conversations and meetings.",
                "https://audioanalyser.co/",
            ),
            P(
                "JavaScript · Security",
                "Crypto Service Suite",
                "https://cloudcdn.pro/clients/crypto-service/v1/logos/crypto-service.svg",
                "Banner for the Crypto Service Suite",
                "A cryptographic service for common application needs: encryption, tokenisation, transaction authorisation, code signing, and key lifecycle management.",
                "https://github.com/sebastienrousseau/crypto-service",
            ),
        ],
    },
    {
        "kicker": "SOVEREIGN ENTERPRISE TECH",
        "title": "Your hardware. Your data.",
        "lede": "Foundations you can own. Audited, memory-safe Rust libraries that run on your infrastructure and ship with a software bill of materials and a Sigstore signature. Read every line. Vendor it. Keep it in-house.",
        "items": [
            P(
                "Rust · SSG",
                "Static Site Generator",
                "https://cloudcdn.pro/clients/static-site-generator/v1/logos/static-site-generator.svg",
                "Banner for the Static Site Generator",
                "A static site generator in Rust, secure by default. It includes WCAG AAA validation, CSP and SRI hardening, a local LLM content pipeline, a WebAssembly target, and 28-locale support.",
                "https://github.com/sebastienrousseau/static-site-generator",
            ),
            P(
                "Rust · YAML",
                "noyalib",
                "https://cloudcdn.pro/clients/noyalib/v1/logos/noyalib.svg",
                "Banner for the noyalib Rust YAML 1.2 ecosystem",
                "A pure-Rust YAML 1.2 implementation. Zero unsafe code, full spec compliance, streaming serde, a lossless syntax tree, and JSON-Schema validation. Ships as a library, CLI, language server, MCP server, and WASM build.",
                "https://github.com/sebastienrousseau/noyalib",
            ),
            P(
                "Rust · Serialisation",
                "Serde YML",
                "https://cloudcdn.pro/clients/serde_yml/v1/logos/serde_yml.svg",
                "Banner for Serde YML",
                "YAML serialisation and deserialisation for Rust data structures, built on the Serde framework.",
                "https://serdeyml.com/",
            ),
            P(
                "Rust · Logging",
                "RustLogs (RLG)",
                "https://cloudcdn.pro/clients/rlg/v1/logos/rlg.svg",
                "Banner for the RustLogs (RLG) library",
                "A logging library for Rust with structured formats, asynchronous logging, and configurable output.",
                "https://rustlogs.com/",
            ),
            P(
                "Rust · Tooling",
                "LibMake",
                "https://cloudcdn.pro/clients/libmake/v1/logos/libmake.svg",
                "Banner for LibMake",
                "A scaffold generator for Rust libraries. It emits pre-filled template files for tests, benchmarks, and CI.",
                "https://github.com/sebastienrousseau/libmake",
            ),
            P(
                "Rust · Time",
                "DateTime (DTT)",
                "https://cloudcdn.pro/clients/dtt/v1/logos/dtt.svg",
                "Banner for the DateTime (DTT) Rust library",
                "A date and time library for Rust: ISO 8601 formatting, time-zone handling, and access to individual date components.",
                "https://github.com/sebastienrousseau/dtt",
            ),
            P(
                "Rust · Math",
                "Random (VRD)",
                "https://cloudcdn.pro/clients/vrd/v1/logos/vrd.svg",
                "Banner for the Random (VRD) Rust library",
                "Random number generation based on the Mersenne Twister algorithm, used in simulations and games.",
                "https://vrdlib.com/",
            ),
            P(
                "Rust · Math",
                "Common (CMN)",
                "https://cloudcdn.pro/clients/cmn/v1/logos/cmn.svg",
                "Banner for the Common (CMN) Rust library",
                "A Rust library for accessing mathematical and cryptographic constants.",
                "https://github.com/sebastienrousseau/cmn",
            ),
            P(
                "Rust · Utility",
                "Mini Functions",
                "https://cloudcdn.pro/clients/mini-functions/v1/logos/mini-functions.svg",
                "Banner for the Mini Functions Rust library",
                "A utility and wrapper-function library for Rust.",
                "http://minifunctions.com/",
            ),
        ],
    },
    {
        "kicker": "WEB, PUBLISHING & ENVIRONMENT",
        "title": "Ship it your way.",
        "lede": "Templates, a CSS framework, two industry publications, and the reproducible setup that ships them all. The stack this site runs on.",
        "items": [
            P(
                "Web · Template",
                "Kaishi",
                "https://cloudcdn.pro/clients/kaishi/v1/logos/kaishi.svg",
                "Banner for Kaishi, a starter template",
                "A starter template for the Static Site Generator, set up for clean and accessible sites. The template I use when starting a new site.",
                "https://github.com/sebastienrousseau/kaishi.github.io",
            ),
            P(
                "CSS · Stylus",
                "Skeletonic Stylus",
                "https://cloudcdn.pro/clients/skeletonic/v1/logos/skeletonic.svg",
                "Banner for the Skeletonic Stylus Library",
                "A modular Stylus library with components and mixins for web and mobile layouts. This site is built on it.",
                "https://github.com/sebastienrousseau/skeletonic-stylus",
            ),
            P(
                "Web · Publication",
                "Banking On AI",
                "https://cloudcdn.pro/clients/bankingonai/v1/logos/bankingonai.svg",
                "Banner for the Banking On AI publication",
                "A publication on how banks are applying AI, covering customer service, fraud detection, and operations.",
                "https://bankingonai.co/",
            ),
            P(
                "Web · Publication",
                "Banking On Quantum",
                "https://cloudcdn.pro/clients/bankingonquantum/v1/logos/bankingonquantum.svg",
                "Banner for the Banking On Quantum publication",
                "A publication on quantum computing in banking and finance, from risk analysis to cryptography.",
                "https://bankingonquantum.com/",
            ),
            P(
                "Web · Finance",
                "L90S",
                "https://cloudcdn.pro/clients/l90s/v1/logos/l90s.svg",
                "Banner for the L90S website",
                "Fractional CFO advisory from a finance leader with more than 20 years in technology, covering growth, funding, and financial operations.",
                "https://l90s.com/",
            ),
            P(
                "Config · Cross-platform",
                "Dotfiles",
                "https://cloudcdn.pro/clients/dotfiles/v2/images/logos/dotfiles.svg",
                "Banner for the Dotfiles project",
                "Configuration files for macOS, Linux, and Windows: scripts and settings for a development workflow.",
                "https://dotfiles.io/",
            ),
        ],
    },
]


# Project images are almost all wide brand banners (logo SVGs); a handful are stock photos
# (.webp). The logo treatment fits-inside on a white panel; photos get the default cover crop.
def _is_logo(image: str) -> bool:
    lower = image.lower()
    if lower.endswith(".webp"):
        return "logo" in lower or "github-" in lower
    return True


def featured_block(item: tuple) -> str:
    eyebrow, title, image, alt, summary, href = item
    media_cls = "newsroom-featured-media logo" if _is_logo(image) else "newsroom-featured-media"
    return f"""<article class="newsroom-featured">
<a class="{media_cls}" href="{href}" title="{title}">
<img alt="{alt}" src="{image}" loading="eager" fetchpriority="high" decoding="async" width="800" height="800" />
</a>
<div class="newsroom-featured-body">
<span class="newsroom-eyebrow">{eyebrow}</span>
<h3><a href="{href}" title="{title}">{title}</a></h3>
<p>{summary}</p>
<p><a class="pill ghost" href="{href}" title="Learn about {title}">Learn about {title}</a></p>
</div>
</article>"""


def card_block(item: tuple) -> str:
    # Apple One-style card: app icon top-left, name, description, "Learn more".
    # Borderless (styled in index.html). eyebrow is intentionally unused here.
    _eyebrow, title, image, alt, summary, href = item
    media_cls = "newsroom-card-media logo" if _is_logo(image) else "newsroom-card-media"
    return f"""<article class="newsroom-card">
<a class="{media_cls}" href="{href}" title="{title}">
<img alt="{alt}" src="{image}" loading="lazy" decoding="async" width="600" height="600" />
</a>
<div class="newsroom-card-body">
<h3><a href="{href}" title="{title}">{title}</a></h3>
<p class="newsroom-excerpt">{summary}</p>
<p class="newsroom-more"><a href="{href}" title="{title}">Learn more <span aria-hidden="true">›</span></a></p>
</div>
</article>"""


def section_block(cat: dict) -> str:
    head = (
        f'<header class="newsroom-section-head"><p class="newsroom-kicker">{cat["kicker"]}</p><h2>{cat["title"]}</h2>'
        + (f'<p class="newsroom-lede">{cat["lede"]}</p>' if cat.get("lede") else "")
        + "</header>"
    )
    if cat.get("is_featured"):
        return head + "\n\n" + featured_block(cat["items"][0])
    cards = "\n\n".join(card_block(i) for i in cat["items"])
    return head + '\n\n<div class="newsroom-grid">\n\n' + cards + "\n\n</div>"


# Three areas of practice — full-bleed alternating image/text panels
# (Apple "section-content" pattern). Each panel lands on a dedicated
# success-story page. `reverse` flips the image to the right.
AREAS = [
    {
        "kicker": "PAYMENTS & ISO 20022",
        "headline": 'Payments in the global <span class="ac">standard.</span>',
        "body": (
            "ISO&nbsp;20022 covers the full message lifecycle. These libraries "
            "generate <strong>pain.001</strong> initiation files, build and "
            "validate <strong>pacs.008</strong> transfers, read "
            "<strong>camt.053</strong> statements, and handle "
            "<strong>acmt.001</strong> account management, with parsers for "
            "older formats. You can adopt one library at a time instead of "
            "replacing a core system."
        ),
        "cta_label": "Read the payments story",
        "cta_href": "/projects-payments/index.html",
        "img": "https://cloudcdn.pro/stocks/images/denys-nevozhai-2vmT5_FeMck-1920.webp",
        "img_alt": "Aerial view of city interchanges at night, representing cross-border payment rails.",
        "reverse": False,
    },
    {
        "kicker": "POST-QUANTUM SECURITY",
        "headline": 'Security past the <span class="ac">RSA era.</span>',
        "body": (
            "Some financial records stay sensitive for decades, long enough "
            "that data captured today could be read once quantum computers "
            "mature. These Rust libraries implement <strong>ML-KEM "
            "(CRYSTALS-Kyber, NIST&nbsp;FIPS&nbsp;203)</strong> along with "
            "hashing and related primitives, so a migration can begin before "
            "the deadlines force it."
        ),
        "cta_label": "Read the security story",
        "cta_href": "/projects-post-quantum/index.html",
        "img": "https://cloudcdn.pro/stocks/images/galina-nelyubova-V70-ng4FuiA-1920.webp",
        "img_alt": "Abstract blue light field, representing post-quantum cryptography for financial systems.",
        "reverse": True,
    },
    {
        "kicker": "DEVELOPER PLATFORM",
        "headline": 'Foundations for your <span class="ac">engineers.</span>',
        "body": (
            "The same Rust libraries that build and secure this site. They "
            "include <strong>noyalib</strong> for YAML and the <strong>Static "
            "Site Generator</strong> itself, published with CycloneDX SBOMs and "
            "Sigstore signatures. Your engineers build on them instead of "
            "maintaining the equivalents in-house."
        ),
        "cta_label": "Read the platform story",
        "cta_href": "/projects-developer-platform/index.html",
        "img": "https://cloudcdn.pro/stocks/images/alex-shuper-YYZnrK8NrSw-unsplash-1920.webp",
        "img_alt": "Clean architectural lines in soft light, representing dependable developer foundations.",
        "reverse": False,
    },
]


FAQ_ITEMS = [
    (
        "What licence are these projects released under?",
        "Most projects are dual-licensed under MIT and Apache-2.0, the standard "
        "for the Rust ecosystem, which gives commercial users explicit patent "
        "rights as well as permissive redistribution. A small number of clients' "
        "tools are released under Apache-2.0 only. The licence file at the root "
        "of each repository is the authoritative source.",
    ),
    (
        "Are these projects production-ready?",
        'Many are. <a href="https://pain001.com">pain001</a> is used by banks '
        "and payment-service providers to automate ISO&nbsp;20022 file creation. "
        '<a href="https://kyberlib.com">KyberLib</a> tracks the NIST FIPS&nbsp;203 '
        "specification and ships test vectors. Each repository's README and CI "
        "badges will tell you the current status; if you need a specific guarantee "
        "for production use, get in touch.",
    ),
    (
        "How can I contribute or report an issue?",
        "Every project has a public GitHub repository under "
        '<a href="https://github.com/sebastienrousseau" rel="external noopener">github.com/sebastienrousseau</a>. '
        "Open an issue describing the problem (a minimal reproducer helps) or a "
        "pull request linked to an issue. Contributions are governed by the "
        "Developer Certificate of Origin and require signed commits.",
    ),
    (
        "Can I use these libraries in a regulated banking environment?",
        "Yes, with the usual caveats. The libraries are independent open-source "
        "work, not a regulated product. Run your normal supply-chain, security, "
        "and dependency-review processes, such as vendoring through your internal mirror, "
        "scanning with SBOM tools, and pinning by Git SHA or cryptographic hash, "
        "before deploying to production payment infrastructure.",
    ),
    (
        "Do you offer commercial support or consulting?",
        "Yes, on a selective basis. Engagements focus on ISO&nbsp;20022 migration, "
        "post-quantum cryptography migration roadmaps, and applied AI in "
        'financial services. <a href="/contact/index.html">Get in touch</a> with '
        "a short brief, your timeline and any constraints.",
    ),
    (
        "How do I follow new releases?",
        "Every dated post on this site is announced through the "
        '<a href="/rss.xml">RSS feed</a> and the '
        '<a href="https://news.bankingonquantum.com" rel="external noopener">Banking On Quantum</a> '
        "newsletter. Individual repositories also publish releases on GitHub, "
        "which you can watch directly.",
    ),
]


def setup_hero_block() -> str:
    """Single eyebrow + CTA strip that sits directly below the layout's
    ap-hero (which already carries the page H1 + subtitle via frontmatter).
    Centered, no duplicate headline."""
    # Rotating ending — pure CSS (no JS, CSP-safe). The animation is
    # aria-hidden; the <p> carries the full phrase as an aria-label for AT.
    # The first word repeats as a 5th cell so the loop resets seamlessly.
    words = ["banks.", "financial institutions.", "enterprise.", "small business."]
    cells = "".join(f"<span>{w}</span>" for w in [*words, words[0]])
    return (
        '<p class="setup-hero-eyebrow rotating-title"'
        ' aria-label="Open source for banks, financial institutions, enterprise and small business.">'
        '<span class="rotating-title-lead">Open source for</span>'
        '<span class="rotating-title-mask" aria-hidden="true">'
        f'<span class="rotating-title-words">{cells}</span>'
        "</span>"
        "</p>\n"
        '<p class="setup-hero-cta">\n'
        '<a class="pill" href="/contact/index.html">Talk to us</a>\n'
        '<a class="pill ghost" href="#catalog">Browse all products</a>\n'
        "</p>"
    )


def proof_rail_block() -> str:
    """Apple-HIG proof rail. Reads _data/proof/metrics.json so the numbers
    stay in sync with the case-studies hub and the home-page stats. If the
    metrics file is missing or unreadable, render zero values rather than
    breaking the build — postbuild link audit will surface the issue."""
    import json

    metrics_path = ROOT / "_data" / "proof" / "metrics.json"
    stats = {}
    try:
        payload = json.loads(metrics_path.read_text())
        for entry in payload.get("stats", []):
            stats[entry["key"]] = entry
    except (OSError, ValueError, KeyError):
        stats = {}

    def _fmt(key: str, fallback: str) -> str:
        entry = stats.get(key)
        if not entry:
            return fallback
        value = entry["value"]
        fmt = entry.get("format", "plain")
        if fmt == "compact" and isinstance(value, int | float):
            n = float(value)
            if n >= 1_000_000:
                return f"{n / 1_000_000:.1f}M".replace(".0M", "M")
            if n >= 1_000:
                return f"{n / 1_000:.0f}k"
            return str(int(n))
        return str(value)

    downloads = _fmt("downloads_total", "42.1M")
    stars = _fmt("github_stars", "672")
    articles = _fmt("articles_signed", "96")
    years = _fmt("years_payments", "19")
    # Split each kpi-cell across multiple lines — SSG's custom-block parser
    # treats single-line <div class="x-y"> as a shortcode and replaces the
    # body with an error alert. Multi-line divs pass through as raw HTML.
    #
    # Each value span carries `data-kpi` so postbuild's inject_kpi_metrics
    # refreshes it on every build, not just on the runs that regenerate this
    # file. Without it this generator silently *stripped* the attributes from
    # the committed projects.md and froze the rail at generation time.
    return (
        '<section class="proof-rail projects-proof" aria-label="Open source by the numbers">\n'
        f'<div class="kpi-cell">\n  <span class="kpi-cell-value" data-kpi="downloads_total">{downloads}</span>\n  <span class="kpi-cell-label">Open-source downloads</span>\n</div>\n'
        f'<div class="kpi-cell">\n  <span class="kpi-cell-value" data-kpi="github_stars">{stars}</span>\n  <span class="kpi-cell-label">GitHub stars</span>\n</div>\n'
        f'<div class="kpi-cell">\n  <span class="kpi-cell-value" data-kpi="articles_signed">{articles}</span>\n  <span class="kpi-cell-label">Sigstore-signed articles</span>\n</div>\n'
        f'<div class="kpi-cell">\n  <span class="kpi-cell-value" data-kpi="years_payments">{years}</span>\n  <span class="kpi-cell-label">Years shipping in production</span>\n</div>\n'
        "</section>"
    )


def _area_card_img(area: dict, *, eager: bool) -> str:
    """The card's image tag; the first card's is the page's LCP element.

    Lazy-loading it deferred the largest paint to 1.8 s and cost the page its
    performance budget — 0.93 against a 0.94 floor, identical across all three
    Lighthouse runs, so not noise. It also left /projects/ with NO non-lazy
    image at all, which made postbuild's inject_lcp_preload find no LCP
    candidate: it took its "nothing to preload" path and left the layout's
    preload pointing at a portrait this page never renders — a high-priority
    fetch of an unused image, competing with the real LCP.

    Eager-loading the first card fixes both halves, because it also gives
    inject_lcp_preload a candidate to realign that stale preload to.
    """
    loading = "eager" if eager else "lazy"
    priority = ' fetchpriority="high"' if eager else ""
    return (
        f'<img alt="{area["img_alt"]}" src="{area["img"]}" '
        f'loading="{loading}"{priority} decoding="async" '
        f'width="1600" height="1000" />'
    )


def setup_three_block() -> str:
    """Three areas of practice as Apple-style cards: large image on top, then
    kicker + headline (with an accent keyword) + body + CTA below, in a 3-up
    grid. Multi-line markup so SSG's custom-block parser passes it through as
    raw HTML. Each card lands on a dedicated success-story page."""
    cards = [
        f'<article class="area-card">\n'
        f'<figure class="area-card-media">\n'
        f"{_area_card_img(a, eager=(i == 0))}\n"
        f"</figure>\n"
        f'<div class="area-card-body">\n'
        f'<p class="area-card-kicker">{a["kicker"]}</p>\n'
        f'<h3 class="area-card-headline">{a["headline"]}</h3>\n'
        f'<p class="area-card-text">{a["body"]}</p>\n'
        f'<p class="area-card-cta">'
        f'<a href="{a["cta_href"]}">'
        f'{a["cta_label"]} <span aria-hidden="true">›</span></a></p>\n'
        f"</div>\n"
        f"</article>"
        for i, a in enumerate(AREAS)
    ]
    return (
        '<section class="setup-three" aria-labelledby="setup-three-heading">'
        '<header class="setup-three-head">'
        '<p class="setup-three-kicker">BUILT FOR FINANCIAL SERVICES</p>'
        '<h2 id="setup-three-heading" class="setup-three-headline">Three areas of work. <span class="setup-three-headline-soft">Payments, security, and tooling.</span></h2>'
        "</header>"
        '<div class="areas-grid">' + "\n".join(cards) + "</div>"
        "</section>"
    )


def faq_block() -> str:
    items = []
    for q, a in FAQ_ITEMS:
        items.append(
            f"""<details class="qa-item">
<summary class="qa-q">{q}</summary>
<section class="qa-a"><p>{a}</p></section>
</details>"""
        )
    return (
        '<section class="qa" aria-labelledby="projects-qa-heading">'
        '<header class="qa-head">'
        '<h2 id="projects-qa-heading" class="qa-headline">Questions? <span class="qa-headline-soft">Answers.</span></h2>'
        "</header>"
        '<section class="qa-list">' + "\n".join(items) + "</section>"
        "</section>"
    )


def bottom_cta_block() -> str:
    return """<aside class="setup-finale" aria-labelledby="projects-finale-heading">
<p class="setup-finale-eyebrow">CONTACT</p>
<h2 id="projects-finale-heading" class="setup-finale-headline">Build on it. Or build it with me.</h2>
<p class="setup-finale-lede">Planning an ISO 20022 migration, a post-quantum review, or applied AI in production? Tell me what you are building. I will show you where these tools fit.</p>
<p class="setup-finale-cta"><a class="pill" href="/contact/index.html">Get in touch</a></p>
</aside>"""


# Map kicker → anchor id used by the three theme cards above to deep-link
# into the relevant slice of the catalogue further down the page.
ANCHOR_MAP = {
    "AUTOMATED FINANCIAL INFRASTRUCTURE": "cat-payments",
    "POST-QUANTUM FINANCIAL SECURITY": "cat-quantum",
    "APPLIED AI & EXECUTIVE INTELLIGENCE": "cat-ai",
    "SOVEREIGN ENTERPRISE TECH": "cat-rust",
    "WEB, PUBLISHING & ENVIRONMENT": "cat-web",
}


def section_block_anchored(cat: dict) -> str:
    """Emit a centred section header (Apple Personal-Setup pattern) and a
    uniform 3-up card grid for the catalogue."""
    anchor = ANCHOR_MAP.get(cat["kicker"])
    id_attr = f' id="{anchor}"' if anchor else ""
    head = (
        f'<header class="cat-section-head"{id_attr}>'
        f'<p class="cat-kicker">{cat["kicker"]}</p>'
        f'<h2 class="cat-headline">{cat["title"]}</h2>'
        + (f'<p class="cat-lede">{cat["lede"]}</p>' if cat.get("lede") else "")
        + "</header>"
    )
    cards = "\n\n".join(card_block(i) for i in cat["items"])
    return head + '\n\n<div class="newsroom-grid cat-grid">\n\n' + cards + "\n\n</div>"


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Rewrite the projects.md listing body.")
    # `--dir` is REQUIRED, with no default — see ADR-0003. This generator
    # rewrites projects.md in place; defaulting to `_posts` meant a bare run
    # silently reverted committed source to the constants baked in above.
    # An intentional source regeneration must pass `--dir _posts` explicitly.
    parser.add_argument(
        "--dir",
        required=True,
        help="Directory containing projects.md (e.g. _posts). Required: this "
        "rewrites the file in place, so the target must be explicit (ADR-0003).",
    )
    args = parser.parse_args()

    src = Path(args.dir) / "projects.md"
    text = src.read_text()
    lines = text.splitlines(keepends=True)
    delim_idx = [i for i, ln in enumerate(lines) if ln.strip() == "---"]
    if len(delim_idx) < 2:
        raise SystemExit("could not locate frontmatter delimiters in projects.md")
    head = "".join(lines[: delim_idx[1] + 1])

    body_parts = [
        # The hero (rotating animated title + CTAs) now lives in the project
        # layout's ap-hero, so the body starts with the proof rail.
        proof_rail_block(),
        setup_three_block(),
        '<section class="newsroom" id="catalog">',
    ]
    body_parts.extend(section_block_anchored(c) for c in CATEGORIES)
    body_parts.append("</section>")
    body_parts.append(faq_block())
    body_parts.append(bottom_cta_block())
    body = "\n\n".join(body_parts) + "\n"

    src.write_text(head + "\n" + body)
    total_items = sum(len(c["items"]) for c in CATEGORIES)
    print(
        f"wrote {src}. hero + 3 themes + {len(CATEGORIES)} catalogue sections, {total_items} items, FAQ + bottom CTA"
    )


if __name__ == "__main__":
    main()
