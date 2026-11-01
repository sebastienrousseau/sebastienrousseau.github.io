# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Regression guards for Static Site Generator (ssg) JS minifier hazards
and entity-escaped HTML5 tags in compiled Markdown output."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
LAYOUTS = ROOT / "_layouts"
PUBLIC = ROOT / "public"

SKIP_IF_NO_BUILD = pytest.mark.skipif(
    not PUBLIC.is_dir() or not (PUBLIC / "index.html").is_file(),
    reason="public/ not built -- run ./build.sh first",
)

# ssg's JS minifier collapses whitespace-only string literals (" " -> "")
# inside .split(" ") and equality comparisons (=== " "), which silently breaks
# token splitting and Space-key keyboard handlers in production bundles.
_WS_LITERAL_HAZARD_RE = re.compile(r"""(?:\.split\(\s*["']\s+["']\s*\)|[!=]==?\s*["']\s+["'])""")

_ESCAPED_BLOCK_RE = re.compile(
    r"&lt;(?:pre&gt;\s*&lt;code&gt;|/code&gt;\s*&lt;/pre&gt;|time\s+datetime=)",
    re.IGNORECASE,
)


def test_no_whitespace_string_literal_hazards_in_layout_js() -> None:
    """Ensure _layouts/*.js never use whitespace-only string literals in
    .split(' ') or === ' ' where ssg's minifier strips them to empty strings."""
    offenders: list[str] = []
    for js_path in sorted(LAYOUTS.glob("*.js")):
        for lineno, line in enumerate(js_path.read_text(encoding="utf-8").splitlines(), 1):
            if _WS_LITERAL_HAZARD_RE.search(line):
                offenders.append(f"{js_path.name}:{lineno}: {line.strip()}")
    assert not offenders, (
        "Whitespace-only string literal hazard found in _layouts/*.js "
        "(use /\\s+/ or String.fromCharCode(32) instead):\n  " + "\n  ".join(offenders)
    )


@SKIP_IF_NO_BUILD
def test_no_escaped_html5_blocks_in_built_articles() -> None:
    """Verify fix_escaped_ssg_html.py unescaped all raw <pre><code> and <time>
    blocks in rendered English and locale pages."""
    offenders: list[str] = []
    for page in sorted(PUBLIC.glob("*/index.html")):
        html = page.read_text(encoding="utf-8", errors="ignore")
        if _ESCAPED_BLOCK_RE.search(html):
            offenders.append(page.relative_to(PUBLIC).as_posix())
    assert not offenders, "Entity-escaped HTML5 tags leaked into built pages:\n  " + "\n  ".join(
        offenders[:20]
    )
