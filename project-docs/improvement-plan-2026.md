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
- **1.1** Promote `tests/validation/` (CSP, hreflang, i18n parity/strings/labels/author, lang-leakage, RTL, sitemap, JSON-LD) to a required CI job.
- **1.2** Introduce `mypy` (strict on `scripts/lib`, `postbuild_lib`, `build_translations`; ratchet elsewhere). Makes the existing "handled by mypy" comment true.
- **1.3** Expand coverage past the 2 gated modules to repo-wide ≥90% / libs 100%; prioritise the 19 untested modules by blast radius.
- **1.4** Golden-file snapshot tests per generator (defends against the "gen_papers silently dropped an entry" class).

## Phase 2 — Security & supply-chain to 10/10
- **2.1** Generate the CycloneDX SBOM that `security.md` already promises (`public/sbom.cdx.json`), validated in CI.
- **2.2** SLSA build-provenance attestation for the deployed artifact + SBOM.
- **2.3** OpenSSF Scorecard (≥8), CodeQL (Python/JS), secret scanning + push protection.
- **2.4** CSP/SRI verification test (no `unsafe-inline`; every inline JSON-LD hash present; every asset SRI matches).

## Phase 3 — Performance / speed to 10/10
- **3.1** Incremental builds (content-hash skip of unchanged pages; model on the pa11y hash-cache). Target <2 min for a 1-article change.
- **3.2** Cut CI wall-clock: adaptive pa11y shard count, binary-level caching of ssg/npm/cargo, parallelise independent build-job checks. Target p50 <20 min.
- **3.3** Promote `lighthouserc.json` thresholds to hard CI assertions (perf ≥0.98, a11y =1.0).
- **3.4** Runtime asset budget test (fonts preloaded, banner `srcset`+dimensions, JS payload budget, cache headers).

## Phase 4 — Structural quality & accuracy (refactor)
- **4.1** Break up the four >1.3k-LOC modules: `article_furniture.py`→`hreflang.py`; `postbuild.py`→`sri.py`; `build_case_studies.py`→`_data/case-studies/i18n.json`; `output.py`→`feeds.py`. Target no module >800 LOC.
- **4.2** Consolidate duplication: single frontmatter parser in `scripts/lib/_frontmatter.py` (≈5 copies today); single `_DATED_SLUG_RE` in `scripts/lib/_core.py` (≈11 copies). Target jscpd <1%.
- **4.3** Mutation testing (`mutmut`) on `scripts/lib` + `postbuild_lib`; raise tests to ≥75% mutation score.

## Phase 5 — DX, docs & governance to 10/10
- **5.1** ADR discipline: backfill ADRs for existing structural decisions (build-copy pipeline, docs→public retirement, pa11y sharding+cache, sigstore), require ADRs for future ones. (Seeded: ADR-0002, ADR-0003.)
- **5.2** `make bootstrap` one-command onboarding; verified "first build <10 min" in README.
- **5.3** Runbooks in `project-docs/operations/`: publish, rollback, CI-flake triage, incident response.
- **5.4** Regenerate `architecture.md` data-flow from the real `build.sh` order; test fails if a generator is added without a doc entry.

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
