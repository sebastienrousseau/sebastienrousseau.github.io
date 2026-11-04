<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Changelog

All notable changes to this repository (schema, build pipeline, security, accessibility, and crawler-facing surface) are recorded here.

This site follows [Semantic Versioning](https://semver.org/) in a `0.0.x` series (incrementing strictly by `0.0.1` from `v0.0.1`) for the **build pipeline + schema graph**; content (articles, translations) lands continuously between tags and is not versioned here. Editorial revision history per article lives in each post's `last_reviewed` frontmatter field.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [0.0.31] - Unreleased

### Changed

- **One column system across every template**: the shared stylesheet in all 12 `_layouts/*.html` now defines three column widths and one fluid gutter: `--col-wide` (75rem, 1200px), `--col-read` (43.25rem, 692px) for long-form text, and `--col-mid` (60rem, 960px) as the single intermediate width, used only for centred display headings and centred hero copy that need more than the reading measure. `--gutter` runs from 20px at a 390px viewport to 60px at 1440px and is 80px from 1920px; `--frame-wide` is the wide column plus both gutters, for containers that pad themselves. `--pad-x`, `--max` and `--max-wide` stay as aliases. Ad-hoc container widths (760px, 1100px, 1120px, 1180px, 1200px, 1400px, 1440px, 640 to 1080px) now resolve to these tokens; component widths (forms, the hero clock stage, `ch` text measures) are unchanged. The nav, the H1 and the main column of every left-aligned template (home, `/iso20022-mcp/`, `/speaking/`, `/trust/`, `/case-studies/`, `/topics/`, `/articles/`, tag landings) now share one content edge: 20px at 390px, 54px at 1280px, 120px at 1440px and 928px at 3056px, where the edges were 22px to 340px apart before. Centred heroes (articles, `/about/`, `/research/`, `/library/`, `/suite/`, `/projects/`, `/contact/`, `/privacy/`, `/playlists/`) stay centred on the same axis. `/about/`, `/contact/`, `/playlists/`, `/articles/` and tag landings move from the 760px column to the wide column; articles and `/privacy/` use the 692px reading column. `/speaking/` and `/iso20022-mcp/` bands now run full width. The page CSS for `/speaking/`, `/iso20022-mcp/`, `/trust/`, `/contact/` and `/playlists/` changed at its source in `scripts/generators/gen_layouts.py`, and the other 11 layouts were regenerated from `_layouts/index.html`, so all 12 carry a byte-identical shared block. No `!important` was added and no colour changed. The visual-regression baselines in `.github/ci-tools/visual/baseline/` were refreshed on purpose.

## [0.0.30] - Unreleased

SEO recovery after the 11 Sep 2026 site-wide quality demotion (Google impressions down 98%). Technical fixes plus the locale cut the owner approved.

### Changed

- **10 locales stay indexable, 24 go `noindex`**: `_data/seo/locale-indexing.json` is the one place that lists the locales search engines may index: English plus `zh-hans`, `zh-hant`, `fr`, `ko`, `es`, `ru`, `ja`, `it`, `cs` and `de` (the top ten by Google impressions, 1 Jun to 10 Sep 2026). Every page of the other 24 active locales now carries one merged `<meta name="robots" content="noindex, follow, ...">`, emits no hreflang links, and is gone from `sitemap.xml`; no page anywhere emits an hreflang alternate for them. The pages stay live and the language switcher still links each one to the translation of the current page. New pass: `scripts/postbuild/finalize_seo.py` with `postbuild_lib/locale_indexing.py`, run after `fix_lang_switcher.py`. `sitemap.xml` drops from 7,679 to 2,423 URLs (233 English + 10 x 219).
- **HTML is cached at the Cloudflare edge for 10 minutes**: the lang-router Worker fetches page navigations with `cf.cacheEverything` and `cacheTtlByStatus` (200 for 600 s, every other status not stored), so a crawler burst no longer reaches GitHub Pages, which answered 30 of 40 parallel requests with HTTP 429. 600 s matches GitHub Pages' own `max-age=600`, so no purge-on-deploy step is needed. Locale redirects are decided before any origin fetch and are never cached; browsers still get `max-age=0, must-revalidate`. Code in the new `workers/edge-routes.js`, covered at 100% with `lang-router.js`.

### Fixed

- **Renamed locale URLs answer one 301**: the 3,170 meta-refresh stub pages left by the ADR-0012 slug localisation (Search Console: 3,804 "Page with redirect") are now answered by the Worker with a single-hop 301 to the final URL, from `worker-assets/redirects.json`. `scripts/build_worker_assets.py` derives that map from the built stubs, collapses chains and rejects loops or off-site targets. The stubs are still built as a fallback for when the Worker or its assets binding is unavailable.
- **Real sitemap `<lastmod>`**: 3,795 of 7,679 URLs shared `2026-05-11`. Each URL now carries its source front-matter date (`last_reviewed`, then `last_build_date`, then `date`; a translation shares its English source's date), or for a listing page the newest date among the articles it links to, or no `<lastmod>` at all. Never the pinned build date. The largest single date now covers 14.5% of URLs (352 of 2,423), and every one of them is dated by its own front matter (31 articles reviewed on 2026-05-11, in 11 languages) or by an article it lists. A gate fails if any date covering more than 5% of URLs includes one that has neither source.
- **Unique titles and descriptions**: paginated listings get their localised "Page N of M" label, listing pages get the site name and lead their description with their own title, values shared across locales get the locale's native name, and values shared within a locale get the publication date or slug. Duplicate titles among indexable pages: 85 groups (287 pages) to 0; duplicate descriptions: 74 groups (2,265 pages) to 0.

### Added

- **Build-output gates** (`tests/unit/test_seo_recovery_output.py`): every noindex-locale page is `noindex`, no indexed page is (bar utility pages and stubs), at most one robots meta per page, the sitemap lists exactly the indexed locales, no hreflang targets a noindex locale, titles and descriptions are unique, no lastmod date over 5% of URLs includes an unsourced one, and every stub is in the Worker redirect map with no chains, loops or dead targets.

## [0.0.28] - Unreleased

### Security

- **pdf-render outbound URL guard (CodeQL #87, py/partial-ssrf)**: `fly/pdf-render/app.py` builds the article path in a new `_article_path` helper that checks `slug` and `lang` with separate `fullmatch` guards, each dominating every use of its value. The previous combined `or` guard let `lang` reach the URL unchecked on its falsy branch, which CodeQL reported. Valid and invalid inputs give the same URLs and the same 400s as before.

### Fixed

- **pa11y retries a page-load timeout once before failing**: `scripts/seo_and_audit/pa11y_run_shard.py` exited 0 when pages had issues and failed only on a wedged or crashed browser, so the shard step never ran `pa11y_retry_flakes.py` and a single "Navigation timeout" went straight to the merge gate. That is how the post-merge run of #515 on main failed on one Polish article that loads in 0.7 s live. The runner now exits 1 when any page has issues, as `pa11y-ci` does: a timeout is re-audited once and cleared from the shard report if it passes, and a real violation, or a second timeout, still fails the shard.
- **pa11y merge gate checks every shard**: the "Merge pa11y, Lighthouse, deploy" job downloaded the shard reports with `merge-multiple: true`, and every shard writes `pa11y.shard.json`, so the last download overwrote the rest and the gate checked one random shard. It now downloads one directory per shard, sums every report, and prints per-shard and total URL and error counts.
- **`/iso20022-mcp/` simulator fallback contrast in dark mode**: once `<iso20022-simulator>` attaches its shadow root it now removes the light-DOM fallback paragraph. With no `<slot>` the paragraph stopped rendering but kept the initial black text, which the dark-mode pa11y sweep measured at 1.07:1 against the 7:1 WCAG2AAA floor. Without JavaScript the paragraph still shows, at 13.3:1 (dark) and 11.4:1 (light).

### Removed

- **Server-side PDF rendering**: the article "Save PDF" control is now a `data-print` button that opens the browser print dialog, and the `@media print` stylesheet lays the article out for "Save as PDF". It was a link to `/api/pdf/<slug>.pdf`, proxied by `workers/pdf-proxy.js` to a WeasyPrint service on Fly.io that was never deployed under an app this site owns: the live route hung for over 20 s before `main.js` fell back to the same print dialog. Removed `fly/pdf-render/`, `workers/pdf-proxy.js` and their tests, the `/api/pdf/` Worker route and its link-audit exemptions, and the `PDF_RENDER_BASE` and `PDF_ORIGIN_TOKEN` Worker settings. The action rail no longer needs a canonical URL, which it only read to build the PDF link. Old `/api/pdf/` URLs answer 404 once the Worker is redeployed.

### Changed

- **Dependencies (#514)**: `ruff` 0.17.3, `mypy` 2.4.1, `types-PyYAML` 6.0.12.20261030, `cyclonedx-bom` 7.6.0 and `pytest` >=9.2.0 in `requirements-dev.txt`, with `requirements-dev.lock` regenerated so the lock-agreement gate passes.

## [0.0.27] - Unreleased

### Fixed

- **External link audit separates bot blocks from link rot (#510)**: `scripts/seo_and_audit/audit_links.py` now classifies each result. A 401, 403 or 429, or a dropped connection (`RemoteDisconnected`, `ConnectionResetError`), is listed as unverifiable under a `  ? [` prefix and no longer counts toward the monthly tracking issue; 404, 410, other 4xx, 5xx, timeouts and DNS failures stay broken. A `URLError` is labelled with its cause (`URLError(gaierror)`) so a DNS failure and a reset can be told apart. The "summarise with AI" prompt links (`chatgpt.com/?q=`, `claude.ai/new?q=`, `perplexity.ai/search/new?q=`) are skipped as share endpoints. Nine of the ten links in #510 were bot blocks; the tenth, the `treasurers.org` 404, was repointed to its Wayback snapshot in 0.0.26.
- **Fly.io app name**: `fly/pdf-render/fly.toml` names `sebastienrousseau-pdf-render`, the app the deploy handover creates, instead of `pdf-render`, which belongs to another account.

## [0.0.26] - Unreleased

### Added

- **Four October 2026 articles across 35 languages ([#509])**: published `2026-10-24-an-ai-s-attack-on-progression-free-sets-a-ledger-of-what-stalled`, `2026-10-25-agentic-ai-breaks-the-assumption-behind-every-task-exposure-forecast`, `2026-10-26-mystery-seeds-behind-nist-curves-were-never-hashes-claude`, and `2026-10-28-why-the-fca-is-regulating-ai-without-an-ai-rulebook`, together with all 136 localised editions across 34 non-English locales, updated topic clusters, and romanisation lexicon entries for `ja`, `zh-hans`, and `zh-hant`.
- **ISO 20022 MCP Suite architecture matrix, 2027 FAQ, and structured data ([#509])**: expanded `/iso20022-mcp/` with a 9-server architecture and clearing rail matrix (documenting the 7-meta-tool gateway pattern and ~94% token reduction), a 6-question accordion on 2026-2027 SWIFT CBPR+ structured/hybrid postal addresses (`TwnNm`, `Ctry`, `AdrLine`) and November 2027 E&I (`camt.056`/`camt.029`), and `SoftwareApplication` + `FAQPage` JSON-LD; added OpenAI Codex CLI, `streamable-http`, all 9 server CLI invocations, and the structured address repair recipe across `/suite/`, `/iso20022-mcp-docs/`, and `/iso20022-mcp-recipes/`.

### Changed

- **Dependencies ([#507], [#508])**: `ruff` 0.17.1 to 0.17.2 in `requirements-dev.txt`, with `requirements-dev.lock` regenerated so the lock-agreement gate passes; `actions/setup-python` 7.0.0 to 7.1.0 across seven workflows; and `github/codeql-action` 4.39.0 to 4.39.1 in the CodeQL and Scorecard workflows.

### Fixed

- **Landscape-only article banners ([#509])**: `scripts/editorial/pick_banner.py` now parses `VP8`, `VP8L`, and `VP8X` WebP dimensions and excludes portrait and square assets (`width <= height`) during inventory collection; replaced seven portrait stock banners across English and all 34 locale editions with `2584x1597` landscape photographs.
- **Social card metadata on `story` and `page` layouts ([#509])**: `story.html` now emits `<meta name="banner-src" content="{{banner}}" />` so `/iso20022-mcp-docs/`, `/iso20022-mcp-reference/`, and `/iso20022-mcp-recipes/` publish full-bleed raster `og:image` / `twitter:image` cards instead of share-button icon fallbacks, and `postbuild_lib.seo.clean_meta_description` repairs truncated body scrapes on non-BlogPosting `og:description` and `twitter:description` tags.
- **WeasyPrint PDF subresource SSRF guard, size cap, and asset cache ([#509])**: `fly/pdf-render/app.py` now supplies a custom `safe_url_fetcher` to WeasyPrint that enforces HTTPS-only allowlisted hosts (`sebastienrousseau.com`, `www.sebastienrousseau.com`, `cdn.cloudcdn.pro`), caps subresource payloads at 10 MiB (`MAX_ASSET_BYTES`), caches immutable `/fonts/*` and `/_csp/*` assets in memory, and supports optional `X-Origin-Verify` token authentication, backed by hermetic unit tests in `tests/unit/test_pdf_render.py`.
- **Edge API security headers and ASN denylist cleanup ([#509])**: `workers/lang-router.js` wraps early-return API responses (`tryActivityPub`, `tryMCP`, `tryPDF`, and `tryClock`) with `withApiSecurityHeaders` (`Strict-Transport-Security`, `X-Content-Type-Options: nosniff`, `Referrer-Policy`, `Permissions-Policy`, `Cross-Origin-Opener-Policy`, and a sandboxed `Content-Security-Policy`), and `workers/security.js` removes the duplicate `16276` ASN entry.
- **Agent API canonical URLs, provenance digests, and postbuild ordering ([#509])**: `scripts/generators/build_agent_api.py` now emits canonical trailing-slash URLs (`https://sebastienrousseau.com/<stem>/` and `https://sebastienrousseau.com/about/`) instead of `/index.html`, includes deterministic `content_sha256` source digests and `sigstore_bundle` URLs on every post entry, and runs immediately after `postbuild.py` in `build.sh` so `word_count` is populated on clean builds.
- **MCP `server_info` discovery, PDF proxy origin token, and parallel JSON-LD audit ([#509])**: `workers/mcp.js` adds `GET /mcp/v1/server_info` exposing MCP protocol version `2025-06-18`, capabilities, and tool descriptors; `workers/pdf-proxy.js` forwards `X-Origin-Verify` when configured; `scripts/seo_and_audit/validate_jsonld.py` adds `--jobs` (`-j`) parallel validation via `ThreadPoolExecutor`; and `_layouts/main.js` scopes homepage lens title/description overrides to `#home-content` while keeping `#mcp-faq` anchored at the tail of `/iso20022-mcp/`.
- **`/api/pdf/*` no longer hangs into a 502**: Search Console reported 678 PDF URLs as 5xx. The Worker proxied to a hard-coded `https://pdf-render.fly.dev`, which does not run `fly/pdf-render` (it answers `/healthz` with an empty 204 and Node `helmet` headers, and never answers a `/render` GET), so each request waited about 60 s for the edge to give up. `workers/pdf-proxy.js` now reads the renderer from the `PDF_RENDER_BASE` Worker variable (503 at once when unset), aborts the upstream fetch after 10 s with a 504, and sends `X-Robots-Tag: noindex, nofollow` on every PDF response. The Save PDF link is `rel="nofollow"` instead of `rel="alternate"`, and carries the locale (`/api/pdf/<lang>/<slug>.pdf`), which `fly/pdf-render/app.py` now accepts as `lang=`; before, every translated article's PDF would have 404ed because its slug only exists under its locale prefix.
- **Sitemaps list only indexable URLs; utility pages are `noindex`**: the root sitemap listed all 34 locale `/404/` pages and every locale `offline` / `thanks` fork, because the exclusion list only named the EN and FR paths, and ssg stamps every page with a robots meta that lacks `noindex`, so `/404/` and its forks answer 200 as indexable pages (5 Soft 404s in Search Console). New `postbuild_lib/indexability.py` sets `noindex, follow` on the 404, offline and thanks pages of every locale, then prunes every sitemap entry that does not render, is a redirect page, is `noindex`, or canonicalises elsewhere. `tests/validation/test_sitemap_indexable.py` gates it in `build.sh`.
- **Redirects for crawled dead URLs**: the Worker 301s a doubled locale prefix (`/nl/th/<slug>/`, `/zh-hant/zh-hant/<slug>`), left in Google's crawl queue by the rewriter bug fixed in #464, to the second locale with the trailing slash added. `_data/redirects/articles.json` adds `/2018-01-09-undpasanding-the-technology-behind-blockchain/`, `/sv/gjord-med-statisk-sajtgenerator/` and `/id/dibuat-dengan-generator-situs-statis/`. `/2026-05-29-fhe-banking-analytics-confidential-compute-2026` stays a 404: that article was never published. `postbuild_lib.internal_links.canonicalise_absolute_self_links` now adds the trailing slash to locale article links too (`…/he/2026-06-07-<slug>`), which it skipped, so every locale article's related-reading links each cost a 301.
- **Dead citation and CodeQL notes**: the `treasurers.org` May 2026 payments-landscape post (404, issue #510) is repointed to its Internet Archive snapshot in 140 posts, and `tests/unit/test_postbuild_assets.py` no longer imports `postbuild_assets` both ways (CodeQL `py/import-and-import-from`, 4 alerts).
- **Advisories in the CI tooling locks**: `msgpack` 1.2.1 to 1.2.3 in `requirements-dev.lock` (CVE-2026-114613) and `qs` 6.16.0 to 6.17.0 in `.github/ci-tools/lighthouse/package-lock.json` (GHSA-6pq8-jhm2-2vcw, via `overrides`). Both `pip-audit` and `npm audit` report 0 vulnerabilities across all lockfiles.

---

## [0.0.25] - 2026-10-27

### Added

- **`--rederive-slugs` redirects live URLs ([#506])**: the 10 articles published from 2026-09-15 to 2026-10-13 are live in 34 locales with English bodies and titles, so translating them renames 340 locale URLs. ADR-0012 makes each such rename an individually redirected change, so when the old locale post exists on `origin/main` the step now adds `old -> new` to `_data/redirects/articles.json` and retargets any redirect that pointed at the old slug, so no chain forms. A stub that was never published is renamed without a redirect.

### Fixed

- **No layout shift when the "Read as" control appears ([#506])**: the control ships `hidden` and `main.js` reveals it once its buttons are wired, about 300 ms after navigation. On desktop it sits inside the first view, so the reveal moved the content below it by 18 px, a cumulative layout shift of 0.0032 on the home page. With scripting enabled its space is now held, invisible, from the first paint; with JavaScript off it stays hidden as before.
- **The home page headline is measurable at any time of day ([#506])**: each badge on the hero clock held every value as a column of labels (61 for the minutes, 13 for the hours), clipped to the badge. The clip hides the column from view but not from layout, so at some angles the minute hand's box reached over the headline, where axe could not measure its contrast: the page's accessibility check passed or failed by the time of day. Each drum now holds two labels, the value shown and the next, and the clock renders pixel-identical.
- **Numbered lists render as lists in bn, mr and fa ([#506])**: 10 posts had their ordered-list markers converted to native digits (`১.`, `१.`, `۱.`). CommonMark opens a list only on ASCII digits, so each list rendered as one paragraph starting with the marker. The markers are ASCII again, and the pipeline-artefacts gate now fails on a native-digit marker.
- **No links to English articles that never existed ([#506])**: 384 links in 169 posts named five English slugs no post ever had (a guessed `-vs-` slug for the humanoid robotics article, a misspelt Kyber slug, two invented slugs and a Polish slug without its `/pl/` prefix), and each served a 404. They now name the real article, the Polish post's own URL fields carry `/pl/`, and the URL-integrity gate fails on any link to an English article that is neither a post nor a redirected retired slug.

---

## [0.0.24] - 2026-10-24

### Added

- **`translate_post.py <slug> --rederive-slugs` ([#504])**: locale stubs are named from the English title, and translating the title left the file name behind, so `test_slug_derivable` failed every translated copy. The new step derives each locale's slug from its translated title, renames the post, rewrites its `url`, `permalink` and `id`, and updates `slugs.json`. A title that derives no slug is reported, so the romanisation lexicon can be extended; `romanisation-lexicon.json` gains 45 words for Japanese, Chinese, Thai, Arabic and Hebrew titles. `publish-today.md` runs it as step 6c.

### Fixed

- **Furniture labels in locale stubs ([#504])**: `translate_post.py` copied the English body into each stub, so the post-lead and author-card `aria-label`s stayed in English and `test_i18n_labels` failed the build. Stubs now take each locale's `labels.json` values when they are written.
- **`pick_banner.py` follows the live CDN layout ([#504])**: its default inventory pointed at `Code/Public/CDN/cloudcdn.pro`, which no longer exists, and it printed `/api/transform` URLs, which have answered 401 since that endpoint closed on 2026-06-23. The inventory now defaults to the `cloudcdn.pro` checkout beside this one (`CDN_INVENTORY` still overrides it), the picker prints the direct `/stocks/images/` URL, and the `-320`/`-640`/`-1200`/`-1920` size variants are no longer offered as banners. `--width` and `--quality` are gone with the transform URL. `publish-today.md`, `docs/publishing.md` and `docs/i18n.md` now give the same path and URL rule and count 35 languages (34 locales), not 28.
- **`CITATION.cff` release date**: `date-released` still read 2026-10-15 (0.0.21); it now reads 2026-10-24, the date 0.0.22 and 0.0.23 were released.

---

## [0.0.23] - 2026-10-24

### Changed

- **Shared postbuild names made public ([#503])**: `article_furniture.py` defined 19 module-level regexes and helpers that only other `postbuild_lib` modules use, all with a leading underscore. CodeQL's `py/unused-global-variable` reported each one and stayed quiet only through dismissed false positives, so any edit to one of their lines re-raised an alert (as with #286). They are now public names in the definitions and every import (`_csp_tag_re` becomes `CSP_TAG_RE`). No behaviour changes; CodeQL's query on `scripts/postbuild` goes from 19 findings to 0.

### Fixed

- **Advisories in the Python locks ([#503])**: `pip-audit` flagged packages in two hash-pinned locks, each fixed by moving only the affected package to its patched release (`uv pip compile -P`, the command `scripts/security/lock-deps.sh` runs). In `requirements-dev.lock` (CI tooling): `certifi` 2026.6.17 to 2026.10.23 (a revoked eMudhra root, GHSA-6q48-6c7w-9gw2), `filelock` 3.29.4 to 4.2.4 (three lock-file advisories) and `urllib3` 2.7.0 to 2.8.0 (three). In `fly/pdf-render/requirements.lock` (the PDF service): `pillow` 12.3.0 to 13.0.0 (37 decoder and parser advisories; 13.0.0 is the first fixed release), `brotli` 1.2.0 to 1.2.1 (two decoder out-of-bounds writes, CVE-2026-111497 and GHSA-9v8h-qqgm-4m35), `werkzeug` 3.1.8 to 3.1.9 (`safe_join`, GHSA-g6x2-hccm-hh4m), and the same `certifi` and `urllib3`. Both locks install with `--require-hashes` and audit clean; WeasyPrint 70 renders a PDF with an embedded image under Pillow 13.

---

## [0.0.22] - 2026-10-24

### Changed

- **Homepage 10/10 design and editorial overhaul ([#496])**: Replaces the hero lead with a clear executive credential band, restores the six institution brand logos (`HSBC`, `PayPal`, `Barclays`, `Shazam`, `AKQA`, `Virgin`), promotes three flagship production repositories (`Static Site Generator`, `Pain001`, `ISO 20022 Rust Ecosystem`) into proof cards, consolidates the three domain pillars into scannable cards, and translates the updated structure across all 34 non-English locales.
- **Layouts re-synchronised with the `ssg-themes` theme (`make theme-sync`, ADR-0014)**: Brings the theme's gallery-gate work back to the site. A first view paints in the metric-matched system faces and no webfont sits on the path to first paint: `main.js` fetches the webfonts after `load`, and `theme-init.js` switches to them on later views (`font-display: optional`, no swap). Also AAA contrast on the playlist hero (opaque text tints and a scrim), wider reference-table labels, `prose` on page bodies (1.5-line paragraph spacing, WCAG 1.4.8, for running text only: classed component paragraphs such as a card's date line keep their spacing), and explicit dimensions on the story hero image.
- **Webfonts trimmed to their declared weights**: The eight WOFF2 files drop unused variable-axis ranges, 569 KB to 387 KB in total (`newsreader-latin.woff2` 131,848 to 95,032 bytes).
- **Client logos served at display size**: The six homepage and About logos come from `/_csp/logo-*.webp` at 190 x 64 (2 to 8 KB each) instead of the CDN originals (80 to 547 KB each, about 1.5 MB together), and the homepage rail loads them lazily.
- **Dependencies ([#497], [#498])**: `ruff` 0.17.0 to 0.17.1, with `requirements-dev.lock` regenerated by `scripts/security/lock-deps.sh` (the Dependabot PR changed only `requirements-dev.txt`, so the lock-agreement test failed), and `github/codeql-action` 4.38.3 to 4.39.0 in the CodeQL and Scorecard workflows.

### Fixed

- **English on translated pages is marked as English (WCAG 3.1.2)**: Up to `ssg 0.0.68` every Markdown body sat in `<div lang="en">`, which declared every body on 646 locale pages English, translated or not. `ssg 0.0.69` drops that wrapper, which left the parts still in English (the tags page, topic-page article cards and headings, a few homepage strings) declared in the page's language. `scripts/postbuild/mark_untranslated_english.py` now gives `lang="en"` to every text node of three or more words, inside `<main>` of a translated page, that appears verbatim on an English page. On the CI build of the merged branch that is 90,887 text nodes on 5,811 pages; the 2,792 retired-article redirect pages that `postbuild.py` copies from their targets afterwards carry the same marks. Topic-page tag eyebrows ("AI · Research · Innovation") are built from tag names that appear on no English page, so they stay unmarked.
- **Homepage frontmatter ampersand encoding ([#496])**: Uses literal `&` instead of `&amp;` in `_posts/index.md` `item_title` and `apple-mobile-web-app-title` so `ssg 0.0.68` does not emit double-encoded `&amp;amp;` in `<meta name="apple-mobile-web-app-title">` across the 35 homepage editions.
- **First visits loaded the page twice**: The service worker claims the page on its first install, which fires `controllerchange`, and `main.js` reloaded on every such event. It now reloads only when a worker replaces an earlier one. Mobile Lighthouse on the homepage moves from 0.81 to 0.91 to 1.0 in four runs of five.
- **Client logos in dark mode**: The rail took the light surface while each tile stayed dark, so the gaps showed as white bars and dark wordmarks sat on dark tiles. Each tile now takes the light surface, Barclays and Virgin are darkened to match the other wordmarks, and on phones the tiles keep room for the image (a 22 px height under 18 px of padding left none).
- **Multi-line links in grid rows**: Links inside `main.prose` text are inline blocks (so a wrapped link never overlaps the line below), and an inline block's baseline is its last line. In the /trust/ records the title link wraps to three lines, and the row's baseline alignment pushed the organisation, date and role 44 px down to that last line. The links now align to the top of their line, so a row aligns on the title's first line.
- **Card grids squeezed to text width**: `main.content ol, ul` take the article measure (`--measure-article`), which also caught two card grids: the four steps on /iso20022-mcp/ and the migration cards on /iso20022-mcp-docs/ sat in about 665 px of a 1,120 px column, and words broke mid-word ("Submissio n", "co nvert_mt942"). Both grids now take the full width; plain lists keep the measure.
- **Fallback faces matched to the webfonts**: A first view now paints in the fallback faces, so their widths show. `Newsreader Fallback` (Georgia) was set at 104%, which made headings 4 to 6% wider than Newsreader; measured on the site's 192 Newsreader headings it is now 99%. `JetBrains Mono Fallback` named `local('Menlo')`, which Chrome does not resolve, so the face never loaded; it now names `Menlo Regular` and `Menlo-Regular`.
- **Legacy CDN paths for the static site generator**: The brand rename from Shokunin rewrote the project's CDN codename `shokunin` in the postbuild URL fixer to `Static Site Generator`, which no path can match, so `/shokunin/images/...` URLs were no longer moved to `/clients/shokunin/v1/...`. Two unit tests failed whenever the per-process string hash put that entry first in the set.
- **Homepage on phones and against the theme gallery's gates**: The three links that ask an AI assistant about the work were 42 px tall and are now at least 44 px (WCAG 2.5.5); card title links are at least 44 px wide, where a title as short as "QRC" (/projects/) measured 43 px in the fallback face; the three credential links under the headline each stay on one line, where a wrapped link's box overlapped its neighbour on phones; the AI kicker is 12 px (was 11.5 px); and the audience band above the offer cards keeps its buttons clear of the cards' rounded top edge, which is pulled 18 px up over it and covered the bottom of a focused button at 768 and 900 px (WCAG 2.4.12); the "Get in touch" eyebrow over the closing photograph is a lighter cyan (#9adcff, was #5ac8fa) and measures 7.33:1 where it measured 5.77:1, under AAA's 7:1; and revealed sections and cards end on `filter: none` instead of `blur(0)`, which looks the same but no longer leaves a stacking context that made axe read the offer cards as covered by their own container. The theme gallery's AAA, responsive and pa11y gates found them.
- **Homepage under the first TCP window**: The hero clock's 123 background dots and 74 odometer digits are drawn by `main.js` from the same values instead of shipping as SVG markup, so the homepage is 13.8 KB gzipped rather than 15.3 KB and fits the first TCP window (about 14.6 KB), saving a round trip before first paint. The clock is identical once the script has run; without JavaScript it shows its dial and hands.
- **Advisories in the CI tooling lockfiles**: Dependabot flagged three packages in `.github/ci-tools/`. `zod` before 4.6.6 can exhaust memory validating oversized collections (GHSA-mrhx-c7xc-m3w5, all three tools); `undici` before 6.29.1 (pa11y) and `body-parser` before 1.20.9 (Lighthouse) are patched by raising or adding `overrides`. `zod` comes only through `chromium-bidi`, which no stable release moves off zod 3, so the override takes it across a major: `chromium-bidi` loads only for WebDriver BiDi, and the three tools drive Chrome over CDP, where neither package is loaded. Each tool installs from its new lockfile with `npm audit` at 0 and was run end to end against Chrome.

---

## [0.0.21] - 2026-10-15

### Highlights

- **Live profile clock Worker route and cookie resilience ([#488], [#492])**: Adds `GET /api/clock/hero-<light|dark>.svg` on the Cloudflare Worker and handles undecodable `pref-lang` cookies gracefully instead of returning HTTP 500.
- **`ssg-themes` layout synchronisation and three-state theme control ([#492])**: Synchronises all 12 layouts from `ssg-themes.github.io` (`make theme-sync`, ADR-0014) with a three-state colour-scheme control (`system`, `light`, `dark`), 44 px tap targets, and on-demand Spotify embeds.
- **Documentation consolidation and release version gate ([#493])**: Consolidates `project-docs/` into `docs/`, adds `AGENTS.md`, `DEVELOPMENT.md`, `SUPPORT.md`, and `CITATION.cff`, and enforces version agreement via `scripts/security/verify-release-versions.sh`.

---

## [0.0.20] - 2026-09-03

### Highlights

- **`Apache-2.0 OR MIT` dual licensing and DCO governance ([#442], [#476], [#477], [#478])**: Dual-licenses the repository under `Apache-2.0 OR MIT` with SPDX headers on every source file, adds `GOVERNANCE.md`, `ROADMAP.md`, and `CODE_OF_CONDUCT.md`, and enforces DCO sign-off.
- **100% 34-locale body and slug localisation ([#441], [#445], [#449], [#451], [#454], [#474])**: Empties the body-translation and English-title backlogs across all 34 non-English locales, localises every article URL slug, and restores 128 retired URLs as redirect pages.
- **Schema.org `Dataset` distributions and byte-identical builds ([#458], [#462], [#472], [#479])**: Publishes index articles as `Dataset` entities advertised in `llms.txt`, pins the build clock for reproducible builds, and raises `scripts/` test coverage to 95% (94% floor).

---

## [0.0.19] - 2026-08-21

### Highlights

- **Zero Dependabot alerts and 6-shard `pa11y` CI ([#387], [#408], [#411], [#419])**: Clears all open npm and Python Dependabot advisories across CI tooling and fans `pa11y` out across 6 light shards with per-shard timeouts.
- **178 locale re-translations and canonical internal links ([#400], [#407])**: Re-translates 178 articles into their target locales and canonicalises internal links across all templates and posts.
- **`ssg 0.0.50` drift tracking and full site audit closure ([#425], [#430], [#436])**: Enforces the pinned `ssg` version in CI, derives `robots.txt` sitemaps and article counts from build data, and closes 19 findings from the full site audit.

---

## [0.0.18] - 2026-07-18

### Highlights

- **35-locale expansion ([#363], [#364], [#365], [#367])**: Scaffolds and activates Persian (`fa`), Marathi (`mr`), Tamil (`ta`), Telugu (`te`), Malay (`ms`), Greek (`el`), and Hungarian (`hu`) with self-hosted Noto Sans Tamil and Telugu fonts.
- **Enterprise ISO 20022 MCP hub and interactive simulator ([#374], [#377], [#378], [#379])**: Ships `/mcp/` with a multi-client configuration grid, enterprise trust pack, schema viewer, and interactive ISO 20022 message simulator.
- **0.95 Lighthouse performance gate and 35-locale switcher ([#361], [#380], [#384])**: Promotes the Lighthouse performance threshold to 0.95 and resolves audit-driven localisation, SEO, and accessibility gaps across all 35 locales.

---

## [0.0.17] - 2026-07-08

### Highlights

- **Interactive DX tools ([#338], [#339], [#340], [#341])**: Launches the audience path selector (boards, engineers, regulators), client-side on-site search, `/changelog/` and `/status/` endpoints, and interactive self-assessment index scorecards.
- **Institutional brand pivot (`/speaking/` and `/trust/`) ([#351])**: Adds dedicated `/speaking/` and `/trust/` pages with credential graphs, live KPI metrics, and Apple-Newsroom homepage 'What's new' styling.
- **Formal threat model and structured-data CI gate ([#357], [#358], [#359])**: Adds `CONTRIBUTING.md`, a STRIDE threat model, gzipped Lighthouse CI fixtures, and automated JSON-LD validation across all locales.

---

## [0.0.16] - 2026-07-03

### Highlights

- **`make verify` repository-integrity suite ([#291])**: Chains lint, strict typecheck, build, unit tests, JSON-LD validation, internal link audit, and CycloneDX SBOM generation into a single pre-deploy gate.
- **Modular `postbuild_lib` decomposition (<800 LOC per file)**: Extracts `feeds`, `_i18n`, `hreflang`, `citations`, `sharing`, `navigation`, `content_blocks`, `html_passes`, `postbuild_assets`, and `postbuild_transforms` with comprehensive unit test suites.
- **244 backlog translations across 6 locales ([#294])**: Completes full article body translations across Indonesian, Ukrainian, Bengali, Hausa, Romanian, and Yoruba.

---

## [0.0.15] - 2026-06-30

### Highlights

- **Pinned toolchains and one-command `make bootstrap` ([#261], [#278])**: Pins Python, Node, Rust, and `ssg` toolchains via `mise.toml`, hash-pins all Python and npm lockfiles, and SHA-pins every GitHub Actions workflow.
- **Strict `mypy` typecheck gate and operations runbooks ([#262], [#276])**: Enables `mypy --check-untyped-defs` on the type-clean tier and adds rollback, CI-flake triage, and incident-response runbooks.
- **CodeQL and OpenSSF Scorecard remediation ([#281], [#282], [#286])**: Resolves SSRF, regex sentinel, DOM XSS, and tag-filter CodeQL alerts and scopes CI token permissions per job.

---

## [0.0.14] - 2026-06-21

### Highlights

- **Authority playbook and case studies ([#212], [#213])**: Adds `/case-studies/` with independent evaluation benchmarks, tactile Problem-Approach-Outcome project cards across 27 locales, and expanded 14-cluster `/topics/` taxonomy.
- **4-way matrix-sharded `pa11y` CI with semantic cache ([#224], [#230])**: Normalises CSP hashes in the `pa11y` cache and shards accessibility sweeps across 4 CI runners.
- **Cloudflare Worker KV free-tier policy**: Adds write-coalescing, binding audits, and free-tier quota guards for Cloudflare Worker KV storage.

---

## [0.0.13] - 2026-06-15

### Highlights

- **FT-Professional editorial overhaul ([#201])**: Redesigns article typography, executive summaries, and citation blocks across the publication catalogue.
- **End-to-end Mermaid v10 diagram engine ([#198])**: Supports dark and light themes in all Mermaid diagrams with static hex palette initialisation.
- **`build_translations` package at 100% coverage**: Splits `build_translations.py` into a tested package at 100% coverage, makes `scripts/lib/_frontmatter.py` the canonical frontmatter parser, and adds per-locale PR translation summary comments.

---

## [0.0.12] - 2026-06-07

### Highlights

- **Self-hosted variable fonts and CLS-safe metrics ([#169])**: Self-hosts Inter, Newsreader, and JetBrains Mono with size-adjusted fallback metrics and reads actual `og:image` dimensions to keep CLS below 0.1.
- **ActivityPub actor and PQC key-size WASM lab ([#171], [#172])**: Ships WebFinger, actor, inbox, and outbox endpoints on the Cloudflare Worker and launches the interactive `/labs/pqc-key-sizes/` estimator.
- **`ssg v0.0.40` migration and naming convention linter**: Upgrades the build pipeline to `ssg v0.0.40`, unifies the repository structure, and enforces file and script naming conventions in `make lint`.

---

## [0.0.11] - 2026-06-02

### Highlights

- **Google News `NewsArticle` JSON-LD ([#165])**: Reshapes posts within 48 hours of publication into Google-News-compliant `NewsArticle` nodes linked to `#person` and `#organization`.
- **Editorial standards and accountability page ([#163])**: Launches `/editorial/` with `EditorialPolicy` and `CorrectionsPolicy` schemas, a 5-tier primary-source hierarchy, 48-hour corrections clause, and Sigstore verification instructions.
- **Named typography tokens and idempotent TOC injection ([#162], [#166])**: Introduces `--type-display`, `--type-body`, and `--type-mono` CSS custom properties, makes H2 anchor and TOC injection idempotent, and strips duplicate body H1 headings.

---

## [0.0.10] - 2026-06-01

### Highlights

- **INP-aware Core Web Vitals Lighthouse gates ([#159])**: Enforces `total-blocking-time <= 200 ms`, `largest-contentful-paint <= 2500 ms`, and `cumulative-layout-shift <= 0.1` as hard CI assertions under Lighthouse 12.
- **`/llms-ctx.txt` and per-category `robots.txt` ([#160])**: Adds a compact 80-line LLM context file, groups 30+ `User-agent` rules into five crawler categories in `robots.txt`, and documents the CC BY-4.0 bot policy at `/about/#bot-policy`.
- **Per-article inline language switcher ([#161])**: Renders native-script locale links with `lang`, `hreflang`, `rel="alternate"`, and RTL directionality directly below each article hero.

---

## [0.0.9] - 2026-06-01

### Highlights

- **`Person` and `Organization` entity graph ([#158])**: Adds ORCID `0009-0005-1434-284X`, three `EducationalOccupationalCredential` entries, 12 `DefinedTerm` authority nodes, and a standalone `#organization` node exposed at `/api/agents/organization.json`.
- **`TechArticle` and `ScholarlyArticle` auto-promotion ([#158])**: Upgrades dated research posts citing 6 or more primary-source authority domains (NIST, ISO, BIS, IETF, SWIFT, ECB) to `ScholarlyArticle` with native `citation` arrays.
- **Additive daily publishing and localized switcher SSR**: Auto-regenerates slug maps and homepage cards from `_posts/` on every build and server-renders localised article URLs into the language switcher.

---

## [0.0.8] - 2026-05-19

### Highlights

- **Minified assets and dual-digest SRI**: Minifies JS and CSS assets, preloads the homepage LCP portrait, and emits dual SHA-384 Subresource Integrity digests so Cloudflare Pages newline normalisation never breaks integrity checks.
- **Sigstore cryptographic article signing**: Publishes the repository cosign public key and activates per-article `.sigstore.json` bundle signing across all 46 dated research posts.
- **Privacy-first telemetry and contact forms**: Replaces Google Analytics with Cloudflare Web Analytics and routes contact and newsletter submissions through tracker-safe AJAX endpoints.

---

## [0.0.7] - 2026-05-16

### Highlights

- **28-locale internationalisation**: Expands the language-parametric translation pipeline (`build_translations.py`) from 2 to 28 live locales, including German, Arabic, Hebrew (RTL), Spanish, Simplified and Traditional Chinese, Japanese, Korean, Hindi, and Ukrainian.
- **Modular `postbuild_lib` at 100% test coverage**: Splits the postbuild monolith into focused domain modules (`seo`, `article_furniture`, `output`, `github_stats`) gated at 100% unit test coverage and McCabe complexity B or below.
- **Edge security Worker and AI discovery surfaces**: Adds the Cloudflare `lang-router` Worker, `TechArticle` and `SoftwareSourceCode` schemas, OpenPGP WKD, and curated AI discovery files.

---

## [0.0.6] - 2026-05-14

### Highlights

- **Apple Books-style `/papers/` and redesigned `/projects/`**: Introduces the `/papers/` publication showcase with the Enterprise Payment Automation Architecture (EPAA) white paper and a 5-section `/projects/` catalogue.
- **Automated JSON-LD, XML feed, and strict CSP validators**: Wires Schema.org JSON-LD validation, RSS/Atom/sitemap XML validation, and per-page Content Security Policy gates into the build pipeline.
- **Full French (`fr`) edition**: Ships the complete `/fr/` localised site with 42 translated articles, French URL slugs, localised navigation and footer chrome, and French XML feeds.
- **WCAG AAA contrast and self-hosted Skeletonic CSS**: Self-hosts Skeletonic CSS to eliminate cross-origin render blocking and brings light and dark themes to WCAG AAA (7:1+) contrast.

---

## [0.0.5] - 2024-05-12

### Highlights

- **`RustLogs (RLG)` and `Serde YML`**: Adds open-source project showcases and technical articles for `RustLogs (RLG)` and `Serde YML`.
- **Multimodal LLM (`MM1`) research and `TETRA` playlist**: Publishes research on multimodal LLMs (`MM1`) and adds the curated `TETRA` playlist.
- **`ssg v0.0.27` migration and PDF research archive**: Upgrades the static site compiler to `ssg v0.0.27`, repairs sitemap URL generation, and publishes 26 downloadable PDF research briefings.

---

## [0.0.4] - 2024-03-02

### Highlights

- **Audio Analyser and Àkàndé Voice Assistant**: Launches project pages and technical articles for Audio Analyser (`audioanalyser.co`) and the Àkàndé voice assistant.
- **Project index redesign**: Refactors the `/projects/` showcase UI and responsive card layout.
- **RSS validation and `ssg v0.0.26`**: Fixes RSS feed validation issues, cleans up WAVE accessibility attributes, and migrates the site to `ssg v0.0.26`.

---

## [0.0.3] - 2024-01-16

### Highlights

- **Post-quantum cryptography and Rust libraries**: Adds project pages and technical deep dives for `KyberLib`, `CRYSTALS-Kyber`, `DateTime (DTT)`, and the Quantum Fourier Transform.
- **Banking AI and quantum computing research**: Publishes the 2023 review of AI and quantum computing in banking and integrates Google Gemini LLM coverage.
- **WAVE accessibility and `ssg v0.0.23`**: Resolves WAVE web accessibility evaluation findings, integrates Google reCAPTCHA v2 on the contact flow, and upgrades to `ssg v0.0.23`.

---

## [0.0.2] - 2023-11-05

### Highlights

- **Articles hub and product showcase**: Adds the `/articles/` index, contact and thank-you flows, and product pages for Kaishi, AudioTextPro, and Skeletonic.
- **Hash Library (`HSH`) and `ssg v0.0.20`**: Publishes the quantum-resistant Hash Library (`HSH`) showcase and migrates the build pipeline to `ssg v0.0.20`.
- **Feed, canonical URL, and CSP hardening**: Repairs RSS XML generation, normalises W3C datetime metadata and canonical URLs, and removes inline `eval()` script execution under Content Security Policy.

---

## [0.0.1] - 2023-09-27

### Highlights

- **Initial static site foundation**: Establishes the repository structure, Markdown content pipeline, and custom layouts compiled with `ssg` (`v0.0.18`).
- **Core engineering library articles**: Publishes foundational technical articles on the Common (`CMN`) library, `LibMake` code generation, and password security.
- **Structured data and CSS validation**: Adds Schema.org JSON-LD structured data, metadata timestamps, and W3C CSS validation fixes across all templates.

---

[0.0.26]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/compare/v0.0.25...HEAD
[0.0.25]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/compare/v0.0.24...v0.0.25
[0.0.24]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/compare/v0.0.23...v0.0.24
[0.0.23]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/compare/v0.0.22...v0.0.23
[0.0.22]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/compare/v0.0.21...v0.0.22
[0.0.21]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/releases/tag/v0.0.21
[0.0.20]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/releases/tag/v0.0.20
[0.0.19]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/releases/tag/v0.0.19
[0.0.18]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/releases/tag/v0.0.18
[0.0.17]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/releases/tag/v0.0.17
[0.0.16]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/releases/tag/v0.0.16
[0.0.15]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/releases/tag/v0.0.15
[0.0.14]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/releases/tag/v0.0.14
[0.0.13]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/releases/tag/v0.0.13
[0.0.12]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/releases/tag/v0.0.12
[0.0.11]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/releases/tag/v0.0.11
[0.0.10]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/releases/tag/v0.0.10
[0.0.9]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/releases/tag/v0.0.9
[0.0.8]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/releases/tag/v0.0.8
[0.0.7]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/releases/tag/v0.0.7
[0.0.6]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/releases/tag/v0.0.6
[0.0.5]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/releases/tag/v0.0.5
[0.0.4]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/releases/tag/v0.0.4
[0.0.3]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/releases/tag/v0.0.3
[0.0.2]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/releases/tag/v0.0.2
[0.0.1]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/releases/tag/v0.0.1

[#496]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/496
[#497]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/497
[#498]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/498
[#503]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/503
[#504]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/504
[#506]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/506
[#507]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/507
[#508]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/508
[#509]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/509
[#158]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/158
[#159]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/159
[#160]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/160
[#161]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/161
[#162]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/162
[#163]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/163
[#165]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/165
[#166]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/166
[#169]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/169
[#171]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/171
[#172]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/172
[#198]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/198
[#201]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/201
[#212]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/212
[#213]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/213
[#224]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/224
[#230]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/230
[#261]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/261
[#262]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/262
[#276]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/276
[#278]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/278
[#281]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/281
[#282]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/282
[#286]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/286
[#291]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/291
[#294]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/294
[#338]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/338
[#339]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/339
[#340]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/340
[#341]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/341
[#351]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/351
[#357]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/357
[#358]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/358
[#359]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/359
[#361]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/361
[#363]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/363
[#364]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/364
[#365]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/365
[#367]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/367
[#374]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/374
[#377]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/377
[#378]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/378
[#379]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/379
[#380]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/380
[#384]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/384
[#387]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/387
[#400]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/400
[#407]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/407
[#408]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/408
[#411]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/411
[#419]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/419
[#425]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/425
[#430]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/430
[#436]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/436
[#441]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/441
[#442]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/442
[#445]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/445
[#449]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/449
[#451]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/451
[#454]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/454
[#458]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/458
[#462]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/462
[#472]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/472
[#474]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/474
[#476]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/476
[#477]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/477
[#478]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/478
[#479]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/479
[#488]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/488
[#492]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/492
[#493]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/493
[#504]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/504
[#506]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/506
[#507]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/507
[#508]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/508
[#509]: https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/509
