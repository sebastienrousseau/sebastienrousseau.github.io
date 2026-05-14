# Deployment configuration

The static site is served by GitHub Pages from `docs/`, with Cloudflare in
front as the CDN. A handful of security headers and the post-quantum TLS
key-exchange cannot be set from the static output — they have to be
configured in the Cloudflare dashboard. This file is the canonical
record so the configuration can be reproduced.

## Cloudflare configuration

### 1. Post-Quantum TLS (X25519MLKEM768)

The whole reason we write about PQC. Visitors using Chrome 124+, Firefox
132+ or Safari 18 negotiate a quantum-resistant key exchange.

**Path:** Cloudflare dashboard → `sebastienrousseau.com` → SSL/TLS →
**Edge Certificates** → enable **"Post-quantum hybrid TLS"**.

**Verify:**

```bash
# Confirm the X25519MLKEM768 hybrid is offered
echo | openssl s_client -connect sebastienrousseau.com:443 \
  -tls1_3 -curves X25519MLKEM768 2>/dev/null | grep -E 'Server (Temp|public) Key|TLS_'

# Browser sanity check
# Chrome → DevTools → Security tab → "Connection — secure connection settings"
# should list "Key exchange group: X25519MLKEM768"
```

Falls back to classical X25519 for clients that don't support PQ — no
risk of breaking legacy traffic.

### 2. HTTP response headers (Transform Rules)

Headers that must be set on the response itself, not via `<meta>`.

**Path:** Cloudflare dashboard → `sebastienrousseau.com` → Rules →
**Transform Rules** → **Modify Response Header** → "Create rule".

| Rule name | When | Set/Add |
|---|---|---|
| `strict-security-headers` | `(http.host eq "sebastienrousseau.com")` | See list below |

Headers to add (one Transform Rule with multiple "Set static" entries):

```
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Resource-Policy: same-origin
X-Frame-Options: DENY
Origin-Agent-Cluster: ?1
```

`Cross-Origin-Embedder-Policy` is **not** set — would break the
Spotify iframes on `/playlists/`. If a future version drops those, add
`Cross-Origin-Embedder-Policy: credentialless`.

`X-Content-Type-Options: nosniff` and `Referrer-Policy:
strict-origin-when-cross-origin` are already shipped via `<meta>` in
the HTML and don't need a Transform Rule.

### 3. HSTS preload submission

After step 2 has been deployed for at least 24 hours and confirmed in
production:

1. Visit https://hstspreload.org/?domain=sebastienrousseau.com
2. Submit. Cloudflare's HSTS header includes `preload` already, so the
   form should accept it on first try.

## Verification

After every Cloudflare change, run the audit:

```bash
# Mozilla Observatory — target A+
open "https://observatory.mozilla.org/analyze/sebastienrousseau.com"

# Security Headers — target A+
open "https://securityheaders.com/?q=sebastienrousseau.com"

# SSL Labs — target A+ with PQ extras
open "https://www.ssllabs.com/ssltest/analyze.html?d=sebastienrousseau.com"
```

## Headers shipped from the static output

These are emitted by the build pipeline (no Cloudflare configuration
required):

| Header | Source |
|---|---|
| `Content-Security-Policy` (strict, hash-based, no `'unsafe-inline'`) | `<meta http-equiv>` in `_layouts/index.html`; per-page JSON-LD hashes computed by `scripts/postbuild.py:inject_jsonld_hashes()` |
| `Permissions-Policy` (deny-by-default for ~40 permissions) | `<meta http-equiv>` |
| `X-Content-Type-Options: nosniff` | `<meta http-equiv>` |
| `Referrer-Policy: strict-origin-when-cross-origin` | `<meta name="referrer">` |

## Speculation Rules API

Every rendered page carries a `<script type="speculationrules">` block
that asks the browser to prerender same-origin pages on hover. Wired in
`scripts/postbuild.py:inject_speculation_rules()` and allowed by the CSP
via `'inline-speculationrules'` in `script-src`.

Excluded patterns: `/_csp/*` (assets), `*.xml`/`*.json`/`*.txt`/`*.pdf`
(static feeds and downloads), `/manifest.json`, `/sw.js`, and contact
pages (don't prerender forms).
