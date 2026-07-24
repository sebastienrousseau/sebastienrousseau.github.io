---
author: "contact@sebastienrousseau.com (Sebastien Rousseau)"
banner_alt: "Abstraktní technické pozadí představující architektonický plán generátoru statických webů podnikové úrovně."
banner_height: "1280"
banner_width: "1920"
banner: "https://cloudcdn.pro/stocks/images/gemini-background.webp"
cdn: "https://cloudcdn.pro"
charset: "UTF-8"
cname: "sebastienrousseau.com"
copyright: "© Copyright 2025 - 2026 - Sebastien Rousseau. All rights reserved."
date: "July 22, 2026"
description: "Hloubková analýza generátoru statických webů v Rustu: bezpečnost při kompilaci, brány WCAG, lokální AI, mezery ve verzi 0.0.41 a podnikový plán k verzi 1.0."
format-detection: "telephone=no"
hreflang: "cs"
icon: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
id: "https://sebastienrousseau.com/cs/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
image_alt: "Černobílý portrét Sebastiena Rousseaua"
image_height: "162"
image_width: "162"
image: "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp"
keywords: "generátor statických webů, Rust, forbid unsafe_code, WCAG 2.2 AA, Content Security Policy, Subresource Integrity, SLSA, CycloneDX SBOM, lokální LLM pipeline, DORA, inkrementální sestavení, lol_html, sandbox pro WASM pluginy, sémantické vektorové vyhledávání, MiniJinja, Ollama"
language: "cs"
last_reviewed: "2026-07-22"
layout: "report"
locale: "cs_CZ"
logo_alt: "Logo Sebastiena Rousseaua"
logo_height: "44"
logo_width: "44"
logo: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
menu: ""
measurementID: "G-169G4ET5HQ"
name: "Sebastien Rousseau"
permalink: "https://sebastienrousseau.com/cs/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
rating: "general"
referrer: "no-referrer"
robots: "index, follow"
schema: "FAQPage, Article"
seo_title: "Generátor statických webů: cesta k verzi 1.0"
short_name: "sebastienrousseau"
subtitle: "Architektonický audit a plán generátoru statických webů v Rustu, postaveného jako bezpečná infrastruktura ve výchozím nastavení: co verze 0.0.41 skutečně přináší oproti slibům README, pět chybějících podnikových schopností a fázovaná cesta k verzi 1.0 v souladu s DORA a EAA."
tags: "generátor statických webů, Rust, webová bezpečnost, přístupnost, DORA, dodavatelský řetězec, SLSA, lokální AI, WCAG, kompilace, plán vývoje, enterprise"
theme-color: "0, 83, 191"
title: "Generátor statických webů (SSG): strategická analýza a plán do verze 1.0"
url: "https://sebastienrousseau.com/cs/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap/rss.xml"
category: "Technology"
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.26)"
item_description: "Hloubková analýza generátoru statických webů v Rustu: bezpečnost při kompilaci, brány WCAG, lokální AI, mezery ve verzi 0.0.41 a podnikový plán k verzi 1.0."
item_guid: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap/rss.xml"
item_link: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap/rss.xml"
item_pub_date: "Wed, 22 Jul 2026 07:07:07 +0000"
item_title: "Generátor statických webů (SSG): strategická analýza a plán do verze 1.0"
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
apple-mobile-web-app-title: "SSG: cesta k 1.0"
apple-touch-fullscreen: "yes"
msapplication-navbutton-color: "0, 83, 191"
twitter_card: "summary_large_image"
twitter_creator: "@wwdseb"
twitter_description: "Brány WCAG při kompilaci, SHA-384 SRI, vkládání CSP a lokální LLM odlišují tento engine v Rustu. Poctivá analýza mezer verze 0.0.41 a cesta k podnikové verzi 1.0."
twitter_image: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
twitter_image_alt: "Logo Sebastiena Rousseaua"
twitter_site: "@wwdseb"
twitter_title: "Generátor statických webů: cesta k verzi 1.0"
twitter_url: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
excerpt: "Brány WCAG při kompilaci, SHA-384 SRI, vkládání CSP a lokální LLM odlišují tento engine v Rustu. Inkrementální sestavení, nativní minifikace a AVIF ale zatím chybí."
author_website: "https://sebastienrousseau.com"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "Děkujeme za přečtení!"
site_last_updated: "2026-07-22"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "Kaishi, Kaishi Builder, Kaishi CLI, Kaishi Templates, Kaishi Themes"
---

# Generátor statických webů (SSG): strategická analýza a plán do verze 1.0

*Datum výzkumu: 2026-06-22. Vychází z inspekce kódové báze `static-site-generator` ve verzi 0.0.41 a z webového výzkumu prostředí generátorů statických webů v roce 2026.*

**Pro regulovaného vydavatele už generátor statických webů není nástrojem pro návrh; je součástí perimetru provozního rizika.** Open-source projekt v Rustu [static-site-generator](https://github.com/sebastienrousseau/static-site-generator) je na tomto předpokladu postaven: přesouvá bezpečnost, přístupnost, internacionalizaci a AI pipeline pro obsah do fáze kompilace, takže selhaná kontrola zastaví sestavení, místo aby se dostala do produkce. Tato analýza odděluje to, co verze 0.0.41 skutečně přináší, od toho, co její dokumentace zatím jen slibuje, popisuje pět podnikových schopností, které dosud nemá, a navrhuje fázovanou cestu k vydání verze 1.0 v souladu s DORA, evropským aktem o přístupnosti a moderními standardy dodavatelského řetězce.

<!-- lead-start -->
<aside class="post-lead" aria-label="Shrnutí článku">
<p class="post-lead-tldr"><strong>Ve zkratce.</strong> Rustový <code>static-site-generator</code> pojímá webové publikování jako auditovatelnou softwarovou pipeline bezpečnou ve výchozím nastavení: <code>forbid(unsafe_code)</code> napříč celým workspace, Subresource Integrity se SHA-384, extrakci Content Security Policy, bránu WCAG 2.2 AA při kompilaci a lokální LLM pipeline. Inspekce kódu verze 0.0.41 ukazuje, že několik dokumentovaných funkcí je zatím jen ambicí, mezi nimi nativní minifikace, inkrementální sestavení a AVIF. Toto je poctivá analýza mezer a fázovaný plán k podnikové verzi 1.0.</p>
<p class="post-lead-heading"><strong>Klíčové body</strong></p>
<ul class="post-lead-takeaways">
  <li><strong>Model bezpečnosti a přístupnosti je skutečný.</strong> SRI při kompilaci, extrakce CSP, podepsaná vydání s atestací Sigstore a SBOM ve formátu CycloneDX plus brána WCAG 2.2 AA zastavující sestavení jsou implementovány v kódu, nejen zdokumentovány.</li>
  <li><strong>Několik hlavních funkcí nikoli.</strong> Minifikátor je jen slučovač bílých znaků, graf závislostí, který by řídil inkrementální sestavení, se v produkci nikdy neplní a kódování AVIF je zástupný kód vracející prázdný vektor.</li>
  <li><strong>Chybí pět podnikových schopností.</strong> Sandbox pro WASM pluginy, streamovaný HTML přepisovač bez kopírování, lokální sémantické vyhledávání, deterministické cachování inference a asynchronní souborové I/O.</li>
  <li><strong>Plán je seřazen podle rizika.</strong> Oprava korektnosti (0.0.42), minorní vydání pro důvěryhodnost a inkrementální sestavení (0.1.0) a poté podniková major verze (1.0.0) nesoucí sandbox, sémantické vyhledávání a proveniences SLSA v1.1.</li>
</ul>
<p class="post-lead-related"><strong>Související četba:</strong> <a href="https://sebastienrousseau.com/2026-07-03-emerging-technology-risk-horizon-banks-2026">Horizont rizik nově vznikajících technologií pro banky</a>, <a href="https://sebastienrousseau.com/2026-07-07-corporate-banking-api-standard-agentic-mcp-2026">Standard API pro korporátní bankovnictví pro agentní MCP</a>.</p>
</aside>
<!-- lead-end -->

> **Shrnutí pro vedení**
>
> - **Publikování je nyní perimetrem provozního rizika.** Podle DORA, evropského aktu o přístupnosti a GDPR je každý veřejně dostupný aktivum potenciálním vstupním bodem pro kompromitaci dodavatelského řetězce, defacement a regulatorní vystavení. Model při kompilaci tento perimetr zužuje tím, že odmítá nevyhovující výstup dříve, než se vydá.
> - **Odlišujícími prvky enginu jsou kontroly vynucené kompilátorem, nikoli zdokumentované ambice.** `forbid(unsafe_code)` napříč celým workspace, skutečné SRI se SHA-256/384, automatická extrakce CSP a brána WCAG 2.2 AA při sestavení mění bezpečnost a přístupnost z dodatečných auditů na tvrdá selhání sestavení.
> - **Verze 0.0.41 má mezeru mezi dokumentací a kódem.** Nativní minifikace, inkrementální sestavení pomocí grafu závislostí a podpora AVIF jsou popsány, ale nefunkční; článek pojmenovává každou mezeru proti přesnému místu ve zdrojovém kódu.
> - **Cesta k 1.0 je posloupnost, ne seznam přání.** Nejprve odolnost (0.0.42), poté inkrementální korektnost (0.1.0) a nakonec podnikové schopnosti, které regulovaný kupující vyžaduje, sandbox WASM, lokální sémantické vyhledávání a ověřitelná proveniences SLSA (1.0.0).

## Současné silné stránky

Kódová báze `static-site-generator` vykazuje několik osobitých inženýrských rozhodnutí, která ji odlišují od starších enginů v JavaScriptu a Go:

- **Bezpečnostní postoj při kompilaci:** `#![forbid(unsafe_code)]` napříč celým workspace poskytuje záruky paměťové bezpečnosti při kompilaci. Pipeline sestavení generuje skutečné hashe Subresource Integrity (SRI) se SHA-256/SHA-384 (`src/plugins/assets.rs`) a provádí automatickou extrakci Content Security Policy (CSP), která odstraňuje nebezpečné inline skripty a styly. Vydání jsou podepsaná, nesou atestaci Sigstore a při každém sestavení vytvářejí SBOM ve formátu CycloneDX 1.5.  
- **Brána přístupnosti vynucená kompilátorem:** Kontroly Web Content Accessibility Guidelines (WCAG) 2.2 na úrovni AA běží uvnitř kompilační pipeline prostřednictvím parseru axe-core při sestavení, řízeného nástrojem Playwright. Přístupnost se stává tvrdou bránou sestavení, nikoli auditem po publikaci: pokud stránka neprojde, kompilace se zastaví s chybami uvádějícími přesná čísla řádků.  
- **AI pipeline se suverenitou nad daty:** Lokální LLM pipeline pro překlad a extrakci metadat (prostřednictvím lokálních endpointů Ollama nebo llama.cpp) umožňuje instituci automatizovat sumarizaci obsahu, generování schémat JSON-LD a vícejazyčný překlad, aniž by odesílala předběžná zveřejnění hospodářských výsledků nebo citlivé duševní vlastnictví do veřejných cloudových AI API.  
- **Paralelizovaná kompilace:** Záruky paměťové bezpečnosti Rustu podpírají paralelizovanou HTML a asset pipeline poháněnou knihovnou Rayon (`src/core/pipeline.rs`). Plugin pipeline provádí spojené transformace, přičemž `SearchPlugin`, `SeoPlugin`, `CanonicalPlugin` a `JsonLdPlugin` operují nad `par_iter()`, takže každá stránka se z disku načte a na disk zapíše jen jednou.  
- **Hygiena dodavatelského řetězce a závislostí:** Migrace šablonovacího enginu z Tery na MiniJinja (`v0.0.37`) snížila velikost binárního souboru, odstranila při kompilaci tranzitivní závislosti jako `rand` a vytvořila kompaktní stopu závislostí, která snižuje vystavení softwarovému dodavatelskému řetězci.

---

## Mezery a realita nasazení

Navzdory těmto výjimečným silným stránkám odhaluje důkladná inspekce kódové báze verze 0.0.41 několik architektonických a funkčních mezer a mezer ve vývojářské zkušenosti mezi tvrzeními v dokumentaci a skutečným kódem v Rustu:

### Architektonické mezery

- **Slučování bílých znaků vs. nativní minifikace:** Ačkoli README slibuje „nativní minifikaci JS/CSS", `MinifyPlugin` (`src/plugins/plugins.rs:96-116`) funguje pouze jako naivní slučovač bílých znaků. U prvků `<pre>` se zkracuje a v HTML slučuje řetězce bílých znaků, ale neprovádí syntakticky uvědomělou nativní minifikaci CSS ani JS. Navíc zpracovává pouze stránky nejvyšší úrovně a nerekurzivně neprochází podadresáře (například `/blog/` nebo `/tags/`), takže hluboko uložené stránky zůstávají neminifikované.  
- **Mrtvá infrastruktura pro inkrementální sestavení:** Graf sledování závislostí (`DepGraph` v `src/core/depgraph.rs`) se kompiluje a načítá do `PluginContext.dep_graph`, ale v produkčním kódu se ve skutečnosti nikdy neplní. Metoda `add_dep()` se volá pouze v jednotkových testech, takže tvrzení README o „inkrementálním sestavení pomocí grafů závislostí" je zatím pouhou ambicí.  
- **Dávková kompilace vs. streamovaná kompilace:** Modul `streaming::compile_batch` (`src/core/streaming.rs`) ve skutečnosti nestreamuje. Místo toho kompiluje stránky po dávkách do dočasného adresáře, spouští `staticdatagen::compile` od začátku pro každou dávku a slučuje výstupy. To vede k výrazné režii diskového I/O a nadbytečnému parsování, což se odchyluje od skutečné streamovací architektury.  
- **Porušení fází životního cyklu pluginů:** Pluginy, které během sestavení generují nové HTML stránky, jako `TaxonomyPlugin`, `PaginationPlugin` a `I18nPlugin`, zapisují přímo na disk ve fázi `after_compile`, místo aby využívaly životní cyklus `transform_html`. V důsledku toho stránky generované těmito pluginy obcházejí klíčové post-processingové pluginy (jako `CanonicalPlugin`, `JsonLdPlugin`, `RobotsPlugin` a `AccessibilityPlugin`), pokud byly tyto pluginy zaregistrovány dříve. To ponechává stránky se štítky, kategoriemi a stránkováním bez správných kanonických odkazů, schémat JSON-LD nebo ověření přístupnosti.  
- **Volání `curl` přes shell v `LlmPlugin`:** Lokální LLM pipeline pro obsah (`src/plugins/llm.rs`) volá přes shell přímo binárku `curl` na hostiteli, aby se dotázala lokálních endpointů. To zavádí závažné chyby napříč platformami (např. na hostitelích s Windows bez `curl` v PATH), představuje bezpečnostní riziko (vektory shell injection) a selhává v uzamčených nebo síťově izolovaných prostředích CI.  
- **Naivní manipulace s řetězci při přepisu HTML:** Extraktory v `image_plugin.rs` a `search.rs` přepisují HTML řetězce pomocí křehkých operací `str::find` a `str::rfind`. Tento přístup je vysoce zranitelný vůči poškozeným HTML tagům, tagům `<img>` uvnitř komentářů, znakovým entitám v alternativním textu nebo již existujícím vlastnostem `srcset`, což může vést k poškozenému výstupu.  
- **Neimplementovaná podpora AVIF:** Ačkoli je kódování obrázků AVIF podrobně zdokumentováno, implementace v `image_plugin.rs` je zástupný kód, kde `avif_variants` jednoduše vrací `Vec::new()`, takže funkce zůstává nefunkční.  
- **Sledovač založený na pollingu:** Sledovač lokálního vývojového serveru (`src/server/watch.rs`) používá polling namísto API pro události souborového systému, což vede k nadměrnému využití CPU v nečinnosti a k latenci modifikací pod jednou sekundou.

### Funkční mezery a mezery ve vývojářské zkušenosti

- **Žádné sledování tranzitivních závislostí:** Graf závislostí nedokáže sledovat vnořené závislosti (např. změny dílčí šablony, která ovlivňuje rozvržení, jež ovlivňuje stránku), jak potvrzuje jednotkový test `transitive_not_tracked`.  
- **Žádný přepínač CLI pro inkrementální kompilaci:** Neexistuje přepínač CLI `--incremental` napojený na spouštěcí kompilátor, což vývojářům brání využívat cachovaná sestavení.  
- **HMR je omezen na CSS:** Hot Module Replacement (HMR) podporuje pouze CSS; jakákoli úprava souborů HTML, rozvržení nebo Markdownu spustí úplné znovunačtení stránky, což snižuje rychlost vývoje.  
- **Nedostatek podpříkazů:** Vývojáři musí ručně předávat rozvláčné přepínače (`ssg -s public -w`), protože standardní podpříkazy jako `ssg dev`, `ssg build`, `ssg check` a `ssg lint` neexistují.

---

## Architektonické mezery, které nám chybí (nová zjištění)

Kromě mezer ve verzi 0.0.41 odhaluje hodnocení projektu proti rizikovému profilu finanční úrovně několik schopností, které zatím neposkytuje, ale které by podnikový kupující vyžadoval:

### 1. Sandboxing pluginů ve WebAssembly (rozšíření zero-trust)

Ačkoli je samotná binárka kompilátoru napsána v bezpečném Rustu, umožnit libovolným pluginům třetích stran nativní spuštění na hostitelských systémech zavádí závažnou zranitelnost dodavatelského řetězce. Kompromitovaný plugin třetí strany by mohl snadno získat přístup k souborovému systému hostitele, číst proprietární soubory Markdownu nebo odcizit soukromé přihlašovací údaje.

* **Chybějící schopnost:** Sandboxované prostředí pro spouštění. K dosažení kompilace v režimu zero-trust by měl kompilátor spouštět pluginy třetích stran uvnitř vestavěného běhového prostředí WebAssembly (jako `wasmtime`). Pluginy by měly s hostitelem komunikovat výhradně prostřednictvím omezeného WebAssembly System Interface (WASI), který jejich přístup striktně omezuje na právě transformovanou stránku.

### 2. Parsování HTML bez kopírování pomocí streamovaného AST (`lol_html`)

Migrace parsovací vrstvy HTML na plnohodnotnou knihovnu DOM v paměti (jako Kuchiki nebo html5ever) zavádí významnou paměťovou režii a pauzy při zpracování u webů s více než 100 000 stránkami.

* **Chybějící schopnost:** Streamovaný HTML přepisovač bez kopírování. Využití knihovny `lol_html` od Cloudflare (HTML přepisovač s nízkou výstupní latencí) umožňuje kompilátoru parsovat, inspektovat a modifikovat HTML prvky v jediném streamovaném průchodu s téměř nulovou alokací paměti, což odpovídá cíli paralelního streamovacího kompilátoru na sestavení pod jednou sekundou.

### 3. Lokální sémantické vektorové vyhledávání (lokální RAG)

Současný vyhledávací index (`SearchPlugin`) generuje těžký, plochý index JSON, který provádí jednoduché porovnávání řetězců na straně klienta a postrádá podporu fuzzy vyhledávání, stemmingu nebo sémantických dotazů. Pagefind je zlepšením, ale stále se spoléhá na stažení velkého indexu.

* **Chybějící schopnost:** Vestavěné sémantické vyhledávání. Kompilátor by měl při sestavení využívat lokální, odlehčený model vektorových embeddingů nativní pro Rust (jako model MiniLM-L6 spouštěný přes `candle` nebo `ort` / ONNX Runtime). Měl by generovat husté vektorové embeddingy pro každý odstavec stránky a vypisovat kompaktní vektorový index. Vyhledávací widget na straně klienta, zkompilovaný do WASM, pak může provádět skutečné offline sémantické vyhledávání přímo v prohlížeči.

### 4. Deterministické cachování překladu a inference

Protože lokální inference LLM (např. přes Ollama nebo Llama.cpp) je velmi náročná na CPU/GPU, překládání nebo generování metadat pro tisíce stránek při každém sestavení je výpočetně neúnosné.

* **Chybějící schopnost:** Cachování inference založené na hashi obsahu. Kompilátor musí udržovat deterministickou cache všech operací LLM. Pokud se hash SHA-256 obsahu souboru Markdownu a jeho parametrů překladu shoduje s položkou v cache, měl by kompilátor znovu použít cachovaný překlad a metadata a obejít nadbytečnou lokální inferenci.

### 5. Asynchronní souborové I/O pro paralelní škálování

Ačkoli je plugin pipeline paralelizována přes Rayon, standardní synchronní zápisy na disk blokují OS vlákna Rayonu, čímž vzniká úzké hrdlo I/O při zápisu desítek tisíc stránek.

* **Chybějící schopnost:** Asynchronní, neblokující diskové I/O. Kompilátor by měl oddělit úlohy náročné na CPU (parsování Markdownu, minifikace) od zápisů vázaných na disk pomocí asynchronních I/O vláknových fondů nebo linuxových vazeb `io_uring` (přes `rio` nebo `tokio`), aby zapisoval zkompilované stránky paralelně bez blokování paralelních CPU exekutorů.

---

## Strategický plán do verze 1.0

Následující plán integruje jak vyřešené mezery, tak nově objevené schopnosti podnikové úrovně do strukturovaného, chronologického rámce vydání.

### Fáze 1: 0.0.42 (oprava odolnosti a korektnosti, 1 až 2 týdny)

1. **Rekonstrukce `MinifyPlugin`:** Integrace `minify-html`, `oxc_minifier` a `lightningcss` pro nativní, syntakticky uvědomělou minifikaci HTML, JS a CSS. Zajistit, aby plugin rekurzivně procházel všechny vnořené adresáře pod `site_dir`.  
2. **Zabezpečení AI pipeline:** Přenést `LlmPlugin` z nativních volání `curl` přes shell na `ureq` (odlehčený, synchronní, bezpečný HTTP klient v Rustu) k zajištění kompatibility napříč platformami a odstranění zranitelností typu shell injection.  
3. **Dokončení implementace AVIF:** Zapojit `ravif` přímo do obrazové asset pipeline a umožnit vysoce výkonné kódování AVIF vedle WebP a PNG.  
4. **Automatizace HrefLang a mapování více lokalizací:** Automaticky detekovat paralelní přeložené stránky ve vícejazyčných sestaveních a vkládat standardní tagy `<link rel="alternate" hreflang="..." />` odpovídající požadavkům Google do hlavičky každého zkompilovaného souboru HTML.  
5. **Podpora JSON Feed 1.1:** Dodat dedikovaný emitor JSON Feed 1.1 vedle standardních syndikačních kanálů RSS 2.0 a Atom 1.0.

### Fáze 2: 0.1.0 (minorní vydání pro důvěryhodnost a inkrementální sestavení, 2 až 3 měsíce)

1. **Naplnění `DepGraph` a povolení `--incremental`:** Plně napojit `DepGraph` na sledování závislostí šablona-stránka a Markdown-stránka. Implementovat vrstvu invalidace cache a napojit přepínač CLI `--incremental` s cílem znovusestavení pod 200 ms pro prostředí s teplou cache.  
2. **Přepis na streamovaný AST pomocí `lol_html`:** Nahradit křehký přepis řetězců v `image_plugin.rs`, `search.rs` a při vkládání CSP streamovaným HTML přepisovačem bez kopírování poháněným `lol_html`.  
3. **Sledovač řízený událostmi a HMR komponent:** Přenést modul sledování z pollingu na knihovnu `notify` řízenou událostmi a implementovat hot reloading pouze pro CSS a částečné HTML pro aktualizace prohlížeče pod 100 ms.  
4. **Sjednocené CLI příkazů:** Přearchitektovat rozhraní kompilátoru tak, aby podporovalo standardní podpříkazy: `ssg dev`, `ssg build`, `ssg check` (audit přístupnosti/SEO) a `ssg deploy`.  
5. **Deterministická cache inference:** Implementovat vrstvu cachování založenou na hashi obsahu pro všechny úlohy lokálního LLM překladu, sumarizace a extrakce metadat.

### Fáze 3: 1.0.0 (podniková a produkční major verze, 6 až 12 měsíců)

1. **Sandboxing WASM pluginů v režimu zero-trust:** Vestavět běhové prostředí WebAssembly (`wasmtime` nebo `wasmer`) ke spouštění pluginů třetích stran v plně sandboxovaném prostředí s přístupem k souborovému systému a síti založeným na schopnostech.  
2. **Lokální sémantické vektorové vyhledávání (lokální RAG):** Vestavět lokální model embeddingů nativní pro Rust (přes `candle` nebo `ort`) k zkompilování hustých embeddingů odstavců do kompaktního indexu a umožnit soukromé sémantické vyhledávání na straně klienta.  
3. **Server Islands a cílová platforma WASM Edge:** Implementovat spouštění komponent `<ssg-island>` na edge runtimech (jako Cloudflare Workers, Vercel Edge nebo Netlify Edge) postavených nad zkompilovaným jádrem `ssg-wasm`.  
4. **Asynchronní paralelní I/O engine:** Přearchitektovat modul zápisu na souborový systém tak, aby využíval asynchronní I/O vláknové fondy a vazby `io_uring`, čímž se eliminuje blokování CPU pracovníků během paralelních zápisů.  
5. **Proveniences sestavení SLSA v1.1 a soulad se SPDX 3.0:** Poskytnout matematicky ověřitelnou proveniences sestavení na úrovni SLSA Level 3 a generovat SBOM odpovídající SPDX 3.0, plně splňující moderní standardy bezpečnosti softwarového dodavatelského řetězce.

---

## Konkurenční matice (prostředí roku 2026)

Následující matice porovnává `static-site-generator` (cíl verze 1.0) proti předním enginům pro webové publikování roku 2026:

| Schopnost | static-site-generator v1.0 | Hugo v0.155+ | Zola v0.19+ | Astro 5 | Eleventy 3 |
| ---- | ---- | ---- | ---- | ---- | ---- |
| **Jazyk / běhové prostředí** | Rust (bez unsafe) | Go | Rust | JS (Node/V8) | JS (Node/V8) |
| **Brána přístupnosti při sestavení** | Validace AST při sestavení | Žádná | Žádná | Linter po sestavení | Linter po sestavení |
| **Bezpečnostní zpevnění** | SHA-384 SRI a vkládání CSP | Ruční | Ruční | Ruční | Ruční |
| **Bezpečnost dodavatelského řetězce** | SLSA L3 \+ SPDX 3.0 \+ WASM sandbox | Minimální | Minimální | Rozsáhlý strom NPM | Rozsáhlý strom NPM |
| **AI pipeline pro obsah** | Soukromá, lokální (lokální LLM) | Žádná | Žádná | Jen veřejné API | Jen veřejné API |
| **Rychlost inkrementálního sestavení** | \<200 ms (teplá cache) | \<100 ms | \<150 ms | \~1,5 s | \~140 ms |
| **Dynamická interaktivita** | Server Islands (cíle WASM) | Žádná | Žádná | Server Islands (JS) | Islands (JS) |
| **Vyhledávací engine** | Lokální sémantické WASM vyhledávání | Jednoduché řetězce | Jednoduché řetězce | Pagefind (JS) | Pagefind (JS) |

---

## Pozicování ve verzi 1.0

Ve verzi 1.0 je zamýšleným pozicováním generátor statických webů navržený jako softwarová infrastruktura bezpečná ve výchozím nastavení: tvorba obsahu podporovaná lokálními AI pipeline; kompilace více než 100 000 stránek paralelní streamovací pipeline; WCAG 2.2 AA a striktní CSP a SRI vynucené jako brány sestavení; a sandboxované dynamické islands, to vše v jediné, paměťově bezpečné binárce v Rustu. Každá klauzule tohoto prohlášení odpovídá konkrétní položce z výše uvedeného plánu, nikoli marketingové ambici.

---

## Integrace regulace a compliance

Ve vysoce rizikových podnikových a finančních sektorech se software posuzuje optikou compliance a rizikového kapitálu. Architektonický plán `static-site-generator` se přímo shoduje s hlavními regulatorními mandáty:

- **DORA, článek 6 (řízení rizik ICT):** Výpočet a vkládání hashů SHA-384 SRI a striktních Content Security Policies při kompilaci splňuje požadavek na ochranu digitálních publikačních kanálů před injektáží do dodavatelského řetězce, web defacementem a vektory cross-site scripting (XSS).  
- **DORA, článek 7 (odolnost systémů ICT):** Přechodem na neměnné statické assety ověřené při kompilaci finanční instituce eliminují zranitelnosti databází a běhových serverů, snižují multiplikátor provozního rizika a zmenšují požadované rezervy rizikového kapitálu podle Basel III.  
- **Evropský akt o přístupnosti (EAA), směrnice (EU) 2019/882:** Posunutí auditu přístupnosti doleva do kompilační pipeline jako tvrdé brány kompilátoru zaručuje 100% soulad před nasazením, čímž se eliminuje riziko poškození značky a občanskoprávních sporů podle EAA a ADA Title III.  
- **GDPR, článek 25 (ochrana údajů již od návrhu):** Provozování pipeline pro překlad a metadata na lokálním, síťově izolovaném hardwaru udržuje proprietární koncepty, finanční metriky a osobní údaje mimo veřejné cloudové poskytovatele LLM třetích stran, což podporuje soulad s principy datové suverenity.

---

## Často kladené otázky

**Co verze 0.0.41 dnes skutečně přináší oproti tomu, co tvrdí README?**
Model bezpečnosti a přístupnosti je skutečný a vynucený v kódu: `forbid(unsafe_code)` napříč celým workspace, generování SRI se SHA-256/384, extrakce CSP, podepsaná vydání s atestací Sigstore a SBOM ve formátu CycloneDX a brána WCAG 2.2 AA zastavující sestavení. Tři dokumentované funkce ve verzi 0.0.41 nefungují. `MinifyPlugin` je slučovač bílých znaků, nikoli syntakticky uvědomělý minifikátor; `DepGraph`, který by řídil inkrementální sestavení, se kompiluje, ale v produkčním kódu se nikdy neplní; a kódování AVIF je zástupný kód, jehož `avif_variants` vrací prázdný vektor.

**Je brána přístupnosti skutečnou bránou kompilátoru, nebo linterem po sestavení?**
Je bránou sestavení. Kontroly WCAG 2.2 AA běží uvnitř kompilační pipeline prostřednictvím parseru axe-core při sestavení, řízeného nástrojem Playwright, a stránka, která neprojde, zastaví kompilaci s chybami uvádějícími přesná čísla řádků, místo aby dodatečně vydala pouhé varování. To je vlastnost, kterou povinnost podle evropského aktu o přístupnosti vyžaduje: nevyhovující výstup se nemůže dostat do nasazení.

**Proč záleží na volání `curl` přes shell v LLM pluginu?**
Lokální LLM pipeline (`src/plugins/llm.rs`) volá binárku `curl` na hostiteli, aby dosáhla lokálních endpointů. To váže sestavení na hostitelský spustitelný soubor, selhává na systémech bez `curl` v PATH, zavádí povrch pro shell injection a selhává v síťově izolovaném CI. Přenesení volání na HTTP klienta v Rustu, jako je `ureq`, odstraňuje externí závislost i vektor injektáže, a proto je druhou položkou v opravě 0.0.42.

**Která jediná položka je na cestě k 1.0 nejdůležitější?**
Naplnění `DepGraph` a napojení přepínače `--incremental`. Inkrementální sestavení jsou mezerou v důvěryhodnosti mezi dokumentovaným a skutečným enginem a každé navazující tvrzení o sestaveních pod jednou sekundou u více než 100 000 stránek závisí na tom, aby graf závislostí sledoval hrany šablona-stránka a Markdown-stránka, místo aby zůstal infrastrukturou pouze pro testy.

## Reference

- [Cloudflare, *lol-html: streamovaný HTML přepisovač s nízkou výstupní latencí*](https://github.com/cloudflare/lol-html "Cloudflare lol-html — streamovaný HTML přepisovač") ⧉. [Streamovaný HTML přepisovač bez kopírování navržený k nahrazení křehké manipulace s řetězci ve fázi 0.1.0.]
- [W3C, *Web Content Accessibility Guidelines (WCAG) 2.2*](https://www.w3.org/TR/WCAG22/ "W3C — doporučení WCAG 2.2") ⧉. [Kritéria úspěchu úrovně AA vynucená bránou přístupnosti při kompilaci.]
- [Evropská unie, *Nařízení (EU) 2022/2554 (DORA)*](https://eur-lex.europa.eu/eli/reg/2022/2554/oj "EUR-Lex — akt o digitální provozní odolnosti") ⧉. [Články o řízení rizik ICT a odolnosti, na které se bezpečnostní postoj mapuje.]
- [OpenSSF, *Supply-chain Levels for Software Artifacts (SLSA) v1.0*](https://slsa.dev/spec/v1.0/ "SLSA — specifikace v1.0") ⧉. [Rámec proveniences sestavení, na který cílí ověřitelná atestace úrovně Level 3 ve verzi 1.0.]
- [Armin Ronacher, *Šablonovací engine MiniJinja*](https://github.com/mitsuhiko/minijinja "MiniJinja — minimální engine Jinja2 pro Rust") ⧉. [Engine s malým počtem závislostí, který nahradil Teru a prořezal tranzitivní strom.]
- [CycloneDX, *Specifikace Software Bill of Materials v1.5*](https://cyclonedx.org/docs/1.5/ "CycloneDX — specifikace SBOM v1.5") ⧉. [Formát SBOM emitovaný při každém sestavení pro audit dodavatelského řetězce.]
- [Evropská unie, *Směrnice (EU) 2019/882 (evropský akt o přístupnosti)*](https://eur-lex.europa.eu/eli/dir/2019/882/oj "EUR-Lex — evropský akt o přístupnosti") ⧉. [Povinnost přístupnosti, kterou má brána WCAG při sestavení splňovat.]

*Naposledy revidováno v červenci 2026. Původní analýza vychází z inspekce kódové báze `static-site-generator` ve verzi 0.0.41; zdroje jsou citovány, nikoli reprodukovány. Čísla verzí a stav funkcí se rychle mění, před opětovnou publikací ověřte proti repozitáři. Licencováno pod CC-BY-4.0.*

