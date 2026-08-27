"""Unit coverage for the /tags/ cover generator — Phase 1.3.

`scripts/generators/build_tags.py` builds the curated /tags/ cover (pillar
cards, featured topics, A–Z canonicals) from the taxonomy + post frontmatter.
It had no unit tests despite driving topic discovery. These cover its pure
data-extraction and rendering helpers.
"""

from __future__ import annotations

import collections
from pathlib import Path

import build_tags as bt

# --- _alias_map ------------------------------------------------------------


def test_alias_map_maps_slug_and_aliases_lowercased() -> None:
    taxonomy = {
        "agentic-ai": {"category": "ai", "aliases": ["Agentic AI", "agents"]},
        "iso-20022": {"category": "payments"},
    }
    amap = bt._alias_map(taxonomy)
    assert amap["agentic-ai"] == "agentic-ai"
    assert amap["agentic ai"] == "agentic-ai"  # alias, lowercased
    assert amap["agents"] == "agentic-ai"
    assert amap["iso-20022"] == "iso-20022"


def test_alias_map_tolerates_missing_aliases_key() -> None:
    amap = bt._alias_map({"rust": {"category": "open-source"}})
    assert amap == {"rust": "rust"}


# --- _post_meta ------------------------------------------------------------

_POST = '---\ntitle: "The Quantum Age"\ntags: "post-quantum, cryptography"\n---\nbody text\n'


def test_post_meta_extracts_title_date_slug_tags(tmp_path: Path) -> None:
    p = tmp_path / "2026-06-29-the-quantum-age.md"
    p.write_text(_POST, encoding="utf-8")
    meta = bt._post_meta(p)
    assert meta is not None
    title, iso_date, slug, tags_line = meta
    assert title == "The Quantum Age"
    assert iso_date == "2026-06-29"
    assert slug == "2026-06-29-the-quantum-age"
    assert tags_line == "post-quantum, cryptography"


def test_post_meta_returns_none_without_tags(tmp_path: Path) -> None:
    p = tmp_path / "2026-06-29-no-tags.md"
    p.write_text('---\ntitle: "No Tags"\n---\nbody\n', encoding="utf-8")
    assert bt._post_meta(p) is None


def test_post_meta_blank_date_for_non_dated_stem(tmp_path: Path) -> None:
    p = tmp_path / "about.md"
    p.write_text(_POST, encoding="utf-8")
    meta = bt._post_meta(p)
    assert meta is not None
    _title, iso_date, slug, _tags = meta
    assert iso_date == ""  # no YYYY-MM-DD prefix
    assert slug == "about"


# --- _group_by_pillar ------------------------------------------------------

_TAXONOMY = {
    "agentic-ai": {"category": "ai", "name": "Agentic AI"},
    "llms": {"category": "ai", "name": "LLMs"},
    "iso-20022": {"category": "payments", "name": "ISO 20022"},
}


def test_group_by_pillar_sorts_by_count_desc() -> None:
    counts = collections.Counter({"agentic-ai": 2, "llms": 5, "iso-20022": 3})
    groups = bt._group_by_pillar(_TAXONOMY, counts)
    assert groups["ai"] == ["llms", "agentic-ai"]  # 5 before 2
    assert groups["payments"] == ["iso-20022"]


def test_group_by_pillar_has_all_pillar_keys() -> None:
    groups = bt._group_by_pillar(_TAXONOMY, collections.Counter())
    for pillar in bt.PILLAR_ORDER:
        assert pillar in groups


# --- _render_featured_tags -------------------------------------------------


def test_render_featured_tags_respects_threshold_and_cap() -> None:
    tax = {f"t{i}": {"category": "ai", "name": f"Tag {i}"} for i in range(20)}
    counts = collections.Counter({f"t{i}": i for i in range(20)})  # t0..t2 below threshold
    out = bt._render_featured_tags(tax, counts)
    # Below-threshold tags (count < 3) are excluded — check by unique aria-label.
    assert 'aria-label="Tag 1 — 1 articles"' not in out
    assert 'aria-label="Tag 2 — 2 articles"' not in out
    assert 'aria-label="Tag 19 — 19 articles"' in out
    # Capped at _FEATURED_TOP_N cards.
    assert out.count('class="tag-featured-card"') == bt._FEATURED_TOP_N


def test_render_featured_tags_labels_article_count() -> None:
    tax = {"rust": {"category": "open-source", "name": "Rust"}}
    out = bt._render_featured_tags(tax, collections.Counter({"rust": 7}))
    assert "Rust — 7 articles" in out
    assert 'href="#tag-rust"' in out


# --- _render_tag_post_list -------------------------------------------------


def test_render_tag_post_list_empty_is_blank() -> None:
    assert bt._render_tag_post_list([]) == ""


def test_render_tag_post_list_pluralises_and_links() -> None:
    posts = [
        ("First Post", "2026-06-29", "2026-06-29-first-post"),
        ("Second Post", "2026-06-28", "2026-06-28-second-post"),
    ]
    out = bt._render_tag_post_list(posts)
    assert "View 2 articles" in out
    assert '<a href="/2026-06-29-first-post/">First Post</a>' in out
    assert '<time datetime="2026-06-29">2026-06-29</time>' in out


def test_render_tag_post_list_singular() -> None:
    out = bt._render_tag_post_list([("Only", "2026-06-29", "2026-06-29-only")])
    assert "View 1 article</summary>" in out


# --- _render_pillar_cards --------------------------------------------------


def test_render_pillar_cards_covers_all_pillars() -> None:
    counts = collections.Counter({"agentic-ai": 2, "llms": 5, "iso-20022": 3})
    by_pillar = bt._group_by_pillar(_TAXONOMY, counts)
    out = bt._render_pillar_cards(counts, by_pillar)
    assert 'aria-label="Editorial pillars"' in out
    for pillar in bt.PILLAR_ORDER:
        assert f'href="#pillar-{pillar}"' in out
    # ai pillar aggregates its two tags' article counts (2 + 5 = 7)
    assert "7 articles" in out
