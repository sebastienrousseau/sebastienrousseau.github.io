# ssg — Fixes & Native-Migration Specification

**Purpose:** implementation spec for the `ssg` static site generator
(`github.com/sebastienrousseau/static-site-generator`). Two parts:
**A. correctness fixes** for defects found while upgrading this site to
ssg 0.0.46, and **B. native features** to absorb the site's Python
post-processing into ssg so the `build.sh` pipeline shrinks toward
`ssg build`.

**Dependency baseline (what ssg 0.0.46 links today):**
`comrak 0.28.0`, `mdx-gen 0.0.1`, `html-generator 0.0.3`,
`staticdatagen 0.0.10`, `frontmatter-gen 0.0.5/0.0.6`, `pulldown-cmark 0.12`.
Newer versions already exist in the workspace cache (`comrak 0.52`,
`mdx-gen 0.0.2`, `html-generator 0.0.6`) and are referenced below.

**Verification rule for every change:** ssg must be built and tested on
**both `ubuntu-latest` and `macos-latest` (Apple Silicon)**. The two
platforms currently diverge (see A1); a macOS↔Linux byte-diff test is the
strongest regression guard and should be added to ssg's own CI.

---

## Part A — Correctness fixes

### A1 — Raw HTML in Markdown is escaped on macOS (P0, critical)

**Symptom.** Markdown bodies containing raw block HTML (`<section>`,
`<div>`, `<figure>`, inline `<svg>`) render as **escaped text**
(`&lt;section…`) on macOS/Apple Silicon, but render correctly on Linux.
Every page with raw HTML in its body is affected (this site's homepage,
article furniture, etc.). CI (Linux) is unaffected, which is why the bug
hid behind "CI is the source of truth."

**Root cause.** `html-generator 0.0.3` `src/generator.rs` (≈ lines 43–51)
sets the intent correctly:
```rust
let mut comrak_options = ComrakOptions::default();
comrak_options.render.unsafe_ = true;   // raw HTML allowed
comrak_options.render.escape  = false;
```
So the *code* asks comrak to pass raw HTML through — and Linux honours it.
On macOS the compiled `comrak 0.28.0` / `mdx-gen 0.0.1` path escapes it
anyway. This is a platform-divergent defect in the pinned markdown stack,
**not** a config error and **not** fixable downstream in site content.

**Fix.**
1. Bump the markdown stack: `comrak 0.28 → 0.52`, `mdx-gen 0.0.1 → 0.0.2`,
   `html-generator 0.0.3 → 0.0.6`. Newer comrak fixed a family of
   raw-HTML/`unsafe` handling issues.
2. **Field rename caveat:** comrak renamed `render.unsafe_` →
   `render.r#unsafe` across the 0.2x→0.5x range. `html-generator 0.0.6`
   already uses `comrak_options.render.r#unsafe = config.allow_unsafe_html;`
   — verify this compiles against comrak 0.52.
3. **Config-default caveat (regression risk):** `html-generator 0.0.6`
   introduced `HtmlConfig.allow_unsafe_html` which **defaults to `false`**
   (`src/lib.rs` ≈ line 446). `staticdatagen 0.0.10`
   `src/compiler/service.rs::generate_html_content` (line ≈ 193) builds its
   config with `..HtmlConfig::default()` and does **not** set it. If you
   only bump versions, raw HTML will now escape on **both** platforms.
   → **In staticdatagen's `generate_html_content`, explicitly set
   `allow_unsafe_html: true`** (the site authors trusted HTML deliberately;
   sanitisation, if wanted, should be an opt-in separate pass, not silent
   escaping).

**Acceptance / tests.**
- Unit (in html-generator): input `<section class="x"><p>hi</p></section>`
  with default site config → output contains `<section class="x">`, not
  `&lt;section`.
- CI matrix: run the full render test suite on `macos-latest` **and**
  `ubuntu-latest`.
- Golden test: build a fixture site containing raw-HTML blocks and assert
  byte-identical output across the two OS runners.

---

### A2 — RSS `channel.link is missing` hard-fails the whole build (P0)

**Symptom.** ssg 0.0.46 aborts the *entire* compile with
`RSS generation failed: Validation errors: [ValidationError { field:
"channel.link", message: "channel.link is missing" }]` if **any** post
lacks a `permalink:` front-matter field. ~963 archive posts (2018–2024) on
this site predate the convention → build dies. (Worked around here with a
build-time Python backfill; see B1.)

**Root cause.** `staticdatagen 0.0.10` RSS generator derives the channel
`<link>` from `permalink` with no fallback and treats absence as fatal.

**Fix.**
1. **Derivation fallback chain** for the channel/item link:
   `permalink` → `url` → `{site.base_url}/{relative_output_path}` →
   `site.base_url`. ssg already knows each file's output path, so a correct
   link is *always* derivable — it should never be "missing."
2. **Never hard-fail the whole compile on one item.** If a single feed
   entry is genuinely underivable, emit a warning and skip that entry (or
   the one feed), not the build.
3. This makes A2 and B1 disappear together: authors never need to hand-write
   `permalink`.

**Acceptance.** A post with only `title` + `date` + body builds; its feed
`<link>` equals `{base_url}/{output-path}`.

---

### A3 — `structured_data: Missing required HTML element: title` (P1, noisy)

**Symptom.** Per-page warning `Structured data generation failed: Missing
required HTML element: title` on normal pages.

**Root cause.** `html-generator` `generator.rs` Step 5a runs
`generate_structured_data_from_doc` on the **fragment** (before
`wrap_full_document` adds `<title>`), so it can't find a `<title>`.

**Fix.** Source the title from metadata, not the DOM: pass the known title
(front-matter `title`/`seo_title`, else first `<h1>`, else config) into the
structured-data generator. Only warn if *no* title is derivable from any
source.

**Acceptance.** No `structured_data` title warnings on pages that have a
title in front matter or an `<h1>`.

---

### A4 — `news_sitemap: 'day' component could not be parsed` (P1)

**Symptom.** Repeated `Parsing failed: the 'day' component could not be
parsed. Using fallback.` from `staticdatagen::generators::news_sitemap`.

**Root cause.** The news-sitemap date parser expects a format that doesn't
match the front-matter dates in use (`date: "July 1, 2026"`, RSS
`item_pub_date: "Wed, 01 Jul 2026 07:07:07 +0000"`, ISO `last_reviewed:
"2026-07-01"`).

**Fix.** Centralise date parsing in **one** util shared by RSS, sitemap,
and news-sitemap that accepts, in order: RFC 2822 (`%a, %d %b %Y %H:%M:%S
%z`), long form (`%B %-d, %Y`), ISO 8601 (`%Y-%m-%d`). Fall back to file
mtime only as a last resort, and log which field/format failed.

**Acceptance.** No day-parse warnings; news sitemap `<publication_date>` is
correct for all three date formats.

---

### A5 — `inLanguage` ≠ `<html lang>` on locale pages (P1)

**Symptom.** Build warns e.g. `hi/2026-…/index.html: inLanguage='en-GB'
(base 'en') ≠ <html lang> base 'hi'`. JSON-LD `inLanguage` is hardcoded to
the default language instead of the page's.

**Root cause.** Structured-data generation uses a default/site language,
not the page's resolved language.

**Fix.** `inLanguage` (and OpenGraph `og:locale`, `<html lang>`, hreflang
self-ref) must all derive from one resolved page-language value
(front-matter `hreflang`/`language`), so they're always consistent.

**Acceptance.** `inLanguage` == `<html lang>` on every localized page; the
site's schema-diff validator emits zero language-mismatch warnings.

---

### A6 — `frontmatter_gen: Potential path traversal detected` false positives (P2)

**Symptom.** Warnings fire when *content* contains path-like strings
(`src/lib.rs`, `#![deny(missing_docs)]`) — i.e. code snippets in article
bodies/descriptions, not actual paths.

**Root cause.** `frontmatter-gen`'s path-traversal heuristic scans
free-text field values.

**Fix.** Apply the path-traversal guard only to values that are actually
resolved as filesystem paths (template names, include paths, output
targets) — never to descriptive/body text.

**Acceptance.** Code snippets in front matter/body don't trigger the
warning; genuine `../` path escapes still do.

---

### A7 — Deterministic, cross-platform output (P1)

**Why.** This site gates on a reproducibility byte-diff; A1 proves macOS
and Linux can diverge.

**Fix.** Audit ssg for `HashMap`/`HashSet` iteration that reaches output
ordering; replace with `BTreeMap`/sorted iteration. Normalise line endings
to `\n`. Ensure no timestamps/absolute paths/locale-dependent formatting
leak into output. Add a CI job that diffs `macos-latest` vs
`ubuntu-latest` build output and fails on any difference.

---

### A8 — Markdown table alignment emits deprecated `align=` attributes (P1)

**Tracking:** [ssg#618](https://github.com/sebastienrousseau/static-site-generator/issues/618)

**Symptom.** Markdown tables that use column-alignment syntax (`:---`,
`---:`, `:---:`) render as deprecated presentational HTML `align=`
attributes on `<th>`/`<td>`. A strict pa11y AAA audit fails them
(`WCAG2AAA.Principle1.Guideline1_3.1_3_1.H49.AlignAttr`), which breaks the
build with `pa11y: real WCAG failures detected`. Observed on macOS **and**
Linux (comrak 0.28 / html-generator 0.0.3), so it is not the A1 platform
split — it is the default table renderer.

**Root cause.** The markdown→HTML stack maps table column alignment to the
obsolete HTML4 `align` attribute rather than CSS. `align` has been
non-conforming since HTML5 and is a WCAG AAA (H49) failure by definition.

**Fix.** Render alignment as CSS, not an attribute — either
`style="text-align:left|center|right"` or a utility class
(`class="text-left|text-center|text-right"`) on the cell. If alignment
styling is not required, strip `align=` from table cells during HTML
generation. Prefer the CSS route so author-intended alignment is preserved
while staying AAA-clean. (comrak's newer releases expose table-rendering
options worth checking when A1's stack bump lands.)

**Acceptance / tests.**
- Unit: a table with `| :--- | ---: |` produces cells with `text-align`
  CSS (style or class) and **no** `align=` attribute.
- Gate: the fixture site passes a pa11y `WCAG2AAA` run with aligned tables
  present (currently only passable by stripping the alignment colons).

**Interim workaround (in use downstream).** The consuming site strips the
alignment colons from delimiter rows (`:----` → `----`); left is the
default so this is visually identical but loses center/right alignment.

---

## Part B — Move Python post-processing into ssg natively

The site runs a large Python pipeline after `ssg` (in `build.sh` and
`scripts/postbuild/`, `scripts/generators/`). Much of it is generic SSG
work that belongs in ssg. Each item: **current Python → proposed native
feature → config surface → acceptance.** Ordered by leverage.

> **Architectural prerequisites** (unlock most of B):
> 1. **Content collection model** — every source page parsed into a
>    queryable in-memory collection (front matter + rendered body + output
>    URL + locale + tags + date). Listings, feeds, taxonomy, "recent",
>    "related", and sitemaps all become queries over this, not Python.
> 2. **i18n/routing subsystem** — a locale registry + localized-slug map +
>    hreflang graph, derived from the content tree, so translation routing,
>    `<link rel=alternate hreflang>`, and the language switcher are native.
> 3. **Post-render asset pipeline** — a single native pass over emitted
>    output for SRI, fingerprinting, CSP hashing, image dims, preload, and
>    minification.
> 4. **Shared date/URL utilities** (also fixes A2/A4).

### B1 — Permalink / canonical URL derivation → native
- **Python:** `scripts/postbuild/backfill_permalink.py` (added this
  session) injects `permalink` for the ~963 posts that lack it.
- **Native:** ssg derives each page's canonical URL from `output_path +
  site.base_url` when front matter omits `permalink`/`url`. Removes the
  Python script **and** fixes A2.
- **Config:** `site.base_url`; locale path rules (from B2/i18n).
- **Acceptance:** posts with no `permalink` get correct canonical + feed
  links; `backfill_permalink.py` deleted.

### B2 — i18n routing, localized slugs, hreflang, language switcher → native
- **Python:** `scripts/postbuild/regen_slug_maps.py`
  (`_data/i18n/<lang>/slugs.json` from filenames);
  `scripts/postbuild/fix_lang_switcher.py`; hreflang injection in
  `postbuild_transforms.py`.
- **Native:** a locale config (the 28-language registry) + convention that
  `_posts/<lang>/<slug>.md` is the `<lang>` translation of the EN post with
  the same date/slug key. From that ssg generates: localized output paths,
  the EN↔locale slug map, `<link rel=alternate hreflang="…">` (incl.
  `x-default`) on every variant, and a language-switcher partial with
  correct per-locale hrefs.
- **Config:** `[i18n] default_locale`, `locales = […]`, slug-map overrides.
- **Acceptance:** removing all three Python scripts + the committed
  `slugs.json` still yields correct routing, hreflang reciprocity, and
  switcher links; i18n-parity gate passes.

### B3 — Subresource Integrity (SRI) → native
- **Python:** `scripts/postbuild/postbuild_assets.py` computes real
  SHA-384 SRI for externalized CSS/JS and rewrites `integrity=`
  placeholders.
- **Native:** ssg already externalizes inline CSS/JS to `/_csp/<hash>`
  with **placeholder** integrity — it has the bytes, so it should emit the
  **real** `integrity="sha384-…" crossorigin="anonymous"` at
  externalization time. No placeholder, no rewrite pass.
- **Acceptance:** emitted `<link>`/`<script>` carry correct SRI; the site's
  `test_sri_integrity` passes with the Python SRI step removed.

### B4 — Per-page CSP with inline-script/JSON-LD hashes → native
- **Python:** `inject_jsonld_hashes` / `postbuild.py` computes
  `script-src`/`style-src` `'sha256-…'` for each inline JSON-LD/style and
  writes a per-page CSP (meta + edge headers).
- **Native:** ssg emits the inline JSON-LD; it should hash each inline
  script/style it emits and produce a per-page CSP (as a `<meta
  http-equiv>` and/or a sidecar `_headers`/JSON for the edge router).
- **Config:** a CSP policy template with a `{hashes}` slot; algorithm
  (sha256).
- **Acceptance:** `test_csp_strict` passes with the Python CSP step removed;
  hash-strict CSP verified.

### B5 — Asset fingerprinting (content hashing) → native
- **Python:** `postbuild_assets.py` stamps `name.<contenthash>.ext` and
  rewrites references.
- **Native:** standard SSG fingerprinting — hash emitted assets, rename,
  rewrite references in HTML/CSS. Long-cache-safe by default.
- **Config:** `[assets] fingerprint = ["js","css","svg",…]`.
- **Acceptance:** fingerprinted filenames + rewritten refs; no dangling
  references (the site's build-smoke check for `main.<hash>.js` passes).

### B6 — Image width/height stamping (CLS) → native
- **Python:** `postbuild.py` stamps `width`/`height` on `<img>`.
- **Native:** for local/known assets, read intrinsic dimensions and stamp
  them. For remote CDN images, extend mdx-gen's image syntax to carry
  explicit dims (mdx-gen already supports `![alt](url).class="…"`; add
  `.width=…&height=…` or an attributes form).
- **Acceptance:** all content `<img>` have width/height; Lighthouse CLS
  unaffected with the Python step removed.

### B7 — LCP preload → native
- **Python:** `inject_lcp_preload` adds `<link rel=preload as=image>` for
  the hero/banner.
- **Native:** ssg adds a preload for the front-matter `banner`/`image`
  (fetchpriority=high) automatically.
- **Acceptance:** hero preload present; Lighthouse LCP unaffected.

### B8 — OpenGraph / Twitter / structured data → consolidate native
- **Python:** og/twitter injection in `postbuild.py`.
- **Native (mostly exists):** ssg already emits og/twitter/JSON-LD.
  Make **all** fields derive from base front matter so posts don't
  duplicate them: `twitter_title` ⇐ `seo_title`⇐`title`;
  `og_image`/`twitter_image` ⇐ `banner`/`image`; `twitter_description` ⇐
  `description`. (This also prevents the class of bug where a re-templated
  post carried a stale `twitter_title` from the source article.)
- **Acceptance:** a post with only `title`/`description`/`banner` gets
  complete, correct og/twitter/JSON-LD with no per-field front matter.

### B9 — Breadcrumbs → native
- **Python:** breadcrumb markup + JSON-LD in `postbuild.py`.
- **Native:** derive `BreadcrumbList` + markup from the URL path segments
  and each segment's title.
- **Acceptance:** breadcrumbs match the URL hierarchy; JSON-LD validates.

### B10 — Feeds & discovery outputs → native (extend existing)
- **Python:** none major, but the site emits `llms.txt`, `llms-full.txt`,
  `/api/agents/…`, `search-index.json`, RSS/Atom/news-sitemap.
- **Native:** ssg already emits RSS + sitemap; extend to: Atom, JSON Feed,
  **news sitemap** (fixing A4), `llms.txt`/`llms-full.txt`, a
  `search-index.json` (title/url/excerpt/locale/tags per page), and an
  optional versioned content API (`/api/v1/*.json`) — all as collection
  queries. `robots.txt`, `sitemap.xml`, `sitemap-index.xml`.
- **Acceptance:** these files are produced by ssg with no Python; feeds
  validate; search index drives the site's client-side search.

### B11 — Taxonomy pages (tags / topics / tag-landings) → native (extend existing)
- **Python:** `scripts/generators/build_tags.py`, `build_topics.py`,
  `build_tag_landings.py`.
- **Native:** ssg has `generate_tags_html`; generalise to a taxonomy engine:
  for each taxonomy (`tags`, `topics`, …) emit a hub page + per-term pages
  listing member posts, from front-matter terms + a taxonomy config (term
  metadata, pillar grouping).
- **Config:** `[[taxonomy]] name="topics" template="…" terms_from="keywords"`.
- **Acceptance:** tag/topic/landing pages generated natively; the curated
  `TOPICS` map (currently Python) expressed as taxonomy config/data.

### B12 — Listing / index pages + pagination → native
- **Python:** `scripts/generators/build_listings.py` (the `/articles/`
  index with pagination), `build_case_studies.py`.
- **Native:** a collection/listing page type with sort, filter, and
  pagination (`page/2/` etc.) over the content collection.
- **Config:** `[[collection]] path="/articles/" source="_posts"
  sort="date desc" per_page=12`.
- **Acceptance:** `/articles/` + pagination generated natively; matches
  current output.

### B13 — Homepage "recent posts" grid → native query
- **Python:** `scripts/postbuild/regen_homepage.py` rewrites the 6-card
  grid from the most recent EN posts (mutates `index.md`).
- **Native:** a template query `collection.posts | recent(6)` the homepage
  template iterates — no source mutation, no regen script, no build-time
  footgun.
- **Acceptance:** homepage shows the latest N posts without editing
  `index.md`.

### B14 — Article furniture: related posts, reading time, review date → native helpers
- **Python:** `scripts/postbuild/post_enrich.py` injects lead aside,
  related posts, review date, key takeaways.
- **Native:** provide template helpers/collection queries: `related(post,
  n)` (by shared tags/topics), `reading_time(body)`, and expose
  `last_reviewed`/`last_build_date`. Keep genuinely editorial furniture
  (hand-curated lead copy) in the site, but the derived bits become native.
- **Acceptance:** related-posts/reading-time render from templates with no
  Python enrichment.

### B15 — Minification → native (verify complete)
- ssg already minifies HTML/CSS/JS. Confirm coverage so no Python minify
  remains. Ensure minification is deterministic (A7).

### B16 — Sigstore / SBOM / accessibility reports → keep or native-optional
- The site emits `sbom.cdx.json`, `accessibility-report.json`,
  `wcag-compliance.json`, Sigstore bundles. ssg already emits some
  accessibility artifacts; SBOM + Sigstore signing can stay in the site's
  CI (they're supply-chain, not rendering). Optional: a native
  accessibility-report emitter consolidated with the pa11y gate.

---

## Suggested delivery order

**P0 (unblocks correct local builds + the 0.0.46 pin):**
A1 (markdown stack + `allow_unsafe_html`), A2 (permalink fallback / never
hard-fail), A7 (cross-platform determinism + macOS CI).

**P1 (removes the biggest Python surfaces):**
A3–A5 (structured-data/title, date parsing, inLanguage), A8 (table-align
`align=` → CSS, WCAG H49), B1 (permalink), B3–B4 (SRI + CSP), B2 (i18n
routing), B8 (og/twitter/JSON-LD from base FM).

**P2 (collection-model features):**
B5–B7 (image dims, preload), B9 (breadcrumbs), B10 (feeds/search/api),
B11–B13 (taxonomy, listings, recent), B14 (related/reading-time), A6, B15.

**End state:** `build.sh` collapses toward `ssg build`, with the site
retaining only genuinely editorial steps (translation authoring, hand-lead
copy) and supply-chain steps (SBOM/Sigstore). Every fix lands with a test,
and ssg's CI runs the render + reproducibility suite on macOS **and** Linux.
