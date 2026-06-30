# ADR-0009: Sign published articles with Sigstore

**Site:** sebastienrousseau.com
**Author:** Sebastien Rousseau
**Status:** Accepted
**Date:** 2026-06-26
**Related:** [Improvement Plan 2026](../improvement-plan-2026.md) Phase 2 / 5; [ADR-0004](0004-sbom-and-build-provenance.md); runbook [`sigstore.md`](../sigstore.md)

---

## Context

ADR-0004 established supply-chain provenance for the *build* (SBOM + SLSA
attestation). The published *content* warranted the same: a reader, citing
author, or auditor should be able to verify that an article's bytes are the
ones that were published, not silently altered afterwards. The site already
markets "signed, dated articles", so the claim needed a verifiable mechanism
behind it.

## Decision

Sign every dated article with **Sigstore**. `build.sh` runs
`scripts/security/sigstore_sign.py` near the end of the pipeline (step 19;
ADR-0007 / architecture.md):

- The pass is a **no-op unless `_data/sigstore/config.json` exists**, so a
  default build (and contributor forks) never fail for lack of signing
  credentials — it logs `signing skipped` and continues.
- Committed signature bundles live in `sigstore-bundles/` and are copied into
  `public/sigstore/` at build time; a local signed build refreshes the bundles,
  which are then committed (the one generated artefact ADR-0007 allows in a
  commit).
- The verification workflow (how to check a signature, what each bundle
  contains) is documented in the runbook `project-docs/sigstore.md`.

## Consequences

- **+** Content provenance is verifiable, not asserted — the "signed articles"
  claim is backed by checkable signatures.
- **+** Decoupled from CI secrets: signing is opt-in via local config, so the
  public build stays green without any Sigstore credentials in CI.
- **−** Signatures are refreshed by a local signed build, not CI, so
  `sigstore-bundles/` can lag if a signed build isn't run after content
  changes; the bundle copy is best-effort and must not block the deploy.
