# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""scripts/release/release_notes.py: dotfiles-format release notes."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "release"))
import release_notes as rn

CHANGELOG = """# Changelog

## [0.0.35] - 2026-11-09

Intro paragraph is not a highlight.

### Added

- **A new thing**: it does X. A second sentence is dropped.
- plain bullet without a lead is skipped

### Fixed

- **Broken thing works** (`file.py`): now it works.
- **A check flags a fault** (`check.py`), so the build fails with the reason.

### Unchanged, measured

- **Not a highlight**: measured only.

## [0.0.34] - 2026-11-08

### Fixed

- **Older**: older.
"""


def test_title_and_version() -> None:
    assert rn.title("v0.0.35") == "sebastienrousseau.github.io 0.0.35"
    with pytest.raises(ValueError, match="not a release tag"):
        rn.version_of("0.0.35")


def test_highlights_take_lead_and_first_sentence_from_release_sections() -> None:
    section = rn.changelog_section(CHANGELOG, "0.0.35")
    assert rn.highlights(section) == [
        "* **A new thing**: it does X.",
        "* **Broken thing works**: now it works.",
        "* **A check flags a fault**, so the build fails with the reason.",
    ]
    assert rn.changelog_section(CHANGELOG, "9.9.9") == ""


def test_changes_are_oldest_first_and_skip_direct_commits() -> None:
    subjects = ["fix: newest (#3)", "chore: no pr", "feat: oldest (#1)"]
    changes = rn.changes_from_subjects(subjects, lambda n: f"user{n}")
    assert [(c.title, c.number, c.author) for c in changes] == [
        ("feat: oldest", 1, "user1"),
        ("fix: newest", 3, "user3"),
    ]


def test_render_matches_the_dotfiles_layout() -> None:
    section = rn.changelog_section(CHANGELOG, "0.0.35")
    body = rn.render("v0.0.35", "v0.0.34", section, [rn.Change("fix: x", 9, "me")])
    assert body.startswith("## Highlights ⭐️\n\n* **A new thing**")
    assert "\n## What's Changed\n\n* `fix: x` by @me in https://github.com/" in body
    assert body.rstrip().endswith("/compare/v0.0.34...v0.0.35")


def test_render_without_highlights_or_changes_still_has_every_section() -> None:
    body = rn.render("v0.0.1", None, "", [])
    assert "Maintenance release" in body and "No pull requests" in body
    assert body.rstrip().endswith("/commits/v0.0.1")


def test_build_reads_git_history(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: dict[tuple[str, ...], str] = {
        ("tag", "--merged", "HEAD"): "v0.0.33\nv0.0.34\nv1.2.0\nnot-a-tag\n",
        ("log", "--first-parent", "--format=%s", "v0.0.34..HEAD"): "feat: y (#7)\n",
        ("show", "HEAD:CHANGELOG.md"): CHANGELOG,
    }
    monkeypatch.setattr(rn, "_git", lambda *a: calls[a])
    body = rn.build("v0.0.35", "HEAD", author_of=lambda n: "me")
    assert "* `feat: y` by @me in https://github.com/" in body
    assert "compare/v0.0.34...v0.0.35" in body


def test_main_prints_title(capsys: pytest.CaptureFixture[str]) -> None:
    assert rn.main(["v0.0.35", "--title"]) == 0
    assert capsys.readouterr().out.strip() == "sebastienrousseau.github.io 0.0.35"


def test_backfill_reads_the_changelog_from_another_ref(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = {
        ("tag", "--merged", "v0.0.35"): "v0.0.34\n",
        ("log", "--first-parent", "--format=%s", "v0.0.34..v0.0.35"): "",
        ("show", "origin/main:CHANGELOG.md"): CHANGELOG,
    }
    monkeypatch.setattr(rn, "_git", lambda *a: calls[a])
    body = rn.build("v0.0.35", "v0.0.35", author_of=str, changelog_ref="origin/main")
    assert "* **A new thing**: it does X." in body
