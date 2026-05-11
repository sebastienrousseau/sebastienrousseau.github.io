#!/usr/bin/env python3
"""Rewrite the body of _posts/projects.md into Apple-Newsroom-style markup.

Featured project at the top, then category sections (AI, Quantum, Rust, …) each as
its own Newsroom grid of cards.
"""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_posts" / "projects.md"

# (eyebrow, title, image, image_alt, summary, href)
P = lambda *a: a

CATEGORIES = [
    {
        "kicker": "PAYMENTS",
        "title": "Payments and settlement.",
        "lede": "ISO 20022 tooling for the global migration. Pain.001 file generation, pacs.008 cross-border credit transfers, and structured bank-statement parsing.",
        "items": [
            P("Featured · Python · ISO 20022",
              "pain001",
              "https://cloudcdn.pro/clients/pain001/v1/github/github-pain001.svg",
              "Banner for the pain001 open-source payments library",
              "A Python library that automates ISO 20022 pain.001 payment file creation from CSV or SQLite. Built for the global migration to structured cross-border messages.",
              "https://pain001.com"),
            P("Python · ISO 20022",
              "pacs008",
              "https://pacs008.com/logo.webp",
              "Banner for the pacs008 ISO 20022 toolkit",
              "Generate, validate, and deliver ISO 20022 pacs.008 payment messages for FI-to-FI customer credit transfers. JSON Schema + XSD validation, IBAN across 75 countries, GDPR/PCI-DSS-compliant PII masking.",
              "https://pacs008.com/"),
            P("Python · Finance",
              "Bank Statement Parser",
              "https://cloudcdn.pro/clients/bankstatementparser/v1/github/github-bankstatementparser.svg",
              "Banner for Bank Statement Parser",
              "A finance-grade Python toolkit that turns multi-format bank statements into structured data — for the realities of real-world statement files and the audit demands of regulated environments.",
              "https://bankstatementparser.com/"),
        ],
    },
    {
        "kicker": "POST-QUANTUM CRYPTOGRAPHY",
        "title": "Post-quantum cryptography.",
        "lede": "Rust implementations of CRYSTALS-Kyber, hash and digest primitives, and quantum-resistant building blocks for financial-grade authentication.",
        "items": [
            P("Rust · Quantum",
              "KyberLib",
              "https://cloudcdn.pro/clients/kyberlib/v1/github/github-kyberlib.svg",
              "Banner for KyberLib",
              "A robust Rust implementation of CRYSTALS-Kyber, the NIST FIPS 203 standard for general-purpose post-quantum key encapsulation.",
              "https://kyberlib.com/"),
            P("Rust · Security",
              "Hash (HSH)",
              "https://cloudcdn.pro/clients/hsh/v1/github/github-hsh.svg",
              "Banner for the Hash (HSH) Rust library",
              "Secure hash and digest algorithms for password encryption and verification, designed with a quantum-resistant posture for the post-PQC era.",
              "https://github.com/sebastienrousseau/hsh"),
            P("Rust · Security",
              "Password Generator Pro",
              "https://cloudcdn.pro/clients/password-generator-pro/v1/github/github-password-generator-pro.svg",
              "Banner for Password Generator Pro",
              "A fast, simple, and powerful cross-platform CLI for generating strong, unique, and random passwords backed by audited cryptographic primitives.",
              "https://password-generator.pro"),
        ],
    },
    {
        "kicker": "AI AND VOICE",
        "title": "Applied artificial intelligence.",
        "lede": "Open-source AI projects applying speech recognition, natural language, and large language models to real-world finance and productivity problems.",
        "items": [
            P("AI · Voice",
              "Àkàndé",
              "https://cloudcdn.pro/clients/akande/v1/github/github-akande.svg",
              "Banner for Àkàndé, an advanced AI voice assistant",
              "An advanced voice assistant using OpenAI's GPT for natural interactions, PDF summaries, and efficient caching. Built for both personal and executive use.",
              "https://akande.co/"),
            P("AI · Speech",
              "Audio Analyser",
              "https://cloudcdn.pro/clients/audioanalyser/v1/github/github-audioanalyser.svg",
              "Banner for Audio Analyser",
              "Convert audio to text in real-time using advanced AI speech recognition. Designed to unlock actionable insights from audio data and enhance customer and employee experience.",
              "https://audioanalyser.co/"),
            P("JavaScript · Security",
              "Crypto Service Suite",
              "https://cloudcdn.pro/stocks/images/steven-wei-Z7NMhw8hcfg.webp",
              "Banner for the Crypto Service Suite",
              "A centralised cryptographic suite that solves common application crypto problems — encryption, tokenisation, transaction authorisation, code signing, and key lifecycle management.",
              "https://github.com/sebastienrousseau/crypto-service"),
        ],
    },
    {
        "kicker": "OPEN-SOURCE RUST",
        "title": "Rust libraries and tooling.",
        "lede": "Open-source Rust projects across serialisation, logging, code generation, math, and developer tooling — including the static site generator behind this site.",
        "items": [
            P("Rust · SSG",
              "Static Site Generator",
              "https://cloudcdn.pro/clients/shokunin/v1/github/github-shokunin.svg",
              "Banner for the Static Site Generator",
              "A secure-by-default static site generator in Rust. WCAG AAA validation, CSP/SRI hardening, local LLM content pipeline, WebAssembly target, and 28-locale i18n.",
              "https://github.com/sebastienrousseau/static-site-generator"),
            P("Rust · YAML",
              "noyalib",
              "https://cloudcdn.pro/clients/noyalib/v1/github/github-noyalib.svg",
              "Banner for the noyalib Rust YAML 1.2 ecosystem",
              "Pure-Rust YAML 1.2 ecosystem. Zero unsafe, 100% spec compliance, streaming-first serde, lossless CST, JSON-Schema validation. Library + CLI + LSP + MCP + WASM bindings.",
              "https://github.com/sebastienrousseau/noyalib"),
            P("Rust · Serialisation",
              "Serde YML",
              "https://cloudcdn.pro/clients/serde_yml/v1/github/github-serde_yml.svg",
              "Banner for Serde YML",
              "Effortless YAML serialisation and deserialisation of Rust data structures, built on the widely used Serde framework.",
              "https://serdeyml.com/"),
            P("Rust · Logging",
              "RustLogs (RLG)",
              "https://cloudcdn.pro/clients/rlg/v1/github/github-rlg.svg",
              "Banner for the RustLogs (RLG) library",
              "A flexible logging library for Rust with structured log formats, asynchronous logging, and extensive customisation options.",
              "https://rustlogs.com/"),
            P("Rust · Tooling",
              "LibMake",
              "https://cloudcdn.pro/clients/libmake/v1/github/github-libmake.svg",
              "Banner for LibMake",
              "A scaffold generator that quickly helps you create high-quality Rust libraries by emitting pre-filled, opinionated templated files.",
              "https://github.com/sebastienrousseau/libmake"),
            P("Rust · Time",
              "DateTime (DTT)",
              "https://cloudcdn.pro/clients/dtt/v1/github/github-dtt.svg",
              "Banner for the DateTime (DTT) Rust library",
              "A high-precision date and time library: day of the month, hour of the day, ISO 8601 formatting, time-zone safety, and much more.",
              "https://github.com/sebastienrousseau/dtt"),
            P("Rust · Math",
              "Random (VRD)",
              "https://cloudcdn.pro/clients/vrd/v1/github/github-vrd.svg",
              "Banner for the Random (VRD) Rust library",
              "High-quality random number generation based on the Mersenne Twister algorithm, widely used in simulations and games.",
              "https://vrdlib.com/"),
            P("Rust · Math",
              "Common (CMN)",
              "https://cloudcdn.pro/clients/cmn/v1/github/github-cmn.svg",
              "Banner for the Common (CMN) Rust library",
              "A modern, fast, user-friendly library that makes it easy to access a wide range of mathematical and cryptographic constants.",
              "https://github.com/sebastienrousseau/cmn"),
            P("Rust · Utility",
              "Mini Functions",
              "https://cloudcdn.pro/clients/mini-functions/v1/github/github-mini-functions.svg",
              "Banner for the Mini Functions Rust library",
              "A highly performant utility and wrapper functions library for Rust, designed with optimisation and efficiency in mind.",
              "http://minifunctions.com/"),
        ],
    },
    {
        "kicker": "WEB AND DEVELOPER ENVIRONMENT",
        "title": "Web, templates and environment.",
        "lede": "Starter templates, two industry-focused publications, a CSS framework, and the dotfiles that keep a development environment reproducible.",
        "items": [
            P("Web · Template",
              "Kaishi",
              "https://cloudcdn.pro/clients/kaishi/v1/titles/title-kaishi.svg",
              "Banner for Kaishi, a starter template",
              "A Static Site Generator starter template designed for clean, accessible, performant sites — the seed I reach for when shipping new content destinations.",
              "https://github.com/sebastienrousseau/kaishi.github.io"),
            P("CSS · Stylus",
              "Skeletonic Stylus",
              "https://cloudcdn.pro/clients/skeletonic/v1/logos/logo-skeletonic-stylus.svg",
              "Banner for the Skeletonic Stylus Library",
              "A lightweight, modular Stylus library with components and mixins optimised for mobile and web application design. This site is built on top of it.",
              "https://github.com/sebastienrousseau/skeletonic-stylus"),
            P("Web · Publication",
              "Banking On AI",
              "https://cloudcdn.pro/clients/bankingonai/v1/github/github-bankingonai.svg",
              "Banner for the Banking On AI publication",
              "How AI is transforming the banking sector — improved customer service, fraud detection, and streamlined operations for a digital age.",
              "https://bankingonai.co/"),
            P("Web · Publication",
              "Banking On Quantum",
              "https://cloudcdn.pro/clients/bankingonquantum/v1/github/github-bankingonquantum.svg",
              "Banner for the Banking On Quantum publication",
              "How quantum computing is set to revolutionise banking and finance, from risk analysis to quantum cryptography and beyond.",
              "https://bankingonquantum.com/"),
            P("Web · Finance",
              "L90S",
              "https://cloudcdn.pro/clients/l90s/v1/github/github-l90s.svg",
              "Banner for the L90S website",
              "Fractional CFO advisory by a trusted finance leader with 20+ years in tech, guiding companies to sustainable growth, funding, and optimised financial operations.",
              "https://l90s.com/"),
            P("Config · Cross-platform",
              "Dotfiles",
              "https://cloudcdn.pro/clients/dotfiles/v2/images/banners/dotfiles.webp",
              "Banner for the Dotfiles project",
              "A powerful set of configuration files for macOS, Linux, and Windows — scripts and customised settings to streamline a development workflow.",
              "https://dotfiles.io/"),
            P("Config · macOS",
              "MacConfig",
              "https://cloudcdn.pro/stocks/images/ibrahim-abazid-MgQnQZA4ByM.webp",
              "Banner for MacConfig (maccfg)",
              "A guide to getting a MacBook Pro M1 ready for software development. Set up and start using a new Mac with free resources and user guides.",
              "https://maccfg.com/"),
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
<p><a class="pill ghost" href="{href}" title="{title}" aria-label="Learn more about {title}">Learn more</a></p>
</div>
</article>"""


def card_block(item: tuple) -> str:
    eyebrow, title, image, alt, summary, href = item
    media_cls = "newsroom-card-media logo" if _is_logo(image) else "newsroom-card-media"
    return f"""<article class="newsroom-card">
<a class="{media_cls}" href="{href}" title="{title}">
<img alt="{alt}" src="{image}" loading="lazy" decoding="async" width="600" height="600" />
</a>
<div class="newsroom-card-body">
<span class="newsroom-eyebrow">{eyebrow}</span>
<h3><a href="{href}" title="{title}">{title}</a></h3>
<p class="newsroom-excerpt">{summary}</p>
</div>
</article>"""


def section_block(cat: dict) -> str:
    head = f'<header class="newsroom-section-head"><p class="newsroom-kicker">{cat["kicker"]}</p><h2>{cat["title"]}</h2>' + (f'<p class="newsroom-lede">{cat["lede"]}</p>' if cat.get("lede") else "") + "</header>"
    if cat.get("is_featured"):
        return head + "\n\n" + featured_block(cat["items"][0])
    cards = "\n\n".join(card_block(i) for i in cat["items"])
    return head + '\n\n<div class="newsroom-grid">\n\n' + cards + "\n\n</div>"


THREE_THEMES = [
    {
        "icon": "https://cloudcdn.pro/clients/pain001/v1/logos/pain001.svg",
        "icon_alt": "pain001 logo",
        "title": "Payments and settlement.",
        "body": (
            "ISO 20022 <strong>pain.001</strong> and <strong>pacs.008</strong> "
            "toolkits, bank-statement parsing, and Rust libraries for the "
            "migration to structured cross-border messages. Built for SWIFT, "
            "SEPA, and the real-time payment schemes that come next."
        ),
        "cta_label": "Explore payments tools",
        "cta_href": "#cat-payments",
    },
    {
        "icon": "https://cloudcdn.pro/clients/kyberlib/v1/logos/kyberlib.svg",
        "icon_alt": "KyberLib logo",
        "title": "Post-quantum cryptography.",
        "body": (
            "Rust implementations of <strong>CRYSTALS-Kyber</strong> "
            "(NIST FIPS&nbsp;203), hash and digest primitives, and "
            "quantum-resistant building blocks. Protection beyond the RSA "
            "and elliptic-curve era of financial-grade authentication."
        ),
        "cta_label": "Explore quantum-safe libraries",
        "cta_href": "#cat-quantum",
    },
    {
        "icon": "https://cloudcdn.pro/clients/hsh/v1/logos/hsh.svg",
        "icon_alt": "HSH logo",
        "title": "Tooling and infrastructure.",
        "body": (
            "Open-source Rust libraries for serialisation, logging, code "
            "generation, date and time. Plus the <strong>Static Site "
            "Generator</strong> (SSG) that builds this very site, and the "
            "developer environment that makes it shippable."
        ),
        "cta_label": "Explore developer tools",
        "cta_href": "#cat-rust",
    },
]


FAQ_ITEMS = [
    ("What licence are these projects released under?",
     "Most projects are dual-licensed under MIT and Apache-2.0 — the standard "
     "for the Rust ecosystem — which gives commercial users explicit patent "
     "rights as well as permissive redistribution. A small number of clients' "
     "tools are released under Apache-2.0 only. The licence file at the root "
     "of each repository is the authoritative source."),
    ("Are these projects production-ready?",
     "Many are. <a href=\"https://pain001.com\">pain001</a> is used by banks "
     "and payment-service providers to automate ISO&nbsp;20022 file creation. "
     "<a href=\"https://kyberlib.com\">KyberLib</a> tracks the NIST FIPS&nbsp;203 "
     "specification and ships test vectors. Each repository's README and CI "
     "badges will tell you the current status; if you need a specific guarantee "
     "for production use, get in touch."),
    ("How can I contribute or report an issue?",
     "Every project has a public GitHub repository under "
     "<a href=\"https://github.com/sebastienrousseau\" rel=\"external noopener\">github.com/sebastienrousseau</a>. "
     "Open an issue describing the problem (a minimal reproducer helps) or a "
     "pull request linked to an issue. Contributions are governed by the "
     "Developer Certificate of Origin and require signed commits."),
    ("Can I use these libraries in a regulated banking environment?",
     "Yes, with the usual caveats. The libraries are independent open-source "
     "work, not a regulated product. Run your normal supply-chain, security, "
     "and dependency-review processes — vendoring through your internal mirror, "
     "scanning with SBOM tools, and pinning by Git SHA or cryptographic hash — "
     "before deploying to production payment infrastructure."),
    ("Do you offer commercial support or consulting?",
     "Yes, on a selective basis. Engagements focus on ISO&nbsp;20022 migration, "
     "post-quantum cryptography migration roadmaps, and applied AI in "
     "financial services. <a href=\"/contact/index.html\">Get in touch</a> with "
     "a short brief, your timeline and any constraints."),
    ("How do I follow new releases?",
     "Every dated post on this site is announced through the "
     "<a href=\"/rss.xml\">RSS feed</a> and the "
     "<a href=\"https://news.bankingonquantum.com\" rel=\"external noopener\">Banking On Quantum</a> "
     "newsletter. Individual repositories also publish releases on GitHub, "
     "which you can watch directly."),
]


def setup_hero_block() -> str:
    """Single eyebrow + CTA strip that sits directly below the layout's
    ap-hero (which already carries the page H1 + subtitle via frontmatter).
    Centered, no duplicate headline."""
    return """<p class="setup-hero-eyebrow">OPEN SOURCE FOR FINANCIAL SERVICES</p>
<p class="setup-hero-cta">
<a class="pill" href="#catalog">Browse all projects</a>
<a class="pill ghost" href="/contact/index.html">Get in touch</a>
</p>"""


def setup_three_block() -> str:
    cards = []
    for t in THREE_THEMES:
        cards.append(
            f"""<article class="setup-card">
<span class="setup-card-icon"><img alt="{t['icon_alt']}" src="{t['icon']}" loading="lazy" decoding="async" width="80" height="80" /></span>
<h3 class="setup-card-title">{t['title']}</h3>
<p class="setup-card-body">{t['body']}</p>
<p class="setup-card-cta"><a href="{t['cta_href']}" class="setup-card-link">{t['cta_label']} <span aria-hidden="true">›</span></a></p>
</article>"""
        )
    return (
        '<section class="setup-three" aria-labelledby="setup-three-heading">'
        '<header class="setup-three-head">'
        '<p class="setup-three-kicker">WHAT IS INSIDE</p>'
        '<h2 id="setup-three-heading" class="setup-three-headline">Three areas of practice. <span class="setup-three-headline-soft">One philosophy.</span></h2>'
        '</header>'
        '<div class="setup-three-grid">' + "\n".join(cards) + '</div>'
        '</section>'
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
        '</header>'
        '<section class="qa-list">' + "\n".join(items) + '</section>'
        '</section>'
    )


def bottom_cta_block() -> str:
    return """<aside class="setup-finale" aria-labelledby="projects-finale-heading">
<p class="setup-finale-eyebrow">GET IN TOUCH</p>
<h2 id="projects-finale-heading" class="setup-finale-headline">Have an idea? Let's build it.</h2>
<p class="setup-finale-lede">Open-source collaboration, commissioned engineering, or a conversation about the future of payments. Whichever fits.</p>
<p class="setup-finale-cta"><a class="pill" href="/contact/index.html">Start a conversation</a></p>
</aside>"""


# Map kicker → anchor id used by the three theme cards above to deep-link
# into the relevant slice of the catalogue further down the page.
ANCHOR_MAP = {
    "PAYMENTS": "cat-payments",
    "POST-QUANTUM CRYPTOGRAPHY": "cat-quantum",
    "AI AND VOICE": "cat-ai",
    "OPEN-SOURCE RUST": "cat-rust",
    "WEB AND DEVELOPER ENVIRONMENT": "cat-web",
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
        + '</header>'
    )
    cards = "\n\n".join(card_block(i) for i in cat["items"])
    return head + '\n\n<div class="newsroom-grid cat-grid">\n\n' + cards + "\n\n</div>"


def main() -> None:
    text = SRC.read_text()
    lines = text.splitlines(keepends=True)
    delim_idx = [i for i, ln in enumerate(lines) if ln.strip() == "---"]
    if len(delim_idx) < 2:
        raise SystemExit("could not locate frontmatter delimiters in projects.md")
    head = "".join(lines[: delim_idx[1] + 1])

    body_parts = [
        setup_hero_block(),
        setup_three_block(),
        '<section class="newsroom" id="catalog">',
    ]
    body_parts.extend(section_block_anchored(c) for c in CATEGORIES)
    body_parts.append("</section>")
    body_parts.append(faq_block())
    body_parts.append(bottom_cta_block())
    body = "\n\n".join(body_parts) + "\n"

    SRC.write_text(head + "\n" + body)
    total_items = sum(len(c["items"]) for c in CATEGORIES)
    print(f"wrote {SRC}. hero + 3 themes + {len(CATEGORIES)} catalogue sections, {total_items} items, FAQ + bottom CTA")


if __name__ == "__main__":
    main()
