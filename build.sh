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

# Copy fingerprinted assets to their unfingerprinted aliases so the layouts'
# /main.js, /sw.js, /highlight.css references resolve.
for f in public/main.*.js public/sw.*.js public/theme-init.*.js public/highlight.*.css; do
  [[ -f "$f" ]] || continue
  base=$(basename "$f")
  short="${base%%.*}.${base##*.}"
  [[ "$short" == "$base" ]] && continue
  cp -f "$f" "public/$short"
done

python3 scripts/build_topics.py
python3 scripts/build_translations.py
python3 scripts/build_lang_feeds.py
python3 scripts/build_agent_api.py
python3 scripts/build_lead_magnets.py
python3 scripts/postbuild.py
# Sigstore signing pass — no-op unless _data/sigstore/config.json exists.
python3 scripts/sigstore_sign.py
python3 scripts/test_search_indexes.py
python3 scripts/test_i18n_parity.py
python3 scripts/test_i18n_strings.py
python3 scripts/test_i18n_labels.py
python3 scripts/test_i18n_takeaway_labels.py
python3 scripts/test_i18n_render_data.py
python3 scripts/test_i18n_author.py
python3 scripts/test_hreflang_reciprocity.py
python3 scripts/test_jsonld_localized.py
python3 scripts/test_sitemap_completeness.py
python3 scripts/test_lang_no_leakage.py
python3 scripts/test_rtl_safe.py --strict
python3 scripts/test_csp_strict.py
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
