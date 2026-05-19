---
description: Promote today's _drafts/ article, translate the 27 locale stubs into native-language full translations, run the build, commit (signed) + push.
---

You are running **locally on Sebastien's laptop**. Your job is to ship today's article end-to-end.

## Steps — execute in this order

### 1. Locate today's source

Run `date -u +%F` to get today's UTC date. Then find `_drafts/<today>-*.md`. If none exists, stop and say "no draft for today — drop one into `_drafts/` first." If there's already a `_posts/<today>-*.md` (someone ran this earlier today), skip step 2.

### 2. Promote + scaffold + add to homepage + featured

Run:

```bash
./scripts/publish_daily.sh
```

That script does:

- `git mv _drafts/<today>-*.md _posts/`
- `python3 scripts/translate_post.py <slug>` — writes 27 stub MD files (one per non-EN locale) with localised frontmatter + the EN body wrapped in a `<!-- translation-stub -->` marker, plus appends EN→native-slug mapping into each `_data/i18n/<lang>/slugs.json`
- Runs every `gen_*.py` script so listing pages pick up the new article
- Runs `./build.sh` so all i18n gates pass and `docs/` is regenerated

**You still need to update two curated files manually** because they're hand-maintained:

- `_posts/index.md` — prepend a new `<article class="newsroom-card">` block at the top of the "From the desk" newsroom-grid (mirror the structure of the other cards in that section). Drop the bottom-most card so there are still five visible.
- `scripts/gen_articles.py` — prepend a new `ARTICLES[0]` tuple of the shape `(date_iso, date_display, eyebrow, title, image_url, image_alt, excerpt, href)` so the article becomes the /articles/ featured story. Then re-run `python3 scripts/gen_articles.py` once.

Re-run `./build.sh` after the manual edits.

### 3. Translate the 27 stubs

Find pending locales:

```bash
python3 scripts/translate_post.py <slug> --list-stubs
```

For each path it lists, **read the stub, then rewrite the entire body** (preserving the frontmatter as-is) with a full native-language translation that satisfies the rules below. Use the Edit tool — replace the placeholder block beginning `<!-- translation-stub -->` through the end of file with the translated body.

**Translation rules (non-negotiable):**

- **Executive register.** No hype. No "delve into", "embark on", "in conclusion", "it is worth noting that". British English origin tone, translated literally into the target language's equivalent register.
- **Markdown structure is load-bearing.** Every heading, blockquote, bullet list, code block, table, and citation link must appear at the same nesting in the same order. Only the prose between markup changes.
- **Citation links: `[Source name](url "Source title")`.** Translate the visible link text AND the `title` attribute. **Never** change the URL.
- **Numbers, percentages, dates, statistics are FACTS** — translate the surrounding sentence; never paraphrase the number itself.
- **Acronyms** (BIS, CPMI, FSB, NIST, NCSC, ISO 20022, RTGS, …) stay in their canonical English form on first mention; add a parenthetical native-language expansion if a standard one exists.
- **Frontmatter title/subtitle/description/keywords/twitter_** fields**: translate these too. Match the SEO intent (length + key terms) of the EN version.
- **Don't invent statistics, sources, or claims** the EN source doesn't make.

Move through locales in this order for best quality: `fr es de it pt-br nl ja zh-hans zh-hant ko ar ru pl cs uk ro tr he hi bn id vi th fil ha yo sv`. Highest-traffic markets first.

### 4. Re-validate

```bash
./build.sh
```

Must exit 0. If `test_lang_no_leakage` flags anything, an EN chrome string leaked into a non-EN page — check `_data/i18n/<lang>/chrome_patches.json` for missing keys.

### 5. Commit + push (signed)

```bash
today=$(date -u +%F)
slug=$(basename _posts/${today}-*.md .md)
title=$(grep -oE '^title: *"[^"]+"' "_posts/${slug}.md" | head -1 | sed 's/title: *"//;s/"$//' | head -c 80)
git add -A
git commit -S -m "content(${today}): ${title} + 27 translations"
git push
```

Cloudflare Pages will pick up `main` and deploy automatically. Verify by `curl -sI https://sebastienrousseau.com/` and checking `last-modified` updates within ~3 minutes.

### 6. Report back

Report to the user:

- The slug
- Total tests passing
- Live URL once deploy lands
- Anything that needed a fix not in this checklist

## Constraints

- **NEVER** put `ANTHROPIC_API_KEY` in repo secrets, in env vars committed to git, in CI workflows, or in `.env` files. All translation work happens here, in this conversation, using the user's existing Claude subscription.
- **NEVER** skip commit signing (`-S`). The repo's `commit.gpgsign=true` + SSH-key-signing is enforced.
- **NEVER** force-push to `main`.
- If a build gate fails (i18n parity, hreflang reciprocity, CSP-strict, lang-leakage, RTL-safe), fix the root cause — don't disable the gate or add the slug to a skip-list.
