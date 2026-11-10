# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""scripts/generators/build_404_latest.py: newest articles on the 404 page."""

from __future__ import annotations

from pathlib import Path

import build_404_latest as b4
import pytest

ROOT = Path(__file__).resolve().parents[2]


def _post(d: Path, name: str, title: str) -> None:
    (d / f"{name}.md").write_text(f'---\ntitle: "{title}"\n---\nbody\n', encoding="utf-8")


def test_committed_404_carries_the_marker_search_and_links() -> None:
    text = (ROOT / "_posts" / "404.md").read_text(encoding="utf-8")
    assert b4.MARKER in text and 'action="/search/index.html"' in text
    assert text.count("<li><a href=") == 6


def test_lists_the_newest_dated_articles(tmp_path: Path) -> None:
    for i, day in enumerate(("01", "02", "03", "04")):
        _post(tmp_path, f"2026-01-{day}-post-{i}", 'Post 3 & \\"co\\"' if i == 3 else f"Post {i}")
    _post(tmp_path, "about", "About")
    (tmp_path / "2026-01-05-no-title.md").write_text("---\n---\n", encoding="utf-8")
    items = b4.newest(tmp_path)
    assert [s for s, _ in items] == ["2026-01-04-post-3", "2026-01-03-post-2", "2026-01-02-post-1"]
    assert 'Post 3 &amp; "co"' in b4.render(items)


def test_main_replaces_the_marker_once(tmp_path: Path) -> None:
    _post(tmp_path, "2026-01-01-a", "A")
    (tmp_path / "404.md").write_text(f"x\n{b4.MARKER}\n", encoding="utf-8")
    assert b4.main(["--dir", str(tmp_path)]) == 0
    assert 'href="/2026-01-01-a/index.html"' in (tmp_path / "404.md").read_text(encoding="utf-8")
    assert b4.main(["--dir", str(tmp_path)]) == 1


def test_dir_is_required() -> None:
    with pytest.raises(SystemExit):
        b4.main([])
