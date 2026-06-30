#!/usr/bin/env bash
# Generate + validate a CycloneDX SBOM of the RUNTIME build dependencies.
#
# improvement-plan-2026.md Phase 2.1 / ADR-0004. The site is built by the
# Python pipeline in requirements.txt (plus the ssg Rust toolchain, pinned in
# ADR-0002). This emits a CycloneDX SBOM of the *resolved runtime* Python deps
# — installed into a throwaway venv so dev/test tooling (ruff, mypy, pytest)
# never pollutes the artifact — to public/sbom.cdx.json for downstream audits.
#
# Usage: scripts/security/gen-sbom.sh [output_path]   (default: public/sbom.cdx.json)
set -euo pipefail

OUT="${1:-public/sbom.cdx.json}"
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

if ! command -v cyclonedx-py >/dev/null 2>&1; then
  echo "error: cyclonedx-py not on PATH (pip install cyclonedx-bom)" >&2
  exit 1
fi

tmp_venv="$(mktemp -d)/sbom-venv"
trap 'rm -rf "$(dirname "$tmp_venv")"' EXIT

python3 -m venv "$tmp_venv"
"$tmp_venv/bin/pip" install --quiet --upgrade pip >/dev/null
"$tmp_venv/bin/pip" install --quiet -r requirements.txt

mkdir -p "$(dirname "$OUT")"
cyclonedx-py environment "$tmp_venv/bin/python" --output-format JSON -o "$OUT"

# Validate: the deployed SBOM must be well-formed CycloneDX, list every
# declared runtime dependency, and carry a version for every component.
python3 - "$OUT" <<'PY'
import json, sys
REQUIRED = {"pyyaml", "markdown-it-py", "rjsmin", "rcssmin"}
d = json.load(open(sys.argv[1]))
assert d.get("bomFormat") == "CycloneDX", f"bad bomFormat: {d.get('bomFormat')!r}"
assert d.get("specVersion"), "missing specVersion"
comps = d.get("components", [])
assert comps, "no components"
names = {c["name"].lower() for c in comps}
missing = REQUIRED - names
assert not missing, f"SBOM missing runtime deps: {sorted(missing)}"
unversioned = [c["name"] for c in comps if not c.get("version")]
assert not unversioned, f"components without version: {unversioned}"
print(f"SBOM ok: CycloneDX {d['specVersion']}, {len(comps)} components, all versioned -> {sys.argv[1]}")
PY
