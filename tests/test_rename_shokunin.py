"""Unit tests for scripts/rename_shokunin.py.

The transform() function is the most-touched code-path and the easiest
to exercise. main() is also covered with a tmp_path tree so the
file-walk + write branches are hit.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import rename_shokunin as rs

# ---------------------------------------------------------------------------
# transform
# ---------------------------------------------------------------------------


def test_transform_replaces_ssg_form():
    assert rs.transform("Shokunin SSG is fast") == "Static Site Generator (SSG) is fast"


def test_transform_replaces_long_form():
    assert (
        rs.transform("Shokunin Static Site Generator rocks")
        == "Static Site Generator rocks"
    )


def test_transform_replaces_made_with():
    assert (
        rs.transform("Made with Shokunin and love.")
        == "Made with Static Site Generator and love."
    )


def test_transform_replaces_powered_by():
    assert (
        rs.transform("Powered by Shokunin under the hood.")
        == "Powered by the Static Site Generator under the hood."
    )


def test_transform_replaces_standalone_titlecase():
    assert rs.transform("Shokunin is great") == "Static Site Generator is great"


def test_transform_replaces_lowercase_in_prose():
    assert (
        rs.transform("we use shokunin for builds.")
        == "we use Static Site Generator for builds."
    )


def test_transform_keeps_lowercase_inside_urls():
    """The URL-ish guard must preserve `/shokunin/`, `shokunin-ssg`,
    domain-style mentions, etc."""
    inp = (
        "Visit https://github.com/sebastienrousseau/shokunin and grab "
        "the shokunin-ssg crate from shokunin.crates.io"
    )
    out = rs.transform(inp)
    assert "github.com/sebastienrousseau/shokunin" in out
    assert "shokunin-ssg" in out
    assert "shokunin.crates.io" in out


def test_transform_keeps_lowercase_inside_paths():
    inp = "src=\"/shokunin/logo.svg\" alt=\"shokunin\""
    out = rs.transform(inp)
    assert "/shokunin/logo.svg" in out
    # Inside attribute value next to `\"` — that's not a URL-ish char, so
    # rewrite WILL fire on the bare `shokunin` quoted alt. That's accepted
    # behaviour (prose-like).
    assert "Static Site Generator" in out


def test_transform_idempotent_when_no_match():
    src = "no mention here at all"
    assert rs.transform(src) == src


# ---------------------------------------------------------------------------
# file_targets
# ---------------------------------------------------------------------------


def test_file_targets_walks_configured_dirs(tmp_path, monkeypatch):
    monkeypatch.setattr(rs, "REPO", tmp_path)
    posts = tmp_path / "_posts"
    drafts = tmp_path / "_drafts"
    layouts = tmp_path / "_layouts"
    for d in (posts, drafts, layouts):
        d.mkdir()
    (posts / "a.md").write_text("x", encoding="utf-8")
    (drafts / "b.html").write_text("x", encoding="utf-8")
    (layouts / "c.html").write_text("x", encoding="utf-8")
    (posts / "skip.png").write_text("not text", encoding="utf-8")

    out = rs.file_targets()
    names = sorted(p.name for p in out)
    assert names == ["a.md", "b.html", "c.html"]


def test_file_targets_skips_missing_dirs(tmp_path, monkeypatch):
    monkeypatch.setattr(rs, "REPO", tmp_path)
    assert rs.file_targets() == []


def test_file_targets_includes_extra_files(tmp_path, monkeypatch):
    monkeypatch.setattr(rs, "REPO", tmp_path)
    (tmp_path / "Makefile").write_text("make-rule", encoding="utf-8")
    out = rs.file_targets()
    assert any(p.name == "Makefile" for p in out)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def test_main_rewrites_affected_files(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(rs, "REPO", tmp_path)
    posts = tmp_path / "_posts"
    posts.mkdir()
    (posts / "a.md").write_text("Shokunin is fast", encoding="utf-8")
    (posts / "b.md").write_text("unrelated content", encoding="utf-8")

    rc = rs.main()
    assert rc == 0
    assert (posts / "a.md").read_text(encoding="utf-8") == "Static Site Generator is fast"
    # b.md untouched
    assert (posts / "b.md").read_text(encoding="utf-8") == "unrelated content"
    msg = capsys.readouterr().out
    assert "1 file(s)" in msg


def test_main_skips_files_with_undecodable_bytes(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(rs, "REPO", tmp_path)
    posts = tmp_path / "_posts"
    posts.mkdir()
    (posts / "binary.md").write_bytes(b"\xff\xfe\x00\x00")

    rc = rs.main()
    assert rc == 0
    # File untouched (still bad bytes).
    assert (posts / "binary.md").read_bytes() == b"\xff\xfe\x00\x00"


def test_main_no_op_on_clean_tree(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(rs, "REPO", tmp_path)
    rc = rs.main()
    assert rc == 0
    assert "0 occurrence(s) across 0 file(s)" in capsys.readouterr().out
