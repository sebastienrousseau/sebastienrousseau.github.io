<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Packaging and Supply Chain

This document specifies the packaging architecture, artifact formats, and supply chain verification for sebastienrousseau.com.

## Architecture overview

The repository produces three distinct deployable and publishable units:

1. **Static Publication (`public/`)**: Pre-rendered static assets and HTML pages across 28+ languages, deployed to GitHub Pages and cached globally by Cloudflare.
2. **Edge Router Worker (`workers/`)**: Cloudflare Worker (`lang-router.js` and `clock.js`) providing language negotiation, dynamic SVG generation, and edge security headers.
3. **Interactive WASM Labs (`labs/`)**: Rust crates compiled to WebAssembly targets with CSP hashes embedded into layouts.

## Static site packaging

Static output is compiled to the `public/` directory via `./build.sh` or `make build`:

```bash
make build
```

Every build executes:
- Rust static site compiler (`ssg`) for English template rendering.
- Python translation engine (`build_translations.py`) for multi-locale rendering.
- 25+ automated postbuild passes (`postbuild.py`) injecting metadata, SRI hashes, canonical links, and Schema.org graphs.
- Strict validation gates blocking build completion upon any broken internal link, invalid JSON-LD entity, or missing translation parity.

## Cloudflare Worker packaging

Edge routing and dynamic asset endpoints live in `workers/`:

- Manifest: `workers/wrangler.toml`
- Entry points: `workers/lang-router.js`, `workers/clock.js`
- Test suite: `workers/test_lang_router.mjs`, `workers/test_clock.mjs`

Local validation runs under Node.js:

```bash
node --test workers/test_*.mjs
```

## Software Bill of Materials (SBOM)

A CycloneDX Software Bill of Materials is generated on every build:

```bash
make sbom
```

Output: `public/sbom.cdx.json`
- Specification: CycloneDX 1.5 (JSON)
- Scope: Python generator dependencies, Node.js tooling, and Rust compiler components.
- Hashes: SHA-256 for all resolved dependencies.

## Sigstore article signing

Every research article published to the site carries a cryptographically verifiable Sigstore bundle under `sigstore-bundles/`:

- Attestation format: Sigstore bundle (bundle v0.3 / cosign format)
- Verification script: `scripts/security/sigstore_sign.py --verify`
- Public identity: Bound to GitHub Actions OIDC issuer and repository commit SHA.

Verification command:

```bash
python3 scripts/security/sigstore_sign.py --verify --bundle sigstore-bundles/<slug>.sigstore.json <rendered_html_path>
```
