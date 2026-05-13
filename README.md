# SebastienRousseau.com — Official Website 🌏

Source for [sebastienrousseau.com](https://sebastienrousseau.com), the
digital home of
[**Sebastien Rousseau**](https://github.com/sebastienrousseau) —
applied AI, ISO 20022 migration, post-quantum cryptography, and the
structural transformation of wholesale payments.

Built with [Shokunin SSG][00] (Rust) and a Python postbuild pipeline.

## Quick start

Prerequisites: **Rust toolchain** (for `ssg`) and **Python 3.11+**
(for the postbuild scripts and `markdown-it-py`).

```shell
cargo install ssg
git clone https://github.com/sebastienrousseau/sebastienrousseau.github.io.git
cd sebastienrousseau.github.io
./build.sh           # build the site into public/ and mirror to docs/
./build.sh --serve   # build + serve on http://127.0.0.1:8000
```

## Pipeline

`build.sh` chains:

1. `ssg` — render English Markdown in `_posts/` → `public/`.
2. `scripts/build_topics.py` — five thematic hubs + `/topics/` index.
3. `scripts/build_translations.py` — manual French translations from
   `_posts/fr/*.md` → `public/fr/<fr-slug>/`. Slugs come from
   `scripts/_fr_slugs.py`, the canonical EN ↔ FR slug map.
4. `scripts/build_fr_feeds.py` — `/fr/rss.xml`, `/fr/atom.xml`,
   `/fr/news-sitemap.xml` for the French edition.
5. `scripts/build_agent_api.py` — JSON endpoints for AI agents at
   `/api/v1/`.
6. `scripts/postbuild.py` — real SRI hashes, CSP JSON-LD hashes,
   tag badges, prev/next nav, reciprocal hreflang, sitemap splice,
   `robots.txt`, `llms.txt`.

## Quality gates

```shell
ruff check scripts/                    # Python lint
python3 scripts/validate_jsonld.py     # JSON-LD + XML feed validity
python3 scripts/audit_links.py         # internal-link 404 audit
```

## French translations

See [`_posts/fr/README.md`](_posts/fr/README.md) for the manual French
translation workflow and the slug-map convention.

[00]: https://shokunin.one "Shokunin Static Site Generator"
