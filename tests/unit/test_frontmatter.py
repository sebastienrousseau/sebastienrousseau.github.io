"""Tests for scripts/_frontmatter.py.

Covers the two APIs (line-based + dict-based) and the specific bugs we've
already shipped — multi-line YAML scalars, missing terminators, etc.
"""

from __future__ import annotations

from pathlib import Path

import _frontmatter as fm

SAMPLE = """---
title: "Hello, World"
description: "A post about cats & dogs"
url: "https://sebastienrousseau.com/hello/index.html"
last_reviewed: "2026-05-13"
---

# Hello

Body content here.
"""


def write(tmp_path: Path, text: str) -> Path:
    p = tmp_path / "post.md"
    p.write_text(text, encoding="utf-8")
    return p


def test_read_fm_basic(tmp_path):
    p = write(tmp_path, SAMPLE)
    out = fm.read_fm(p)
    assert out["title"] == "Hello, World"
    assert out["url"] == "https://sebastienrousseau.com/hello/index.html"
    assert out["last_reviewed"] == "2026-05-13"


def test_read_fm_missing_returns_empty(tmp_path):
    p = write(tmp_path, "no frontmatter here\n")
    assert fm.read_fm(p) == {}


def test_split_frontmatter_returns_lines(tmp_path):
    parts = fm.split_frontmatter(SAMPLE)
    assert parts is not None
    fm_lines, body_lines = parts
    assert fm_lines[0] == "---\n"
    assert fm_lines[-1] == "---\n"
    assert "# Hello\n" in body_lines


def test_split_frontmatter_returns_none_on_unterminated():
    text = "---\ntitle: x\n# Hello\n"
    assert fm.split_frontmatter(text) is None


def test_fm_get_quoted_and_unquoted():
    fm_lines = ["---\n", 'title: "Quoted"\n', "tag: unquoted\n", "---\n"]
    assert fm.fm_get(fm_lines, "title") == "Quoted"
    assert fm.fm_get(fm_lines, "tag") == "unquoted"
    assert fm.fm_get(fm_lines, "missing") is None


def test_fm_set_replaces_existing():
    fm_lines = ["---\n", 'title: "Old"\n', "---\n"]
    out = fm.fm_set(fm_lines, "title", "New")
    assert any('title: "New"' in ln for ln in out)
    assert not any('"Old"' in ln for ln in out)


def test_fm_set_inserts_when_missing():
    fm_lines = ["---\n", 'title: "x"\n', "---\n"]
    out = fm.fm_set(fm_lines, "url", "https://example.com/")
    # Inserted before the closing `---`.
    assert out.index('url: "https://example.com/"\n') < out.index("---\n", 1)
