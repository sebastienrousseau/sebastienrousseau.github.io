# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Guard: ADR hygiene — improvement-plan-2026 Phase 5.1.

Keeps the architecture-decision record honest as it grows:
- numbering is contiguous from 0001 (no gaps, no duplicates),
- every ADR carries a Status and Date header,
- every ADR (bar the pre-template 0001) has Context / Decision /
  Consequences sections.

This backs the plan's "ADR per structural decision" discipline: a new ADR
that skips the template, or a numbering gap, fails CI.
"""

from __future__ import annotations

import re
from pathlib import Path

ADR_DIR = Path(__file__).resolve().parents[2] / "project-docs" / "adr"

# 0001 predates the ADR template (it is an implementation plan, not a
# Context/Decision/Consequences record). Header checks still apply to it.
_NO_TEMPLATE = {1}

_NUM_RE = re.compile(r"^(\d{4})-[a-z0-9-]+\.md$")


def _adrs() -> list[tuple[int, Path]]:
    out = []
    for p in ADR_DIR.glob("*.md"):
        m = _NUM_RE.match(p.name)
        if m:
            out.append((int(m.group(1)), p))
    return sorted(out)


def test_adr_numbering_is_contiguous() -> None:
    nums = [n for n, _ in _adrs()]
    assert nums, "no ADRs found"
    expected = list(range(1, len(nums) + 1))
    assert nums == expected, (
        f"ADR numbering not contiguous from 0001: got {nums}, expected {expected}"
    )


def test_every_adr_has_status_and_date() -> None:
    missing = []
    for _, p in _adrs():
        text = p.read_text(encoding="utf-8")
        if not re.search(r"^\*\*Status:\*\*", text, re.MULTILINE):
            missing.append(f"{p.name}: Status")
        if not re.search(r"^\*\*Date:\*\*", text, re.MULTILINE):
            missing.append(f"{p.name}: Date")
    assert not missing, "ADRs missing required header field(s): " + ", ".join(missing)


def test_templated_adrs_have_core_sections() -> None:
    required = ("## Context", "## Decision", "## Consequences")
    missing = []
    for num, p in _adrs():
        if num in _NO_TEMPLATE:
            continue
        text = p.read_text(encoding="utf-8")
        missing.extend(f"{p.name}: {s}" for s in required if s not in text)
    assert not missing, "ADRs missing required section(s): " + ", ".join(missing)
