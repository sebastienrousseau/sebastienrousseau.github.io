"""Shared utilities used across the build pipeline.

Before this module existed there were three different bespoke YAML
frontmatter parsers spread across ``gen_articles.py``,
``check_voice.py``, and ``build_topics.py``. Each one was *almost*
identical but differed in a subtle way (return type, handling of
unclosed delimiters, etc.). One canonical implementation here, and
every caller imports from this module.

This module is intentionally tiny and has zero external dependencies
beyond stdlib — it's imported very early in every pipeline step.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------------
# Frontmatter
# ---------------------------------------------------------------------------

_FM_KEY_RE = re.compile(r'^([a-z_]+):\s*"((?:[^"\\]|\\.)*)"\s*$')


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Parse a Markdown file's YAML frontmatter.

    Returns ``({}, text)`` if the text doesn't start with ``---`` or if
    the closing ``---`` delimiter is missing. Otherwise returns a flat
    dict of key→value (quoted-string values only — same shape every
    caller in this repo uses) and the body after the delimiter.

    This is deliberately *not* full PyYAML — that would pull in a
    dependency, and the pipeline only emits single-line ``key: "value"``
    frontmatter anyway. Multi-line blocks aren't supported.
    """
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        return {}, text
    head = text[3:end]
    body = text[end + 4 :].lstrip("\n")
    fm: dict[str, str] = {}
    for line in head.splitlines():
        m = _FM_KEY_RE.match(line)
        if m:
            fm[m.group(1)] = m.group(2)
    return fm, body


def read_frontmatter(path: Path) -> dict[str, str]:
    """Convenience wrapper: open a file and return only its frontmatter
    dict. Returns ``{}`` for missing files / unparseable headers — the
    same fail-soft contract every caller in this repo expects."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return {}
    fm, _body = parse_frontmatter(text)
    return fm


# ---------------------------------------------------------------------------
# Dates
# ---------------------------------------------------------------------------

_MONTH_NAMES = (
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)


def display_date(iso: str) -> str:
    """``YYYY-MM-DD`` → ``Month DD, YYYY``."""
    y, m, d = iso.split("-")
    return f"{_MONTH_NAMES[int(m) - 1]} {int(d)}, {y}"


# ---------------------------------------------------------------------------
# Data files (configuration extracted from Python)
# ---------------------------------------------------------------------------


def load_banner_affinity() -> dict[str, tuple[str, ...]]:
    """Load the keyword → image-substring affinity map.

    Source: ``_data/banner_tags.json``. Falls back to an empty dict if
    the file is missing so the picker still works (random pick, no
    keyword bias).
    """
    p = ROOT / "_data" / "banner_tags.json"
    if not p.is_file():
        return {}
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return {k: tuple(v) for k, v in raw.items() if isinstance(v, list)}
