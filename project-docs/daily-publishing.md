<!-- SPDX-License-Identifier: Apache-2.0 -->

# Daily publishing runbook (local Claude Code, no cloud API keys)

The site ships one long-form article per day across 28 locales (EN +
27 native translations). **All translation work happens locally** in
your Claude Code session using your existing subscription — no
Anthropic API key, no repo secret, nothing cloud-side except the
signed `git push` to `main` and the automatic Cloudflare Pages deploy
that follows.

You can drive the whole flow from any device that has Claude Code:
laptop, desktop, mobile (via the Claude iOS/Android app pointing at
your laptop's session). The work runs where Claude Code runs.

## TL;DR

```bash
# 1. Drop today's article into _drafts/ with the YYYY-MM-DD- prefix
mv my-piece.md _drafts/2026-05-20-my-piece.md

# 2. In Claude Code on your laptop:
/publish-today
```

That's it. The slash command (`.claude/commands/publish-today.md`)
walks you and Claude through: promote → scaffold 27 stubs → translate
each stub in-conversation → build → signed commit → push.

## Why this design

- **No API key risk.** Your `ANTHROPIC_API_KEY` never touches this
  repo. The translation work uses the Claude subscription you've
  already paid for via Claude Code — same auth as everything else
  you do in this CLI.
- **One-tap approval.** You see every translation Claude writes before
  it lands on disk, because every Edit is a tool call you approve.
  Mistakes get caught at scaffold time, not at deploy time.
- **Device-portable.** Open Claude Code on a different machine,
  pull main, type `/publish-today` — same result.

## What the slash command does

`.claude/commands/publish-today.md` is the source of truth for the
flow. Open it for the full checklist; the summary is:

1. Find `_drafts/<today>-*.md`. If none, stop.
2. Run `./scripts/editorial/publish-daily.sh` which:
   - `git mv`s draft → `_posts/`
   - calls `scripts/editorial/translate_post.py <slug>` to **scaffold 27 stub
     posts** (one per non-EN locale) with localised frontmatter + the
     EN body wrapped in a `<!-- translation-stub -->` marker
   - appends EN→native-slug mappings to every
     `_data/i18n/<lang>/slugs.json`
   - re-runs every `gen_*.py` so listings pick up the new post
   - runs `./build.sh` (i18n gates pass because stubs satisfy parity)
3. Manually update two curated files: `_posts/index.md`
   (newsroom-grid) and `scripts/generators/gen_articles.py` (ARTICLES[0]).
4. Translate each of the 27 stubs in-conversation. Claude reads each
   stub, rewrites the body in the target language following the
   tone-of-voice / markdown / citation / numeric-accuracy rules in
   the slash command.
5. Re-run `./build.sh`.
6. Signed `git commit -S` + `git push`. Cloudflare Pages auto-deploys.

## Frontmatter contract for the draft

The pipeline expects the draft to have at minimum:

```yaml
title: "Headline (publishable, 50-65 chars)"
subtitle: "One-sentence framing, 120-180 chars"
description: "Two-sentence SEO summary, 155-250 chars"
date: "Month Day, Year"
keywords: "comma, separated, twenty-or-so, terms"
tags: "comma, separated, public-facing, tags"
banner: "https://cloudcdn.pro/stocks/images/<filename>.webp"
banner_alt: "WCAG-compliant alt text describing the topic"
banner_width: "1425"
banner_height: "571"
layout: "report"
schema: "FAQPage, Article"
```

Use the structure of any `_posts/2026-05-1*-*.md` as a reference for
the body — executive summary → numbered sections → "what it means for
banks" → references.

## Timing

There's no cron. **Publish whenever you finish writing.** That said,
if you want maximum first-day reach across every market, hit `git
push` at one of these times:

| You push at (UTC) | Catches |
|-------------------|---------|
| **06:30** | Pre-business London, mid-day Mumbai, mid-afternoon Tokyo, fully warm by NY market open |
| **13:00** | NY pre-market, end-of-business London, evening Singapore |
| **22:00** | LA mid-afternoon, NY evening, Tokyo overnight (catches APAC morning) |

The first slot has the most upside because every Cloudflare POP is
warm before the largest traffic wave (UK + EU + US-East morning).

## Translation rules (enforced by the slash command)

- Executive register, British English origin tone, translated literally
- Markdown structure load-bearing (headings, lists, blockquotes, tables, code blocks all preserved)
- Citation links: visible text + `title` attribute translated, URL untouched
- Numbers / percentages / dates / statistics — translate the sentence around them, never paraphrase the number
- Acronyms (BIS, CPMI, FSB, NIST, NCSC, ISO 20022, RTGS, …) stay English on first mention with native expansion in parentheses
- Frontmatter `title`/`subtitle`/`description`/`keywords`/`twitter_*` get translated too
- No invented sources or statistics

## Idempotency

- Re-running `/publish-today` on a day that already shipped is a no-op
  (`_drafts/<today>-*.md` no longer exists, so the script exits 0).
- Re-running `scripts/editorial/translate_post.py <slug>` only overwrites stubs
  (files still carrying the `<!-- translation-stub -->` marker). Files
  that have already been translated are left alone.
- `scripts/editorial/translate_post.py <slug> --list-stubs` prints exactly which
  locales still need a translation pass — use it to resume an
  interrupted run.

## Failure modes + fixes

| Symptom | Fix |
|---------|-----|
| `./scripts/editorial/publish-daily.sh: no _drafts/<today>-*.md` | You haven't dropped a draft. Do that, retry. |
| `test_i18n_parity` fails on a locale | `_data/i18n/<lang>/slugs.json` didn't get the new EN→native mapping. Re-run `python3 scripts/editorial/translate_post.py <slug>`. |
| `test_hreflang_reciprocity` fails | A `_posts/<lang>/<slug>.md` file is missing. Same fix as above. |
| `test_lang_no_leakage` fails | An EN chrome string leaked into a non-EN page. Add the missing translation to `_data/i18n/<lang>/chrome_patches.json` — the failing-test output names the string. |
| `test_csp_strict` fails | A new inline `<script>` or `<style>` block didn't get its sha256 in CSP. `scripts/postbuild.py`'s `inject_jsonld_hashes` should cover it; check the failing-page output. |
| Banner image 404 | Check the asset exists at `https://cloudcdn.pro/stocks/images/<filename>.webp` before you ship. |
| Signed-push fails | `ssh-add -l` shows no identities. Run `ssh-add ~/.ssh/id_ed25519`, retry. |

## What's intentionally NOT automated

- **No GitHub Action cron.** Translation can't happen without Claude
  Code; a cron-driven publish would mean stub-only translations going
  live every day, which is worse than not running.
- **No Anthropic API key in secrets.** Same reason — and a key in CI
  has a much bigger blast radius than a key locked to your laptop.
- **No auto-edit of curated lists.** `_posts/index.md`'s newsroom-grid
  and `scripts/generators/gen_articles.py`'s `ARTICLES` tuple are editorial
  decisions (what to feature, what to drop). The slash command tells
  Claude to ask you what to drop.
