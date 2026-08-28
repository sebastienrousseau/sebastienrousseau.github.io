---
author: "contact@sebastienrousseau.com (Sebastien Rousseau)"
banner_alt: "Un arrière-plan technique abstrait représentant la feuille de route architecturale d'un générateur de sites statiques de niveau entreprise."
banner_height: "1280"
banner_width: "1920"
banner: "https://cloudcdn.pro/stocks/images/gemini-background.webp"
cdn: "https://cloudcdn.pro"
charset: "UTF-8"
cname: "sebastienrousseau.com"
copyright: "© Copyright 2025 - 2026 - Sebastien Rousseau. All rights reserved."
date: "July 22, 2026"
description: "Analyse d'un générateur de sites statiques en Rust : sécurité à la compilation, barrières WCAG, IA locale, lacunes de la v0.0.41 et feuille de route vers 1.0."
format-detection: "telephone=no"
hreflang: "fr"
icon: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
id: "https://sebastienrousseau.com/fr/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
image_alt: "Portrait en noir et blanc de Sebastien Rousseau"
image_height: "162"
image_width: "162"
image: "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp"
keywords: "générateur de sites statiques, Rust, forbid unsafe_code, WCAG 2.2 AA, Content Security Policy, Subresource Integrity, SLSA, SBOM CycloneDX, pipeline LLM local, DORA, builds incrémentaux, lol_html, bac à sable de plugins WASM, recherche vectorielle sémantique, MiniJinja, Ollama"
language: "fr"
last_reviewed: "2026-07-22"
layout: "report"
locale: "fr_FR"
logo_alt: "Logo de Sebastien Rousseau"
logo_height: "44"
logo_width: "44"
logo: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
menu: ""
measurementID: "G-169G4ET5HQ"
name: "Sebastien Rousseau"
permalink: "https://sebastienrousseau.com/fr/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
rating: "general"
referrer: "no-referrer"
robots: "index, follow"
schema: "FAQPage, Article"
seo_title: "Générateur de sites statiques : la route vers la 1.0"
short_name: "sebastienrousseau"
subtitle: "Un audit architectural et une feuille de route pour un générateur de sites statiques en Rust conçu comme une infrastructure sécurisée par défaut : ce que la v0.0.41 livre réellement face aux promesses du README, cinq capacités d'entreprise manquantes et un chemin par étapes vers une 1.0 alignée sur DORA et l'EAA."
tags: "générateur de sites statiques, Rust, sécurité web, accessibilité, DORA, chaîne d'approvisionnement, SLSA, IA locale, WCAG, compilation, feuille de route, entreprise"
theme-color: "0, 83, 191"
title: "Générateur de sites statiques (SSG) : audit et feuille de route"
url: "https://sebastienrousseau.com/fr/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap/rss.xml"
category: "Technology"
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.26)"
item_description: "Analyse d'un générateur de sites statiques en Rust : sécurité à la compilation, barrières WCAG, IA locale, lacunes de la v0.0.41 et feuille de route vers 1.0."
item_guid: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap/rss.xml"
item_link: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap/rss.xml"
item_pub_date: "Wed, 22 Jul 2026 07:07:07 +0000"
item_title: "Générateur de sites statiques (SSG) : audit et feuille de route"
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
apple-mobile-web-app-title: "SSG : route vers la 1.0"
apple-touch-fullscreen: "yes"
msapplication-navbutton-color: "0, 83, 191"
twitter_card: "summary_large_image"
twitter_creator: "@wwdseb"
twitter_description: "Barrières WCAG à la compilation, SRI SHA-384, injection CSP, pipeline LLM local : ce moteur Rust se distingue. Analyse honnête de la v0.0.41 et route vers 1.0."
twitter_image: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
twitter_image_alt: "Logo de Sebastien Rousseau"
twitter_site: "@wwdseb"
twitter_title: "Générateur de sites statiques : la route vers la 1.0"
twitter_url: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
excerpt: "Barrières WCAG, SRI SHA-384, injection CSP et pipeline LLM local distinguent ce moteur Rust ; build incrémental, minification et AVIF restent à faire."
author_website: "https://sebastienrousseau.com"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "Merci de votre lecture !"
site_last_updated: "2026-07-22"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "Kaishi, Kaishi Builder, Kaishi CLI, Kaishi Templates, Kaishi Themes"
---

# Générateur de sites statiques (SSG) : audit stratégique de niveau entreprise et feuille de route architecturale

*Date de la recherche : 2026-06-22. Fondé sur l'inspection du code source de `static-site-generator` en v0.0.41 et sur une revue documentaire de l'écosystème des SSG en 2026.*

**Pour un éditeur régulé, un générateur de sites statiques n'est plus un outil de conception ; il fait partie du périmètre de risque opérationnel.** Le projet open source en Rust [static-site-generator](https://github.com/sebastienrousseau/static-site-generator) part de cette prémisse : il déplace la sécurité, l'accessibilité, l'internationalisation et les pipelines de contenu par IA vers la compilation, de sorte qu'un contrôle en échec arrête la construction au lieu d'atteindre la production. Cette analyse distingue ce que la version 0.0.41 livre réellement de ce que sa documentation ne fait encore que promettre, énumère cinq capacités d'entreprise qui lui manquent, et propose un chemin par étapes vers une version 1.0 alignée sur DORA, la loi européenne sur l'accessibilité (European Accessibility Act) et les normes actuelles de la chaîne d'approvisionnement logicielle.

<!-- lead-start -->
<aside class="post-lead" aria-label="Résumé de l'article">
<p class="post-lead-tldr"><strong>En bref.</strong> Le projet Rust <code>static-site-generator</code> traite la publication web comme un pipeline logiciel auditable et sécurisé par défaut : <code>forbid(unsafe_code)</code> à l'échelle de l'espace de travail, intégrité des sous-ressources (Subresource Integrity) en SHA-384, extraction de Content Security Policy, une barrière WCAG 2.2 AA à la compilation et un pipeline LLM local en priorité. L'inspection du code de la v0.0.41 montre que plusieurs fonctionnalités documentées restent à l'état d'intention : minification native, constructions incrémentales et AVIF en font partie. Voici l'analyse honnête des écarts et une feuille de route par étapes vers une 1.0 de niveau entreprise.</p>
<p class="post-lead-heading"><strong>Points clés</strong></p>
<ul class="post-lead-takeaways">
  <li><strong>Le modèle de sécurité et d'accessibilité est réel.</strong> SRI à la compilation, extraction de CSP, versions signées avec attestation Sigstore et SBOM CycloneDX, plus une barrière WCAG 2.2 AA qui arrête la construction : tout cela est implémenté dans le code, pas seulement documenté.</li>
  <li><strong>Plusieurs fonctionnalités mises en avant ne le sont pas.</strong> Le minifieur se contente de réduire les espaces, le graphe de dépendances censé piloter les constructions incrémentales n'est jamais renseigné en production, et l'encodage AVIF est une ébauche qui retourne un vecteur vide.</li>
  <li><strong>Cinq capacités d'entreprise manquent.</strong> Bac à sable de plugins WASM, réécrivain HTML en flux sans copie, recherche sémantique locale, cache d'inférence déterministe et E/S fichier asynchrones.</li>
  <li><strong>La feuille de route est ordonnée par le risque.</strong> Un correctif de justesse (0.0.42), une version mineure de crédibilité et d'incrémental (0.1.0), puis une version majeure d'entreprise (1.0.0) portant le bac à sable, la recherche sémantique et la provenance SLSA v1.1.</li>
</ul>
<p class="post-lead-related"><strong>À lire également :</strong> <a href="https://sebastienrousseau.com/2026-07-03-emerging-technology-risk-horizon-banks-2026">L'horizon de risque des technologies émergentes pour les banques</a>, <a href="https://sebastienrousseau.com/2026-07-07-corporate-banking-api-standard-agentic-mcp-2026">Un standard d'API de banque d'entreprise pour le MCP agentique</a>.</p>
</aside>
<!-- lead-end -->

> **Synthèse pour dirigeants**
>
> - **La publication est désormais un périmètre de risque opérationnel.** Sous DORA, la loi européenne sur l'accessibilité et le RGPD, chaque actif exposé au public est un point d'entrée possible pour une compromission de la chaîne d'approvisionnement, une défiguration et une exposition réglementaire. Un modèle par compilation resserre ce périmètre en rejetant toute sortie non conforme avant sa mise en production.
> - **Les différenciateurs du moteur sont imposés par le compilateur, pas des intentions documentées.** `forbid(unsafe_code)` à l'échelle de l'espace de travail, une véritable SRI en SHA-256/384, une extraction CSP automatique et une barrière WCAG 2.2 AA à la compilation transforment la sécurité et l'accessibilité, d'audits a posteriori en échecs de construction fermes.
> - **La version 0.0.41 présente un écart entre documentation et code.** La minification native, les constructions incrémentales via un graphe de dépendances et la prise en charge d'AVIF sont décrites mais non fonctionnelles ; l'article désigne chaque écart en pointant l'emplacement exact dans le code source.
> - **Le chemin vers la 1.0 est une séquence, pas une liste de souhaits.** La robustesse d'abord (0.0.42), puis la justesse de l'incrémental (0.1.0), puis les capacités d'entreprise, bac à sable WASM, recherche sémantique locale et provenance SLSA vérifiable, qu'exige un acheteur régulé (1.0.0).

## Points forts actuels

Le code de `static-site-generator` traduit plusieurs choix d'ingénierie distinctifs qui le séparent des moteurs historiques en JavaScript et en Go :

- **Posture de sécurité à la compilation :** `#![forbid(unsafe_code)]` à l'échelle de l'espace de travail fournit des garanties de sûreté mémoire à la compilation. Le pipeline de construction génère de véritables empreintes d'intégrité des sous-ressources (Subresource Integrity, SRI) en SHA-256/SHA-384 (`src/plugins/assets.rs`) et procède à une extraction automatique de la Content Security Policy (CSP) qui supprime les scripts et styles unsafe-inline. Les versions sont signées, portent une attestation Sigstore et produisent un SBOM CycloneDX 1.5 à chaque construction.  
- **Barrière d'accessibilité imposée par le compilateur :** les contrôles WCAG (Web Content Accessibility Guidelines) 2.2 niveau AA s'exécutent au sein du pipeline de compilation via un analyseur axe-core à la compilation piloté par Playwright. L'accessibilité devient une barrière de compilation ferme plutôt qu'un audit post-publication : si une page échoue, la compilation s'arrête avec des erreurs indiquant le numéro de ligne exact.  
- **Pipeline d'IA à souveraineté des données :** un pipeline local de traduction et d'extraction de métadonnées par LLM (via des points d'accès Ollama ou llama.cpp locaux) permet à une institution d'automatiser le résumé de contenu, la génération de schémas JSON-LD et la traduction multilingue sans transmettre de communications antérieures aux résultats ni de propriété intellectuelle sensible à des API d'IA de cloud public.  
- **Compilation parallélisée :** les garanties de sûreté mémoire de Rust soutiennent un pipeline HTML et d'actifs parallélisé, piloté par Rayon (`src/core/pipeline.rs`). Le pipeline de plugins exécute des transformations fusionnées, avec `SearchPlugin`, `SeoPlugin`, `CanonicalPlugin` et `JsonLdPlugin` opérant sur `par_iter()`, de sorte que chaque page est lue et écrite sur disque une seule fois.  
- **Hygiène de la chaîne d'approvisionnement et des dépendances :** la migration du moteur de gabarits de Tera vers MiniJinja (`v0.0.37`) a réduit la taille du binaire, supprimé des dépendances transitives comme `rand` à la compilation et produit une empreinte de dépendances compacte qui abaisse l'exposition de la chaîne d'approvisionnement logicielle.

---

## Écarts et réalités du terrain

Malgré ces points forts remarquables, une inspection rigoureuse du code de la v0.0.41 révèle plusieurs écarts architecturaux, fonctionnels et d'expérience développeur entre ses annonces documentaires et le code Rust réel :

### Écarts architecturaux

- **Réduction d'espaces plutôt que minification native :** alors que le README promet une « minification JS/CSS native », le `MinifyPlugin` (`src/plugins/plugins.rs:96-116`) agit simplement comme un réducteur d'espaces rudimentaire. Il court-circuite les éléments `<pre>` et compacte les séquences d'espaces en HTML, mais n'effectue pas de minification CSS ou JS native consciente de la syntaxe. De plus, il ne traite que les pages de premier niveau et ne parcourt pas récursivement les sous-répertoires (tels que `/blog/` ou `/tags/`), laissant les pages profondes non minifiées.  
- **Infrastructure incrémentale morte :** le graphe de suivi des dépendances (`DepGraph` dans `src/core/depgraph.rs`) est compilé et chargé dans `PluginContext.dep_graph`, mais n'est jamais réellement renseigné dans le code de production. La méthode `add_dep()` n'est appelée que dans les tests unitaires, ce qui rend l'affirmation du README, « constructions incrémentales via des graphes de dépendances », pour l'instant à l'état d'intention.  
- **Compilation par lots plutôt que compilation en flux :** le module `streaming::compile_batch` (`src/core/streaming.rs`) ne traite pas véritablement en flux. Il compile plutôt les pages par lots vers un répertoire temporaire, exécute `staticdatagen::compile` à partir de zéro pour chaque lot, puis fusionne les sorties. Il en résulte une surcharge d'E/S disque importante et une analyse redondante, ce qui s'écarte d'une véritable architecture en flux.  
- **Violations de phase du cycle de vie des plugins :** les plugins qui génèrent de nouvelles pages HTML pendant la construction, tels que `TaxonomyPlugin`, `PaginationPlugin` et `I18nPlugin`, écrivent directement sur disque dans `after_compile` au lieu d'emprunter le cycle de vie `transform_html`. Par conséquent, les pages générées par ces plugins contournent des plugins de post-traitement critiques (tels que `CanonicalPlugin`, `JsonLdPlugin`, `RobotsPlugin` et `AccessibilityPlugin`) si ces derniers ont été enregistrés plus tôt. Cela laisse les pages de tags, de catégories et paginées sans liens canoniques corrects, sans schémas JSON-LD, ni validations d'accessibilité.  
- **Appel de `curl` en sous-processus dans `LlmPlugin` :** le pipeline de contenu LLM local (`src/plugins/llm.rs`) invoque directement le binaire `curl` de l'hôte pour interroger les points d'accès locaux. Cela introduit de graves bogues multiplateformes (par exemple, sur les hôtes Windows sans curl dans le PATH), pose un risque de sécurité (vecteurs d'injection shell) et échoue dans les environnements d'intégration continue verrouillés ou isolés du réseau.  
- **Manipulation de chaînes rudimentaire dans la réécriture HTML :** les extracteurs de `image_plugin.rs` et de `search.rs` réécrivent les chaînes HTML au moyen d'opérations fragiles `str::find` et `str::rfind`. Cette approche est très vulnérable aux balises HTML mal formées, aux balises `<img>` à l'intérieur de commentaires, aux entités de caractères dans le texte alternatif ou aux propriétés `srcset` préexistantes, ce qui peut produire une sortie corrompue.  
- **Prise en charge d'AVIF non implémentée :** bien que l'encodage d'images AVIF soit abondamment documenté, l'implémentation dans `image_plugin.rs` est une ébauche où `avif_variants` retourne simplement `Vec::new()`, laissant la fonctionnalité inopérante.  
- **Surveillance par interrogation :** le surveillant du serveur de développement local (`src/server/watch.rs`) recourt à l'interrogation plutôt qu'aux API d'événements du système de fichiers, d'où une consommation CPU excessive au repos et une latence de détection des modifications inférieure à la seconde.

### Écarts fonctionnels et d'expérience développeur

- **Aucun suivi des dépendances transitives :** le graphe de dépendances ne peut pas suivre les dépendances imbriquées (par exemple, une modification d'un sous-gabarit qui affecte une mise en page qui affecte une page), comme le confirme le test unitaire `transitive_not_tracked`.  
- **Aucune option CLI de compilation incrémentale :** il n'existe aucune option CLI `--incremental` reliée au compilateur d'exécution, ce qui empêche les développeurs de tirer parti des constructions mises en cache.  
- **Le HMR se limite au CSS :** le rechargement à chaud des modules (Hot Module Replacement, HMR) ne prend en charge que le CSS ; toute modification des fichiers HTML, des mises en page ou des fichiers markdown déclenche un rechargement complet de la page, ce qui dégrade la vélocité du développeur.  
- **Déficit de sous-commandes :** les développeurs doivent passer manuellement des options verbeuses (`ssg -s public -w`) car des sous-commandes standard comme `ssg dev`, `ssg build`, `ssg check` et `ssg lint` n'existent pas.

---

## Écarts architecturaux qu'il nous manque (nouvelles découvertes)

Au-delà des écarts de la v0.0.41, évaluer le projet à l'aune d'un profil de risque de niveau financier fait apparaître plusieurs capacités qu'il n'offre pas encore mais qu'un acheteur d'entreprise exigerait :

### 1. Bac à sable de plugins WebAssembly (extension à confiance nulle)

Si le binaire du compilateur lui-même est écrit en Rust sûr, autoriser des plugins tiers arbitraires à s'exécuter nativement sur les systèmes hôtes introduit une grave vulnérabilité de la chaîne d'approvisionnement. Un plugin tiers compromis pourrait aisément accéder au système de fichiers de l'hôte, lire des fichiers Markdown propriétaires ou exfiltrer des identifiants privés.

* **Capacité manquante :** un environnement d'exécution en bac à sable. Pour parvenir à une compilation à confiance nulle, le compilateur devrait exécuter les plugins tiers à l'intérieur d'un moteur d'exécution WebAssembly embarqué (tel que `wasmtime`). Les plugins devraient interagir avec l'hôte uniquement via une interface système WebAssembly (WASI) restreinte, limitant strictement leur accès à la page en cours de transformation.

### 2. Analyse HTML sans copie via un AST en flux (`lol_html`)

Faire migrer la couche d'analyse HTML vers une bibliothèque DOM entièrement en mémoire (comme Kuchiki ou html5ever) introduit une surcharge mémoire importante et des pauses de traitement lors du traitement de sites de plus de 100 000 pages.

* **Capacité manquante :** un réécrivain HTML en flux, sans copie. Recourir à `lol_html` de Cloudflare (réécrivain HTML à faible latence de sortie) permet au compilateur d'analyser, d'inspecter et de modifier les éléments HTML en une seule passe en flux, avec une allocation mémoire proche de zéro, à la hauteur de l'objectif du compilateur parallèle en flux : des constructions inférieures à la seconde.

### 3. Recherche vectorielle sémantique locale (RAG local)

L'index de recherche actuel (`SearchPlugin`) génère un index JSON lourd et plat qui effectue de simples correspondances de chaînes côté client, sans prise en charge de la recherche approximative, de la racinisation ni des requêtes sémantiques. Pagefind constitue une amélioration, mais il repose encore sur le téléchargement d'un index volumineux.

* **Capacité manquante :** une recherche sémantique embarquée. Le compilateur devrait exploiter à la compilation un modèle local et léger de plongements vectoriels natif de Rust (tel qu'un modèle MiniLM-L6 exécuté via `candle` ou `ort` / ONNX Runtime). Il devrait générer des plongements vectoriels denses pour chaque paragraphe de page et produire un index vectoriel compact. Le widget de recherche côté client, compilé en WASM, peut alors effectuer une véritable recherche sémantique hors ligne directement dans le navigateur.

### 4. Cache déterministe de traduction et d'inférence

Parce que l'inférence LLM locale (par exemple via Ollama ou Llama.cpp) est très gourmande en CPU/GPU, traduire ou générer des métadonnées pour des milliers de pages à chaque construction est prohibitif sur le plan calculatoire.

* **Capacité manquante :** un cache d'inférence fondé sur l'empreinte du contenu. Le compilateur doit maintenir un cache déterministe de toutes les opérations LLM. Si l'empreinte SHA-256 du contenu d'un fichier markdown et de ses paramètres de traduction correspond à une entrée du cache, le compilateur devrait réutiliser la traduction et les métadonnées en cache, en évitant une inférence locale redondante.

### 5. E/S fichier asynchrones pour la montée en charge parallèle

Bien que le pipeline de plugins soit parallélisé via Rayon, les écritures disque synchrones standard bloquent les threads système de Rayon, créant un goulet d'étranglement d'E/S lors de l'écriture de dizaines de milliers de pages.

* **Capacité manquante :** des E/S disque asynchrones et non bloquantes. Le compilateur devrait découpler les tâches gourmandes en CPU (analyse Markdown, minification) des écritures liées au disque, en recourant à des pools de threads d'E/S asynchrones ou aux liaisons Linux `io_uring` (via `rio` ou `tokio`) pour écrire les pages compilées en parallèle sans bloquer les exécuteurs CPU parallèles.

---

## La feuille de route stratégique vers la 1.0

La feuille de route ci-dessous intègre à la fois les écarts résolus et les capacités de niveau entreprise nouvellement découvertes dans un cadre de publication structuré et chronologique.

### Phase 1 : 0.0.42 (le correctif de robustesse et de justesse, 1 à 2 semaines)

1. **Reconstruire `MinifyPlugin` :** intégration de `minify-html`, `oxc_minifier` et `lightningcss` pour une minification HTML, JS et CSS native et consciente de la syntaxe. Veiller à ce que le plugin parcoure récursivement tous les répertoires imbriqués sous `site_dir`.  
2. **Sécuriser le pipeline d'IA :** faire migrer `LlmPlugin` des appels natifs à `curl` en sous-processus vers `ureq` (un client HTTP Rust léger, synchrone et sûr) afin d'assurer la compatibilité multiplateforme et d'éliminer les vulnérabilités d'injection shell.  
3. **Achever l'implémentation d'AVIF :** raccorder `ravif` directement au pipeline d'actifs d'images, pour activer un encodage AVIF performant aux côtés de WebP et PNG.  
4. **Automatiser le HrefLang et la cartographie multilocale :** détecter automatiquement les pages traduites parallèles dans les constructions multilingues et injecter des balises `<link rel="alternate" hreflang="..." />` standard et conformes aux exigences de Google dans l'en-tête de chaque fichier HTML compilé.  
5. **Prise en charge de JSON Feed 1.1 :** livrer un émetteur JSON Feed 1.1 dédié aux côtés des canaux de syndication standard RSS 2.0 et Atom 1.0.

### Phase 2 : 0.1.0 (la version mineure de crédibilité et d'incrémental, 2 à 3 mois)

1. **Renseigner `DepGraph` et activer `--incremental` :** relier entièrement `DepGraph` pour suivre les dépendances gabarit-vers-page et markdown-vers-page. Implémenter une couche d'invalidation de cache et relier l'option CLI `--incremental`, en visant des reconstructions inférieures à 200 ms pour les environnements à cache chaud.  
2. **Réécriture d'AST en flux via `lol_html` :** remplacer la réécriture de chaînes fragile dans `image_plugin.rs`, `search.rs` et les injections CSP par un réécrivain HTML en flux, sans copie, propulsé par `lol_html`.  
3. **Surveillance pilotée par événements et HMR par composant :** faire migrer le module de surveillance de l'interrogation vers la crate `notify` pilotée par événements, et implémenter un rechargement à chaud CSS uniquement et HTML partiel pour des mises à jour du navigateur inférieures à 100 ms.  
4. **CLI à commandes unifiées :** repenser l'interface du compilateur pour prendre en charge des sous-commandes standard : `ssg dev`, `ssg build`, `ssg check` (audit d'accessibilité/SEO) et `ssg deploy`.  
5. **Cache d'inférence déterministe :** implémenter une couche de cache fondée sur l'empreinte du contenu pour toutes les tâches locales de traduction, de résumé et d'extraction de métadonnées par LLM.

### Phase 3 : 1.0.0 (la version majeure d'entreprise et de production, 6 à 12 mois)

1. **Bac à sable de plugins WASM à confiance nulle :** embarquer un moteur d'exécution WebAssembly (`wasmtime` ou `wasmer`) pour exécuter les plugins tiers dans un environnement entièrement en bac à sable, avec un accès au système de fichiers et au réseau fondé sur les capacités.  
2. **Recherche vectorielle sémantique locale (RAG local) :** embarquer un modèle de plongements natif de Rust (via `candle` ou `ort`) pour compiler des plongements de paragraphes denses en un index compact, permettant une recherche sémantique privée, côté client.  
3. **Îlots serveur et cible edge WASM :** implémenter l'exécution de composants `<ssg-island>` sur des runtimes edge (tels que Cloudflare Workers, Vercel Edge ou Netlify Edge) construits par-dessus le cœur `ssg-wasm` compilé.  
4. **Moteur d'E/S parallèles asynchrones :** repenser le module d'écriture sur le système de fichiers pour recourir à des pools de threads d'E/S asynchrones et aux liaisons `io_uring`, éliminant les blocages des travailleurs CPU pendant les écritures parallèles.  
5. **Provenance de construction SLSA v1.1 et conformité SPDX 3.0 :** fournir une provenance de construction SLSA niveau 3 mathématiquement vérifiable et générer des SBOM conformes à SPDX 3.0, satisfaisant pleinement les normes actuelles de sécurité de la chaîne d'approvisionnement logicielle.

---

## Matrice concurrentielle (écosystème 2026)

La matrice ci-dessous compare `static-site-generator` (cible v1.0) aux principaux moteurs de publication web de 2026 :

| Capacité | static-site-generator v1.0 | Hugo v0.155+ | Zola v0.19+ | Astro 5 | Eleventy 3 |
| ---- | ---- | ---- | ---- | ---- | ---- |
| **Langage / Runtime** | Rust (zéro unsafe) | Go | Rust | JS (Node/V8) | JS (Node/V8) |
| **Barrière d'accessibilité à la construction** | Validation d'AST à la compilation | Aucune | Aucune | Linter post-construction | Linter post-construction |
| **Durcissement de la sécurité** | SRI SHA-384 et injection CSP | Manuel | Manuel | Manuel | Manuel |
| **Sûreté de la chaîne d'approvisionnement** | SLSA L3 \+ SPDX 3.0 \+ bac à sable WASM | Minimale | Minimale | Arbre NPM lourd | Arbre NPM lourd |
| **Pipeline de contenu par IA** | Privé, local en priorité (LLM local) | Aucun | Aucun | API publique uniquement | API publique uniquement |
| **Vitesse incrémentale** | \<200 ms (cache chaud) | \<100 ms | \<150 ms | \~1,5 s | \~140 ms |
| **Interactivité dynamique** | Îlots serveur (cibles WASM) | Aucune | Aucune | Îlots serveur (JS) | Îlots (JS) |
| **Moteur de recherche** | Recherche sémantique WASM locale | Chaîne simple | Chaîne simple | Pagefind (JS) | Pagefind (JS) |

---

## Positionnement à la 1.0

À la 1.0, le positionnement visé est celui d'un générateur de sites statiques conçu comme une infrastructure logicielle sécurisée par défaut : une rédaction assistée par des pipelines d'IA locaux en priorité ; la compilation de plus de 100 000 pages via un pipeline parallèle en flux ; WCAG 2.2 AA ainsi qu'une CSP et une SRI strictes imposées comme barrières de compilation ; et des îlots dynamiques en bac à sable, le tout dans un unique binaire Rust à sûreté mémoire. Chaque proposition de cet énoncé correspond à un élément précis de la feuille de route ci-dessus plutôt qu'à une intention marketing.

---

## Intégration réglementaire et conformité

Dans les secteurs d'entreprise et financiers à enjeux élevés, un logiciel est évalué au prisme de la conformité et du capital de risque. La feuille de route architecturale de `static-site-generator` s'aligne directement sur des obligations réglementaires majeures :

- **DORA article 6 (gestion du risque TIC) :** le calcul et l'injection à la compilation des empreintes SRI SHA-384 et de politiques de sécurité du contenu strictes répondent à l'exigence de protéger les canaux de publication numérique contre l'injection dans la chaîne d'approvisionnement, la défiguration web et les vecteurs de script intersite (XSS).  
- **DORA article 7 (résilience des systèmes TIC) :** en passant à des actifs statiques immuables et vérifiés à la compilation, les institutions financières éliminent les vulnérabilités des bases de données et des serveurs d'exécution, abaissant le multiplicateur de risque opérationnel et réduisant les réserves de capital de risque requises au titre de Bâle III.  
- **Loi européenne sur l'accessibilité (EAA), directive (UE) 2019/882 :** déplacer l'audit d'accessibilité en amont, dans le pipeline de compilation en tant que barrière de compilation ferme, garantit une conformité à 100 % avant tout déploiement, écartant le risque d'atteinte à la marque et de contentieux civil au titre de l'EAA et du Titre III de l'ADA.  
- **RGPD article 25 (protection des données dès la conception) :** exécuter le pipeline de traduction et de métadonnées sur du matériel local, isolé du réseau, maintient les brouillons propriétaires, les indicateurs financiers et les données personnelles hors des fournisseurs LLM de cloud tiers publics, soutenant la conformité aux principes de souveraineté des données.

---

## Foire aux questions

**Que livre réellement la version 0.0.41 aujourd'hui, par rapport à ce qu'annonce le README ?**
Le modèle de sécurité et d'accessibilité est réel et imposé dans le code : `forbid(unsafe_code)` à l'échelle de l'espace de travail, génération de SRI SHA-256/384, extraction de CSP, versions signées avec attestation Sigstore et SBOM CycloneDX, ainsi qu'une barrière WCAG 2.2 AA qui arrête la construction. Trois fonctionnalités documentées ne sont pas fonctionnelles en v0.0.41. Le `MinifyPlugin` est un réducteur d'espaces plutôt qu'un minifieur conscient de la syntaxe ; le `DepGraph` censé piloter les constructions incrémentales est compilé mais jamais renseigné dans le code de production ; et l'encodage AVIF est une ébauche dont `avif_variants` retourne un vecteur vide.

**La barrière d'accessibilité est-elle une véritable barrière de compilation ou un linter post-construction ?**
C'est une barrière de compilation. Les contrôles WCAG 2.2 AA s'exécutent au sein du pipeline de compilation via un analyseur axe-core à la compilation piloté par Playwright, et une page en échec arrête la compilation avec des erreurs indiquant le numéro de ligne exact plutôt que d'émettre un avertissement après coup. C'est précisément la propriété qu'exige une obligation au titre de la loi européenne sur l'accessibilité : une sortie non conforme ne peut pas atteindre le déploiement.

**Pourquoi l'appel de `curl` en sous-processus dans le plugin LLM importe-t-il ?**
Le pipeline LLM local (`src/plugins/llm.rs`) invoque le binaire `curl` de l'hôte pour joindre les points d'accès locaux. Cela couple la construction à un exécutable de l'hôte, échoue sur les systèmes sans `curl` dans le PATH, introduit une surface d'injection shell et casse en intégration continue isolée du réseau. Faire migrer l'appel vers un client HTTP Rust tel que `ureq` supprime la dépendance externe et le vecteur d'injection, ce qui explique pourquoi il s'agit du deuxième point du correctif 0.0.42.

**Quel est l'élément le plus important sur la route vers la 1.0 ?**
Renseigner le `DepGraph` et relier l'option `--incremental`. Les constructions incrémentales constituent l'écart de crédibilité entre le moteur documenté et le moteur réel, et toute affirmation en aval sur des constructions inférieures à la seconde à plus de 100 000 pages dépend de la capacité du graphe de dépendances à suivre les arêtes gabarit-vers-page et markdown-vers-page plutôt que de rester une infrastructure réservée aux tests.

## Références

- [Cloudflare, *lol-html : réécrivain HTML en flux à faible latence de sortie*](https://github.com/cloudflare/lol-html "Cloudflare lol-html — réécrivain HTML en flux") ⧉. [Le réécrivain HTML en flux, sans copie, proposé pour remplacer la manipulation de chaînes fragile en phase 0.1.0.]
- [W3C, *Règles pour l'accessibilité des contenus web (WCAG) 2.2*](https://www.w3.org/TR/WCAG22/ "W3C — Recommandation WCAG 2.2") ⧉. [Les critères de succès de niveau AA imposés par la barrière d'accessibilité à la compilation.]
- [Union européenne, *Règlement (UE) 2022/2554 (DORA)*](https://eur-lex.europa.eu/eli/reg/2022/2554/oj "EUR-Lex — Règlement sur la résilience opérationnelle numérique") ⧉. [Les articles de gestion du risque TIC et de résilience auxquels la posture de sécurité correspond.]
- [OpenSSF, *Supply-chain Levels for Software Artifacts (SLSA) v1.0*](https://slsa.dev/spec/v1.0/ "SLSA — spécification v1.0") ⧉. [Le cadre de provenance de construction visé pour une attestation de niveau 3 vérifiable à la 1.0.]
- [Armin Ronacher, *Moteur de gabarits MiniJinja*](https://github.com/mitsuhiko/minijinja "MiniJinja — moteur Jinja2 minimal pour Rust") ⧉. [Le moteur à faibles dépendances qui a remplacé Tera et allégé l'arbre transitif.]
- [CycloneDX, *Spécification de la nomenclature logicielle (SBOM) v1.5*](https://cyclonedx.org/docs/1.5/ "CycloneDX — spécification SBOM v1.5") ⧉. [Le format de SBOM émis à chaque construction pour l'audit de la chaîne d'approvisionnement.]
- [Union européenne, *Directive (UE) 2019/882 (loi européenne sur l'accessibilité)*](https://eur-lex.europa.eu/eli/dir/2019/882/oj "EUR-Lex — Loi européenne sur l'accessibilité") ⧉. [L'obligation d'accessibilité que la barrière WCAG à la compilation est conçue pour satisfaire.]

*Dernière relecture en juillet 2026. Analyse d'origine fondée sur l'inspection du code de `static-site-generator` en v0.0.41 ; les sources sont citées, non reproduites. Les numéros de version et l'état des fonctionnalités évoluent rapidement : vérifiez dans le dépôt avant toute republication. Sous licence CC-BY-4.0.*

