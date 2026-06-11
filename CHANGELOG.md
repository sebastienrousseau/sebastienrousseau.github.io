<!-- SPDX-License-Identifier: Apache-2.0 -->

# Changelog

All notable changes to this repository — schema, build pipeline, security, accessibility, and crawler-facing surface — are recorded here.

This site follows [Semantic Versioning](https://semver.org/) for the **build pipeline + schema graph**; content (articles, translations) lands continuously between tags and isn't versioned here. Editorial revision history per article lives in each post's `last_reviewed` frontmatter field.

The format is loosely based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [1.2.0] — 2026-06-02

Phase 1 Week 3 + Google News readiness + template hygiene.

### Added

- **`NewsArticle` JSON-LD on fresh posts ([#165])** — `inject_news_article` in `schemas.py` reshapes the existing `BlogPosting` graph into a Google-News-spec-compliant `NewsArticle` node (with `author` / `publisher` refs to `#person` / `#organization`, `speakable`, image, article section) on posts within 48 hours of `datePublished`. Stale posts stay indexed via `TechArticle` / `ScholarlyArticle` / `BlogPosting`. New `NEWS_FRESHNESS_HOURS = 48` constant. Liberal ISO 8601 parser handles `+HH:MM` offsets, `Z` suffix, bare `YYYY-MM-DD` (stamped UTC).
- **Editorial standards page ([#163])** — new `/editorial/` page with full `EditorialPolicy` + `CorrectionsPolicy` JSON-LD. Sections: sourcing (5-tier primary-source hierarchy), 48-hour corrections clause (IFCN-aligned), AI assistance disclosure (Claude + Copilot — explicit boundary on claim verification / source citation / author voice), conflict-of-interest disclosure (HSBC employment, past employers, no paid placements), CC BY-4.0 republication terms, accountability table with sigstore verification command. The single highest-leverage Google News reviewer signal the site was missing.
- **`Organization` graph extended with policy refs ([#163])** — `editorialPolicy` / `correctionsPolicy` / `ethicsPolicy` / `diversityPolicy` properties added to the `#organization` node across all 11 layouts. All four point at `/editorial/` (corrections has its own anchor). These are the `NewsMediaOrganization` fields Google News reviewers and Article Search Result enhancers look for.
- **Named typography abstraction layer ([#162])** — three CSS custom properties in every layout's `:root`: `--type-display` (display / headings), `--type-body` (body / nav / UI), `--type-mono` (code). Values are system-font stacks for now; the abstraction lets a follow-up swap in self-hosted Inter + Newsreader + JetBrains Mono with size-adjust fallback metrics in three lines per layout without touching any other CSS.
- **`/about/` ORCID iD published** — `0009-0005-1434-284X` replaces the `Pending registration` placeholder, and is also surfaced in the editorial page's accountability table.

### Fixed

- **Idempotent TOC injection ([#166])** — `inject_anchor_links_and_toc` was non-idempotent. Every rerun on already-processed HTML re-anchored existing H2s (extracting the prior `#` as part of the heading text) and appended a fresh `<aside class="article-toc">`. Today's article had **5 stacked TOCs and 5 anchor links per H2**; every H2 in the TOC ended ` # # # #`. The whole deployed back catalogue carried the same artefacts. Top-of-function guard now returns html unchanged when `class="article-toc"` or `class="heading-anchor"` is already present inside `<main>`. Defensive `_HEADING_ANCHOR_RE` also strips prior anchor markup from inner content so narrow regression paths (hand-crafted partial state in tests) still degrade safely.
- **Duplicate `<h1>` on every article page ([#166])** — every dated article had two `<h1>` tags with identical text: one from the layout's hero band, one from the markdown body's `# Title`. WCAG 1.3.1 / 2.4.6 violation + structural noise. New `strip_duplicate_body_h1` postbuild pass removes the first H1 inside `<main>` when its text matches the hero H1. `check_voice` still requires exactly one H1 in the markdown source.

### Verification

- 388 / 388 unit tests pass (39 new)
- 100 % `postbuild_lib` coverage held
- `radon cc -n C` clean — no C-grade complexity
- `ruff` clean
- Verified on the deployed back catalogue: H1 count 2 → 1, TOC count 5 → 1, TOC labels clean
- Lighthouse (audit-level CWV gates) + pa11y WCAG2AAA + JSON-LD validate all green on every PR

---

## [1.1.0] — 2026-06-01

Phase 1 Week 2 — performance gates + crawler policy + inline language switcher.

### Added

- **INP-aware Core Web Vitals lighthouse-ci gates ([#159])** — audit-level assertions added on top of category scores: `total-blocking-time` ≤ 200 ms (lab proxy for real-user INP < 200 ms p75), `largest-contentful-paint` ≤ 2500 ms, `cumulative-layout-shift` ≤ 0.1 (all error); `first-contentful-paint` ≤ 1800 ms (warn). lhci's default `interaction-to-next-paint` `auditRan` assertion explicitly disabled because INP is field-only on static pages. `.github/workflows/ci.yml` bumped from `@lhci/cli@^0.13` to `0.14.x` for Lighthouse-12 audit parity with the `lighthouse.yml` workflow.
- **`/llms-ctx.txt` ([#160])** — compact agent-context companion to `llms.txt`. URL + one-line description pairs grouped into Content / Feeds / JSON API / Author / Bot policy. Stays under 80 lines so it fits inside the smallest reasonable LLM context budget.
- **Per-category `robots.txt` taxonomy ([#160])** — same all-Allow stance, but the 30+ `User-agent` blocks are now grouped under five explicit category headers: Web search · Social / link-preview · SEO audit · AI retrieval (cite-on-query) · AI training (broad ingest) · Specialised indexers. Newly added: `Claude-User`, `Claude-SearchBot` (Anthropic split these from a single UA in late 2025).
- **Human-readable bot policy ([#160])** — new `/about/#bot-policy` section enumerates each crawler category, states the CC BY-4.0 licence, links every machine-readable surface (`/llms.txt`, `/llms-ctx.txt`, `/llms-full.txt`, `/api/agents/`, `/robots.txt`), and tells operators how to request a per-bot rule change.
- **Per-article inline language switcher ([#161])** — surfaces the 28-locale advantage to readers as content, not chrome. Rendered as a bordered band between the article hero and `<main>`. Native-script labels (`Français · 日本語 · العربية · 简体中文 · …`) localised lead-in per page locale (`Cet article est aussi disponible en…` / `この記事は次の言語でもご覧いただけます…`). Each link carries `lang` + `hreflang` + `rel="alternate"`; Arabic + Hebrew get `dir="rtl"`.

### Verification

- 372 / 372 unit tests pass
- 100 % `postbuild_lib` coverage held
- `radon cc -n C` clean
- 7 new test cases for the language switcher; 4 for the per-category `robots.txt`

---

## [1.0.0] — 2026-06-01

Phase 1 Week 1 — schema baseline. First tagged release.

### Added

- **`Person` graph overhaul ([#158])** — ORCID `0009-0005-1434-284X` added as `PropertyValue` `identifier` and prepended to `sameAs`. Three `EducationalOccupationalCredential` `hasCredential` entries (HSBC professional experience, ISO 20022 / SWIFT, NIST Post-Quantum Cryptography). 12-entry `knowsAbout` migrated from plain strings to `DefinedTerm` objects with `sameAs` to Wikipedia / NIST CSRC / SWIFT / Federal Reserve / TCH / ECB — the entity graph AI engines walk. `alumniOf` entries now carry `url`.
- **`Organization` graph node ([#158])** — new standalone `Organization` + `Brand` node with `@id` `#organization`, `logo`, `founder` → `#person`, `sameAs` to GitHub / Twitter / LinkedIn / Medium. `WebSite.publisher` rewired to `#organization`; `WebSite.author` added pointing at `#person`.
- **`TechArticle` / `ScholarlyArticle` article subtypes ([#158])** — `inject_tech_article` generalised to fire on every dated post. Auto-upgrades to `ScholarlyArticle` when the rendered body cites ≥ 6 distinct primary-source authority domains (NIST, ISO, BIS, IETF, SWIFT, ECB, Treasury, …). `ScholarlyArticle` carries the `citation` array natively. `BlogPosting` left untouched so the 30+ downstream gates (`article_furniture`, `seo`, `build_translations`, `validate_jsonld`) keep matching.
- **`/api/agents/organization.json` ([#158])** — new endpoint exposing the `Organization` + `Brand` graph as static JSON.

### Why this matters

Post-March-2026 Google core update moved E-E-A-T to an active filter (r = 0.81 correlation with AI Overview citation; 96 % of AI Overview citations now come from high-E-E-A-T sources). Domain Authority correlation collapsed to r = 0.18. Authority is now individuated and credential-graph-driven, not domain-wide — so the load-bearing schema work is at the `Person` / `Organization` / `Article-subtype` layer with ORCID + `hasCredential` + `DefinedTerm`.

### Verification

- 102 / 102 schema + postbuild orchestration tests pass
- JSON-LD structural validation passes
- Lighthouse + accessibility + diff + build CI gates all green

---

[1.2.0]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/releases/tag/v1.2.0
[1.1.0]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/releases/tag/v1.1.0
[1.0.0]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/releases/tag/v1.0.0

[#158]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/158
[#159]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/159
[#160]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/160
[#161]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/161
[#162]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/162
[#163]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/163
[#165]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/165
[#166]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/166
