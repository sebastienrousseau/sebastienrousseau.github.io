#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Record the true pixel size of every stock image the site uses.

Pages name stock photos as ``https://cloudcdn.pro/stocks/images/<stem>.webp``
or one of its ``-320/-640/-1200/-1920`` variants, and their ``<img>`` tags
declare a width and height from front matter or a postbuild default. Those
guesses were wrong (a 2584x1597 photo shipped as 1200x675, 1600x1000 or
800x800), so the browser reserved the wrong box before the image arrived.

This script reads the first 64 bytes of each original over an HTTP Range
request, parses the WebP header and writes ``_data/stock_image_dims.json``
(``{stem: [width, height]}``). ``postbuild_lib.image_ratio`` then corrects
every stock ``<img>`` to the real aspect ratio. Run it after adding a new
banner; ``tests/unit/test_stock_image_dims.py`` fails until you do.

    python3 scripts/editorial/stock_image_dims.py           # add missing stems
    python3 scripts/editorial/stock_image_dims.py --refresh # re-read all
"""

from __future__ import annotations

import argparse
import json
import re
import struct
import sys
import urllib.request
from collections.abc import Callable, Iterable
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "_data" / "stock_image_dims.json"
BASE = "https://cloudcdn.pro/stocks/images/"
SOURCES = ("_posts", "_data", "scripts/generators")
STOCK_URL_RE = re.compile(
    r"https://cloudcdn\.pro/stocks/images/([A-Za-z0-9_.-]+?)(?:-(?:320|640|1200|1920))?\.webp"
)


def webp_size(header: bytes) -> tuple[int, int]:
    """(width, height) from the first 30 bytes of a WebP file."""
    if header[:4] != b"RIFF" or header[8:12] != b"WEBP":
        raise ValueError("not a WebP file")
    chunk = header[12:16]
    if chunk == b"VP8X":
        w = int.from_bytes(header[24:27], "little") + 1
        h = int.from_bytes(header[27:30], "little") + 1
        return w, h
    if chunk == b"VP8 ":
        w, h = struct.unpack("<HH", header[26:30])
        return w & 0x3FFF, h & 0x3FFF
    if chunk == b"VP8L":
        bits = int.from_bytes(header[21:25], "little")
        return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
    raise ValueError(f"unknown WebP chunk {chunk!r}")


def referenced_stems(root: Path = ROOT) -> set[str]:
    """Every stock stem named under the content and data sources."""
    stems: set[str] = set()
    for source in SOURCES:
        for path in (root / source).rglob("*"):
            if path.suffix in {".md", ".json", ".yml", ".yaml", ".py", ".html"}:
                text = path.read_text(encoding="utf-8", errors="ignore")
                stems.update(STOCK_URL_RE.findall(text))
    return stems


def fetch_header(stem: str) -> bytes:  # pragma: no cover - network
    req = urllib.request.Request(
        f"{BASE}{stem}.webp",
        headers={"Range": "bytes=0-63", "User-Agent": "sebastienrousseau.com-build"},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return bytes(resp.read(64))


def update(
    current: dict[str, list[int]],
    stems: Iterable[str],
    fetch: Callable[[str], bytes] = fetch_header,
) -> tuple[dict[str, list[int]], list[str]]:
    """Add each stem's size; return the new manifest and the stems that failed."""
    out = dict(current)
    failed: list[str] = []
    for stem in sorted(stems):
        try:
            out[stem] = list(webp_size(fetch(stem)))
        except (OSError, ValueError) as exc:
            print(f"stock_image_dims: {stem}: {exc}", file=sys.stderr)
            failed.append(stem)
    return dict(sorted(out.items())), failed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--refresh", action="store_true", help="re-read every stem")
    args = parser.parse_args(argv)
    current = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {}
    wanted = referenced_stems()
    todo = wanted if args.refresh else wanted - current.keys()
    manifest, failed = update(current, todo)
    MANIFEST.write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    print(
        f"stock_image_dims: {len(manifest)} stems, {len(todo) - len(failed)} read, {len(failed)} failed"
    )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
