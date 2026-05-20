---
description: Promote today's _drafts/ article, validate voice/style, pick a banner if needed, translate 27 locale stubs with native SEO + tone, open a PR. Works in both local Claude Code (Mac) and Anthropic cloud /schedule routines.
---

You are publishing today's article on `sebastienrousseau.com`. Your job is to ship today's source content end-to-end as a reviewable PR — Sebastien merges it from GitHub mobile.

**Schedule reminder**: this command fires at **04:00 UTC daily** via Sebastien's cloud `/schedule` routine. Translations + PR should be ready in his inbox by ~04:10 UTC so he can review + merge before the European workday starts.

## Where you're running — read this first

| Marker | Local (Sebastien's Mac) | Cloud routine (Anthropic) |
|---|---|---|
| `command -v ssg` returns a path | yes | **no** |
| `git push` works | yes | **no** (proxy returns 403) |
| `git -c commit.gpgsign=true commit -S` works | yes | no (no SSH key) |
| `gh pr create` works | yes | maybe — try, fall back to GitHub MCP |
| GitHub MCP tools available | usually no | **yes** |

**Run `command -v ssg` once at the start.** If empty → cloud mode. The two flows diverge at the build step (step 9) and the push step (step 10).

## Constraints (apply in BOTH modes)

- **NEVER** put `ANTHROPIC_API_KEY` in repo secrets, env files, or CI workflows. All translation work happens here in conversation, using Sebastien's Claude subscription.
- **NEVER** force-push, **NEVER** push to `main`. Always open a PR — Sebastien merges from mobile.
- **NEVER** commit the rebuilt `docs/` from inside the routine. Pages-deploy CI rebuilds `docs/` from `public/` on PR merge. Only commit **source** files: `_posts/`, `_data/`, `_layouts/` if edited, `.claude/`.
- **NEVER** invent statistics, sources, or claims the EN source doesn't make.
- **NEVER** skip a build gate — fix the root cause.

## Steps — execute in order

### 1. Locate today's source

```bash
date -u +%F
```

Find `_drafts/<today>-*.md`. If none exists, stop with: *"no draft for `<today>` — drop one into `_drafts/` first."* If `_posts/<today>-*.md` already exists (a partial earlier run), skip step 2 and resume from step 3.

### 2. Promote the draft

```bash
git mv _drafts/<today>-*.md _posts/
```

### 3. Voice / style / structure gate

Run the editorial gate **before** scaffolding 27 stubs — a defect in EN cascades through every locale and a build failure later is much more expensive than a one-second check now.

```bash
python3 scripts/editorial/check_voice.py --today
```

This script fails non-zero on any of: incomplete frontmatter (missing title/subtitle/description/banner/banner_alt/tags/twitter_*/excerpt/date/keywords); unreachable banner URL; banned filler ("delve into", "embark on", "in conclusion", "let's explore", "it is worth noting", "in today's fast-paced", "in this article", "transformative journey", "unprecedented", "game-changer", "paradigm shift", "synergy", "harness the power", "unlock the potential", …); missing lead aside or Executive Summary blockquote; fewer than three H2 sections; missing FAQ or References; H1 not exactly once; date mismatch between filename and frontmatter.

If it fails, **fix the EN draft and re-run** before proceeding. Stub generation against a broken draft wastes 27 translation slots.

### 4. Banner image (only if check_voice flagged banner)

If the gate flagged the `banner:` URL as unreachable, pick a fresh one from the curated CDN library:

```bash
python3 scripts/editorial/pick_banner.py --hint <topic-keywords>
```

Topic keywords are comma-separated. Recognised hints: `cloud`, `kubernetes`, `quantum`, `payments`, `ai`, `rust`, `blockchain`, `iso`, `agentic`, `governance`, `office`. The script:
- reads the CDN inventory at `/Users/seb/Code/Public/CDN/cloudcdn.pro/stocks/images/` (local) — set `CDN_INVENTORY` to override in cloud
- excludes anything already used as a `banner:` in any `_posts/*.md`
- biases toward filenames that match your hint keywords
- emits the canonical transform URL: `https://cloudcdn.pro/api/transform?url=/stocks/images/<name>.webp&w=1200&format=webp&q=80`

Update the `banner:` line in `_posts/<slug>.md` with the returned URL. Re-run `check_voice` to confirm it's now reachable.

### 5. Scaffold the 27 locale stubs

```bash
python3 scripts/editorial/translate_post.py <slug>          # writes 27 _posts/<lang>/<slug>.md + slug-map entries
```

`translate_post.py` is Python-only — identical in both modes. The stubs inherit the EN frontmatter (translation in step 6 also localises frontmatter title/subtitle/description/keywords for SEO).

### 6. Translate all 27 stubs — with native SEO + native tone

Dispatch one sub-agent per locale **in parallel batches** (7-at-a-time keeps tool budget reasonable). Each agent edits its locale's stub file via a single `Edit` tool call. Use this template — replace `<LOC>` (locale code), `<LOCALE_NAME>` (human-readable, e.g. "French — France register"), and adjust the per-locale glossary line:

> Translate the body of `_posts/<LOC>/<slug>.md` into native `<LOCALE_NAME>`. Read the EN body from `_posts/<slug>.md` (lines from the H1 onwards, including the `<!-- enrich-start --> ... <!-- enrich-end -->` block at the end).
>
> **Drop** the `<!-- translation-stub -->` comment and the "Translation pending" blockquote, replace everything from there through end of file with the translation.
>
> **Native tone-of-voice (non-negotiable):** match the executive register a senior banking technologist would use writing for a board / lead-architect audience in `<LOCALE_NAME>`. No hype filler. No "plongeons dans" / "sumérgete" / "tauchen wir ein" / "vamos mergulhar" / equivalent. Cite the same kind of authoritative sources the EN piece does.
>
> **Native SEO (also non-negotiable):** translate `title`, `subtitle`, `description`, `keywords`, `twitter_title`, `twitter_description`, and `excerpt` in the frontmatter too. Match the EN SEO intent — keep the primary keyword phrases that natively rank in the target market, expand acronyms once on first mention (DORA, ICT, GDPR, NIS2, FMI, PSP) and then keep the canonical English form. `title` ≤ 70 chars after translation; `description` 140–160 chars; `keywords` should remain a comma-separated list translated to native terms while preserving key English search terms (e.g. "Kubernetes", "DORA", "ISO 20022", "ML-KEM", "RTGS").
>
> **Markdown structure is load-bearing.** Every heading (H1/H2/H3), blockquote, bullet, table row, citation link, and the `<!-- enrich-start --> ... <!-- enrich-end -->` aside must appear at exactly the same nesting in the same order. Only the prose between markup changes.
>
> **Citation links: `[Visible text](url "title")`.** Translate visible text + `title` attribute. **NEVER** change the URL.
>
> **Numbers, percentages, dates, statistics are facts.** Translate the surrounding sentence; never paraphrase the number itself.
>
> **Acronyms** stay canonical English with a parenthetical native expansion on first mention if a standard one exists. Native-language glossary for `<LOCALE_NAME>`: <ONE LINE OF KEY TERM MAPPINGS — e.g. for FR: "cloud-native → cloud natif; container → conteneur; resilience → résilience; sovereignty → souveraineté; outsourcing → externalisation; workload → charge de travail; data residency → résidence des données">.
>
> **Enrich block at the bottom** (`<!-- enrich-start --> ... <!-- enrich-end -->`): localise to the per-locale canonical pattern. Model on the most recent `_posts/<LOC>/2026-*.md` for the canonical "About the author" structure (aria-label + bio + credentials + "Last reviewed" line).
>
> Do **not** invent statistics, sources, or claims the EN source doesn't make.

Dispatch in priority order (highest-traffic markets first): **fr es de it pt-br nl ja zh-hans zh-hant ko ar ru pl cs uk ro tr he hi bn id vi th fil ha yo sv** (27 total).

When the parallel batch completes, verify completeness:

```bash
python3 scripts/editorial/translate_post.py <slug> --list-stubs       # should report 'all 27 locales translated'
```

### 7. Homepage card rotation

Edit `_posts/index.md`: in the `<div class="newsroom-grid feat-latest-grid">` block, **prepend** a new `<article class="newsroom-card">` for today (mirror the structure of the cards already there) and **drop the bottom card** so there are still **6 visible**. The 6-card balance fills the 3-column grid cleanly across all 28 locales (`build_translations.py` rewrites per-locale at build time).

### 8. Listings refresh

These are Python-only and run identically in both modes. `gen_articles.py` now **auto-discovers** the latest dated post — you no longer need to hand-edit the `ARTICLES` list.

```bash
python3 scripts/generators/gen_layouts.py
python3 scripts/generators/gen_articles.py    # auto-prepends today's article via _discover_latest_article()
python3 scripts/generators/gen_projects.py
python3 scripts/generators/gen_papers.py
python3 scripts/postbuild/topic_link.py
python3 scripts/postbuild/post_enrich.py
python3 scripts/generators/build_topics.py    # if today's article fits an existing cluster OR you've added it to TOPICS, the slug shows up here
python3 scripts/generators/build_lang_feeds.py
python3 scripts/generators/build_agent_api.py
```

**Topic cluster note**: if today's article belongs to an existing cluster in `scripts/generators/build_topics.py:TOPICS`, prepend its slug to that cluster's `slugs:` list. If it needs a brand-new cluster, add it (mirror the existing cluster shape — title, banner, lede, slugs). Per-locale topic clones are generated automatically by `build_translations.py`.

### 9. Validate

**Local mode (ssg present):**

```bash
./build.sh
```

Must exit 0. Surfaces i18n leakage, hreflang regression, CSP issue, RTL bug, sitemap completeness gap, news-sitemap duplicate, JSON-LD validation.

**Cloud mode (no ssg):** skip `./build.sh`. Pages-deploy CI runs it on PR merge. Best-effort Python checks:

```bash
python3 -m pytest tests/test_build_translations_smoke.py::test_parse_frontmatter_basic tests/test_translate_post.py tests/test_gen_articles_autodiscover.py -q  || true
```

### 10. Commit + open PR

**Local mode:**

```bash
today=$(date -u +%F)
slug=$(basename _posts/${today}-*.md .md)
title=$(grep -oE '^title: *"[^"]+"' "_posts/${slug}.md" | head -1 | sed 's/title: *"//;s/"$//' | head -c 80)
branch="content/${today}-$(echo "$slug" | cut -d'-' -f4-7 | head -c 30)"

git checkout -b "$branch"
git add _posts/ _data/ scripts/generators/gen_articles.py scripts/generators/build_topics.py _layouts/ .claude/ 2>/dev/null || true
git commit -S -m "content(${today}): ${title} + 27 translations"
git push -u origin "$branch"
gh pr create --title "content(${today}): ${title}" --body "$(cat <<EOF
## Summary
- EN article: **${title}**
- 27 non-EN locales translated with native SEO + tone (fr/es/de/it/pt-br/nl/ja/zh-hans/zh-hant/ko/ar/ru/pl/cs/uk/ro/tr/he/hi/bn/id/vi/th/fil/ha/yo/sv)
- Homepage card rotated to keep 6 visible
- gen_articles.py auto-discovered the new post; /articles/ featured story refreshed
- check_voice gate passed: frontmatter complete, banner reachable, no hype filler, structural shape OK

## Test plan
- [x] check_voice green
- [x] all 27 locales translated (no stubs remaining)
- [x] \\\`./build.sh\\\` green (local) OR pending CI (cloud)
- [ ] CI build + diff + accessibility + lighthouse pass
EOF
)"
```

**Cloud mode** (`git push` returns 403, no SSH key for signing): use the GitHub MCP server.

1. `mcp__github__create_branch` — base `main`, head `content/<today>-<slug-frag>`
2. For each changed file (collect via `git status --porcelain | grep -v '^?? docs/' | grep -v '^?? public/'`), call `mcp__github__create_or_update_file` with the path + base64 content + branch.
3. `mcp__github__create_pull_request` — same title/body as above.

Do **not** attempt `git push` in cloud mode — it will 403.

### 11. Report back

Tell Sebastien:
- The PR URL
- Slug + title
- 28/28 locale count
- Any voice-gate defects you fixed before scaffolding
- The banner image used (URL or filename + hint that drove the pick)
- Anything that needed a fix not in this checklist
- Reminder: merge from GitHub mobile when CI is green

## Surfaces this routine automatically updates

After a clean run, every reference to today's article is in place across:

- `_posts/<slug>.md` (EN source)
- `_posts/<lang>/<slug>.md` × 27 (locale translations)
- `_data/i18n/<lang>/slugs.json` × 27 (slug map entries)
- `_posts/index.md` (homepage 6-card grid)
- `_posts/articles.md` (regenerated by `gen_articles.py` auto-discover)
- All 28 RSS/Atom/JSON Feed/news-sitemap files (regenerated by `build_lang_feeds.py`)
- `sitemap.xml` (ssg generates → postbuild augments with rendered topic pages)
- All 28 `search-index.json` files (regenerated by ssg + build_translations)
- `/api/agents/posts.json` (regenerated by `build_agent_api.py`)
- `/llms-full.txt` (regenerated by `postbuild.py`)
- `/topics/<cluster>/index.html` × 6 EN topic pages + 6 × 27 per-locale forks (if cluster updated)

If your final commit diff includes hundreds of `docs/` or `public/` files, you ran `./build.sh` and committed its output — back those out (`git reset HEAD~1; git checkout -- docs/ public/`) before pushing.
