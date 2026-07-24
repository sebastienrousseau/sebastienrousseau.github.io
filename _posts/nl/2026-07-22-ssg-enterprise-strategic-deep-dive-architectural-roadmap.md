---
author: "contact@sebastienrousseau.com (Sebastien Rousseau)"
banner_alt: "Een abstracte technische achtergrond die de architecturale routekaart van een enterprise-grade static site generator verbeeldt."
banner_height: "1280"
banner_width: "1920"
banner: "https://cloudcdn.pro/stocks/images/gemini-background.webp"
cdn: "https://cloudcdn.pro"
charset: "UTF-8"
cname: "sebastienrousseau.com"
copyright: "© Copyright 2025 - 2026 - Sebastien Rousseau. All rights reserved."
date: "July 22, 2026"
description: "Diepgaande analyse van een Rust static-site generator: compile-time beveiliging, WCAG-gates, lokale AI, de tekortkomingen in v0.0.41 en de routekaart naar 1.0."
format-detection: "telephone=no"
hreflang: "nl"
icon: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
id: "https://sebastienrousseau.com/nl/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
image_alt: "Zwart-witportret van Sebastien Rousseau"
image_height: "162"
image_width: "162"
image: "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp"
keywords: "static site generator, Rust, forbid unsafe_code, WCAG 2.2 AA, Content Security Policy, Subresource Integrity, SLSA, CycloneDX SBOM, lokale LLM-pipeline, DORA, incrementele builds, lol_html, WASM-plugin-sandbox, semantisch vectorzoeken, MiniJinja, Ollama"
language: "nl"
last_reviewed: "2026-07-22"
layout: "report"
locale: "nl_NL"
logo_alt: "Logo van Sebastien Rousseau"
logo_height: "44"
logo_width: "44"
logo: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
menu: ""
measurementID: "G-169G4ET5HQ"
name: "Sebastien Rousseau"
permalink: "https://sebastienrousseau.com/nl/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
rating: "general"
referrer: "no-referrer"
robots: "index, follow"
schema: "FAQPage, Article"
seo_title: "Static Site Generator: de weg naar 1.0"
short_name: "sebastienrousseau"
subtitle: "Een architecturale audit en routekaart voor een Rust static-site generator die is gebouwd als secure-by-default infrastructuur: wat v0.0.41 werkelijk levert versus wat de README belooft, vijf ontbrekende enterprise-mogelijkheden en een gefaseerd pad naar een op DORA en EAA afgestemde 1.0."
tags: "static site generator, Rust, webbeveiliging, toegankelijkheid, DORA, toeleveringsketen, SLSA, lokale AI, WCAG, compile-time, routekaart, enterprise"
theme-color: "0, 83, 191"
title: "Static Site Generator (SSG): enterprise-analyse en routekaart"
url: "https://sebastienrousseau.com/nl/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap/rss.xml"
category: "Technology"
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.26)"
item_description: "Diepgaande analyse van een Rust static-site generator: compile-time beveiliging, WCAG-gates, lokale AI, de tekortkomingen in v0.0.41 en de routekaart naar 1.0."
item_guid: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap/rss.xml"
item_link: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap/rss.xml"
item_pub_date: "Wed, 22 Jul 2026 07:07:07 +0000"
item_title: "Static Site Generator (SSG): enterprise-analyse en routekaart"
last_build_date: "Wed, 22 Jul 2026 06:06:06 +0000"
managing_editor: "contact@sebastienrousseau.com (Sebastien Rousseau)"
pub_date: "Wed, 22 Jul 2026 07:07:07 +0000"
ttl: "60"
type: "article"
webmaster: "contact@sebastienrousseau.com"
apple_mobile_web_app_orientations: "portrait"
apple_touch_icon_sizes: "192x192"
apple-mobile-web-app-capable: "yes"
apple-mobile-web-app-status-bar-inset: "black"
apple-mobile-web-app-status-bar-style: "black-translucent"
apple-mobile-web-app-title: "SSG: de weg naar 1.0"
apple-touch-fullscreen: "yes"
msapplication-navbutton-color: "0, 83, 191"
twitter_card: "summary_large_image"
twitter_creator: "@wwdseb"
twitter_description: "Compile-time WCAG-gates, SHA-384 SRI, CSP-injectie en lokale LLM-pipeline onderscheiden deze Rust-engine. Eerlijke analyse van v0.0.41 en de weg naar 1.0."
twitter_image: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
twitter_image_alt: "Logo van Sebastien Rousseau"
twitter_site: "@wwdseb"
twitter_title: "Static Site Generator: de weg naar 1.0"
twitter_url: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
excerpt: "Compile-time WCAG-gates, SHA-384 SRI, CSP-injectie en lokale LLM-pipeline onderscheiden deze Rust-engine. Een eerlijke analyse van v0.0.41 en de weg naar 1.0."
author_website: "https://sebastienrousseau.com"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "Bedankt voor het lezen!"
site_last_updated: "2026-07-22"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "Kaishi, Kaishi Builder, Kaishi CLI, Kaishi Templates, Kaishi Themes"
---

# Static Site Generator (SSG): strategische diepgaande analyse en architecturale routekaart voor enterprises

*Onderzoeksdatum: 2026-06-22. Gebaseerd op codebase-inspectie van `static-site-generator` op v0.0.41 en webonderzoek naar de SSG-markt van 2026.*

**Voor een gereguleerde uitgever is een static site generator geen ontwerptool meer; het maakt deel uit van de operationele risicoperimeter.** De opensource Rust-[static-site-generator](https://github.com/sebastienrousseau/static-site-generator) is op die premisse gebouwd: beveiliging, toegankelijkheid, internationalisatie en AI-contentpipelines verschuiven naar compile-time, zodat een mislukte controle de build stopzet in plaats van de productie te bereiken. Deze analyse scheidt wat versie 0.0.41 werkelijk levert van wat de documentatie nog slechts belooft, benoemt vijf enterprise-mogelijkheden die nog ontbreken en stelt een gefaseerd pad voor naar een 1.0-release die is afgestemd op DORA (Digital Operational Resilience Act), de European Accessibility Act (Europese toegankelijkheidsrichtlijn) en moderne standaarden voor de toeleveringsketen.

<!-- lead-start -->
<aside class="post-lead" aria-label="Artikelsamenvatting">
<p class="post-lead-tldr"><strong>TL;DR.</strong> De Rust-<code>static-site-generator</code> behandelt webpublicatie als een auditeerbare, secure-by-default softwarepipeline: workspace-brede <code>forbid(unsafe_code)</code>, SHA-384 Subresource Integrity, extractie van Content Security Policy, een compile-time WCAG 2.2 AA-gate en een lokale LLM-pipeline. Een code-inspectie van v0.0.41 laat zien dat verschillende gedocumenteerde functies nog aspiraties zijn, waaronder native minificatie, incrementele rebuilds en AVIF. Dit is de eerlijke tekortkomingenanalyse en een gefaseerde routekaart naar een enterprise-grade 1.0.</p>
<p class="post-lead-heading"><strong>Belangrijkste conclusies</strong></p>
<ul class="post-lead-takeaways">
  <li><strong>Het beveiligings- en toegankelijkheidsmodel is echt.</strong> Compile-time SRI, CSP-extractie, ondertekende releases met Sigstore-attestatie en CycloneDX-SBOM's, plus een build-stoppende WCAG 2.2 AA-gate, zijn in code geïmplementeerd en niet alleen gedocumenteerd.</li>
  <li><strong>Verschillende kernfuncties niet.</strong> De minifier is een whitespace-samenvouwer, de dependency-graph die incrementele builds zou aandrijven wordt in productie nooit gevuld, en AVIF-encoding is een stub die een lege vector teruggeeft.</li>
  <li><strong>Vijf enterprise-mogelijkheden ontbreken.</strong> WASM-plugin-sandboxing, een streaming zero-copy HTML-rewriter, lokaal semantisch zoeken, deterministische inference-caching en asynchrone bestands-I/O.</li>
  <li><strong>De routekaart is op risico gerangschikt.</strong> Een correctheidspatch (0.0.42), een minor voor geloofwaardigheid en incrementele builds (0.1.0), daarna een enterprise-major (1.0.0) met de sandbox, semantisch zoeken en SLSA v1.1-provenance.</li>
</ul>
<p class="post-lead-related"><strong>Verder lezen:</strong> <a href="https://sebastienrousseau.com/2026-07-03-emerging-technology-risk-horizon-banks-2026">De risicohorizon van opkomende technologie voor banken</a>, <a href="https://sebastienrousseau.com/2026-07-07-corporate-banking-api-standard-agentic-mcp-2026">Een API-standaard voor corporate banking voor agentische MCP</a>.</p>
</aside>
<!-- lead-end -->

> **Managementsamenvatting**
>
> - **Publiceren is nu een operationele risicoperimeter.** Onder DORA, de European Accessibility Act en de GDPR (Algemene Verordening Gegevensbescherming, AVG) is elk publiek toegankelijk asset een potentieel toegangspunt voor compromittering van de toeleveringsketen, defacement en regelgevingsrisico. Een compile-time model verkleint die perimeter door niet-conforme output te weigeren voordat deze wordt verzonden.
> - **De onderscheidende eigenschappen van de engine worden door de compiler afgedwongen, het zijn geen gedocumenteerde aspiraties.** Workspace-brede `forbid(unsafe_code)`, echte SHA-256/384 SRI, automatische CSP-extractie en een WCAG 2.2 AA-gate tijdens de build maken van beveiliging en toegankelijkheid geen achteraf uitgevoerde audits meer, maar harde build-fouten.
> - **Versie 0.0.41 kent een kloof tussen documentatie en code.** Native minificatie, incrementele rebuilds via een dependency-graph en AVIF-ondersteuning worden beschreven maar zijn niet functioneel; het artikel benoemt elke tekortkoming bij de exacte broncodelocatie.
> - **Het pad naar 1.0 is een volgorde, geen wensenlijst.** Eerst robuustheid (0.0.42), dan incrementele correctheid (0.1.0), daarna de enterprise-mogelijkheden, WASM-sandboxing, lokaal semantisch zoeken en verifieerbare SLSA-provenance, die een gereguleerde koper vereist (1.0.0).

## Huidige sterke punten

De `static-site-generator`-codebase toont verschillende onderscheidende engineeringkeuzes die deze scheiden van oudere JavaScript- en Go-engines:

- **Beveiligingshouding op compile-time:** Workspace-brede `#![forbid(unsafe_code)]` biedt geheugenveiligheidsgaranties op compile-time. De build-pipeline genereert echte SHA-256/SHA-384 Subresource Integrity (SRI)-hashes (`src/plugins/assets.rs`) en voert automatische extractie van de Content Security Policy (CSP) uit, waarbij unsafe-inline scripts en styles worden verwijderd. Releases worden ondertekend, dragen Sigstore-attestatie en produceren bij elke build een CycloneDX 1.5-SBOM (Software Bill of Materials).  
- **Door de compiler afgedwongen toegankelijkheidsgate:** Controles op Web Content Accessibility Guidelines (WCAG) 2.2 niveau AA draaien binnen de compilatiepipeline via een axe-core-parser tijdens de build, aangestuurd door Playwright. Toegankelijkheid wordt een harde build-gate in plaats van een audit na publicatie: als een pagina faalt, stopt de compilatie met foutmeldingen op exacte regelnummers.  
- **Datasoevereine AI-pipeline:** Een vertaal- en metadata-extractiepipeline op basis van een lokale LLM (via lokale Ollama- of llama.cpp-endpoints) stelt een instelling in staat om contentsamenvatting, generatie van JSON-LD-schema's en meertalige vertaling te automatiseren zonder vertrouwelijke informatie vóór cijferpublicaties of gevoelig intellectueel eigendom naar publieke cloud-AI-API's te sturen.  
- **Geparallelliseerde compilatie:** Rusts geheugenveiligheidsgaranties liggen ten grondslag aan een geparallelliseerde, door Rayon aangestuurde HTML- en assetpipeline (`src/core/pipeline.rs`). De plugin-pipeline voert gefuseerde transformaties uit, waarbij `SearchPlugin`, `SeoPlugin`, `CanonicalPlugin` en `JsonLdPlugin` werken via `par_iter()`, zodat elke pagina één keer wordt gelezen en naar schijf geschreven.  
- **Hygiëne van toeleveringsketen en dependencies:** Het migreren van de template-engine van Tera naar MiniJinja (`v0.0.37`) verkleinde de binary, verwijderde transitieve dependencies zoals `rand` op compile-time en leverde een compacte dependency-footprint op die de blootstelling van de softwaretoeleveringsketen verlaagt.

---

## Tekortkomingen en de realiteit in de praktijk

Ondanks deze uitzonderlijke sterke punten onthult een grondige codebase-inspectie van v0.0.41 verschillende architecturale, functionele en developer-experience-tekortkomingen tussen de documentatieclaims en de daadwerkelijke Rust-code:

### Architecturale tekortkomingen

- **Whitespace samenvouwen versus native minificatie:** Hoewel de README "native JS/CSS-minificatie" belooft, functioneert de `MinifyPlugin` (`src/plugins/plugins.rs:96-116`) slechts als een naïeve whitespace-samenvouwer. De plugin stopt vroegtijdig bij `<pre>`-elementen en vouwt whitespace-reeksen in HTML samen, maar voert geen syntactisch bewuste native CSS- of JS-minificatie uit. Bovendien verwerkt de plugin alleen pagina's op het hoogste niveau en doorloopt deze de submappen (zoals `/blog/` of `/tags/`) niet recursief, waardoor diepe pagina's ongeminificeerd blijven.  
- **Dode incrementele infrastructuur:** De dependency-trackinggraph (`DepGraph` in `src/core/depgraph.rs`) wordt gecompileerd en in `PluginContext.dep_graph` geladen, maar wordt in productiecode nooit daadwerkelijk gevuld. De methode `add_dep()` wordt alleen in unittests aangeroepen, waardoor de README-claim van "incrementele rebuilds via dependency-graphs" vooralsnog een aspiratie is.  
- **Batchcompilatie versus streamingcompilatie:** De module `streaming::compile_batch` (`src/core/streaming.rs`) streamt niet echt. In plaats daarvan compileert deze pagina's in batches naar een tijdelijke map, voert `staticdatagen::compile` voor elke batch opnieuw vanaf nul uit en voegt de outputs samen. Dit leidt tot aanzienlijke disk-I/O-overhead en overbodige parsing, wat afwijkt van een echte streamingarchitectuur.  
- **Schendingen van de plugin-lifecyclefase:** Plugins die tijdens het buildproces nieuwe HTML-pagina's genereren, zoals `TaxonomyPlugin`, `PaginationPlugin` en `I18nPlugin`, schrijven in `after_compile` rechtstreeks naar schijf in plaats van de `transform_html`-lifecycle te gebruiken. Als gevolg daarvan omzeilen door deze plugins gegenereerde pagina's cruciale nabewerkingsplugins (zoals `CanonicalPlugin`, `JsonLdPlugin`, `RobotsPlugin` en `AccessibilityPlugin`) wanneer die plugins eerder waren geregistreerd. Hierdoor blijven tag-, categorie- en gepagineerde pagina's zonder correcte canonieke links, JSON-LD-schema's of toegankelijkheidsvalidaties.  
- **Shell-aanroep van `curl` in `LlmPlugin`:** De lokale LLM-contentpipeline (`src/plugins/llm.rs`) roept rechtstreeks de `curl`-binary van de host aan via de shell om lokale endpoints te bevragen. Dit veroorzaakt ernstige platformoverschrijdende bugs (bijvoorbeeld op Windows-hosts zonder curl in de PATH), vormt een beveiligingsrisico (shell-injectievectoren) en faalt in afgeschermde of netwerkgeïsoleerde CI-omgevingen.  
- **Naïeve stringmanipulatie bij het herschrijven van HTML:** De extractors `image_plugin.rs` en `search.rs` herschrijven HTML-strings met fragiele `str::find`- en `str::rfind`-operaties. Deze aanpak is zeer kwetsbaar voor kapotte HTML-tags, `<img>`-tags in commentaar, karakterentiteiten in alt-tekst of reeds bestaande `srcset`-eigenschappen, wat kan leiden tot corrupte output.  
- **Niet-geïmplementeerde AVIF-ondersteuning:** Hoewel AVIF-beeldencoding uitgebreid gedocumenteerd is, is de implementatie in `image_plugin.rs` een stub waarin `avif_variants` simpelweg `Vec::new()` teruggeeft, waardoor de functie niet werkt.  
- **Polling-gebaseerde watcher:** De watcher van de lokale ontwikkelserver (`src/server/watch.rs`) gebruikt polling in plaats van filesystem-event-API's, wat leidt tot buitensporig CPU-gebruik in rust en wijzigingslatentie van onder een seconde.

### Functionele en DX-tekortkomingen

- **Geen tracking van transitieve dependencies:** De dependency-graph kan geneste dependencies niet volgen (bijvoorbeeld wijzigingen aan een sub-template die een layout beïnvloeden die weer een pagina beïnvloedt), zoals bevestigd door de unittest `transitive_not_tracked`.  
- **Geen CLI-flag voor incrementele compilatie:** Er is geen `--incremental`-CLI-flag gekoppeld aan de uitvoerende compiler, waardoor ontwikkelaars geen gebruik kunnen maken van gecachete builds.  
- **HMR is beperkt tot CSS:** Hot Module Replacement (HMR) ondersteunt alleen CSS; elke wijziging aan HTML-, layout- of markdown-bestanden veroorzaakt een volledige paginaherlaad, wat de ontwikkelsnelheid verlaagt.  
- **Tekort aan subcommando's:** Ontwikkelaars moeten handmatig uitgebreide flags meegeven (`ssg -s public -w`) omdat standaardsubcommando's zoals `ssg dev`, `ssg build`, `ssg check` en `ssg lint` niet bestaan.

---

## Architecturale tekortkomingen die we missen (nieuwe bevindingen)

Naast de tekortkomingen in v0.0.41 brengt een beoordeling van het project tegen een risicoprofiel van financiële kwaliteit verschillende mogelijkheden aan het licht die het nog niet biedt maar die een enterprise-koper zou vereisen:

### 1. WebAssembly-plugin-sandboxing (zero-trust-uitbreiding)

Hoewel de compiler-binary zelf in veilig Rust is geschreven, introduceert het native uitvoeren van willekeurige plugins van derden op hostsystemen een ernstige kwetsbaarheid in de toeleveringsketen. Een gecompromitteerde plugin van derden zou eenvoudig toegang kunnen krijgen tot het bestandssysteem van de host, propriëtaire Markdown-bestanden kunnen lezen of private credentials kunnen exfiltreren.

* **Ontbrekende mogelijkheid:** Een omgeving met sandbox-uitvoering. Om zero-trust-compilatie te bereiken zou de compiler plugins van derden moeten uitvoeren binnen een ingebedde WebAssembly-runtime (zoals `wasmtime`). Plugins zouden uitsluitend via een beperkte WebAssembly System Interface (WASI) met de host moeten communiceren, waardoor hun toegang strikt beperkt blijft tot de pagina die wordt getransformeerd.

### 2. Zero-copy HTML-parsing via streaming-AST (`lol_html`)

Het migreren van de HTML-parsinglaag naar een volledige in-memory DOM-bibliotheek (zoals Kuchiki of html5ever) introduceert aanzienlijke geheugenoverhead en verwerkingspauzes bij sites met meer dan 100.000 pagina's.

* **Ontbrekende mogelijkheid:** Een streaming, zero-copy HTML-rewriter. Het gebruik van Cloudflares `lol_html` (Low-Output-Latency HTML-rewriter) stelt de compiler in staat om HTML-elementen in één streaming-pass te parsen, inspecteren en wijzigen met bijna nul geheugenallocatie, wat aansluit bij het doel van de parallelle streamingcompiler van builds onder een seconde.

### 3. Lokaal semantisch vectorzoeken (lokale RAG)

De huidige zoekindex (`SearchPlugin`) genereert een zware, platte JSON-index die eenvoudige stringmatches aan de clientzijde uitvoert en geen ondersteuning biedt voor fuzzy zoeken, stemming of semantische query's. Pagefind is een verbetering, maar is nog steeds afhankelijk van het downloaden van een grote index.

* **Ontbrekende mogelijkheid:** Ingebed semantisch zoeken. De compiler zou tijdens de build gebruik moeten maken van een lokaal, lichtgewicht Rust-native vector-embeddingmodel (zoals een MiniLM-L6-model uitgevoerd via `candle` of `ort` / ONNX Runtime). Het model zou dichte vector-embeddings moeten genereren voor elke paragraaf van een pagina en een compacte vectorindex moeten produceren. De naar WASM gecompileerde zoekwidget aan de clientzijde kan dan echt offline semantisch zoeken rechtstreeks in de browser uitvoeren.

### 4. Deterministische vertaling en inference-caching

Omdat lokale LLM-inference (bijvoorbeeld via Ollama of Llama.cpp) zeer CPU/GPU-intensief is, is het vertalen of genereren van metadata voor duizenden pagina's bij elke build rekentechnisch onhaalbaar.

* **Ontbrekende mogelijkheid:** Inference-caching op basis van content-hash. De compiler moet een deterministische cache van alle LLM-operaties bijhouden. Als de SHA-256-hash van de inhoud van een markdown-bestand en de bijbehorende vertaalparameters overeenkomt met een cache-invoer, zou de compiler de gecachete vertaling en metadata moeten hergebruiken en zo overbodige lokale inference moeten vermijden.

### 5. Asynchrone bestands-I/O voor parallelle schaalbaarheid

Hoewel de plugin-pipeline via Rayon is geparallelliseerd, blokkeren standaard synchrone schijfschrijfacties de OS-threads van Rayon, wat een I/O-bottleneck veroorzaakt bij het schrijven van tienduizenden pagina's.

* **Ontbrekende mogelijkheid:** Asynchrone, niet-blokkerende schijf-I/O. De compiler zou CPU-intensieve taken (Markdown-parsing, minificatie) moeten ontkoppelen van schijfgebonden schrijfacties, met behulp van asynchrone I/O-threadpools of Linux `io_uring`-bindings (via `rio` of `tokio`) om gecompileerde pagina's parallel te schrijven zonder de parallelle CPU-executors te blokkeren.

---

## De strategische routekaart naar 1.0

De volgende routekaart integreert zowel de opgeloste tekortkomingen als de nieuw ontdekte enterprise-grade mogelijkheden in een gestructureerd, chronologisch releasekader.

### Fase 1: 0.0.42 (de robuustheids- en correctheidspatch, 1 tot 2 weken)

1. **Herbouw `MinifyPlugin`:** Integratie van `minify-html`, `oxc_minifier` en `lightningcss` voor native, syntactisch bewuste HTML-, JS- en CSS-minificatie. Zorg dat de plugin alle geneste mappen onder `site_dir` recursief doorloopt.  
2. **Beveilig de AI-pipeline:** Migreer `LlmPlugin` van native `curl`-shell-aanroepen naar `ureq` (een lichtgewicht, synchrone, veilige Rust-HTTP-client) om platformoverschrijdende compatibiliteit te waarborgen en shell-injectiekwetsbaarheden te elimineren.  
3. **Voltooi de AVIF-implementatie:** Koppel `ravif` rechtstreeks aan de image-assetpipeline, waardoor hoogwaardige AVIF-encoding naast WebP en PNG mogelijk wordt.  
4. **Automatiseer HrefLang- en multi-locale-mapping:** Detecteer automatisch parallelle vertaalde pagina's in meertalige builds en injecteer standaard Google-conforme `<link rel="alternate" hreflang="..." />`-tags in de head van elk gecompileerd HTML-bestand.  
5. **JSON Feed 1.1-ondersteuning:** Lever een dedicated JSON Feed 1.1-emitter naast de standaard syndicatiekanalen RSS 2.0 en Atom 1.0.

### Fase 2: 0.1.0 (de geloofwaardigheids- en incrementele minor, 2 tot 3 maanden)

1. **Vul `DepGraph` en schakel `--incremental` in:** Koppel `DepGraph` volledig om afhankelijkheden van template naar pagina en van markdown naar pagina te volgen. Implementeer een laag voor cache-invalidatie en koppel de `--incremental`-CLI-flag, met als doel rebuilds onder 200 ms voor omgevingen met een warme cache.  
2. **Streaming-AST-herschrijving via `lol_html`:** Vervang de fragiele stringherschrijving in `image_plugin.rs`, `search.rs` en CSP-injecties door een streaming, zero-copy HTML-rewriter aangedreven door `lol_html`.  
3. **Event-gestuurde watcher en component-HMR:** Migreer de watch-module van polling naar de event-gestuurde `notify`-crate en implementeer hot reloading voor alleen CSS en gedeeltelijke HTML voor browserupdates onder 100 ms.  
4. **Uniforme command-CLI:** Herstructureer de compiler-interface om standaardsubcommando's te ondersteunen: `ssg dev`, `ssg build`, `ssg check` (toegankelijkheids-/SEO-audit) en `ssg deploy`.  
5. **Deterministische inference-cache:** Implementeer een content-hash-cachinglaag voor alle taken op het gebied van lokale LLM-vertaling, samenvatting en metadata-extractie.

### Fase 3: 1.0.0 (de enterprise- en productie-major, 6 tot 12 maanden)

1. **Zero-trust WASM-plugin-sandboxing:** Bed een WebAssembly-runtime (`wasmtime` of `wasmer`) in om plugins van derden uit te voeren in een volledig gesandboxte omgeving met op capabilities gebaseerde toegang tot bestandssysteem en netwerk.  
2. **Lokaal semantisch vectorzoeken (lokale RAG):** Bed een lokaal Rust-native embeddingmodel (via `candle` of `ort`) in om dichte paragraaf-embeddings te compileren tot een compacte index, waardoor privé semantisch zoeken aan de clientzijde mogelijk wordt.  
3. **Server islands en WASM-edge-target:** Implementeer de uitvoering van `<ssg-island>`-componenten op edge-runtimes (zoals Cloudflare Workers, Vercel Edge of Netlify Edge), gebouwd bovenop de gecompileerde `ssg-wasm`-core.  
4. **Asynchrone parallelle I/O-engine:** Herstructureer de module voor het schrijven naar het bestandssysteem zodat deze asynchrone I/O-threadpools en `io_uring`-bindings gebruikt, waardoor CPU-workerblokkades tijdens parallelle schrijfacties worden geëlimineerd.  
5. **SLSA v1.1-build-provenance en SPDX 3.0-conformiteit:** Lever wiskundig verifieerbare SLSA Level 3-build-provenance en genereer SPDX 3.0-conforme SBOM's, volledig voldoend aan moderne beveiligingsstandaarden voor de softwaretoeleveringsketen.

---

## Concurrentiematrix (marktbeeld 2026)

De volgende matrix vergelijkt `static-site-generator` (v1.0-doel) met de toonaangevende webpublicatie-engines van 2026:

| Mogelijkheid | static-site-generator v1.0 | Hugo v0.155+ | Zola v0.19+ | Astro 5 | Eleventy 3 |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Taal / runtime** | Rust (Zero Unsafe) | Go | Rust | JS (Node/V8) | JS (Node/V8) |
| **A11y-build-gate** | AST-validatie tijdens build | Geen | Geen | Linter na build | Linter na build |
| **Beveiligingsverharding** | SHA-384 SRI en CSP-injectie | Handmatig | Handmatig | Handmatig | Handmatig |
| **Veiligheid toeleveringsketen** | SLSA L3 \+ SPDX 3.0 \+ WASM-sandbox | Minimaal | Minimaal | Zware NPM-boom | Zware NPM-boom |
| **AI-contentpipeline** | Privé, lokaal-eerst (lokale LLM) | Geen | Geen | Alleen publieke API | Alleen publieke API |
| **Incrementele snelheid** | \<200 ms (warme cache) | \<100 ms | \<150 ms | \~1,5 s | \~140 ms |
| **Dynamische interactiviteit** | Server islands (WASM-targets) | Geen | Geen | Server islands (JS) | Islands (JS) |
| **Zoekmachine** | Lokaal semantisch WASM-zoeken | Simpele string | Simpele string | Pagefind (JS) | Pagefind (JS) |

---

## Positionering bij 1.0

Bij 1.0 is de beoogde positionering een static site generator die is ontworpen als secure-by-default software-infrastructuur: auteurschap ondersteund door lokaal-eerst AI-pipelines; compilatie van meer dan 100.000 pagina's via een parallelle streamingpipeline; WCAG 2.2 AA en strikte CSP en SRI afgedwongen als build-gates; en gesandboxte dynamische islands, alles binnen één geheugenveilige Rust-binary. Elke bewering in die uitspraak verwijst naar een specifiek item in de bovenstaande routekaart en niet naar een marketingaspiratie.

---

## Integratie van regelgeving en compliance

In enterprise- en financiële sectoren met hoge inzet wordt software beoordeeld door de bril van compliance en risicokapitaal. De architecturale routekaart van `static-site-generator` sluit rechtstreeks aan op belangrijke regelgevende verplichtingen:

- **DORA Artikel 6 (ICT-risicobeheer):** De berekening en injectie op compile-time van SHA-384 SRI-hashes en strikte Content Security Policies voldoen aan de eis om digitale publicatiekanalen te beschermen tegen injectie via de toeleveringsketen, web-defacement en cross-site scripting (XSS)-vectoren.  
- **DORA Artikel 7 (veerkracht van ICT-systemen):** Door over te stappen op onveranderlijke, op compile-time geverifieerde statische assets elimineren financiële instellingen kwetsbaarheden in databases en runtime-servers, waardoor de operationele-risicomultiplier daalt en de vereiste risicokapitaalreserves onder Basel III afnemen.  
- **European Accessibility Act (EAA), Richtlijn (EU) 2019/882:** Door toegankelijkheidsaudits naar links te verschuiven in de compilatiepipeline als een harde compiler-gate wordt 100% compliance vóór deployment gegarandeerd, waardoor het risico op merkschade en civiele rechtszaken onder de EAA en ADA Title III wordt geëlimineerd.  
- **GDPR Artikel 25 (privacy-by-design):** Het draaien van de vertaal- en metadatapipeline op lokale, netwerkgeïsoleerde hardware houdt propriëtaire concepten, financiële cijfers en persoonsgegevens buiten publieke cloud-LLM-providers van derden, wat de naleving van datasoevereiniteitsprincipes ondersteunt.

---

## Veelgestelde vragen

**Wat levert versie 0.0.41 vandaag daadwerkelijk, versus wat de README beweert?**
Het beveiligings- en toegankelijkheidsmodel is echt en wordt in code afgedwongen: workspace-brede `forbid(unsafe_code)`, generatie van SHA-256/384 SRI, CSP-extractie, ondertekende releases met Sigstore-attestatie en een CycloneDX-SBOM, en een build-stoppende WCAG 2.2 AA-gate. Drie gedocumenteerde functies werken niet in v0.0.41. De `MinifyPlugin` is een whitespace-samenvouwer in plaats van een syntaxbewuste minifier; de `DepGraph` die incrementele rebuilds zou aandrijven wordt gecompileerd maar in productiecode nooit gevuld; en AVIF-encoding is een stub waarvan `avif_variants` een lege vector teruggeeft.

**Is de toegankelijkheidsgate een echte compiler-gate of een linter na de build?**
Het is een build-gate. WCAG 2.2 AA-controles draaien binnen de compilatiepipeline via een axe-core-parser tijdens de build, aangestuurd door Playwright, en een falende pagina stopt de compilatie met foutmeldingen op exacte regelnummers in plaats van achteraf een waarschuwing te geven. Dat is de eigenschap die een verplichting onder de European Accessibility Act nodig heeft: niet-conforme output kan de deployment niet bereiken.

**Waarom is de shell-aanroep van `curl` in de LLM-plugin van belang?**
De lokale LLM-pipeline (`src/plugins/llm.rs`) roept de `curl`-binary van de host aan om lokale endpoints te bereiken. Dat koppelt de build aan een host-executable, faalt op systemen zonder `curl` in de PATH, introduceert een shell-injectie-oppervlak en breekt in netwerkgeïsoleerde CI. Het overzetten van de aanroep naar een Rust-HTTP-client zoals `ureq` verwijdert de externe dependency en de injectievector, en daarom is dit het tweede item in de 0.0.42-patch.

**Wat is het allerbelangrijkste item op weg naar 1.0?**
Het vullen van de `DepGraph` en het koppelen van de `--incremental`-flag. Incrementele rebuilds vormen de geloofwaardigheidskloof tussen de gedocumenteerde en de daadwerkelijke engine, en elke afgeleide claim over builds onder een seconde bij meer dan 100.000 pagina's hangt ervan af of de dependency-graph de verbindingen van template naar pagina en van markdown naar pagina volgt, in plaats van louter test-infrastructuur te blijven.

## Referenties

- [Cloudflare, *lol-html: Low-Output-Latency streaming HTML-rewriter*](https://github.com/cloudflare/lol-html "Cloudflare lol-html — streaming HTML-rewriter") ⧉. [De streaming, zero-copy HTML-rewriter die is voorgesteld om de fragiele stringmanipulatie in de 0.1.0-fase te vervangen.]
- [W3C, *Web Content Accessibility Guidelines (WCAG) 2.2*](https://www.w3.org/TR/WCAG22/ "W3C — WCAG 2.2 Recommendation") ⧉. [De succescriteria van niveau AA die door de toegankelijkheidsgate op compile-time worden afgedwongen.]
- [Europese Unie, *Verordening (EU) 2022/2554 (DORA)*](https://eur-lex.europa.eu/eli/reg/2022/2554/oj "EUR-Lex — Digital Operational Resilience Act") ⧉. [De artikelen over ICT-risicobeheer en veerkracht waarop de beveiligingshouding aansluit.]
- [OpenSSF, *Supply-chain Levels for Software Artifacts (SLSA) v1.0*](https://slsa.dev/spec/v1.0/ "SLSA — v1.0-specificatie") ⧉. [Het build-provenance-framework dat wordt beoogd voor verifieerbare Level 3-attestatie bij 1.0.]
- [Armin Ronacher, *MiniJinja template engine*](https://github.com/mitsuhiko/minijinja "MiniJinja — minimale Jinja2-engine voor Rust") ⧉. [De dependency-lichte engine die Tera verving en de transitieve boom uitdunde.]
- [CycloneDX, *Software Bill of Materials-specificatie v1.5*](https://cyclonedx.org/docs/1.5/ "CycloneDX — SBOM-specificatie v1.5") ⧉. [Het SBOM-formaat dat bij elke build wordt uitgevoerd voor audit van de toeleveringsketen.]
- [Europese Unie, *Richtlijn (EU) 2019/882 (European Accessibility Act)*](https://eur-lex.europa.eu/eli/dir/2019/882/oj "EUR-Lex — European Accessibility Act") ⧉. [De toegankelijkheidsverplichting waaraan de WCAG-gate tijdens de build is ontworpen te voldoen.]

*Laatst herzien in juli 2026. Oorspronkelijke analyse gebaseerd op inspectie van de `static-site-generator`-codebase op v0.0.41; bronnen worden geciteerd, niet gereproduceerd. Versienummers en functiestatus veranderen snel; verifieer deze tegen de repository vóór herpublicatie. Gelicentieerd onder CC-BY-4.0.*
