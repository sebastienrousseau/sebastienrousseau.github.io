# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Every counter name used in postbuild must exist in `__slots__`.

`_PostbuildCounters` declares `__slots__`, so assigning a name that is not
declared raises `AttributeError` — and the counters are bumped per page,
deep inside `_process_page`. A missing declaration therefore does not fail
fast: the build runs, every single page raises, and the error surfaces
6,856 times as

    postbuild: FAILED <page>: AttributeError: '_PostbuildCounters' object
    has no attribute 'jsonld_entities_decoded'

That happened. It reached CI because the pre-build unit gate cannot run the
postbuild smoke suite (it needs a built `public/`), so nothing exercised the
new pass until `./build.sh` itself ran — 13 minutes into the job.

This test needs neither a build nor an import of the page pipeline: it reads
the counter names out of the source and checks them against the declared
slots. A new pass with an undeclared counter now fails in milliseconds.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POSTBUILD = ROOT / "scripts" / "postbuild" / "postbuild.py"
sys.path.insert(0, str(ROOT / "scripts" / "postbuild"))

import postbuild

# `_bump(pass_fn, html, ctr, "counter_name")` — the last string literal.
_BUMP_NAME = re.compile(r"_bump\([^()]*?\"([a-z0-9_]+)\"\s*\)")


def _counter_names_in_source() -> set[str]:
    return set(_BUMP_NAME.findall(POSTBUILD.read_text(encoding="utf-8")))


def test_every_bumped_counter_is_declared() -> None:
    used = _counter_names_in_source()
    assert used, "no _bump() counter names found — the regex or the file changed"

    declared = set(postbuild._PostbuildCounters.__slots__)
    undeclared = sorted(used - declared)
    assert not undeclared, (
        "these counters are bumped but missing from _PostbuildCounters.__slots__, "
        "which raises AttributeError on every page at build time: "
        f"{undeclared}"
    )


def test_counters_start_at_zero() -> None:
    """`__init__` zeroes every slot, so a newly declared counter needs no
    other wiring — and a slot that somehow escapes initialisation would
    raise here rather than on the first bump."""
    ctr = postbuild._PostbuildCounters()
    for name in postbuild._PostbuildCounters.__slots__:
        assert getattr(ctr, name) == 0, f"{name} did not start at 0"


def test_slots_are_sorted() -> None:
    """The list is alphabetical; keeping it so is what makes a missing entry
    visible in review rather than lost in a 55-line tuple."""
    slots = list(postbuild._PostbuildCounters.__slots__)
    assert slots == sorted(slots), "counter __slots__ is no longer alphabetical"
