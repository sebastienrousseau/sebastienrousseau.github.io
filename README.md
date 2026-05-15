<!-- SPDX-License-Identifier: Apache-2.0 -->

<p align="center">
  <img src="https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg" alt="Sebastien Rousseau logo" width="128" />
</p>

<h1 align="center">sebastienrousseau.com</h1>

<p align="center">
  The build pipeline behind <a href="https://sebastienrousseau.com"><code>sebastienrousseau.com</code></a> — applied AI, ISO 20022 payments,
  and post-quantum cryptography for financial services.
</p>

<p align="center">
  <a href="https://github.com/sebastienrousseau/sebastienrousseau.github.io/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/sebastienrousseau/sebastienrousseau.github.io/ci.yml?style=for-the-badge&logo=github&label=build" alt="Build" /></a>
  <a href="https://github.com/sebastienrousseau/sebastienrousseau.github.io/actions/workflows/lighthouse.yml"><img src="https://img.shields.io/github/actions/workflow/status/sebastienrousseau/sebastienrousseau.github.io/lighthouse.yml?style=for-the-badge&logo=lighthouse&label=lighthouse" alt="Lighthouse" /></a>
  <a href="https://sebastienrousseau.com"><img src="https://img.shields.io/website?url=https%3A%2F%2Fsebastienrousseau.com&style=for-the-badge&logo=cloudflare&label=live" alt="Live site" /></a>
  <a href="https://github.com/sebastienrousseau/sebastienrousseau.github.io/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-66c2a5?style=for-the-badge" alt="License" /></a>
</p>

---

## Contents

**Getting started**

- [Install](#install) — toolchain, clone, build
- [Quick Start](#quick-start) — build the site in three commands

**Pipeline**

- [Architecture at a glance](#architecture-at-a-glance) — the build is a Unix pipeline
- [Build stages](#build-stages) — what each script does, in order
- [Inputs](#inputs) — `_posts/`, `_layouts/`, `_data/`
- [Outputs](#outputs) — `public/` and `docs/`

**Why this approach?**

- [Why a static pipeline](#why-a-static-pipeline) — design rationale
- [Capabilities shipped](#capabilities-shipped) — what's in production right now

**Reference**

- [Features](#features) — the build pipeline's capability matrix
- [Bilingual model (EN ↔ FR)](#bilingual-model-en--fr) — slug mapping, search-index parity, hreflang reciprocity
- [Security posture](#security-posture) — CSP, PQC TLS, SRI, SBOM, signed commits

**Operational**

- [Development](#development) — `make` targets, local audit recipe
- [CI gates](#ci-gates) — what every push must clear
- [Deployment](#deployment) — GitHub Pages + Cloudflare
- [When this repo is not what you want](#when-this-repo-is-not-what-you-want) — fork considerations
- [Documentation](#documentation) — companion docs in this repo
- [License](#license)

---

## Install

### Prerequisites

| Tool | Version | Why |
|---|---|---|
| Rust toolchain | stable | `ssg` (Shokunin) is a Rust binary; install via `cargo install ssg --locked` |
| Python | 3.11+ | Postbuild pipeline (`scripts/*.py`) |
| `markdown-it-py` | latest | FR translation pipeline parser. Installed via `requirements.txt`. |
| `gh` CLI | optional | Repo administration, CI inspection |

### Clone and bootstrap

```bash
git clone https://github.com/sebastienrousseau/sebastienrousseau.github.io.git
cd sebastienrousseau.github.io
cargo install ssg --locked
pip install -r requirements.txt
```

### Build from source

```bash
./build.sh           # build into public/, mirror to docs/
./build.sh --serve   # build + serve on http://127.0.0.1:8000
```

The `Makefile` exposes the same surface plus QA targets:

```bash
make build              # full build pipeline
make serve              # build + serve locally
make audit              # internal-link audit (strict)
make validate           # JSON-LD + XML feed validity
make test-search-index  # EN + FR search-index shape guard
make lint               # ruff
make test               # pytest
```

---

## Quick Start

A from-scratch build runs end-to-end in ~3 seconds on a modern laptop:

```bash
$ ./build.sh
ssg → public/ (English markdown + topic posts)
build_topics: wrote 5 topic page(s) + 1 hub
build_translations: wrote 65 page(s) (43 translation(s) + hub + 20 static page(s))
build_fr_feeds: wrote 43 entry feeds (rss.xml + atom.xml + news-sitemap.xml)
build_agent_api: wrote 43 posts + 5 topics + person + index
postbuild: 130 HTML pages, 130 got real SRI, 920 img(s) stamped w/h, …
ok: 2 search-index file(s) pass shape check
```

Then open <http://127.0.0.1:8000/> for the English site or
<http://127.0.0.1:8000/fr/> for French.

---

## Architecture at a glance

```
_posts/*.md ┐
            │
_posts/fr/*.md
            │
_layouts/*.html ───►  ssg (Rust SSG)  ───►  public/{slug}/
            │
_data/*.json
            │
            ▼
   scripts/build_topics.py        ───►  public/topics/{topic}/
   scripts/build_translations.py  ───►  public/fr/{fr-slug}/
   scripts/build_fr_feeds.py      ───►  public/fr/{rss,atom,news-sitemap}.xml
   scripts/build_agent_api.py     ───►  public/api/agents/*.json
   scripts/postbuild.py           ───►  every page: SRI, CSP hashes,
                                        og:* completion, image w/h,
                                        hreflang, HowTo JSON-LD,
                                        GitHub stats, sitemaps
            │
            ▼
        public/   ───  rsync ───►   docs/  (GitHub Pages root)
            │                          │
            └─────  Cloudflare CDN ◄───┘
                       (PQC TLS, HSTS preload, COOP/CORP/X-Frame-Options
                        via Transform Rules — see DEPLOY.md)
```

No JavaScript framework. No client-side renderer. Every URL is a real
HTML file. Speculation Rules API prerenders the next likely page on
hover; everything else is static.

### Build stages

`build.sh` chains six tools in this order. Each is a pure
transformation on `public/`:

1. **`ssg`** — Shokunin renders English Markdown under `_posts/*.md`
   into `public/{slug}/index.html`. Picks up the layout selected by
   each post's `layout:` frontmatter (`report`, `link`, `articles`,
   `papers`, `projects`, `contact`, …).
2. **`scripts/build_topics.py`** — Five hand-curated topic clusters
   (Post-Quantum, ISO 20022, Applied AI, Rust OSS, Blockchain). Forks
   `public/articles/index.html` as the shell and emits one page per
   topic + a `/topics/` hub.
3. **`scripts/build_translations.py`** — French edition. Reads
   manually-translated Markdown from `_posts/fr/*.md`; the EN↔FR slug
   map (`scripts/_fr_slugs.py`) is the single source of truth for
   slug rewrites. Patches JSON-LD `inLanguage`, swaps chrome (nav,
   footer, search, CTAs), localises dates, fixes hreflang
   reciprocity.
4. **`scripts/build_fr_feeds.py`** — Per-language RSS / Atom /
   news-sitemap. Same article ordering as the EN feeds.
5. **`scripts/build_agent_api.py`** — Machine-readable JSON
   endpoints at `/api/agents/{posts,topics,person,index}.json` for
   AI crawlers and agentic clients.
6. **`scripts/postbuild.py`** — The big one. Single-pass over every
   built page applying ~15 independent transforms:
   - Stamp real SHA-256 SRI on every `/_csp/*` asset
   - Inject `og:url` / `og:locale` / `og:site_name` / `og:image`
   - Add explicit `width`/`height` + `fetchpriority`/`loading` to
     every `<img>` (920+ on a clean build)
   - Inject `HowTo` JSON-LD on practical articles
   - Build the article table-of-contents, citations graph,
     prev/next nav, FAQ accordion
   - Compute SHA-256 of every inline `<script type="application/ld+json">`
     plus the `<script type="speculationrules">` block and fold
     into the page's CSP `script-src`
   - Hoist any in-body `<link rel=stylesheet>` back into `<head>`
     (sanitises SSG's malformed widget link tag in transit)
   - Emit `robots.txt`, `llms.txt`, `llms-full.txt`
   - Splice missing sitemap entries

The pipeline finishes with `scripts/test_search_indexes.py` — a
shape guard that fails the build if EN or FR search-index entries
ever drop the required `title`/`url`/`content`/`headings` keys.

---

## Inputs

```
_posts/*.md          # 59 English source documents (43 dated articles + 16 static pages)
_posts/fr/*.md       # 44 French translations
_layouts/*.html      # 11 page layouts (index, articles, papers, projects, …)
_data/gh-stats.json  # nightly GitHub repo stats (stars, forks, last commit) — refresh-gh-stats workflow
scripts/_fr_slugs.py # EN ↔ FR slug map (42 entries + static-page slugs)
```

## Outputs

```
public/              # canonical build output — 130 HTML pages
docs/                # mirror of public/ that GitHub Pages serves
public/sitemap.xml   # 249 URLs (EN + FR + news-sitemap split)
public/llms.txt      # 86 entries (one per article)
public/llms-full.txt # 6029-line corpus dump for AI crawlers
public/sbom.cdx.json # CycloneDX SBOM — supply-chain provenance
public/api/agents/   # JSON endpoints for AI / agentic clients
```

---

## Why this approach?

### Why a static pipeline

The site exists to host long-form research on payments, AI, and PQC
for senior banking technologists. Three constraints made a static
build the right choice:

1. **Read-heavy traffic, write-light authorship.** One author, ~50
   articles a year. No comments, no user accounts. The cost ratio
   of "server-side render every request" vs "render once, serve
   from CDN" is dominated by the latter.
2. **Strict content-security posture.** The site is the public face
   of someone who writes about post-quantum cryptography. CSP must
   be strict, hash-allowlisted JSON-LD only, no `unsafe-inline`,
   PQC TLS at the edge, SRI on every asset, SBOM published.
   Easier to enforce on a static artefact than a runtime stack.
3. **Future-resistant publishing.** Markdown + Git history + the
   build script in this repo is enough to reconstruct any version
   of the site indefinitely. No managed service, no SaaS dependency
   for content.

### Architectural choices that follow

- **Shokunin SSG over Hugo/Jekyll.** Rust, fast, fewer build deps,
  generates an emit-everything tree on every invocation (no
  incremental cache to corrupt).
- **Python postbuild over Rust postbuild.** The transforms are
  regex-heavy and frequently revised; iteration speed matters more
  than runtime. Postbuild runs in ~1.5s on 130 pages.
- **FR pipeline forks rendered EN HTML rather than re-rendering FR
  from layout templates.** Cuts manual layout drift to zero: any
  HTML change ships to both languages by construction.
- **No client-side framework.** No build artefact ships JavaScript
  beyond a 4 KB main bundle (theme toggle, ⌘K search, reading
  progress, back-to-top). Lighthouse Best-Practices/SEO/A11y all
  score 1.0; performance lands ≥0.96 on every audited URL.

---

## Capabilities shipped

What's in production right now (≠ what's on the roadmap):

| Surface | What ships |
|---|---|
| Languages | English (`en-GB`, 86 dated + 14 static pages) + French (`fr-FR`, 43 articles + hub + 20 static). |
| Content | 43 long-form articles, 5 topic-cluster hubs, papers index, projects portfolio, playlists, contact form. |
| Security | Strict CSP (no `unsafe-inline`, hash-allowlisted JSON-LD + speculationrules), HSTS preload, X25519MLKEM768 PQC TLS at the edge, COOP/CORP/X-Frame-Options via Cloudflare Transform Rules. |
| Discovery | sitemap.xml (249 URLs), news-sitemap per language, RSS + Atom per language, `robots.txt` (20 AI bots listed explicitly), `llms.txt` + `llms-full.txt`. |
| Performance | Speculation Rules API (hover-prerender), 920+ images with explicit width/height, hero `fetchpriority=high`, below-fold `loading=lazy`, system fonts only, ~4 KB JS. |
| Accessibility | WCAG 2.2 AAA — 0 pa11y violations across 130 pages, all interactive targets ≥24×24 (WCAG 2.5.5), focus-visible rings, `prefers-reduced-motion` honored. |
| SEO / GEO | `Person` / `Article` / `FAQPage` / `HowTo` / `BreadcrumbList` / `ItemList` / `ProfilePage` JSON-LD, complete OG/Twitter metadata, hreflang reciprocity, regional BCP-47 tags. |
| Build provenance | CycloneDX SBOM published at `/sbom.cdx.json`, SRI on every asset, signed commits, CI gates on every push. |

---

## Features

| | |
| :--- | :--- |
| **EN render** | Shokunin SSG (Rust) reads `_posts/*.md` + `_layouts/*.html`, emits `public/{slug}/index.html`. Asset fingerprinting under `/_csp/*` with `integrity=…` placeholders that `postbuild.py` later replaces with real SHA-256. |
| **FR render** | `build_translations.py` reads `_posts/fr/*.md` and the canonical `scripts/_fr_slugs.py` EN↔FR slug map, then forks each rendered EN page, swaps chrome (nav, footer, search, CTAs, aria-labels), localises dates ("August 2026" → "août 2026"), patches JSON-LD `inLanguage`, fixes hreflang reciprocity. 65 FR pages in ~0.4s. |
| **Topics** | Five curated topic clusters (`post-quantum-cryptography`, `iso-20022-payments`, `applied-ai-banking`, `rust-open-source`, `blockchain-digital-assets`). Each is a manually-curated list of article slugs + a French translation of title + lede. Hub at `/topics/` + `/fr/sujets/`. |
| **AI / agentic API** | `/api/agents/{index,posts,topics,person}.json` — machine-readable inventory of every dated post (title, URL, summary, date, topic), every topic (slug, title, lede, article list), and the canonical `Person` schema. `robots.txt` advertises `llms.txt` + `llms-full.txt`. |
| **JSON-LD** | `Person`, `WebSite`, `ProfilePage` on `/about/`, `BlogPosting` on every article, `CollectionPage` on listing pages, `FAQPage` on `/papers/` + `/projects/`, `HowTo` on the practical articles (pain001, pacs.008), `BreadcrumbList` and `ItemList` everywhere. Hash-allowlisted in CSP per page. |
| **OG / Twitter Cards** | Every page emits `og:title`, `og:description`, `og:url`, `og:locale`, `og:site_name`, `og:image`, `twitter:card=summary_large_image`. `og:image` defaults to the article banner; falls back to the author headshot when absent. |
| **Search** | `/search-index.json` (EN) + `/fr/search-index.json` (FR). 65 FR + 100+ EN entries. `scripts/test_search_indexes.py` is wired into `build.sh` and fails the build if any entry is missing `title`/`url`/`content`/`headings`. |
| **Sitemaps** | Root `sitemap.xml` (249 URLs), `news-sitemap.xml` for fresh content, per-language `/fr/news-sitemap.xml`. `scripts/postbuild.py:_splice_fr_urls()` repopulates from authoritative sources if SSG emits an empty `<urlset>`. |
| **Feeds** | `/rss.xml`, `/atom.xml`, and JSON-Feed-style `/api/agents/posts.json`. `/fr/rss.xml`, `/fr/atom.xml`, `/fr/news-sitemap.xml` for the French edition. |
| **Speculation Rules** | Every page carries a `<script type="speculationrules">` block that asks Chromium 126+ to prerender same-origin pages on hover. Excludes `/_csp/*`, `*.xml`, `*.json`, `*.txt`, `*.pdf`, contact forms. CSP allows it via `'inline-speculation-rules'` keyword plus the block's SHA-256 hash. |
| **GitHub stats** | Nightly `refresh-gh-stats` GitHub Action queries the GitHub API for 20 repos and writes `_data/gh-stats.json`. `postbuild.py:inject_github_stats()` injects star/fork/license/last-commit pills onto every project card. |
| **Search widget** | ⌘K / Ctrl-K opens the SSG-built search overlay; language-aware (auto-loads `/fr/search-index.json` when the URL is under `/fr/`). |
| **Image pipeline** | 920+ images on a clean build get explicit `width`/`height` (CLS budget = 0). Hero image gets `fetchpriority="high"`; everything else `loading="lazy"` + `decoding="async"`. Per-asset manifest pins known dimensions for common SVGs and the author portrait. |
| **HowTo schema** | Curated per-article steps for practical guides (pain001 ISO 20022 file generation, pacs.008 structured-address migration). Step text is decoupled from heading styling so the article can be refactored without invalidating the schema. |
| **GEO** | TL;DR + Key Takeaways on every dated post (extracted by `post_enrich.py`). `llms.txt` directory; `llms-full.txt` corpus dump (6029 lines) for AI crawlers. `Article.about` / `mentions` cross-linking to Wikidata where applicable. |
| **PWA** | `manifest.json`, service worker (`sw.js`) with stale-while-revalidate on `/_csp/*` assets and network-first on HTML. Offline page at `/offline/`. |
| **SBOM** | CycloneDX 1.4 SBOM published at `/sbom.cdx.json` on every build — supply-chain provenance for downstream auditors. |

---

## Bilingual model (EN ↔ FR)

English is the source of truth. The FR pipeline forks rendered EN
HTML rather than re-rendering from templates — that guarantees layout
parity by construction. Three components keep the two languages
synchronised:

| Component | Role |
|---|---|
| `scripts/_fr_slugs.py` | Single source of truth for EN ↔ FR slug mapping (42 articles + every static page). Both directions exposed so hreflang and the FR pipeline use the same data. |
| `scripts/build_translations.py` | The FR build pipeline. Forks each EN page, patches `<html lang>`, swaps chrome strings, rewrites links to FR counterparts, localises dates, patches JSON-LD `inLanguage`, fixes hreflang reciprocity. Two passes: chrome (nav/footer/search/aria) and content (article-card titles, eyebrows, tooltips). |
| `scripts/test_search_indexes.py` | CI gate. Fails the build if EN or FR search-index entries don't share the `title`/`url`/`content`/`headings` shape. This guard exists because the FR widget silently returned zero results before it was added. |

### URL slug discipline

| English | French |
|---|---|
| `/about/` | `/fr/a-propos/` |
| `/articles/` | `/fr/articles/` |
| `/papers/` | `/fr/publications/` |
| `/projects/` | `/fr/projets/` |
| `/topics/` | `/fr/sujets/` |
| `/tags/` | `/fr/etiquettes/` |
| `/privacy/` | `/fr/confidentialite/` |
| `/contact/` | `/fr/contact/` |
| `/2026-05-12-iso-20022-pacs008-structured-address-deadline/` | `/fr/2026-05-12-iso-20022-pacs008-adresse-structuree-echeance/` |

Slugs are ASCII-only — Unicode in URLs harms SERP CTR. Idiomatic, not
transliterated.

### Hreflang reciprocity

Every translated page emits a complete `<link rel="alternate"
hreflang="…" href="…">` set including `x-default`. The pairs are
symmetric: if A claims B is its FR alternate, B claims A is its EN
alternate. 103 pages currently carry hreflang on a clean build.

---

## Security posture

| Surface | Posture |
|---|---|
| **TLS** | Cloudflare edge with the post-quantum hybrid X25519MLKEM768 (NIST FIPS 203), classical X25519 fallback for legacy clients. Negotiated by Chrome 124+, Firefox 132+, Safari 18+. |
| **HSTS** | `max-age=63072000; includeSubDomains; preload`. Submitted to the Chromium HSTS preload list. |
| **CSP** | Strict; no `unsafe-inline` for scripts. JSON-LD allowed strictly by per-page SHA-256 hash. `'inline-speculation-rules'` keyword authorises the Speculation Rules API block (which also carries its own hash). |
| **Frame protection** | `frame-ancestors 'none'` + `X-Frame-Options: DENY` shipped via Cloudflare Transform Rules (meta CSP can't express it). |
| **MIME** | `X-Content-Type-Options: nosniff`. |
| **Referrer** | `Referrer-Policy: strict-origin-when-cross-origin`. |
| **Permissions** | `Permissions-Policy` denies ~40 sensitive permissions by default (camera, mic, geolocation, USB, payment, etc.). |
| **Cross-origin** | `Cross-Origin-Opener-Policy: same-origin`, `Cross-Origin-Resource-Policy: same-origin`. `COEP` deliberately not set to keep Spotify iframes working on `/playlists/`. |
| **SRI** | Real SHA-256 SRI on every `/_csp/*` asset. Browsers refuse the file if it doesn't byte-for-byte match. |
| **SBOM** | CycloneDX 1.4 published at `/sbom.cdx.json`. |
| **Git** | Signed commits enforced. Branch protection on `main`. |

Full deployment notes including the Cloudflare configuration and
verification commands live in [`DEPLOY.md`](DEPLOY.md).

---

## Development

Local QA recipe — every gate that CI runs, runnable locally:

```bash
ruff check scripts/ tests/         # Python lint (target = 0 errors)
pytest tests/ -ra                  # 58 unit tests
./build.sh                         # full build pipeline
python3 scripts/audit_links.py     # 0 internal-link breakages
python3 scripts/validate_jsonld.py # 0 JSON-LD / XML feed errors
python3 scripts/test_search_indexes.py  # EN + FR search-index shape guard
```

The pre-commit-equivalent one-liner is `make build && make audit && make validate`.

### Worked example: build a single layout change

```bash
$ vim _layouts/index.html      # change a CSS rule
$ python3 scripts/gen_layouts.py    # propagate the shared shell to the 10 sibling layouts
$ ./build.sh                   # full rebuild
$ python3 -m http.server -d public 8000
# visit http://127.0.0.1:8000/
```

If the change touches a CSS variable, bump `_layouts/sw.js`'s
`CACHE` constant so the service worker invalidates and re-fetches.

---

## CI gates

Six workflows guard every push:

| Workflow | Runs on | Gates |
|---|---|---|
| `ci.yml` (build-audit) | every push + PR | ruff, pytest, build, audit_links, validate_jsonld, pa11y AAA against all 130 pages, nested Lighthouse (LHCI 0.13 / Lighthouse 11) |
| `lighthouse.yml` | every push + weekly cron | Full Lighthouse CI on 7 representative URLs × 3 runs (LHCI 0.14 / Lighthouse 12 — stricter `target-size` audit). Thresholds: perf ≥0.90 warn, a11y/best-practices/SEO ≥0.95 error. |
| `pages-deploy.yml` | push to `main` | Build + upload-pages-artifact + deploy-pages |
| `schema-diff.yml` | every PR | Builds the PR base and HEAD, diffs JSON-LD, posts a comment. Read-only. |
| `refresh-gh-stats.yml` | nightly cron + manual | Refreshes `_data/gh-stats.json` from the GitHub API. Opens a PR on changes (cannot push directly to protected `main`). |
| `link-audit.yml` | first of every month | External link audit. Files a tracking issue if any external link 404s. |

All six green at HEAD. Local `make` parity is `make build && make
test && make audit && make validate && make test-search-index`.

---

## Deployment

GitHub Pages serves `docs/` (mirrored from `public/` by `build.sh`).
Cloudflare sits in front of Pages as the CDN — see
[`DEPLOY.md`](DEPLOY.md) for the canonical record of headers,
PQC TLS toggle, HSTS preload submission, and Transform Rules.

`pages-deploy.yml` is the active deploy path. The legacy
`main`-branch `docs/` auto-deploy still works as a fallback.

Production URL: <https://sebastienrousseau.com/>.

---

## When this repo is **not** what you want

This is the source-tree for a single author's personal site. It's
public so anyone curious about the pipeline can read it, but:

- **No CMS.** Adding content means a Git commit. Comfortable with
  Markdown, frontmatter, and Git is a hard prerequisite.
- **No theming system.** Layouts are bespoke. Forking and rebranding
  is possible but involves rewriting `_layouts/index.html` end to
  end.
- **No multi-tenant story.** The build pipeline assumes one origin
  (`sebastienrousseau.com`) and one author identity.

For a general-purpose Rust SSG with theming, see
[Shokunin](https://shokunin.one).

---

## Documentation

| Document | Covers |
|---|---|
| [`DEPLOY.md`](DEPLOY.md) | Cloudflare configuration: PQC TLS toggle, Transform Rules for HSTS / COOP / CORP / X-Frame-Options, HSTS preload submission, verification commands. |
| [`_posts/fr/README.md`](_posts/fr/README.md) | Manual French translation workflow: adding a new translation, slug-map convention, chrome-patch authoring rules. |
| `_data/gh-stats.json` | Nightly snapshot of GitHub repo stats (stars, forks, last commit) consumed by `postbuild.py:inject_github_stats()`. |
| `scripts/_fr_slugs.py` | The EN ↔ FR slug map. Single source of truth. |
| `requirements.txt` | Python runtime dependencies (currently `markdown-it-py`). |
| `pyproject.toml` | Ruff + pytest configuration, MSRV-equivalent for the Python pipeline (3.11+). |

---

## License

[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0). Content (articles, papers) is © Sebastien Rousseau, all rights reserved; the build pipeline (scripts, layouts, build configuration) is Apache-2.0.

<p align="right"><a href="#contents">Back to Top</a></p>
