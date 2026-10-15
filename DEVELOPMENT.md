<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Developer Guide: sebastienrousseau.com

Welcome to the development environment for `sebastienrousseau.com`. This document explains how to set up the pinned toolchain, execute builds, reproduce CI quality gates locally, and run the automated test taxonomy.

---

## 1. Prerequisites & Toolchain Setup

The repository uses [mise](https://mise.jdx.dev) to provision and pin exact versions of all runtime environments:

* **Rust** (stable): Compiles the static site generator `ssg`.
* **Python** (3.12): Executes generator scripts and postbuild passes.
* **Node.js** (22): Executes accessibility audits (`pa11y-ci`) and Edge Worker tests.
* **uv**: Compiles hash-pinned lockfiles (`requirements.lock`, `requirements-dev.lock`).

### Provisioning with Mise

```bash
git clone https://github.com/sebastienrousseau/sebastienrousseau.github.io.git
cd sebastienrousseau.github.io

# Install toolchains and dependencies in one idempotent command
make bootstrap
```

### Git Hooks

Install pre-commit validation hooks to catch formatting and naming conventions locally:

```bash
pip install pre-commit
pre-commit install
```

---

## 2. Local Build & Serve Loop

### Build the Full Static Site

The build pipeline generates 2,500+ pages across 34 languages, including feed outputs, search indices, and sitemaps:

```bash
# Build the entire site to public/
make build
# or run the build script directly
./build.sh
```

### Local Development Server

Serve the compiled site locally on `http://127.0.0.1:8000`:

```bash
make serve
```

### Clean Build Output

Force-remove temporary build trees and cached assets:

```bash
make clean
```

---

## 3. Local Verification & CI Gate Reproduction

Every CI quality gate is runnable locally without relying on remote runners.

### 1. Dependency Lock Agreement

Verify that `requirements.txt` and `requirements-dev.txt` match `requirements.lock` and `requirements-dev.lock`:

```bash
python3 -m pytest tests/unit/test_requirements_locks_agree.py
```

To regenerate locks after updating packages:

```bash
./scripts/security/lock-deps.sh
```

### 2. Linters & Code Formatters

Check Python code quality across scripts, tests, and microservices:

```bash
# Lint checks
python3 -m ruff check scripts/ tests/ fly/

# Formatting checks
python3 -m ruff format --check scripts/ tests/ fly/

# Auto-format
python3 -m ruff format scripts/ tests/ fly/
```

### 3. Type Checking (Mypy Strict Tier)

Run strict type checking over verified packages:

```bash
./scripts/typecheck.sh
```

### 4. Cyclomatic Complexity

Verify that functions stay within the McCabe complexity ceiling (maximum 10):

```bash
python3 -m radon cc -s -n B scripts/
```

### 5. Unit Test Suite

Execute the unit test suites:

```bash
# Postbuild library suite
python3 -m pytest tests/unit/test_postbuild_*.py

# Full pre-build unit test suite with coverage gate
pytest tests/unit/ -ra \
  --cov=scripts/postbuild/postbuild_lib \
  --cov-fail-under=100
```

### 6. Vulnerability Scanning

Check dependencies for known CVEs:

```bash
pip-audit --strict -r requirements.txt
npm audit --prefix .github/ci-tools/visual
```

### 7. Cloudflare Worker Tests

Run Worker test suites:

```bash
npm test --prefix workers
```

---

## 4. Test Taxonomy

Tests are structured under `tests/`:

* `tests/unit/`: Fast, isolated tests for generators, postbuild helpers, feed builders, and metadata stampers. Runs pre-build.
* `tests/validation/`: Structural invariant validators (for example, CSP strictness, hreflang reciprocity, JSON-LD schema validity). Runs post-build.
* `fuzz/`: Fuzz harnesses testing markdown parsers and slug generation against crash regressions.

---

## 5. Branch & Pull Request Standards

* **Release Branch**: All work begins on `feat/v<next-version>`.
* **Commits**: SSH signed (`git commit -S -s`) with descriptive BLUF headers and Assisted-by trailers.
* **Pull Requests**: Single active PR targeting `main`. Follow `.github/pull_request_template.md`.
