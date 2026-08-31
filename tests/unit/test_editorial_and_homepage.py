# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Two more previously untested utilities: the banner picker and the homepage.

pick_banner chooses the image that fronts an article. Its job is to never
reuse one that is already in service, and to bias toward the article's topic
when hints are given. Both properties were unchecked.

regen_homepage renders the cards on the front page. Its escaping is subtle on
purpose — frontmatter is hand-authored and sometimes already contains `&amp;`,
so naive html.escape would double-encode it into `&amp;amp;` on the most
visible page of the site. Nothing tested that.
"""

from __future__ import annotations

import random
from pathlib import Path

import pick_banner as pb
import regen_homepage as rh

# ---------------------------------------------------------------------------
# pick_banner — inventory and usage
# ---------------------------------------------------------------------------


def test_collect_inventory_is_empty_for_a_missing_directory(tmp_path: Path) -> None:
    assert pb.collect_inventory(tmp_path / "absent") == []


def test_collect_inventory_takes_webp_only_and_sorts(tmp_path: Path) -> None:
    for name in ("b.webp", "a.webp", "c.png", "d.WEBP"):
        (tmp_path / name).write_bytes(b"x")
    assert pb.collect_inventory(tmp_path) == ["a.webp", "b.webp", "d.WEBP"]


def test_collect_used_banners_is_empty_for_a_missing_directory(tmp_path: Path) -> None:
    assert pb.collect_used_banners(tmp_path / "absent") == set()


def test_collect_used_banners_scans_every_locale(tmp_path: Path) -> None:
    """Locale posts count as usage: a banner in fr/ is not free to reuse."""
    (tmp_path / "fr").mkdir()
    (tmp_path / "a.md").write_text(
        'banner: "https://cloudcdn.pro/stocks/images/one.webp"\n', encoding="utf-8"
    )
    (tmp_path / "fr" / "b.md").write_text(
        'banner: "https://cloudcdn.pro/stocks/images/two.webp"\n', encoding="utf-8"
    )
    assert pb.collect_used_banners(tmp_path) == {"one.webp", "two.webp"}


# ---------------------------------------------------------------------------
# pick_banner — scoring and selection
# ---------------------------------------------------------------------------


def test_score_candidate_is_zero_without_hints() -> None:
    assert pb.score_candidate("anything.webp", []) == 0


def test_score_candidate_rewards_a_hint_appearing_in_the_name() -> None:
    assert pb.score_candidate("quantum-computer.webp", ["quantum"]) >= 1
    assert pb.score_candidate("unrelated.webp", ["quantum"]) == 0


def test_score_candidate_accumulates_across_hints() -> None:
    both = pb.score_candidate("quantum-payments.webp", ["quantum", "payments"])
    one = pb.score_candidate("quantum-payments.webp", ["quantum"])
    assert both > one


def test_pick_returns_none_when_everything_is_used() -> None:
    """Exhausted inventory must return None, never reuse a live banner."""
    assert pb.pick(["a.webp"], {"a.webp"}, []) is None


def test_pick_never_returns_a_used_banner() -> None:
    rng = random.Random(0)
    for _ in range(20):
        chosen = pb.pick(["a.webp", "b.webp", "c.webp"], {"a.webp", "b.webp"}, [], rng=rng)
        assert chosen == "c.webp"


def test_pick_honours_the_exclude_set() -> None:
    chosen = pb.pick(["a.webp", "b.webp"], set(), [], exclude={"a.webp"}, rng=random.Random(1))
    assert chosen == "b.webp"


def test_pick_is_biased_toward_a_matching_hint() -> None:
    inv = ["random-one.webp", "quantum-computer.webp", "random-two.webp"]
    assert pb.pick(inv, set(), ["quantum"], rng=random.Random(7)) == "quantum-computer.webp"


def test_pick_falls_back_to_random_when_no_hint_matches() -> None:
    inv = ["alpha.webp", "beta.webp"]
    chosen = pb.pick(inv, set(), ["nothing-matches-this"], rng=random.Random(3))
    assert chosen in inv


def test_hint_biased_pick_returns_none_without_hints() -> None:
    assert pb._hint_biased_pick(["a.webp"], [], random.Random(0)) is None


def test_hint_biased_pick_returns_none_when_nothing_scores() -> None:
    assert pb._hint_biased_pick(["a.webp"], ["zzz"], random.Random(0)) is None


def test_transform_url_carries_the_parameters() -> None:
    url = pb.transform_url("x.webp", width=800, q=60)
    assert "/stocks/images/x.webp" in url
    assert "w=800" in url
    assert "q=60" in url
    assert "format=webp" in url


# ---------------------------------------------------------------------------
# regen_homepage — frontmatter
# ---------------------------------------------------------------------------


FM = """---
title: "A Title"
description: "A description"
tags: "iso 20022, uk payments, ai"
banner: "https://cdn/b.webp"
---

Body text that is not frontmatter.
"""


def test_parse_minimal_frontmatter_reads_the_block() -> None:
    fm = rh._parse_minimal_frontmatter(FM)
    assert fm["title"] == "A Title"
    assert fm["description"] == "A description"


def test_parse_minimal_frontmatter_stops_at_the_closing_delimiter() -> None:
    """Body content must never leak into the card."""
    fm = rh._parse_minimal_frontmatter(FM)
    assert not any("Body text" in v for v in fm.values())


def test_parse_minimal_frontmatter_on_a_file_without_frontmatter() -> None:
    assert rh._parse_minimal_frontmatter("just body\n") == {}


# ---------------------------------------------------------------------------
# regen_homepage — presentation helpers
# ---------------------------------------------------------------------------


def test_smart_title_preserves_acronyms() -> None:
    """`.title()` would render UK as 'Uk' on the front page."""
    assert rh._smart_title("uk") == "UK"
    assert rh._smart_title("ai") == "AI"


def test_smart_title_trusts_existing_mixed_case() -> None:
    assert rh._smart_title("FedNow") == "FedNow"


def test_smart_title_title_cases_an_ordinary_word() -> None:
    assert rh._smart_title("payments") == "Payments"


def test_eyebrow_takes_the_first_three_tags() -> None:
    out = rh._eyebrow_from_tags("one, two, three, four")
    assert out.count("·") == 2
    assert "Four" not in out


def test_eyebrow_preserves_acronyms_inside_multiword_tags() -> None:
    assert rh._eyebrow_from_tags("uk payments") == "UK Payments"


def test_eyebrow_on_an_empty_tag_line() -> None:
    assert rh._eyebrow_from_tags("") == ""


def test_excerpt_preference_order() -> None:
    assert rh._excerpt_for({"excerpt": "e", "subtitle": "s", "description": "d"}) == "e"
    assert rh._excerpt_for({"subtitle": "s", "description": "d"}) == "s"
    assert rh._excerpt_for({"description": "d"}) == "d"
    assert rh._excerpt_for({"title": "t"}) == "t"
    assert rh._excerpt_for({}) == ""


def test_tldr_prefers_description_over_excerpt() -> None:
    """The description is the SEO-tuned one-liner; that is the card shape."""
    assert rh._tldr_for({"excerpt": "e", "description": "d"}) == "d"
    assert rh._tldr_for({"excerpt": "e"}) == "e"


def test_display_date_is_human_readable() -> None:
    assert rh._display_date(2026, 3, 4) == "March 4, 2026"


# ---------------------------------------------------------------------------
# regen_homepage — escaping, the subtle one
# ---------------------------------------------------------------------------


def test_esc_escapes_a_bare_ampersand() -> None:
    assert rh._esc("Payments & money") == "Payments &amp; money"


def test_esc_does_not_double_encode_an_existing_entity() -> None:
    """Hand-authored frontmatter often already contains &amp;."""
    assert rh._esc("Payments &amp; money") == "Payments &amp; money"


def test_esc_is_idempotent() -> None:
    once = rh._esc("A & B &amp; C")
    assert rh._esc(once) == once


def test_esc_escapes_angle_brackets() -> None:
    assert "<script>" not in rh._esc("<script>alert(1)</script>")


# ---------------------------------------------------------------------------
# regen_homepage — the card
# ---------------------------------------------------------------------------


def _card(**fm: str) -> str:
    base = {"title": "T", "tags": "ai", "banner": "https://cdn/b.webp"}
    base.update(fm)
    return rh._render_card("2026-03-04-slug", 2026, 3, 4, base)


def test_render_card_links_to_the_post_and_dates_it() -> None:
    card = _card()
    assert 'href="/2026-03-04-slug/index.html"' in card
    assert 'datetime="2026-03-04"' in card
    assert "March 4, 2026" in card


def test_render_card_falls_back_to_the_title_for_alt_text() -> None:
    """An image with no alt text is an accessibility failure, so never empty."""
    assert 'alt="T"' in _card(title="T")


def test_render_card_uses_the_supplied_alt_when_present() -> None:
    assert 'alt="Specific alt"' in _card(banner_alt="Specific alt")


def test_render_card_escapes_the_title() -> None:
    assert "&amp;" in _card(title="A & B")


def test_render_card_has_a_default_eyebrow() -> None:
    assert "Banking · Technology" in _card(tags="")
