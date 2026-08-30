# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Unit coverage for the /articles/ listing generator — Phase 1.3.

`scripts/generators/build_listings.py` builds the article index that
surfaces every post (high blast radius — a regression here silently drops
articles from discovery), but had no unit tests. These cover its pure
data-extraction and rendering helpers.
"""

from __future__ import annotations

from pathlib import Path

import build_listings as bl

# --- _esc ------------------------------------------------------------------


def test_esc_escapes_html_metacharacters() -> None:
    assert bl._esc("a & b < c > d \" e ' f") == ("a &amp; b &lt; c &gt; d &quot; e &#x27; f")


# --- _alias_map ------------------------------------------------------------


def test_alias_map_maps_slug_and_aliases_lowercased() -> None:
    taxonomy = {
        "agentic-ai": {"category": "ai", "aliases": ["Agentic AI", "agents"]},
        "iso-20022": {"category": "payments"},
    }
    amap = bl._alias_map(taxonomy)
    assert amap["agentic-ai"] == "agentic-ai"
    assert amap["agentic ai"] == "agentic-ai"  # alias, lowercased
    assert amap["agents"] == "agentic-ai"
    assert amap["iso-20022"] == "iso-20022"


# --- _post_pillars ---------------------------------------------------------

_TAXONOMY = {
    "agentic-ai": {"category": "ai", "aliases": ["Agentic AI"]},
    "iso-20022": {"category": "payments", "aliases": ["ISO 20022"]},
}
_AMAP = bl._alias_map(_TAXONOMY)


def test_post_pillars_resolves_tags_through_aliases_in_pillar_order() -> None:
    text = 'tags: "ISO 20022, Agentic AI"\n'
    # PILLAR_ORDER puts "ai" before "payments" regardless of tag order.
    assert bl._post_pillars(text, _TAXONOMY, _AMAP) == ["ai", "payments"]


def test_post_pillars_empty_when_no_tags_or_unknown() -> None:
    assert bl._post_pillars("title: x\n", _TAXONOMY, _AMAP) == []
    assert bl._post_pillars('tags: "totally-unknown"\n', _TAXONOMY, _AMAP) == []


# --- _post_card_fields -----------------------------------------------------


def _write(tmp: Path, name: str, body: str) -> Path:
    p = tmp / name
    p.write_text(body, encoding="utf-8")
    return p


def test_post_card_fields_extracts_frontmatter(tmp_path: Path) -> None:
    md = _write(
        tmp_path,
        "2026-06-30-example-article.md",
        'title: "An Example Title"\n'
        'excerpt: "The card excerpt."\n'
        'description: "The meta description."\n'
        'banner: "https://cloudcdn.pro/stocks/images/x-1920.webp"\n'
        'banner_alt: "Banner alt text"\n'
        'tags: "Agentic AI"\n\n# Body\n',
    )
    out = bl._post_card_fields(md, _TAXONOMY, _AMAP)
    assert out is not None
    title, iso, slug, excerpt, pillars, banner, banner_alt = out
    assert title == "An Example Title"
    assert iso == "2026-06-30"
    assert slug == "2026-06-30-example-article"
    assert excerpt == "The card excerpt."  # excerpt wins over description
    assert pillars == ["ai"]
    assert banner == "https://cloudcdn.pro/stocks/images/x-1920.webp"
    assert banner_alt == "Banner alt text"


def test_post_card_fields_excerpt_falls_back_to_description(tmp_path: Path) -> None:
    md = _write(
        tmp_path,
        "2026-06-30-no-excerpt.md",
        'title: "T"\ndescription: "Only a description."\n\n# Body\n',
    )
    out = bl._post_card_fields(md, {}, {})
    assert out is not None
    assert out[3] == "Only a description."
    assert out[5] == bl._DEFAULT_BANNER  # default banner when none set
    assert out[6] == "T"  # banner_alt defaults to title


def test_post_card_fields_returns_none_for_non_dated(tmp_path: Path) -> None:
    md = _write(tmp_path, "about.md", 'title: "About"\n')
    assert bl._post_card_fields(md, {}, {}) is None


# --- _render_pagination ----------------------------------------------------


def test_pagination_single_page_is_empty() -> None:
    assert bl._render_pagination(1, 1, "/articles") == ""


def test_pagination_first_page_has_next_not_prev() -> None:
    html = bl._render_pagination(1, 3, "/articles")
    assert 'rel="prev"' not in html
    assert 'rel="next"' in html
    assert "/articles/page/2/" in html
    assert "/articles/page/3/" in html
    assert 'aria-current="page">1<' in html  # page 1 is current


def test_pagination_middle_page_has_prev_and_next() -> None:
    html = bl._render_pagination(2, 3, "/articles")
    assert 'href="/articles/" rel="prev"' in html  # page 1 → base/
    assert "/articles/page/3/" in html
    assert 'aria-current="page">2<' in html
