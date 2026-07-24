---

# Front Matter (YAML)

author: "contact@sebastienrousseau.com (Sebastien Rousseau)"
banner_alt: "An abstract technical background, representing the architectural roadmap of an enterprise-grade static site generator."
banner_height: "1280"
banner_width: "1920"
banner: "https://cloudcdn.pro/stocks/images/gemini-background.webp"
cdn: "https://cloudcdn.pro"
charset: "UTF-8"
cname: "sebastienrousseau.com"
copyright: "© Copyright 2025 - 2026 - Sebastien Rousseau. All rights reserved."
date: "July 22, 2026"
description: "A deep dive into a Rust static-site generator: compile-time security, WCAG gates and local-first AI, the gaps in v0.0.41, and an enterprise roadmap to 1.0."
format-detection: "telephone=no"
hreflang: "en"
icon: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
id: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
image_alt: "Black and White Portrait of Sebastien Rousseau"
image_height: "162"
image_width: "162"
image: "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp"
keywords: "static site generator, Rust, forbid unsafe_code, WCAG 2.2 AA, Content Security Policy, Subresource Integrity, SLSA, CycloneDX SBOM, local LLM pipeline, DORA, incremental builds, lol_html, WASM plugin sandbox, semantic vector search, MiniJinja, Ollama"
language: "en-GB"
last_reviewed: "2026-07-22"
layout: "report"
locale: "en_GB"
logo_alt: "Logo for Sebastien Rousseau"
logo_height: "44"
logo_width: "44"
logo: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
menu: ""
measurementID: "G-169G4ET5HQ"
name: "Sebastien Rousseau"
permalink: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
rating: "general"
referrer: "no-referrer"
robots: "index, follow"
schema: "FAQPage, Article"
seo_title: "Static Site Generator: The Road to 1.0"
short_name: "sebastienrousseau"
subtitle: "An architectural audit and roadmap for a Rust static-site generator built as secure-by-default infrastructure: what v0.0.41 genuinely ships versus what the README promises, five missing enterprise capabilities, and a phased path to a DORA- and EAA-aligned 1.0."
tags: "static site generator, Rust, web security, accessibility, DORA, supply chain, SLSA, local AI, WCAG, compile-time, roadmap, enterprise"
theme-color: "0, 83, 191"
title: "Static Site Generator (SSG): Enterprise-Grade Strategic Deep Dive and Architectural Roadmap"
url: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"

# RSS - The RSS feed front matter (YAML).
atom_link: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap/rss.xml"
category: "Technology"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "Static Site Generator (SSG) (version 0.0.26)"
item_description: "A deep dive into a Rust static-site generator: compile-time security, WCAG gates and local-first AI, the gaps in v0.0.41, and an enterprise roadmap to 1.0."
item_guid: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap/rss.xml"
item_link: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap/rss.xml"
item_pub_date: "Wed, 22 Jul 2026 07:07:07 +0000"
item_title: "Static Site Generator (SSG): Enterprise-Grade Strategic Deep Dive and Architectural Roadmap"
last_build_date: "Wed, 22 Jul 2026 06:06:06 +0000"
managing_editor: "contact@sebastienrousseau.com (Sebastien Rousseau)"
pub_date: "Wed, 22 Jul 2026 07:07:07 +0000"
ttl: "60"
type: "article"
webmaster: "contact@sebastienrousseau.com"

# Apple - The Apple front matter (YAML).
apple_mobile_web_app_orientations: "portrait"
apple_touch_icon_sizes: "192x192"
apple-mobile-web-app-capable: "yes"
apple-mobile-web-app-status-bar-inset: "black"
apple-mobile-web-app-status-bar-style: "black-translucent"
apple-mobile-web-app-title: "SSG Road to 1.0"
apple-touch-fullscreen: "yes"

# MS Application - The MS Application front matter (YAML).

msapplication-navbutton-color: "0, 83, 191"

# Twitter Card - The Twitter Card front matter (YAML).

twitter_card: "summary_large_image"
twitter_creator: "@wwdseb"
twitter_description: "Compile-time WCAG gates, SHA-384 SRI, CSP injection and a local-first LLM pipeline set this Rust engine apart. An honest gap analysis of v0.0.41 and the road to an enterprise-grade 1.0."
twitter_image: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
twitter_image_alt: "Logo of Sebastien Rousseau"
twitter_site: "@wwdseb"
twitter_title: "Static Site Generator: The Road to 1.0"
twitter_url: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"

excerpt: "Compile-time WCAG gates, SHA-384 SRI, CSP injection and a local-first LLM pipeline set this Rust engine apart, but incremental builds, native minification and AVIF are still aspirational. Here is the honest gap analysis and the road to 1.0."

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://sebastienrousseau.com"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "Thanks for reading!"
site_last_updated: "2026-07-22"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "Kaishi, Kaishi Builder, Kaishi CLI, Kaishi Templates, Kaishi Themes"

---

# Static Site Generator (SSG): Enterprise-Grade Strategic Deep Dive and Architectural Roadmap

*Research date: 2026-06-22. Based on codebase inspection of `static-site-generator` at v0.0.41 and web research of the 2026 SSG landscape.*

**For a regulated publisher, a static site generator is no longer a design tool; it is part of the operational risk perimeter.** The open-source Rust [static-site-generator](https://github.com/sebastienrousseau/static-site-generator) is built on that premise, moving security, accessibility, internationalisation and AI content pipelines to compile-time so that a failed check halts the build rather than reaching production. This analysis separates what version 0.0.41 genuinely ships from what its documentation still only promises, sets out five enterprise capabilities it does not yet have, and proposes a phased path to a 1.0 release aligned with DORA, the European Accessibility Act and modern supply-chain standards.

<!-- lead-start -->
<aside class="post-lead" aria-label="Article summary">
<p class="post-lead-tldr"><strong>TL;DR.</strong> The Rust <code>static-site-generator</code> treats web publishing as an auditable, secure-by-default software pipeline: workspace-wide <code>forbid(unsafe_code)</code>, SHA-384 Subresource Integrity, Content Security Policy extraction, a compile-time WCAG 2.2 AA gate and a local-first LLM pipeline. A code inspection of v0.0.41 shows several documented features are still aspirational, native minification, incremental rebuilds and AVIF among them. This is the honest gap analysis and a phased roadmap to an enterprise-grade 1.0.</p>
<p class="post-lead-heading"><strong>Key takeaways</strong></p>
<ul class="post-lead-takeaways">
  <li><strong>The security and accessibility model is real.</strong> Compile-time SRI, CSP extraction, signed releases with Sigstore attestation and CycloneDX SBOMs, plus a build-halting WCAG 2.2 AA gate, are implemented in code, not just documented.</li>
  <li><strong>Several headline features are not.</strong> The minifier is a whitespace collapser, the dependency graph that would drive incremental builds is never populated in production, and AVIF encoding is a stub returning an empty vector.</li>
  <li><strong>Five enterprise capabilities are missing.</strong> WASM plugin sandboxing, a streaming zero-copy HTML rewriter, local semantic search, deterministic inference caching and asynchronous file I/O.</li>
  <li><strong>The roadmap is sequenced by risk.</strong> A correctness patch (0.0.42), a credibility-and-incremental minor (0.1.0), then an enterprise major (1.0.0) carrying the sandbox, semantic search and SLSA v1.1 provenance.</li>
</ul>
<p class="post-lead-related"><strong>Related reading:</strong> <a href="https://sebastienrousseau.com/2026-07-03-emerging-technology-risk-horizon-banks-2026">The Emerging-Technology Risk Horizon for Banks</a>, <a href="https://sebastienrousseau.com/2026-07-07-corporate-banking-api-standard-agentic-mcp-2026">A Corporate Banking API Standard for Agentic MCP</a>.</p>
</aside>
<!-- lead-end -->

> **Executive Summary**
>
> - **Publishing is now an operational risk perimeter.** Under DORA, the European Accessibility Act and GDPR, every public-facing asset is a potential entry point for supply-chain compromise, defacement and regulatory exposure. A compile-time model narrows that perimeter by rejecting non-compliant output before it ships.
> - **The engine's differentiators are compiler-enforced, not documented aspirations.** Workspace-wide `forbid(unsafe_code)`, true SHA-256/384 SRI, automatic CSP extraction, and a build-time WCAG 2.2 AA gate turn security and accessibility from post-hoc audits into hard build failures.
> - **Version 0.0.41 has a documentation-to-code gap.** Native minification, incremental rebuilds via a dependency graph, and AVIF support are described but not functional; the article names each gap against the exact source location.
> - **The path to 1.0 is a sequence, not a wish list.** Robustness first (0.0.42), then incremental correctness (0.1.0), then the enterprise capabilities, WASM sandboxing, local semantic search and verifiable SLSA provenance, that a regulated buyer requires (1.0.0).

## Current Strengths

The `static-site-generator` codebase exhibits several distinctive engineering decisions that separate it from legacy JavaScript and Go engines:

- **Compile-time security posture:** Workspace-wide `#![forbid(unsafe_code)]` provides compile-time memory-safety guarantees. The build pipeline generates true SHA-256/SHA-384 Subresource Integrity (SRI) hashes (`src/plugins/assets.rs`) and performs automatic Content Security Policy (CSP) extraction that removes unsafe-inline scripts and styles. Releases are signed, carry Sigstore attestation, and produce a CycloneDX 1.5 SBOM on every build.  
- **Compiler-enforced accessibility gate:** Web Content Accessibility Guidelines (WCAG) 2.2 Level AA checks run inside the compilation pipeline via a build-time axe-core parser driven by Playwright. Accessibility becomes a hard build gate rather than a post-publication audit: if a page fails, compilation halts with exact line-number errors.  
- **Data-sovereign AI pipeline:** A local-LLM translation and metadata-extraction pipeline (via local Ollama or llama.cpp endpoints) lets an institution automate content summarisation, JSON-LD schema generation and multilingual translation without sending pre-earnings disclosures or sensitive intellectual property to public cloud AI APIs.  
- **Parallelised compilation:** Rust's memory-safety guarantees underpin a parallelised, Rayon-driven HTML and asset pipeline (`src/core/pipeline.rs`). The plugin pipeline executes fused transforms, with `SearchPlugin`, `SeoPlugin`, `CanonicalPlugin` and `JsonLdPlugin` operating over `par_iter()`, so each page is read and written to disk once.  
- **Supply-chain and dependency hygiene:** Migrating the template engine from Tera to MiniJinja (`v0.0.37`) reduced binary size, removed transitive dependencies such as `rand` at compile-time, and produced a compact dependency footprint that lowers software supply-chain exposure.

---

## Gaps and Real-World Realities

Despite these exceptional strengths, a rigorous codebase inspection of v0.0.41 reveals several architectural, functional, and developer-experience gaps between its documentation claims and the actual rust code:

### Architectural Gaps

- **Whitespace Collapse vs. Native Minification:** While the README promises "native JS/CSS minification," the `MinifyPlugin` (`src/plugins/plugins.rs:96-116`) acts merely as a naive whitespace collapser. It short-circuits on `<pre>` elements and collapses whitespace runs in HTML, but does not perform syntactically aware native CSS or JS minification. Furthermore, it only processes top-level pages and does not recursively walk subdirectories (such as `/blog/` or `/tags/`), leaving deep pages unminified.  
- **Dead Incremental Infrastructure:** The dependency tracking graph (`DepGraph` in `src/core/depgraph.rs`) is compiled and loaded into `PluginContext.dep_graph` but is never actually populated in production code. The method `add_dep()` is only called in unit tests, making the README's claim of "incremental rebuilds via dependency graphs" currently aspirational.  
- **Batched Compilation vs. Streaming Compilation:** The `streaming::compile_batch` module (`src/core/streaming.rs`) does not truly stream. Instead, it compiles pages in batches to a temporary directory, executes `staticdatagen::compile` from scratch for each batch, and merges the outputs. This results in significant disk I/O overhead and redundant parsing, deviating from a true streaming architecture.  
- **Plugin Lifecycle Phase Violations:** Plugins that generate new HTML pages during the build process, such as `TaxonomyPlugin`, `PaginationPlugin` and `I18nPlugin`, write directly to disk in `after_compile` rather than using the `transform_html` lifecycle. Consequently, pages generated by these plugins bypass critical post-processing plugins (such as `CanonicalPlugin`, `JsonLdPlugin`, `RobotsPlugin`, and `AccessibilityPlugin`) if those plugins were registered earlier. This leaves tag, category, and paginated pages without correct canonical links, JSON-LD schemas, or accessibility validations.  
- **Shelling Out to `curl` in `LlmPlugin`:** The local LLM content pipeline (`src/plugins/llm.rs`) shells out directly to the host's `curl` binary to query local endpoints. This introduces severe cross-platform bugs (e.g., on Windows hosts without curl in the PATH), poses a security risk (shell injection vectors), and fails in locked-down or network-isolated CI environments.  
- **Naive String Manipulation in HTML Rewriting:** The `image_plugin.rs` and `search.rs` extractors rewrite HTML strings using fragile `str::find` and `str::rfind` operations. This approach is highly vulnerable to broken HTML tags, `<img>` tags inside comments, character entities in alt text, or pre-existing `srcset` properties, which can result in corrupted output.  
- **Unimplemented AVIF Support:** Although AVIF image encoding is heavily documented, the implementation in `image_plugin.rs` is a stub where `avif_variants` simply returns `Vec::new()`, leaving the feature non-functional.  
- **Polling-Based Watcher:** The local development server's watcher (`src/server/watch.rs`) uses polling rather than filesystem event APIs, leading to excessive idle CPU usage and sub-second modification latency.

### Functional & DX Gaps

- **No Transitive Dependency Tracking:** The dependency graph cannot track nested dependencies (e.g., changes to a sub-template that affects a layout that affects a page), as verified by the unit test `transitive_not_tracked`.  
- **No Incremental Compilation CLI Flag:** There is no `--incremental` CLI flag wired to the execution compiler, preventing developers from using cached builds.  
- **HMR is Limited to CSS:** Hot Module Replacement (HMR) only supports CSS; any modification to HTML, layouts, or markdown files triggers a full page reload, degrading developer velocity.  
- **Subcommand Deficit:** Developers must manually pass verbose flags (`ssg -s public -w`) because standard subcommands like `ssg dev`, `ssg build`, `ssg check`, and `ssg lint` do not exist.

---

## Architectural Gaps We Are Missing (New Discoveries)

Beyond the gaps in v0.0.41, assessing the project against a financial-grade risk profile surfaces several capabilities it does not yet provide but an enterprise buyer would require:

### 1. WebAssembly Plugin Sandboxing (Zero-Trust Extension)

While the compiler binary itself is written in safe Rust, allowing arbitrary third-party plugins to execute natively on host systems introduces a severe supply-chain vulnerability. A compromised third-party plugin could easily access the host's filesystem, read proprietary Markdown files, or exfiltrate private credentials.

* **Missing Capability:** A sandboxed execution environment. To achieve zero-trust compilation, the compiler should execute third-party plugins inside an embedded WebAssembly runtime (such as `wasmtime`). Plugins should interact with the host solely via a restricted WebAssembly System Interface (WASI), limiting their access strictly to the page being transformed.

### 2. Zero-Copy HTML Parsing via Streaming AST (`lol_html`)

Migrating the HTML parsing layer to a full in-memory DOM library (like Kuchiki or html5ever) introduces significant memory overhead and processing pauses when handling sites with over 100,000 pages.

* **Missing Capability:** A streaming, zero-copy HTML rewriter. Utilizing Cloudflare's `lol_html` (Low-Output-Latency HTML rewriter) allows the compiler to parse, inspect, and modify HTML elements in a single streaming pass with near-zero memory allocation, matching the parallel streaming compiler's target of sub-second builds.

### 3. Local Semantic Vector Search (Local RAG)

The current search index (`SearchPlugin`) generates a heavy, flat JSON index that performs simple client-side string matches, lacking support for fuzzy search, stemming, or semantic queries. Pagefind is an improvement, but it still relies on downloading a large index.

* **Missing Capability:** Embedded semantic search. The compiler should leverage a local, lightweight Rust-native vector embedding model (such as a MiniLM-L6 model executed via `candle` or `ort` / ONNX Runtime) at build-time. It should generate dense vector embeddings for every page paragraph and output a compact vector index. The client-side search widget, compiled to WASM, can then perform true offline semantic search directly in the browser.

### 4. Deterministic Translation and Inference Caching

Because local LLM inference (e.g., via Ollama or Llama.cpp) is highly CPU/GPU intensive, translating or generating metadata for thousands of pages on every build is computationally prohibitive.

* **Missing Capability:** Content-hash-based inference caching. The compiler must maintain a deterministic cache of all LLM operations. If the SHA-256 hash of a markdown file's content and its translation parameters matches a cache entry, the compiler should reuse the cached translation and metadata, bypassing redundant local inference.

### 5. Asynchronous File I/O for Parallel Scaling

While the plugin pipeline is parallelised via Rayon, standard synchronous disk writes block Rayon's OS threads, creating an I/O bottleneck when writing tens of thousands of pages.

* **Missing Capability:** Asynchronous, non-blocking disk I/O. The compiler should decouple CPU-intensive tasks (Markdown parsing, minification) from disk-bound writes, using asynchronous I/O thread pools or Linux `io_uring` bindings (via `rio` or `tokio`) to write compiled pages in parallel without blocking the parallel CPU executors.

---

## The Strategic 1.0 Roadmap

The following roadmap integrates both the resolved gaps and the newly discovered enterprise-grade capabilities into a structured, chronological release framework.

### Phase 1: 0.0.42 (The Robustness and Correctness Patch, 1 to 2 weeks)

1. **Reconstruct `MinifyPlugin`:** Integration of `minify-html`, `oxc_minifier`, and `lightningcss` for native, syntactically aware HTML, JS, and CSS minification. Ensure the plugin recursively walks all nested directories under `site_dir`.  
2. **Secure the AI Pipeline:** Port `LlmPlugin` from native `curl` shellouts to `ureq` (a lightweight, synchronous, safe Rust HTTP client) to ensure cross-platform compatibility and eliminate shell injection vulnerabilities.  
3. **Complete AVIF Implementation:** Plumb `ravif` directly into the image asset pipeline, enabling high-performance AVIF encoding alongside WebP and PNG.  
4. **Automate HrefLang and Multi-Locale Mapping:** Automatically detect parallel translated pages in multilingual builds and inject standard Google-compliant `<link rel="alternate" hreflang="..." />` tags into the head of each compiled HTML file.  
5. **JSON Feed 1.1 Support:** Ship a dedicated JSON Feed 1.1 emitter alongside standard RSS 2.0 and Atom 1.0 syndication channels.

### Phase 2: 0.1.0 (The Credibility and Incremental Minor, 2 to 3 months)

1. **Populate `DepGraph` and Enable `--incremental`:** Fully wire `DepGraph` to track template-to-page and markdown-to-page dependencies. Implement a cache invalidation layer and wire the `--incremental` CLI flag, targeting sub-200ms rebuilds for warm-cache environments.  
2. **Streaming AST Rewrite via `lol_html`:** Replace fragile string rewriting in `image_plugin.rs`, `search.rs`, and CSP injections with a streaming, zero-copy HTML rewriter powered by `lol_html`.  
3. **Event-Driven Watcher and Component HMR:** Port the watch module from polling to the event-driven `notify` crate, and implement CSS-only and partial-HTML hot reloading for sub-100ms browser updates.  
4. **Unified Command CLI:** Re-architect the compiler interface to support standard subcommands: `ssg dev`, `ssg build`, `ssg check` (accessibility/SEO audit), and `ssg deploy`.  
5. **Deterministic Inference Cache:** Implement a content-hash caching layer for all local LLM translation, summarisation, and metadata extraction tasks.

### Phase 3: 1.0.0 (The Enterprise and Production Major, 6 to 12 months)

1. **Zero-Trust WASM Plugin Sandboxing:** Embed a WebAssembly runtime (`wasmtime` or `wasmer`) to execute third-party plugins in a fully sandboxed environment with capability-based filesystem and network access.  
2. **Local Semantic Vector Search (Local RAG):** Embed a local Rust-native embedding model (via `candle` or `ort`) to compile dense paragraph embeddings into a compact index, enabling private, client-side semantic search.  
3. **Server Islands and WASM Edge Target:** Implement `<ssg-island>` component execution on edge runtimes (such as Cloudflare Workers, Vercel Edge, or Netlify Edge) built on top of the compiled `ssg-wasm` core.  
4. **Asynchronous Parallel I/O Engine:** Re-architect the file system writing module to use asynchronous I/O thread pools and `io_uring` bindings, eliminating CPU worker blocks during parallel writes.  
5. **SLSA v1.1 Build Provenance & SPDX 3.0 Compliance:** Provide mathematically verifiable SLSA Level 3 build provenance and generate SPDX 3.0 compliant SBOMs, fully satisfying modern software supply-chain security standards.

---

## Competitor Matrix (2026 Landscape)

The following matrix compares `static-site-generator` (v1.0 target) against the leading web publishing engines of 2026:

| Capability | static-site-generator v1.0 | Hugo v0.155+ | Zola v0.19+ | Astro 5 | Eleventy 3 |
| ---- | ---- | ---- | ---- | ---- | ---- |
| **Language / Runtime** | Rust (Zero Unsafe) | Go | Rust | JS (Node/V8) | JS (Node/V8) |
| **A11y Build Gate** | Build-Time AST Validation | None | None | Post-build Linter | Post-build Linter |
| **Security Hardening** | SHA-384 SRI & CSP Injection | Manual | Manual | Manual | Manual |
| **Supply-Chain Safety** | SLSA L3 \+ SPDX 3.0 \+ WASM Sandbox | Minimal | Minimal | Heavy NPM Tree | Heavy NPM Tree |
| **AI Content Pipeline** | Private, Local-First (Local LLM) | None | None | Public API Only | Public API Only |
| **Incremental Speed** | \<200ms (Warm Cache) | \<100ms | \<150ms | \~1.5s | \~140ms |
| **Dynamic Interactivity** | Server Islands (WASM Targets) | None | None | Server Islands (JS) | Islands (JS) |
| **Search Engine** | Local Semantic WASM Search | Simple String | Simple String | Pagefind (JS) | Pagefind (JS) |

---

## Positioning at 1.0

At 1.0, the intended positioning is a static site generator engineered as secure-by-default software infrastructure: authoring supported by local-first AI pipelines; compilation of 100,000-plus pages through a parallel streaming pipeline; WCAG 2.2 AA and strict CSP and SRI enforced as build gates; and sandboxed dynamic islands, all within a single, memory-safe Rust binary. Each clause in that statement maps to a specific item in the roadmap above rather than to a marketing aspiration.

---

## Regulatory and Compliance Integration

In high-stakes enterprise and financial sectors, software is evaluated through the lens of compliance and risk capital. The architectural roadmap of `static-site-generator` aligns directly with major regulatory mandates:

- **DORA Article 6 (ICT Risk Management):** The compile-time calculation and injection of SHA-384 SRI hashes and strict Content Security Policies satisfy the requirement to protect digital publishing channels from supply-chain injection, web defacement, and cross-site scripting (XSS) vectors.  
- **DORA Article 7 (ICT Systems Resilience):** By moving to immutable, compile-time verified static assets, financial institutions eliminate database and runtime server vulnerabilities, lowering the operational risk multiplier and reducing required risk capital reserves under Basel III.  
- **European Accessibility Act (EAA) Directive (EU) 2019/882:** Shifting accessibility auditing left into the compilation pipeline as a hard compiler gate guarantees 100% compliance prior to deployment, eliminating the risk of brand damage and civil litigation under EAA and ADA Title III.  
- **GDPR Article 25 (Privacy-by-Design):** Running the translation and metadata pipeline on local, network-isolated hardware keeps proprietary drafts, financial metrics and personal data out of public third-party cloud LLM providers, supporting compliance with data-sovereignty principles.

---

## Frequently Asked Questions

**What does version 0.0.41 actually ship today, versus what the README claims?**
The security and accessibility model is real and enforced in code: workspace-wide `forbid(unsafe_code)`, SHA-256/384 SRI generation, CSP extraction, signed releases with Sigstore attestation and a CycloneDX SBOM, and a build-halting WCAG 2.2 AA gate. Three documented features are not functional in v0.0.41. The `MinifyPlugin` is a whitespace collapser rather than a syntax-aware minifier; the `DepGraph` that would drive incremental rebuilds is compiled but never populated in production code; and AVIF encoding is a stub whose `avif_variants` returns an empty vector.

**Is the accessibility gate a real compiler gate or a post-build linter?**
It is a build gate. WCAG 2.2 AA checks run inside the compilation pipeline through a build-time axe-core parser driven by Playwright, and a failing page halts compilation with exact line-number errors rather than emitting a warning after the fact. That is the property a European Accessibility Act obligation needs: non-compliant output cannot reach deployment.

**Why does shelling out to `curl` in the LLM plugin matter?**
The local LLM pipeline (`src/plugins/llm.rs`) invokes the host's `curl` binary to reach local endpoints. That couples the build to a host executable, fails on systems without `curl` on the PATH, introduces shell-injection surface, and breaks in network-isolated CI. Porting the call to a Rust HTTP client such as `ureq` removes the external dependency and the injection vector, which is why it is the second item in the 0.0.42 patch.

**What is the single most important item on the road to 1.0?**
Populating the `DepGraph` and wiring the `--incremental` flag. Incremental rebuilds are the credibility gap between the documented and the actual engine, and every downstream claim about sub-second builds at 100,000-plus pages depends on the dependency graph tracking template-to-page and markdown-to-page edges rather than remaining test-only infrastructure.

## References

- [Cloudflare, *lol-html: Low-Output-Latency streaming HTML rewriter*](https://github.com/cloudflare/lol-html "Cloudflare lol-html — streaming HTML rewriter") ⧉. [The streaming, zero-copy HTML rewriter proposed to replace fragile string manipulation in the 0.1.0 phase.]
- [W3C, *Web Content Accessibility Guidelines (WCAG) 2.2*](https://www.w3.org/TR/WCAG22/ "W3C — WCAG 2.2 Recommendation") ⧉. [The Level AA success criteria enforced by the compile-time accessibility gate.]
- [European Union, *Regulation (EU) 2022/2554 (DORA)*](https://eur-lex.europa.eu/eli/reg/2022/2554/oj "EUR-Lex — Digital Operational Resilience Act") ⧉. [The ICT risk-management and resilience articles the security posture maps to.]
- [OpenSSF, *Supply-chain Levels for Software Artifacts (SLSA) v1.0*](https://slsa.dev/spec/v1.0/ "SLSA — v1.0 specification") ⧉. [The build-provenance framework targeted for verifiable Level 3 attestation at 1.0.]
- [Armin Ronacher, *MiniJinja template engine*](https://github.com/mitsuhiko/minijinja "MiniJinja — minimal Jinja2 engine for Rust") ⧉. [The dependency-light engine that replaced Tera and trimmed the transitive tree.]
- [CycloneDX, *Software Bill of Materials specification v1.5*](https://cyclonedx.org/docs/1.5/ "CycloneDX — SBOM specification v1.5") ⧉. [The SBOM format emitted on every build for supply-chain audit.]
- [European Union, *Directive (EU) 2019/882 (European Accessibility Act)*](https://eur-lex.europa.eu/eli/dir/2019/882/oj "EUR-Lex — European Accessibility Act") ⧉. [The accessibility obligation the build-time WCAG gate is designed to satisfy.]

*Last reviewed July 2026. Original analysis based on inspection of the `static-site-generator` codebase at v0.0.41; sources are cited, not reproduced. Version numbers and feature status move quickly, verify against the repository before republication. Licensed under CC-BY-4.0.*

