"""Canonical EN → FR slug map for every translated article.

A single source of truth used by:
  * ``build_translations.py``  — writes ``public/fr/<fr_slug>/index.html``
                                  and rewrites EN cross-links to FR.
  * ``build_fr_feeds.py``      — emits ``public/fr/rss.xml`` /
                                  ``atom.xml`` / ``news-sitemap.xml``.
  * ``postbuild.py``           — pairs hreflang en ↔ fr by slug.

Every key MUST be the markdown stem of a file present in
``_posts/fr/``. The value is the FR URL slug under ``/fr/`` — same
date prefix, then a translated, ASCII-folded body.
"""
from __future__ import annotations

EN_TO_FR: dict[str, str] = {
    "2018-01-01-bitcoin-the-year-in-review":
        "2018-01-01-bitcoin-l-annee-en-revue",
    "2018-01-02-blockchain-the-technology-that-matters-in-2018":
        "2018-01-02-blockchain-la-technologie-qui-compte-en-2018",
    "2018-01-09-understanding-the-technology-behind-blockchain":
        "2018-01-09-comprendre-la-technologie-derriere-la-blockchain",
    "2018-01-24-the-erc-20-token-standard":
        "2018-01-24-la-norme-de-jeton-erc-20",
    "2018-02-04-unveiling-a-new-cryptocurrency-and-offering-future-faster-payment-solution":
        "2018-02-04-nouvelle-cryptomonnaie-solution-de-paiement-plus-rapide",
    "2018-02-15-the-making-of-the-express-transaction-credits-platform":
        "2018-02-15-creation-de-la-plateforme-express-transaction-credits",
    "2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001":
        "2023-09-29-automatiser-fichiers-de-paiement-iso-20022-avec-pain001",
    "2023-10-09-shokunin-the-fastest-rust-based-static-site-generator":
        "2023-10-09-shokunin-generateur-de-sites-statiques-rust-le-plus-rapide",
    "2023-10-16-protecting-data-in-the-quantum-age-the-hash-library-hsh":
        "2023-10-16-proteger-les-donnees-a-l-ere-quantique-bibliotheque-de-hachage-hsh",
    "2023-10-26-libmake-a-code-generator-to-reduce-repetitive-tasks-and-build-high-quality-rust-libraries":
        "2023-10-26-libmake-generateur-de-code-pour-bibliotheques-rust",
    "2023-11-05-mathematical-and-cryptographic-constants-for-rust-security":
        "2023-11-05-constantes-mathematiques-et-cryptographiques-pour-rust",
    "2023-11-12-exploring-generative-ai":
        "2023-11-12-explorer-l-ia-generative",
    "2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age":
        "2023-11-19-algorithme-de-protection-a-l-ere-quantique-crystals-kyber",
    "2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats":
        "2023-11-28-kyberlib-bouclier-rust-contre-les-menaces-quantiques",
    "2023-12-04-mastering-date-and-time-in-rust-with-the-dtt-library":
        "2023-12-04-maitriser-date-et-heure-en-rust-avec-la-bibliotheque-dtt",
    "2023-12-11-quantum-key-distribution-revolutionising-security-in-banking":
        "2023-12-11-distribution-quantique-de-cles-revolution-securite-bancaire",
    "2023-12-18-state-of-ai-and-quantum-computing-in-banking-a-2023-review":
        "2023-12-18-etat-ia-et-informatique-quantique-banque-revue-2023",
    "2023-12-25-revolutionising-finance-with-ai-enhanced-quantum-algorithms":
        "2023-12-25-revolutionner-la-finance-avec-des-algorithmes-quantiques-ia",
    "2024-01-01-ai-trends-2024-insights-and-predictions-for-the-future":
        "2024-01-01-tendances-ia-2024-perspectives-et-predictions",
    "2024-01-08-optimising-credit-ratio-analysis-with-ibm-qiskit-and-quantum-fourier-transform":
        "2024-01-08-optimiser-le-ratio-de-credit-avec-ibm-qiskit-et-fourier-quantique",
    "2024-01-15-alien-studio-revolutionising-art-with-ai-photography":
        "2024-01-15-revolution-de-l-art-par-la-photographie-ia-alien-studio",
    "2024-01-23-advancements-in-ai-prompt-engineering":
        "2024-01-23-avancees-en-ingenierie-de-prompts-ia",
    "2024-01-29-ai-powered-audio-insights-analysis-translations":
        "2024-01-29-analyse-audio-traductions-et-perspectives-par-l-ia",
    "2024-02-08-revolutionising-advertising-how-ai-shapes-the-future":
        "2024-02-08-revolutionner-la-publicite-comment-l-ia-faconne-l-avenir",
    "2024-02-12-akande-voice-assistant-revolutionising-personal-and-executive-assistance":
        "2024-02-12-akande-assistant-vocal-revolution-assistance-personnelle-et-executive",
    "2024-02-13-eus-ai-act-shaping-the-future-of-global-ai-regulation":
        "2024-02-13-reglement-europeen-sur-l-ia-faconner-l-avenir-de-la-regulation-mondiale",
    "2024-02-19-unlocking-gemini-google-ai-revolution-explained":
        "2024-02-19-decouvrir-gemini-la-revolution-ia-de-google-expliquee",
    "2024-02-26-google-gemma-ai-transforming-open-source-ai-development":
        "2024-02-26-google-gemma-transformer-le-developpement-ia-en-source-ouverte",
    "2024-03-04-le-chat-by-mistral-ai-a-new-era-in-conversational-ai":
        "2024-03-04-le-chat-de-mistral-ai-une-nouvelle-ere-de-l-ia-conversationnelle",
    "2024-03-08-rustlogs-advanced-logging-library-for-rust-applications":
        "2024-03-08-rustlogs-bibliotheque-de-journalisation-avancee-pour-rust",
    "2024-03-12-revolutionising-real-time-speech-recognition-on-macos-with-openai-whisper":
        "2024-03-12-revolutionner-la-reconnaissance-vocale-en-temps-reel-sur-macos-avec-whisper",
    "2024-03-18-advancing-ai-with-multimodal-llms-insights-from-mm1":
        "2024-03-18-faire-avancer-l-ia-avec-les-llm-multimodaux-enseignements-de-mm1",
    "2024-03-25-fully-homomorphic-encryption-in-a-banking-quantum-era":
        "2024-03-25-chiffrement-completement-homomorphique-a-l-ere-quantique-bancaire",
    "2024-04-01-openvoice-leading-innovation-in-voice-cloning-technology":
        "2024-04-01-openvoice-innovation-de-pointe-dans-le-clonage-vocal",
    "2024-04-15-quantum-algorithm-challenges-lattice-based-cryptography":
        "2024-04-15-l-algorithme-quantique-defie-la-cryptographie-fondee-sur-les-reseaux",
    "2024-04-22-bug-discovered-in-quantum-algorithm-for-lattice-based-crypto":
        "2024-04-22-anomalie-dans-l-algorithme-quantique-pour-la-cryptographie-fondee-sur-les-reseaux",
    "2025-09-01-quantum-safe-payments-epaa":
        "2025-09-01-paiements-resistants-au-quantique-epaa",
    "2026-04-11-quantum-thresholds-are-moving-again":
        "2026-04-11-les-seuils-quantiques-bougent-a-nouveau",
    "2026-05-11-lucy-besson-knowledge-transfer-ai-quantum":
        "2026-05-11-lucy-besson-transfert-de-connaissances-ia-et-quantique",
    "2026-05-12-iso-20022-pacs008-structured-address-deadline":
        "2026-05-12-iso-20022-pacs008-adresse-structuree-echeance",
    "2026-05-14-securing-the-ledger-post-quantum-migration-corporate-finance":
        "2026-05-14-securiser-le-livre-comptable-migration-post-quantique-finance-entreprise",
    "2026-05-15-blackrock-brsrv-bstbl-genius-act-tokenised-mmf":
        "2026-05-15-rendement-cache-decryptage-depots-blackrock-brsrv-bstbl-genius-act",
    "2026-05-18-agentic-engineering-banks-blueprint-2026":
        "2026-05-18-ingenierie-agentique-banques-blueprint-2026",
}

FR_TO_EN: dict[str, str] = {fr: en for en, fr in EN_TO_FR.items()}


def fr_slug(en_slug: str) -> str:
    """Return the FR slug for an EN slug, or the EN slug unchanged if
    no translation is recorded (so legacy fall-through still works)."""
    return EN_TO_FR.get(en_slug, en_slug)


def en_slug(fr_slug: str) -> str:
    """Reverse map (FR → EN). Returns the input unchanged if not found."""
    return FR_TO_EN.get(fr_slug, fr_slug)
