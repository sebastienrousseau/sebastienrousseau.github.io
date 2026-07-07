# Institutional Brand Pivot & Web-Quality Plan — 2026

**Site:** sebastienrousseau.com
**Author of record:** Sebastien Rousseau
**Status:** Draft for review
**Created:** 2026-07-07
**Scope:** Close the delta between the current site (already ~80% of an "institutional-grade" brief) and a state that (a) reads to banking CFOs/COOs/CTOs, not only engineers, and (b) holds a defensible 100/100 Lighthouse + WCAG 2.2 AA + Google-News posture. Companion to `improvement-plan-2026.md` (platform 10/10) and `web-performance-seo-spec.md` (the perf/SEO code guide).

> **Framing.** A generic "2026 institutional blueprint" was the input. Most of it is **already built here** — case studies with regulatory framing (DORA, SR 11-7, FCA/PRA), a Boards/Engineers/Regulators audience lens, `ProfilePage`+`Person`+`Organization`+`NewsArticle` schema, a `news:news` sitemap on the 48 h freshness rule, CSP-strict + SRI + SBOM + SLSA + Scorecard, real-world Lighthouse **0.97** (FCP 0.6 s, LCP 1.2 s, TBT 0, CLS 0). This plan therefore does **not** rebuild any of that. It fixes a short list of **real, verified defects** and wires up **data that already exists but isn't rendered**.

---

## 0. Two honesty constraints (read first)

These override any instruction to "add ROI numbers" or "move to FINOS."

- **No fabricated ROI.** The brief asks for lines like *"reduced cross-border settlement failures by 12%"* and *"saved Treasury teams 40 hours/week."* We do **not** have those measurements, and `_data/proof/case-studies/*.yml` already encodes the rule *"Never fabricate adopter counts."* Inventing percentages is the single fastest way to lose a Tier-1 risk/compliance reader — the exact audience we want. **Rule:** quantify only what is externally verifiable (downloads, XSD-validation coverage, ISO-7064 checksums, EPAA citation). Everything else is framed as *mechanism → outcome* ("pre-flight XSD validation → payment errors caught before they reach the clearing network"), not a fake number. Where an illustrative figure genuinely helps, label it *"illustrative model"* with its assumptions.
- **FINOS/Linux Foundation is an org action, not a code change.** Donating `pain001`/`KyberLib` to a foundation is a real multi-month governance process (IP assignment, HSBC employer sign-off, foundation acceptance). We can't "ship" it. What we *can* ship is the **enterprise-trust evidence** that closes the bus-factor objection today: the projects are already Apache-2.0 / MIT, SBOM-attested, Sigstore-signed, Scorecard-scored. Section 1C surfaces that. Treat "FINOS donation" as a roadmap intent to *state*, not a claim to *assert*.

---

## 1. Strategic content — surface what already exists

### 1A. Business-value translation — mostly done; finish the project cards
**State:** `/case-studies/` is live (`pain001`, `kyberlib`, `hsbc-treasury-apis`, `bankstatementparser`, `cloudcdn`) with problem → what-I-built → rigour → validation, regulatory framing, and NDA-safe copy. Case studies are the strong asset. **Gap:** the `/projects/` cards still lead with tech/features and **don't link to the matching case study**.

**Fix (content, `_posts/projects*.md`):**
- Add a "Business impact" line to each flagship project card, mechanism-framed (no invented %):
  - *pain001* — "Removes the proprietary translator between your ERP and the clearing network. Every message XSD-validated and IBAN/BIC/LEI-checksummed pre-flight, so malformed payments are caught before submission — auditable, Apache-2.0, no vendor lock-in."
  - *KyberLib* — "ML-KEM (FIPS 203) you can pilot against harvest-now-decrypt-later today, evaluated by Qtonic Quantum Lab — a migration you can start per-service instead of a core rebuild."
- Add `Read the case study →` link from each flagship card to `/case-studies/<slug>/`.

**Acceptance:** every flagship project card has a mechanism→outcome line and a case-study link; `test_no_fabricated_metrics` (new, §5) passes.

### 1B. Thought-leadership / speaker hub — build `/speaking/` (data already exists)
**State:** `_data/proof/speaking.yml` is **complete** — short/medium/long bios, outcome-framed topics (PQC migration, FIPS 203), EPAA credentials — and **nothing renders it.** `recognition.yml`, `testimonials.yml` also unrendered. There is **no `/speaking/` page and no generator.**

**Fix (new generator, mirrors `build_case_studies.py`):**
- `scripts/generators/build_speaking.py` → renders `public/speaking/index.html` from `speaking.yml`: bio (3 lengths, copy-to-clipboard), topics as talk cards, a downloadable media-kit link, and a "Book / invite" CTA to `/contact/`. Positions for Money20/20 · SIBOS · SWIFT summits explicitly in the intro copy.
- Emit `Event`/`EventSeries` + `subjectOf` JSON-LD hanging off `#person` (schema hook in `schemas.py`).
- Add `Speaking` to primary nav (`_layouts/*.html`) and footer "Work" column.
- Register in `build.sh` after `build_case_studies.py`; add i18n stubs per the 28-locale gate.

**Acceptance:** `/speaking/` builds, validates (JSON-LD gate), is linked from nav, and passes i18n parity.

### 1C. Enterprise Governance & Trust — build `/trust/`
**State:** `recognition.yml` (EPAA paper, working-group membership, features) exists; the platform already produces `sbom.cdx.json`, SLSA provenance, Sigstore bundles, OpenSSF Scorecard — but there is **no page that assembles them into a buyer-facing trust story.** Compliance/vendor-risk readers currently have to infer it.

**Fix (new generator):**
- `scripts/generators/build_trust.py` → `public/trust/index.html` with four blocks:
  1. **Provenance** — SBOM (link `/sbom.cdx.json`), SLSA attestation (`gh attestation verify` one-liner), Sigstore-signed articles, Scorecard badge.
  2. **Licensing** — Apache-2.0 / MIT table per project; "free to fork, audit, and self-host."
  3. **Governance & bus-factor** — honest single-maintainer statement **plus** the mitigations (open source, reproducible builds, signed releases) **plus** the stated intent to pursue foundation stewardship (FINOS/LF) for the payments libraries. Do not assert a donation that hasn't happened.
  4. **Recognition** — render `recognition.yml` (verifiable, dated, linked).
- Link from footer + `/about/#trust`.

**Acceptance:** `/trust/` builds and validates; every recognition item resolves to a live, dated external URL (extend `audit_links.py`).

### 1D. Single-source the KPI numbers (credibility bug)
**State — real inconsistency:** the same three metrics disagree across pages.

| Metric | Home (`_posts/index.md`) | Projects | About | Source of truth `metrics.json` |
|---|---|---|---|---|
| Downloads | 37.1M | 37.3M | 37M | **37,316,388 (37.3M)** |
| GitHub stars | 663 | 664 | — | **664** |
| Signed articles | 84 | 88 | 73 | **88** |

Hand-maintained literals drift. For an institutional reader, three different numbers for the same fact reads as sloppy.

**Fix:** a postbuild pass injects the KPI values from `_data/proof/metrics.json` (already the fetched source of truth) into `data-kpi="downloads|stars|articles|years"` spans, replacing the hardcoded strings on home/projects/about. One number, one source, updated at build.

**Acceptance:** `grep` for hardcoded `37.1M|37.3M|663|84` in `_posts/*.md` returns 0; a guard test asserts KPI spans carry `data-kpi` and match `metrics.json`.

### 1E. Job-title / positioning drift
**State:** `Person.jobTitle` (schema) = **"Senior Product Manager"**; `about.md` = **"Senior payments leader"**; `speaking.yml` = **"senior banking technologist."** Pick one canonical title and propagate.
**Fix:** set the canonical string once (recommend *"Senior Banking Technologist — Wholesale Payments, HSBC CIB"* for the exec audience) in the identity graph and reference it everywhere.

### 1F. Portfolio focus
General-purpose Rust utilities (`DTT`, `VRD`, `CMN`, `LibMake`, `RustLogs`, `dotfiles`) dilute the banking narrative on `/projects/`. **Fix (content):** move them under a collapsed "Developer platform & tooling" section; keep Payments / Post-Quantum / Applied-AI as the three headline pillars above the fold.

---

## 2. Performance — already 0.97; close the CI gap and take the marginal wins
**State (verified):** real-world perf 0.97, CWV green and hard-gated (LCP/CLS/TBT `error` in `lighthouserc.json`). The CI "0.76" is a **measurement artifact** — `lhci`'s `staticDistDir` server ships no gzip/immutable-cache, unlike Cloudflare (documented in ADR-0006). So "100/100" is largely a *measurement* problem, not a *site* problem.

- **2.1 (P1) Make the CI score trustworthy.** Serve the Lighthouse run through a gzip + `Cache-Control: immutable` static server (or point `lhci collect` at a `wrangler dev` / Cloudflare preview) so the category can be promoted from `warn` to `error ≥0.98`. This is the single highest-leverage perf item — it converts an artifact into a real gate.
- **2.2 (P2) Critical-CSS inline.** Today two render-blocking stylesheets load (`/_csp/*.css` ~132 KB + page CSS). Add a postbuild critical-CSS pass (inline ~8–10 KB above-the-fold, `preload`+`onload` swap the rest) per `web-performance-seo-spec.md` §1A — which already documents the exact pattern but isn't wired. Marginal (~130 ms render-block) given LCP is already 1.2 s.
- **2.3 (P2) Responsive images.** Built pages ship a single fixed-width WebP, **no `srcset`/`<picture>`, no AVIF**. `postbuild_assets.py::wrap_cdn_images_in_transform()` exists but **is not applied to shipped output** (the transform pass postdates the committed build). Finish it: emit AVIF+WebP `srcset` via the CDN `/api/transform` endpoint with `width`/`height` retained (CLS already safe).
- **2.4 (P2) INP is unmeasured** — `interaction-to-next-paint` is `"off"` in `lighthouserc.json`. Turn it on as `warn` first. The interactive surfaces (audience lens, theme toggle, search, scorecards) are light; likely already green, but it should be watched, not off.
- **Non-issue:** no in-repo Brotli/gzip config — that's correct; Cloudflare negotiates Brotli at the edge. Don't add an `_headers` file for it.

---

## 3. Accessibility — strong base; six concrete WCAG 2.2 fixes
**State:** skip link, site-wide `:focus-visible`, full ARIA search dialog with `aria-live`, theme toggle with synced `aria-pressed`, language menu with `aria-expanded`/`role=menu`, all `img` have `alt`, per-locale `lang`+`dir="rtl"`, reduced-motion + prefers-contrast, AAA-annotated colour tokens. Genuinely good. The findings are small:

- **3.1 (P1) Heading-order skip on articles.** DOM order is `H1 → H3×8 (cite/share popover) → H2×5`. The cite-popover format labels ("Format for Medium", "BibTeX", …) are `H3` and appear before the first `H2` → **WCAG 1.3.1 / 2.4.10 smell.** Fix: demote those popover labels to non-heading (`<p class="...">` or `role="presentation"`), or move the popover after `<main>` in DOM. (`_layouts/report.html` + the sharing component in `postbuild_lib/sharing.py`.)
- **3.2 (P1) Hamburger has no `aria-expanded`.** The checkbox-hack toggle exposes state only via `:checked`. Add `aria-expanded` sync (tiny JS in `main.js`, or an `aria-controls` pattern on the `<label>`).
- **3.3 (P2) No `<article>` landmark** on dated posts; wrap the post body in `<article>` (`report.html`).
- **3.4 (P2) `<main aria-label="main">` is redundant** on non-home layouts — drop the label (the landmark role is implicit).
- **3.5 (P2) H1 sits outside `<main>`; skip target `#main` lands after the H1.** Either move the hero H1 inside `<main>`, or point the skip link at the hero. Low severity but trivially correct.
- **3.6 (P3) Banner `<figure>` has no `<figcaption>`; forms have no `<fieldset>/<legend>`.** Add a visually-hidden `<figcaption>` from `banner_alt`; wrap contact fields in a `<fieldset><legend class="visually-hidden">`.

Note: accessibility is **already `error ≥1.00`** in CI, so these are AA/AAA polish, not gate failures — but 3.1 is the kind of thing WAVE/axe flags.

---

## 4. SEO / schema — three real defects to fix
The schema graph is excellent (`ProfilePage`/`Person`/`Organization`/`WebSite`/`BlogPosting`/`BreadcrumbList`/`NewsArticle`-when-fresh/`TechArticle`/`ScholarlyArticle`/FAQ/`SpeakableSpecification`). The `news:news` sitemap is correct and the empty root file is correct-by-design (48 h window; newest post is >48 h old). The defects:

- **4.1 (P0) `meta description` / `og:description` / `twitter:description` are corrupted site-wide.** They contain **double-escaped article-body HTML** — e.g. `&amp;lt;div lang=&amp;quot;en&amp;quot;&amp;gt;&amp;lt;h1&amp;gt;…` — instead of a clean summary. The SSG derives the description by scraping the rendered body first block; the clean summary already exists in the `BlogPosting.description` JSON-LD. **This is the top priority:** it's the string that renders when an executive shares your link on LinkedIn/Slack from their phone at a summit — the brief's core scenario — and it currently renders as garbage.
  **Fix (postbuild, `postbuild_lib/seo.py`):** add a pass that reads the clean `BlogPosting.description` (or front-matter `description`) and rewrites the three meta tags with a properly-escaped, ≤160-char summary. Add `tests/validation/test_meta_description_clean.py` asserting no `&lt;`/`&amp;lt;`/`<` in any `description`/`og:description`/`twitter:description` across `public/`. **Make it a blocking gate.**
- **4.2 (P1) Canonicalisation is inconsistent — three URL forms per page.** `rel="canonical"` = `…/slug/index.html`; `og:url` = `…/slug`; sitemap `<loc>` = `…/slug/`. Pick the trailing-slash form as canonical everywhere. Fix in `seo.py` (normalise the canonical tag to strip `index.html` → `/`, matching `_page_canonical_url` which already does this for home only). Also collapse the duplicate `hreflang="en"` (one bare-domain, one trailing-slash) on the homepage.
- **4.3 (P1) `og:type` is `website` on dated posts** (should be `article`), and **publisher entity is inconsistent** — `BlogPosting.publisher` → `#person` while `NewsArticle`/`TechArticle.publisher` → `#organization`. For Google News, `publisher` should consistently be the `Organization`. Fix both in `report.html` + `schemas.py`. Also align `dateModified`: JSON-LD uses `last_reviewed` (bare date) while the head `itemprop=dateModified` uses `last_build_date` — emit one ISO-8601 value.
- **Google News editorial checklist (already satisfied — verify, don't rebuild):** author byline + `/about/` editor bio, visible publication dates, `editorialPolicy`/`correctionsPolicy` on the Organization, clean article HTML. Confirm these survive after 4.1/4.3.

---

## 5. Guards (so fixes don't regress)
Add to the `tests/validation/` gate (already blocking in `build.sh`):
- `test_meta_description_clean.py` — no HTML/entities in any description meta (4.1).
- `test_canonical_consistency.py` — `canonical` == `og:url` == sitemap `<loc>` per page (4.2).
- `test_kpi_single_source.py` — KPI spans match `metrics.json` (1D).
- `test_no_fabricated_metrics.py` — case-study/project copy carries no bare `\d+%` without an `illustrative`/`source` annotation (0 / 1A).

---

## 6. Sequencing

```
P0  4.1 description corruption ................... 0.5 d  (ship first — visible everywhere)
P1  1D KPI single-source ........................ 0.5 d
    1E title drift ............................... 0.25 d
    4.2 canonical consistency ................... 0.5 d
    4.3 og:type/publisher/dateModified .......... 0.5 d
    3.1 heading-order  · 3.2 aria-expanded ...... 0.5 d
    2.1 trustworthy Lighthouse CI gate .......... 1 d
P1  1B /speaking/ page (data exists) ............ 1.5 d
    1C /trust/ page ............................. 1.5 d
P2  1A project cards + case-study links ......... 1 d
    1F portfolio focus .......................... 0.5 d
    2.2 critical-CSS · 2.3 srcset/AVIF · 2.4 INP  2 d
    3.3–3.6 a11y polish ......................... 1 d
```
Total ≈ 12–13 engineering days, ~6 PRs. P0+P1 (the defects + the two missing pages) is the ~7-day core that moves the needle for the institutional audience.

## 7. Definition of done
- No corrupted description meta anywhere (gated). One canonical URL form per page (gated). `og:type=article` + Organization publisher on posts.
- One KPI source (`metrics.json`), one job title, across home/projects/about.
- `/speaking/` and `/trust/` live, linked, i18n-parity-clean, schema-valid.
- Lighthouse perf promotable to `error ≥0.98` on a gzip+cache CI server; INP watched.
- Article heading order linear; hamburger exposes `aria-expanded`.
- Zero fabricated ROI numbers; foundation stewardship stated as intent, not claim.

## Files this plan touches
- Content: `_posts/index.md`, `_posts/projects*.md`, `_posts/about.md`, `_data/proof/{metrics,speaking,recognition}.*`
- Generators: **new** `scripts/generators/build_speaking.py`, **new** `build_trust.py`; `build.sh` registration
- Postbuild: `scripts/postbuild/postbuild_lib/seo.py` (description, canonical, KPI), `schemas.py` (og:type, publisher, Event), `sharing.py` (heading order), `postbuild_assets.py` (srcset/AVIF, critical-CSS)
- Layouts: `_layouts/report.html`, `_layouts/*.html` (nav, `<article>`, `<main>` label), `_layouts/main.js` (aria-expanded)
- CI: `lighthouserc.json` (INP, promote perf gate), **new** `tests/validation/test_*` guards
