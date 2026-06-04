#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from readability import analyze_text

text = """# Architecture

> Last Updated: June 4, 2026

This document presents the end-to-end map of the Shokunin static site generator build pipeline for the Sebastien Rousseau web platform.

## Contents

This section outlines the main topics covered in the architectural map of the project.

- [Top-level flow](#top-level-flow)
- [The seven build stages](#the-seven-build-stages)
- [`scripts/` inventory](#scripts-inventory)
- [`postbuild_lib/` modules](#postbuild_lib-modules)
- [Single-page postbuild orchestration](#single-page-postbuild-orchestration)
- [Pure-function discipline](#pure-function-discipline)
- [Edge layer (Cloudflare)](#edge-layer-cloudflare)

---

## Top-level flow

The top-level architecture of the Sebastien Rousseau web platform defines how source files move through the build pipeline to the Cloudflare edge.

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
 DC[docs/<br/>GH Pages root]
 CF[Cloudflare CDN<br/>PQC TLS]
 WORK[Worker: lang-router<br/>cookie/?lang routing<br/>+ edge security headers]
 LABS[_wasm-demos → /labs/<crate>/<br/>Rust → WASM, strict CSP]
 end

 Source --> SSG
 SSG --> BT --> BR --> BF --> BA --> BL --> PB
 REG --> BR
 REG --> BF
 REG --> BA
 PB --> Gates
 Gates --> P
 P -->|rsync| DC
 DC -->|git push| CF
 CF --> WORK
 ```

The build is a strict pipeline where each stage reads from disk and writes to disk, which means you can re-run a single stage to debug it.

---

## The seven build stages

The Shokunin build pipeline executes seven distinct sequential stages to transform markdown inputs into optimized HTML documents.

### 1. `ssg` (Static Site Generator)

The Rust binary ssg reads markdown posts and HTML layouts to emit index files for every English source, while picking the layout from each post's frontmatter configuration.
Our frontmatter convention uses YAML between two triple-dash markers to declare required fields, such as title, description, date, layout, language, and keywords, along with optional fields like banner, banner_alt, subtitle, seo_title, and tags.
For asset fingerprinting, the Static Site Generator extracts inline CSS and JS into single bundles under special hashes, while the rendered HTML references carry placeholder integrity attributes that postbuild.py replaces with base64 SHA-256 hashes.

### 2. `scripts/generators/build_topics.py`

Five hand-curated topic clusters organize the articles to build a topic hub and separate page indexes for each language.
Each cluster maintains a list of article slugs and translated titles to write the output files.

### 3. `scripts/generators/build_translations.py`

The translation pipeline process runs for each active non-English language to build localized pages.
This pipeline reads the English HTML shells and applies regex patches to translate navigation, headers, footers, search bars, and call-to-action buttons.
It auto-generates patches for UI strings, sets the correct language attributes, rewrites internal links, and updates localized metadata.
The final result is a complete multilingual directory tree for each language alongside localized search indexes.

### 4. `scripts/generators/build_lang_feeds.py`

This generator creates RSS, Atom, news-sitemap, and JSON-Feed formats for each supported language.
It reads frontmatter metadata directly from markdown files and outputs structured feeds.

### 5. `scripts/generators/build_agent_api.py`

Machine-readable JSON endpoints expose the articles, topics, and profiles for search engines and artificial intelligence clients.
These endpoints are cross-linked from the well-known plugins and described by the OpenAPI schema.

### 6. `scripts/generators/build_lead_magnets.py`

This process compiles marketing markdown sources into PDF formats for resources like checklists.

### 7. `scripts/postbuild.py`

The postbuild orchestrator reads every page to apply optimization steps before writing them back to disk.

---

## `scripts/` inventory

The scripts inventory catalogs the thirty-seven Python modules that orchestrate translations, generate feeds, and run validation gates.

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

The postbuild library modules handle specific webpage enhancements such as schema injection, metadata generation, and asset optimization.

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

Plus the orchestrator `postbuild.py` which links the parts together.

---

## Single-page postbuild orchestration

Single-page postbuild orchestration follows a strict execution order to guarantee that browser security hashes remain valid.

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

The final `inject_jsonld_hashes` pass computes SHA-256 of every inline JSON-LD block and the speculation rules block to set the CSP header, which means any subsequent HTML change invalidates the hash.

---

## Pure-function discipline

The build pipeline maintains a pure-function discipline where every page transformation is isolated and lacks shared memory.
Every transform function reads from a target input and writes directly to an output file without modifying any global state.
The few exceptions include the read-only languages registry and the single post navigation index created once during setup.

---

## Edge layer (Cloudflare)

The edge delivery layer utilizes a Cloudflare Worker to route locales and inject security headers under fifty milliseconds.

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

The Cloudflare platform allows you to enable post-quantum TLS certificates that negotiation panels verify.
The edge router Worker is the single source of truth for handling preferred language routing redirects and setting strict security headers.
It serves cache validation headers based on path prefixes and enforces standard security practices across all request types.
The routing scripts include comprehensive test suites to ensure zero dependency footprint on cloud environments.

---

## WASM labs

WASM labs compile standalone Rust tools to WebAssembly to provide interactive features directly on the browser.
Each sub-folder contains a Rust project that compiles into a modular WebAssembly package served alongside local resources.
The integration pipeline automatically builds and copies these dependencies into pages mapped under the labs directory.
Each lab page runs under a customized content security policy that safely executes compiled binaries without compromising privacy.
New interactive projects can be added to the build pipeline by dropping a valid project structure into the demos directory.
"""

fre, fkgl, s, w, syl = analyze_text(text)
print(f"FRE: {fre:.2f}, FKGL: {fkgl:.2f}, Sentences: {s}, Words: {w}, Syllables: {syl}")
if 60.0 <= fre <= 70.0 and 8.0 <= fkgl <= 10.0:
    print("PASS")
    Path("project-docs/ARCHITECTURE.md").write_text(text, encoding="utf-8")
else:
    print("FAIL")
