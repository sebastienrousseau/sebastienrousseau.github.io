<!-- SPDX-License-Identifier: Apache-2.0 -->

# Governance

This document describes how decisions are made in this project, who holds which
role, and what happens if the person holding a role becomes unavailable.

It is deliberately honest about the project's size. This is a
single-maintainer project. Writing that down is more useful to a prospective
contributor than describing a committee that does not exist.

## Governance model

**Benevolent dictator, single maintainer.** Sebastien Rousseau owns the
technical direction and has the final say on what is merged. There is no
steering committee, no voting, and no formal RFC process, because at the
current size those would be ceremony rather than governance.

Decisions are made in the open:

- Substantive changes land through pull requests on `main`, never by direct
  push. Branch protection enforces this.
- Design decisions with long-term consequences are recorded as numbered
  Architecture Decision Records under [`project-docs/adr/`](project-docs/adr/).
  An ADR states the context, the decision, and the consequences — including the
  ones that turned out badly.
- Disagreement is resolved in the pull request or issue thread. If consensus is
  not reached, the maintainer decides and records why.

## Key roles and who holds them

| Role | Holder | Responsibilities |
| --- | --- | --- |
| **Maintainer / project lead** | Sebastien Rousseau ([@sebastienrousseau](https://github.com/sebastienrousseau)) | Technical direction; final review and merge; releases; the CI gate set; responding to issues and pull requests. |
| **Security contact** | Sebastien Rousseau | Receiving and triaging vulnerability reports per [`SECURITY.md`](SECURITY.md); coordinating disclosure. |
| **Code of Conduct contact** | Sebastien Rousseau | Receiving and acting on Code of Conduct reports per [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md). |
| **Release manager** | Sebastien Rousseau | Tagging releases and maintaining [`CHANGELOG.md`](CHANGELOG.md). |
| **Contributor** | anyone | Opening issues and pull requests under [`CONTRIBUTING.md`](CONTRIBUTING.md). |

All four maintainer-side roles are currently held by one person. See
**Bus factor** below for what that means and what mitigates it.

## How to become a maintainer

There is no secret process. A contributor who lands several substantive changes,
reviews others' work usefully, and shows good judgement about when *not* to
change something will be invited to become a maintainer with commit rights. If
you want this, say so in an issue — the project would benefit from a second
maintainer and the maintainer is not precious about it.

## How decisions get made

1. **Routine changes** — a fix, a translation, a dependency bump. Open a pull
   request. It merges when the gates pass and the maintainer approves.
2. **Behaviour changes** — anything a reader or a downstream consumer would
   notice. Same as above, plus the test that would have caught the bug, in the
   same pull request.
3. **Structural decisions** — anything that would be expensive to reverse: a new
   locale, a URL scheme, a build-pipeline stage, a security control. These get
   an ADR before or alongside the change.

## Bus factor

**The bus factor of this project is 1.** One person can review and merge, holds
the deployment credentials, and is the security and Code of Conduct contact.
That is a genuine risk and this document does not pretend otherwise.

What reduces the damage if that person disappears:

- **The project is fully reproducible from this public repository.** The site is
  a static build: `./build.sh` regenerates every published page from the content
  and code in this repository. Nothing essential lives only on a laptop or only
  in a CI secret.
- **The licences permit anyone to continue it.** The code is Apache-2.0 OR MIT.
  Any person or organisation can fork the repository and carry on without asking
  permission, including publishing under their own domain.
- **The build has no proprietary dependency.** Every build tool is FLOSS, every
  Python dependency is hash-pinned in a committed lock file, and every GitHub
  Action is pinned to a commit SHA. A fork can reproduce the build years later.
- **The decisions are written down.** The ADR series, `project-docs/`, and the
  commit history record *why* things are the way they are, not just what they
  are. A successor does not have to reverse-engineer intent.
- **The gates encode the standards.** Someone taking over does not need to know
  the maintainer's preferences: the CI gate set — linting, a `mypy --strict`
  tier, a complexity ceiling, 100% coverage on the core library packages, and
  the build-time validation gates — will reject a change that violates them.

What is *not* mitigated: only the maintainer can currently merge to `main`,
publish a release, or receive a private vulnerability report. Recruiting a
second maintainer is the fix, and it is an open invitation (above).

## Access and continuity

- **Source of truth**: this public GitHub repository. Losing any local machine
  loses nothing that is not already pushed.
- **Deployment**: GitHub Pages, driven by GitHub Actions from `main`. The
  workflow definitions are in the repository; only the account credentials are
  external.
- **Credentials**: deployment secrets live in GitHub Actions secrets, not in the
  repository. A Cloudflare KV write audit runs in CI to catch accidental
  exposure.
- **Domain**: `sebastienrousseau.com` is registered to the maintainer. A fork
  can publish under a different domain without any change to the build.

## Changing this document

By pull request, like everything else.
