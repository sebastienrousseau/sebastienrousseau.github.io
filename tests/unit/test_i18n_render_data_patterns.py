# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""The render-data parity gate compares patterns, not just counts.

A locale's home_patches.json can hold as many entries as FR's while
matching different (stale) patterns, which left English on 32 locale
home pages. ``check_pattern_set`` must catch a same-length list.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    "i18n_render_data", ROOT / "tests" / "validation" / "test_i18n_render_data.py"
)
assert _spec and _spec.loader
gate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gate)

FR = [">What I build</p>", "<h3>Payments</h3>"]


def test_identical_pattern_set_passes() -> None:
    entries = [(">What I build</p>", ">X</p>"), ("<h3>Payments</h3>", "<h3>Y</h3>")]
    assert gate.check_pattern_set("xx", "home_patches", entries, FR) == []


def test_same_count_different_patterns_fails() -> None:
    entries = [(">What I build</p>", ">X</p>"), (">Latest research<", ">Y<")]
    problems = gate.check_pattern_set("xx", "home_patches", entries, FR)
    assert problems == [
        "[xx/home_patches] patterns differ from FR: 1 missing, 1 extra (first: '<h3>Payments</h3>')"
    ]


def test_missing_only_fails() -> None:
    problems = gate.check_pattern_set("xx", "home_patches", [(">What I build</p>", ">X</p>")], FR)
    assert problems and "1 missing, 0 extra" in problems[0]
