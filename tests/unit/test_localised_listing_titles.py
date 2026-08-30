"""Locale listing titles are put into their own language.

2154 of the 7004 non-EN pages served a <title> byte-identical to an English
page's, from four templates repeated across all 34 locales. The pillar names
they combine with already existed per locale in listings.json; only the
frames were missing.
"""

from __future__ import annotations

import json
from pathlib import Path

from postbuild_lib.html_passes import localise_listing_titles, localised_listing_title

JA = json.loads(Path("_data/i18n/ja/labels.json").read_text(encoding="utf-8"))
FR = json.loads(Path("_data/i18n/fr/labels.json").read_text(encoding="utf-8"))


def test_the_bare_listing_title_is_translated():
    assert localised_listing_title("Articles", "ja", JA) == "記事"


def test_a_year_archive_keeps_its_year():
    assert localised_listing_title("Articles — 2018", "ja", JA) == "記事 — 2018"


def test_a_pillar_name_is_translated_with_its_frame():
    """The pillar name comes from listings.json, the frame from labels.json."""
    got = localised_listing_title("Infrastructure &amp; cryptography — Editorial pillar", "ja", JA)
    assert got == "インフラと暗号技術 — 編集の柱"


def test_a_tag_name_is_left_alone():
    """A tag is a canonical taxonomy label and appears in the URL; many are
    proper nouns (pain.001, ISO 20022, Rust)."""
    assert localised_listing_title("Research — Articles by topic", "ja", JA) == (
        "Research — トピック別の記事"
    )


def test_a_translation_identical_to_english_is_still_applied():
    """French for Articles is Articles; that is a translation, not a miss."""
    assert localised_listing_title("Articles", "fr", FR) == "Articles"


def test_an_unrecognised_title_is_untouched():
    assert localised_listing_title("Something else entirely", "ja", JA) == "Something else entirely"


def test_the_page_pass_rewrites_title_og_and_h1_together(tmp_path):
    """A page must not say one thing to a reader and another to a crawler."""
    html = (
        "<html><head><title>Articles</title>"
        '<meta property="og:title" content="Articles">'
        '<meta name="twitter:title" content="Articles">'
        "</head><body><h1>Articles</h1></body></html>"
    )
    out = localise_listing_titles(Path("ja/kiji/index.html"), html)
    assert "<title>記事</title>" in out
    assert 'property="og:title" content="記事"' in out
    assert 'name="twitter:title" content="記事"' in out
    assert "<h1>記事</h1>" in out


def test_an_english_page_is_untouched():
    html = "<html><head><title>Articles</title></head><body></body></html>"
    assert localise_listing_titles(Path("articles/index.html"), html) == html


def test_a_page_with_no_title_is_untouched():
    html = "<html><head></head><body>x</body></html>"
    assert localise_listing_titles(Path("ja/kiji/index.html"), html) == html


def test_a_pillar_pages_h1_is_translated_too():
    """The H1 is the bare pillar name, not the full title, so the title-match
    rewrite does not reach it — the page read Arabic in the title and English
    in the visible heading."""
    html = (
        "<html><head><title>Infrastructure &amp; cryptography — Editorial pillar</title>"
        "</head><body><h1>Infrastructure &amp; cryptography</h1></body></html>"
    )
    out = localise_listing_titles(Path("ar/categories/infra/index.html"), html)
    assert "<h1>البنية التحتية والتشفير</h1>" in out
    assert "Infrastructure &amp; cryptography</h1>" not in out


def test_a_locale_without_the_frames_is_left_alone():
    """A labels.json missing the keys must not produce a half-translated
    title; the page keeps the English one until the key is added."""
    assert localised_listing_title("Articles", "ja", {}) == "Articles"
    assert (
        localised_listing_title("Research — Articles by topic", "ja", {"Articles": "記事"})
        == "Research — Articles by topic"
    )


def test_a_missing_labels_file_is_not_an_error(tmp_path, monkeypatch):
    """A locale directory without labels.json must not break the build."""
    from postbuild_lib import html_passes

    monkeypatch.setattr(html_passes, "_LOCALE_LABELS_CACHE", {})
    monkeypatch.setattr(html_passes, "_LISTINGS_CACHE", {})
    monkeypatch.chdir(tmp_path)
    html = "<html><head><title>Articles</title></head><body></body></html>"
    assert localise_listing_titles(Path("ja/kiji/index.html"), html) == html


def test_an_unknown_pillar_name_is_kept(tmp_path):
    """A pillar the EN map does not know stays as it is rather than vanishing."""
    got = localised_listing_title("Some New Pillar — Editorial pillar", "ja", JA)
    assert got == "Some New Pillar — 編集の柱"


def test_a_missing_listings_file_leaves_the_pillar_name(tmp_path, monkeypatch):
    """listings.json holds the translated pillar names. Without it the frame
    is still translated and the name kept, rather than the build failing."""
    from postbuild_lib import html_passes

    monkeypatch.setattr(html_passes, "_LISTINGS_CACHE", {})
    monkeypatch.chdir(tmp_path)
    got = localised_listing_title("Applied AI — Editorial pillar", "ja", JA)
    assert got == "Applied AI — 編集の柱"
