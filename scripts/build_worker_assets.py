#!/usr/bin/env python3
"""Emit static JSON assets the lang-router Worker reads at runtime.

Cloudflare KV Free tier allows 1,000 writes/day. To avoid running into that
limit, anything that can be computed at deploy time goes into the Worker's
``[assets]`` binding instead. The Worker serves these files edge-local with
no KV touch and no Worker compute beyond a single fetch.

Currently emitted:
  - lang-registry.json  — active locale codes the lang-router routes to.

Adding a new asset:
  1. Add a builder function below.
  2. Call it from ``main()``.
  3. Update ``project-docs/adr/0001-kv-free-tier-policy.md`` if the new
     asset replaces a runtime KV read.

Run from repo root: ``python3 scripts/build_worker_assets.py``.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

import _lang_registry as registry

OUT_DIR = ROOT / "worker-assets"


def emit_lang_registry() -> Path:
    """Write the active-locale routing table the Worker uses to decide
    whether ``/fr/foo`` is a valid pre-existing locale subtree."""
    active = [lang.code for lang in registry.active()]
    payload = {
        "version": 1,
        "active": active,
    }
    out = OUT_DIR / "lang-registry.json"
    out.write_text(json.dumps(payload, separators=(",", ":")) + "\n", encoding="utf-8")
    return out


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    written = [emit_lang_registry()]
    for path in written:
        rel = path.relative_to(ROOT)
        print(f"wrote {rel} ({path.stat().st_size} B)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
