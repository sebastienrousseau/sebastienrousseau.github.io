#!/usr/bin/env bash
# Cyclomatic-complexity gate over ALL of scripts/ — with a shrinking allowlist.
#
# The gate used to run over four directories only (postbuild.py,
# postbuild_lib/, generators/, lib/) while the README described complexity as
# a CI gate without qualification. The ungated half held the worst function in
# the repo — translate_frontmatter._process_article at D/25 — plus the whole
# translation pipeline, which rewrites content across 27 locales and has the
# least test coverage behind it.
#
# Widening the scope surfaced 31 C-or-worse functions. Rather than restructure
# untested build gates in one pass to hit a number — which is how correctness
# regressions get introduced — this used the same RATCHET the mypy gate uses
# (scripts/typecheck.sh): every directory is checked, accepted debt is listed
# in ALLOWLIST_FILE, and the gate fails on anything not listed.
#
# All 31 have since been cleared, each proven equivalent by differential-testing
# the refactor against the original over real corpus data. The allowlist is now
# EMPTY, so in practice this gate says: no C-or-worse function anywhere in
# scripts/. The ratchet stays because it is what keeps that true.
#
# The properties that matter:
#   * no NEW C-or-worse function can be added anywhere in scripts/;
#   * an allowlisted function that gets refactored must be REMOVED from the
#     list — the gate fails on a stale entry, so the list cannot rot;
#   * any future debt is enumerated in one place instead of being invisible.
#
# RATCHET: refactor an entry, delete its line, done. Target: empty list.
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

# "<path>:<function>" for every C-or-worse function accepted today.
# Sorted by grade, worst first. Nothing may be added without also fixing it.
ALLOWLIST_FILE="scripts/dev/complexity-allowlist.txt"

report=$(radon cc scripts/ -n C -s)

# radon prints "path" on its own line then indented "  F 12:0 name - C (13)".
current=$(printf '%s\n' "$report" | awk '
  /^[^[:space:]]/ { file=$0; next }
  /^[[:space:]]+[FCM] / { for (i=1;i<=NF;i++) if ($i=="-") { print file ":" $(i-1); break } }
' | sort -u)

# `grep -v` exits 1 when the file is nothing but comments — which is the
# target state — so it must not be allowed to kill the script under `set -e`.
allowed=$(grep -vE '^\s*(#|$)' "$ALLOWLIST_FILE" | sort -u || true)
allowed_count=$(printf '%s\n' "$allowed" | grep -c . || true)

new=$(comm -23 <(printf '%s\n' "$current") <(printf '%s\n' "$allowed"))
stale=$(comm -13 <(printf '%s\n' "$current") <(printf '%s\n' "$allowed"))

status=0
if [[ -n "$new" ]]; then
  echo "::error::new C-or-worse complexity (refactor it, or justify and add to $ALLOWLIST_FILE):" >&2
  printf '  %s\n' $new >&2
  status=1
fi
if [[ -n "$stale" ]]; then
  echo "::error::$ALLOWLIST_FILE lists functions that are no longer complex — delete these lines:" >&2
  printf '  %s\n' $stale >&2
  status=1
fi

if [[ "$status" -eq 0 ]]; then
  if [[ "$allowed_count" -eq 0 ]]; then
    echo "✓ complexity gate clean — allowlist empty, no C-or-worse function in scripts/"
  else
    echo "✓ complexity gate clean ($allowed_count allowlisted, 0 new)"
  fi
fi
exit "$status"
