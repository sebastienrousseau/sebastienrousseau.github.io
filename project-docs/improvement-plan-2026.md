# Repository Improvement Plan — Road to 10/10 (2026)

**Site:** sebastienrousseau.com
**Author:** Sebastien Rousseau
**Status:** Active — phased delivery
**Created:** 2026-06-26
**Scope:** Drive the build/publish platform to a verifiable 10/10 across performance, security, quality, accuracy, reliability, and DX.

This is a living roadmap. Each item carries an acceptance criterion so "10/10"
is *measured*, not asserted. Progress is tracked against the baseline captured
in `project-docs/audits/baseline-2026-06.md` (Phase −1) via `make metrics`.

---

## The rubric — what 10/10 means

| Dimension | Baseline | Target | Acceptance (verifiable) |
|---|---|---|---|
| Performance / Speed | 6 | 10 | Incremental build <2 min for a 1-article change; CI p50 <20 min; Lighthouse perf ≥0.98 gated; no render-blocking regressions. |
| Security / Supply-chain | 6.5 | 10 | SBOM emitted + attested; SLSA provenance; OpenSSF Scorecard ≥8; all toolchains pinned; CSP hash-strict verified in CI; secret scanning on; no doc/reality drift. |
| Quality (tests/types/structure) | 7 | 10 | mypy strict in CI; coverage ≥90% repo-wide (100% libs); no module >800 LOC; jscpd <1%; mutation score ≥75% on core libs. |
| Accuracy / Correctness | 7.5 | 10 | i18n/validation suite is a blocking gate; reproducible byte-identical builds; link + schema integrity gated; golden-file snapshots per generator. |
| Reliability / Operability | 5.5 | 10 | No source-mutating foot-guns; every CI job time-bounded; required status checks enforced; documented rollback. |
| DX / Docs / Governance | 6 | 10 | ADR per structural decision; one-command onboarding; publish/rollback/incident runbooks; architecture doc matches code. |

**Guiding principle:** make CI the source of truth before optimising anything else.

---

## Phase −1 — Baseline & instrumentation
- Capture CI per-job p50, full `build.sh` wall-time (ssg vs post-processing vs validation), repo-wide coverage %, `radon` average, `jscpd` %, Lighthouse scores, untested-module count, mypy error count → `project-docs/audits/baseline-2026-06.md`.
- Add `make metrics` to regenerate those numbers.

## Phase 0 — Stop the bleeding (safety & reliability) — IN PROGRESS
- **0.1** Eliminate source-mutation foot-guns: `post_enrich.py` / `topic_link.py` require an explicit `--dir` (no `_posts` default); smoke tests run against a temp copy, never committed source; guard test asserts the enrichers refuse to write source by default.
- **0.2** `timeout-minutes` on every CI job (build, finalise, lighthouse, link-audit, schema-diff).
- **0.3** Pin every toolchain (`ssg`, `ruff`, `pa11y-ci`, `@lhci/cli`, `wasm-pack`, Node) — see ADR-0002.
- **0.4** Mark `Build + smoke tests + partition` and `Merge pa11y, Lighthouse, deploy` as required status checks on `main`.
- **0.1b (follow-up)** Apply the same `--dir` safety to the listing writers, remove the `perl -i` layout hack in `make regenerate` by emitting final markup from `gen_layouts.py`, and add a `git diff --exit-code` source-cleanliness guard across all generators.

## Phase 1 — Make quality gates real & complete
- **1.1 — DONE (already gated).** `tests/validation/` (CSP, hreflang, i18n parity/strings/labels/author, lang-leakage, RTL, sitemap, JSON-LD) already gates: `build.sh` runs all 13 under `set -euo pipefail`, and `build.sh` is the CI build step, so a validation failure fails the build job. No new gate needed.
- **1.2 — DONE (tier + postbuild_lib).** `mypy` (`check_untyped_defs`, `disallow_incomplete_defs`) gates the strict-clean tier in CI via `scripts/typecheck.sh`: `lib`, `security`, `editorial`, `dev`, `i18n`, `build_translations`, and now `postbuild/postbuild_lib` (6 annotation fixes: widened `str | None` entity params, removed 3 dead `type: ignore`, annotated `_dedupe_blocks` callback). **Ratchet remaining:** `postbuild` / `generators` / `seo_and_audit` (~1 each).
- **1.3 — IN PROGRESS.** Expand coverage past the gated modules to repo-wide ≥90% / libs 100%; prioritise untested modules by blast radius. **Done:** `check_voice.py` (publishing gate) → `tests/unit/test_check_voice.py` (13 cases); `build_listings.py` (the /articles/ index generator, 908 LOC) → `tests/unit/test_build_listings.py` (10 cases over `_esc`, `_alias_map`, `_post_pillars`, `_post_card_fields`, `_render_pagination`). **Remaining (by blast radius):** `build_case_studies.py`, `backfill_locale_frontmatter.py`, `regen_homepage.py`, `regen_slug_maps.py`, `build_tags.py`, `fetch_metrics.py`, `build_rag_corpus.py`, and the smaller editorial/seo modules.
- **1.4 — DONE.** Golden-file snapshot tests for the listing generators' pure render functions (`tests/unit/test_generator_golden.py` + `tests/unit/golden/*.html`): `gen_articles` (card/featured/eyebrow), `gen_papers` (epaa/whisper/card — the featured cards also pin committed paper metadata), `gen_projects` (card/featured/section). Pins exact markup bytes per fixed input; `UPDATE_GOLDEN=1` regenerates. Defends the "gen_papers silently dropped an entry / renamed a class" class. Runs in the gated unit suite.

## Phase 2 — Security & supply-chain to 10/10
- **2.1 — DONE.** CycloneDX SBOM generated + validated in CI (`scripts/security/gen-sbom.sh` → `public/sbom.cdx.json`); `security.md` corrected. Follow-up: hash-pinned deps for per-component hashes. (ADR-0004)
- **2.2 — DONE.** SLSA build-provenance attestation on the deployed SBOM via `actions/attest-build-provenance` (main only); verifiable with `gh attestation verify`. (ADR-0004)
- **2.3 — DONE.** CodeQL (`security-and-quality`, Python + JS, path-filtered) + OpenSSF Scorecard (weekly + push to main) workflows added; secret scanning + push protection enabled repo-wide. (ADR-0005) Follow-up: pin actions by SHA to lift the Scorecard score.
- **2.4 — DONE.** CSP enforcement was already covered by `test_csp_strict.py` (no `unsafe-inline`, inline JSON-LD hashes present); added the missing **SRI correctness** gate `test_sri_integrity.py` (recomputes every integrity hash from file bytes), wired into `build.sh`. (ADR-0005)

## Phase 3 — Performance / speed to 10/10
**Finding (ADR-0006):** real-world perf is already **0.97** (FCP 0.6s, LCP 1.2s, TBT 0, CLS 0, verified against live). The CI "0.76" is a measurement artifact — lhci's `staticDistDir` server has no gzip/cache, unlike Cloudflare. Core Web Vitals are already `error`-gated and green.
- **3.1 — Out of scope.** True incremental page builds need `ssg` (external Rust binary) support; pa11y is already incremental via its hash cache.
- **3.2 — DONE (this PR).** Static analysis (ruff/mypy/naming/KV/radon/jscpd) moved to a parallel `static` job → failures surface in minutes, shorter build critical path; pre-build pytest de-duplicated. (ADR-0006) Follow-up: adaptive pa11y shard count.
- **3.3 — Partly done / by design.** CWV (LCP/TBT/CLS) already hard-gated and accurate in CI; the category score stays `warn` (artifact). Follow-up: a gzip+cache Lighthouse server to make the category hard-gatable at ≥0.95.
- **3.4 — Follow-up.** Marginal real wins only (site already 0.97): trim `unused-css` (~16 KB) / `unused-js` (~80 KB) / render-blocking CSS (~130 ms); optional per-page weight budget test.

## Phase 4 — Structural quality & accuracy (refactor)
- **4.1** Break up the four >1.3k-LOC modules: `article_furniture.py`→`hreflang.py`; `postbuild.py`→`sri.py`; `build_case_studies.py`→`_data/case-studies/i18n.json`; `output.py`→`feeds.py`. Target no module >800 LOC.
- **4.2** Consolidate duplication: single frontmatter parser in `scripts/lib/_frontmatter.py` (≈5 copies today); single `_DATED_SLUG_RE` in `scripts/lib/_core.py` (≈11 copies). Target jscpd <1%.
- **4.3** Mutation testing (`mutmut`) on `scripts/lib` + `postbuild_lib`; raise tests to ≥75% mutation score.

## Phase 5 — DX, docs & governance to 10/10
- **5.1 — DONE.** ADR discipline: build-copy pipeline already ADR-0003; backfilled the rest — ADR-0007 (docs→public deploy), ADR-0008 (pa11y sharding+cache), ADR-0009 (Sigstore content signing). `tests/unit/test_adr_hygiene.py` enforces contiguous numbering, required Status/Date headers, and Context/Decision/Consequences sections (0001 exempt as a pre-template implementation plan), so future structural decisions can't skip the template.
- **5.2 — DONE.** `make bootstrap` one-command onboarding (mise-first: provisions the pinned toolchain + Python build/dev deps + `ssg` 0.0.44, idempotent; ADR-0002). README Quick Start leads with `make bootstrap` → `make build` (first-build target: under 10 min), with a manual no-mise fallback.
- **5.3 — DONE.** Runbooks in `project-docs/operations/`: rollback, CI-flake triage, incident response (publish already covered by `publishing.md` / `daily-publishing.md`), plus an `operations/README.md` index. Grounded in real operational experience: `main`-is-the-deploy, Cloudflare edge-cache staleness, pa11y 50-min hang re-runs, the local-0.0.45 lang-leakage artifact, and the locale-slug-identity broken-link class.
- **5.4 — DONE.** `architecture.md` "build pipeline" section rewritten from the real `build.sh` order (19 generator/postbuild scripts across 4 phases, was a stale "seven stages"). Guard test `tests/unit/test_architecture_doc_current.py` parses `build.sh` for `python3 scripts/...py` steps and fails if any is undocumented — so adding a generator without a doc entry breaks CI.

---

## Sequencing & effort
```
Phase −1 (0.5d) → Phase 0 (2d) → Phase 1 (4d) ┬→ Phase 2 (3d)
                                              ├→ Phase 3 (4d)
                                              └→ Phase 4 (5d)
Phase 5 (2d) runs alongside 2–4.   Total ≈ 20–22 engineering days, ~10–12 PRs.
```
Critical path: −1 → 0 → 1 (these make every later metric trustworthy and mergeable). Phases 2/3/4 are independent and can interleave.

## Definition of done
`make metrics` shows: CI p50 <20 min, incremental build <2 min, coverage ≥90%/libs 100%, mypy strict green, jscpd <1%, no module >800 LOC, Lighthouse perf ≥0.98 gated, SBOM + provenance shipping, Scorecard ≥8, validation suite gating, zero source-mutation foot-guns — all enforced in CI.

---

## Phase 6 — External audit remediation (2026-08-19)

A full audit of the repo, the build output and the live origin produced 21
confirmed findings. Nineteen are closed in code; the rest are editorial or need
a Cloudflare login. What follows is the record, including what was *not* done
and why.

### Closed in this change

| ID | Finding | Fix | Gate that stops it recurring |
|---|---|---|---|
| F-01 | `.well-known/` never deployed — `/.well-known/security.txt` (RFC 9116), `ai.txt`, WKD and `openapi.json` all 404 in production while present in the build | `include-hidden-files: true` on the Pages artifact | `verify_deploy.py` after every `main` deploy |
| F-02 | Home page had no meta description; og/twitter description was a scrape of the nav ending mid-sentence on a comma; `og:type=article`; square og:image with no dimensions | Authored copy now wins over any scrape; symmetric og:type; card sourced from the authored landscape banner | `test_home_social_card.py`, `verify_deploy.py` |
| F-03 | Build not hermetic — `public/` never cleaned, so local builds accumulated 7,124 pages titled "My SSG Site", a 13,940-URL sitemap and a 32.5 MB search index | `rm -rf public` at the top of `build.sh` | `reproducible` CI job: builds twice, diffs |
| F-04 | EN news sitemap empty, FR served months-old entries, publication name was an email address | 48 h window + real publication name in `build_lang_feeds`; stray ssg sitemap copies pruned | `test_news_sitemap_locale.py`, `test_prune_duplicate_sitemaps.py` |
| F-05 | Median 2 internal links per article, 0 contextual in-prose links | Taxonomy-driven contextual linker + cluster block; absolute self-links canonicalised | `test_internal_links.py` |
| F-07 | No analytics of any kind | Cloudflare Web Analytics plumbing, off until a token is configured | `test_analytics_beacon.py` |
| F-08 | Article JSON-LD bound to a non-canonical URL; two article nodes disagreeing | `align_article_identity` binds every Article node to the canonical | `test_schema_identity_and_faq.py` |
| F-09 | Four conflicting `ssg` pins; `make bootstrap` installed one CI would reject | Makefile derives `SSG_VERSION` from `ci.yml` | `test_ssg_pin_single_source.py` |
| F-10 | Eight near-identical stylesheets; `--accent` inside the shared block made the whole 138 KB file page-variable | Accent split into its own 62 B block; byte-identical assets deduped | `test_asset_dedupe.py` |
| F-11 | Complexity gate covered 4 of 8 script dirs; worst function in the repo was ungated at D/25 | Gate covers all of `scripts/`, ratcheted | `check-complexity.sh` + allowlist |
| F-12 | FAQ sections written but never marked up | `FAQPage` emitted from the existing prose | `test_schema_identity_and_faq.py` |
| F-13 | Slug localisation inconsistent across 28 locales, undocumented | ADR-0012 + per-locale baseline | `test_slug_policy.py` |
| F-15 | 42 % duplicate CSP hash tokens; a hash of the empty string in `style-src` | Dedupe on emit; dead hash removed | `test_csp_hash_dedupe.py` |
| F-17 | Duplicate `integrity` attributes on 6,854 pages | Consequence of F-03; gone with the hermetic build | `reproducible` job |
| F-18 | Three frontmatter parsers | Two collapsed onto `scripts/lib/_frontmatter`, differential-tested over 240 posts | — |
| F-19 | Deprecated ChatGPT-plugin manifest maintained and advertised | Deleted | — |
| F-20 | 20 locales rendered in whatever font the platform chose | Explicit per-script stacks in `fonts.css` | — |
| F-21 | Unreferenced `/main.js` and `/highlight.css` aliases shipped | Only `sw.js` keeps a stable alias, and the comment now says why | `test_build_output.py` |

### Needs a Cloudflare or Google login — see `.git/post-audit-actions.sh`

- **F-16 — edge CSP carries `unsafe-inline`.** Inert today (the strict meta
  policy also applies and both must allow), but it inverts defence in depth.
  `DEPLOY.md` carries the exact Transform Rule to paste; do **not** simply
  delete the token, which would block the hash-allowed inline JSON-LD.
- **F-07 completion.** Beacon token, Search Console, Bing Webmaster Tools.

### Open, deliberately

- **F-06 — publishing cadence.** 27 articles in June, 13 in July, 4 in August,
  none since 2026-08-04. This is a decay curve, not a pause, and it is an
  editorial decision rather than an engineering one. Two things are worth more
  than resuming a daily target that will be missed again: a cadence that will
  actually hold, and a **quarterly refresh rotation** over the existing 105
  articles. AI citation rates fall off sharply past roughly three months
  without revision, so updating a piece that already ranks beats publishing one
  that does not — and 37 articles carry a past year in the title.
- **F-14 — dated article URLs.** See ADR-0013. Deliberately unchanged: the
  measurement that would justify a migration only starts collecting now.

### Backlogs now tracked rather than invisible

- `scripts/dev/complexity-allowlist.txt` — 25 functions. Four cleared already
  (two at D/25 and D/22), each differential-tested against its pre-refactor
  implementation before the line was deleted.
- `tests/validation/slug-policy-baseline.json` — 34 locales.
