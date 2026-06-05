# Postbuild

> Last Updated: June 4, 2026

The postbuild script is a single-page orchestrator that applies eighteen independent changes to every rendered page.
These tasks run inside the Shokunin static site generator after the main HTML compile step finishes.

## Contents

This guide covers the order of operations, details for each pass, counters, file safety, development patterns, and build speeds.

## Order of operations

The order of operations ensures that each page optimization occurs in a sequence that keeps security hashes valid.

```mermaid
%%{init: {'theme':'neutral'} }%%
flowchart TB
 P0[HTML page<br/>from public/]

 subgraph SEO["SEO + JSON-LD"]
 S1[scrub_localhost_urls]
 S2[stamp_asset_fingerprints]
 S3[fix_sri]
 S4[inject_itemlist]
 S5[inject_tech_article]
 S6[inject_software_source_code]
 S7[fix_social_image]
 S8[inject_og_completeness]
 S9[stamp_image_dimensions]
 S10[inject_howto]
 S11[inject_word_count]
 S12[inject_about]
 end

 subgraph ART["Article furniture"]
 A1[inject_article_furniture<br/>(tag badges, meta bar)]
 A2[inject_sigstore_attestation]
 A3[inject_anchor_links_and_toc]
 A4[inject_citations]
 A5[inject_sources_list]
 A6[inject_mermaid]
 end

 subgraph NAV["Navigation"]
 N1[inject_nav_active]
 N2[inject_prev_next_nav]
 N3[inject_hreflang]
 end

 subgraph FIN["Finalisation"]
 F1[inject_speculation_rules]
 F2[inject_github_stats]
 F3[hoist_body_link_stylesheets]
 F4[inject_jsonld_hashes<br/>MUST run last]
 end

 P0 --> S1 --> S2 --> S3 --> S4 --> S5 --> S6 --> S7 --> S8 --> S9 --> S10 --> S11 --> S12
 S12 --> A1 --> A2 --> A3 --> A4 --> A5 --> A6
 A6 --> N1 --> N2 --> N3
 N3 --> F1 --> F2 --> F3 --> F4
 F4 --> OUT[Patched HTML<br/>written back]
```

We must compute the script hashes last because any changes to the page after this step will block the scripts from running.

## Pass-by-pass reference

The postbuild process runs a series of functions that modify HTML tags, security hashes, and layout elements.

### 1: `scrub_localhost_urls`

This pass rewrites local host URLs to the production web site links on every page.

### 2: `stamp_asset_fingerprints`

This pass copies fingerprinted assets to their bare name files so references resolve correctly.

### 3: `fix_sri`

This pass replaces style integrity hashes with real codes computed from the actual file bytes.

### 5: `inject_itemlist`

This pass inserts structured list schemas on section landing pages to help search engine crawlers.

### 5: `inject_tech_article`

This pass appends technical article schema tags to posts that cover coding or software topics.

### 6: `inject_software_source_code`

This pass adds software source code schemas to project pages to describe open source libraries.

### 7: `fix_social_image`

This pass sets social share images using the banner path defined in the page headers.

### 8: `inject_og_completeness`

This pass fills in missing open graph tags to ensure page cards render nicely on social feeds.

### 9: `stamp_image_dimensions`

This pass stamps explicit width and height dimensions on image tags to prevent layout shifts.

### 10: `inject_howto`

This pass creates step-by-step schema blocks for guides that describe specific setup procedures.

### 11: `inject_word_count`

This pass counts words in the main article body and stores it in the page schema.

### 12: `inject_about`

This pass links article entities to Wikidata records to help AI search engines parse the context.

### 13: `inject_article_furniture`

This pass injects E-E-A-T author cards and reading time badges into the post layouts.

### 14: `inject_sigstore_attestation`

This pass appends a verification link if the local cryptographic signing config file is present.

### 15: `inject_anchor_links_and_toc`

This pass adds clickable hash anchors to headings and inserts a table of contents block.

### 16: `inject_citations`

This pass builds a schema list of all external sources cited in the article body.

### 17: `inject_sources_list`

This pass renders a visible bibliography list at the bottom of posts with external references.

### 18: `inject_mermaid`

This pass loads the diagram library if a post contains raw diagram code blocks.

### 19: `inject_nav_active`

This pass marks the active header nav link to highlight the current section page.

### 20: `inject_prev_next_nav`

This pass adds navigation links to the previous and next articles in date order.

### 21: `inject_hreflang`

This pass injects alternate language tags for every active translation to help search engines.

### 22: `inject_speculation_rules`

This pass adds rules that tell modern browsers to prerender linked pages in the background.

### 23: `inject_github_stats`

This pass updates repository stars and forks statistics on open source project cards.

### 24: `hoist_body_link_stylesheets`

This pass moves body style links to the page head block to meet accessibility standards.

### 25: `inject_jsonld_hashes`

This pass computes hashes of inline scripts and updates the content security policy rule.

## Per-pass counters

A counters class tracks how many times each optimization step changes a page during a build run.

The tool outputs these counts at the end of the build to help you check the output.

## Idempotence guarantees

The postbuild script is idempotent, which means running it multiple times on the same files will not change them.

The functions check for existing tags and only apply changes to pages that have not been optimized.

## Common patterns

We use simple developer workflows to add new build runs or test existing functions in isolation.

- Step 1: Create the function in the postbuild library.
- Step 2: Add unit tests to check the function behavior.
- Step 3: Register the function in the main build run order.
- Step 4: Run the test command to verify that all tests stay green.

## Performance

The entire postbuild suite optimizes thousands of pages in less than three seconds on a modern computer.

Most of the execution time is spent reading and writing files rather than processing the HTML string.

| Pass | Time per page | Total time |
|---|---|---|
| `fix_sri` | 80 micro seconds | 150 ms |
| `inject_word_count` | 200 micro seconds | 370 ms |
| `inject_article_furniture` | 350 micro seconds | 650 ms |
| `inject_jsonld_hashes` | 500 micro seconds | 920 ms |
| Combined passes | 200 micro seconds | 370 ms |
