<!-- SPDX-License-Identifier: Apache-2.0 -->

# Roadmap

What this project intends to do, and deliberately not do, over the next year
(to 2027-08). It is reviewed when a phase completes; the date above each
section is when it was last revised.

The detailed plans behind these headings live in
[`project-docs/improvement-plan-2026.md`](project-docs/improvement-plan-2026.md)
and
[`project-docs/developer-experience-plan-2026.md`](project-docs/developer-experience-plan-2026.md).

*Last revised: 2026-08-30.*

## What this project is

The static-site pipeline behind <https://sebastienrousseau.com> — long-form
research on applied AI, ISO 20022 payments and post-quantum cryptography for
financial services, published in 35 languages, plus the open-source tooling that
builds it.

## Intended — next 12 months

### Internationalisation

- **Localise the static-page slug maps.** Seven locales (`fa`, `mr`, `ta`, `te`,
  `ms`, `el`, `hu`) still serve English static-page slugs — `/hu/about/` where
  Dutch serves `/nl/onderzoek/`. This needs redirects designed in, since it
  renames live URLs. The article-slug backlog is already closed at 0%.
- **Keep the title and body gates at zero.** The localised-title backlog is
  closed; the ratchets exist so it cannot silently reopen.

### Supply chain and security

- **Raise the OpenSSF Scorecard score** where the remaining checks are honestly
  movable. `Code-Review` and `Contributors` are not, while the project has one
  maintainer — see [Governance](GOVERNANCE.md#bus-factor).
- **Keep every dependency hash-pinned** and every GitHub Action SHA-pinned, with
  advisories resolved by bumping the pin and regenerating the lock.
- **Extend coverage-guided fuzzing** beyond the front-matter parser and the slug
  deriver to the other text-transforming passes.

### Quality

- **Widen the `mypy --strict` tier** outward from `scripts/lib` and
  `postbuild_lib` until it covers the whole build pipeline.
- **Raise overall statement coverage** from its current 67% across `scripts/`.
  The two core library packages are held at 100% and gated; the gap is the
  one-shot editorial and maintenance utilities.
- **Keep the build byte-identical on rebuild.** The reproducibility gate exists
  and the build clock is pinned; this must not regress.

### Content and reader experience

- Interactive index scorecards and real on-site search, per the
  developer-experience plan.
- A published content API with an OpenAPI description.

### Governance

- **Recruit a second maintainer.** This is the single highest-value change
  available to the project and the precondition for a bus factor above 1.

## Explicitly not intended

Saying what a project will *not* do is as useful as saying what it will.

- **No user accounts, authentication, or comments.** The site stores no
  credentials and performs no cryptographic operations at runtime. This is a
  deliberate constraint that keeps a large class of vulnerabilities out of
  scope, and it will not change.
- **No server-side application.** The published output stays a static site. Edge
  routing is the only exception, and it stays minimal.
- **No tracking or advertising.** Analytics stay anonymous and aggregate.
- **No bespoke cryptography.** Where cryptography is discussed it is
  NIST-standard primitives in the separately published libraries, never an
  implementation invented here.
- **No new locales** until the existing 34 are free of English leakage. Breadth
  at the cost of quality is not an improvement.
- **No dependency added for convenience.** Every runtime dependency runs on
  every build; the list stays short and hash-pinned.

## How to influence this

Open an issue. The roadmap is not a contract, and an argument backed by a
concrete use case will change it.
