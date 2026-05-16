---
title: "The November 2026 pacs.008 Structured-Address Deadline: A Six-Month View"
subtitle: "From mid-November 2026, SWIFT CBPR+ will reject unstructured postal addresses in pacs.008 and related cross-border payment messages. With approximately 65% of messages still non-compliant, the remediation window is closing fast."
description: "From November 2026, SWIFT CBPR+ requires structured postal addresses in cross-border payment messages. Unstructured address lines (AdrLine alone) will no longer be accepted for key party fields in pacs.008. At minimum, TwnNm and Ctry are required, with StrtNm and BldgNb or PstBx recommended. With six months to go, 65% of payment messages still contain unstructured addresses and 44% of banks remain behind schedule."
date: "May 12, 2026"
language: "ro-RO"
locale: "ro_RO"
banner: "https://cloudcdn.pro/stocks/images/markus-winkler-IrRbSND5EUc-unsplash.webp"
banner_alt: "ISO 20022 pacs.008 structured address diagram — cross-border payment message fields with TwnNm and Ctry highlighted"
keywords: "ISO 20022, pacs.008, SWIFT CBPR+, structured address, November 2026, postal address, TwnNm, Ctry, StrtNm, BldgNb"
---

![ISO 20022 pacs.008 structured address diagram — cross-border payment message fields with TwnNm and Ctry highlighted](https://cloudcdn.pro/stocks/images/markus-winkler-IrRbSND5EUc-unsplash.webp).class="img-fluid clearfix"

---

> **TL;DR.** From November 2026, SWIFT CBPR+ requires structured postal addresses in cross-border payment messages. Unstructured address lines (AdrLine alone) will no longer be accepted for key party fields in pacs.008. At minimum, TwnNm and Ctry are required, with StrtNm and BldgNb or PstBx recommended. With six months to go, 65% of payment messages still contain unstructured addresses and 44% of banks remain behind schedule.
>
> **Concluzii cheie**
>
> - DRAFT translation: this article is a Română stub generated from the English source. Body text is intentionally left in English until a native reviewer signs off.
> - Source title: *The November 2026 pacs.008 Structured-Address Deadline: A Six-Month View*.
> - Source subtitle: *From mid-November 2026, SWIFT CBPR+ will reject unstructured postal addresses in pacs.008 and related cross-border payment messages. With approximately 65% of messages still non-compliant, the remediation window is closing fast.*.
> - Editorial note: replace this block with hand-translated copy before flipping `active=True` for ro in `scripts/_lang_registry.py`.

---

From mid-November 2026, SWIFT CBPR+ will reject unstructured postal addresses in pacs.008 and related cross-border payment messages. With approximately 65% of messages still non-compliant and 44% of banks behind schedule, the remediation window is closing faster than most readiness programmes are designed to handle.

---

> **Key Takeaways**
>
> - From **November 2026**, SWIFT CBPR+ will no longer accept unstructured postal addresses in cross-border payment messages. The change applies to **pacs.008** (customer credit transfer), **pacs.009** (FI credit transfer), **pacs.004** (returns), and **pacs.003** (direct debits), as well as to the upstream **pain.001** flows that feed them.
> - At minimum, **Town Name (TwnNm)** and **Country (Ctry)** must be present in dedicated structured fields. **Street Name (StrtNm)** and either **Building Number (BldgNb)** or **PO Box (PstBx)** are strongly recommended. Free-text address lines (AdrLine) alone will no longer satisfy the requirement for key party fields.
> - The change improves sanctions screening accuracy, reduces manual-repair rates, and protects straight-through processing — but only for institutions that have remediated their upstream customer data, not just their message engines.
> - Industry readiness is uneven. As of March 2026, around **65% of CBPR+ messages still carry unstructured addresses**, **44% of banks** are not on track for the deadline, and **32% of customer address records** remain unstructured on average.
> - Open-source tooling — including **[pacs008](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API")**, a Python library and FastAPI service for generating, validating, and orchestrating pacs.008 message flows — can compress remediation timelines by automating schema validation, address-quality checks, and CI-level enforcement before messages reach the SWIFT network.

---

## A Deadline That Was Always Coming

The November 2026 structured-address requirement is not a sudden regulatory move. It has been on the SWIFT CBPR+ roadmap since the original [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) migration was announced, and it follows the end of MT/MX coexistence in November 2025. What has changed in 2026 is the proximity. With approximately six months remaining, the industry is now operating inside the window where unresolved data-quality issues become operational risk.

The numbers tell the story plainly. SWIFT's own March 2026 community update notes that [approximately 65% of payment messages still contain unstructured addresses ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed"), and that adoption remains uneven across geographies and institution types. A March 2026 [RedCompass Labs survey of 308 senior payments professionals ⧉](https://financialit.net/news/banking/nearly-half-banks-are-behind-iso-20022 "Nearly Half of Banks Are Behind on ISO 20022") found that 44% of banks are not currently on track to meet the structured-address deadline, despite spending an average of $20 million — and in the largest institutions over $30 million — on 2026 readiness, with an average of 13 additional staff assigned to ISO 20022 programmes. The same survey found that 32% of customer address records remain unstructured on average, and that 60% of banks report gaps in core banking systems when supporting structured address fields.

This is not, in other words, a problem that can be solved by another month of message-engine work. It is a data-quality problem that runs upstream from the message layer into onboarding systems, KYC processes, corporate channels, and decades of accumulated free-text customer master data.

## What the Rule Actually Requires

Under the SWIFT CBPR+ Standards Release 2026 (SR2026), the key requirement is straightforward in principle and unforgiving in detail. From mid-November 2026, [Town Name and Country must be provided in their designated structured fields ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed") for all agents and parties in CBPR+ payment messages, with very limited exceptions (statements and notifications in camt.052, camt.053, camt.054, plus a few administrative messages remain outside the strict requirement). For agents, continued use of the BIC alone remains a valid alternative to name-and-address.

Two address formats are permitted after the cutover:

- **Fully structured** — every component of the postal address is mapped to its dedicated ISO 20022 element: StrtNm (Street Name), BldgNb (Building Number) or BldgNm (Building Name), PstCd (Post Code), TwnNm (Town Name), CtrySubDvsn (Country Subdivision), Ctry (Country, as an ISO 3166-1 alpha-2 code). This is the format SWIFT explicitly identifies as the more desirable option where possible.
- **Hybrid** — Town Name and Country are populated in their structured fields, while the remainder of the address may use up to two unstructured AdrLine elements. Importantly, [structured elements must not be repeated inside the unstructured lines ⧉](https://www.statestreet.com/web/insights/articles/documents/state-street-client-guide-to-iso-20022-2025.pdf "State Street Client Guide to ISO 20022 2025"); the address is one or the other for any given component.

Fully unstructured addresses — where the entire address sits inside AdrLine elements with no TwnNm or Ctry — will not be accepted for any of the affected party fields. The European Payments Council has aligned its SEPA rulebook to the same cutover, so from [15 November 2026 the unstructured format is also banned across SCT, SDD, and SCT Inst ⧉](https://clearingpost.com/insights/iso-20022-structured-address-deadline-november-2026/ "The November 2026 Structured Address Deadline: What Every PSP Needs to Do Now"). The alignment is deliberate: SWIFT and the EPC have engineered a single industry cut-over weekend.

For the avoidance of doubt, the [pacs008 documentation lists the affected messages directly ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008"): pacs.008 (debtor and creditor in customer credit transfers), pacs.009 (institution addresses in FI credit transfers and cover payments), pacs.004 (party addresses in returns), and pacs.003 (direct debits). The requirement also flows upstream: corporate pain.001 files carrying unstructured addresses will block compliant pacs.008 generation at the receiving bank.

## Why the Industry Has Made This a Priority

The case for structured addresses is not aesthetic. It is operational, and it shows up in three places.

**Sanctions screening.** The single biggest practical benefit is that structured addresses let screening systems separate party name from location data. Free-text address blocks regularly cause false positives when a town name happens to overlap with a sanctioned-person name token, or when a country embedded in free-text is missed entirely. Structured fields let screening engines apply country-specific risk rules deterministically, and they make it possible to enforce sanctions list matching against the country code rather than guessing at a parsed string. The CGI UK analysis published in March 2026 emphasises this point explicitly: [structured address data is becoming central to operational resilience, not merely a compliance obligation ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement").

**Manual repair rates.** Cross-border payments today carry significant operational cost in the form of manual investigations, exception handling, and repair queues — much of it driven by addresses that screening or routing systems cannot parse with confidence. Banks that have already moved to structured addresses report material reductions in straight-through-processing exceptions, particularly in mid-corridor flows where intermediary agents previously had to interpret free-text data they did not originate.

**Network-level enforcement.** SR2026 hardens validation at the SWIFT network layer. Some of the new checks will operate in non-blocking mode initially — flagging data-quality issues without stopping payments — but the trajectory is clear, and post-cutover, [non-conforming messages will be rejected outright ⧉](https://www.redcompasslabs.com/insights/iso-20022-is-arriving-all-at-once-for-us-banks/ "ISO 20022 is arriving all at once for US banks"). Several US payment rails (Fedwire, CHIPS) and SWIFT CBPR+ are converging on essentially the same timeline, which removes the option of staggered cutover that some institutions had assumed in earlier plans.

## The Field-Level View: What Changes in the Message

The pacs.008 message has carried structured-address support since the early CBPR+ usage guidelines went live in March 2023. What changes in November 2026 is not the schema — it is the validation. Until now, banks have been allowed to populate AdrLine elements with free text and pass that through the network. From the deadline, the contents of the party blocks must satisfy minimum structured-field requirements.

### Required, Recommended, and Retired

| Element | XPath (under `PstlAdr`) | Status after Nov 2026 | Notes |
|---|---|---|---|
| Town Name | `<TwnNm>` | **Mandatory** | At least one structured Town Name per affected party |
| Country | `<Ctry>` | **Mandatory** | ISO 3166-1 alpha-2 code |
| Street Name | `<StrtNm>` | Strongly recommended | Required for fully structured format |
| Building Number | `<BldgNb>` | Recommended | Either BldgNb or PstBx, not both |
| PO Box | `<PstBx>` | Recommended | Alternative to BldgNb |
| Post Code | `<PstCd>` | Recommended | Required by some local schemes |
| Country Subdivision | `<CtrySubDvsn>` | Optional | State, region, province |
| Address Line (free text) | `<AdrLine>` | **Restricted** | Max 2 lines under hybrid; never alongside the same component in structured fields |
| Address Type | `<AdrTp>` | Optional | Use of `ADDR` recommended for postal addresses |

*Source: Synthesis of SWIFT CBPR+ usage guidelines for SR2026 and [pacs008.com structured-address documentation ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008").*

The practical implication is that any institution still relying on AdrLine alone — whether in its own message generation, in pain.001 files received from corporate clients, or in master-data records used to enrich payments in-flight — needs to migrate that data to structured fields before the cutover. SWIFT's in-flow translation service can help in transit, but [it attracts surcharges from January 2026 ⧉](https://www.pcbb.com/products/international-banking/international-payments/iso20022-faq "ISO 20022 FAQ — PCBB") and cannot reliably parse every address format. SWIFT has also released [an open-source AI address-structuring model ⧉](https://www.swift.com/standards/iso-20022/iso-20022-faqs/swift-ai-address-structuring-model "ISO 20022: The Swift AI address structuring model") trained on data from over 200 countries to infer Town and Country from unstructured legacy data with confidence scores, but it is explicitly a remediation aid, not a long-term substitute for clean upstream data.

## How pacs008.com Helps Compress the Timeline

For institutions that need to industrialise their address-quality and message-validation pipelines quickly, [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") provides an MIT-licensed open-source toolkit and FastAPI service designed specifically for the FI-to-FI customer credit transfer workflow. It addresses the three layers where remediation programmes most often stall: data validation, XML generation, and pipeline enforcement.

The toolkit's structured-address capabilities are aligned to the SR2026 requirements:

- **Pre-generation validation** of structured and hybrid postal address fields, so that non-compliant data is caught before any XML is produced or sent.
- **Flagging of unstructured address data** that would fail after the November 2026 deadline, with a clear distinction between hybrid-acceptable and fully unstructured cases.
- **Dual-format support** for both pre-deadline hybrid formats and post-deadline fully structured layouts, allowing institutions to migrate progressively without breaking interoperability with counterparties that have not yet completed their own transitions.
- **CI-pipeline integration** so that address-quality checks become part of the build process, not an end-of-flow afterthought — the practical answer to the [CGI observation that data governance must be a foundational design principle ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement") rather than a compliance overlay.

Beyond addresses, the toolkit covers the broader validation surface that the SR2026 release tightens: JSON Schema validation against 20 message-specific schemas, IBAN format and checksum verification across 75 countries, XSD validation of generated XML against the official ISO 20022 schemas, and version-aware generation across all 13 supported pacs.008 revisions (pacs.008.001.01 through pacs.008.001.13). For operational and compliance teams, it also includes XXE prevention via defusedxml, strict path-traversal protection, and PII masking in structured JSON logs to support GDPR and PCI DSS requirements — the kind of controls that are non-negotiable in production payment flows but are often retrofitted late in vendor-led migrations.

The library is available [on PyPI ⧉](https://pypi.org/project/pacs008/ "pacs008 on PyPI") as a `pip install pacs008` package and on [GitHub ⧉](https://github.com/sebastienrousseau/pacs008 "pacs008 on GitHub") with full source transparency. For institutions evaluating their options, this matters: open-source tooling lets internal teams audit the validation logic, integrate it into existing Python or FastAPI estates without licence negotiations, and contribute fixes back as their own edge cases surface.

It is worth being precise about scope. pacs008 is a message-layer toolkit; it does not replace a payments engine, a screening system, or the customer master-data remediation that an institution still needs to do at source. What it does is take that remediation work and make it enforceable — turning structured-address compliance from a manual review at the end of a long pipeline into an automated gate at the point of generation. For programmes running short on time, that gate is the difference between a clean cutover and a post-cutover surge in rejections.

## The Tooling Landscape

pacs008 sits within a wider ecosystem of ISO 20022 message tooling, and the choice of approach depends on the institution's stack, scale, and migration philosophy. The open-source and commercial landscape includes [pyiso20022 ⧉](https://github.com/phoughton/pyiso20022 "pyiso20022 — an ISO 20022 message generator and parser") (broad multi-category Python library with beta validation), the related [pain001 ⧉](https://pain001.com/ "Pain001 — Automate ISO 20022-compliant payment file creation") library for upstream payment initiation, [Prowide ISO 20022 ⧉](https://www.prowidesoftware.com/development-tools/iso20022 "Prowide ISO 20022 — open source MX message parser for Java") (a comprehensive Apache 2.0 Java library with a commercial layer for CBPR+ validation and translations), and a number of commercial platforms — Mambu, Kyriba, PaymentComponents, and others — that bundle ISO 20022 capability into broader treasury or payments-platform offerings.

The trade-off is familiar. Commercial platforms reduce in-house engineering burden but bind the institution to a vendor roadmap that may not match its own. Comprehensive multi-category libraries cover a wider surface but require more integration work for any single message type. Focused open-source libraries — pacs008 for FI-to-FI customer credit transfer, [pain001](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) for payment initiation — minimise integration time for institutions that need to address specific bottlenecks quickly, and they leave the institution in control of its own validation rules. For the structured-address problem in particular, a focused approach has the advantage that the rules being enforced are narrow, well-defined, and unlikely to change before the cutover.

## What This Means by Sector

The November 2026 deadline does not affect all institutions equally. The right response depends on the volume of cross-border traffic, the maturity of the existing data estate, and the role the institution plays in the payment chain.

### Large Correspondent and Cross-Border Banks

For tier-one banks running significant CBPR+ traffic, the structured-address requirement is one workstream within a much larger SR2026 readiness programme that also covers exceptions and investigations, BAH hardening, and (in the US) the simultaneous migration of Fedwire and CHIPS. The RedCompass Labs data suggests most of these institutions are spending $20–30 million on 2026 readiness, with delivery teams of 10–20 specialists. The risk for this group is not technical capability — it is delivery capacity. With multiple parallel workstreams competing for the same release windows, address-quality remediation can quietly slip behind more visible workstreams until it becomes a cutover-week problem. The practical mitigation is to bring address validation forward in the pipeline, so that failures surface in development and test environments months before they would have reached production.

### Mid-Tier Banks and Payment Institutions

For mid-tier banks and EMI/PI institutions, the structured-address requirement is often the most material 2026 obligation they face, because they do not carry the same surrounding workstream load as the tier-ones. The challenge here is usually upstream data quality. Customer onboarding processes that have captured addresses as free-text for decades produce master-data estates that are not straightforwardly parseable. Automated remediation — using SWIFT's open-source address-structuring model, commercial address-cleansing services, or a combination — can address a substantial share of records, but a residual long tail of complex international addresses will require manual review. The earlier this work starts, the smaller that tail becomes.

### Corporates and Payment Service Providers

Corporates initiating payments via pain.001 are upstream of the bank's pacs.008 generation but are not exempt from the structured-address requirement. Banks will not retroactively populate beneficiary addresses on behalf of corporate clients; the structured data must originate from the corporate's own systems. For corporate treasurers, this means ensuring that ERP and treasury systems capture beneficiary addresses in structured form, that signatory and ultimate-debtor information is similarly structured, and that payment-initiation templates do not silently drop fields during file generation. Pre-flight validation of pain.001 files — using either the corporate's own tooling or services exposed by the bank — is becoming the practical control point.

### Vendors, Fintechs, and System Integrators

For vendors building on top of payment rails, the deadline is a forcing function for ISO 20022 capability that may have been pushed to later phases. Fintechs that route or originate cross-border payments through banking partners need to surface structured-address capture in their own UIs and APIs, or accept that compliant pain.001 files cannot be produced from their data. The opportunity, for vendors that can move quickly, is to absorb the remediation burden on behalf of corporate clients — turning a compliance problem into a service.

## Conclusion

The November 2026 structured-address deadline is, in one sense, a narrow change: two mandatory fields, a couple of recommended ones, and the retirement of a free-text option that should never have been used for sanctions-relevant data in the first place. In another sense, it is the most operationally significant ISO 20022 milestone since the original CBPR+ migration, because it forces structured data not just into the message layer but into the upstream systems that feed it.

The industry-level readiness picture, six months out, is not encouraging. Two-thirds of CBPR+ messages still carry unstructured addresses. Nearly half of banks are not on track. Almost a third of customer address records remain unparseable. The funding is in place — the surveys consistently show eight- and nine-figure investments — but the work is not, and the data-quality dimension of the problem cannot be solved by spending alone in the final months.

What helps now is automation at the point of validation: pushing the rules into pipelines that catch problems before they reach the network, rather than after. For institutions running Python or FastAPI estates, open-source tooling like [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") provides a practical way to make that shift without a vendor selection cycle. For everyone, regardless of stack, the strategic point is the same: the institutions that industrialise change now will be in a far stronger position than those relying on last-minute compliance — to borrow the phrasing of the RedCompass Labs research that has framed much of the 2026 conversation.

The cutover weekend in November will close one chapter. The institutions that arrive at it with clean data, automated validation, and a working understanding of what structured addresses actually do for sanctions screening will spend that weekend monitoring traffic. The ones that arrive without those things will spend it on the phones.

## Frequently Asked Questions

**What exactly changes on the November 2026 deadline?**

From mid-November 2026, SWIFT CBPR+ will reject pacs.008, pacs.009, pacs.004, and pacs.003 messages whose party fields contain unstructured-only postal addresses. The minimum structured requirement is the Town Name in the TwnNm element and Country in the Ctry element (using the ISO 3166-1 alpha-2 code). Hybrid addresses are still permitted — Town and Country in structured fields, plus up to two free-text AdrLine elements for the remaining components — but the same component cannot appear in both structured and unstructured fields. Fully structured addresses are the preferred format. The European Payments Council has aligned the SEPA schemes (SCT, SDD, SCT Inst) to the same cutover date.

**Which messages and which party fields are affected?**

For pacs.008, the requirement applies to debtor and creditor postal addresses. For pacs.009, it applies to institution addresses in FI credit transfers and cover payments. For pacs.004, it applies to party addresses in payment returns. For pacs.003, it applies to creditor and debtor addresses in customer direct debits. Statement and notification messages (camt.052, camt.053, camt.054) and certain administrative messages remain outside the strict requirement. Upstream pain.001 messages from corporate clients are not directly governed by CBPR+, but unstructured addresses in pain.001 files will block compliant pacs.008 generation downstream and so are effectively in scope.

**What is the difference between structured, hybrid, and unstructured addresses?**

A fully structured address maps every component to its dedicated ISO 20022 element: StrtNm, BldgNb or PstBx, PstCd, TwnNm, CtrySubDvsn, Ctry. A hybrid address has Town Name and Country in structured fields, with the rest of the address in up to two free-text AdrLine elements; the same component must not appear in both. An unstructured address has the entire postal address in AdrLine elements with no structured TwnNm or Ctry — this is the format being retired in November 2026 for the affected party fields.

**How does pacs008.com help with this transition?**

The [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") library validates structured and hybrid postal address fields before XML generation, flags unstructured data that would fail after the deadline, supports both pre-deadline hybrid and post-deadline fully structured formats, and integrates into CI pipelines and batch validation workflows. It generates XML for all 13 supported pacs.008 versions, validates against the official ISO 20022 XSD schemas, and exposes a FastAPI service for automated orchestration. It is open source under an MIT-style licence, available on PyPI, and designed specifically for FI-to-FI customer credit transfer workflows — so the validation rules are calibrated to the SR2026 CBPR+ usage guidelines rather than abstracted across many message types.

**What happens if my institution is not ready by November 2026?**

Messages with unstructured addresses in the affected party fields will be rejected at the network level after the cutover. Practically, this translates into payment failures, increased exception volumes, manual repair surges, and probable customer impact. SWIFT's in-flow translation service is available for some transitional cases but attracts surcharges from January 2026 and cannot reliably parse every address format. SWIFT has also released an open-source AI address-structuring model that infers Town and Country from legacy unstructured data, but it is designed for remediation and pre-processing, not as a permanent substitute for clean upstream data. Institutions that arrive at the deadline without a remediated customer master-data estate and an automated validation pipeline should expect a difficult cutover week and a meaningful operational uplift in the months that follow.

## References

- Sebastien Rousseau, (2023). [Automating ISO 20022-Compliant Payment File Creation with Pain001](https://sebastienrousseau.com/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html "Automating ISO 20022-Compliant Payment File Creation with Pain001").
- pacs008, (2026). [November 2026 structured-address deadline ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008"). pacs008.com.
- pacs008, (2026). [pacs008 — ISO 20022 pacs.008 Toolkit and API ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API"). pacs008.com.
- SWIFT, (2026). [ISO 20022 milestone for November 2026: Unstructured addresses to be removed ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed"). SWIFT.
- SWIFT, (2026). [ISO 20022 for Financial Institutions ⧉](https://www.swift.com/standards/iso-20022/iso-20022-financial-institutions-focus-payments-instructions "ISO 20022 for Financial Institutions"). SWIFT.
- SWIFT, (2026). [The Swift AI address structuring model ⧉](https://www.swift.com/standards/iso-20022/iso-20022-faqs/swift-ai-address-structuring-model "ISO 20022: The Swift AI address structuring model"). SWIFT.
- RedCompass Labs, (2026). [Nearly Half of Banks Are Behind on ISO 20022 ⧉](https://financialit.net/news/banking/nearly-half-banks-are-behind-iso-20022 "Nearly Half of Banks Are Behind on ISO 20022"). Financial IT.
- RedCompass Labs, (2026). [ISO 20022 is arriving all at once for US banks ⧉](https://www.redcompasslabs.com/insights/iso-20022-is-arriving-all-at-once-for-us-banks/ "ISO 20022 is arriving all at once for US banks"). RedCompass Labs.
- ClearingPost, (2026). [The November 2026 Structured Address Deadline: What Every PSP Needs to Do Now ⧉](https://clearingpost.com/insights/iso-20022-structured-address-deadline-november-2026/ "The November 2026 Structured Address Deadline"). ClearingPost.
- CGI UK, (2026). [2026: A defining year for ISO 20022 and structured data enforcement ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement"). CGI UK.
- J.P. Morgan, (2026). [ISO 20022 Migration: Guidance, Messaging & More ⧉](https://www.jpmorgan.com/insights/payments/fx-cross-border/iso-20022-migration "ISO 20022 Migration: Guidance, Messaging & More"). J.P. Morgan.
- ING, (2026). [FAQ Swift ISO 20022 ⧉](https://www.ingwb.com/en/service/payments-and-collections/swift-iso20022/faq-swift-iso-20022 "FAQ Swift ISO 20022 — ING"). ING Wholesale Banking.
- Mambu, (2026). [CBPR+ is live: what ISO 20022 means in practice ⧉](https://mambu.com/en/insights/articles/cbpr-is-live-what-iso-20022-means-in-practice "CBPR+ is live: what ISO 20022 means in practice"). Mambu.
- Kyriba, (2026). [ISO 20022 migration: what every treasury team needs to know about what's next ⧉](https://www.kyriba.com/blog/iso-20022-corporate-treasury-2026/ "ISO 20022 migration: what every treasury team needs to know about what's next"). Kyriba.
- Standard Chartered, (2025). [ISO 20022 – Standard Chartered Address Guidelines (H2H and API) ⧉](https://www.sc.com/en/uploads/sites/66/content/docs/sc-cib-tb-ISO-20022%E2%80%93CBPR-Address-guidelines-H2H-and-API-sept-2025.pdf "Standard Chartered ISO 20022 Address Guidelines"). Standard Chartered.
- State Street, (2025). [Client Guide to ISO 20022 ⧉](https://www.statestreet.com/web/insights/articles/documents/state-street-client-guide-to-iso-20022-2025.pdf "State Street Client Guide to ISO 20022 2025"). State Street.
- ISO 20022, (2026). [Message Definitions Catalogue ⧉](https://www.iso20022.org/iso-20022-message-definitions "ISO 20022 Message Definitions"). ISO 20022.

<!-- enrich-start -->
<aside class="author-card" aria-label="About the author"><img alt="Portrait of Sebastien Rousseau" src="https://cloudcdn.pro/stocks/images/sebastien-rousseau.png" width="64" height="64" loading="lazy" decoding="async" /><span class="author-card-body"><strong class="author-card-name"><a href="/about/index.html">Sebastien Rousseau</a></strong><span class="author-card-bio">Senior banking technologist writing on applied AI, ISO 20022 migration, post-quantum cryptography for financial services, and the structural transformation of wholesale payments.</span><span class="author-credentials">20+ years across HSBC Commercial &amp; Investment Bank, PayPal, Barclays, Shazam, AKQA, Virgin Group. <a href="/about/index.html">Full profile</a> &middot; <a href="https://www.linkedin.com/in/sebastienrousseau/" rel="external noopener">LinkedIn</a> &middot; <a href="https://github.com/sebastienrousseau" rel="external noopener">GitHub</a></span></span></aside>
<p class="post-reviewed">Last reviewed <time datetime="2026-05-15">2026-05-15</time>.</p>
<aside class="related-posts" aria-labelledby="related-heading">
<h2 id="related-heading" class="related-heading">Related reading</h2>
<div class="related-grid">
<article class="related-card"><a href="https://sebastienrousseau.com/2025-09-01-quantum-safe-payments-epaa" class="related-media" aria-label="Quantum-Safe Payments: Why the Industry Must Act Now" tabindex="-1"><img alt="Quantum computing circuit board in blue light" src="https://cloudcdn.pro/stocks/images/digital-nodes.webp" loading="lazy" decoding="async" width="600" height="400" /></a><footer class="related-body"><h3><a href="https://sebastienrousseau.com/2025-09-01-quantum-safe-payments-epaa">Quantum-Safe Payments: Why the Industry Must Act Now</a></h3><p><time datetime="2025-09-01">2025-09-01</time></p></footer></article>
<article class="related-card"><a href="https://sebastienrousseau.com/2023-10-09-shokunin-the-fastest-rust-based-static-site-generator/index.html" class="related-media" aria-label="Static Site Generator: Fastest Rust-Based SSG" tabindex="-1"><img alt="Turned off laptop computer on top of a white table with a glass of water on the left and a pen, notepad and plant on the right" src="https://cloudcdn.pro/stocks/images/anna-nekrashevich-8534387.webp" loading="lazy" decoding="async" width="600" height="400" /></a><footer class="related-body"><h3><a href="https://sebastienrousseau.com/2023-10-09-shokunin-the-fastest-rust-based-static-site-generator/index.html">Static Site Generator: Fastest Rust-Based SSG</a></h3><p><time datetime="2023-10-09">2023-10-09</time></p></footer></article>
<article class="related-card"><a href="https://sebastienrousseau.com/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html" class="related-media" aria-label="Automating ISO 20022 Payment Files Creation with Pain001" tabindex="-1"><img alt="Turned off laptop computer on top of brown wooden table" src="https://cloudcdn.pro/stocks/images/andrea-de-santis-T3Qen8vVgRc.webp" loading="lazy" decoding="async" width="600" height="400" /></a><footer class="related-body"><h3><a href="https://sebastienrousseau.com/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html">Automating ISO 20022 Payment Files Creation with Pain001</a></h3><p><time datetime="2023-09-29">2023-09-29</time></p></footer></article>
</div>
</aside>
<!-- enrich-end -->
