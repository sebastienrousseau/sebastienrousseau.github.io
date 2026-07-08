<!-- SPDX-License-Identifier: Apache-2.0 -->

# Threat model

A structured view of what this project protects, the boundaries an attacker
would have to cross, and the controls already in place. It complements the
operational detail in [`security.md`](security.md) and the scanning suite in
[`adr/0005-security-scanning-suite.md`](adr/0005-security-scanning-suite.md).

This is a **static content site** — there is no application backend holding user
data, no authenticated session, and no database. That shapes the model: the
prize for an attacker is not data exfiltration but **integrity of the published
artifact** and **the supply chain that produces it**.

## Assets

| Asset | Why it matters |
|---|---|
| Published site (`public/` on GitHub Pages) | The thing readers trust; integrity is the primary asset. |
| Source + build pipeline | Compromise here forges signed, trusted output at scale. |
| Signing keys / OIDC identity (sigstore) | Provenance of every article and build. |
| Cloudflare KV (search/routing state) | Availability + free-tier budget ([`adr/0001-kv-free-tier-policy.md`](adr/0001-kv-free-tier-policy.md)). |
| `fly/pdf-render` service | Renders first-party HTML to PDF; a lateral surface. |

## Trust boundaries

1. **Contributor → repository.** Signed commits + PR review + required CI gates.
2. **Repository → CI runner.** Pinned toolchains; no long-lived secrets; no
   `ANTHROPIC_API_KEY` in CI.
3. **CI → GitHub Pages.** Build-from-source + `upload-pages-artifact`
   ([`adr/0007-docs-to-public-deploy.md`](adr/0007-docs-to-public-deploy.md)).
4. **Site → browser.** Hash-strict CSP + SRI + Worker-set headers.
5. **Site → third parties** (fonts CDN, reCAPTCHA, Spotify). Constrained by CSP
   allow-lists.

## Threats and mitigations

| # | Threat | Mitigation (in place) |
|---|---|---|
| T1 | **Supply-chain compromise** — malicious dependency or build step injects content. | Pinned toolchains (ADR-0002); SBOM + provenance (ADR-0004); OpenSSF Scorecard + CodeQL + Dependabot (ADR-0005); **sigstore signing** of every article/build (ADR-0009). |
| T2 | **Cross-site scripting** via injected markup in content or translations. | **Hash-strict CSP** (no `unsafe-inline` for scripts; per-page inline-JSON-LD hashes) + **SRI** on subresources; `test_csp_strict` + `test_meta_description_clean` build gates. |
| T3 | **Malicious/broken translation** across 27 locales (RTL override, tag breakage, EN leakage). | `check_voice` editorial gate; `tests/validation/` gates for i18n leakage, hreflang, RTL safety, JSON-LD `inLanguage`. |
| T4 | **Known-vulnerable dependency** shipped. | Dependabot alerts + grouped update PRs; security dashboard held at **0 open**. Un-patchable advisories are triaged and documented (e.g. WeasyPrint CSS-injection — no upstream fix; the renderer only processes first-party trusted content, so the vector is unreachable). |
| T5 | **Canonical / structured-data poisoning** degrading SEO or misrepresenting authorship. | `test_canonical_consistency`, JSON-LD validation, news-sitemap de-duplication gates. |
| T6 | **Secret leakage** through CI logs or committed files. | No secrets in workflows/env; translation runs on the maintainer's subscription, never a repo secret; gitleaks-style hygiene. |
| T7 | **KV abuse / cost overrun** (availability + budget). | Free-tier policy + burndown monitoring (ADR-0001, `kv-burndown.yml`). |
| T8 | **Deploy bypass** — merging around required checks. | Signed commits + required status checks. *Residual: admin-merge can bypass — see below.* |

## Residual risks / accepted

- **Admin-merge bypass (T8).** Repository admins can merge past required checks.
  *Planned control:* enable branch-protection "require status checks" without
  admin exemption. Until then, this is an accepted, monitored risk.
- **Local-vs-CI build drift.** The pinned `ssg` emits benign local warnings that
  do not reproduce in CI; merge readiness is defined by CI, not local output.
  Being retired by the native-migration spec.
- **Third-party embeds** (reCAPTCHA, Spotify, fonts) execute under CSP
  allow-lists; a compromise of an allow-listed origin is out of scope for
  first-party controls.

## Review cadence

Revisit this model when a new external integration, a new data store, or a new
deploy path is introduced — see the trust-boundary list as the trigger.
