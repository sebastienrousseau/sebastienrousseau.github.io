"""Unit tests for the postbuild SEO meta passes added in the brand-pivot
work: clean_meta_description, normalize_canonical, fix_article_og_type,
inject_kpi_metrics, and align_jsonld_inlanguage (plus their helpers).

Targets 100 % branch coverage of the new code paths in
``postbuild_lib.seo`` (the CI coverage gate).
"""

from __future__ import annotations

from pathlib import Path

from postbuild_lib import seo


def _ld(body: str) -> str:
    return f'<script type="application/ld+json">{body}</script>'


# ---------------------------------------------------------------------------
# _iter_jsonld_nodes / _is_clean_desc / _node_is_article
# ---------------------------------------------------------------------------


def test_iter_jsonld_nodes_walks_dicts_lists_and_ignores_scalars():
    data = {"a": 1, "b": [{"c": 2}, "s"], "d": {"e": 3}}
    nodes = seo._iter_jsonld_nodes(data)
    assert {"c": 2} in nodes and {"e": 3} in nodes
    assert data in nodes
    assert seo._iter_jsonld_nodes(5) == []


def test_is_clean_desc_rejects_empty_short_and_corrupt():
    assert seo._is_clean_desc("A perfectly clean description over twenty chars")
    assert not seo._is_clean_desc("")
    assert not seo._is_clean_desc("too short")
    assert not seo._is_clean_desc("has a <div> literal tag twenty-plus chars")
    assert not seo._is_clean_desc("has &lt;div escaped tag twenty-plus chars here")
    assert not seo._is_clean_desc("double &amp;lt;div escaped twenty-plus chars ok")


def test_node_is_article():
    assert seo._node_is_article({"@type": "BlogPosting"})
    assert seo._node_is_article({"@type": ["Thing", "NewsArticle"]})
    assert not seo._node_is_article({"@type": "Person"})
    assert not seo._node_is_article({})


# ---------------------------------------------------------------------------
# _clean_descriptions / _desc_from_jsonld
# ---------------------------------------------------------------------------


def test_desc_from_jsonld_prefers_article_over_identity():
    html = _ld('{"@type":"Person","description":"Identity graph blurb twenty-plus chars"}') + _ld(
        '{"@type":"BlogPosting","description":"Article summary twenty-plus chars here now"}'
    )
    assert seo._desc_from_jsonld(html).startswith("Article summary")


def test_desc_from_jsonld_falls_back_to_generic_and_skips_bad_json():
    html = _ld("{not valid json") + _ld(
        '{"@type":"WebSite","description":"Generic clean blurb twenty-plus chars here"}'
    )
    assert seo._desc_from_jsonld(html).startswith("Generic clean")


def test_desc_from_jsonld_none_when_absent_or_non_string():
    assert seo._desc_from_jsonld("<p>no json-ld here</p>") is None
    assert seo._desc_from_jsonld(_ld('{"description":123}')) is None


# ---------------------------------------------------------------------------
# _desc_from_source (front-matter of the home page only)
# ---------------------------------------------------------------------------


def test_desc_from_source_home_reads_frontmatter():
    # Real _posts/index.md carries a description.
    assert seo._desc_from_source(Path("public/index.html"))


def test_desc_from_source_none_for_non_home():
    assert seo._desc_from_source(Path("public/about/index.html")) is None


def test_desc_from_source_none_outside_public():
    assert seo._desc_from_source(Path("/etc/hosts")) is None


def test_desc_from_source_missing_and_undescribed(monkeypatch, tmp_path):
    monkeypatch.setattr(seo, "POSTS", tmp_path)
    # No index.md at all.
    assert seo._desc_from_source(Path("public/index.html")) is None
    # index.md present but no description key.
    (tmp_path / "index.md").write_text("---\ntitle: x\n---\nbody\n", encoding="utf-8")
    assert seo._desc_from_source(Path("public/index.html")) is None
    # index.md with a description.
    (tmp_path / "index.md").write_text(
        '---\ndescription: "A sourced description"\n---\n', encoding="utf-8"
    )
    assert seo._desc_from_source(Path("public/index.html")) == "A sourced description"


# ---------------------------------------------------------------------------
# _sanitised_scrape / _current_meta_description / _tag_is_corrupt
# ---------------------------------------------------------------------------


def test_sanitised_scrape_recovers_readable_text():
    html = (
        '<meta name="description" content="'
        "&amp;lt;div&amp;gt;Quantum thresholds are moving again and the timeline "
        'is shifting fast for banks&amp;lt;/div&amp;gt;">'
    )
    out = seo._sanitised_scrape(html)
    assert out and "<" not in out and "&lt;" not in out
    assert "Quantum thresholds" in out


def test_sanitised_scrape_none_when_no_meta_or_too_short():
    assert seo._sanitised_scrape("<p>nothing</p>") is None
    assert seo._sanitised_scrape('<meta name="description" content="&amp;lt;a&amp;gt;">') is None


def test_sanitised_scrape_truncates_long_text():
    long = "word " * 60
    html = f'<meta name="description" content="{long.strip()}">'
    out = seo._sanitised_scrape(html)
    assert out.endswith("…") and len(out) <= 160


def test_current_meta_description_present_and_absent():
    assert seo._current_meta_description('<meta name="description" content="hello">') == "hello"
    assert seo._current_meta_description("<p>x</p>") is None


def test_tag_is_corrupt():
    assert seo._tag_is_corrupt('<meta content="&amp;lt;div">')
    assert not seo._tag_is_corrupt('<meta content="clean text">')
    assert not seo._tag_is_corrupt("<meta>")


# ---------------------------------------------------------------------------
# clean_meta_description
# ---------------------------------------------------------------------------

_CORRUPT = "&amp;lt;div lang=&amp;quot;en&amp;quot;&amp;gt;"


def test_clean_meta_description_uses_own_clean_name_desc_for_other_tags():
    # name= is clean; only twitter:description is corrupt → fixed from name.
    html = (
        '<meta name="description" content="A clean page description over twenty chars">'
        '<meta property="og:description" content="A clean page description over twenty chars">'
        f'<meta name="twitter:description" content="{_CORRUPT}">'
    )
    out = seo.clean_meta_description(Path("public/topics/x/index.html"), html)
    assert out.count("A clean page description over twenty chars") == 3
    assert "&amp;lt;" not in out


def test_clean_meta_description_repairs_article_from_jsonld():
    html = (
        f'<meta name="description" content="{_CORRUPT}">'
        f'<meta property="og:description" content="{_CORRUPT}">'
        f'<meta name="twitter:description" content="{_CORRUPT}">'
        + _ld('{"@type":"BlogPosting","description":"Real article summary twenty-plus chars"}')
    )
    out = seo.clean_meta_description(Path("public/some-post/index.html"), html)
    # Only the three description meta tags carry content="…" (the 4th
    # occurrence lives in the JSON-LD body).
    assert out.count('content="Real article summary twenty-plus chars"') == 3
    assert "&amp;lt;" not in out


def test_clean_meta_description_unchanged_when_no_source():
    # Corrupt but nothing recoverable (strips to <20, non-home, no json-ld).
    html = '<meta name="description" content="&amp;lt;a&amp;gt;">'
    assert seo.clean_meta_description(Path("public/x/index.html"), html) == html


def test_clean_meta_description_idempotent():
    html = f'<meta name="twitter:description" content="{_CORRUPT}">' + _ld(
        '{"@type":"BlogPosting","description":"Real article summary twenty-plus chars"}'
    )
    once = seo.clean_meta_description(Path("public/p/index.html"), html)
    assert seo.clean_meta_description(Path("public/p/index.html"), once) == once


# ---------------------------------------------------------------------------
# _pretty_canonical_url / normalize_canonical
# ---------------------------------------------------------------------------

BASE = "https://sebastienrousseau.com"


def test_pretty_canonical_url_forms():
    assert seo._pretty_canonical_url(Path("public/index.html")) == f"{BASE}/"
    assert seo._pretty_canonical_url(Path("public/about/index.html")) == f"{BASE}/about/"
    assert seo._pretty_canonical_url(Path("public/rss.xml")) == f"{BASE}/rss.xml"


def test_normalize_canonical_article():
    html = (
        '<link rel="canonical" href="https://sebastienrousseau.com/p/index.html">'
        '<meta property="og:url" content="https://sebastienrousseau.com/p">'
    )
    out = seo.normalize_canonical(Path("public/p/index.html"), html)
    assert out.count(f"{BASE}/p/") == 2
    assert "/index.html" not in out


def test_normalize_canonical_home_self_alternate():
    html = (
        '<link rel="canonical" href="https://sebastienrousseau.com/index.html">'
        '<meta property="og:url" content="https://sebastienrousseau.com">'
        '<link rel="alternate" hreflang="en" href="https://sebastienrousseau.com">'
    )
    out = seo.normalize_canonical(Path("public/index.html"), html)
    assert 'href="https://sebastienrousseau.com/"' in out
    assert 'href="https://sebastienrousseau.com"' not in out


# ---------------------------------------------------------------------------
# fix_article_og_type
# ---------------------------------------------------------------------------


def test_fix_article_og_type_promotes_article_pages():
    html = '<meta property="og:type" content="website">' + _ld('{"@type":"BlogPosting"}')
    assert 'content="article"' in seo.fix_article_og_type(html)


def test_fix_article_og_type_leaves_non_article_and_already_article():
    home = '<meta property="og:type" content="website">' + _ld('{"@type":"Person"}')
    assert seo.fix_article_og_type(home) == home
    already = '<meta property="og:type" content="article">' + _ld('{"@type":"NewsArticle"}')
    assert seo.fix_article_og_type(already) == already


# ---------------------------------------------------------------------------
# _format_metric / _kpi_metrics / inject_kpi_metrics
# ---------------------------------------------------------------------------


def test_format_metric():
    assert seo._format_metric(37_316_388, "compact") == "37.3M"
    assert seo._format_metric(1500, "compact") == "1.5K"
    assert seo._format_metric(664, "compact") == "664"
    assert seo._format_metric(19, "plain") == "19"
    assert seo._format_metric("FIPS 203", "plain") == "FIPS 203"


def test_kpi_metrics_reads_real_file_and_caches(monkeypatch):
    monkeypatch.setattr(seo, "_kpi_cache", None)
    first = seo._kpi_metrics()
    assert "downloads_total" in first
    assert seo._kpi_metrics() is first  # cache hit


def test_kpi_metrics_error_returns_empty(monkeypatch, tmp_path):
    monkeypatch.setattr(seo, "_kpi_cache", None)
    monkeypatch.setattr(seo, "_METRICS_JSON", tmp_path / "nope.json")
    assert seo._kpi_metrics() == {}


def test_inject_kpi_metrics_fills_known_skips_unknown(monkeypatch):
    monkeypatch.setattr(seo, "_kpi_cache", {"downloads_total": "9.9M"})
    html = (
        '<span class="kpi-cell-value" data-kpi="downloads_total">1M</span>'
        '<span class="kpi-cell-value" data-kpi="nope">x</span>'
    )
    out = seo.inject_kpi_metrics(html)
    assert ">9.9M</span>" in out
    assert ">x</span>" in out  # unknown key left untouched


def test_inject_kpi_metrics_no_op(monkeypatch):
    monkeypatch.setattr(seo, "_kpi_cache", {"downloads_total": "9.9M"})
    assert seo.inject_kpi_metrics("<p>no kpi cells</p>") == "<p>no kpi cells</p>"
    monkeypatch.setattr(seo, "_kpi_cache", {})
    assert seo.inject_kpi_metrics('<span data-kpi="x">y</span>') == '<span data-kpi="x">y</span>'


def test_inject_kpi_metrics_fills_entity_escaped_span(monkeypatch):
    # The homepage proof-rail is raw HTML inside index.md; SSG escapes the
    # leading `<` of the inline tags before postbuild runs. The fill must
    # still land on the `&lt;span … &lt;/span>` form (regression: the
    # homepage "By the numbers" stayed frozen on stale source values).
    monkeypatch.setattr(seo, "_kpi_cache", {"downloads_total": "38.1M"})
    html = '&lt;span class="kpi-cell-value" data-kpi="downloads_total">37.1M&lt;/span>'
    out = seo.inject_kpi_metrics(html)
    assert out == '&lt;span class="kpi-cell-value" data-kpi="downloads_total">38.1M&lt;/span>'


# ---------------------------------------------------------------------------
# align_jsonld_inlanguage
# ---------------------------------------------------------------------------


def test_align_jsonld_inlanguage_fixes_mismatch_only():
    html = (
        '<html lang="ar">'
        + _ld('{"@type":"WebSite","inLanguage":"en-GB"}')
        + _ld('{"@type":"BlogPosting","inLanguage":"ar"}')
    )
    out = seo.align_jsonld_inlanguage(html)
    assert out.count('"inLanguage":"ar"') == 2
    assert "en-GB" not in out


def test_align_jsonld_inlanguage_noop_without_html_lang():
    html = _ld('{"inLanguage":"en-GB"}')
    assert seo.align_jsonld_inlanguage(html) == html
