#!/usr/bin/env bash
# Cloudflare KV write audit — guards the 1,000 writes/day Free-tier budget.
#
# Fails the build when a Worker module calls `.put()` on a KV-like binding
# without an `// adr: <ADR-NN> — <reason>` opt-in comment on the line
# immediately above.
#
# Heuristics applied:
#   - Skips files under workers/ ending in .bundled.js and test_*.mjs.
#   - Ignores comment lines (those starting with `*` or `//`).
#   - Ignores Cache API and Durable Object storage puts
#     (caches.default.put / state.storage.put / ctx.storage.put).
#   - Accepts a `.put(` call if the preceding non-blank line matches `// adr:`.
#
# Policy: project-docs/adr/0001-kv-free-tier-policy.md
#
# Run locally: scripts/dev/check_kv_writes.sh
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

violations=$(find workers -type f \
  \( -name '*.js' -o -name '*.mjs' \) \
  ! -name '*.bundled.js' \
  ! -name 'test_*.mjs' \
  -print0 \
  | xargs -0 awk '
    {
      # Trim leading whitespace for comment-line detection.
      stripped = $0
      sub(/^[[:space:]]+/, "", stripped)
      is_comment = (stripped ~ /^\*/ || stripped ~ /^\/\//)
      if (!is_comment && $0 ~ /\.put[[:space:]]*\(/ \
          && $0 !~ /(caches\.default|state\.storage|ctx\.storage)\.put/) {
        if (prev !~ /\/\/[[:space:]]*adr:/) {
          print FILENAME ":" FNR ": " $0
        }
      }
      prev = $0
    }
    FNR == 1 { prev = "" }
  ')

if [ -n "$violations" ]; then
  echo "::error::KV write without an ADR opt-in comment found."
  echo "Policy: project-docs/adr/0001-kv-free-tier-policy.md"
  echo "Fix: add '// adr: <ADR-NN> — <one-line reason>' above each .put() call."
  echo
  printf '%s\n' "$violations"
  exit 1
fi

echo "ok: no untagged KV writes."
