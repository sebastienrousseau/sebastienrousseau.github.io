#!/usr/bin/env bash
# Regenerate the hash-pinned dependency locks consumed by CI and the Fly
# PDF container with `pip install --require-hashes` (OpenSSF Scorecard
# Pinned-Dependencies). Run this whenever requirements.txt,
# requirements-dev.txt, or fly/pdf-render/requirements.txt changes.
#
#   scripts/security/lock-deps.sh
#
# Locks are universal (every platform's wheel hash) so the same file
# verifies on Linux CI and local macOS. CI Python is 3.12; the Fly image
# is 3.13 — each lock is compiled for its target interpreter.
set -euo pipefail

cd "$(dirname "$0")/../.."

command -v uv >/dev/null 2>&1 || {
  echo "error: uv not on PATH (https://docs.astral.sh/uv/)" >&2
  exit 1
}

echo "→ requirements.lock (runtime, py3.12)"
uv pip compile requirements.txt \
  --universal --generate-hashes --python-version 3.12 \
  --output-file requirements.lock

echo "→ requirements-dev.lock (runtime + CI tooling, py3.12)"
uv pip compile requirements.txt requirements-dev.txt \
  --universal --generate-hashes --python-version 3.12 \
  --output-file requirements-dev.lock

echo "→ fly/pdf-render/requirements.lock (runtime, py3.13)"
uv pip compile fly/pdf-render/requirements.txt \
  --universal --generate-hashes --python-version 3.13 \
  --output-file fly/pdf-render/requirements.lock

echo "✓ locks regenerated"
