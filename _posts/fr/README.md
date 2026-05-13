---
# This README is ignored by the build pipeline (the loader skips any
# file starting with "README" or with a non-dated stem).
---

# French translations

Manual French translations of dated posts from `_posts/`. Published
at `https://sebastienrousseau.com/fr/<fr-slug>/`.

## Slug map — single source of truth

`scripts/_fr_slugs.py` holds the canonical EN ↔ FR slug map. Every
entry follows the contract:

* **Key** — markdown stem in `_posts/fr/` AND `_posts/`.
* **Value** — published FR URL slug under `/fr/`.

```python
EN_TO_FR = {
    "2026-05-15-blackrock-brsrv-bstbl-genius-act-tokenised-mmf":
        "2026-05-15-rendement-cache-decryptage-depots-blackrock-brsrv-bstbl-genius-act",
    ...
}
```

The build pipeline accepts either form for the markdown filename — EN
slug (legacy) or FR slug (current convention) — and resolves the
counterpart via the map.

## File convention

```
_posts/2026-05-15-blackrock-brsrv-bstbl-genius-act-tokenised-mmf.md
_posts/fr/2026-05-15-rendement-cache-decryptage-depots-blackrock-brsrv-bstbl-genius-act.md
```

Published URL:

```
https://sebastienrousseau.com/fr/2026-05-15-rendement-cache-decryptage-depots-blackrock-brsrv-bstbl-genius-act/
```

## Frontmatter

```yaml
---
title: "Rendement caché : décryptage des dépôts BRSRV et BSTBL de BlackRock"
subtitle: "..."
description: "..."
date: "May 15, 2026"   # keep an English month string — parses cross-locale
language: "fr"
locale: "fr_FR"
banner: "https://cloudcdn.pro/stocks/images/..."
banner_alt: "..."
keywords: "..., ..."
---
```

## Build flow

1. `scripts/build_translations.py` walks `_posts/fr/*.md`, resolves
   the EN counterpart via `_fr_slugs.py`, forks the rendered English
   shell, swaps the body in French, rewrites every internal EN URL to
   its FR counterpart, localises chrome strings, breadcrumb JSON-LD,
   feed `<link>` tags, then writes `public/fr/<fr-slug>/index.html`.
2. `scripts/build_fr_feeds.py` emits `/fr/rss.xml`, `/fr/atom.xml`,
   `/fr/news-sitemap.xml`.
3. `scripts/postbuild.py` injects reciprocal hreflang on every paired
   page, splices the FR URLs into `sitemap.xml`, advertises the FR
   news-sitemap in `robots.txt`.

## Adding a new translation

1. Add the EN → FR slug pair to `scripts/_fr_slugs.py`.
2. Create `_posts/fr/<fr-slug>.md` with French frontmatter + body.
3. Run `./build.sh`.
4. Verify with `python3 scripts/validate_jsonld.py` and
   `python3 scripts/audit_links.py`.

## French UI strings

`scripts/build_translations.py` ships `CHROME_PATCHES` (regex pairs
that localise nav / footer / search / breadcrumb / aria labels) and
`I18N_FR` (Published / Updated / Previous / Next / etc.). Postbuild's
furniture renderers detect `<html lang="fr">` and pick the French
labels automatically.
