<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# AGENTS.md: Repository Standards for sebastienrousseau.com

Invariants and operating standards for AI agents and human contributors working on `sebastienrousseau.github.io`. Read this before modifying any code or opening a pull request.

---

## 0. About This Repository

`sebastienrousseau.com` is a high-assurance static research publishing platform covering applied artificial intelligence, wholesale payments, and post-quantum cryptography.

The architecture comprises:
1. **Static Site Core**: Rust `ssg` compiler executing over Markdown articles and layouts.
2. **Generators & Postbuild**: Python pipelines in `scripts/` handling taxonomy, schema generation, SEO metadata, and HTML post-processing.
3. **Edge Layer**: Cloudflare Workers in `workers/` executing language routing, security headers, and edge caching.
4. **Microservices**: Containerized WeasyPrint PDF render service on Fly.io in `fly/pdf-render/`.

---

## 1. Hygiene First (Before Any Other Task)

An agent MUST NOT start new feature, content, or enhancement work on a repository that fails health checks without first resolving the findings:

1. **Vulnerabilities & Dependencies**:
   - Check open Dependabot alerts and PRs: `gh pr list --author app/dependabot`, `gh api repos/sebastienrousseau/sebastienrousseau.github.io/dependabot/alerts?state=open`.
   - Check code scanning and secret scanning alerts: `gh api repos/sebastienrousseau/sebastienrousseau.github.io/code-scanning/alerts?state=open`.
   - Verify Python dependency locks: `python3 -m pytest tests/unit/test_requirements_locks_agree.py`.
2. **CI Health**:
   - The default branch (`main`) must be green.
3. **Linters & Formatters**:
   - Linters pass with zero new warnings or suppressions: `python3 -m ruff check scripts/ tests/ fly/` and `python3 -m ruff format --check scripts/ tests/ fly/`.
4. **Complexity Ceilings**:
   - Cyclomatic complexity (McCabe): maximum 10 per function (ratcheted via Radon in CI).
   - Lines of code: maximum 60 per function, 500 per file.

---

## 2. Core Invariants

1. **Never edit generated output**:
   - Directories such as `public/`, `output/`, `output.build-tmp/`, and `.gen/` are not source code.
   - If output is wrong, fix the generator in `scripts/` or the source layout in `_layouts/`.
2. **Single source of truth**:
   - Never duplicate taxonomy keywords, schema definitions, or routing maps. Derive them from `_data/taxonomy.yml` and canonical sources.
3. **Preserve documentation and license integrity**:
   - Retain existing docstrings, architecture notes, and SPDX license identifiers. Never strip explanatory comments.
4. **Keep the workspace clean**:
   - Do not create unmanaged directories or place temporary caches outside gitignored locations.
5. **Never invent facts**:
   - Performance benchmarks, cryptographic claims, and security ratings must be backed by verifiable code or repository evidence.
6. **Never silence a check by feeding it**:
   - Do not add entries to allowlists, ignore files, or test skip decorators to hide regressions. Fix root causes.
7. **Fix forward, now**:
   - Defects discovered during a working session must be resolved in that session. No deferred follow-up tickets.
8. **Humans are accountable; agents do not attest**:
   - Agents MUST NOT add `Signed-off-by:` on a human's behalf.
   - Agents MUST NOT publish releases or perform actions outside the local system.
   - Commits generated with agent assistance carry attribution in git trailers: `Assisted-by: <agent>:<model> [<tools>]`.
9. **Zero em dashes**:
   - NEVER use the em dash character (`—`) anywhere in commit messages, pull requests, documentation, or release notes. Use commas, colons, parentheses, or spaced hyphens.

---

## 3. Semantic Versioning & Branch Lifecycle

1. **Strict Version Progression**:
   - Increments proceed strictly by `0.0.1` (for example, `v1.2.0` -> `v1.2.1` -> `v1.2.2`).
2. **Release Branch**:
   - All work for the next iteration MUST be developed on `feat/v<next-version>` targeting `main`.
3. **Single Active Release PR Invariant**:
   - There MUST be at most ONE active pull request targeting the default branch (`main`), which MUST be the release branch `feat/v<next-version>`.
4. **Branch Funneling Policy**:
   - Dependabot PRs, security patches, documentation fixes, or topic branches MUST NEVER be merged directly into `main`.
   - They MUST be merged or cherry-picked into `feat/v<next-version>`, and their standalone pull requests closed with a reference to the active release PR.

---

## 4. Commit & Handover Standards

1. **Header**: `<type>: <subject>` (maximum 50 characters, imperative mood). Allowed types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`.
2. **Body**: Explain WHAT and WHY (not HOW), wrapped strictly at 72 characters.
3. **Signing**: Commits and tags MUST be SSH signed (`git commit -S -s`).
4. **Merge Authority**: NEVER merge pull requests into `main` without explicit human authorization. Provide handover commands formatted as:
   `cd /Users/seb/Code/Public/Web/sebastienrousseau.github.io && <command>`.

---

## 5. Single Validation Gate

Before pushing any commit, run the local verification suite:

```bash
# 1. Dependency lock agreement
python3 -m pytest tests/unit/test_requirements_locks_agree.py

# 2. Lint and formatting
python3 -m ruff check scripts/ tests/ fly/
python3 -m ruff format --check scripts/ tests/ fly/

# 3. Type checking
./scripts/typecheck.sh

# 4. Postbuild unit tests
python3 -m pytest tests/unit/test_postbuild_*.py
```
