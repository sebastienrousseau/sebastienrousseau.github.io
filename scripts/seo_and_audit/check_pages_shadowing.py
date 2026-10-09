#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Fail when a project GitHub Pages site shadows a path this site publishes.

A repository of the same owner with GitHub Pages enabled is served at
``<user site>/<repo-name>/``, and GitHub routes that path to the project
site before this one. On 2026-10-07 ``sebastienrousseau.com/iso20022-mcp/``
answered "Site not found · GitHub Pages" because the ``iso20022-mcp``
repository had Pages switched on with nothing deployed. The build and the
deploy were both green; only the live path was gone.

Inputs: a file of repository names that have Pages enabled (one per line,
from ``gh api users/<owner>/repos``) and the site's sitemap as a file (the
workflow fetches it with curl, so this script never touches the network).
Exit 1 names every collision; exit 0 otherwise.

Usage:
    check_pages_shadowing.py --repos FILE --sitemap FILE [--self NAME]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

_LOC_RE = re.compile(r"<loc>\s*([^<\s]+)\s*</loc>")


def top_level_paths(sitemap_xml: str) -> set[str]:
    """First path segment of every URL in a sitemap, lower-cased."""
    out: set[str] = set()
    for loc in _LOC_RE.findall(sitemap_xml):
        segment = urlparse(loc).path.strip("/").split("/", 1)[0]
        if segment:
            out.add(segment.lower())
    return out


def shadowed(pages_repos: list[str], published: set[str], self_repo: str) -> list[str]:
    """Repos with Pages whose name is a published top-level path."""
    names = {r.strip().lower() for r in pages_repos if r.strip()}
    names.discard(self_repo.lower())
    return sorted(names & published)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--repos", required=True, help="file: repo names with Pages enabled")
    ap.add_argument("--sitemap", required=True, help="sitemap file")
    ap.add_argument("--self", dest="self_repo", default="sebastienrousseau.github.io")
    args = ap.parse_args(argv)

    repos = Path(args.repos).read_text(encoding="utf-8").splitlines()
    published = top_level_paths(Path(args.sitemap).read_text(encoding="utf-8"))
    if not published:
        print("::error::the sitemap yielded no paths; refusing to report a pass")
        return 1
    hits = shadowed(repos, published, args.self_repo)
    print(f"{len(repos)} repo(s) with Pages, {len(published)} published top-level path(s)")
    for name in hits:
        print(
            f"::error::/{name}/ is published by this site but the repository "
            f"'{name}' has GitHub Pages enabled, so GitHub serves that path from "
            "the project site instead. Disable Pages on that repository."
        )
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
