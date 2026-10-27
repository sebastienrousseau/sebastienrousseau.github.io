# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Unit tests for tests/validation/test_no_pipeline_artefacts.py.

CommonMark opens an ordered list only on ASCII digits. A digit-localising
pass that rewrites ``1. `` as ``১. `` or ``१. `` turns the list into one
paragraph that starts with the marker, as five bn and mr posts showed.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
_SPEC = importlib.util.spec_from_file_location(
    "no_pipeline_artefacts_gate",
    ROOT / "tests" / "validation" / "test_no_pipeline_artefacts.py",
)
gate = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = gate
_SPEC.loader.exec_module(gate)


def test_native_digit_list_marker_is_an_offence() -> None:
    text = "Intro.\n\n১. **One.** Body.\n২. **Two.** Body.\n"
    assert any("native-digit list marker" in o for o in gate.offences(text))


def test_devanagari_list_marker_is_an_offence() -> None:
    assert gate.offences("  १. पहिला\n")


def test_ascii_list_marker_is_clean() -> None:
    assert gate.offences("১৯৮৫ সালে।\n\n1. **One.** ২০২৬ সালে।\n") == []


def test_native_digits_mid_line_are_clean() -> None:
    assert gate.offences("সংস্করণ ২. এটি একটি বাক্য।\n") == []
