# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""The article listing generator — pagination, cards, share rails, archives.

scripts/generators/build_listings.py had 219 uncovered statements. It builds
every paged listing and year archive, in English and in 34 locales, so an
off-by-one in the pagination or a mis-encoded share URL is replicated
thousands of times.

Pagination gets the most attention here because its contract is easy to get
subtly wrong: page 1 lives at `<base>/` and not `<base>/page/1/`, the current
page is a span rather than a link, and prev/next disappear at the ends.
"""

from __future__ import annotations

import urllib.parse as urlparse

import build_listings as bl

# ---------------------------------------------------------------------------
# Escaping
# ---------------------------------------------------------------------------


def test_esc_escapes_the_five_dangerous_characters() -> None:
    out = bl._esc("""<a href="x" title='y'>&</a>""")
    for ch in ("<", ">", '"', "'"):
        assert ch not in out
    assert "&amp;" in out


def test_esc_escapes_the_ampersand_first() -> None:
    """Escaping & last would double-encode the entities just produced."""
    assert bl._esc("<") == "&lt;"
    assert bl._esc("&lt;") == "&amp;lt;"


# ---------------------------------------------------------------------------
# Pagination
# ---------------------------------------------------------------------------


def test_pagination_is_empty_for_a_single_page() -> None:
    """One page needs no navigation at all."""
    assert bl._render_pagination(1, 1, "/articles") == ""
    assert bl._render_pagination(1, 0, "/articles") == ""


def test_pagination_page_one_has_no_previous() -> None:
    out = bl._render_pagination(1, 3, "/articles")
    assert "page-nav-prev" not in out
    assert "page-nav-next" in out


def test_pagination_last_page_has_no_next() -> None:
    out = bl._render_pagination(3, 3, "/articles")
    assert "page-nav-next" not in out
    assert "page-nav-prev" in out


def test_pagination_page_one_url_has_no_page_segment() -> None:
    """Page 1 is `/articles/`, never `/articles/page/1/`."""
    out = bl._render_pagination(2, 3, "/articles")
    assert 'href="/articles/"' in out
    assert "/page/1/" not in out


def test_pagination_numbers_other_pages_with_a_page_segment() -> None:
    out = bl._render_pagination(1, 3, "/articles")
    assert 'href="/articles/page/2/"' in out
    assert 'href="/articles/page/3/"' in out


def test_pagination_marks_the_current_page_as_a_span() -> None:
    """The current page must not be a link to itself."""
    out = bl._render_pagination(2, 3, "/articles")
    assert '<span class="page-nav-num is-current" aria-current="page">2</span>' in out
    assert 'href="/articles/page/2/"' not in out


def test_pagination_emits_every_page_number() -> None:
    out = bl._render_pagination(1, 5, "/articles")
    for n in range(1, 6):
        assert f">{n}<" in out


def test_pagination_uses_the_locale_base_path() -> None:
    out = bl._render_pagination(2, 3, "/fr/articles")
    assert 'href="/fr/articles/"' in out
    assert 'href="/fr/articles/page/3/"' in out


def test_pagination_is_a_labelled_landmark() -> None:
    out = bl._render_pagination(2, 3, "/articles")
    assert 'aria-label="Pagination"' in out


def test_pagination_prev_and_next_carry_rel_hints() -> None:
    out = bl._render_pagination(2, 3, "/articles")
    assert 'rel="prev"' in out
    assert 'rel="next"' in out


# ---------------------------------------------------------------------------
# Chunking and grouping
# ---------------------------------------------------------------------------


def test_chunk_splits_evenly() -> None:
    assert bl._chunk([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]


def test_chunk_keeps_a_short_final_chunk() -> None:
    assert bl._chunk([1, 2, 3], 2) == [[1, 2], [3]]


def test_chunk_of_an_empty_list() -> None:
    assert bl._chunk([], 5) == []


def _post(date: str, slug: str = "s") -> tuple:
    return ("Title", date, slug, "excerpt", [], "banner", "alt")


def test_group_by_year_keys_on_the_date_prefix() -> None:
    groups = bl._group_by_year([_post("2026-01-01"), _post("2025-12-31"), _post("2026-06-06")])
    assert set(groups) == {"2026", "2025"}
    assert len(groups["2026"]) == 2


def test_group_by_year_preserves_input_order_within_a_year() -> None:
    a, b = _post("2026-01-01", "a"), _post("2026-02-02", "b")
    assert [p[2] for p in bl._group_by_year([a, b])["2026"]] == ["a", "b"]


def test_group_by_year_of_nothing() -> None:
    assert bl._group_by_year([]) == {}


# ---------------------------------------------------------------------------
# Share rail
# ---------------------------------------------------------------------------


RAIL = bl._card_share_rail("/2026-01-01-post/", "A Title & Thing", "A description")


def test_share_rail_is_a_group_not_a_landmark() -> None:
    """Every card emits one; 24 <nav> landmarks per page trips landmark-unique."""
    assert 'role="group"' in RAIL
    assert "<nav" not in RAIL


def test_share_rail_makes_the_url_absolute() -> None:
    assert bl._BASE_URL in RAIL


def test_share_rail_leaves_an_already_absolute_url_alone() -> None:
    out = bl._card_share_rail("https://example.com/x/", "T", "D")
    assert out.count("https://example.com/x/") >= 1
    assert f"{bl._BASE_URL}https://" not in out


def test_share_rail_percent_encodes_the_shared_text() -> None:
    """An unencoded & or newline would truncate the share target."""
    assert "A Title & Thing" not in RAIL
    assert urlparse.quote("A Title & Thing", safe="") in RAIL


def test_share_rail_has_all_six_destinations() -> None:
    for host in ("twitter.com", "linkedin.com", "facebook.com", "wa.me", "mailto:"):
        assert host in RAIL
    assert "data-copy-link" in RAIL


def test_share_rail_marks_external_links_noopener() -> None:
    assert RAIL.count('rel="noopener noreferrer"') == 4


def test_share_rail_labels_every_control() -> None:
    """Icon-only controls need an accessible name."""
    assert RAIL.count("aria-label=") == 7  # 6 controls + the group itself


def test_share_rail_copy_button_escapes_its_url() -> None:
    out = bl._card_share_rail('/a"b/', "T", "D")
    assert 'data-copy-link="' in out
    assert '"b/"' not in out.split("data-copy-link=")[1][:60]


# ---------------------------------------------------------------------------
# Card fields from front matter
# ---------------------------------------------------------------------------


def test_post_card_fields_returns_none_for_an_undated_file(tmp_path) -> None:
    p = tmp_path / "glossary.md"
    p.write_text('title: "G"\n', encoding="utf-8")
    assert bl._post_card_fields(p, {}, {}) is None


def test_post_card_fields_reads_the_frontmatter(tmp_path) -> None:
    p = tmp_path / "2026-03-04-a-post.md"
    p.write_text(
        'title: "The Title"\nexcerpt: "The excerpt"\n'
        'banner: "https://cdn/b.webp"\nbanner_alt: "Alt"\n',
        encoding="utf-8",
    )
    title, iso, slug, excerpt, _pillars, banner, alt = bl._post_card_fields(p, {}, {})
    assert (title, iso, slug) == ("The Title", "2026-03-04", "2026-03-04-a-post")
    assert excerpt == "The excerpt"
    assert banner == "https://cdn/b.webp"
    assert alt == "Alt"


def test_post_card_fields_prefers_excerpt_then_description(tmp_path) -> None:
    p = tmp_path / "2026-03-04-x.md"
    p.write_text('title: "T"\ndescription: "The description"\n', encoding="utf-8")
    assert bl._post_card_fields(p, {}, {})[3] == "The description"


def test_post_card_fields_falls_back_to_the_default_banner_and_title(tmp_path) -> None:
    p = tmp_path / "2026-03-04-x.md"
    p.write_text('title: "The Title"\n', encoding="utf-8")
    fields = bl._post_card_fields(p, {}, {})
    assert fields[5] == bl._DEFAULT_BANNER
    assert fields[6] == "The Title", "alt text falls back to the title, never empty"


def test_post_card_fields_falls_back_to_the_stem_without_a_title(tmp_path) -> None:
    p = tmp_path / "2026-03-04-no-title.md"
    p.write_text('description: "d"\n', encoding="utf-8")
    assert bl._post_card_fields(p, {}, {})[0] == "2026-03-04-no-title"
