# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Unit tests for scripts/postbuild/backfill_permalink.py.

Covers permalink derivation (EN vs locale), idempotency, front-matter
insertion position, and the skip rules (README, no front matter).
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

_MODULE_PATH = (
    Path(__file__).resolve().parents[2] / "scripts" / "postbuild" / "backfill_permalink.py"
)
_spec = importlib.util.spec_from_file_location("backfill_permalink", _MODULE_PATH)
assert _spec and _spec.loader
bp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bp)


def _write(p: Path, text: str) -> Path:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def test_en_permalink_has_no_locale_segment(tmp_path: Path) -> None:
    md = _write(tmp_path / "2020-01-01-hello.md", '---\ntitle: "Hi"\n---\nBody\n')
    assert bp.backfill(tmp_path) == 1
    out = md.read_text(encoding="utf-8")
    assert 'permalink: "https://sebastienrousseau.com/2020-01-01-hello"' in out


def test_locale_permalink_includes_locale_dir(tmp_path: Path) -> None:
    md = _write(tmp_path / "zh-hans" / "2020-01-01-ni-hao.md", '---\ntitle: "你好"\n---\n正文\n')
    bp.backfill(tmp_path)
    out = md.read_text(encoding="utf-8")
    assert 'permalink: "https://sebastienrousseau.com/zh-hans/2020-01-01-ni-hao"' in out


def test_permalink_inserted_after_opening_delimiter(tmp_path: Path) -> None:
    md = _write(tmp_path / "p.md", '---\ntitle: "T"\n---\nBody\n')
    bp.backfill(tmp_path)
    lines = md.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "---"
    assert lines[1].startswith("permalink:")


def test_idempotent_when_permalink_present(tmp_path: Path) -> None:
    original = '---\npermalink: "https://sebastienrousseau.com/keep"\ntitle: "T"\n---\nB\n'
    md = _write(tmp_path / "keep.md", original)
    assert bp.backfill(tmp_path) == 0
    assert md.read_text(encoding="utf-8") == original


def test_readme_and_frontmatterless_files_skipped(tmp_path: Path) -> None:
    _write(tmp_path / "de" / "README.md", '---\ntitle: "x"\n---\n')
    _write(tmp_path / "loose.md", "no front matter here\n")
    assert bp.backfill(tmp_path) == 0


def test_unknown_dir_treated_as_en(tmp_path: Path) -> None:
    # a directory that is not a known locale => EN-style permalink (no segment)
    md = _write(tmp_path / "drafts" / "x.md", '---\ntitle: "T"\n---\nB\n')
    bp.backfill(tmp_path)
    assert 'permalink: "https://sebastienrousseau.com/x"' in md.read_text(encoding="utf-8")
