"""Shared frontmatter helpers used by post_enrich.py + postbuild.py.

Posts in ``_posts/`` carry a YAML frontmatter block delimited by ``---``
lines. We parse the subset of YAML we actually use (``key: "value"`` and
``key: value`` on a single line), not the full spec.

Two complementary APIs:

* ``split_frontmatter`` / ``fm_get`` / ``fm_set`` — line-based, preserves
  the original frontmatter ordering and formatting (used by
  post_enrich.py to rewrite single fields without churning the rest).
* ``read_fm`` — dict-based, useful when you only want to *read* fields
  (used by postbuild.py to look up titles, urls, last_reviewed dates).
"""

from __future__ import annotations

import re
from pathlib import Path

# ---------------------------------------------------------------------------
# Line-based API (preserves source formatting)
# ---------------------------------------------------------------------------


def split_frontmatter(text: str) -> tuple[list[str], list[str]] | None:
    """Split a post into (frontmatter_lines, body_lines). Returns ``None``
    if the document doesn't have a closing ``---``."""
    lines = text.splitlines(keepends=True)
    bounds = [i for i, ln in enumerate(lines) if ln.strip() == "---"]
    if len(bounds) < 2:
        return None
    return lines[: bounds[1] + 1], lines[bounds[1] + 1 :]


def fm_get(fm_lines: list[str], key: str) -> str | None:
    """Look up a single frontmatter field by key, returning its string
    value (unwrapped from surrounding double-quotes if present)."""
    pat = re.compile(rf'^{re.escape(key)}:\s*"?(.+?)"?\s*$')
    for ln in fm_lines:
        m = pat.match(ln)
        if m:
            return m.group(1)
    return None


def fm_set(fm_lines: list[str], key: str, value: str) -> list[str]:
    """Set (or insert) a frontmatter field. Always emits the value
    double-quoted for safety. Inserts before the closing ``---`` if the
    field isn't already present."""
    pat = re.compile(rf"^{re.escape(key)}:")
    formatted = f'{key}: "{value}"\n'
    for i, ln in enumerate(fm_lines):
        if pat.match(ln):
            fm_lines[i] = formatted
            return fm_lines
    out = list(fm_lines)
    closing = next(i for i in range(len(out) - 1, -1, -1) if out[i].strip() == "---")
    out.insert(closing, formatted)
    return out


# ---------------------------------------------------------------------------
# Dict-based API (read-only)
# ---------------------------------------------------------------------------


_FM_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
_FM_FIELD_RE = re.compile(r'^([a-zA-Z_-]+):\s*"?([^"\n]*)"?', re.MULTILINE)


def read_fm(path: Path) -> dict[str, str]:
    """Parse the first frontmatter block from ``path`` into a flat dict.
    Repeated keys are kept as the first occurrence (``setdefault``)."""
    src = path.read_text(encoding="utf-8", errors="ignore")
    m = _FM_RE.match(src)
    if not m:
        return {}
    fm_text = m.group(1)
    out: dict[str, str] = {}
    for fm in _FM_FIELD_RE.finditer(fm_text):
        out.setdefault(fm.group(1), fm.group(2).strip())
    return out
