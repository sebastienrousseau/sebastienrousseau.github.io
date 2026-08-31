# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Case-study page stages — the section renderers behind every study page.

Each stage takes study data and returns a fragment of a published page, in
English and 34 locales. The contract every one of them shares is that absent
data renders NOTHING: an empty <section> carrying a heading and a stage
number reads as missing content rather than content that does not apply, and
it still consumes a numbered slot in the visible sequence.

That contract is the bulk of what is tested here, alongside escaping — the
inputs are hand-authored prose from a YAML brief — and the accessibility
affordances that are invisible when they break.
"""

from __future__ import annotations

import case_studies_render as csr
import pytest

# Every label key the renderers read, extracted from the source rather than
# guessed. A missing key is a KeyError at render time, not a blank string, so
# an incomplete fixture fails as a crash and hides whatever was being tested.
LBL = {
    "Aligned standards": "Aligned standards",
    "By the numbers": "By the numbers",
    "Case studies": "Case studies",
    "Categories": "Categories",
    "Engineering rigour": "Engineering rigour",
    "Filter by category": "Filter by category",
    "Independently verified": "Independently verified",
    "More case studies": "More case studies",
    "Related articles": "Related articles",
    "Verifiable links": "Verifiable links",
    "count": "count",
    "deck": "deck",
    "eyebrow": "eyebrow",
    "eyebrow_plural": "eyebrow_plural",
}


# ---------------------------------------------------------------------------
# The empty-input contract, stage by stage
# ---------------------------------------------------------------------------


def test_outcomes_stage_renders_nothing_when_empty() -> None:
    assert csr._render_outcomes_stage([], LBL) == ""


def test_rigour_stage_renders_nothing_when_empty() -> None:
    assert csr._render_rigour_stage([], LBL, 1) == ""


def test_validation_stage_renders_nothing_when_empty() -> None:
    assert csr._render_validation_stage([], LBL, 1) == ""


def test_standards_stage_renders_nothing_when_empty() -> None:
    assert csr._render_standards_stage([], LBL, 1) == ""


def test_links_stage_renders_nothing_when_empty() -> None:
    assert csr._render_links_stage({}, LBL, 1) == ""


def test_story_stage_renders_nothing_without_body_text() -> None:
    assert csr._render_story_stage(1, "The problem", "") == ""


@pytest.mark.parametrize("quote", ["", "   ", '""', "“”"])
def test_quote_stage_renders_nothing_for_an_effectively_empty_quote(quote: str) -> None:
    """A brief with only quotation marks in the field is an empty quote."""
    assert csr._render_quote_stage(quote) == ""


# ---------------------------------------------------------------------------
# Populated stages
# ---------------------------------------------------------------------------


def test_outcomes_stage_pairs_value_with_label() -> None:
    out = csr._render_outcomes_stage([{"value": "40%", "label": "faster"}], LBL)
    assert "<dt>40%</dt>" in out
    assert "<dd>faster</dd>" in out


def test_outcomes_stage_is_labelled_for_screen_readers() -> None:
    out = csr._render_outcomes_stage([{"value": "1", "label": "x"}], LBL)
    assert 'aria-label="By the numbers"' in out


def test_quote_stage_strips_surrounding_quotation_marks() -> None:
    """The template supplies the quotation marks; doubling them looks broken."""
    for raw in ('"A claim"', "“A claim”"):
        assert ">A claim<" in csr._render_quote_stage(raw)


def test_story_stage_carries_its_anchor_only_when_given() -> None:
    with_anchor = csr._render_story_stage(1, "Problem", "text", anchor="problem")
    without = csr._render_story_stage(1, "Problem", "text")
    assert 'id="problem"' in with_anchor
    assert "id=" not in without


def test_story_stage_numbers_the_heading() -> None:
    out = csr._render_story_stage(3, "Approach", "text")
    assert "03" in out
    assert "APPROACH" in out


def test_validation_and_standards_render_one_item_each() -> None:
    v = csr._render_validation_stage(["a", "b"], LBL, 1)
    s = csr._render_standards_stage(["a", "b", "c"], LBL, 2)
    assert v.count("<li>") == 2
    assert s.count("<li>") == 3


def test_rigour_stage_renders_a_row_per_signal() -> None:
    out = csr._render_rigour_stage(
        [{"metric": "Coverage", "value": "100%"}, {"metric": "Latency", "value": "9ms"}], LBL, 1
    )
    assert "Coverage" in out
    assert "Latency" in out


# ---------------------------------------------------------------------------
# Links stage — ordering and safety
# ---------------------------------------------------------------------------


def test_links_stage_follows_the_declared_order() -> None:
    known = list(csr._LINK_ORDER)[:2]
    if len(known) < 2:
        pytest.skip("needs at least two ordered keys")
    out = csr._render_links_stage({known[1]: "https://b", known[0]: "https://a"}, LBL, 1)
    assert out.index("https://a") < out.index("https://b"), "declared order, not dict order"


def test_links_stage_appends_unknown_keys_after_known_ones() -> None:
    known = csr._LINK_ORDER[0]
    out = csr._render_links_stage({known: "https://a", "custom": "https://z"}, LBL, 1)
    assert out.index("https://a") < out.index("https://z")


def test_links_stage_marks_every_link_noopener() -> None:
    out = csr._render_links_stage({csr._LINK_ORDER[0]: "https://a", "custom": "https://z"}, LBL, 1)
    assert out.count('rel="noopener noreferrer"') == 2


def test_links_stage_escapes_the_href() -> None:
    out = csr._render_links_stage({csr._LINK_ORDER[0]: 'https://a"onmouseover=x'}, LBL, 1)
    assert '"onmouseover' not in out


def test_links_grid_is_marked_as_a_list() -> None:
    """Styled lists lose their implicit role in Safari; role="list" restores it."""
    out = csr._render_links_stage({csr._LINK_ORDER[0]: "https://a"}, LBL, 1)
    assert 'role="list"' in out


# ---------------------------------------------------------------------------
# Escaping — every stage takes hand-authored prose
# ---------------------------------------------------------------------------


def test_every_stage_escapes_its_text_input() -> None:
    payload = "<script>alert(1)</script>"
    rendered = [
        csr._render_outcomes_stage([{"value": payload, "label": payload}], LBL),
        csr._render_quote_stage(payload),
        csr._render_story_stage(1, "L", payload),
        csr._render_rigour_stage([{"metric": payload, "value": payload}], LBL, 1),
        csr._render_validation_stage([payload], LBL, 1),
        csr._render_standards_stage([payload], LBL, 1),
    ]
    for out in rendered:
        assert "<script>" not in out, out[:120]


def test_stages_are_marked_with_the_data_stage_attribute() -> None:
    """The scroll choreography selects on [data-stage]; a stage without it
    is invisible to that machinery while looking correct in the markup."""
    out = csr._render_story_stage(1, "L", "text")
    assert "data-stage" in out
