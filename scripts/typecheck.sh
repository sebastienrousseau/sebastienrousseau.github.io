#!/usr/bin/env bash
# Strict mypy gate — improvement-plan-2026.md Phase 1.2.
#
# Runs mypy (check_untyped_defs + disallow_incomplete_defs, configured in
# pyproject.toml) over the "strict-clean" tier — the modules that pass strict
# checking with zero errors today. Each package is checked with its own
# MYPYPATH so intra-package imports resolve as top-level, matching the
# sys.path wiring in tests/unit/conftest.py and avoiding mypy's
# "found twice under different module names" namespace-package trap.
#
# RATCHET: when a dir below the tier is cleaned, move it up. Outstanding:
#   - scripts/postbuild  /  scripts/generators  /  scripts/seo_and_audit (~1 each)
set -euo pipefail

fail=0
run() { # <mypypath> <mypy-target...>
  local mp="$1"; shift
  echo "mypy: $* (MYPYPATH=$mp)"
  MYPYPATH="$mp" mypy "$@" || fail=1
}

run scripts/lib            scripts/lib
run scripts/security       scripts/security
run scripts/editorial      scripts/editorial
run scripts/dev            scripts/dev
run scripts/i18n           scripts/i18n
run scripts/generators     -p build_translations
run scripts/postbuild:scripts/lib  scripts/postbuild/postbuild_lib

if [[ "$fail" -ne 0 ]]; then
  echo "✗ mypy strict tier has errors" >&2
  exit 1
fi
echo "✓ mypy strict tier clean"
