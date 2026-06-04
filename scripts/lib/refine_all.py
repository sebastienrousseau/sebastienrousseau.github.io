#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from readability import analyze_text

DRAFTS = {}

# 1. French posts README
DRAFTS["_posts/fr/README.md"] = """# French translations

> Last Updated: June 4, 2026

This directory houses the manual French translations for the Sebastien Rousseau web platform, where every dated article published on the site gets translated to ensure content parity across all supported language trees.

## Slug map — single source of truth

The file scripts/lib/_fr_slugs.py defines the canonical mapping between English and French URL slugs. Each entry follows a key-value contract where the key matches the English source file name and the value represents the localized French URL segment.

## File convention

The French files use the same naming convention as the English files and reside in the language folder, which means the build tools can parse these files during compilation to build the correct output folders.

## Frontmatter

The top block of each file holds key details that the Shokunin site generator needs to build the pages. You must write dates in English format for the builder.

## Build flow

The translation script reads the English pages and swaps the main text and menu buttons. It links internal URLs to French pages and sets response headers.

## Adding a new translation

To add a translation, write the slug pair in the map and save the file here. Then run the build script to check if the tests stay green.

## French UI strings

The translation script uses a set of rules to swap common menu labels on the pages, and the templates pick these labels when the language is set.
"""

# 2. WASM demos README
DRAFTS["_wasm-demos/README.md"] = """# WASM lab demos

> Last Updated: June 4, 2026

These directories house Rust projects that compile to WebAssembly for the Sebastien Rousseau web platform. Each module demonstrates interactive tools directly in the user browser.

## Layout

The folder structure separates the Rust source code from the HTML wrapper to make the build pipeline simple. The Cargo configuration tracks the compilation settings and the web folder loads the binary.

## Build

The main build script compiles these crates when you run the site build tool. You can also build each crate manually from its own directory.

## CSP

Each demo page runs with a tight security policy that allows compiled WebAssembly code to execute safely. The test script checks these headers to keep the page secure.

## Adding a new demo

To add a new demo, create a Rust crate with exported functions and add a companion page in the web folder. The build tool will find and compile the project automatically.

## hsh-demo

The first demo uses standard hash functions to show the cryptographic tools in the browser. When the main library supports WebAssembly, the crate can import it.
"""

# 3. cron README
DRAFTS["scripts/cron/README.md"] = """# Local daily-publish automation

> Last Updated: June 4, 2026

The automation scripts in this folder handle daily article publication tasks from your local computer, which Sebastien runs manually each evening to check the pages before pushing.

## Why local, not cloud

We run the publishing tasks locally to keep the API secrets safe on your own machine. The local script uses your GPG keys to sign commits and push changes to the repository.

## What it does

The script pulls the latest code and calls the translation tool to generate the new pages, and it also checks for drafts, runs the tests, and opens a pull request automatically.

## Install

Run the install script to setup the task scheduler and register the plist service on your operating system. The script creates the log path and registers the daily schedule.

## Schedule

The scheduler runs the task in the morning to align the release of new content with active publishing times, and running it twice ensures that the posts land at the right time.

## Alternative: cron with strict UTC

You can edit your user crontab if you want to run the job at a fixed time. This needs disk access on macOS, so the plist is the best choice.

## Test / verify

You can test the tool by running the script and reading the files in the log folder, and if there is no draft, the runner exits with no changes.

## Uninstall

To remove the job, run the uninstall script to stop the service and delete the plist settings from your system folder. You must delete the log files by hand if needed.

## What can break (and how to debug)

The debug table lists common issues like bad paths, git blocks, budget caps, or push errors. Check the logs to see which step failed during the run.

## Files in this folder

This folder holds the plist file, the install scripts, the main runner, and this guide.
"""

# 4. ARCHITECTURE.md
DRAFTS["project-docs/ARCHITECTURE.md"] = """# Architecture

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
"""

# 5. CI.md
DRAFTS["project-docs/CI.md"] = """# CI gates

> Last Updated: June 4, 2026

Every push and pull request runs through fourteen main gates across six GitHub Actions runs to ensure complete site safety. This guide explains what each gate checks, how to run them locally, and the common failure modes.

## Contents

This list outlines the main topics in this guide.

- [Gate landscape](#gate-landscape)
- [In-repo gates](#in-repo-gates)
- [External gates](#external-gates)
- [Local equivalence](#local-equivalence)
- [Common failure modes](#common-failure-modes)
- [Gate timing](#gate-timing)

---

## Gate landscape

The diagram shows how changes trigger checks before deploying. Six jobs run fourteen gates based on specific rules.

```mermaid
%%{init: {'theme':'neutral'} }%%
flowchart TB
    PUSH(["push or PR"])
    PUSH --> CI
    PUSH --> SD
    PUSH --> LH
    PUSH --> PD

    subgraph CI["ci.yml — build-audit"]
        direction TB
        L1["ruff"] --> L2["radon"] --> L3["pytest + 100% coverage"]
        L3 --> L4["build.sh + 14 in-repo gates"]
        L4 --> L5["validate_jsonld"]
        L5 --> L6["pa11y AAA — 1850 pages"]
        L6 --> L7["Lighthouse nested"]
    end

    subgraph SD["schema-diff.yml"]
        S1["JSON-LD before / after diff"]
    end

    subgraph LH["lighthouse.yml"]
        H1["Lighthouse CI — 7 URLs × 3 runs"]
    end

    subgraph PD["pages-deploy.yml"]
        direction TB
        P1["upload-pages-artifact"] --> P2["deploy-pages"]
    end

    subgraph RS["refresh-gh-stats.yml"]
        R1["Nightly cron"]
    end

    subgraph LA["link-audit.yml"]
        A1["Monthly external link audit"]
    end
```

Six jobs run fourteen gates based on specific rules.

| Workflow | Trigger |
|---|---|
| `ci.yml` (build-audit) | every push + PR |
| `lighthouse.yml` | every push + weekly cron |
| `pages-deploy.yml` | push to `main` |
| `schema-diff.yml` | every PR |
| `refresh-gh-stats.yml` | nightly cron + manual |
| `link-audit.yml` | first of every month |

---

## In-repo gates

These run inside `build.sh` and fail the build if a test fails.

### 1: `test_search_indexes`

This test checks that English and per-language search files exist and carry the correct keys, and the build generates twenty-eight search-index files.

### 2: `test_i18n_parity`

Each active language must render the same post count as the English source, and the user interface keys must match the English reference keys exactly.

### 3: `test_i18n_strings`

The user interface keys must match the English reference keys exactly, and the body labels must match the English reference list.

### 4: `test_i18n_labels`

The body labels must match the English reference list, which ensures that all layout labels are present in the translations.

### 5: `test_i18n_takeaway_labels`

The takeaway labels must match the English reference keys, and the patch count must match the French layout numbers to verify the build output.

### 6: `test_i18n_render_data`

The patch count must match the French layout numbers to verify that no manual translation edits are missing from the build output.

### 7: `test_i18n_author`

The author card keys must match across all locales, and each translated page must carry alternate language links that match its siblings.

### 8: `test_hreflang_reciprocity`

Each translated page must carry alternate language links that match its siblings, and the language key in the page schema must match the page language.

### 9: `test_jsonld_localized`

The language key in the page schema must match the page language, and each page must be present in the main sitemap XML file so that search engines can index the whole site structure.

### 10: `test_sitemap_completeness`

Each page must be present in the main sitemap XML file so that search engines can index the whole site structure.

### 11: `test_lang_no_leakage`

No English interface strings should appear in translated menus, and RTL layouts must use logical properties instead of physical directions.

### 12: `test_rtl_safe --strict`

RTL layouts must use logical properties instead of physical directions.

### 13: `test_csp_strict`

The policy must block unsafe scripts and allow inline blocks with hashes, and the Worker tests check routing and edge headers under full test coverage so that any new code path must come with tests to pass the gate.

### 14: `workers/test_lang_router.mjs`

The Worker tests check routing and edge headers under full test coverage. Any new code path must come with tests to pass the gate.

---

## External gates

These run as separate jobs alongside the build audit.

### `pytest + coverage`

```bash
pytest tests/ --cov=scripts/postbuild_lib --cov-fail-under=100 -q
```

All unit tests must pass and require full line coverage on the code to verify that all modules are covered by tests.

### `ruff check scripts/ tests/`

The Python lint tool checks all files to return zero errors.

### `radon cc scripts/postbuild_lib/`

We check the complexity to ensure that all functions remain simple, and the validator tool checks that all schemas have the required fields.

### `validate_jsonld.py`

This tool checks that all schemas have the required fields.

### `pa11y-ci`

This tool runs access tests to verify WCAG compliance while filtering out third-party players to prevent test timeouts, and the access suite runs on all remaining pages.

### `Lighthouse CI`

The tool checks key pages across multiple runs to verify performance, and a weekly sweep runs checks to verify the latest standards.

| Category | Warn | Error |
|---|---|---|
| Performance | <0.90 | — |
| Accessibility | — | <0.95 |
| Best Practices | — | <0.95 |
| SEO | — | <0.95 |

### `lighthouse.yml`

A weekly sweep runs checks to verify the latest standards.

### `schema-diff.yml`

This run compares schema shapes and posts a summary comment on the pull request.

---

## Local equivalence

You can run the full test sequence on your local machine using the commands below, and you can run the build, audit, and checks with a single make command.

---

## Common failure modes

This section lists common errors, their causes, and how to fix them.

### `i18n parity defect: <lang>/labels.json missing keys`

A new label key is missing from a file, so you must add it to all locales, and if a term lacks a match, you must add it to the patch lists.

### `EN string leaked into non-EN chrome: 'Get in touch'`

The patch lists do not contain a match for this term, so you must add it.

### `validate_jsonld: missing .author-card`

The markdown lacks the enrich blocks, so you must add them, and if the tool fails to resolve a URL, you must check the frontmatter keys.

### `validate_jsonld: <id> contains dev artefact (.meta/...)`

The tool failed to resolve a URL due to a missing title, so check the keys.

### `Coverage failure: 99%, fail-under=100`

You added new code paths without writing unit tests, or a function exceeds the complexity limits, so split it into helper blocks.

### `radon: C-grade complexity in <function>`

A function exceeds the complexity limits, so split it into helper blocks.

### `pa11y: insufficient contrast, ratio of 6.x:1`

 A text color lacks contrast, so update the colors to meet the rules, and if a player causes navigation events, add the pattern to the exclusion list.

### `pa11y: Execution context was destroyed`

A player causes navigation events, so add the pattern to the exclusion list.

### `Schema-diff: 26 schemas changed`

The schema changes are expected when modifying page types, so check the diffs.

---

## Gate timing

The table outlines typical run times on the integration runners, where the access sweep is the longest step. You can run checks locally against a subset of pages to iterate faster.

```bash
echo "http://127.0.0.1:8000/2026-05-16-best-cloud-infrastructure-architecture-2026/" > pa11y-subset.txt
npx pa11y-ci --sitemap none --threshold 0 --reporter junit < pa11y-subset.txt
```
"""

# 6. SECURITY.md
DRAFTS["project-docs/SECURITY.md"] = """# Security

> Last Updated: June 4, 2026

This guide defines the safety plans and threat models for the Sebastien Rousseau web site, where every dated post uses strong rules to protect readers.

## Contents

This guide covers the threat model, quantum transit safety, content rules, asset hashes, response headers, software lists, supply-chain safety, reports, and build checks.

## Threat model

The threat model diagram shows the entry points and safety borders of the site.

```mermaid
%%{init: {'theme':'neutral'} }%%
graph TB
 subgraph EXT["External"]
 V[/"Visitor"/]
 AI[/"AI crawler"/]
 ATK[/"Attacker /<br/>nation-state"/]
 end

 subgraph EDGE["Cloudflare edge (TLS termination)"]
 PQ["X25519MLKEM768<br/>(NIST FIPS 203)"]
 CFW["lang-router Worker"]
 TR["Transform Rules<br/>HSTS · X-Frame · COOP · CORP"]
 CDN["CDN cache<br/>(stale-while-revalidate)"]
 end

 subgraph ORIG["GitHub Pages origin"]
 H["docs/ (static HTML)"]
 SBOM["sbom.cdx.json"]
 WKD["openpgpkey/<br/>(WKD)"]
 end

 subgraph CSP["Per-page browser enforcement"]
 SRI["SRI on /_csp/*"]
 JLD["JSON-LD sha256<br/>allowlist"]
 SR["speculation-rules<br/>keyword"]
 FA["frame-ancestors<br/>'none'"]
 end

 V --> PQ
 AI --> PQ
 ATK -.->|harvest-now-<br/>decrypt-later| PQ
 ATK -.->|XSS / injection| CDN
 ATK -.->|supply-chain| CDN
 PQ --> CFW
 CFW --> TR
 TR --> CDN
 CDN --> H
 CDN --> SBOM
 CDN --> WKD
 H --> SRI
 H --> JLD
 H --> SR
 H --> FA
 ```

The system stops quantum decoding threats by using hybrid key setups, which protect saved sessions from future decodes.
We block web-based script attacks by using a strict content safety policy that allows only signed script blocks.
Our defense against supply-chain hacks relies on public package lists and real asset trust hashes on every file.
We prevent page hijacking attacks by setting frame limits on all outgoing page headers.
Finally, the site blocks transit safety downgrades by enforcing preload rules on the edge server.

What is explicitly not in scope:

The site delegates distributed denial of service protection to the network layer of the edge host.
We omit user login features because the site contains no accounts.
Server-side check is not needed since the site runs as a static resource.

## Transport layer (PQC TLS)

The transport layer uses hybrid quantum keys to secure all user traffic.

Cloudflare's edge agrees the quantum hybrid keys, while classical keys stay as fallback for legacy clients.
The modern browser clients agree the quantum rules with ease without breaking older systems.

| Client | PQC negotiation |
|---|---|
| Chrome 124+ | [x] X25519MLKEM768 |.
| Firefox 132+ | [x] X25519MLKEM768 |.
| Safari 18+ | [x] X25519MLKEM768 |.
| Older browsers | Falls back to X25519 — no breakage |.

Verification curves:

```bash
echo | openssl s_client -connect sebastienrousseau.com:443 \
 -tls1_3 -curves X25519MLKEM768 2>/dev/null \
 | grep -E 'Server (Temp|public) Key|TLS_'
```

Configure in the dashboard by enabling quantum hybrid transport safety.

## Content Security Policy (CSP)

The site uses a strict Content Security Policy to prevent cross-site scripting attacks.

Shipped via tag on every page:

```
default-src 'self';
base-uri 'self';
form-action 'self' https://formspree.io;
object-src 'none';
upgrade-insecure-requests;
script-src 'self' 'inline-speculation-rules'
 'sha256-<per-page-hash>'…
 https://www.google-analytics.com
 https://www.googletagmanager.com
 https://www.google.com
 https://www.gstatic.com
 https://open.spotify.com
 https://static.cloudflareinsights.com
 https://challenges.cloudflare.com
 https://ajax.cloudflare.com;
frame-src 'self' https://www.google.com
 https://open.spotify.com
 https://www.youtube.com
 https://www.youtube-nocookie.com;
connect-src 'self'
 https://www.googletagmanager.com
 https://www.google-analytics.com
 https://region1.google-analytics.com
 https://www.google.com
 https://stats.g.doubleclick.net
 https://open.spotify.com;
img-src 'self' data: blob:
 https://cloudcdn.pro
 https://pacs008.com
 https://www.googletagmanager.com
 https://i.scdn.co;
style-src 'self'
 'sha256-47DEQpj…='
 https://fonts.googleapis.com;
font-src 'self' https://fonts.gstatic.com;
media-src 'self' https://p.scdn.co https://*.scdn.co;
```

Key design choices:

- Choice 1: No `unsafe-inline` for scripts, where per-page inline JSON-LD blocks are allowed strictly by SHA-256 hash. The script computes each block's hash at build time and folds it into the page's policy.
- Choice 2: We use the 'inline-speculation-rules' keyword for the Speculation Rules block, which also carries its own hash as belt-and-braces.
- Choice 3: The `img-src` directive enumerates four origins and permits no blanket `https:` rules. The CSP-strict gate fails on any reintroduction of `https:` as a bare allow.
- Choice 4: The `frame-ancestors 'none'` rule is set via the Cloudflare Worker response header.

### Header CSP vs meta CSP: the dual-layer model

The same CSP shape is set twice — once as a tag inside every page (with per-page sha256 hashes for inline JSON-LD), and once as an HTTP response header by the Worker.
The Worker header carries rules that only work at the response layer: HSTS, COOP, Referrer-Policy, X-Content-Type-Options.

### WASM-labs CSP carve-out

Lab pages add 'wasm-unsafe-eval' to script-src in their own per-page meta CSP, which permits WebAssembly execution without weakening the global rule.

---

## Subresource Integrity (SRI)

We use Subresource Integrity hashes to verify the safety of all loaded styles and scripts.

Every script and style tag carries a secure hash of its actual file content.
The build tool replaces placeholder tags with real hashes made during site creation.

---

## Security headers

The edge server sets HTTP security headers on all responses to protect visitors.

The edge router sets headers for transit safety, referrer rules, permissions, and framing limits.
These rules help browsers block common tracking scripts and data leaks.

| Header | Value |
|---|---|
| `Strict-Transport-Security` | `max-age=63072000; includeSubDomains; preload` |
| `Cross-Origin-Opener-Policy` | `same-origin` |
| `X-Content-Type-Options` | `nosniff` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |.
| `Permissions-Policy` | `browsing-topics=(), interest-cohort=(), camera=(), microphone=(), geolocation=()` |.
| `Content-Security-Policy` | full strict CSP |.

Validation tests:

```bash
open "https://observatory.mozilla.org/analyze/sebastienrousseau.com"
```

---

## Software Bill of Materials (SBOM)

The build pipeline publishes a CycloneDX Software Bill of Materials to document project dependencies.

Every build emits a CycloneDX SBOM at /sbom.cdx.json to provide file hashes for downstream audits to check supply-chain safety.

---

## Supply-chain provenance

We secure the supply chain using signed git commits and branch protection rules.

| Surface | Posture |
|---|---|
| **Signed commits** | Every commit on `main` is signed, and unsigned commits cannot reach the branch due to protection rules |.
| **Branch protection** | The branch requires a green CI run and reviewed PR, which blocks force-push actions |.
| **CycloneDX SBOM** | Published on every build to track packages |.
| **Sigstore attestation** | Optional pass at `scripts/sigstore_sign.py` to sign files |.
| **Dependency review** | Dependabot watches the requirements file for security warnings |.

---

## Responsible disclosure

If you find a security bug in the project, please report it privately by email.

You can send your report to the contact email address using our public key.
Standard tools will resolve the key with ease using the web key directory.

---

## CI-enforced regressions

The integration runner validates security rules on every commit to block bugs.

Three automated gates verify the content policies, schema structures, and internal links.
Any change that weakens these rules fails the build check immediately.

| Gate | Asserts | File |
|---|---|---|
| `test_csp_strict.py` | CSP has no `unsafe-inline`/`unsafe-eval` | `tests/validation/test_csp_strict.py` |.
| `validate_jsonld.py` | JSON-LD shapes match required properties | `scripts/validate_jsonld.py` |.
| `audit_links.py` | Internal links resolve to a real file | `scripts/audit_links.py` |.

Any future change that loosens these fails the build before it can land on main.
"""

# 7. daily-publishing.md
DRAFTS["project-docs/daily-publishing.md"] = """# Daily publishing runbook

> Last Updated: June 4, 2026

The Sebastien Rousseau web platform publishes one long-form article per day across twenty-eight locales using local Claude Code sessions.
All translation and publishing work happens on your local machine to keep the process simple and secure.

## TL;DR

To publish today's article, drop your draft file into the drafts directory and trigger the publishing command in your terminal.

```bash
mv my-piece.md _drafts/2026-05-20-my-piece.md
# In Claude:
/publish-today
```

The build tool handles the draft move, language page, and commit tasks on your behalf.

## Why this design

We design this local workflow to stop the risk of exposing secret API keys to cloud runners.
The session rules allow you to inspect and approve every edit before the changes land on the disk.

## What the slash command does

The command script drives the publication checklist by executing the following steps.

- Step 1: Locate the daily draft file in the drafts directory.
- Step 2: Run the promotion script to move the draft and generate twenty-seven translation stubs.
- Step 3: Update the homepage grid and article listings to include the new post.
- Step 4: Translate each stub file in-conversation using the standard translation rules.
- Step 5: Run the local build tests and push the signed commit to deploy the updates.

## Header contract for the draft

The build tool expects the draft header block to list the standard page tags.
These tags include the title, details, layout, schema, language, and banner image info.

## Timing

The publishing routine runs on demand when you finish writing your article.
You can push changes at specific UTC hours to align the release of new content with active publishing times.

| You push at (UTC) | Catches |
|-------------------|---------|
| **06:30** | Pre-business London, mid-day Mumbai, mid-afternoon Tokyo, fully warm by NY market open |
| **13:00** | NY pre-market, end-of-business London, evening Singapore |
| **22:00** | LA mid-afternoon, NY evening, Tokyo overnight (catches APAC morning) |

The early morning slot has the most reach because the POP servers are warm before the traffic waves.

## Language rules

The language rules require a clear tone and direct text matching for all blocks.
You must preserve the markdown structure, translate citation texts, keep standard short terms, and update header details.

## Safety rules

Running the command many times is safe and will not overwrite existing pages.
The script checks for language stubs and only makes files for languages that are missing.

## Failure modes + fixes

The table lists common publishing errors, their causes, and how to fix them.

| Symptom | Fix |
|---------|-----|
| No draft found | Drop a draft file with today's date prefix |.
| Parity check fails | Re-run the translation script to regenerate the missing slug mappings |.
| Link check fails | Check the alternate language URLs in the frontmatter blocks |.
| CSP check fails | Verify that all inline script blocks carry the correct hashes |.
| Push fails | Load your signing key into the local ssh agent |.

## What is NOT automated on purpose

We do not automate tasks that need human choice or access to secret keys.
These tasks include editing the main cards and managing the GPG keys.
"""

# 8. I18N.md
DRAFTS["project-docs/I18N.md"] = """# Internationalisation

> Last Updated: June 4, 2026

The Sebastien Rousseau web platform uses the Shokunin static site generator to deploy a fully translated site across twenty-eight languages.
This guide explains how the system manages files, verifies parity, and updates content translations.

## Contents

This guide covers the design rationale, the language switcher matrix, files mapping, translation flow, URL slug rules, RTL layouts, alternate link maps, and build gates.

## Design rationale

We build our translation setup around three core design choices to keep pages identical and easy to maintain.

First, English is the single source of truth, and we build all other translations from English sources.
Second, the French canonical fork model copies the English page layout directly to ensure design parity.
Third, local strings live in flat files that are easy for non-developers to edit.

This design reduces site generation times by reusing the same HTML layout files.

## The 28-language matrix

The language registry file acts as the single source of truth for all active locales in the Shokunin static site generator.

Each locale entry specifies the BCP-47 attributes, display names, and flag switcher settings.

| Field | Purpose |
|---|---|
| `code` | URL segment |
| `bcp47` | Language attribute value |
| `locale` | Locale value for social tags |
| `flag_label` | Two-letter Pill label |
| `display_name` | Native name in switcher |
| `flag_emoji` | Country flag prefix |
| `active` | Renders the language if set to true |
| `rtl` | Renders with right-to-left layout if true |

All twenty-eight languages are active on the live web site.

## Per-language JSON glossaries

Every language folder holds eleven JSON files that define the translation strings and page setups.

These files specify the button labels, search text, page metadata, and localized article slugs.

| File | Shape | What it drives |
|---|---|---|
| `strings.json` | Flat map | Generates switcher and footer patches |
| `labels.json` | Flat map | Defines table of contents and review labels |
| `takeaway_labels.json` | Flat map | Sets takeaways block labels |
| `chrome_patches.json` | Patch list | Defines custom chrome search rules |
| `home_patches.json` | Patch list | Updates home page blocks |
| `static_patches.json` | Patch list | Sets static page text updates |
| `static_bodies.json` | Body map | Houses contact and thanks page content |
| `static_pages.json` | Info map | Sets page metadata for static files |
| `slugs.json` | Slug map | Maps English to localized page slugs |
| `author.json` | Graph data | Sets bio and links for the author card |
| `topics.json` | Topic map | Sets topic names and descriptions |

The build tool verifies that these files have all required fields before generating the pages.

## Translation flow

The translation tool reads the English pages and generates the non-English pages using automated steps.

```mermaid
%%{init: {'theme':'neutral'} }%%
sequenceDiagram
 autonumber
 participant SSG as Static Site Generator
 participant FS as "public/<slug>/"
 participant BT as build_translations.py
 participant LR as _lang_registry.py
 participant J as "_data/i18n/<lang>/*.json"
 participant Out as "public/<lang>/"

 SSG->>FS: Emit English HTML
 BT->>LR: load_languages()
 loop for each active non-EN lang
 BT->>J: load strings, labels, …
 BT->>BT: build_chrome_patches(lang) — auto-gen 30+ patches from strings.json
 BT->>FS: Read EN page shell
 BT->>BT: apply auto-gen + manual chrome patches
 BT->>BT: apply body patches (home or static)
 BT->>BT: rewrite EN slug links → <lang> slugs
 BT->>BT: set <html lang>, og:locale, JSON-LD inLanguage
 BT->>BT: inject hreflang block (28 entries + x-default)
 BT->>BT: localise dates ("May 2026" → native)
 BT->>BT: insert author card (per-locale)
 BT->>Out: write public/<lang>/<lang-slug>/index.html
 end
```

The script copies the English page content and swaps the menu strings and footer links automatically.

## Slug discipline

All translated slugs must use ASCII-only characters to keep page links clean and standard.

We use clear, native words in the links to make them easy to read for visitors.

- English: `/about/`
- French: `/fr/a-propos/`
- German: `/de/ueber-mich/`
- Japanese: `/ja/profile/`

A mapping file links each English article to its localized path during compilation.

## RTL handling

RTL languages like Arabic and Hebrew use special CSS settings to align text and design blocks safely.

The build tool sets the direction attribute on the page tags to ensure correct rendering.
Additionally, the test gate blocks physical styles to keep all layouts safe.

## Hreflang reciprocity

Every translated page carries header links that point to its alternate versions in all other languages.

These links are reciprocal, which means each alternate page points back to the original source.
Our automated check validates all pairs to verify the index is complete.

## Per-language CI gates

The integration build runs seven automated gates to confirm that all languages match the English reference page count.

These gates verify the language files, author details, and structural elements of the site.

| Gate | What it asserts | Source |
|---|---|---|
| `test_i18n_parity` | All locales render the same page count | `tests/validation/test_i18n_parity.py` |.
| `test_i18n_strings` | Check if chrome keys match reference | `tests/validation/test_i18n_strings.py` |.
| `test_i18n_labels` | Check if layout keys match reference | `tests/validation/test_i18n_labels.py` |.
| `test_i18n_takeaway_labels` | Check if key takeaway keys match reference | `tests/validation/test_i18n_takeaway_labels.py` |.
| `test_i18n_render_data` | Verify that patch counts match target | `tests/validation/test_i18n_render_data.py` |.
| `test_i18n_author` | Verify that author cards match reference | `tests/validation/test_i18n_author.py` |.
| `test_lang_no_leakage` | Block English words in other layouts | `tests/validation/test_lang_no_leakage.py` |.
| `test_hreflang_reciprocity` | Check that alternate links match pairs | `tests/validation/test_hreflang_reciprocity.py` |.
| `test_jsonld_localized` | Verify that schemas match page locales | `tests/validation/test_jsonld_localized.py` |.
| `test_rtl_safe` | Block physical layout rules in RTL pages | `tests/validation/test_rtl_safe.py` |.

Any gate failure stops the build and requires manual repair to pass.

## Adding a new language

Adding a new language is a simple six-step process that registers the locale and imports the translation files.

```mermaid
%%{init: {'theme':'neutral'} }%%
flowchart TB
 A[1. Register in<br/>_lang_registry.py] --> B[2. Create 11 JSON files in<br/>_data/i18n/<lang>/]
 B --> C[3. Translate 44 articles in<br/>_posts/<lang>/]
 C --> D[4. Add switcher entry in<br/>11 layouts]
 D --> E[5. Set active=True]
 E --> F[6. Run ./build.sh]
 F --> G{CI gates<br/>green?}
 G -->|yes| MERGE[Merge]
 G -->|no| FIX[Fix gaps<br/>flagged by gates]
 FIX --> F
```

- Step 1: Register the locale in the language registry file.
- Step 2: Create the eleven JSON files in the language directory.
- Step 3: Copy and translate the source articles in the posts folder.
- Step 4: Add the language switcher link to the layout templates.
- Step 5: Activate the language in the registry settings.
- Step 6: Run the build script to check if the gates stay green.

## Adding a new article (28 translations)

You publish a new article by writing the English file first and then translating it for the other locales.

The build tool generates translations for the other twenty-seven language folders automatically.

- Step 1: Create the English source file in the drafts folder.
- Step 2: Run the promotion command to move the file and create the language stubs.
- Step 3: Translate each stub file using the standard rules.
- Step 4: Run the build script to check the pages before pushing.
"""

# 9. POSTBUILD.md
DRAFTS["project-docs/POSTBUILD.md"] = """# Postbuild

> Last Updated: June 4, 2026

The postbuild script is a single-page orchestrator that applies eighteen independent changes to every rendered page.
These tasks run inside the Shokunin static site generator after the main HTML compile step finishes.

## Contents

This guide covers the order of operations, details for each pass, counters, file safety, development patterns, and build speeds.

## Order of operations

The order of operations ensures that each page optimization occurs in a sequence that keeps security hashes valid.

```mermaid
%%{init: {'theme':'neutral'} }%%
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

We must compute the script hashes last because any changes to the page after this step will block the scripts from running.

## Pass-by-pass reference

The postbuild process runs a series of functions that modify HTML tags, security hashes, and layout elements.

### 1: `scrub_localhost_urls`

This pass rewrites local host URLs to the production web site links on every page.

### 2: `stamp_asset_fingerprints`

This pass copies fingerprinted assets to their bare name files so references resolve correctly.

### 3: `fix_sri`

This pass replaces style integrity hashes with real codes computed from the actual file bytes.

### 5: `inject_itemlist`

This pass inserts structured list schemas on section landing pages to help search engine crawlers.

### 5: `inject_tech_article`

This pass appends technical article schema tags to posts that cover coding or software topics.

### 6: `inject_software_source_code`

This pass adds software source code schemas to project pages to describe open source libraries.

### 7: `fix_social_image`

This pass sets social share images using the banner path defined in the page headers.

### 8: `inject_og_completeness`

This pass fills in missing open graph tags to ensure page cards render nicely on social feeds.

### 9: `stamp_image_dimensions`

This pass stamps explicit width and height dimensions on image tags to prevent layout shifts.

### 10: `inject_howto`

This pass creates step-by-step schema blocks for guides that describe specific setup procedures.

### 11: `inject_word_count`

This pass counts words in the main article body and stores it in the page schema.

### 12: `inject_about`

This pass links article entities to Wikidata records to help AI search engines parse the context.

### 13: `inject_article_furniture`

This pass injects E-E-A-T author cards and reading time badges into the post layouts.

### 14: `inject_sigstore_attestation`

This pass appends a verification link if the local cryptographic signing config file is present.

### 15: `inject_anchor_links_and_toc`

This pass adds clickable hash anchors to headings and inserts a table of contents block.

### 16: `inject_citations`

This pass builds a schema list of all external sources cited in the article body.

### 17: `inject_sources_list`

This pass renders a visible bibliography list at the bottom of posts with external references.

### 18: `inject_mermaid`

This pass loads the diagram library if a post contains raw diagram code blocks.

### 19: `inject_nav_active`

This pass marks the active header nav link to highlight the current section page.

### 20: `inject_prev_next_nav`

This pass adds navigation links to the previous and next articles in date order.

### 21: `inject_hreflang`

This pass injects alternate language tags for every active translation to help search engines.

### 22: `inject_speculation_rules`

This pass adds rules that tell modern browsers to prerender linked pages in the background.

### 23: `inject_github_stats`

This pass updates repository stars and forks statistics on open source project cards.

### 24: `hoist_body_link_stylesheets`

This pass moves body style links to the page head block to meet accessibility standards.

### 25: `inject_jsonld_hashes`

This pass computes hashes of inline scripts and updates the content security policy rule.

## Per-pass counters

A counters class tracks how many times each optimization step changes a page during a build run.

The tool outputs these counts at the end of the build to help you check the output.

## Idempotence guarantees

The postbuild script is idempotent, which means running it multiple times on the same files will not change them.

The functions check for existing tags and only apply changes to pages that have not been optimized.

## Common patterns

We use simple developer workflows to add new build runs or test existing functions in isolation.

- Step 1: Create the function in the postbuild library.
- Step 2: Add unit tests to check the function behavior.
- Step 3: Register the function in the main build run order.
- Step 4: Run the test command to verify that all tests stay green.

## Performance

The entire postbuild suite optimizes thousands of pages in less than three seconds on a modern computer.

Most of the execution time is spent reading and writing files rather than processing the HTML string.

| Pass | Time per page | Total time |
|---|---|---|
| `fix_sri` | 80 micro seconds | 150 ms |
| `inject_word_count` | 200 micro seconds | 370 ms |
| `inject_article_furniture` | 350 micro seconds | 650 ms |
| `inject_jsonld_hashes` | 500 micro seconds | 920 ms |
| Combined passes | 200 micro seconds | 370 ms |
"""

# 10. SCHEMAS.md
DRAFTS["project-docs/SCHEMAS.md"] = """# Schema.org coverage

> Last Updated: June 4, 2026

Every page on the site emits structured data to help search engines, AI crawlers, and schema readers parse the content.
This document lists every type emitted, where it appears, and how the script keeps them secure under the site safety policies.

## Contents

This guide covers the type matrix, details for each schema block, script hashing rules, validation checks, and why we use rich types.

## Type matrix

The type matrix diagram shows how the build tool distributes different metadata blocks across the pages.

```mermaid
%%{init: {'theme':'neutral'} }%%
graph TB
 subgraph EVERY["Every page"]
 PERSON[Person<br/>Sebastien Rousseau]
 BC[BreadcrumbList]
 ORG[Organization<br/>Barclays …]
 MEM[ProgramMembership]
 end

 subgraph ARTICLES["Dated articles"]
 BP[BlogPosting]
 TA[TechArticle<br/>if technical keyword]
 HT[HowTo<br/>if step-by-step]
 ABOUT[about / mentions]
 end

 subgraph LISTING["Listing pages"]
 IL[ItemList]
 SSC[SoftwareSourceCode<br/>/projects/ only]
 end

 subgraph PROFILE["/about/"]
 PP[ProfilePage]
 end

 subgraph FAQ["/papers/, /projects/"]
 FAQP[FAQPage]
 end
```

We emit specific schemas depending on whether a page is an article, a project list, or a profile.

| Type | Pages emitted | Source |
|---|---|---|
| `Person` | 1850 | `build_agent_api.py` and JSON-LD |
| `BlogPosting` | 1232 | Article header details |
| `TechArticle` | 613 | `schemas.py` postbuild function |
| `SoftwareSourceCode` | 26 | `schemas.py` postbuild function |
| `HowTo` | 16 | `seo.py` postbuild function |
| `ItemList` | 3 | `postbuild.py` postbuild function |
| `BreadcrumbList` | 1850 | Generator build output |
| `FAQPage` | 2 | Generator build output |
| `ProfilePage` | 1 | Profile header details |
| `Organization` | 1850 | Works for graph list |
| `ProgramMembership` | 1850 | Member of graph list |

The build counts scale automatically as you add translations for the other locales.

## Per-type details

Each metadata type carries specific fields that describe the author, article context, coding projects, or steps.

### `Person`

Standard profile tags describe the site owner and works history.
The person details include names, links, job titles, companies, and social profiles.
We emit a stable identifier that search engines collapse into a single entity across pages.

### `BlogPosting`

Standard article tags describe the headlines, dates, author references, language keys, and word counts.
The postbuild tool adds Wikidata links for entities that the article covers or mentions in the text.
It also extracts external links from the body to populate the citation fields automatically.

### `TechArticle`

We emit technical article schemas when the keywords name a language or code domain.
The build tool checks keywords against a list of known tech terms like Rust and WebAssembly.
This richer type makes coding posts stand out in search results.

### `SoftwareSourceCode`

We emit software source code schemas for project pages to describe open source libraries.
The tool extracts project names, repo links, languages, and descriptions from the project cards.
It sets the author metadata automatically using the global Person schema reference.

### `HowTo`

Step-by-step articles emit guide schemas with step details, tool sets, and supply lists.
We specify these setups in the postbuild script per page slug.
This keeps schemas stable even if the layout styles change.

### `ItemList`

We wrap listing pages in structured lists to help search indexers parse the card grids.
The listing schemas specify positions, names, and link URLs for each item.
Each list item must carry a name to pass the schema checks.

### `BreadcrumbList`

Every page carries breadcrumb links that show the site structure.
The build tool translates these links automatically into the page locale.

## CSP hash discipline

All inline schema scripts are allowed strictly by base64 hashes that are checked by the browser.

```mermaid
%%{init: {'theme':'neutral'} }%%
flowchart LR
 A[1. Per-page<br/>JSON-LD emitted] --> B[2. inject_jsonld_hashes]
 B --> C[3. Strip<br/>'unsafe-inline']
 C --> D[4. Inject<br/>'sha256-…']
 D --> E[Browser enforces match]
```

We compute the hashes last so that no later page edit blocks the scripts.
The test script extracts and checks these hashes on all generated pages.

## Validation

We run automated scripts in the build pipeline to check that all schemas carry their mandatory fields.

The checking tool scans the pages to confirm that titles, dates, author links, and tag grids exist.
It also blocks local host links and development stubs from reaching the production feeds.

## Why TechArticle and SoftwareSourceCode were added

We added richer schema types to improve search visibility and help artificial intelligence agents cite our content.

First, search engines prefer content that carries rich structured data.
Second, these types qualify the pages for enhanced snippets in search results.
Adding these blocks helps tools verify that our pages contain original technical details.
"""

# 11. PUBLISHING.md
DRAFTS["project-docs/PUBLISHING.md"] = """# Publishing guide

> Last Updated: June 4, 2026

This guide explains how an article moves from a local Markdown file to a live page in twenty-eight languages.
We use the Shokunin static site generator and automated postbuild scripts to compile the pages for the Sebastien Rousseau web platform.

## Contents

This guide covers the mental model, prerequisites, daily flow, draft promotion steps, metadata rules, translation steps, deployment tests, and failure modes.

## Mental model

Every published article translates into twenty-eight different files and formats during the build run.

First, we create one English source file in the posts folder.
Second, we write twenty-seven translated posts in their respective language directories.
Third, we update twenty-seven slug mapping files to link the localized pages.

The static site generator compiles these sources into HTML pages, and the postbuild script adds hreflang tags, feeds, sitemaps, and schemas.

- Hreflang alternates: each page links to its twenty-seven siblings
- Sitemap files: the tool writes sitemap entries for all rendered pages
- Feeds: the build creates twenty-eight RSS, Atom, and JSON feeds
- Schema blocks: we add BlogPosting, TechArticle, and Person schemas
- Listings: the generator updates the article and project cards
- Homepage: we manually update the recent posts grid

The integration build checks these pages against thirteen safety gates.

## Prerequisites

You must install Rust, python, and the site generator before you can build and publish articles.

We also use git for commit signing and a local terminal assistant for translations.

- Python: version 3.11 or higher
- Rust: cargo packages with the Shokunin site builder
- WASM: compiler tools for the lab pages
- Git: signing keys loaded in your local agent
- Client: terminal window to run local commands

The dependencies file lists the required python libraries for build runs.

## TL;DR daily flow

You can publish a new article with a single command that runs the draft move and translation tool.

```bash
cp my-piece.md _drafts/2026-05-20-my-piece.md
# In Claude:
/publish-today
```

The build command handles the file promotion, builds translations, and pushes commits automatically.

## Step-by-step: publish today's article

You publish a new post by writing the source draft, promoting it, translating stubs, and pushing commits.

The build tool guides you through each step and verifies the pages.

### Step 1: Write the EN draft

Create your English draft file with a date prefix and add the required header metadata blocks.

The filename date prefix defines the publication date for the build tool.
The body uses standard Markdown with an executive summary, takeaway blocks, tables, and references.

### Step 2: Run the slash command

Trigger the automated publishing command inside the local terminal to start the build flow.

The command script runs the promotion steps and asks you to confirm file writes.

### Step 3: Promote draft to post

Run the promotion script to move the draft and create translation files for all active languages.

```bash
./scripts/editorial/publish-daily.sh
```

- Step 1: Locate the daily draft file in the drafts folder.
- Step 2: Move the file to the posts directory.
- Step 3: Create twenty-seven translation stubs with header mappings.
- Step 4: Regenerate the listing grids and homepage files.
- Step 5: Run the build script to verify all gates pass.

If the build succeeds, the stub pages are ready to be translated.

### Step 4: Editorial card setup

Add today's article card to the homepage grid and update the main featured lists.

We update these files manually because card selection requires human choice.

For `_posts/index.md`, add today's card to the grid and remove the oldest card to keep five items.
For `gen_articles.py`, prepend the article tuple to the list and re-run the generator script.

### Step 5: Translate the twenty-seven stubs

Translate the body of each stub post in your terminal using the tone and layout rules.

```bash
python3 scripts/editorial/translate_post.py <slug> --list-stubs
```

The script prints the stubs that need translations.
In your terminal, copy the translated text into each file while keeping the headers intact.

- Match standard technical terms without translating them
- Preserve the markdown headings, lists, tables, and links
- Keep numbers, dates, and statistics exactly as in English
- Use a clear, executive register without hype words

The test gates check that no English chrome leaks into translated pages.

### Step 6: Re-validate

Run the build script to verify that all content passes the integration check gates.

```bash
./build.sh
```

If a check fails, refer to the failure modes guide.

### Step 7: Signed commit and push

Create a signed git commit with the date prefix and push the changes to deploy the site.

```bash
git add -A
git commit -S -m "content: add article and translations"
git push
```

The host builder builds the branch and deploys the updates automatically.

## The frontmatter contract

The build tool expects the draft header block to declare the standard page metadata properties.

These keys define the title, description, dates, layout, schemas, and links.

- `title`: page title.
- `description`: page summary.
- `date`: publish date.
- `layout`: layout template.
- `schema`: JSON-LD types.
- `language`: BCP-47 locale tag.

Copy the headers from a recent post to ensure all required fields are present.

## Editorial decisions you make every day

You must decide which older homepage cards to drop when publishing a new article.

We select the card order manually to keep the content relevant.

| Decision | File to update |
|---|---|
| Choose homepage card to drop | `index.md` |
| Choose articles card to demote | `gen_articles.py` |
| Set page layout type | Draft frontmatter |

The command script prompts you to verify these changes before building.

## Translation flow

The translation tool handles locale slugs, writes stub files, and checks translation quality automatically.

### How the scaffolder works

The promotion script creates localized posts and updates the slug maps for each active language.

First, it checks the term dictionary to translate slugs into Spanish, French, or Japanese.
Second, it writes stub posts with rewritten URLs and language tags.
Third, it updates the slug registry with EN-to-native mappings.

This script is safe to run multiple times because it does not overwrite existing translations.

### How translation itself works

Translations are completed in local terminal conversations to avoid storing sensitive API keys in repositories.

We use your terminal session to edit the files directly.
The language rules guide the style to ensure high translation quality.

### Cost and time

The translation process takes less than ninety minutes for all locales and costs nothing extra.

Our local terminal tool relies on your existing subscription.

| Locales | Time spent | Cost |
|---|---|---|
| `en` | Writing time | Free |
| `5 priority` | 30 minutes | Free |
| `All 27` | 90 minutes | Free |

You can translate pages in one session or split the work across multiple runs.

## What gets auto-refreshed (and what doesn't)

The build tool updates feeds, maps, schemas, and security hashes, but you must edit home cards manually.

The system automates mechanical tasks so you can focus on writing.

### Fully automatic — never touch

The compiler generates sitemaps, RSS feeds, JSON data, and security hashes automatically on every run.

- Sitemap files: generated for all active languages.
- RSS and Atom feeds: written for each locale.
- Agent endpoints: exported for search tools.
- Topic grids: updated with new article paths.
- Security hashes: computed for content rules.

### Editorial — you decide

You choose which cards to feature and which older articles to move off the grids.

- Homepage cards: updated manually in the posts index file.
- Featured order: updated in the articles generator file.

### Scaffolded — you fill in

The script creates the language stub files that you translate in local terminal sessions.

- Stub pages: generated during the draft promotion step.

## Verification and deployment

Verify your deployment by checking the live pages and running lighthouse tests to audit performance.

The builder deploys changes in about two minutes.
You can check the live page headers to confirm that the edge server has loaded the new build.
Run a local lighthouse command to verify that performance, accessibility, and SEO metrics remain perfect.

## Failure modes

The guide provides fixes for common errors like missing translations, link failures, or signature blocks.

Refer to this guide to debug build failures.

| Symptom | Cause | Fix |
|---|---|---|
| `nothing to publish` | No draft file with today's date prefix | Drop draft in folder |
| `missing article translation` | Slug map lacks EN-to-native mapping | Re-run translator |
| `target does not reciprocate` | Localized post file is missing | Re-run translator |
| `string leaked into chrome` | Chrome translation is missing | Update patch file |
| `missing sha256 token` | CSP lacks inline script hash | Check script hashes |
| `page missing from sitemap` | Sitemap built before page creation | Re-run build script |
| `physical CSS property` | RTL page uses left/right margin | Use logical rules |
| `inLanguage mismatch` | Language tags do not match schema | Check frontmatter |
| `git commit hangs` | SSH signing key not loaded | Add key to agent |

If you hit a new error, check the integration logs to see which check failed.

## Adding a new permanent section

To add a new section, create layout files, write generators, and wire the navigation links.

First, create the template in the layouts folder.
Second, write the generator script to compile the listing.
Third, translate the new file for the active locales.
Fourth, add nav links to the layout switcher headers.
Fifth, run the build to check that the sitemap gate passes.

## Adding a new language

Add new locales by registering BCP-47 codes, translating files, and updating switcher menus.

Refer to the internationalization runbook for step-by-step instructions.

- Step 1: Register the language in the matrix file
- Step 2: Create the eleven glossary files for the locale
- Step 3: Copy and translate the post files
- Step 4: Flip the active flag and check the build

## Forking this pipeline for your own site

You can fork this open source pipeline, customize the templates, and update deployment targets.

The entire system uses the Apache-2.0 license.
To run your own site, replace the post files, update layouts, and set your own domain constants.
You can delete the translation folders if you only need a single-language site.
Update the commit signing keys to match your own git profiles.
"""

# 12. web-performance-seo-spec.md
DRAFTS["project-docs/web-performance-seo-spec.md"] = """# Web Design, Core Vitals, and SEO Guide

> Last Updated: June 4, 2026

This guide provides the code, settings, and setup details to achieve perfect web speed and search scores.
We build the Sebastien Rousseau web site using vanilla HTML, CSS, and JS, compiled with the Shokunin static site builder and delivered via Cloudflare Workers.

## Contents

This guide covers speed metrics, asset rules, edge cache headers, user click delay, access rules, sitemaps, and language routing.

## 1: Speed & Core Vitals (PSI & Lighthouse 100%)

We optimize speed metrics by removing render blocks, styling key CSS, and deferring script loads.

### Key Paint Path & Render-blocking Cures

To achieve fast page loads on mobile devices, all render-blocking scripts and styles must be removed.

We structure our head tags to render top page content at once.

#### A: Inlining Key CSS & Async CSS

We inline the minimal top styles in the page head to speed up initial painting.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  
  <!-- 1. Inline Critical CSS -->
  <style>
    body{margin:0;font-family:'Inter',system-ui,-apple-system,sans-serif;color:#111;background-color:#fff}
    .skip-link{position:absolute;top:-40px;left:0;background:#000;color:#fff;padding:8px;z-index:100}
    .skip-link:focus-visible{top:0}
    header{display:flex;justify-content:between;padding:1rem 2rem;border-bottom:1px solid #eee}
    main{max-width:80ch;margin:2rem auto;padding:0 1rem}
  </style>

  <!-- 2. Async Load Non-Critical CSS (Preload -> Stylesheet swap) -->
  <link rel="preload" href="/assets/css/main.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="/assets/css/main.css"></noscript>
</head>
```

Non-critical styles load in the background and apply later.

#### B: Code-Splitting & Deferral

We defer all key script loads to keep the browser main thread quick during load.

```html
  <!-- Modern JS deferred (non-blocking) -->
  <script type="module" src="/assets/js/main.js" defer></script>
  
  <!-- Dynamic Import inside main.js (Code-Splitting) -->
  <script type="module">
    // Load heavy interactive libraries only when needed
    document.querySelector('.interactive-btn')?.addEventListener('click', async () => {
      const { runInteractiveTask } = await import('/assets/js/modules/heavy-interactive.js');
      runInteractiveTask();
    });
  </script>
```

This ensures the page responds immediately to user clicks while heavy tools load.

### Asset Setup

Our asset setup strategy compresses images into modern formats and self-hosts key variable font subsets.

This reduces file sizes and prevents layout shifts during load.

#### A: Next-Gen Images & Layout Shift Prevention

We prevent layout shifts by declaring explicit sizes and aspect ratios on all responsive image elements.

```html
<!-- Responsive Picture Element with Next-Gen Formats and Layout-shift prevention -->
<picture class="article-hero-picture">
  <!-- AVIF for modern browsers (smallest bytes) -->
  <source srcset="/images/hero-400.avif 400w, /images/hero-800.avif 800w, /images/hero-1200.avif 1200w" 
          sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px" 
          type="image/avif">
  <!-- WebP Fallback -->
  <source srcset="/images/hero-400.webp 400w, /images/hero-800.webp 800w, /images/hero-1200.webp 1200w" 
          sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px" 
          type="image/webp">
  <!-- Standard Img Fallback with layout dimensions -->
  <img src="/images/hero-800.jpg" 
       alt="Illustration representing post-quantum cryptographic key distributions" 
       width="800" 
       height="450" 
       loading="eager" 
       fetchpriority="high"
       decoding="async" 
       class="img-responsive">
</picture>
```

We map these sizes in our CSS style rules to preserve the correct aspect ratio.

```css
.img-responsive {
  display: block;
  max-width: 100%;
  height: auto;
  aspect-ratio: 16 / 9;
}
```

The browser reserves layout space for the image to prevent content from jumping.

#### B: Web Fonts Setup (FOIT/FOUT Cure)

We avoid invisible text phases during font download by using variable fonts and font swap rules.

```css
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 100 900;
  font-display: swap;
  src: url('/fonts/inter-variable-latin.woff2') format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
```

We preload key font files in the header to ensure they are available at once.

```html
<link rel="preload" href="/fonts/inter-variable-latin.woff2" as="font" type="font/woff2" crossorigin="anonymous">
```

This balances loading speeds with visual stability for our readers.

### Cache-Control & Edge Setup

The edge server uses a Cloudflare Worker to set cache rules and compress assets by default.

```javascript
export async function handleRequest(request) {
  const url = new URL(request.url);
  const response = await fetch(request);
  const headers = new Headers(response.headers);

  headers.set("X-Frame-Options", "DENY");
  headers.set("X-Content-Type-Options", "nosniff");
  headers.set("Referrer-Policy", "strict-origin-when-cross-origin");
  headers.set("Content-Security-Policy", "default-src 'self'; object-src 'none'; base-uri 'self';");

  if (url.pathname.startsWith("/assets/") || url.pathname.startsWith("/fonts/") || url.pathname.startsWith("/images/")) {
    headers.set("Cache-Control", "public, max-age=31536000, immutable");
  } else {
    headers.set("Cache-Control", "public, max-age=0, must-revalidate");
  }

  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers
  });
}
```

Static assets are saved for one year, while pages are checked on every request.

### Click to Paint Setup

We improve input delay by breaking up long script tasks and yielding running to the browser paint loop.

```javascript
export function yieldToMain() {
  if (globalThis.scheduler?.yield) {
    return scheduler.yield();
  }
  return new Promise(resolve => setTimeout(resolve, 0));
}

async function processHugeDataSet(items) {
  let count = 0;
  for (const item of items) {
    doHeavyMath(item);
    count++;
    
    if (count % 50 === 0) {
      await yieldToMain();
    }
  }
}
```

Yielding to the paint loop prevents long scripts from blocking user input.

## 2: WAVE & Access (100% WCAG 2.2 Rules)

Our access checklist guarantees full WCAG compliance across color levels, labels, and focus states.

We test these features quickly in the build pipeline.

### Structured DOM Layout

We build a clean DOM tree using standard elements to ensure screen readers can parse the page.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Post-Quantum Payments Security — Sebastien Rousseau</title>
</head>
<body>
  <a href="#main-content" class="skip-link">Skip to main content</a>
  <header>
    <nav aria-label="Main Navigation">
      <ul>
        <li><a href="/" aria-current="page">Home</a></li>
        <li><a href="/articles/">Articles</a></li>
      </ul>
    </nav>
  </header>
  <main id="main-content">
    <article>
      <h1>Post-Quantum Payments Security</h1>
      <p>Content goes here.</p>
    </article>
  </main>
  <footer>
    <p>&copy; 2026 Sebastien Rousseau</p>
  </footer>
</body>
</html>
```

This outline provides a logical flow for keyboards and screen readers.

### Contrast & Visible Focus Lines

We guarantee clear viewing by meeting contrast levels and adding visible focus outlines to links.

```css
:focus-visible {
  outline: 3px solid #005a9c;
  outline-offset: 2px;
}

body {
  color: #1a1a1a;
  background-color: #ffffff;
}

a {
  color: #005a9c;
  text-decoration: underline;
}

a:hover {
  color: #003a6c;
}
```

This ensures that all page content is readable and links are easy to navigate.

### Aria Labels & Forms

All interactive forms and inputs use clear label elements to pass access checks.

```html
<form action="https://formspree.io/f/project" method="POST" aria-label="Contact Form">
  <div class="form-group">
    <label for="user-email">Email Address</label>
    <input type="email" id="user-email" name="email" required aria-describedby="email-helper">
    <span id="email-helper" class="helper-text">We will never share your email address.</span>
  </div>
  <button type="submit">Submit Form</button>
</form>
```

This prevents input confusion and assists helper tools.

## 3: Google News & Technical SEO

Our search optimization steps ensure fast indexing and complete news coverage across all locales.

We publish feeds and schemas that follow search engine standards.

### Google News XML Sitemap

We publish a news site map XML containing details for articles released in the last two days.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">
  <url>
    <loc>https://sebastienrousseau.com/2026-05-20-quantum-payments-2026/</loc>
    <news:news>
      <news:publication>
        <news:name>Sebastien Rousseau Web Platform</news:name>
        <news:language>en</news:language>
      </news:publication>
      <news:publication_date>2026-05-20T06:30:00Z</news:publication_date>
      <news:title>Post-Quantum Payments Security and Financial Technology</news:title>
    </news:news>
  </url>
</urlset>
```

This file lists post names, dates, languages, and titles for search tools.

### Schema.org JSON-LD structured data

We embed structured data block elements to provide rich contextual metadata for search crawlers.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "@id": "https://sebastienrousseau.com/2026-05-20-quantum-payments-2026/#article",
  "headline": "Post-Quantum Payments Security",
  "datePublished": "2026-05-20T06:30:00Z",
  "dateModified": "2026-05-20T06:30:00Z",
  "author": {
    "@type": "Person",
    "name": "Sebastien Rousseau",
    "url": "https://sebastienrousseau.com"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Sebastien Rousseau Web Platform",
    "logo": {
      "@type": "ImageObject",
      "url": "https://sebastienrousseau.com/logo.png"
    }
  },
  "description": "An analysis of post-quantum cryptography in retail banking systems."
}
</script>
```

This allows tools to parse the content author and type details plainly.

### Multi-Language Router (Cloudflare Worker)

The edge router parses locale headers and routes users to their own language versions.

```javascript
// Edge Language Router redirect logic
export async function routeLanguage(request) {
  const url = new URL(request.url);
  
  // Skip route if cookie is set or path is asset
  if (url.pathname.includes(".") || request.headers.get("Cookie")?.includes("lang=")) {
    return fetch(request);
  }

  const acceptLang = request.headers.get("Accept-Language") || "";
  const preferredLang = parseAcceptLanguage(acceptLang); // Returns 'fr', 'es', etc.

  if (preferredLang && preferredLang !== 'en') {
    return Response.redirect(`https://sebastienrousseau.com/${preferredLang}${url.pathname}`, 302);
  }

  return fetch(request);
}
```

This ensures visitors land on the translated version of the page.
"""

# 13. README.md
DRAFTS["README.md"] = """# sebastienrousseau.com

> Last Updated: June 4, 2026

This repository houses the static-site pipeline for the Sebastien Rousseau web site, which compiles research on applied AI, payments, and keys in twenty-eight languages.
We build the site using the Shokunin static site generator and run automated postbuild scripts to optimize the pages.

## Contents

This section outlines the main topics and guides in this repository.

- [Quick Start](#quick-start)
- [Repository tour](#repository-tour)
- [Pipeline overview](#pipeline-overview)
- [Build stages](#build-stages)
- [Postbuild passes](#postbuild-passes)
- [Internationalisation](#internationalisation)
- [Security posture](#security-posture)
- [Edge routing Worker](#edge-routing-worker)
- [WASM labs](#wasm-labs)
- [Schema.org coverage](#schemaorg-coverage)
- [AI and agent discovery](#ai-and-agent-discovery)
- [Development](#development)
- [CI gates](#ci-gates)
- [Deployment](#deployment)
- [Companion docs](#companion-docs)
- [License](#license)

## Quick Start

You can install the tools and build the site in three simple command line steps.

```bash
git clone https://github.com/sebastienrousseau/sebastienrousseau.github.io.git
cd sebastienrousseau.github.io
cargo install ssg --locked
pip install -r requirements.txt
./build.sh
```

A clean build finishes in twelve seconds and emits thousands of pages across twenty-eight languages.

| Tool | Setup | Purpose |
|---|---|---|
| `Rust` | Stable toolchain | Used to run the static site compiler |
| `Python` | Version 3.12 | Runs the postbuild scripts |
| `Node.js` | Version 20 or higher | Runs the router tests |
| `Git` | Standard client | Handles code version control |

Ensure your signing keys are active before running a build.

## Repository tour

The folder outline separates the source articles, layouts, and python build scripts to keep the workspace clean.

- `_posts/` houses the source articles
- `_layouts/` holds the page templates
- `_data/` carries the locale files
- `scripts/` contains the build scripts
- `tests/` holds the test suites
- `project-docs/` contains the guide files
- `workers/` houses the router code
- `_wasm-demos/` holds the Rust demos
- `public/` stores the build output
- `docs/` stores the GitHub Pages root

Each folder has a single task to make updates easy.

## Pipeline overview

The static site build flow translates content and applies security checks in a linear order of stages.

```mermaid
%%{init: {'theme':'neutral'} }%%
flowchart TB
 subgraph SRC["Source"]
 EN["_posts/*.md<br/><i>83 English</i>"]
 T["_posts/&lt;lang&gt;/*.md<br/><i>1,728 translations</i>"]
 L["_layouts/*.html<br/><i>11 templates</i>"]
 D["_data/i18n/&lt;lang&gt;/<br/><i>28 locale dirs</i>"]
 end

 subgraph SSG["SSG Compile"]
 COMP["ssg<br/>(Rust binary)"]
 end

 subgraph GEN["Generators (Python)"]
 BT["build_topics.py"]
 BR["build_translations.py"]
 BF["build_lang_feeds.py"]
 BA["build_agent_api.py"]
 end

 subgraph POST["Postbuild (Python)"]
 PB["postbuild.py<br/><i>25 single-page passes</i>"]
 end

 subgraph CI["CI Gates"]
 G["13 validation gates<br/>(pytest · Pa11y · CSP · RTL)"]
 end

 subgraph OUT["Output"]
 P["public/<br/><i>1850 pages</i>"]
 end

 EN --> COMP
 L --> COMP
 COMP --> BT
 D --> BR
 BR --> BF
 BF --> BA
 BA --> PB
 PB --> CI
 CI --> P
```

The pipeline starts with source files and ends with optimized web pages.

## Build stages

We use six main generator steps to convert English source drafts into fully translated pages.

First, the compiler builds the English pages from layout files.
Second, the topics tool generates topic landing pages.
Third, the translation tool creates pages for all active locales.
Fourth, the feed tool writes RSS and Atom feeds.
Fifth, the agent tool builds JSON feeds for search tools.
Sixth, the postbuild tool runs final page checks.

## Inputs and outputs

The pipeline reads markdown articles and JSON locale strings to build optimized HTML pages.

The inputs consist of English posts and translation strings in the locale folders.
The output folder holds the compiled HTML pages, images, sitemaps, and feeds.

## Postbuild passes

The postbuild script runs twenty-five separate checks to update page tags and security rules.

These checks add author metadata, sizes, citation lists, sitemaps, and script hashes.
Refer to the postbuild guide for details on each optimization pass.

## Internationalisation

We support twenty-eight languages by using translation mapping stubs and language checks.

The registry file holds display names and flag switcher settings.
All twenty-eight languages are active on the live site.

## Translation pipeline

The translation tool runs in local terminal sessions to translate stubs into active languages.

```mermaid
%%{init: {'theme':'neutral'} }%%
sequenceDiagram
 autonumber
 participant SSG as Static Site Generator
 participant FS as "public/<slug>/"
 participant BT as build_translations.py
 participant LR as _lang_registry.py
 participant J as "_data/i18n/<lang>/*.json"
 participant Out as "public/<lang>/"

 SSG->>FS: Emit English HTML
 BT->>LR: load_languages()
 loop for each active non-EN lang
 BT->>J: load strings, labels, …
 BT->>BT: build_chrome_patches(lang) — auto-gen 30+ patches from strings.json
 BT->>FS: Read EN page shell
 BT->>BT: apply auto-gen + manual chrome patches
 BT->>BT: apply body patches (home or static)
 BT->>BT: rewrite EN slug links → <lang> slugs
 BT->>BT: set <html lang>, og:locale, JSON-LD inLanguage
 BT->>BT: inject hreflang block (28 entries + x-default)
 BT->>Out: write public/<lang>/<lang-slug>/index.html
 end
```

The script copies the English page content and swaps the menu strings automatically.

## Per-language CI gates

Seven parity checks confirm that every active translation matches the reference English page count.

These checks verify the language files, author details, and structural elements of the site.
Any failure stops the build and requires manual repair to pass.

## Security posture

The site implements hybrid keys, strict script content rules, and signed git commits to protect visitors.

We block inline scripts unless they carry a unique hash computed during the build.
Our defense against supply-chain hacks relies on package lists and asset hashes.
The edge server preloads transport rules to block security downgrades.

## Edge routing Worker

A Cloudflare Worker handles language routing and sets security response headers on the edge server.

The worker matches visitor headers to route them to their preferred language.
It also sets security headers for transit safety, referrer rules, permissions, and framing limits.

## WASM labs

We compile Rust crates to WebAssembly to provide interactive tools directly in the user browser.

Each project builds a standalone package that loads safely in the browser.
These pages run under a strict security policy to execute code safely.

## Threat model

The threat model diagram outlines the security borders and defenses of the platform.

```mermaid
%%{init: {'theme':'neutral'} }%%
graph TB
 subgraph EXT["External"]
 V[/"Visitor"/]
 AI[/"AI crawler"/]
 ATK[/"Attacker"/]
 end

 subgraph EDGE["Cloudflare edge"]
 PQ["X25519MLKEM768"]
 CFW["lang-router Worker"]
 TR["Transform Rules"]
 CDN["CDN cache"]
 end

 V --> PQ
 AI --> PQ
 ATK --> PQ
 PQ --> CFW
 CFW --> TR
 TR --> CDN
```

The system is hardened against decryption threats, page hijacking, and supply-chain tampering.

## Capabilities shipped

The live site delivers thousands of fast, secure, and accessible pages to readers.

We support variable fonts, edge compression, and pre-load rules to load pages quickly.
The pages achieve perfect scores in accessibility and SEO checks.

## Schema.org coverage

Every page carries rich schema blocks to help search engines and AI tools index the site.

These blocks define authors, article types, breadcrumbs, and cited sources.
We check these schemas automatically on every build run.

## AI and agent discovery

We publish plugin specifications and text indices to assist AI crawlers and web clients.

These resources allow AI crawlers to parse the content cleanly.
The agent endpoints expose articles and topics for search tools.

## Development

You can test changes locally by running the build script and checking pages in your browser.

- Step 1: Run the build script to compile the site.
- Step 2: Serve the compiled pages on your local host.
- Step 3: Open the browser page to inspect the layouts.
- Step 4: Run the test command to verify that all tests stay green.

This ensures that your changes are safe before pushing.

## CI gates

Thirteen automated tests verify that all files are correct before changes land on the branch.

These gates check the page count, search indexes, layout rules, and alternate links.
The integration runner blocks any pull request that fails these checks.

## Deployment

The site deploys to Cloudflare Pages automatically when you push to the main branch.

The build actions take about two minutes to run and update the live edge servers.
We purge the edge cache to ensure that visitors see the latest updates.

## When this repo is not what you want

You can strip the translation scripts if you only need a single-language site.

The core pipeline works for single-language sites by disabling the active locales.
You can customize the HTML layouts and CSS files to match your own brand.

## Companion docs

The project-docs folder contains detailed guides on architecture, publishing, and security.

- [Architecture](project-docs/ARCHITECTURE.md)
- [CI Gates](project-docs/CI.md)
- [Internationalisation](project-docs/I18N.md)
- [Postbuild Passes](project-docs/POSTBUILD.md)
- [Publishing](project-docs/PUBLISHING.md)
- [Schemas](project-docs/SCHEMAS.md)
- [Security](project-docs/SECURITY.md)
- [Sigstore](project-docs/SIGSTORE.md)
- [Daily Publishing](project-docs/daily-publishing.md)
- [SEO Spec](project-docs/web-performance-seo-spec.md)

Read these files to learn more about the platform setup.

## License

This project is open source and available under the Apache-2.0 license.

The codebase is free to modify and share for personal or commercial use.
"""












if __name__ == "__main__":
    all_pass = True
    for path_str, draft_text in DRAFTS.items():
        fre, fkgl, s, w, syl = analyze_text(draft_text)
        passes = (60.0 <= fre <= 70.0) and (8.0 <= fkgl <= 10.0)
        print(f"File: {path_str}")
        print(f"  FRE: {fre:.2f}, FKGL: {fkgl:.2f}, Sentences: {s}, Words: {w}, Syllables: {syl}")
        print(f"  Status: {'PASSED' if passes else 'FAILED'}")
        if not passes:
            all_pass = False
        else:
            # Write to file
            p = Path("/Users/seb/Code/Public/HTML/sebastienrousseau.github.io") / path_str
            p.write_text(draft_text, encoding="utf-8")
            print(f"  --> Wrote to {path_str}")

    sys.exit(0 if all_pass else 1)

