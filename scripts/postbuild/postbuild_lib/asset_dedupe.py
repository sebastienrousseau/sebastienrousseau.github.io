# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Collapse byte-identical ``/_csp/`` assets onto one URL.

Every layout embeds the site stylesheet inline, and ssg extracts each layout's
block to its own fingerprinted file. The fingerprint is per-layout, not
per-content, so identical CSS shipped under several URLs and a reader crossing
between page types re-downloaded ~25 KB gzipped of bytes they already had.

The worst case was subtle. ``--accent`` was a per-page template variable
(``rgb({{theme-color}})``) sitting *inside* the shared block, which made the
whole ~138 KB stylesheet page-variable: ssg emitted a separate full copy per
distinct accent — two 138 KB bundles differing in six bytes, covering 82 % of
pages between them. Splitting the accent into its own tiny block (see the
second ``<style>`` in ``_layouts/*.html``) made the big blocks byte-identical,
but ssg still fingerprints them separately.

This pass is the other half: hash the actual bytes, keep one file per distinct
hash, delete the rest, and rewrite every reference. Content-addressed, so it
cannot change rendering — the bytes a page gets are identical either way.

Idempotent: a second run finds no duplicates.
"""

from __future__ import annotations

import hashlib
import re
from collections import defaultdict
from pathlib import Path

_ASSET_DIR = "_csp"
_SUFFIXES = (".css", ".js")


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def find_duplicate_assets(public: Path) -> dict[str, str]:
    """``{duplicate_url: canonical_url}`` for byte-identical assets.

    The lexicographically-first filename in each group wins, so the surviving
    URL is stable across rebuilds — the reproducibility gate compares trees.
    """
    asset_dir = public / _ASSET_DIR
    if not asset_dir.is_dir():
        return {}
    by_hash: dict[str, list[Path]] = defaultdict(list)
    for path in sorted(asset_dir.iterdir()):
        if path.is_file() and path.suffix in _SUFFIXES:
            by_hash[_digest(path)].append(path)

    mapping: dict[str, str] = {}
    for paths in by_hash.values():
        if len(paths) < 2:
            continue
        keeper, *dupes = paths
        for dupe in dupes:
            mapping[f"/{_ASSET_DIR}/{dupe.name}"] = f"/{_ASSET_DIR}/{keeper.name}"
    return mapping


def rewrite_asset_refs(html: str, mapping: dict[str, str]) -> str:
    """Point every duplicate asset reference at its canonical twin."""
    if not mapping:
        return html
    pattern = re.compile("|".join(re.escape(u) for u in sorted(mapping, key=len, reverse=True)))
    return pattern.sub(lambda m: mapping[m.group(0)], html)


def remove_duplicate_files(public: Path, mapping: dict[str, str]) -> int:
    """Delete the now-unreferenced duplicates. Returns the count removed."""
    removed = 0
    for url in mapping:
        path = public / url.lstrip("/")
        if path.is_file():
            path.unlink()
            removed += 1
    return removed
