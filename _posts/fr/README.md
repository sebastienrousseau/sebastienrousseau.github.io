# French translations

> Last Updated: June 4, 2026

This directory houses the manual French translations for the Sebastien Rousseau web platform, where every dated article published on the site gets translated to ensure content parity across all supported language trees.

## Slug map — single source of truth

The file scripts/lib/_fr_slugs.py defines the canonical mapping between English and French URL slugs. Each entry follows a key-value contract where the key matches the English source file name and the value represents the localized French URL segment.

## File convention

The French files use the same naming convention as the English files and reside in the language folder, which means the build tools can parse these files during compilation to build the correct output folders.

## Frontmatter

The top block of each file holds key details that the Static Site Generator site generator needs to build the pages. You must write dates in English format for the builder.

## Build flow

The translation script reads the English pages and swaps the main text and menu buttons. It links internal URLs to French pages and sets response headers.

## Adding a new translation

To add a translation, write the slug pair in the map and save the file here. Then run the build script to check if the tests stay green.

## French UI strings

The translation script uses a set of rules to swap common menu labels on the pages, and the templates pick these labels when the language is set.
