# Publishing guide

> Last Updated: June 4, 2026

This guide explains how an article moves from a local Markdown file to a live page in twenty-eight languages.
We use the Static Site Generator static site generator and automated postbuild scripts to compile the pages for the Sebastien Rousseau web platform.

## Contents

This guide covers the mental model, prerequisites, daily flow, draft promotion steps, metadata rules, translation steps, deployment tests, and failure modes.

## Mental model

Every published article translates into twenty-eight different files and formats during the build run.

First, we create one English source file in the posts folder.
Second, we write twenty-seven translated posts in their respective language directories.
Third, we update twenty-seven slug mapping files to link the localized pages.

The static site generator compiles these sources into HTML pages, and the postbuild script adds hreflang tags, feeds, sitemaps, and schemas.

- Hreflang alternates: each page links to its twenty-seven siblings
- Sitemap files: the tool writes sitemap entries for all rendered pages
- Feeds: the build creates twenty-eight RSS, Atom, and JSON feeds
- Schema blocks: we add BlogPosting, TechArticle, and Person schemas
- Listings: the generator updates the article and project cards
- Homepage: we manually update the recent posts grid

The integration build checks these pages against thirteen safety gates.

## Prerequisites

You must install Rust, python, and the site generator before you can build and publish articles.

We also use git for commit signing and a local terminal assistant for translations.

- Python: version 3.11 or higher
- Rust: cargo packages with the Static Site Generator site builder
- WASM: compiler tools for the lab pages
- Git: signing keys loaded in your local agent
- Client: terminal window to run local commands

The dependencies file lists the required python libraries for build runs.

## TL;DR daily flow

You can publish a new article with a single command that runs the draft move and translation tool.

```bash
cp my-piece.md _drafts/2026-05-20-my-piece.md
# In Claude:
/publish-today
```

The build command handles the file promotion, builds translations, and pushes commits automatically.

## Step-by-step: publish today's article

You publish a new post by writing the source draft, promoting it, translating stubs, and pushing commits.

The build tool guides you through each step and verifies the pages.

### Step 1: Write the EN draft

Create your English draft file with a date prefix and add the required header metadata blocks.

The filename date prefix defines the publication date for the build tool.
The body uses standard Markdown with an executive summary, takeaway blocks, tables, and references.

### Step 2: Run the slash command

Trigger the automated publishing command inside the local terminal to start the build flow.

The command script runs the promotion steps and asks you to confirm file writes.

### Step 3: Promote draft to post

Run the promotion script to move the draft and create translation files for all active languages.

```bash
./scripts/editorial/publish-daily.sh
```

- Step 1: Locate the daily draft file in the drafts folder.
- Step 2: Move the file to the posts directory.
- Step 3: Create twenty-seven translation stubs with header mappings.
- Step 4: Regenerate the listing grids and homepage files.
- Step 5: Run the build script to verify all gates pass.

If the build succeeds, the stub pages are ready to be translated.

### Step 4: Editorial card setup

Add today's article card to the homepage grid and update the main featured lists.

We update these files manually because card selection requires human choice.

For `_posts/index.md`, add today's card to the grid and remove the oldest card to keep five items.
For `gen_articles.py`, prepend the article tuple to the list and re-run the generator script.

### Step 5: Translate the twenty-seven stubs

Translate the body of each stub post in your terminal using the tone and layout rules.

```bash
python3 scripts/editorial/translate_post.py <slug> --list-stubs
```

The script prints the stubs that need translations.
In your terminal, copy the translated text into each file while keeping the headers intact.

- Match standard technical terms without translating them
- Preserve the markdown headings, lists, tables, and links
- Keep numbers, dates, and statistics exactly as in English
- Use a clear, executive register without hype words

The test gates check that no English chrome leaks into translated pages.

### Step 6: Re-validate

Run the build script to verify that all content passes the integration check gates.

```bash
./build.sh
```

If a check fails, refer to the failure modes guide.

### Step 7: Signed commit and push

Create a signed git commit with the date prefix and push the changes to deploy the site.

```bash
git add -A
git commit -S -m "content: add article and translations"
git push
```

The host builder builds the branch and deploys the updates automatically.

## The frontmatter contract

The build tool expects the draft header block to declare the standard page metadata properties.

These keys define the title, description, dates, layout, schemas, and links.

- `title`: page title.
- `description`: page summary.
- `date`: publish date.
- `layout`: layout template.
- `schema`: JSON-LD types.
- `language`: BCP-47 locale tag.

Copy the headers from a recent post to ensure all required fields are present.

## Editorial decisions you make every day

You must decide which older homepage cards to drop when publishing a new article.

We select the card order manually to keep the content relevant.

| Decision | File to update |
|---|---|
| Choose homepage card to drop | `index.md` |
| Choose articles card to demote | `gen_articles.py` |
| Set page layout type | Draft frontmatter |

The command script prompts you to verify these changes before building.

## Translation flow

The translation tool handles locale slugs, writes stub files, and checks translation quality automatically.

### How the scaffolder works

The promotion script creates localized posts and updates the slug maps for each active language.

First, it checks the term dictionary to translate slugs into Spanish, French, or Japanese.
Second, it writes stub posts with rewritten URLs and language tags.
Third, it updates the slug registry with EN-to-native mappings.

This script is safe to run multiple times because it does not overwrite existing translations.

### How translation itself works

Translations are completed in local terminal conversations to avoid storing sensitive API keys in repositories.

We use your terminal session to edit the files directly.
The language rules guide the style to ensure high translation quality.

### Cost and time

The translation process takes less than ninety minutes for all locales and costs nothing extra.

Our local terminal tool relies on your existing subscription.

| Locales | Time spent | Cost |
|---|---|---|
| `en` | Writing time | Free |
| `5 priority` | 30 minutes | Free |
| `All 27` | 90 minutes | Free |

You can translate pages in one session or split the work across multiple runs.

## What gets auto-refreshed (and what doesn't)

The build tool updates feeds, maps, schemas, and security hashes, but you must edit home cards manually.

The system automates mechanical tasks so you can focus on writing.

### Fully automatic — never touch

The compiler generates sitemaps, RSS feeds, JSON data, and security hashes automatically on every run.

- Sitemap files: generated for all active languages.
- RSS and Atom feeds: written for each locale.
- Agent endpoints: exported for search tools.
- Topic grids: updated with new article paths.
- Security hashes: computed for content rules.

### Editorial — you decide

You choose which cards to feature and which older articles to move off the grids.

- Homepage cards: updated manually in the posts index file.
- Featured order: updated in the articles generator file.

### Scaffolded — you fill in

The script creates the language stub files that you translate in local terminal sessions.

- Stub pages: generated during the draft promotion step.

## Verification and deployment

Verify your deployment by checking the live pages and running lighthouse tests to audit performance.

The builder deploys changes in about two minutes.
You can check the live page headers to confirm that the edge server has loaded the new build.
Run a local lighthouse command to verify that performance, accessibility, and SEO metrics remain perfect.

## Failure modes

The guide provides fixes for common errors like missing translations, link failures, or signature blocks.

Refer to this guide to debug build failures.

| Symptom | Cause | Fix |
|---|---|---|
| `nothing to publish` | No draft file with today's date prefix | Drop draft in folder |
| `missing article translation` | Slug map lacks EN-to-native mapping | Re-run translator |
| `target does not reciprocate` | Localized post file is missing | Re-run translator |
| `string leaked into chrome` | Chrome translation is missing | Update patch file |
| `missing sha256 token` | CSP lacks inline script hash | Check script hashes |
| `page missing from sitemap` | Sitemap built before page creation | Re-run build script |
| `physical CSS property` | RTL page uses left/right margin | Use logical rules |
| `inLanguage mismatch` | Language tags do not match schema | Check frontmatter |
| `git commit hangs` | SSH signing key not loaded | Add key to agent |

If you hit a new error, check the integration logs to see which check failed.

## Adding a new permanent section

To add a new section, create layout files, write generators, and wire the navigation links.

First, create the template in the layouts folder.
Second, write the generator script to compile the listing.
Third, translate the new file for the active locales.
Fourth, add nav links to the layout switcher headers.
Fifth, run the build to check that the sitemap gate passes.

## Adding a new language

Add new locales by registering BCP-47 codes, translating files, and updating switcher menus.

Refer to the internationalization runbook for step-by-step instructions.

- Step 1: Register the language in the matrix file
- Step 2: Create the eleven glossary files for the locale
- Step 3: Copy and translate the post files
- Step 4: Flip the active flag and check the build

## Forking this pipeline for your own site

You can fork this open source pipeline, customize the templates, and update deployment targets.

The entire system uses the Apache-2.0 license.
To run your own site, replace the post files, update layouts, and set your own domain constants.
You can delete the translation folders if you only need a single-language site.
Update the commit signing keys to match your own git profiles.
