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
description: "Tool reference for the ISO 20022 MCP Suite: every server and the tools it exposes — the gateway, pain001, pacs008, camt053, acmt001, reconcile, camt-exceptions and the AP2/x402 bridge."
format-detection: "telephone=no"
hreflang: "en"
icon: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
id: "https://sebastienrousseau.com/iso20022-mcp-reference"
image_alt: "ISO 20022 MCP Suite tool reference"
image_height: "162"
image_width: "162"
image: "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp"
keywords: "ISO 20022 MCP tools, MCP tool reference, pain001 tools, pacs008 tools, camt053 tools, reconcile-mcp tools, ap2-iso20022 tools, generate_message, validate_records"
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
name: "ISO 20022 MCP Suite — tool reference."
permalink: "https://sebastienrousseau.com/iso20022-mcp-reference"
rating: "general"
referrer: "no-referrer"
revisit-after: "7 days"
robots: "index, follow"
short_name: "iso20022-mcp reference"
subtitle: "Every server in the suite and the tools it exposes. Eight servers, one consistent contract: JSON in, validated JSON or XSD-checked XML out."
tags: "ISO 20022, MCP, Tool Reference, pain.001, pacs.008, camt.053, acmt.001, Reconciliation, AP2, x402, Fintech, Open Source"
theme-color: "0, 67, 165"
title: "ISO 20022 MCP Suite — tool reference"
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
item_title: "ISO 20022 MCP Suite — tool reference"
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

twitter_card: "summary"
twitter_creator: "@wwdseb"
twitter_description: "Tool reference for the ISO 20022 MCP Suite: every server and the tools it exposes."
twitter_image: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
twitter_image_alt: "ISO 20022 MCP Suite tool reference"
twitter_site: "@wwdseb"
twitter_title: "ISO 20022 MCP Suite — tool reference"
twitter_url: "https://sebastienrousseau.com/iso20022-mcp-reference"

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

<p class="story-intro">Every server speaks the same contract: JSON records in, validated JSON or XSD-checked XML out, with an <code>{"error": …}</code> payload rather than an exception when something is wrong. Below is what each exposes. New to the suite? Start with <a href="/iso20022-mcp-docs/index.html">the quickstart</a>.</p>

<section class="newsroom" id="gateway">
<header class="cat-section-head"><p class="cat-kicker">iso20022-mcp · THE GATEWAY</p><h2 class="cat-headline">One surface, all families.</h2></header>
<div class="story-why"><ul class="story-why-list">
<li><code>search(query)</code> — find message types and suite servers by use-case ("cancel a payment").</li>
<li><code>list_families()</code> · <code>list_servers()</code> — the families and the full suite map, with install status.</li>
<li><code>describe(message_type)</code> — required fields + input schema for a type.</li>
<li><code>validate(message_type, records)</code> · <code>generate(message_type, records)</code> · <code>parse(message_type, xml)</code> — routed to the family's backing server; camt.056/camt.029 route to camt-exceptions.</li>
</ul></div>
</section>

<section class="newsroom" id="pain001">
<header class="cat-section-head"><p class="cat-kicker">pain001-mcp · INITIATE</p><h2 class="cat-headline">Customer credit transfers.</h2></header>
<div class="story-why"><ul class="story-why-list">
<li><code>list_message_types</code> · <code>get_required_fields</code> · <code>get_input_schema</code> — discover pain.001 shapes.</li>
<li><code>validate_records</code> · <code>validate_identifier</code> · <code>validate_xml_against_schema</code> · <code>validate_payment_scheme</code> — pre-flight checks (IBAN/BIC, XSD, SEPA/CBPR rulebooks).</li>
<li><code>generate_message</code> · <code>generate_message_from_file</code> · <code>build_payment_batch</code> — produce validated pain.001.</li>
<li><code>migrate_records</code> · <code>sanitize_to_iso</code> · <code>convert_mt</code> — cross-version migration, charset sanitisation, MT101 → pain.001.</li>
</ul></div>
</section>

<section class="newsroom" id="pacs008">
<header class="cat-section-head"><p class="cat-kicker">pacs008-mcp · SETTLE</p><h2 class="cat-headline">FI-to-FI transfers, returns, status.</h2></header>
<div class="story-why"><ul class="story-why-list">
<li><code>list_message_types</code> · <code>list_schemes</code> · <code>get_scheme</code> · <code>get_required_fields</code> · <code>get_input_schema</code> — pacs.008/.004/.002 discovery.</li>
<li><code>validate_records</code> · <code>validate_scheme</code> · <code>validate_xml</code> · <code>generate_message</code> · <code>parse_message</code> — the generate/validate/parse core.</li>
<li><code>convert_mt103</code> — legacy MT103 → pacs.008.</li>
<li><code>classify_address</code> · <code>validate_address</code> · <code>repair_address</code> · <code>validate_addresses</code> — the November 2026 structured-address cliff toolkit.</li>
</ul></div>
</section>

<section class="newsroom" id="camt053">
<header class="cat-section-head"><p class="cat-kicker">camt053-mcp · READ STATEMENTS</p><h2 class="cat-headline">Bank-to-customer statements.</h2></header>
<div class="story-why"><ul class="story-why-list">
<li><code>list_message_types</code> · <code>get_required_fields</code> · <code>get_input_schema</code> · <code>validate_records</code> · <code>validate_statement</code> — camt.053/052 discovery + validation.</li>
<li><code>parse_statement</code> · <code>list_entries</code> · <code>filter_entries</code> — parse and query booked entries.</li>
<li><code>convert_mt940</code> · <code>convert_mt942</code> — legacy MT94x → camt.</li>
<li><code>list_return_reasons</code> · <code>generate_reversal</code> · <code>check_cbpr_readiness</code> — reason-code lookup, reversing entries, Nov-2026 CBPR+ readiness.</li>
</ul></div>
</section>

<section class="newsroom" id="reconcile">
<header class="cat-section-head"><p class="cat-kicker">reconcile-mcp · RECONCILE</p><h2 class="cat-headline">Statements against expected payments.</h2></header>
<div class="story-why"><ul class="story-why-list">
<li><code>reconcile(expected, observed, options)</code> — exact, short/over, one-to-many and many-to-one matching with an explainable score and reasons.</li>
<li><code>explain_match(expected, observed)</code> — the per-signal breakdown for a single pair (a tuning aid).</li>
<li><code>normalize_pain001(document)</code> · <code>normalize_camt053(document)</code> — adapt parsed output into canonical records.</li>
<li><code>list_sandbox_scenarios</code> · <code>load_sandbox_scenario</code> · <code>run_sandbox_scenario</code> — deterministic test-mode; try it with zero real data.</li>
</ul></div>
</section>

<section class="newsroom" id="camt-exceptions">
<header class="cat-section-head"><p class="cat-kicker">camt-exceptions · RESOLVE</p><h2 class="cat-headline">Cancellation &amp; investigation.</h2></header>
<div class="story-why"><ul class="story-why-list">
<li><code>list_message_types</code> · <code>get_required_fields</code> — supported E&amp;I types (camt.056, camt.029) and their fields.</li>
<li><code>generate_message(message_type, record)</code> — a validated E&amp;I message, checked against the bundled official XSD before it is returned.</li>
<li><code>validate_xml(message_type, xml)</code> — validate raw XML against the message's XSD.</li>
</ul></div>
</section>

<section class="newsroom" id="ap2">
<header class="cat-section-head"><p class="cat-kicker">ap2-iso20022 · BRIDGE</p><h2 class="cat-headline">Agent mandate → bank rail.</h2></header>
<div class="story-why"><ul class="story-why-list">
<li><code>normalize_ap2(payload)</code> · <code>normalize_x402(payload)</code> — a Google AP2 or Coinbase x402 mandate into a canonical mandate.</li>
<li><code>check_mandate(mandate, as_of)</code> — guardrails: required fields, spending cap, expiry, authorisation proof.</li>
<li><code>to_pain001(mandate)</code> · <code>to_pacs008(mandate)</code> — records that feed pain001 / pacs008 for wire-valid XML. Never moves money.</li>
</ul></div>
</section>

<section class="newsroom" id="acmt001">
<header class="cat-section-head"><p class="cat-kicker">acmt001-mcp · ACCOUNTS</p><h2 class="cat-headline">Account management.</h2></header>
<div class="story-why"><ul class="story-why-list">
<li><code>list_message_types</code> · <code>get_required_fields</code> · <code>get_input_schema</code> · <code>validate_records</code> · <code>validate_identifier</code> · <code>generate_message</code> — open, maintain and verify accounts (acmt.001), validated against the bundled schema.</li>
</ul></div>
</section>

<section class="setup-finale" aria-labelledby="finale-heading"><p class="setup-finale-eyebrow">CONSISTENT ACROSS ALL EIGHT SERVERS</p><h2 id="finale-heading" class="setup-finale-headline">Same contract, every server.</h2><p class="setup-finale-lede">JSON in; validated JSON or XSD-checked XML out; a structured error rather than an exception. Read-only, idempotent, closed-world hints so your client can reason about safety.</p><p class="setup-finale-cta"><a href="/iso20022-mcp-recipes/index.html">See the recipes <span aria-hidden="true">›</span></a> · <a href="/iso20022-mcp/index.html">Back to the suite <span aria-hidden="true">›</span></a></p></section>
