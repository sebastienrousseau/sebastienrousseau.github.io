<!-- SPDX-License-Identifier: Apache-2.0 -->

# Postbuild

`scripts/postbuild.py` is a single-page orchestrator that applies 18 independent transforms to every rendered HTML page. This document explains each transform, the orchestration order, and why it matters.

## Contents

- [Order of operations](#order-of-operations)
- [Pass-by-pass reference](#pass-by-pass-reference)
- [Per-pass counters](#per-pass-counters)
- [Idempotence guarantees](#idempotence-guarantees)
- [Common patterns](#common-patterns)
- [Performance](#performance)

---

## Order of operations

```mermaid
flowchart TB
    P0[HTML page<br/>from public/]
    
    subgraph SEO["SEO + JSON-LD"]
        S1[scrub_localhost_urls]
        S2[stamp_asset_fingerprints]
        S3[fix_sri]
        S4[inject_itemlist]
        S5[inject_tech_article]
        S6[inject_software_source_code]
        S7[fix_social_image]
        S8[inject_og_completeness]
        S9[stamp_image_dimensions]
        S10[inject_howto]
        S11[inject_word_count]
        S12[inject_about]
    end

    subgraph ART["Article furniture"]
        A1[inject_article_furniture<br/>(tag badges, meta bar)]
        A2[inject_sigstore_attestation]
        A3[inject_anchor_links_and_toc]
        A4[inject_citations]
        A5[inject_sources_list]
        A6[inject_mermaid]
    end

    subgraph NAV["Navigation"]
        N1[inject_nav_active]
        N2[inject_prev_next_nav]
        N3[inject_hreflang]
    end

    subgraph FIN["Finalisation"]
        F1[inject_speculation_rules]
        F2[inject_github_stats]
        F3[hoist_body_link_stylesheets]
        F4[inject_jsonld_hashes<br/>MUST run last]
    end

    P0 --> S1 --> S2 --> S3 --> S4 --> S5 --> S6 --> S7 --> S8 --> S9 --> S10 --> S11 --> S12
    S12 --> A1 --> A2 --> A3 --> A4 --> A5 --> A6
    A6 --> N1 --> N2 --> N3
    N3 --> F1 --> F2 --> F3 --> F4
    F4 --> OUT[Patched HTML<br/>written back]
```

Why the order matters:

- `inject_word_count` MUST come before `inject_article_furniture` — the meta bar (`.article-meta`) renders the word count.
- `inject_about` MUST come before `inject_jsonld_hashes` — adding `about`/`mentions` arrays to BlogPosting changes the JSON-LD body, which changes the sha256 hash.
- `inject_jsonld_hashes` MUST run LAST — it computes per-page sha256 hashes for every inline JSON-LD block + the speculation-rules block, strips `'unsafe-inline'`, and folds the hashes into `script-src`. Any later mutation invalidates browser enforcement.

---

## Pass-by-pass reference

### 1. `scrub_localhost_urls`

Static Site Generator's dev server bakes `http://localhost:port` into og:url and a few other places when invoked locally. This pass rewrites every occurrence to `https://sebastienrousseau.com`.

Counter: `localhost_patched`.

### 2. `stamp_asset_fingerprints`

Static Site Generator emits `/_csp/<short-hex>.{css,js}` filenames for fingerprinted bundles, but page-level references use bare `/main.js`. This pass copies fingerprinted assets to their bare-name aliases so all references resolve.

Counter: `asset_fp_patched`.

### 3. `fix_sri`

Replaces the placeholder `integrity="sha256-<short-hex>"` that Static Site Generator emits with a real base64 SHA-256 computed from the actual asset bytes. Without this, browsers refuse to load the asset.

Counter: `sri_patched`.

### 4. `inject_itemlist`

`/articles/`, `/papers/`, `/projects/` get an `ItemList` JSON-LD block. Each `<article class="newsroom-card">` becomes a `ListItem` with `position`, `name`, `url`.

Counter: `itemlist_patched`.

### 5. `inject_tech_article`

Dated posts whose keywords name a programming language or technical domain get an additional `TechArticle` block alongside `BlogPosting`. See [`SCHEMAS.md`](SCHEMAS.md#techarticle).

Counter: `techarticle_patched`.

### 6. `inject_software_source_code`

`/projects/index.html` gets a `SoftwareSourceCode` ItemList. See [`SCHEMAS.md`](SCHEMAS.md#softwaresourcecode).

Counter: `softwaresourcecode_patched`.

### 7. `fix_social_image`

Static Site Generator auto-picks the first `<img>` in the body for `og:image`, often a decorative divider. This pass rebuilds `og:image` + `twitter:image` from the article's `BlogPosting.image` (which reads from the post's `banner:` frontmatter).

Counter: `social_patched`.

### 8. `inject_og_completeness`

Fills in `og:url`, `og:locale`, `og:site_name`, `og:image` when Static Site Generator omits them. Handles locale variants (e.g. `fr_FR`, `zh_CN`) from `<html lang>`.

Counter: `og_patched`.

### 9. `stamp_image_dimensions`

Every `<img>` gets explicit `width`/`height` attributes (CLS budget = 0). The hero image gets `fetchpriority="high"`; below-fold images get `loading="lazy"` + `decoding="async"`. Per-asset manifest pins known dimensions for common SVGs and the author portrait.

Counter: `img_dims_patched`.

### 10. `inject_howto`

Step-by-step articles emit `HowTo` JSON-LD. Specs in `seo.py:_HOWTO_SPECS` per slug. Decoupled from heading styling so the article can be refactored without invalidating the schema.

Counter: `howto_patched`.

### 11. `inject_word_count`

Computes word count from `<main>` body (stripping `<aside>`, `<script>`, `<style>`) and injects it into the BlogPosting JSON-LD `wordCount` field.

Counter: `wc_patched`.

### 12. `inject_about`

Cross-links articles to canonical entities (Wikidata, Wikipedia) so AI engines can ground them in their knowledge graphs. Driven by `ENTITY_AUTHORITY` in `seo.py` — e.g. "post-quantum cryptography" → `https://www.wikidata.org/wiki/Q1364608`.

Counter: `about_patched`.

### 13. `inject_article_furniture`

The "AI citation surface" — tag badges between H1 and body, meta bar (author/date/reading-time), and the author E-E-A-T bio card at end of body. Driven by labels from `_data/i18n/<lang>/labels.json`.

Counter: `furniture_patched`.

### 14. `inject_sigstore_attestation`

Optional pass that appends a `Last verified: <sigstore-bundle-URL>` line if `_data/sigstore/config.json` exists. Skipped by default.

### 15. `inject_anchor_links_and_toc`

Adds `id="…"` + clickable `<a class="heading-anchor">#</a>` to every H2/H3 in `<main>`. If the post has ≥5 H2 headings, builds a table-of-contents card and inserts it at the top of `<main>`.

Counter: `anchor_patched`.

### 16. `inject_citations`

Builds a citations graph from every external `<a href>` referenced in body prose. Adds them to BlogPosting `citation` (Schema.org `citation` accepts an array of `CreativeWork`).

Counter: `citation_patched`.

### 17. `inject_sources_list`

Renders a visible "Sources" list at the end of `<main>` for articles with ≥3 external references.

Counter: `sources_patched`.

### 18. `inject_mermaid`

Lazily upgrades ` ```mermaid ` code fences in article bodies to client-side rendered diagrams via mermaid.js. Loaded only when a mermaid block is present.

Counter: `mermaid_patched`.

### 19. `inject_nav_active`

Marks the nav link for the current section with `aria-current="page"` + `class="active"`.

Counter: `nav_patched`.

### 20. `inject_prev_next_nav`

Adds a `<nav class="post-pagination">` block at the bottom of each dated article with links to the previous + next chronological article.

Counter: `nav_patched` (shared).

### 21. `inject_hreflang`

Emits a complete `<link rel="alternate" hreflang="…" href="…">` block including `x-default` for every translated page. Reciprocity enforced by [`scripts/test_hreflang_reciprocity.py`](../scripts/test_hreflang_reciprocity.py).

Counter: `hreflang_patched`.

### 22. `inject_speculation_rules`

Adds a `<script type="speculationrules">` block that asks Chromium 126+ to prerender same-origin pages on hover. Excludes `/_csp/*`, `*.xml`/`*.json`/`*.txt`/`*.pdf`, `/manifest.json`, `/sw.js`, contact pages.

### 23. `inject_github_stats`

Injects star/fork/license/last-commit pills onto project cards. Stats refreshed nightly by `refresh-gh-stats.yml` into `_data/gh-stats.json`.

### 24. `hoist_body_link_stylesheets`

Static Site Generator's search-widget injects a `<link rel=stylesheet>` into the `<body>`, which fails pa11y AAA ("link elements must be in `<head>`"). This pass moves it back into `<head>`.

Counter: `link_hoisted`.

### 25. `inject_jsonld_hashes` ⚠️ Must run last

Computes SHA-256 of every inline `<script type="application/ld+json">` block + the `<script type="speculationrules">` block. Strips `'unsafe-inline'` from the page's `script-src` and folds in the per-block hashes as `'sha256-<base64>'` tokens.

Counter: `csp_patched`.

---

## Per-pass counters

`scripts/postbuild.py:_PostbuildCounters` is a `__slots__`-bound counter object threaded through every pass. The orchestrator increments a per-pass counter when a transform changes the HTML; the summary print at the end of postbuild reads them all:

```
postbuild: 1849 HTML pages, 72 got localhost→prod scrubbed, 168 got asset URLs fingerprinted,
1849 got real SRI, 3 got ItemList JSON-LD, 613 got TechArticle, 1 got SoftwareSourceCode,
1232 got og:image fixed, 1849 got og:url/locale/site_name, 12069 img(s) stamped w/h,
16 HowTo schema(s) injected, 1232 got wordCount, 741 got about/mentions entities,
1232 got tag badges + meta bar, 1232 got anchor links + ToC, 502 got citation graphs,
502 got visible sources list, 0 got mermaid blocks, 1456 got prev/next nav,
1848 got hreflang pairs, 1849 got CSP JSON-LD hashes
```

If a counter's value is unexpected (e.g. 0 hreflang pairs would mean the i18n pipeline is broken), it's a signal worth investigating.

---

## Idempotence guarantees

Re-running `postbuild.py` on already-patched output is a no-op:

- Every pass checks for the marker it would add. `inject_article_furniture` skips pages that already have `class="article-tags"`. `inject_tech_article` skips pages that already have `"@type":"TechArticle"`. Etc.
- The CSP-hash pass is naturally idempotent — recomputing sha256 of unchanged JSON-LD gives the same hash.

This matters for incremental development: you can `python3 scripts/postbuild.py` directly without re-running the full build.

---

## Common patterns

### Adding a new pass

1. Implement as `inject_<name>(html, …) -> html` in the appropriate `postbuild_lib/` submodule.
2. Add unit tests in `tests/test_<module>.py` — aim for 100% coverage (CI gate).
3. Add a counter slot to `_PostbuildCounters.__slots__`.
4. Call from `_apply_seo_passes` or `_apply_article_passes` at the right place in the order chain.
5. Add to the summary print in `main()`.
6. Update this document.

### Debugging a pass

```bash
python3 -c "
import sys; sys.path.insert(0,'scripts')
from postbuild_lib.schemas import inject_tech_article
from pathlib import Path
page = Path('public/2026-05-21-best-cloud-infrastructure-architecture-2026/index.html')
html = page.read_text()
out = inject_tech_article(page, html)
# Compare lengths, check for the expected marker, etc.
print(f'before: {len(html)}  after: {len(out)}')
print('marker present:', '\"@type\":\"TechArticle\"' in out)
"
```

Each pass is a pure function — you can test it in isolation without invoking the whole pipeline.

---

## Performance

A clean build with 1849 pages × 18 postbuild passes runs in **~3 seconds** on a modern laptop. The hot path is pa11y / Lighthouse (each takes 30-45 min in CI for the full 1849-page sweep) — postbuild itself isn't on the critical path.

Time budget per pass (rough — measured on M1 MacBook Pro):

| Pass | Time per page | Total (1849 pages) |
|---|---:|---:|
| `fix_sri` | 80 µs | 150 ms |
| `inject_word_count` | 200 µs | 370 ms |
| `inject_article_furniture` | 350 µs | 650 ms |
| `inject_jsonld_hashes` | 500 µs | 920 ms |
| Everything else combined | 200 µs | 370 ms |
| **Total** | **~1.3 ms** | **~2.5s** |

The pipeline is I/O-bound on page read+write, not CPU. Parallelisation is possible but the gains don't justify the complexity at current scale.
