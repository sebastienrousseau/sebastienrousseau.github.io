---
author: "contact@sebastienrousseau.com (Sebastien Rousseau)"
banner_alt: "Un fondo técnico abstracto que representa la hoja de ruta arquitectónica de un generador de sitios estáticos de nivel empresarial."
banner_height: "1280"
banner_width: "1920"
banner: "https://cloudcdn.pro/stocks/images/gemini-background.webp"
cdn: "https://cloudcdn.pro"
charset: "UTF-8"
cname: "sebastienrousseau.com"
copyright: "© Copyright 2025 - 2026 - Sebastien Rousseau. All rights reserved."
date: "July 22, 2026"
description: "Análisis a fondo de un generador de sitios estáticos en Rust: seguridad en compilación, barreras WCAG, IA local, carencias de la v0.0.41 y hoja de ruta a 1.0."
format-detection: "telephone=no"
hreflang: "es"
icon: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
id: "https://sebastienrousseau.com/es/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
image_alt: "Retrato en blanco y negro de Sebastien Rousseau"
image_height: "162"
image_width: "162"
image: "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp"
keywords: "generador de sitios estáticos, Rust, forbid unsafe_code, WCAG 2.2 AA, Content Security Policy, Subresource Integrity, SLSA, CycloneDX SBOM, pipeline de LLM local, DORA, compilaciones incrementales, lol_html, entorno aislado para complementos WASM, búsqueda vectorial semántica, MiniJinja, Ollama"
language: "es"
last_reviewed: "2026-07-22"
layout: "report"
locale: "es_ES"
logo_alt: "Logotipo de Sebastien Rousseau"
logo_height: "44"
logo_width: "44"
logo: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
menu: ""
measurementID: "G-169G4ET5HQ"
name: "Sebastien Rousseau"
permalink: "https://sebastienrousseau.com/es/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
rating: "general"
referrer: "no-referrer"
robots: "index, follow"
schema: "FAQPage, Article"
seo_title: "Generador de sitios estáticos: el camino hacia la 1.0"
short_name: "sebastienrousseau"
subtitle: "Auditoría arquitectónica y hoja de ruta de un generador de sitios estáticos en Rust concebido como infraestructura segura por defecto: lo que la v0.0.41 entrega realmente frente a lo que promete el README, cinco capacidades empresariales ausentes y un camino por fases hacia una 1.0 alineada con DORA y la EAA."
tags: "generador de sitios estáticos, Rust, seguridad web, accesibilidad, DORA, cadena de suministro, SLSA, IA local, WCAG, compilación, hoja de ruta, empresa"
theme-color: "0, 83, 191"
title: "Generador de sitios estáticos (SSG): análisis y hoja de ruta a 1.0"
url: "https://sebastienrousseau.com/es/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap/rss.xml"
category: "Technology"
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.26)"
item_description: "Análisis a fondo de un generador de sitios estáticos en Rust: seguridad en compilación, barreras WCAG, IA local, carencias de la v0.0.41 y hoja de ruta a 1.0."
item_guid: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap/rss.xml"
item_link: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap/rss.xml"
item_pub_date: "Wed, 22 Jul 2026 07:07:07 +0000"
item_title: "Generador de sitios estáticos (SSG): análisis y hoja de ruta a 1.0"
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
apple-mobile-web-app-title: "SSG: rumbo a la 1.0"
apple-touch-fullscreen: "yes"
msapplication-navbutton-color: "0, 83, 191"
twitter_card: "summary_large_image"
twitter_creator: "@wwdseb"
twitter_description: "Barreras WCAG en compilación, SRI SHA-384, inyección de CSP y un LLM local distinguen a este motor en Rust. Análisis honesto de la v0.0.41 y su camino a la 1.0."
twitter_image: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
twitter_image_alt: "Logotipo de Sebastien Rousseau"
twitter_site: "@wwdseb"
twitter_title: "Generador de sitios estáticos: el camino hacia la 1.0"
twitter_url: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
excerpt: "Barreras WCAG en compilación, SRI SHA-384 y LLM local distinguen a este motor en Rust; compilaciones incrementales, minificación nativa y AVIF siguen pendientes."
author_website: "https://sebastienrousseau.com"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "¡Gracias por leer!"
site_last_updated: "2026-07-22"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "Kaishi, Kaishi Builder, Kaishi CLI, Kaishi Templates, Kaishi Themes"
---

# Generador de sitios estáticos (SSG): análisis estratégico integral y hoja de ruta arquitectónica de nivel empresarial

*Fecha de investigación: 2026-06-22. Basado en la inspección del código de `static-site-generator` en la v0.0.41 y en investigación web del ecosistema de los SSG en 2026.*

**Para un editor regulado, un generador de sitios estáticos ya no es una herramienta de diseño; forma parte del perímetro de riesgo operativo.** El [static-site-generator](https://github.com/sebastienrousseau/static-site-generator) de código abierto escrito en Rust parte de esa premisa: traslada la seguridad, la accesibilidad, la internacionalización y los pipelines de contenido con IA al momento de compilación, de modo que una comprobación fallida detiene la compilación en lugar de llegar a producción. Este análisis separa lo que la versión 0.0.41 entrega realmente de lo que su documentación todavía solo promete, expone cinco capacidades empresariales de las que aún carece y propone un camino por fases hacia una versión 1.0 alineada con DORA, la Ley Europea de Accesibilidad y los estándares modernos de cadena de suministro.

<!-- lead-start -->
<aside class="post-lead" aria-label="Resumen del artículo">
<p class="post-lead-tldr"><strong>TL;DR.</strong> El <code>static-site-generator</code> escrito en Rust trata la publicación web como un pipeline de software auditable y seguro por defecto: <code>forbid(unsafe_code)</code> en todo el espacio de trabajo, Subresource Integrity con SHA-384, extracción de Content Security Policy, una barrera WCAG 2.2 AA en compilación y un pipeline de LLM local. Una inspección del código de la v0.0.41 muestra que varias funciones documentadas siguen siendo aspiraciones: la minificación nativa, las recompilaciones incrementales y AVIF, entre ellas. Este es el análisis honesto de carencias y una hoja de ruta por fases hacia una 1.0 de nivel empresarial.</p>
<p class="post-lead-heading"><strong>Puntos clave</strong></p>
<ul class="post-lead-takeaways">
  <li><strong>El modelo de seguridad y accesibilidad es real.</strong> La SRI en compilación, la extracción de CSP, las versiones firmadas con atestación de Sigstore y los SBOM de CycloneDX, más una barrera WCAG 2.2 AA que detiene la compilación, están implementados en código, no solo documentados.</li>
  <li><strong>Varias funciones destacadas no lo son.</strong> El minificador es un compactador de espacios en blanco, el grafo de dependencias que impulsaría las compilaciones incrementales nunca se rellena en producción y la codificación AVIF es un esbozo que devuelve un vector vacío.</li>
  <li><strong>Faltan cinco capacidades empresariales.</strong> El aislamiento de complementos WASM en un entorno aislado, un reescritor de HTML en streaming y sin copias, la búsqueda semántica local, el almacenamiento en caché determinista de inferencias y la E/S de archivos asíncrona.</li>
  <li><strong>La hoja de ruta se ordena por riesgo.</strong> Un parche de corrección (0.0.42), una versión menor de credibilidad e incrementalidad (0.1.0) y luego una versión mayor empresarial (1.0.0) que incorpora el entorno aislado, la búsqueda semántica y la procedencia SLSA v1.1.</li>
</ul>
<p class="post-lead-related"><strong>Lecturas relacionadas:</strong> <a href="https://sebastienrousseau.com/2026-07-03-emerging-technology-risk-horizon-banks-2026">El horizonte de riesgo de las tecnologías emergentes para los bancos</a>, <a href="https://sebastienrousseau.com/2026-07-07-corporate-banking-api-standard-agentic-mcp-2026">Un estándar de API de banca corporativa para el MCP agéntico</a>.</p>
</aside>
<!-- lead-end -->

> **Resumen ejecutivo**
>
> - **La publicación es ahora un perímetro de riesgo operativo.** Bajo DORA, la Ley Europea de Accesibilidad y el RGPD, todo activo público es un posible punto de entrada para el compromiso de la cadena de suministro, la desfiguración y la exposición regulatoria. Un modelo en compilación estrecha ese perímetro al rechazar la salida no conforme antes de su publicación.
> - **Los factores diferenciales del motor los impone el compilador, no son aspiraciones documentadas.** El `forbid(unsafe_code)` en todo el espacio de trabajo, la SRI SHA-256/384 real, la extracción automática de CSP y una barrera WCAG 2.2 AA en compilación convierten la seguridad y la accesibilidad de auditorías a posteriori en fallos de compilación tajantes.
> - **La versión 0.0.41 tiene una brecha entre documentación y código.** La minificación nativa, las recompilaciones incrementales mediante un grafo de dependencias y la compatibilidad con AVIF se describen pero no funcionan; el artículo señala cada carencia frente a su ubicación exacta en el código.
> - **El camino hacia la 1.0 es una secuencia, no una lista de deseos.** Primero la robustez (0.0.42), después la corrección incremental (0.1.0) y por último las capacidades empresariales que exige un comprador regulado: aislamiento WASM, búsqueda semántica local y procedencia SLSA verificable (1.0.0).

## Fortalezas actuales

El código de `static-site-generator` presenta varias decisiones de ingeniería distintivas que lo separan de los motores heredados en JavaScript y Go:

- **Postura de seguridad en compilación:** El `#![forbid(unsafe_code)]` en todo el espacio de trabajo aporta garantías de seguridad de memoria en compilación. El pipeline de compilación genera hashes reales de Subresource Integrity (SRI) SHA-256/SHA-384 (`src/plugins/assets.rs`) y realiza una extracción automática de Content Security Policy (CSP) que elimina los scripts y estilos unsafe-inline. Las versiones se firman, llevan atestación de Sigstore y producen un SBOM CycloneDX 1.5 en cada compilación.  
- **Barrera de accesibilidad impuesta por el compilador:** Las comprobaciones de las Pautas de Accesibilidad para el Contenido Web (WCAG) 2.2 nivel AA se ejecutan dentro del pipeline de compilación mediante un analizador axe-core en compilación gobernado por Playwright. La accesibilidad se convierte en una barrera de compilación tajante en vez de una auditoría posterior a la publicación: si una página falla, la compilación se detiene con errores que indican el número exacto de línea.  
- **Pipeline de IA con soberanía de datos:** Un pipeline local de traducción y extracción de metadatos con LLM (a través de endpoints locales de Ollama o llama.cpp) permite a una institución automatizar el resumen de contenido, la generación de esquemas JSON-LD y la traducción multilingüe sin enviar divulgaciones previas a resultados ni propiedad intelectual sensible a las API de IA de la nube pública.  
- **Compilación paralelizada:** Las garantías de seguridad de memoria de Rust sustentan un pipeline de HTML y activos paralelizado y gobernado por Rayon (`src/core/pipeline.rs`). El pipeline de complementos ejecuta transformaciones fusionadas, con `SearchPlugin`, `SeoPlugin`, `CanonicalPlugin` y `JsonLdPlugin` operando sobre `par_iter()`, de modo que cada página se lee y se escribe en disco una sola vez.  
- **Higiene de la cadena de suministro y de dependencias:** Migrar el motor de plantillas de Tera a MiniJinja (`v0.0.37`) redujo el tamaño del binario, eliminó dependencias transitivas como `rand` en compilación y produjo una huella de dependencias compacta que reduce la exposición de la cadena de suministro de software.

---

## Carencias y realidades prácticas

A pesar de estas fortalezas excepcionales, una inspección rigurosa del código de la v0.0.41 revela varias carencias arquitectónicas, funcionales y de experiencia de desarrollo entre lo que afirma su documentación y el código Rust real:

### Carencias arquitectónicas

- **Compactación de espacios frente a minificación nativa:** Aunque el README promete «minificación nativa de JS/CSS», el `MinifyPlugin` (`src/plugins/plugins.rs:96-116`) actúa apenas como un compactador ingenuo de espacios en blanco. Se cortocircuita en los elementos `<pre>` y colapsa las secuencias de espacios en el HTML, pero no realiza una minificación nativa de CSS o JS consciente de la sintaxis. Además, solo procesa las páginas de nivel superior y no recorre recursivamente los subdirectorios (como `/blog/` o `/tags/`), dejando sin minificar las páginas profundas.  
- **Infraestructura incremental muerta:** El grafo de seguimiento de dependencias (`DepGraph` en `src/core/depgraph.rs`) se compila y se carga en `PluginContext.dep_graph`, pero nunca se rellena en el código de producción. El método `add_dep()` solo se invoca en las pruebas unitarias, lo que convierte en aspiración la afirmación del README sobre «recompilaciones incrementales mediante grafos de dependencias».  
- **Compilación por lotes frente a compilación en streaming:** El módulo `streaming::compile_batch` (`src/core/streaming.rs`) no transmite realmente. En su lugar, compila las páginas por lotes en un directorio temporal, ejecuta `staticdatagen::compile` desde cero para cada lote y fusiona las salidas. Esto genera una sobrecarga considerable de E/S de disco y un análisis redundante, alejándose de una arquitectura de streaming genuina.  
- **Violaciones de fase en el ciclo de vida de los complementos:** Los complementos que generan páginas HTML nuevas durante la compilación, como `TaxonomyPlugin`, `PaginationPlugin` e `I18nPlugin`, escriben directamente en disco en `after_compile` en lugar de usar el ciclo de vida `transform_html`. En consecuencia, las páginas generadas por estos complementos eluden complementos críticos de posprocesamiento (como `CanonicalPlugin`, `JsonLdPlugin`, `RobotsPlugin` y `AccessibilityPlugin`) si dichos complementos se registraron antes. Esto deja las páginas de etiquetas, categorías y paginación sin enlaces canónicos correctos, sin esquemas JSON-LD ni validaciones de accesibilidad.  
- **Invocación de `curl` desde el shell en `LlmPlugin`:** El pipeline local de contenido con LLM (`src/plugins/llm.rs`) invoca directamente el binario `curl` del host para consultar los endpoints locales. Esto introduce errores graves entre plataformas (por ejemplo, en hosts Windows sin curl en el PATH), plantea un riesgo de seguridad (vectores de inyección de shell) y falla en entornos de CI bloqueados o aislados de la red.  
- **Manipulación ingenua de cadenas en la reescritura de HTML:** Los extractores `image_plugin.rs` y `search.rs` reescriben cadenas HTML mediante operaciones frágiles `str::find` y `str::rfind`. Este enfoque es muy vulnerable a etiquetas HTML rotas, etiquetas `<img>` dentro de comentarios, entidades de caracteres en el texto alternativo o propiedades `srcset` preexistentes, lo que puede corromper la salida.  
- **Compatibilidad con AVIF sin implementar:** Aunque la codificación de imágenes AVIF está ampliamente documentada, la implementación en `image_plugin.rs` es un esbozo donde `avif_variants` simplemente devuelve `Vec::new()`, lo que deja la función sin funcionar.  
- **Observador basado en sondeo:** El observador del servidor de desarrollo local (`src/server/watch.rs`) usa sondeo en lugar de las API de eventos del sistema de archivos, lo que provoca un uso excesivo de CPU en reposo y una latencia de modificación inferior al segundo.

### Carencias funcionales y de experiencia de desarrollo

- **Sin seguimiento de dependencias transitivas:** El grafo de dependencias no puede rastrear dependencias anidadas (por ejemplo, cambios en una subplantilla que afectan a una maquetación que afecta a una página), como verifica la prueba unitaria `transitive_not_tracked`.  
- **Sin indicador de CLI para compilación incremental:** No existe un indicador `--incremental` de la CLI conectado al compilador de ejecución, lo que impide a los desarrolladores usar compilaciones en caché.  
- **La HMR se limita a CSS:** La sustitución de módulos en caliente (HMR) solo admite CSS; cualquier modificación de HTML, maquetaciones o archivos markdown desencadena una recarga completa de la página, lo que degrada la velocidad de desarrollo.  
- **Déficit de subcomandos:** Los desarrolladores deben pasar manualmente indicadores prolijos (`ssg -s public -w`) porque no existen subcomandos estándar como `ssg dev`, `ssg build`, `ssg check` y `ssg lint`.

---

## Carencias arquitectónicas que nos faltan (nuevos hallazgos)

Más allá de las carencias de la v0.0.41, evaluar el proyecto frente a un perfil de riesgo de grado financiero saca a la luz varias capacidades que aún no ofrece pero que un comprador empresarial exigiría:

### 1. Aislamiento de complementos en WebAssembly (extensión de confianza cero)

Aunque el propio binario del compilador está escrito en Rust seguro, permitir que complementos de terceros arbitrarios se ejecuten de forma nativa en los sistemas host introduce una vulnerabilidad grave en la cadena de suministro. Un complemento de terceros comprometido podría acceder con facilidad al sistema de archivos del host, leer archivos Markdown propietarios o exfiltrar credenciales privadas.

* **Capacidad ausente:** Un entorno de ejecución aislado. Para lograr una compilación de confianza cero, el compilador debería ejecutar los complementos de terceros dentro de un entorno de ejecución de WebAssembly embebido (como `wasmtime`). Los complementos deberían interactuar con el host únicamente a través de una Interfaz de Sistema de WebAssembly (WASI) restringida, limitando su acceso estrictamente a la página que se transforma.

### 2. Análisis de HTML sin copias mediante AST en streaming (`lol_html`)

Migrar la capa de análisis de HTML a una biblioteca DOM completa en memoria (como Kuchiki o html5ever) introduce una sobrecarga de memoria considerable y pausas de procesamiento al gestionar sitios con más de 100 000 páginas.

* **Capacidad ausente:** Un reescritor de HTML en streaming y sin copias. Emplear el `lol_html` de Cloudflare (reescritor de HTML de baja latencia de salida) permite al compilador analizar, inspeccionar y modificar elementos HTML en una única pasada en streaming con una asignación de memoria casi nula, a la altura del objetivo de compilaciones inferiores al segundo del compilador paralelo en streaming.

### 3. Búsqueda vectorial semántica local (RAG local)

El índice de búsqueda actual (`SearchPlugin`) genera un índice JSON pesado y plano que realiza coincidencias de cadenas sencillas del lado del cliente, sin admitir búsqueda difusa, lematización ni consultas semánticas. Pagefind es una mejora, pero sigue dependiendo de la descarga de un índice grande.

* **Capacidad ausente:** Búsqueda semántica embebida. El compilador debería aprovechar un modelo local y ligero de incrustaciones vectoriales nativo de Rust (como un modelo MiniLM-L6 ejecutado mediante `candle` u `ort` / ONNX Runtime) en compilación. Debería generar incrustaciones vectoriales densas para cada párrafo de página y producir un índice vectorial compacto. El widget de búsqueda del lado del cliente, compilado a WASM, puede entonces realizar una búsqueda semántica sin conexión real directamente en el navegador.

### 4. Traducción determinista y almacenamiento en caché de inferencias

Como la inferencia local con LLM (por ejemplo, mediante Ollama o Llama.cpp) es muy intensiva en CPU/GPU, traducir o generar metadatos para miles de páginas en cada compilación resulta computacionalmente prohibitivo.

* **Capacidad ausente:** Almacenamiento en caché de inferencias basado en el hash del contenido. El compilador debe mantener una caché determinista de todas las operaciones de LLM. Si el hash SHA-256 del contenido de un archivo markdown y sus parámetros de traducción coinciden con una entrada de la caché, el compilador debería reutilizar la traducción y los metadatos en caché, evitando la inferencia local redundante.

### 5. E/S de archivos asíncrona para el escalado paralelo

Aunque el pipeline de complementos está paralelizado mediante Rayon, las escrituras síncronas estándar en disco bloquean los hilos del sistema operativo de Rayon, creando un cuello de botella de E/S al escribir decenas de miles de páginas.

* **Capacidad ausente:** E/S de disco asíncrona y no bloqueante. El compilador debería desacoplar las tareas intensivas en CPU (análisis de Markdown, minificación) de las escrituras ligadas al disco, usando grupos de hilos de E/S asíncrona o los enlaces `io_uring` de Linux (mediante `rio` o `tokio`) para escribir las páginas compiladas en paralelo sin bloquear los ejecutores paralelos de CPU.

---

## La hoja de ruta estratégica hacia la 1.0

La siguiente hoja de ruta integra tanto las carencias resueltas como las capacidades de nivel empresarial recién descubiertas en un marco de versiones estructurado y cronológico.

### Fase 1: 0.0.42 (el parche de robustez y corrección, de 1 a 2 semanas)

1. **Reconstruir `MinifyPlugin`:** Integración de `minify-html`, `oxc_minifier` y `lightningcss` para una minificación nativa de HTML, JS y CSS consciente de la sintaxis. Asegurar que el complemento recorra recursivamente todos los directorios anidados bajo `site_dir`.  
2. **Asegurar el pipeline de IA:** Portar `LlmPlugin` de las invocaciones nativas de `curl` desde el shell a `ureq` (un cliente HTTP en Rust ligero, síncrono y seguro) para garantizar la compatibilidad entre plataformas y eliminar las vulnerabilidades de inyección de shell.  
3. **Completar la implementación de AVIF:** Conectar `ravif` directamente al pipeline de activos de imagen, habilitando una codificación AVIF de alto rendimiento junto a WebP y PNG.  
4. **Automatizar el HrefLang y el mapeo multilocalización:** Detectar automáticamente las páginas traducidas paralelas en las compilaciones multilingües e inyectar etiquetas estándar y conformes con Google `<link rel="alternate" hreflang="..." />` en la cabecera de cada archivo HTML compilado.  
5. **Compatibilidad con JSON Feed 1.1:** Publicar un emisor de JSON Feed 1.1 dedicado junto a los canales de sindicación estándar RSS 2.0 y Atom 1.0.

### Fase 2: 0.1.0 (la versión menor de credibilidad e incrementalidad, de 2 a 3 meses)

1. **Rellenar `DepGraph` y habilitar `--incremental`:** Conectar por completo `DepGraph` para rastrear las dependencias de plantilla a página y de markdown a página. Implementar una capa de invalidación de caché y conectar el indicador `--incremental` de la CLI, con el objetivo de recompilaciones inferiores a 200 ms en entornos de caché caliente.  
2. **Reescritura del AST en streaming mediante `lol_html`:** Sustituir la frágil reescritura de cadenas en `image_plugin.rs`, `search.rs` y las inyecciones de CSP por un reescritor de HTML en streaming y sin copias impulsado por `lol_html`.  
3. **Observador orientado a eventos y HMR de componentes:** Portar el módulo de observación del sondeo al crate `notify` orientado a eventos, e implementar una recarga en caliente solo de CSS y de HTML parcial para actualizaciones del navegador inferiores a 100 ms.  
4. **CLI de comandos unificada:** Rediseñar la interfaz del compilador para admitir subcomandos estándar: `ssg dev`, `ssg build`, `ssg check` (auditoría de accesibilidad/SEO) y `ssg deploy`.  
5. **Caché de inferencias determinista:** Implementar una capa de almacenamiento en caché basada en el hash del contenido para todas las tareas locales de traducción, resumen y extracción de metadatos con LLM.

### Fase 3: 1.0.0 (la versión mayor empresarial y de producción, de 6 a 12 meses)

1. **Aislamiento de complementos WASM de confianza cero:** Embeber un entorno de ejecución de WebAssembly (`wasmtime` o `wasmer`) para ejecutar complementos de terceros en un entorno totalmente aislado con acceso al sistema de archivos y a la red basado en capacidades.  
2. **Búsqueda vectorial semántica local (RAG local):** Embeber un modelo de incrustaciones local nativo de Rust (mediante `candle` u `ort`) para compilar incrustaciones densas de párrafos en un índice compacto, habilitando una búsqueda semántica privada del lado del cliente.  
3. **Islas de servidor y objetivo WASM en el borde:** Implementar la ejecución de componentes `<ssg-island>` en entornos de ejecución en el borde (como Cloudflare Workers, Vercel Edge o Netlify Edge) construidos sobre el núcleo compilado `ssg-wasm`.  
4. **Motor de E/S paralela asíncrona:** Rediseñar el módulo de escritura del sistema de archivos para usar grupos de hilos de E/S asíncrona y enlaces `io_uring`, eliminando los bloqueos de los trabajadores de CPU durante las escrituras en paralelo.  
5. **Procedencia de compilación SLSA v1.1 y conformidad con SPDX 3.0:** Proporcionar una procedencia de compilación SLSA nivel 3 verificable matemáticamente y generar SBOM conformes con SPDX 3.0, satisfaciendo por completo los estándares modernos de seguridad de la cadena de suministro de software.

---

## Matriz de competidores (ecosistema de 2026)

La siguiente matriz compara `static-site-generator` (objetivo v1.0) con los principales motores de publicación web de 2026:

| Capacidad | static-site-generator v1.0 | Hugo v0.155+ | Zola v0.19+ | Astro 5 | Eleventy 3 |
| ---- | ---- | ---- | ---- | ---- | ---- |
| **Lenguaje / runtime** | Rust (cero unsafe) | Go | Rust | JS (Node/V8) | JS (Node/V8) |
| **Barrera de accesibilidad en compilación** | Validación de AST en compilación | Ninguna | Ninguna | Linter posterior a la compilación | Linter posterior a la compilación |
| **Endurecimiento de seguridad** | SRI SHA-384 e inyección de CSP | Manual | Manual | Manual | Manual |
| **Seguridad de la cadena de suministro** | SLSA L3 \+ SPDX 3.0 \+ entorno aislado WASM | Mínima | Mínima | Árbol NPM pesado | Árbol NPM pesado |
| **Pipeline de contenido con IA** | Privado, local primero (LLM local) | Ninguno | Ninguno | Solo API pública | Solo API pública |
| **Velocidad incremental** | \<200 ms (caché caliente) | \<100 ms | \<150 ms | \~1,5 s | \~140 ms |
| **Interactividad dinámica** | Islas de servidor (objetivos WASM) | Ninguna | Ninguna | Islas de servidor (JS) | Islas (JS) |
| **Motor de búsqueda** | Búsqueda semántica WASM local | Cadenas simples | Cadenas simples | Pagefind (JS) | Pagefind (JS) |

---

## Posicionamiento en la 1.0

En la 1.0, el posicionamiento previsto es el de un generador de sitios estáticos diseñado como infraestructura de software segura por defecto: creación de contenido apoyada por pipelines de IA local primero; compilación de más de 100 000 páginas mediante un pipeline paralelo en streaming; WCAG 2.2 AA y una CSP y una SRI estrictas impuestas como barreras de compilación; e islas dinámicas aisladas, todo dentro de un único binario de Rust con seguridad de memoria. Cada cláusula de esa afirmación se corresponde con un elemento concreto de la hoja de ruta anterior y no con una aspiración de marketing.

---

## Integración normativa y de cumplimiento

En los sectores empresariales y financieros de alto riesgo, el software se evalúa a través del prisma del cumplimiento y del capital de riesgo. La hoja de ruta arquitectónica de `static-site-generator` se alinea directamente con los principales mandatos regulatorios:

- **DORA, artículo 6 (gestión del riesgo de las TIC):** El cálculo y la inyección en compilación de los hashes SRI SHA-384 y de las Content Security Policies estrictas satisfacen el requisito de proteger los canales de publicación digital frente a la inyección en la cadena de suministro, la desfiguración web y los vectores de scripting entre sitios (XSS).  
- **DORA, artículo 7 (resiliencia de los sistemas de TIC):** Al pasar a activos estáticos inmutables y verificados en compilación, las entidades financieras eliminan las vulnerabilidades de las bases de datos y de los servidores en tiempo de ejecución, reduciendo el multiplicador de riesgo operativo y las reservas de capital de riesgo exigidas por Basilea III.  
- **Directiva (UE) 2019/882 sobre la Ley Europea de Accesibilidad (EAA):** Desplazar la auditoría de accesibilidad hacia la izquierda, hacia el pipeline de compilación como barrera de compilación tajante, garantiza el 100 % de cumplimiento antes del despliegue, eliminando el riesgo de daño reputacional y de litigio civil bajo la EAA y el título III de la ADA.  
- **RGPD, artículo 25 (protección de datos desde el diseño):** Ejecutar el pipeline de traducción y metadatos en hardware local aislado de la red mantiene los borradores propietarios, las métricas financieras y los datos personales fuera de los proveedores públicos de LLM en la nube de terceros, lo que respalda el cumplimiento de los principios de soberanía de datos.

---

## Preguntas frecuentes

**¿Qué entrega realmente la versión 0.0.41 hoy, frente a lo que afirma el README?**
El modelo de seguridad y accesibilidad es real y está impuesto en código: `forbid(unsafe_code)` en todo el espacio de trabajo, generación de SRI SHA-256/384, extracción de CSP, versiones firmadas con atestación de Sigstore y un SBOM de CycloneDX, y una barrera WCAG 2.2 AA que detiene la compilación. Tres funciones documentadas no funcionan en la v0.0.41. El `MinifyPlugin` es un compactador de espacios en blanco en vez de un minificador consciente de la sintaxis; el `DepGraph` que impulsaría las recompilaciones incrementales se compila pero nunca se rellena en el código de producción; y la codificación AVIF es un esbozo cuyo `avif_variants` devuelve un vector vacío.

**¿La barrera de accesibilidad es una barrera de compilación real o un linter posterior a la compilación?**
Es una barrera de compilación. Las comprobaciones WCAG 2.2 AA se ejecutan dentro del pipeline de compilación mediante un analizador axe-core en compilación gobernado por Playwright, y una página que falla detiene la compilación con errores que indican el número exacto de línea en lugar de emitir una advertencia a posteriori. Esa es la propiedad que necesita una obligación de la Ley Europea de Accesibilidad: la salida no conforme no puede llegar al despliegue.

**¿Por qué importa invocar `curl` desde el shell en el complemento de LLM?**
El pipeline local de LLM (`src/plugins/llm.rs`) invoca el binario `curl` del host para alcanzar los endpoints locales. Eso acopla la compilación a un ejecutable del host, falla en sistemas sin `curl` en el PATH, introduce una superficie de inyección de shell y se rompe en la CI aislada de la red. Portar la llamada a un cliente HTTP de Rust como `ureq` elimina la dependencia externa y el vector de inyección, y por eso es el segundo elemento del parche 0.0.42.

**¿Cuál es el elemento más importante en el camino hacia la 1.0?**
Rellenar el `DepGraph` y conectar el indicador `--incremental`. Las recompilaciones incrementales son la brecha de credibilidad entre el motor documentado y el real, y toda afirmación posterior sobre compilaciones inferiores al segundo con más de 100 000 páginas depende de que el grafo de dependencias rastree las aristas de plantilla a página y de markdown a página en lugar de seguir siendo infraestructura solo para pruebas.

## Referencias

- [Cloudflare, *lol-html: reescritor de HTML en streaming de baja latencia de salida*](https://github.com/cloudflare/lol-html "Cloudflare lol-html: reescritor de HTML en streaming") ⧉. [El reescritor de HTML en streaming y sin copias propuesto para sustituir la frágil manipulación de cadenas en la fase 0.1.0.]
- [W3C, *Pautas de Accesibilidad para el Contenido Web (WCAG) 2.2*](https://www.w3.org/TR/WCAG22/ "W3C: Recomendación WCAG 2.2") ⧉. [Los criterios de conformidad de nivel AA que impone la barrera de accesibilidad en compilación.]
- [Unión Europea, *Reglamento (UE) 2022/2554 (DORA)*](https://eur-lex.europa.eu/eli/reg/2022/2554/oj "EUR-Lex: Ley de Resiliencia Operativa Digital") ⧉. [Los artículos de gestión del riesgo y de resiliencia de las TIC a los que se corresponde la postura de seguridad.]
- [OpenSSF, *Niveles de Cadena de Suministro para Artefactos de Software (SLSA) v1.0*](https://slsa.dev/spec/v1.0/ "SLSA: especificación v1.0") ⧉. [El marco de procedencia de compilación cuya atestación verificable de nivel 3 se busca en la 1.0.]
- [Armin Ronacher, *motor de plantillas MiniJinja*](https://github.com/mitsuhiko/minijinja "MiniJinja: motor Jinja2 mínimo para Rust") ⧉. [El motor ligero en dependencias que sustituyó a Tera y recortó el árbol transitivo.]
- [CycloneDX, *especificación de la Lista de Materiales de Software v1.5*](https://cyclonedx.org/docs/1.5/ "CycloneDX: especificación de SBOM v1.5") ⧉. [El formato de SBOM emitido en cada compilación para la auditoría de la cadena de suministro.]
- [Unión Europea, *Directiva (UE) 2019/882 (Ley Europea de Accesibilidad)*](https://eur-lex.europa.eu/eli/dir/2019/882/oj "EUR-Lex: Ley Europea de Accesibilidad") ⧉. [La obligación de accesibilidad que la barrera WCAG en compilación está diseñada para satisfacer.]

*Última revisión: julio de 2026. Análisis original basado en la inspección del código de `static-site-generator` en la v0.0.41; las fuentes se citan, no se reproducen. Los números de versión y el estado de las funciones cambian con rapidez; verifíquelos con el repositorio antes de volver a publicar. Bajo licencia CC-BY-4.0.*
