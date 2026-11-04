#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Emit static JSON assets the lang-router Worker reads at runtime.

Cloudflare KV Free tier allows 1,000 writes/day. To avoid running into that
limit, anything that can be computed at deploy time goes into the Worker's
``[assets]`` binding instead. The Worker serves these files edge-local with
no KV touch and no Worker compute beyond a single fetch.

Currently emitted:
  - lang-registry.json: active locale codes the lang-router routes to.
  - redirects.json: every meta-refresh redirect stub in the built
    ``public/`` (renamed locale article slugs, ADR-0012, plus the static
    /papers -> /research move), mapped old path -> final path with chains
    collapsed, so the Worker can answer each with one 301. Derived from the
    built stubs rather than from ``_data/redirects/articles.json`` because
    postbuild only materialises a stub when its target renders and its
    source does not: the build output is the ground truth. Skipped (the
    committed file is kept) when ``public/`` has not been built.

Adding a new asset:
  1. Add a builder function below.
  2. Call it from ``main()``.
  3. Update ``docs/adr/0001-kv-free-tier-policy.md`` if the new
     asset replaces a runtime KV read.

Run from repo root: ``python3 scripts/build_worker_assets.py``.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

import _lang_registry as registry

OUT_DIR = ROOT / "worker-assets"
PUBLIC = ROOT / "public"
SITE = "https://sebastienrousseau.com"

# postbuild_lib.redirects injects the refresh tag directly after <head>, so
# it is always inside the first few KB of a stub page.
_HEAD_BYTES = 16384
_REFRESH_RE = re.compile(
    r'<meta\s+http-equiv=["\']?refresh["\']?\s+content=["\']?\d+;\s*url=([^"\'\s>]+)',
    re.IGNORECASE,
)


class RedirectMapError(ValueError):
    """Raised when the stubs form a loop or point off-site."""


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


def _page_path(rel: str) -> str:
    """``fr/old/index.html`` -> ``/fr/old/``."""
    return "/" + rel.removesuffix("index.html")


def _target_path(url: str, source: str) -> str:
    """Site-relative path of a refresh target, which must be on this site."""
    if url.startswith(SITE + "/"):
        return url[len(SITE) :]
    if url.startswith("/"):
        return url
    raise RedirectMapError(f"{source}: refresh target {url!r} is not on {SITE}")


def stub_redirects(public: Path = PUBLIC) -> dict[str, str]:
    """``{stub path: refresh target path}`` for every redirect stub page."""
    out: dict[str, str] = {}
    for page in sorted(public.rglob("index.html")):
        with page.open("r", encoding="utf-8", errors="ignore") as fh:
            m = _REFRESH_RE.search(fh.read(_HEAD_BYTES))
        if m:
            source = _page_path(page.relative_to(public).as_posix())
            out[source] = _target_path(m.group(1), source)
    return out


def collapse_chains(redirects: dict[str, str]) -> dict[str, str]:
    """Point every source straight at its final target. Raises on a loop."""
    out: dict[str, str] = {}
    for source in redirects:
        seen = {source}
        target = redirects[source]
        while target in redirects:
            if target in seen:
                raise RedirectMapError(f"redirect loop through {source}")
            seen.add(target)
            target = redirects[target]
        out[source] = target
    return out


def emit_redirects(public: Path = PUBLIC) -> Path | None:
    """Write ``redirects.json`` from the built stubs; None when unbuilt."""
    if not (public / "index.html").is_file():
        return None
    redirects = collapse_chains(stub_redirects(public))
    payload = {"version": 1, "redirects": dict(sorted(redirects.items()))}
    out = OUT_DIR / "redirects.json"
    out.write_text(
        json.dumps(payload, separators=(",", ":"), ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return out


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    written = [emit_lang_registry()]
    redirects = emit_redirects()
    if redirects is None:
        print("skip worker-assets/redirects.json: public/ not built, committed map kept")
    else:
        written.append(redirects)
    for path in written:
        rel = path.relative_to(ROOT)
        print(f"wrote {rel} ({path.stat().st_size} B)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
