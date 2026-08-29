# OpenSSF Best Practices badge — prepared answers

The OpenSSF Scorecard check `CII-Best-Practices` scores 0 until this project
is registered at <https://www.bestpractices.dev> and has earned a badge.
Registration requires a GitHub OAuth sign-in by the repository owner, so it
cannot be automated. This file is the evidence gathered so the questionnaire
is a short exercise rather than a research one.

Register at <https://www.bestpractices.dev/en/projects/new>, then add the
badge ID to `README.md`; Scorecard picks it up from the API on its next run.

## Identification

| Field | Answer |
| --- | --- |
| Project name | Sebastien Rousseau |
| Homepage | <https://sebastienrousseau.com> |
| Repository | <https://github.com/sebastienrousseau/sebastienrousseau.github.io> |
| Description | Research and open-source tooling on applied AI, ISO 20022 payments and post-quantum cryptography for financial services, published as a statically generated multilingual site. |
| Programming languages | Python, Rust, JavaScript |
| CPE | not applicable — not distributed software |

## Basics

| Criterion | Answer | Evidence |
| --- | --- | --- |
| `description_good` | Met | `README.md` |
| `interact` | Met | `CONTRIBUTING.md` |
| `contribution` | Met | `CONTRIBUTING.md` |
| `contribution_requirements` | Met | `CONTRIBUTING.md` documents the gates a change must pass |
| `license_location` | Met | `LICENSE`, `LICENSE-APACHE`, `LICENSE-MIT` at the repository root |
| `floss_license` | Met | Apache-2.0 OR MIT (`SPDX-License-Identifier` in `LICENSE`) |
| `floss_license_osi` | Met | both are OSI-approved |
| `documentation_basics` | Met | `README.md`, `project-docs/architecture.md` |
| `documentation_interface` | Met | `project-docs/architecture.md` documents every build-pipeline script; `test_architecture_doc_current.py` fails the build if one is undocumented |
| `english` | Met | repository, issues and commits are in English |

## Change control

| Criterion | Answer | Evidence |
| --- | --- | --- |
| `repo_public` | Met | public GitHub repository |
| `repo_track` | Met | git |
| `repo_interim` | Met | every change lands through a pull request on `main` |
| `repo_distributed` | Met | git |
| `version_unique` | Met | site releases are continuous; each deploy is identified by its commit SHA |
| `release_notes` | Met | `CHANGELOG.md` and the generated `/changelog` page |
| `release_notes_vulns` | Met | security fixes are described in the commit that makes them |

## Reporting

| Criterion | Answer | Evidence |
| --- | --- | --- |
| `report_process` | Met | `CONTRIBUTING.md`, GitHub Issues |
| `report_tracker` | Met | GitHub Issues |
| `report_responses` | Met | issues are triaged by the maintainer |
| `enhancement_responses` | Met | as above |
| `report_archive` | Met | GitHub Issues history is public |
| `vulnerability_report_process` | Met | `SECURITY.md` |
| `vulnerability_report_private` | Met | `SECURITY.md` directs reporters to email, with a PGP key at `/.well-known/openpgpkey/` |
| `vulnerability_report_response` | Met | `SECURITY.md` states the response window |

## Quality

| Criterion | Answer | Evidence |
| --- | --- | --- |
| `build` | Met | `./build.sh`, `Makefile` |
| `build_common_tools` | Met | GNU Make, Python, Cargo, npm |
| `build_floss_tools` | Met | all FLOSS |
| `test` | Met | 1665 unit test functions plus 31 build-time validation gates |
| `test_invocation` | Met | `make test`, `make verify` |
| `test_most` | Met | `postbuild_lib` and `build_translations` are held at 100 % line coverage in CI |
| `test_continuous_integration` | Met | `.github/workflows/ci.yml` on every push and pull request |
| `test_policy` | Met | `CONTRIBUTING.md`: a behaviour change ships with the test that would have caught it |
| `tests_are_added` | Met | see the pull request history |
| `tests_documented_added` | Met | `CONTRIBUTING.md` |
| `warnings` | Met | `ruff`, `ruff format`, `mypy --strict` tier, a radon complexity gate with an empty allowlist |
| `warnings_fixed` | Met | the gates fail the build; the complexity allowlist is empty |
| `warnings_strict` | Met | as above |

## Security

| Criterion | Answer | Evidence |
| --- | --- | --- |
| `know_secure_design` | Met | `project-docs/architecture.md`, the ADR series |
| `know_common_errors` | Met | as above |
| `crypto_published` | Met | no bespoke cryptography; the published libraries use NIST-standard primitives |
| `crypto_call` | Met | no bespoke cryptography in this repository |
| `crypto_floss` | Met | as above |
| `crypto_keylength`, `crypto_working`, `crypto_weaknesses`, `crypto_pfs`, `crypto_password_storage`, `crypto_random` | N/A | the site stores no credentials and performs no cryptographic operations at runtime |
| `delivery_mitm` | Met | HTTPS with HSTS; dependencies are hash-pinned in `requirements.lock`, `requirements-dev.lock`, `fly/pdf-render/requirements.lock` and `fuzz/requirements.lock`; every GitHub Action is SHA-pinned |
| `delivery_unsigned` | Met | as above |
| `vulnerabilities_fixed_60_days` | Met | no known unpatched vulnerabilities; every pinned package is checked against OSV |
| `vulnerabilities_critical_fixed` | Met | as above |
| `no_leaked_credentials` | Met | no credentials in the repository; a Cloudflare KV write audit runs in CI |

## Analysis

| Criterion | Answer | Evidence |
| --- | --- | --- |
| `static_analysis` | Met | CodeQL on every push and pull request to `main`; `ruff`; `mypy --strict`; `jscpd` duplication; radon complexity |
| `static_analysis_common_vulnerabilities` | Met | CodeQL |
| `static_analysis_fixed` | Met | CodeQL findings block the merge through required conversation resolution |
| `static_analysis_often` | Met | every push and pull request |
| `dynamic_analysis` | Met | `.github/workflows/fuzz.yml` — atheris coverage-guided fuzzing of the front-matter parser and the slug deriver, on every pull request and nightly |
| `dynamic_analysis_unsafe` | N/A | no memory-unsafe code in this repository |
| `dynamic_analysis_enable_assertions` | Met | the fuzz targets assert their invariants |
| `dynamic_analysis_fixed` | Met | a fuzz failure blocks the merge and uploads the crash reproducer |
