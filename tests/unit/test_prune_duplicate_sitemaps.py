# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""ssg's per-directory sitemap copies must not survive into the deploy."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
sys.path.insert(0, str(ROOT / "scripts" / "postbuild"))

import prune_duplicate_sitemaps as pruner


def _touch(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("<urlset/>", encoding="utf-8")
    return path


@pytest.fixture
def tree(tmp_path: Path) -> Path:
    public = tmp_path / "public"
    _touch(public / "sitemap.xml")
    _touch(public / "news-sitemap.xml")
    _touch(public / "fr" / "news-sitemap.xml")
    _touch(public / "fr" / "sitemap.xml")
    _touch(public / "tags" / "sitemap.xml")
    _touch(public / "tags" / "news-sitemap.xml")
    _touch(public / "2026-08-04-a-post" / "sitemap.xml")
    _touch(public / "made-with" / "nested" / "news-sitemap.xml")
    _touch(public / "rss.xml")  # unrelated, must survive
    return public


def test_root_sitemaps_survive(tree: Path) -> None:
    pruner.prune(tree)
    assert (tree / "sitemap.xml").is_file()
    assert (tree / "news-sitemap.xml").is_file()


def test_locale_news_sitemap_survives(tree: Path) -> None:
    """build_lang_feeds.py writes these deliberately, per active locale."""
    pruner.prune(tree)
    assert (tree / "fr" / "news-sitemap.xml").is_file()


def test_locale_plain_sitemap_is_pruned(tree: Path) -> None:
    """Only the root sitemap.xml is real — there is no sitemap index."""
    pruner.prune(tree)
    assert not (tree / "fr" / "sitemap.xml").exists()


def test_page_directory_copies_are_pruned(tree: Path) -> None:
    pruner.prune(tree)
    assert not (tree / "tags" / "sitemap.xml").exists()
    assert not (tree / "tags" / "news-sitemap.xml").exists()
    assert not (tree / "2026-08-04-a-post" / "sitemap.xml").exists()
    assert not (tree / "made-with" / "nested" / "news-sitemap.xml").exists()


def test_unrelated_files_untouched(tree: Path) -> None:
    pruner.prune(tree)
    assert (tree / "rss.xml").is_file()


def test_returns_the_removal_count(tree: Path) -> None:
    assert pruner.prune(tree) == 5


def test_is_idempotent(tree: Path) -> None:
    pruner.prune(tree)
    assert pruner.prune(tree) == 0


def test_missing_public_dir_is_a_noop(tmp_path: Path) -> None:
    assert pruner.prune(tmp_path / "nope") == 0
