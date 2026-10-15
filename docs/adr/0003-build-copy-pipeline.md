# ADR-0003: Generators operate on a build copy, never committed source

**Site:** sebastienrousseau.com
**Author:** Sebastien Rousseau
**Status:** Accepted
**Date:** 2026-06-26
**Related:** [Improvement Plan 2026](../improvement-plan-2026.md) Phase 0.1

---

## Context

The site is compiled by `ssg` from `_posts/`, with a chain of Python
generators/enrichers that decorate content (lead asides, topic cross-links,
homepage rotation, tag pages). Some of these enrichers historically defaulted to
mutating **committed source** (`_posts/`) in place:

- `post_enrich.py` defaulted `--dir` to `_posts`, so a bare run rewrote 60+
  committed posts' lead blocks.
- `topic_link.py` hard-coded `_posts` and was invoked bare from `make regenerate`
  and `publish-daily.sh`, rewriting post bodies.
- Two smoke tests called these `main()`s with no args, mutating committed source
  during `make test`.

This produced real incidents: post lead asides overwritten with auto-derived
bullets, and an unrelated whitepaper dropped from `papers.md`, during routine
generator runs. It also breaks the "article PRs are additive-only" invariant.

## Decision

**The canonical build (`build.sh`) copies `_posts/` → `_posts_build/` and runs all
enrichers against the copy** (`--dir _posts_build`). Committed `_posts/` is the
durable source of truth and is never mutated by a build.

Enrichers that decorate post bodies (`post_enrich.py`, `topic_link.py`) **require
an explicit `--dir`** — no default to `_posts`. An accidental bare invocation
errors instead of corrupting the working tree. Any intentional source write
(e.g. `make regenerate`) must pass `--dir _posts` explicitly.

Listing writers (`gen_articles.py`, `gen_projects.py`, `gen_papers.py`) emit
specific committed files (`articles.md`, `projects.md`, `papers.md`) by design;
these are regenerated intentionally when content changes, and are slated for the
same `--dir` discipline + golden-file snapshots in Phase 0.1b / Phase 1.4.

## Consequences

- **+** A build can never dirty the working tree; article PRs stay additive-only.
- **+** Accidental enricher runs fail loudly instead of silently rewriting source.
- **−** Callers must pass `--dir` explicitly (build.sh, publish-daily.sh, Makefile
  updated accordingly).
