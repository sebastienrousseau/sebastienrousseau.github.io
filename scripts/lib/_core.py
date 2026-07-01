"""Shared utilities used across the build pipeline.

Before this module existed there were three different bespoke YAML
frontmatter parsers spread across ``gen_articles.py``,
``check_voice.py``, and ``build_topics.py``. The single canonical
implementation now lives in ``scripts/lib/_frontmatter.py``;
``parse_frontmatter`` here is a re-export kept for the existing
import sites (``from _core import parse_frontmatter``).

This module is intentionally tiny and has zero external dependencies
beyond stdlib — it's imported very early in every pipeline step.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from _frontmatter import parse_frontmatter  # re-exported for legacy import sites

ROOT = Path(__file__).resolve().parents[2]

# Canonical dated-post slug matcher. A published article slug is
# ``YYYY-MM-DD-<rest>``; group 1 is the ISO date, group 2 the title slug.
# This replaces six near-identical local copies across the generators
# (build_tags/listings/tag_landings/oembed, article_furniture, rag_corpus);
# every call site used it either for the date/rest groups or as a boolean
# "is this a dated post" guard, both of which this two-group form serves.
DATED_SLUG_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-(.+)$")


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
