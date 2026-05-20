---
description: Promote today's _drafts/ article, translate the 27 locale stubs into native-language full translations, open a PR for review. Works in both local Claude Code (Mac) and Anthropic cloud /schedule routines.
---

You are publishing today's article on `sebastienrousseau.com`. Your job is to ship today's source content end-to-end as a reviewable PR — Sebastien merges it from GitHub mobile.

## Where you're running — read this first

There are two execution environments. Detect which one and branch accordingly. **Do not try to bridge between them.**

| Marker | Local (Sebastien's Mac) | Cloud routine (Anthropic) |
|---|---|---|
| `command -v ssg` returns a path | yes | **no** |
| `git push` works | yes | **no** (proxy returns 403) |
| `git -c commit.gpgsign=true commit -S` works | yes | no (no SSH key) |
| `gh pr create` works | yes | maybe — try, fall back to GitHub MCP |
| GitHub MCP tools available | usually no | **yes** |

**Run `command -v ssg` once at the start.** If empty → you are in cloud mode. The two flows diverge at the build step and at the push step.

## Constraints (apply in BOTH modes)

- **NEVER** put `ANTHROPIC_API_KEY` in repo secrets, env files, or CI workflows. All translation work happens here in conversation, using Sebastien's Claude subscription.
- **NEVER** force-push, **NEVER** push to `main` directly. Always open a PR — Sebastien merges from mobile.
- **NEVER** commit the rebuilt `docs/` from inside the routine. Pages-deploy CI rebuilds `docs/` from `public/` on PR merge. Committing `docs/` here just bloats the diff with output that will be regenerated. Only commit **source** files: `_posts/`, `_data/`, `scripts/gen_articles.py`, `_layouts/` if edited, `.claude/`.
- **NEVER** invent statistics, sources, or claims the EN source doesn't make.
- **NEVER** skip the i18n gates — fix the root cause if they fail.

## Steps — execute in this order

### 1. Locate today's source

```bash
date -u +%F
```

Find `_drafts/<today>-*.md`. If none exists, stop with: *"no draft for `<today>` — drop one into `_drafts/` first."* If a `_posts/<today>-*.md` already exists (a partial earlier run), skip step 2 and resume from step 3.

### 2. Promote + scaffold the 27 stubs

```bash
git mv _drafts/<today>-*.md _posts/
python3 scripts/translate_post.py <slug>          # writes 27 _posts/<lang>/<slug>.md stubs + slug-map entries
```

`translate_post.py` is Python-only — runs identically in both modes.

### 3. Verify banner image is reachable

The draft's `banner:` URL must return 200 from CloudCDN. Quick check:

```bash
banner=$(grep -oE '^banner: *"[^"]+"' _posts/<slug>.md | sed 's/banner: *"//;s/"$//')
curl -sIo /dev/null -w "%{http_code}\n" "$banner"
```

If 404, ask Sebastien for the correct CDN URL **before continuing** (a broken banner cascades through 28 locales). Update the URL in `_posts/<slug>.md` and in all 27 `_posts/<lang>/<slug>.md` stubs using `sed -i`.

### 4. Translate all 27 stubs

For maximum throughput, **launch parallel translation agents in batches**. Each agent edits one locale's stub file using a single `Edit` tool call.

```text
List pending:  python3 scripts/translate_post.py <slug> --list-stubs
```

For each locale path, dispatch a sub-agent with this template (replace `<LOC>` and `<LOCALE_NAME>`):

> Translate the body of `_posts/<LOC>/<slug>.md` into native `<LOCALE_NAME>`. Read lines 104–223 of `_posts/<slug>.md` as the EN source. Drop the `<!-- translation-stub -->` comment + the "Translation pending" blockquote and replace through end of file with the translation. Preserve every markdown construct at the same nesting (H1/H2/H3, blockquote bullets, table rows, citation links). Citation URLs are immutable — translate only visible text + `title=""`. Numbers/dates are facts — never paraphrase them. Acronyms (DORA, ICT, GDPR, NIS2, AI/ML, VM, Kubernetes, GitOps, SaaS, PSP, FMI, etc.) stay canonical English with native expansion on first mention. Enrich block at bottom → locale-localised pattern (model on `_posts/<LOC>/2026-05-18-*.md` for the canonical author-card structure). Executive register only. No invented stats.

Order locales by priority (highest-traffic first): **fr es de it pt-br nl ja zh-hans zh-hant ko ar ru pl cs uk ro tr he hi bn id vi th fil ha yo sv** (27 total).

When the parallel batch completes, re-run `--list-stubs` — should print `all 27 locales translated for <slug>.`

### 5. Update the homepage + featured article

Two curated files need a touch:

**`_posts/index.md`** — In the `<div class="newsroom-grid feat-latest-grid">` block, **prepend** a new `<article class="newsroom-card">` for the new post (mirror the existing card structure exactly) and **delete the bottom-most card** so there are still **6 visible**. The 6-card balance fills the 3-column grid cleanly across all 28 locales (`build_translations.py` rewrites per-locale at build time).

**`scripts/gen_articles.py`** — Prepend a new `ARTICLES[0]` tuple of shape:

```python
("YYYY-MM-DD", "Month DD, YYYY", "Eyebrow · Eyebrow · Eyebrow",
 "Full title",
 "https://cloudcdn.pro/stocks/images/<image>.webp",
 "Image alt text",
 "Short excerpt (1–2 sentences).",
 "/<slug>/index.html"),
```

Then regenerate `/articles/`:

```bash
python3 scripts/gen_articles.py
```

### 6. Refresh listings + topic graph

These are all Python-only and run identically in both modes:

```bash
python3 scripts/gen_layouts.py
python3 scripts/gen_projects.py
python3 scripts/gen_papers.py
python3 scripts/topic_link.py
python3 scripts/post_enrich.py
python3 scripts/build_topics.py
python3 scripts/build_lang_feeds.py
python3 scripts/build_agent_api.py
```

### 7. Validate

**Local mode (ssg present):** run the full gate stack —

```bash
./build.sh
```

Must exit 0. Surfaces any i18n leakage, hreflang regression, CSP issue, RTL bug, sitemap completeness gap. If it fails, fix the root cause and re-run.

**Cloud mode (no ssg):** skip `./build.sh`. Pages-deploy CI runs it on PR merge against the freshly-cloned source. Instead, run the Python-only checks that don't need a build output:

```bash
python3 -m pytest tests/test_build_translations_smoke.py::test_parse_frontmatter_basic tests/test_translate_post.py -q  || true
```

These are best-effort — the real gates run in CI.

### 8. Commit + open PR

**Local mode:**

```bash
today=$(date -u +%F)
slug=$(basename _posts/${today}-*.md .md)
title=$(grep -oE '^title: *"[^"]+"' "_posts/${slug}.md" | head -1 | sed 's/title: *"//;s/"$//' | head -c 80)
branch="content/${today}-$(echo "$slug" | cut -d'-' -f4-7 | head -c 30)"

git checkout -b "$branch"
# Stage SOURCE only — never commit docs/ from the routine
git add _posts/ _data/ scripts/gen_articles.py _layouts/ .claude/ 2>/dev/null || true
git commit -S -m "content(${today}): ${title} + 27 translations"
git push -u origin "$branch"
gh pr create --title "content(${today}): ${title}" --body "$(cat <<EOF
## Summary
- EN article: **${title}**
- 27 non-EN locales translated (fr/es/de/it/pt-br/nl/ja/zh-hans/zh-hant/ko/ar/ru/pl/cs/uk/ro/tr/he/hi/bn/id/vi/th/fil/ha/yo/sv)
- Homepage card rotated; gen_articles.py ARTICLES[0] swapped

## Test plan
- [x] \\\`./build.sh\\\` green locally (or pending CI for cloud mode)
- [x] 6 cards balanced on homepage
- [ ] CI build + diff + accessibility + lighthouse pass
EOF
)"
```

**Cloud mode** (`git push` returns 403, no SSH key for signing):

Use the GitHub MCP server. Approximate sequence:

1. `mcp__github__create_branch` — base `main`, head `content/<today>-<slug-frag>`
2. For each changed file (collect via `git status --porcelain | grep -v '^?? docs/'`), call `mcp__github__create_or_update_file` with the file path + base64 content + the branch.
3. `mcp__github__create_pull_request` — title `content(YYYY-MM-DD): <title>`, body as above, base `main`, head `<branch>`.

If the MCP tools aren't available, fall back to authenticated REST: `POST /repos/sebastienrousseau/sebastienrousseau.github.io/git/refs` for the branch, `PUT /repos/.../contents/<path>` per file (use the `Authorization: Bearer $GH_TOKEN` from the routine's env if present), then `POST /repos/.../pulls` to open the PR.

Do **not** attempt `git push` in cloud mode — it will 403.

### 9. Report back

Tell Sebastien:
- The slug
- Locale count (should be 28/28: 1 EN + 27 translations)
- The PR URL
- Anything that needed a fix not in this checklist (broken banner, missing locale chrome key, etc.)
- Reminder: merge from GitHub mobile when CI is green

## What goes in this directory's git history

After a clean run, your commit touches roughly:

- 28 × `_posts/[<lang>/]<slug>.md` (EN + 27 locales)
- 27 × `_data/i18n/<lang>/slugs.json` (slug-map entries)
- `_posts/index.md` (homepage card rotation)
- `_posts/articles.md` (regenerated)
- `scripts/gen_articles.py` (ARTICLES[0] swap)
- A handful of `_data/i18n/<lang>/home_patches.json` if listing markup changed
- **Nothing under `docs/` or `public/`** — CI rebuilds those on merge.

If your diff includes hundreds of `docs/.meta/*.meta.json` files, you ran `./build.sh` and committed its output — back those out before pushing.
