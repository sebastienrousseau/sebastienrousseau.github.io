# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""URL freeze gate (ADR-0015): moving or removing a published URL fails."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "seo_and_audit"))

import check_url_freeze as cuf


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        [
            "git",
            "-c",
            "commit.gpgsign=false",
            "-c",
            "tag.gpgsign=false",
            "-c",
            "user.name=t",
            "-c",
            "user.email=t@t",
            *args,
        ],
        cwd=repo,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def _write(repo: Path, rel: str, text: str) -> None:
    (repo / rel).parent.mkdir(parents=True, exist_ok=True)
    (repo / rel).write_text(text, encoding="utf-8")


@pytest.fixture
def repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    _git(tmp_path, "init", "-q")
    _write(tmp_path, "_posts/2026-01-01-a.md", "english article body\n" * 5)
    _write(tmp_path, "_posts/fr/2026-01-01-a-fr.md", "corps de l article\n" * 5)
    _write(
        tmp_path,
        "_data/i18n/fr/slugs.json",
        json.dumps(
            {"articles": {"2026-01-01-a": "2026-01-01-a-fr"}, "static": {"about": "a-propos"}}
        ),
    )
    _git(tmp_path, "add", ".")
    _git(tmp_path, "commit", "-qm", "base")
    _git(tmp_path, "tag", "base")
    monkeypatch.setattr(cuf, "ROOT", tmp_path)
    return tmp_path


def _commit(repo: Path) -> None:
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "change")


def test_adding_pages_passes(repo: Path) -> None:
    _write(repo, "_posts/2026-01-02-b.md", "b")
    _commit(repo)
    assert cuf.main(["--base", "base"]) == 0


def test_renamed_and_deleted_posts_fail(repo: Path) -> None:
    (repo / "_posts/fr/2026-01-01-a-fr.md").rename(repo / "_posts/fr/2026-01-01-nouveau.md")
    (repo / "_posts/2026-01-01-a.md").unlink()
    _commit(repo)
    problems = cuf.moved_posts("base")
    assert any(p.startswith("renamed _posts/fr/2026-01-01-a-fr.md") for p in problems)
    assert "deleted _posts/2026-01-01-a.md" in problems
    assert cuf.main(["--base", "base"]) == 1


def test_changed_or_removed_slug_values_fail(repo: Path) -> None:
    _write(
        repo,
        "_data/i18n/fr/slugs.json",
        json.dumps({"articles": {"2026-01-01-a": "2026-01-01-autre"}, "static": {}}),
    )
    _commit(repo)
    problems = cuf.changed_slugs("base")
    assert len(problems) == 2
    assert any("articles.2026-01-01-a" in p for p in problems)
    assert any("static.about a-propos -> (removed)" in p for p in problems)


def test_a_deleted_slug_map_fails(repo: Path) -> None:
    (repo / "_data/i18n/fr/slugs.json").unlink()
    _commit(repo)
    assert len(cuf.changed_slugs("base")) == 2
