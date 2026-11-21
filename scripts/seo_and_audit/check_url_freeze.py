#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""URL freeze (ADR-0015): fail when a change moves or removes a published URL.

A page's URL comes from its file under ``_posts/`` (EN at the root, each
locale in ``_posts/<lang>/``) and from the slug maps in
``_data/i18n/<lang>/slugs.json``. Against a base ref (``origin/main`` by
default; CI passes the PR's base), this reports:

* a ``_posts`` Markdown file deleted or renamed;
* a ``slugs.json`` entry (article or static page) whose value changed or
  that was removed.

Adding pages is fine. There is no allowlist: a published URL that must
change needs the ADR to be amended first.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout


def moved_posts(base: str, head: str = "HEAD") -> list[str]:
    """``_posts`` Markdown files deleted or renamed between base and head."""
    out = _git("diff", "--name-status", "-M", "--diff-filter=DR", base, head, "--", "_posts")
    problems = []
    for line in out.splitlines():
        status, *paths = line.split("\t")
        if not paths[0].endswith(".md"):
            continue
        if status.startswith("R"):
            problems.append(f"renamed {paths[0]} -> {paths[1]}")
        else:
            problems.append(f"deleted {paths[0]}")
    return problems


def _slug_values(raw: str) -> dict[str, str]:
    data = json.loads(raw) if raw.strip() else {}
    flat = {}
    for section, entries in data.items():
        if isinstance(entries, dict):
            for key, value in entries.items():
                if isinstance(value, str):
                    flat[f"{section}.{key}"] = value
    return flat


def changed_slugs(base: str, head: str = "HEAD") -> list[str]:
    """Slug-map entries that changed value or vanished between base and head."""
    files = _git("ls-tree", "-r", "--name-only", base, "--", "_data/i18n").split()
    problems = []
    for rel in (f for f in files if f.endswith("/slugs.json")):
        old = _slug_values(_git("show", f"{base}:{rel}"))
        try:
            new = _slug_values(_git("show", f"{head}:{rel}"))
        except subprocess.CalledProcessError:
            new = {}
        for key, value in old.items():
            if new.get(key) != value:
                problems.append(f"{rel}: {key} {value} -> {new.get(key, '(removed)')}")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--base", default="origin/main", help="ref holding the published URLs")
    ap.add_argument("--head", default="HEAD")
    args = ap.parse_args(argv)
    problems = moved_posts(args.base, args.head) + changed_slugs(args.base, args.head)
    for p in problems[:50]:
        print(f"::error::URL freeze (ADR-0015): {p}")
    print(f"check_url_freeze: {len(problems)} published URL change(s) against {args.base}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
