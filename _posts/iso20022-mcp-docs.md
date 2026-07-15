---

# Front Matter (YAML)

author: "contact@sebastienrousseau.com (Sebastien Rousseau)"
banner_alt: "Aerial view of illuminated financial district at night"
banner_height: "100vh"
banner_width: "100vw"
banner: "https://cloudcdn.pro/stocks/images/denys-nevozhai-2vmT5_FeMck-1920.webp"
cdn: "https://cloudcdn.pro/clients"
changefreq: "weekly"
charset: "UTF-8"
cname: "sebastienrousseau.com"
copyright: "© Copyright 2007 - 2026 - Sebastien Rousseau. All rights reserved."
date: "Jul 14, 2026"
description: "Documentation for the ISO 20022 MCP Suite: install, a 60-second quickstart, which server to use for each job, the safety model, and the 2026–2028 migration timeline."
format-detection: "telephone=no"
hreflang: "en"
icon: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
id: "https://sebastienrousseau.com/iso20022-mcp-docs"
image_alt: "ISO 20022 MCP Suite documentation"
image_height: "162"
image_width: "162"
image: "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp"
keywords: "ISO 20022 MCP docs, MCP server quickstart, pain.001 MCP, pacs.008 MCP, camt.053 MCP, reconciliation MCP, AP2 x402 bridge, agent payments documentation"
last_reviewed: "2026-07-14"
language: "en-GB"
layout: "story"
locale: "en_GB"
logo_alt: "Logo for Sebastien Rousseau"
logo_height: "44"
logo_width: "44"
logo: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
menu: ""
measurementID: "G-169G4ET5HQ"
name: "ISO 20022 MCP Suite: documentation."
permalink: "https://sebastienrousseau.com/iso20022-mcp-docs"
rating: "general"
referrer: "no-referrer"
revisit-after: "7 days"
robots: "index, follow"
short_name: "iso20022-mcp docs"
subtitle: "Install in one line, make your first validated ISO 20022 message in under a minute, and pick the right server for the job. Vendor-neutral, runs anywhere."
tags: "ISO 20022, MCP, Documentation, Quickstart, pain.001, pacs.008, camt.053, Reconciliation, AP2, x402, Agent Payments, Fintech, Open Source"
theme-color: "0, 67, 165"
title: "ISO 20022 MCP Suite: documentation"
url: "https://sebastienrousseau.com/iso20022-mcp-docs"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"

# RSS - The RSS feed front matter (YAML).
atom_link: "https://sebastienrousseau.com/iso20022-mcp-docs/rss.xml"
category: "Technology"
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.26)"
item_description: "Documentation for the ISO 20022 MCP Suite: install, quickstart, which server per job, safety model, and migration timeline."
item_guid: "https://sebastienrousseau.com/iso20022-mcp-docs/rss.xml"
item_link: "https://sebastienrousseau.com/iso20022-mcp-docs/rss.xml"
item_pub_date: "Tue, 14 Jul 2026 06:06:06 +0000"
item_title: "ISO 20022 MCP Suite: documentation"
last_build_date: "Tue, 14 Jul 2026 06:06:06 +0000"
managing_editor: "contact@sebastienrousseau.com (Sebastien Rousseau)"
pub_date: "Tue, 14 Jul 2026 06:06:06 +0000"
ttl: "60"
type: "website"
webmaster: "contact@sebastienrousseau.com"

# Apple - The Apple front matter (YAML).
apple_mobile_web_app_orientations: "portrait"
apple_touch_icon_sizes: "192x192"
apple-mobile-web-app-capable: "yes"
apple-mobile-web-app-status-bar-inset: "black"
apple-mobile-web-app-status-bar-style: "black-translucent"
apple-mobile-web-app-title: "ISO 20022 MCP docs"
apple-touch-fullscreen: "yes"

# MS Application - The MS Application front matter (YAML).

msapplication-navbutton-color: "0, 67, 165"

# Twitter Card - The Twitter Card front matter (YAML).

twitter_card: "summary"
twitter_creator: "@wwdseb"
twitter_description: "Docs for the ISO 20022 MCP Suite: one-line install, 60-second quickstart, which server per job, safety model, migration timeline."
twitter_image: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
twitter_image_alt: "ISO 20022 MCP Suite documentation"
twitter_site: "@wwdseb"
twitter_title: "ISO 20022 MCP Suite: documentation"
twitter_url: "https://sebastienrousseau.com/iso20022-mcp-docs"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://sebastienrousseau.com"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "Thanks for reading!"
site_last_updated: "2026-07-14"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "Kaishi, Kaishi Builder, Kaishi CLI, Kaishi Templates, Kaishi Themes"
site_software: "Static Site Generator, Rust"

---

<p class="story-intro">The ISO 20022 MCP Suite is the open bank-message layer for AI agents: nine vendor-neutral servers to generate, validate, reconcile and settle ISO 20022 payments from natural language. Everything below gets you from nothing to a validated message in under a minute: no account, no key, no lock-in.</p>

<section class="newsroom" id="quickstart">
<header class="cat-section-head"><p class="cat-kicker">60-SECOND QUICKSTART</p><h2 class="cat-headline">Install one line, send one message.</h2><p class="cat-lede">Run the gateway with no install and no account. It routes to whichever server the job needs.</p></header>
<div class="story-why">
<ul class="story-why-list">
<li><strong>1 · Run it.</strong> <code>uvx --from "iso20022-mcp[all]" iso20022-mcp</code>, or add it to your MCP client (Claude Desktop, Cursor) as the command <code>iso20022-mcp</code>.</li>
<li><strong>2 · Find the message.</strong> Ask <em>search "cancel a payment"</em> → the gateway points you at <code>camt.056</code> and the <code>camt-exceptions</code> server.</li>
<li><strong>3 · Generate it.</strong> Ask <em>generate camt.056</em> with the payment details → you get back XSD-validated ISO 20022 XML. Done.</li>
</ul>
</div>
</section>

<section class="newsroom" id="which-server">
<header class="cat-section-head"><p class="cat-kicker">WHICH SERVER DO I NEED?</p><h2 class="cat-headline">One job, one server.</h2><p class="cat-lede">Install the gateway and let it route, or install just the one for the task in front of you. Every server is <code>pip install</code>-able and live on the official MCP registry.</p></header>
<div class="newsroom-grid cat-grid">
<article class="newsroom-card">
<a class="newsroom-card-media logo" href="https://github.com/sebastienrousseau/iso20022-mcp" title="iso20022-mcp">
<img alt="Gateway" src="https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg" loading="lazy" decoding="async" width="600" height="600" />
</a>
<div class="newsroom-card-body">
<h3><a href="https://github.com/sebastienrousseau/iso20022-mcp">Discover &amp; route</a></h3>
<p class="newsroom-excerpt">Start here. The gateway's <code>search</code> / <code>describe</code> / <code>generate</code> / <code>validate</code> / <code>parse</code> meta-tools span every family.</p>
<p class="newsroom-more"><code>iso20022-mcp</code></p>
</div>
</article>
<article class="newsroom-card">
<a class="newsroom-card-media logo" href="https://github.com/sebastienrousseau/pain001-mcp" title="pain001-mcp">
<img alt="pain001" src="https://cloudcdn.pro/clients/pain001/v1/logos/pain001.svg" loading="lazy" decoding="async" width="600" height="600" />
</a>
<div class="newsroom-card-body">
<h3><a href="https://github.com/sebastienrousseau/pain001-mcp">Initiate a payment</a></h3>
<p class="newsroom-excerpt">pain.001 customer credit transfers, with IBAN/BIC and XSD validation and an MT101 converter.</p>
<p class="newsroom-more"><code>pain001-mcp</code></p>
</div>
</article>
<article class="newsroom-card">
<a class="newsroom-card-media logo" href="https://github.com/sebastienrousseau/pacs008-mcp" title="pacs008-mcp">
<img alt="pacs008" src="https://cloudcdn.pro/clients/pacs008/v1/logos/pacs008.svg" loading="lazy" decoding="async" width="600" height="600" />
</a>
<div class="newsroom-card-body">
<h3><a href="https://github.com/sebastienrousseau/pacs008-mcp">Settle interbank</a></h3>
<p class="newsroom-excerpt">pacs.008 transfers, pacs.004 returns, pacs.002 status, the Nov-2026 address toolkit, MT103.</p>
<p class="newsroom-more"><code>pacs008-mcp</code></p>
</div>
</article>
<article class="newsroom-card">
<a class="newsroom-card-media logo" href="https://github.com/sebastienrousseau/reconcile-mcp" title="reconcile-mcp">
<img alt="reconcile" src="https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg" loading="lazy" decoding="async" width="600" height="600" />
</a>
<div class="newsroom-card-body">
<h3><a href="https://github.com/sebastienrousseau/reconcile-mcp">Reconcile</a></h3>
<p class="newsroom-excerpt">Match camt.053 statements against expected pain.001 (exact, partial, split, batch), explainably.</p>
<p class="newsroom-more"><code>reconcile-mcp</code></p>
</div>
</article>
<article class="newsroom-card">
<a class="newsroom-card-media logo" href="https://github.com/sebastienrousseau/camt-exceptions" title="camt-exceptions">
<img alt="camt-exceptions" src="https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg" loading="lazy" decoding="async" width="600" height="600" />
</a>
<div class="newsroom-card-body">
<h3><a href="https://github.com/sebastienrousseau/camt-exceptions">Cancel &amp; resolve</a></h3>
<p class="newsroom-excerpt">camt.056 payment cancellation and camt.029 resolution of investigation, XSD-valid.</p>
<p class="newsroom-more"><code>camt-exceptions</code></p>
</div>
</article>
<article class="newsroom-card">
<a class="newsroom-card-media logo" href="https://github.com/sebastienrousseau/ap2-iso20022" title="ap2-iso20022">
<img alt="ap2-iso20022" src="https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg" loading="lazy" decoding="async" width="600" height="600" />
</a>
<div class="newsroom-card-body">
<h3><a href="https://github.com/sebastienrousseau/ap2-iso20022">Bridge an agent mandate</a></h3>
<p class="newsroom-excerpt">Turn an AP2 / x402 mandate into a wire-valid pain.001 / pacs.008, guardrailed.</p>
<p class="newsroom-more"><code>ap2-iso20022</code></p>
</div>
</article>
</div>
<p class="story-intro"><a href="/iso20022-mcp-reference/index.html">Full tool reference for every server <span aria-hidden="true">›</span></a> · <a href="/iso20022-mcp-recipes/index.html">End-to-end recipes <span aria-hidden="true">›</span></a></p>
</section>

<section class="newsroom" id="safety">
<header class="cat-section-head"><p class="cat-kicker">SAFE BY DESIGN</p><h2 class="cat-headline">Built to hand to an agent.</h2></header>
<div class="story-why">
<ul class="story-why-list">
<li><strong>Validated before return.</strong> Every generator checks its output against the official bundled XSD before it hands it back; malformed messages never leave the tool.</li>
<li><strong>Never moves money.</strong> The AP2/x402 bridge only transforms and validates; producing a message is deliberately separate from sending it, so the money-movement step stays a human-guarded action.</li>
<li><strong>Read-only where it counts.</strong> Reconciliation is pure matching; every tool is marked read-only, idempotent and closed-world so clients can reason about safety.</li>
<li><strong>Provenance you can audit.</strong> Bundled schemas are the official ISO 20022 XSDs; every server is Apache-2.0 at 100% branch-test coverage, on PyPI and the official MCP registry.</li>
</ul>
</div>
</section>

<section class="newsroom" id="migration">
<header class="cat-section-head"><p class="cat-kicker">THE 2026–2028 MIGRATION</p><h2 class="cat-headline">Move off MT, one message at a time.</h2><p class="cat-lede">MT/MX coexistence ended in November 2025; MT retires through 2028, and structured postal addresses become mandatory in November 2026. The suite ships the tools for exactly this.</p></header>
<div class="story-why">
<ul class="story-why-list">
<li><strong>MT → MX converters.</strong> <code>convert_mt103</code> → pacs.008, <code>convert_mt101</code> → pain.001, <code>convert_mt940</code>/<code>convert_mt942</code> → camt, with validated output wired into the servers.</li>
<li><strong>Structured-address toolkit.</strong> classify / validate-by-policy / repair / batch, in <code>pacs008-mcp</code>, for the November 2026 cliff.</li>
<li><strong>Exceptions ready.</strong> pacs.004 returns and pacs.002 status in pacs008-mcp; camt.056 cancellation and camt.029 resolution in camt-exceptions.</li>
</ul>
</div>
</section>

<section class="setup-finale" aria-labelledby="finale-heading"><p class="setup-finale-eyebrow">OPEN SOURCE · APACHE-2.0 · ON PYPI + THE MCP REGISTRY</p><h2 id="finale-heading" class="setup-finale-headline">Back to the suite.</h2><p class="setup-finale-lede">Nine servers, the whole ISO 20022 payment lifecycle, installable in one line.</p><p class="setup-finale-cta"><a href="/iso20022-mcp/index.html">Explore the suite <span aria-hidden="true">›</span></a> · <a href="/iso20022-mcp-reference/index.html">Tool reference <span aria-hidden="true">›</span></a></p></section>
