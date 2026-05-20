#!/usr/bin/env python3
"""Apply SEO metadata rewrites across `_posts/`.

Three classes of edit, all keyed by relative file path:

  * ``TITLES``    — replace ``title:`` frontmatter with a 50–60 character variant
                    that places the primary keyword near the front.
  * ``DESCS``     — replace ``description:`` with a 120–160 character variant that
                    answers the user query directly and ends with a clear CTA or
                    differentiator.
  * ``SUBTITLES`` — drop the boilerplate "Open Source Software (OSS) Developer …"
                    line on the 21 posts that share it, replacing each with a
                    category-specific tagline that strengthens topical authority
                    and keeps per-page metadata distinct.

The script reads each file, rewrites only the affected lines, and writes back.
Idempotent: running twice produces no further changes.
"""
from __future__ import annotations

import sys as _sys  # path bootstrap — scripts reorg (scripts/lib/ on sys.path)
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "lib"))

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
POSTS = REPO / "_posts"
DRAFTS = REPO / "_drafts"

TITLES: dict[str, str] = {
    "_posts/index.md": "Sebastien Rousseau: AI, Payments & Quantum Cryptography",
    "_posts/tags.md": "Topics & Tags Index: AI, Payments, Quantum, Rust OSS",
    "_posts/terms.md": "Website Terms & Conditions of Use — Sebastien Rousseau",
    "_posts/privacy.md": "Privacy Statement — How Your Data Is Collected & Used",
    "_posts/made-with-static-site-generator.md": (
        "Made with Static Site Generator: Rust-Powered SSG"
    ),
    "_posts/2025-09-01-quantum-safe-payments-epaa.md": (
        "Quantum-Safe Payments: Why the Industry Must Act Now"
    ),
    "_posts/2026-04-11-quantum-thresholds-are-moving-again.md": (
        "Quantum Thresholds Are Moving: 10,000-Qubit Shor Risk"
    ),
    "_posts/2026-05-11-lucy-besson-knowledge-transfer-ai-quantum.md": (
        "Lucy's Flash Drive Revisited: AI, Quantum & Knowledge"
    ),
    "_drafts/unlocking-security-with-password-generator-pro-a-fast-simple-and-secure-password-solution.md": (
        "Password Generator Pro: Fast, Secure CLI Tool in Rust"
    ),
    # Round 2 — surfaced after redesign + brand rename audit.
    "_posts/2023-10-09-shokunin-the-fastest-rust-based-static-site-generator.md": (
        "Static Site Generator: Fastest Rust-Based SSG"
    ),
    "_posts/2023-11-12-exploring-generative-ai.md": (
        "Generative AI in 2023: How It Works, Where It Lands"
    ),
    "_posts/2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats.md": (
        "KyberLib: Rust CRYSTALS-Kyber for Post-Quantum"
    ),
    "_posts/2024-01-23-advancements-in-ai-prompt-engineering.md": (
        "AI Prompt Engineering 2024: Techniques That Work"
    ),
    "_posts/2024-02-08-revolutionising-advertising-how-ai-shapes-the-future.md": (
        "Generative AI in Advertising: Amazon Rufus & Meta"
    ),
    "_posts/2024-02-12-akande-voice-assistant-revolutionising-personal-and-executive-assistance.md": (
        "Àkàndé: GPT-Powered Voice Assistant for Executives"
    ),
    "_posts/2024-03-04-le-chat-by-mistral-ai-a-new-era-in-conversational-ai.md": (
        "Le Chat by Mistral AI: Multilingual Conversational AI"
    ),
    "_posts/2024-03-08-rustlogs-advanced-logging-library-for-rust-applications.md": (
        "RustLogs (RLG): Structured Logging Library for Rust"
    ),
    "_posts/2024-04-22-bug-discovered-in-quantum-algorithm-for-lattice-based-crypto.md": (
        "Quantum Lattice Crypto: Bug in Chen's LWE Attack"
    ),
}

DESCS: dict[str, str] = {
    "_posts/index.md": (
        "AI, banking and payments expert. Senior payments leader. Applied AI, "
        "ISO 20022 migration, wholesale payments and post-quantum cryptography."
    ),
    "_posts/2024-04-15-quantum-algorithm-challenges-lattice-based-cryptography.md": (
        "A new polynomial-time quantum algorithm by Yilei Chen targets "
        "lattice-based cryptography. Implications for post-quantum standards "
        "including CRYSTALS-Kyber."
    ),
    "_posts/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001.md": (
        "Automate the creation of ISO 20022 pain.001 payment files from CSV or "
        "SQLite. pain001 is the open-source Python library that streamlines "
        "compliance."
    ),
    "_posts/2023-11-12-exploring-generative-ai.md": (
        "Explore Generative AI in 2023: how it works, where it lands first in "
        "financial services, and the ethical and architectural questions worth "
        "asking."
    ),
    "_posts/2024-02-19-unlocking-gemini-google-ai-revolution-explained.md": (
        "Gemini 1.5 from Google scales context windows past 1M tokens. What "
        "that unlocks for retrieval-augmented finance and the trade-offs worth "
        "knowing."
    ),
    "_posts/2023-12-04-mastering-date-and-time-in-rust-with-the-dtt-library.md": (
        "DateTime (DTT) is a Rust library for parsing, validating, manipulating "
        "and formatting dates and times — high precision, broad functionality."
    ),
    "_posts/2025-09-01-quantum-safe-payments-epaa.md": (
        "Quantum computing threatens payment system cryptography. The EPAA "
        "white paper outlines the structural risk and the urgent case for PQC "
        "migration."
    ),
    "_posts/2026-04-11-quantum-thresholds-are-moving-again.md": (
        "Shor's algorithm may now run on as few as 10,000 qubits. RSA, ECC and "
        "the timeline for post-quantum migration are all moving up. Here's why."
    ),
    "_posts/2026-05-11-lucy-besson-knowledge-transfer-ai-quantum.md": (
        "Twelve years on, Besson's Lucy reads like a thought experiment about "
        "knowledge migrating from flesh to machine — quietly validated by LLMs "
        "and qubits."
    ),
    "_posts/tags.md": (
        "Browse Sebastien Rousseau's site by topic and tag: AI, payments, "
        "ISO 20022, post-quantum cryptography, Rust open source, and more."
    ),
    "_posts/made-with-static-site-generator.md": (
        "Static Site Generator is a Rust-based static site generator built for performance, "
        "accessibility and SEO. Lightning-fast builds with first-class JSON-LD."
    ),
    # Round 2 — descriptions still outside the 120–160 char band.
    "_posts/2024-01-01-ai-trends-2024-insights-and-predictions-for-the-future.md": (
        "AI trends for 2024: generative AI in finance, multimodal models, on-device LLMs and the "
        "shifts that will reshape banking and product engineering."
    ),
    "_posts/2024-02-13-eus-ai-act-shaping-the-future-of-global-ai-regulation.md": (
        "The EU AI Act sets the first comprehensive framework for ethical, risk-tiered AI "
        "regulation worldwide. What changes for banks, vendors and high-risk systems."
    ),
    "_posts/2024-04-01-openvoice-leading-innovation-in-voice-cloning-technology.md": (
        "OpenVoice from MIT, Tsinghua and MyShell delivers production-grade voice cloning with "
        "fine-grained tone, accent and emotion control — and the trade-offs worth knowing."
    ),
    "_posts/2024-04-22-bug-discovered-in-quantum-algorithm-for-lattice-based-crypto.md": (
        "A bug in Yilei Chen's quantum LWE algorithm temporarily reprieves lattice-based "
        "cryptography. What it means for CRYSTALS-Kyber, Dilithium and the PQC roadmap."
    ),
}

# Category-specific subtitle replacements for the 21 posts that share the
# generic "Open Source Software (OSS) Developer, Banking & Financial Service
# Professional" line. Each is mapped to a topic-coherent tagline that reinforces
# the topic cluster and gives Google / AI crawlers an entity-rich line of text
# to attach to the page.
BOILER = "Open Source Software (OSS) Developer, Banking & Financial Service Professional"
SUBTITLES: dict[str, str] = {
    # 2018 — blockchain & cryptocurrency
    "_posts/2018-01-01-bitcoin-the-year-in-review.md":
        "Bitcoin, cryptocurrency, and the technology reshaping financial markets.",
    "_posts/2018-01-02-blockchain-the-technology-that-matters-in-2018.md":
        "Blockchain, distributed ledgers, and the technology that matters in 2018.",
    "_posts/2018-01-09-understanding-the-technology-behind-blockchain.md":
        "A practical walk-through of the cryptography and consensus behind blockchain.",
    "_posts/2018-01-24-the-erc-20-token-standard.md":
        "ERC-20 tokens, Ethereum smart contracts and the standardisation of digital assets.",
    "_posts/2018-02-04-unveiling-a-new-cryptocurrency-and-offering-future-faster-payment-solution.md":
        "A new cryptocurrency and faster-payments solution for the next-generation of finance.",
    "_posts/2018-02-15-the-making-of-the-express-transaction-credits-platform.md":
        "Designing the Express Transaction Credits platform with ERC-223 smart contracts.",
    # 2023 — Rust open-source libraries
    "_posts/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001.md":
        "ISO 20022 payment automation and wholesale-payments engineering with pain001.",
    "_posts/2023-10-09-shokunin-the-fastest-rust-based-static-site-generator.md":
        "Static Site Generator, the fastest Rust-based static site generator for high-impact websites.",
    "_posts/2023-10-16-protecting-data-in-the-quantum-age-the-hash-library-hsh.md":
        "HSH: a quantum-resistant hash library for the post-quantum era of authentication.",
    "_posts/2023-10-26-libmake-a-code-generator-to-reduce-repetitive-tasks-and-build-high-quality-rust-libraries.md":
        "LibMake: a Rust code generator that enforces best practices from day one.",
    "_posts/2023-11-05-mathematical-and-cryptographic-constants-for-rust-security.md":
        "Vetted mathematical and cryptographic constants for memory-safe Rust security.",
    "_posts/2023-11-12-exploring-generative-ai.md":
        "Applied artificial intelligence in banking and financial services.",
    "_posts/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age.md":
        "CRYSTALS-Kyber, the NIST FIPS 203 standard for post-quantum key encapsulation.",
    "_posts/2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats.md":
        "KyberLib, a robust Rust implementation of CRYSTALS-Kyber for the quantum era.",
    "_posts/2023-12-04-mastering-date-and-time-in-rust-with-the-dtt-library.md":
        "DTT, the high-precision Rust library for date and time operations.",
    "_posts/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking.md":
        "Quantum Key Distribution (QKD) for financial-grade security in banking.",
    # Listing pages with the generic boilerplate
    "_posts/articles.md":
        "Articles on AI, post-quantum cryptography, ISO 20022 and the future of payments.",
    "_posts/projects.md":
        "Open-source projects in Python, Rust and JavaScript for the future of finance.",
    "_posts/tags.md":
        "Browse the site by topic: AI, payments, post-quantum cryptography, open source.",
    "_posts/papers.md":
        "Industry white papers and applied research for senior payments and security leaders.",
    "_posts/playlists.md":
        "Curated Spotify playlists for deep work, creativity and the engineering mind.",
}


def patch_line(text: str, key: str, new: str) -> tuple[str, bool]:
    """Replace a `key: "old"` frontmatter line with `key: "new"`. Returns
    ``(new_text, changed)``. Tolerates HTML entities in the existing value."""
    pat = re.compile(rf'^{re.escape(key)}:\s*"[^"]*"\s*$', re.MULTILINE)
    if not pat.search(text):
        return text, False
    replacement = f'{key}: "{new}"'
    new_text, n = pat.subn(replacement, text, count=1)
    return new_text, n > 0 and new_text != text


def apply(path: Path, edits: list[tuple[str, str]]) -> int:
    text = path.read_text(encoding="utf-8")
    original = text
    for key, value in edits:
        text, _ = patch_line(text, key, value)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return 1
    return 0


def main() -> int:
    by_path: dict[str, list[tuple[str, str]]] = {}
    for rel, new in TITLES.items():
        by_path.setdefault(rel, []).append(("title", new))
    for rel, new in DESCS.items():
        by_path.setdefault(rel, []).append(("description", new))
    for rel, new in SUBTITLES.items():
        by_path.setdefault(rel, []).append(("subtitle", new))

    changed = 0
    missing: list[str] = []
    for rel, edits in sorted(by_path.items()):
        path = REPO / rel
        if not path.is_file():
            missing.append(rel)
            continue
        changed += apply(path, edits)

    print(f"updated {changed} file(s)")
    if missing:
        print(f"WARNING: {len(missing)} file(s) not found:")
        for m in missing:
            print(f"  {m}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
