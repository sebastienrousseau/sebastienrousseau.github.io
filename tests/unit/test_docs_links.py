# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Verify that all relative Markdown links in docs/ and root docs resolve."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"

_MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def _gather_markdown_files() -> list[Path]:
    files = list(DOCS.rglob("*.md"))
    files.extend(ROOT.glob("*.md"))
    return files


def test_internal_docs_links_resolve() -> None:
    broken: list[str] = []
    md_files = _gather_markdown_files()

    for md_file in md_files:
        content = md_file.read_text(encoding="utf-8")
        # Strip fenced code blocks
        clean_content = re.sub(r"```[\s\S]*?```", "", content)
        # Strip inline code spans
        clean_content = re.sub(r"`[^`]+`", "", clean_content)

        for match in _MD_LINK_RE.finditer(clean_content):
            target = match.group(2).strip()
            # Ignore absolute URLs, protocol links, mailto, anchor-only, or placeholders
            if target.startswith(("http://", "https://", "mailto:", "#", "tel:")) or "{{" in target:
                continue

            # Strip anchor if present
            path_part = target.split("#")[0].strip()
            if not path_part:
                continue

            # Strip query params if present
            path_part = path_part.split("?")[0].strip()

            # Resolve relative to current md_file parent
            resolved = (md_file.parent / path_part).resolve()

            # If path doesn't exist, check relative to ROOT
            if not resolved.exists():
                resolved_root = (ROOT / path_part).resolve()
                if not resolved_root.exists():
                    rel_src = md_file.relative_to(ROOT)
                    broken.append(f"{rel_src} -> {target}")

    assert not broken, "Broken internal Markdown links found:\n  " + "\n  ".join(broken)
