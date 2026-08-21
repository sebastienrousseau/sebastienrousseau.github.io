"""Byte-identical /_csp/ assets collapse onto one URL (F-10).

Each layout embeds the site stylesheet inline and ssg extracts each layout's
block to its own fingerprinted file — fingerprinted per layout, not per
content. Two 138 KB bundles differing in six bytes covered 82 % of pages
between them, so crossing from an article to a listing re-downloaded ~25 KB
gzipped of bytes the reader already had.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "postbuild"))

from postbuild_lib.asset_dedupe import (
    find_duplicate_assets,
    remove_duplicate_files,
    rewrite_asset_refs,
)


@pytest.fixture
def public(tmp_path: Path) -> Path:
    root = tmp_path / "public"
    csp = root / "_csp"
    csp.mkdir(parents=True)
    (csp / "aaa11111.css").write_text("body{color:red}", encoding="utf-8")
    (csp / "bbb22222.css").write_text("body{color:red}", encoding="utf-8")  # identical
    (csp / "ccc33333.css").write_text("body{color:blue}", encoding="utf-8")  # unique
    (csp / "ddd44444.js").write_text("console.log(1)", encoding="utf-8")
    (csp / "eee55555.js").write_text("console.log(1)", encoding="utf-8")  # identical
    (csp / "notes.txt").write_text("body{color:red}", encoding="utf-8")  # wrong suffix
    return root


def test_identical_css_is_detected(public: Path) -> None:
    assert find_duplicate_assets(public)["/_csp/bbb22222.css"] == "/_csp/aaa11111.css"


def test_identical_js_is_detected(public: Path) -> None:
    assert find_duplicate_assets(public)["/_csp/eee55555.js"] == "/_csp/ddd44444.js"


def test_unique_assets_are_not_mapped(public: Path) -> None:
    assert "/_csp/ccc33333.css" not in find_duplicate_assets(public)


def test_keeper_is_never_mapped_away(public: Path) -> None:
    mapping = find_duplicate_assets(public)
    assert "/_csp/aaa11111.css" not in mapping
    assert "/_csp/ddd44444.js" not in mapping


def test_non_asset_suffixes_are_ignored(public: Path) -> None:
    """notes.txt shares bytes with the CSS but is not an asset."""
    assert not any("notes.txt" in k for k in find_duplicate_assets(public))


def test_keeper_choice_is_stable(public: Path) -> None:
    """The surviving URL must not move between rebuilds — the
    reproducibility gate diffs whole trees."""
    assert find_duplicate_assets(public) == find_duplicate_assets(public)


def test_missing_asset_dir_is_a_noop(tmp_path: Path) -> None:
    assert find_duplicate_assets(tmp_path / "nope") == {}


def test_references_are_rewritten(public: Path) -> None:
    mapping = find_duplicate_assets(public)
    html = '<link rel="stylesheet" href="/_csp/bbb22222.css">'
    assert rewrite_asset_refs(html, mapping) == (
        '<link rel="stylesheet" href="/_csp/aaa11111.css">'
    )


def test_unaffected_references_are_untouched(public: Path) -> None:
    mapping = find_duplicate_assets(public)
    html = '<link href="/_csp/ccc33333.css"><script src="/main.abc.js"></script>'
    assert rewrite_asset_refs(html, mapping) == html


def test_empty_mapping_is_a_noop() -> None:
    html = '<link href="/_csp/x.css">'
    assert rewrite_asset_refs(html, {}) is html


def test_rewrite_is_idempotent(public: Path) -> None:
    mapping = find_duplicate_assets(public)
    html = '<link href="/_csp/bbb22222.css"><link href="/_csp/eee55555.js">'
    once = rewrite_asset_refs(html, mapping)
    assert rewrite_asset_refs(once, mapping) == once


def test_duplicates_are_deleted_and_keepers_survive(public: Path) -> None:
    mapping = find_duplicate_assets(public)
    assert remove_duplicate_files(public, mapping) == 2
    assert not (public / "_csp" / "bbb22222.css").exists()
    assert not (public / "_csp" / "eee55555.js").exists()
    assert (public / "_csp" / "aaa11111.css").is_file()
    assert (public / "_csp" / "ccc33333.css").is_file()


def test_removal_is_idempotent(public: Path) -> None:
    mapping = find_duplicate_assets(public)
    remove_duplicate_files(public, mapping)
    assert remove_duplicate_files(public, mapping) == 0


def test_dedupe_never_changes_delivered_bytes(public: Path) -> None:
    """Content-addressed: the bytes a page receives are identical either way."""
    before = (public / "_csp" / "bbb22222.css").read_bytes()
    mapping = find_duplicate_assets(public)
    remove_duplicate_files(public, mapping)
    canonical = mapping["/_csp/bbb22222.css"].lstrip("/")
    assert (public / canonical).read_bytes() == before
