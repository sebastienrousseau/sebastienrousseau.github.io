# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Frontmatter + markdown glue.

The frontmatter parser is the canonical one in
``scripts/lib/_frontmatter.py`` — re-exported here so
``build_translations.parse_frontmatter`` keeps working for every
existing call site.
"""

from __future__ import annotations

from _frontmatter import parse_frontmatter  # re-exported (canonical parser)
from markdown_it import MarkdownIt

__all__ = ["parse_frontmatter", "render_markdown"]


def render_markdown(body: str) -> str:
    md = MarkdownIt("commonmark", {"html": True, "linkify": True})
    md.enable(["table", "strikethrough"])
    return md.render(body)
