# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""docs/bios.md carries profile.yml's bios word for word."""

from __future__ import annotations

from pathlib import Path

import _profile

ROOT = Path(__file__).resolve().parents[2]


def _flat(text: str) -> str:
    return " ".join(text.split())


def test_bios_doc_matches_the_profile() -> None:
    doc = _flat((ROOT / "docs" / "bios.md").read_text(encoding="utf-8"))
    profile = _profile.load()
    for key in ("one_line", "short"):
        assert _flat(profile["bios"][key]) in doc, f"docs/bios.md is out of date: {key}"
    assert profile["job_title_short"] in doc
