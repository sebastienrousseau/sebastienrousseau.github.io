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
python3 scripts/build_agent_api.py
python3 scripts/postbuild.py

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
