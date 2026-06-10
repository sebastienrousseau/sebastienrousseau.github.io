"""Tests for the postbuild structured-data passes — word count,
about/mentions graph, HowTo JSON-LD, and FAQ-to-QAPage conversion.

Split out of test_postbuild.py; tests are verbatim copies.
"""

from __future__ import annotations

import postbuild as pb

# ---------------------------------------------------------------------------
# inject_word_count + fix_social_image (seo.py)
# ---------------------------------------------------------------------------


def test_inject_word_count_adds_field_to_blogposting():
    html = (
        '<script type="application/ld+json">'
        '{"@type":"BlogPosting","headline":"X"}'
        "</script>"
        "<main>One two three four five six.</main>"
    )
    out = pb.inject_word_count(html)
    assert '"wordCount":6' in out


def test_inject_word_count_skips_when_no_main():
    html = '<script type="application/ld+json">{"@type":"BlogPosting"}</script>'
    assert pb.inject_word_count(html) == html


def test_inject_word_count_skips_when_main_is_empty():
    html = (
        '<script type="application/ld+json">{"@type":"BlogPosting","headline":"X"}</script>'
        "<main></main>"
    )
    out = pb.inject_word_count(html)
    assert '"wordCount"' not in out


def test_compute_word_count_strips_aside_blocks():
    """Asides (lead, related-cards) are not counted toward the article body."""
    html = "<main><aside>ignore this aside content</aside>" "<p>real body words here</p></main>"
    n = pb.compute_word_count(html)
    assert n == 4  # "real body words here"


# ---------------------------------------------------------------------------
# _convert_faq_to_qa — FAQ → <details qa-item> rewrite
# ---------------------------------------------------------------------------


def test_convert_faq_to_qa_rewrites_strong_q_a_pattern():
    from postbuild_lib.article_furniture import _convert_faq_to_qa

    html = (
        '<main><div class="wrap">'
        '<h2 id="frequently-asked-questions">FAQ</h2>'
        "<p><strong>Q1: Is this hot?</strong></p>"
        "<p>Yes, very.</p>"
        "<p><strong>Q2: Anything else?</strong></p>"
        "<p>Maybe later.</p>"
        '<h2 id="next">Next section</h2>'
        "</div></main>"
    )
    out = _convert_faq_to_qa(html)
    assert '<details class="qa-item" open>' in out
    assert '<summary class="qa-q">Q1: Is this hot?</summary>' in out
    assert '<summary class="qa-q">Q2: Anything else?</summary>' in out
    assert '<section class="qa-a"><p>Yes, very.</p></section>' in out


def test_convert_faq_to_qa_no_op_without_faq_h2():
    from postbuild_lib.article_furniture import _convert_faq_to_qa

    html = '<main><div class="wrap"><h2 id="intro">Hello</h2><p>Body.</p></div></main>'
    assert _convert_faq_to_qa(html) == html


# ---------------------------------------------------------------------------
# seo.inject_about + _build_howto_jsonld
# ---------------------------------------------------------------------------


def test_inject_about_no_op_when_no_keyword_matches():
    """BlogPosting keywords that match no ENTITY_AUTHORITY → unchanged."""
    html = (
        '<script type="application/ld+json">'
        '{"@type":"BlogPosting","headline":"X","keywords":"basketweaving, ceramics"}'
        "</script>"
    )
    assert pb.inject_about(html) == html


def test_inject_about_injects_about_field_for_known_entity():
    """A keyword that maps to ENTITY_AUTHORITY produces an ``about`` field."""
    html = (
        '<script type="application/ld+json">'
        '{"@type":"BlogPosting","keywords":"post-quantum cryptography, banking","headline":"X"}'
        "</script>"
    )
    out = pb.inject_about(html)
    assert '"about":' in out
    assert '"@type":"Thing"' in out


def test_inject_howto_no_op_when_no_resource_marker():
    """Pages without the ``data-resource-howto`` marker are untouched."""
    from pathlib import Path as _P

    html = "<p>regular content</p>"
    assert pb.inject_howto(_P("public/index.html"), html) == html


def test_inject_howto_emits_jsonld_for_known_slug():
    """A page whose slug is in HOWTO_SCHEMAS gets a HowTo JSON-LD before </body>."""
    from pathlib import Path as _P

    from postbuild_lib.seo import HOWTO_SCHEMAS, inject_howto

    slug = next(iter(HOWTO_SCHEMAS))
    page = _P(f"public/{slug}/index.html")
    html = "<html><body>content</body></html>"
    out = inject_howto(page, html)
    assert '"@type":"HowTo"' in out


def test_inject_howto_idempotent_when_already_present():
    from pathlib import Path as _P

    from postbuild_lib.seo import HOWTO_SCHEMAS, inject_howto

    slug = next(iter(HOWTO_SCHEMAS))
    html = '<html><body><script>"@type":"HowTo"</script></body></html>'
    assert inject_howto(_P(f"public/{slug}/index.html"), html) == html


def test_convert_faq_to_qa_handles_no_qa_pairs():
    """A FAQ section whose body has no <p><strong>Q?</strong></p> pattern
    is returned unchanged (line 520)."""
    from postbuild_lib.article_furniture import _convert_faq_to_qa

    html = (
        '<main><div class="wrap">'
        '<h2 id="frequently-asked-questions">FAQ</h2>'
        "<p>Just prose, no Q strong markers.</p>"
        '<h2 id="next">Next</h2>'
        "</div></main>"
    )
    out = _convert_faq_to_qa(html)
    assert 'class="qa-item"' not in out


def test_convert_faq_to_qa_french_uses_localised_headline():
    """A FR FAQ section uses ``Questions ?`` + ``Réponses.``."""
    from postbuild_lib.article_furniture import _convert_faq_to_qa

    html = (
        '<html lang="fr">'
        '<main><div class="wrap">'
        '<h2 id="foire-aux-questions">FAQ</h2>'
        "<p><strong>Q1: Ça va?</strong></p><p>Oui.</p>"
        '<h2 id="suivant">Suivant</h2>'
        "</div></main>"
    )
    out = _convert_faq_to_qa(html)
    assert "Questions ?" in out
    assert "Réponses." in out


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
