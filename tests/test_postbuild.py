"""Tests for scripts/postbuild.py — the SRI + CSP + feed-repair pass.

Each test exercises one of the postbuild transforms in isolation. We use
the in-process functions; we don't drive build.sh end-to-end because
postbuild has 10+ stages and the full smoke test belongs in CI.
"""
from __future__ import annotations

import postbuild as pb

# ---------------------------------------------------------------------------
# XML feed ampersand escape pass (`escape_xml_ampersands`)
# ---------------------------------------------------------------------------


def test_escape_xml_bare_amp_to_amp():
    assert pb.escape_xml_ampersands("AI & Payments") == "AI &amp; Payments"


def test_escape_xml_preserves_existing_amp_entity():
    assert pb.escape_xml_ampersands("AI &amp; Payments") == "AI &amp; Payments"


def test_escape_xml_undoes_double_escape():
    # Shokunin's bug — &amp;amp; should collapse back to &amp;.
    assert pb.escape_xml_ampersands("AI &amp;amp; Payments") == "AI &amp; Payments"


def test_escape_xml_preserves_apos_quot_lt_gt():
    s = "She said &apos;hi&apos; &lt;3 &quot;text&quot;"
    assert pb.escape_xml_ampersands(s) == s


def test_escape_xml_numeric_entities_preserved():
    assert pb.escape_xml_ampersands("&#169; &#x2014;") == "&#169; &#x2014;"


# ---------------------------------------------------------------------------
# XML feed URL repair — `_patch_block` lookup-by-title path
# Regression guard for #32: an earlier refactor (#31) rewrote _patch_block
# to slug-extract from the URL itself. Shokunin emits ``.../.meta/`` for
# every per-item link, so the regex fell back to the home URL on every
# match — producing 50 duplicate <guid>/<link> values per feed.
# ---------------------------------------------------------------------------


def test_patch_block_rewrites_localhost_url_using_title():
    """RSS <item> with localhost URL gets rewritten to canonical URL."""
    from postbuild_lib import output as out
    block = (
        "<item>"
        "<title>The Best Cloud Infrastructure Architecture in 2026</title>"
        "<link>http://127.0.0.1:8000/.meta/</link>"
        "<guid isPermaLink=\"true\">http://127.0.0.1:8000/.meta/</guid>"
        "</item>"
    )
    idx = {
        "The Best Cloud Infrastructure Architecture in 2026":
            "https://sebastienrousseau.com/best-cloud-2026",
    }
    rewritten = out._patch_block(block, idx)
    assert "https://sebastienrousseau.com/best-cloud-2026" in rewritten
    assert "127.0.0.1" not in rewritten
    assert "/.meta/" not in rewritten


def test_patch_block_no_op_when_title_not_in_index():
    """If we can't resolve the title, leave the block untouched —
    don't fall back to the home URL."""
    from postbuild_lib import output as out
    block = (
        "<item><title>Unknown post</title>"
        "<link>http://127.0.0.1:8000/.meta/</link></item>"
    )
    rewritten = out._patch_block(block, {})
    assert rewritten == block


def test_patch_block_decodes_xml_entities_in_title_lookup():
    """Feed emits ``&amp;`` in titles; the index should resolve via
    either escaped or unescaped form."""
    from postbuild_lib import output as out
    block = (
        "<item><title>AI &amp; Quantum</title>"
        "<link>http://localhost:8000/.meta/</link></item>"
    )
    idx = {"AI & Quantum": "https://sebastienrousseau.com/ai-quantum"}
    rewritten = out._patch_block(block, idx)
    assert "https://sebastienrousseau.com/ai-quantum" in rewritten


def test_patch_block_rewrites_meta_path_on_any_host():
    """``host/.meta/`` is rewritten even when the host isn't localhost."""
    from postbuild_lib import output as out
    block = (
        "<item><title>X</title>"
        "<link>https://example.com/.meta/</link></item>"
    )
    idx = {"X": "https://sebastienrousseau.com/x"}
    rewritten = out._patch_block(block, idx)
    assert "https://sebastienrousseau.com/x" in rewritten
    assert "/.meta/" not in rewritten


# ---------------------------------------------------------------------------
# GitHub stats — `_format_count`, `_relative_time`
# ---------------------------------------------------------------------------


def test_gh_format_count_under_1000():
    from postbuild_lib import github_stats as gh
    assert gh._format_count(0) == "0"
    assert gh._format_count(42) == "42"
    assert gh._format_count(999) == "999"


def test_gh_format_count_thousands():
    from postbuild_lib import github_stats as gh
    assert gh._format_count(1000) == "1k"
    assert gh._format_count(1234) == "1.2k"
    assert gh._format_count(12345) == "12.3k"


def test_gh_format_count_millions():
    from postbuild_lib import github_stats as gh
    assert gh._format_count(1000000) == "1M"
    assert gh._format_count(1234567) == "1.2M"


def test_gh_relative_time_empty_input():
    from postbuild_lib import github_stats as gh
    assert gh._relative_time("") == ""


def test_gh_relative_time_invalid_input():
    from postbuild_lib import github_stats as gh
    assert gh._relative_time("not-an-iso-timestamp") == ""


def test_gh_relative_time_returns_french_label_when_fr():
    """fr label should render seconds/minutes/etc. in French."""
    from datetime import UTC, datetime, timedelta

    from postbuild_lib import github_stats as gh
    one_hour_ago = (datetime.now(tz=UTC) - timedelta(hours=2)).isoformat()
    out = gh._relative_time(one_hour_ago, fr=True)
    # French uses "h" or "heures" depending on the format string; just
    # confirm we got a non-empty result and it isn't the English form.
    assert out
    assert "ago" not in out


def test_gh_stats_index_missing_file_returns_empty():
    """gh_stats_index gracefully returns {} when the JSON file is missing."""
    from pathlib import Path as _P
    from unittest.mock import patch

    from postbuild_lib import github_stats as gh
    with patch.object(gh, "_GH_STATS_PATH", _P("/nonexistent/path/gh-stats.json")):
        assert gh.gh_stats_index() == {}


# ---------------------------------------------------------------------------
# Frontmatter parser — `_parse_frontmatter`
# ---------------------------------------------------------------------------


def test_parse_frontmatter_basic(tmp_path):
    from postbuild_lib import output as out
    p = tmp_path / "post.md"
    p.write_text('---\ntitle: "Hello"\nurl: "https://example.com"\n---\n\nBody', encoding="utf-8")
    fm = out._parse_frontmatter(p)
    assert fm == {"title": "Hello", "url": "https://example.com"}


def test_parse_frontmatter_stops_at_second_delimiter(tmp_path):
    """Once we've seen the second ``---`` we ignore everything below
    even if it looks frontmatter-ish."""
    from postbuild_lib import output as out
    p = tmp_path / "post.md"
    p.write_text(
        '---\ntitle: "A"\n---\nbody\ntitle: "B" (in body)\n---\nmore\n', encoding="utf-8"
    )
    fm = out._parse_frontmatter(p)
    assert fm == {"title": "A"}


def test_parse_frontmatter_ignores_unquoted_values(tmp_path):
    """Parser only takes quoted string values — bare YAML scalars
    (numbers, booleans, lists) are skipped."""
    from postbuild_lib import output as out
    p = tmp_path / "post.md"
    p.write_text('---\ntitle: "Hi"\nweight: 42\nactive: true\n---\n', encoding="utf-8")
    fm = out._parse_frontmatter(p)
    assert fm == {"title": "Hi"}


def test_parse_frontmatter_no_frontmatter(tmp_path):
    """A file with no ``---`` block returns an empty dict."""
    from postbuild_lib import output as out
    p = tmp_path / "post.md"
    p.write_text("# Heading\n\nJust a body\n", encoding="utf-8")
    fm = out._parse_frontmatter(p)
    assert fm == {}


# ---------------------------------------------------------------------------
# Heading slug uniqueness — `inject_anchor_links_and_toc`
# Guards the WCAG/AAA "Duplicate id attribute value" failure: non-ASCII
# scripts (Arabic, Cyrillic, CJK) collapse multiple headings to the
# same Latin fragment (e.g. "FHE", "2026"). Pa11y rejects duplicate ids.
# ---------------------------------------------------------------------------


def test_inject_anchor_dedupes_colliding_slugs():
    """Two H2s that slugify to the same value get -2 suffix on the second."""
    from postbuild_lib.article_furniture import inject_anchor_links_and_toc
    html = (
        '<script type="application/ld+json">{"@type":"BlogPosting"}</script>'
        '<main><div class="wrap">'
        '<h2>تأثير FHE على القطاع المصرفي</h2>'
        '<h2>مستقبل FHE في القطاع المصرفي</h2>'
        '</div></main>'
    )
    out = inject_anchor_links_and_toc(html)
    import re as _re
    ids = _re.findall(r'<h2 id="([^"]+)"', out)
    assert len(ids) == 2
    assert ids[0] != ids[1]
    assert ids[0] == "fhe"
    assert ids[1] == "fhe-2"


def test_inject_anchor_empty_slug_gets_section_fallback():
    """A heading that slugifies to '' (pure Arabic, no Latin) gets
    a 'section-N' fallback so the id attribute is non-empty + unique."""
    from postbuild_lib.article_furniture import inject_anchor_links_and_toc
    html = (
        '<script type="application/ld+json">{"@type":"BlogPosting"}</script>'
        '<main><div class="wrap">'
        '<h2>كل النص عربي</h2><h2>عربي آخر</h2>'
        '</div></main>'
    )
    out = inject_anchor_links_and_toc(html)
    import re as _re
    ids = _re.findall(r'<h2 id="([^"]+)"', out)
    assert len(ids) == 2
    assert all(i for i in ids)  # non-empty
    assert ids[0] != ids[1]     # unique


# ---------------------------------------------------------------------------
# Localhost URL scrub — `scrub_localhost_urls`
# Guards the SEO/canonical regression: Shokunin bakes the dev-server URL
# into <link rel="canonical"> and the Atom-feed alternate; if it ships,
# Lighthouse SEO fails ("Document does not have a valid rel=canonical").
# ---------------------------------------------------------------------------


def test_scrub_localhost_canonical_to_prod():
    html = '<link rel="canonical" href="http://127.0.0.1:8000/about/index.html">'
    out, n = pb.scrub_localhost_urls(html)
    assert n == 1
    assert "127.0.0.1" not in out
    assert "https://sebastienrousseau.com/about/index.html" in out


def test_scrub_localhost_atom_alternate():
    html = '<link rel="alternate" type="application/atom+xml" href="http://localhost:8000/atom.xml"/>'
    out, _ = pb.scrub_localhost_urls(html)
    assert "https://sebastienrousseau.com/atom.xml" in out


def test_scrub_localhost_idempotent_when_no_match():
    html = '<link rel="canonical" href="https://sebastienrousseau.com/">'
    out, n = pb.scrub_localhost_urls(html)
    assert out == html
    assert n == 0


def test_scrub_localhost_handles_no_port():
    html = '<a href="http://127.0.0.1/feed.xml">feed</a>'
    out, _ = pb.scrub_localhost_urls(html)
    assert "https://sebastienrousseau.com/feed.xml" in out


# ---------------------------------------------------------------------------
# Word count
# ---------------------------------------------------------------------------


def test_compute_word_count_strips_asides():
    html = """<main>
        <aside class="post-lead"><p>TL;DR. ignore me totally please.</p></aside>
        <p>Real body content with some words.</p>
        <p>More body content here for the count.</p>
    </main>"""
    n = pb.compute_word_count(html)
    # 13 words in the two non-aside paragraphs ("Real body content with some
    # words" + "More body content here for the count"). The aside is stripped
    # so its 5 words don't count.
    assert n == 13


def test_compute_word_count_excludes_aside_content():
    only_aside = """<main>
        <aside class="post-lead"><p>This sentence is inside an aside block.</p></aside>
    </main>"""
    n = pb.compute_word_count(only_aside)
    # All the words are inside <aside>, which the stripper removes.
    assert n is None or n == 0


def test_compute_word_count_returns_none_without_main():
    assert pb.compute_word_count("<p>no main here</p>") is None


# ---------------------------------------------------------------------------
# About / mentions graph
# ---------------------------------------------------------------------------


def test_about_graph_emits_primary_only_when_one_match():
    html = """<script>
"@type":"BlogPosting","keywords":"Rust, unrelated-thing"
"url":"https://sebastienrousseau.com/x/index.html","datePublished":"2026-01-01"
</script>"""
    out = pb.build_about_graph(html)
    assert out is not None
    assert '"about"' in out
    assert '"mentions"' not in out
    assert "Rust" in out


def test_about_graph_emits_mentions_when_multiple_matches():
    html = """<script>
"@type":"BlogPosting","keywords":"CRYSTALS-Kyber, post-quantum cryptography, ISO 20022"
"url":"https://sebastienrousseau.com/x/index.html","datePublished":"2026-01-01"
</script>"""
    out = pb.build_about_graph(html)
    assert out is not None
    assert '"about"' in out
    assert '"mentions"' in out


def test_about_graph_suppresses_self_canonical_url():
    # When the current post IS the canonical for an entity, its own URL
    # must not appear in the entity's sameAs array.
    html = """<script>
"@type":"BlogPosting","keywords":"CRYSTALS-Kyber"
"url":"https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html","datePublished":"2023-11-19"
</script>"""
    out = pb.build_about_graph(html)
    assert out is not None
    assert "crystals-kyber-the-safeguarding" not in out


def test_about_graph_returns_none_when_no_keywords():
    html = '"@type":"BlogPosting","keywords":""'
    assert pb.build_about_graph(html) is None


# ---------------------------------------------------------------------------
# OG image swap (fix_social_image)
# ---------------------------------------------------------------------------


def test_fix_social_image_rewrites_og_and_twitter():
    html = '''
"@type":"BlogPosting","image":{"@type":"ImageObject","url":"https://cloudcdn.pro/banner.webp","width":"1200","height":"630"}
<meta property="og:image" content="https://cloudcdn.pro/divider.svg">
<meta property="og:image:width" content="1">
<meta property="og:image:height" content="1">
<meta name="twitter:image" content="https://cloudcdn.pro/divider.svg">
'''
    out = pb.fix_social_image(html)
    assert 'og:image" content="https://cloudcdn.pro/banner.webp"' in out
    assert 'twitter:image" content="https://cloudcdn.pro/banner.webp"' in out
    assert 'og:image:width" content="1200"' in out


def test_fix_social_image_promotes_twitter_card_summary_to_large():
    html = '''
"@type":"BlogPosting","image":{"@type":"ImageObject","url":"https://cloudcdn.pro/banner.webp"}
<meta name="twitter:card" content="summary">
'''
    out = pb.fix_social_image(html)
    assert 'twitter:card" content="summary_large_image"' in out


def test_fix_social_image_refuses_to_propagate_divider():
    html = '''
"@type":"BlogPosting","image":{"@type":"ImageObject","url":"https://cloudcdn.pro/divider.svg"}
<meta property="og:image" content="https://cloudcdn.pro/whatever.svg">
'''
    # Should NOT propagate a divider value into og:image.
    out = pb.fix_social_image(html)
    assert out == html
