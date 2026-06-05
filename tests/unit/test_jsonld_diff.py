"""Unit tests for scripts/jsonld_diff.py.

The file is a small, pure pipeline:
  extract_blocks → index → diff_pages → main

Covering each pure function plus a fixture-driven main() drives the
module to ~100% with no real-tree dependency."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import jsonld_diff as jd

# ---------------------------------------------------------------------------
# extract_blocks
# ---------------------------------------------------------------------------


def test_extract_blocks_returns_parsed_jsonld(tmp_path):
    page = tmp_path / "page.html"
    page.write_text(
        "<html><head>"
        '<script type="application/ld+json">{"@type": "Person", "name": "Seb"}</script>'
        '<script type="application/ld+json">{"@graph":[{"@type":"WebSite"}]}</script>'
        "</head></html>",
        encoding="utf-8",
    )
    blocks = jd.extract_blocks(page)
    assert len(blocks) == 2
    assert blocks[0]["@type"] == "Person"
    assert blocks[1]["@graph"][0]["@type"] == "WebSite"


def test_extract_blocks_ignores_invalid_json(tmp_path):
    page = tmp_path / "p.html"
    page.write_text(
        '<script type="application/ld+json">{not valid json</script>'
        '<script type="application/ld+json">{"@type":"X"}</script>',
        encoding="utf-8",
    )
    blocks = jd.extract_blocks(page)
    assert len(blocks) == 1
    assert blocks[0]["@type"] == "X"


def test_extract_blocks_strips_html_comments(tmp_path):
    page = tmp_path / "p.html"
    page.write_text(
        '<!-- <script type="application/ld+json">{"@type":"Hidden"}</script> -->'
        '<script type="application/ld+json">{"@type":"Visible"}</script>',
        encoding="utf-8",
    )
    blocks = jd.extract_blocks(page)
    assert len(blocks) == 1
    assert blocks[0]["@type"] == "Visible"


def test_extract_blocks_handles_no_jsonld(tmp_path):
    page = tmp_path / "p.html"
    page.write_text("<html><body>no jsonld here</body></html>", encoding="utf-8")
    assert jd.extract_blocks(page) == []


# ---------------------------------------------------------------------------
# index
# ---------------------------------------------------------------------------


def test_index_walks_html_tree(tmp_path):
    (tmp_path / "a.html").write_text(
        '<script type="application/ld+json">{"@type":"A"}</script>',
        encoding="utf-8",
    )
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "b.html").write_text(
        '<script type="application/ld+json">{"@type":"B"}</script>',
        encoding="utf-8",
    )
    (tmp_path / "skip.txt").write_text("not html", encoding="utf-8")

    out = jd.index(tmp_path)
    assert set(out.keys()) == {"a.html", "sub/b.html"}
    assert out["a.html"][0]["@type"] == "A"


def test_index_returns_empty_when_root_missing(tmp_path):
    assert jd.index(tmp_path / "does-not-exist") == {}


# ---------------------------------------------------------------------------
# summarise_block
# ---------------------------------------------------------------------------


def test_summarise_block_dict_with_graph():
    blk = {"@graph": [{"@type": "WebSite"}, {"@type": "Person"}]}
    assert jd.summarise_block(blk) == "@graph[WebSite, Person]"


def test_summarise_block_dict_with_simple_type():
    assert jd.summarise_block({"@type": "BlogPosting"}) == "@type:BlogPosting"


def test_summarise_block_list_of_blocks():
    assert jd.summarise_block([{"@type": "A"}, {"@type": "B"}]) == "list[2 blocks]"


def test_summarise_block_unknown_shape():
    assert jd.summarise_block(42) == "?"


def test_summarise_block_dict_missing_type():
    assert jd.summarise_block({}) == "@type:?"


# ---------------------------------------------------------------------------
# diff_pages
# ---------------------------------------------------------------------------


def test_diff_pages_no_changes_returns_success_marker():
    out = jd.diff_pages({}, {})
    assert "No structured-data changes" in out


def test_diff_pages_reports_added_pages():
    base = {}
    head = {"new.html": [{"@type": "Article"}]}
    out = jd.diff_pages(base, head)
    assert "1 page(s) added" in out
    assert "new.html" in out
    assert "@type:Article" in out


def test_diff_pages_reports_removed_pages():
    out = jd.diff_pages({"old.html": [{"@type": "X"}]}, {})
    assert "1 page(s) removed" in out
    assert "old.html" in out


def test_diff_pages_reports_changed_pages_same_shape():
    base = {"p.html": [{"@type": "Article", "name": "Old"}]}
    head = {"p.html": [{"@type": "Article", "name": "New"}]}
    out = jd.diff_pages(base, head)
    assert "1 page(s) with schema changes" in out
    assert "content changed" in out


def test_diff_pages_reports_changed_pages_different_shape():
    base = {"p.html": [{"@type": "Article"}]}
    head = {"p.html": [{"@type": "BlogPosting"}]}
    out = jd.diff_pages(base, head)
    assert "was: @type:Article" in out
    assert "now: @type:BlogPosting" in out


def test_diff_pages_truncates_long_added_lists():
    head = {f"page{i}.html": [{"@type": "X"}] for i in range(30)}
    out = jd.diff_pages({}, head)
    assert "and 5 more" in out


def test_diff_pages_truncates_long_removed_lists():
    base = {f"p{i}.html": [{"@type": "X"}] for i in range(30)}
    out = jd.diff_pages(base, {})
    assert "and 5 more" in out


def test_diff_pages_truncates_long_changed_lists():
    base = {f"p{i}.html": [{"@type": "Article", "n": i}] for i in range(30)}
    head = {f"p{i}.html": [{"@type": "Article", "n": i + 1}] for i in range(30)}
    out = jd.diff_pages(base, head)
    assert "and 5 more" in out


def test_diff_pages_empty_blocks_render_empty_marker():
    """When a page has no JSON-LD blocks, summary should fall back to (empty)."""
    base = {}
    head = {"page.html": []}
    out = jd.diff_pages(base, head)
    assert "(empty)" in out


# ---------------------------------------------------------------------------
# main entrypoint
# ---------------------------------------------------------------------------


def test_main_runs_against_two_fixture_trees(tmp_path, monkeypatch, capsys):
    base = tmp_path / "base"
    head = tmp_path / "head"
    base.mkdir()
    head.mkdir()
    (base / "p.html").write_text(
        '<script type="application/ld+json">{"@type":"A"}</script>',
        encoding="utf-8",
    )
    (head / "p.html").write_text(
        '<script type="application/ld+json">{"@type":"B"}</script>',
        encoding="utf-8",
    )
    monkeypatch.setattr(sys, "argv", ["jsonld_diff", str(base), str(head)])
    rc = jd.main()
    assert rc == 0
    out = capsys.readouterr().out
    assert "@type:A" in out
    assert "@type:B" in out


def test_main_missing_base_dir_yields_empty_diff(tmp_path, monkeypatch, capsys):
    """index() returns {} for missing dirs, so a missing base yields a no-pages diff."""
    head = tmp_path / "head"
    head.mkdir()
    (head / "x.html").write_text(
        '<script type="application/ld+json">{"@type":"NewThing"}</script>',
        encoding="utf-8",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["jsonld_diff", str(tmp_path / "missing"), str(head)],
    )
    rc = jd.main()
    assert rc == 0
    out = capsys.readouterr().out
    assert "1 page(s) added" in out


def test_main_no_args_exits_via_argparse(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["jsonld_diff"])
    with pytest.raises(SystemExit):
        jd.main()
