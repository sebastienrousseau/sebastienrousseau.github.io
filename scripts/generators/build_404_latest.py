#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""List the three newest English articles on the 404 page (plan F-8).

``_posts/404.md`` carries the marker ``<!-- 404:latest -->`` under its
search box and key links. This step replaces it, in the build copy only,
with a list of the three newest dated English articles, so a reader who
followed a dead link still finds current writing. ``--dir`` is required,
with no default (ADR-0003): build.sh passes ``_posts_build``.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

MARKER = "<!-- 404:latest -->"
COUNT = 3
_DATED_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-")
_TITLE_RE = re.compile(r'^title:\s*"((?:[^"\\]|\\.)*)"\s*$', re.M)


def newest(posts: Path, count: int = COUNT) -> list[tuple[str, str]]:
    """(slug, title) of the newest dated English articles, newest first."""
    out: list[tuple[str, str]] = []
    for path in sorted(posts.glob("*.md"), reverse=True):
        if not _DATED_RE.match(path.name):
            continue
        m = _TITLE_RE.search(path.read_text(encoding="utf-8")[:4000])
        if m:
            out.append((path.stem, m.group(1).replace('\\"', '"')))
        if len(out) == count:
            break
    return out


def render(items: list[tuple[str, str]]) -> str:
    links = "".join(
        f'<li><a href="/{slug}/index.html">{html.escape(title, quote=False)}</a></li>'
        for slug, title in items
    )
    return f'<ul class="ap-404-latest">{links}</ul>'


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dir", required=True, type=Path, help="posts directory (build copy)")
    args = parser.parse_args(argv)
    target = args.dir / "404.md"
    text = target.read_text(encoding="utf-8")
    if MARKER not in text:
        print(f"build_404_latest: {MARKER} not found in {target}", file=sys.stderr)
        return 1
    target.write_text(text.replace(MARKER, render(newest(args.dir))), encoding="utf-8")
    print(f"build_404_latest: listed {COUNT} newest articles in {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
