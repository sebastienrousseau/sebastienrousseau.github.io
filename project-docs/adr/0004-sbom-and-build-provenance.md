# ADR-0004: CycloneDX SBOM + SLSA build provenance

**Site:** sebastienrousseau.com
**Author:** Sebastien Rousseau
**Status:** Accepted
**Date:** 2026-06-26
**Related:** [Improvement Plan 2026](../improvement-plan-2026.md) Phase 2.1 / 2.2; [ADR-0002](0002-pin-build-toolchains.md)

---

## Context

`security.md` claimed *"Every build emits a CycloneDX SBOM at `/sbom.cdx.json`…"*
but **no SBOM was ever generated** — a verifiably false provenance claim, worse
than silence. The site also signs content with sigstore (optional pass) but
produced **no build-provenance attestation** for the deployed artifact, leaving a
gap against 2026 supply-chain norms (SLSA, `gh attestation verify`).

## Decision

**SBOM.** CI generates a CycloneDX 1.6 SBOM of the *resolved runtime build
dependencies* on every deploy, via `scripts/security/gen-sbom.sh`:

1. Install `requirements.txt` into a clean throwaway venv — so dev/test tooling
   (ruff, mypy, pytest, pip-audit) never appears as a "project dependency".
2. `cyclonedx-py environment` over that venv → `public/sbom.cdx.json`.
3. Validate before it ships: well-formed CycloneDX, every declared runtime
   dependency present, every component versioned. A failure fails the build job.

`cyclonedx-bom==7.3.0` is pinned (ADR-0002 discipline).

**Provenance.** The `finalise` job (main only) runs
`actions/attest-build-provenance@v4` over `public/sbom.cdx.json`, producing a
SLSA attestation tied to the repo, workflow, and commit. The job carries
`attestations: write` + `id-token: write`. Verify with:

```
gh attestation verify public/sbom.cdx.json \
  --repo sebastienrousseau/sebastienrousseau.github.io
```

## Consequences

- **+** The documented SBOM is now real and validated; doc/reality drift closed.
- **+** The deployed SBOM has verifiable build provenance.
- **−** No per-component hashes yet — `requirements.txt` uses version ranges, so
  hashes need `--hash` pinning (tracked as a Phase 2 follow-up). Versions are
  present; hashes are the remaining gap.
- **Scope:** the SBOM covers the Python build pipeline's runtime deps. The Rust
  `ssg` toolchain is pinned separately (ADR-0002); folding it in as a component
  is a possible enhancement.
