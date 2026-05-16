# State-of-site audit — 2026-05-16

Captured after merging #32 (AR + postbuild module split), #33 (gh-stats refresh)
and #34 (CDN asset-fingerprint fix). All measurements are reproducible from the
build output in `public/`.

## Lighthouse — desktop preset, 3 runs per URL, median reported

| URL                                                            | Perf | A11y | BP  | SEO | LCP    | CLS   | TBT  | FCP    |
|----------------------------------------------------------------|-----:|-----:|----:|----:|-------:|------:|-----:|-------:|
| /                                                              | 100  | 100  | 100 | 100 | 0.81 s | 0.000 | 0 ms | 0.29 s |
| /about/                                                        |  96  | 100  | 100 | 100 | 1.38 s | 0.000 | 0 ms | 0.31 s |
| /articles/                                                     |  96  | 100  | 100 | 100 | 1.38 s | 0.000 | 0 ms | 0.35 s |
| /papers/                                                       |  98  | 100  | 100 | 100 | 1.10 s | 0.000 | 0 ms | 0.32 s |
| /projects/                                                     |  99  | 100  | 100 | 100 | 0.92 s | 0.000 | 0 ms | 0.32 s |
| /contact/                                                      | 100  | 100  | 100 | 100 | 0.65 s | 0.000 | 0 ms | 0.34 s |
| /2026-05-11-lucy-besson…/                                      |  99  | 100  | 100 | 100 | 0.82 s | 0.000 | 0 ms | 0.37 s |
| /fr/                                                           | 100  | 100  | 100 | 100 | 0.78 s | 0.000 | 0 ms | 0.29 s |
| /fr/a-propos/                                                  | 100  | 100  | 100 | 100 | 0.72 s | 0.000 | 0 ms | 0.32 s |
| /fr/2026-05-11-lucy-besson…/                                   | 100  | 100  | 100 | 100 | 0.66 s | 0.000 | 0 ms | 0.35 s |

Targets (Google "good" thresholds): LCP ≤ 2.5 s, CLS ≤ 0.1, FID/TBT ≤ 200 ms.
**Every measured page is comfortably inside the green band on every metric.**

## Accessibility — pa11y-ci WCAG2AAA

* 265 / 265 pages pass.
* Standard: WCAG2AAA (strictest tier).
* CI gate: `.github/workflows/ci.yml::accessibility` — fails the build on any violation.

## Static analysis & complexity

* `ruff check scripts/ tests/` — **clean**.
* `radon mi` (maintainability index, A is best, ≥ 20):
  | File                                 | MI            |
  |--------------------------------------|---------------|
  | `scripts/postbuild.py`               | A (34.26)     |
  | `scripts/postbuild_lib/seo.py`       | A (47.73)     |
  | `scripts/postbuild_lib/output.py`    | A (32.53)     |
  | `scripts/postbuild_lib/article_furniture.py` | A (24.63) |
  | `scripts/postbuild_lib/github_stats.py` | A (47.31)  |
* `radon cc -a` average **A (4.82)** across 95 blocks. Highest-complexity functions:
  | Function                                              | Grade  |
  |-------------------------------------------------------|--------|
  | `seo.build_about_graph`                               | C (17) |
  | `github_stats._gh_lookup`                             | C (16) |
  | `github_stats._relative_time`                         | C (15) |
  | `postbuild.build_itemlist`                            | C (14) |
  | `article_furniture._nav_active_target`                | C (13) |
  | `seo.inject_og_completeness`, `output._splice_fr_urls`, `article_furniture.inject_article_furniture` | C (11–12) |

  Phase 1 of the next push will refactor these to ≤ B (10).

## Code duplication — jscpd

* `npx jscpd scripts/ tests/ _layouts/ --min-tokens 50`
* **1.46 %** duplicated lines across 11 808 source lines.
  | Format     | Lines  | Duplicated  | %     |
  |------------|-------:|------------:|------:|
  | Python     | 11 241 | 172         | 1.53  |
  | JavaScript |    564 | 0           | 0.00  |
  | CSS        |      3 | 0           | 0.00  |
* All 17 clones are in the parallel i18n-parity test scripts
  (`test_i18n_labels.py` ↔ `test_i18n_takeaway_labels.py` etc.). Industry-standard
  warn threshold is 10 %; we sit at 1.46 % which is acceptable.

## Test coverage

| Module                                       | Coverage |
|----------------------------------------------|---------:|
| `postbuild_lib/seo.py`                       |   54 %   |
| `postbuild_lib/output.py`                    |   44 %   |
| `postbuild_lib/github_stats.py`              |   34 %   |
| `postbuild_lib/article_furniture.py`         |   29 %   |
| `postbuild_lib/__init__.py`                  |  100 %   |

Total `postbuild_lib`: **38 %**. 141 pytest cases. Phase 2 of the next push will
target ≥ 80 % on each of the core four modules.

## Technical SEO

* `validate_jsonld.py`: 265 HTML pages, 4 XML feeds, **0 err / 0 warn**.
* hreflang reciprocity: 264 paired pages, 264 with alternates.
* JSON-LD `inLanguage` matches `<html lang>` on all 265 pages.
* Sitemap completeness: 256 non-excluded rendered pages, all present (16 143 total entries).
* No bare-`localhost` URLs in any built HTML (postbuild scrub).
* No bare asset names in `<script src>` / `<link href>` — every cacheable
  asset reference is fingerprinted (`stamp_asset_fingerprints`).

## Security

* Strict CSP per page, inline JSON-LD allowed by SHA-256 hash only.
* Real SRI on every `/_csp/*` asset (browsers enforce SRI).
* `Permissions-Policy` opts out of every privacy-invasive sensor / API:
  browsing-topics, interest-cohort, attribution-reporting, geolocation,
  camera, microphone, etc.
* `_headers` ships HSTS preload, X-Content-Type-Options, Referrer-Policy
  strict-origin-when-cross-origin, COOP, CORP, X-Frame-Options.
* `/.well-known/security.txt` present with disclosure address.
* Sigstore signing scaffolding wired (no-op until `_data/sigstore/config.json`).

## Build pipeline gates

12 CI gates run on every push:

1. search-index shape
2. i18n parity (en/fr/ar/de)
3. UI-strings parity
4. body-labels parity
5. takeaway-labels parity
6. render-data parity
7. author-card parity
8. hreflang reciprocity
9. JSON-LD inLanguage
10. sitemap completeness
11. no EN UI strings leak into non-EN page chrome
12. no physical CSS properties in layouts (RTL safety)

All twelve are green on `main`.

## Source size

* `scripts/postbuild.py`: 656 lines (down from 2 007 pre-#31/#32)
* `scripts/postbuild_lib/`: five focused modules (output, seo, article_furniture,
  github_stats, __init__).

## What 10/10 still needs

1. **Cyclomatic complexity max** — six functions sit at C grade. Refactor to ≤ B (10).
2. **Coverage** — lift `postbuild_lib` from 38 % to ≥ 80 % per module.
3. (Optional) Wire `radon cc --max-rank B` and `jscpd --threshold 5` as CI gates so neither metric can regress silently.
