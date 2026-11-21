#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Fail when committed content links to a retired URL; ``--fix`` rewrites it.

``worker-assets/redirects.json`` maps every retired path to its final
target. The Worker answers those paths with one 301, and a postbuild pass
rewrites links in the built HTML, but the Markdown sources kept the old
URLs: llms-full.txt is built from them, front-matter ``id`` and
``permalink`` named old slugs, and every crawl of a stale link costs a
redirect hop. This check scans the content sources and reports each link
whose target is a redirect source. ``--fix`` rewrites it to the final URL,
keeping the link's own style (``/index.html``, a trailing slash, or
neither).

Matched forms, so prose and regex patterns are left alone: ``](url``,
``href="url"`` (also JSON-escaped), Markdown reference definitions
``[x]: url``, and absolute ``https://sebastienrousseau.com/...`` URLs.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REDIRECTS = ROOT / "worker-assets" / "redirects.json"
SCOPE = ("_posts", "_drafts", "_layouts", "_includes", "_data/i18n")
_DOMAIN = r"https?://(?:www\.)?sebastienrousseau\.com"
LINK_RE = re.compile(
    rf"((?:\]\(|href=\\?\"|href='|^\[[^\]]+\]:\s*|{_DOMAIN})(?:{_DOMAIN})?)"
    r"(/[A-Za-z0-9%._~-]+(?:/[A-Za-z0-9%._~-]+)*?)(/index\.html|/)?"
    r"(?=[)\"'\s#?>\\]|$)",
    re.M,
)


def load_map(path: Path = REDIRECTS) -> dict[str, str]:
    """Retired path (with trailing slash) -> final target path."""
    return json.loads(path.read_text(encoding="utf-8"))["redirects"]


def rewrite(text: str, redirects: dict[str, str]) -> tuple[str, list[str]]:
    """``text`` with stale links rewritten, and the retired paths found."""
    found: list[str] = []

    def sub(m: re.Match[str]) -> str:
        target = redirects.get(m.group(2) + "/")
        if target is None:
            return m.group(0)
        found.append(m.group(2) + "/")
        if m.group(3) == "/index.html":
            return m.group(1) + target + "index.html"
        return m.group(1) + (target if m.group(3) == "/" else target.rstrip("/"))

    return LINK_RE.sub(sub, text), found


def content_files(root: Path = ROOT) -> list[Path]:
    """Tracked content sources: Markdown, HTML and i18n JSON (not slug maps)."""
    out = subprocess.run(
        ["git", "ls-files", *SCOPE], cwd=root, capture_output=True, text=True, check=True
    ).stdout.split()
    return [
        root / f
        for f in out
        if f.endswith((".md", ".html", ".json")) and not f.endswith("slugs.json")
    ]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--fix", action="store_true", help="rewrite stale links in place")
    args = ap.parse_args(argv)
    redirects = load_map()
    total = files = 0
    for path in content_files():
        text = path.read_text(encoding="utf-8")
        out, found = rewrite(text, redirects)
        if not found:
            continue
        files += 1
        total += len(found)
        if args.fix:
            path.write_text(out, encoding="utf-8")
        elif files <= 20:
            print(f"{path.relative_to(ROOT)}: {', '.join(sorted(set(found))[:3])}")
    verb = "rewrote" if args.fix else "found"
    print(f"check_stale_links: {verb} {total} stale link(s) in {files} file(s)")
    return 0 if args.fix or total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
