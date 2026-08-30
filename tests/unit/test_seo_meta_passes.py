# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

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


def test_inject_kpi_metrics_fills_minified_unquoted_attributes(monkeypatch):
    # Regression: the ssg release CI pins emits the homepage minified —
    # attribute quotes stripped. The old `class="kpi-cell-value"` pattern
    # (and the `'data-kpi="'` guard) both missed that form, so the live
    # "By the numbers" rail stayed frozen on 37.1M / 663 / 84 while
    # /about/ and /projects/ — emitted unminified — showed fetched figures.
    monkeypatch.setattr(seo, "_kpi_cache", {"downloads_total": "42.1M", "github_stars": "672"})
    html = (
        "<div class=kpi-cell>"
        "<span class=kpi-cell-value data-kpi=downloads_total>37.1M</span>"
        "<span class=kpi-cell-label>Open-source downloads</span>"
        "</div>"
        "<span class=kpi-cell-value data-kpi=github_stars>663</span>"
    )
    out = seo.inject_kpi_metrics(html)
    assert ">42.1M</span>" in out
    assert ">672</span>" in out
    assert ">37.1M</span>" not in out
    assert seo.inject_kpi_metrics(out) == out  # idempotent


def test_inject_kpi_metrics_is_quoting_and_order_agnostic(monkeypatch):
    monkeypatch.setattr(seo, "_kpi_cache", {"github_stars": "672"})
    for html in (
        "<span class='kpi-cell-value' data-kpi='github_stars'>663</span>",
        "<span data-kpi=github_stars class=kpi-cell-value>663</span>",
        '<span class="stat kpi-cell-value big" data-kpi="github_stars">663</span>',
    ):
        assert ">672</span>" in seo.inject_kpi_metrics(html), html


def test_inject_kpi_metrics_requires_the_kpi_class(monkeypatch):
    # `data-kpi` alone is not the contract — the cell must also carry
    # `kpi-cell-value`, and a tag merely *starting* with "span" is not a span.
    monkeypatch.setattr(seo, "_kpi_cache", {"github_stars": "672"})
    for html in (
        "<span data-kpi=github_stars>663</span>",
        '<span class="kpi-cell-label" data-kpi="github_stars">663</span>',
        "<spanner class=kpi-cell-value data-kpi=github_stars>663</spanner>",
    ):
        assert seo.inject_kpi_metrics(html) == html, html


# ---------------------------------------------------------------------------
# canonicalise_internal_links
# ---------------------------------------------------------------------------


def test_canonicalise_internal_links_rewrites_every_quoting_style():
    # The ssg release CI pins minifies pages and strips attribute quotes, so
    # the pass has to handle bare values as well as quoted ones.
    for html, want in (
        ('<a href="/about/index.html">A</a>', '<a href="/about/">A</a>'),
        ("<a href='/about/index.html'>A</a>", "<a href='/about/'>A</a>"),
        ("<a href=/about/index.html>A</a>", "<a href=/about/>A</a>"),
    ):
        out, n = seo.canonicalise_internal_links(html)
        assert out == want, html
        assert n == 1


def test_canonicalise_internal_links_handles_root_absolute_and_nested():
    for html, want in (
        # Home page: canonical is "/", not "/index.html".
        ('<a href="/index.html">H</a>', '<a href="/">H</a>'),
        (
            '<a href="https://sebastienrousseau.com/articles/index.html">A</a>',
            '<a href="https://sebastienrousseau.com/articles/">A</a>',
        ),
        ('<a href="/fr/a-propos/index.html">A</a>', '<a href="/fr/a-propos/">A</a>'),
        ('<form action="/contact/index.html">', '<form action="/contact/">'),
    ):
        assert seo.canonicalise_internal_links(html)[0] == want, html


def test_canonicalise_internal_links_preserves_fragment_and_query():
    out, _ = seo.canonicalise_internal_links('<a href="/editorial/index.html#bot-policy">p</a>')
    assert out == '<a href="/editorial/#bot-policy">p</a>'
    out, _ = seo.canonicalise_internal_links('<a href="/search/index.html?q=iso">s</a>')
    assert out == '<a href="/search/?q=iso">s</a>'


def test_canonicalise_internal_links_leaves_everything_else_alone():
    for html in (
        # External host — not ours to canonicalise.
        '<a href="https://example.com/a/index.html">e</a>',
        # Not an href/action attribute.
        '<img src="/assets/index.html" />',
        # index.html is not the final path segment.
        '<a href="/docs/index.html.bak">x</a>',
        # JSON-LD sameAs carries the index.html form deliberately; it has no
        # href= prefix, so the pass must not reach into it.
        '<script type="application/ld+json">'
        '{"sameAs":["https://sebastienrousseau.com/p/index.html"]}</script>',
        # Already canonical.
        '<a href="/about/">A</a>',
    ):
        assert seo.canonicalise_internal_links(html) == (html, 0), html


def test_canonicalise_internal_links_is_idempotent_and_counts():
    html = (
        '<a href="/about/index.html">A</a>'
        "<a href=/articles/index.html>B</a>"
        '<a href="https://example.com/x/index.html">skip</a>'
    )
    once, n1 = seo.canonicalise_internal_links(html)
    twice, n2 = seo.canonicalise_internal_links(once)
    assert n1 == 2
    assert twice == once and n2 == 0
    assert "example.com/x/index.html" in once


def test_canonicalise_internal_links_no_op_without_index_html():
    html = "<p>nothing to do</p>"
    assert seo.canonicalise_internal_links(html) == (html, 0)


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


def test_inject_kpi_metrics_fills_inline_prose_span(monkeypatch):
    # /about/ quoted the article count mid-sentence as a hand-maintained
    # number: it said "73 signed, dated pieces" while the KPI rail directly
    # above it, filled from metrics.json, said 105. The prose opts in with
    # `kpi-inline` so it tracks the same source without rail styling.
    monkeypatch.setattr(seo, "_kpi_cache", {"articles_signed": "105"})
    html = (
        '<p class="story-card-body">'
        '<span class="kpi-inline" data-kpi="articles_signed">73</span>'
        " signed, dated pieces.</p>"
    )
    out = seo.inject_kpi_metrics(html)
    assert ">105</span>" in out
    assert ">73</span>" not in out
    assert seo.inject_kpi_metrics(out) == out  # idempotent


def test_about_prose_article_count_is_not_hand_maintained():
    """The count in /about/ prose must come from metrics.json, in every locale.

    A bare number here goes stale on the next publish — it had drifted 32
    articles behind (73 in prose, 105 in the rail directly above) before this
    was caught. Asserting on the source rather than the built page means a
    hand-edit is rejected at unit-test time, not noticed months later.
    """
    import json
    import re
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent.parent
    # The articles card: the story card whose body states the count.
    span = re.compile(
        r'<p class="story-card-body">[^<]*<span class="kpi-inline" '
        r'data-kpi="articles_signed">\d+</span>'
    )
    missing = []

    def check(label: str, body: str) -> None:
        if len(span.findall(body)) != 1:
            missing.append(label)

    check("en", (root / "_posts" / "about.md").read_text())
    for p in sorted((root / "_data" / "i18n").glob("*/static_bodies.json")):
        check(p.parent.name, json.loads(p.read_text()).get("bodies", {}).get("about", ""))

    assert not missing, (
        "about prose must state the article count via a kpi-inline span, "
        f"not a hand-typed number; missing in: {missing}"
    )


def test_robots_sitemap_lines_derive_from_disk(tmp_path):
    """robots.txt must name the sitemaps the build produced, not a literal.

    The previous version hardcoded three Sitemap lines, so adding a locale
    left its news sitemap unadvertised with nothing to notice: 34 non-empty
    locale news sitemaps existed while robots.txt named 2.
    """
    from postbuild_lib import output

    (tmp_path / "fr").mkdir()
    (tmp_path / "sitemap.xml").write_text("<urlset/>")
    # Root legitimately empty — nothing published inside the 48 h window.
    (tmp_path / "news-sitemap.xml").write_text("<urlset></urlset>")
    (tmp_path / "fr" / "news-sitemap.xml").write_text("<urlset><url/></urlset>")

    lines = output._news_sitemap_lines(tmp_path, origin="https://example.test")
    assert lines == [
        "Sitemap: https://example.test/sitemap.xml",
        "Sitemap: https://example.test/news-sitemap.xml",
        "Sitemap: https://example.test/fr/news-sitemap.xml",
    ]


def test_robots_skips_sitemaps_the_build_did_not_produce(tmp_path):
    """An advertised locale with no file on disk is omitted, not invented."""
    from postbuild_lib import output

    (tmp_path / "sitemap.xml").write_text("<urlset/>")
    (tmp_path / "news-sitemap.xml").write_text("<urlset></urlset>")
    # No fr/ directory at all.
    lines = output._news_sitemap_lines(tmp_path, origin="https://example.test")
    assert "fr/news-sitemap.xml" not in " ".join(lines)


def test_robots_does_not_filter_on_emptiness(tmp_path):
    """Regression: an empty root news sitemap is the *correct* state.

    Filtering on `<url>` presence drops the compliant root (nothing published
    in 48 h) while keeping locale sitemaps that carry months of entries — the
    exact inversion of what is wanted. See #433.
    """
    from postbuild_lib import output

    (tmp_path / "sitemap.xml").write_text("<urlset/>")
    (tmp_path / "news-sitemap.xml").write_text("<urlset></urlset>")  # zero <url>
    lines = output._news_sitemap_lines(tmp_path, origin="https://example.test")
    assert "Sitemap: https://example.test/news-sitemap.xml" in lines
