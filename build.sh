#!/usr/bin/env bash
set -euo pipefail

# Build sebastienrousseau.com with Static Site Generator (SSG), then post-process the output:
#   1. Replace Static Site Generator's placeholder integrity="sha256-<short-hex>" with real
#      base64 SHA-256 hashes computed from the actual file content. Browsers
#      will then enforce SRI on every /_csp/* asset, which is what the attribute
#      is supposed to do.
#   2. Asset fingerprinting emits main.<hash>.js but layouts reference /main.js.
#      Copy fingerprinted assets to their bare names so the references resolve.
#   3. Compute SHA-256 of every inline <script type="application/ld+json"> block
#      per page and inject those hashes into that page's CSP script-src. The
#      'unsafe-inline' carve-out is removed; the inline JSON-LD is then allowed
#      strictly by hash, not blanket-inline.
#
# Usage: ./build.sh          (build + patch only)
#        ./build.sh --serve  (build, patch, then serve public/ on :8000)

SERVE=0
[[ "${1:-}" == "--serve" ]] && SERVE=1

# Regenerate listings that are derived from `_posts/` on every build so
# article PRs can ship as additive-only diffs (just the new article
# source + 27 locale translations, no homepage rotation, no slug-map
# edits). Without these regens, each PR would have to hand-edit the
# same shared files and stacked PRs would collide.
#
#   - regen_slug_maps.py rewrites `_data/i18n/<lang>/slugs.json` from
#     the actual `_posts/<lang>/*.md` filenames.
#   - regen_homepage.py rewrites the 6-card grid in `_posts/index.md`
#     from the top-6 most recent dated EN posts.
#
# Both are idempotent: a no-op rebuild leaves the working tree clean.
# Create a temporary copy of the content directory to build from
rm -rf _posts_build
cp -R _posts _posts_build

# ssg's metadata-extraction pass scans EVERY *.md under the content dir for
# front matter. Translator/maintainer docs (e.g. _posts/<lang>/README.md) have
# none, which trips "Failed to extract metadata: No valid front matter found"
# on ssg >=0.0.44. Strip non-content markdown from the build copy (committed
# source is untouched).
find _posts_build -name 'README.md' -delete

# Run homepage rotation and post-enrichment on the temporary directory
python3 scripts/postbuild/regen_slug_maps.py
python3 scripts/postbuild/regen_homepage.py --dir _posts_build
python3 scripts/postbuild/post_enrich.py --dir _posts_build
# Rewrite the /tags/ cover page from _data/taxonomy.yml so the
# editorial pillar grid replaces the legacy monolithic anchor list.
# Lenient on missing taxonomy (WS3 commit 1 must have shipped first).
python3 scripts/generators/build_tags.py --dir _posts_build
# Backfill a permalink into any archive post that predates the convention.
# ssg >=0.0.45 derives the RSS channel <link> from permalink and aborts if
# it is missing; source stays untouched (build-copy only). See ADR-0002.
python3 scripts/postbuild/backfill_permalink.py --dir _posts_build

# Compile the site from the temporary directory instead of _posts
ssg -n=docs -c=_posts_build -t=_layouts -o=public

# Clean up the temporary directory
rm -rf _posts_build

# Static Site Generator doesn't pick up theme-init.js as a managed asset; we ship it as-is.
cp -f _layouts/theme-init.js public/theme-init.js

# On-site search runtime (DX plan Phase 2, ADR-0010). Same hands-off pattern as
# theme-init.js: SSG doesn't manage these, so ship them verbatim to public/. Both
# are lazy-loaded on first Cmd/Ctrl-K (or on /search) by main.js — never on the
# initial LCP path — and are same-origin under script-src/style-src 'self', so
# they need no CSP change and no SRI attribute. postbuild minifies them in place.
cp -f _layouts/search.js public/search.js
cp -f _layouts/search.css public/search.css

# Mirror .well-known/ into the build output so the OpenPGP Web Key
# Directory (WKD) endpoint is served at
#   https://sebastienrousseau.com/.well-known/openpgpkey/hu/<hash>
# Researchers verify the disclosure key here per .github/SECURITY.md
# in the sebastienrousseau/dotfiles repo. Files are static; no
# post-processing applies.
if [[ -d .well-known ]]; then
  mkdir -p public/.well-known
  cp -R .well-known/. public/.well-known/
fi

# Mirror fonts/ (self-hosted Inter + Newsreader + JetBrains Mono variable
# WOFF2, latin + latin-ext subsets) into public/fonts/. Same hands-off
# pattern as .well-known — files are static, served as-is, immutable cache.
if [[ -d fonts ]]; then
  mkdir -p public/fonts
  cp -R fonts/. public/fonts/
fi

# Compile and copy all client-side lab demos under labs/ into public/labs/.
# If a directory contains Cargo.toml, it is built with wasm-pack and the WASM
# artifacts (and any web shell content) are staged. Otherwise, it is a pure
# JavaScript/HTML/CSS demo and copied directly.
if [[ -d labs ]]; then
  mkdir -p public/labs
  if [[ -f labs/README.md ]]; then
    cp labs/README.md public/labs/README.md
  fi
  for demo in labs/*/; do
    [[ -d "$demo" ]] || continue
    name=$(basename "$demo")
    if [[ -f "$demo/Cargo.toml" ]]; then
      if command -v wasm-pack >/dev/null 2>&1; then
        echo "wasm-pack[$name]: building"
        (cd "$demo" && wasm-pack build --target web --release 2>&1 | tail -3)
        mkdir -p "public/labs/$name"
        cp "$demo/pkg/${name//-/_}.js" "public/labs/$name/"
        cp "$demo/pkg/${name//-/_}_bg.wasm" "public/labs/$name/"
        if [[ -d "$demo/web" ]]; then
          cp -R "$demo/web/." "public/labs/$name/"
        fi
      else
        echo "warning: wasm-pack not found, skipping Rust compilation for $name"
      fi
    else
      mkdir -p "public/labs/$name"
      cp -R "$demo/." "public/labs/$name/"
    fi
  done
fi

# Copy fingerprinted assets to their unfingerprinted aliases so the layouts'
# /main.js, /sw.js, /highlight.css references resolve.
for f in public/main.*.js public/sw.*.js public/theme-init.*.js public/highlight.*.css; do
  [[ -f "$f" ]] || continue
  base=$(basename "$f")
  short="${base%%.*}.${base##*.}"
  [[ "$short" == "$base" ]] && continue
  cp -f "$f" "public/$short"
done

# Rewrite syntect Base16 Ocean Dark inline styles to AAA-compliant values.
#
# The SSG bundles Base16 Ocean Dark as its syntect highlighter theme. The
# theme's token palette does not all clear 7:1 contrast against its own
# background (#2b303b). pa11y under WCAG2AAA flags multiple tokens — the
# comment colour (#65737e on #2b303b = 2.71:1) is the worst, the red error
# colour (#bf616a) sits at 3.62:1, and tokens like #8fa1b3 / #b48ead /
# #d08770 land in the 4-5:1 band that still fails AAA.
#
# A CSS override against the inner <pre style="bg"> wrapper doesn't reach
# this page because the SSG does not link /highlight.css on syntect-only
# pages (the existing rules only target pre.highlight). The reliable fix
# is to rewrite the inline styles directly in the served HTML: swap the
# inner-pre bg to pure black (max contrast headroom), then brighten the
# two tokens that still fall short on black. The remaining Base16 tokens
# all clear 7:1 on #000 once the bg swap is in place.
python3 - <<'PY'
from pathlib import Path
import re

# Inline-style remap. Keys are the original Ocean Dark inline values that
# the SSG emits; values are AAA-passing replacements measured against a
# pure-black background.
REMAP = {
    "background-color:#2b303b": "background-color:#000000",
    # Tokens that still fail 7:1 on #000 get explicit replacements.
    "color:#65737e": "color:#aab8cc",  # comments  — 2.71:1 → 9.78:1 on #000
    "color:#bf616a": "color:#ff8a93",  # red errors — 6.27:1 on #000 → 9.40:1
}
# Match either `style="...background-color:#2b303b..."` (the inner-pre wrapper)
# or `style="color:#XXXXXX"` (per-token spans). Restrict to syntect outputs
# by anchoring the bg-color value as a sentinel for the rest of the file.
SENTINEL = re.compile(r'style="background-color:#2b303b')

touched = 0
total_subs = 0
root = Path("public")
for html in root.rglob("*.html"):
    text = html.read_text(encoding="utf-8")
    if not SENTINEL.search(text):
        continue
    new = text
    subs = 0
    for src, dst in REMAP.items():
        n = new.count(src)
        if n:
            new = new.replace(src, dst)
            subs += n
    if subs:
        html.write_text(new, encoding="utf-8")
        touched += 1
        total_subs += subs
print(f"syntect-aaa-recolor: {touched} html files, {total_subs} inline-style substitutions")
PY

# Authority Playbook surfaces — fetch externally verifiable metrics first
# (graceful fallback if any single fetch errors) so the case-study templates
# can render aggregate numbers from the same source the homepage does.
python3 scripts/seo_and_audit/fetch_metrics.py
# Outcome-led case studies — reads `_data/proof/case-studies/*.yml` and
# forks the FT-tier `/articles/index.html` shell as template skeleton.
python3 scripts/generators/build_case_studies.py
python3 scripts/generators/build_topics.py
# Per-tag landing pages — reads the ssg-emitted /tags/index.html as
# template skeleton + the canonical taxonomy, and writes
# /tags/<slug>/index.html per landing-eligible canonical (>=3 posts).
# Locale forks land in a follow-up WS3 commit.
python3 scripts/generators/build_tag_landings.py
# Paged article listings — /articles/page/N/ + locale forks. Must run
# after ssg has produced /articles/index.html (used as template
# skeleton) and before build_translations (so the locale variants the
# generator emits don't get clobbered).
python3 scripts/generators/build_listings.py
# Static oEmbed JSON per article (build-time, zero-Worker pattern).
# Notion / Discord / Slack / WordPress / Atlassian use this for the
# rich link card when readers paste-share a sebastienrousseau.com URL.
python3 scripts/generators/build_oembed.py
python3 scripts/generators/build_translations/__main__.py
# Per-locale search UI microcopy (search-ui.json) for the client-side search
# runtime — projected from _data/i18n/<lang>/strings.json (ADR-0010). Runs after
# build_translations so every public/<lang>/ directory exists.
python3 scripts/generators/build_search_ui.py
python3 scripts/generators/build_lang_feeds.py
python3 scripts/generators/build_agent_api.py
python3 scripts/generators/build_lead_magnets.py
python3 scripts/generators/build_news_sitemap.py
# Changelog + "what's new" strip + build/deploy/uptime status (Phase 5).
# Runs AFTER build_translations so the homepage strip only lands on the
# English public/index.html (locale homepages are forked earlier and must
# not carry untranslated English entries), and BEFORE postbuild so the new
# /changelog/ + /status/ pages are picked up by the sitemap-augment pass and
# their inline JSON-LD is hashed into the per-page CSP. Deterministic:
# derives from committed dated-post front matter, no wall-clock time.
python3 scripts/generators/build_changelog.py
python3 scripts/postbuild/postbuild.py
# RAG-ready corpus export — JSONL one-object-per-article + per-tag
# subsets. Consumed by Claude / ChatGPT / Perplexity / LangChain etc.
# Runs after postbuild so body_text reflects the final article HTML
# (table-card data-labels stamped, breadcrumb chrome injected, etc.).
python3 scripts/seo_and_audit/build_rag_corpus.py
# Rewrite the in-page language switcher so each .ap-lang-item link
# points to the localised URL of THIS page (per the page's own
# hreflang alternates), not just /<lang>/. Without this, clicking
# "🇫🇷 Français" while reading an article sends the user to the
# French homepage instead of the French translation of that article.
# Must run after build_translations.py + postbuild.py have finalised
# every page's hreflang head links.
python3 scripts/postbuild/fix_lang_switcher.py
# Sigstore signing pass — no-op unless _data/sigstore/config.json exists
# (the cosign private key is machine-local, never in CI). Always mirror
# the *committed* bundles from sigstore-bundles/ into public/sigstore/
# first, so CI deploys ship the signatures even though CI has no key.
# Local builds with the key set will then overwrite each bundle with a
# fresh signature (and write it back to sigstore-bundles/) for any
# article whose HTML changed.
if [[ -d sigstore-bundles ]]; then
  mkdir -p public/sigstore
  cp -a sigstore-bundles/. public/sigstore/
fi
# Allow the signing pass to fail (e.g. wrong COSIGN_PASSWORD on this
# machine) without breaking the build — the committed bundles still ship.
python3 scripts/security/sigstore_sign.py || true
python3 tests/validation/test_search_indexes.py
python3 tests/validation/test_search_ui_parity.py
python3 tests/validation/test_i18n_parity.py
python3 tests/validation/test_i18n_strings.py
python3 tests/validation/test_i18n_labels.py
python3 tests/validation/test_i18n_takeaway_labels.py
python3 tests/validation/test_i18n_render_data.py
python3 tests/validation/test_i18n_author.py
python3 tests/validation/test_hreflang_reciprocity.py
python3 tests/validation/test_jsonld_localized.py
python3 tests/validation/test_sitemap_completeness.py
python3 tests/validation/test_lang_no_leakage.py
python3 tests/validation/test_rtl_safe.py --strict
python3 tests/validation/test_csp_strict.py
python3 tests/validation/test_sri_integrity.py
# Cloudflare Worker (edge Accept-Language router + security headers) —
# pure-logic tests, no Cloudflare runtime required. 100% line/branch/
# function coverage is enforced via Node's built-in test coverage so the
# CSP and locale-routing decision tree stays exhaustively tested.
# Skip silently if node isn't on the path.
if command -v node >/dev/null 2>&1; then
  node --test \
    --experimental-test-coverage \
    --test-coverage-lines=100 \
    --test-coverage-branches=100 \
    --test-coverage-functions=100 \
    --test-coverage-include='workers/lang-router.js' \
    workers/test_lang_router.mjs
  # ActivityPub sibling — same 100% line/branch/function coverage gate,
  # tested in isolation so the webfinger / actor / inbox / outbox decision
  # tree stays exhaustively covered as it grows past starter scope.
  node --test \
    --experimental-test-coverage \
    --test-coverage-lines=100 \
    --test-coverage-branches=100 \
    --test-coverage-functions=100 \
    --test-coverage-include='workers/activitypub.js' \
    workers/test_activitypub.mjs
  # MCP sibling — exposes the corpus over /mcp/v1/* as a read-only API.
  # Same exhaustive-coverage gate; hermetic (stubs globalThis.fetch for
  # manifest + JSONL). 100/100/100 mandatory because the route is the
  # discovery surface that AI clients hit.
  node --test \
    --experimental-test-coverage \
    --test-coverage-lines=100 \
    --test-coverage-branches=100 \
    --test-coverage-functions=100 \
    --test-coverage-include='workers/mcp.js' \
    workers/test_mcp.mjs
  # PDF proxy sibling — forwards /api/pdf/<slug>.pdf to the Fly.io
  # WeasyPrint service and Edge-caches the response. Same 100/100/100
  # gate; hermetic.
  node --test \
    --experimental-test-coverage \
    --test-coverage-lines=100 \
    --test-coverage-branches=100 \
    --test-coverage-functions=100 \
    --test-coverage-include='workers/pdf-proxy.js' \
    workers/test_pdf_proxy.mjs
fi

# Deployment is the public/ Pages artifact uploaded by CI
# (.github/workflows/ci.yml) — nothing is served from a git-tracked
# directory, so no local mirror step is needed.

if (( SERVE )); then
  exec python3 -m http.server 8000 --directory public --bind 127.0.0.1
fi
