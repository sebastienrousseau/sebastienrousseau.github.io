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

The CI deploy publishes a CycloneDX Software Bill of Materials documenting the
resolved runtime build dependencies.

Each deploy emits a CycloneDX 1.6 SBOM at `/sbom.cdx.json`. It is generated by
`scripts/security/gen-sbom.sh`, which installs `requirements.txt` into a clean
throwaway environment (so dev/test tooling never pollutes the artifact) and
records every resolved runtime component with its exact version. CI validates
the SBOM (well-formed CycloneDX, every declared runtime dependency present, all
components versioned) before it ships, and attaches a SLSA build-provenance
attestation to it — see ADR-0004. Verify with:

```
gh attestation verify public/sbom.cdx.json \
  --repo sebastienrousseau/sebastienrousseau.github.io
```

> The human-edited `requirements.txt` keeps version *ranges* for low-friction
> dependency bumps; CI installs from the hash-pinned `requirements.lock`
> (`pip install --require-hashes`, regenerated by `scripts/security/lock-deps.sh`)
> so every wheel is verified by SHA-256 before install. See "Batch 7" under
> CodeQL remediation for the full lock set.

---

## Supply-chain provenance

We secure the supply chain using signed git commits and branch protection rules.

| Surface | Posture |
|---|---|
| **Signed commits** | Every commit on `main` is signed, and unsigned commits cannot reach the branch due to protection rules |.
| **Branch protection** | The branch requires a green CI run and reviewed PR, which blocks force-push actions |.
| **CycloneDX SBOM** | Published on every CI deploy at `/sbom.cdx.json` (resolved runtime deps, validated in CI) — ADR-0004 |.
| **SLSA build provenance** | `actions/attest-build-provenance` attests the deployed SBOM; verify with `gh attestation verify` — ADR-0004 |.
| **Sigstore attestation** | Optional pass at `scripts/security/sigstore_sign.py` to sign files |.
| **Static analysis (CodeQL)** | `security-and-quality` queries over Python + JS on code-touching PRs and weekly — ADR-0005 |.
| **Supply-chain score (OpenSSF Scorecard)** | Weekly + on push to `main`, published to the public Scorecard API — ADR-0005 |.
| **Secret scanning + push protection** | Enabled repo-wide; push protection blocks commits containing detected secrets |.
| **SRI correctness gate** | `tests/validation/test_sri_integrity.py` recomputes every integrity hash from file bytes — ADR-0005 |.
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

## CodeQL remediation (Phase 4)

CodeQL (`security-and-quality`, ADR-0005) runs on every push. The open
alerts are being remediated in severity order; each fix is verified by the
next scan and, where the code is in the main test scope, by a unit test.

**Batch 1 — critical + regex (done):**

| Alert | Where | Fix |
|---|---|---|
| `py/partial-ssrf` (critical) | `fly/pdf-render/app.py` | Re-validate the slug against `^[a-z0-9][a-z0-9-]{0,127}$` at the network sink before building the outbound URL, so the request host can never be attacker-influenced. |
| `py/log-injection` (medium ×2) | `fly/pdf-render/app.py` | The same charset guard makes the logged value provably free of CR/LF control characters. |
| `py/uninitialized-local-variable` (error) | `fly/pdf-render/app.py` | The fetch error path now `raise`s a `werkzeug` `BadGateway` instead of `abort()`, so `res` is unambiguously bound on the success path. |
| `py/regex/unmatchable-caret` / `-dollar` (error ×6) | `build_translations/_maps.py` | Replace the "match nothing" sentinel `r"$^"` with the canonical always-fails regex `r"(?!)"` (unit-locked in `tests/unit/test_maps_never_match.py`). |

**Batch 2 — high (done):**

| Alert | Where | Fix |
|---|---|---|
| `py/bad-tag-filter` (high ×3) | `_search.py`, `postbuild.py`, `test_lang_no_leakage.py` | Dismissed as "won't fix": these regexes strip tags from our **own build-generated HTML** (`public/` output), not untrusted input, so the bypass is not reachable; a full HTML parser is disproportionate for build tooling. `_extract_visible_text` is now unit-covered (`tests/unit/test_search_extract.py`). |
| `js/xss-through-dom` (high) | `_layouts/main.js` | The tag-filter `<select>` value is validated against `^[a-z0-9-]+$` before it reaches `location.href`; anything else falls back to the base listing. |
| `js/missing-origin-check` (medium) | `_layouts/sw.js` | The service-worker `message` handler ignores messages whose `event.origin` is not same-origin. |
| `js/xss-through-exception` (medium) | `labs/hsh-demo/web/demo.js` | The boot-error node is built with `textContent`, so an exception message can never be parsed as HTML. |
| `py/incomplete-url-substring-sanitization` (high ×6) | `test_schemas.py`, `test_postbuild_furniture.py` (×4) | Test assertions tightened to full-URL prefixes (`https://…/`). The remaining instance in `pa11y_cache.py` is page-content detection, not a URL security boundary, and is dismissed in code-scanning as a false positive (documented inline). |

**Batch 3 — OpenSSF Scorecard pinned dependencies (done):** every GitHub
Action across the nine workflows is pinned to a full commit SHA with the
version as a trailing comment (e.g. `actions/checkout@9c091bb… # v7`),
clearing the 26 `PinnedDependenciesID` findings. Bump deliberately by
re-resolving the tag → SHA (ADR-0002 philosophy).

**Batch 4 — unused module-private constants (done):** of the 52
`py/unused-global-variable` notes, a repo-wide reference scan split them into
two sets. **13 genuinely dead** module-level constants — whose only repo
reference was their own definition — were deleted (`_QUOTED_RE`,
`_DATE_FM_RE`, the four `_BLOGPOSTING_*_RE` regexes, `_CDN_TRANSFORM_PREFIX`,
`_NAV_LINK_RE`, `_STATIC_EN_TO_FR`, `_SVG_HEADPHONES/_MASTODON/_MEDIUM`, and a
test-only `_CRUMB_BASE`). The remaining **26 are false positives**: they are
shared `build_translations/_state.py` state and `_chrome.py` patch regexes
read by sibling modules via attribute access (`st.FR_TO_EN`, …) or mutated
through in-function `global` re-declarations — CodeQL's intra-module analysis
cannot see the cross-module reads, so they are kept and dismissed in
code-scanning with that rationale. The reference scan that proves the split is
reproducible (`grep -rwn <name> scripts/ tests/`).

**Batch 5 — import / definition / regex quality notes (done):**

| Alert | Where | Disposition |
|---|---|---|
| `py/repeated-import` (×2) | `article_furniture.py`, `seo.py` | Removed the redundant in-function `import json as _json`; the module-level import is in scope. |
| `py/import-and-import-from` (×2) | `article_furniture.py` | Dropped the local `import html as _h` in `_html_unescape` and the Mermaid helper; both now call the module-level `from html import unescape as _unesc`. |
| `py/constant-conditional-expression` | `test_schemas.py` | Removed a dead `... if False else ...` branch in the idempotence test; the assertion is unchanged. |
| `py/regex/duplicate-in-character-class` (×2) | `backfill_locale_frontmatter.py` | De-duplicated the Yoruba (24→16) and Latin (118→93) detection character classes; identical code-point coverage, verified by an `ast`-extracted match test. |
| `py/multiple-definition` (×2) | `build_case_studies.py`, `translate_stubs_gemini.py` | **Dismissed (false positive):** the "redefined" first assignment is the default kept when the wrapping `contextlib.suppress(...)` block raises — CodeQL does not model `suppress`. |
| `py/unused-import` (×3) | `postbuild.py` | **Dismissed (used in tests):** these are the documented `# noqa: F401` re-export surface (`from postbuild import slugify`, `pb.compute_word_count`, …) consumed by `tests/unit/test_postbuild_*`. |

**Batch 6 — remaining high/medium CodeQL (done):**

| Alert | Where | Disposition |
|---|---|---|
| `js/xss-through-dom` (high) | `_layouts/main.js` | The navigate-mode handler now validates **both** DOM-sourced inputs before they reach `location.href`: the `data-navigate-base` attribute against `^/[a-z0-9/-]+$` and the option value against `^[a-z0-9-]+$`. Either failing falls back to `/articles`. (The earlier batch only guarded the option value; `base` was the live taint.) |
| `py/log-injection` (medium ×2) | `fly/pdf-render/app.py` | **Dismissed (false positive):** the only logged user value is `slug`, validated against `^[a-z0-9][a-z0-9-]{0,127}$` at every entry sink (`render()` line 115, `_fetch_article_html` line 69) before reaching the `LOG.info` calls, so it provably contains no CR/LF/control characters. CodeQL's taint tracker does not model the regex `fullmatch` as a log-injection sanitizer. |

**Batch 7 — Scorecard Pinned-Dependencies, Python (done):** every CI `pip
install` is now hash-pinned. Three committed, uv-generated lock files carry a
`--hash` for every distribution of every (transitive) dependency:
`requirements.lock` (runtime, py3.12), `requirements-dev.lock` (runtime + CI
toolchain, py3.12), and `fly/pdf-render/requirements.lock` (PDF service,
py3.13). Workflows install with `pip install --require-hashes -r <lock>`, so a
tampered or substituted wheel fails the build. Locks are *universal* (every
platform's wheel hash) so the same file verifies on Linux CI and local macOS.
Regenerate after editing any `requirements*.txt` with
`scripts/security/lock-deps.sh`. This also resolves the SBOM hash follow-up
noted above. The `S104` bind-all in the Fly container is intentional and
outside the linted `scripts/ tests/` scope.

**Batch 8 — Scorecard Token-Permissions (done):** `refresh-gh-stats.yml` no
longer grants `contents: write` at the workflow top level; the token is
read-only by default and write is scoped to the single job that commits
`gh-stats.json`. All other workflows already use minimal top-level
`contents: read`.

**Phantom finding (dismissed):** Scorecard `Vulnerabilities` reported four
Pillow CVEs (PYSEC-2018-49 / 2021-142 / 2023-23 / 2023-24). Pillow is in **no**
manifest, Dependabot reports zero open alerts, and the dependency-graph SBOM
contains no Pillow — stale OSV data, not a present exposure.

**Remaining (owner action — GitHub *settings* only the owner can toggle):**
- **Branch protection** (`BranchProtectionID`, Phase 0.4): in
  *Settings → Branches → main*, require status checks to pass, require a PR
  before merging, and include administrators. See the step list below.
- **Code review** (`CodeReviewID`): scores 0/30 approved changesets because a
  solo maintainer admin-merges their own PRs and cannot self-approve. This is
  structural for a single-owner repo; **dismissed** as not-applicable until a
  second reviewer exists. Re-enable required reviews once one does.
- **Reasonable won't-fix for a static-site build repo:** `FuzzingID` (no
  fuzzable runtime surface), `CIIBestPracticesID` (external OpenSSF badge
  application), and `SASTID` (CodeQL already runs on every push/PR; the
  "8/27 commits" coverage self-heals as history rolls forward).

### Branch-protection steps (owner)

1. *Settings → Branches → Add branch ruleset* (or classic *Branch protection
   rule*) targeting `main`.
2. Enable **Require a pull request before merging** (1 approval once a second
   reviewer exists; until then leave approvals at 0 and keep admin-merge).
3. Enable **Require status checks to pass** and select: `Build + smoke tests +
   partition`, `Static analysis (lint, types, complexity)`, `CodeQL`,
   `Analyze python`, `Analyze javascript`, the four `pa11y shard` jobs, and
   `diff`.
4. Enable **Require branches to be up to date before merging** and **Require
   signed commits**.
5. Enable **Include administrators** for full coverage (note: this is what
   forces the `--admin` flag on solo merges today).

Any future change that loosens these fails the build before it can land on main.
