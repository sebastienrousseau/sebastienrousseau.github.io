# ADR-0008: pa11y accessibility gate — incremental cache + 4-way sharding

**Site:** sebastienrousseau.com
**Author:** Sebastien Rousseau
**Status:** Accepted
**Date:** 2026-06-26
**Related:** [Improvement Plan 2026](../improvement-plan-2026.md) Phase 0.2 / 3; [ADR-0002](0002-pin-build-toolchains.md); [ADR-0006](0006-ci-performance-and-perf-measurement.md)

---

## Context

The site is gated at **WCAG2AAA** by pa11y. The rendered tree is ~5,000 pages
(EN + 27 locales). Running pa11y over every page on every PR is prohibitively
slow, yet skipping a11y is not an option. Two failure modes also had to be
contained:

- A **wedged headless-Chrome** process can leave pa11y-ci hanging on a single
  URL far past its per-URL timeout (observed 5h+).
- pa11y/axe contrast cannot read an **image or gradient background**, so white
  text over a full-bleed hero reports `NaN:1` — a false positive.

## Decision

Run pa11y as an **incremental, sharded, time-bounded** gate
(`scripts/seo_and_audit/pa11y_cache.py` + the `pa11y` matrix job in
`.github/workflows/ci.yml`):

- **Incremental.** A pre-pass diffs the built pages against a committed hash
  cache (`_data/pa11y-cache.json`) and writes only the changed (delta) URLs to
  `.pa11yci`. A config-hash (pa11y version, chromium version, WCAG standard,
  `hideElements`) invalidates the whole cache when the check itself changes.
- **Skip on full cache hit.** If the delta is empty, the partition step sets
  `pa11y-needed=false` and the matrix is skipped entirely.
- **4-way shards.** Delta URLs are round-robin-partitioned (`i % 4`) across a
  `shard: [1,2,3,4]` matrix — stable across runs so the cache stays coherent —
  with `fail-fast: false` so one bad URL doesn't mask the others.
- **Time-bounded.** Each shard has `timeout-minutes: 50` so a hung Chrome fails
  fast instead of stalling the deploy.
- **Pinned engine.** `pa11y-ci@4.1.1` (ADR-0002): v4's pa11y v8 + axe-core
  contrast calculator agrees with current sRGB→luminance; v3 disagreed by ~0.2
  ratio points and produced false AAA failures on warm backgrounds.
- **`hideElements`** removes regions pa11y cannot fairly evaluate: the search
  widget, recaptcha iframes, and the `/projects-*` story-hero image overlay
  (white text on a scrim over a background image — legible, but `NaN:1` to a
  contrast checker, which also gets a solid dark `background-color`).

## Consequences

- **+** A full a11y AAA gate that costs ~0 on no-page-change PRs and ~34 min on
  a full sweep, instead of hours.
- **+** A hung run fails in ≤50 min, not 5h; a single flaky shard is re-runnable
  in isolation (`gh run rerun --failed` — see `operations/ci-flake-triage.md`).
- **−** The cache and shard assignment must stay coherent: the round-robin must
  be stable and the config-hash must cover anything that changes pa11y's
  verdict, or a stale cache could skip a page that should be re-checked. New
  uncomputable-contrast surfaces must be added to `hideElements` deliberately,
  with a solid background so the hidden element is still genuinely accessible.
