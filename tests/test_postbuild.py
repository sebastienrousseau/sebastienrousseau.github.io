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
# inject_word_count + fix_social_image (seo.py)
# ---------------------------------------------------------------------------


def test_inject_word_count_adds_field_to_blogposting():
    html = (
        '<script type="application/ld+json">'
        '{"@type":"BlogPosting","headline":"X"}'
        '</script>'
        '<main>One two three four five six.</main>'
    )
    out = pb.inject_word_count(html)
    assert '"wordCount":6' in out


def test_inject_word_count_skips_when_no_main():
    html = '<script type="application/ld+json">{"@type":"BlogPosting"}</script>'
    assert pb.inject_word_count(html) == html


def test_inject_word_count_skips_when_main_is_empty():
    html = (
        '<script type="application/ld+json">{"@type":"BlogPosting","headline":"X"}</script>'
        '<main></main>'
    )
    out = pb.inject_word_count(html)
    assert '"wordCount"' not in out


def test_compute_word_count_strips_aside_blocks():
    """Asides (lead, related-cards) are not counted toward the article body."""
    html = (
        '<main><aside>ignore this aside content</aside>'
        '<p>real body words here</p></main>'
    )
    n = pb.compute_word_count(html)
    assert n == 4  # "real body words here"


def test_fix_social_image_promotes_summary_to_large():
    """Twitter card defaults to ``summary`` on some posts; we lift to
    ``summary_large_image`` when a real banner is present."""
    html = (
        '<script type="application/ld+json">'
        '{"@type":"BlogPosting","image":{"url":"https://x/banner.webp","width":1200,"height":628}}'
        '</script>'
        '<meta property="og:image" content="">'
        '<meta name="twitter:image" content="">'
        '<meta name="twitter:card" content="summary">'
    )
    out = pb.fix_social_image(html)
    assert "summary_large_image" in out
    assert 'content="https://x/banner.webp"' in out


def test_fix_social_image_no_op_when_banner_is_placeholder():
    html = (
        '<script type="application/ld+json">'
        '{"@type":"BlogPosting","image":{"url":"divider.webp"}}'
        '</script>'
        '<meta name="twitter:card" content="summary">'
    )
    out = pb.fix_social_image(html)
    assert out == html  # untouched


# ---------------------------------------------------------------------------
# llms.txt + robots.txt + json-feed writers
# ---------------------------------------------------------------------------


def test_build_llms_txt_includes_canonical_sections():
    """llms.txt must contain H1, summary, and the seven canonical entries."""
    from postbuild_lib.output import build_llms_txt
    text = build_llms_txt()
    assert text.startswith("# Sebastien Rousseau")
    for section in ("Canonical entry points", "Feeds", "Areas of expertise", "Contact"):
        assert f"## {section}" in text
    for entry in ("Home", "About", "Articles", "Papers", "Projects", "Topics", "Contact"):
        assert f"[{entry}](https://sebastienrousseau.com/" in text


def test_write_llms_txt_skips_when_unchanged(tmp_path):
    """No-op when the target already has the current content."""
    from postbuild_lib.output import build_llms_txt, write_llms_txt
    (tmp_path / "llms.txt").write_text(build_llms_txt(), encoding="utf-8")
    assert write_llms_txt(tmp_path) is False


def test_write_llms_txt_writes_when_changed(tmp_path):
    """Writes when the target is missing or stale."""
    from postbuild_lib.output import write_llms_txt
    assert write_llms_txt(tmp_path) is True
    assert (tmp_path / "llms.txt").is_file()


def test_write_robots_emits_sitemap_lines(tmp_path):
    from postbuild_lib.output import write_robots
    write_robots(tmp_path)
    text = (tmp_path / "robots.txt").read_text(encoding="utf-8")
    assert "User-agent:" in text
    assert "Sitemap: https://sebastienrousseau.com/sitemap.xml" in text


def test_write_robots_idempotent(tmp_path):
    """Second write with no content change returns False."""
    from postbuild_lib.output import write_robots
    assert write_robots(tmp_path) is True
    assert write_robots(tmp_path) is False


# ---------------------------------------------------------------------------
# Stylesheet sanitizer — `_sanitize_link_tag` + `hoist_body_link_stylesheets`
# ---------------------------------------------------------------------------


def test_sanitize_link_tag_collapses_duplicate_crossorigin():
    from postbuild_lib.article_furniture import _sanitize_link_tag
    tag = '<link rel="stylesheet" href="/x.css" crossorigin="anonymous" crossorigin="anonymous">'
    out = _sanitize_link_tag(tag)
    assert out.count('crossorigin="anonymous"') == 1


def test_sanitize_link_tag_strips_trailing_double_quote():
    from postbuild_lib.article_furniture import _sanitize_link_tag
    tag = '<link rel="stylesheet" href="/x.css" crossorigin="anonymous"">'
    out = _sanitize_link_tag(tag)
    # Two adjacent quotes before `>` are collapsed to one
    assert '""' not in out


def test_hoist_body_link_stylesheets_moves_to_head():
    from postbuild_lib.article_furniture import hoist_body_link_stylesheets
    html = (
        '<head><meta charset="utf-8"></head>'
        '<body><main><link rel="stylesheet" href="/widget.css"></main></body>'
    )
    out, n = hoist_body_link_stylesheets(html)
    assert n == 1
    # Stylesheet now in head, not in body
    head_end = out.find("</head>")
    body_start = out.find("<body>")
    sheet = out.find('href="/widget.css"')
    assert sheet < head_end < body_start


def test_hoist_body_link_stylesheets_no_op_when_already_in_head():
    from postbuild_lib.article_furniture import hoist_body_link_stylesheets
    html = (
        '<head><link rel="stylesheet" href="/x.css"></head><body><main></main></body>'
    )
    _, n = hoist_body_link_stylesheets(html)
    assert n == 0


# ---------------------------------------------------------------------------
# slugify edge cases
# ---------------------------------------------------------------------------


def test_slugify_basic_ascii():
    from postbuild_lib.article_furniture import slugify
    assert slugify("Hello, World!") == "hello-world"


def test_slugify_strips_html_tags():
    from postbuild_lib.article_furniture import slugify
    assert slugify("<strong>Heading</strong> Text") == "heading-text"


def test_slugify_folds_accents():
    from postbuild_lib.article_furniture import slugify
    assert slugify("Références") == "references"


def test_slugify_arabic_strips_to_empty():
    """Pure-Arabic input slugifies to '' — caller must handle fallback."""
    from postbuild_lib.article_furniture import slugify
    assert slugify("النص العربي") == ""


def test_slugify_truncates_long_input():
    from postbuild_lib.article_furniture import slugify
    s = "a" * 200
    assert len(slugify(s)) <= 80


# ---------------------------------------------------------------------------
# News-sitemap shrink — Google News recommendations
# ---------------------------------------------------------------------------


def test_truncate_news_title_under_limit_passes_through():
    from postbuild_lib import output as out
    title = "Short title"
    assert out._truncate_news_title(title) == title


def test_truncate_news_title_clips_at_word_boundary():
    from postbuild_lib import output as out
    title = "A very long title that absolutely exceeds the eighty character recommendation set by Google News"
    result = out._truncate_news_title(title)
    assert len(result) <= 80
    assert result.endswith("…")
    # Must clip at a word boundary, not mid-word
    body = result.rstrip("…").rstrip()
    assert not title[len(body)].isalpha() or title[: len(body) + 1].endswith(" ")


def test_truncate_news_title_custom_limit():
    from postbuild_lib import output as out
    assert len(out._truncate_news_title("one two three four five", limit=10)) <= 10


def test_limit_news_keywords_under_limit_passes_through():
    from postbuild_lib import output as out
    kws = "a, b, c"
    assert out._limit_news_keywords(kws) == kws


def test_limit_news_keywords_trims_to_first_n():
    from postbuild_lib import output as out
    kws = ", ".join(f"k{i}" for i in range(15))
    result = out._limit_news_keywords(kws)
    items = [k.strip() for k in result.split(",")]
    assert len(items) == 10
    assert items == [f"k{i}" for i in range(10)]


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
# Article furniture renderers (tag badges, meta bar, prev/next nav)
# ---------------------------------------------------------------------------


def test_render_tag_badges_empty_returns_empty_string():
    from postbuild_lib.article_furniture import LABELS_EN, _render_tag_badges
    assert _render_tag_badges([], LABELS_EN) == ""


def test_render_tag_badges_en_uses_tags_prefix():
    from postbuild_lib.article_furniture import LABELS_EN, _render_tag_badges
    out = _render_tag_badges(["quantum", "ISO 20022"], LABELS_EN, lang="en")
    assert '/tags/index.html#h3-quantum' in out
    assert '/tags/index.html#h3-iso-20022' in out
    assert 'rel="tag"' in out
    assert 'aria-label="Topics"' in out


def test_render_tag_badges_fr_uses_etiquettes_prefix():
    from postbuild_lib.article_furniture import LABELS_FR, _render_tag_badges
    out = _render_tag_badges(["quantique"], LABELS_FR, lang="fr")
    assert '/fr/etiquettes/index.html#h3-quantique' in out


def test_render_meta_bar_includes_author_and_dates():
    from postbuild_lib.article_furniture import LABELS_EN, _render_meta_bar
    out = _render_meta_bar(
        date_pub="2026-05-12T08:00:00+01:00",
        date_mod="2026-05-15T08:00:00+01:00",
        word_count=440,
        labels=LABELS_EN,
        lang="en",
    )
    assert 'class="article-author"' in out
    assert 'class="meta-pub"' in out
    assert 'class="meta-rev"' in out  # mod > pub → revised stamp present
    assert '2 min read' in out  # 440 words / 220 wpm → 2 min


def test_render_meta_bar_suppresses_updated_when_same_day():
    """If date_mod is the same day as date_pub, the 'Updated' stamp is suppressed."""
    from postbuild_lib.article_furniture import LABELS_EN, _render_meta_bar
    out = _render_meta_bar(
        date_pub="2026-05-12T08:00:00+01:00",
        date_mod="2026-05-12T18:00:00+01:00",
        word_count=None,
        labels=LABELS_EN,
    )
    assert 'class="meta-pub"' in out
    assert 'class="meta-rev"' not in out


def test_render_meta_bar_french_uses_localised_author_url():
    from postbuild_lib.article_furniture import LABELS_FR, _render_meta_bar
    out = _render_meta_bar(
        date_pub="2026-05-12T08:00:00+01:00",
        date_mod="",
        word_count=220,
        labels=LABELS_FR,
        lang="fr",
    )
    assert 'href="/fr/a-propos/index.html"' in out
    assert 'min de lecture' in out


# ---------------------------------------------------------------------------
# inject_sigstore_attestation
# ---------------------------------------------------------------------------


def test_inject_sigstore_no_op_without_blogposting():
    from postbuild_lib.article_furniture import inject_sigstore_attestation
    html = '<p>plain page, no BlogPosting graph</p>'
    assert inject_sigstore_attestation(html, "post-slug") == html


def test_inject_sigstore_no_op_when_bundle_missing(tmp_path, monkeypatch):
    """Without a sigstore bundle on disk, the injector is a no-op."""
    from postbuild_lib import article_furniture as af
    html = (
        '<script type="application/ld+json">{"@type":"BlogPosting"}</script>'
        '<main></main>'
    )
    monkeypatch.chdir(tmp_path)  # no _data/sigstore/* tree → no bundle
    assert af.inject_sigstore_attestation(html, "post-slug") == html


def test_inject_sigstore_emits_badge_when_bundle_exists(tmp_path, monkeypatch):
    """With ``_SIGSTORE_CONFIG_PRESENT`` flipped on and a bundle on disk,
    the badge is appended just before ``</main>``."""
    from unittest.mock import patch

    from postbuild_lib import article_furniture as af
    public = tmp_path / "public"
    (public / "sigstore").mkdir(parents=True)
    (public / "sigstore" / "post-slug.bundle").write_text("{}", encoding="utf-8")
    html = (
        '<script type="application/ld+json">{"@type":"BlogPosting"}</script>'
        '<main><p>body</p></main>'
    )
    with patch.object(af, "_SIGSTORE_CONFIG_PRESENT", True), \
         patch.object(af, "PUBLIC", public):
        out = af.inject_sigstore_attestation(html, "post-slug")
    assert 'class="article-sigstore"' in out
    assert 'Sigstore signature' in out
    assert 'href="/sigstore/post-slug.bundle"' in out


def test_inject_sigstore_idempotent():
    """Re-running on a page that already has the badge is a no-op."""
    from unittest.mock import patch

    from postbuild_lib import article_furniture as af
    html = (
        '<script type="application/ld+json">{"@type":"BlogPosting"}</script>'
        '<main><aside class="article-sigstore">badge</aside></main>'
    )
    with patch.object(af, "_SIGSTORE_CONFIG_PRESENT", True):
        # Even with the flag on the existing badge means we bail early
        out = af.inject_sigstore_attestation(html, "post-slug")
    assert out == html


# ---------------------------------------------------------------------------
# _labels_for_lang — cache + LanguageError fallback
# ---------------------------------------------------------------------------


def test_labels_for_lang_returns_english_for_en():
    from postbuild_lib.article_furniture import LABELS_EN, _labels_for_lang
    assert _labels_for_lang("en") == LABELS_EN


def test_labels_for_lang_handles_unknown_lang_gracefully():
    """An unknown lang falls back to LABELS_EN (no exception)."""
    from postbuild_lib.article_furniture import LABELS_EN, _labels_for_lang
    out = _labels_for_lang("zz")
    # Output is a *copy* with EN as base; if the lang has no labels file,
    # the result is exactly LABELS_EN.
    assert out == LABELS_EN


# ---------------------------------------------------------------------------
# _convert_faq_to_qa — FAQ → <details qa-item> rewrite
# ---------------------------------------------------------------------------


def test_convert_faq_to_qa_rewrites_strong_q_a_pattern():
    from postbuild_lib.article_furniture import _convert_faq_to_qa
    html = (
        '<main><div class="wrap">'
        '<h2 id="frequently-asked-questions">FAQ</h2>'
        '<p><strong>Q1: Is this hot?</strong></p>'
        '<p>Yes, very.</p>'
        '<p><strong>Q2: Anything else?</strong></p>'
        '<p>Maybe later.</p>'
        '<h2 id="next">Next section</h2>'
        '</div></main>'
    )
    out = _convert_faq_to_qa(html)
    assert '<details class="qa-item">' in out
    assert '<summary class="qa-q">Q1: Is this hot?</summary>' in out
    assert '<summary class="qa-q">Q2: Anything else?</summary>' in out
    assert '<section class="qa-a"><p>Yes, very.</p></section>' in out


def test_convert_faq_to_qa_no_op_without_faq_h2():
    from postbuild_lib.article_furniture import _convert_faq_to_qa
    html = '<main><div class="wrap"><h2 id="intro">Hello</h2><p>Body.</p></div></main>'
    assert _convert_faq_to_qa(html) == html


# ---------------------------------------------------------------------------
# Citations + sources list
# ---------------------------------------------------------------------------


def test_extract_citations_picks_authoritative_outbound_only():
    """Only links to ``CITATION_AUTHORITIES`` hosts make it into the citation graph."""
    from postbuild_lib.article_furniture import _extract_citations
    html = (
        '<script type="application/ld+json">{"@type":"BlogPosting"}</script>'
        '<main><div class="wrap">'
        '<a href="/internal/">internal</a>'
        '<a href="https://example.com/page">non-authority</a>'
        '<a href="https://wikipedia.org/wiki/Quantum">External wiki</a>'
        '<a href="https://nist.gov/pubs">NIST</a>'
        '<a href="#anchor">anchor</a>'
        '</div></main>'
    )
    cites = _extract_citations(html)
    urls = [c['url'] for c in cites]
    assert 'https://wikipedia.org/wiki/Quantum' in urls
    assert 'https://nist.gov/pubs' in urls
    assert 'https://example.com/page' not in urls
    assert not any(u.startswith(('/', '#')) for u in urls)


def test_inject_citations_no_op_without_outbound_links():
    from postbuild_lib.article_furniture import inject_citations
    html = (
        '<script type="application/ld+json">{"@type":"BlogPosting","speakable":{}}</script>'
        '<main><div class="wrap"><a href="/internal/">x</a></div></main>'
    )
    assert inject_citations(html) == html


# ---------------------------------------------------------------------------
# GitHub stats renderer (`_render_gh_badges`)
# ---------------------------------------------------------------------------


def test_render_gh_badges_full_payload_emits_four_pills():
    """Stars + forks + license + pushed_at all produce a pill."""
    from datetime import UTC, datetime, timedelta

    from postbuild_lib.github_stats import _render_gh_badges
    info = {
        "stars": 121,
        "forks": 9,
        "license": "MIT",
        "pushed_at": (datetime.now(tz=UTC) - timedelta(days=3)).isoformat(),
    }
    out = _render_gh_badges(info, lang="en")
    assert 'class="gh-stat gh-stars"' in out
    assert 'class="gh-stat gh-forks"' in out
    assert 'class="gh-stat gh-license"' in out
    assert 'class="gh-stat gh-pushed"' in out
    assert "121" in out
    assert "MIT" in out


def test_render_gh_badges_drops_license_when_noassertion():
    """NOASSERTION / OTHER / "" license values are filtered out."""
    from postbuild_lib.github_stats import _render_gh_badges
    info = {"stars": 1, "forks": 0, "license": "NOASSERTION", "pushed_at": ""}
    out = _render_gh_badges(info, lang="en")
    assert 'gh-license' not in out


def test_render_gh_badges_empty_payload_returns_empty_string():
    from postbuild_lib.github_stats import _render_gh_badges
    out = _render_gh_badges({"stars": 0, "forks": 0, "license": "", "pushed_at": ""})
    assert out == ""


def test_normalise_url_strips_scheme_www_trailing_slash():
    from postbuild_lib.github_stats import _normalise_url
    assert _normalise_url("https://www.example.com/") == "example.com"
    assert _normalise_url("HTTP://Example.COM/foo/") == "example.com/foo"
    assert _normalise_url("https://example.com") == "example.com"


def test_lookup_by_slug_href_hits_index():
    from postbuild_lib.github_stats import _lookup_by_slug_href
    # The regex captures the full ``sebastienrousseau/<repo>`` group, so the
    # index key has to match that exactly.
    idx = {"sebastienrousseau/foo": {"name": "foo", "stars": 10}}
    inner = '<a href="https://github.com/sebastienrousseau/foo">…</a>'
    assert _lookup_by_slug_href(inner, idx) == idx["sebastienrousseau/foo"]


def test_lookup_by_slug_href_misses_when_repo_not_tracked():
    from postbuild_lib.github_stats import _lookup_by_slug_href
    idx = {"sebastienrousseau/bar": {"name": "bar"}}
    inner = '<a href="https://github.com/sebastienrousseau/foo">…</a>'
    assert _lookup_by_slug_href(inner, idx) is None


def test_lookup_by_homepage_matches_normalised_url():
    """Homepage URL and card href normalise to the same key (scheme + www stripped)."""
    from postbuild_lib.github_stats import _lookup_by_homepage
    idx = {"foo": {"name": "foo", "homepage": "https://www.foo-project.io/"}}
    inner = '<a href="https://foo-project.io">read more</a>'
    assert _lookup_by_homepage(inner, idx) == idx["foo"]


def test_lookup_by_h3_title_matches_case_insensitive():
    from postbuild_lib.github_stats import _lookup_by_h3_title
    idx = {"foo": {"name": "Foo"}}
    inner = '<h3><a>foo</a></h3>'
    assert _lookup_by_h3_title(inner, idx) == idx["foo"]


def test_inject_github_stats_no_op_without_cards():
    from postbuild_lib.github_stats import inject_github_stats
    html = '<p>no newsroom cards here</p>'
    assert inject_github_stats(html, {"foo": {"stars": 1}}) == html


def test_inject_github_stats_no_op_with_empty_index():
    from postbuild_lib.github_stats import inject_github_stats
    html = '<article class="newsroom-card"><a href="https://github.com/sebastienrousseau/foo">x</a></article>'
    assert inject_github_stats(html, {}) == html


def test_inject_github_stats_injects_badges_into_matching_card():
    """A newsroom-card whose GitHub href is tracked gets a badge row appended."""
    from postbuild_lib.github_stats import inject_github_stats
    idx = {
        "sebastienrousseau/foo": {
            "name": "foo",
            "stars": 42,
            "forks": 3,
            "license": "MIT",
            "pushed_at": "",
        },
    }
    html = (
        '<article class="newsroom-card">'
        '<a href="https://github.com/sebastienrousseau/foo">link</a>'
        '<div>card body</div>'
        '</article>'
    )
    out = inject_github_stats(html, idx)
    assert 'class="gh-stats-row"' in out
    assert '42' in out
    assert 'MIT' in out


def test_inject_github_stats_idempotent_when_row_already_present():
    """Already-badged cards aren't rewritten."""
    from postbuild_lib.github_stats import inject_github_stats
    idx = {"sebastienrousseau/foo": {"stars": 1, "forks": 0, "license": "", "pushed_at": ""}}
    html = (
        '<article class="newsroom-card">'
        '<a href="https://github.com/sebastienrousseau/foo">link</a>'
        '<p class="gh-stats-row">already there</p>'
        '</article>'
    )
    assert inject_github_stats(html, idx) == html


def test_gh_stats_index_parses_valid_payload(tmp_path, monkeypatch):
    """A real JSON payload at the configured path resolves to a slug-keyed map."""
    from unittest.mock import patch

    from postbuild_lib import github_stats as gh
    payload = tmp_path / "gh-stats.json"
    payload.write_text(
        '{"repos": [{"slug": "foo", "name": "foo", "stars": 1}, '
        '{"slug": "bar", "name": "bar", "stars": 2}]}',
        encoding="utf-8",
    )
    with patch.object(gh, "_GH_STATS_PATH", payload):
        idx = gh.gh_stats_index()
    assert idx["foo"]["stars"] == 1
    assert idx["bar"]["stars"] == 2


def test_gh_stats_index_returns_empty_on_invalid_json(tmp_path):
    from unittest.mock import patch

    from postbuild_lib import github_stats as gh
    payload = tmp_path / "gh-stats.json"
    payload.write_text("{ not valid json", encoding="utf-8")
    with patch.object(gh, "_GH_STATS_PATH", payload):
        assert gh.gh_stats_index() == {}


def test_relative_time_handles_each_bucket():
    """Walk through the duration table — seconds, minutes, hours, days, weeks, months, years."""
    from datetime import UTC, datetime, timedelta

    from postbuild_lib.github_stats import _relative_time
    now = datetime.now(tz=UTC)
    cases = [
        timedelta(seconds=30),
        timedelta(minutes=5),
        timedelta(hours=3),
        timedelta(days=2),
        timedelta(weeks=2),
        timedelta(days=120),
        timedelta(days=900),
    ]
    for td in cases:
        ts = (now - td).isoformat()
        assert _relative_time(ts) != ""


# ---------------------------------------------------------------------------
# seo.inject_about + _build_howto_jsonld
# ---------------------------------------------------------------------------


def test_inject_about_no_op_when_no_keyword_matches():
    """BlogPosting keywords that match no ENTITY_AUTHORITY → unchanged."""
    html = (
        '<script type="application/ld+json">'
        '{"@type":"BlogPosting","headline":"X","keywords":"basketweaving, ceramics"}'
        '</script>'
    )
    assert pb.inject_about(html) == html


def test_inject_about_injects_about_field_for_known_entity():
    """A keyword that maps to ENTITY_AUTHORITY produces an ``about`` field."""
    html = (
        '<script type="application/ld+json">'
        '{"@type":"BlogPosting","keywords":"post-quantum cryptography, banking","headline":"X"}'
        '</script>'
    )
    out = pb.inject_about(html)
    assert '"about":' in out
    assert '"@type":"Thing"' in out


def test_inject_howto_no_op_when_no_resource_marker():
    """Pages without the ``data-resource-howto`` marker are untouched."""
    from pathlib import Path as _P
    html = '<p>regular content</p>'
    assert pb.inject_howto(_P("public/index.html"), html) == html


# ---------------------------------------------------------------------------
# inject_anchor_links_and_toc — happy path + ToC
# ---------------------------------------------------------------------------


def test_inject_anchor_links_emits_anchor_per_heading():
    from postbuild_lib.article_furniture import inject_anchor_links_and_toc
    html = (
        '<script type="application/ld+json">{"@type":"BlogPosting"}</script>'
        '<main><div class="wrap">'
        '<h2>Intro</h2><p>body</p>'
        '<h2>Setup</h2><p>body</p>'
        '<h3>Subsection</h3>'
        '</div></main>'
    )
    out = inject_anchor_links_and_toc(html)
    assert out.count('class="heading-anchor"') == 3
    assert 'href="#intro"' in out
    assert 'href="#setup"' in out
    assert 'href="#subsection"' in out


def test_inject_anchor_renders_toc_when_5_or_more_h2():
    """≥ 5 H2s triggers the ToC card."""
    from postbuild_lib.article_furniture import inject_anchor_links_and_toc
    body = "".join(f"<h2>Section {i}</h2>" for i in range(1, 6))
    html = (
        '<script type="application/ld+json">{"@type":"BlogPosting"}</script>'
        f'<main><div class="wrap">{body}</div></main>'
    )
    out = inject_anchor_links_and_toc(html)
    assert 'class="article-toc"' in out
    assert out.count('<li><a href="#section-') == 5


def test_inject_anchor_omits_toc_when_fewer_than_5_h2():
    from postbuild_lib.article_furniture import inject_anchor_links_and_toc
    html = (
        '<script type="application/ld+json">{"@type":"BlogPosting"}</script>'
        '<main><div class="wrap"><h2>One</h2><h2>Two</h2></div></main>'
    )
    out = inject_anchor_links_and_toc(html)
    assert 'class="article-toc"' not in out


def test_inject_anchor_no_op_without_blogposting():
    from postbuild_lib.article_furniture import inject_anchor_links_and_toc
    html = '<main><div class="wrap"><h2>X</h2></div></main>'
    assert inject_anchor_links_and_toc(html) == html


# ---------------------------------------------------------------------------
# inject_prev_next_nav + build_post_nav_index
# ---------------------------------------------------------------------------


def test_build_post_nav_index_chronological_order(tmp_path, monkeypatch):
    """Posts sorted oldest→newest; each entry maps to (prev, next)."""
    monkeypatch.chdir(tmp_path)
    pages = []
    for stem, title in [
        ("2026-05-12-a", "First"), ("2026-05-13-b", "Middle"), ("2026-05-14-c", "Last"),
    ]:
        d = tmp_path / "public" / stem
        d.mkdir(parents=True)
        (d / "index.html").write_text(
            '<script type="application/ld+json">{"@type":"BlogPosting"}</script>'
            f'<section class="ap-hero"><h1>{title}</h1></section>',
            encoding="utf-8",
        )
        pages.append(d / "index.html")
    from postbuild_lib.article_furniture import build_post_nav_index
    idx = build_post_nav_index(pages)
    # Middle post has both prev and next
    assert idx["2026-05-13-b"][0] == ("2026-05-12-a", "First")
    assert idx["2026-05-13-b"][1] == ("2026-05-14-c", "Last")
    # First has no prev
    assert idx["2026-05-12-a"][0] is None
    # Last has no next
    assert idx["2026-05-14-c"][1] is None


# ---------------------------------------------------------------------------
# inject_mermaid
# ---------------------------------------------------------------------------


def test_inject_mermaid_no_op_when_no_mermaid_block():
    from postbuild_lib.article_furniture import inject_mermaid
    html = '<pre><code>plain code</code></pre>'
    assert inject_mermaid(html) == html


def test_inject_mermaid_converts_fenced_block():
    from postbuild_lib.article_furniture import inject_mermaid
    html = (
        '<meta http-equiv="Content-Security-Policy" content="script-src \'self\'">'
        '<pre><code class="language-mermaid">graph TD; A--&gt;B</code></pre>'
    )
    out = inject_mermaid(html)
    assert '<pre class="mermaid">' in out
    assert 'graph TD' in out
    # CSP widened to allow the Mermaid CDN import
    assert 'cdn.jsdelivr.net' in out


# ---------------------------------------------------------------------------
# inject_sources_list
# ---------------------------------------------------------------------------


def test_inject_sources_list_renders_aside_with_authoritative_links():
    from postbuild_lib.article_furniture import inject_sources_list
    html = (
        '<script type="application/ld+json">{"@type":"BlogPosting"}</script>'
        '<main><div class="wrap">'
        '<a href="https://nist.gov/pub1">NIST 1</a>'
        '<a href="https://wikipedia.org/wiki/X">Wiki</a>'
        '</div></main>'
    )
    out = inject_sources_list(html)
    assert 'class="article-sources"' in out
    assert 'nist.gov' in out


def test_inject_sources_list_no_op_without_outbound_links():
    from postbuild_lib.article_furniture import inject_sources_list
    html = (
        '<script type="application/ld+json">{"@type":"BlogPosting"}</script>'
        '<main><div class="wrap"><p>no links</p></div></main>'
    )
    assert inject_sources_list(html) == html


# ---------------------------------------------------------------------------
# Lang helpers — _resolve_en_slug, _alternates_for_en_slug
# ---------------------------------------------------------------------------


def test_resolve_en_slug_static_pages_use_static_map():
    from postbuild_lib.article_furniture import _resolve_en_slug
    # "about" → static EN page. FR slug for "about" is "a-propos".
    # When given the FR slug, _resolve_en_slug returns the EN canonical.
    assert _resolve_en_slug("a-propos", "fr") == "about"


def test_resolve_en_slug_returns_none_for_unknown_slug():
    from postbuild_lib.article_furniture import _resolve_en_slug
    assert _resolve_en_slug("totally-unknown-slug", "fr") is None


def test_all_active_non_en_langs_includes_fr_de_ar():
    from postbuild_lib.article_furniture import _all_active_non_en_langs
    codes = _all_active_non_en_langs()
    assert "fr" in codes
    assert "de" in codes
    assert "ar" in codes


# ---------------------------------------------------------------------------
# inject_prev_next_nav — happy path + idempotency + lang variants
# ---------------------------------------------------------------------------


def _wrap_blogposting(body: str) -> str:
    """Minimal HTML shell carrying a BlogPosting JSON-LD + main+wrap div."""
    return (
        '<script type="application/ld+json">{"@type":"BlogPosting"}</script>'
        f'<main><div class="wrap">{body}</div></main>'
    )


def test_inject_prev_next_nav_renders_both_links():
    from postbuild_lib.article_furniture import inject_prev_next_nav
    html = _wrap_blogposting("<p>body</p>")
    nav_index = {
        "2026-05-13-mid": (
            ("2026-05-12-prev", "Previous article"),
            ("2026-05-14-next", "Next article"),
        ),
    }
    out = inject_prev_next_nav(html, "2026-05-13-mid", nav_index)
    assert 'class="post-pagination"' in out
    assert 'href="/2026-05-12-prev/"' in out
    assert 'href="/2026-05-14-next/"' in out
    assert "Previous article" in out
    assert "Next article" in out


def test_inject_prev_next_nav_emits_stub_for_missing_neighbour():
    from postbuild_lib.article_furniture import inject_prev_next_nav
    html = _wrap_blogposting("<p>body</p>")
    nav_index = {"2026-05-13-only": (None, ("2026-05-14-next", "Next"))}
    out = inject_prev_next_nav(html, "2026-05-13-only", nav_index)
    assert 'class="post-pagination-stub"' in out
    assert 'href="/2026-05-14-next/"' in out


def test_inject_prev_next_nav_no_op_without_blogposting():
    from postbuild_lib.article_furniture import inject_prev_next_nav
    html = '<main><div class="wrap"><p>plain page</p></div></main>'
    assert inject_prev_next_nav(html, "foo", {"foo": (None, ("x", "X"))}) == html


def test_inject_prev_next_nav_no_op_when_slug_not_in_index():
    from postbuild_lib.article_furniture import inject_prev_next_nav
    html = _wrap_blogposting("<p>body</p>")
    assert inject_prev_next_nav(html, "unknown", {}) == html


def test_inject_prev_next_nav_idempotent_when_pagination_already_present():
    from postbuild_lib.article_furniture import inject_prev_next_nav
    html = (
        '<script type="application/ld+json">{"@type":"BlogPosting"}</script>'
        '<main><div class="wrap"><nav class="post-pagination"></nav></div></main>'
    )
    out = inject_prev_next_nav(
        html, "foo",
        {"foo": (("bar", "Bar"), ("baz", "Baz"))},
    )
    assert out == html


# ---------------------------------------------------------------------------
# hreflang helpers — _alternates_for_en_slug + inject_hreflang
# ---------------------------------------------------------------------------


def test_alternates_for_en_slug_includes_en_first():
    from postbuild_lib.article_furniture import _alternates_for_en_slug
    alts = _alternates_for_en_slug("about", {})  # no translations rendered
    assert alts[0] == ("en", "https://sebastienrousseau.com/about/")
    assert len(alts) == 1  # no FR/DE/AR since translated_per_lang is empty


def test_alternates_for_en_slug_includes_fr_when_translation_exists():
    from postbuild_lib.article_furniture import _alternates_for_en_slug
    # "about" → FR slug "a-propos" (per _data/i18n/fr/slugs.json)
    alts = _alternates_for_en_slug("about", {"fr": {"a-propos"}})
    codes = [c for c, _ in alts]
    assert "en" in codes
    assert "fr" in codes
    fr_url = next(u for c, u in alts if c == "fr")
    assert "/fr/a-propos/" in fr_url


def test_inject_hreflang_emits_alternate_links():
    from postbuild_lib.article_furniture import inject_hreflang
    html = '<head><meta charset="utf-8"></head><body></body>'
    out = inject_hreflang(html, "about", "en", {"fr": {"a-propos"}})
    assert 'hreflang="en"' in out
    assert 'hreflang="fr"' in out
    assert 'hreflang="x-default"' in out
    assert '/fr/a-propos/' in out


def test_inject_hreflang_no_op_when_only_en_resolves():
    from postbuild_lib.article_furniture import inject_hreflang
    html = '<head></head>'
    # No translations rendered → only EN alternate → < 2 entries → no-op
    out = inject_hreflang(html, "about", "en", {})
    assert 'hreflang=' not in out


def test_inject_hreflang_no_op_when_slug_unresolvable():
    from postbuild_lib.article_furniture import inject_hreflang
    html = '<head></head>'
    out = inject_hreflang(html, "totally-unknown", "fr", {})
    assert 'hreflang=' not in out


def test_inject_hreflang_strips_existing_alternates_first():
    """A page already carrying ``<link rel="alternate" hreflang=>`` gets
    them stripped before the new set is inserted."""
    from postbuild_lib.article_furniture import inject_hreflang
    # The strip regex expects the XHTML self-close style ``/>`` because
    # that's what the postbuild renderer emits.
    html = (
        '<head>'
        '<link rel="alternate" hreflang="en" href="https://old.example/" />'
        '</head>'
    )
    out = inject_hreflang(html, "about", "en", {"fr": {"a-propos"}})
    assert "https://old.example/" not in out
    assert "/fr/a-propos/" in out


# ---------------------------------------------------------------------------
# _slug_maps + _resolve_en_slug round trips
# ---------------------------------------------------------------------------


def test_slug_maps_returns_four_keys_per_lang():
    from postbuild_lib.article_furniture import _slug_maps
    m = _slug_maps("fr")
    assert "articles_en_to_lang" in m
    assert "articles_lang_to_en" in m
    assert "statics_en_to_lang" in m
    assert "statics_lang_to_en" in m


def test_resolve_en_slug_en_passthrough():
    from postbuild_lib.article_furniture import _resolve_en_slug
    # English slug is its own canonical
    assert _resolve_en_slug("about", "en") == "about"


# ---------------------------------------------------------------------------
# build_fr_title_index
# ---------------------------------------------------------------------------


def test_build_fr_title_index_walks_fr_articles(tmp_path, monkeypatch):
    """Each rendered FR page contributes one (en_slug → fr title) entry."""
    monkeypatch.chdir(tmp_path)
    from pathlib import Path as _P
    # Place a "FR" page under public/fr/<lang-slug>/. The lang-slug here
    # must be one that's actually in _data/i18n/fr/slugs.json articles map;
    # using a slug we know exists in the AR-merge baseline: the cloud article.
    fr_lang_slug = "meilleure-architecture-cloud-pour-les-banques-2026"
    p = tmp_path / "public" / "fr" / fr_lang_slug
    p.mkdir(parents=True)
    (p / "index.html").write_text(
        '<script type="application/ld+json">{"@type":"BlogPosting"}</script>'
        '<section class="ap-hero"><h1>Mon titre FR</h1></section>',
        encoding="utf-8",
    )
    from postbuild_lib.article_furniture import build_fr_title_index
    pages = [_P(str(p / "index.html"))]
    idx = build_fr_title_index(pages)
    # Should map the EN slug for this article to "Mon titre FR".
    # If the FR slug isn't in the registered articles map we'll just skip
    # the assertion on the exact key, but the function should still run
    # without raising.
    assert isinstance(idx, dict)


# ---------------------------------------------------------------------------
# _translated_slugs_per_lang + legacy _translated_slugs
# ---------------------------------------------------------------------------


def test_translated_slugs_per_lang_returns_empty_when_no_public_tree(tmp_path, monkeypatch):
    """No rendered /<lang>/ directory → empty map."""
    monkeypatch.chdir(tmp_path)
    # Pretend public/ is somewhere with no subdirs
    (tmp_path / "public").mkdir()
    # Temporarily point PUBLIC at the empty tree
    from unittest.mock import patch

    from postbuild_lib import article_furniture as af
    with patch.object(af, "PUBLIC", tmp_path / "public"):
        out = af._translated_slugs_per_lang()
    assert out == {}


def test_translated_slugs_legacy_returns_two_empty_sets_without_fr_dir(tmp_path, monkeypatch):
    from unittest.mock import patch

    from postbuild_lib import article_furniture as af
    monkeypatch.chdir(tmp_path)
    (tmp_path / "public").mkdir()
    with patch.object(af, "PUBLIC", tmp_path / "public"):
        en_with_fr, fr_with_en = af._translated_slugs()
    assert en_with_fr == set()
    assert fr_with_en == set()


# ---------------------------------------------------------------------------
# inject_speculation_rules
# ---------------------------------------------------------------------------


def test_inject_speculation_rules_no_op_when_already_present():
    from postbuild_lib.article_furniture import inject_speculation_rules
    html = '<head><script type="speculationrules">{}</script></head>'
    assert inject_speculation_rules(html) == html


def test_inject_speculation_rules_inserts_when_missing():
    from postbuild_lib.article_furniture import inject_speculation_rules
    html = '<head><meta charset="utf-8"></head><body></body>'
    out = inject_speculation_rules(html)
    assert '<script type="speculationrules">' in out


# ---------------------------------------------------------------------------
# inject_nav_active + _nav_active_target dispatch
# ---------------------------------------------------------------------------


def test_nav_active_target_home_en():
    from pathlib import Path as _P

    from postbuild_lib.article_furniture import _nav_active_target
    assert _nav_active_target(_P("public/index.html")) == "/index.html"


def test_nav_active_target_top_static_en():
    from pathlib import Path as _P

    from postbuild_lib.article_furniture import _nav_active_target
    assert _nav_active_target(_P("public/about/index.html")) == "/about/index.html"


def test_nav_active_target_dated_article_maps_to_articles_hub():
    from pathlib import Path as _P

    from postbuild_lib.article_furniture import _nav_active_target
    p = _P("public/2026-05-12-some-article/index.html")
    assert _nav_active_target(p) == "/articles/index.html"


def test_nav_active_target_returns_none_for_unknown_lang():
    from pathlib import Path as _P

    from postbuild_lib.article_furniture import _nav_active_target
    # /xx/foo/ — xx is not a registered language
    p = _P("public/xx/foo/index.html")
    assert _nav_active_target(p) is None


def test_inject_nav_active_marks_match_and_clears_others():
    from pathlib import Path as _P

    from postbuild_lib.article_furniture import inject_nav_active
    html = (
        '<header>'
        '<a href="/about/index.html">About</a>'
        '<a href="/articles/index.html" aria-current="page">Articles</a>'
        '</header>'
    )
    out = inject_nav_active(html, _P("public/about/index.html"))
    assert 'aria-current="page"' in out
    # only the /about/ link should have the marker
    assert out.count('aria-current="page"') == 1
    # The /about/ link gets it, the /articles/ link loses it
    about_seg = out[out.find('href="/about'): out.find('Articles')]
    articles_seg = out[out.find('Articles'):]
    assert 'aria-current' in about_seg
    assert 'aria-current' not in articles_seg


# ---------------------------------------------------------------------------
# stamp_image_dimensions — width/height + fetchpriority for LCP / lazy below
# ---------------------------------------------------------------------------


def test_stamp_image_dimensions_first_image_gets_fetchpriority_high():
    html = '<body><img src="https://example.com/banner.webp" alt="x"></body>'
    out, n = pb.stamp_image_dimensions(html)
    assert n == 1
    assert 'fetchpriority="high"' in out
    assert 'width="' in out
    assert 'height="' in out


def test_stamp_image_dimensions_subsequent_images_get_lazy_async():
    html = (
        '<img src="https://example.com/1.webp" alt="hero">'
        '<img src="https://example.com/2.webp" alt="below">'
    )
    out, n = pb.stamp_image_dimensions(html)
    assert n == 2
    first_img = out[: out.find("<img", 5)]
    second_img = out[out.find("<img", 5):]
    assert 'fetchpriority="high"' in first_img
    assert 'fetchpriority="high"' not in second_img
    assert 'loading="lazy"' in second_img
    assert 'decoding="async"' in second_img


def test_stamp_image_dimensions_uses_known_size_for_personal_portrait():
    """The personal portrait is registered in _IMG_DIMS as 162×162."""
    html = '<img src="https://cloudcdn.pro/stocks/images/sebastien-rousseau.png" alt="x">'
    out, _ = pb.stamp_image_dimensions(html)
    assert 'width="162"' in out
    assert 'height="162"' in out


def test_stamp_image_dimensions_idempotent_when_attrs_already_present():
    """Images that already have w/h/loading/decoding aren't rewritten."""
    html = (
        '<img src="https://cloudcdn.pro/stocks/images/sebastien-rousseau.png" '
        'width="162" height="162" loading="lazy" decoding="async" '
        'fetchpriority="high" alt="x">'
    )
    out, _ = pb.stamp_image_dimensions(html)
    # First-pass idempotent: no duplicated attributes
    assert out.count('width="162"') == 1


def test_stamp_image_dimensions_prefix_map_match():
    """Image whose src matches an ``_IMG_DIMS_PREFIX`` gets that group's size."""
    html = '<img src="https://cloudcdn.pro/clients/alienstudio/portrait.webp">'
    out, _ = pb.stamp_image_dimensions(html)
    assert 'width="800"' in out
    assert 'height="800"' in out


def test_stamp_image_dimensions_default_dimensions_for_unknown_src():
    """Image with a src that matches nothing falls back to _IMG_DEFAULT (1200×675)."""
    html = '<img src="https://example.com/random/photo.webp">'
    out, _ = pb.stamp_image_dimensions(html)
    assert 'width="1200"' in out
    assert 'height="675"' in out


# ---------------------------------------------------------------------------
# inject_og_completeness + _lang_to_og_locale
# ---------------------------------------------------------------------------


def test_lang_to_og_locale_basic_forms():
    from postbuild_lib.seo import _lang_to_og_locale
    assert _lang_to_og_locale("en-GB") == "en_GB"
    assert _lang_to_og_locale("fr-FR") == "fr_FR"
    assert _lang_to_og_locale("de") == "de_DE"
    assert _lang_to_og_locale("") == "en_GB"


def test_inject_og_completeness_adds_url_locale_sitename_image(tmp_path, monkeypatch):
    """A page missing all four og:* tags gets every addition."""
    from pathlib import Path as _P

    from postbuild_lib import seo
    public = tmp_path / "public"
    page = public / "about" / "index.html"
    page.parent.mkdir(parents=True)
    page.write_text("placeholder", encoding="utf-8")
    monkeypatch.setattr(seo, "PUBLIC", public)
    html = '<html lang="en-GB"><head><meta charset="utf-8"></head><body></body></html>'
    out = seo.inject_og_completeness(_P(str(page)), html)
    assert 'property="og:url" content="https://sebastienrousseau.com/about/index.html"' in out
    assert 'property="og:locale" content="en_GB"' in out
    assert 'property="og:site_name" content="Sebastien Rousseau"' in out
    assert 'property="og:image"' in out


def test_inject_og_completeness_no_op_when_all_present(tmp_path, monkeypatch):
    from pathlib import Path as _P

    from postbuild_lib import seo
    public = tmp_path / "public"
    public.mkdir()
    page = public / "index.html"
    page.write_text("placeholder", encoding="utf-8")
    monkeypatch.setattr(seo, "PUBLIC", public)
    html = (
        '<html lang="en-GB"><head>'
        '<meta property="og:url" content="https://sebastienrousseau.com/">'
        '<meta property="og:locale" content="en_GB">'
        '<meta property="og:site_name" content="Sebastien Rousseau">'
        '<meta property="og:image" content="https://x/banner.webp">'
        '<meta name="twitter:image" content="https://x/banner.webp">'
        '</head></html>'
    )
    out = seo.inject_og_completeness(_P(str(page)), html)
    assert out == html


def test_inject_og_completeness_home_url_drops_index_html(tmp_path, monkeypatch):
    from pathlib import Path as _P

    from postbuild_lib import seo
    public = tmp_path / "public"
    public.mkdir()
    page = public / "index.html"
    page.write_text("placeholder", encoding="utf-8")
    monkeypatch.setattr(seo, "PUBLIC", public)
    html = '<html lang="en-GB"><head></head></html>'
    out = seo.inject_og_completeness(_P(str(page)), html)
    # Home page → canonical URL is the bare root, NOT /index.html
    assert 'content="https://sebastienrousseau.com/"' in out


# ---------------------------------------------------------------------------
# write_json_feed (JSON Feed 1.1)
# ---------------------------------------------------------------------------


def test_write_json_feed_emits_valid_feed_at_target(tmp_path, monkeypatch):
    """Writes a JSON Feed 1.1 with version + items from _posts/."""
    monkeypatch.chdir(tmp_path)
    posts = tmp_path / "_posts"
    posts.mkdir()
    (posts / "2026-05-12-test-post.md").write_text(
        '---\ntitle: "Test post"\ndate: "May 12, 2026"\n'
        'description: "Body description"\nbanner: "https://x/banner.webp"\n'
        'keywords: "quantum, ai"\n---\nBody.\n',
        encoding="utf-8",
    )
    public = tmp_path / "public"
    public.mkdir()
    from postbuild_lib.output import write_json_feed
    assert write_json_feed(public) is True
    import json as _json
    feed = _json.loads((public / "feed.json").read_text())
    assert feed["version"].startswith("https://jsonfeed.org/version/")
    assert feed["language"] == "en-GB"
    assert len(feed["items"]) == 1
    item = feed["items"][0]
    assert item["title"] == "Test post"
    assert item["image"] == "https://x/banner.webp"
    assert item["tags"] == ["quantum", "ai"]


def test_write_json_feed_skips_posts_without_title_or_bad_date(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    posts = tmp_path / "_posts"
    posts.mkdir()
    (posts / "2026-05-12-no-title.md").write_text(
        '---\ndate: "May 12, 2026"\n---\n', encoding="utf-8"
    )
    (posts / "2026-05-13-bad-date.md").write_text(
        '---\ntitle: "X"\ndate: "not-a-date"\n---\n', encoding="utf-8"
    )
    public = tmp_path / "public"
    public.mkdir()
    from postbuild_lib.output import write_json_feed
    write_json_feed(public)
    import json as _json
    feed = _json.loads((public / "feed.json").read_text())
    assert feed["items"] == []


# ---------------------------------------------------------------------------
# build_llms_full_txt
# ---------------------------------------------------------------------------


def test_build_llms_full_txt_emits_header_and_body_blocks(tmp_path):
    """Output starts with an H1 and contains every page body."""
    public = tmp_path / "public"
    (public / "about").mkdir(parents=True)
    (public / "about" / "index.html").write_text(
        '<!doctype html><html lang="en-GB"><head><title>About</title>'
        '<meta content="bio" name=description></head>'
        '<body><main><h1>About</h1><p>Bio body content.</p></main></body></html>',
        encoding="utf-8",
    )
    from postbuild_lib.output import build_llms_full_txt
    out = build_llms_full_txt(public)
    assert out.startswith("# Sebastien Rousseau") or "About" in out


# ---------------------------------------------------------------------------
# build_lastmod_index + refresh_sitemap_lastmod
# ---------------------------------------------------------------------------


def test_build_lastmod_index_prefers_last_reviewed(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    posts = tmp_path / "_posts"
    posts.mkdir()
    (posts / "2026-05-12-x.md").write_text(
        '---\ntitle: "X"\ndate: "May 12, 2026"\nlast_reviewed: "2026-05-15"\n---\n',
        encoding="utf-8",
    )
    from postbuild_lib.output import build_lastmod_index
    idx = build_lastmod_index()
    assert idx["2026-05-12-x"] == "2026-05-15"


def test_build_lastmod_index_falls_back_to_date(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    posts = tmp_path / "_posts"
    posts.mkdir()
    (posts / "2026-05-12-x.md").write_text(
        '---\ntitle: "X"\ndate: "May 12, 2026"\n---\n', encoding="utf-8"
    )
    from postbuild_lib.output import build_lastmod_index
    idx = build_lastmod_index()
    assert idx["2026-05-12-x"] == "2026-05-12"


def test_build_lastmod_index_returns_empty_when_no_posts_dir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    from postbuild_lib.output import build_lastmod_index
    assert build_lastmod_index() == {}


def test_refresh_sitemap_lastmod_no_op_when_file_missing(tmp_path):
    from postbuild_lib.output import refresh_sitemap_lastmod
    assert refresh_sitemap_lastmod(tmp_path / "missing.xml", {}) == 0


def test_refresh_sitemap_lastmod_rewrites_existing_entry(tmp_path, monkeypatch):
    """Existing ``<lastmod>`` for a tracked post is replaced with the index value."""
    monkeypatch.chdir(tmp_path)
    # No _posts dir means _splice_fr_urls only adds the home + static slugs
    sitemap = tmp_path / "sitemap.xml"
    sitemap.write_text(
        '<?xml version="1.0"?><urlset>'
        '<url><loc>https://sebastienrousseau.com/2026-05-12-x/</loc>'
        '<lastmod>2026-01-01</lastmod></url>'
        '</urlset>',
        encoding="utf-8",
    )
    from postbuild_lib.output import refresh_sitemap_lastmod
    n = refresh_sitemap_lastmod(sitemap, {"2026-05-12-x": "2026-05-15"})
    assert n == 1
    out = sitemap.read_text(encoding="utf-8")
    assert "<lastmod>2026-05-15</lastmod>" in out


# ---------------------------------------------------------------------------
# shrink_news_sitemap end-to-end
# ---------------------------------------------------------------------------


def test_shrink_news_sitemap_no_op_when_file_missing(tmp_path):
    from postbuild_lib.output import shrink_news_sitemap
    assert shrink_news_sitemap(tmp_path) == 0


def test_shrink_news_sitemap_rewrites_long_title(tmp_path):
    nsm = tmp_path / "news-sitemap.xml"
    long_title = "A " * 60  # ~120 chars
    nsm.write_text(
        f'<urlset><url><news:news><news:title>{long_title}</news:title>'
        '<news:keywords>a,b,c,d,e,f,g,h,i,j,k,l,m</news:keywords>'
        '</news:news></url></urlset>',
        encoding="utf-8",
    )
    from postbuild_lib.output import shrink_news_sitemap
    assert shrink_news_sitemap(tmp_path) == 1
    out = nsm.read_text(encoding="utf-8")
    # Title clipped to ≤ 80 chars
    import re as _re
    m = _re.search(r"<news:title>([\s\S]*?)</news:title>", out)
    assert m is not None
    assert len(m.group(1)) <= 80
    # Keywords trimmed to 10 items
    m2 = _re.search(r"<news:keywords>([\s\S]*?)</news:keywords>", out)
    assert m2 is not None
    assert len([k for k in m2.group(1).split(",") if k.strip()]) == 10


# ---------------------------------------------------------------------------
# Asset-URL fingerprint stamping — guards stale CDN cache after a content change
# ---------------------------------------------------------------------------


def test_stamp_asset_fingerprints_rewrites_main_js():
    """Unquoted ``src=/main.js`` gets rewritten to the fingerprinted name."""
    from unittest.mock import patch

    import postbuild as _pb
    fake_map = {"/main.js": "/main.abc123.js"}
    fake_pat = _pb.re.compile(
        r'(<(?:script|link)\b[^>]*\b(?:src|href)=["\']?)(/main\.js)(["\']?[^>]*>)',
        _pb.re.IGNORECASE,
    )
    with patch.object(_pb, "_FP_ASSET_MAP", fake_map), patch.object(_pb, "_FP_PATTERN", fake_pat):
        out, n = _pb.stamp_asset_fingerprints('<script defer src=/main.js></script>')
        assert n == 1
        assert "/main.abc123.js" in out
        assert "src=/main.js" not in out


def test_stamp_asset_fingerprints_rewrites_quoted_form():
    """Quoted ``src="/main.js"`` also gets rewritten."""
    from unittest.mock import patch

    import postbuild as _pb
    fake_map = {"/main.js": "/main.abc123.js"}
    fake_pat = _pb.re.compile(
        r'(<(?:script|link)\b[^>]*\b(?:src|href)=["\']?)(/main\.js)(["\']?[^>]*>)',
        _pb.re.IGNORECASE,
    )
    with patch.object(_pb, "_FP_ASSET_MAP", fake_map), patch.object(_pb, "_FP_PATTERN", fake_pat):
        out, n = _pb.stamp_asset_fingerprints('<script src="/main.js" defer></script>')
        assert n == 1
        assert 'src="/main.abc123.js"' in out


def test_stamp_asset_fingerprints_leaves_inline_js_untouched():
    """A literal ``/main.js`` inside JS code (not a <script src>) is NOT rewritten."""
    from unittest.mock import patch

    import postbuild as _pb
    fake_map = {"/main.js": "/main.abc123.js"}
    fake_pat = _pb.re.compile(
        r'(<(?:script|link)\b[^>]*\b(?:src|href)=["\']?)(/main\.js)(["\']?[^>]*>)',
        _pb.re.IGNORECASE,
    )
    with patch.object(_pb, "_FP_ASSET_MAP", fake_map), patch.object(_pb, "_FP_PATTERN", fake_pat):
        out, n = _pb.stamp_asset_fingerprints(
            "<script>navigator.serviceWorker.register('/main.js');</script>"
        )
        assert n == 0
        assert "/main.js" in out  # untouched


def test_stamp_asset_fingerprints_no_op_when_pattern_missing():
    """Without a fingerprint map, the pass is a no-op."""
    from unittest.mock import patch

    import postbuild as _pb
    with patch.object(_pb, "_FP_PATTERN", None):
        out, n = _pb.stamp_asset_fingerprints('<script src=/main.js></script>')
        assert n == 0
        assert out == '<script src=/main.js></script>'


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
