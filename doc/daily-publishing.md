<!-- SPDX-License-Identifier: Apache-2.0 -->

# Daily publishing runbook

The site ships **one long-form article per day** across 28 locales
(EN + 27 native translations). This document is the steady-state
process: drop a draft into `_drafts/`, the pipeline picks it up and
publishes it everywhere on the next scheduled run.

## TL;DR

```bash
# 1. Drop today's article into _drafts/ with the YYYY-MM-DD- prefix
cp my-new-piece.md _drafts/2026-05-20-my-new-piece.md

# 2. Wait for the cron, or trigger manually:
make publish-today

# Done. Article will live at:
#   https://sebastienrousseau.com/2026-05-20-my-new-piece/
# in every supported language.
```

## Daily timing — picked to catch every major market

The site reads in **APAC, Europe, UK, US-East and US-West**. The cron
runs at **06:30 UTC** — that's 7:30 am Lagos, 8:30 am Cape Town, 12:00
noon Mumbai, 2:30 pm Singapore, 3:30 pm Tokyo. By UK business open
(09:00 BST = 08:00 UTC) the article is already in front of APAC
readers and warming Cloudflare edges before the European traffic wave.
US morning hits the same article that's now fully cached across every
edge POP.

| Region | Local time when 06:30 UTC fires |
|--------|---------------------------------|
| Singapore (SGT) | 14:30 (same day) |
| Tokyo (JST) | 15:30 (same day) |
| Sydney (AEST) | 16:30 (same day) |
| London (BST) | 07:30 (same day, pre-business) |
| Lagos / Cape Town | 07:30 / 08:30 |
| New York (EDT) | 02:30 (same day) — fully warm by 09:00 EDT |
| Los Angeles (PDT) | 23:30 (previous day) — fully warm by 06:00 PDT |

## Inputs the pipeline expects

A single Markdown file under `_drafts/` whose filename starts with the
publication date in ISO format:

```
_drafts/YYYY-MM-DD-<kebab-slug>.md
```

Frontmatter MUST include at minimum:

```yaml
title: "Headline (publishable; 50-65 chars)"
subtitle: "One sentence framing (120-180 chars)"
description: "Two-sentence SEO summary (155-250 chars)"
date: "Month Day, Year"     # ← English form; the pipeline localises
keywords: "comma, separated, twenty-or-so, terms"
tags: "comma, separated, public-facing, tags"
banner: "https://cloudcdn.pro/stocks/images/<filename>.webp"
banner_alt: "WCAG-compliant alt text describing the topic, not the photo"
banner_width: "1425"
banner_height: "571"
layout: "report"            # or "page" / "article"
schema: "FAQPage, Article"  # JSON-LD types
```

Plus the body in standard Markdown. Use the structure of any
`_posts/2026-05-1*-*.md` as a reference (executive summary → numbered
sections → "What it means for banks" → references).

## What the pipeline does (in order)

1. **Find today's draft.** `scripts/publish_daily.sh` looks for the
   first file under `_drafts/` whose date prefix matches `date -u +%F`.
   If none exists, the run exits 0 (no-op).
2. **Promote → `_posts/`.** `git mv _drafts/<slug>.md _posts/<slug>.md`.
3. **Update curated lists.**
   - `_posts/index.md` — newsroom-grid: prepend today's card, drop the
     oldest of the visible five.
   - `scripts/gen_articles.py` — prepend a new tuple at the top of
     `ARTICLES` so the article becomes the featured story on
     `/articles/`.
4. **Re-run generators.** `python3 scripts/gen_articles.py`,
   `scripts/gen_projects.py`, etc. (`make regenerate`).
5. **Translate.** `python3 scripts/translate_post.py <slug>` walks every
   active non-EN locale, calls the Anthropic API to translate the body
   (with a strict tone-of-voice / markdown-preservation / citation-
   preservation system prompt), localises the frontmatter, writes
   `_posts/<lang>/<localised-slug>.md`, and appends the EN→native slug
   mapping into `_data/i18n/<lang>/slugs.json`.
6. **Build.** `./build.sh` runs SSG → postbuild → all i18n gates
   (parity, hreflang reciprocity, JSON-LD inLanguage, sitemap
   completeness, RTL safety, strict CSP, lang-leakage).
7. **Commit + push.** Conventional-commit subject:
   `content: YYYY-MM-DD <short title> + 27 translations`. Signed.
   Pushed to `main`. Cloudflare Pages deploys.

## Manual one-shot

```bash
# All in one (same as cron):
make publish-today

# Or step-by-step:
git mv _drafts/2026-05-20-my-new-piece.md _posts/
$EDITOR _posts/index.md scripts/gen_articles.py   # add card + ARTICLES entry
make regenerate                                    # regen articles.md + topics + …
python3 scripts/translate_post.py 2026-05-20-my-new-piece
./build.sh
git add _posts/ _data/i18n/ scripts/gen_articles.py docs/
git commit -S -m "content: 2026-05-20 my new piece + 27 translations"
git push
```

## Translation cost + quality

- **API**: Anthropic Claude 4.6 Sonnet. ~5k tokens in + ~3k tokens out
  per locale × 27 locales ≈ 135k in / 81k out per article. At current
  pricing that's ≈ **$3 per article** — daily cost ≈ $90/month.
- **Quality**: the system prompt in `scripts/translate_post.py`
  enforces (a) executive tone-of-voice, (b) Markdown structure
  preservation, (c) citation-link URL preservation with translated
  link text, (d) zero hallucinated statistics. The author's edit pass
  on a randomly-chosen locale weekly is sufficient QA.
- **No-API fallback**: if `ANTHROPIC_API_KEY` is missing, the script
  still emits stub posts with a "translation pending" header pointing
  at the EN original. The article ships in all 28 locales; the 27
  non-EN versions read "see English original" until the API run lands.

## What's automated by CI

`.github/workflows/publish-daily.yml` runs at 06:30 UTC daily on a
schedule and on manual `workflow_dispatch`:

1. Checkout main with full history + signing key.
2. Install Python deps + `anthropic` SDK.
3. Run `make publish-today`.
4. If anything got committed, push (the workflow has `contents: write`
   + `id-token: write` and uses a deploy key for signed pushes from
   the runner).

The workflow is idempotent: running twice on the same day produces no
change (the draft is gone after the first run).

## Failure modes

| Symptom | Fix |
|---------|-----|
| No draft for today | Workflow exits 0. Nothing posted. Drop a file. |
| `test_i18n_parity` fails | A locale's slugs.json didn't pick up the new EN slug. Re-run `scripts/translate_post.py <slug>`. |
| `test_hreflang_reciprocity` fails | Translated MD file missing under `_posts/<lang>/`. Same fix. |
| `test_lang_no_leakage` fails | A locale's chrome translation needs updating in `_data/i18n/<lang>/chrome_patches.json`. |
| Claude API quota / rate limit | Script retries 3× with exponential backoff. If it still fails, the article ships with the no-API stub. Re-run later. |
| Banner image 404s | `wrap_cdn_images_in_transform` won't help — verify the asset exists at `https://cloudcdn.pro/stocks/images/<filename>.webp` first. |
