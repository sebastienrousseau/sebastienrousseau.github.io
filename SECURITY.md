<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Security Policy

## Reporting a Vulnerability

Report vulnerabilities privately to **sebastian.rousseau@gmail.com** (PGP key at [`/.well-known/openpgpkey/hu/`](https://sebastienrousseau.com/.well-known/openpgpkey/hu/)). Machine-readable disclosure metadata lives at [`/.well-known/security.txt`](https://sebastienrousseau.com/.well-known/security.txt) per [RFC 9116](https://www.rfc-editor.org/rfc/rfc9116).

Please do **not** open a public GitHub issue for a suspected vulnerability: email first, and we will coordinate disclosure.

## Response SLA

* **Initial Acknowledgement**: Within 48 hours of report receipt.
* **Assessment & Triage**: Within 5 business days, confirming vulnerability scope and impact.
* **Remediation & Coordinated Disclosure**: Security fixes are published on a fast-track release branch before public disclosure.

## Scope & Supported Versions

| Component | Status | Supported Version |
| :--- | :--- | :--- |
| Static Site & Generators | Supported | Latest release on `main` |
| Cloudflare Edge Workers | Supported | Latest release in `workers/` |
| Fly.io PDF Render Container | Supported | Latest release in `fly/pdf-render/` |

The detailed threat model, architectural safeguards, and past vulnerability disclosures are documented in [`docs/security.md`](docs/security.md) and [`docs/threat-model.md`](docs/threat-model.md). See [`/about/#security`](https://sebastienrousseau.com/about/#security) for public acknowledgements.
