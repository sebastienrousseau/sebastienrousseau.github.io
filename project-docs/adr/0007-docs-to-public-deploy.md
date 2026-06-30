# ADR-0007: Retire the committed `docs/` snapshot; build and deploy `public/` from source

**Site:** sebastienrousseau.com
**Author:** Sebastien Rousseau
**Status:** Accepted
**Date:** 2026-06-26
**Related:** [Improvement Plan 2026](../improvement-plan-2026.md) Phase 5; [ADR-0003](0003-build-copy-pipeline.md)

---

## Context

The site historically committed a built `docs/` snapshot as the GitHub Pages
deploy source. That made the rendered HTML a second source of truth alongside
`_posts/` / `_layouts/`, and it caused three recurring problems:

- **Drift.** The committed snapshot could lag the source, so what shipped was
  not always what the source said.
- **Diff noise.** Every content PR carried thousands of lines of regenerated
  HTML, burying the real source change and making review hard.
- **Merge collisions.** Stacked PRs each rewrote the same generated files.

## Decision

Retire the committed `docs/` snapshot (2026-06-10). CI builds `public/`
**fresh from source** on every run of `build.sh` and deploys it with
`actions/upload-pages-artifact` → `actions/deploy-pages` (Pages), on `main`
only.

- **`main` is the deploy.** There is no separate deploy artefact in the repo;
  whatever `build-audit` produces from `main` is what goes live.
- **Never commit `docs/` or `public/`.** Both are `.gitignore`d. Commits carry
  source only — `_posts/`, `_layouts/`, `_data/`, `scripts/` — plus
  `sigstore-bundles/` when a local signed build refreshed it (see ADR-0009).

## Consequences

- **+** Single source of truth; no source↔snapshot drift.
- **+** PR diffs show only the real source change; no generated-HTML noise; no
  stacked-PR collisions on generated files.
- **+** Smaller repo, faster clones.
- **−** The deployed output is not inspectable in the repo; you read it from
  the live site or a local `./build.sh`. This makes build **determinism** and
  the validation gates (ADR-0003, the `tests/validation/` suite) load-bearing —
  if the build isn't reproducible, there's no committed artefact to fall back
  on. Rollback is therefore "revert source, let CI redeploy" (see
  `operations/rollback.md`), not "check out an old `docs/`".
