---
# This README is ignored by the build pipeline (the loader skips any
# file starting with "README" or with a non-dated stem).
---

# French translations

This folder holds manual French translations of dated posts from
`_posts/`.

## Convention

Mirror the English slug exactly:

```
_posts/2026-05-15-blackrock-brsrv-bstbl-genius-act-tokenised-mmf.md
_posts/fr/2026-05-15-blackrock-brsrv-bstbl-genius-act-tokenised-mmf.md
```

The build script `scripts/build_translations.py` walks this folder, parses
each markdown file, and emits `public/fr/{slug}/index.html`. The published
URL becomes:

```
https://sebastienrousseau.com/fr/2026-05-15-blackrock-brsrv-bstbl-genius-act-tokenised-mmf/
```

## Frontmatter

Required:

```yaml
---
title: "Rendement caché : décodage des dépôts BRSRV et BSTBL de BlackRock"
description: "Sous le GENIUS Act, les stablecoins ne peuvent pas verser de rendement..."
date: "May 15, 2026"   # keep the English date string — it parses cross-locale
language: "fr"
locale: "fr_FR"
banner: "https://cloudcdn.pro/stocks/images/alev-takil-7ojyp-IXW7w-unsplash.webp"
banner_alt: "Pièces de dollars empilées sous une lumière chaude"
---
```

Then the markdown body in French. Same heading hierarchy as the English
source — the build script doesn't enforce structural parity but readers
expect it.

## What the build script does

1. Reads `_posts/fr/*.md` (skips this README, skips anything not
   matching `YYYY-MM-DD-slug.md`).
2. For each translation, locates the rendered English page at
   `public/{slug}/index.html` and uses it as the shell template.
3. Replaces the English `<main>` body with the French rendered body.
4. Patches `<html lang>`, meta tags, og:* tags, JSON-LD `inLanguage`
   and `headline`, canonical URL.
5. Writes `public/fr/{slug}/index.html`.
6. The postbuild pipeline then adds reciprocal hreflang links to BOTH
   the English original and the French translation, and emits a
   `/fr/index.html` hub page listing every translated article.

## French UI strings

The build script ships a small i18n map (`I18N_FR`) covering the
furniture labels: Published / Updated / min read / Previous / Next /
Sources & references / About the author / Topics. Edit
`scripts/build_translations.py` if you need new ones.
