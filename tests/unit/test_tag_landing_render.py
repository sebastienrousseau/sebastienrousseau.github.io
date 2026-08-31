# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Tag landing pages — related-tag chips, hreflang chains, category lists.

scripts/generators/tag_landing_render.py had 113 uncovered statements.

The property worth protecting most here is determinism. `_render_related_tags`
carries a comment explaining that `Counter.most_common()` breaks ties by
insertion order, the counter is built by iterating a set, and set order is
randomised per process — so tied co-occurrence counts made the page differ
between builds. The fix sorts by `(-count, slug)`. That is the same class of
bug as the wall-clock stamping that broke the byte-identical rebuild, and it
had no test.

The landing threshold is the other load-bearing rule: a tag below it gets no
landing page, so linking to it would 404 and fail the strict internal-link
audit. Both the chip filter and the category list depend on that.
"""

from __future__ import annotations

import collections
from pathlib import Path

import pytest
import tag_landing_render as tlr

# ---------------------------------------------------------------------------
# Related tags — determinism and the landing threshold
# ---------------------------------------------------------------------------


def _posts(**counts: int) -> dict[str, list]:
    """A posts map where each canonical has `count` placeholder entries."""
    return {
        slug: [("t", "2026-01-01", f"s{i}", "e", [], "b", "a") for i in range(n)]
        for slug, n in counts.items()
    }


def _taxonomy(*slugs: str) -> dict:
    return {s: {"name": s.upper(), "description": f"About {s}."} for s in slugs}


def test_related_tags_are_ordered_by_count_then_slug() -> None:
    """Ties must break on slug, not on however the counter was populated."""
    threshold = tlr._LANDING_THRESHOLD
    cooccur = collections.Counter({"zebra": 5, "alpha": 5, "beta": 9})
    posts = _posts(zebra=threshold, alpha=threshold, beta=threshold)
    out = tlr._render_related_tags(cooccur, _taxonomy("zebra", "alpha", "beta"), "x", posts)
    assert out.index("/tags/beta/") < out.index("/tags/alpha/") < out.index("/tags/zebra/")


def test_related_tags_order_does_not_depend_on_counter_insertion_order() -> None:
    """The regression: two counters with identical contents, built differently."""
    threshold = tlr._LANDING_THRESHOLD
    posts = _posts(a=threshold, b=threshold, c=threshold)
    tax = _taxonomy("a", "b", "c")
    forward = collections.Counter()
    for k in ("a", "b", "c"):
        forward[k] = 3
    backward = collections.Counter()
    for k in ("c", "b", "a"):
        backward[k] = 3
    assert tlr._render_related_tags(forward, tax, "x", posts) == tlr._render_related_tags(
        backward, tax, "x", posts
    )


def test_related_tags_drop_a_tag_below_the_landing_threshold() -> None:
    """Below threshold there is no landing page, so a chip would 404."""
    threshold = tlr._LANDING_THRESHOLD
    cooccur = collections.Counter({"thin": 99, "thick": 1})
    posts = _posts(thin=threshold - 1, thick=threshold)
    out = tlr._render_related_tags(cooccur, _taxonomy("thin", "thick"), "x", posts)
    assert "/tags/thin/" not in out
    assert "/tags/thick/" in out


def test_related_tags_render_nothing_when_none_are_eligible() -> None:
    posts = _posts(thin=tlr._LANDING_THRESHOLD - 1)
    out = tlr._render_related_tags(collections.Counter({"thin": 5}), _taxonomy("thin"), "x", posts)
    assert out == ""


def test_related_tags_respect_the_limit() -> None:
    threshold = tlr._LANDING_THRESHOLD
    slugs = [f"t{i}" for i in range(10)]
    cooccur = collections.Counter({s: 10 - i for i, s in enumerate(slugs)})
    out = tlr._render_related_tags(
        cooccur, _taxonomy(*slugs), "x", _posts(**dict.fromkeys(slugs, threshold)), n=3
    )
    assert out.count("related-tag-chip") == 3


def test_related_tags_heading_id_is_scoped_to_the_slug() -> None:
    """Two landings on one page would otherwise share a duplicate id."""
    threshold = tlr._LANDING_THRESHOLD
    out = tlr._render_related_tags(
        collections.Counter({"a": 1}), _taxonomy("a"), "my-slug", _posts(a=threshold)
    )
    assert 'id="related-tags-h2-my-slug"' in out
    assert 'aria-labelledby="related-tags-h2-my-slug"' in out


# ---------------------------------------------------------------------------
# Category tag list — same threshold, different consequence
# ---------------------------------------------------------------------------


def test_category_item_links_a_tag_at_or_above_the_threshold() -> None:
    entry = {"name": "Payments", "description": "About payments."}
    out = tlr._render_category_tag_item("payments", entry, tlr._LANDING_THRESHOLD)
    assert 'href="/tags/payments/"' in out


def test_category_item_lists_but_does_not_link_a_thin_tag() -> None:
    """Listed with its count, unlinked — the landing page does not exist."""
    entry = {"name": "Thin", "description": "About thin."}
    out = tlr._render_category_tag_item("thin", entry, tlr._LANDING_THRESHOLD - 1)
    assert "href=" not in out
    assert "Thin" in out


def test_category_item_pluralises_the_count() -> None:
    entry = {"name": "T", "description": "d"}
    assert "1 article<" in tlr._render_category_tag_item("t", entry, 1)
    assert "2 articles<" in tlr._render_category_tag_item("t", entry, 2)


def test_category_item_escapes_name_and_description() -> None:
    entry = {"name": "<b>N</b>", "description": "<i>D</i>"}
    out = tlr._render_category_tag_item("t", entry, 1)
    assert "<b>" not in out and "<i>" not in out


# ---------------------------------------------------------------------------
# Recent posts across a pillar
# ---------------------------------------------------------------------------


def _post(date: str, slug: str) -> tuple:
    return ("Title", date, slug, "excerpt", [], "banner", "alt")


def test_category_recent_posts_sorts_newest_first() -> None:
    posts = {"a": [_post("2025-01-01", "old"), _post("2026-06-06", "new")]}
    out = tlr._category_recent_posts(["a"], posts)
    assert [p[2] for p in out] == ["new", "old"]


def test_category_recent_posts_dedupes_across_canonicals() -> None:
    """One post carrying two tags in the same pillar must appear once."""
    shared = _post("2026-01-01", "shared")
    posts = {"a": [shared], "b": [shared, _post("2026-02-02", "other")]}
    out = tlr._category_recent_posts(["a", "b"], posts)
    assert [p[2] for p in out].count("shared") == 1
    assert len(out) == 2


def test_category_recent_posts_respects_the_limit() -> None:
    posts = {"a": [_post(f"2026-01-{i:02d}", f"s{i}") for i in range(1, 10)]}
    assert len(tlr._category_recent_posts(["a"], posts, n=3)) == 3


def test_category_recent_posts_tolerates_a_missing_date() -> None:
    """A dateless post sorts last rather than raising."""
    posts = {"a": [_post("", "undated"), _post("2026-01-01", "dated")]}
    out = tlr._category_recent_posts(["a"], posts)
    assert [p[2] for p in out] == ["dated", "undated"]


def test_category_recent_posts_on_an_unknown_pillar() -> None:
    assert tlr._category_recent_posts(["nope"], {}) == []


# ---------------------------------------------------------------------------
# hreflang chain
# ---------------------------------------------------------------------------


def test_append_slug_extends_every_alternate_url() -> None:
    """The chain must stay reciprocal across all locale forks of a tag."""
    html = (
        '<link rel="alternate" hreflang="en" href="https://sebastienrousseau.com/tags/">'
        '<link rel="alternate" hreflang="fr" href="https://sebastienrousseau.com/fr/etiquettes/">'
    )
    out = tlr._append_slug_to_hreflang(html, "payments")
    assert "/tags/payments/" in out
    assert "/fr/etiquettes/payments/" in out


def test_append_slug_leaves_other_markup_alone() -> None:
    html = '<link rel="stylesheet" href="/a.css"><p>text</p>'
    assert tlr._append_slug_to_hreflang(html, "x") == html


# ---------------------------------------------------------------------------
# Locale card fields
# ---------------------------------------------------------------------------


def test_locale_card_fields_returns_none_without_a_title(tmp_path: Path) -> None:
    p = tmp_path / "2026-01-01-x.md"
    p.write_text('description: "d"\n', encoding="utf-8")
    assert tlr._locale_post_card_fields(p) is None


def test_locale_card_fields_reads_title_excerpt_and_banner(tmp_path: Path) -> None:
    p = tmp_path / "2026-01-01-x.md"
    p.write_text(
        'title: "Le titre"\nexcerpt: "L\'extrait"\nbanner: "https://cdn/b.webp"\n',
        encoding="utf-8",
    )
    stem, title, excerpt, banner = tlr._locale_post_card_fields(p)
    assert stem == "2026-01-01-x"
    assert title == "Le titre"
    assert excerpt == "L'extrait"
    assert banner == "https://cdn/b.webp"


def test_locale_card_fields_falls_back_to_description_then_default_banner(
    tmp_path: Path,
) -> None:
    p = tmp_path / "2026-01-01-x.md"
    p.write_text('title: "T"\ndescription: "La description"\n', encoding="utf-8")
    _, _, excerpt, banner = tlr._locale_post_card_fields(p)
    assert excerpt == "La description"
    assert banner == tlr._DEFAULT_BANNER


# ---------------------------------------------------------------------------
# Localising a tag's posts
# ---------------------------------------------------------------------------


def test_localise_posts_swaps_translated_fields() -> None:
    en = [("EN title", "2026-01-01", "2026-01-01-post", "EN excerpt", [], "en.webp", "alt")]
    index = {"2026-01-01-post": ("2026-01-01-billet", "FR titre", "FR extrait", "fr.webp")}
    out = tlr._localise_posts_for_tag(en, index)
    assert out[0][0] == "FR titre"
    assert out[0][3] == "FR extrait"


def test_localise_posts_passes_through_an_unmapped_post() -> None:
    en = [("EN title", "2026-01-01", "2026-01-01-post", "EN excerpt", [], "en.webp", "alt")]
    assert tlr._localise_posts_for_tag(en, {}) == en


@pytest.mark.parametrize("bad", ["", "&", "<x>"])
def test_esc_neutralises_markup_characters(bad: str) -> None:
    out = tlr._esc(bad)
    assert "<" not in out and ">" not in out
