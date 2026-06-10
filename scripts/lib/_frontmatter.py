"""Shared frontmatter helpers — the ONE canonical parser for the repo.

Posts in ``_posts/`` carry a YAML frontmatter block delimited by ``---``
lines. We parse the subset of YAML we actually use (``key: "value"``,
``key: 'value'`` and ``key: value`` on a single line), not the full spec.

Three complementary APIs:

* ``parse_frontmatter`` — the canonical dict-based parser. Returns
  ``(frontmatter_dict, body)``. ``_core.parse_frontmatter`` and
  ``build_translations.parse_frontmatter`` are thin re-exports of it.
* ``split_frontmatter`` / ``fm_get`` / ``fm_set`` — line-based, preserves
  the original frontmatter ordering and formatting (used by
  post_enrich.py to rewrite single fields without churning the rest).
* ``read_fm`` — dict-based file wrapper, useful when you only want to
  *read* fields (used by postbuild.py to look up titles, urls,
  last_reviewed dates).
"""

from __future__ import annotations

import re
from pathlib import Path

# ---------------------------------------------------------------------------
# Canonical parser (dict-based)
#
# Union of the behaviours of the three historical implementations
# (scripts/lib/_core.py, scripts/generators/build_translations.py, and
# the original read_fm below):
#
# * the block must open with a ``---`` line at the very start and close
#   with another ``---`` line — otherwise ``({}, text)`` is returned
#   unchanged (the _core / gen_articles contract);
# * values may be double-quoted (with escapes), single-quoted (with
#   escapes — the build_translations extension), or bare (the read_fm
#   extension); bare values are whitespace-trimmed. A value that *opens*
#   with a quote but isn't a well-formed quoted string (e.g. an
#   unescaped quote inside) is dropped — the historical _core /
#   build_translations behaviour, which downstream renderers rely on to
#   fall back to derived values instead of ingesting mangled text;
# * keys match ``[A-Za-z][A-Za-z0-9_-]*`` (union of the three key
#   grammars);
# * repeated keys: last occurrence wins by default (the _core /
#   build_translations contract); ``first_wins=True`` preserves the
#   read_fm contract;
# * the body is everything after the closing ``---`` with leading
#   newlines stripped (the _core contract; markdown rendering is
#   insensitive to the leading blank line build_translations kept).
# ---------------------------------------------------------------------------

_KEY = r"[A-Za-z][A-Za-z0-9_-]*"
_QUOTED_LINE_RE = re.compile(
    rf"^({_KEY}):\s*(?:\"((?:[^\"\\]|\\.)*)\"|'((?:[^'\\]|\\.)*)')\s*$"
)
_BARE_LINE_RE = re.compile(rf"^({_KEY}):\s*(\S.*?)\s*$")


def parse_frontmatter(text: str, *, first_wins: bool = False) -> tuple[dict[str, str], str]:
    """Parse a Markdown document's YAML frontmatter.

    Returns ``({}, text)`` if the document doesn't open with a ``---``
    line or the closing ``---`` delimiter is missing. Otherwise returns
    a flat ``key -> value`` dict and the body after the delimiter.

    Deliberately *not* full PyYAML — that would pull in a dependency,
    and the pipeline only emits single-line frontmatter anyway.
    Multi-line blocks aren't supported.
    """
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return {}, text
    close = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if close is None:
        return {}, text
    fm: dict[str, str] = {}
    for raw in lines[1:close]:
        line = raw.strip()
        m = _QUOTED_LINE_RE.match(line)
        if m:
            value = m.group(2) if m.group(2) is not None else m.group(3)
        else:
            m = _BARE_LINE_RE.match(line)
            if not m:
                continue
            value = m.group(2)
            if value[0] in "\"'":
                # Opens like a quoted string but didn't parse as one
                # (unescaped inner quote, missing closer, …) — drop the
                # key rather than ingest mangled text.
                continue
        key = m.group(1)
        if first_wins:
            fm.setdefault(key, value)
        else:
            fm[key] = value
    body = "".join(lines[close + 1 :]).lstrip("\n")
    return fm, body

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


def read_fm(path: Path) -> dict[str, str]:
    """Parse the first frontmatter block from ``path`` into a flat dict.
    Repeated keys are kept as the first occurrence. Returns ``{}`` for
    missing/unreadable files — the fail-soft contract every caller
    expects."""
    try:
        src = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return {}
    fm, _body = parse_frontmatter(src, first_wins=True)
    return fm
