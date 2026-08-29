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
description: "Tool reference for the ISO 20022 MCP Suite: every server and the tools it exposes, from the gateway and message servers to reconcile, camt-exceptions, bankstatementparser and the AP2/x402 bridge."
format-detection: "telephone=no"
hreflang: "en"
icon: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
id: "https://sebastienrousseau.com/iso20022-mcp-reference"
image_alt: "ISO 20022 MCP Suite tool reference"
image_height: "162"
image_width: "162"
image: "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp"
keywords: "ISO 20022 MCP tools, MCP tool reference, pain001 tools, pacs008 tools, camt053 tools, reconcile-mcp tools, ap2-iso20022 tools, generate_message, validate_records"
last_reviewed: "2026-07-15"
language: "en-GB"
layout: "story"
locale: "en_GB"
logo_alt: "Logo for Sebastien Rousseau"
logo_height: "44"
logo_width: "44"
logo: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
menu: ""
measurementID: "G-169G4ET5HQ"
name: "ISO 20022 MCP Suite: tool reference."
permalink: "https://sebastienrousseau.com/iso20022-mcp-reference"
rating: "general"
referrer: "no-referrer"
revisit-after: "7 days"
robots: "index, follow"
short_name: "iso20022-mcp"
subtitle: "Every server in the suite and the tools it exposes. Nine servers, one consistent contract: JSON in, validated JSON or XSD-checked XML out."
tags: "ISO 20022, MCP, Tool Reference, pain.001, pacs.008, camt.053, acmt.001, Reconciliation, AP2, x402, Fintech, Open Source"
theme-color: "0, 67, 165"
title: "ISO 20022 MCP Suite: tool reference"
url: "https://sebastienrousseau.com/iso20022-mcp-reference"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"

# RSS - The RSS feed front matter (YAML).
atom_link: "https://sebastienrousseau.com/iso20022-mcp-reference/rss.xml"
category: "Technology"
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.26)"
item_description: "Tool reference for the ISO 20022 MCP Suite: every server and the tools it exposes."
item_guid: "https://sebastienrousseau.com/iso20022-mcp-reference/rss.xml"
item_link: "https://sebastienrousseau.com/iso20022-mcp-reference/rss.xml"
item_pub_date: "Tue, 14 Jul 2026 06:06:06 +0000"
item_title: "ISO 20022 MCP Suite: tool reference"
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
apple-mobile-web-app-title: "ISO 20022 MCP reference"
apple-touch-fullscreen: "yes"

# MS Application - The MS Application front matter (YAML).

msapplication-navbutton-color: "0, 67, 165"

# Twitter Card - The Twitter Card front matter (YAML).

twitter_card: "summary_large_image"
twitter_creator: "@wwdseb"
twitter_description: "Tool reference for the ISO 20022 MCP Suite: every server and the tools it exposes."
twitter_image: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
twitter_image_alt: "ISO 20022 MCP Suite tool reference"
twitter_site: "@wwdseb"
twitter_title: "ISO 20022 MCP Suite: tool reference"
twitter_url: "https://sebastienrousseau.com/iso20022-mcp-reference"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://sebastienrousseau.com"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "Thanks for reading!"
site_last_updated: "2026-07-15"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "Kaishi, Kaishi Builder, Kaishi CLI, Kaishi Templates, Kaishi Themes"
site_software: "Static Site Generator, Rust"

---

<p class="story-intro">Every server speaks the same contract: JSON records in, validated JSON or XSD-checked XML out, with an <code>{"error": …}</code> payload rather than an exception when something is wrong. Below is what each exposes. New to the suite? Start with <a href="/iso20022-mcp-docs/index.html">the quickstart</a>.</p>

<!-- Tool catalog: generated from the captured tools/list snapshots in _data/mcp/.
     Do not edit between the markers; regenerate with:
     python3 scripts/generators/render_mcp_reference.py -->
<!-- BEGIN GENERATED: mcp-tool-catalog. Do not edit by hand. -->
<!-- Regenerated from _data/mcp/*.json by scripts/generators/render_mcp_reference.py -->
<p class="ref-totals">9 servers · 87 tools. Every entry below is generated from a live <code>tools/list</code> capture over MCP stdio; nothing is hand-written.</p>
<nav class="ref-index" aria-label="Servers in this reference">
<ol class="ref-index-list">
<li class="ref-index-item">
<a class="ref-index-link" href="#gateway">
<span class="ref-index-name"><code>iso20022-mcp</code></span>
<span class="ref-index-role">Routes search, describe, validate, generate and parse to whichever family server the job needs.</span>
<span class="ref-index-count">7 tools · v0.0.3</span>
</a>
</li>
<li class="ref-index-item">
<a class="ref-index-link" href="#pain001">
<span class="ref-index-name"><code>pain001-mcp</code></span>
<span class="ref-index-role">pain.001 initiation: discovery, IBAN/BIC and XSD validation, generation, migration and MT101 conversion.</span>
<span class="ref-index-count">17 tools · v0.0.55</span>
</a>
</li>
<li class="ref-index-item">
<a class="ref-index-link" href="#pacs008">
<span class="ref-index-name"><code>pacs008-mcp</code></span>
<span class="ref-index-role">pacs.008 interbank settlement plus pacs.004 returns, pacs.002 status, MT103 conversion and the structured-address toolkit.</span>
<span class="ref-index-count">15 tools · v0.0.4</span>
</a>
</li>
<li class="ref-index-item">
<a class="ref-index-link" href="#camt053">
<span class="ref-index-name"><code>camt053-mcp</code></span>
<span class="ref-index-role">camt.053/camt.052 parsing, entry queries, MT94x conversion, reversals and CBPR+ readiness.</span>
<span class="ref-index-count">21 tools · v0.0.12</span>
</a>
</li>
<li class="ref-index-item">
<a class="ref-index-link" href="#reconcile">
<span class="ref-index-name"><code>reconcile-mcp</code></span>
<span class="ref-index-role">Explainable matching of observed statement entries against expected payments, with a zero-data sandbox.</span>
<span class="ref-index-count">7 tools · v0.0.1</span>
</a>
</li>
<li class="ref-index-item">
<a class="ref-index-link" href="#camt-exceptions">
<span class="ref-index-name"><code>camt-exceptions</code></span>
<span class="ref-index-role">camt.056 payment cancellation and camt.029 resolution of investigation, XSD-checked.</span>
<span class="ref-index-count">4 tools · v0.0.2</span>
</a>
</li>
<li class="ref-index-item">
<a class="ref-index-link" href="#ap2">
<span class="ref-index-name"><code>ap2-iso20022</code></span>
<span class="ref-index-role">Normalises AP2/x402 agent mandates, checks guardrails, and emits pain.001/pacs.008-ready records. Never moves money.</span>
<span class="ref-index-count">5 tools · v0.0.1</span>
</a>
</li>
<li class="ref-index-item">
<a class="ref-index-link" href="#acmt001">
<span class="ref-index-name"><code>acmt001-mcp</code></span>
<span class="ref-index-role">acmt.001 account opening, maintenance and verification, validated against the bundled schema.</span>
<span class="ref-index-count">6 tools · v0.0.5</span>
</a>
</li>
<li class="ref-index-item">
<a class="ref-index-link" href="#bankstatementparser">
<span class="ref-index-name"><code>bankstatementparser-mcp</code></span>
<span class="ref-index-role">Format detection and parsing for camt.053, pain.001, MT940, CSV, OFX and QFX statements.</span>
<span class="ref-index-count">5 tools · v1.28.1</span>
</a>
</li>
</ol>
</nav>

<section class="newsroom ref-server" id="gateway">
<header class="cat-section-head">
<p class="cat-kicker">iso20022-mcp · THE GATEWAY</p>
<h2 class="cat-headline">One surface, all families.</h2>
<p class="cat-lede">Routes search, describe, validate, generate and parse to whichever family server the job needs.</p>
</header>
<p class="ref-capture">7 tools · v0.0.3 · captured live over MCP stdio on 2026-07-16 with <code>uvx --from &quot;iso20022-mcp[all]&quot; iso20022-mcp</code></p>
<div class="qa-list ref-tools">
<details class="qa-item ref-tool" id="gateway-search">
<summary class="qa-q">
<span class="ref-tool-name"><code>search</code></span>
<span class="ref-tool-brief">Search the ISO 20022 catalogue by use-case, message type or keyword (e.g. 'reconciliation', 'make a payment', 'pacs.008') and get the matching message types, their family, and which package provides them.</span>
<span class="ref-tool-meta">1 parameter · 0 required</span>
</summary>
<div class="qa-a ref-tool-body">
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of search</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>query</code></td>
<td>string</td>
<td><span class="ref-req ref-req-optional">Optional</span></td>
<td>Use-case, message type or keyword. Empty = all.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="gateway-list_families">
<summary class="qa-q">
<span class="ref-tool-name"><code>list_families</code></span>
<span class="ref-tool-brief">List every ISO 20022 family the gateway routes to (pain, pacs, camt, acmt): its capabilities, backing package, and whether that package is installed in this environment.</span>
<span class="ref-tool-meta">No parameters</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-noparams">This tool takes no parameters.</p>
</div>
</details>
<details class="qa-item ref-tool" id="gateway-list_servers">
<summary class="qa-q">
<span class="ref-tool-name"><code>list_servers</code></span>
<span class="ref-tool-brief">List the whole ISO 20022 suite the gateway knows: the message families (pain/pacs/camt/acmt), the Exceptions &amp; Investigations messages (camt.056/camt.029), and the specialized servers (reconciliation, agent-payment bridge) with what each does.</span>
<span class="ref-tool-meta">No parameters</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-noparams">This tool takes no parameters.</p>
</div>
</details>
<details class="qa-item ref-tool" id="gateway-describe">
<summary class="qa-q">
<span class="ref-tool-name"><code>describe</code></span>
<span class="ref-tool-brief">Describe a message type: its required fields and input JSON Schema, resolved from the family's backing server.</span>
<span class="ref-tool-meta">1 parameter · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of describe</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>message_type</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>ISO 20022 message type or family prefix, e.g. 'pacs.008' or 'camt.053'.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="gateway-validate">
<summary class="qa-q">
<span class="ref-tool-name"><code>validate</code></span>
<span class="ref-tool-brief">Validate records for a message type against its JSON Schema, via the family's backing server.</span>
<span class="ref-tool-meta">2 parameters · 2 required</span>
</summary>
<div class="qa-a ref-tool-body">
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of validate</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>message_type</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>ISO 20022 message type or family prefix, e.g. 'pacs.008' or 'camt.053'.</td>
</tr>
<tr>
<td><code>records</code></td>
<td>array of object</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>List of record objects to validate or generate a message from.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="gateway-generate">
<summary class="qa-q">
<span class="ref-tool-name"><code>generate</code></span>
<span class="ref-tool-brief">Generate a validated ISO 20022 XML message from records; the XML document is returned in the 'xml' key. Supported for initiation and interbank families (pain, pacs, acmt); statement families (camt) are inbound-only and return an explanatory error.</span>
<span class="ref-tool-meta">2 parameters · 2 required</span>
</summary>
<div class="qa-a ref-tool-body">
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of generate</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>message_type</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>ISO 20022 message type or family prefix, e.g. 'pacs.008' or 'camt.053'.</td>
</tr>
<tr>
<td><code>records</code></td>
<td>array of object</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>List of record objects to validate or generate a message from.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="gateway-parse">
<summary class="qa-q">
<span class="ref-tool-name"><code>parse</code></span>
<span class="ref-tool-brief">Parse an inbound ISO 20022 XML message into structured data. Supported for interbank (pacs) and statement (camt) families; initiation families return an explanatory error.</span>
<span class="ref-tool-meta">2 parameters · 2 required</span>
</summary>
<div class="qa-a ref-tool-body">
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of parse</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>message_type</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>ISO 20022 message type or family prefix, e.g. 'pacs.008' or 'camt.053'.</td>
</tr>
<tr>
<td><code>xml</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>Raw ISO 20022 XML to parse.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
</div>
</section>

<section class="newsroom ref-server" id="pain001">
<header class="cat-section-head">
<p class="cat-kicker">pain001-mcp · INITIATE</p>
<h2 class="cat-headline">Customer credit transfers.</h2>
<p class="cat-lede">pain.001 initiation: discovery, IBAN/BIC and XSD validation, generation, migration and MT101 conversion.</p>
</header>
<p class="ref-capture">17 tools · v0.0.55 · captured live over MCP stdio on 2026-07-15 with <code>uvx --from &quot;pain001-mcp&quot; pain001-mcp</code></p>
<div class="qa-list ref-tools">
<details class="qa-item ref-tool" id="pain001-list_message_types">
<summary class="qa-q">
<span class="ref-tool-name"><code>list_message_types</code></span>
<span class="ref-tool-brief">List every supported ISO 20022 pain message type and its human name.</span>
<span class="ref-tool-meta">No parameters</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this first, before any generation or validation call, to discover the exact <code>message_type</code> strings this server accepts. Do not use it to fetch a type's fields or schema - call <code>get_required_fields</code> or <code>get_input_schema</code> for that.</p>
<p class="ref-tool-desc">Returns a list of <code>{"message_type": ..., "name": ...}</code> dictionaries, one per supported message type (e.g. <code>pain.001.001.09</code>).</p>
<p class="ref-noparams">This tool takes no parameters.</p>
</div>
</details>
<details class="qa-item ref-tool" id="pain001-get_required_fields">
<summary class="qa-q">
<span class="ref-tool-name"><code>get_required_fields</code></span>
<span class="ref-tool-brief">List only the required input field names for a pain message type.</span>
<span class="ref-tool-meta">1 parameter · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this for a quick checklist of the mandatory columns before building records. When you need full type/format constraints (not just which fields are required), call <code>get_input_schema</code> instead.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of get_required_fields</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>message_type</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>A supported ISO 20022 pain message type. Must be exactly one of: 'pain.001.001.03', 'pain.001.001.04', 'pain.001.001.05', 'pain.001.001.06', 'pain.001.001.07', 'pain.001.001.08', 'pain.001.001.09', 'pain.001.001.10', 'pain.001.001.11', 'pain.001.001.12', 'pain.008.001.02' (see list_message_types). One of: <code>pain.001.001.03</code> · <code>pain.001.001.04</code> · <code>pain.001.001.05</code> · <code>pain.001.001.06</code> · <code>pain.001.001.07</code> · <code>pain.001.001.08</code> · <code>pain.001.001.09</code> · <code>pain.001.001.10</code> · <code>pain.001.001.11</code> · <code>pain.001.001.12</code> · <code>pain.008.001.02</code>.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="pain001-get_input_schema">
<summary class="qa-q">
<span class="ref-tool-name"><code>get_input_schema</code></span>
<span class="ref-tool-brief">Return the full JSON Schema for a message type's flat input record.</span>
<span class="ref-tool-meta">1 parameter · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this to learn every field, its type, and its constraints before assembling records, or to drive a form/UI. For just the required-field names use <code>get_required_fields</code>; to actually check records against this schema use <code>validate_records</code>.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of get_input_schema</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>message_type</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>A supported ISO 20022 pain message type. Must be exactly one of: 'pain.001.001.03', 'pain.001.001.04', 'pain.001.001.05', 'pain.001.001.06', 'pain.001.001.07', 'pain.001.001.08', 'pain.001.001.09', 'pain.001.001.10', 'pain.001.001.11', 'pain.001.001.12', 'pain.008.001.02' (see list_message_types). One of: <code>pain.001.001.03</code> · <code>pain.001.001.04</code> · <code>pain.001.001.05</code> · <code>pain.001.001.06</code> · <code>pain.001.001.07</code> · <code>pain.001.001.08</code> · <code>pain.001.001.09</code> · <code>pain.001.001.10</code> · <code>pain.001.001.11</code> · <code>pain.001.001.12</code> · <code>pain.008.001.02</code>.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="pain001-validate_records">
<summary class="qa-q">
<span class="ref-tool-name"><code>validate_records</code></span>
<span class="ref-tool-brief">Validate flat records against a message type's input JSON Schema.</span>
<span class="ref-tool-meta">2 parameters · 2 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this before <code>generate_message</code> to catch structural/type errors per record and get a row-by-row error report. This checks JSON-Schema shape only; for payment-scheme rulebook checks (SEPA field lengths, charset, etc.) also run <code>validate_payment_scheme</code>.</p>
<p class="ref-tool-desc">Returns a report <code>{"valid": bool, "total": int, "valid_count": int, "errors": [...]}</code>.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of validate_records</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>message_type</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>A supported ISO 20022 pain message type. Must be exactly one of: 'pain.001.001.03', 'pain.001.001.04', 'pain.001.001.05', 'pain.001.001.06', 'pain.001.001.07', 'pain.001.001.08', 'pain.001.001.09', 'pain.001.001.10', 'pain.001.001.11', 'pain.001.001.12', 'pain.008.001.02' (see list_message_types). One of: <code>pain.001.001.03</code> · <code>pain.001.001.04</code> · <code>pain.001.001.05</code> · <code>pain.001.001.06</code> · <code>pain.001.001.07</code> · <code>pain.001.001.08</code> · <code>pain.001.001.09</code> · <code>pain.001.001.10</code> · <code>pain.001.001.11</code> · <code>pain.001.001.12</code> · <code>pain.008.001.02</code>.</td>
</tr>
<tr>
<td><code>records</code></td>
<td>array of object</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>One or more flat payment records to validate, each a dict of field name → value (see get_input_schema for the fields and get_required_fields for the mandatory ones).</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="pain001-validate_identifier">
<summary class="qa-q">
<span class="ref-tool-name"><code>validate_identifier</code></span>
<span class="ref-tool-brief">Validate a single financial identifier (IBAN or BIC).</span>
<span class="ref-tool-meta">2 parameters · 2 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this for a one-off identifier check with a clear pass/fail and reason. To validate identifiers embedded across a whole batch, prefer <code>validate_records</code> / <code>validate_payment_scheme</code> instead of calling this per field.</p>
<p class="ref-tool-desc">Returns <code>{"kind": str, "value": str, "valid": bool, "error": str}</code> (the <code>error</code> key is present only when <code>valid</code> is <code>False</code>).</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of validate_identifier</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>kind</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>Which identifier to validate: 'iban' or 'bic' (case-insensitive). Any other value returns an error.</td>
</tr>
<tr>
<td><code>value</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>The identifier string to check - an IBAN or BIC/SWIFT code matching the chosen kind.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="pain001-generate_message">
<summary class="qa-q">
<span class="ref-tool-name"><code>generate_message</code></span>
<span class="ref-tool-brief">Generate a validated ISO 20022 pain XML message from in-memory records.</span>
<span class="ref-tool-meta">2 parameters · 2 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">This is the primary generation tool: pass records you already hold in memory. Use <code>generate_message_from_file</code> when the data lives in a CSV on disk, and <code>generate_message_async</code> for very large batches you want to run off the event loop. The result is XSD-validated before return; no file is written.</p>
<p class="ref-tool-desc">Returns the validated XML document as a string, or a JSON-encoded <code>{"error": ...}</code> payload if generation fails.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of generate_message</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>message_type</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>A supported ISO 20022 pain message type. Must be exactly one of: 'pain.001.001.03', 'pain.001.001.04', 'pain.001.001.05', 'pain.001.001.06', 'pain.001.001.07', 'pain.001.001.08', 'pain.001.001.09', 'pain.001.001.10', 'pain.001.001.11', 'pain.001.001.12', 'pain.008.001.02' (see list_message_types). One of: <code>pain.001.001.03</code> · <code>pain.001.001.04</code> · <code>pain.001.001.05</code> · <code>pain.001.001.06</code> · <code>pain.001.001.07</code> · <code>pain.001.001.08</code> · <code>pain.001.001.09</code> · <code>pain.001.001.10</code> · <code>pain.001.001.11</code> · <code>pain.001.001.12</code> · <code>pain.008.001.02</code>.</td>
</tr>
<tr>
<td><code>records</code></td>
<td>array of object</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>One or more flat payment records (each a dict of field name → value) to render into the XML; validate them first with validate_records. See get_input_schema for the fields.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="pain001-list_supported_formats">
<summary class="qa-q">
<span class="ref-tool-name"><code>list_supported_formats</code></span>
<span class="ref-tool-brief">List the on-disk data formats the pain001 loader can read.</span>
<span class="ref-tool-meta">No parameters</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this to tell a user which file types they may supply to <code>generate_message_from_file</code>. This lists <em>data-source</em> formats (CSV, SQLite, …); for the list of ISO 20022 <em>message</em> types call <code>list_message_types</code> instead.</p>
<p class="ref-tool-desc">Returns a list of <code>{"id", "name", "extension"}</code> dictionaries covering CSV, SQLite, JSON, JSONL, and Parquet (the last requires the <code>pain001[parquet]</code> extra).</p>
<p class="ref-noparams">This tool takes no parameters.</p>
</div>
</details>
<details class="qa-item ref-tool" id="pain001-generate_message_async">
<summary class="qa-q">
<span class="ref-tool-name"><code>generate_message_async</code></span>
<span class="ref-tool-brief">Generate validated pain XML off the event loop, for large batches.</span>
<span class="ref-tool-meta">2 parameters · 2 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Behaves exactly like <code>generate_message</code> but runs the synchronous renderer in a worker thread so an agent can interleave a long generation with other tool calls. Use <code>generate_message</code> for small or interactive batches; use this only when the record count is large enough that blocking would matter.</p>
<p class="ref-tool-desc">Delegates to <code>pain001.async_adapter.generate_xml_string_async</code>. Returns the validated XML, or a JSON-encoded <code>{"error": ...}</code> payload.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of generate_message_async</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>message_type</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>A supported ISO 20022 pain message type. Must be exactly one of: 'pain.001.001.03', 'pain.001.001.04', 'pain.001.001.05', 'pain.001.001.06', 'pain.001.001.07', 'pain.001.001.08', 'pain.001.001.09', 'pain.001.001.10', 'pain.001.001.11', 'pain.001.001.12', 'pain.008.001.02' (see list_message_types). One of: <code>pain.001.001.03</code> · <code>pain.001.001.04</code> · <code>pain.001.001.05</code> · <code>pain.001.001.06</code> · <code>pain.001.001.07</code> · <code>pain.001.001.08</code> · <code>pain.001.001.09</code> · <code>pain.001.001.10</code> · <code>pain.001.001.11</code> · <code>pain.001.001.12</code> · <code>pain.008.001.02</code>.</td>
</tr>
<tr>
<td><code>records</code></td>
<td>array of object</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>One or more flat payment records (each a dict of field name → value) to render into the XML; use this async variant only when the batch is large. See get_input_schema.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="pain001-generate_message_from_file">
<summary class="qa-q">
<span class="ref-tool-name"><code>generate_message_from_file</code></span>
<span class="ref-tool-brief">Generate validated pain XML from a CSV file on the local disk.</span>
<span class="ref-tool-meta">2 parameters · 2 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this when the records live in a CSV file rather than in memory; it reads <code>data_file_path</code> from the local filesystem, then delegates to <code>generate_message</code>. If you already have the records as dicts, call <code>generate_message</code> directly. Only CSV is supported today (JSON / JSONL / SQLite / Parquet are planned for a follow-up release).</p>
<p class="ref-tool-desc">Loads <code>data_file_path</code> via <code>pain001.csv.load_csv_data.load_csv_data</code> so the same path-safety guards apply as in the core library.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of generate_message_from_file</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>message_type</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>A supported ISO 20022 pain message type. Must be exactly one of: 'pain.001.001.03', 'pain.001.001.04', 'pain.001.001.05', 'pain.001.001.06', 'pain.001.001.07', 'pain.001.001.08', 'pain.001.001.09', 'pain.001.001.10', 'pain.001.001.11', 'pain.001.001.12', 'pain.008.001.02' (see list_message_types). One of: <code>pain.001.001.03</code> · <code>pain.001.001.04</code> · <code>pain.001.001.05</code> · <code>pain.001.001.06</code> · <code>pain.001.001.07</code> · <code>pain.001.001.08</code> · <code>pain.001.001.09</code> · <code>pain.001.001.10</code> · <code>pain.001.001.11</code> · <code>pain.001.001.12</code> · <code>pain.008.001.02</code>.</td>
</tr>
<tr>
<td><code>data_file_path</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>Local filesystem path to a CSV file with one payment record per row and a header matching the template columns (see inspect_template). Only CSV is supported today.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="pain001-parse_camt053">
<summary class="qa-q">
<span class="ref-tool-name"><code>parse_camt053</code></span>
<span class="ref-tool-brief">Parse a camt.053 bank-statement XML file on disk into structured data.</span>
<span class="ref-tool-meta">2 parameters · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this to read a bank's account statement (the reply that confirms settlement) into a header + entry list. Reads <code>xml_file_path</code> from the local filesystem. For the payment-status reply (accepted/rejected per transaction) use <code>parse_pain002</code> instead; to validate a camt.053 string you already hold, this is not it - this tool needs a file path.</p>
<p class="ref-tool-desc">Wraps <code>pain001.parse_camt053_statement</code>. When <code>xsd_file_path</code> is provided, the document is first validated against that XSD; on a schema or parse error the tool returns <code>{"error": ...}</code> rather than raising.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of parse_camt053</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>xml_file_path</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>Local filesystem path to the camt.053 bank-statement XML file to parse.</td>
</tr>
<tr>
<td><code>xsd_file_path</code></td>
<td>string, nullable</td>
<td><span class="ref-req ref-req-optional">Optional</span></td>
<td>Optional local path to a camt.053 XSD; when given, the document is validated against it before parsing. Omit to skip schema validation.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="pain001-parse_pain002">
<summary class="qa-q">
<span class="ref-tool-name"><code>parse_pain002</code></span>
<span class="ref-tool-brief">Parse a pain.002 payment-status report file on disk into structured data.</span>
<span class="ref-tool-meta">2 parameters · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this to read the bank's acknowledgement of a submitted pain.001 - the per-transaction accepted/rejected status and reason codes. Reads <code>xml_file_path</code> from the local filesystem. For the account statement that later confirms booked entries, use <code>parse_camt053</code> instead.</p>
<p class="ref-tool-desc">Wraps <code>pain001.parse_pain002_report</code>. When <code>xsd_file_path</code> is provided, the document is first validated against that XSD; on a schema or parse error the tool returns <code>{"error": ...}</code> rather than raising.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of parse_pain002</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>xml_file_path</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>Local filesystem path to the pain.002 payment-status report XML file to parse.</td>
</tr>
<tr>
<td><code>xsd_file_path</code></td>
<td>string, nullable</td>
<td><span class="ref-req ref-req-optional">Optional</span></td>
<td>Optional local path to a pain.002 XSD; when given, the document is validated against it before parsing. Omit to skip schema validation.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="pain001-inspect_template">
<summary class="qa-q">
<span class="ref-tool-name"><code>inspect_template</code></span>
<span class="ref-tool-brief">Return the CSV column headers the message type's bundled template uses.</span>
<span class="ref-tool-meta">1 parameter · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this to see the exact column order for hand-building a CSV before <code>generate_message_from_file</code>. This returns column <em>names</em> from the bundled sample; for the typed JSON contract (types, required flags) use <code>get_input_schema</code>.</p>
<p class="ref-tool-desc">Mirrors the in-tree <code>pain001.mcp.server.inspect_template</code> tool so an agent can introspect the column layout before assembling rows.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of inspect_template</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>message_type</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>A supported ISO 20022 pain message type. Must be exactly one of: 'pain.001.001.03', 'pain.001.001.04', 'pain.001.001.05', 'pain.001.001.06', 'pain.001.001.07', 'pain.001.001.08', 'pain.001.001.09', 'pain.001.001.10', 'pain.001.001.11', 'pain.001.001.12', 'pain.008.001.02' (see list_message_types). One of: <code>pain.001.001.03</code> · <code>pain.001.001.04</code> · <code>pain.001.001.05</code> · <code>pain.001.001.06</code> · <code>pain.001.001.07</code> · <code>pain.001.001.08</code> · <code>pain.001.001.09</code> · <code>pain.001.001.10</code> · <code>pain.001.001.11</code> · <code>pain.001.001.12</code> · <code>pain.008.001.02</code>.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="pain001-validate_payment_scheme">
<summary class="qa-q">
<span class="ref-tool-name"><code>validate_payment_scheme</code></span>
<span class="ref-tool-brief">Validate records against a payment-scheme rulebook (e.g. SEPA).</span>
<span class="ref-tool-meta">2 parameters · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this after <code>validate_records</code> to enforce scheme-specific business rules (SEPA field lengths, allowed characters, currency/BIC constraints) that JSON-Schema validation alone does not cover. <code>validate_records</code> checks structural shape; this checks rulebook compliance for one profile.</p>
<p class="ref-tool-desc">Delegates to <code>pain001.validate_scheme</code>. Supported profiles: <code>sepa-sct</code>, <code>sepa-sdd</code>, <code>sepa-inst</code>, <code>xborder-ct</code>.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of validate_payment_scheme</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>records</code></td>
<td>array of object</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>Payment records as a list of flat dicts (field name → value) to check against the scheme rulebook.</td>
</tr>
<tr>
<td><code>profile</code></td>
<td>string</td>
<td><span class="ref-req ref-req-optional">Optional</span></td>
<td>The payment-scheme rulebook profile to enforce. One of 'sepa-sct', 'sepa-sdd', 'sepa-inst', or 'xborder-ct'. Defaults to 'sepa-sct'. Default: <code>&quot;sepa-sct&quot;</code>.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="pain001-migrate_records">
<summary class="qa-q">
<span class="ref-tool-name"><code>migrate_records</code></span>
<span class="ref-tool-brief">Migrate flat payment records between two pain.001 schema versions.</span>
<span class="ref-tool-meta">3 parameters · 3 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this to upgrade/downgrade records when your bank requires a different pain.001 version than your source data uses (e.g. move <code>.03</code> rows to <code>.09</code>); it reports which fields were renamed, derived, or dropped. This transforms records only - run <code>validate_records</code> afterwards, then <code>generate_message</code> to emit XML.</p>
<p class="ref-tool-desc">Wraps <code>pain001.migration.VersionMapper</code>. Returns the migrated rows plus a summary of which fields were renamed, derived, or dropped; <code>{"error": ...}</code> if either version is unsupported.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of migrate_records</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>records</code></td>
<td>array of object</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>Flat payment records in the from_version shape, each a dict of field name → value, to transform to to_version.</td>
</tr>
<tr>
<td><code>from_version</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>Source pain.001 schema version the records currently use, e.g. 'pain.001.001.03' - see list_message_types.</td>
</tr>
<tr>
<td><code>to_version</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>Target pain.001 schema version to migrate the records to, e.g. 'pain.001.001.09' - see list_message_types.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="pain001-validate_xml_against_schema">
<summary class="qa-q">
<span class="ref-tool-name"><code>validate_xml_against_schema</code></span>
<span class="ref-tool-brief">Validate a raw pain.001 / pain.008 XML string against its official XSD.</span>
<span class="ref-tool-meta">2 parameters · 2 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this to check XML you already have as a string (e.g. received from another system) without touching the filesystem. To validate records <em>before</em> they become XML, use <code>validate_records</code>; to parse a statement or status-report file, use <code>parse_camt053</code> / <code>parse_pain002</code>.</p>
<p class="ref-tool-desc">Wraps <code>pain001.xml.validate_via_xsd.validate_xml_string_via_xsd</code>.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of validate_xml_against_schema</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>xml_content</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>The full pain.001 / pain.008 XML document as a string, validated against the message type's official XSD.</td>
</tr>
<tr>
<td><code>message_type</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>A supported ISO 20022 pain message type. Must be exactly one of: 'pain.001.001.03', 'pain.001.001.04', 'pain.001.001.05', 'pain.001.001.06', 'pain.001.001.07', 'pain.001.001.08', 'pain.001.001.09', 'pain.001.001.10', 'pain.001.001.11', 'pain.001.001.12', 'pain.008.001.02' (see list_message_types). One of: <code>pain.001.001.03</code> · <code>pain.001.001.04</code> · <code>pain.001.001.05</code> · <code>pain.001.001.06</code> · <code>pain.001.001.07</code> · <code>pain.001.001.08</code> · <code>pain.001.001.09</code> · <code>pain.001.001.10</code> · <code>pain.001.001.11</code> · <code>pain.001.001.12</code> · <code>pain.008.001.02</code>.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="pain001-sanitize_to_iso20022_charset">
<summary class="qa-q">
<span class="ref-tool-name"><code>sanitize_to_iso20022_charset</code></span>
<span class="ref-tool-brief">Sanitise one free-text field to the ISO 20022 Latin character set.</span>
<span class="ref-tool-meta">1 parameter · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this on a single free-text value (name, remittance info) to transliterate accents and drop unsupported symbols before placing it in a record, and to see whether the value changed. Operates on one string; to check a whole batch's rulebook compliance use <code>validate_payment_scheme</code>.</p>
<p class="ref-tool-desc">Wraps <code>pain001.sanitize_to_charset</code>. Transliterates accents (<code>é</code> -&gt; <code>e</code>), removes unsupported symbols, and returns both the cleaned string and a flag for whether the original was already valid - useful for surfacing the change to the user before writing it back to a record.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of sanitize_to_iso20022_charset</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>value</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>A single free-text field value (e.g. a name or remittance line) to transliterate to the ISO 20022 Latin character set.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="pain001-convert_mt101">
<summary class="qa-q">
<span class="ref-tool-name"><code>convert_mt101</code></span>
<span class="ref-tool-brief">Convert a legacy SWIFT MT101 message into pain.001-ready records.</span>
<span class="ref-tool-meta">1 parameter · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this to bridge the Nov-2025+ SWIFT MT→MX migration: parse an MT101 (<em>Request for Transfer</em>) into the flat records the other tools consume - feed the result straight to <code>validate_records</code> / <code>validate_payment_scheme</code> and then <code>generate_message</code> to emit pain.001.001.09 XML. An MT101 can request many transfers (repeating sequence B), so this returns <em>one record per transaction</em>. Operates on the supplied text only; no file is read or written.</p>
<p class="ref-tool-desc">Wraps <code>pain001_loader_mt101.loader.parse_mt101</code>. Sequence-A ordering-customer / account-servicing fields apply to every transaction unless a sequence-B block overrides them; fields the MT101 does not carry are synthesised to schema defaults (<code>payment_method</code> <code>"TRF"</code>, <code>service_level_code</code> <code>"SEPA"</code>, etc.).</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of convert_mt101</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>mt101_text</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>A legacy SWIFT MT101 (Request for Transfer) message as text - a bare ':tag:' field list or a raw '{4:...-}' block-4 envelope. An MT101 may carry several sequence-B transfers; each becomes its own record.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
</div>
</section>

<section class="newsroom ref-server" id="pacs008">
<header class="cat-section-head">
<p class="cat-kicker">pacs008-mcp · SETTLE</p>
<h2 class="cat-headline">FI-to-FI transfers, returns, status.</h2>
<p class="cat-lede">pacs.008 interbank settlement plus pacs.004 returns, pacs.002 status, MT103 conversion and the structured-address toolkit.</p>
</header>
<p class="ref-capture">15 tools · v0.0.4 · captured live over MCP stdio on 2026-07-15 with <code>uvx --from &quot;pacs008-mcp&quot; pacs008-mcp</code></p>
<div class="qa-list ref-tools">
<details class="qa-item ref-tool" id="pacs008-list_message_types">
<summary class="qa-q">
<span class="ref-tool-name"><code>list_message_types</code></span>
<span class="ref-tool-brief">List every supported ISO 20022 pacs message type and its human name.</span>
<span class="ref-tool-meta">No parameters</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this first, before any generation or validation call, to discover the exact <code>message_type</code> strings this server accepts (e.g. <code>pacs.008.001.08</code> FI-to-FI Customer Credit Transfer). To learn a type's required fields or full schema, call <code>get_required_fields</code> or <code>get_input_schema</code> instead.</p>
<p class="ref-tool-desc">Returns a list of <code>{"message_type": ..., "name": ...}</code> dictionaries, one per supported message type.</p>
<p class="ref-noparams">This tool takes no parameters.</p>
</div>
</details>
<details class="qa-item ref-tool" id="pacs008-list_schemes">
<summary class="qa-q">
<span class="ref-tool-name"><code>list_schemes</code></span>
<span class="ref-tool-brief">List every registered scheme / usage-guideline profile.</span>
<span class="ref-tool-meta">No parameters</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Scheme profiles (CBPR+, HVPS+, Fedwire, CHAPS, T2 RTGS, SCT Inst, generic) layer rail-specific rules on top of base ISO 20022. Use this to discover the <code>scheme</code> names accepted by <code>get_scheme</code> and <code>validate_scheme</code>.</p>
<p class="ref-tool-desc">Registry aliases (e.g. <code>cbpr+</code>, <code>cbprplus</code>) collapse to their canonical profile, so each profile appears exactly once. Returns a list of <code>{"scheme": ..., "name": ...}</code> dictionaries.</p>
<p class="ref-noparams">This tool takes no parameters.</p>
</div>
</details>
<details class="qa-item ref-tool" id="pacs008-get_scheme">
<summary class="qa-q">
<span class="ref-tool-name"><code>get_scheme</code></span>
<span class="ref-tool-brief">Return the rule attributes of a scheme / usage-guideline profile.</span>
<span class="ref-tool-meta">1 parameter · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this to inspect a rail's constraints -- whether the UETR is mandatory, the permitted charge bearers, remittance-info length cap, per-message transaction cardinality, pinned message versions, and which parties must carry an LEI -- before assembling or validating a batch.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of get_scheme</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>scheme</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>A registered scheme / usage-guideline profile name (case-insensitive), e.g. 'cbpr_plus', 'fedwire', 'chaps'. Must be one of: 'cbpr+', 'cbpr_plus', 'cbprplus', 'chaps', 'fedwire', 'generic', 'hvps+', 'hvps_plus', 'hvpsplus', 'sct-inst', 'sct_inst', 'sctinst', 't2_rtgs', 't2rtgs', 'target2' (see list_schemes). One of: <code>cbpr+</code> · <code>cbpr_plus</code> · <code>cbprplus</code> · <code>chaps</code> · <code>fedwire</code> · <code>generic</code> · <code>hvps+</code> · <code>hvps_plus</code> · <code>hvpsplus</code> · <code>sct-inst</code> · <code>sct_inst</code> · <code>sctinst</code> · <code>t2_rtgs</code> · <code>t2rtgs</code> · <code>target2</code>.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="pacs008-get_required_fields">
<summary class="qa-q">
<span class="ref-tool-name"><code>get_required_fields</code></span>
<span class="ref-tool-brief">List only the required input field names for a pacs message type.</span>
<span class="ref-tool-meta">1 parameter · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this for a quick checklist of the mandatory columns before building payment records. For full type/format constraints (not just which fields are required), call <code>get_input_schema</code> instead.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of get_required_fields</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>message_type</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>A supported ISO 20022 pacs message type, e.g. 'pacs.008.001.08' FI-to-FI Customer Credit Transfer. Must be exactly one of: 'pacs.002.001.12', 'pacs.003.001.09', 'pacs.004.001.11', 'pacs.007.001.11', 'pacs.008.001.01', 'pacs.008.001.02', 'pacs.008.001.03', 'pacs.008.001.04', 'pacs.008.001.05', 'pacs.008.001.06', 'pacs.008.001.07', 'pacs.008.001.08', 'pacs.008.001.09', 'pacs.008.001.10', 'pacs.008.001.11', 'pacs.008.001.12', 'pacs.008.001.13', 'pacs.009.001.10', 'pacs.010.001.05', 'pacs.028.001.05' (see list_message_types). One of: <code>pacs.002.001.12</code> · <code>pacs.003.001.09</code> · <code>pacs.004.001.11</code> · <code>pacs.007.001.11</code> · <code>pacs.008.001.01</code> · <code>pacs.008.001.02</code> · <code>pacs.008.001.03</code> · <code>pacs.008.001.04</code> · <code>pacs.008.001.05</code> · <code>pacs.008.001.06</code> · <code>pacs.008.001.07</code> · <code>pacs.008.001.08</code> · <code>pacs.008.001.09</code> · <code>pacs.008.001.10</code> · <code>pacs.008.001.11</code> · <code>pacs.008.001.12</code> · <code>pacs.008.001.13</code> · <code>pacs.009.001.10</code> · <code>pacs.010.001.05</code> · <code>pacs.028.001.05</code>.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="pacs008-get_input_schema">
<summary class="qa-q">
<span class="ref-tool-name"><code>get_input_schema</code></span>
<span class="ref-tool-brief">Return the full JSON Schema for a message type's flat input record.</span>
<span class="ref-tool-meta">1 parameter · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this to learn every field, its type, and its constraints before assembling records, or to drive a form/UI. For just the required-field names use <code>get_required_fields</code>; to check records against this schema use <code>validate_records</code>.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of get_input_schema</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>message_type</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>A supported ISO 20022 pacs message type, e.g. 'pacs.008.001.08' FI-to-FI Customer Credit Transfer. Must be exactly one of: 'pacs.002.001.12', 'pacs.003.001.09', 'pacs.004.001.11', 'pacs.007.001.11', 'pacs.008.001.01', 'pacs.008.001.02', 'pacs.008.001.03', 'pacs.008.001.04', 'pacs.008.001.05', 'pacs.008.001.06', 'pacs.008.001.07', 'pacs.008.001.08', 'pacs.008.001.09', 'pacs.008.001.10', 'pacs.008.001.11', 'pacs.008.001.12', 'pacs.008.001.13', 'pacs.009.001.10', 'pacs.010.001.05', 'pacs.028.001.05' (see list_message_types). One of: <code>pacs.002.001.12</code> · <code>pacs.003.001.09</code> · <code>pacs.004.001.11</code> · <code>pacs.007.001.11</code> · <code>pacs.008.001.01</code> · <code>pacs.008.001.02</code> · <code>pacs.008.001.03</code> · <code>pacs.008.001.04</code> · <code>pacs.008.001.05</code> · <code>pacs.008.001.06</code> · <code>pacs.008.001.07</code> · <code>pacs.008.001.08</code> · <code>pacs.008.001.09</code> · <code>pacs.008.001.10</code> · <code>pacs.008.001.11</code> · <code>pacs.008.001.12</code> · <code>pacs.008.001.13</code> · <code>pacs.009.001.10</code> · <code>pacs.010.001.05</code> · <code>pacs.028.001.05</code>.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="pacs008-validate_records">
<summary class="qa-q">
<span class="ref-tool-name"><code>validate_records</code></span>
<span class="ref-tool-brief">Validate flat payment records against a message type's JSON Schema.</span>
<span class="ref-tool-meta">2 parameters · 2 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this before <code>generate_message</code> to catch structural/type errors per record and get a row-by-row error report. This checks JSON-Schema shape only; to check a batch against a rail's usage guidelines use <code>validate_scheme</code>.</p>
<p class="ref-tool-desc">Returns a report <code>{"is_valid": bool, "total": int, "valid": int, "errors": [...]}</code>.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of validate_records</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>message_type</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>A supported ISO 20022 pacs message type, e.g. 'pacs.008.001.08' FI-to-FI Customer Credit Transfer. Must be exactly one of: 'pacs.002.001.12', 'pacs.003.001.09', 'pacs.004.001.11', 'pacs.007.001.11', 'pacs.008.001.01', 'pacs.008.001.02', 'pacs.008.001.03', 'pacs.008.001.04', 'pacs.008.001.05', 'pacs.008.001.06', 'pacs.008.001.07', 'pacs.008.001.08', 'pacs.008.001.09', 'pacs.008.001.10', 'pacs.008.001.11', 'pacs.008.001.12', 'pacs.008.001.13', 'pacs.009.001.10', 'pacs.010.001.05', 'pacs.028.001.05' (see list_message_types). One of: <code>pacs.002.001.12</code> · <code>pacs.003.001.09</code> · <code>pacs.004.001.11</code> · <code>pacs.007.001.11</code> · <code>pacs.008.001.01</code> · <code>pacs.008.001.02</code> · <code>pacs.008.001.03</code> · <code>pacs.008.001.04</code> · <code>pacs.008.001.05</code> · <code>pacs.008.001.06</code> · <code>pacs.008.001.07</code> · <code>pacs.008.001.08</code> · <code>pacs.008.001.09</code> · <code>pacs.008.001.10</code> · <code>pacs.008.001.11</code> · <code>pacs.008.001.12</code> · <code>pacs.008.001.13</code> · <code>pacs.009.001.10</code> · <code>pacs.010.001.05</code> · <code>pacs.028.001.05</code>.</td>
</tr>
<tr>
<td><code>records</code></td>
<td>array of object</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>One or more flat payment records, each a dict of field name -&gt; value; validated against the message type's input JSON Schema (see get_input_schema / get_required_fields).</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="pacs008-validate_scheme">
<summary class="qa-q">
<span class="ref-tool-name"><code>validate_scheme</code></span>
<span class="ref-tool-brief">Validate payment records against a scheme's usage-guideline rules.</span>
<span class="ref-tool-meta">2 parameters · 2 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this to check a batch against a rail's rulebook (CBPR+, HVPS+, Fedwire, CHAPS, T2 RTGS, SCT Inst) -- charge-bearer restrictions, UETR presence, remittance-info length, and per-message transaction cardinality. This is complementary to <code>validate_records</code> (JSON-Schema shape).</p>
<p class="ref-tool-desc">Returns <code>{"scheme": str, "is_valid": bool, "total": int, "violations": [...]}</code>.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of validate_scheme</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>scheme</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>A registered scheme / usage-guideline profile name (case-insensitive), e.g. 'cbpr_plus', 'fedwire', 'chaps'. Must be one of: 'cbpr+', 'cbpr_plus', 'cbprplus', 'chaps', 'fedwire', 'generic', 'hvps+', 'hvps_plus', 'hvpsplus', 'sct-inst', 'sct_inst', 'sctinst', 't2_rtgs', 't2rtgs', 'target2' (see list_schemes). One of: <code>cbpr+</code> · <code>cbpr_plus</code> · <code>cbprplus</code> · <code>chaps</code> · <code>fedwire</code> · <code>generic</code> · <code>hvps+</code> · <code>hvps_plus</code> · <code>hvpsplus</code> · <code>sct-inst</code> · <code>sct_inst</code> · <code>sctinst</code> · <code>t2_rtgs</code> · <code>t2rtgs</code> · <code>target2</code>.</td>
</tr>
<tr>
<td><code>records</code></td>
<td>array of object</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>One or more flat payment records, each a dict of field name -&gt; value; checked against the scheme's usage-guideline business rules (charge bearer, UETR, remittance length, per-message cardinality).</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="pacs008-generate_message">
<summary class="qa-q">
<span class="ref-tool-name"><code>generate_message</code></span>
<span class="ref-tool-brief">Generate a validated ISO 20022 pacs XML message from in-memory records.</span>
<span class="ref-tool-meta">2 parameters · 2 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">This is the primary generation tool: pass payment records you already hold in memory and receive an XSD-validated XML document; no file is written. Run <code>validate_records</code> first to surface record-level errors, and <code>list_message_types</code> to confirm the <code>message_type</code> string.</p>
<p class="ref-tool-desc">Returns the validated XML document as a string, or an <code>{"error": ...}</code> payload (serialized) if generation fails.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of generate_message</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>message_type</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>A supported ISO 20022 pacs message type, e.g. 'pacs.008.001.08' FI-to-FI Customer Credit Transfer. Must be exactly one of: 'pacs.002.001.12', 'pacs.003.001.09', 'pacs.004.001.11', 'pacs.007.001.11', 'pacs.008.001.01', 'pacs.008.001.02', 'pacs.008.001.03', 'pacs.008.001.04', 'pacs.008.001.05', 'pacs.008.001.06', 'pacs.008.001.07', 'pacs.008.001.08', 'pacs.008.001.09', 'pacs.008.001.10', 'pacs.008.001.11', 'pacs.008.001.12', 'pacs.008.001.13', 'pacs.009.001.10', 'pacs.010.001.05', 'pacs.028.001.05' (see list_message_types). One of: <code>pacs.002.001.12</code> · <code>pacs.003.001.09</code> · <code>pacs.004.001.11</code> · <code>pacs.007.001.11</code> · <code>pacs.008.001.01</code> · <code>pacs.008.001.02</code> · <code>pacs.008.001.03</code> · <code>pacs.008.001.04</code> · <code>pacs.008.001.05</code> · <code>pacs.008.001.06</code> · <code>pacs.008.001.07</code> · <code>pacs.008.001.08</code> · <code>pacs.008.001.09</code> · <code>pacs.008.001.10</code> · <code>pacs.008.001.11</code> · <code>pacs.008.001.12</code> · <code>pacs.008.001.13</code> · <code>pacs.009.001.10</code> · <code>pacs.010.001.05</code> · <code>pacs.028.001.05</code>.</td>
</tr>
<tr>
<td><code>records</code></td>
<td>array of object</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>One or more flat payment records, each a dict of field name -&gt; value, from which the pacs XML is generated; run validate_records first to surface record-level errors.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="pacs008-validate_xml">
<summary class="qa-q">
<span class="ref-tool-name"><code>validate_xml</code></span>
<span class="ref-tool-brief">Validate a raw XML string against a message type's bundled XSD.</span>
<span class="ref-tool-meta">2 parameters · 2 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this to check an externally produced XML document against the official ISO 20022 schema. To generate a document that is already XSD-validated, use <code>generate_message</code> instead.</p>
<p class="ref-tool-desc">Returns <code>{"message_type": str, "is_valid": bool}</code>.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of validate_xml</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>message_type</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>A supported ISO 20022 pacs message type, e.g. 'pacs.008.001.08' FI-to-FI Customer Credit Transfer. Must be exactly one of: 'pacs.002.001.12', 'pacs.003.001.09', 'pacs.004.001.11', 'pacs.007.001.11', 'pacs.008.001.01', 'pacs.008.001.02', 'pacs.008.001.03', 'pacs.008.001.04', 'pacs.008.001.05', 'pacs.008.001.06', 'pacs.008.001.07', 'pacs.008.001.08', 'pacs.008.001.09', 'pacs.008.001.10', 'pacs.008.001.11', 'pacs.008.001.12', 'pacs.008.001.13', 'pacs.009.001.10', 'pacs.010.001.05', 'pacs.028.001.05' (see list_message_types). One of: <code>pacs.002.001.12</code> · <code>pacs.003.001.09</code> · <code>pacs.004.001.11</code> · <code>pacs.007.001.11</code> · <code>pacs.008.001.01</code> · <code>pacs.008.001.02</code> · <code>pacs.008.001.03</code> · <code>pacs.008.001.04</code> · <code>pacs.008.001.05</code> · <code>pacs.008.001.06</code> · <code>pacs.008.001.07</code> · <code>pacs.008.001.08</code> · <code>pacs.008.001.09</code> · <code>pacs.008.001.10</code> · <code>pacs.008.001.11</code> · <code>pacs.008.001.12</code> · <code>pacs.008.001.13</code> · <code>pacs.009.001.10</code> · <code>pacs.010.001.05</code> · <code>pacs.028.001.05</code>.</td>
</tr>
<tr>
<td><code>xml</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>A raw ISO 20022 XML document to validate against the bundled XSD schema for the given message type.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="pacs008-parse_message">
<summary class="qa-q">
<span class="ref-tool-name"><code>parse_message</code></span>
<span class="ref-tool-brief">Parse and classify an inbound ISO 20022 XML message.</span>
<span class="ref-tool-meta">1 parameter · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this on the receiving side to identify what a message is -- its <code>msg_def_idr</code> (e.g. <code>pacs.002.001.10</code>), family, version, and any Business Application Header -- before processing it. Handles both bare <code>Document</code> messages and BAH-wrapped envelopes.</p>
<p class="ref-tool-desc">Returns a dict with <code>msg_def_idr</code>, <code>msg_family</code>, <code>version</code>, <code>root_local_name</code>, <code>namespace_uri</code>, <code>envelope_wrapped</code> and <code>bah</code>.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of parse_message</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>xml</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>A raw inbound ISO 20022 XML message (pacs.008 / pacs.002 / pacs.004, optionally BAH-envelope-wrapped) to classify.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="pacs008-convert_mt103">
<summary class="qa-q">
<span class="ref-tool-name"><code>convert_mt103</code></span>
<span class="ref-tool-brief">Convert a legacy SWIFT MT103 into pacs.008-ready flat records.</span>
<span class="ref-tool-meta">1 parameter · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">This is the SWIFT MT-to-MX migration path (correspondent-banking MT103 coexistence with ISO 20022 ends November 2025): parse an MT103 text payload and get back the flat pacs.008 record(s) that can be fed straight into <code>validate_records</code> / <code>generate_message</code>. An MT103 carries exactly one transfer, so the <code>records</code> list always holds a single record. No file is read or written.</p>
<p class="ref-tool-desc">Returns <code>{"message_type": "pacs.008.001.08", "records": [{...}]}</code> with the parsed flat record, or an <code>{"error": ...}</code> payload if the MT103 is missing a mandatory field (<code>:20:</code>, <code>:32A:</code>, beneficiary) or malformed.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of convert_mt103</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>mt103_text</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>A legacy SWIFT MT103 (single customer credit transfer) payload as text. A raw '{4:...-}' block-4 envelope, trailing whitespace and CRLF/LF differences are tolerated.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="pacs008-classify_address">
<summary class="qa-q">
<span class="ref-tool-name"><code>classify_address</code></span>
<span class="ref-tool-brief">Classify a postal address as structured, hybrid, or unstructured.</span>
<span class="ref-tool-meta">1 parameter · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this to see where an address stands against the 14 November 2026 SWIFT cliff: <code>structured</code> (town + country + structured detail, no free-form lines), <code>hybrid</code> (town + country + 1-2 free-form <code>adr_line</code> lines, the minimum CBPR+ UG2026 bar), or <code>unstructured</code> (free-form only - rejected from the cliff date). To check acceptability under a policy use <code>validate_address</code>; to upgrade legacy lines use <code>repair_address</code>.</p>
<p class="ref-tool-desc">Returns <code>{"classification": str, "is_structured": bool, "is_hybrid": bool, "is_unstructured": bool, "has_structured_fields": bool}</code> or an <code>{"error": ...}</code> payload.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of classify_address</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>address</code></td>
<td>object</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>An ISO 20022 PostalAddress27 as a dict of snake_case fields, e.g. {'strt_nm': 'High St', 'bldg_nb': '1', 'pst_cd': 'AB1 2CD', 'twn_nm': 'London', 'ctry': 'GB'} and optional 'adr_line' (list of free-form lines). 'ctry' must be ISO 3166-1 alpha-2.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="pacs008-validate_address">
<summary class="qa-q">
<span class="ref-tool-name"><code>validate_address</code></span>
<span class="ref-tool-brief">Validate one postal address against an address policy.</span>
<span class="ref-tool-meta">2 parameters · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this to decide whether an address will clear a rail. The default <code>hybrid_or_structured</code> policy is the November 14, 2026 cliff rule (SWIFT CBPR+, HVPS+, T2 RTGS, CHAPS, Fedwire, Lynx): it rejects fully unstructured addresses. Findings mirror the library's pipeline severity (a policy rejection is a blocking finding).</p>
<p class="ref-tool-desc">Returns <code>{"policy": str, "classification": str, "is_acceptable": bool, "findings": [{"severity": str, "message": str}, ...]}</code> or an <code>{"error": ...}</code> payload.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of validate_address</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>address</code></td>
<td>object</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>An ISO 20022 PostalAddress27 as a dict of snake_case fields, e.g. {'strt_nm': 'High St', 'bldg_nb': '1', 'pst_cd': 'AB1 2CD', 'twn_nm': 'London', 'ctry': 'GB'} and optional 'adr_line' (list of free-form lines). 'ctry' must be ISO 3166-1 alpha-2.</td>
</tr>
<tr>
<td><code>policy</code></td>
<td>string</td>
<td><span class="ref-req ref-req-optional">Optional</span></td>
<td>Postal-address validation policy. 'unstructured_ok' permits any form (pre-cliff / generic); 'hybrid_or_structured' rejects fully unstructured addresses (the SWIFT CBPR+ UG2026 default in force from 14 November 2026); 'structured_only' requires full structured form. Must be one of: 'unstructured_ok', 'hybrid_or_structured', 'structured_only'. One of: <code>unstructured_ok</code> · <code>hybrid_or_structured</code> · <code>structured_only</code>. Default: <code>&quot;hybrid_or_structured&quot;</code>.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="pacs008-repair_address">
<summary class="qa-q">
<span class="ref-tool-name"><code>repair_address</code></span>
<span class="ref-tool-brief">Upgrade legacy unstructured address lines toward hybrid/structured form.</span>
<span class="ref-tool-meta">2 parameters · 2 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Experimental country-aware repair (<code>GB</code>, <code>US</code>, <code>DE</code>, <code>FR</code>, <code>JP</code> have dedicated heuristics; other countries get a best-effort pass promoting the last line to a town). Use this to lift pre-cliff data over the November 14, 2026 bar; audit the output before submitting, and keep both the original and derived address in your audit trail.</p>
<p class="ref-tool-desc">Returns <code>{"address": {...}, "classification": str, "is_structured": bool, "is_hybrid": bool}</code> (so you can see the unstructured -&gt; hybrid / structured upgrade) or an <code>{"error": ...}</code> payload.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of repair_address</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>lines</code></td>
<td>array of string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>Legacy unstructured address lines (free-form). Empty or whitespace-only lines are skipped.</td>
</tr>
<tr>
<td><code>country</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>ISO 3166-1 alpha-2 country code (e.g. 'GB', 'US', 'DE', 'FR', 'JP') used to drive country-aware repair heuristics.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="pacs008-validate_addresses">
<summary class="qa-q">
<span class="ref-tool-name"><code>validate_addresses</code></span>
<span class="ref-tool-brief">Batch-validate every party address across a list of payment rows.</span>
<span class="ref-tool-meta">2 parameters · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this before <code>generate_message</code> to catch addresses that will be rejected at the rail. The default <code>hybrid_or_structured</code> policy enforces the November 14, 2026 cliff. Each finding is reported per offending <code>(row, party)</code> pair.</p>
<p class="ref-tool-desc">Returns <code>{"policy": str, "is_valid": bool, "total": int, "errors": [{"row": int, "party": str, "severity": str, "message": str, "classification": str}, ...]}</code> or an <code>{"error": ...}</code> payload.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of validate_addresses</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>addresses</code></td>
<td>array of object</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>Payment-row dicts. The pipeline scans each row for columns of the form '{party}_address_{field}' (party in debtor, creditor, debtor_agent, creditor_agent, ultimate_debtor, ultimate_creditor; field a snake_case PostalAddress field such as twn_nm/ctry/strt_nm or adr_line_0..adr_line_6) and validates each party's address.</td>
</tr>
<tr>
<td><code>policy</code></td>
<td>string</td>
<td><span class="ref-req ref-req-optional">Optional</span></td>
<td>Postal-address validation policy. 'unstructured_ok' permits any form (pre-cliff / generic); 'hybrid_or_structured' rejects fully unstructured addresses (the SWIFT CBPR+ UG2026 default in force from 14 November 2026); 'structured_only' requires full structured form. Must be one of: 'unstructured_ok', 'hybrid_or_structured', 'structured_only'. One of: <code>unstructured_ok</code> · <code>hybrid_or_structured</code> · <code>structured_only</code>. Default: <code>&quot;hybrid_or_structured&quot;</code>.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
</div>
</section>

<section class="newsroom ref-server" id="camt053">
<header class="cat-section-head">
<p class="cat-kicker">camt053-mcp · READ STATEMENTS</p>
<h2 class="cat-headline">Bank-to-customer statements.</h2>
<p class="cat-lede">camt.053/camt.052 parsing, entry queries, MT94x conversion, reversals and CBPR+ readiness.</p>
</header>
<p class="ref-capture">21 tools · v0.0.12 · captured live over MCP stdio on 2026-07-15 with <code>uvx --from &quot;camt053-mcp&quot; camt053-mcp</code></p>
<div class="qa-list ref-tools">
<details class="qa-item ref-tool" id="camt053-list_message_types">
<summary class="qa-q">
<span class="ref-tool-name"><code>list_message_types</code></span>
<span class="ref-tool-brief">List every supported ISO 20022 camt.05x message type and its name.</span>
<span class="ref-tool-meta">No parameters</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this first, before any validation or generation call, to discover the exact <code>message_type</code> strings this server accepts. For the return-reason codes rather than message types, call <code>list_return_reasons</code> instead.</p>
<p class="ref-tool-desc">Returns a list of <code>{"message_type": ..., "name": ...}</code> dictionaries, one per supported message type (e.g. <code>camt.053.001.14</code>).</p>
<p class="ref-noparams">This tool takes no parameters.</p>
</div>
</details>
<details class="qa-item ref-tool" id="camt053-list_return_reasons">
<summary class="qa-q">
<span class="ref-tool-name"><code>list_return_reasons</code></span>
<span class="ref-tool-brief">List every known ISO external return reason code with its name.</span>
<span class="ref-tool-meta">No parameters</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this to discover the <code>reason_code</code> values that <code>filter_entries</code> and <code>generate_reversal</code> accept (e.g. <code>AC04</code> Closed Account). For the supported message types rather than reason codes, use <code>list_message_types</code>.</p>
<p class="ref-tool-desc">Returns a list of <code>{"code": ..., "name": ...}</code> dictionaries (e.g. <code>{"code": "AC04", "name": "Closed Account Number"}</code>).</p>
<p class="ref-noparams">This tool takes no parameters.</p>
</div>
</details>
<details class="qa-item ref-tool" id="camt053-get_required_fields">
<summary class="qa-q">
<span class="ref-tool-name"><code>get_required_fields</code></span>
<span class="ref-tool-brief">List only the required input field names for a camt message type.</span>
<span class="ref-tool-meta">1 parameter · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this for a quick checklist of the mandatory columns before building reversing-entry records. When you need full type/format constraints (not just which fields are required), call <code>get_input_schema</code> instead.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of get_required_fields</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>message_type</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>A supported ISO 20022 camt.05x message type string. Must be exactly one of: 'camt.052.001.14', 'camt.053.001.14', 'camt.054.001.14' (see list_message_types). One of: <code>camt.052.001.14</code> · <code>camt.053.001.14</code> · <code>camt.054.001.14</code>.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="camt053-get_input_schema">
<summary class="qa-q">
<span class="ref-tool-name"><code>get_input_schema</code></span>
<span class="ref-tool-brief">Return the full JSON Schema for a message type's flat input record.</span>
<span class="ref-tool-meta">1 parameter · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this to learn every field, its type, and its constraints before assembling records, or to drive a form/UI. For just the required-field names use <code>get_required_fields</code>; to actually check records against this schema use <code>validate_records</code>.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of get_input_schema</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>message_type</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>A supported ISO 20022 camt.05x message type string. Must be exactly one of: 'camt.052.001.14', 'camt.053.001.14', 'camt.054.001.14' (see list_message_types). One of: <code>camt.052.001.14</code> · <code>camt.053.001.14</code> · <code>camt.054.001.14</code>.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="camt053-validate_records">
<summary class="qa-q">
<span class="ref-tool-name"><code>validate_records</code></span>
<span class="ref-tool-brief">Validate flat records against a message type's input JSON Schema.</span>
<span class="ref-tool-meta">2 parameters · 2 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this on in-memory reversing-entry records to catch structural/type errors per row before generation. To validate a whole camt.05x <em>document</em> (XML) against its XSD instead, use <code>validate_statement</code>.</p>
<p class="ref-tool-desc">Returns a report <code>{"valid": bool, "total": int, "valid_count": int, "errors": [...]}</code>.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of validate_records</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>message_type</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>A supported ISO 20022 camt.05x message type string. Must be exactly one of: 'camt.052.001.14', 'camt.053.001.14', 'camt.054.001.14' (see list_message_types). One of: <code>camt.052.001.14</code> · <code>camt.053.001.14</code> · <code>camt.054.001.14</code>.</td>
</tr>
<tr>
<td><code>records</code></td>
<td>array of object</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>One or more flat reversing-entry records (each a dict of field name to value) to validate row-by-row against the message type's input JSON Schema.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="camt053-validate_identifier">
<summary class="qa-q">
<span class="ref-tool-name"><code>validate_identifier</code></span>
<span class="ref-tool-brief">Validate a single financial identifier (IBAN, BIC, or LEI).</span>
<span class="ref-tool-meta">2 parameters · 2 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this for a one-off identifier check with a clear pass/fail. To validate identifiers embedded across a whole batch of records, prefer <code>validate_records</code> rather than calling this per field.</p>
<p class="ref-tool-desc">Returns <code>{"kind": str, "value": str, "valid": bool}</code>.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of validate_identifier</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>kind</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>The financial identifier type to validate (case-insensitive). Must be exactly one of: 'bic', 'iban', 'lei'. One of: <code>bic</code> · <code>iban</code> · <code>lei</code>.</td>
</tr>
<tr>
<td><code>value</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>The identifier value to check, matching the chosen kind (e.g. an IBAN, an 8- or 11-character BIC, or a 20-character LEI). Whitespace/case handling follows the underlying validator.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="camt053-parse_statement">
<summary class="qa-q">
<span class="ref-tool-name"><code>parse_statement</code></span>
<span class="ref-tool-brief">Parse an incoming camt.05x statement XML string into structured data.</span>
<span class="ref-tool-meta">1 parameter · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this to turn a raw statement into a navigable dict (header, statements, accounts, balances, entries). To pull just the flat entry list use <code>list_entries</code>; to only check the document is schema-valid use <code>validate_statement</code>.</p>
<p class="ref-tool-desc">Returns the parsed document as a JSON-serialisable dict (group header plus statements, each with its account, balances, and entries), or an <code>{"error": ...}</code> payload if the XML cannot be parsed.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of parse_statement</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>xml</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>The raw camt.05x statement XML document as a string, with its root camt &lt;Document&gt; element. Returned verbatim from the bank; no file path is accepted.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="camt053-convert_mt940_to_camt053">
<summary class="qa-q">
<span class="ref-tool-name"><code>convert_mt940_to_camt053</code></span>
<span class="ref-tool-brief">Convert a legacy SWIFT MT940 statement into a camt.053 structure.</span>
<span class="ref-tool-meta">1 parameter · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this as the Phase-1 migration wedge: SWIFT MT940 customer statements retire in **November 2028**, so this tool bridges the gap by turning raw MT940 text into the same JSON-serialisable camt.053 document shape that <code>parse_statement</code> returns (group header plus statements, each with its account, balances, and entries). Downstream tools (<code>list_entries</code>, <code>filter_entries</code>, <code>classify_entry</code>, <code>export_journal</code>) then work on the result unchanged.</p>
<p class="ref-tool-desc">Wraps the <code>camt053-loader-mt940</code> library's <code>parse_mt940</code>; the MT parsing itself is delegated (no MT grammar is reimplemented here). The resulting <code>ParsedDocument</code> is serialised with the same <code>to_dict()</code> the server's other parse tools use, so agents get a consistent structure. Nothing is read from or written to disk.</p>
<p class="ref-tool-desc">Returns the converted document as a JSON-serialisable dict, or an <code>{"error": ...}</code> payload if the MT940 text cannot be parsed (e.g. a missing <code>:20:</code> reference or a malformed balance / statement line).</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of convert_mt940_to_camt053</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>mt940_text</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>The raw legacy SWIFT MT940 statement text as a string (<code>:20:</code> / <code>:25:</code> / <code>:28C:</code> / <code>:60F:</code> / <code>:61:</code> / <code>:86:</code> / <code>:62F:</code> fields). Passed verbatim from the bank or ERP; no file path is accepted.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="camt053-convert_mt942">
<summary class="qa-q">
<span class="ref-tool-name"><code>convert_mt942</code></span>
<span class="ref-tool-brief">Convert a legacy SWIFT MT942 interim report into a camt.052 structure.</span>
<span class="ref-tool-meta">1 parameter · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this as the Phase-1 migration wedge for intraday reporting: SWIFT MT94x messages retire in **November 2028**, so this tool bridges the gap by turning raw MT942 <em>Interim Transaction Report</em> text into the same JSON-serialisable camt.052 (Bank-to-Customer Account **Report**) document shape the server's parse tools return (group header plus statements, each with its account, balances, and entries). MT942 is the intraday sibling of MT940: where MT940 maps to camt.053 (end-of-day statement), MT942 maps to camt.052, so the resulting <code>message_type</code> is <code>camt.052.001.08</code>. Downstream tools (<code>list_entries</code>, <code>filter_entries</code>, <code>classify_entry</code>, <code>export_journal</code>) then work on the result unchanged.</p>
<p class="ref-tool-desc">Wraps the <code>camt053-loader-mt942</code> library's <code>parse_mt942</code>; the MT parsing itself is delegated (no MT grammar is reimplemented here). The resulting <code>ParsedDocument</code> is serialised with the same <code>to_dict()</code> the server's other parse tools use, so agents get a consistent structure. Nothing is read from or written to disk.</p>
<p class="ref-tool-desc">**Documented model limitation.** The <code>camt053</code> typed model is camt.053-statement-oriented: it has no dedicated field for camt.052's floor-limit (<code>&lt;Lmt&gt;</code>) or transaction-summary (<code>&lt;TxsSummry&gt;</code>) blocks. Rather than drop that data, the loader surfaces it on the balance list using clearly proprietary <code>type_code</code> values so consumers can recognise and filter them: <code>:34F:</code> floor limits become <code>FLIMD</code> / <code>FLIMC</code> balances, and <code>:90D:</code> / <code>:90C:</code> entry-count summaries become <code>SUMD:&lt;count&gt;</code> / <code>SUMC:&lt;count&gt;</code> balances (the ISO <code>NbOfNtries</code> count is encoded after the colon; the sum is the balance <code>amount</code>). See the loader's README.</p>
<p class="ref-tool-desc">Returns the converted document as a JSON-serialisable dict, or an <code>{"error": ...}</code> payload if the MT942 text cannot be parsed (e.g. a missing <code>:20:</code> reference or a malformed floor-limit / summary / statement line).</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of convert_mt942</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>mt942_text</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>The raw legacy SWIFT MT942 interim transaction report text as a string (<code>:20:</code> / <code>:25:</code> / <code>:28C:</code> / <code>:34F:</code> / <code>:13D:</code> / <code>:61:</code> / <code>:86:</code> / <code>:90D:</code> / <code>:90C:</code> fields). Passed verbatim from the bank or ERP; no file path is accepted.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="camt053-validate_statement">
<summary class="qa-q">
<span class="ref-tool-name"><code>validate_statement</code></span>
<span class="ref-tool-brief">Validate an incoming camt.05x statement XML against its XSD schema.</span>
<span class="ref-tool-meta">1 parameter · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this to confirm a document is well-formed and schema-valid before processing it. This checks XSD conformance only; for the Nov 2026 CBPR+ business rules use <code>check_cbpr_readiness</code>, and to extract the data use <code>parse_statement</code>.</p>
<p class="ref-tool-desc">Detects the document's message type, validates it against the matching ISO 20022 schema, and returns a report <code>{"valid": bool, "message_type": str, "errors": [...]}</code>. A well-formed but schema-invalid document yields <code>valid=False</code> with a populated <code>errors</code> list (and the detected <code>message_type</code>); a valid one yields <code>valid=True</code> with no errors.</p>
<p class="ref-tool-desc">Returns an <code>{"error": ...}</code> payload instead if the XML cannot be parsed (e.g. it is malformed or is not a camt <code>Document</code>).</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of validate_statement</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>xml</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>The raw camt.05x statement XML document as a string, with its root camt &lt;Document&gt; element. Validated against the matching ISO 20022 XSD; no file path is accepted.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="camt053-check_cbpr_readiness">
<summary class="qa-q">
<span class="ref-tool-name"><code>check_cbpr_readiness</code></span>
<span class="ref-tool-brief">Check a camt.053 statement against the CBPR+ Nov 2026 acceptance rules.</span>
<span class="ref-tool-meta">1 parameter · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this to audit a statement for the business-rule changes (schema version, structured postal addresses) enforced from the Nov 2026 cutover. For plain XSD schema validity use <code>validate_statement</code> instead; for just the cutover date use <code>get_cbpr_cutover_date</code>.</p>
<p class="ref-tool-desc">A coordinated CBPR+ / Fedwire / CHAPS / T2 cutover lands on **14-16 November 2026**: unstructured-only postal addresses get rejected, <code>camt.110/111</code> exceptions and investigations become mandatory, and T2S R2026.NOV upgrades camt.053 / 054 to schema revision MR2026.</p>
<p class="ref-tool-desc">This tool walks the supplied payload and reports every issue that will fail the Nov 2026 acceptance rules:</p>
<p class="ref-tool-desc">* **Schema version** vs the CBPR+ current set (<code>camt.053.001.08</code> / <code>camt.053.001.13</code>); <code>.02</code>-<code>.07</code> are flagged as deprecated warnings; unknown / non-camt.053 namespaces as errors. * **Postal addresses**: every <code>&lt;PstlAdr&gt;</code> is classified as fully structured, hybrid, or **unstructured-only** (<code>&lt;AdrLine&gt;</code> without <code>&lt;TwnNm&gt;</code> + <code>&lt;Ctry&gt;</code> siblings, the Nov 2026 reject case).</p>
<p class="ref-tool-desc">Returns a dictionary <code>{"cbpr_ready": bool, "schema_version": str | None, "checked_at": ISO-8601 UTC, "cutover_date": "2026-11-16", "issues": [...], "summary": {...}}</code>. <code>cbpr_ready</code> is <code>True</code> iff no <code>severity="error"</code> issue was raised. An <code>{"error": ...}</code> envelope is returned instead if the XML is malformed or refused by the hardened pre-flight (DOCTYPE / ENTITY / oversized payload).</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of check_cbpr_readiness</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>xml</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>The raw camt.05x statement XML document as a string, audited against the CBPR+ Nov 2026 acceptance rules (schema version and structured postal addresses). Rejected by the hardened pre-flight if it carries a DOCTYPE/ENTITY or is oversized.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="camt053-get_cbpr_cutover_date">
<summary class="qa-q">
<span class="ref-tool-name"><code>get_cbpr_cutover_date</code></span>
<span class="ref-tool-brief">Return the official CBPR+ / Nov 2026 cutover date as ISO 8601.</span>
<span class="ref-tool-meta">No parameters</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this to quote the enforcement date directly, without parsing a document. To actually audit a statement against the rules that take effect on that date, call <code>check_cbpr_readiness</code> instead.</p>
<p class="ref-tool-desc">The cutover (<code>2026-11-16</code>) is the date after which the rules checked by <code>check_cbpr_readiness</code> are enforced by the major clearing systems; payments that fail will be rejected at receive-time. Surfaced as a discrete tool so agents can quote it directly without having to call a readiness check first.</p>
<p class="ref-noparams">This tool takes no parameters.</p>
</div>
</details>
<details class="qa-item ref-tool" id="camt053-cite_rulebook">
<summary class="qa-q">
<span class="ref-tool-name"><code>cite_rulebook</code></span>
<span class="ref-tool-brief">Return a curated payments-rulebook citation for a single clause.</span>
<span class="ref-tool-meta">3 parameters · 3 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this to quote one specific rule (with its canonical source URL) once you know the <code>scheme</code>/<code>version</code>/<code>clause</code>. To discover which clauses exist first, call <code>list_rulebook_clauses</code>.</p>
<p class="ref-tool-desc">Looks up one well-known rule across the SEPA, CBPR+, and HVPS+ rulebooks and returns a short summary together with the canonical source URL so an agent can quote the rule and the operator can verify it against the official document.</p>
<p class="ref-tool-desc">The registry is a curated convenience layer, not a verbatim reproduction of copyrighted text. Always defer to <code>source_url</code> for authoritative wording before relying on a citation for compliance or contractual decisions; the returned <code>disclaimer</code> field repeats this for the calling agent.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of cite_rulebook</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>scheme</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>The payments-rulebook scheme to cite (case-sensitive). Must be exactly one of: 'CBPR+', 'HVPS+', 'SEPA' (see list_rulebook_clauses). One of: <code>CBPR+</code> · <code>HVPS+</code> · <code>SEPA</code>.</td>
</tr>
<tr>
<td><code>version</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>The rulebook version, e.g. '2025' or '2026'. Use list_rulebook_clauses to see which versions exist per scheme.</td>
</tr>
<tr>
<td><code>clause</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>A kebab-case clause identifier (e.g. 'iban-only') as returned by list_rulebook_clauses for the chosen scheme and version.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="camt053-list_rulebook_clauses">
<summary class="qa-q">
<span class="ref-tool-name"><code>list_rulebook_clauses</code></span>
<span class="ref-tool-brief">List the curated rulebook clauses the server can cite, optionally filtered.</span>
<span class="ref-tool-meta">2 parameters · 0 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this to browse the citation registry and pick a <code>clause</code> id; then pass that id to <code>cite_rulebook</code> to fetch the full summary and source URL.</p>
<p class="ref-tool-desc">Returns the full registry, optionally filtered by <code>scheme</code> and / or <code>version</code>. Use the resulting <code>clause</code> values as input to <code>cite_rulebook</code>.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of list_rulebook_clauses</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>scheme</code></td>
<td>string, nullable</td>
<td><span class="ref-req ref-req-optional">Optional</span></td>
<td>Restrict the listing to one scheme. When given, must be exactly one of: 'CBPR+', 'HVPS+', 'SEPA'. None (the default) returns clauses for all schemes. One of: <code>CBPR+</code> · <code>HVPS+</code> · <code>SEPA</code>.</td>
</tr>
<tr>
<td><code>version</code></td>
<td>string, nullable</td>
<td><span class="ref-req ref-req-optional">Optional</span></td>
<td>Restrict the listing to one rulebook version, e.g. '2026'. None (the default) returns clauses for all versions.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="camt053-export_journal">
<summary class="qa-q">
<span class="ref-tool-name"><code>export_journal</code></span>
<span class="ref-tool-brief">Export a camt.053 statement as accounting-platform journal-entry payloads.</span>
<span class="ref-tool-meta">2 parameters · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this to reshape a statement's booked entries into ready-to-POST Xero or QuickBooks payloads (the tool builds the payloads only; it does not call any external API or write files). To discover the valid <code>target</code> values first, call <code>list_export_journal_targets</code>.</p>
<p class="ref-tool-desc">Parses the supplied statement and re-shapes every booked entry into a target-specific journal-entry payload ready for direct POST to the accounting platform's REST API.</p>
<p class="ref-tool-desc">Supported targets (see <code>camt053_mcp.export_journal.SUPPORTED_TARGETS</code>):</p>
<p class="ref-tool-desc"><em> <code>"xero"</code> - returns a list of Xero <code>BankTransactions</code> payloads. Each entry maps to <code>{Type, Reference, Date, BankAccount, Contact, LineAmountTypes, CurrencyCode, LineItems}</code>; CRDT entries become <code>Type=RECEIVE</code> and DBIT entries <code>Type=SPEND</code>. </em> <code>"qbo"</code> - returns a list of QuickBooks Online <code>JournalEntry</code> payloads. Each entry produces a balanced two-line journal (one to the bank account, one to a clearing account; sign flipped on debit entries).</p>
<p class="ref-tool-desc">Operator-specific values (account codes, contact identifiers, realm IDs) appear as <code>"OPERATOR_FILL"</code> placeholders so the operator knows exactly what still needs wiring. The response's <code>placeholder_count</code> field reports the total.</p>
<p class="ref-tool-desc">NetSuite + SAP S/4HANA targets are tracked as a follow-up in #17.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of export_journal</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>xml</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>The raw camt.053 statement XML document as a string; its booked entries are reshaped into journal-entry payloads.</td>
</tr>
<tr>
<td><code>target</code></td>
<td>string</td>
<td><span class="ref-req ref-req-optional">Optional</span></td>
<td>The accounting platform to shape journal-entry payloads for. Must be exactly one of: 'qbo', 'xero' (see list_export_journal_targets). One of: <code>qbo</code> · <code>xero</code>. Default: <code>&quot;xero&quot;</code>.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="camt053-list_export_journal_targets">
<summary class="qa-q">
<span class="ref-tool-name"><code>list_export_journal_targets</code></span>
<span class="ref-tool-brief">List the accounting-platform targets the <code>export_journal</code> tool supports.</span>
<span class="ref-tool-meta">No parameters</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this to tell a user which <code>target</code> values <code>export_journal</code> accepts before invoking it. This lists export destinations only; for the LLM classifier's category vocabulary use <code>list_classify_entry_categories</code>.</p>
<p class="ref-tool-desc">Returns the sorted list of valid <code>target</code> arguments accepted by <code>export_journal</code> (<code>["qbo", "xero"]</code> today). NetSuite and SAP S/4HANA support is a tracked follow-up.</p>
<p class="ref-noparams">This tool takes no parameters.</p>
</div>
</details>
<details class="qa-item ref-tool" id="camt053-classify_entry">
<summary class="qa-q">
<span class="ref-tool-name"><code>classify_entry</code></span>
<span class="ref-tool-brief">Classify one statement entry into a category via MCP LLM Sampling.</span>
<span class="ref-tool-meta">2 parameters · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this when you want a semantic, model-driven label for an entry (payroll, fee, refund, …) rather than a deterministic rule match. Because it delegates an LLM completion to the client it is open-world and non-idempotent; for the fixed candidate categories it chooses from, call <code>list_classify_entry_categories</code> first.</p>
<p class="ref-tool-desc">Uses the **MCP Sampling** protocol primitive: the server (this process) asks the <em>client</em> (the agent's host application) to perform an LLM completion on the server's behalf, then receives the model's structured response. Keeps every LLM call in the operator's existing model contract (privacy, billing, audit).</p>
<p class="ref-tool-desc">The model is asked to choose exactly one category from <code>categories</code> (or <code>camt053_mcp.classify.DEFAULT_CATEGORIES</code> if <code>None</code> is passed) and return a structured <code>{category, confidence, explanation}</code> payload.</p>
<p class="ref-tool-desc">Clients that do not support Sampling will get an <code>{"error": "..."}</code> envelope and can fall back to a rules-only classifier.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of classify_entry</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>entry</code></td>
<td>object</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>A single statement entry dict, in the shape returned by parse_statement / list_entries, to classify into one category.</td>
</tr>
<tr>
<td><code>categories</code></td>
<td>array of string, nullable</td>
<td><span class="ref-req ref-req-optional">Optional</span></td>
<td>The candidate categories the model must choose exactly one from. None (the default) uses the built-in default list exposed by list_classify_entry_categories.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="camt053-list_classify_entry_categories">
<summary class="qa-q">
<span class="ref-tool-name"><code>list_classify_entry_categories</code></span>
<span class="ref-tool-brief">List the default candidate categories the <code>classify_entry</code> tool uses.</span>
<span class="ref-tool-meta">No parameters</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this to quote the built-in category vocabulary to a user before running the LLM classifier. This is a static list lookup (no model call); to actually classify an entry, call <code>classify_entry</code>.</p>
<p class="ref-tool-desc">Operators can override the list per call; this tool exposes the default the prompt template ships with so an agent can quote them to the user before invoking the classifier.</p>
<p class="ref-noparams">This tool takes no parameters.</p>
</div>
</details>
<details class="qa-item ref-tool" id="camt053-list_entries">
<summary class="qa-q">
<span class="ref-tool-name"><code>list_entries</code></span>
<span class="ref-tool-brief">List every booked entry across all statements in a camt.05x document.</span>
<span class="ref-tool-meta">3 parameters · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this to get the flat, paginable entry list from a statement. To keep only the entries carrying a given return-reason code use <code>filter_entries</code>; for the full nested document structure use <code>parse_statement</code>.</p>
<p class="ref-tool-desc">When <code>limit</code> is <code>None</code> (the default) the full list of entries is returned. When <code>limit</code> is given, a paginated envelope <code>{"total", "offset", "limit", "entries"}</code> is returned instead, exposing the <code>offset:offset + limit</code> slice. A negative <code>offset</code> or <code>limit</code> yields an <code>{"error": ...}</code> payload.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of list_entries</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>xml</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>The raw camt.05x statement XML document as a string; every booked entry across all its statements is returned.</td>
</tr>
<tr>
<td><code>offset</code></td>
<td>integer</td>
<td><span class="ref-req ref-req-optional">Optional</span></td>
<td>Zero-based index of the first entry to return. Applies only when limit is given; must be non-negative. Defaults to 0. Default: <code>0</code>.</td>
</tr>
<tr>
<td><code>limit</code></td>
<td>integer, nullable</td>
<td><span class="ref-req ref-req-optional">Optional</span></td>
<td>Maximum number of entries to return, starting at offset. None (the default) returns the full unpaginated list; a non-None value returns a {total, offset, limit, entries} envelope. Must be non-negative.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="camt053-filter_entries">
<summary class="qa-q">
<span class="ref-tool-name"><code>filter_entries</code></span>
<span class="ref-tool-brief">List only the statement entries carrying a given return reason code.</span>
<span class="ref-tool-meta">4 parameters · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this to preview exactly which entries a reversal would touch before calling <code>generate_reversal</code> with the same <code>reason_code</code>. For every entry regardless of reason code use <code>list_entries</code> instead.</p>
<p class="ref-tool-desc">When <code>limit</code> is <code>None</code> (the default) the full list of matching entries is returned, preserving the behaviour expected by existing callers. When <code>limit</code> is given, a paginated envelope <code>{"total", "offset", "limit", "entries"}</code> is returned instead, exposing the <code>offset:offset + limit</code> slice. A negative <code>offset</code> or <code>limit</code> yields an <code>{"error": ...}</code> payload.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of filter_entries</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>xml</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>The raw camt.05x statement XML document as a string; only its entries carrying the given return reason code are returned.</td>
</tr>
<tr>
<td><code>reason_code</code></td>
<td>string</td>
<td><span class="ref-req ref-req-optional">Optional</span></td>
<td>An ISO external return reason code, e.g. 'AC04' Closed Account. Must be exactly one of: 'AC01', 'AC02', 'AC03', 'AC04', 'AC06', 'AC13', 'AC14', 'AG01', 'AG02', 'AM01', 'AM02', 'AM03', 'AM04', 'AM05', 'AM06', 'AM07', 'AM08', 'AM09', 'BE01', 'BE05', 'CNOR', 'DNOR', 'DT01', 'ED01', 'ED05', 'FF01', 'MD01', 'MD06', 'MD07', 'MS02', 'MS03', 'NARR', 'NOAS', 'NOOR', 'RC01', 'RR01', 'RR02', 'RR03', 'RR04', 'SL01', 'TM01' (see list_return_reasons). One of: <code>AC01</code> · <code>AC02</code> · <code>AC03</code> · <code>AC04</code> · <code>AC06</code> · <code>AC13</code> · <code>AC14</code> · <code>AG01</code> · <code>AG02</code> · <code>AM01</code> · <code>AM02</code> · <code>AM03</code> · <code>AM04</code> · <code>AM05</code> · <code>AM06</code> · <code>AM07</code> · <code>AM08</code> · <code>AM09</code> · <code>BE01</code> · <code>BE05</code> · <code>CNOR</code> · <code>DNOR</code> · <code>DT01</code> · <code>ED01</code> · <code>ED05</code> · <code>FF01</code> · <code>MD01</code> · <code>MD06</code> · <code>MD07</code> · <code>MS02</code> · <code>MS03</code> · <code>NARR</code> · <code>NOAS</code> · <code>NOOR</code> · <code>RC01</code> · <code>RR01</code> · <code>RR02</code> · <code>RR03</code> · <code>RR04</code> · <code>SL01</code> · <code>TM01</code>. Default: <code>&quot;AC04&quot;</code>.</td>
</tr>
<tr>
<td><code>offset</code></td>
<td>integer</td>
<td><span class="ref-req ref-req-optional">Optional</span></td>
<td>Zero-based index of the first matching entry to return. Applies only when limit is given; must be non-negative. Defaults to 0. Default: <code>0</code>.</td>
</tr>
<tr>
<td><code>limit</code></td>
<td>integer, nullable</td>
<td><span class="ref-req ref-req-optional">Optional</span></td>
<td>Maximum number of matching entries to return, starting at offset. None (the default) returns the full unpaginated list; a non-None value returns a {total, offset, limit, entries} envelope. Must be non-negative.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="camt053-generate_reversal">
<summary class="qa-q">
<span class="ref-tool-name"><code>generate_reversal</code></span>
<span class="ref-tool-brief">Generate a validated camt.053.001.14 reversal document from a statement.</span>
<span class="ref-tool-meta">2 parameters · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">This is the headline one-shot workflow: pass an incoming statement and a return-reason code and get back the reversal XML (nothing is written to disk). Preview which entries will be reversed first with <code>filter_entries</code> using the same <code>reason_code</code>.</p>
<p class="ref-tool-desc">This is the headline one-shot workflow: parse the incoming camt.053, pick the entries with the requested return reason (e.g. AC04 Closed Account), and emit a validated camt.053.001.14 reversal statement.</p>
<p class="ref-tool-desc">Returns the validated XML document as a string, or an <code>{"error": ...}</code> payload (serialized) if generation fails.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of generate_reversal</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>xml</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>The raw incoming camt.053 statement XML document as a string; the entries carrying reason_code are reversed into a new camt.053.001.14 document.</td>
</tr>
<tr>
<td><code>reason_code</code></td>
<td>string</td>
<td><span class="ref-req ref-req-optional">Optional</span></td>
<td>An ISO external return reason code, e.g. 'AC04' Closed Account. Must be exactly one of: 'AC01', 'AC02', 'AC03', 'AC04', 'AC06', 'AC13', 'AC14', 'AG01', 'AG02', 'AM01', 'AM02', 'AM03', 'AM04', 'AM05', 'AM06', 'AM07', 'AM08', 'AM09', 'BE01', 'BE05', 'CNOR', 'DNOR', 'DT01', 'ED01', 'ED05', 'FF01', 'MD01', 'MD06', 'MD07', 'MS02', 'MS03', 'NARR', 'NOAS', 'NOOR', 'RC01', 'RR01', 'RR02', 'RR03', 'RR04', 'SL01', 'TM01' (see list_return_reasons). One of: <code>AC01</code> · <code>AC02</code> · <code>AC03</code> · <code>AC04</code> · <code>AC06</code> · <code>AC13</code> · <code>AC14</code> · <code>AG01</code> · <code>AG02</code> · <code>AM01</code> · <code>AM02</code> · <code>AM03</code> · <code>AM04</code> · <code>AM05</code> · <code>AM06</code> · <code>AM07</code> · <code>AM08</code> · <code>AM09</code> · <code>BE01</code> · <code>BE05</code> · <code>CNOR</code> · <code>DNOR</code> · <code>DT01</code> · <code>ED01</code> · <code>ED05</code> · <code>FF01</code> · <code>MD01</code> · <code>MD06</code> · <code>MD07</code> · <code>MS02</code> · <code>MS03</code> · <code>NARR</code> · <code>NOAS</code> · <code>NOOR</code> · <code>RC01</code> · <code>RR01</code> · <code>RR02</code> · <code>RR03</code> · <code>RR04</code> · <code>SL01</code> · <code>TM01</code>. Default: <code>&quot;AC04&quot;</code>.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
</div>
</section>

<section class="newsroom ref-server" id="reconcile">
<header class="cat-section-head">
<p class="cat-kicker">reconcile-mcp · RECONCILE</p>
<h2 class="cat-headline">Statements against expected payments.</h2>
<p class="cat-lede">Explainable matching of observed statement entries against expected payments, with a zero-data sandbox.</p>
</header>
<p class="ref-capture">7 tools · v0.0.1 · captured live over MCP stdio on 2026-07-15 with <code>uvx --from &quot;reconcile-mcp&quot; reconcile-mcp</code></p>
<div class="qa-list ref-tools">
<details class="qa-item ref-tool" id="reconcile-reconcile">
<summary class="qa-q">
<span class="ref-tool-name"><code>reconcile</code></span>
<span class="ref-tool-brief">Reconcile expected payments against observed bank-statement entries, returning exact matches, short/over payments, split settlements (one-to-many), batch credits (many-to-one) and unmatched residuals, each with an explainable score and reasons.</span>
<span class="ref-tool-meta">3 parameters · 2 required</span>
</summary>
<div class="qa-a ref-tool-body">
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of reconcile</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>expected</code></td>
<td>array of object</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>List of canonical records. Each is an object with 'id' (string) and 'amount' (number) required, plus optional 'currency' (ISO 4217), 'date' (ISO-8601), 'counterparty' (name), 'reference' (remittance/end-to-end id).</td>
</tr>
<tr>
<td><code>observed</code></td>
<td>array of object</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>List of canonical records. Each is an object with 'id' (string) and 'amount' (number) required, plus optional 'currency' (ISO 4217), 'date' (ISO-8601), 'counterparty' (name), 'reference' (remittance/end-to-end id).</td>
</tr>
<tr>
<td><code>options</code></td>
<td>object, nullable</td>
<td><span class="ref-req ref-req-optional">Optional</span></td>
<td>Optional tuning object: 'abs_tol'/'rel_tol' (amount tolerance), 'date_window_days', 'high_threshold', 'review_threshold', 'currency_strict', 'enable_one_to_many', 'max_combination'.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="reconcile-explain_match">
<summary class="qa-q">
<span class="ref-tool-name"><code>explain_match</code></span>
<span class="ref-tool-brief">Score a single expected/observed pair and break down every signal (reference, amount, date, name). A tuning aid -- it explains the score even for pairs below the review threshold.</span>
<span class="ref-tool-meta">3 parameters · 2 required</span>
</summary>
<div class="qa-a ref-tool-body">
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of explain_match</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>expected</code></td>
<td>object</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>One expected record.</td>
</tr>
<tr>
<td><code>observed</code></td>
<td>object</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>One observed record.</td>
</tr>
<tr>
<td><code>options</code></td>
<td>object, nullable</td>
<td><span class="ref-req ref-req-optional">Optional</span></td>
<td>Optional tuning object: 'abs_tol'/'rel_tol' (amount tolerance), 'date_window_days', 'high_threshold', 'review_threshold', 'currency_strict', 'enable_one_to_many', 'max_combination'.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="reconcile-normalize_pain001">
<summary class="qa-q">
<span class="ref-tool-name"><code>normalize_pain001</code></span>
<span class="ref-tool-brief">Convert parsed pain.001 payment instructions into canonical expected records ready to reconcile. Accepts a list of transactions or a dict wrapping them under 'transactions'/'payments'/'records'.</span>
<span class="ref-tool-meta">1 parameter · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of normalize_pain001</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>document</code></td>
<td>any</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>Parsed pain.001 document or transaction list.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="reconcile-normalize_camt053">
<summary class="qa-q">
<span class="ref-tool-name"><code>normalize_camt053</code></span>
<span class="ref-tool-brief">Convert parsed camt.053 statement entries into canonical observed records ready to reconcile. Accepts a list of entries or a dict wrapping them under 'entries'/'transactions'/'statements'.</span>
<span class="ref-tool-meta">1 parameter · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of normalize_camt053</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>document</code></td>
<td>any</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>Parsed camt.053 document or entry list.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="reconcile-list_sandbox_scenarios">
<summary class="qa-q">
<span class="ref-tool-name"><code>list_sandbox_scenarios</code></span>
<span class="ref-tool-brief">List the built-in sandbox scenarios (test-mode fixtures). Each demonstrates one reconciliation outcome so you can try the flow with zero real data.</span>
<span class="ref-tool-meta">No parameters</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-noparams">This tool takes no parameters.</p>
</div>
</details>
<details class="qa-item ref-tool" id="reconcile-load_sandbox_scenario">
<summary class="qa-q">
<span class="ref-tool-name"><code>load_sandbox_scenario</code></span>
<span class="ref-tool-brief">Return the expected/observed inputs for one named sandbox scenario, so you can inspect or edit the fixture before reconciling.</span>
<span class="ref-tool-meta">1 parameter · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of load_sandbox_scenario</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>name</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>Scenario name, e.g. 'clean_match'.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="reconcile-run_sandbox_scenario">
<summary class="qa-q">
<span class="ref-tool-name"><code>run_sandbox_scenario</code></span>
<span class="ref-tool-brief">Load a named sandbox scenario and immediately reconcile it -- the one-call way to see a full, explainable result with zero setup. Great for a first run or a smoke test.</span>
<span class="ref-tool-meta">2 parameters · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of run_sandbox_scenario</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>name</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>Scenario name, e.g. 'month_end'.</td>
</tr>
<tr>
<td><code>options</code></td>
<td>object, nullable</td>
<td><span class="ref-req ref-req-optional">Optional</span></td>
<td>Optional tuning object: 'abs_tol'/'rel_tol' (amount tolerance), 'date_window_days', 'high_threshold', 'review_threshold', 'currency_strict', 'enable_one_to_many', 'max_combination'.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
</div>
</section>

<section class="newsroom ref-server" id="camt-exceptions">
<header class="cat-section-head">
<p class="cat-kicker">camt-exceptions · RESOLVE</p>
<h2 class="cat-headline">Cancellation &amp; investigation.</h2>
<p class="cat-lede">camt.056 payment cancellation and camt.029 resolution of investigation, XSD-checked.</p>
</header>
<p class="ref-capture">4 tools · v0.0.2 · captured live over MCP stdio on 2026-07-15 with <code>uvx --from &quot;camt-exceptions&quot; camt-exceptions-mcp</code></p>
<div class="qa-list ref-tools">
<details class="qa-item ref-tool" id="camt-exceptions-list_message_types">
<summary class="qa-q">
<span class="ref-tool-name"><code>list_message_types</code></span>
<span class="ref-tool-brief">List the supported ISO 20022 Exceptions &amp; Investigations message types (e.g. camt.056 payment cancellation request) and their names.</span>
<span class="ref-tool-meta">No parameters</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-noparams">This tool takes no parameters.</p>
</div>
</details>
<details class="qa-item ref-tool" id="camt-exceptions-get_required_fields">
<summary class="qa-q">
<span class="ref-tool-name"><code>get_required_fields</code></span>
<span class="ref-tool-brief">Return the required top-level fields for an E&amp;I message type.</span>
<span class="ref-tool-meta">1 parameter · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of get_required_fields</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>message_type</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>An E&amp;I message type, e.g. 'camt.056.001.12' (see list_message_types).</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="camt-exceptions-generate_message">
<summary class="qa-q">
<span class="ref-tool-name"><code>generate_message</code></span>
<span class="ref-tool-brief">Generate a validated ISO 20022 E&amp;I XML message from a record. For camt.056, the record cancels/recalls a previously sent payment (assignment ids + agent BICs + a list of 'transactions' with the original payment references and a cancellation reason code). Output is validated against the bundled XSD before it is returned.</span>
<span class="ref-tool-meta">2 parameters · 2 required</span>
</summary>
<div class="qa-a ref-tool-body">
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of generate_message</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>message_type</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>An E&amp;I message type, e.g. 'camt.056.001.12' (see list_message_types).</td>
</tr>
<tr>
<td><code>record</code></td>
<td>object</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>Message fields; see get_required_fields.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="camt-exceptions-validate_xml">
<summary class="qa-q">
<span class="ref-tool-name"><code>validate_xml</code></span>
<span class="ref-tool-brief">Validate raw ISO 20022 XML against an E&amp;I message type's bundled XSD; returns is_valid plus any schema errors.</span>
<span class="ref-tool-meta">2 parameters · 2 required</span>
</summary>
<div class="qa-a ref-tool-body">
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of validate_xml</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>message_type</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>An E&amp;I message type, e.g. 'camt.056.001.12' (see list_message_types).</td>
</tr>
<tr>
<td><code>xml</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>Raw ISO 20022 XML to validate.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
</div>
</section>

<section class="newsroom ref-server" id="ap2">
<header class="cat-section-head">
<p class="cat-kicker">ap2-iso20022 · BRIDGE</p>
<h2 class="cat-headline">Agent mandate to bank rail.</h2>
<p class="cat-lede">Normalises AP2/x402 agent mandates, checks guardrails, and emits pain.001/pacs.008-ready records. Never moves money.</p>
</header>
<p class="ref-capture">5 tools · v0.0.1 · captured live over MCP stdio on 2026-07-15 with <code>uvx --from &quot;ap2-iso20022&quot; ap2-iso20022-mcp</code></p>
<div class="qa-list ref-tools">
<details class="qa-item ref-tool" id="ap2-normalize_ap2">
<summary class="qa-q">
<span class="ref-tool-name"><code>normalize_ap2</code></span>
<span class="ref-tool-brief">Normalise a Google AP2 (Agent Payments Protocol) mandate payload into a canonical mandate the other tools accept.</span>
<span class="ref-tool-meta">1 parameter · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of normalize_ap2</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>payload</code></td>
<td>object</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>An AP2 mandate payload.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="ap2-normalize_x402">
<summary class="qa-q">
<span class="ref-tool-name"><code>normalize_x402</code></span>
<span class="ref-tool-brief">Normalise a Coinbase x402 (HTTP-402) payment requirement/receipt into a canonical mandate the other tools accept.</span>
<span class="ref-tool-meta">1 parameter · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of normalize_x402</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>payload</code></td>
<td>object</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>An x402 payment payload.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="ap2-check_mandate">
<summary class="qa-q">
<span class="ref-tool-name"><code>check_mandate</code></span>
<span class="ref-tool-brief">Guardrail a mandate before it becomes a payment: check required fields, the spending cap (amount &lt;= max_amount), expiry (when 'as_of' is supplied), and whether an authorisation proof is present. Returns ok plus any violations and warnings. Run this before converting.</span>
<span class="ref-tool-meta">2 parameters · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of check_mandate</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>mandate</code></td>
<td>object</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>A canonical mandate object (see normalize_ap2/normalize_x402 output): payer_/payee_ name+account_iban, amount, currency, plus optional reference, execution_date, max_amount, expiry, proof_type/proof_value.</td>
</tr>
<tr>
<td><code>as_of</code></td>
<td>string, nullable</td>
<td><span class="ref-req ref-req-optional">Optional</span></td>
<td>ISO date/datetime to evaluate expiry against.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="ap2-to_pain001">
<summary class="qa-q">
<span class="ref-tool-name"><code>to_pain001</code></span>
<span class="ref-tool-brief">Convert a canonical mandate into a pain.001 record (customer credit transfer initiation) using the exact field names pain001 expects, so it feeds straight into pain001 generate_message for wire-valid XML.</span>
<span class="ref-tool-meta">1 parameter · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of to_pain001</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>mandate</code></td>
<td>object</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>A canonical mandate object (see normalize_ap2/normalize_x402 output): payer_/payee_ name+account_iban, amount, currency, plus optional reference, execution_date, max_amount, expiry, proof_type/proof_value.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="ap2-to_pacs008">
<summary class="qa-q">
<span class="ref-tool-name"><code>to_pacs008</code></span>
<span class="ref-tool-brief">Convert a canonical mandate into a pacs.008 record (FI-to-FI credit transfer) using the field names pacs008 expects, for interbank settlement of an agent-authorised payment.</span>
<span class="ref-tool-meta">1 parameter · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of to_pacs008</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>mandate</code></td>
<td>object</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>A canonical mandate object (see normalize_ap2/normalize_x402 output): payer_/payee_ name+account_iban, amount, currency, plus optional reference, execution_date, max_amount, expiry, proof_type/proof_value.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
</div>
</section>

<section class="newsroom ref-server" id="acmt001">
<header class="cat-section-head">
<p class="cat-kicker">acmt001-mcp · ACCOUNTS</p>
<h2 class="cat-headline">Account management.</h2>
<p class="cat-lede">acmt.001 account opening, maintenance and verification, validated against the bundled schema.</p>
</header>
<p class="ref-capture">6 tools · v0.0.5 · captured live over MCP stdio on 2026-07-15 with <code>uvx --from &quot;acmt001-mcp&quot; acmt001-mcp</code></p>
<div class="qa-list ref-tools">
<details class="qa-item ref-tool" id="acmt001-list_message_types">
<summary class="qa-q">
<span class="ref-tool-name"><code>list_message_types</code></span>
<span class="ref-tool-brief">List every supported ISO 20022 acmt message type and its human name.</span>
<span class="ref-tool-meta">No parameters</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this first, before any generation or validation call, to discover the exact <code>message_type</code> strings this server accepts (e.g. <code>acmt.001.001.08</code> Account Opening Instruction). Do not use it to fetch a type's fields or schema -- call <code>get_required_fields</code> or <code>get_input_schema</code> for that.</p>
<p class="ref-tool-desc">Returns a list of <code>{"message_type": ..., "name": ...}</code> dictionaries, one per supported message type (e.g. <code>acmt.001.001.08</code>).</p>
<p class="ref-noparams">This tool takes no parameters.</p>
</div>
</details>
<details class="qa-item ref-tool" id="acmt001-get_required_fields">
<summary class="qa-q">
<span class="ref-tool-name"><code>get_required_fields</code></span>
<span class="ref-tool-brief">List only the required input field names for an acmt message type.</span>
<span class="ref-tool-meta">1 parameter · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this for a quick checklist of the mandatory columns before building account records. When you need full type/format constraints (not just which fields are required), call <code>get_input_schema</code> instead.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of get_required_fields</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>message_type</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>A supported ISO 20022 acmt message type, e.g. 'acmt.001.001.08' Account Opening Instruction. Must be exactly one of: 'acmt.001.001.08', 'acmt.002.001.08', 'acmt.003.001.08', 'acmt.005.001.06', 'acmt.006.001.07', 'acmt.007.001.05', 'acmt.008.001.05', 'acmt.009.001.04', 'acmt.010.001.04', 'acmt.011.001.04', 'acmt.012.001.04', 'acmt.013.001.04', 'acmt.014.001.05', 'acmt.015.001.05', 'acmt.016.001.05', 'acmt.017.001.05', 'acmt.018.001.05', 'acmt.019.001.04', 'acmt.020.001.04', 'acmt.021.001.04', 'acmt.022.001.04', 'acmt.023.001.04', 'acmt.024.001.04', 'acmt.027.001.06', 'acmt.028.001.06', 'acmt.029.001.06', 'acmt.030.001.04', 'acmt.031.001.06', 'acmt.032.001.06', 'acmt.033.001.02', 'acmt.034.001.06', 'acmt.035.001.02', 'acmt.036.001.01', 'acmt.037.001.02' (see list_message_types). One of: <code>acmt.001.001.08</code> · <code>acmt.002.001.08</code> · <code>acmt.003.001.08</code> · <code>acmt.005.001.06</code> · <code>acmt.006.001.07</code> · <code>acmt.007.001.05</code> · <code>acmt.008.001.05</code> · <code>acmt.009.001.04</code> · <code>acmt.010.001.04</code> · <code>acmt.011.001.04</code> · <code>acmt.012.001.04</code> · <code>acmt.013.001.04</code> · <code>acmt.014.001.05</code> · <code>acmt.015.001.05</code> · <code>acmt.016.001.05</code> · <code>acmt.017.001.05</code> · <code>acmt.018.001.05</code> · <code>acmt.019.001.04</code> · <code>acmt.020.001.04</code> · <code>acmt.021.001.04</code> · <code>acmt.022.001.04</code> · <code>acmt.023.001.04</code> · <code>acmt.024.001.04</code> · <code>acmt.027.001.06</code> · <code>acmt.028.001.06</code> · <code>acmt.029.001.06</code> · <code>acmt.030.001.04</code> · <code>acmt.031.001.06</code> · <code>acmt.032.001.06</code> · <code>acmt.033.001.02</code> · <code>acmt.034.001.06</code> · <code>acmt.035.001.02</code> · <code>acmt.036.001.01</code> · <code>acmt.037.001.02</code>.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="acmt001-get_input_schema">
<summary class="qa-q">
<span class="ref-tool-name"><code>get_input_schema</code></span>
<span class="ref-tool-brief">Return the full JSON Schema for a message type's flat input record.</span>
<span class="ref-tool-meta">1 parameter · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this to learn every field, its type, and its constraints before assembling records, or to drive a form/UI. For just the required-field names use <code>get_required_fields</code>; to actually check records against this schema use <code>validate_records</code>.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of get_input_schema</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>message_type</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>A supported ISO 20022 acmt message type, e.g. 'acmt.001.001.08' Account Opening Instruction. Must be exactly one of: 'acmt.001.001.08', 'acmt.002.001.08', 'acmt.003.001.08', 'acmt.005.001.06', 'acmt.006.001.07', 'acmt.007.001.05', 'acmt.008.001.05', 'acmt.009.001.04', 'acmt.010.001.04', 'acmt.011.001.04', 'acmt.012.001.04', 'acmt.013.001.04', 'acmt.014.001.05', 'acmt.015.001.05', 'acmt.016.001.05', 'acmt.017.001.05', 'acmt.018.001.05', 'acmt.019.001.04', 'acmt.020.001.04', 'acmt.021.001.04', 'acmt.022.001.04', 'acmt.023.001.04', 'acmt.024.001.04', 'acmt.027.001.06', 'acmt.028.001.06', 'acmt.029.001.06', 'acmt.030.001.04', 'acmt.031.001.06', 'acmt.032.001.06', 'acmt.033.001.02', 'acmt.034.001.06', 'acmt.035.001.02', 'acmt.036.001.01', 'acmt.037.001.02' (see list_message_types). One of: <code>acmt.001.001.08</code> · <code>acmt.002.001.08</code> · <code>acmt.003.001.08</code> · <code>acmt.005.001.06</code> · <code>acmt.006.001.07</code> · <code>acmt.007.001.05</code> · <code>acmt.008.001.05</code> · <code>acmt.009.001.04</code> · <code>acmt.010.001.04</code> · <code>acmt.011.001.04</code> · <code>acmt.012.001.04</code> · <code>acmt.013.001.04</code> · <code>acmt.014.001.05</code> · <code>acmt.015.001.05</code> · <code>acmt.016.001.05</code> · <code>acmt.017.001.05</code> · <code>acmt.018.001.05</code> · <code>acmt.019.001.04</code> · <code>acmt.020.001.04</code> · <code>acmt.021.001.04</code> · <code>acmt.022.001.04</code> · <code>acmt.023.001.04</code> · <code>acmt.024.001.04</code> · <code>acmt.027.001.06</code> · <code>acmt.028.001.06</code> · <code>acmt.029.001.06</code> · <code>acmt.030.001.04</code> · <code>acmt.031.001.06</code> · <code>acmt.032.001.06</code> · <code>acmt.033.001.02</code> · <code>acmt.034.001.06</code> · <code>acmt.035.001.02</code> · <code>acmt.036.001.01</code> · <code>acmt.037.001.02</code>.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="acmt001-validate_records">
<summary class="qa-q">
<span class="ref-tool-name"><code>validate_records</code></span>
<span class="ref-tool-brief">Validate flat account records against a message type's input JSON Schema.</span>
<span class="ref-tool-meta">2 parameters · 2 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this before <code>generate_message</code> to catch structural/type errors per record and get a row-by-row error report. This checks JSON-Schema shape only; to validate a single financial identifier in isolation use <code>validate_identifier</code>.</p>
<p class="ref-tool-desc">Returns a report <code>{"valid": bool, "total": int, "valid_count": int, "errors": [...]}</code>.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of validate_records</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>message_type</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>A supported ISO 20022 acmt message type, e.g. 'acmt.001.001.08' Account Opening Instruction. Must be exactly one of: 'acmt.001.001.08', 'acmt.002.001.08', 'acmt.003.001.08', 'acmt.005.001.06', 'acmt.006.001.07', 'acmt.007.001.05', 'acmt.008.001.05', 'acmt.009.001.04', 'acmt.010.001.04', 'acmt.011.001.04', 'acmt.012.001.04', 'acmt.013.001.04', 'acmt.014.001.05', 'acmt.015.001.05', 'acmt.016.001.05', 'acmt.017.001.05', 'acmt.018.001.05', 'acmt.019.001.04', 'acmt.020.001.04', 'acmt.021.001.04', 'acmt.022.001.04', 'acmt.023.001.04', 'acmt.024.001.04', 'acmt.027.001.06', 'acmt.028.001.06', 'acmt.029.001.06', 'acmt.030.001.04', 'acmt.031.001.06', 'acmt.032.001.06', 'acmt.033.001.02', 'acmt.034.001.06', 'acmt.035.001.02', 'acmt.036.001.01', 'acmt.037.001.02' (see list_message_types). One of: <code>acmt.001.001.08</code> · <code>acmt.002.001.08</code> · <code>acmt.003.001.08</code> · <code>acmt.005.001.06</code> · <code>acmt.006.001.07</code> · <code>acmt.007.001.05</code> · <code>acmt.008.001.05</code> · <code>acmt.009.001.04</code> · <code>acmt.010.001.04</code> · <code>acmt.011.001.04</code> · <code>acmt.012.001.04</code> · <code>acmt.013.001.04</code> · <code>acmt.014.001.05</code> · <code>acmt.015.001.05</code> · <code>acmt.016.001.05</code> · <code>acmt.017.001.05</code> · <code>acmt.018.001.05</code> · <code>acmt.019.001.04</code> · <code>acmt.020.001.04</code> · <code>acmt.021.001.04</code> · <code>acmt.022.001.04</code> · <code>acmt.023.001.04</code> · <code>acmt.024.001.04</code> · <code>acmt.027.001.06</code> · <code>acmt.028.001.06</code> · <code>acmt.029.001.06</code> · <code>acmt.030.001.04</code> · <code>acmt.031.001.06</code> · <code>acmt.032.001.06</code> · <code>acmt.033.001.02</code> · <code>acmt.034.001.06</code> · <code>acmt.035.001.02</code> · <code>acmt.036.001.01</code> · <code>acmt.037.001.02</code>.</td>
</tr>
<tr>
<td><code>records</code></td>
<td>array of object</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>One or more flat account records, each a dict of field name -&gt; value; validated against the message type's input JSON Schema (see get_input_schema / get_required_fields).</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="acmt001-validate_identifier">
<summary class="qa-q">
<span class="ref-tool-name"><code>validate_identifier</code></span>
<span class="ref-tool-brief">Validate a single financial identifier (IBAN, BIC, or LEI).</span>
<span class="ref-tool-meta">2 parameters · 2 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">Use this for a one-off identifier check with a clear pass/fail. To validate identifiers embedded across a whole batch of account records, prefer <code>validate_records</code> rather than calling this per field.</p>
<p class="ref-tool-desc">Returns <code>{"kind": str, "value": str, "valid": bool}</code>.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of validate_identifier</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>kind</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>The financial identifier scheme to validate against (case-insensitive). Must be exactly one of: 'bic', 'iban', 'lei'. One of: <code>bic</code> · <code>iban</code> · <code>lei</code>.</td>
</tr>
<tr>
<td><code>value</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>The identifier value to check, e.g. an IBAN, BIC/SWIFT code, or LEI; validated according to the given kind.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="acmt001-generate_message">
<summary class="qa-q">
<span class="ref-tool-name"><code>generate_message</code></span>
<span class="ref-tool-brief">Generate a validated ISO 20022 acmt XML message from in-memory records.</span>
<span class="ref-tool-meta">2 parameters · 2 required</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-tool-desc">This is the primary generation tool: pass account records you already hold in memory and receive an XSD-validated XML document; no file is written. Run <code>validate_records</code> first to surface record-level errors, and <code>list_message_types</code> to confirm the <code>message_type</code> string.</p>
<p class="ref-tool-desc">Returns the validated XML document as a string, or an <code>{"error": ...}</code> payload (serialized) if generation fails.</p>
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of generate_message</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>message_type</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>A supported ISO 20022 acmt message type, e.g. 'acmt.001.001.08' Account Opening Instruction. Must be exactly one of: 'acmt.001.001.08', 'acmt.002.001.08', 'acmt.003.001.08', 'acmt.005.001.06', 'acmt.006.001.07', 'acmt.007.001.05', 'acmt.008.001.05', 'acmt.009.001.04', 'acmt.010.001.04', 'acmt.011.001.04', 'acmt.012.001.04', 'acmt.013.001.04', 'acmt.014.001.05', 'acmt.015.001.05', 'acmt.016.001.05', 'acmt.017.001.05', 'acmt.018.001.05', 'acmt.019.001.04', 'acmt.020.001.04', 'acmt.021.001.04', 'acmt.022.001.04', 'acmt.023.001.04', 'acmt.024.001.04', 'acmt.027.001.06', 'acmt.028.001.06', 'acmt.029.001.06', 'acmt.030.001.04', 'acmt.031.001.06', 'acmt.032.001.06', 'acmt.033.001.02', 'acmt.034.001.06', 'acmt.035.001.02', 'acmt.036.001.01', 'acmt.037.001.02' (see list_message_types). One of: <code>acmt.001.001.08</code> · <code>acmt.002.001.08</code> · <code>acmt.003.001.08</code> · <code>acmt.005.001.06</code> · <code>acmt.006.001.07</code> · <code>acmt.007.001.05</code> · <code>acmt.008.001.05</code> · <code>acmt.009.001.04</code> · <code>acmt.010.001.04</code> · <code>acmt.011.001.04</code> · <code>acmt.012.001.04</code> · <code>acmt.013.001.04</code> · <code>acmt.014.001.05</code> · <code>acmt.015.001.05</code> · <code>acmt.016.001.05</code> · <code>acmt.017.001.05</code> · <code>acmt.018.001.05</code> · <code>acmt.019.001.04</code> · <code>acmt.020.001.04</code> · <code>acmt.021.001.04</code> · <code>acmt.022.001.04</code> · <code>acmt.023.001.04</code> · <code>acmt.024.001.04</code> · <code>acmt.027.001.06</code> · <code>acmt.028.001.06</code> · <code>acmt.029.001.06</code> · <code>acmt.030.001.04</code> · <code>acmt.031.001.06</code> · <code>acmt.032.001.06</code> · <code>acmt.033.001.02</code> · <code>acmt.034.001.06</code> · <code>acmt.035.001.02</code> · <code>acmt.036.001.01</code> · <code>acmt.037.001.02</code>.</td>
</tr>
<tr>
<td><code>records</code></td>
<td>array of object</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td>One or more flat account records, each a dict of field name -&gt; value, from which the acmt XML is generated; run validate_records first to surface record-level errors.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
</div>
</section>

<section class="newsroom ref-server" id="bankstatementparser">
<header class="cat-section-head">
<p class="cat-kicker">bankstatementparser-mcp · PARSE STATEMENTS</p>
<h2 class="cat-headline">Legacy statements, structured.</h2>
<p class="cat-lede">Format detection and parsing for camt.053, pain.001, MT940, CSV, OFX and QFX statements.</p>
</header>
<p class="ref-capture">5 tools · v1.28.1 · captured live over MCP stdio on 2026-07-15 with <code>uvx --from &quot;bankstatementparser-mcp&quot; bankstatementparser-mcp</code></p>
<div class="qa-list ref-tools">
<details class="qa-item ref-tool" id="bankstatementparser-list_supported_formats">
<summary class="qa-q">
<span class="ref-tool-name"><code>list_supported_formats</code></span>
<span class="ref-tool-brief">List every bank statement format the parser can read.</span>
<span class="ref-tool-meta">No parameters</span>
</summary>
<div class="qa-a ref-tool-body">
<p class="ref-noparams">This tool takes no parameters.</p>
</div>
</details>
<details class="qa-item ref-tool" id="bankstatementparser-detect_format">
<summary class="qa-q">
<span class="ref-tool-name"><code>detect_format</code></span>
<span class="ref-tool-brief">Detect which statement format a payload is.</span>
<span class="ref-tool-meta">2 parameters · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of detect_format</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>content</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td></td>
</tr>
<tr>
<td><code>filename</code></td>
<td>string</td>
<td><span class="ref-req ref-req-optional">Optional</span></td>
<td>Default: <code>&quot;statement.xml&quot;</code>.</td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="bankstatementparser-parse_statement">
<summary class="qa-q">
<span class="ref-tool-name"><code>parse_statement</code></span>
<span class="ref-tool-brief">Parse a statement into structured transactions and a summary.</span>
<span class="ref-tool-meta">4 parameters · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of parse_statement</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>content</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td></td>
</tr>
<tr>
<td><code>filename</code></td>
<td>string</td>
<td><span class="ref-req ref-req-optional">Optional</span></td>
<td>Default: <code>&quot;statement.xml&quot;</code>.</td>
</tr>
<tr>
<td><code>format</code></td>
<td>string, nullable</td>
<td><span class="ref-req ref-req-optional">Optional</span></td>
<td></td>
</tr>
<tr>
<td><code>limit</code></td>
<td>integer, nullable</td>
<td><span class="ref-req ref-req-optional">Optional</span></td>
<td></td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="bankstatementparser-validate_statement">
<summary class="qa-q">
<span class="ref-tool-name"><code>validate_statement</code></span>
<span class="ref-tool-brief">Check whether a statement parses cleanly (a dry run).</span>
<span class="ref-tool-meta">3 parameters · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of validate_statement</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>content</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td></td>
</tr>
<tr>
<td><code>filename</code></td>
<td>string</td>
<td><span class="ref-req ref-req-optional">Optional</span></td>
<td>Default: <code>&quot;statement.xml&quot;</code>.</td>
</tr>
<tr>
<td><code>format</code></td>
<td>string, nullable</td>
<td><span class="ref-req ref-req-optional">Optional</span></td>
<td></td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
<details class="qa-item ref-tool" id="bankstatementparser-summarize_statement">
<summary class="qa-q">
<span class="ref-tool-name"><code>summarize_statement</code></span>
<span class="ref-tool-brief">Return only the statement summary (no per-transaction rows).</span>
<span class="ref-tool-meta">3 parameters · 1 required</span>
</summary>
<div class="qa-a ref-tool-body">
<div class="ref-params-wrap">
<table class="ref-params">
<caption class="visually-hidden">Parameters of summarize_statement</caption>
<thead>
<tr>
<th scope="col">Parameter</th>
<th scope="col">Type</th>
<th scope="col">Required</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>content</code></td>
<td>string</td>
<td><span class="ref-req ref-req-required">Required</span></td>
<td></td>
</tr>
<tr>
<td><code>filename</code></td>
<td>string</td>
<td><span class="ref-req ref-req-optional">Optional</span></td>
<td>Default: <code>&quot;statement.xml&quot;</code>.</td>
</tr>
<tr>
<td><code>format</code></td>
<td>string, nullable</td>
<td><span class="ref-req ref-req-optional">Optional</span></td>
<td></td>
</tr>
</tbody>
</table>
</div>
</div>
</details>
</div>
</section>

<!-- END GENERATED: mcp-tool-catalog -->

<section class="setup-finale" aria-labelledby="finale-heading"><p class="setup-finale-eyebrow">CONSISTENT ACROSS ALL NINE SERVERS</p><h2 id="finale-heading" class="setup-finale-headline">Same contract, every server.</h2><p class="setup-finale-lede">JSON in; validated JSON or XSD-checked XML out; a structured error rather than an exception. Read-only, idempotent, closed-world hints so your client can reason about safety.</p><p class="setup-finale-cta"><a href="/iso20022-mcp-recipes/index.html">See the recipes <span aria-hidden="true">›</span></a> · <a href="/iso20022-mcp/index.html">Back to the suite <span aria-hidden="true">›</span></a></p></section>
