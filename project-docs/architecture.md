# Architecture

> Last Updated: June 4, 2026

This guide shows the build steps of the Shokunin site builder for the Sebastien Rousseau web site.

## Contents

This list shows the main topics in this guide.

- [Top-level flow](#top-level-flow)
- [The seven build stages](#the-seven-build-stages)
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
 DC[docs/<br/>GH Pages root]
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
 P -->|rsync| DC
 DC -->|git push| CF
 CF --> WORK
 ```

The build is a simple chain where each tool reads files and saves files, which makes it easy to run a single tool by hand to test it.

---

## The seven build stages

The build runner uses seven steps to change text drafts into web pages.

### 1. `ssg` (Static Site Generator)

The Rust tool reads markdown posts and layout files to build the English pages, and it picks the layout based on the settings in the frontmatter block.
The frontmatter uses YAML keys between two lines to define the title, description, and keywords.
To keep the site secure, the tool puts style and script code into files with unique hashes, which the script later replaces with real hashes.

### 2. `scripts/generators/build_topics.py`

Five topic groups organize the articles to build a topic page and language lists, and each group uses a list of article paths and translated titles to write the pages.

### 3. `scripts/generators/build_translations.py`

The translation tool builds localized pages for each active language in the registry, and it reads the English pages to swap the main text, menus, footers, and buttons.
The script translates UI terms, updates links, and sets response headers. The run writes a multilingual directory tree and search files.

### 4. `scripts/generators/build_lang_feeds.py`

This script creates RSS, Atom, news-sitemap, and JSON feeds for each language. It reads frontmatter records directly from the source markdown files to build the feeds.

### 5. `scripts/generators/build_agent_api.py`

JSON endpoints expose articles and topics for search tools and AI clients. These feeds are linked from the plugin manifests and described by the OpenAPI schema.

### 6. `scripts/generators/build_lead_magnets.py`

This tool compiles source files into PDF resources such as checklists.

### 7. `scripts/postbuild.py`

The postbuild script processes every page to apply optimization steps before saving.

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
