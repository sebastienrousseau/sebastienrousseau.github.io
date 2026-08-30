#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""SRI correctness gate — every Subresource Integrity hash must match the
file it guards.

`build.sh` replaces the SSG's placeholder ``integrity="sha256-<short>"`` with
a real base64 SHA-256 computed from the asset's bytes, so browsers enforce SRI
on every ``/_csp/*`` asset. Existing tests only check the token is *base64-
shaped*; this one recomputes the digest from the actual file and fails on any
**mismatch or unresolvable reference** — the failure mode where a stale hash
makes the browser silently refuse to load the script/style.

Properties enforced across every rendered page:
1. Every tag carrying ``integrity="sha256-…"`` with a local ``src``/``href``
   resolves to a file on disk.
2. The integrity digest equals base64(sha256(file bytes)).

Run from repo root: ``python3 tests/validation/test_sri_integrity.py``.
Exit 0 = clean, 1 = mismatches found.
"""

from __future__ import annotations

import base64
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"

# Tags that carry both a local reference and an integrity attribute, in either
# attribute order (minifier emits both). Capture the url + the sha256 token.
_TAG_RE = re.compile(r"<(?:script|link)\b[^>]*>", re.IGNORECASE)
_URL_RE = re.compile(r'(?:src|href)=(["\'])(?P<url>[^"\']+)\1', re.IGNORECASE)
_INTEGRITY_RE = re.compile(r'integrity=(["\'])(?P<val>[^"\']+)\1', re.IGNORECASE)
_SHA256_RE = re.compile(r"sha256-([A-Za-z0-9+/=]+)")


def _b64_sha256(data: bytes) -> str:
    return base64.b64encode(hashlib.sha256(data).digest()).decode("ascii")


def _resolve(url: str, public_dir: Path) -> Path | None:
    """Map a page-local URL to a file under public_dir. External URLs and
    data: URIs return None (not our integrity to check)."""
    if url.startswith(("http://", "https://", "//", "data:", "mailto:")):
        return None
    path = url.split("?", 1)[0].split("#", 1)[0]
    if path.startswith("/"):
        return public_dir / path.lstrip("/")
    return None  # relative refs are rare here; absolute-from-root is the contract


def find_sri_mismatches(public_dir: Path) -> list[str]:
    """Return a list of human-readable defects. Empty list = all SRI valid."""
    defects: list[str] = []
    for html in public_dir.rglob("*.html"):
        text = html.read_text(encoding="utf-8", errors="replace")
        for tag in _TAG_RE.findall(text):
            integ = _INTEGRITY_RE.search(tag)
            url = _URL_RE.search(tag)
            if not integ or not url:
                continue
            m = _SHA256_RE.search(integ.group("val"))
            if not m:
                continue  # non-sha256 algo — out of scope here
            target = _resolve(url.group("url"), public_dir)
            if target is None:
                continue  # external resource — SRI optional, can't verify locally
            rel = html.relative_to(public_dir)
            if not target.is_file():
                defects.append(f"{rel}: integrity on missing asset {url.group('url')}")
                continue
            actual = _b64_sha256(target.read_bytes())
            if actual != m.group(1):
                defects.append(
                    f"{rel}: SRI mismatch for {url.group('url')} "
                    f"(attr sha256-{m.group(1)[:12]}… != file sha256-{actual[:12]}…)"
                )
    return defects


def main() -> int:
    if not PUBLIC.is_dir():
        print("public/ not built — run ./build.sh first", file=sys.stderr)
        return 0  # nothing to check; build.sh runs this only after a build
    defects = find_sri_mismatches(PUBLIC)
    if defects:
        print(f"SRI integrity check FAILED — {len(defects)} defect(s):")
        for d in defects[:50]:
            print(f"  {d}")
        return 1
    print("SRI integrity: all integrity hashes match their assets.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
