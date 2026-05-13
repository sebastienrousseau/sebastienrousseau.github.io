#!/usr/bin/env python3
"""Rewrite legacy kura.pro / cloudcdn.pro URLs to the current cloudcdn.pro layout.

For every ``https://kura.pro/...`` or ``https://cloudcdn.pro/...`` URL discovered
in the project's source files, derive candidate target paths against the local
CDN checkout (``/Users/seb/Code/Public/CDN/cloudcdn.pro``) and apply the first
candidate that exists on disk. URLs whose target cannot be resolved are
reported but left untouched so the build still passes.

New CDN conventions (see /Users/seb/Code/Public/CDN/cloudcdn.pro):

  - per-project assets live under ``clients/<project>/v1/...``
  - shared assets live under ``clients/common/...``
  - stock photography / diagrams live under ``stocks/{images,diagrams}/...``
  - legacy ``kura.pro/<project>/images/<rest>`` ≡ ``clients/<project>/v1/<rest>``
  - logo SVGs replaced WebP/PNG bitmaps where available
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CDN_ROOT = Path("/Users/seb/Code/Public/CDN/cloudcdn.pro")
SOURCE_GLOBS = ("_posts/**/*.md", "_layouts/**/*.html", "_layouts/**/*.js",
                "scripts/**/*.py", "_drafts/**/*.md", "*.md", "*.html")
URL_RE = re.compile(r"https://(?:kura|cloudcdn)\.pro/[^\s\"'<>)\\]+")

# Project codenames that historically used ``/<proj>/images/...`` and now live
# under ``/clients/<proj>/v1/...`` — verified by listing the CDN tree.
PROJECT_PREFIXES = {
    "akande", "alienstudio", "audioanalyser", "audiotextpro", "audiowave",
    "bankingonai", "bankingonquantum", "bankstatementparser", "beonux",
    "cloudcdn", "cmn", "cs50x", "dotfiles", "dtt", "frontmatter-gen", "hsh",
    "html-generator", "http-handle", "kaishi", "kyberlib", "l90s", "langweave",
    "libmake", "libyml", "llamadev", "maccfg", "mdx-gen", "metadata-gen",
    "mini-functions", "nalufx", "neferankh", "noyalib", "nucleusflow", "pain001",
    "password-generator-pro", "pipelines", "pm2md", "publications", "pythondev",
    "qrc", "rlg", "routefinder", "rssgen", "rustdev", "sebastienrousseau",
    "serde_yml", "shokunin", "sinewavegenerator", "sitemap-gen", "skeletonic",
    "vrd",
}

# Brand logos that used to live at /logos/<brand>.webp now live under
# clients/sebastienrousseau/v1/logos.
BRAND_LOGOS = {"akqa", "barclays", "hsbc", "paypal", "shazam", "virgin",
               "capgemini", "rufusleonard"}

EXT_FALLBACKS = (".svg", ".webp", ".png", ".jpg", ".jpeg")


def cdn_has(rel: str) -> bool:
    return (CDN_ROOT / rel).is_file()


def try_ext_variants(rel: str) -> str | None:
    """Try the path as-is, then swap the extension for known fallbacks."""
    if cdn_has(rel):
        return rel
    if "." in Path(rel).name:
        stem = rel.rsplit(".", 1)[0]
        for ext in EXT_FALLBACKS:
            candidate = stem + ext
            if cdn_has(candidate):
                return candidate
    return None


def candidate_paths(url: str) -> list[str]:
    """Generate ordered candidate CDN-relative paths for ``url``."""
    # Strip scheme + host.
    path = re.sub(r"^https://(kura|cloudcdn)\.pro/", "", url)
    cands: list[str] = []

    # Pass-through: already-correct cloudcdn paths.
    cands.append(path)

    # /stock/<x> → /stocks/<x>
    if path.startswith("stock/"):
        cands.append("stocks/" + path[len("stock/"):])
    # /unsplash/images/banners/<x> → /stocks/images/<x>
    if path.startswith("unsplash/images/banners/"):
        cands.append("stocks/images/" + path[len("unsplash/images/banners/"):])
    # /unsplash/images/<x> → /stocks/images/<x>
    elif path.startswith("unsplash/images/"):
        cands.append("stocks/images/" + path[len("unsplash/images/"):])

    # /common/images/<x> → /clients/common/images/<x>
    if path.startswith("common/images/"):
        cands.append("clients/" + path)

    # /clients/common/... is already correct, leave alone.

    # /<brand>.webp or /logos/<brand>.<ext> → /clients/sebastienrousseau/v1/logos/<brand>.<ext>
    m = re.match(r"^logos/([A-Za-z0-9_-]+)\.[a-z]+$", path)
    if m and m.group(1) in BRAND_LOGOS:
        cands.append(f"clients/sebastienrousseau/v1/logos/{m.group(1)}.svg")

    # /<project>/images/<rest> → /clients/<project>/v1/<rest>
    m = re.match(r"^([A-Za-z0-9_-]+)/images/(.+)$", path)
    if m and m.group(1) in PROJECT_PREFIXES:
        cands.append(f"clients/{m.group(1)}/v1/{m.group(2)}")

    # /<project>/v<n>/<rest> → /clients/<project>/v<n>/<rest>
    m = re.match(r"^([A-Za-z0-9_-]+)/(v\d+)/(.+)$", path)
    if m and m.group(1) in PROJECT_PREFIXES:
        cands.append(f"clients/{m.group(1)}/{m.group(2)}/{m.group(3)}")

    # Deduplicate while preserving order.
    seen, out = set(), []
    for c in cands:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


def resolve(url: str) -> str | None:
    """Return the rewritten URL (or None if the original already resolves)."""
    for cand in candidate_paths(url):
        resolved = try_ext_variants(cand)
        if resolved is None:
            continue
        new_url = f"https://cloudcdn.pro/{resolved}"
        return None if new_url == url else new_url
    return None


def main() -> int:  # noqa: C901 — one-shot CLI; sequential pipeline by design
    files: list[Path] = []
    for pattern in SOURCE_GLOBS:
        files.extend(REPO.glob(pattern))
    files = [f for f in files if f.is_file()]

    rewrite_count = 0
    file_count = 0
    missing: dict[str, list[Path]] = {}

    for f in files:
        text = f.read_text(encoding="utf-8")
        urls = sorted(set(URL_RE.findall(text)))
        if not urls:
            continue
        new_text = text
        for url in urls:
            target = resolve(url)
            if target is None:
                # Either fine (resolves as-is) or unresolvable. Distinguish.
                rels = [c for c in candidate_paths(url) if try_ext_variants(c)]
                if not rels:
                    missing.setdefault(url, []).append(f)
                continue
            if url == target:
                continue
            count = new_text.count(url)
            new_text = new_text.replace(url, target)
            rewrite_count += count
        if new_text != text:
            f.write_text(new_text, encoding="utf-8")
            file_count += 1

    print(f"rewrote {rewrite_count} URL occurrences across {file_count} file(s)")
    if missing:
        print(f"\n{len(missing)} unresolved URL(s) (no matching file under {CDN_ROOT}):")
        for url, paths in sorted(missing.items()):
            print(f"  {url}")
            for p in paths[:3]:
                print(f"    used in {p.relative_to(REPO)}")
            if len(paths) > 3:
                print(f"    … and {len(paths) - 3} more")
        return 0  # report-only, not failure
    return 0


if __name__ == "__main__":
    sys.exit(main())
