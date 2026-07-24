---
author: "contact@sebastienrousseau.com (Sebastien Rousseau)"
banner_alt: "Uno sfondo tecnico astratto che rappresenta la roadmap architetturale di un generatore di siti statici di livello enterprise."
banner_height: "1280"
banner_width: "1920"
banner: "https://cloudcdn.pro/stocks/images/gemini-background.webp"
cdn: "https://cloudcdn.pro"
charset: "UTF-8"
cname: "sebastienrousseau.com"
copyright: "© Copyright 2025 - 2026 - Sebastien Rousseau. All rights reserved."
date: "July 22, 2026"
description: "Analisi di uno static-site generator in Rust: sicurezza in compilazione, gate WCAG e IA locale, i gap della v0.0.41 e la roadmap enterprise verso la 1.0."
format-detection: "telephone=no"
hreflang: "it"
icon: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
id: "https://sebastienrousseau.com/it/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
image_alt: "Ritratto in bianco e nero di Sebastien Rousseau"
image_height: "162"
image_width: "162"
image: "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp"
keywords: "generatore di siti statici, Rust, forbid unsafe_code, WCAG 2.2 AA, Content Security Policy, Subresource Integrity, SLSA, CycloneDX SBOM, pipeline LLM locale, DORA, build incrementali, lol_html, sandbox plugin WASM, ricerca vettoriale semantica, MiniJinja, Ollama"
language: "it"
last_reviewed: "2026-07-22"
layout: "report"
locale: "it_IT"
logo_alt: "Logo di Sebastien Rousseau"
logo_height: "44"
logo_width: "44"
logo: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
menu: ""
measurementID: "G-169G4ET5HQ"
name: "Sebastien Rousseau"
permalink: "https://sebastienrousseau.com/it/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
rating: "general"
referrer: "no-referrer"
robots: "index, follow"
schema: "FAQPage, Article"
seo_title: "Static Site Generator: la strada verso la 1.0"
short_name: "sebastienrousseau"
subtitle: "Un audit architetturale e una roadmap per uno static-site generator in Rust concepito come infrastruttura sicura per impostazione predefinita: cosa la v0.0.41 offre davvero rispetto a quanto promette il README, cinque capacità enterprise mancanti e un percorso a fasi verso una 1.0 allineata a DORA ed EAA."
tags: "generatore di siti statici, Rust, sicurezza web, accessibilità, DORA, catena di fornitura, SLSA, IA locale, WCAG, compile-time, roadmap, enterprise"
theme-color: "0, 83, 191"
title: "SSG enterprise: analisi strategica e roadmap architetturale"
url: "https://sebastienrousseau.com/it/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap/rss.xml"
category: "Technology"
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.26)"
item_description: "Analisi di uno static-site generator in Rust: sicurezza in compilazione, gate WCAG e IA locale, i gap della v0.0.41 e la roadmap enterprise verso la 1.0."
item_guid: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap/rss.xml"
item_link: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap/rss.xml"
item_pub_date: "Wed, 22 Jul 2026 07:07:07 +0000"
item_title: "SSG enterprise: analisi strategica e roadmap architetturale"
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
apple-mobile-web-app-title: "SSG verso la 1.0"
apple-touch-fullscreen: "yes"
msapplication-navbutton-color: "0, 83, 191"
twitter_card: "summary_large_image"
twitter_creator: "@wwdseb"
twitter_description: "Gate WCAG in compilazione, SRI SHA-384, iniezione CSP e pipeline LLM locale distinguono questo motore Rust. Analisi dei gap della v0.0.41 verso la 1.0."
twitter_image: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
twitter_image_alt: "Logo di Sebastien Rousseau"
twitter_site: "@wwdseb"
twitter_title: "Static Site Generator: la strada verso la 1.0"
twitter_url: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
excerpt: "Gate WCAG in compilazione, SRI SHA-384, iniezione CSP e una pipeline LLM locale distinguono questo motore Rust: l'analisi dei gap e la strada verso la 1.0."
author_website: "https://sebastienrousseau.com"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "Grazie per la lettura!"
site_last_updated: "2026-07-22"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "Kaishi, Kaishi Builder, Kaishi CLI, Kaishi Templates, Kaishi Themes"
---

# Static Site Generator (SSG): analisi strategica di livello enterprise e roadmap architetturale

*Data della ricerca: 2026-06-22. Basato sull'ispezione del codice di `static-site-generator` alla v0.0.41 e sulla ricerca web del panorama SSG del 2026.*

**Per un editore regolamentato, un generatore di siti statici non è più uno strumento di design; è parte del perimetro di rischio operativo.** Il progetto open source in Rust [static-site-generator](https://github.com/sebastienrousseau/static-site-generator) nasce da questa premessa: sposta sicurezza, accessibilità, internazionalizzazione e pipeline di contenuti IA al momento della compilazione, così che un controllo fallito interrompa la compilazione anziché raggiungere la produzione. Questa analisi distingue ciò che la versione 0.0.41 offre davvero da ciò che la sua documentazione ancora si limita a promettere, individua cinque capacità enterprise di cui non dispone ancora e propone un percorso a fasi verso una release 1.0 allineata a DORA, allo European Accessibility Act e ai moderni standard della catena di fornitura.

<!-- lead-start -->
<aside class="post-lead" aria-label="Riepilogo dell'articolo">
<p class="post-lead-tldr"><strong>TL;DR.</strong> Il <code>static-site-generator</code> in Rust tratta la pubblicazione web come una pipeline software verificabile e sicura per impostazione predefinita: <code>forbid(unsafe_code)</code> esteso all'intero workspace, Subresource Integrity SHA-384, estrazione della Content Security Policy, un gate WCAG 2.2 AA in compilazione e una pipeline LLM locale. Un'ispezione del codice della v0.0.41 mostra che diverse funzionalità documentate restano aspirazionali, tra cui la minificazione nativa, le ricompilazioni incrementali e AVIF. Questa è l'analisi onesta dei gap e una roadmap a fasi verso una 1.0 di livello enterprise.</p>
<p class="post-lead-heading"><strong>Punti chiave</strong></p>
<ul class="post-lead-takeaways">
  <li><strong>Il modello di sicurezza e accessibilità è reale.</strong> SRI in compilazione, estrazione CSP, release firmate con attestazione Sigstore e SBOM CycloneDX, oltre a un gate WCAG 2.2 AA che interrompe la compilazione, sono implementati nel codice, non solo documentati.</li>
  <li><strong>Diverse funzionalità di punta non lo sono.</strong> Il minificatore si limita a comprimere gli spazi, il grafo delle dipendenze che alimenterebbe le build incrementali non viene mai popolato in produzione e la codifica AVIF è uno stub che restituisce un vettore vuoto.</li>
  <li><strong>Mancano cinque capacità enterprise.</strong> Il sandboxing dei plugin WASM, un riscrittore HTML in streaming e zero-copy, la ricerca semantica locale, la cache deterministica delle inferenze e l'I/O su file asincrono.</li>
  <li><strong>La roadmap è ordinata per rischio.</strong> Una patch di correttezza (0.0.42), una minor di credibilità e incrementalità (0.1.0), poi una major enterprise (1.0.0) che porta con sé la sandbox, la ricerca semantica e la provenance SLSA v1.1.</li>
</ul>
<p class="post-lead-related"><strong>Letture correlate:</strong> <a href="https://sebastienrousseau.com/2026-07-03-emerging-technology-risk-horizon-banks-2026">L'orizzonte di rischio delle tecnologie emergenti per le banche</a>, <a href="https://sebastienrousseau.com/2026-07-07-corporate-banking-api-standard-agentic-mcp-2026">Uno standard API per il corporate banking nell'MCP agentico</a>.</p>
</aside>
<!-- lead-end -->

> **Sintesi esecutiva**
>
> - **La pubblicazione è ora un perimetro di rischio operativo.** Ai sensi di DORA, dello European Accessibility Act e del GDPR, ogni asset pubblico è un potenziale punto di ingresso per compromissioni della catena di fornitura, defacement ed esposizione normativa. Un modello in compilazione restringe quel perimetro rifiutando l'output non conforme prima che venga pubblicato.
> - **I fattori distintivi del motore sono imposti dal compilatore, non aspirazioni documentate.** `forbid(unsafe_code)` esteso all'intero workspace, vero SRI SHA-256/384, estrazione automatica della CSP e un gate WCAG 2.2 AA in compilazione trasformano sicurezza e accessibilità da audit a posteriori in errori di compilazione bloccanti.
> - **La versione 0.0.41 presenta un divario tra documentazione e codice.** Minificazione nativa, ricompilazioni incrementali tramite grafo delle dipendenze e supporto AVIF sono descritti ma non funzionanti; l'articolo indica ogni gap rispetto all'esatta posizione nel sorgente.
> - **Il percorso verso la 1.0 è una sequenza, non una lista dei desideri.** Prima la robustezza (0.0.42), poi la correttezza incrementale (0.1.0), poi le capacità enterprise, sandboxing WASM, ricerca semantica locale e provenance SLSA verificabile, che un acquirente regolamentato richiede (1.0.0).

## Punti di forza attuali

Il codice di `static-site-generator` presenta diverse scelte ingegneristiche distintive che lo separano dai motori JavaScript e Go tradizionali:

- **Postura di sicurezza in compilazione:** `#![forbid(unsafe_code)]` esteso all'intero workspace fornisce garanzie di memory-safety in fase di compilazione. La pipeline di build genera veri hash Subresource Integrity (SRI) SHA-256/SHA-384 (`src/plugins/assets.rs`) ed esegue un'estrazione automatica della Content Security Policy (CSP) che rimuove script e stili unsafe-inline. Le release sono firmate, includono l'attestazione Sigstore e producono a ogni build un SBOM CycloneDX 1.5 (distinta base del software).  
- **Gate di accessibilità imposto dal compilatore:** i controlli Web Content Accessibility Guidelines (WCAG) 2.2 Livello AA vengono eseguiti all'interno della pipeline di compilazione tramite un parser axe-core in fase di build guidato da Playwright. L'accessibilità diventa un gate di compilazione bloccante anziché un audit successivo alla pubblicazione: se una pagina fallisce, la compilazione si interrompe con errori che indicano l'esatto numero di riga.  
- **Pipeline IA a sovranità del dato:** una pipeline di traduzione ed estrazione di metadati basata su LLM locali (tramite endpoint locali Ollama o llama.cpp) consente a un'istituzione di automatizzare la sintesi dei contenuti, la generazione di schemi JSON-LD e la traduzione multilingue senza inviare comunicazioni finanziarie pre-risultati o proprietà intellettuale sensibile a API IA di cloud pubblici.  
- **Compilazione parallelizzata:** le garanzie di memory-safety di Rust sono alla base di una pipeline HTML e asset parallelizzata e guidata da Rayon (`src/core/pipeline.rs`). La pipeline di plugin esegue trasformazioni fuse, con `SearchPlugin`, `SeoPlugin`, `CanonicalPlugin` e `JsonLdPlugin` che operano su `par_iter()`, così ogni pagina viene letta e scritta su disco una sola volta.  
- **Igiene della catena di fornitura e delle dipendenze:** la migrazione del motore di template da Tera a MiniJinja (`v0.0.37`) ha ridotto la dimensione del binario, rimosso dipendenze transitive come `rand` in fase di compilazione e prodotto un'impronta di dipendenze compatta che riduce l'esposizione della catena di fornitura del software.

---

## Gap e realtà operative

Nonostante questi punti di forza eccezionali, un'ispezione rigorosa del codice della v0.0.41 rivela diversi gap architetturali, funzionali e di developer experience tra le affermazioni della documentazione e il codice Rust effettivo:

### Gap architetturali

- **Compressione degli spazi vs. minificazione nativa:** benché il README prometta la «minificazione nativa di JS/CSS», il `MinifyPlugin` (`src/plugins/plugins.rs:96-116`) si comporta semplicemente come un ingenuo compressore di spazi. Si arresta sugli elementi `<pre>` e comprime le sequenze di spazi nell'HTML, ma non esegue una minificazione nativa di CSS o JS consapevole della sintassi. Inoltre elabora solo le pagine di primo livello e non attraversa ricorsivamente le sottocartelle (come `/blog/` o `/tags/`), lasciando non minificate le pagine più profonde.  
- **Infrastruttura incrementale inattiva:** il grafo di tracciamento delle dipendenze (`DepGraph` in `src/core/depgraph.rs`) viene compilato e caricato in `PluginContext.dep_graph`, ma non viene mai effettivamente popolato nel codice di produzione. Il metodo `add_dep()` viene richiamato solo nei test unitari, il che rende l'affermazione del README sulle «ricompilazioni incrementali tramite grafi delle dipendenze» al momento aspirazionale.  
- **Compilazione a lotti vs. compilazione in streaming:** il modulo `streaming::compile_batch` (`src/core/streaming.rs`) non esegue un vero streaming. Compila invece le pagine a lotti in una directory temporanea, esegue `staticdatagen::compile` da zero per ogni lotto e unisce gli output. Ne derivano un notevole overhead di I/O su disco e un parsing ridondante, con una deviazione da una vera architettura di streaming.  
- **Violazioni delle fasi del ciclo di vita dei plugin:** i plugin che generano nuove pagine HTML durante la build, come `TaxonomyPlugin`, `PaginationPlugin` e `I18nPlugin`, scrivono direttamente su disco in `after_compile` anziché usare il ciclo di vita `transform_html`. Di conseguenza, le pagine generate da questi plugin aggirano i plugin di post-elaborazione critici (come `CanonicalPlugin`, `JsonLdPlugin`, `RobotsPlugin` e `AccessibilityPlugin`) se questi ultimi erano stati registrati prima. Questo lascia le pagine di tag, categoria e paginazione prive di link canonici corretti, schemi JSON-LD o validazioni di accessibilità.  
- **Ricorso a `curl` esterno in `LlmPlugin`:** la pipeline di contenuti LLM locale (`src/plugins/llm.rs`) invoca direttamente il binario `curl` dell'host per interrogare gli endpoint locali. Ciò introduce gravi bug multipiattaforma (per esempio su host Windows privi di curl nel PATH), comporta un rischio di sicurezza (vettori di shell injection) e fallisce negli ambienti CI bloccati o isolati dalla rete.  
- **Manipolazione ingenua delle stringhe nella riscrittura HTML:** gli estrattori in `image_plugin.rs` e `search.rs` riscrivono le stringhe HTML usando fragili operazioni `str::find` e `str::rfind`. Questo approccio è altamente vulnerabile a tag HTML malformati, tag `<img>` all'interno di commenti, entità carattere nel testo alternativo o proprietà `srcset` preesistenti, con il rischio di produrre output corrotto.  
- **Supporto AVIF non implementato:** benché la codifica di immagini AVIF sia ampiamente documentata, l'implementazione in `image_plugin.rs` è uno stub in cui `avif_variants` restituisce semplicemente `Vec::new()`, lasciando la funzionalità non operativa.  
- **Watcher basato su polling:** il watcher del server di sviluppo locale (`src/server/watch.rs`) usa il polling anziché le API di eventi del filesystem, con un consumo eccessivo di CPU a riposo e una latenza di rilevamento delle modifiche inferiore al secondo.

### Gap funzionali e di DX

- **Nessun tracciamento delle dipendenze transitive:** il grafo delle dipendenze non è in grado di tracciare le dipendenze annidate (per esempio, modifiche a un sotto-template che influisce su un layout che influisce su una pagina), come verificato dal test unitario `transitive_not_tracked`.  
- **Nessun flag CLI per la compilazione incrementale:** non esiste alcun flag CLI `--incremental` collegato al compilatore di esecuzione, il che impedisce agli sviluppatori di usare build memorizzate nella cache.  
- **L'HMR è limitato al CSS:** l'Hot Module Replacement (HMR, sostituzione a caldo dei moduli) supporta solo il CSS; qualsiasi modifica a file HTML, layout o markdown provoca un ricaricamento completo della pagina, riducendo la velocità di sviluppo.  
- **Carenza di sottocomandi:** gli sviluppatori devono passare manualmente flag prolissi (`ssg -s public -w`) perché sottocomandi standard come `ssg dev`, `ssg build`, `ssg check` e `ssg lint` non esistono.

---

## Gap architetturali che ci mancano (nuove scoperte)

Oltre ai gap della v0.0.41, valutare il progetto rispetto a un profilo di rischio di livello finanziario fa emergere diverse capacità che non offre ancora ma che un acquirente enterprise richiederebbe:

### 1. Sandboxing dei plugin WebAssembly (estensione zero-trust)

Sebbene il binario del compilatore sia scritto in Rust sicuro, consentire a plugin arbitrari di terze parti di eseguirsi in modo nativo sui sistemi host introduce una grave vulnerabilità della catena di fornitura. Un plugin di terze parti compromesso potrebbe facilmente accedere al filesystem dell'host, leggere file Markdown proprietari o esfiltrare credenziali private.

* **Capacità mancante:** un ambiente di esecuzione sandbox. Per ottenere una compilazione zero-trust, il compilatore dovrebbe eseguire i plugin di terze parti all'interno di un runtime WebAssembly incorporato (come `wasmtime`). I plugin dovrebbero interagire con l'host esclusivamente tramite una WebAssembly System Interface (WASI) ristretta, limitando il loro accesso strettamente alla pagina in corso di trasformazione.

### 2. Parsing HTML zero-copy tramite AST in streaming (`lol_html`)

Migrare il livello di parsing HTML a una libreria DOM completamente in memoria (come Kuchiki o html5ever) introduce un notevole overhead di memoria e pause di elaborazione nella gestione di siti con oltre 100.000 pagine.

* **Capacità mancante:** un riscrittore HTML in streaming e zero-copy. L'uso di `lol_html` di Cloudflare (riscrittore HTML a bassa latenza di output) consente al compilatore di analizzare, ispezionare e modificare gli elementi HTML in un unico passaggio in streaming con un'allocazione di memoria pressoché nulla, in linea con l'obiettivo di build inferiori al secondo del compilatore in streaming parallelo.

### 3. Ricerca vettoriale semantica locale (RAG locale)

L'attuale indice di ricerca (`SearchPlugin`) genera un pesante indice JSON piatto che esegue semplici confronti di stringhe lato client, privo di supporto per ricerca fuzzy, stemming o query semantiche. Pagefind rappresenta un miglioramento, ma dipende comunque dal download di un indice di grandi dimensioni.

* **Capacità mancante:** ricerca semantica incorporata. Il compilatore dovrebbe sfruttare un modello di embedding vettoriale locale, leggero e nativo in Rust (come un modello MiniLM-L6 eseguito tramite `candle` o `ort` / ONNX Runtime) in fase di build. Dovrebbe generare embedding vettoriali densi per ogni paragrafo di pagina e produrre un indice vettoriale compatto. Il widget di ricerca lato client, compilato in WASM, può quindi eseguire una vera ricerca semantica offline direttamente nel browser.

### 4. Traduzione deterministica e cache delle inferenze

Poiché l'inferenza LLM locale (per esempio tramite Ollama o Llama.cpp) è fortemente intensiva per CPU/GPU, tradurre o generare metadati per migliaia di pagine a ogni build è computazionalmente proibitivo.

* **Capacità mancante:** cache delle inferenze basata sull'hash del contenuto. Il compilatore deve mantenere una cache deterministica di tutte le operazioni LLM. Se l'hash SHA-256 del contenuto di un file markdown e dei suoi parametri di traduzione corrisponde a una voce della cache, il compilatore dovrebbe riutilizzare la traduzione e i metadati memorizzati, evitando inferenze locali ridondanti.

### 5. I/O su file asincrono per la scalabilità parallela

Sebbene la pipeline di plugin sia parallelizzata tramite Rayon, le scritture su disco sincrone standard bloccano i thread del sistema operativo di Rayon, creando un collo di bottiglia di I/O nella scrittura di decine di migliaia di pagine.

* **Capacità mancante:** I/O su disco asincrono e non bloccante. Il compilatore dovrebbe disaccoppiare i task intensivi per la CPU (parsing del Markdown, minificazione) dalle scritture vincolate al disco, usando pool di thread di I/O asincrono o i binding Linux `io_uring` (tramite `rio` o `tokio`) per scrivere le pagine compilate in parallelo senza bloccare gli esecutori CPU paralleli.

---

## La roadmap strategica verso la 1.0

La roadmap seguente integra sia i gap risolti sia le capacità di livello enterprise appena individuate in un quadro di release strutturato e cronologico.

### Fase 1: 0.0.42 (la patch di robustezza e correttezza, da 1 a 2 settimane)

1. **Ricostruire `MinifyPlugin`:** integrazione di `minify-html`, `oxc_minifier` e `lightningcss` per una minificazione nativa di HTML, JS e CSS consapevole della sintassi. Garantire che il plugin attraversi ricorsivamente tutte le directory annidate sotto `site_dir`.  
2. **Mettere in sicurezza la pipeline IA:** migrare `LlmPlugin` dalle chiamate esterne a `curl` native a `ureq` (un client HTTP Rust leggero, sincrono e sicuro) per garantire la compatibilità multipiattaforma ed eliminare le vulnerabilità di shell injection.  
3. **Completare l'implementazione AVIF:** collegare `ravif` direttamente alla pipeline degli asset immagine, abilitando una codifica AVIF ad alte prestazioni accanto a WebP e PNG.  
4. **Automatizzare la mappatura di HrefLang e multi-locale:** rilevare automaticamente le pagine tradotte parallele nelle build multilingue e iniettare tag standard conformi a Google `<link rel="alternate" hreflang="..." />` nell'head di ogni file HTML compilato.  
5. **Supporto a JSON Feed 1.1:** rilasciare un emettitore JSON Feed 1.1 dedicato accanto ai canali di syndication standard RSS 2.0 e Atom 1.0.

### Fase 2: 0.1.0 (la minor di credibilità e incrementalità, da 2 a 3 mesi)

1. **Popolare `DepGraph` e abilitare `--incremental`:** collegare completamente `DepGraph` per tracciare le dipendenze da template a pagina e da markdown a pagina. Implementare un livello di invalidazione della cache e collegare il flag CLI `--incremental`, puntando a ricompilazioni inferiori a 200 ms per ambienti con cache calda.  
2. **Riscrittura dell'AST in streaming tramite `lol_html`:** sostituire la fragile riscrittura di stringhe in `image_plugin.rs`, `search.rs` e nelle iniezioni CSP con un riscrittore HTML in streaming e zero-copy basato su `lol_html`.  
3. **Watcher basato su eventi e HMR dei componenti:** migrare il modulo di watch dal polling al crate `notify` basato su eventi e implementare il ricaricamento a caldo solo-CSS e HTML-parziale per aggiornamenti del browser inferiori a 100 ms.  
4. **CLI a comando unificato:** riprogettare l'interfaccia del compilatore per supportare i sottocomandi standard: `ssg dev`, `ssg build`, `ssg check` (audit di accessibilità/SEO) e `ssg deploy`.  
5. **Cache deterministica delle inferenze:** implementare un livello di cache basato sull'hash del contenuto per tutti i task locali di traduzione, sintesi ed estrazione di metadati tramite LLM.

### Fase 3: 1.0.0 (la major enterprise e di produzione, da 6 a 12 mesi)

1. **Sandboxing zero-trust dei plugin WASM:** incorporare un runtime WebAssembly (`wasmtime` o `wasmer`) per eseguire i plugin di terze parti in un ambiente completamente sandbox con accesso a filesystem e rete basato su capability.  
2. **Ricerca vettoriale semantica locale (RAG locale):** incorporare un modello di embedding locale nativo in Rust (tramite `candle` o `ort`) per compilare embedding densi dei paragrafi in un indice compatto, abilitando una ricerca semantica privata lato client.  
3. **Server Islands e target edge WASM:** implementare l'esecuzione dei componenti `<ssg-island>` su runtime edge (come Cloudflare Workers, Vercel Edge o Netlify Edge) costruiti sul core compilato `ssg-wasm`.  
4. **Motore di I/O parallelo asincrono:** riprogettare il modulo di scrittura del filesystem per usare pool di thread di I/O asincrono e binding `io_uring`, eliminando i blocchi dei worker CPU durante le scritture parallele.  
5. **Provenance di build SLSA v1.1 e conformità SPDX 3.0:** fornire una provenance di build SLSA Livello 3 matematicamente verificabile e generare SBOM conformi a SPDX 3.0, soddisfacendo pienamente i moderni standard di sicurezza della catena di fornitura del software.

---

## Matrice competitiva (panorama 2026)

La matrice seguente confronta `static-site-generator` (target v1.0) con i principali motori di pubblicazione web del 2026:

| Capacità | static-site-generator v1.0 | Hugo v0.155+ | Zola v0.19+ | Astro 5 | Eleventy 3 |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Linguaggio / Runtime** | Rust (zero unsafe) | Go | Rust | JS (Node/V8) | JS (Node/V8) |
| **Gate di accessibilità in build** | Validazione AST in compilazione | Nessuno | Nessuno | Linter post-build | Linter post-build |
| **Hardening di sicurezza** | SRI SHA-384 e iniezione CSP | Manuale | Manuale | Manuale | Manuale |
| **Sicurezza della catena di fornitura** | SLSA L3 \+ SPDX 3.0 \+ sandbox WASM | Minima | Minima | Albero NPM pesante | Albero NPM pesante |
| **Pipeline di contenuti IA** | Privata, local-first (LLM locale) | Nessuna | Nessuna | Solo API pubbliche | Solo API pubbliche |
| **Velocità incrementale** | \<200 ms (cache calda) | \<100 ms | \<150 ms | \~1,5 s | \~140 ms |
| **Interattività dinamica** | Server Islands (target WASM) | Nessuna | Nessuna | Server Islands (JS) | Islands (JS) |
| **Motore di ricerca** | Ricerca semantica WASM locale | Stringa semplice | Stringa semplice | Pagefind (JS) | Pagefind (JS) |

---

## Posizionamento alla 1.0

Alla 1.0, il posizionamento previsto è un generatore di siti statici progettato come infrastruttura software sicura per impostazione predefinita: authoring supportato da pipeline IA local-first; compilazione di oltre 100.000 pagine attraverso una pipeline di streaming parallelo; WCAG 2.2 AA e rigorose CSP e SRI imposte come gate di compilazione; e dynamic island in sandbox, il tutto entro un singolo binario Rust memory-safe. Ogni clausola di questa affermazione corrisponde a un elemento specifico della roadmap sopra riportata anziché a un'aspirazione di marketing.

---

## Integrazione normativa e di conformità

Nei settori enterprise e finanziari ad alto rischio, il software viene valutato attraverso la lente della conformità e del capitale di rischio. La roadmap architetturale di `static-site-generator` si allinea direttamente ai principali mandati normativi:

- **DORA Articolo 6 (gestione del rischio ICT):** il calcolo e l'iniezione in compilazione degli hash SRI SHA-384 e di rigorose Content Security Policy soddisfano il requisito di proteggere i canali di pubblicazione digitale da iniezioni nella catena di fornitura, defacement web e vettori di cross-site scripting (XSS).  
- **DORA Articolo 7 (resilienza dei sistemi ICT):** passando ad asset statici immutabili e verificati in compilazione, le istituzioni finanziarie eliminano le vulnerabilità dei database e dei server a runtime, abbassando il moltiplicatore di rischio operativo e riducendo le riserve di capitale di rischio richieste da Basilea III.  
- **European Accessibility Act (EAA), Direttiva (UE) 2019/882:** spostare l'audit di accessibilità a monte, nella pipeline di compilazione come gate bloccante del compilatore, garantisce una conformità del 100% prima del deployment, eliminando il rischio di danno reputazionale e contenzioso civile ai sensi dell'EAA e del Titolo III dell'ADA.  
- **GDPR Articolo 25 (privacy by design):** eseguire la pipeline di traduzione e metadati su hardware locale e isolato dalla rete mantiene bozze proprietarie, metriche finanziarie e dati personali al di fuori dei provider LLM di cloud pubblici di terze parti, favorendo la conformità ai principi di sovranità del dato.

---

## Domande frequenti

**Cosa offre davvero oggi la versione 0.0.41, rispetto a quanto afferma il README?**
Il modello di sicurezza e accessibilità è reale e imposto nel codice: `forbid(unsafe_code)` esteso all'intero workspace, generazione di SRI SHA-256/384, estrazione CSP, release firmate con attestazione Sigstore e un SBOM CycloneDX, e un gate WCAG 2.2 AA che interrompe la compilazione. Tre funzionalità documentate non sono operative nella v0.0.41. Il `MinifyPlugin` è un compressore di spazi anziché un minificatore consapevole della sintassi; il `DepGraph` che alimenterebbe le ricompilazioni incrementali viene compilato ma mai popolato nel codice di produzione; e la codifica AVIF è uno stub il cui `avif_variants` restituisce un vettore vuoto.

**Il gate di accessibilità è un vero gate del compilatore o un linter post-build?**
È un gate di compilazione. I controlli WCAG 2.2 AA vengono eseguiti all'interno della pipeline di compilazione tramite un parser axe-core in fase di build guidato da Playwright, e una pagina non conforme interrompe la compilazione con errori che indicano l'esatto numero di riga anziché emettere un avviso a posteriori. È la proprietà di cui necessita un obbligo dello European Accessibility Act: l'output non conforme non può raggiungere il deployment.

**Perché il ricorso a `curl` esterno nel plugin LLM è rilevante?**
La pipeline LLM locale (`src/plugins/llm.rs`) invoca il binario `curl` dell'host per raggiungere gli endpoint locali. Ciò lega la build a un eseguibile dell'host, fallisce sui sistemi privi di `curl` nel PATH, introduce una superficie di shell injection e si rompe nella CI isolata dalla rete. Migrare la chiamata a un client HTTP Rust come `ureq` rimuove la dipendenza esterna e il vettore di iniezione, ed è per questo che rappresenta il secondo elemento della patch 0.0.42.

**Qual è l'elemento più importante in assoluto sulla strada verso la 1.0?**
Popolare il `DepGraph` e collegare il flag `--incremental`. Le ricompilazioni incrementali sono il divario di credibilità tra il motore documentato e quello reale, e ogni affermazione a valle sulle build inferiori al secondo con oltre 100.000 pagine dipende dal fatto che il grafo delle dipendenze tracci gli archi da template a pagina e da markdown a pagina anziché restare un'infrastruttura solo per i test.

## Riferimenti

- [Cloudflare, *lol-html: riscrittore HTML in streaming a bassa latenza di output*](https://github.com/cloudflare/lol-html "Cloudflare lol-html, riscrittore HTML in streaming") ⧉. [Il riscrittore HTML in streaming e zero-copy proposto per sostituire la fragile manipolazione di stringhe nella fase 0.1.0.]
- [W3C, *Web Content Accessibility Guidelines (WCAG) 2.2*](https://www.w3.org/TR/WCAG22/ "W3C, Raccomandazione WCAG 2.2") ⧉. [I criteri di successo di Livello AA imposti dal gate di accessibilità in compilazione.]
- [Unione europea, *Regolamento (UE) 2022/2554 (DORA)*](https://eur-lex.europa.eu/eli/reg/2022/2554/oj "EUR-Lex, Digital Operational Resilience Act") ⧉. [Gli articoli su gestione del rischio ICT e resilienza a cui la postura di sicurezza fa riferimento.]
- [OpenSSF, *Supply-chain Levels for Software Artifacts (SLSA) v1.0*](https://slsa.dev/spec/v1.0/ "SLSA, specifica v1.0") ⧉. [Il framework di provenance di build previsto per l'attestazione verificabile di Livello 3 alla 1.0.]
- [Armin Ronacher, *MiniJinja, motore di template*](https://github.com/mitsuhiko/minijinja "MiniJinja, motore Jinja2 minimale per Rust") ⧉. [Il motore a basso impatto di dipendenze che ha sostituito Tera e ridotto l'albero transitivo.]
- [CycloneDX, *Specifica Software Bill of Materials v1.5*](https://cyclonedx.org/docs/1.5/ "CycloneDX, specifica SBOM v1.5") ⧉. [Il formato SBOM emesso a ogni build per l'audit della catena di fornitura.]
- [Unione europea, *Direttiva (UE) 2019/882 (European Accessibility Act)*](https://eur-lex.europa.eu/eli/dir/2019/882/oj "EUR-Lex, European Accessibility Act") ⧉. [L'obbligo di accessibilità che il gate WCAG in compilazione è progettato per soddisfare.]

*Ultima revisione luglio 2026. Analisi originale basata sull'ispezione del codice di `static-site-generator` alla v0.0.41; le fonti sono citate, non riprodotte. I numeri di versione e lo stato delle funzionalità cambiano rapidamente: verificare rispetto al repository prima di ripubblicare. Distribuito con licenza CC-BY-4.0.*
