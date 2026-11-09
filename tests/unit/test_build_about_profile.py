# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""scripts/generators/build_about_profile.py: About sections from profile.yml."""

from __future__ import annotations

from pathlib import Path

import build_about_profile as bap
import pytest

ROOT = Path(__file__).resolve().parents[2]


def test_committed_about_carries_the_marker() -> None:
    assert bap.MARKER in (ROOT / "_posts" / "about.md").read_text(encoding="utf-8")


def test_timeline_has_one_card_per_role_and_the_earlier_line() -> None:
    html = bap.render()
    assert html.count('<article class="story-card">') == 6
    assert "HSBC · 2016–present" in html
    assert "AKQA · 2005–2012" in html
    assert "Earlier at AKQA: Technical Web Architect / Senior Web Developer → " in html
    assert "Earlier: web and internet technology roles at Virgin" in html
    assert "Rufus Leonard" not in html


def test_credentials_list_education_languages_and_awards() -> None:
    html = bap.render()
    assert "<dt>Education</dt>" in html and "University of Westminster" in html
    assert "French (native or bilingual)" in html
    assert "Mobile Agency of the Year" in html
    assert "Institut Supérieur de Gestion" in html


def test_text_is_escaped() -> None:
    html = bap.render()
    assert "Commercial &amp; Investment Banking" in html
    assert "& Investment" not in html


def test_empty_rows_are_left_out() -> None:
    assert bap._row("Awards", []) == ""


def test_apply_replaces_the_marker_once(tmp_path: Path) -> None:
    about = tmp_path / "about.md"
    about.write_text(f"intro\n\n{bap.MARKER}\n\noutro\n", encoding="utf-8")
    assert bap.main(["--dir", str(tmp_path)]) == 0
    text = about.read_text(encoding="utf-8")
    assert bap.MARKER not in text and 'id="about-leadership"' in text
    assert bap.main(["--dir", str(tmp_path)]) == 1


def test_dir_is_required() -> None:
    with pytest.raises(SystemExit):
        bap.main([])
