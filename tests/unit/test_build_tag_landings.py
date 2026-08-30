# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Tag landings are generated for 34 locales, and had no test at all.

scripts/generators/build_tag_landings.py sat at 0% coverage across 236
statements while emitting the per-tag landing pages and their locale forks.
The risky part is not the HTML assembly, it is the frontmatter parsing and
link rewriting: a tag string mis-split, an alias unresolved, or an article
href rewritten too eagerly all produce pages that look right and point wrong.

These tests pin that layer — the parsing, the alias resolution, the pillar
ordering, and the deliberate strictness of the article-slug rewrite.
"""

from __future__ import annotations

from pathlib import Path

import build_tag_landings as btl
import pytest

# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------


def test_parse_raw_tags_splits_strips_and_drops_empties() -> None:
    assert btl._parse_raw_tags(' "ISO 20022", payments , , "AI" ') == [
        "ISO 20022",
        "payments",
        "AI",
    ]


def test_parse_raw_tags_on_an_empty_line() -> None:
    assert btl._parse_raw_tags("") == []
    assert btl._parse_raw_tags("  ,  , ") == []


def test_extract_excerpt_prefers_excerpt_over_description() -> None:
    text = 'excerpt: "the excerpt"\ndescription: "the description"\n'
    assert btl._extract_excerpt(text) == "the excerpt"


def test_extract_excerpt_falls_back_to_description() -> None:
    assert btl._extract_excerpt('description: "the description"\n') == "the description"


def test_extract_excerpt_returns_empty_when_neither_present() -> None:
    assert btl._extract_excerpt("title: nothing useful\n") == ""


def test_extract_banner_falls_back_to_the_default_and_the_title() -> None:
    banner, alt = btl._extract_banner("title: x\n", "A Title")
    assert banner == btl._DEFAULT_BANNER
    assert alt == "A Title", "alt text must never be empty; the title is the fallback"


def test_extract_banner_reads_both_fields() -> None:
    text = 'banner: "https://cdn/img.webp"\nbanner_alt: "a description"\n'
    banner, alt = btl._extract_banner(text, "A Title")
    assert banner == "https://cdn/img.webp"
    assert alt == "a description"


# ---------------------------------------------------------------------------
# _post_meta
# ---------------------------------------------------------------------------


def _post(tmp: Path, stem: str, body: str) -> Path:
    p = tmp / f"{stem}.md"
    p.write_text(body, encoding="utf-8")
    return p


def test_post_meta_returns_none_without_tags(tmp_path: Path) -> None:
    """A post with no tags cannot land on a tag page; it must not be guessed."""
    p = _post(tmp_path, "2026-01-01-untagged", 'title: "T"\n')
    assert btl._post_meta(p) is None


def test_post_meta_extracts_every_field(tmp_path: Path) -> None:
    p = _post(
        tmp_path,
        "2026-03-04-a-post",
        'title: "The Title"\n'
        'excerpt: "The excerpt"\n'
        'tags: "iso 20022, payments"\n'
        'banner: "https://cdn/b.webp"\n'
        'banner_alt: "Alt text"\n',
    )
    title, iso, slug, excerpt, raw_tags, banner, alt = btl._post_meta(p)
    assert title == "The Title"
    assert iso == "2026-03-04"
    assert slug == "2026-03-04-a-post"
    assert excerpt == "The excerpt"
    assert raw_tags == ["iso 20022", "payments"]
    assert banner == "https://cdn/b.webp"
    assert alt == "Alt text"


def test_post_meta_falls_back_to_the_stem_for_a_missing_title(tmp_path: Path) -> None:
    p = _post(tmp_path, "2026-03-04-no-title", 'tags: "payments"\n')
    assert btl._post_meta(p)[0] == "2026-03-04-no-title"


def test_post_meta_leaves_the_date_empty_for_an_undated_stem(tmp_path: Path) -> None:
    p = _post(tmp_path, "glossary", 'tags: "payments"\n')
    assert btl._post_meta(p)[1] == ""


# ---------------------------------------------------------------------------
# Alias resolution and pillars
# ---------------------------------------------------------------------------


AMAP = {"iso 20022": "iso-20022", "iso20022": "iso-20022", "ai": "applied-ai"}


def test_canonical_set_resolves_aliases_and_deduplicates() -> None:
    """Two aliases of one tag must collapse to a single canonical slug."""
    assert btl._canonical_set(["ISO 20022", "iso20022", "AI"], AMAP) == {
        "iso-20022",
        "applied-ai",
    }


def test_canonical_set_drops_unknown_tags() -> None:
    """An unrecognised tag is dropped, never invented into a landing page."""
    assert btl._canonical_set(["not-a-real-tag"], AMAP) == set()


def test_post_pillars_are_returned_in_the_canonical_order() -> None:
    taxonomy = {
        "iso-20022": {"category": btl.PILLAR_ORDER[1]},
        "applied-ai": {"category": btl.PILLAR_ORDER[0]},
    }
    pillars = btl._post_pillars(["ISO 20022", "AI"], taxonomy, AMAP)
    assert pillars == [btl.PILLAR_ORDER[0], btl.PILLAR_ORDER[1]], (
        "pillar order must follow PILLAR_ORDER, not tag order"
    )


def test_post_pillars_ignores_tags_without_a_category() -> None:
    taxonomy = {"iso-20022": {}}
    assert btl._post_pillars(["ISO 20022"], taxonomy, AMAP) == []


def test_post_pillars_deduplicates_two_tags_sharing_a_pillar() -> None:
    taxonomy = {
        "iso-20022": {"category": btl.PILLAR_ORDER[0]},
        "applied-ai": {"category": btl.PILLAR_ORDER[0]},
    }
    assert btl._post_pillars(["ISO 20022", "AI"], taxonomy, AMAP) == [btl.PILLAR_ORDER[0]]


# ---------------------------------------------------------------------------
# Locale link rewriting — the part that silently breaks URLs
# ---------------------------------------------------------------------------


EN_HTML = (
    '<html lang="en">'
    '<link rel="canonical" href="https://sebastienrousseau.com/tags/payments/">'
    '<meta property="og:url" content="https://sebastienrousseau.com/tags/payments/">'
    '<a href="/2026-01-01-known-post/">known</a>'
    '<a href="/2026-02-02-unmapped/">unmapped</a>'
    '<a href="/tags/other/">chip</a>'
    '<script>{"inLanguage": "en-GB"}</script>'
    "</html>"
)


@pytest.fixture
def fr_html() -> str:
    return btl._localise_html_links(
        EN_HTML, "fr", "payments", {"2026-01-01-known-post": "2026-01-01-article-connu"}
    )


def test_localise_sets_the_html_lang(fr_html: str) -> None:
    assert '<html lang="fr"' in fr_html


def test_localise_rewrites_canonical_and_og_url_together(fr_html: str) -> None:
    expected = f"{btl._BASE_URL}/fr/{btl.LOCALE_TAGS_PATH['fr']}/payments/"
    assert f'href="{expected}"' in fr_html
    assert f'content="{expected}"' in fr_html


def test_localise_maps_a_known_article_slug(fr_html: str) -> None:
    assert 'href="/fr/2026-01-01-article-connu/"' in fr_html


def test_localise_keeps_an_unmapped_slug_but_still_prefixes_the_locale(fr_html: str) -> None:
    """No mapping is not licence to drop the link — prefix it and move on."""
    assert 'href="/fr/2026-02-02-unmapped/"' in fr_html


def test_localise_rewrites_tag_chips(fr_html: str) -> None:
    assert f'href="/fr/{btl.LOCALE_TAGS_PATH["fr"]}/other/"' in fr_html


def test_localise_updates_jsonld_inlanguage(fr_html: str) -> None:
    """A locale page declaring inLanguage 'en' fails JSON-LD validation."""
    assert '"inLanguage":"fr"' in fr_html
    assert "en-GB" not in fr_html


def test_localise_leaves_unrelated_hrefs_alone() -> None:
    """The article rewrite is deliberately strict — dated slugs only."""
    html = '<a href="/about/">about</a><a href="/projects/index.html">p</a>'
    out = btl._localise_html_links(html, "fr", "payments", {})
    assert 'href="/about/"' in out
    assert 'href="/projects/index.html"' in out


def test_localise_is_idempotent_on_the_lang_attribute() -> None:
    once = btl._localise_html_links(EN_HTML, "de", "payments", {})
    twice = btl._localise_html_links(once, "de", "payments", {})
    assert twice.count('<html lang="de"') == 1


# ---------------------------------------------------------------------------
# Module invariants
# ---------------------------------------------------------------------------


def test_every_non_en_locale_has_a_tags_path() -> None:
    """A locale without a tags path would emit /fr/None/ URLs."""
    missing = [c for c in btl.LOCALES_NON_EN if not btl.LOCALE_TAGS_PATH.get(c)]
    assert missing == []


def test_en_is_excluded_from_the_locale_fork_list() -> None:
    assert "en" not in btl.LOCALES_NON_EN


def test_pillar_order_has_no_duplicates() -> None:
    assert len(btl.PILLAR_ORDER) == len(set(btl.PILLAR_ORDER))
