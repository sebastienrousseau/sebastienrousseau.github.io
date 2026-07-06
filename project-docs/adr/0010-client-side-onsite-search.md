# ADR-0010: Client-side on-site search engine choice

**Site:** sebastienrousseau.com
**Author:** Sebastien Rousseau
**Status:** Accepted
**Date:** 2026-07-03
**Supersedes:** —
**Related:** [Developer-Experience Plan 2026](../developer-experience-plan-2026.md) Phase 2; [ADR-0002](0002-pin-build-toolchains.md) (toolchain pinning); [ADR-0003](0003-build-copy-pipeline.md) (build/copy pipeline)

---

## Context

The site has 200+ articles across 28 locales and **zero on-site search** (Phase 2
of the DX plan). The build already emits a per-locale full-text index at
`public/search-index.json` and `public/<lang>/search-index.json` (produced by the
translation renderer, `scripts/generators/build_translations/_search.py`), with the
entry shape `{title, url, content, headings}`. We need instant, client-side,
no-backend search over that index.

The site operates under hard, CI-blocking guardrails that constrain the choice:

- **Hash-strict CSP.** Every page ships `script-src 'self' …` (no `'unsafe-inline'`,
  no `'unsafe-eval'`) and `style-src 'self' '<hash>' …` (hash-only inline). Enforced
  by `tests/validation/test_csp_strict.py`. Any `'wasm-unsafe-eval'` or
  `worker-src` addition would be a **global CSP relaxation** unless route-scoped.
- **Progressive enhancement.** JS-off navigation must keep working; `/search` must
  degrade gracefully.
- **Perf budget.** The search runtime must lazy-load on first use and add **0** to
  initial LCP (Lighthouse-gated).
- **Reproducibility / minimal attack surface.** Prefer no-backend, build-time,
  no-new-binary solutions (ADR-0002 pins every build tool; a new binary is a new
  pin + a new supply-chain edge).
- **28-locale coverage**, including no-space scripts (中文, 日本語, ไทย) and RTL
  (العربية, עברית).

Three options were considered: **Pagefind**, **Lunr**, and a **dependency-free
inverted index** over the existing `search-index.json`.

## Decision

Ship a **dependency-free, client-side inverted-index search** over the existing
per-locale `search-index.json`. No new runtime library, no new build binary, no CSP
change.

The runtime is a single lazily-loaded same-origin module (`/search.js` + `/search.css`,
copied from `_layouts/` by `build.sh` exactly as `theme-init.js` is). It is injected
on first invocation of the `⌘K` / `Ctrl-K` command palette (or on load of the
`/search` page), so pages that never invoke search pay nothing. It fetches the active
locale's `search-index.json` (`connect-src 'self'`), builds a small ranked inverted
index in the browser, and renders an ARIA `listbox` of results. UI microcopy comes
from a per-locale `search-ui.json` emitted at build time from
`_data/i18n/<lang>/strings.json` (the same `search.*` keys the parity gate already
enforces).

### Why not Pagefind

Pagefind is excellent and genuinely i18n-aware, but it does not fit *this* pipeline:

1. **CSP.** Pagefind's runtime is WebAssembly executed from a Web Worker. That
   requires `script-src … 'wasm-unsafe-eval'` **and** `worker-src`, i.e. a relaxation
   of the site-wide hash-strict CSP. Per the guardrails this would have to be
   route-scoped and ADR-documented — but search is invoked from *every* page (the
   nav `⌘K`), so "route-scoped" is meaningless here; it would be a de-facto global
   weakening. That is the single disqualifying factor.
2. **Duplicate index.** Pagefind crawls the built HTML and emits its *own* index
   fragments, duplicating the `search-index.json` the build already produces and
   inflating the deploy artifact.
3. **New pinned binary.** Pagefind is a Rust binary run after `ssg`; adopting it adds
   a new toolchain pin (ADR-0002) and a new supply-chain edge for no functional gain
   over the existing index.

### Why not Lunr

Lunr is pure-JS and CSP-clean, so it clears the hardest gate — but it is still the
weaker fit:

1. **New vendored dependency + SRI/build plumbing** for a job the existing index
   already 90 % solves. More surface, more to pin, more to hash.
2. **Multilingual tokenization.** Lunr's default tokenizer splits on whitespace and
   applies an English stemmer. For the CJK/Thai portion of our 28 locales (no word
   boundaries) it degrades to whole-field tokens; correct handling needs
   `lunr-languages` stemmer packs per locale — 20+ extra assets to load and pin, and
   still no segmenter for 中/日/ไทย.
3. Our corpus is already trimmed (`content` capped at ~2200 chars/entry), so the
   ranking sophistication Lunr buys over a hand-rolled tf + field-boost scorer is
   marginal at this size.

A ~4 KB hand-rolled index gives us: uniform behaviour across all 28 locales (word
tokens **plus** a substring/bigram fallback so no-space and RTL scripts still match),
zero new dependencies, zero CSP change, and trivial lazy-loading — the guardrail-optimal
outcome.

## Consequences

- **+** No CSP relaxation; the hash-strict `script-src`/`style-src` is untouched.
  `test_csp_strict.py` and `test_sri_integrity.py` stay green.
- **+** No new build binary or runtime dependency to pin (ADR-0002 unaffected); no
  new supply-chain edge.
- **+** Reuses the existing per-locale `search-index.json`; no duplicate index, no
  deploy-size regression.
- **+** Fully lazy: `/search.js` + `/search.css` load on first `⌘K` or on the
  `/search` page only, so initial LCP is unchanged on every other page.
- **+** Locale-aware by construction (fetches `/<lang>/search-index.json`), with a
  "search all locales" toggle; UI strings flow through the existing `strings.json`
  parity gate.
- **−** We own the ranking function rather than delegating to a maintained library.
  Mitigated by a golden-file test (`tests/validation/test_search_ui_parity.py`) and
  the small, well-scoped scorer.
- **−** No stemming/typo-tolerance out of the box. Acceptable for v1; if demand
  appears, a per-locale stemmer can be layered behind the same lazy module without
  revisiting the engine decision.
