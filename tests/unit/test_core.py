# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Unit coverage for scripts/lib/_core.py — Phase 1.3 / Phase 4.2.

`_core` is the highest-blast-radius shared module: it holds the canonical
`DATED_SLUG_RE` (consolidated from six copies), the fail-soft
`read_frontmatter`, `display_date`, and `load_banner_affinity`. It had no
direct tests. These lock the contracts every generator now depends on.
"""

from __future__ import annotations

import json
from pathlib import Path

import _core as core

# --- DATED_SLUG_RE ---------------------------------------------------------


def test_dated_slug_re_captures_date_and_rest() -> None:
    m = core.DATED_SLUG_RE.match("2026-06-29-post-quantum-scorecard")
    assert m is not None
    assert m.group(1) == "2026-06-29"
    assert m.group(2) == "post-quantum-scorecard"


def test_dated_slug_re_rejects_non_dated() -> None:
    assert core.DATED_SLUG_RE.match("about") is None
    assert core.DATED_SLUG_RE.match("2026-06-29") is None  # no trailing -<rest>
    assert core.DATED_SLUG_RE.match("26-6-9-x") is None  # wrong date shape


# --- read_frontmatter ------------------------------------------------------


def test_read_frontmatter_returns_dict(tmp_path: Path) -> None:
    p = tmp_path / "post.md"
    p.write_text('---\ntitle: "Hello"\ndate: "2026-06-29"\n---\nbody\n', encoding="utf-8")
    fm = core.read_frontmatter(p)
    assert fm["title"] == "Hello"
    assert fm["date"] == "2026-06-29"


def test_read_frontmatter_missing_file_is_empty(tmp_path: Path) -> None:
    assert core.read_frontmatter(tmp_path / "nope.md") == {}


def test_read_frontmatter_no_frontmatter_is_empty(tmp_path: Path) -> None:
    p = tmp_path / "plain.md"
    p.write_text("no frontmatter here\n", encoding="utf-8")
    assert core.read_frontmatter(p) == {}


# --- display_date ----------------------------------------------------------


def test_display_date_formats() -> None:
    assert core.display_date("2026-06-29") == "June 29, 2026"
    assert core.display_date("2026-01-01") == "January 1, 2026"  # single-digit day, no zero-pad
    assert core.display_date("2025-12-31") == "December 31, 2025"


def test_display_date_all_months() -> None:
    for i, name in enumerate(core._MONTH_NAMES, start=1):
        assert core.display_date(f"2026-{i:02d}-15") == f"{name} 15, 2026"


# --- load_banner_affinity --------------------------------------------------


def test_load_banner_affinity_missing_file(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(core, "ROOT", tmp_path)  # no _data/banner_tags.json
    assert core.load_banner_affinity() == {}


def test_load_banner_affinity_parses_lists_to_tuples(tmp_path, monkeypatch) -> None:
    d = tmp_path / "_data"
    d.mkdir()
    (d / "banner_tags.json").write_text(
        json.dumps({"quantum": ["kyber", "lattice"], "bad": "not-a-list"}),
        encoding="utf-8",
    )
    monkeypatch.setattr(core, "ROOT", tmp_path)
    out = core.load_banner_affinity()
    assert out["quantum"] == ("kyber", "lattice")  # list → tuple
    assert "bad" not in out  # non-list values filtered out


def test_load_banner_affinity_bad_json(tmp_path, monkeypatch) -> None:
    d = tmp_path / "_data"
    d.mkdir()
    (d / "banner_tags.json").write_text("{not valid json", encoding="utf-8")
    monkeypatch.setattr(core, "ROOT", tmp_path)
    assert core.load_banner_affinity() == {}
