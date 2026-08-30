# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Guard for the `make verify` repo-integrity regression suite — Phase 1.

`make verify` is the single command that must exercise every integrity gate
before a deploy. If a gate is silently dropped from the recipe the suite would
pass while covering less, so this test pins the composition: `verify` must
invoke each expected sub-target, and each of those targets must exist.
"""

from __future__ import annotations

import re
from pathlib import Path

MAKEFILE = Path(__file__).resolve().parents[2] / "Makefile"

# The gate layers `make verify` must chain, in intent (order not asserted, but
# presence is). Keep in sync with the verify recipe + its rationale comment.
EXPECTED_STAGES = ["lint", "typecheck", "test", "build", "validate", "audit", "sbom"]


def _makefile_text() -> str:
    return MAKEFILE.read_text(encoding="utf-8")


def _target_names(text: str) -> set[str]:
    return {m.group(1) for m in re.finditer(r"(?m)^([a-zA-Z][\w-]*):", text)}


def test_verify_target_exists() -> None:
    assert "verify" in _target_names(_makefile_text()), "Makefile lost its `verify` target"


def test_verify_target_is_phony() -> None:
    phony = ""
    for line in _makefile_text().splitlines():
        if line.startswith(".PHONY:"):
            phony += " " + line
    assert "verify" in phony.split(), "`verify` must be declared .PHONY"


def test_verify_chains_every_gate() -> None:
    text = _makefile_text()
    # Isolate the verify recipe block (from `verify:` to the next top-level target).
    m = re.search(r"(?ms)^verify:\n(.*?)(?=^\S)", text)
    assert m, "could not locate the verify recipe body"
    recipe = m.group(1)
    for stage in EXPECTED_STAGES:
        assert re.search(rf"\$\(MAKE\)[^\n]*\b{re.escape(stage)}\b", recipe), (
            f"`make verify` no longer invokes the `{stage}` gate"
        )


def test_all_verify_stages_are_real_targets() -> None:
    targets = _target_names(_makefile_text())
    for stage in EXPECTED_STAGES:
        assert stage in targets, f"verify references `{stage}` but no such Makefile target exists"
