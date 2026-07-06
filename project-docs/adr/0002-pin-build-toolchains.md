# ADR-0002: Pin build toolchains for reproducibility

**Site:** sebastienrousseau.com
**Author:** Sebastien Rousseau
**Status:** Accepted
**Date:** 2026-06-26
**Supersedes:** —
**Related:** [Improvement Plan 2026](../improvement-plan-2026.md) Phase 0.3

---

## Context

The CI workflows installed build toolchains at **floating versions**, so two runs
of the same commit could use different binaries:

- `cargo install ssg --locked` — no `--version`, installs whatever is latest on
  crates.io. The repo has shipped incompatible `ssg` upgrades before (history
  shows bumps to `0.0.40`), and `mise.toml` itself notes the version should be
  pinned "when reproducibility matters."
- `ruff==0.15.*`, `pa11y-ci@^4`, `@lhci/cli@0.14.x` — floating patch/minor.
- `wasm-pack` installed via `curl … | sh` (always latest).
- Node pinned to `24` in `mise.toml` but `22` in CI.

Floating toolchains break **reproducibility** (Phase 2/3 goal of byte-identical
builds) and cause silent behaviour drift — e.g. an `ssg` Markdown/metadata change
can alter output mid-PR with no code change.

## Decision

Pin every build toolchain to an exact version, bump deliberately:

| Tool | Pin |
|---|---|
| `ssg` | `0.0.46` (via `cargo install ssg --locked --version 0.0.46`) |
| `ruff` | exact `0.15.x` patch |
| `pa11y-ci` | exact `4.1.1` |
| `@lhci/cli` | exact `0.14.0` |
| `ruff` | exact `0.15.9` |
| `mypy` | exact `2.1.0` (+ `types-PyYAML==6.0.12.20260518`) |
| `wasm-pack` | `cargo install wasm-pack --version 0.15.0 --locked` (no per-release `init.sh` exists) |
| Node | `22` across `mise.toml` and all workflows |

Each pin equals the version CI already resolved at the time of this ADR, so
adopting them is behaviour-neutral — it only locks the floor.

## Bump procedure

1. Open a PR that changes the pin in **all** workflows + `build.sh` + `mise.toml`
   in one commit.
2. Let the full `build-audit` run go green (it diffs the built artifact).
3. Record the new version + rationale by amending this ADR.

## Consequences

- **+** Reproducible builds; no surprise mid-PR behaviour changes.
- **+** A toolchain bump is now an explicit, reviewable event.
- **−** Manual bumps required to pick up upstream fixes (acceptable trade-off;
  reproducibility outranks always-latest per `mise.toml`).

## History

- **2026-07-03 — `ssg` `0.0.44` → `0.0.46`.** 0.0.46 tightened RSS validation:
  it derives the channel `<link>` from each post's `permalink` and aborts with
  `channel.link is missing` when absent. ~963 older locale posts (2018–2024)
  predate the permalink convention, so the bump required a build-time
  `permalink` backfill (`scripts/postbuild/backfill_permalink.py`, run on the
  `_posts_build` copy — committed source is untouched) rather than editing the
  archive. The residual `structured_data: title` and `news_sitemap: day`
  messages are non-fatal warnings (present on 0.0.44 too) and do not block the
  build. Bumped across all five workflows + `Makefile` + `mise.toml` + `README`.
