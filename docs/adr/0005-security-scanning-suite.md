# ADR-0005: Security scanning suite (Scorecard, CodeQL, secret scanning, SRI)

**Site:** sebastienrousseau.com
**Author:** Sebastien Rousseau
**Status:** Accepted
**Date:** 2026-06-26
**Related:** [Improvement Plan 2026](../improvement-plan-2026.md) Phase 2.3 / 2.4; [ADR-0004](0004-sbom-and-build-provenance.md)

---

## Context

After SBOM + provenance (ADR-0004), the remaining Phase 2 gaps were the standard
2026 security-automation baseline: no static analysis, no supply-chain posture
score, secret scanning disabled, and SRI hashes checked only for *shape* (not
*correctness*) — a stale hash would silently break asset loading without failing
the build.

## Decision

**Static analysis — CodeQL** (`.github/workflows/codeql.yml`): analyses the
Python pipeline and Worker/layout JavaScript with the `security-and-quality`
query suite. Path-filtered so markdown-only PRs skip it. Alerts surface in the
Security tab; it does not fail content PRs.

**Posture score — OpenSSF Scorecard** (`.github/workflows/scorecard.yml`):
weekly + on push to `main`; publishes to the public Scorecard API and uploads
SARIF to code scanning. Target ≥8.

**Secret scanning + push protection:** enabled at the repo level (GitHub native).
Push protection blocks commits that contain detected secrets.

**SRI correctness gate** (`tests/validation/test_sri_integrity.py`): recomputes
`base64(sha256(file))` for every `integrity="sha256-…"` asset reference and fails
the build on any mismatch or unresolvable local reference. Runs in `build.sh`
alongside `test_csp_strict.py`, so it gates inside the CI build job.

CSP enforcement (no `unsafe-inline`, per-page inline JSON-LD hashes present) was
already covered by `test_csp_strict.py`; this ADR adds the missing SRI half.

## Consequences

- **+** Continuous static analysis + a public supply-chain score + leaked-secret
  prevention + provable SRI integrity.
- **+** CodeQL/Scorecard are informational (Security tab), so they don't block
  the content workflow; the SRI gate *does* block (it's a correctness invariant).
- **−** CodeQL adds ~10 min when code paths change (path-filtered to avoid
  content-only PRs). Scorecard may initially score <8 until actions are pinned by
  SHA and branch-protection required-checks land (Phase 0.4 handoff).
