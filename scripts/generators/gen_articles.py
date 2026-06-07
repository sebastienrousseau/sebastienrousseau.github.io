#!/usr/bin/env python3
"""Rewrite the body of _posts/articles.md into Apple-Newsroom-style markup.

Featured (most recent) story sits in a 1:1 split-card; the rest fill a 3-col grid.
Image, title, eyebrow tag, date and excerpt come from the existing markdown.

Auto-discovery: any dated `_posts/YYYY-MM-DD-*.md` newer than ARTICLES[0]'s
date is automatically prepended at run-time. The static ARTICLES list below
is the long-tail; only the *latest* article needs to be auto-injected so
the daily routine doesn't need to edit this file. Auto-injection reads
frontmatter (title, banner, banner_alt, excerpt, tags) and derives the
eyebrow from the first three comma-separated tags.
"""

from __future__ import annotations

import sys as _sys  # path bootstrap — scripts reorg (scripts/lib/ on sys.path)
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "lib"))

import re

from _core import ROOT, display_date, parse_frontmatter

SRC = ROOT / "_posts" / "articles.md"
POSTS = ROOT / "_posts"

_DATED_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-")

# (date_iso, date_display, eyebrow, title, image_url, image_alt, excerpt, href)
ARTICLES = [
    (
        "2026-05-20",
        "May 20, 2026",
        "Cloud Native · DORA · Banking",
        "Cloud Native Banking in 2026: Kubernetes, DORA, Sovereignty, and the End of the VM vs Container Divide",
        "https://cloudcdn.pro/stocks/images/freeman-zhou-oV9hp8wXkPE.webp",
        "Cloud-native banking architecture for 2026 showing Kubernetes, VM coexistence, DORA resilience, sovereign cloud, observability, and bank platform engineering",
        "Cloud native banking in 2026 is a regulated platform-engineering discipline: Kubernetes plus VM coexistence, DORA-tested resilience, sovereign cloud, data portability, and proof that critical services can survive provider disruption. Architecture is now a supervisory artefact.",
        "/2026-05-20-cloud-native-banking-financial-institutions-2026/index.html",
    ),
    (
        "2026-05-19",
        "May 19, 2026",
        "Payments · ISO 20022 · Cross-Border",
        "Global Wholesale Payments in 2026: ISO 20022, RTGS Renewal, and the Economics of Interoperability",
        "https://cloudcdn.pro/stocks/images/meiying-ng-OrwkD-iWgqg.webp",
        "Global wholesale payments architecture map for 2026 showing ISO 20022, RTGS renewal, cross-border corridors, liquidity windows, and DLT settlement pilots",
        "Wholesale payments in 2026 are part of macroeconomic resilience: ISO 20022 harmonisation, RTGS renewal and extended operating hours, non-bank access, interlinking, and DLT settlement pilots are converging around the cost of moving global liquidity — and the G20 cross-border targets are still off-track for 2027.",
        "/2026-05-19-global-wholesale-payments-economics-2026/index.html",
    ),
    (
        "2026-05-15",
        "May 15, 2026",
        "Payments · Stablecoins · Regulation",
        "Stablecoin Yield by Another Name: BlackRock's BRSRV and BSTBL Filings Decoded",
        "https://cloudcdn.pro/stocks/images/alev-takil-7ojyp-IXW7w-unsplash.webp",
        "Stacked US dollar coins under warm light, representing tokenised money-market fund yield",
        "Stablecoins cannot pay yield under the GENIUS Act. BlackRock's BRSRV and BSTBL filings show the workaround — a tokenised money-market fund running alongside a regulated stablecoin to deliver yield through an adjacent, compliant rail.",
        "/2026-05-15-blackrock-brsrv-bstbl-genius-act-tokenised-mmf/index.html",
    ),
    (
        "2026-05-14",
        "May 14, 2026",
        "Post-Quantum · Treasury · Governance",
        "Securing the Ledger: A Board-Level Guide to Post-Quantum Migration for Corporate Finance",
        "https://cloudcdn.pro/stocks/images/getty-images-LaU3HadwEeE-unsplash.webp",
        "Open vault door framed by gold light — visual metaphor for cryptographic protection of financial records",
        "Quantum risk has moved from research curiosity to active regulatory mandate. With the G7 roadmap published in January 2026 and BIS Project Leap proving feasibility in live payment systems, the board-level question is no longer whether to migrate.",
        "/2026-05-14-securing-the-ledger-post-quantum-migration-corporate-finance/index.html",
    ),
    (
        "2026-05-12",
        "May 12, 2026",
        "ISO 20022 · Payments · CBPR+",
        "The November 2026 pacs.008 Structured-Address Deadline: A Six-Month View",
        "https://cloudcdn.pro/stocks/images/markus-winkler-IrRbSND5EUc-unsplash.webp",
        "Cross-border payment message structured-address diagram with TwnNm and Ctry highlighted",
        "From November 2026, SWIFT CBPR+ rejects unstructured postal addresses in cross-border payment messages. Six months out, 65% of pacs.008 messages still ship non-compliant addresses and 44% of banks remain behind on the remediation programme.",
        "/2026-05-12-iso-20022-pacs008-structured-address-deadline/index.html",
    ),
    (
        "2026-05-11",
        "May 11, 2026",
        "AI · Quantum · Philosophy",
        "Lucy's Flash Drive, Revisited: What Besson Saw About Knowledge Migrating to Machines",
        "https://cloudcdn.pro/stocks/images/lucy-knowledge-transfer-banner.webp",
        "Abstract visualisation of neural networks and quantum atomic arrays. A black computer forming from rearranging particles",
        "Twelve years after its release, Luc Besson's Lucy reads less like pseudo-science and more like a thought experiment about what happens when human knowledge migrates from biological to non-biological substrates.",
        "/2026-05-11-lucy-besson-knowledge-transfer-ai-quantum/index.html",
    ),
    (
        "2026-04-11",
        "April 11, 2026",
        "Quantum",
        "Quantum Thresholds Are Moving Again",
        "https://cloudcdn.pro/stocks/images/leo_visions-Q_y8ZzhQ2_s-unsplash.webp",
        "Quantum computing circuit board with blue light patterns",
        "A new paper suggests Shor's algorithm could run on as few as 10,000 qubits. The threshold for cryptographically relevant quantum computing is dropping fast.",
        "/2026-04-11-quantum-thresholds-are-moving-again/index.html",
    ),
    (
        "2024-04-22",
        "April 22, 2024",
        "Quantum",
        "Bug Discovered in Quantum Algorithm for Lattice-Based Crypto",
        "https://cloudcdn.pro/stocks/images/digital-nodes.webp",
        "Image generated using MidJourney. A network of digital nodes in red and blue hues",
        "A bug in Yilei Chen's quantum algorithm for solving LWE has been found, temporarily securing lattice-based cryptography and highlighting the need for ongoing research.",
        "/2024-04-22-bug-discovered-in-quantum-algorithm-for-lattice-based-crypto/index.html",
    ),
    (
        "2024-04-15",
        "April 15, 2024",
        "Quantum",
        "Quantum Algorithm Challenges Lattice-Based Cryptography",
        "https://cloudcdn.pro/stocks/images/digital-constellation.webp",
        "Banner Image of Network nodes in a digital blue space",
        "New quantum algorithm solves key crypto problem, urges research into quantum-safe security.",
        "/2024-04-15-quantum-algorithm-challenges-lattice-based-cryptography/index.html",
    ),
    (
        "2024-04-01",
        "April 1, 2024",
        "AI",
        "OpenVoice: Leading Innovation in Voice Cloning Technology",
        "https://cloudcdn.pro/stocks/images/open-voice.webp",
        "Banner of vibrant gradient overlay on repeated profiles",
        "Explore OpenVoice's groundbreaking voice cloning tech, offering unmatched speed, accuracy, and control in synthetic speech generation.",
        "/2024-04-01-openvoice-leading-innovation-in-voice-cloning-technology/index.html",
    ),
    (
        "2024-03-25",
        "March 25, 2024",
        "Quantum",
        "Fully Homomorphic Encryption (FHE) in a Banking Quantum Era",
        "https://cloudcdn.pro/stocks/images/fully-homomorphic-encryption.webp",
        "Banner for Fully Homomorphic Encryption",
        "Explore how Fully Homomorphic Encryption revolutionises data security in Banking and the Financial Industry, ensuring privacy against quantum computing threats.",
        "/2024-03-25-fully-homomorphic-encryption-in-a-banking-quantum-era/index.html",
    ),
    (
        "2024-03-18",
        "March 18, 2024",
        "AI",
        "Advancing AI with Multimodal LLMs: Insights from MM1",
        "https://cloudcdn.pro/stocks/images/mm1-visual.webp",
        "Banner for the Apple MM1 multimodal LLM research",
        "Explore Apple's MM1 paper on Multimodal Large Language Models. Learn about their architecture, pre-training strategies, and AI potentials.",
        "/2024-03-18-advancing-ai-with-multimodal-llms-insights-from-mm1/index.html",
    ),
    (
        "2024-03-12",
        "March 12, 2024",
        "AI · macOS",
        "Accelerating Real-Time Speech Recognition on macOS with OpenAI Whisper",
        "https://cloudcdn.pro/stocks/images/research-paper.webp",
        "Banner for Real-time automatic speech recognition research",
        "Explore how OpenAI Whisper and Metal Performance Shaders are transforming real-time speech recognition on macOS, offering unparalleled speed and accuracy.",
        "/2024-03-12-revolutionising-real-time-speech-recognition-on-macos-with-openai-whisper/index.html",
    ),
    (
        "2024-03-08",
        "March 8, 2024",
        "Open source · Rust",
        "Unleashing the Power of Logging in Rust with RustLogs (RLG)",
        "https://cloudcdn.pro/stocks/images/rustlogs.webp",
        "Banner for RustLogs (RLG) library",
        "Discover RustLogs (RLG), the flexible logging library for Rust with structured log formats, asynchronous logging, and extensive customisation options.",
        "/2024-03-08-rustlogs-advanced-logging-library-for-rust-applications/index.html",
    ),
    (
        "2024-03-04",
        "March 4, 2024",
        "AI",
        "Le Chat by Mistral AI: A New Era in Conversational AI",
        "https://cloudcdn.pro/stocks/images/abstract-digital-art-of-a-cat.webp",
        "Colourful, abstract digital art of a cat",
        "Meet Mistral AI's new multilingual Assistant. An advanced AI that can understand and respond in multiple languages, all in one conversation and in real time.",
        "/2024-03-04-le-chat-by-mistral-ai-a-new-era-in-conversational-ai/index.html",
    ),
    (
        "2024-02-26",
        "February 26, 2024",
        "AI",
        "Google Gemma AI: Transforming Open-Source AI Development",
        "https://cloudcdn.pro/stocks/images/ai-ship.webp",
        "Futuristic blue spaceship with neon lights",
        "Explore Google's Gemma AI Model: An open-source project offering ethical AI solutions for both personal and enterprise use.",
        "/2024-02-26-google-gemma-ai-transforming-open-source-ai-development/index.html",
    ),
    (
        "2024-02-19",
        "February 19, 2024",
        "AI",
        "Unlocking Gemini 1.5: Google's AI Revolution Explained",
        "https://cloudcdn.pro/stocks/images/abstract-visualization-of-gemini.webp",
        "Abstract visualisation of AI networks, representing Gemini 1.5",
        "Explore Gemini 1.5, Google's AI breakthrough, enhancing efficiency, quality, and context understanding in the AI landscape.",
        "/2024-02-19-unlocking-gemini-google-ai-revolution-explained/index.html",
    ),
    (
        "2024-02-13",
        "February 13, 2024",
        "Policy",
        "EU's AI Act: Pioneering Ethical AI Regulation Worldwide",
        "https://cloudcdn.pro/stocks/images/ryoji-iwata-a-qsFZimp1M.webp",
        "A person sitting on a black bench reading a newspaper",
        "Delve into the EU's Artificial Intelligence Act, a revolutionary framework setting global standards for ethical AI development and usage.",
        "/2024-02-13-eus-ai-act-shaping-the-future-of-global-ai-regulation/index.html",
    ),
    (
        "2024-02-12",
        "February 12, 2024",
        "AI",
        "Àkàndé Voice Assistant, A Personal and Executive Assistance",
        "https://cloudcdn.pro/stocks/images/akande-voice-assistant.webp",
        "A white, spherical modern AI device",
        "Discover how Àkàndé leverages OpenAI GPT's natural language understanding, PDF summaries, and efficient caching to redefine personal and executive assistance.",
        "/2024-02-12-akande-voice-assistant-revolutionising-personal-and-executive-assistance/index.html",
    ),
    (
        "2024-02-08",
        "February 8, 2024",
        "AI · Advertising",
        "Revolutionising Advertising: How AI Shapes the Future",
        "https://cloudcdn.pro/stocks/images/advertising-ai.webp",
        "A robotic woman with butterflies and flowers",
        "Explore how AI transforms advertising with insights on Amazon's Rufus and Meta's latest developments. Discover the impact on consumer engagement.",
        "/2024-02-08-revolutionising-advertising-how-ai-shapes-the-future/index.html",
    ),
    (
        "2024-01-29",
        "January 29, 2024",
        "AI",
        "AI-Powered Speech Analysis, Translation & Insight Tool",
        "https://cloudcdn.pro/stocks/images/modern-corporate-office-with-technological-displays.webp",
        "A minimalist, modern corporate office with technological displays",
        "Explore how Audio Analyser transforms speech-to-text conversion, text analysis, and translations for actionable insights.",
        "/2024-01-29-ai-powered-audio-insights-analysis-translations/index.html",
    ),
    (
        "2024-01-23",
        "January 23, 2024",
        "AI",
        "AI Prompt Engineering 2024: Insights & Advanced Techniques",
        "https://cloudcdn.pro/stocks/images/ai-prompt-engineering-modern-office.webp",
        "Man analysing data on screens in a modern office",
        "Explore the 2024 advancements in AI Prompt Engineering, uncovering innovative trends and techniques revolutionising tech and finance sectors.",
        "/2024-01-23-advancements-in-ai-prompt-engineering/index.html",
    ),
    (
        "2024-01-15",
        "January 15, 2024",
        "Art",
        "Alien Studio: My Tech-to-Art Journey in Photography",
        "https://cloudcdn.pro/clients/alienstudio/v1/collections/radiance/radiance-08.webp",
        "A sunset's muse. Beauty in stillness from Alien Studio's Radiance collection",
        "Join me on my personal journey from Rust, AI, and Quantum Computing to redefining art and photography through Alien Studio.",
        "/2024-01-15-alien-studio-revolutionising-art-with-ai-photography/index.html",
    ),
    (
        "2024-01-08",
        "January 8, 2024",
        "Quantum · Finance",
        "Qiskit & Quantum Fourier Transform for Credit Ratio Analysis",
        "https://cloudcdn.pro/stocks/images/quantum-computer-room.webp",
        "A Quantum Computer Room",
        "Explore how IBM Qiskit and Quantum Fourier Transform revolutionise credit ratio analysis in finance, offering unprecedented accuracy and speed.",
        "/2024-01-08-optimising-credit-ratio-analysis-with-ibm-qiskit-and-quantum-fourier-transform/index.html",
    ),
    (
        "2024-01-01",
        "January 1, 2024",
        "AI",
        "AI Trends 2024: Insights and Predictions for the Future",
        "https://cloudcdn.pro/stocks/images/drone-view-of-london.webp",
        "A Drone View of London",
        "Explore the transformative AI trends of 2024, from generative AI to AI in retail, and how they'll shape our future.",
        "/2024-01-01-ai-trends-2024-insights-and-predictions-for-the-future/index.html",
    ),
    (
        "2023-12-25",
        "December 25, 2023",
        "Quantum · Finance",
        "Revolutionising Finance with AI-Enhanced Quantum Algorithms",
        "https://cloudcdn.pro/stocks/images/circuit_board_cityscape.webp",
        "A circuit board cityscape",
        "Explore the transformative role of AI in quantum algorithms for finance, with a focus on their mathematical intricacies and banking applications.",
        "/2023-12-25-revolutionising-finance-with-ai-enhanced-quantum-algorithms/index.html",
    ),
    (
        "2023-12-18",
        "December 18, 2023",
        "AI · Quantum",
        "State of AI and Quantum Computing in Banking: A 2023 Review",
        "https://cloudcdn.pro/stocks/images/getty-images-aTWKwJllPOA.webp",
        "A circuit board with an AI GPU",
        "Exploring 2023's technological landscape: AI and quantum computing revolutionising banking, rising open-source models, and evolving regulations.",
        "/2023-12-18-state-of-ai-and-quantum-computing-in-banking-a-2023-review/index.html",
    ),
    (
        "2023-12-11",
        "December 11, 2023",
        "Quantum · Banking",
        "Quantum Key Distribution Revolutionising Security in Banking",
        "https://cloudcdn.pro/stocks/images/hsbc-from-the-docks.webp",
        "HSBC Headquarter in London Canary Wharf Docks",
        "As quantum computers pose a threat to traditional encryption methods, Quantum Key Distribution (QKD) emerges as a game-changer for security.",
        "/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html",
    ),
    (
        "2023-12-04",
        "December 4, 2023",
        "Open source · Rust",
        "Efficient Date and Time Management with DateTime (DTT)",
        "https://cloudcdn.pro/clients/dtt/v1/logos/dtt.svg",
        "The DTT (DateTime) Rust library logo",
        "DateTime (DTT) is a comprehensive Rust library for parsing, validating, manipulating, and formatting dates and times. With high precision and broad functionality.",
        "/2023-12-04-mastering-date-and-time-in-rust-with-the-dtt-library/index.html",
    ),
    (
        "2023-11-28",
        "November 28, 2023",
        "Quantum · Rust",
        "KyberLib: A Rust-Powered Shield Against Quantum Threats",
        "https://cloudcdn.pro/clients/kyberlib/v1/logos/kyberlib.svg",
        "The KyberLib Rust library logo",
        "A robust and quantum-safe cryptography implementation of the CRYSTALS-Kyber algorithm, to protect data from quantum threats and cryptanalytic attacks.",
        "/2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats/index.html",
    ),
    (
        "2023-11-19",
        "November 19, 2023",
        "Quantum",
        "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age",
        "https://cloudcdn.pro/stocks/images/galina-nelyubova-V70-ng4FuiA.webp",
        "A complex quantum computer architecture",
        "Discover how CRYSTALS-Kyber, a quantum-resistant cryptography algorithm, is revolutionising the world of cryptography and preparing us for the quantum era.",
        "/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html",
    ),
    (
        "2023-11-12",
        "November 12, 2023",
        "AI",
        "Exploring Generative AI: Shaping the Future of Technology",
        "https://cloudcdn.pro/stocks/images/fabio-oyXis2kALVg.webp",
        "Holographic cubes at a concert",
        "Embark on a journey to explore Generative AI: investigating its impact, ethical implications, and future synergies.",
        "/2023-11-12-exploring-generative-ai/index.html",
    ),
    (
        "2023-11-05",
        "November 5, 2023",
        "Open source · Rust",
        "Mathematical and Cryptographic Constants for Rust Security",
        "https://cloudcdn.pro/stocks/images/antoine-dautry-05A-kdOH6Hw.webp",
        "Mathematical and cryptographic constants",
        "Safeguard code integrity with meticulously vetted mathematical and cryptographic constants, bolstering memory and concurrency safety for enhanced security.",
        "/2023-11-05-mathematical-and-cryptographic-constants-for-rust-security/index.html",
    ),
    (
        "2023-10-26",
        "October 26, 2023",
        "Open source · Rust",
        "Streamlining Rust Library Development with Code Generation",
        "https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp",
        "A white modern building",
        "Boost Rust library development with LibMake. A code generator tool that enforces best practices and generates initial code, saving developers time and effort.",
        "/2023-10-26-libmake-a-code-generator-to-reduce-repetitive-tasks-and-build-high-quality-rust-libraries/index.html",
    ),
    (
        "2023-10-16",
        "October 16, 2023",
        "Quantum · Rust",
        "Protecting Data in the Quantum Age: The Hash Library (HSH)",
        "https://cloudcdn.pro/stocks/images/galina-nelyubova-7ej8VWfwFsg.webp",
        "A creative illustration on the quantum computing theme",
        "The Hash Library (HSH) is a quantum-resistant cryptographic hash library that offers a lightweight, efficient, and easy-to-use solution for keeping data secure.",
        "/2023-10-16-protecting-data-in-the-quantum-age-the-hash-library-hsh/index.html",
    ),
    (
        "2023-10-09",
        "October 9, 2023",
        "Open source · Rust",
        "Static Site Generator: the fastest Rust-based SSG",
        "https://cloudcdn.pro/stocks/images/anna-nekrashevich-8534387.webp",
        "Turned-off laptop computer on top of a white table",
        "Empowering you to create high-impact static websites with infinite possibilities, limitless scalability, and a truly unique web presence that you control.",
        "/2023-10-09-shokunin-the-fastest-rust-based-static-site-generator/index.html",
    ),
    (
        "2023-09-29",
        "September 29, 2023",
        "Payments",
        "Automating ISO 20022 Payment Files Creation with pain001",
        "https://cloudcdn.pro/stocks/images/andrea-de-santis-T3Qen8vVgRc.webp",
        "A very tall building with intricate hollow façade detailing",
        "Streamlining the creation and compliance of ISO 20022 payment messages for cross-border payments and reporting.",
        "/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html",
    ),
    (
        "2018-02-15",
        "February 15, 2018",
        "Blockchain",
        "The Making of the Express Transaction Credits Platform",
        "https://cloudcdn.pro/stocks/images/rawpixel-com-369782.webp",
        "Man typing on a laptop keyboard",
        "Developing a comprehensive framework for the next generation of Ethereum Request for Comment compliant tokens using the ERC-223 standard.",
        "/2018-02-15-the-making-of-the-express-transaction-credits-platform/index.html",
    ),
    (
        "2018-02-04",
        "February 4, 2018",
        "Blockchain · Payments",
        "Unveiling a New Cryptocurrency and Faster Payment Solution",
        "https://cloudcdn.pro/stocks/images/laureen-missaire-DBbuhMbAIsQ.webp",
        "Canary Wharf clocks",
        "A significant chapter in the ongoing evolution of the global financial landscape, shaped by technological innovation, geopolitical shifts, and the future of money.",
        "/2018-02-04-unveiling-a-new-cryptocurrency-and-offering-future-faster-payment-solution/index.html",
    ),
    (
        "2018-01-24",
        "January 24, 2018",
        "Blockchain",
        "ERC-20: The Ethereum Token Interface That Changed the World",
        "https://cloudcdn.pro/stocks/images/m-ZzOa5G8hSPI.webp",
        "Computer screen with trades",
        "Ethereum Token Interface. Understanding ERC-20, which allows for the implementation of a standard API for tokens within smart contracts.",
        "/2018-01-24-the-erc-20-token-standard/index.html",
    ),
    (
        "2018-01-09",
        "January 9, 2018",
        "Blockchain",
        "Understanding the Technology behind Blockchain",
        "https://cloudcdn.pro/stocks/images/adam-smigielski-K5mPtONmpHM.webp",
        "Computer and mobile screens with trades",
        "Building a cryptocurrency on the Ethereum Blockchain: a comprehensive guide to blockchain development, tokenisation and cryptocurrency implementation.",
        "/2018-01-09-understanding-the-technology-behind-blockchain/index.html",
    ),
    (
        "2018-01-02",
        "January 2, 2018",
        "Blockchain",
        "Blockchain Explained. The Technology That Matters the Most",
        "https://cloudcdn.pro/stocks/images/bogdan-karlenko-cNcX6PPjEm8.webp",
        "Horizontal view of a tall building",
        "A story of the extraordinary journey of securing digital transactions through private-key cryptography and peer-to-peer (P2P) networks.",
        "/2018-01-02-blockchain-the-technology-that-matters-in-2018/index.html",
    ),
    (
        "2018-01-01",
        "January 1, 2018",
        "Blockchain",
        "Bitcoin: A Year in Review of the First Cryptocurrency",
        "https://cloudcdn.pro/stocks/images/traxer-AIKjbZdNOlw.webp",
        "Physical bitcoins on a flat surface",
        "Bitcoin. A Peer-to-Peer Electronic Cash System (P2P ECS) that has the potential to revolutionise the way people transact online.",
        "/2018-01-01-bitcoin-the-year-in-review/index.html",
    ),
]


def card_block(
    eyebrow: str,
    title: str,
    image: str,
    alt: str,
    date_iso: str,
    date_display: str,
    excerpt: str,
    href: str,
) -> str:
    return f"""<article class="newsroom-card">
<a class="newsroom-card-media" href="{href}" title="{title}">
<img alt="{alt}" src="{image}" loading="lazy" decoding="async" width="600" height="600" />
</a>
<div class="newsroom-card-body">
<span class="newsroom-eyebrow">{eyebrow}</span>
<h3><a href="{href}" title="{title}">{title}</a></h3>
<p class="newsroom-meta"><time datetime="{date_iso}">{date_display}</time> · Sebastien Rousseau</p>
<p class="newsroom-excerpt">{excerpt}</p>
</div>
</article>"""


def featured_block(art) -> str:
    date_iso, date_display, eyebrow, title, image, alt, excerpt, href = art
    return f"""<article class="newsroom-featured">
<a class="newsroom-featured-media" href="{href}" title="{title}">
<img alt="{alt}" src="{image}" loading="eager" fetchpriority="high" decoding="async" width="800" height="800" />
</a>
<div class="newsroom-featured-body">
<span class="newsroom-eyebrow">{eyebrow}</span>
<h3><a href="{href}" title="{title}">{title}</a></h3>
<p class="newsroom-meta"><time datetime="{date_iso}">{date_display}</time> · Sebastien Rousseau</p>
<p>{excerpt}</p>
<p><a class="pill ghost" href="{href}" title="{title}">Read the full story</a></p>
</div>
</article>"""


def _eyebrow_from_tags(tags: str) -> str:
    """Take the first three comma-separated tags, Title-Case them, and
    join with ` · `. Mirrors the manual ARTICLES eyebrow convention."""
    parts = [t.strip() for t in tags.split(",") if t.strip()][:3]
    return " · ".join(p.title() for p in parts)


def _tuple_from_post(date_str: str, path: _Path) -> tuple | None:
    """Build an ARTICLES-shaped tuple from a dated _posts/ entry. Returns
    None if the file lacks a usable title."""
    fm, _body = parse_frontmatter(path.read_text(encoding="utf-8"))
    if not fm.get("title"):
        return None
    slug = path.stem
    title = fm["title"]
    banner = fm.get("banner", "")
    banner_alt = fm.get("banner_alt", title)
    excerpt = (fm.get("excerpt") or fm.get("subtitle") or fm.get("description") or title)[:320]
    eyebrow = _eyebrow_from_tags(fm.get("tags", "")) or "Banking · Technology"
    return (
        date_str,
        display_date(date_str),
        eyebrow,
        title,
        banner,
        banner_alt,
        excerpt,
        f"/{slug}/index.html",
    )


def _discover_missing_articles() -> list[tuple]:
    """Scan _posts/YYYY-MM-DD-*.md for any article newer than ARTICLES[0]
    that is not already present in ARTICLES (matched by date + slug).
    Return a list of ARTICLES-shaped tuples in date-descending order so
    they can be prepended ahead of the existing curated list.

    Previously this function only surfaced the single latest article,
    which meant if more than one daily article published between two
    ARTICLES[] refreshes, the in-between ones silently disappeared from
    /articles/. The fix is to surface ALL missing dated posts."""
    if not POSTS.is_dir():
        return []
    dated: list[tuple[str, _Path]] = []
    for md in POSTS.glob("*.md"):
        m = _DATED_RE.match(md.name)
        if m:
            dated.append((m.group(1), md))
    if not dated:
        return []
    head_date = ARTICLES[0][0] if ARTICLES else ""
    existing_hrefs = {a[7] for a in ARTICLES}
    discovered: list[tuple] = []
    for date_str, path in sorted(dated, reverse=True):
        if date_str <= head_date:
            break
        href = f"/{path.stem}/index.html"
        if href in existing_hrefs:
            continue
        tup = _tuple_from_post(date_str, path)
        if tup is not None:
            discovered.append(tup)
    return discovered


def _refresh_banner_from_frontmatter(article: tuple) -> tuple:
    """Re-read the article's current ``banner:`` + ``banner_alt:`` from
    ``_posts/<slug>.md`` and patch them into the static ``ARTICLES``
    tuple. Without this step, the hard-coded image URL drifts whenever
    a back-catalogue article gets a banner swap — the homepage card
    (hand-edited in ``_posts/index.md``) and the article-page hero (read
    from frontmatter) stay in sync, but the /articles/ grid card keeps
    serving the old URL until someone hand-edits this file.

    The tuple shape is preserved; only fields 4 (banner) and 5 (alt)
    are overwritten with current frontmatter values. If the post file
    is missing the tuple is passed through unchanged.
    """
    date_iso, date_display, eyebrow, title, banner, banner_alt, excerpt, href = article
    slug = href.strip("/").removesuffix("/index.html")
    md = POSTS / f"{slug}.md"
    if not md.is_file():
        return article
    fm, _ = parse_frontmatter(md.read_text(encoding="utf-8"))
    new_banner = fm.get("banner", banner) or banner
    new_alt = fm.get("banner_alt", banner_alt) or banner_alt
    if new_banner == banner and new_alt == banner_alt:
        return article
    return (date_iso, date_display, eyebrow, title, new_banner, new_alt, excerpt, href)


def main() -> None:
    # Re-sync every static ARTICLES entry's banner + alt from current
    # frontmatter so the /articles/ grid never serves a stale image
    # when an older article gets a banner swap upstream.
    articles = [_refresh_banner_from_frontmatter(a) for a in ARTICLES]
    discovered = _discover_missing_articles()
    for auto in reversed(discovered):
        articles.insert(0, auto)
        print(f"gen_articles: auto-prepended {auto[0]} (slug={auto[7]})")

    text = SRC.read_text()
    # Preserve YAML frontmatter (lines bounded by `---`), drop the body.
    lines = text.splitlines(keepends=True)
    delim_idx = [i for i, ln in enumerate(lines) if ln.strip() == "---"]
    if len(delim_idx) < 2:
        raise SystemExit("could not locate frontmatter delimiters in articles.md")
    head = "".join(lines[: delim_idx[1] + 1]) + "\n"

    featured = featured_block(articles[0])
    cards = "\n\n".join(
        card_block(a[2], a[3], a[4], a[5], a[0], a[1], a[6], a[7]) for a in articles[1:]
    )

    body = f"""<section class="newsroom">

<header class="newsroom-section-head"><p class="newsroom-kicker">FEATURED</p><h2>Latest story</h2></header>

{featured}

<header class="newsroom-section-head"><p class="newsroom-kicker">ARCHIVE</p><h2>All news stories and articles</h2></header>

<div class="newsroom-grid">

{cards}

</div>

</section>
"""

    SRC.write_text(head + body)
    print(f"wrote {SRC}. Featured: 1, grid cards: {len(articles) - 1}")


if __name__ == "__main__":
    main()
