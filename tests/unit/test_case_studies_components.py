# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Case-study page components, rendered in English and 34 locales.

scripts/generators/case_studies_components.py had 176 uncovered statements.
Every function here takes study data and returns a fragment of a public page,
so the failures that matter are the quiet ones: a locale link that resolves
to the English article, a share URL whose title truncates at the first
ampersand, or a section that renders an empty shell instead of nothing.

The empty-input contract is tested for every component, because an empty
<section> with a heading and no content is worse than an absent section — it
looks like missing data rather than data that does not apply.
"""

from __future__ import annotations

import json
import re
import urllib.parse as urlparse

import case_studies_components as csc
import pytest

LBL = {
    "Home": "Home",
    "Case studies": "Case studies",
    "By the numbers": "By the numbers",
    "Engineering rigour": "Engineering rigour",
    "Signal": "Signal",
    "Evidence": "Evidence",
    "Role": "Role",
    "Period": "Period",
    "Status": "Status",
    "Sector": "Sector",
    "Verifiable links": "Verifiable links",
    "Share": "Share",
    "Share on X": "Share on X",
    "Share on LinkedIn": "Share on LinkedIn",
    "Related articles": "Related articles",
}


# ---------------------------------------------------------------------------
# Escaping
# ---------------------------------------------------------------------------


def test_esc_handles_none_as_empty() -> None:
    """Missing study fields arrive as None; they must not print 'None'."""
    assert csc._esc(None) == ""


def test_esc_escapes_quotes_because_output_lands_in_attributes() -> None:
    assert '"' not in csc._esc('a "quoted" value')


# ---------------------------------------------------------------------------
# Related-article hrefs — the locale trap
# ---------------------------------------------------------------------------


def test_related_href_is_bare_for_english() -> None:
    assert csc._related_article_href("2026-01-01-post", "en", {}) == "/2026-01-01-post/"


def test_related_href_uses_the_localised_slug() -> None:
    """A locale link must point at the locale article, not the English one."""
    out = csc._related_article_href(
        "2026-01-01-post", "fr", {"2026-01-01-post": "2026-01-01-billet"}
    )
    assert out == "/fr/2026-01-01-billet/"


def test_related_href_falls_back_to_the_english_slug_under_the_locale_prefix() -> None:
    """No mapping is not a reason to drop the locale prefix."""
    assert csc._related_article_href("2026-01-01-post", "fr", {}) == "/fr/2026-01-01-post/"


def test_related_href_ignores_the_map_for_english() -> None:
    out = csc._related_article_href("2026-01-01-post", "en", {"2026-01-01-post": "wrong"})
    assert out == "/2026-01-01-post/"


# ---------------------------------------------------------------------------
# Breadcrumb
# ---------------------------------------------------------------------------


def test_breadcrumb_links_home_and_the_hub_for_english() -> None:
    out = csc._render_breadcrumb(LBL, "en", "etudes-de-cas")
    assert 'href="/"' in out
    assert 'href="/case-studies/"' in out


def test_breadcrumb_uses_the_locale_root_and_segment() -> None:
    out = csc._render_breadcrumb(LBL, "fr", "etudes-de-cas")
    assert 'href="/fr/"' in out
    assert 'href="/fr/etudes-de-cas/"' in out


def test_breadcrumb_marks_the_current_page_without_linking_it() -> None:
    out = csc._render_breadcrumb(LBL, "en", "x", current="This Study")
    assert 'aria-current="page"' in out
    assert "This Study" in out


def test_breadcrumb_omits_the_current_segment_when_absent() -> None:
    assert 'aria-current="page"' not in csc._render_breadcrumb(LBL, "en", "x")


def test_breadcrumb_separators_are_hidden_from_screen_readers() -> None:
    assert 'aria-hidden="true"' in csc._render_breadcrumb(LBL, "en", "x")


# ---------------------------------------------------------------------------
# Empty-input contract
# ---------------------------------------------------------------------------


def test_outcomes_renders_nothing_when_empty() -> None:
    assert csc._render_outcomes([], LBL) == ""


def test_rigour_table_renders_nothing_when_empty() -> None:
    assert csc._render_rigour_table([], LBL) == ""


def test_list_section_renders_nothing_when_empty() -> None:
    assert csc._render_list_section("Heading", [], "cs-x") == ""


def test_rail_links_render_nothing_when_empty() -> None:
    assert csc._render_rail_links({}, LBL) == ""


def test_meta_strip_renders_nothing_when_every_field_is_blank() -> None:
    assert csc._render_meta_strip({"role": "", "period": ""}, LBL) == ""


@pytest.mark.parametrize("quote", ["", "   ", "\n"])
def test_pullquote_renders_nothing_for_blank_input(quote: str) -> None:
    assert csc._render_pullquote(quote) == ""


def test_related_articles_render_nothing_when_empty() -> None:
    assert csc._render_related_articles_section([], LBL, "en", {}) == ""


# ---------------------------------------------------------------------------
# Populated components
# ---------------------------------------------------------------------------


def test_outcomes_pairs_value_with_label() -> None:
    out = csc._render_outcomes([{"value": "40%", "label": "faster"}], LBL)
    assert "<dt>40%</dt>" in out
    assert "<dd>faster</dd>" in out


def test_outcomes_escapes_its_content() -> None:
    out = csc._render_outcomes([{"value": "<b>x</b>", "label": "y"}], LBL)
    assert "<b>" not in out


def test_pullquote_strips_surrounding_quotation_marks() -> None:
    """The template supplies the quote marks; doubling them looks broken."""
    out = csc._render_pullquote('"A quoted claim"')
    assert ">A quoted claim<" in out


def test_meta_strip_includes_only_the_fields_present() -> None:
    out = csc._render_meta_strip({"role": "Lead", "sector": "Banking"}, LBL)
    assert "Lead" in out and "Banking" in out
    assert "Period" not in out


def test_rigour_table_has_a_caption_and_row_headers() -> None:
    """A data table without a caption or scoped headers fails WCAG."""
    out = csc._render_rigour_table([{"metric": "Coverage", "value": "100%"}], LBL)
    assert "<caption>" in out
    assert 'scope="row"' in out
    assert 'scope="col"' in out


def test_list_section_renders_one_item_per_entry() -> None:
    out = csc._render_list_section("Heading", ["a", "b"], "cs-x")
    assert out.count("<li>") == 2


# ---------------------------------------------------------------------------
# Rail links — ordering and safety
# ---------------------------------------------------------------------------


def test_rail_links_follow_the_canonical_order() -> None:
    known = list(csc._LINK_ORDER)[:2]
    if len(known) < 2:
        pytest.skip("needs at least two ordered link keys")
    links = {known[1]: "https://b", known[0]: "https://a"}
    out = csc._render_rail_links(links, LBL)
    assert out.index("https://a") < out.index("https://b"), "declared order, not dict order"


def test_rail_links_append_unknown_keys_after_the_known_ones() -> None:
    known = csc._LINK_ORDER[0]
    out = csc._render_rail_links({known: "https://a", "custom": "https://z"}, LBL)
    assert out.index("https://a") < out.index("https://z")


def test_rail_links_are_noopener() -> None:
    out = csc._render_rail_links({csc._LINK_ORDER[0]: "https://a"}, LBL)
    assert 'rel="noopener noreferrer"' in out


def test_rail_links_escape_the_href() -> None:
    out = csc._render_rail_links({csc._LINK_ORDER[0]: 'https://a"onmouseover=x'}, LBL)
    assert '"onmouseover' not in out


# ---------------------------------------------------------------------------
# Share rail
# ---------------------------------------------------------------------------


def test_share_rail_makes_a_relative_url_absolute() -> None:
    out = csc._render_share_rail("/case-studies/x/", "Title", LBL)
    assert urlparse.quote(f"{csc._BASE_URL}/case-studies/x/", safe="") in out


def test_share_rail_leaves_an_absolute_url_alone() -> None:
    out = csc._render_share_rail("https://example.com/x/", "Title", LBL)
    assert urlparse.quote("https://example.com/x/", safe="") in out


def test_share_rail_encodes_a_title_containing_an_ampersand() -> None:
    """Unencoded, the title truncates at the & and the share text is wrong."""
    out = csc._render_share_rail("/x/", "A & B", LBL)
    assert urlparse.quote("A & B", safe="") in out


def test_share_rail_labels_both_icon_links() -> None:
    out = csc._render_share_rail("/x/", "T", LBL)
    assert out.count("aria-label=") == 2


def test_share_rail_targets_are_noopener() -> None:
    out = csc._render_share_rail("/x/", "T", LBL)
    assert out.count('rel="noopener noreferrer"') == 2


# ---------------------------------------------------------------------------
# Related articles display
# ---------------------------------------------------------------------------


def test_related_articles_strip_the_date_prefix_from_the_link_text_only() -> None:
    """The date is noise in the label but load-bearing in the URL."""
    out = csc._render_related_articles_section(["2026-01-01-a-good-post"], LBL, "en", {})
    link_text = re.search(r'<a href="[^"]+">([^<]+)</a>', out).group(1)
    assert link_text == "A good post"
    assert 'href="/2026-01-01-a-good-post/"' in out, "the href must keep the date"


# ---------------------------------------------------------------------------
# Stage numbering and JSON-LD
# ---------------------------------------------------------------------------


def test_stage_no_pads_to_two_digits() -> None:
    assert "01 — " in csc._stage_no(1, "The problem")


def test_stage_no_uppercases_the_label() -> None:
    assert "THE PROBLEM" in csc._stage_no(1, "The problem")


def test_stage_number_is_hidden_from_screen_readers() -> None:
    """The number is decoration; the label carries the meaning."""
    assert 'aria-hidden="true"' in csc._stage_no(2, "Approach")


def test_json_ld_block_round_trips() -> None:
    out = csc._json_ld_block({"@type": "Article", "name": "é & ü"})
    blob = out.split(">", 1)[1].rsplit("</script>", 1)[0]
    assert json.loads(blob)["name"] == "é & ü"


def test_json_ld_block_keeps_unicode_unescaped() -> None:
    assert "é" in csc._json_ld_block({"n": "é"})
