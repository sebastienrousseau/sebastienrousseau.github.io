#!/usr/bin/env python3
"""Replace the legacy "Shokunin" brand name with "Static Site Generator" (SSG).

URL paths, GitHub repo names, package names, asset paths and short-form code
identifiers stay as ``shokunin`` because they refer to immutable resources
(the published Rust crate, the GitHub repository, the on-CDN logo file). Only
prose mentions and human-facing labels are renamed.

Rules (applied in order):

  1. ``Shokunin SSG`` → ``Static Site Generator (SSG)``
  2. ``Shokunin Static Site Generator`` → ``Static Site Generator``
  3. ``Made with Shokunin`` → ``Made with Static Site Generator``
  4. ``Powered by Shokunin`` → ``Powered by the Static Site Generator``
  5. Standalone ``Shokunin`` (Title-cased, word boundary) → ``Static Site Generator``
  6. Standalone ``shokunin`` (lower-cased, but ONLY inside human-readable
     prose — never inside URLs, ``href=…``, ``src=…``, JSON values or paths).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TARGETS = [
    "_posts",
    "_drafts",
    "_layouts",
]
EXTRA_FILES = [
    "Makefile",
    "build.sh",
    "scripts/postbuild.py",
    "scripts/gen_articles.py",
    "scripts/gen_projects.py",
    "scripts/gen_papers.py",
    "scripts/gen_layouts.py",
    "scripts/fix_seo_meta.py",
    "scripts/fix_cdn_urls.py",
]
EXTENSIONS = {".md", ".html", ".js", ".py", ".sh"}

# Lowercase "shokunin" surrounded by characters that are part of a URL or path:
# `/`, `.`, `-`, `_`, `:`, or it sits inside an obvious href/src attribute. We
# match by demanding that neither neighbour is one of those "URL-ish" chars.
URLISH = r"[A-Za-z0-9/._\-:]"
LOWER_PROSE = re.compile(rf"(?<!{URLISH})shokunin(?!{URLISH})")


def transform(text: str) -> str:
    # Order matters: longer phrases first so they don't get sub-matched.
    text = re.sub(r"\bShokunin SSG\b", "Static Site Generator (SSG)", text)
    text = re.sub(r"\bShokunin Static Site Generator\b", "Static Site Generator", text)
    text = re.sub(r"\bMade with Shokunin\b", "Made with Static Site Generator", text)
    text = re.sub(r"\bPowered by Shokunin\b", "Powered by the Static Site Generator", text)
    # Generic Title-cased standalone "Shokunin"
    text = re.sub(r"\bShokunin\b", "Static Site Generator", text)
    # Lowercase "shokunin" in prose only (not inside URLs/paths)
    text = LOWER_PROSE.sub("Static Site Generator", text)
    return text


def file_targets() -> list[Path]:
    out: list[Path] = []
    for d in TARGETS:
        base = REPO / d
        if not base.is_dir():
            continue
        for p in base.rglob("*"):
            if p.is_file() and p.suffix in EXTENSIONS:
                out.append(p)
    for rel in EXTRA_FILES:
        p = REPO / rel
        if p.is_file():
            out.append(p)
    return sorted(set(out))


def main() -> int:
    changed = 0
    total_subs = 0
    for path in file_targets():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        new = transform(text)
        if new == text:
            continue
        # Count substitutions for the report.
        delta = text.count("Shokunin") - new.count("Shokunin")
        delta += text.count("shokunin") - new.count("shokunin")
        path.write_text(new, encoding="utf-8")
        changed += 1
        total_subs += delta
        print(f"  {path.relative_to(REPO)}: {delta} sub(s)")
    print(f"rewrote {total_subs} occurrence(s) across {changed} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
