#!/usr/bin/env bash
set -euo pipefail

# Run the same pa11y-ci accessibility sweep as CI, but locally and with
# the delta cache so only changed pages get re-tested.
#
# Why local? GitHub-hosted runners take 60-90 min for a full sweep of
# 1,990 pages. Locally on an M-series Mac it's typically 3-8 min for
# the delta, and you can scope to specific URLs for sub-minute feedback.
#
# Usage:
#   scripts/dev/pa11y-local.sh                       # delta sweep (cache-aware)
#   scripts/dev/pa11y-local.sh --full                # ignore cache; re-sweep everything
#   scripts/dev/pa11y-local.sh --scope <slug>        # only URLs matching <slug>
#                                                    # e.g. 2026-06-04-quantum-safe-…
#   scripts/dev/pa11y-local.sh --scope-en-only       # EN tree only (skip 27 locales)
#   scripts/dev/pa11y-local.sh --dark                # dark-mode representative subset
#                                                    # (.pa11yci.dark; theme forced via
#                                                    # pa11y actions; cache not touched)
#                                                    # combine with --scope to narrow
#
# The script:
#   1. Installs pa11y-ci to scripts/dev/node_modules/ if missing
#      (so it doesn't touch your global npm tree).
#   2. Boots a static server on a free port over public/.
#   3. Runs scripts/seo_and_audit/pa11y_cache.py pre (same call as CI).
#   4. Invokes pa11y-ci on the delta.
#   5. Retries Puppeteer "Execution context was destroyed" flakes.
#   6. Updates _data/pa11y-cache.json on success.
#
# Exit 0 on a clean sweep; non-zero on real WCAG violation.

cd "$(git rev-parse --show-toplevel)"

mode=delta
scope=""
scope_en_only=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --full)          mode=full ;;
    --dark)          mode=dark ;;
    --scope)         scope="$2"; shift ;;
    --scope-en-only) scope_en_only=1 ;;
    -h|--help)
      sed -n '/^# Usage:/,/^$/p' "$0" | sed 's/^# \?//'
      exit 0
      ;;
    *) echo "unknown flag: $1" >&2; exit 2 ;;
  esac
  shift
done

# ── 1. Toolchain check (mise-managed via mise.toml) ──────────────────────────
# Both `pa11y-ci` (WCAG sweeper) and `http-server` (static origin) are
# pinned in mise.toml under the `npm:` backend. `mise install` provisions
# them; this script doesn't need to install anything itself.
if ! command -v pa11y-ci >/dev/null 2>&1 || ! command -v http-server >/dev/null 2>&1; then
  echo "==> missing pa11y-ci or http-server on PATH — running 'mise install'"
  mise install
fi

# pa11y-ci 3.x bundles an old Puppeteer (Chromium r869685, 2021-era).
# That binary doesn't auto-download under mise's npm shim, and even when
# it does it's flagged on macOS Gatekeeper. Easier path: point Puppeteer
# at the system-installed Chrome that Sebastien already keeps signed and
# trusted. The path is the same on every Mac that has Chrome installed.
if [[ -z "${PUPPETEER_EXECUTABLE_PATH:-}" ]]; then
  CHROME_MAC="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
  if [[ -x "$CHROME_MAC" ]]; then
    export PUPPETEER_EXECUTABLE_PATH="$CHROME_MAC"
  else
    echo "Chrome not found at $CHROME_MAC — set PUPPETEER_EXECUTABLE_PATH" >&2
    echo "to an installed Chromium/Chrome binary, or install Chrome." >&2
    exit 1
  fi
fi

# ── 2. Boot a static server ──────────────────────────────────────────────────
[[ -d public ]] || { echo "public/ missing — run ./build.sh first" >&2; exit 1; }

port=$(python3 -c 'import socket; s=socket.socket(); s.bind(("",0)); print(s.getsockname()[1]); s.close()')
echo "==> serving public/ on http://127.0.0.1:$port"
http-server public -p "$port" --silent >/dev/null 2>&1 &
server_pid=$!
# Make sure the server dies with us.
trap 'kill "$server_pid" 2>/dev/null || true' EXIT
sleep 1

# ── 3. Pre — partition pages against the cache ──────────────────────────────
cache=_data/pa11y-cache.json
[[ "$mode" == "full" ]] && rm -f "$cache"

python3 scripts/seo_and_audit/pa11y_cache.py pre \
  --public-dir public \
  --cache "$cache" \
  --pa11yci-out .pa11yci \
  --manifest-out .pa11y-cache-manifest.json \
  --base-url "http://127.0.0.1:$port"

# Dark mode — swap in the representative dark subset the pre-pass wrote.
# Entries are {url, actions} objects that click .theme-toggle and wait
# for html[data-theme="dark"] before auditing. The light cache is
# neither consulted nor updated for this run.
if [[ "$mode" == "dark" ]]; then
  cp .pa11yci.dark .pa11yci
  echo "==> dark-mode subset run (.pa11yci.dark)"
fi

# Optional scoping — filter the URL list to a slug / EN-only subtree.
# Entries may be strings (light) or {url, actions} objects (dark).
if [[ -n "$scope" ]]; then
  python3 -c "
import json, sys
cfg = json.load(open('.pa11yci'))
cfg['urls'] = [u for u in cfg['urls']
               if '$scope' in (u['url'] if isinstance(u, dict) else u)]
json.dump(cfg, open('.pa11yci', 'w'), indent=2)
print(f'scoped to {len(cfg[\"urls\"])} URL(s) containing {\"$scope\"!r}')
"
fi
if [[ "$scope_en_only" -eq 1 ]]; then
  python3 -c "
import json, re
cfg = json.load(open('.pa11yci'))
# Drop any URL under a 2-3 letter locale prefix like /fr/, /zh-hans/, /pt-br/.
LOC = re.compile(r'http://[^/]+/(?:[a-z]{2}|fil|zh-hans|zh-hant|pt-br)/')
cfg['urls'] = [u for u in cfg['urls'] if not LOC.match(u)]
json.dump(cfg, open('.pa11yci', 'w'), indent=2)
print(f'scoped to EN only — {len(cfg[\"urls\"])} URL(s)')
"
fi

# Inject the resolved Chrome path into chromeLaunchConfig so Puppeteer
# doesn't fall back to its bundled (missing) Chromium download. CI never
# needs this because the GitHub-hosted runner ships Chromium on PATH.
python3 -c "
import json, os
cfg = json.load(open('.pa11yci'))
cfg.setdefault('defaults', {}).setdefault('chromeLaunchConfig', {})['executablePath'] = os.environ['PUPPETEER_EXECUTABLE_PATH']
json.dump(cfg, open('.pa11yci', 'w'), indent=2)
"

n=$(python3 -c "import json; print(len(json.load(open('.pa11yci'))['urls']))")
echo "==> pa11y-ci will run on $n URL(s)"

if [[ "$n" -eq 0 ]]; then
  echo "Full cache hit — nothing to test. Run with --full to force re-sweep."
  exit 0
fi

# ── 4. Run pa11y-ci on the delta ─────────────────────────────────────────────
set +e
pa11y-ci -c .pa11yci --reporter json > pa11y.json
rc=$?
set -e

# ── 5. Retry Puppeteer flakes ────────────────────────────────────────────────
if [[ "$rc" -ne 0 ]]; then
  echo "==> pa11y-ci returned non-zero; partitioning real failures vs Puppeteer flakes"
  python3 scripts/seo_and_audit/pa11y_retry_flakes.py pa11y.json
fi

# ── 6. Update cache on success ───────────────────────────────────────────────
# Dark runs never touch the cache: the manifest describes the LIGHT
# delta sweep, and `post` would mark those pages as passed unswept.
if [[ "$mode" == "dark" ]]; then
  echo "==> clean (dark subset). cache left untouched."
  exit 0
fi

python3 scripts/seo_and_audit/pa11y_cache.py post \
  --public-dir public \
  --cache "$cache" \
  --manifest .pa11y-cache-manifest.json

echo "==> clean. cache updated at $cache"
