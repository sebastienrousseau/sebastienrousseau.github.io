# Security

> Last Updated: June 4, 2026

This guide defines the safety plans and threat models for the Sebastien Rousseau web site, where every dated post uses strong rules to protect readers.

## Contents

This guide covers the threat model, quantum transit safety, content rules, asset hashes, response headers, software lists, supply-chain safety, reports, and build checks.

## Threat model

The threat model diagram shows the entry points and safety borders of the site.

```mermaid
%%{init: {'theme':'neutral'} }%%
graph TB
 subgraph EXT["External"]
 V[/"Visitor"/]
 AI[/"AI crawler"/]
 ATK[/"Attacker /<br/>nation-state"/]
 end

 subgraph EDGE["Cloudflare edge (TLS termination)"]
 PQ["X25519MLKEM768<br/>(NIST FIPS 203)"]
 CFW["lang-router Worker"]
 TR["Transform Rules<br/>HSTS · X-Frame · COOP · CORP"]
 CDN["CDN cache<br/>(stale-while-revalidate)"]
 end

 subgraph ORIG["GitHub Pages origin"]
 H["public/ (static HTML,<br/>Pages artifact)"]
 SBOM["sbom.cdx.json"]
 WKD["openpgpkey/<br/>(WKD)"]
 end

 subgraph CSP["Per-page browser enforcement"]
 SRI["SRI on /_csp/*"]
 JLD["JSON-LD sha256<br/>allowlist"]
 SR["speculation-rules<br/>keyword"]
 FA["frame-ancestors<br/>'none'"]
 end

 V --> PQ
 AI --> PQ
 ATK -.->|harvest-now-<br/>decrypt-later| PQ
 ATK -.->|XSS / injection| CDN
 ATK -.->|supply-chain| CDN
 PQ --> CFW
 CFW --> TR
 TR --> CDN
 CDN --> H
 CDN --> SBOM
 CDN --> WKD
 H --> SRI
 H --> JLD
 H --> SR
 H --> FA
 ```

The system stops quantum decoding threats by using hybrid key setups, which protect saved sessions from future decodes.
We block web-based script attacks by using a strict content safety policy that allows only signed script blocks.
Our defense against supply-chain hacks relies on public package lists and real asset trust hashes on every file.
We prevent page hijacking attacks by setting frame limits on all outgoing page headers.
Finally, the site blocks transit safety downgrades by enforcing preload rules on the edge server.

What is explicitly not in scope:

The site delegates distributed denial of service protection to the network layer of the edge host.
We omit user login features because the site contains no accounts.
Server-side check is not needed since the site runs as a static resource.

## Transport layer (PQC TLS)

The transport layer uses hybrid quantum keys to secure all user traffic.

Cloudflare's edge agrees the quantum hybrid keys, while classical keys stay as fallback for legacy clients.
The modern browser clients agree the quantum rules with ease without breaking older systems.

| Client | PQC negotiation |
|---|---|
| Chrome 124+ | [x] X25519MLKEM768 |.
| Firefox 132+ | [x] X25519MLKEM768 |.
| Safari 18+ | [x] X25519MLKEM768 |.
| Older browsers | Falls back to X25519 — no breakage |.

Verification curves:

```bash
echo | openssl s_client -connect sebastienrousseau.com:443  -tls1_3 -curves X25519MLKEM768 2>/dev/null  | grep -E 'Server (Temp|public) Key|TLS_'
```

Configure in the dashboard by enabling quantum hybrid transport safety.

## Content Security Policy (CSP)

The site uses a strict Content Security Policy to prevent cross-site scripting attacks.

Shipped via tag on every page:

```
default-src 'self';
base-uri 'self';
form-action 'self' https://formspree.io;
object-src 'none';
upgrade-insecure-requests;
script-src 'self' 'inline-speculation-rules'
 'sha256-<per-page-hash>'…
 https://www.google-analytics.com
 https://www.googletagmanager.com
 https://www.google.com
 https://www.gstatic.com
 https://open.spotify.com
 https://static.cloudflareinsights.com
 https://challenges.cloudflare.com
 https://ajax.cloudflare.com;
frame-src 'self' https://www.google.com
 https://open.spotify.com
 https://www.youtube.com
 https://www.youtube-nocookie.com;
connect-src 'self'
 https://www.googletagmanager.com
 https://www.google-analytics.com
 https://region1.google-analytics.com
 https://www.google.com
 https://stats.g.doubleclick.net
 https://open.spotify.com;
img-src 'self' data: blob:
 https://cloudcdn.pro
 https://pacs008.com
 https://www.googletagmanager.com
 https://i.scdn.co;
style-src 'self'
 'sha256-47DEQpj…='
 https://fonts.googleapis.com;
font-src 'self' https://fonts.gstatic.com;
media-src 'self' https://p.scdn.co https://*.scdn.co;
```

Key design choices:

- Choice 1: No `unsafe-inline` for scripts, where per-page inline JSON-LD blocks are allowed strictly by SHA-256 hash. The script computes each block's hash at build time and folds it into the page's policy.
- Choice 2: We use the 'inline-speculation-rules' keyword for the Speculation Rules block, which also carries its own hash as belt-and-braces.
- Choice 3: The `img-src` directive enumerates four origins and permits no blanket `https:` rules. The CSP-strict gate fails on any reintroduction of `https:` as a bare allow.
- Choice 4: The `frame-ancestors 'none'` rule is set via the Cloudflare Worker response header.

### Header CSP vs meta CSP: the dual-layer model

The same CSP shape is set twice — once as a tag inside every page (with per-page sha256 hashes for inline JSON-LD), and once as an HTTP response header by the Worker.
The Worker header carries rules that only work at the response layer: HSTS, COOP, Referrer-Policy, X-Content-Type-Options.

### WASM-labs CSP carve-out

Lab pages add 'wasm-unsafe-eval' to script-src in their own per-page meta CSP, which permits WebAssembly execution without weakening the global rule.

---

## Subresource Integrity (SRI)

We use Subresource Integrity hashes to verify the safety of all loaded styles and scripts.

Every script and style tag carries a secure hash of its actual file content.
The build tool replaces placeholder tags with real hashes made during site creation.

---

## Security headers

The edge server sets HTTP security headers on all responses to protect visitors.

The edge router sets headers for transit safety, referrer rules, permissions, and framing limits.
These rules help browsers block common tracking scripts and data leaks.

| Header | Value |
|---|---|
| `Strict-Transport-Security` | `max-age=63072000; includeSubDomains; preload` |
| `Cross-Origin-Opener-Policy` | `same-origin` |
| `X-Content-Type-Options` | `nosniff` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |.
| `Permissions-Policy` | `browsing-topics=(), interest-cohort=(), camera=(), microphone=(), geolocation=()` |.
| `Content-Security-Policy` | full strict CSP |.

Validation tests:

```bash
open "https://observatory.mozilla.org/analyze/sebastienrousseau.com"
```

---

## Software Bill of Materials (SBOM)

The build pipeline publishes a CycloneDX Software Bill of Materials to document project dependencies.

Every build emits a CycloneDX SBOM at /sbom.cdx.json to provide file hashes for downstream audits to check supply-chain safety.

---

## Supply-chain provenance

We secure the supply chain using signed git commits and branch protection rules.

| Surface | Posture |
|---|---|
| **Signed commits** | Every commit on `main` is signed, and unsigned commits cannot reach the branch due to protection rules |.
| **Branch protection** | The branch requires a green CI run and reviewed PR, which blocks force-push actions |.
| **CycloneDX SBOM** | Published on every build to track packages |.
| **Sigstore attestation** | Optional pass at `scripts/sigstore_sign.py` to sign files |.
| **Dependency review** | Dependabot watches the requirements file for security warnings |.

---

## Responsible disclosure

If you find a security bug in the project, please report it privately by email.

You can send your report to the contact email address using our public key.
Standard tools will resolve the key with ease using the web key directory.

---

## CI-enforced regressions

The integration runner validates security rules on every commit to block bugs.

Three automated gates verify the content policies, schema structures, and internal links.
Any change that weakens these rules fails the build check immediately.

| Gate | Asserts | File |
|---|---|---|
| `test_csp_strict.py` | CSP has no `unsafe-inline`/`unsafe-eval` | `tests/validation/test_csp_strict.py` |.
| `validate_jsonld.py` | JSON-LD shapes match required properties | `scripts/validate_jsonld.py` |.
| `audit_links.py` | Internal links resolve to a real file | `scripts/audit_links.py` |.

Any future change that loosens these fails the build before it can land on main.
