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
python3 scripts/postbuild/regen_slug_maps.py
python3 scripts/postbuild/regen_homepage.py

ssg -n=docs -c=_posts -t=_layouts -o=public

# Static Site Generator doesn't pick up theme-init.js as a managed asset; we ship it as-is.
cp -f _layouts/theme-init.js public/theme-init.js

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

# Build + stage WASM lab demos. Each subdirectory of _wasm-demos/ is a
# self-contained Rust→WASM crate plus a `web/` folder with the standalone
# HTML/JS/CSS shell. The compiled wasm-pack artefacts + the web shell are
# copied into public/labs/<crate-name>/ where they're served alongside the
# rest of the static site. Skipped if wasm-pack isn't on the PATH (e.g.
# minimal local builds) — CI installs it explicitly.
if command -v wasm-pack >/dev/null 2>&1 && [[ -d _wasm-demos ]]; then
  for demo in _wasm-demos/*/; do
    [[ -f "$demo/Cargo.toml" ]] || continue
    name=$(basename "$demo")
    echo "wasm-pack[$name]: building"
    (cd "$demo" && wasm-pack build --target web --release 2>&1 | tail -3)
    mkdir -p "public/labs/$name"
    cp "$demo/pkg/${name//-/_}.js" "public/labs/$name/"
    cp "$demo/pkg/${name//-/_}_bg.wasm" "public/labs/$name/"
    if [[ -d "$demo/web" ]]; then
      cp -R "$demo/web/." "public/labs/$name/"
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

python3 scripts/generators/build_topics.py
python3 scripts/generators/build_translations.py
python3 scripts/generators/build_lang_feeds.py
python3 scripts/generators/build_agent_api.py
python3 scripts/generators/build_lead_magnets.py
python3 scripts/postbuild/postbuild.py
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
# the *previously committed* bundles from docs/sigstore/ into
# public/sigstore/ first, so CI deploys ship the signatures even though
# CI has no key. Local builds with the key set will then overwrite each
# bundle with a fresh signature for any article whose HTML changed.
if [[ -d docs/sigstore ]]; then
  mkdir -p public/sigstore
  cp -a docs/sigstore/. public/sigstore/
fi
# Allow the signing pass to fail (e.g. wrong COSIGN_PASSWORD on this
# machine) without breaking the build — the committed bundles still ship.
python3 scripts/security/sigstore_sign.py || true
python3 scripts/tests/test_search_indexes.py
python3 scripts/tests/test_i18n_parity.py
python3 scripts/tests/test_i18n_strings.py
python3 scripts/tests/test_i18n_labels.py
python3 scripts/tests/test_i18n_takeaway_labels.py
python3 scripts/tests/test_i18n_render_data.py
python3 scripts/tests/test_i18n_author.py
python3 scripts/tests/test_hreflang_reciprocity.py
python3 scripts/tests/test_jsonld_localized.py
python3 scripts/tests/test_sitemap_completeness.py
python3 scripts/tests/test_lang_no_leakage.py
python3 scripts/tests/test_rtl_safe.py --strict
python3 scripts/tests/test_csp_strict.py
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
fi

# GitHub Pages serves from main/docs, so mirror the postbuild output into
# docs/ on every build. CNAME and .nojekyll are preserved.
rsync -a --delete --exclude CNAME --exclude .nojekyll public/ docs/
cat > docs/CNAME <<'CNAME'
sebastienrousseau.com
www.sebastienrousseau.com
CNAME
touch docs/.nojekyll

if (( SERVE )); then
  exec python3 -m http.server 8000 --directory public --bind 127.0.0.1
fi
