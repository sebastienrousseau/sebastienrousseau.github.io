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
