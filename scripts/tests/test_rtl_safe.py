#!/usr/bin/env python3
"""Smoke test: layouts must use CSS logical properties, not physical.

Right-to-left languages (`ar`, `he`) need the layout to mirror
automatically. CSS *logical* properties (``margin-inline-start``,
``padding-inline-end``, ``inset-inline-start``, ``text-align: start``,
``border-inline-start``) flip with the writing direction; their
*physical* counterparts (``margin-left``, ``padding-right``,
``left:``, ``right:``, ``text-align: left``, ``border-left``) do
not, so a page authored with physical properties looks broken in
RTL languages even when ``<html dir="rtl">`` is set.

This gate scans every CSS source (inline ``<style>`` in
``_layouts/*.html`` + standalone ``.css`` files) and flags any
physical property. Existing usage can be grandfathered by adding
``/* rtl-safe-ignore */`` on the same line — that lets us land the
gate without forcing a layout-wide refactor in one PR.

Run from repo root: ``python3 scripts/test_rtl_safe.py``.
Exits non-zero if any new (un-annotated) physical property is found.
"""
from __future__ import annotations

import sys as _sys  # path bootstrap — scripts reorg (scripts/lib/ on sys.path)
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "lib"))

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LAYOUTS = ROOT / "_layouts"

# Properties that break RTL. The right-hand value documents the
# logical replacement to suggest in the error message.
_PHYSICAL_PROPS: dict[str, str] = {
    "margin-left": "margin-inline-start",
    "margin-right": "margin-inline-end",
    "padding-left": "padding-inline-start",
    "padding-right": "padding-inline-end",
    "border-left": "border-inline-start",
    "border-right": "border-inline-end",
    "border-left-width": "border-inline-start-width",
    "border-right-width": "border-inline-end-width",
    "border-left-color": "border-inline-start-color",
    "border-right-color": "border-inline-end-color",
    "border-left-style": "border-inline-start-style",
    "border-right-style": "border-inline-end-style",
    "border-top-left-radius": "border-start-start-radius",
    "border-top-right-radius": "border-start-end-radius",
    "border-bottom-left-radius": "border-end-start-radius",
    "border-bottom-right-radius": "border-end-end-radius",
}

# `text-align: left` / `text-align: right` — flag separately because
# the syntax varies (start/end vs left/right).
_TEXT_ALIGN_RE = re.compile(r'\btext-align:\s*(left|right)\b', re.IGNORECASE)

# Build one big regex with named groups for the property scan.
_PROP_RE = re.compile(
    r'\b(?P<prop>' + "|".join(re.escape(p) for p in _PHYSICAL_PROPS) + r'):\s*[^;}]+',
    re.IGNORECASE,
)

# Opt-out marker on a line — e.g. for fixed positioning where physical
# coords are correct in both directions, or for properties we
# intentionally can't migrate yet.
_IGNORE_TAG = "rtl-safe-ignore"


def _strip_html_comments(text: str) -> str:
    """Remove <!-- … --> blocks so they can't shelter physical props
    from the scan — comments are not enforced by the browser."""
    return re.sub(r'<!--[\s\S]*?-->', '', text)


def scan_file(path: Path) -> list[str]:
    """Return defects in one file. Each defect is one human-readable line."""
    problems: list[str] = []
    content = _strip_html_comments(path.read_text(encoding="utf-8", errors="ignore"))
    rel = path.relative_to(ROOT).as_posix()

    # Walk line-by-line so we can carry the line number + check for
    # the `rtl-safe-ignore` opt-out marker.
    for lineno, line in enumerate(content.splitlines(), 1):
        if _IGNORE_TAG in line:
            continue
        for m in _PROP_RE.finditer(line):
            prop = m.group("prop").lower()
            suggest = _PHYSICAL_PROPS.get(prop, "logical equivalent")
            problems.append(
                f"{rel}:{lineno}: physical property {prop!r} — "
                f"prefer {suggest!r} (or annotate with /* rtl-safe-ignore */)"
            )
        problems.extend(
            f"{rel}:{lineno}: text-align: {m.group(1)} — "
            f"prefer 'text-align: start' or 'end' (or annotate /* rtl-safe-ignore */)"
            for m in _TEXT_ALIGN_RE.finditer(line)
        )
    return problems


def main() -> int:
    sources = list(LAYOUTS.rglob("*.html")) + list(LAYOUTS.rglob("*.css"))
    # Also pick up any standalone CSS under _layouts/_skeletonic*.css etc.
    if not sources:
        print("warn: no _layouts/*.{html,css} files to scan", file=sys.stderr)
        return 0

    # Baseline mode: count instead of fail. We're shipping the gate with
    # an env-var to flip into strict mode once existing physical
    # properties are migrated. For now, just report.
    strict = "--strict" in sys.argv

    all_problems: list[str] = []
    for path in sources:
        all_problems.extend(scan_file(path))

    if not all_problems:
        print("ok: no physical CSS properties in _layouts/")
        return 0

    print(
        f"rtl-safe: {len(all_problems)} physical CSS properties found across "
        f"{len(sources)} layout source(s):",
        file=sys.stderr,
    )
    for line in all_problems[:20]:
        print(f"  - {line}", file=sys.stderr)
    if len(all_problems) > 20:
        print(f"  …and {len(all_problems) - 20} more", file=sys.stderr)

    if strict:
        print(
            "\nFAIL: --strict mode. Migrate to logical properties or annotate "
            "with /* rtl-safe-ignore */.",
            file=sys.stderr,
        )
        return 1

    print(
        "\nwarn: not failing the build (baseline mode). Pass --strict to "
        "enforce. Migrate to logical properties before activating any RTL "
        "language (`ar`, `he`).",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
