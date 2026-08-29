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
description: "End-to-end recipes for the ISO 20022 MCP Suite: migrate a legacy MT103, reconcile a statement, cancel and resolve a wrong payment, and turn an AP2 agent mandate into a wire-valid bank message."
format-detection: "telephone=no"
hreflang: "en"
icon: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
id: "https://sebastienrousseau.com/iso20022-mcp-recipes"
image_alt: "ISO 20022 MCP Suite recipes"
image_height: "162"
image_width: "162"
image: "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp"
keywords: "ISO 20022 MCP recipes, MT103 to pacs.008, reconcile camt.053 pain.001, camt.056 cancellation, AP2 pain.001, agent payment recipe"
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
name: "ISO 20022 MCP Suite: recipes."
permalink: "https://sebastienrousseau.com/iso20022-mcp-recipes"
rating: "general"
referrer: "no-referrer"
revisit-after: "7 days"
robots: "index, follow"
short_name: "iso20022-mcp"
subtitle: "Four end-to-end flows an agent runs entirely through the suite: from a legacy MT103 to a validated wire, from a bank statement to a reconciled ledger."
tags: "ISO 20022, MCP, Recipes, MT103, pacs.008, Reconciliation, camt.056, AP2, x402, Agent Payments, Fintech, Open Source"
theme-color: "0, 67, 165"
title: "ISO 20022 MCP Suite: recipes"
url: "https://sebastienrousseau.com/iso20022-mcp-recipes"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"

# RSS - The RSS feed front matter (YAML).
atom_link: "https://sebastienrousseau.com/iso20022-mcp-recipes/rss.xml"
category: "Technology"
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.26)"
item_description: "End-to-end recipes for the ISO 20022 MCP Suite."
item_guid: "https://sebastienrousseau.com/iso20022-mcp-recipes/rss.xml"
item_link: "https://sebastienrousseau.com/iso20022-mcp-recipes/rss.xml"
item_pub_date: "Tue, 14 Jul 2026 06:06:06 +0000"
item_title: "ISO 20022 MCP Suite: recipes"
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
apple-mobile-web-app-title: "ISO 20022 MCP recipes"
apple-touch-fullscreen: "yes"

# MS Application - The MS Application front matter (YAML).

msapplication-navbutton-color: "0, 67, 165"

# Twitter Card - The Twitter Card front matter (YAML).

twitter_card: "summary_large_image"
twitter_creator: "@wwdseb"
twitter_description: "End-to-end recipes for the ISO 20022 MCP Suite: migrate, reconcile, cancel, bridge."
twitter_image: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
twitter_image_alt: "ISO 20022 MCP Suite recipes"
twitter_site: "@wwdseb"
twitter_title: "ISO 20022 MCP Suite: recipes"
twitter_url: "https://sebastienrousseau.com/iso20022-mcp-recipes"

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

<p class="story-intro">Four flows an agent runs end to end, entirely through the published servers. Each is a short chain of tool calls: no glue code, every step validated. New here? Read <a href="/iso20022-mcp-docs/index.html">the quickstart</a> first, or the <a href="/iso20022-mcp-reference/index.html">tool reference</a>.</p>

<section class="newsroom" id="migrate">
<header class="cat-section-head"><p class="cat-kicker">RECIPE 01 · MIGRATE</p><h2 class="cat-headline">A legacy MT103 becomes a validated pacs.008.</h2></header>
<div class="story-why"><ul class="story-why-list">
<li><strong>Convert.</strong> <code>pacs008-mcp · convert_mt103(mt_text)</code> → structured pacs.008 records.</li>
<li><strong>Validate.</strong> <code>validate_records("pacs.008.001.08", records)</code> → schema + rail checks pass.</li>
<li><strong>Generate.</strong> <code>generate_message("pacs.008.001.08", records)</code> → XSD-valid XML, ready for the network.</li>
</ul></div>
<p class="story-intro">The same shape works for <code>convert_mt101</code> → pain.001 and <code>convert_mt940</code>/<code>convert_mt942</code> → camt. Migrate one message type at a time.</p>
</section>

<section class="newsroom" id="reconcile-recipe">
<header class="cat-section-head"><p class="cat-kicker">RECIPE 02 · RECONCILE</p><h2 class="cat-headline">A statement, matched to what you expected.</h2></header>
<div class="story-why"><ul class="story-why-list">
<li><strong>Normalise both sides.</strong> <code>reconcile-mcp · normalize_camt053(statement)</code> and <code>normalize_pain001(payments)</code> → canonical observed + expected records.</li>
<li><strong>Match.</strong> <code>reconcile(expected, observed)</code> → exact matches, short/over payments (with the delta), split settlements and batch credits, each with a reason.</li>
<li><strong>Explain the edge case.</strong> <code>explain_match(expected, observed)</code> → the per-signal score for anything that needs a human.</li>
</ul></div>
<p class="story-intro">No data yet? <code>run_sandbox_scenario("month_end")</code> reconciles a realistic mixed close in one call.</p>
</section>

<section class="newsroom" id="cancel">
<header class="cat-section-head"><p class="cat-kicker">RECIPE 03 · CANCEL &amp; RESOLVE</p><h2 class="cat-headline">Recall a duplicate wire, then close the case.</h2></header>
<div class="story-why"><ul class="story-why-list">
<li><strong>Cancel.</strong> <code>camt-exceptions · generate_message("camt.056", record)</code> with the original payment references and a cancellation reason (e.g. <code>DUPL</code>) → an XSD-valid FI-to-FI Payment Cancellation Request.</li>
<li><strong>Resolve.</strong> When the response comes back, <code>generate_message("camt.029", record)</code> with a confirmation code (e.g. <code>CNCL</code> cancelled, <code>RJCR</code> rejected) → the Resolution of Investigation.</li>
</ul></div>
</section>

<section class="newsroom" id="bridge">
<header class="cat-section-head"><p class="cat-kicker">RECIPE 04 · BRIDGE AN AGENT PAYMENT</p><h2 class="cat-headline">An AP2 mandate becomes a wire-valid pain.001.</h2></header>
<div class="story-why"><ul class="story-why-list">
<li><strong>Normalise.</strong> <code>ap2-iso20022 · normalize_ap2(mandate)</code> → a canonical mandate (works for Coinbase x402 too via <code>normalize_x402</code>).</li>
<li><strong>Guardrail.</strong> <code>check_mandate(mandate, as_of)</code> → required fields present, within the spending cap, not expired, signed. Stop here if it fails.</li>
<li><strong>Convert, then generate.</strong> <code>to_pain001(mandate)</code> → a pain.001 record; hand it to <code>pain001-mcp · generate_message</code> for wire-valid XML. The bridge never moves money; sending stays a separate, human-guarded step.</li>
</ul></div>
</section>

<section class="setup-finale" aria-labelledby="finale-heading"><p class="setup-finale-eyebrow">ONE SUITE · THE WHOLE LIFECYCLE</p><h2 id="finale-heading" class="setup-finale-headline">Compose your own.</h2><p class="setup-finale-lede">These four chain the servers end to end; the gateway lets an agent discover and run any of them from natural language.</p><p class="setup-finale-cta"><a href="/iso20022-mcp-docs/index.html">Quickstart <span aria-hidden="true">›</span></a> · <a href="/iso20022-mcp-reference/index.html">Tool reference <span aria-hidden="true">›</span></a> · <a href="/iso20022-mcp/index.html">The suite <span aria-hidden="true">›</span></a></p></section>
