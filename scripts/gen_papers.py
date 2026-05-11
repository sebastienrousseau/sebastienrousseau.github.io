#!/usr/bin/env python3
"""Rewrite _posts/papers.md body into Apple-Newsroom-style markup.

The latest industry white paper (EPAA Quantum-Safe Payments) is shown as the
featured hero with full abstract and Read CTA. The previous Whisper/MPS paper
is preserved as a second publication card at the top of the related grid.
Beneath those, a curated set of research-flavoured articles keeps the page
feeling like a publications archive rather than a single product page.
"""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_posts" / "papers.md"

EPAA_PDF = (
    "https://emergingpaymentsasia.org/wp-content/uploads/2025/09/"
    "Quantum-Safe-Payments-Why-the-Payments-Industry-Must-Act-Now.pdf"
)

FEATURED = {
    "eyebrow": "INDUSTRY WHITE PAPER · EPAA",
    "title": (
        "Quantum-Safe Payments: Why the Payments Industry Must Act Now"
    ),
    "date_iso": "2025-09-01",
    "date_display": "September 2025",
    "image": "https://cloudcdn.pro/clients/common/images/elements/publication.webp",
    "image_alt": (
        "Cover of the EPAA Quantum-Safe Payments white paper"
    ),
    "format": "English · PDF · 18.9 MB · Free download",
    "publisher": "Emerging Payments Association Asia (EPAA)",
    "publisher_url": "https://emergingpaymentsasia.org/",
    "abstract": (
        "Quantum computing threatens the cryptographic foundations of "
        "financial services. Payments, from real-time to cross-border "
        "settlement, rely on protections that quantum computing will "
        "eventually render obsolete, and regulators are already treating "
        "harvest-now-decrypt-later as a credible present risk. This paper, "
        "produced for the Emerging Payments Association Asia, outlines the "
        "structural threat post-quantum cryptography poses to payment "
        "infrastructure across SWIFT, real-time gross settlement (RTGS) "
        "rails and instant payment schemes, and argues for coordinated "
        "industry action — starting with cryptographic-asset inventories, "
        "PQC migration roadmaps aligned to the NIST FIPS 203/204/205 "
        "standards, and crypto-agility built into wholesale payment "
        "authentication."
    ),
    "buy_url": EPAA_PDF,
    "buy_label": "Read the white paper",
    "read_url": EPAA_PDF,
}

PREVIOUS_PUBLICATION = {
    "date_iso": "2024-03-12",
    "date_display": "March 12, 2024",
    "eyebrow": "PUBLICATION · WHITE PAPER",
    "title": (
        "Accelerating Real-Time Speech Recognition with OpenAI Whisper and "
        "Metal Performance Shaders on macOS"
    ),
    "image": "https://cloudcdn.pro/clients/common/images/elements/publication.webp",
    "image_alt": (
        "Cover of the white paper on real-time speech recognition with "
        "OpenAI Whisper and Metal Performance Shaders on macOS"
    ),
    "excerpt": (
        "A system for real-time speech-to-text transcription that leverages "
        "OpenAI Whisper and Metal Performance Shaders GPU acceleration on "
        "macOS to achieve sub-second latency at 8-12x real-time on M1 Max."
    ),
    "href": "/2024-03-12-revolutionising-real-time-speech-recognition-on-macos-with-openai-whisper/index.html",
    "buy_url": "https://www.paypal.com/ncp/payment/5T6L9WBXHNZUU",
    "price": "$49.00",
    "format": "English · PDF · 95 KB",
}

# Curated research-flavoured articles to surround the publication.
# (date_iso, date_display, eyebrow, title, image, image_alt, excerpt, href)
RELATED = [
    ("2026-04-11", "April 11, 2026", "RESEARCH NOTE · QUANTUM",
     "Quantum Thresholds Are Moving Again",
     "https://cloudcdn.pro/stocks/images/leo_visions-Q_y8ZzhQ2_s-unsplash.webp",
     "Quantum computing circuit board with blue light patterns",
     "A new paper suggests Shor's algorithm could run on as few as 10,000 qubits. The threshold for cryptographically relevant quantum computing is dropping fast.",
     "/2026-04-11-quantum-thresholds-are-moving-again/index.html"),
    ("2024-04-22", "April 22, 2024", "RESEARCH NOTE · QUANTUM",
     "Bug Discovered in Quantum Algorithm for Lattice-Based Crypto",
     "https://cloudcdn.pro/stocks/images/digital-nodes.webp",
     "Network of digital nodes in red and blue hues",
     "A bug in Yilei Chen's quantum algorithm for solving LWE has been found, temporarily securing lattice-based cryptography and highlighting the need for ongoing research.",
     "/2024-04-22-bug-discovered-in-quantum-algorithm-for-lattice-based-crypto/index.html"),
    ("2024-04-15", "April 15, 2024", "RESEARCH NOTE · QUANTUM",
     "Quantum Algorithm Challenges Lattice-Based Cryptography",
     "https://cloudcdn.pro/stocks/images/digital-constellation.webp",
     "Network nodes in a digital blue space",
     "New quantum algorithm solves a key cryptographic problem, urging accelerated research into quantum-safe security.",
     "/2024-04-15-quantum-algorithm-challenges-lattice-based-cryptography/index.html"),
    ("2024-03-25", "March 25, 2024", "RESEARCH · CRYPTOGRAPHY",
     "Fully Homomorphic Encryption (FHE) in a Banking Quantum Era",
     "https://cloudcdn.pro/stocks/images/fully-homomorphic-encryption.webp",
     "Banner for Fully Homomorphic Encryption",
     "How Fully Homomorphic Encryption revolutionises data security in banking and financial services, preserving privacy against quantum-era threats.",
     "/2024-03-25-fully-homomorphic-encryption-in-a-banking-quantum-era/index.html"),
    ("2024-03-18", "March 18, 2024", "RESEARCH · AI",
     "Advancing AI with Multimodal LLMs: Insights from MM1",
     "https://cloudcdn.pro/stocks/images/mm1-visual.webp",
     "Banner for Apple's MM1 multimodal LLM research",
     "An analysis of Apple's MM1 paper on Multimodal Large Language Models — architecture, pre-training strategies and emerging capabilities.",
     "/2024-03-18-advancing-ai-with-multimodal-llms-insights-from-mm1/index.html"),
    ("2024-01-08", "January 8, 2024", "RESEARCH · QUANTUM FINANCE",
     "Qiskit and Quantum Fourier Transform for Credit Ratio Analysis",
     "https://cloudcdn.pro/stocks/images/quantum-computer-room.webp",
     "A quantum computer room",
     "How IBM Qiskit and the Quantum Fourier Transform reshape credit ratio analysis in finance, offering unprecedented accuracy and speed.",
     "/2024-01-08-optimising-credit-ratio-analysis-with-ibm-qiskit-and-quantum-fourier-transform/index.html"),
    ("2023-12-25", "December 25, 2023", "RESEARCH · QUANTUM FINANCE",
     "Revolutionising Finance with AI-Enhanced Quantum Algorithms",
     "https://cloudcdn.pro/stocks/images/circuit_board_cityscape.webp",
     "A circuit board cityscape",
     "The transformative role of AI inside quantum algorithms for finance, focusing on their mathematical structure and banking applications.",
     "/2023-12-25-revolutionising-finance-with-ai-enhanced-quantum-algorithms/index.html"),
    ("2023-12-11", "December 11, 2023", "RESEARCH · QUANTUM BANKING",
     "Quantum Key Distribution: Revolutionising Security in Banking",
     "https://cloudcdn.pro/stocks/images/hsbc-from-the-docks.webp",
     "HSBC headquarter in London Canary Wharf docks",
     "As quantum computers threaten traditional encryption, Quantum Key Distribution (QKD) emerges as a structural answer for financial-grade security.",
     "/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html"),
    ("2023-11-19", "November 19, 2023", "RESEARCH · CRYPTOGRAPHY",
     "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age",
     "https://cloudcdn.pro/stocks/images/galina-nelyubova-V70-ng4FuiA.webp",
     "A complex quantum computer architecture",
     "How CRYSTALS-Kyber, the NIST-selected quantum-resistant key-encapsulation mechanism, is reshaping cryptography for the quantum era.",
     "/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html"),
]


def epaa_card_block() -> str:
    f = FEATURED
    return f"""<article class="book">
<a class="book-cover" href="{f['buy_url']}" title="{f['buy_label']} (PDF)" rel="external noopener">
<img alt="{f['image_alt']}" src="{f['image']}" loading="eager" fetchpriority="high" decoding="async" width="320" height="480" />
</a>
<div class="book-body">
<p class="book-eyebrow">{f['eyebrow']}</p>
<h2 class="book-title"><a href="{f['read_url']}" rel="external noopener" title="{f['title']}">{f['title']}</a></h2>
<p class="book-meta"><time datetime="{f['date_iso']}">{f['date_display']}</time> &middot; <a href="{f['publisher_url']}" rel="external noopener">{f['publisher']}</a></p>
<p class="book-meta book-meta-faint">{f['format']}</p>
<p class="book-excerpt">{f['abstract']}</p>
<p class="book-actions"><a class="pill primary no-chev" href="{f['buy_url']}" rel="external noopener" title="{f['buy_label']} (PDF)">{f['buy_label']}</a> <a class="pill ghost no-chev" href="{f['publisher_url']}" rel="external noopener" title="Visit the Emerging Payments Association Asia">About EPAA</a></p>
</div>
</article>"""


def whisper_card_block() -> str:
    p = PREVIOUS_PUBLICATION
    return f"""<article class="book">
<a class="book-cover" href="{p['buy_url']}" title="Buy {p['title']} on PayPal" rel="external noopener">
<img alt="{p['image_alt']}" src="{p['image']}" loading="lazy" decoding="async" width="320" height="480" />
</a>
<div class="book-body">
<p class="book-eyebrow">{p['eyebrow']}</p>
<h2 class="book-title"><a href="{p['href']}" title="{p['title']}">{p['title']}</a></h2>
<p class="book-meta"><time datetime="{p['date_iso']}">{p['date_display']}</time> &middot; Sebastien Rousseau</p>
<p class="book-meta book-meta-faint">{p['format']}</p>
<p class="book-excerpt">{p['excerpt']}</p>
<p class="book-actions"><a class="pill primary no-chev" href="{p['buy_url']}" rel="external noopener" title="Buy the publication on PayPal">Buy &middot; {p['price']}</a> <a class="pill ghost no-chev" href="{p['href']}" title="Read the companion article">Read the article</a></p>
</div>
</article>"""


def card_block(date_iso: str, date_display: str, eyebrow: str, title: str,
               image: str, alt: str, excerpt: str, href: str) -> str:
    return f"""<article class="newsroom-card">
<a class="newsroom-card-media" href="{href}" title="{title}">
<img alt="{alt}" src="{image}" loading="lazy" decoding="async" width="600" height="600" />
</a>
<div class="newsroom-card-body">
<span class="newsroom-eyebrow">{eyebrow}</span>
<h3><a href="{href}" title="{title}">{title}</a></h3>
<p class="newsroom-meta"><time datetime="{date_iso}">{date_display}</time> &middot; Sebastien Rousseau</p>
<p class="newsroom-excerpt">{excerpt}</p>
</div>
</article>"""


def main() -> None:
    text = SRC.read_text()
    lines = text.splitlines(keepends=True)
    delim_idx = [i for i, ln in enumerate(lines) if ln.strip() == "---"]
    if len(delim_idx) < 2:
        raise SystemExit("could not locate frontmatter delimiters in papers.md")
    head = "".join(lines[: delim_idx[1] + 1]) + "\n"

    related_cards = "\n\n".join(card_block(*a) for a in RELATED)

    body = f"""<section class="newsroom papers">

<div class="books-shelf">

{epaa_card_block()}

{whisper_card_block()}

</div>

<header class="newsroom-section-head"><p class="newsroom-kicker">RESEARCH NOTES</p><h2>Recent research and analysis</h2></header>

<div class="newsroom-grid newsroom-grid-tight">

{related_cards}

</div>

<section class="qa" aria-labelledby="qa-heading">
<header class="qa-head">
<h2 id="qa-heading" class="qa-headline">Questions? <span class="qa-headline-soft">Answers.</span></h2>
</header>
<section class="qa-list">
<details class="qa-item">
<summary class="qa-q">What kind of research and papers do you publish?</summary>
<section class="qa-a"><p>Two strands sit side-by-side. <strong>Industry white papers</strong>, produced for organisations such as the <a href="https://emergingpaymentsasia.org/" rel="external noopener">Emerging Payments Association Asia</a> (EPAA), examine structural shifts to payment infrastructure — most recently the impact of cryptographically-relevant quantum computing on wholesale and real-time settlement rails. <strong>Applied research papers</strong>, published independently, share reproducible engineering work — for example, real-time speech recognition on macOS using OpenAI Whisper and Metal Performance Shaders.</p></section>
</details>
<details class="qa-item">
<summary class="qa-q">Who is the intended audience?</summary>
<section class="qa-a"><p>Heads of payments, CISOs and senior architects in Tier-1 banks, central banks, payment system operators and scheme owners. The applied research is written for engineers and product leaders building on top of large language models, on-device AI, and quantum-resistant cryptography. Each paper assumes domain literacy and skips background that a working professional would already have.</p></section>
</details>
<details class="qa-item">
<summary class="qa-q">Are the white papers free to read?</summary>
<section class="qa-a"><p>The EPAA <em>Quantum-Safe Payments</em> paper is a free public download from <a href="{EPAA_PDF}" rel="external noopener">emergingpaymentsasia.org</a>. The independent research paper on real-time speech recognition with OpenAI Whisper and Metal Performance Shaders is licensed and available for individual purchase at $49.00 (English, PDF, ~95 KB). One copy per buyer; downloads are personal-use only and may not be redistributed.</p></section>
</details>
<details class="qa-item">
<summary class="qa-q">May I cite or quote from these papers?</summary>
<section class="qa-a"><p>Yes. Short quotations with attribution are welcome under fair-dealing/fair-use norms. For EPAA papers, cite the EPAA as publisher with the working group, year and PDF URL. For the independent research papers, cite as <em>Rousseau, S. (year). Title. Self-published.</em> with the canonical URL. If you'd like to reproduce a figure or extended passage, please <a href="/contact/index.html">get in touch</a> first.</p></section>
</details>
<details class="qa-item">
<summary class="qa-q">Can I commission a paper or speak at an event?</summary>
<section class="qa-a"><p>Yes — limited, by selection. Commissioned work focuses on wholesale payments, ISO 20022 migration, post-quantum cryptography for financial services, and applied AI in banking. Speaking engagements at industry conferences, central-bank fora, and regulator round-tables are considered case-by-case. Use the <a href="/contact/index.html">contact form</a> with the brief, the audience and the timeline.</p></section>
</details>
<details class="qa-item">
<summary class="qa-q">How do I follow new publications?</summary>
<section class="qa-a"><p>New papers and research notes are announced first through the site's <a href="/rss.xml">RSS feed</a> and the <a href="https://news.bankingonquantum.com" rel="external noopener">Banking On Quantum</a> newsletter, which covers post-quantum cryptography, central-bank policy, and the migration roadmap across major payment schemes. There is no spam — only new work.</p></section>
</details>
</section>
</section>

</section>
"""

    SRC.write_text(head + body)
    print(f"wrote {SRC}. Publications: 2 (paired), related cards: {len(RELATED)}")


if __name__ == "__main__":
    main()
