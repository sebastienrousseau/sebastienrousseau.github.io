"""Unit coverage for regen_slug_maps — Phase 1.3.

regen_slug_maps.py derives each locale's article slug map from on-disk
filenames (so article PRs stay additive). Its per-date pairing logic (sticky /
exact-stem / sorted-residual) is subtle and drives hreflang correctness, but
was untested. Cover the EN-index and the pairing algorithm.
"""

from __future__ import annotations

from pathlib import Path

import regen_slug_maps as rsm


def _touch(d: Path, *names: str) -> None:
    d.mkdir(parents=True, exist_ok=True)
    for n in names:
        (d / f"{n}.md").write_text("x", encoding="utf-8")


# --- _index_en_slugs_by_date -----------------------------------------------


def test_index_en_slugs_by_date_groups_and_sorts(tmp_path, monkeypatch) -> None:
    posts = tmp_path / "_posts"
    _touch(posts, "2026-06-29-zeta", "2026-06-29-alpha", "2026-06-28-solo", "about")
    monkeypatch.setattr(rsm, "POSTS", posts)
    idx = rsm._index_en_slugs_by_date()
    assert idx["2026-06-29"] == ["2026-06-29-alpha", "2026-06-29-zeta"]  # sorted
    assert idx["2026-06-28"] == ["2026-06-28-solo"]
    assert "about" not in str(idx)  # non-dated ignored


# --- _articles_map_for_language --------------------------------------------


def test_map_exact_stem_match(tmp_path) -> None:
    lang = tmp_path / "fr"
    _touch(lang, "2026-06-29-post")  # EN-named locale file
    en_by_date = {"2026-06-29": ["2026-06-29-post"]}
    assert rsm._articles_map_for_language(lang, en_by_date) == {
        "2026-06-29-post": "2026-06-29-post"
    }


def test_map_sticky_preference_wins(tmp_path) -> None:
    lang = tmp_path / "fr"
    _touch(lang, "2026-06-29-article-fr")
    en_by_date = {"2026-06-29": ["2026-06-29-article"]}
    prev = {"2026-06-29-article": "2026-06-29-article-fr"}
    out = rsm._articles_map_for_language(lang, en_by_date, previous=prev)
    assert out == {"2026-06-29-article": "2026-06-29-article-fr"}


def test_map_sorted_residual_pairing(tmp_path) -> None:
    lang = tmp_path / "fr"
    _touch(lang, "2026-06-29-magnifica-q", "2026-06-29-stablecoins-t")
    en_by_date = {"2026-06-29": ["2026-06-29-magnifica", "2026-06-29-stablecoins"]}
    out = rsm._articles_map_for_language(lang, en_by_date)
    assert out["2026-06-29-magnifica"] == "2026-06-29-magnifica-q"
    assert out["2026-06-29-stablecoins"] == "2026-06-29-stablecoins-t"


def test_map_empty_lang_dir(tmp_path) -> None:
    assert rsm._articles_map_for_language(tmp_path / "nope", {"2026-06-29": ["x"]}) == {}


def test_map_skips_dates_absent_from_en_index(tmp_path) -> None:
    lang = tmp_path / "fr"
    _touch(lang, "2020-01-01-orphan-fr")  # date not in en_by_date
    assert rsm._articles_map_for_language(lang, {"2026-06-29": ["2026-06-29-x"]}) == {}
