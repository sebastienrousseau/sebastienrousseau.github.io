# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Tests for scripts/lib/_frontmatter.py.

Covers the canonical ``parse_frontmatter`` (now the single parser behind
``_core.parse_frontmatter``, ``read_fm`` and
``build_translations.parse_frontmatter``), the line-based API, and the
specific bugs we've already shipped — multi-line YAML scalars, missing
terminators, etc.
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


# ---------------------------------------------------------------------------
# Canonical parser — parse_frontmatter
# ---------------------------------------------------------------------------


def test_parse_frontmatter_basic_key_value():
    src = '---\ntitle: "Hello"\ndate: "2026-06-10"\n---\n\n# Body\n'
    out, body = fm.parse_frontmatter(src)
    assert out == {"title": "Hello", "date": "2026-06-10"}
    assert body == "# Body\n"


def test_parse_frontmatter_double_quoted_with_escapes():
    src = '---\ntitle: "He said \\"hi\\""\n---\nbody'
    out, _ = fm.parse_frontmatter(src)
    assert out["title"] == 'He said \\"hi\\"'


def test_parse_frontmatter_single_quoted_values():
    src = "---\ntitle: 'Single'\n---\nbody"
    out, _ = fm.parse_frontmatter(src)
    assert out["title"] == "Single"


def test_parse_frontmatter_bare_values_trimmed():
    src = "---\ntags: ai, payments  \nlayout: post\n---\nbody"
    out, _ = fm.parse_frontmatter(src)
    assert out["tags"] == "ai, payments"
    assert out["layout"] == "post"


def test_parse_frontmatter_missing_frontmatter_returns_text_unchanged():
    text = "no frontmatter here\n"
    out, body = fm.parse_frontmatter(text)
    assert out == {}
    assert body == text


def test_parse_frontmatter_unclosed_delimiter_returns_text_unchanged():
    text = '---\ntitle: "x"\n\nbody'
    out, body = fm.parse_frontmatter(text)
    assert out == {}
    assert body == text


def test_parse_frontmatter_malformed_lines_are_skipped():
    src = '---\n: no key\n- list item\ntitle: "ok"\nnot a field\n---\nbody'
    out, _ = fm.parse_frontmatter(src)
    assert out == {"title": "ok"}


def test_parse_frontmatter_malformed_quoted_value_is_dropped():
    # An unescaped quote inside a quoted value (real case: _posts/de/
    # 2026-05-17 subtitle with „Hochrisiko") must NOT fall through to
    # the bare-value branch — the historical parsers dropped the key
    # and downstream renderers rely on the absence to derive fallbacks.
    src = '---\nsubtitle: "the „high-risk" deadline"\ntitle: "ok"\n---\nbody'
    out, _ = fm.parse_frontmatter(src)
    assert "subtitle" not in out
    assert out["title"] == "ok"


def test_parse_frontmatter_empty_text():
    out, body = fm.parse_frontmatter("")
    assert out == {}
    assert body == ""


def test_parse_frontmatter_body_extraction_strips_leading_newlines():
    src = '---\ntitle: "x"\n---\n\n\nFirst line.\n'
    _, body = fm.parse_frontmatter(src)
    assert body == "First line.\n"


def test_parse_frontmatter_repeated_keys_last_wins_by_default():
    src = '---\ntitle: "first"\ntitle: "second"\n---\nbody'
    out, _ = fm.parse_frontmatter(src)
    assert out["title"] == "second"


def test_parse_frontmatter_repeated_keys_first_wins_opt_in():
    src = '---\ntitle: "first"\ntitle: "second"\n---\nbody'
    out, _ = fm.parse_frontmatter(src, first_wins=True)
    assert out["title"] == "first"


def test_parse_frontmatter_closing_delim_with_trailing_whitespace():
    src = '---\ntitle: "x"\n---   \nbody\n'
    out, body = fm.parse_frontmatter(src)
    assert out == {"title": "x"}
    assert body == "body\n"


def test_read_fm_unreadable_path_returns_empty(tmp_path):
    assert fm.read_fm(tmp_path / "does-not-exist.md") == {}


def test_core_parse_frontmatter_is_the_canonical_one():
    import _core

    assert _core.parse_frontmatter is fm.parse_frontmatter
