# Architecture

> Last Updated: June 4, 2026

This guide shows the build steps of the Static Site Generator site builder for the Sebastien Rousseau web site.

## Contents

This list shows the main topics in this guide.

- [Top-level flow](#top-level-flow)
- [The build pipeline](#the-build-pipeline)
- [`scripts/` inventory](#scripts-inventory)
- [`postbuild_lib/` modules](#postbuild_lib-modules)
- [Single-page postbuild orchestration](#single-page-postbuild-orchestration)
- [Pure-function discipline](#pure-function-discipline)
- [Edge layer (Cloudflare)](#edge-layer-cloudflare)

---

## Top-level flow

The main flow shows how source files move from the Git repository to the web edge.

```mermaid
%%{init: {'theme':'neutral'} }%%
flowchart TB
 subgraph Source["Source (Git)"]
 EN[_posts/*.md<br/>61 English]
 T[_posts/<lang>/*.md<br/>1189 translations]
 L[_layouts/*.html<br/>11 layouts]
 D[_data/i18n/<lang>/<br/>28 × 11 JSON files]
 REG[scripts/lib/_lang_registry.py<br/>28-lang truth]
 end

 subgraph Build["Build (12s)"]
 SSG[Static Site Generator<br/>Rust binary]
 BT[build_topics.py]
 BR[build_translations.py]
 BF[build_lang_feeds.py]
 BA[build_agent_api.py]
 BL[build_lead_magnets.py]
 PB[postbuild.py<br/>18 passes]
 end

 subgraph Gates["14 CI gates"]
 G[ruff · radon · pytest 100%<br/>JSON-LD validate<br/>i18n parity ×7<br/>pa11y AAA · Lighthouse<br/>CSP strict-shape<br/>EN-leakage · Workers]
 end

 subgraph Output["Output"]
 P[public/<br/>1850 pages]
 DC[GH Pages<br/>artifact deploy]
 CF[Cloudflare CDN<br/>PQC TLS]
 WORK[Worker: lang-router<br/>cookie/?lang routing<br/>+ edge security headers]
 LABS[labs/ → /labs/<crate>/<br/>Rust → WASM, strict CSP]
 end

 Source --> SSG
 SSG --> BT --> BR --> BF --> BA --> BL --> PB
 REG --> BR
 REG --> BF
 REG --> BA
 PB --> Gates
 Gates --> P
 P -->|upload-pages-artifact| DC
 DC -->|deploy-pages| CF
 CF --> WORK
 ```

The build is a simple chain where each tool reads files and saves files, which makes it easy to run a single tool by hand to test it.

---

## The build pipeline

`build.sh` is the single source of truth for build order. It runs three
phases: listing-regen + enrichment on a throwaway `_posts_build` copy, the
`ssg` Rust compile, then a chain of post-compile generators and a per-page
postbuild pass over `public/`. The steps below are in execution order;
`tests/unit/test_architecture_doc_current.py` fails if a
`python3 scripts/...py` step is added to `build.sh` without an entry here.

### Phase A — pre-compile (operates on the `_posts_build` copy + `_data/`)

1. **`scripts/postbuild/regen_slug_maps.py`** — rewrites `_data/i18n/<lang>/slugs.json` from the actual `_posts/<lang>/*.md` filenames (idempotent; keeps EN↔locale slug pairs in sync).
2. **`scripts/postbuild/regen_homepage.py`** — rewrites the "From the desk" card grid in `index.md` from the most recent dated EN posts.
3. **`scripts/postbuild/post_enrich.py`** — injects article furniture (lead aside, related-posts, review date) into the build copy. Requires `--dir` (ADR-0003; never mutates committed source by default).
4. **`scripts/generators/build_tags.py`** — builds the tag taxonomy and per-post tag badges/meta.
5. **`scripts/postbuild/backfill_permalink.py`** — backfills a `permalink:` into any build-copy post that lacks one (older locale archive posts), derived from the post's locale dir + slug. ssg ≥ 0.0.45 derives the RSS channel `<link>` from `permalink` and aborts without it; source stays untouched (ADR-0002).

### Phase B — `ssg` (Static Site Generator)

The Rust tool reads the `_posts_build` markdown and `_layouts/` and writes the English pages to `public/`, choosing each layout from the frontmatter. It externalises inline CSS/JS to `/_csp/<hash>` files with placeholder integrity hashes that postbuild later replaces with real SHA-256 values.

### Phase C — post-compile generators (operate on `public/`)

- **`scripts/postbuild/fix_escaped_ssg_html.py`** — repairs entity-escaped head metas and escaped enrich/lead body blobs that local ssg builds emit (renders as raw-markup prose otherwise). Head-bounded meta unescape with keep-first dedupe of the leaked meta names, plus whole-region unescape of each `&lt;div lang=`-marked blob, skipping `<pre>`/`<code>`. Runs first in Phase C so downstream generators fork a sane `/articles/` shell; idempotent and a no-op on CI, where ssg emits real tags.
5. **`scripts/seo_and_audit/fetch_metrics.py`** — fetches live crates.io download + GitHub star/fork totals into `_data/proof/metrics.json`.
6. **`scripts/generators/build_case_studies.py`** — renders the outcome-led case-study pages.
7. **`scripts/generators/build_topics.py`** — topic-cluster pillar pages and the topic hub from the `TOPICS` taxonomy (per-locale clones generated downstream).
8. **`scripts/generators/build_tag_landings.py`** — per-tag landing pages.
9. **`scripts/generators/build_listings.py`** — the `/articles/` index and related listing pages, scanned from `_posts/`.
10. **`scripts/generators/build_oembed.py`** — oEmbed JSON endpoints for each page.
11. **`scripts/generators/build_translations/__main__.py`** — the localised page tree for every active language in the registry: swaps body text, chrome, UI strings, hreflang, and search indexes.
12. **`scripts/generators/build_search_ui.py`** — per-locale `search-ui.json` UI microcopy for the client-side search runtime (ADR-0010), projected from `_data/i18n/<lang>/strings.json`.
- **`scripts/generators/build_speaking.py`** — renders the `/speaking/` authority hub (bios, outcome-framed talk topics, invite CTA) from `_data/proof/speaking.yml`, reusing the `/articles/` shell. English-only; runs after `build_translations`, before `postbuild`.
- **`scripts/generators/build_iso20022_mcp.py`** — renders the premium `/iso20022-mcp/` hub (the What-is-MCP explainer, the suite cards, quickstart FAQ, CTA) from an inline content dict, reusing the `/articles/` shell like `build_speaking`. English-only; runs after `build_speaking`.
- **`scripts/generators/build_trust.py`** — renders the `/trust/` enterprise-governance page (provenance, licensing, single-maintainer governance, recognition) from `_data/proof/recognition.yml` + platform provenance facts, reusing the `/articles/` shell. English-only; same slot as `build_speaking.py`.
- **`scripts/generators/build_changelog.py`** — generates the `/changelog` page (dated posts grouped by month), the homepage "what's new" strip, and a `/status` page + `status.json` build badge; deterministic (derived from committed post front-matter). No new JS/CSS; CSP-safe.
13. **`scripts/generators/build_lang_feeds.py`** — RSS, Atom, news-sitemap, and JSON feeds per language.
14. **`scripts/generators/build_agent_api.py`** — JSON endpoints exposing articles/topics for AI and search clients.
15. **`scripts/generators/build_lead_magnets.py`** — compiles source files into PDF resources (checklists, etc.).
16. **`scripts/generators/build_news_sitemap.py`** — the Google News sitemap.

### Phase D — postbuild + finalisation

17. **`scripts/postbuild/postbuild.py`** — the per-page optimisation pass: real SRI hashes, per-page CSP JSON-LD hashes, structured data, og/twitter tags, image width/height stamping, asset fingerprinting, breadcrumbs, and the rest of the page furniture.
18. **`scripts/seo_and_audit/build_rag_corpus.py`** — the RAG/LLM corpus (`feed.jsonl`, per-tag JSONL, MCP resources).
19. **`scripts/postbuild/fix_lang_switcher.py`** — rewrites the language-switcher hrefs to per-locale targets.
20. **`scripts/security/sigstore_sign.py`** — signs dated articles with Sigstore (best-effort; skipped when no signing config is present).

After these, `build.sh` runs the validation gate (`tests/validation/`) under `set -euo pipefail`, so any CSP/hreflang/i18n/RTL/sitemap/JSON-LD failure fails the build.

---

## `scripts/` inventory

This list cataloges the Python files that manage translations, feeds, and test gates.

| Group | Modules |
|---|---|
| **Build stages** | `build_topics.py`, `build_translations.py`, `build_lang_feeds.py`, `build_fr_feeds.py` (legacy), `build_agent_api.py`, `build_lead_magnets.py`, `postbuild.py` |
| **Postbuild library** | `postbuild_lib/__init__.py`, `article_furniture.py`, `github_stats.py`, `output.py`, `schemas.py`, `seo.py` |
| **Single source of truth** | `_lang_registry.py` (28-language matrix), `build_topics.py` (topic taxonomy), `gen_projects.py` (projects portfolio source) |
| **In-repo CI gates** | `test_csp_strict.py`, `test_hreflang_reciprocity.py`, `test_i18n_*.py` (5 × parity gates), `test_jsonld_localized.py`, `test_lang_no_leakage.py`, `test_rtl_safe.py`, `test_search_indexes.py`, `test_sitemap_completeness.py` |
| **One-shot generators** | `gen_articles.py`, `gen_projects.py`, `gen_layouts.py`, `fetch_github_stats.py`, `fix_cdn_urls.py`, `fix_seo_meta.py`, `topic_link.py`, `postbuild.py:scrub_localhost_urls()`, `sigstore_sign.py` |
| **External validators** | `validate_jsonld.py`, `audit_links.py` |

---

## `postbuild_lib/` modules

The library files handle details like metadata tags, statistics, and page markup.

```mermaid
%%{init: {'theme':'neutral'} }%%
flowchart LR
 PB["postbuild.py"]
 PB --> AF[article_furniture<br/>tag badges,<br/>meta bar, author<br/>card, prev/next]
 PB --> GH[github_stats<br/>repo star/fork<br/>pills injection]
 PB --> OUT[output<br/>llms.txt,<br/>sitemap splice,<br/>XML feed fix]
 PB --> SC[schemas<br/>TechArticle,<br/>SoftwareSourceCode]
 PB --> SEO[seo<br/>og:image, HowTo,<br/>about/mentions,<br/>image w/h]
 ```

| Module | Stmts | Coverage | Responsibility |
|---|---:|---:|---|
| `article_furniture.py` | 470 | 100% | Tag badges, article meta bar, anchor links + ToC, citations graph, sources list, prev/next nav, hreflang, sigstore attestation, mermaid blocks. |
| `github_stats.py` | 130 | 100% | Inject star/fork/license/last-commit pills onto project cards. |
| `output.py` | 392 | 100% | `llms.txt`, `llms-full.txt`, sitemap splice, RSS/Atom/news-sitemap URL repair, JSON Feed write, robots.txt. |
| `schemas.py` | 168 | 100% | TechArticle JSON-LD on technical posts; SoftwareSourceCode JSON-LD on /projects/. |
| `seo.py` | 209 | 100% | `og:image` repair, HowTo schema, `about`/`mentions` Wikidata cross-links, image w/h stamping, `og:url`/`og:locale`/`og:site_name` completion, word count injection. |

The main script uses these modules to enhance the pages.

---

## Single-page postbuild orchestration

The page optimization steps run in a set order to keep the security hashes valid.

```mermaid
%%{init: {'theme':'neutral'} }%%
sequenceDiagram
 autonumber
 participant FS as "public/<page>"
 participant PB as postbuild.py
 participant SEO as seo
 participant SC as schemas
 participant AF as article_furniture
 participant GH as github_stats
 participant CSP as inject_jsonld_hashes

 FS->>PB: Read original HTML
 PB->>PB: scrub_localhost_urls
 PB->>PB: stamp_asset_fingerprints
 PB->>PB: fix_sri (real sha256)
 PB->>SEO: inject_itemlist
 PB->>SC: inject_tech_article
 PB->>SC: inject_software_source_code
 PB->>SEO: fix_social_image
 PB->>SEO: inject_og_completeness
 PB->>SEO: stamp_image_dimensions
 PB->>SEO: inject_howto
 PB->>SEO: inject_word_count
 PB->>SEO: inject_about
 PB->>AF: inject_article_furniture (tag badges, meta bar)
 PB->>AF: inject_sigstore_attestation
 PB->>AF: inject_anchor_links_and_toc
 PB->>AF: inject_citations
 PB->>AF: inject_sources_list
 PB->>AF: inject_mermaid
 PB->>AF: inject_nav_active
 PB->>AF: inject_prev_next_nav
 PB->>AF: inject_hreflang
 PB->>AF: inject_speculation_rules
 PB->>GH: inject_github_stats
 PB->>AF: hoist_body_link_stylesheets
 PB->>CSP: inject_jsonld_hashes (final)
 FS->>PB: Patched HTML written
 ```

The final step computes security hashes of the script blocks for the security header, which means any later changes to the page will block the scripts from running.

---

## Pure-function discipline

The build tools run as pure functions that do not share state or modify global values, which means each function reads a page and writes the output directly to a file.

---

## Edge layer (Cloudflare)

The edge layer uses a Cloudflare Worker to route visitors and set security headers quickly. The platform supports post-quantum certificate options that browsers display.

```mermaid
%%{init: {'theme':'neutral'} }%%
flowchart LR
 REQ[Browser request] --> CF
 subgraph CF["Cloudflare edge"]
 PQ[PQC TLS<br/>X25519MLKEM768]
 WORK[lang-router Worker<br/>routing + security headers<br/>~50ms]
 CACHE[CDN cache]
 end
 CF --> PAGES[GitHub Pages<br/>docs/]
 PAGES --> CACHE
 ```

The edge router is the single source of truth for language routing and security headers, and it sets headers based on paths and runs tests to ensure the rules remain stable.

---

## WASM labs

We compile Rust projects to WebAssembly to provide interactive tools on the site. Each project lives in its own folder and builds a package for the labs page.
The build tool copies these files automatically during compilation. The lab pages run with a strict security policy to execute code safely, and you can add a new lab page by adding a project folder to the demos directory.
