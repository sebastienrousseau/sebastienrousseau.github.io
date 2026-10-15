# ADR-0006: CI performance + the Lighthouse measurement caveat

**Site:** sebastienrousseau.com
**Author:** Sebastien Rousseau
**Status:** Accepted
**Date:** 2026-06-27
**Related:** [Improvement Plan 2026](../improvement-plan-2026.md) Phase 3

---

## Context

Phase 3 targets performance/speed. Two findings reframed the work:

1. **Real-world performance is already excellent.** Lighthouse against the live
   site (desktop) scores **0.97** — FCP 0.6 s, LCP 1.2 s, TBT 0 ms, CLS 0. The
   Core Web Vitals are well inside budget.

2. **The CI Lighthouse score (~0.76) is a measurement artifact, not a real
   regression.** `lhci`'s `staticDistDir` server sends **no gzip and no cache
   headers**, so the `uses-text-compression`, `uses-long-cache-ttl`, and
   network-dependency audits are penalised in CI even though Cloudflare handles
   all three in production. The Core Web Vitals assertions (LCP/TBT/CLS) are
   already `error`-gated and pass; the category score is appropriately left as
   `warn` because it is unreliable in `staticDistDir`.

3. **True incremental builds (3.1) are out of scope.** Page compilation is done
   by the external `ssg` Rust binary; the pipeline cannot skip unchanged pages
   without `ssg` support. pa11y is already incremental via its hash cache.

So the achievable, high-value Phase 3 win is **CI wall-clock + feedback speed**,
not fixing an already-fast site.

## Decision

**Parallelise static analysis.** Lint (ruff), type-check (mypy), naming, KV
audit, complexity (radon), and duplication (jscpd) move out of the serial build
job into a dedicated `static` job that runs concurrently. Source-only — no `ssg`
or site build — so lint/type failures surface in ~2-3 min instead of ~18 min.

**De-duplicate pre-build tests.** The build job ran `pytest` twice pre-build
(once plain, once for the coverage gate); collapsed into one run with the
`postbuild_lib` 100 % gate.

**Document the perf posture.** Core Web Vitals stay `error`-gated (the metrics
that reflect real UX and are accurate in `staticDistDir`). The category score
stays `warn` with this caveat recorded, rather than chasing a misleading number.

## Consequences

- **+** Faster CI feedback (static failures in minutes) and a shorter build
  critical path.
- **+** Honest perf gating: enforce the metrics that matter and are measured
  accurately; don't gate on an artifact.
- **−** The `static` job repeats Python/Node setup (~1 min) — paid in parallel,
  off the critical path.
- **Follow-ups:** a representative (gzip + cache) Lighthouse server would let the
  category score be hard-gated; trimming `unused-css` (~16 KB) / `unused-js`
  (~80 KB) and the render-blocking CSS (~130 ms) are marginal real wins on an
  already-0.97 site.
