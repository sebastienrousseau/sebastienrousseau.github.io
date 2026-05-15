<!-- SPDX-License-Identifier: Apache-2.0 -->

# German (`de`) — translation tracker

**Status:** `planned` — data foundation in place; pending native-speaker review and article translation. Will flip to `active` in `scripts/_lang_registry.py` only when every box below is checked.

## Definition of Done

Per the Phase 1 plan, this language is **fully green** when:

- [ ] Every English article in `_posts/*.md` has a counterpart in `_posts/de/<de-slug>.md`
- [ ] `_data/i18n/de/slugs.json`, `topics.json`, `static_pages.json` all reviewed by a native speaker (sign-offs below)
- [ ] `scripts/test_i18n_parity.py` green for `de`
- [ ] `scripts/test_hreflang_reciprocity.py` green
- [ ] pa11y AAA: 0 violations on every `/de/` page
- [ ] Lighthouse: perf ≥0.90, a11y ≥0.98, best-practices ≥0.95, SEO ≥0.95 (median of 3 runs)
- [ ] WAVE manual pass on `/de/`, `/de/uber-mich/`, one article
- [ ] Visual diff vs EN at desktop / tablet / mobile within ±10% pixel tolerance — DE expansion is +25-40%, layout must absorb it
- [ ] Newsletter form + contact form submit successfully with localised subject lines
- [ ] Search overlay (⌘K) auto-loads `/de/search-index.json` and returns ranked hits for `Zahlung`, `Quanten`, `KI`, `ISO 20022`
- [ ] `Language("de", ..., active=True)` flipped in `scripts/_lang_registry.py`

## Inventory

### Slug map — `slugs.json`
- [x] **DRAFT** — 16 static + 42 article slugs (this PR)
- [ ] Native review (idiomatic German, no obvious calque)
- [ ] Sign-off: _________ (date: _________)

### Topic glossary — `topics.json`
- [x] **DRAFT** — 5 topic clusters (this PR)
- [ ] Native review
- [ ] Domain review (banking + crypto terminology)
- [ ] Sign-off: _________ (date: _________)

### Static-page metadata — `static_pages.json`
- [x] **DRAFT** — 15 static pages (this PR)
- [ ] Native review
- [ ] Verify titles ≤55 chars (SERP truncation budget; DE expansion may breach)
- [ ] Sign-off: _________ (date: _________)

### Article translations — `_posts/de/*.md`
None yet. 42 EN articles to translate.

| EN slug | DE slug | translator | reviewer | status |
|---|---|---|---|---|
| 2018-01-01-bitcoin-the-year-in-review | 2018-01-01-bitcoin-das-jahr-im-rueckblick | — | — | pending |
| 2018-01-02-blockchain-the-technology-that-matters-in-2018 | 2018-01-02-blockchain-die-technologie-die-2018-zaehlt | — | — | pending |
| 2018-01-09-understanding-the-technology-behind-blockchain | 2018-01-09-die-technologie-hinter-blockchain-verstehen | — | — | pending |
| 2018-01-24-the-erc-20-token-standard | 2018-01-24-der-erc-20-token-standard | — | — | pending |
| 2018-02-04-unveiling-a-new-cryptocurrency-and-offering-future-faster-payment-solution | 2018-02-04-neue-kryptowaehrung-schnellere-zahlungsloesung-fuer-die-zukunft | — | — | pending |
| 2018-02-15-the-making-of-the-express-transaction-credits-platform | 2018-02-15-entstehung-der-express-transaction-credits-plattform | — | — | pending |
| 2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001 | 2023-09-29-iso-20022-konforme-zahlungsdateien-automatisieren-mit-pain001 | — | — | pending |
| 2023-10-09-shokunin-the-fastest-rust-based-static-site-generator | 2023-10-09-shokunin-der-schnellste-rust-basierte-static-site-generator | — | — | pending |
| 2023-10-16-protecting-data-in-the-quantum-age-the-hash-library-hsh | 2023-10-16-daten-im-quantenzeitalter-schuetzen-die-hash-bibliothek-hsh | — | — | pending |
| 2023-10-26-libmake-a-code-generator-to-reduce-repetitive-tasks-and-build-high-quality-rust-libraries | 2023-10-26-libmake-codegenerator-fuer-hochwertige-rust-bibliotheken | — | — | pending |
| 2023-11-05-mathematical-and-cryptographic-constants-for-rust-security | 2023-11-05-mathematische-und-kryptografische-konstanten-fuer-rust-sicherheit | — | — | pending |
| 2023-11-12-exploring-generative-ai | 2023-11-12-generative-ki-im-detail | — | — | pending |
| 2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age | 2023-11-19-crystals-kyber-der-schutzalgorithmus-im-quantenzeitalter | — | — | pending |
| 2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats | 2023-11-28-kyberlib-rust-schild-gegen-quantenbedrohungen | — | — | pending |
| 2023-12-04-mastering-date-and-time-in-rust-with-the-dtt-library | 2023-12-04-datum-und-zeit-in-rust-meistern-mit-der-dtt-bibliothek | — | — | pending |
| 2023-12-11-quantum-key-distribution-revolutionising-security-in-banking | 2023-12-11-quantenschluesselverteilung-revolution-der-banksicherheit | — | — | pending |
| 2023-12-18-state-of-ai-and-quantum-computing-in-banking-a-2023-review | 2023-12-18-stand-von-ki-und-quantencomputern-im-banking-rueckblick-2023 | — | — | pending |
| 2023-12-25-revolutionising-finance-with-ai-enhanced-quantum-algorithms | 2023-12-25-finanzwesen-revolutionieren-mit-ki-gestuetzten-quantenalgorithmen | — | — | pending |
| 2024-01-01-ai-trends-2024-insights-and-predictions-for-the-future | 2024-01-01-ki-trends-2024-einblicke-und-vorhersagen | — | — | pending |
| 2024-01-08-optimising-credit-ratio-analysis-with-ibm-qiskit-and-quantum-fourier-transform | 2024-01-08-kreditquotenanalyse-optimieren-mit-ibm-qiskit-und-quanten-fourier-transformation | — | — | pending |
| 2024-01-15-alien-studio-revolutionising-art-with-ai-photography | 2024-01-15-alien-studio-kunst-revolution-durch-ki-fotografie | — | — | pending |
| 2024-01-23-advancements-in-ai-prompt-engineering | 2024-01-23-fortschritte-im-ki-prompt-engineering | — | — | pending |
| 2024-01-29-ai-powered-audio-insights-analysis-translations | 2024-01-29-ki-gestuetzte-audio-einblicke-analyse-uebersetzungen | — | — | pending |
| 2024-02-08-revolutionising-advertising-how-ai-shapes-the-future | 2024-02-08-werbung-revolutionieren-wie-ki-die-zukunft-gestaltet | — | — | pending |
| 2024-02-12-akande-voice-assistant-revolutionising-personal-and-executive-assistance | 2024-02-12-akande-sprachassistent-revolution-persoenlicher-und-fuehrungsassistenz | — | — | pending |
| 2024-02-13-eus-ai-act-shaping-the-future-of-global-ai-regulation | 2024-02-13-eu-ki-verordnung-die-zukunft-der-globalen-ki-regulierung | — | — | pending |
| 2024-02-19-unlocking-gemini-google-ai-revolution-explained | 2024-02-19-gemini-erklaert-die-ki-revolution-von-google | — | — | pending |
| 2024-02-26-google-gemma-ai-transforming-open-source-ai-development | 2024-02-26-google-gemma-transformiert-die-open-source-ki-entwicklung | — | — | pending |
| 2024-03-04-le-chat-by-mistral-ai-a-new-era-in-conversational-ai | 2024-03-04-le-chat-von-mistral-ai-neue-aera-der-konversations-ki | — | — | pending |
| 2024-03-08-rustlogs-advanced-logging-library-for-rust-applications | 2024-03-08-rustlogs-erweiterte-logging-bibliothek-fuer-rust-anwendungen | — | — | pending |
| 2024-03-12-revolutionising-real-time-speech-recognition-on-macos-with-openai-whisper | 2024-03-12-echtzeit-spracherkennung-auf-macos-mit-openai-whisper | — | — | pending |
| 2024-03-18-advancing-ai-with-multimodal-llms-insights-from-mm1 | 2024-03-18-ki-voranbringen-mit-multimodalen-llms-erkenntnisse-aus-mm1 | — | — | pending |
| 2024-03-25-fully-homomorphic-encryption-in-a-banking-quantum-era | 2024-03-25-vollstaendig-homomorphe-verschluesselung-im-quanten-banking | — | — | pending |
| 2024-04-01-openvoice-leading-innovation-in-voice-cloning-technology | 2024-04-01-openvoice-fuehrende-innovation-im-voice-cloning | — | — | pending |
| 2024-04-15-quantum-algorithm-challenges-lattice-based-cryptography | 2024-04-15-quantenalgorithmus-fordert-gitterbasierte-kryptografie-heraus | — | — | pending |
| 2024-04-22-bug-discovered-in-quantum-algorithm-for-lattice-based-crypto | 2024-04-22-fehler-im-quantenalgorithmus-fuer-gitterbasierte-kryptografie-entdeckt | — | — | pending |
| 2025-09-01-quantum-safe-payments-epaa | 2025-09-01-quantensichere-zahlungen-epaa | — | — | pending |
| 2026-04-11-quantum-thresholds-are-moving-again | 2026-04-11-quantenschwellen-verschieben-sich-erneut | — | — | pending |
| 2026-05-11-lucy-besson-knowledge-transfer-ai-quantum | 2026-05-11-lucy-besson-wissenstransfer-ki-und-quanten | — | — | pending |
| 2026-05-12-iso-20022-pacs008-structured-address-deadline | 2026-05-12-iso-20022-pacs008-strukturierte-adresse-frist | — | — | pending |
| 2026-05-14-securing-the-ledger-post-quantum-migration-corporate-finance | 2026-05-14-das-hauptbuch-sichern-post-quanten-migration-im-corporate-finance | — | — | pending |
| 2026-05-15-blackrock-brsrv-bstbl-genius-act-tokenised-mmf | 2026-05-15-blackrock-brsrv-bstbl-genius-act-tokenisierter-geldmarktfonds | — | — | pending |
| 2026-05-18-agentic-engineering-banks-blueprint-2026 | 2026-05-18-agentische-engineering-banken-blueprint-2026 | — | — | pending |

### UI chrome strings (CHROME_PATCHES equivalent)
Not yet extracted. The current FR pipeline carries ~200 regex patches in `scripts/build_translations.py:CHROME_PATCHES` covering nav, footer, search, aria-labels, CTAs. Required deliverable before German articles can render: `_data/i18n/de/strings.json` with the same key set as `_data/i18n/fr/strings.json` (still to be authored as a future-Phase-0 deliverable).

### Static page bodies (curated `<main>` content)
`STATIC_BODIES_FR` in `build_translations.py` curates the `<main>` body for ~15 pages (about, contact, privacy, terms, accessibility, thanks, offline, etc.). Required deliverable: `_posts/de/*.md` per static page **or** a `_data/i18n/de/static_bodies/<slug>.md` set if we keep the body separate from the article-style markdown.

### Feeds
- `/de/rss.xml`, `/de/atom.xml`, `/de/news-sitemap.xml` — generated by `build_fr_feeds.py` (will need a `build_lang_feeds.py` refactor or a per-language config). Tracked under the broader Phase 2 work.

### Search index
- `/de/search-index.json` — emitted by `build_translations.py:_build_fr_search_index()` (rename + generalise needed).

## Quick numbers — German specifics

| Metric | Value |
|---|---|
| Text expansion vs EN | +25-40% (worst-case among target languages) |
| Compound-noun risk | High — long compounds may break nav buttons (`Zahlungsverkehrstransformation`) |
| Layout risk | Largest of any active candidate. Visual-diff CI must pass before flipping `active=True` |
| Native-speaker reviewer | TBD — engage before article translation kicks off |
| Translation memory | None yet. Set up Weblate + import EN/FR pair as starter TM after lang 5 (per plan) |

## How to flip the language to `active`

1. All boxes above checked
2. `scripts/_lang_registry.py`: change `Language("de", ..., active=True)`
3. `scripts/test_i18n_parity.py` must pass — fails if any EN article lacks a `_posts/de/*.md` counterpart
4. CI gates green
5. Update `_layouts/index.html` to remove the "Coming soon" `aria-disabled` from the DE entry in the language switcher

Until all four happen, German appears in the menu as "Coming soon" and contributes nothing to sitemaps or hreflang.
