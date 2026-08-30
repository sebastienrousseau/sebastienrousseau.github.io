#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Backfill a ``permalink:`` front-matter field into any post that lacks
one, at build time, inside the temporary build directory.

Why: ssg >= 0.0.45 tightened RSS validation — every post that emits a
feed must carry a channel ``<link>``, which ssg derives from the post's
``permalink``. The archive's older locale posts (2018–2024) predate the
permalink convention and carry only minimal front matter, so a 0.0.46
build aborts with ``RSS generation failed: channel.link is missing``.
ssg 0.0.44 tolerated the gap; 0.0.46 does not (see ADR-0002).

Rather than editing ~960 committed source files, this runs on the build
copy (``--dir _posts_build``) alongside ``regen_slug_maps`` /
``post_enrich`` and derives the permalink deterministically from the
file's locale directory and slug (its filename). Source stays untouched;
the derived permalink matches the URL the post is already served at:

    EN     _posts_build/<slug>.md            -> https://sebastienrousseau.com/<slug>
    locale _posts_build/<lang>/<slug>.md      -> https://sebastienrousseau.com/<lang>/<slug>

Idempotent: a post that already declares ``permalink:`` is left as-is.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

BASE_URL = "https://sebastienrousseau.com"

# The 34 active translation locales (dirs under _posts/). Kept in sync with
# _lang_registry.py; a directory not in this set is treated as EN content.
LOCALES = {
    "ar",
    "bn",
    "cs",
    "de",
    "el",
    "es",
    "fa",
    "fil",
    "fr",
    "ha",
    "he",
    "hi",
    "hu",
    "id",
    "it",
    "ja",
    "ko",
    "mr",
    "ms",
    "nl",
    "pl",
    "pt-br",
    "ro",
    "ru",
    "sv",
    "ta",
    "te",
    "th",
    "tr",
    "uk",
    "vi",
    "yo",
    "zh-hans",
    "zh-hant",
}


def _has_frontmatter(text: str) -> bool:
    return text.startswith("---\n") or text.startswith("---\r\n")


def _frontmatter_has_permalink(text: str) -> bool:
    """True if the first front-matter block declares a ``permalink:`` key."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return False
    for line in lines[1:]:
        if line.strip() == "---":
            return False
        if line.startswith("permalink:"):
            return True
    return False


def _permalink_for(md: Path, root: Path) -> str:
    """Derive the canonical permalink from the post's locale + slug."""
    slug = md.stem
    rel_parent = md.parent.relative_to(root)
    first = rel_parent.parts[0] if rel_parent.parts else ""
    if first in LOCALES:
        return f"{BASE_URL}/{first}/{slug}"
    return f"{BASE_URL}/{slug}"


def _insert_permalink(text: str, permalink: str) -> str:
    """Insert the permalink line immediately after the opening ``---``."""
    newline = "\r\n" if text.startswith("---\r\n") else "\n"
    marker = f"---{newline}"
    rest = text[len(marker) :]
    return f'{marker}permalink: "{permalink}"{newline}{rest}'


def backfill(root: Path) -> int:
    count = 0
    for md in sorted(root.rglob("*.md")):
        if md.name == "README.md":
            continue
        text = md.read_text(encoding="utf-8")
        if not _has_frontmatter(text) or _frontmatter_has_permalink(text):
            continue
        permalink = _permalink_for(md, root)
        md.write_text(_insert_permalink(text, permalink), encoding="utf-8")
        count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dir",
        default="_posts_build",
        help="Build directory to process (default: _posts_build).",
    )
    args = parser.parse_args()
    root = Path(args.dir)
    if not root.is_dir():
        print(f"backfill_permalink: {root} is not a directory", file=sys.stderr)
        return 1
    count = backfill(root)
    print(f"backfill_permalink: added permalink to {count} post(s) in {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
