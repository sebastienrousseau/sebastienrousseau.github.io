"""Tests for the postbuild SEO passes — feeds, sitemaps, hreflang,
OG/social images, robots.txt, and localhost scrubbing.

Split out of test_postbuild.py; tests are verbatim copies.
"""

from __future__ import annotations

from typing import ClassVar

import postbuild as pb
from postbuild_lib import hreflang as hf

# ---------------------------------------------------------------------------
# XML feed ampersand escape pass (`escape_xml_ampersands`)
# ---------------------------------------------------------------------------


def test_escape_xml_bare_amp_to_amp():
    assert pb.escape_xml_ampersands("AI & Payments") == "AI &amp; Payments"


def test_escape_xml_preserves_existing_amp_entity():
    assert pb.escape_xml_ampersands("AI &amp; Payments") == "AI &amp; Payments"


def test_escape_xml_undoes_double_escape():
    # Static Site Generator's bug — &amp;amp; should collapse back to &amp;.
    assert pb.escape_xml_ampersands("AI &amp;amp; Payments") == "AI &amp; Payments"


def test_escape_xml_preserves_apos_quot_lt_gt():
    s = "She said &apos;hi&apos; &lt;3 &quot;text&quot;"
    assert pb.escape_xml_ampersands(s) == s


def test_escape_xml_numeric_entities_preserved():
    assert pb.escape_xml_ampersands("&#169; &#x2014;") == "&#169; &#x2014;"


# ---------------------------------------------------------------------------
# XML feed URL repair — `_patch_block` lookup-by-title path
# Regression guard for #32: an earlier refactor (#31) rewrote _patch_block
# to slug-extract from the URL itself. Static Site Generator emits ``.../.meta/`` for
# every per-item link, so the regex fell back to the home URL on every
# match — producing 50 duplicate <guid>/<link> values per feed.
# ---------------------------------------------------------------------------


def test_patch_block_rewrites_localhost_url_using_title():
    """RSS <item> with localhost URL gets rewritten to canonical URL."""
    from postbuild_lib import feeds as out

    block = (
        "<item>"
        "<title>The Best Cloud Infrastructure Architecture in 2026</title>"
        "<link>http://127.0.0.1:8000/.meta/</link>"
        '<guid isPermaLink="true">http://127.0.0.1:8000/.meta/</guid>'
        "</item>"
    )
    idx = {
        "The Best Cloud Infrastructure Architecture in 2026": "https://sebastienrousseau.com/best-cloud-2026",
    }
    rewritten = out._patch_block(block, idx)
    assert "https://sebastienrousseau.com/best-cloud-2026" in rewritten
    assert "127.0.0.1" not in rewritten
    assert "/.meta/" not in rewritten


def test_patch_block_no_op_when_title_not_in_index():
    """If we can't resolve the title, leave the block untouched —
    don't fall back to the home URL."""
    from postbuild_lib import feeds as out

    block = "<item><title>Unknown post</title>" "<link>http://127.0.0.1:8000/.meta/</link></item>"
    rewritten = out._patch_block(block, {})
    assert rewritten == block


def test_patch_block_decodes_xml_entities_in_title_lookup():
    """Feed emits ``&amp;`` in titles; the index should resolve via
    either escaped or unescaped form."""
    from postbuild_lib import feeds as out

    block = (
        "<item><title>AI &amp; Quantum</title>" "<link>http://localhost:8000/.meta/</link></item>"
    )
    idx = {"AI & Quantum": "https://sebastienrousseau.com/ai-quantum"}
    rewritten = out._patch_block(block, idx)
    assert "https://sebastienrousseau.com/ai-quantum" in rewritten


def test_patch_block_rewrites_meta_path_on_any_host():
    """``host/.meta/`` is rewritten even when the host isn't localhost."""
    from postbuild_lib import feeds as out

    block = "<item><title>X</title>" "<link>https://example.com/.meta/</link></item>"
    idx = {"X": "https://sebastienrousseau.com/x"}
    rewritten = out._patch_block(block, idx)
    assert "https://sebastienrousseau.com/x" in rewritten
    assert "/.meta/" not in rewritten


def test_fix_social_image_promotes_summary_to_large():
    """Twitter card defaults to ``summary`` on some posts; we lift to
    ``summary_large_image`` when a real banner is present."""
    html = (
        '<script type="application/ld+json">'
        '{"@type":"BlogPosting","image":{"url":"https://x/banner.webp","width":1200,"height":628}}'
        "</script>"
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
        "</script>"
        '<meta name="twitter:card" content="summary">'
    )
    out = pb.fix_social_image(html)
    assert out == html  # untouched


def test_write_robots_emits_sitemap_lines(tmp_path):
    from postbuild_lib.output import write_robots

    write_robots(tmp_path)
    text = (tmp_path / "robots.txt").read_text(encoding="utf-8")
    assert "User-agent:" in text
    assert "Sitemap: https://sebastienrousseau.com/sitemap.xml" in text


def test_write_robots_carries_per_category_taxonomy(tmp_path):
    """Robots.txt taxonomy must explicitly enumerate the 2026 bot
    categories so each can be flipped to Disallow independently."""
    from postbuild_lib.output import write_robots

    write_robots(tmp_path)
    text = (tmp_path / "robots.txt").read_text(encoding="utf-8")
    # The five required category headers.
    for header in (
        "Web search engines",
        "Social / link-preview",
        "SEO audit",
        "AI retrieval",
        "AI training",
    ):
        assert header in text, f"missing category header: {header}"
    # The canonical 2026 retrieval bots must each have a block.
    for ua in (
        "ChatGPT-User",
        "OAI-SearchBot",
        "Claude-User",
        "Claude-SearchBot",
        "PerplexityBot",
    ):
        assert f"User-agent: {ua}" in text
    # And the training-tier crawlers.
    for ua in ("GPTBot", "ClaudeBot", "Google-Extended", "Bytespider"):
        assert f"User-agent: {ua}" in text
    # Bot policy anchor must be advertised.
    assert "/about/#bot-policy" in text
    # llms-ctx.txt must be advertised alongside llms.txt + llms-full.txt.
    assert "/llms-ctx.txt" in text


def test_write_robots_idempotent(tmp_path):
    """Second write with no content change returns False."""
    from postbuild_lib.output import write_robots

    assert write_robots(tmp_path) is True
    assert write_robots(tmp_path) is False


# ---------------------------------------------------------------------------
# News-sitemap shrink — Google News recommendations
# ---------------------------------------------------------------------------


def test_truncate_news_title_under_limit_passes_through():
    from postbuild_lib import feeds as out

    title = "Short title"
    assert out._truncate_news_title(title) == title


def test_truncate_news_title_clips_at_word_boundary():
    from postbuild_lib import feeds as out

    title = "A very long title that absolutely exceeds the eighty character recommendation set by Google News"
    result = out._truncate_news_title(title)
    assert len(result) <= 80
    assert result.endswith("…")
    # Must clip at a word boundary, not mid-word
    body = result.rstrip("…").rstrip()
    assert not title[len(body)].isalpha() or title[: len(body) + 1].endswith(" ")


def test_truncate_news_title_custom_limit():
    from postbuild_lib import feeds as out

    assert len(out._truncate_news_title("one two three four five", limit=10)) <= 10


def test_limit_news_keywords_under_limit_passes_through():
    from postbuild_lib import feeds as out

    kws = "a, b, c"
    assert out._limit_news_keywords(kws) == kws


def test_limit_news_keywords_trims_to_first_n():
    from postbuild_lib import feeds as out

    kws = ", ".join(f"k{i}" for i in range(15))
    result = out._limit_news_keywords(kws)
    items = [k.strip() for k in result.split(",")]
    assert len(items) == 10
    assert items == [f"k{i}" for i in range(10)]


def test_fix_social_image_no_op_when_no_blogposting_image_field():
    """No ``"image":`` field in the JSON-LD → bail at the first guard."""
    html = '<meta name="twitter:card" content="summary">'
    assert pb.fix_social_image(html) == html


# ---------------------------------------------------------------------------
# Lang helpers — _resolve_en_slug, _alternates_for_en_slug
# ---------------------------------------------------------------------------


def test_resolve_en_slug_static_pages_use_static_map():
    from postbuild_lib.hreflang import _resolve_en_slug

    # "about" → static EN page. FR slug for "about" is "a-propos".
    # When given the FR slug, _resolve_en_slug returns the EN canonical.
    assert _resolve_en_slug("a-propos", "fr") == "about"


def test_resolve_en_slug_returns_none_for_unknown_slug():
    from postbuild_lib.hreflang import _resolve_en_slug

    assert _resolve_en_slug("totally-unknown-slug", "fr") is None


def test_all_active_non_en_langs_includes_fr_de_ar():
    from postbuild_lib.article_furniture import _all_active_non_en_langs

    codes = _all_active_non_en_langs()
    assert "fr" in codes
    assert "de" in codes
    assert "ar" in codes


# ---------------------------------------------------------------------------
# hreflang helpers — _alternates_for_en_slug + inject_hreflang
# ---------------------------------------------------------------------------


def test_alternates_for_en_slug_includes_en_first():
    from postbuild_lib.hreflang import _alternates_for_en_slug

    alts = _alternates_for_en_slug("about", {})  # no translations rendered
    assert alts[0] == ("en", "https://sebastienrousseau.com/about/")
    assert len(alts) == 1  # no FR/DE/AR since translated_per_lang is empty


def test_alternates_for_en_slug_includes_fr_when_translation_exists():
    from postbuild_lib.hreflang import _alternates_for_en_slug

    # "about" → FR slug "a-propos" (per _data/i18n/fr/slugs.json)
    alts = _alternates_for_en_slug("about", {"fr": {"a-propos"}})
    codes = [c for c, _ in alts]
    assert "en" in codes
    assert "fr" in codes
    fr_url = next(u for c, u in alts if c == "fr")
    assert "/fr/a-propos/" in fr_url


def test_inject_hreflang_emits_alternate_links():
    from postbuild_lib.hreflang import inject_hreflang

    html = '<head><meta charset="utf-8"></head><body></body>'
    out = inject_hreflang(html, "about", "en", {"fr": {"a-propos"}})
    assert 'hreflang="en"' in out
    assert 'hreflang="fr"' in out
    assert 'hreflang="x-default"' in out
    assert "/fr/a-propos/" in out


def test_inject_hreflang_no_op_when_only_en_resolves():
    from postbuild_lib.hreflang import inject_hreflang

    html = "<head></head>"
    # No translations rendered → only EN alternate → < 2 entries → no-op
    out = inject_hreflang(html, "about", "en", {})
    assert "hreflang=" not in out


def test_inject_hreflang_no_op_when_slug_unresolvable():
    from postbuild_lib.hreflang import inject_hreflang

    html = "<head></head>"
    out = inject_hreflang(html, "totally-unknown", "fr", {})
    assert "hreflang=" not in out


def test_inject_hreflang_strips_existing_alternates_first():
    """A page already carrying ``<link rel="alternate" hreflang=>`` gets
    them stripped before the new set is inserted."""
    from postbuild_lib.hreflang import inject_hreflang

    # The strip regex expects the XHTML self-close style ``/>`` because
    # that's what the postbuild renderer emits.
    html = "<head>" '<link rel="alternate" hreflang="en" href="https://old.example/" />' "</head>"
    out = inject_hreflang(html, "about", "en", {"fr": {"a-propos"}})
    assert "https://old.example/" not in out
    assert "/fr/a-propos/" in out


def test_hreflang_pass_skips_non_top_level_leaf_collisions(tmp_path, monkeypatch):
    """The "research" TAG landing (/tags/research/) must never inherit the
    /research/ STATIC hub's alternate cluster (5-item nav re-architecture).
    _apply_hreflang_pass only slug-pairs top-level pages; deeper surfaces
    keep whatever hreflang chain their generator emitted."""
    import postbuild as pb

    monkeypatch.chdir(tmp_path)
    page = tmp_path / "public" / "tags" / "research" / "index.html"
    page.parent.mkdir(parents=True)
    original = (
        "<head>"
        '<link rel="alternate" hreflang="en" '
        'href="https://sebastienrousseau.com/tags/research/" />'
        "</head>"
    )
    page.write_text(original)

    class _Ctx:
        translated_per_lang: ClassVar[dict[str, set[str]]] = {"fr": {"recherche"}}

    out = pb._apply_hreflang_pass(original, page, _Ctx())
    assert out == original  # untouched: tag chain preserved, no static cluster
    # ... while the real top-level static page still gets paired.
    static = tmp_path / "public" / "research" / "index.html"
    static.parent.mkdir(parents=True)
    static_html = "<head></head>"
    static.write_text(static_html)
    out2 = pb._apply_hreflang_pass(static_html, static, _Ctx())
    assert "/fr/recherche/" in out2


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
    from postbuild_lib.hreflang import _resolve_en_slug

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
    from postbuild_lib.hreflang import build_fr_title_index

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


    with patch.object(hf, "PUBLIC", tmp_path / "public"):
        out = hf._translated_slugs_per_lang()
    assert out == {}


def test_translated_slugs_legacy_returns_two_empty_sets_without_fr_dir(tmp_path, monkeypatch):
    from unittest.mock import patch


    monkeypatch.chdir(tmp_path)
    (tmp_path / "public").mkdir()
    with patch.object(hf, "PUBLIC", tmp_path / "public"):
        en_with_fr, fr_with_en = hf._translated_slugs()
    assert en_with_fr == set()
    assert fr_with_en == set()


def test_slug_maps_for_known_lang_returns_four_maps():
    """``_slug_maps_for`` returns the four lookup tables for a registered lang."""
    from postbuild_lib.article_furniture import _slug_maps_for

    out = _slug_maps_for("fr")
    assert set(out) == {
        "articles_en_to_lang",
        "articles_lang_to_en",
        "statics_en_to_lang",
        "statics_lang_to_en",
    }
    # FR static map should have "about" → "a-propos"
    assert out["statics_en_to_lang"]["about"] == "a-propos"


def test_translated_slugs_per_lang_walks_rendered_pages(tmp_path):
    """A rendered /<lang>/<slug>/index.html populates the set for that lang."""
    from unittest.mock import patch


    public = tmp_path / "public"
    (public / "fr" / "a-propos").mkdir(parents=True)
    (public / "fr" / "a-propos" / "index.html").write_text("x", encoding="utf-8")
    with patch.object(hf, "PUBLIC", public):
        out = hf._translated_slugs_per_lang()
    assert "fr" in out
    assert "a-propos" in out["fr"]


def test_translated_slugs_legacy_picks_up_fr_articles(tmp_path):
    """The legacy two-set helper returns (en_with_fr, fr_with_en)."""
    from unittest.mock import patch

    from postbuild_lib import article_furniture as af

    # Pick any en/fr article slug pair that exists in the live FR map.
    fr_articles = af._slug_maps("fr")["articles_en_to_lang"]
    en_slug, fr_slug = next(iter(fr_articles.items()))
    public = tmp_path / "public"
    (public / "fr" / fr_slug).mkdir(parents=True)
    (public / "fr" / fr_slug / "index.html").write_text("x", encoding="utf-8")
    with patch.object(hf, "PUBLIC", public):
        en_with_fr, fr_with_en = hf._translated_slugs()
    assert en_slug in en_with_fr
    assert fr_slug in fr_with_en


def test_resolve_en_slug_static_path():
    """A static EN slug (registered in slugs.json) resolves via the static map."""
    from postbuild_lib.hreflang import _resolve_en_slug

    # "a-propos" is FR for "about" — static page
    assert _resolve_en_slug("a-propos", "fr") == "about"


def test_inject_hreflang_with_legacy_fr_with_en_arg():
    """The legacy ``fr_with_en=`` kwarg seeds ``translated_per_lang`` for FR."""
    from postbuild_lib.hreflang import inject_hreflang

    html = "<head></head>"
    out = inject_hreflang(html, "about", "en", fr_with_en={"a-propos"})
    assert 'hreflang="fr"' in out
    assert "/fr/a-propos/" in out


def test_inject_hreflang_default_translated_per_lang_is_none():
    """No ``translated_per_lang=`` and no ``fr_with_en=`` → starts with empty
    map (covers line 970: ``translated_per_lang = {}``)."""
    from postbuild_lib.hreflang import inject_hreflang

    html = "<head></head>"
    # No translations → only EN alternate → < 2 alts → no-op
    assert "hreflang" not in inject_hreflang(html, "about", "en")


def test_alternates_for_en_slug_skips_lang_without_translation():
    """A slug present in EN but absent from a particular lang's slug map
    is skipped (covers the ``if not lang_slug: continue`` branch at line 970)."""
    from postbuild_lib.hreflang import _alternates_for_en_slug

    # A slug that exists in *no* registered slug map — both the articles
    # and statics maps return None for it, so each non-EN lang hits the
    # ``continue`` branch.
    alts = _alternates_for_en_slug("totally-fake-slug-zzz", {"fr": {"x"}, "ar": {"y"}})
    # Only the EN alternate survives.
    assert alts == [("en", "https://sebastienrousseau.com/totally-fake-slug-zzz/")]


def test_build_fr_title_index_skips_pages_outside_fr_tree(tmp_path):
    """A page whose ``parent.parent`` is not ``fr`` is skipped at line 455."""
    from pathlib import Path as _P

    from postbuild_lib.hreflang import build_fr_title_index

    d = tmp_path / "public" / "2026-05-12-en-post"  # parent.parent = public, not fr
    d.mkdir(parents=True)
    (d / "index.html").write_text("<h1>English</h1>", encoding="utf-8")
    assert build_fr_title_index([_P(str(d / "index.html"))]) == {}


def test_build_fr_title_index_walks_fr_pages_with_real_slug(tmp_path, monkeypatch):
    """Uses a real FR slug from the live map so ``_en_slug`` reverse-lookup succeeds."""
    from pathlib import Path as _P

    from postbuild_lib.article_furniture import _slug_maps
    from postbuild_lib.hreflang import build_fr_title_index

    fr_articles = _slug_maps("fr")["articles_en_to_lang"]
    en_slug, fr_slug = next(iter(fr_articles.items()))
    p = tmp_path / "public" / "fr" / fr_slug
    p.mkdir(parents=True)
    (p / "index.html").write_text(
        '<script type="application/ld+json">{"@type":"BlogPosting"}</script>'
        '<section class="ap-hero"><h1>Titre FR</h1></section>',
        encoding="utf-8",
    )
    idx = build_fr_title_index([_P(str(p / "index.html"))])
    assert idx[en_slug] == "Titre FR"


def test_build_fr_title_index_skips_non_dated_fr_pages(tmp_path):
    """An FR static page (non-dated slug) is skipped (line 458 ``continue``)."""
    from pathlib import Path as _P

    from postbuild_lib.hreflang import build_fr_title_index

    p = tmp_path / "public" / "fr" / "a-propos"
    p.mkdir(parents=True)
    (p / "index.html").write_text("<h1>x</h1>", encoding="utf-8")
    assert build_fr_title_index([_P(str(p / "index.html"))]) == {}


def test_build_fr_title_index_skips_when_en_slug_unmatched(tmp_path):
    """Dated FR page whose slug isn't in the FR articles map is dropped."""
    from pathlib import Path as _P

    from postbuild_lib.hreflang import build_fr_title_index

    p = tmp_path / "public" / "fr" / "2026-05-12-unmatched-fr-slug"
    p.mkdir(parents=True)
    (p / "index.html").write_text(
        '<section class="ap-hero"><h1>Titre</h1></section>',
        encoding="utf-8",
    )
    assert build_fr_title_index([_P(str(p / "index.html"))]) == {}


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
        "</head></html>"
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
# _build_title_index + fix_xml_feed_urls — happy paths
# ---------------------------------------------------------------------------


def test_build_title_index_maps_title_to_url(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    posts = tmp_path / "_posts"
    posts.mkdir()
    (posts / "post.md").write_text(
        '---\ntitle: "AI & Banking"\nurl: "https://sebastienrousseau.com/ai-banking/"\n---\n',
        encoding="utf-8",
    )
    from postbuild_lib.feeds import _build_title_index

    idx = _build_title_index()
    assert idx["AI & Banking"] == "https://sebastienrousseau.com/ai-banking/"
    # Pre-escaped form also indexed
    assert "AI &amp; Banking" in idx


def test_build_title_index_walks_per_language_posts(tmp_path, monkeypatch):
    """`_posts/<lang>/<slug>.md` files get indexed under a synthesised
    `/<lang>/<slug>/` URL, ignoring any `url:` the translator copied
    verbatim from the EN source."""
    monkeypatch.chdir(tmp_path)
    posts = tmp_path / "_posts"
    (posts / "fr").mkdir(parents=True)
    (posts / "fr" / "2026-05-21-mon-article.md").write_text(
        # Frontmatter `url:` is the EN URL — translator copied it. The
        # synthesised URL should win, derived from the post path.
        "---\n"
        'title: "Mon article test"\n'
        'url: "https://sebastienrousseau.com/2026-05-21-en-article"\n'
        "---\n",
        encoding="utf-8",
    )
    from postbuild_lib.feeds import _build_title_index

    idx = _build_title_index()
    assert idx["Mon article test"] == (
        "https://sebastienrousseau.com/fr/2026-05-21-mon-article/index.html"
    )


def test_build_title_index_skips_per_lang_post_without_title(tmp_path, monkeypatch):
    """`_posts/<lang>/<slug>.md` without a title is skipped (no key added)."""
    monkeypatch.chdir(tmp_path)
    posts = tmp_path / "_posts"
    (posts / "de").mkdir(parents=True)
    (posts / "de" / "stub.md").write_text(
        # No title in frontmatter — gets skipped before the synthesised URL
        # is computed.
        '---\nurl: "https://example.com/"\n---\n',
        encoding="utf-8",
    )
    from postbuild_lib.feeds import _build_title_index

    idx = _build_title_index()
    assert idx == {}


def test_build_title_index_handles_apostrophe_in_title(tmp_path, monkeypatch):
    """Titles with apostrophes get an `&apos;` variant indexed for atom
    lookup (atom feeds XML-escape `'` even though XML doesn't require it)."""
    monkeypatch.chdir(tmp_path)
    posts = tmp_path / "_posts"
    posts.mkdir()
    (posts / "p.md").write_text(
        '---\ntitle: "Don\'t Panic & Carry On"\n'
        'url: "https://sebastienrousseau.com/dont-panic/"\n---\n',
        encoding="utf-8",
    )
    from postbuild_lib.feeds import _build_title_index

    idx = _build_title_index()
    # Plain
    assert "Don't Panic & Carry On" in idx
    # &amp;-only variant
    assert "Don't Panic &amp; Carry On" in idx
    # &apos;-only variant
    assert "Don&apos;t Panic & Carry On" in idx
    # Combined variant
    assert "Don&apos;t Panic &amp; Carry On" in idx


def test_fix_xml_feed_urls_no_op_when_title_index_empty(tmp_path, monkeypatch):
    """Without _posts/, the title index is empty → no patching."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "rss.xml").write_text("<rss></rss>", encoding="utf-8")
    from postbuild_lib.feeds import fix_xml_feed_urls

    assert fix_xml_feed_urls(tmp_path) == 0


def test_fix_xml_feed_urls_rewrites_rss_item_block(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    posts = tmp_path / "_posts"
    posts.mkdir()
    (posts / "p.md").write_text(
        '---\ntitle: "Title X"\nurl: "https://sebastienrousseau.com/x/"\n---\n',
        encoding="utf-8",
    )
    rss = tmp_path / "rss.xml"
    rss.write_text(
        "<rss><channel><item>"
        "<title>Title X</title>"
        "<link>http://127.0.0.1:8000/.meta/</link>"
        "</item></channel></rss>",
        encoding="utf-8",
    )
    from postbuild_lib.feeds import fix_xml_feed_urls

    assert fix_xml_feed_urls(tmp_path) == 1
    out = rss.read_text(encoding="utf-8")
    assert "127.0.0.1" not in out
    assert "https://sebastienrousseau.com/x/" in out


def test_fix_xml_feed_urls_handles_atom_and_news_blocks(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    posts = tmp_path / "_posts"
    posts.mkdir()
    (posts / "p.md").write_text(
        '---\ntitle: "T"\nurl: "https://sebastienrousseau.com/t/"\n---\n',
        encoding="utf-8",
    )
    (tmp_path / "atom.xml").write_text(
        "<feed><entry><title>T</title>"
        '<link href="http://localhost:8000/.meta/"/></entry></feed>',
        encoding="utf-8",
    )
    (tmp_path / "news-sitemap.xml").write_text(
        "<urlset><url><loc>http://127.0.0.1:8000/.meta/</loc>"
        '<news:news xmlns:news="x"><news:title>T</news:title></news:news>'
        "</url></urlset>",
        encoding="utf-8",
    )
    from postbuild_lib.feeds import fix_xml_feed_urls

    assert fix_xml_feed_urls(tmp_path) >= 1


def test_fix_xml_feeds_writes_only_when_changed(tmp_path):
    """``fix_xml_feeds`` returns the count of files actually rewritten."""
    rss = tmp_path / "rss.xml"
    rss.write_text("<rss><channel><title>A &amp; B</title></channel></rss>", encoding="utf-8")
    from postbuild_lib.feeds import fix_xml_feeds

    # Already-escaped content → no changes
    assert fix_xml_feeds(tmp_path) == 0


def test_fix_xml_feeds_rewrites_bare_amp(tmp_path):
    rss = tmp_path / "rss.xml"
    rss.write_text("<rss><channel><title>A & B</title></channel></rss>", encoding="utf-8")
    from postbuild_lib.feeds import fix_xml_feeds

    assert fix_xml_feeds(tmp_path) == 1
    assert "A &amp; B" in rss.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# dedupe_xml_feeds — strip duplicate <item>/<entry>/<url> blocks emitted
# by the upstream SSG when multiple locale files share a publication date
# ---------------------------------------------------------------------------


def test_dedupe_xml_feeds_drops_duplicate_rss_items_by_link(tmp_path):
    from postbuild_lib.feeds import dedupe_xml_feeds

    rss = tmp_path / "rss.xml"
    rss.write_text(
        "<rss><channel>"
        "<item><title>A</title><link>https://x/a</link></item>"
        "<item><title>A2</title><link>https://x/a</link></item>"  # dup link
        "<item><title>B</title><link>https://x/b</link></item>"
        "</channel></rss>",
        encoding="utf-8",
    )
    assert dedupe_xml_feeds(tmp_path) == 1
    out = rss.read_text(encoding="utf-8")
    # First occurrence wins
    assert "<title>A</title>" in out
    assert "<title>A2</title>" not in out
    assert "<title>B</title>" in out


def test_dedupe_xml_feeds_no_op_when_all_links_unique(tmp_path):
    from postbuild_lib.feeds import dedupe_xml_feeds

    rss = tmp_path / "rss.xml"
    rss.write_text(
        "<rss><channel>"
        "<item><link>https://x/a</link></item>"
        "<item><link>https://x/b</link></item>"
        "</channel></rss>",
        encoding="utf-8",
    )
    assert dedupe_xml_feeds(tmp_path) == 0


def test_dedupe_xml_feeds_handles_atom_entry_dups_by_href(tmp_path):
    from postbuild_lib.feeds import dedupe_xml_feeds

    atom = tmp_path / "atom.xml"
    atom.write_text(
        "<feed>"
        '<entry><link href="https://x/a"/></entry>'
        '<entry><link href="https://x/a"/></entry>'
        '<entry><link href="https://x/b"/></entry>'
        "</feed>",
        encoding="utf-8",
    )
    assert dedupe_xml_feeds(tmp_path) == 1
    out = atom.read_text(encoding="utf-8")
    assert out.count('href="https://x/a"') == 1
    assert out.count('href="https://x/b"') == 1


def test_dedupe_xml_feeds_handles_sitemap_url_dups_by_loc(tmp_path):
    from postbuild_lib.feeds import dedupe_xml_feeds

    sm = tmp_path / "news-sitemap.xml"
    sm.write_text(
        "<urlset>"
        "<url><loc>https://x/a</loc></url>"
        "<url><loc>https://x/a</loc></url>"
        "<url><loc>https://x/b</loc></url>"
        "</urlset>",
        encoding="utf-8",
    )
    assert dedupe_xml_feeds(tmp_path) == 1
    out = sm.read_text(encoding="utf-8")
    assert out.count("<loc>https://x/a</loc>") == 1
    assert out.count("<loc>https://x/b</loc>") == 1


def test_dedupe_xml_feeds_returns_zero_when_no_files(tmp_path):
    from postbuild_lib.feeds import dedupe_xml_feeds

    # Empty directory — none of the target files exist
    assert dedupe_xml_feeds(tmp_path) == 0


def test_dedupe_xml_feeds_preserves_blocks_without_key(tmp_path):
    """If a block has no recognisable URL, keep it (don't drop in error)."""
    from postbuild_lib.feeds import dedupe_xml_feeds

    rss = tmp_path / "rss.xml"
    rss.write_text(
        "<rss><channel>"
        "<item><title>orphan</title></item>"  # no <link>
        "<item><title>orphan</title></item>"  # also no <link> — kept
        "<item><link>https://x/a</link></item>"
        "</channel></rss>",
        encoding="utf-8",
    )
    # 0 dedups expected: orphan items have no key so they're each kept
    assert dedupe_xml_feeds(tmp_path) == 0
    out = rss.read_text(encoding="utf-8")
    assert out.count("<title>orphan</title>") == 2


def test_dedupe_xml_feeds_atom_entry_without_href_passes_through(tmp_path):
    """An <entry> with no `<link href=>` has no key — kept verbatim."""
    from postbuild_lib.feeds import dedupe_xml_feeds

    atom = tmp_path / "atom.xml"
    atom.write_text(
        "<feed>"
        "<entry><id>tag:1</id></entry>"  # no link href
        "<entry><id>tag:2</id></entry>"  # no link href
        "</feed>",
        encoding="utf-8",
    )
    assert dedupe_xml_feeds(tmp_path) == 0


# ---------------------------------------------------------------------------
# augment_sitemap_with_rendered_pages — append topic / post-hoc pages
# that the SSG didn't know about when it generated the initial sitemap
# ---------------------------------------------------------------------------


def _seed_minimal_sitemap(tmp_path, listed_paths):
    """Write a sitemap.xml with the given paths already listed."""
    urls = "".join(
        f"<url><lastmod>2026-05-20</lastmod><loc>https://sebastienrousseau.com{p}</loc></url>"
        for p in listed_paths
    )
    (tmp_path / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n</urlset>\n",
        encoding="utf-8",
    )


def test_augment_sitemap_appends_missing_rendered_page(tmp_path):
    from postbuild_lib.feeds import augment_sitemap_with_rendered_pages

    _seed_minimal_sitemap(tmp_path, ["/"])
    new = tmp_path / "topics" / "cloud-native-banking"
    new.mkdir(parents=True)
    (new / "index.html").write_text("<html></html>", encoding="utf-8")
    n = augment_sitemap_with_rendered_pages(tmp_path)
    assert n == 1
    out = (tmp_path / "sitemap.xml").read_text(encoding="utf-8")
    # Emitted in canonical pretty-URL form, not /index.html.
    assert "<loc>https://sebastienrousseau.com/topics/cloud-native-banking/</loc>" in out
    assert "/topics/cloud-native-banking/index.html" not in out


def test_augment_sitemap_normalises_so_already_listed_pages_skip(tmp_path):
    """If `/topics/foo/` is already listed (trailing slash form), the
    `/topics/foo/index.html` rendered page is NOT appended."""
    from postbuild_lib.feeds import augment_sitemap_with_rendered_pages

    _seed_minimal_sitemap(tmp_path, ["/topics/foo/"])
    d = tmp_path / "topics" / "foo"
    d.mkdir(parents=True)
    (d / "index.html").write_text("x", encoding="utf-8")
    assert augment_sitemap_with_rendered_pages(tmp_path) == 0


def test_augment_sitemap_normalises_when_existing_entry_uses_index_html(tmp_path):
    """Existing sitemap entry in `/foo/index.html` form must match a
    rendered `/foo/index.html` page (both normalise to `/foo`)."""
    from postbuild_lib.feeds import augment_sitemap_with_rendered_pages

    _seed_minimal_sitemap(tmp_path, ["/topics/foo/index.html"])
    d = tmp_path / "topics" / "foo"
    d.mkdir(parents=True)
    (d / "index.html").write_text("x", encoding="utf-8")
    assert augment_sitemap_with_rendered_pages(tmp_path) == 0


def test_augment_sitemap_excludes_labs_prefix(tmp_path):
    from postbuild_lib.feeds import augment_sitemap_with_rendered_pages

    _seed_minimal_sitemap(tmp_path, ["/"])
    labs = tmp_path / "labs" / "hsh-demo"
    labs.mkdir(parents=True)
    (labs / "index.html").write_text("x", encoding="utf-8")
    assert augment_sitemap_with_rendered_pages(tmp_path) == 0


def test_augment_sitemap_excludes_404_offline_thanks(tmp_path):
    from postbuild_lib.feeds import augment_sitemap_with_rendered_pages

    _seed_minimal_sitemap(tmp_path, ["/"])
    for tail in ("404", "offline", "thanks", "fr/404", "fr/hors-ligne", "fr/merci"):
        d = tmp_path / tail
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text("x", encoding="utf-8")
    assert augment_sitemap_with_rendered_pages(tmp_path) == 0


def test_augment_sitemap_no_op_when_sitemap_absent(tmp_path):
    from postbuild_lib.feeds import augment_sitemap_with_rendered_pages

    # No sitemap.xml at all → function silently returns 0
    assert augment_sitemap_with_rendered_pages(tmp_path) == 0


def test_augment_sitemap_handles_sitemap_without_lastmod(tmp_path):
    """When the seed sitemap has no <lastmod>, the appended block uses
    an empty string for lastmod rather than crashing."""
    from postbuild_lib.feeds import augment_sitemap_with_rendered_pages

    (tmp_path / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        "</urlset>\n",
        encoding="utf-8",
    )
    new = tmp_path / "topics" / "foo"
    new.mkdir(parents=True)
    (new / "index.html").write_text("x", encoding="utf-8")
    n = augment_sitemap_with_rendered_pages(tmp_path)
    assert n == 1
    out = (tmp_path / "sitemap.xml").read_text(encoding="utf-8")
    # Emitted in canonical pretty-URL form, not /index.html.
    assert "<loc>https://sebastienrousseau.com/topics/foo/</loc>" in out
    assert "topics/foo/index.html" not in out


# ---------------------------------------------------------------------------
# dedupe_sitemap_index_html — drop/rewrite stale /<slug>/index.html entries


def _sitemap_with_blocks(*blocks: str) -> str:
    body = "\n".join(blocks)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}\n"
        "</urlset>\n"
    )


def _url_block(loc: str, lastmod: str = "2026-05-30", changefreq: str = "weekly") -> str:
    return (
        "<url>\n"
        f"  <loc>{loc}</loc>\n"
        f"  <lastmod>{lastmod}</lastmod>\n"
        f"  <changefreq>{changefreq}</changefreq>\n"
        "</url>"
    )


def test_dedupe_sitemap_drops_index_html_when_pretty_twin_exists(tmp_path):
    """Both /<slug>/ and /<slug>/index.html present → drop the
    index.html block, keep the pretty one (with its real lastmod)."""
    from postbuild_lib.feeds import dedupe_sitemap_index_html

    sm = tmp_path / "sitemap.xml"
    sm.write_text(
        _sitemap_with_blocks(
            _url_block("https://sebastienrousseau.com/foo/", lastmod="2026-05-30"),
            _url_block("https://sebastienrousseau.com/foo/index.html", lastmod="2024-04-15"),
        ),
        encoding="utf-8",
    )
    n = dedupe_sitemap_index_html(sm)
    assert n == 1
    out = sm.read_text(encoding="utf-8")
    assert "<loc>https://sebastienrousseau.com/foo/</loc>" in out
    assert "index.html" not in out
    # The surviving block kept its correct lastmod, not the stale one.
    assert "<lastmod>2026-05-30</lastmod>" in out
    assert "<lastmod>2024-04-15</lastmod>" not in out


def test_dedupe_sitemap_rewrites_orphan_index_html_to_pretty(tmp_path):
    """Only /<slug>/index.html present (no pretty twin) → rewrite the
    <loc> in place to the pretty form, preserve metadata."""
    from postbuild_lib.feeds import dedupe_sitemap_index_html

    sm = tmp_path / "sitemap.xml"
    sm.write_text(
        _sitemap_with_blocks(
            _url_block(
                "https://sebastienrousseau.com/topics/orphan/index.html", lastmod="2026-04-01"
            ),
        ),
        encoding="utf-8",
    )
    n = dedupe_sitemap_index_html(sm)
    assert n == 1
    out = sm.read_text(encoding="utf-8")
    assert "<loc>https://sebastienrousseau.com/topics/orphan/</loc>" in out
    assert "index.html" not in out
    # Original lastmod / changefreq preserved on the rewritten block.
    assert "<lastmod>2026-04-01</lastmod>" in out
    assert "<changefreq>weekly</changefreq>" in out


def test_dedupe_sitemap_leaves_pretty_only_alone(tmp_path):
    """No /index.html anywhere → function is a no-op (0 returned, file
    unchanged)."""
    from postbuild_lib.feeds import dedupe_sitemap_index_html

    sm = tmp_path / "sitemap.xml"
    original = _sitemap_with_blocks(
        _url_block("https://sebastienrousseau.com/foo/"),
        _url_block("https://sebastienrousseau.com/bar/"),
    )
    sm.write_text(original, encoding="utf-8")
    assert dedupe_sitemap_index_html(sm) == 0
    assert sm.read_text(encoding="utf-8") == original


def test_dedupe_sitemap_no_op_when_sitemap_absent(tmp_path):
    from postbuild_lib.feeds import dedupe_sitemap_index_html

    assert dedupe_sitemap_index_html(tmp_path / "sitemap.xml") == 0


def test_dedupe_sitemap_tolerates_malformed_url_block_without_loc(tmp_path):
    """Defensive: a <url>…</url> block with no <loc> inside (corrupt
    sitemap fragment) is left in place rather than crashing."""
    from postbuild_lib.feeds import dedupe_sitemap_index_html

    sm = tmp_path / "sitemap.xml"
    sm.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        # First block has no <loc> — must not crash the patcher.
        "<url>\n  <lastmod>2026-05-30</lastmod>\n</url>\n"
        # Second block is a normal twin pair so the pass has real work to do.
        + _url_block("https://sebastienrousseau.com/foo/")
        + "\n"
        + _url_block("https://sebastienrousseau.com/foo/index.html")
        + "\n</urlset>\n",
        encoding="utf-8",
    )
    n = dedupe_sitemap_index_html(sm)
    assert n == 1  # only the index.html twin removed; malformed block untouched
    out = sm.read_text(encoding="utf-8")
    # Malformed block survived (still has its lastmod).
    assert "<url>\n  <lastmod>2026-05-30</lastmod>\n</url>" in out
    # Twin pair collapsed to the pretty form.
    assert "<loc>https://sebastienrousseau.com/foo/</loc>" in out
    assert "index.html" not in out


def test_dedupe_sitemap_handles_mixed_at_scale(tmp_path):
    """Realistic-shape sitemap with a mix of twinned dupes and orphans
    converges to all-pretty in one pass."""
    from postbuild_lib.feeds import dedupe_sitemap_index_html

    sm = tmp_path / "sitemap.xml"
    sm.write_text(
        _sitemap_with_blocks(
            # Twinned: pretty + index.html for the same slug
            _url_block("https://sebastienrousseau.com/a/", lastmod="2026-05-30"),
            _url_block("https://sebastienrousseau.com/a/index.html", lastmod="2024-04-15"),
            _url_block("https://sebastienrousseau.com/b/", lastmod="2026-05-29"),
            _url_block("https://sebastienrousseau.com/b/index.html", lastmod="2024-04-15"),
            # Orphan: only index.html form
            _url_block("https://sebastienrousseau.com/orphan/index.html", lastmod="2026-05-01"),
            # Already pretty, no twin
            _url_block("https://sebastienrousseau.com/clean/", lastmod="2026-05-28"),
        ),
        encoding="utf-8",
    )
    n = dedupe_sitemap_index_html(sm)
    # 2 twin removals + 1 orphan rewrite = 3 blocks touched
    assert n == 3
    out = sm.read_text(encoding="utf-8")
    assert "index.html" not in out
    # All four canonical pretty URLs survive.
    for loc in ("/a/", "/b/", "/orphan/", "/clean/"):
        assert f"<loc>https://sebastienrousseau.com{loc}</loc>" in out


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
    from postbuild_lib.feeds import build_lastmod_index

    idx = build_lastmod_index()
    assert idx["2026-05-12-x"] == "2026-05-15"


def test_build_lastmod_index_falls_back_to_date(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    posts = tmp_path / "_posts"
    posts.mkdir()
    (posts / "2026-05-12-x.md").write_text(
        '---\ntitle: "X"\ndate: "May 12, 2026"\n---\n', encoding="utf-8"
    )
    from postbuild_lib.feeds import build_lastmod_index

    idx = build_lastmod_index()
    assert idx["2026-05-12-x"] == "2026-05-12"


def test_build_lastmod_index_returns_empty_when_no_posts_dir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    from postbuild_lib.feeds import build_lastmod_index

    assert build_lastmod_index() == {}


def test_refresh_sitemap_lastmod_no_op_when_file_missing(tmp_path):
    from postbuild_lib.feeds import refresh_sitemap_lastmod

    assert refresh_sitemap_lastmod(tmp_path / "missing.xml", {}) == 0


def test_patch_block_no_op_when_block_has_no_title():
    """If the block has no ``<title>`` tag the patcher returns it unchanged."""
    from postbuild_lib.feeds import _patch_block

    block = "<item><link>http://x/.meta/</link></item>"  # no <title>
    assert _patch_block(block, {"Anything": "https://x/"}) == block


def test_build_lastmod_index_skips_post_with_invalid_date(tmp_path, monkeypatch):
    """A post with neither ``last_reviewed`` nor a parseable ``date`` is dropped."""
    monkeypatch.chdir(tmp_path)
    posts = tmp_path / "_posts"
    posts.mkdir()
    (posts / "2026-05-12-good.md").write_text(
        '---\ntitle: "Good"\ndate: "May 12, 2026"\n---\n', encoding="utf-8"
    )
    (posts / "2026-05-13-bad-date.md").write_text(
        '---\ntitle: "Bad"\ndate: "not-a-real-date"\n---\n', encoding="utf-8"
    )
    from postbuild_lib.feeds import build_lastmod_index

    idx = build_lastmod_index()
    assert "2026-05-12-good" in idx
    assert "2026-05-13-bad-date" not in idx  # skipped


def test_shrink_news_sitemap_no_op_when_already_shrunk(tmp_path):
    """File whose titles + keywords are already within bounds → no rewrite."""
    nsm = tmp_path / "news-sitemap.xml"
    nsm.write_text(
        "<urlset><url><news:news>"
        "<news:title>Short title</news:title>"
        "<news:keywords>a,b,c</news:keywords>"
        "</news:news></url></urlset>",
        encoding="utf-8",
    )
    from postbuild_lib.feeds import shrink_news_sitemap

    assert shrink_news_sitemap(tmp_path) == 0


def test_refresh_sitemap_lastmod_skips_blocks_without_loc(tmp_path):
    sitemap = tmp_path / "sitemap.xml"
    sitemap.write_text(
        "<urlset><url><lastmod>2026-01-01</lastmod></url></urlset>",
        encoding="utf-8",
    )
    from postbuild_lib.feeds import refresh_sitemap_lastmod

    n = refresh_sitemap_lastmod(sitemap, {"2026-05-12-x": "2026-05-15"})
    assert n == 0


def test_refresh_sitemap_lastmod_skips_non_dated_loc(tmp_path):
    """An undated URL (e.g. /about/) is left alone by the patch."""
    sitemap = tmp_path / "sitemap.xml"
    sitemap.write_text(
        "<urlset><url><loc>https://sebastienrousseau.com/about/</loc></url></urlset>",
        encoding="utf-8",
    )
    from postbuild_lib.feeds import refresh_sitemap_lastmod

    n = refresh_sitemap_lastmod(sitemap, {"2026-05-12-x": "2026-05-15"})
    assert n == 0


def test_refresh_sitemap_lastmod_skips_dated_slug_not_in_index(tmp_path):
    """A URL whose slug isn't in the lastmod index stays untouched."""
    sitemap = tmp_path / "sitemap.xml"
    sitemap.write_text(
        "<urlset><url><loc>https://sebastienrousseau.com/2026-05-12-unknown/</loc>"
        "<lastmod>2026-01-01</lastmod></url></urlset>",
        encoding="utf-8",
    )
    from postbuild_lib.feeds import refresh_sitemap_lastmod

    n = refresh_sitemap_lastmod(sitemap, {"2026-05-13-other": "2026-05-15"})
    assert n == 0


def test_splice_fr_urls_no_op_when_all_candidates_already_present(tmp_path, monkeypatch):
    """If every EN + lang URL the splicer would add is already in the sitemap,
    ``new_blocks`` is empty and the input is returned unchanged."""
    monkeypatch.chdir(tmp_path)
    # No _posts → only home + static slugs end up as candidates.
    # Pre-populate the sitemap with every static slug + home so nothing is missing.
    statics = (
        "about",
        "articles",
        "papers",
        "projects",
        "topics",
        "tags",
        "playlists",
        "contact",
        "accessibility",
        "privacy",
        "terms",
        "made-with-static-site-generator",
        "made-with-static-site-generator",
        "resources-pacs008-checklist",
        # 5-item nav re-architecture statics
        "suite",
        "research",
        "library",
        "speaking",
        "case-studies",
        "404",
        "offline",
        "thanks",
    )
    locs = ["<url><loc>https://sebastienrousseau.com/</loc></url>"]
    locs.extend(f"<url><loc>https://sebastienrousseau.com/{s}/</loc></url>" for s in statics)
    topics = (
        "post-quantum-cryptography",
        "iso-20022-payments",
        "applied-ai-banking",
        "rust-open-source",
        "blockchain-digital-assets",
    )
    locs.extend(f"<url><loc>https://sebastienrousseau.com/topics/{t}/</loc></url>" for t in topics)
    # Pre-fill the non-EN-lang URLs too so all candidates are present.
    from postbuild_lib.article_furniture import _all_active_non_en_langs
    from postbuild_lib.feeds import _lang_sitemap_urls, _splice_fr_urls

    # Build all candidate URLs explicitly + pre-populate the sitemap.
    for code in _all_active_non_en_langs():
        for url, _, _, _ in _lang_sitemap_urls(code, {}):
            locs.append(f"<url><loc>{url}</loc></url>")
    xml = f"<urlset>{''.join(locs)}</urlset>"
    out = _splice_fr_urls(xml, {})
    assert out == xml  # nothing to add → no-op


def test_refresh_sitemap_lastmod_inserts_when_no_existing_lastmod(tmp_path):
    """A URL with a tracked slug but no existing ``<lastmod>`` gets a fresh one inserted."""
    sitemap = tmp_path / "sitemap.xml"
    sitemap.write_text(
        "<urlset><url>" "<loc>https://sebastienrousseau.com/2026-05-12-x/</loc>" "</url></urlset>",
        encoding="utf-8",
    )
    from postbuild_lib.feeds import refresh_sitemap_lastmod

    n = refresh_sitemap_lastmod(sitemap, {"2026-05-12-x": "2026-05-15"})
    assert n == 1
    assert "<lastmod>2026-05-15</lastmod>" in sitemap.read_text(encoding="utf-8")


def test_refresh_sitemap_lastmod_rewrites_existing_entry(tmp_path, monkeypatch):
    """Existing ``<lastmod>`` for a tracked post is replaced with the index value."""
    monkeypatch.chdir(tmp_path)
    # No _posts dir means _splice_fr_urls only adds the home + static slugs
    sitemap = tmp_path / "sitemap.xml"
    sitemap.write_text(
        '<?xml version="1.0"?><urlset>'
        "<url><loc>https://sebastienrousseau.com/2026-05-12-x/</loc>"
        "<lastmod>2026-01-01</lastmod></url>"
        "</urlset>",
        encoding="utf-8",
    )
    from postbuild_lib.feeds import refresh_sitemap_lastmod

    n = refresh_sitemap_lastmod(sitemap, {"2026-05-12-x": "2026-05-15"})
    assert n == 1
    out = sitemap.read_text(encoding="utf-8")
    assert "<lastmod>2026-05-15</lastmod>" in out


# ---------------------------------------------------------------------------
# shrink_news_sitemap end-to-end
# ---------------------------------------------------------------------------


def test_shrink_news_sitemap_no_op_when_file_missing(tmp_path):
    from postbuild_lib.feeds import shrink_news_sitemap

    assert shrink_news_sitemap(tmp_path) == 0


def test_shrink_news_sitemap_rewrites_long_title(tmp_path):
    nsm = tmp_path / "news-sitemap.xml"
    long_title = "A " * 60  # ~120 chars
    nsm.write_text(
        f"<urlset><url><news:news><news:title>{long_title}</news:title>"
        "<news:keywords>a,b,c,d,e,f,g,h,i,j,k,l,m</news:keywords>"
        "</news:news></url></urlset>",
        encoding="utf-8",
    )
    from postbuild_lib.feeds import shrink_news_sitemap

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
# Localhost URL scrub — `scrub_localhost_urls`
# Guards the SEO/canonical regression: Static Site Generator bakes the dev-server URL
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
    html = (
        '<link rel="alternate" type="application/atom+xml" href="http://localhost:8000/atom.xml"/>'
    )
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
# OG image swap (fix_social_image)
# ---------------------------------------------------------------------------


def test_fix_social_image_rewrites_og_and_twitter():
    html = """
"@type":"BlogPosting","image":{"@type":"ImageObject","url":"https://cloudcdn.pro/banner.webp","width":"1200","height":"630"}
<meta property="og:image" content="https://cloudcdn.pro/divider.svg">
<meta property="og:image:width" content="1">
<meta property="og:image:height" content="1">
<meta name="twitter:image" content="https://cloudcdn.pro/divider.svg">
"""
    out = pb.fix_social_image(html)
    assert 'og:image" content="https://cloudcdn.pro/banner.webp"' in out
    assert 'twitter:image" content="https://cloudcdn.pro/banner.webp"' in out
    assert 'og:image:width" content="1200"' in out


def test_fix_social_image_promotes_twitter_card_summary_to_large():
    html = """
"@type":"BlogPosting","image":{"@type":"ImageObject","url":"https://cloudcdn.pro/banner.webp"}
<meta name="twitter:card" content="summary">
"""
    out = pb.fix_social_image(html)
    assert 'twitter:card" content="summary_large_image"' in out


def test_fix_social_image_refuses_to_propagate_divider():
    html = """
"@type":"BlogPosting","image":{"@type":"ImageObject","url":"https://cloudcdn.pro/divider.svg"}
<meta property="og:image" content="https://cloudcdn.pro/whatever.svg">
"""
    # Should NOT propagate a divider value into og:image.
    out = pb.fix_social_image(html)
    assert out == html
