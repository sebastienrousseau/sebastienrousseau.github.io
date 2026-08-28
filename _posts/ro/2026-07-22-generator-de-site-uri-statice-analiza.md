---
author: "contact@sebastienrousseau.com (Sebastien Rousseau)"
banner_alt: "Un fundal tehnic abstract, reprezentând foaia de parcurs arhitecturală a unui generator de site-uri statice de nivel enterprise."
banner_height: "1280"
banner_width: "1920"
banner: "https://cloudcdn.pro/stocks/images/gemini-background.webp"
cdn: "https://cloudcdn.pro"
charset: "UTF-8"
cname: "sebastienrousseau.com"
copyright: "© Copyright 2025 - 2026 - Sebastien Rousseau. All rights reserved."
date: "July 22, 2026"
description: "Analiză a unui generator de site-uri statice în Rust: securitate la compilare, porți WCAG și AI local, lipsurile din v0.0.41 și o foaie de parcurs enterprise spre 1.0."
format-detection: "telephone=no"
hreflang: "ro"
icon: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
id: "https://sebastienrousseau.com/ro/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
image_alt: "Portret alb-negru al lui Sebastien Rousseau"
image_height: "162"
image_width: "162"
image: "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp"
keywords: "generator site-uri statice, Rust, forbid unsafe_code, WCAG 2.2 AA, Content Security Policy, Subresource Integrity, SLSA, CycloneDX SBOM, pipeline LLM local, DORA, compilări incrementale, lol_html, sandbox plugin WASM, căutare vectorială semantică, MiniJinja, Ollama"
language: "ro"
last_reviewed: "2026-07-22"
layout: "report"
locale: "ro_RO"
logo_alt: "Logo pentru Sebastien Rousseau"
logo_height: "44"
logo_width: "44"
logo: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
menu: ""
measurementID: "G-169G4ET5HQ"
name: "Sebastien Rousseau"
permalink: "https://sebastienrousseau.com/ro/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
rating: "general"
referrer: "no-referrer"
robots: "index, follow"
schema: "FAQPage, Article"
seo_title: "Generator de site-uri statice: drumul spre 1.0"
short_name: "sebastienrousseau"
subtitle: "Un audit arhitectural și o foaie de parcurs pentru un generator de site-uri statice în Rust construit ca infrastructură securizată implicit: ce livrează cu adevărat v0.0.41 față de ce promite README-ul, cinci capabilități enterprise absente și un drum etapizat spre un 1.0 aliniat cu DORA și EAA."
tags: "generator site-uri statice, Rust, securitate web, accesibilitate, DORA, lanț de aprovizionare, SLSA, AI local, WCAG, la compilare, foaie de parcurs, enterprise"
theme-color: "0, 83, 191"
title: "Generator de site-uri statice: analiză strategică și foaie de parcurs"
url: "https://sebastienrousseau.com/ro/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap/rss.xml"
category: "Technology"
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.26)"
item_description: "Analiză a unui generator de site-uri statice în Rust: securitate la compilare, porți WCAG și AI local, lipsurile din v0.0.41 și o foaie de parcurs enterprise spre 1.0."
item_guid: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap/rss.xml"
item_link: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap/rss.xml"
item_pub_date: "Wed, 22 Jul 2026 07:07:07 +0000"
item_title: "Generator de site-uri statice: analiză strategică și foaie de parcurs"
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
apple-mobile-web-app-title: "SSG spre 1.0"
apple-touch-fullscreen: "yes"
msapplication-navbutton-color: "0, 83, 191"
twitter_card: "summary_large_image"
twitter_creator: "@wwdseb"
twitter_description: "Porți WCAG la compilare, SRI SHA-384, injecție CSP și un pipeline LLM local disting acest motor Rust. O analiză onestă a lipsurilor din v0.0.41 și drumul spre un 1.0 enterprise."
twitter_image: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
twitter_image_alt: "Logo al lui Sebastien Rousseau"
twitter_site: "@wwdseb"
twitter_title: "Generator de site-uri statice: drumul spre 1.0"
twitter_url: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
excerpt: "Porți WCAG la compilare, SRI SHA-384, injecție CSP și un pipeline LLM local disting acest motor Rust, dar compilările incrementale, minificarea nativă și AVIF rămân aspirații. Iată analiza onestă a lipsurilor și drumul spre 1.0."
author_website: "https://sebastienrousseau.com"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "Mulțumim pentru lectură!"
site_last_updated: "2026-07-22"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "Kaishi, Kaishi Builder, Kaishi CLI, Kaishi Templates, Kaishi Themes"
---

# Static Site Generator (SSG): Enterprise-Grade Strategic Deep Dive and Architectural Roadmap

*Data cercetării: 2026-06-22. Bazată pe inspecția codului sursă al `static-site-generator` la v0.0.41 și pe cercetarea web a peisajului SSG din 2026.*

**Pentru un editor supus reglementărilor, un generator de site-uri statice nu mai este un instrument de design; face parte din perimetrul de risc operațional.** Motorul open-source Rust [static-site-generator](https://github.com/sebastienrousseau/static-site-generator) este construit pe această premisă, mutând securitatea, accesibilitatea, internaționalizarea și pipeline-urile de conținut AI la momentul compilării, astfel încât o verificare eșuată oprește compilarea în loc să ajungă în producție. Această analiză separă ceea ce livrează cu adevărat versiunea 0.0.41 de ceea ce documentația încă doar promite, prezintă cinci capabilități enterprise pe care nu le deține încă și propune un drum etapizat spre o versiune 1.0 aliniată cu DORA, cu Actul European privind Accesibilitatea și cu standardele moderne de lanț de aprovizionare.

<!-- lead-start -->
<aside class="post-lead" aria-label="Rezumatul articolului">
<p class="post-lead-tldr"><strong>Pe scurt.</strong> Motorul Rust <code>static-site-generator</code> tratează publicarea web ca pe un pipeline software auditabil și securizat implicit: <code>forbid(unsafe_code)</code> la nivel de întreg workspace, Subresource Integrity SHA-384, extracție Content Security Policy, o poartă WCAG 2.2 AA la compilare și un pipeline LLM local. O inspecție a codului la v0.0.41 arată că mai multe funcționalități documentate rămân aspirații, printre ele minificarea nativă, recompilările incrementale și AVIF. Iată analiza onestă a lipsurilor și o foaie de parcurs etapizată spre un 1.0 de nivel enterprise.</p>
<p class="post-lead-heading"><strong>Concluzii principale</strong></p>
<ul class="post-lead-takeaways">
  <li><strong>Modelul de securitate și accesibilitate este real.</strong> SRI la compilare, extracția CSP, versiunile semnate cu atestare Sigstore și SBOM-uri CycloneDX, plus o poartă WCAG 2.2 AA care oprește compilarea, sunt implementate în cod, nu doar documentate.</li>
  <li><strong>Mai multe funcționalități de prim-plan nu sunt.</strong> Minificatorul este un simplu colapsor de spații albe, graful de dependențe care ar propulsa compilările incrementale nu este niciodată populat în producție, iar codarea AVIF este un ciot care returnează un vector gol.</li>
  <li><strong>Cinci capabilități enterprise lipsesc.</strong> Sandbox-area plugin-urilor WASM, un rescriitor HTML zero-copy în flux, căutarea semantică locală, cache-ul determinist de inferență și operațiile de I/O asincrone pe fișiere.</li>
  <li><strong>Foaia de parcurs este ordonată după risc.</strong> Un patch de corectitudine (0.0.42), o versiune minoră de credibilitate și incrementalitate (0.1.0), apoi o versiune majoră enterprise (1.0.0) care aduce sandbox-ul, căutarea semantică și proveniența SLSA v1.1.</li>
</ul>
<p class="post-lead-related"><strong>Lecturi conexe:</strong> <a href="https://sebastienrousseau.com/2026-07-03-emerging-technology-risk-horizon-banks-2026">Orizontul de risc al tehnologiilor emergente pentru bănci</a>, <a href="https://sebastienrousseau.com/2026-07-07-corporate-banking-api-standard-agentic-mcp-2026">Un standard API de banking corporativ pentru MCP agentic</a>.</p>
</aside>
<!-- lead-end -->

> **Rezumat executiv**
>
> - **Publicarea este acum un perimetru de risc operațional.** Sub DORA, Actul European privind Accesibilitatea și GDPR, fiecare activ expus public este un potențial punct de intrare pentru compromiterea lanțului de aprovizionare, defacement și expunere de reglementare. Un model la compilare îngustează acest perimetru respingând rezultatele neconforme înainte ca acestea să fie livrate.
> - **Elementele de diferențiere ale motorului sunt impuse de compilator, nu aspirații documentate.** `forbid(unsafe_code)` la nivel de întreg workspace, SRI SHA-256/384 real, extracția automată a CSP și o poartă WCAG 2.2 AA la compilare transformă securitatea și accesibilitatea din audituri ulterioare în eșecuri ferme de compilare.
> - **Versiunea 0.0.41 are un decalaj între documentație și cod.** Minificarea nativă, recompilările incrementale printr-un graf de dependențe și suportul AVIF sunt descrise, dar nu sunt funcționale; articolul indică fiecare lipsă la locația exactă din codul sursă.
> - **Drumul spre 1.0 este o secvență, nu o listă de dorințe.** Mai întâi robustețea (0.0.42), apoi corectitudinea incrementală (0.1.0), apoi capabilitățile enterprise, sandbox-area WASM, căutarea semantică locală și proveniența SLSA verificabilă, pe care le cere un cumpărător reglementat (1.0.0).

## Puncte forte actuale

Codul `static-site-generator` prezintă mai multe decizii de inginerie distinctive care îl separă de motoarele JavaScript și Go tradiționale:

- **Postură de securitate la compilare:** `#![forbid(unsafe_code)]` la nivel de întreg workspace oferă garanții de siguranță a memoriei la compilare. Pipeline-ul de compilare generează hash-uri Subresource Integrity (SRI) SHA-256/SHA-384 reale (`src/plugins/assets.rs`) și efectuează extracția automată a Content Security Policy (CSP), care elimină scripturile și stilurile unsafe-inline. Versiunile sunt semnate, poartă atestare Sigstore și produc un SBOM CycloneDX 1.5 la fiecare compilare.  
- **Poartă de accesibilitate impusă de compilator:** Verificările Web Content Accessibility Guidelines (WCAG) 2.2 Nivel AA rulează în interiorul pipeline-ului de compilare printr-un parser axe-core la compilare acționat de Playwright. Accesibilitatea devine o poartă de compilare fermă, nu un audit post-publicare: dacă o pagină eșuează, compilarea se oprește cu erori la numărul exact de linie.  
- **Pipeline AI cu suveranitate a datelor:** Un pipeline local de traducere și extracție de metadate bazat pe LLM (prin endpoint-uri locale Ollama sau llama.cpp) permite unei instituții să automatizeze rezumarea conținutului, generarea schemelor JSON-LD și traducerea multilingvă fără a trimite dezvăluiri pre-rezultate sau proprietate intelectuală sensibilă către API-uri AI din cloud public.  
- **Compilare paralelizată:** Garanțiile de siguranță a memoriei din Rust stau la baza unui pipeline HTML și de active paralelizat, propulsat de Rayon (`src/core/pipeline.rs`). Pipeline-ul de plugin-uri execută transformări fuzionate, cu `SearchPlugin`, `SeoPlugin`, `CanonicalPlugin` și `JsonLdPlugin` operând peste `par_iter()`, astfel încât fiecare pagină este citită și scrisă pe disc o singură dată.  
- **Igiena lanțului de aprovizionare și a dependențelor:** Migrarea motorului de șabloane de la Tera la MiniJinja (`v0.0.37`) a redus dimensiunea binarului, a eliminat dependențe tranzitive precum `rand` la compilare și a produs o amprentă compactă de dependențe care reduce expunerea lanțului de aprovizionare software.

---

## Lipsuri și realități concrete

În pofida acestor puncte forte excepționale, o inspecție riguroasă a codului la v0.0.41 dezvăluie mai multe lipsuri arhitecturale, funcționale și de experiență a dezvoltatorului între ceea ce afirmă documentația și codul rust efectiv:

### Lipsuri arhitecturale

- **Colaps de spații albe vs. minificare nativă:** Deși README-ul promite „minificare nativă JS/CSS”, `MinifyPlugin` (`src/plugins/plugins.rs:96-116`) acționează doar ca un colapsor naiv de spații albe. Se oprește la elementele `<pre>` și colapsează secvențele de spații albe din HTML, dar nu efectuează o minificare nativă CSS sau JS conștientă de sintaxă. În plus, procesează doar paginile de nivel superior și nu parcurge recursiv subdirectoarele (precum `/blog/` sau `/tags/`), lăsând paginile de adâncime neminificate.  
- **Infrastructură incrementală moartă:** Graful de urmărire a dependențelor (`DepGraph` în `src/core/depgraph.rs`) este compilat și încărcat în `PluginContext.dep_graph`, dar nu este niciodată populat efectiv în codul de producție. Metoda `add_dep()` este apelată doar în testele unitare, ceea ce face ca afirmația README-ului despre „recompilări incrementale prin grafuri de dependențe” să fie deocamdată o aspirație.  
- **Compilare pe loturi vs. compilare în flux:** Modulul `streaming::compile_batch` (`src/core/streaming.rs`) nu transmite cu adevărat în flux. În schimb, compilează paginile pe loturi într-un director temporar, execută `staticdatagen::compile` de la zero pentru fiecare lot și îmbină rezultatele. Aceasta duce la o supraîncărcare semnificativă de I/O pe disc și la parsare redundantă, deviind de la o arhitectură reală în flux.  
- **Încălcări ale fazelor din ciclul de viață al plugin-urilor:** Plugin-urile care generează pagini HTML noi în timpul compilării, precum `TaxonomyPlugin`, `PaginationPlugin` și `I18nPlugin`, scriu direct pe disc în `after_compile` în loc să folosească ciclul de viață `transform_html`. În consecință, paginile generate de aceste plugin-uri ocolesc plugin-uri critice de post-procesare (precum `CanonicalPlugin`, `JsonLdPlugin`, `RobotsPlugin` și `AccessibilityPlugin`) dacă acele plugin-uri au fost înregistrate mai devreme. Aceasta lasă paginile de etichete, de categorii și cele paginate fără linkuri canonice corecte, fără scheme JSON-LD sau fără validări de accesibilitate.  
- **Apelarea externă a `curl` în `LlmPlugin`:** Pipeline-ul local de conținut LLM (`src/plugins/llm.rs`) apelează direct binarul `curl` al gazdei pentru a interoga endpoint-urile locale. Aceasta introduce erori grave între platforme (de exemplu, pe gazde Windows fără curl în PATH), reprezintă un risc de securitate (vectori de injecție în shell) și eșuează în medii CI blocate sau izolate de rețea.  
- **Manipulare naivă de șiruri în rescrierea HTML:** Extractoarele din `image_plugin.rs` și `search.rs` rescriu șirurile HTML folosind operații fragile `str::find` și `str::rfind`. Această abordare este extrem de vulnerabilă la etichete HTML rupte, la etichete `<img>` din interiorul comentariilor, la entități de caractere în textul alternativ sau la proprietăți `srcset` preexistente, ceea ce poate duce la rezultate corupte.  
- **Suport AVIF neimplementat:** Deși codarea imaginilor AVIF este intens documentată, implementarea din `image_plugin.rs` este un ciot în care `avif_variants` returnează pur și simplu `Vec::new()`, lăsând funcționalitatea nefuncțională.  
- **Supraveghetor bazat pe sondare:** Supraveghetorul serverului local de dezvoltare (`src/server/watch.rs`) folosește sondarea în loc de API-urile de evenimente ale sistemului de fișiere, ceea ce duce la un consum excesiv de CPU în repaus și la o latență de modificare sub o secundă.

### Lipsuri funcționale și de DX

- **Fără urmărirea dependențelor tranzitive:** Graful de dependențe nu poate urmări dependențele imbricate (de exemplu, modificări ale unui sub-șablon care afectează un layout care afectează o pagină), așa cum verifică testul unitar `transitive_not_tracked`.  
- **Fără flag CLI de compilare incrementală:** Nu există niciun flag CLI `--incremental` conectat la compilatorul de execuție, ceea ce împiedică dezvoltatorii să folosească compilări din cache.  
- **HMR limitat la CSS:** Hot Module Replacement (HMR) suportă doar CSS; orice modificare a fișierelor HTML, layout sau markdown declanșează o reîncărcare completă a paginii, degradând viteza de dezvoltare.  
- **Deficit de subcomenzi:** Dezvoltatorii trebuie să transmită manual flag-uri prolixe (`ssg -s public -w`), deoarece subcomenzile standard precum `ssg dev`, `ssg build`, `ssg check` și `ssg lint` nu există.

---

## Lipsuri arhitecturale pe care le avem (descoperiri noi)

Dincolo de lipsurile din v0.0.41, evaluarea proiectului în raport cu un profil de risc de nivel financiar scoate la iveală mai multe capabilități pe care nu le oferă încă, dar pe care un cumpărător enterprise le-ar cere:

### 1. Sandbox-area plugin-urilor WebAssembly (extensie zero-trust)

Deși binarul compilatorului este scris în Rust sigur, permiterea execuției native a plugin-urilor terțe arbitrare pe sistemele gazdă introduce o vulnerabilitate gravă de lanț de aprovizionare. Un plugin terț compromis ar putea accesa cu ușurință sistemul de fișiere al gazdei, ar putea citi fișiere Markdown proprietare sau ar putea exfiltra credențiale private.

* **Capabilitate absentă:** Un mediu de execuție izolat în sandbox. Pentru a obține o compilare zero-trust, compilatorul ar trebui să execute plugin-urile terțe într-un runtime WebAssembly încorporat (precum `wasmtime`). Plugin-urile ar trebui să interacționeze cu gazda exclusiv printr-o interfață restricționată WebAssembly System Interface (WASI), limitându-le accesul strict la pagina în curs de transformare.

### 2. Parsare HTML zero-copy printr-un AST în flux (`lol_html`)

Migrarea stratului de parsare HTML către o bibliotecă DOM completă în memorie (precum Kuchiki sau html5ever) introduce o supraîncărcare semnificativă de memorie și pauze de procesare la gestionarea site-urilor cu peste 100.000 de pagini.

* **Capabilitate absentă:** Un rescriitor HTML în flux, zero-copy. Utilizarea `lol_html` de la Cloudflare (rescriitor HTML cu latență redusă a rezultatelor) permite compilatorului să parseze, să inspecteze și să modifice elemente HTML într-o singură trecere în flux, cu alocare de memorie aproape nulă, atingând ținta compilatorului paralel în flux de compilări sub o secundă.

### 3. Căutare vectorială semantică locală (RAG local)

Indexul de căutare actual (`SearchPlugin`) generează un index JSON greu și plat care efectuează simple potriviri de șiruri pe partea de client, fără suport pentru căutare fuzzy, stemming sau interogări semantice. Pagefind este o îmbunătățire, dar tot se bazează pe descărcarea unui index de mari dimensiuni.

* **Capabilitate absentă:** Căutare semantică încorporată. Compilatorul ar trebui să valorifice un model local, ușor, nativ în Rust, de încorporare vectorială (precum un model MiniLM-L6 executat prin `candle` sau `ort` / ONNX Runtime) la compilare. Ar trebui să genereze încorporări vectoriale dense pentru fiecare paragraf al paginii și să producă un index vectorial compact. Widget-ul de căutare de pe partea de client, compilat în WASM, poate apoi să efectueze o căutare semantică offline reală direct în browser.

### 4. Cache determinist de traducere și inferență

Deoarece inferența LLM locală (de exemplu, prin Ollama sau Llama.cpp) este extrem de intensivă pentru CPU/GPU, traducerea sau generarea de metadate pentru mii de pagini la fiecare compilare este prohibitivă din punct de vedere computațional.

* **Capabilitate absentă:** Cache de inferență bazat pe hash-ul conținutului. Compilatorul trebuie să mențină un cache determinist al tuturor operațiilor LLM. Dacă hash-ul SHA-256 al conținutului unui fișier markdown și al parametrilor săi de traducere corespunde unei intrări din cache, compilatorul ar trebui să reutilizeze traducerea și metadatele din cache, ocolind inferența locală redundantă.

### 5. I/O asincron pe fișiere pentru scalare paralelă

Deși pipeline-ul de plugin-uri este paralelizat prin Rayon, scrierile sincrone standard pe disc blochează firele de execuție ale sistemului de operare gestionate de Rayon, creând un blocaj de I/O la scrierea a zeci de mii de pagini.

* **Capabilitate absentă:** I/O pe disc asincron, neblocant. Compilatorul ar trebui să decupleze sarcinile intensive pentru CPU (parsarea Markdown, minificarea) de scrierile legate de disc, folosind pool-uri de fire de I/O asincron sau legături Linux `io_uring` (prin `rio` sau `tokio`) pentru a scrie paginile compilate în paralel fără a bloca executorii CPU paraleli.

---

## Foaia de parcurs strategică spre 1.0

Următoarea foaie de parcurs integrează atât lipsurile rezolvate, cât și capabilitățile de nivel enterprise nou descoperite, într-un cadru de lansare structurat și cronologic.

### Faza 1: 0.0.42 (patch-ul de robustețe și corectitudine, 1 până la 2 săptămâni)

1. **Reconstruirea `MinifyPlugin`:** Integrarea `minify-html`, `oxc_minifier` și `lightningcss` pentru o minificare nativă, conștientă de sintaxă, a HTML, JS și CSS. Se asigură parcurgerea recursivă de către plugin a tuturor subdirectoarelor imbricate din `site_dir`.  
2. **Securizarea pipeline-ului AI:** Portarea `LlmPlugin` de la apelurile externe native `curl` la `ureq` (un client HTTP Rust ușor, sincron și sigur) pentru a asigura compatibilitatea între platforme și a elimina vulnerabilitățile de injecție în shell.  
3. **Finalizarea implementării AVIF:** Conectarea directă a `ravif` în pipeline-ul de active de imagine, activând codarea AVIF de înaltă performanță alături de WebP și PNG.  
4. **Automatizarea maparii HrefLang și multi-locale:** Detectarea automată a paginilor traduse paralele în compilările multilingve și injectarea de etichete standard, conforme cu Google, `<link rel="alternate" hreflang="..." />` în head-ul fiecărui fișier HTML compilat.  
5. **Suport JSON Feed 1.1:** Livrarea unui emițător dedicat JSON Feed 1.1 alături de canalele standard de sindicalizare RSS 2.0 și Atom 1.0.

### Faza 2: 0.1.0 (versiunea minoră de credibilitate și incrementalitate, 2 până la 3 luni)

1. **Popularea `DepGraph` și activarea `--incremental`:** Conectarea completă a `DepGraph` pentru a urmări dependențele șablon-la-pagină și markdown-la-pagină. Implementarea unui strat de invalidare a cache-ului și conectarea flag-ului CLI `--incremental`, țintind recompilări sub 200 ms pentru medii cu cache cald.  
2. **Rescriere AST în flux prin `lol_html`:** Înlocuirea rescrierii fragile de șiruri din `image_plugin.rs`, `search.rs` și a injecțiilor CSP cu un rescriitor HTML în flux, zero-copy, propulsat de `lol_html`.  
3. **Supraveghetor bazat pe evenimente și HMR de componente:** Portarea modulului de supraveghere de la sondare la crate-ul bazat pe evenimente `notify` și implementarea reîncărcării la cald doar pentru CSS și parțiale HTML pentru actualizări de browser sub 100 ms.  
4. **CLI cu comenzi unificate:** Rearhitectarea interfeței compilatorului pentru a suporta subcomenzi standard: `ssg dev`, `ssg build`, `ssg check` (audit de accesibilitate/SEO) și `ssg deploy`.  
5. **Cache determinist de inferență:** Implementarea unui strat de cache bazat pe hash-ul conținutului pentru toate sarcinile locale de traducere, rezumare și extracție de metadate cu LLM.

### Faza 3: 1.0.0 (versiunea majoră enterprise și de producție, 6 până la 12 luni)

1. **Sandbox-area plugin-urilor WASM zero-trust:** Încorporarea unui runtime WebAssembly (`wasmtime` sau `wasmer`) pentru a executa plugin-uri terțe într-un mediu complet izolat în sandbox, cu acces la sistemul de fișiere și la rețea bazat pe capabilități.  
2. **Căutare vectorială semantică locală (RAG local):** Încorporarea unui model local de încorporare nativ în Rust (prin `candle` sau `ort`) pentru a compila încorporări dense de paragrafe într-un index compact, activând o căutare semantică privată, pe partea de client.  
3. **Server Islands și țintă WASM edge:** Implementarea execuției componentelor `<ssg-island>` pe runtime-uri edge (precum Cloudflare Workers, Vercel Edge sau Netlify Edge) construite peste nucleul compilat `ssg-wasm`.  
4. **Motor de I/O paralel asincron:** Rearhitectarea modulului de scriere în sistemul de fișiere pentru a folosi pool-uri de fire de I/O asincron și legături `io_uring`, eliminând blocajele lucrătorilor CPU în timpul scrierilor paralele.  
5. **Proveniență de compilare SLSA v1.1 și conformitate SPDX 3.0:** Oferirea unei proveniențe de compilare SLSA Nivel 3 verificabile matematic și generarea de SBOM-uri conforme cu SPDX 3.0, satisfăcând pe deplin standardele moderne de securitate a lanțului de aprovizionare software.

---

## Matricea competitorilor (peisajul 2026)

Următoarea matrice compară `static-site-generator` (ținta v1.0) cu principalele motoare de publicare web ale anului 2026:

| Capabilitate | static-site-generator v1.0 | Hugo v0.155+ | Zola v0.19+ | Astro 5 | Eleventy 3 |
| ---- | ---- | ---- | ---- | ---- | ---- |
| **Limbaj / Runtime** | Rust (zero unsafe) | Go | Rust | JS (Node/V8) | JS (Node/V8) |
| **Poartă de compilare A11y** | Validare AST la compilare | Niciuna | Niciuna | Linter post-compilare | Linter post-compilare |
| **Întărire de securitate** | SRI SHA-384 și injecție CSP | Manuală | Manuală | Manuală | Manuală |
| **Siguranța lanțului de aprovizionare** | SLSA L3 \+ SPDX 3.0 \+ sandbox WASM | Minimă | Minimă | Arbore NPM greu | Arbore NPM greu |
| **Pipeline de conținut AI** | Privat, local-first (LLM local) | Niciunul | Niciunul | Doar API public | Doar API public |
| **Viteză incrementală** | \<200ms (cache cald) | \<100ms | \<150ms | \~1.5s | \~140ms |
| **Interactivitate dinamică** | Server Islands (ținte WASM) | Niciuna | Niciuna | Server Islands (JS) | Islands (JS) |
| **Motor de căutare** | Căutare semantică WASM locală | Șir simplu | Șir simplu | Pagefind (JS) | Pagefind (JS) |

---

## Poziționare la 1.0

La 1.0, poziționarea urmărită este cea a unui generator de site-uri statice construit ca infrastructură software securizată implicit: creație susținută de pipeline-uri AI local-first; compilarea a peste 100.000 de pagini printr-un pipeline paralel în flux; WCAG 2.2 AA și CSP și SRI stricte impuse ca porți de compilare; și insule dinamice izolate în sandbox, toate într-un singur binar Rust cu memorie sigură. Fiecare clauză din această afirmație corespunde unui element specific din foaia de parcurs de mai sus, nu unei aspirații de marketing.

---

## Integrarea reglementară și de conformitate

În sectoarele enterprise și financiare cu miză mare, software-ul este evaluat prin prisma conformității și a capitalului de risc. Foaia de parcurs arhitecturală a `static-site-generator` se aliniază direct cu mandatele majore de reglementare:

- **DORA Articolul 6 (managementul riscului TIC):** Calcularea și injectarea la compilare a hash-urilor SRI SHA-384 și a politicilor stricte de Content Security satisfac cerința de a proteja canalele de publicare digitală împotriva injecției în lanțul de aprovizionare, a defacement-ului web și a vectorilor de cross-site scripting (XSS).  
- **DORA Articolul 7 (reziliența sistemelor TIC):** Prin trecerea la active statice imuabile, verificate la compilare, instituțiile financiare elimină vulnerabilitățile de bază de date și de server de runtime, reducând multiplicatorul de risc operațional și diminuând rezervele de capital de risc necesare sub Basel III.  
- **Actul European privind Accesibilitatea (EAA) Directiva (UE) 2019/882:** Deplasarea auditului de accesibilitate la stânga, în pipeline-ul de compilare, ca poartă fermă a compilatorului, garantează 100% conformitate înainte de implementare, eliminând riscul de deteriorare a imaginii de marcă și de litigii civile sub EAA și ADA Titlul III.  
- **GDPR Articolul 25 (confidențialitate prin design):** Rularea pipeline-ului de traducere și metadate pe hardware local, izolat de rețea, ține ciornele proprietare, indicatorii financiari și datele personale în afara furnizorilor LLM din cloud public terț, susținând conformitatea cu principiile de suveranitate a datelor.

---

## Întrebări frecvente

**Ce livrează cu adevărat versiunea 0.0.41 astăzi, față de ce afirmă README-ul?**
Modelul de securitate și accesibilitate este real și impus în cod: `forbid(unsafe_code)` la nivel de întreg workspace, generarea SRI SHA-256/384, extracția CSP, versiuni semnate cu atestare Sigstore și un SBOM CycloneDX, plus o poartă WCAG 2.2 AA care oprește compilarea. Trei funcționalități documentate nu sunt funcționale în v0.0.41. `MinifyPlugin` este un colapsor de spații albe, nu un minificator conștient de sintaxă; `DepGraph` care ar propulsa recompilările incrementale este compilat, dar niciodată populat în codul de producție; iar codarea AVIF este un ciot al cărui `avif_variants` returnează un vector gol.

**Poarta de accesibilitate este o poartă reală de compilare sau un linter post-compilare?**
Este o poartă de compilare. Verificările WCAG 2.2 AA rulează în interiorul pipeline-ului de compilare printr-un parser axe-core la compilare acționat de Playwright, iar o pagină care eșuează oprește compilarea cu erori la numărul exact de linie, în loc să emită un avertisment ulterior. Aceasta este proprietatea de care are nevoie o obligație din Actul European privind Accesibilitatea: rezultatele neconforme nu pot ajunge la implementare.

**De ce contează apelarea externă a `curl` în plugin-ul LLM?**
Pipeline-ul LLM local (`src/plugins/llm.rs`) invocă binarul `curl` al gazdei pentru a ajunge la endpoint-urile locale. Aceasta cuplează compilarea de un executabil al gazdei, eșuează pe sistemele fără `curl` în PATH, introduce o suprafață de injecție în shell și se rupe în CI izolat de rețea. Portarea apelului către un client HTTP Rust precum `ureq` elimină dependența externă și vectorul de injecție, motiv pentru care este al doilea element din patch-ul 0.0.42.

**Care este cel mai important element de pe drumul spre 1.0?**
Popularea `DepGraph` și conectarea flag-ului `--incremental`. Recompilările incrementale reprezintă decalajul de credibilitate dintre motorul documentat și cel real, iar fiecare afirmație ulterioară despre compilări sub o secundă la peste 100.000 de pagini depinde de faptul că graful de dependențe urmărește muchiile șablon-la-pagină și markdown-la-pagină, în loc să rămână o infrastructură doar pentru teste.

## Referințe

- [Cloudflare, *lol-html: rescriitor HTML în flux cu latență redusă a rezultatelor*](https://github.com/cloudflare/lol-html "Cloudflare lol-html — rescriitor HTML în flux") ⧉. [Rescriitorul HTML în flux, zero-copy, propus pentru a înlocui manipularea fragilă de șiruri în faza 0.1.0.]
- [W3C, *Web Content Accessibility Guidelines (WCAG) 2.2*](https://www.w3.org/TR/WCAG22/ "W3C — Recomandarea WCAG 2.2") ⧉. [Criteriile de succes de Nivel AA impuse de poarta de accesibilitate la compilare.]
- [Uniunea Europeană, *Regulamentul (UE) 2022/2554 (DORA)*](https://eur-lex.europa.eu/eli/reg/2022/2554/oj "EUR-Lex — Actul privind reziliența operațională digitală") ⧉. [Articolele de management al riscului TIC și de reziliență cu care se aliniază postura de securitate.]
- [OpenSSF, *Supply-chain Levels for Software Artifacts (SLSA) v1.0*](https://slsa.dev/spec/v1.0/ "SLSA — specificația v1.0") ⧉. [Cadrul de proveniență de compilare țintit pentru atestarea verificabilă de Nivel 3 la 1.0.]
- [Armin Ronacher, *motorul de șabloane MiniJinja*](https://github.com/mitsuhiko/minijinja "MiniJinja — motor Jinja2 minimal pentru Rust") ⧉. [Motorul cu dependențe reduse care a înlocuit Tera și a subțiat arborele tranzitiv.]
- [CycloneDX, *specificația Software Bill of Materials v1.5*](https://cyclonedx.org/docs/1.5/ "CycloneDX — specificația SBOM v1.5") ⧉. [Formatul SBOM emis la fiecare compilare pentru auditul lanțului de aprovizionare.]
- [Uniunea Europeană, *Directiva (UE) 2019/882 (Actul European privind Accesibilitatea)*](https://eur-lex.europa.eu/eli/dir/2019/882/oj "EUR-Lex — Actul European privind Accesibilitatea") ⧉. [Obligația de accesibilitate pe care poarta WCAG la compilare este concepută să o satisfacă.]

*Ultima revizuire: iulie 2026. Analiza originală se bazează pe inspecția codului `static-site-generator` la v0.0.41; sursele sunt citate, nu reproduse. Numerele de versiune și starea funcționalităților se schimbă rapid, verificați în raport cu depozitul înainte de republicare. Licențiat sub CC-BY-4.0.*
