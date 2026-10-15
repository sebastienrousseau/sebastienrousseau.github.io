# Developer-Experience & Interactivity Plan — "Beyond the Bank Portal" (2026)

**Site:** sebastienrousseau.com
**Author:** Sebastien Rousseau
**Status:** Proposed — phased delivery, sequenced *after* the current content backlog
**Created:** 2026-07-03
**Scope:** Turn a best-in-class *static thought-leadership* site into a site that also beats a bank developer portal on the one axis such portals win — **live, interactive, machine-usable tooling** — without trading away the openness, speed, and machine-readability that already put this site ahead.

---

## Why this plan exists

Benchmarked against HSBC's developer portal (`develop.hsbc.com` / `beta.developer.hsbc.com/web-hub`), this site already wins decisively on every *shared* dimension: 27-locale i18n with hreflang reciprocity, WCAG/axe/pa11y-gated accessibility, Lighthouse-gated performance, rich JSON-LD, hash-strict CSP + SRI + Sigstore attestation with **0 open code-scanning/Dependabot alerts**, and machine surfaces (`llms.txt`, `/api/agents/`, oEmbed, RSS/Atom/news-sitemap).

What a bank portal has that a content site does not is **interactivity and a first-class machine-facing catalogue**: an API catalogue, in-doc "try it now", a sandbox, downloadable collections. The strategic move is to *convert static authority into usable tools* — because a reader who **uses a tool returns**; a reader who reads an article rarely does. No bank thought-piece ships an interactive index.

**Guiding principles.** (1) Every feature ships as a focused, CI-green, admin-merged PR, same as the platform work. (2) Nothing regresses the a11y/perf/security gates — new interactivity must stay progressive-enhancement (works with JS off, degrades to the existing static content), CSP-hash-clean, and within the Lighthouse budget. (3) Prefer **no-backend, build-time** solutions (static JSON, WASM, client-side) so the site stays a deployable static artifact with no new attack surface.

---

## The rubric — what "way above the portal" means

| Dimension | Today | Target | Acceptance (verifiable) |
|---|---|---|---|
| Interactivity | Static tables/diagrams | Live tools | ≥2 flagship interactive tools shipped; each works JS-off (progressive enhancement) and passes the pa11y/axe gate. |
| Discoverability (human) | No on-site search | Instant search | Client-side full-text search over `search-index.json`, <150 ms p95, keyboard-accessible, 27-locale aware. |
| Discoverability (machine) | `/api/agents/`, `llms.txt` | Documented content API | Versioned JSON API + published OpenAPI 3.1 spec + a `/api/` catalogue page; schema-validated in CI. |
| Try-it (own tooling) | Links to repos | Runnable demos | ≥1 in-browser WASM/JS playground for an owned library; sandboxed; CSP-clean. |
| Freshness signals | Dated posts | Changelog + status | Auto-generated `/changelog`; CI/uptime status badge; both build-gated. |
| Distribution | Read-only pages | Embeddable widgets | ≥1 documented embeddable component (oEmbed/iframe/snippet) others can drop in. |

**Sequencing note:** ordered by *impact ÷ effort*. Items 1–2 are the highest leverage and should land first.

---

## Phase 1 — Interactive Index Scorecards ⭐ (flagship, highest impact)

**Rationale.** The "Agentic AI Index" (six dimensions) and "Certified Blockchain Index" (five-level CMM across five layers) currently ship as *static tables*. HSBC's edge is "try it now." Ship each index as an **interactive self-assessment**: the reader scores their own institution dimension-by-dimension → a **live composite score**, a radar/bar visualisation, a maturity band, and a **shareable + exportable result** (permalink-encoded state + PDF/PNG export). This is the single biggest differentiator — it converts a one-time reader into a returning tool-user, which no bank thought-piece does.

**Approach.**
- A reusable, data-driven web component `<index-scorecard>` fed by a per-index JSON spec in `_data/indices/<slug>.json` (dimensions, levels, weights, tolerances, copy). One component, N indices.
- Progressive enhancement: server-render the existing static table; the component *upgrades* it in place when JS is available. JS-off readers still get the full table.
- State lives in the URL (`?s=<base64>`) so results are shareable/bookmarkable with **no backend**. Export via client-side canvas → PNG and the existing PDF route.
- Visualisation with a tiny dependency-free SVG radar (no charting lib — keep the perf budget).
- CSP: component script hashed by the existing `inject_jsonld_hashes`/SRI pipeline; no inline handlers.

**Effort:** M (1 component + 2 index JSON specs + a generator to inject the mount point). **Depends on:** nothing. **Risk:** a11y of the interactive controls — mitigate with native form controls + `aria-live` for the running score, verified by the pa11y gate.

**Acceptance:** both indices interactive; JS-off shows the static table; score maths matches the article's formulas; shareable permalink round-trips; pa11y/axe/Lighthouse gates stay green; a golden-file test pins the score computation.

---

## Phase 2 — Real on-site search ⭐

**Rationale.** 200+ articles across 27 locales with **zero on-site search** — HSBC surfaces its catalogue; this site surfaces nothing. Instant search is table-stakes for authority at this content volume.

**Approach.**
- Client-side full-text search over the **existing `search-index.json`** (already emitted by ssg) — no backend, no external service.
- Prefer **Pagefind** (build-time index, ranked, tiny runtime, i18n-aware) over Lunr if index size is a concern; both are static-friendly. Wire the index build into `build.sh` after ssg.
- A `⌘K`/`Ctrl-K` command-palette overlay + a `/search` page fallback; locale-aware (search within the active language, with a "search all locales" toggle).
- Keyboard-navigable, `role="listbox"` results, respects `prefers-reduced-motion`.

**Effort:** S–M. **Depends on:** `search-index.json` (exists). **Risk:** index weight on the perf budget — lazy-load the search runtime on first invocation only.

**Acceptance:** search returns ranked results <150 ms p95 client-side; keyboard-accessible; 27-locale aware; lazy-loaded so it adds **0** to initial LCP; pa11y gate green.

---

## Phase 3 — "Try it" sandboxes for the open-source libraries

**Rationale.** The author *builds* (KyberLib, pain001, libmake, and the crates behind the site). HSBC offers Postman collections; this can go further with **runnable, in-browser demos** — the developer-portal "sandbox" pattern applied to owned tooling, with none of the auth friction.

**Approach.**
- **KyberLib WASM playground:** compile the Rust crate to `wasm32-unknown-unknown`, expose ML-KEM key-encapsulation in a sandboxed page (generate keypair → encapsulate → decapsulate, showing sizes/timings). Ships as a static `.wasm` asset behind the existing SRI/CSP pipeline (add `wasm-unsafe-eval` to a **scoped** CSP only on that route, not site-wide).
- **pain001 ISO 20022 generator:** a form → valid `pain.001` XML message, generated client-side (WASM or JS port), downloadable. Doubles as living documentation for the library.
- Each demo is a standalone route linked from the relevant article/project page; progressive enhancement (link to the repo when JS/WASM unavailable).

**Effort:** L (WASM build pipeline + per-demo UI). **Depends on:** the crates building to WASM. **Risk:** CSP relaxation for WASM — keep it route-scoped and documented in an ADR; verify the site-wide hash-strict CSP is untouched.

**Acceptance:** ≥1 demo live and runnable; scoped CSP documented via ADR; no relaxation of the global CSP; demo route passes a11y/perf gates; WASM asset is SRI-pinned.

---

## Phase 4 — Published content API + OpenAPI spec + `/api/` catalogue

**Rationale.** `/api/agents/` already exists. Extend it into a **documented, versioned content API** (articles, indices, taxonomy, case studies as JSON) with an OpenAPI 3.1 spec and a mini **catalogue page** — literally out-doing a bank's API catalogue *at the meta level*: an open, spec-backed, zero-auth data layer.

**Approach.**
- Generate static JSON endpoints at build time: `/api/v1/articles.json`, `/api/v1/articles/<slug>.json`, `/api/v1/indices/<slug>.json`, `/api/v1/taxonomy.json` (reuse the existing generators + `/api/agents/` machinery).
- Author an **OpenAPI 3.1** document (`/api/openapi.json`) describing the static endpoints; validate it in CI (schema lint) and render a **`/api/` catalogue page** (Redoc/Elements static render, or a bespoke lightweight one to keep the budget).
- Version prefix (`/api/v1/`) + a deprecation policy in the OpenAPI `info`.

**Effort:** M. **Depends on:** existing generators. **Risk:** keeping the spec in sync with the emitted JSON — add a CI check that every documented path resolves to a real generated file (a golden-file/contract test).

**Acceptance:** OpenAPI 3.1 spec validates in CI; every documented endpoint resolves to a generated static file (contract-tested); `/api/` catalogue page renders and is linked from the footer/`llms.txt`.

---

## Phase 5 — Changelog + "what's new" + status

**Rationale.** Developer portals live and die on **freshness signals**. Surface them.

**Approach.**
- **`/changelog`** auto-generated at build time from git history + dated posts (group by month; link each entry to the article/PR). A generator in `scripts/generators/`.
- **"What's new"** strip on the homepage (latest N changelog entries).
- **Status/uptime badge:** the site already gates heavily in CI — surface a lightweight build/deploy status + a public uptime check (static badge from an uptime provider, or a self-hosted JSON pinged by the Lighthouse/deploy workflow). No new backend.

**Effort:** S. **Depends on:** git history (exists). **Risk:** none material.

**Acceptance:** `/changelog` generated deterministically (reproducible build); homepage "what's new" reflects the latest entries; a status indicator is live; all within the perf budget.

---

## Phase 6 — Interactive (steppable) diagrams

**Rationale.** Mermaid diagrams currently render **statically**. The consensus-to-audit sequence diagram in the July-2nd "Certified Blockchains" article — and the architecture diagrams elsewhere — are perfect candidates for **step-through/zoomable** interaction.

**Approach.**
- Keep Mermaid's static SVG as the baseline (progressive enhancement). Layer a small controller that adds **pan/zoom** (svg-pan-zoom, tiny) and, for sequence diagrams, a **"step" mode** that highlights each message in turn with a caption.
- Driven by the existing Mermaid source in the post; no per-diagram bespoke code.

**Effort:** S–M. **Depends on:** the existing `inject_mermaid` pipeline. **Risk:** a11y — provide a text-equivalent step list; keep controls keyboard-navigable.

**Acceptance:** ≥1 diagram is zoomable + steppable; static SVG remains the JS-off baseline; text-equivalent present; pa11y gate green.

---

## Phase 7 — Design-system / component showcase + embeddable widgets

**Rationale.** The site's citation/sources component, index cards, lead blocks, etc. are reusable. Publishing them as **embeddable snippets** others can drop into their own pages turns readers into **distributors** — organic reach a bank portal never gets.

**Approach.**
- A `/components` (or `/design`) showcase page documenting the visual system (typography, colour, cards, citation rail, index scorecard) with copy-paste snippets — a lightweight design-system reference.
- **Embeds:** extend the existing oEmbed support so an index scorecard or a citation card can be embedded via `<script>`/iframe on third-party sites, with a documented, versioned embed URL.

**Effort:** M. **Depends on:** Phase 1 (scorecard) + existing oEmbed. **Risk:** embed security — sandbox iframes, no third-party JS execution in the host page.

**Acceptance:** showcase page live; ≥1 documented embeddable widget with a stable embed URL; embeds are sandboxed; oEmbed discovery works.

---

## Phase 8 — Audience onboarding / path selector

**Rationale.** The articles already segment guidance by institution type (G-SIBs, transaction banks, regional banks, fintechs, SMEs) and by audience (boards / engineers / regulators). Surface that as **navigation**.

**Approach.**
- A homepage/landing **"Read as…"** selector (for boards · for engineers · for regulators) that filters/re-orders content and sets a lightweight, cookie-free preference (URL param + `localStorage`).
- Reuse the existing taxonomy/pillar structure; no new content required — just a lens over it.

**Effort:** S. **Depends on:** existing taxonomy. **Risk:** none material.

**Acceptance:** path selector re-orders content by audience; preference persists without cookies; works JS-off (URL-param driven); no a11y/perf regression.

---

## Cross-cutting guardrails (apply to every phase)

- **Progressive enhancement is mandatory** — every interactive feature must degrade to the existing static content with JS/WASM off.
- **No global CSP relaxation** — new scripts are hashed by the existing SRI/CSP pipeline; any `wasm-unsafe-eval` is route-scoped and ADR-documented.
- **Perf budget unbroken** — interactive runtimes lazy-load on demand; initial LCP unchanged; Lighthouse gate stays green.
- **a11y-first** — native controls, `aria-live` for dynamic values, keyboard paths, text equivalents; pa11y/axe stay blocking gates.
- **i18n-aware** — new UI strings go through `_data/i18n/<lang>/strings.json` (the parity gate enforces the shape).
- **ADR per structural decision** — WASM CSP scope, API versioning policy, search engine choice.

## Suggested delivery order

1. **Phase 1 — Interactive index scorecards** (flagship differentiator)
2. **Phase 2 — On-site search** (table-stakes at this content volume)
3. **Phase 4 — Content API + OpenAPI** (meta-level catalogue win)
4. **Phase 5 — Changelog + status** (cheap freshness signals)
5. **Phase 6 — Interactive diagrams**
6. **Phase 8 — Audience path selector**
7. **Phase 3 — WASM sandboxes** (highest effort; highest "builder" credibility)
8. **Phase 7 — Design-system + embeds** (compounds Phase 1)
