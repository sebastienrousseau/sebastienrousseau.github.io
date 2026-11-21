# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Thin listing pages (tag and category terms, page 2+ of a listing) are
published but kept out of the index: ``noindex, follow``."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
sys.path.insert(0, str(ROOT / "scripts" / "postbuild"))

from postbuild_lib import thin_listings as tl

CODES = frozenset({"fr", "pt-br"})


@pytest.mark.parametrize(
    "rel",
    [
        "tags/agentic-ai/index.html",
        "fr/tags/agentic-ai/index.html",
        "categories/payments/index.html",
        "pt-br/categories/payments/index.html",
        "articles/page/2/index.html",
        "fr/articles/page/12/index.html",
        "pt-br/artigos/page/3/index.html",
    ],
)
def test_thin_listings_are_detected(rel: str) -> None:
    assert tl.is_thin_listing(rel, CODES)


@pytest.mark.parametrize(
    "rel",
    [
        "index.html",
        "tags/index.html",
        "fr/tags/index.html",
        "categories/index.html",
        "articles/index.html",
        "articles/page/1/index.html",
        "topics/post-quantum-cryptography/index.html",
        "2026-11-17-treasury-automation-half-done/index.html",
        "fr/2026-11-17-tresorerie/index.html",
        "tags/agentic-ai/rss.xml",
        "xx/tags/agentic-ai/index.html",
        "2026-05-01-tags-explained/index.html",
    ],
)
def test_hubs_articles_and_first_pages_stay_indexable(rel: str) -> None:
    assert not tl.is_thin_listing(rel, CODES)


def _page(robots: str = "max-snippet:-1") -> str:
    return f'<html><head><meta name="robots" content="{robots}"><title>t</title></head></html>'


def test_apply_noindexes_only_thin_listings_and_is_idempotent(tmp_path: Path) -> None:
    files = {
        "tags/agentic-ai/index.html": _page(),
        "fr/articles/page/2/index.html": _page(),
        "articles/index.html": _page(),
        "tags/index.html": _page(),
    }
    for rel, html in files.items():
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_text(html, encoding="utf-8")

    assert tl.apply_thin_noindex(tmp_path, CODES) == 2
    tag = (tmp_path / "tags/agentic-ai/index.html").read_text(encoding="utf-8")
    assert 'content="noindex, follow, max-snippet:-1"' in tag
    assert "noindex" in (tmp_path / "fr/articles/page/2/index.html").read_text(encoding="utf-8")
    assert "noindex" not in (tmp_path / "articles/index.html").read_text(encoding="utf-8")
    assert "noindex" not in (tmp_path / "tags/index.html").read_text(encoding="utf-8")
    assert tl.apply_thin_noindex(tmp_path, CODES) == 0
