"""Unit tests for the auto-discover behaviour in gen_articles.py.

The daily-publishing routine should not need to hand-edit
``scripts/gen_articles.py`` to make tomorrow's article appear on
``/articles/``. ``_discover_latest_article()`` walks ``_posts/`` and
yields an ARTICLES-shaped tuple if it finds anything newer than the
current ARTICLES[0].
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import gen_articles

_SAMPLE_FM = """---
title: "Tomorrow's headline"
banner: "https://cloudcdn.pro/stocks/images/x.webp"
banner_alt: "Tomorrow's banner alt"
excerpt: "A one-sentence excerpt about tomorrow's article."
tags: "topic one, topic two, topic three, extra topic"
date: "May 21, 2026"
---

# Body

prose
"""


def test_parse_frontmatter_returns_dict_for_well_formed_post():
    fm, _body = gen_articles.parse_frontmatter(_SAMPLE_FM)
    assert fm["title"] == "Tomorrow's headline"
    assert fm["tags"].startswith("topic one")


def test_parse_frontmatter_returns_empty_for_unframed_text():
    fm, body = gen_articles.parse_frontmatter("no frontmatter")
    assert fm == {}
    assert body == "no frontmatter"


def test_parse_frontmatter_returns_empty_when_closing_delim_missing():
    fm, _body = gen_articles.parse_frontmatter("---\ntitle: 'x'\n\nbody")
    assert fm == {}


def test_eyebrow_picks_first_three_tags_titlecased():
    out = gen_articles._eyebrow_from_tags("alpha, beta, gamma, delta")
    assert out == "Alpha · Beta · Gamma"


def test_eyebrow_handles_empty_tags():
    assert gen_articles._eyebrow_from_tags("") == ""


def test_display_date_converts_iso_to_month_day_year():
    """display_date now lives in _core; gen_articles imports it."""
    assert gen_articles.display_date("2026-05-20") == "May 20, 2026"
    assert gen_articles.display_date("2026-01-01") == "January 1, 2026"


def test_discover_returns_none_when_no_post_newer_than_articles_head(monkeypatch, tmp_path):
    """If `_posts/` has nothing newer than ARTICLES[0]'s date, no auto-prepend."""
    posts = tmp_path / "_posts"
    posts.mkdir()
    # Seed an OLDER post than ARTICLES[0] (which is 2026-05-20 today).
    (posts / "2024-01-01-some-old-post.md").write_text(_SAMPLE_FM, encoding="utf-8")
    monkeypatch.setattr(gen_articles, "POSTS", posts)
    assert gen_articles._discover_latest_article() is None


def test_discover_returns_tuple_when_newer_post_exists(monkeypatch, tmp_path):
    posts = tmp_path / "_posts"
    posts.mkdir()
    (posts / "2099-12-31-tomorrows-article.md").write_text(
        _SAMPLE_FM, encoding="utf-8",
    )
    monkeypatch.setattr(gen_articles, "POSTS", posts)
    tup = gen_articles._discover_latest_article()
    assert tup is not None
    date_iso, date_display, eyebrow, title, banner, _banner_alt, _excerpt, href = tup
    assert date_iso == "2099-12-31"
    assert date_display == "December 31, 2099"
    assert title == "Tomorrow's headline"
    assert banner == "https://cloudcdn.pro/stocks/images/x.webp"
    assert "Topic One" in eyebrow
    assert href == "/2099-12-31-tomorrows-article/index.html"


def test_discover_returns_none_when_post_lacks_title(monkeypatch, tmp_path):
    posts = tmp_path / "_posts"
    posts.mkdir()
    bad = "---\nbanner: \"x\"\n---\nno-title\n"
    (posts / "2099-12-31-x.md").write_text(bad, encoding="utf-8")
    monkeypatch.setattr(gen_articles, "POSTS", posts)
    assert gen_articles._discover_latest_article() is None


def test_discover_falls_back_to_subtitle_then_description_for_excerpt(monkeypatch, tmp_path):
    posts = tmp_path / "_posts"
    posts.mkdir()
    fm = (
        '---\ntitle: "T"\nbanner: "b"\nbanner_alt: "ba"\n'
        'subtitle: "Subtitle takes over when excerpt missing"\n'
        'tags: "alpha"\ndate: "May 21, 2099"\n---\nbody'
    )
    (posts / "2099-12-31-x.md").write_text(fm, encoding="utf-8")
    monkeypatch.setattr(gen_articles, "POSTS", posts)
    tup = gen_articles._discover_latest_article()
    assert tup is not None
    assert "Subtitle takes over" in tup[6]


def test_discover_returns_none_when_posts_dir_missing(monkeypatch, tmp_path):
    monkeypatch.setattr(gen_articles, "POSTS", tmp_path / "missing")
    assert gen_articles._discover_latest_article() is None


def test_discover_returns_none_when_only_non_dated_posts_present(monkeypatch, tmp_path):
    posts = tmp_path / "_posts"
    posts.mkdir()
    (posts / "about.md").write_text(_SAMPLE_FM, encoding="utf-8")
    monkeypatch.setattr(gen_articles, "POSTS", posts)
    assert gen_articles._discover_latest_article() is None
