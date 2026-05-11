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
        "kicker": "FEATURED",
        "title": "pain001. ISO 20022 payments, automated",
        "lede": None,
        "is_featured": True,
        "items": [
            P("Open source · Python · Payments",
              "pain001. Automate ISO 20022-compliant payment file creation",
              "https://cloudcdn.pro/clients/pain001/v1/github/github-pain001.svg",
              "Banner for the pain001 open-source payments library",
              "A powerful Python library for ISO 20022-compliant payment file creation from CSV or SQLite sources. pain001 directly supports the global payments industry's migration to ISO 20022. The universal financial messaging standard now mandated across SWIFT, SEPA, and major payment schemes worldwide.",
              "https://pain001.com"),
        ],
    },
    {
        "kicker": "AI",
        "title": "Artificial intelligence",
        "lede": "Open-source AI projects applying machine learning and modern techniques to real-world problems. Voice assistants, audio analysis and more.",
        "items": [
            P("AI · Voice",
              "Àkàndé. Advanced AI Voice Assistant",
              "https://cloudcdn.pro/clients/akande/v1/github/github-akande.svg",
              "Banner for Àkàndé, an advanced AI voice assistant",
              "Àkàndé is an advanced voice assistant using OpenAI's GPT for natural interactions, PDF summaries, and efficient caching. Built for both personal and executive tasks.",
              "https://akande.co/"),
            P("AI · Speech",
              "Audio Analyser",
              "https://cloudcdn.pro/clients/audioanalyser/v1/github/github-audioanalyser.svg",
              "Banner for Audio Analyser",
              "Convert audio to text accurately in real-time using advanced AI speech recognition technology. Designed to unlock actionable insights from audio data to enhance customer and employee experience.",
              "https://audioanalyser.co/"),
        ],
    },
    {
        "kicker": "QUANTUM",
        "title": "Quantum computing & cryptography",
        "lede": "Open-source Rust libraries spanning post-quantum cryptography and quantum-resistant primitives, designed to keep data safe in the quantum era.",
        "items": [
            P("Quantum · Rust",
              "KyberLib. CRYSTALS-Kyber for Rust",
              "https://cloudcdn.pro/clients/kyberlib/v1/github/github-kyberlib.svg",
              "Banner for KyberLib",
              "A robust Rust library for CRYSTALS-Kyber post-quantum cryptography, the algorithm selected by NIST for general-purpose encryption in the post-quantum era.",
              "https://kyberlib.com/"),
            P("Quantum · Rust",
              "Hash (HSH). Secure hash library for Rust",
              "https://cloudcdn.pro/clients/hsh/v1/github/github-hsh.svg",
              "Banner for the Hash (HSH) Rust library",
              "An interface for implementing secure hash and digest algorithms in Rust, designed for password encryption and verification with a quantum-resistant posture.",
              "https://github.com/sebastienrousseau/hsh"),
        ],
    },
    {
        "kicker": "RUST",
        "title": "Rust libraries & tools",
        "lede": "A collection of open-source Rust projects covering serialisation, logging, code generation, and developer tooling. Built on the latest Rust technologies.",
        "items": [
            P("Rust · YAML",
              "noyalib. Pure-Rust YAML 1.2 ecosystem",
              "https://cloudcdn.pro/clients/noyalib/v1/github/github-noyalib.svg",
              "Banner for the noyalib Rust YAML 1.2 ecosystem",
              "Zero unsafe, 100% spec compliance (406 / 406 official suite), streaming-first serde, lossless CST, JSON-Schema validation. Library + CLI (noyafmt, noyavalidate) + LSP + MCP + WASM bindings.",
              "https://github.com/sebastienrousseau/noyalib"),
            P("Rust · Serialisation",
              "Serde YML. Effortless YAML serialisation in Rust",
              "https://cloudcdn.pro/clients/serde_yml/v1/github/github-serde_yml.svg",
              "Banner for Serde YML",
              "A robust Rust library that simplifies serialisation and deserialisation of Rust data structures to and from YAML, built on the widely used Serde framework.",
              "https://serdeyml.com/"),
            P("Rust · SSG",
              "Static Site Generator",
              "https://cloudcdn.pro/clients/shokunin/v1/github/github-shokunin.svg",
              "Banner for the Static Site Generator",
              "A secure-by-default static site generator built in Rust. WCAG 2.1 AA validation, CSP/SRI hardening, local LLM content pipeline, WebAssembly target, interactive islands, streaming compilation for 100K+ pages, 28-locale i18n, and one-command deployment.",
              "https://github.com/sebastienrousseau/static-site-generator"),
            P("Rust · Logging",
              "RustLogs (RLG)",
              "https://cloudcdn.pro/clients/rlg/v1/github/github-rlg.svg",
              "Banner for the RustLogs (RLG) library",
              "A flexible logging library for Rust with structured log formats, asynchronous logging, and extensive customisation options.",
              "https://rustlogs.com/"),
            P("Rust · Security",
              "Password Generator Pro",
              "https://cloudcdn.pro/clients/password-generator-pro/v1/github/github-password-generator-pro.svg",
              "Banner for Password Generator Pro",
              "A fast, simple, and powerful open-source cross-platform utility for generating strong, unique, and random passwords.",
              "https://password-generator.pro"),
            P("Rust · Tooling",
              "LibMake. Rust library scaffold generator",
              "https://cloudcdn.pro/clients/libmake/v1/github/github-libmake.svg",
              "Banner for LibMake",
              "A tool designed to quickly help create high-quality Rust libraries by generating a set of pre-filled and pre-defined templated files.",
              "https://github.com/sebastienrousseau/libmake"),
            P("Rust · Time",
              "DateTime (DTT). Rust date/time library",
              "https://cloudcdn.pro/clients/dtt/v1/github/github-dtt.svg",
              "Banner for the DateTime (DTT) Rust library",
              "A range of functions and data structures for date and time operations: day of the month, hour of the day, ISO 8601 formatting, and much more.",
              "https://github.com/sebastienrousseau/dtt"),
            P("Rust · Math",
              "Random (VRD). Mersenne Twister for Rust",
              "https://cloudcdn.pro/clients/vrd/v1/github/github-vrd.svg",
              "Banner for the Random (VRD) Rust library",
              "A Rust library for generating high-quality random numbers based on the Mersenne Twister algorithm, widely used in simulations and games.",
              "https://vrdlib.com/"),
            P("Rust · Math",
              "Common (CMN). Math & crypto constants",
              "https://cloudcdn.pro/clients/cmn/v1/github/github-cmn.svg",
              "Banner for the Common (CMN) Rust library",
              "A modern, fast, user-friendly library that makes it easy to access a wide range of mathematical and cryptographic constants.",
              "https://github.com/sebastienrousseau/cmn"),
            P("Rust · Utility",
              "Mini Functions. Rust utility wrappers",
              "https://cloudcdn.pro/clients/mini-functions/v1/github/github-mini-functions.svg",
              "Banner for the Mini Functions Rust library",
              "A highly performant utility and wrapper functions library for Rust, designed with optimisation and efficiency in mind.",
              "http://minifunctions.com/"),
        ],
    },
    {
        "kicker": "PAYMENTS",
        "title": "Payments toolkits",
        "lede": "ISO 20022 tooling for the global payments migration. Pacs.008 cross-border credit transfers and Pain.001 message generation, plus bank-statement parsing.",
        "items": [
            P("Python · ISO 20022",
              "pacs008. Cross-border credit transfer toolkit",
              "https://pacs008.com/logo.webp",
              "Banner for the pacs008 ISO 20022 toolkit",
              "Generate, validate, and deliver ISO 20022 pacs.008 payment messages for FI-to-FI customer credit transfers. JSON Schema checks, IBAN verification across 75 countries, XSD validation against official ISO 20022 schemas, and GDPR/PCI DSS-compliant PII masking.",
              "https://pacs008.com/"),
            P("Python · Finance",
              "Bank Statement Parser",
              "https://cloudcdn.pro/clients/bankstatementparser/v1/github/github-bankstatementparser.svg",
              "Banner for Bank Statement Parser",
              "A specialised Python library crafted for finance professionals, simplifying the intricate process of parsing bank statements into structured data.",
              "https://bankstatementparser.com/"),
        ],
    },
    {
        "kicker": "JAVASCRIPT",
        "title": "JavaScript projects",
        "lede": "Centralised cryptographic services bringing together encryption, tokenisation, transaction authorisation, code signing, and key lifecycle management.",
        "items": [
            P("JavaScript · Security",
              "Crypto Service Suite",
              "https://cloudcdn.pro/stocks/images/steven-wei-Z7NMhw8hcfg.webp",
              "Banner for the Crypto Service Suite",
              "A powerful, centralised cryptographic suite that solves common application crypto problems. Integration, data encryption, tokenisation, transaction authorisation, code-signing, and key lifecycle management.",
              "https://github.com/sebastienrousseau/crypto-service"),
        ],
    },
    {
        "kicker": "CSS",
        "title": "CSS framework",
        "lede": None,
        "items": [
            P("CSS · Stylus",
              "Skeletonic Stylus Library",
              "https://cloudcdn.pro/clients/skeletonic/v1/logos/logo-skeletonic-stylus.svg",
              "Banner for the Skeletonic Stylus Library",
              "A lightweight, modular Stylus library. A suite of components and mixins optimised for mobile and web application design and development. This site is built with it.",
              "https://github.com/sebastienrousseau/skeletonic-stylus"),
        ],
    },
    {
        "kicker": "WEB",
        "title": "Web-based projects",
        "lede": "Starter templates and content destinations. From a Static Site Generator starter kit to two industry-focused publications on the future of banking.",
        "items": [
            P("Web · Template",
              "Kaishi. A Static Site Generator starter template",
              "https://cloudcdn.pro/clients/kaishi/v1/titles/title-kaishi.svg",
              "Banner for Kaishi, a starter template",
              "Make beautiful websites with Kaishi, a Static Site Generator starter template designed for clean, accessible, performant sites.",
              "https://github.com/sebastienrousseau/kaishi.github.io"),
            P("Web · Finance",
              "L90S. Fractional CFO advisory",
              "https://cloudcdn.pro/clients/l90s/v1/github/github-l90s.svg",
              "Banner for the L90S website",
              "A trusted finance leader with 20+ years of experience in the tech industry, guiding companies to sustainable growth, funding, and optimised financial operations.",
              "https://l90s.com/"),
            P("Web · Publication",
              "Banking On AI",
              "https://cloudcdn.pro/clients/bankingonai/v1/github/github-bankingonai.svg",
              "Banner for the Banking On AI publication",
              "How AI is transforming the banking sector. Improved customer service, fraud detection, and streamlined operations for a digital age.",
              "https://bankingonai.co/"),
            P("Web · Publication",
              "Banking On Quantum",
              "https://cloudcdn.pro/clients/bankingonquantum/v1/github/github-bankingonquantum.svg",
              "Banner for the Banking On Quantum publication",
              "How quantum computing is set to revolutionise the banking and finance industry. From risk analysis to quantum cryptography and beyond.",
              "https://bankingonquantum.com/"),
        ],
    },
    {
        "kicker": "GENERAL",
        "title": "Developer environment",
        "lede": None,
        "items": [
            P("Config · Cross-platform",
              "Dotfiles",
              "https://cloudcdn.pro/clients/dotfiles/v2/images/banners/dotfiles.webp",
              "Banner for the Dotfiles project",
              "A powerful set of configuration files for macOS, Linux, and Windows. Scripts and customised settings to streamline your workflow.",
              "https://dotfiles.io/"),
            P("Config · macOS",
              "MacConfig. MacBook Pro M1 dev setup",
              "https://cloudcdn.pro/stocks/images/ibrahim-abazid-MgQnQZA4ByM.webp",
              "Banner for MacConfig (maccfg)",
              "A guide to getting your MacBook Pro M1 ready for software development. Set up and start using your new Mac with free resources and user guides.",
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


def main() -> None:
    text = SRC.read_text()
    # Frontmatter is bounded by lines containing exactly "---". Keep everything up to
    # the *second* such line, drop the body and rewrite.
    lines = text.splitlines(keepends=True)
    delim_idx = [i for i, ln in enumerate(lines) if ln.strip() == "---"]
    if len(delim_idx) < 2:
        raise SystemExit("could not locate frontmatter delimiters in projects.md")
    head = "".join(lines[: delim_idx[1] + 1])

    intro_para = ("My passion lies in harnessing open-source software and experimentation to push "
                  "boundaries and tackle real-world challenges. I'm eager to team up with like-minded "
                  "individuals on open-source initiatives. If you have a project concept or want to "
                  "collaborate, [get in touch](/contact/index.html).")

    body_parts = [f'<p class="newsroom-intro">{intro_para}</p>', '<section class="newsroom">']
    body_parts.extend(section_block(c) for c in CATEGORIES)
    body_parts.append("</section>")
    body = "\n\n".join(body_parts) + "\n"

    SRC.write_text(head + "\n" + body)
    total_items = sum(len(c["items"]) for c in CATEGORIES)
    print(f"wrote {SRC}. {len(CATEGORIES)} sections, {total_items} items")


if __name__ == "__main__":
    main()
