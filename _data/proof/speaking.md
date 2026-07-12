---
# =============================================================================
# Speaking page content, the single source of truth for /speaking/.
# All copy lives here (not in Python) so it can be edited and translated.
# Per-locale translations overlay this file via _data/proof/i18n/<lang>/speaking.md
# (English is the fallback until a locale is backfilled).
#
# Style: no em dashes anywhere (house rule). Standards identifiers
# (ISO 20022, pacs.008, FIPS 203, ...) are wrapped in `mono` at render time.
# =============================================================================

title: "Speaking & advisory"
meta_title: "Sebastien Rousseau: keynotes, panels & expert comment on payments, post-quantum & applied AI"
meta_description: "Senior banking technologist with 20+ years across HSBC, PayPal and Barclays. Keynotes, panels and expert media comment on payments modernisation, post-quantum cryptography and applied AI, for boards, conferences and newsrooms."

# --- Hero -------------------------------------------------------------------
hero:
  eyebrow: "Keynotes · Panels · Expert comment"
  headline: "The technologies reshaping banking, explained to the people who have to act."
  lede: "Sebastien Rousseau is a senior banking technologist with 20+ years across HSBC, PayPal and Barclays. He turns payments modernisation, post-quantum cryptography and applied AI from policy paper into inspectable code, and into keynotes a board can act on."
  primary_cta: "Invite me to speak"
  secondary_cta: "Explore keynotes"
  press_nudge: "Journalist on deadline?"
  press_nudge_cta: "Book expert comment"
  microproof:
    - "Shipped payments at HSBC, PayPal & Barclays"
    - "Co-author, EPA quantum-safe white paper"
    - "Contributor, Emerging Payments Association Asia"

# --- Employer proof strip ---------------------------------------------------
employers_label: "Shipped payment platforms at"
employers:
  - "HSBC"
  - "PayPal"
  - "Barclays"
  - "Shazam"
  - "AKQA"
  - "Virgin Group"

# --- Stats band (all figures real; downloads/stars/articles refreshed from metrics.json) ---
stats_eyebrow: "By the numbers"
stats:
  - { kpi: "years_payments", label: "Years in banking & payments" }
  - { kpi: "articles_signed", label: "Signed, dated articles" }
  - { kpi: "downloads_total", label: "Open-source downloads" }
  - { kpi: "github_stars",    label: "GitHub stars" }
stats_foot: 'Contributor to the EPAA Quantum-Safe Cryptography Working Group. Co-author of the EPA white paper "Quantum-Safe Payments: Why the Payments Industry Must Act Now" (September 2025).'

# --- Two paths (organisers vs journalists) ----------------------------------
paths:
  eyebrow: "Two ways to work with me"
  headline: "Book a stage, or book a source."
  lede: "Boards and conferences need someone who can hold a room. Newsrooms need someone who can give a clean, accurate quote on deadline. I do both."
  items:
    - eyebrow: "For organisers"
      title: "Speak at your event"
      body: "Keynotes, panels and workshops for boards, conferences and executive teams navigating payments, post-quantum and AI."
      bullets:
        - "Boards, exec committees & risk functions"
        - "Industry conferences & standards bodies"
        - "Tailored to your stack, vendor-neutral, no product pitch"
      cta_label: "Invite me to speak"
      cta_target: "book"
    - eyebrow: "For journalists & producers"
      title: "Book me for expert comment"
      body: "Broadcast-ready commentary on payments, post-quantum cryptography and applied AI, for print, radio, TV and podcasts."
      bullets:
        - "Fast turnaround on deadline"
        - "Plain-English quotes, or deep technical detail"
        - "Background briefings & data on request"
      cta_label: "See press & media"
      cta_target: "media"

# --- Signature keynotes -----------------------------------------------------
keynotes:
  eyebrow: "Signature keynotes"
  headline: "Talks built for the boardroom."
  lede: "Each talk turns a live industry problem into a decision a room can act on. Every one is tagged for the audience it is written for, and can be tailored to yours."
  flag_delivered: "Delivered · Available now"
  flag_new: "New for 2026"
  outcome_label: "You leave with:"
  talks:
    - title: "Post-Quantum Migration for Payments: From FIPS 203 to Inspectable Code"
      new: false
      desc: "What the November 2026 SWIFT cutover, FIPS 203, and harvest-now-decrypt-later mean for a Tier-1 payments stack, and how to turn migration into a measurable, board-grade engineering programme."
      outcome: "a board-ready migration roadmap and the metrics to govern it."
      audience: "Board / CISO / Head of Payments"
    - title: "ISO 20022 in Practice: pacs.008, pain.001, and the Structured-Address Cliff"
      new: false
      desc: "A field guide to building production-grade ISO 20022 automation: structured-address compliance, BAH/head.001 wrapping, BIC/IBAN/LEI checksums, and OpenTelemetry UETR tracing."
      outcome: "a concrete engineering checklist for the address deadline."
      audience: "Payments Architects / Treasury Engineering Leads"
    - title: "Open Source as Financial Infrastructure"
      new: false
      desc: "Why open-source reference implementations beat proprietary black boxes for security, compliance, and supplier risk under DORA, and how to govern them inside a regulated institution."
      outcome: "a supplier-risk framework for open-source in production."
      audience: "Heads of Engineering / Procurement / Risk"
    - title: "Harvest-Now-Decrypt-Later: The Board-Level Case for Quantum-Safe Payments"
      new: false
      desc: "Translating cryptographic agility from a project paper into a board-level operational-resilience commitment, using the EPAA framework, NIST PQC standards, and a concrete migration roadmap."
      outcome: "the language to brief a board on cryptographic risk."
      audience: "Board / Executive Committee / Group CRO"
    - title: "Agentic AI in Banking: From Demo to Auditable Workflow"
      new: true
      desc: "The five-component control plane that turns autonomous workflows into SR 11-7 / SS1/23 supervisory-ready evidence: OAuth-scoped accounts, deterministic routing, OPA policy gates, immutable WORM audit logs, and a tested kill switch."
      outcome: "a control plane your model-risk team can actually sign off."
      audience: "CTO / Head of AI / Model Risk Management"
  custom:
    title: "Need a talk tailored to your stack?"
    body: "Every keynote can be re-cut for your institution, your regulators and your migration timeline."
    cta_label: "Discuss a custom talk"

# --- How I work (formats + reach) -------------------------------------------
work:
  eyebrow: "For organisers"
  headline: "How I work."
  formats:
    - { name: "Keynote", duration: "30 to 45 min", body: "A single, tightly-argued talk built around one decision your audience has to make. Tailored to your stack and regulators." }
    - { name: "Panel", duration: "60 min", body: "Moderated or contributing. I bring the technical detail that keeps a panel honest and the plain English that keeps it useful." }
    - { name: "Workshop", duration: "Half-day or full-day", body: "Hands-on, board-to-engineering. We leave with an artefact: a roadmap, a checklist, or a reference implementation." }
  reach:
    - "London, UK"
    - "Mainland Europe (in-person)"
    - "Remote (worldwide)"
    - "English & French"

# --- Press & media (expert source) ------------------------------------------
media:
  eyebrow: "Press & media"
  headline: "An expert source, on deadline."
  availability: "Available for live comment · UK / GMT"
  body: "Broadcast-ready commentary on payments, post-quantum cryptography and applied AI. I give plain-English quotes for a general audience, or go as deep as your specialist desk needs."
  spec:
    - "studio-quality audio + backup line"
    - "camera-ready for remote TV"
    - "typical reply within 2 hours on deadline"
  cta_label: "Book expert comment"
  topics:
    - { tag: "Payments", text: "What the Nov 2026 SWIFT / ISO 20022 cutover means for banks" }
    - { tag: "Post-quantum", text: 'Why "harvest now, decrypt later" is a board-level risk today' }
    - { tag: "FIPS 203", text: "The NIST standards and the migration race behind them" }
    - { tag: "Applied AI", text: "Agentic AI, model risk and what regulators will demand" }
    - { tag: "Open source", text: "Open code as regulated financial infrastructure" }

# --- Biography (headline here; prose is the markdown body below) -------------
biography:
  eyebrow: "Biography"
  headline: "About Sebastien."
  portrait: "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp"
  portrait_alt: "Portrait of Sebastien Rousseau"

# --- Ready-to-use bios ------------------------------------------------------
bios:
  eyebrow: "For producers & chairs"
  headline: "Ready-to-use bio."
  lede: "Copy-paste, pre-approved, in three lengths. No back-and-forth."
  copy_label: "Copy"
  items:
    - length: "Short"
      text: "Sebastien Rousseau is a senior banking technologist who writes and builds at the edge of payments, post-quantum cryptography, and applied AI. Author of open-source libraries used in financial infrastructure; contributor to the Emerging Payments Association Asia Quantum-Safe Cryptography Working Group."
    - length: "Medium"
      text: "Sebastien Rousseau is a senior banking technologist with 20+ years across HSBC Commercial & Investment Bank, PayPal, Barclays, Shazam, AKQA, and Virgin Group. He authors open-source Python and Rust libraries that turn ISO 20022 migration, post-quantum cryptography, and applied AI from policy paper into inspectable code. He contributes to the Emerging Payments Association Asia Quantum-Safe Cryptography Working Group and publishes Banking On Quantum and Banking On AI at sebastienrousseau.com."
    - length: "Long"
      text: 'Sebastien Rousseau is a senior banking technologist focused on the structural transformation of wholesale payments. Across HSBC Commercial & Investment Bank, PayPal, Barclays, Shazam, AKQA, and Virgin Group, he has shipped payment platforms, AI products, and open-source infrastructure used in production by treasury and payments teams. He authors and maintains pacs.008, pain.001, BankStatementParser, KyberLib, CloudCDN, and dotfiles, each positioned as a reference implementation, not a demo, for inspectable, board-grade financial infrastructure. He is a contributor to the Emerging Payments Association Asia Quantum-Safe Cryptography Working Group, co-author of the EPA white paper "Quantum-Safe Payments: Why the Payments Industry Must Act Now" (September 2025), and publishes Banking On Quantum and Banking On AI. He works at the intersection of agentic AI, real-time payments, post-quantum cryptography, cloud-native resilience, structured data, and regulatory evidence.'

# --- FAQ --------------------------------------------------------------------
faq:
  eyebrow: "Before you ask"
  headline: "Booking, in plain terms."
  items:
    - q: "Will you tailor the talk to our institution?"
      a: "Yes. Every keynote is re-cut for your stack, your regulators, and your migration timeline. I will take a short briefing call beforehand so the examples land as your problem, not a generic one."
    - q: "Are you vendor-neutral, or is this a product pitch?"
      a: "Vendor-neutral. I do not sell a platform and I do not take the stage to promote one. The open-source work is reference implementation, not a sales funnel. If your audience needs impartial technical judgement, that is the point."
    - q: "Can you present under NDA or on sensitive topics?"
      a: "Yes. I am comfortable working under NDA and briefing on confidential migration or risk programmes. Say so in your enquiry and we will handle paperwork before anything else."
    - q: "Do you travel, and what lead time do you need?"
      a: "I speak in London, across mainland Europe in person, and remotely worldwide. Typical lead time is a few weeks; deadline media comment is far faster. Tell me your date and I will confirm availability quickly."
    - q: "What are your fees?"
      a: "Fee on request, and it depends on format, location and audience. Reduced or waived rates for standards bodies, non-profits and academic events; mention your context in the enquiry."
    - q: "What do you need from us on the day?"
      a: "For in-person: a confidence monitor, a slide clicker, and a lav or headset mic. For remote: I present from a studio-quality setup with a backup line. Full AV rider available on request."

# --- Booking / final CTA ----------------------------------------------------
book:
  eyebrow: "Book a keynote"
  headline: "Bring this to your stage."
  lede: "Tell me about your event. The more you share, the faster I can confirm fit, availability and fee."
  cta_label: "Invite me to speak"
  aside_eyebrow: "At a glance"
  aside_title: "Fast, direct, no agency in the middle."
  aside_body: "You deal with me, not a booking desk. That means quicker answers and a talk actually shaped to your room."
  aside_availability: "Currently taking bookings for 2026"
  aside_facts:
    - { k: "Response time", v: "~1 working day" }
    - { k: "Formats", v: "Keynote · Panel · Workshop" }
    - { k: "Languages", v: "English · French" }
    - { k: "Reach", v: "UK · Europe · Remote" }
    - { k: "Media comment", v: "Same-day on deadline" }

final_cta:
  headline: "Ready when your board is."
  lede: "Keynotes, panels and expert comment on payments, post-quantum cryptography and applied AI. In London, across Europe, or remote."
  primary_cta: "Invite me to speak"
  secondary_cta: "Book expert comment"

# Where every "Invite me to speak" / booking CTA points.
booking_url: "/contact/index.html"
---

Sebastien Rousseau is a senior banking technologist focused on the structural
transformation of wholesale payments. Across HSBC Commercial & Investment Bank,
PayPal, Barclays, Shazam, AKQA, and Virgin Group, he has shipped payment
platforms, AI products, and open-source infrastructure used in production by
treasury and payments teams. He authors and maintains pacs.008, pain.001,
BankStatementParser, KyberLib, CloudCDN, and dotfiles, each positioned as a
reference implementation, not a demo: inspectable, board-grade financial
infrastructure.

He contributes to the Emerging Payments Association Asia Quantum-Safe
Cryptography Working Group, co-authored the EPA white paper "Quantum-Safe
Payments: Why the Payments Industry Must Act Now" (September 2025), and publishes
Banking On Quantum and Banking On AI. He works at the intersection of agentic AI,
real-time payments, post-quantum cryptography, cloud-native resilience,
structured data, and regulatory evidence.
