---
author: "contact@sebastienrousseau.com (Sebastien Rousseau)"
banner_alt: "Um fundo técnico abstrato, representando o roadmap arquitetural de um gerador de sites estáticos de nível corporativo."
banner_height: "1280"
banner_width: "1920"
banner: "https://cloudcdn.pro/stocks/images/gemini-background.webp"
cdn: "https://cloudcdn.pro"
charset: "UTF-8"
cname: "sebastienrousseau.com"
copyright: "© Copyright 2025 - 2026 - Sebastien Rousseau. All rights reserved."
date: "July 22, 2026"
description: "Análise de um gerador de sites estáticos em Rust: segurança em tempo de compilação, gates WCAG e IA local, as lacunas da v0.0.41 e o roadmap até a 1.0."
format-detection: "telephone=no"
hreflang: "pt-br"
icon: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
id: "https://sebastienrousseau.com/pt-br/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
image_alt: "Retrato em preto e branco de Sebastien Rousseau"
image_height: "162"
image_width: "162"
image: "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp"
keywords: "gerador de sites estáticos, Rust, forbid unsafe_code, WCAG 2.2 AA, Content Security Policy, Subresource Integrity, SLSA, CycloneDX SBOM, pipeline LLM local, DORA, builds incrementais, lol_html, sandbox de plugin WASM, busca vetorial semântica, MiniJinja, Ollama"
language: "pt-br"
last_reviewed: "2026-07-22"
layout: "report"
locale: "pt_BR"
logo_alt: "Logotipo de Sebastien Rousseau"
logo_height: "44"
logo_width: "44"
logo: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
menu: ""
measurementID: "G-169G4ET5HQ"
name: "Sebastien Rousseau"
permalink: "https://sebastienrousseau.com/pt-br/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
rating: "general"
referrer: "no-referrer"
robots: "index, follow"
schema: "FAQPage, Article"
seo_title: "Gerador de Sites Estáticos: O Caminho até a 1.0"
short_name: "sebastienrousseau"
subtitle: "Uma auditoria arquitetural e um roadmap para um gerador de sites estáticos em Rust construído como infraestrutura segura por padrão: o que a v0.0.41 realmente entrega versus o que o README promete, cinco capacidades corporativas ausentes e um caminho em fases até uma 1.0 alinhada a DORA e EAA."
tags: "gerador de sites estáticos, Rust, segurança web, acessibilidade, DORA, cadeia de suprimentos, SLSA, IA local, WCAG, tempo de compilação, roadmap, enterprise"
theme-color: "0, 83, 191"
title: "Gerador de Sites Estáticos (SSG): Análise e Roadmap Corporativo"
url: "https://sebastienrousseau.com/pt-br/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap/rss.xml"
category: "Technology"
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.26)"
item_description: "Análise de um gerador de sites estáticos em Rust: segurança em tempo de compilação, gates WCAG e IA local, as lacunas da v0.0.41 e o roadmap até a 1.0."
item_guid: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap/rss.xml"
item_link: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap/rss.xml"
item_pub_date: "Wed, 22 Jul 2026 07:07:07 +0000"
item_title: "Gerador de Sites Estáticos (SSG): Análise e Roadmap Corporativo"
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
apple-mobile-web-app-title: "SSG: Caminho até a 1.0"
apple-touch-fullscreen: "yes"
msapplication-navbutton-color: "0, 83, 191"
twitter_card: "summary_large_image"
twitter_creator: "@wwdseb"
twitter_description: "Gates WCAG em compilação, SRI SHA-384, injeção de CSP e um pipeline LLM local distinguem este motor Rust. Uma análise honesta da v0.0.41 e o caminho até a 1.0."
twitter_image: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
twitter_image_alt: "Logotipo de Sebastien Rousseau"
twitter_site: "@wwdseb"
twitter_title: "Gerador de Sites Estáticos: O Caminho até a 1.0"
twitter_url: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
excerpt: "Gates WCAG em compilação, SRI SHA-384, injeção de CSP e um pipeline LLM local distinguem este motor Rust. Builds incrementais e AVIF seguem aspiracionais."
author_website: "https://sebastienrousseau.com"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "Obrigado pela leitura!"
site_last_updated: "2026-07-22"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "Kaishi, Kaishi Builder, Kaishi CLI, Kaishi Templates, Kaishi Themes"
---

# Gerador de Sites Estáticos (SSG): Análise Estratégica Aprofundada e Roadmap Arquitetural de Nível Corporativo

*Data da pesquisa: 2026-06-22. Baseado na inspeção do código-fonte de `static-site-generator` na v0.0.41 e em pesquisa web sobre o panorama de SSGs em 2026.*

**Para um publicador regulado, um gerador de sites estáticos deixou de ser uma ferramenta de design; passou a integrar o perímetro de risco operacional.** O [static-site-generator](https://github.com/sebastienrousseau/static-site-generator) em Rust e de código aberto parte dessa premissa, levando os pipelines de segurança, acessibilidade, internacionalização e conteúdo por IA para o tempo de compilação, de modo que uma verificação reprovada interrompe o build em vez de chegar à produção. Esta análise separa o que a versão 0.0.41 realmente entrega daquilo que sua documentação ainda apenas promete, apresenta cinco capacidades corporativas que ela ainda não possui e propõe um caminho em fases até um lançamento 1.0 alinhado à DORA, à Lei Europeia de Acessibilidade e aos padrões modernos de cadeia de suprimentos.

<!-- lead-start -->
<aside class="post-lead" aria-label="Resumo do artigo">
<p class="post-lead-tldr"><strong>TL;DR.</strong> O <code>static-site-generator</code> em Rust trata a publicação web como um pipeline de software auditável e seguro por padrão: <code>forbid(unsafe_code)</code> em todo o workspace, Subresource Integrity SHA-384, extração de Content Security Policy, um gate WCAG 2.2 AA em tempo de compilação e um pipeline LLM local. Uma inspeção do código da v0.0.41 mostra que vários recursos documentados ainda são aspiracionais, entre eles a minificação nativa, os rebuilds incrementais e o AVIF. Esta é a análise honesta das lacunas e um roadmap em fases até uma 1.0 de nível corporativo.</p>
<p class="post-lead-heading"><strong>Principais conclusões</strong></p>
<ul class="post-lead-takeaways">
  <li><strong>O modelo de segurança e acessibilidade é real.</strong> SRI em tempo de compilação, extração de CSP, releases assinados com atestação Sigstore e SBOMs CycloneDX, além de um gate WCAG 2.2 AA que interrompe o build, estão implementados em código, não apenas documentados.</li>
  <li><strong>Vários recursos de destaque não estão.</strong> O minificador apenas colapsa espaços em branco, o grafo de dependências que conduziria os builds incrementais nunca é preenchido em produção e a codificação AVIF é um stub que retorna um vetor vazio.</li>
  <li><strong>Faltam cinco capacidades corporativas.</strong> Sandbox de plugins WASM, um reescritor de HTML em streaming e zero-copy, busca semântica local, cache determinístico de inferência e I/O de arquivos assíncrono.</li>
  <li><strong>O roadmap é sequenciado por risco.</strong> Um patch de correção (0.0.42), uma minor de credibilidade e builds incrementais (0.1.0) e, então, uma major corporativa (1.0.0) trazendo o sandbox, a busca semântica e a proveniência SLSA v1.1.</li>
</ul>
<p class="post-lead-related"><strong>Leituras relacionadas:</strong> <a href="https://sebastienrousseau.com/2026-07-03-emerging-technology-risk-horizon-banks-2026">O Horizonte de Risco das Tecnologias Emergentes para os Bancos</a>, <a href="https://sebastienrousseau.com/2026-07-07-corporate-banking-api-standard-agentic-mcp-2026">Um Padrão de API de Banco Corporativo para MCP Agêntico</a>.</p>
</aside>
<!-- lead-end -->

> **Resumo Executivo**
>
> - **A publicação agora é um perímetro de risco operacional.** Sob a DORA, a Lei Europeia de Acessibilidade e o GDPR, cada ativo voltado ao público é um ponto de entrada potencial para comprometimento da cadeia de suprimentos, desfiguração e exposição regulatória. Um modelo em tempo de compilação estreita esse perímetro ao rejeitar saídas não conformes antes que sejam publicadas.
> - **Os diferenciais do motor são impostos pelo compilador, não aspirações documentadas.** `forbid(unsafe_code)` em todo o workspace, SRI SHA-256/384 verdadeiro, extração automática de CSP e um gate WCAG 2.2 AA em tempo de compilação transformam segurança e acessibilidade de auditorias posteriores em falhas de build inegociáveis.
> - **A versão 0.0.41 tem uma lacuna entre documentação e código.** Minificação nativa, rebuilds incrementais via grafo de dependências e suporte a AVIF são descritos, mas não funcionam; o artigo aponta cada lacuna em relação à localização exata no código-fonte.
> - **O caminho até a 1.0 é uma sequência, não uma lista de desejos.** Primeiro a robustez (0.0.42), depois a correção incremental (0.1.0) e, por fim, as capacidades corporativas — sandbox WASM, busca semântica local e proveniência SLSA verificável — que um comprador regulado exige (1.0.0).

## Pontos Fortes Atuais

O código-fonte do `static-site-generator` exibe várias decisões de engenharia distintivas que o separam dos motores legados em JavaScript e Go:

- **Postura de segurança em tempo de compilação:** `#![forbid(unsafe_code)]` em todo o workspace fornece garantias de segurança de memória em tempo de compilação. O pipeline de build gera hashes verdadeiros de Subresource Integrity (SRI) SHA-256/SHA-384 (`src/plugins/assets.rs`) e realiza extração automática de Content Security Policy (CSP), que remove scripts e estilos unsafe-inline. Os releases são assinados, carregam atestação Sigstore e produzem um SBOM CycloneDX 1.5 a cada build.  
- **Gate de acessibilidade imposto pelo compilador:** As verificações das Diretrizes de Acessibilidade para Conteúdo Web (WCAG, Web Content Accessibility Guidelines) 2.2 Nível AA rodam dentro do pipeline de compilação por meio de um parser axe-core em tempo de compilação conduzido pelo Playwright. A acessibilidade torna-se um gate de compilação inegociável, e não uma auditoria pós-publicação: se uma página falha, a compilação é interrompida com erros de número de linha exatos.  
- **Pipeline de IA com soberania de dados:** Um pipeline de tradução e extração de metadados por LLM local (via endpoints locais Ollama ou llama.cpp) permite que uma instituição automatize a sumarização de conteúdo, a geração de esquemas JSON-LD e a tradução multilíngue sem enviar divulgações pré-resultados ou propriedade intelectual sensível a APIs públicas de IA em nuvem.  
- **Compilação paralelizada:** As garantias de segurança de memória do Rust sustentam um pipeline de HTML e ativos paralelizado e movido a Rayon (`src/core/pipeline.rs`). O pipeline de plugins executa transformações fundidas, com `SearchPlugin`, `SeoPlugin`, `CanonicalPlugin` e `JsonLdPlugin` operando sobre `par_iter()`, de modo que cada página é lida e escrita em disco uma única vez.  
- **Higiene de cadeia de suprimentos e dependências:** Migrar o motor de templates de Tera para MiniJinja (`v0.0.37`) reduziu o tamanho do binário, removeu dependências transitivas como `rand` em tempo de compilação e produziu uma pegada de dependências compacta que reduz a exposição da cadeia de suprimentos de software.

---

## Lacunas e Realidades Práticas

Apesar desses pontos fortes excepcionais, uma inspeção rigorosa do código-fonte da v0.0.41 revela várias lacunas arquiteturais, funcionais e de experiência do desenvolvedor entre o que a documentação afirma e o código Rust real:

### Lacunas Arquiteturais

- **Colapso de espaços vs. minificação nativa:** Embora o README prometa "minificação nativa de JS/CSS", o `MinifyPlugin` (`src/plugins/plugins.rs:96-116`) atua apenas como um colapsador ingênuo de espaços em branco. Ele interrompe o processamento em elementos `<pre>` e colapsa sequências de espaços no HTML, mas não realiza minificação nativa de CSS ou JS com consciência sintática. Além disso, processa somente as páginas de nível superior e não percorre recursivamente os subdiretórios (como `/blog/` ou `/tags/`), deixando as páginas profundas sem minificar.  
- **Infraestrutura incremental morta:** O grafo de rastreamento de dependências (`DepGraph` em `src/core/depgraph.rs`) é compilado e carregado em `PluginContext.dep_graph`, mas nunca é de fato preenchido no código de produção. O método `add_dep()` só é chamado em testes unitários, o que torna a afirmação do README sobre "rebuilds incrementais via grafos de dependências" atualmente aspiracional.  
- **Compilação em lotes vs. compilação em streaming:** O módulo `streaming::compile_batch` (`src/core/streaming.rs`) não faz streaming de verdade. Em vez disso, compila páginas em lotes para um diretório temporário, executa `staticdatagen::compile` do zero para cada lote e mescla as saídas. Isso resulta em sobrecarga significativa de I/O de disco e parsing redundante, afastando-se de uma arquitetura de streaming real.  
- **Violações de fase no ciclo de vida dos plugins:** Plugins que geram novas páginas HTML durante o build, como `TaxonomyPlugin`, `PaginationPlugin` e `I18nPlugin`, escrevem diretamente em disco no `after_compile` em vez de usar o ciclo de vida `transform_html`. Por consequência, as páginas geradas por esses plugins ignoram plugins críticos de pós-processamento (como `CanonicalPlugin`, `JsonLdPlugin`, `RobotsPlugin` e `AccessibilityPlugin`) caso esses plugins tenham sido registrados antes. Isso deixa páginas de tags, categorias e paginação sem links canônicos corretos, esquemas JSON-LD ou validações de acessibilidade.  
- **Chamada ao `curl` via shell no `LlmPlugin`:** O pipeline de conteúdo por LLM local (`src/plugins/llm.rs`) invoca diretamente via shell o binário `curl` do host para consultar endpoints locais. Isso introduz bugs graves de compatibilidade entre plataformas (por exemplo, em hosts Windows sem o curl no PATH), representa um risco de segurança (vetores de injeção de shell) e falha em ambientes de CI bloqueados ou isolados de rede.  
- **Manipulação ingênua de strings na reescrita de HTML:** Os extratores em `image_plugin.rs` e `search.rs` reescrevem strings de HTML usando operações frágeis de `str::find` e `str::rfind`. Essa abordagem é altamente vulnerável a tags HTML quebradas, tags `<img>` dentro de comentários, entidades de caracteres no texto alternativo ou propriedades `srcset` preexistentes, o que pode resultar em saída corrompida.  
- **Suporte a AVIF não implementado:** Embora a codificação de imagens AVIF seja amplamente documentada, a implementação em `image_plugin.rs` é um stub em que `avif_variants` simplesmente retorna `Vec::new()`, deixando o recurso não funcional.  
- **Watcher baseado em polling:** O watcher do servidor de desenvolvimento local (`src/server/watch.rs`) usa polling em vez de APIs de eventos do sistema de arquivos, o que leva a uso excessivo de CPU em repouso e latência de modificação abaixo de um segundo.

### Lacunas Funcionais e de DX

- **Sem rastreamento de dependências transitivas:** O grafo de dependências não consegue rastrear dependências aninhadas (por exemplo, alterações em um subtemplate que afeta um layout que afeta uma página), conforme verificado pelo teste unitário `transitive_not_tracked`.  
- **Sem flag de CLI para compilação incremental:** Não há uma flag de CLI `--incremental` conectada ao compilador de execução, o que impede os desenvolvedores de usar builds em cache.  
- **HMR limitado a CSS:** O Hot Module Replacement (HMR) só suporta CSS; qualquer modificação em arquivos HTML, layouts ou markdown dispara um recarregamento completo da página, degradando a velocidade do desenvolvedor.  
- **Déficit de subcomandos:** Os desenvolvedores precisam passar manualmente flags verbosas (`ssg -s public -w`) porque subcomandos padrão como `ssg dev`, `ssg build`, `ssg check` e `ssg lint` não existem.

---

## Lacunas Arquiteturais que Nos Faltam (Novas Descobertas)

Além das lacunas na v0.0.41, avaliar o projeto contra um perfil de risco de nível financeiro revela várias capacidades que ele ainda não oferece, mas que um comprador corporativo exigiria:

### 1. Sandbox de Plugins WebAssembly (Extensão Zero-Trust)

Embora o próprio binário do compilador seja escrito em Rust seguro, permitir que plugins de terceiros arbitrários executem nativamente nos sistemas host introduz uma grave vulnerabilidade de cadeia de suprimentos. Um plugin de terceiros comprometido poderia facilmente acessar o sistema de arquivos do host, ler arquivos Markdown proprietários ou exfiltrar credenciais privadas.

* **Capacidade ausente:** Um ambiente de execução em sandbox. Para alcançar compilação zero-trust, o compilador deveria executar plugins de terceiros dentro de um runtime WebAssembly embarcado (como o `wasmtime`). Os plugins deveriam interagir com o host exclusivamente por meio de uma WebAssembly System Interface (WASI) restrita, limitando seu acesso estritamente à página em transformação.

### 2. Parsing de HTML Zero-Copy via AST em Streaming (`lol_html`)

Migrar a camada de parsing de HTML para uma biblioteca de DOM totalmente em memória (como Kuchiki ou html5ever) introduz sobrecarga significativa de memória e pausas de processamento ao lidar com sites com mais de 100.000 páginas.

* **Capacidade ausente:** Um reescritor de HTML em streaming e zero-copy. Utilizar o `lol_html` da Cloudflare (Low-Output-Latency HTML rewriter) permite que o compilador analise, inspecione e modifique elementos HTML em uma única passagem de streaming com alocação de memória próxima de zero, atingindo a meta de builds abaixo de um segundo do compilador paralelo de streaming.

### 3. Busca Vetorial Semântica Local (RAG Local)

O índice de busca atual (`SearchPlugin`) gera um índice JSON pesado e plano que realiza correspondências simples de strings no lado do cliente, sem suporte a busca aproximada, stemming ou consultas semânticas. O Pagefind é uma melhoria, mas ainda depende do download de um índice grande.

* **Capacidade ausente:** Busca semântica embarcada. O compilador deveria empregar um modelo local e leve de embeddings vetoriais nativo em Rust (como um modelo MiniLM-L6 executado via `candle` ou `ort` / ONNX Runtime) em tempo de build. Ele deveria gerar embeddings vetoriais densos para cada parágrafo de página e produzir um índice vetorial compacto. O widget de busca no lado do cliente, compilado para WASM, poderia então realizar busca semântica offline de verdade diretamente no navegador.

### 4. Cache Determinístico de Tradução e Inferência

Como a inferência de LLM local (por exemplo, via Ollama ou Llama.cpp) é altamente intensiva em CPU/GPU, traduzir ou gerar metadados para milhares de páginas a cada build é computacionalmente proibitivo.

* **Capacidade ausente:** Cache de inferência baseado em hash de conteúdo. O compilador deve manter um cache determinístico de todas as operações de LLM. Se o hash SHA-256 do conteúdo de um arquivo markdown e seus parâmetros de tradução corresponderem a uma entrada do cache, o compilador deveria reutilizar a tradução e os metadados em cache, evitando inferência local redundante.

### 5. I/O de Arquivos Assíncrono para Escala Paralela

Embora o pipeline de plugins seja paralelizado via Rayon, as escritas síncronas padrão em disco bloqueiam as threads de SO do Rayon, criando um gargalo de I/O ao escrever dezenas de milhares de páginas.

* **Capacidade ausente:** I/O de disco assíncrono e não bloqueante. O compilador deveria desacoplar as tarefas intensivas em CPU (parsing de Markdown, minificação) das escritas limitadas por disco, usando pools de threads de I/O assíncrono ou bindings de `io_uring` do Linux (via `rio` ou `tokio`) para escrever páginas compiladas em paralelo sem bloquear os executores paralelos de CPU.

---

## O Roadmap Estratégico da 1.0

O roadmap a seguir integra tanto as lacunas resolvidas quanto as capacidades de nível corporativo recém-descobertas em um framework de lançamento estruturado e cronológico.

### Fase 1: 0.0.42 (O Patch de Robustez e Correção, 1 a 2 semanas)

1. **Reconstruir o `MinifyPlugin`:** Integração de `minify-html`, `oxc_minifier` e `lightningcss` para minificação nativa e com consciência sintática de HTML, JS e CSS. Garantir que o plugin percorra recursivamente todos os diretórios aninhados sob `site_dir`.  
2. **Proteger o pipeline de IA:** Migrar o `LlmPlugin` das chamadas nativas ao `curl` via shell para o `ureq` (um cliente HTTP em Rust leve, síncrono e seguro), garantindo compatibilidade entre plataformas e eliminando vulnerabilidades de injeção de shell.  
3. **Concluir a implementação de AVIF:** Conectar o `ravif` diretamente ao pipeline de ativos de imagem, habilitando codificação AVIF de alto desempenho ao lado de WebP e PNG.  
4. **Automatizar HrefLang e mapeamento multi-locale:** Detectar automaticamente páginas traduzidas paralelas em builds multilíngues e injetar tags `<link rel="alternate" hreflang="..." />` padrão e compatíveis com o Google no head de cada arquivo HTML compilado.  
5. **Suporte a JSON Feed 1.1:** Entregar um emissor dedicado de JSON Feed 1.1 ao lado dos canais de sindicação padrão RSS 2.0 e Atom 1.0.

### Fase 2: 0.1.0 (A Minor de Credibilidade e Incremental, 2 a 3 meses)

1. **Preencher o `DepGraph` e habilitar o `--incremental`:** Conectar completamente o `DepGraph` para rastrear dependências de template para página e de markdown para página. Implementar uma camada de invalidação de cache e conectar a flag de CLI `--incremental`, mirando rebuilds abaixo de 200 ms para ambientes de cache quente.  
2. **Reescrita de AST em streaming via `lol_html`:** Substituir a frágil reescrita de strings em `image_plugin.rs`, `search.rs` e nas injeções de CSP por um reescritor de HTML em streaming e zero-copy movido a `lol_html`.  
3. **Watcher orientado a eventos e HMR de componentes:** Migrar o módulo de watch de polling para o crate `notify`, orientado a eventos, e implementar hot reloading somente de CSS e de HTML parcial para atualizações no navegador abaixo de 100 ms.  
4. **CLI de comandos unificada:** Rearquitetar a interface do compilador para suportar subcomandos padrão: `ssg dev`, `ssg build`, `ssg check` (auditoria de acessibilidade/SEO) e `ssg deploy`.  
5. **Cache determinístico de inferência:** Implementar uma camada de cache baseada em hash de conteúdo para todas as tarefas de tradução, sumarização e extração de metadados por LLM local.

### Fase 3: 1.0.0 (A Major Corporativa e de Produção, 6 a 12 meses)

1. **Sandbox zero-trust de plugins WASM:** Embarcar um runtime WebAssembly (`wasmtime` ou `wasmer`) para executar plugins de terceiros em um ambiente totalmente em sandbox, com acesso a sistema de arquivos e rede baseado em capacidades.  
2. **Busca vetorial semântica local (RAG local):** Embarcar um modelo de embeddings local e nativo em Rust (via `candle` ou `ort`) para compilar embeddings densos de parágrafos em um índice compacto, habilitando busca semântica privada no lado do cliente.  
3. **Server Islands e alvo WASM na edge:** Implementar a execução de componentes `<ssg-island>` em runtimes de edge (como Cloudflare Workers, Vercel Edge ou Netlify Edge) construídos sobre o núcleo `ssg-wasm` compilado.  
4. **Motor de I/O paralelo assíncrono:** Rearquitetar o módulo de escrita no sistema de arquivos para usar pools de threads de I/O assíncrono e bindings de `io_uring`, eliminando bloqueios dos workers de CPU durante as escritas paralelas.  
5. **Proveniência de build SLSA v1.1 e conformidade com SPDX 3.0:** Fornecer proveniência de build SLSA Nível 3 matematicamente verificável e gerar SBOMs em conformidade com SPDX 3.0, satisfazendo plenamente os padrões modernos de segurança da cadeia de suprimentos de software.

---

## Matriz de Concorrentes (Panorama de 2026)

A matriz a seguir compara o `static-site-generator` (alvo v1.0) com os principais motores de publicação web de 2026:

| Capacidade | static-site-generator v1.0 | Hugo v0.155+ | Zola v0.19+ | Astro 5 | Eleventy 3 |
| ---- | ---- | ---- | ---- | ---- | ---- |
| **Linguagem / Runtime** | Rust (Zero Unsafe) | Go | Rust | JS (Node/V8) | JS (Node/V8) |
| **Gate de Build de A11y** | Validação de AST em Tempo de Build | Nenhum | Nenhum | Linter pós-build | Linter pós-build |
| **Endurecimento de Segurança** | SRI SHA-384 e injeção de CSP | Manual | Manual | Manual | Manual |
| **Segurança da Cadeia de Suprimentos** | SLSA L3 \+ SPDX 3.0 \+ Sandbox WASM | Mínima | Mínima | Árvore NPM pesada | Árvore NPM pesada |
| **Pipeline de Conteúdo por IA** | Privado, Local-First (LLM local) | Nenhum | Nenhum | Apenas API pública | Apenas API pública |
| **Velocidade Incremental** | \<200ms (cache quente) | \<100ms | \<150ms | \~1.5s | \~140ms |
| **Interatividade Dinâmica** | Server Islands (alvos WASM) | Nenhum | Nenhum | Server Islands (JS) | Islands (JS) |
| **Motor de Busca** | Busca semântica WASM local | String simples | String simples | Pagefind (JS) | Pagefind (JS) |

---

## Posicionamento na 1.0

Na 1.0, o posicionamento pretendido é o de um gerador de sites estáticos projetado como infraestrutura de software segura por padrão: autoria apoiada por pipelines de IA local-first; compilação de mais de 100.000 páginas através de um pipeline paralelo de streaming; WCAG 2.2 AA e CSP e SRI estritos impostos como gates de compilação; e ilhas dinâmicas em sandbox, tudo dentro de um único binário Rust seguro em memória. Cada cláusula dessa afirmação corresponde a um item específico do roadmap acima, e não a uma aspiração de marketing.

---

## Integração Regulatória e de Conformidade

Em setores corporativos e financeiros de alto risco, o software é avaliado sob a ótica da conformidade e do capital de risco. O roadmap arquitetural do `static-site-generator` alinha-se diretamente aos principais mandatos regulatórios:

- **DORA Artigo 6 (Gestão de Risco de TIC):** O cálculo e a injeção em tempo de compilação de hashes SRI SHA-384 e de Content Security Policies estritas satisfazem a exigência de proteger os canais de publicação digital contra injeção na cadeia de suprimentos, desfiguração web e vetores de cross-site scripting (XSS).  
- **DORA Artigo 7 (Resiliência dos Sistemas de TIC):** Ao migrar para ativos estáticos imutáveis e verificados em tempo de compilação, as instituições financeiras eliminam vulnerabilidades de banco de dados e de servidor em runtime, reduzindo o multiplicador de risco operacional e as reservas de capital de risco exigidas sob Basileia III.  
- **Lei Europeia de Acessibilidade (EAA), Diretiva (UE) 2019/882:** Deslocar a auditoria de acessibilidade para a esquerda, para dentro do pipeline de compilação, como um gate inegociável do compilador garante 100% de conformidade antes do deploy, eliminando o risco de dano à marca e de litígio civil sob a EAA e o Título III da ADA.  
- **GDPR Artigo 25 (Privacy-by-Design):** Executar o pipeline de tradução e metadados em hardware local e isolado de rede mantém rascunhos proprietários, métricas financeiras e dados pessoais fora de provedores públicos de LLM em nuvem de terceiros, apoiando a conformidade com os princípios de soberania de dados.

---

## Perguntas Frequentes

**O que a versão 0.0.41 realmente entrega hoje, em comparação com o que o README afirma?**
O modelo de segurança e acessibilidade é real e imposto em código: `forbid(unsafe_code)` em todo o workspace, geração de SRI SHA-256/384, extração de CSP, releases assinados com atestação Sigstore e um SBOM CycloneDX, além de um gate WCAG 2.2 AA que interrompe o build. Três recursos documentados não funcionam na v0.0.41. O `MinifyPlugin` é um colapsador de espaços em branco, e não um minificador com consciência sintática; o `DepGraph` que conduziria os rebuilds incrementais é compilado, mas nunca preenchido no código de produção; e a codificação AVIF é um stub cujo `avif_variants` retorna um vetor vazio.

**O gate de acessibilidade é um gate real de compilador ou um linter pós-build?**
É um gate de compilação. As verificações WCAG 2.2 AA rodam dentro do pipeline de compilação por meio de um parser axe-core em tempo de compilação conduzido pelo Playwright, e uma página reprovada interrompe a compilação com erros de número de linha exatos, em vez de emitir um aviso depois do fato. Essa é a propriedade de que uma obrigação da Lei Europeia de Acessibilidade precisa: a saída não conforme não pode chegar ao deploy.

**Por que a chamada ao `curl` via shell no plugin de LLM é relevante?**
O pipeline de LLM local (`src/plugins/llm.rs`) invoca o binário `curl` do host para alcançar endpoints locais. Isso acopla o build a um executável do host, falha em sistemas sem o `curl` no PATH, introduz superfície de injeção de shell e quebra em CI isolado de rede. Migrar a chamada para um cliente HTTP em Rust como o `ureq` remove a dependência externa e o vetor de injeção, razão pela qual é o segundo item do patch 0.0.42.

**Qual é o item mais importante no caminho até a 1.0?**
Preencher o `DepGraph` e conectar a flag `--incremental`. Os rebuilds incrementais são a lacuna de credibilidade entre o motor documentado e o real, e toda afirmação subsequente sobre builds abaixo de um segundo em mais de 100.000 páginas depende de o grafo de dependências rastrear as arestas de template para página e de markdown para página, em vez de permanecer como infraestrutura restrita a testes.

## Referências

- [Cloudflare, *lol-html: reescritor de HTML em streaming de baixa latência de saída*](https://github.com/cloudflare/lol-html "Cloudflare lol-html — reescritor de HTML em streaming") ⧉. [O reescritor de HTML em streaming e zero-copy proposto para substituir a frágil manipulação de strings na fase 0.1.0.]
- [W3C, *Web Content Accessibility Guidelines (WCAG) 2.2*](https://www.w3.org/TR/WCAG22/ "W3C — Recomendação WCAG 2.2") ⧉. [Os critérios de sucesso de Nível AA impostos pelo gate de acessibilidade em tempo de compilação.]
- [União Europeia, *Regulamento (UE) 2022/2554 (DORA)*](https://eur-lex.europa.eu/eli/reg/2022/2554/oj "EUR-Lex — Lei de Resiliência Operacional Digital") ⧉. [Os artigos de gestão de risco e resiliência de TIC aos quais a postura de segurança corresponde.]
- [OpenSSF, *Supply-chain Levels for Software Artifacts (SLSA) v1.0*](https://slsa.dev/spec/v1.0/ "SLSA — especificação v1.0") ⧉. [O framework de proveniência de build almejado para atestação verificável de Nível 3 na 1.0.]
- [Armin Ronacher, *Motor de templates MiniJinja*](https://github.com/mitsuhiko/minijinja "MiniJinja — motor Jinja2 mínimo para Rust") ⧉. [O motor leve em dependências que substituiu o Tera e enxugou a árvore transitiva.]
- [CycloneDX, *Especificação de Software Bill of Materials v1.5*](https://cyclonedx.org/docs/1.5/ "CycloneDX — especificação de SBOM v1.5") ⧉. [O formato de SBOM emitido a cada build para auditoria da cadeia de suprimentos.]
- [União Europeia, *Diretiva (UE) 2019/882 (Lei Europeia de Acessibilidade)*](https://eur-lex.europa.eu/eli/dir/2019/882/oj "EUR-Lex — Lei Europeia de Acessibilidade") ⧉. [A obrigação de acessibilidade que o gate WCAG em tempo de compilação foi projetado para satisfazer.]

*Última revisão em julho de 2026. Análise original baseada na inspeção do código-fonte do `static-site-generator` na v0.0.41; as fontes são citadas, não reproduzidas. Números de versão e status de recursos mudam rapidamente; verifique no repositório antes de republicar. Licenciado sob CC-BY-4.0.*
