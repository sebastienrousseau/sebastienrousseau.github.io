# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Apply design system v2 to a layout's shared stylesheet.

Every layout carries one large inline ``<style>`` block (the shell's),
which ssg extracts to a fingerprinted file. Over time that block grew 45
distinct ``max-width`` values and ~70 one-off ``clamp()`` font sizes, so
pages stopped sharing a column or a type scale.

Rather than rewrite 2,000+ lines per layout in one go, this module:

1. wraps the existing block in ``@layer legacy { ... }``, and
2. appends ``assets/css/design-system.css`` *unlayered* after it.

Unlayered rules beat every layered rule regardless of selector
specificity, so the design system's tokens win wherever it names an
element, and the legacy rules still style everything it does not name.
Legacy ``!important`` declarations keep winning (layered important beats
unlayered normal), which preserves the print and reduced-motion overrides.

``apply`` is idempotent: it strips any previous wrapper before re-applying,
so page-specific CSS that generators append to the block (speaking, hub,
playlists) always ends up inside the legacy layer, never after the design
system. ``tests/unit/test_design_system.py`` asserts every layout carries
the current file verbatim.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DS_PATH = ROOT / "assets" / "css" / "design-system.css"

STYLE_OPEN = "    <style>\n"
STYLE_CLOSE = "    </style>"

LAYER_OPEN = "      @layer legacy { /* ds:legacy-start */\n"
LAYER_CLOSE = "\n      } /* ds:legacy-end */\n"
DS_START = "/* ds:start */\n"
DS_END = "\n/* ds:end */\n"

_DS_BLOCK_RE = re.compile(re.escape(LAYER_CLOSE) + r".*?" + re.escape(DS_END), re.DOTALL)


def design_system_css() -> str:
    """The canonical design-system stylesheet, verbatim."""
    return DS_PATH.read_text(encoding="utf-8").rstrip("\n")


def strip(html: str) -> str:
    """Remove a previously applied wrapper and design-system block."""
    html = html.replace(LAYER_OPEN, "", 1)
    return _DS_BLOCK_RE.sub("\n", html, count=1)


def apply(html: str, css: str | None = None) -> str:
    """Wrap the first shell ``<style>`` block in ``@layer legacy`` and
    append the design system after it. Idempotent."""
    css = design_system_css() if css is None else css
    html = strip(html)
    start = html.find(STYLE_OPEN)
    if start == -1:
        raise RuntimeError("design_system.apply: shell <style> block not found")
    body_start = start + len(STYLE_OPEN)
    end = html.find(STYLE_CLOSE, body_start)
    if end == -1:
        raise RuntimeError("design_system.apply: shell </style> not found")
    legacy = html[body_start:end].rstrip("\n")
    return (
        html[:body_start] + LAYER_OPEN + legacy + LAYER_CLOSE + DS_START + css + DS_END + html[end:]
    )


def applied_css(html: str) -> str | None:
    """The design-system CSS embedded in ``html``, or None."""
    i = html.find(DS_START)
    if i == -1:
        return None
    j = html.find(DS_END, i)
    if j == -1:
        return None
    return html[i + len(DS_START) : j]
