"""Unit tests for the ``build_translations`` package internals.

The integration smoke (test_build_translations_smoke.py) drives
``main()`` against the real public/ tree and covers the happy paths
end-to-end. These tests pin the branch-level behaviours that the smoke
can't reach deterministically: malformed JSON-LD handling, RTL
attribute stamping, link/date rewrite edge cases, and the per-language
state rebinding contract.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts" / "generators"))

import build_translations as bt
from build_translations import _article, _chrome, _maps, _run, _search
from build_translations import _state as st


@pytest.fixture(autouse=True)
def _fr_bound(monkeypatch):
    """Pin the per-language state to FR for every test (an earlier
    smoke-test main() leaves the last rendered language bound), and
    run from the repo root like the CLI does."""
    monkeypatch.chdir(ROOT)
    st.bind_lang("fr")
    yield
    st.bind_lang("fr")


# ---------------------------------------------------------------------------
# _chrome — JSON-LD patch passes
# ---------------------------------------------------------------------------

BREADCRUMB = (
    '<script type="application/ld+json">'
    '{"@type":"BreadcrumbList","itemListElement":['
    '{"@type":"ListItem","position":1,"name":"Home","item":"https://sebastienrousseau.com/"},'
    '{"@type":"ListItem","position":2,"name":"Articles","item":"https://sebastienrousseau.com/articles/"},'
    '{"@type":"ListItem","position":3,"name":"Old","item":"https://sebastienrousseau.com/x/"},'
    "null]}"
    "</script>"
)


def test_swap_breadcrumb_localises_items():
    out = _chrome._swap_breadcrumb(f"<html>{BREADCRUMB}</html>", "mon-slug", "Titre FR")
    assert '"name":"Accueil"' in out
    assert '"item":"https://sebastienrousseau.com/fr/"' in out
    assert '"name":"Titre FR"' in out
    assert '"item":"https://sebastienrousseau.com/fr/mon-slug/"' in out


def test_swap_breadcrumb_malformed_json_warns_and_keeps_html(capsys):
    """Task-2 regression: a malformed BreadcrumbList block must leave
    the HTML byte-identical AND print a one-line stderr warning naming
    the page — silent failure is how /he/ shipped a broken breadcrumb."""
    html = (
        '<html><script type="application/ld+json">'
        '{"@type":"BreadcrumbList","itemListElement":[{oops]}'
        "</script></html>"
    )
    out = _chrome._swap_breadcrumb(html, "broken-slug", "T")
    assert out == html
    err = capsys.readouterr().err
    assert "WARNING" in err
    assert "malformed JSON-LD" in err
    assert "/fr/broken-slug/" in err
    assert err.count("\n") == 1  # one line, not a traceback


def test_swap_breadcrumb_ignores_blocks_without_breadcrumb(capsys):
    html = '<script type="application/ld+json">{"@type":"WebSite"}</script>'
    assert _chrome._swap_breadcrumb(html, "s", "t") == html
    assert capsys.readouterr().err == ""


def test_patch_jsonld_scripts_malformed_without_context_is_silent(capsys):
    html = '<script type="application/ld+json">{nope}</script>'
    out = _chrome._patch_jsonld_scripts(html, lambda node: True)
    assert out == html
    assert capsys.readouterr().err == ""


def test_patch_jsonld_scripts_non_dict_top_level_unchanged():
    html = '<script type="application/ld+json">[1,2,3]</script>'
    assert _chrome._patch_jsonld_scripts(html, lambda node: True) == html


def test_patch_jsonld_scripts_graph_nodes_are_patched():
    html = (
        '<script type="application/ld+json">'
        '{"@graph":[{"@type":"WebSite","inLanguage":"en"},"str",'
        '{"@type":"Person"}]}'
        "</script>"
    )

    def patch(node: dict) -> bool:
        if node.get("@type") == "WebSite":
            node["inLanguage"] = "fr"
            return True
        return False

    out = _chrome._patch_jsonld_scripts(html, patch)
    assert '"inLanguage":"fr"' in out


def test_patch_blogposting_jsonld_rewrites_fields():
    html = (
        '<script type="application/ld+json">'
        '{"@type":"BlogPosting","headline":"EN","description":"EN d",'
        '"inLanguage":"en-GB","url":"https://sebastienrousseau.com/x/",'
        '"mainEntityOfPage":"https://sebastienrousseau.com/x/",'
        '"isPartOf":{"@id":"https://sebastienrousseau.com/#blog"}}'
        "</script>"
    )
    out = _chrome._patch_blogposting_jsonld(
        html,
        title="T",
        description="D",
        keywords="k1, k2",
        url_fr="https://sebastienrousseau.com/fr/x/",
        banner="https://cdn/x.webp",
        banner_alt="alt",
    )
    assert '"headline":"T"' in out
    assert '"keywords":"k1, k2"' in out
    assert '"mainEntityOfPage":"https://sebastienrousseau.com/fr/x/"' in out
    assert '"inLanguage":"fr"' in out
    assert "Articles (français)" in out


def test_patch_blogposting_jsonld_dict_main_entity():
    html = (
        '<script type="application/ld+json">'
        '{"@type":"BlogPosting","mainEntityOfPage":{"@id":"https://sebastienrousseau.com/x/"}}'
        "</script>"
    )
    out = _chrome._patch_blogposting_jsonld(
        html, title="T", description="D", keywords="", url_fr="U", banner="", banner_alt=""
    )
    assert '"@id":"U"' in out


def test_localize_inlanguage_globally_walks_every_node():
    html = (
        '<script type=application/ld+json>{"@type":"WebSite","inLanguage":"en-GB",'
        '"publisher":{"inLanguage":"en-GB"},"keywords":["a"],"n":1}</script>'
    )
    out = _chrome._localize_inlanguage_globally(html, "fr")
    assert out.count('"inLanguage":"fr"') == 2


def test_localize_inlanguage_globally_skips_malformed_and_absent():
    bad = '<script type="application/ld+json">{"inLanguage": broken}</script>'
    assert _chrome._localize_inlanguage_globally(bad) == bad
    none = '<script type="application/ld+json">{"@type":"WebSite"}</script>'
    assert _chrome._localize_inlanguage_globally(none) == none


# ---------------------------------------------------------------------------
# _chrome — lang attribute, dates, links
# ---------------------------------------------------------------------------


def test_set_html_lang_fr_strips_rtl_dir():
    out = _chrome._set_html_lang('<html lang="en-GB" dir="rtl"><body></body></html>')
    assert 'lang="fr-FR"' in out
    assert 'dir="rtl"' not in out


def test_set_html_lang_rtl_language_adds_dir():
    st.bind_lang("ar")
    out = _chrome._set_html_lang('<html lang="en-GB"><body></body></html>')
    assert 'dir="rtl"' in out


def test_is_rtl_cached_per_code():
    assert st._is_rtl("ar") is True
    assert st._is_rtl("fr") is False
    st.bind_lang("he")
    assert st._is_current_rtl() is True


def test_localize_en_dates_full_short_and_year_month():
    html = "<p>May 19, 2026 and Sep 3, 2025 and November 2024</p>"
    out = _chrome.localize_en_dates(html)
    assert "19 mai 2026" in out
    assert "3 sept. 2025" in out
    assert "novembre 2024" in out


def test_translate_chrome_applies_patches_and_links():
    html = '<a href="/about/">About</a> <time>May 19, 2026</time>'
    out = _chrome.translate_chrome(html)
    assert 'href="/fr/a-propos/"' in out
    assert "19 mai 2026" in out


def test_rewrite_static_links_variants():
    html = (
        '<a href="/privacy/">p</a> '
        '<a href="https://sebastienrousseau.com/contact/index.html">c</a> '
        '<a href="/fr/privacy/">legacy</a> '
        '<a href="/fr/articles/">same</a> '
        '<a href="/topics/payments/">t</a>'
    )
    out = _chrome.rewrite_static_links(html)
    assert 'href="/fr/confidentialite/"' in out
    assert 'href="/fr/contact/index.html"' in out
    assert out.count("confidentialite") == 2  # /privacy/ + legacy /fr/privacy/
    assert 'href="/fr/articles/"' in out
    assert 'href="/fr/sujets/payments/"' in out


def test_localize_feed_links_absolute_and_relative():
    html = '<link href="https://sebastienrousseau.com/atom.xml"><link href="/rss.xml">'
    out = _chrome.localize_feed_links(html)
    assert 'href="/fr/atom.xml"' in out
    assert 'href="/fr/rss.xml"' in out


def test_date_today_is_iso():
    assert len(_chrome._date_today()) == 10


# ---------------------------------------------------------------------------
# _state — bind_lang contract
# ---------------------------------------------------------------------------


def test_bind_lang_rebinds_slug_maps_and_out_dir():
    st.bind_lang("de")
    assert st.LANG_CODE == "de"
    assert st.OUT.as_posix() == "public/de"
    assert st.SRC.as_posix() == "_posts/de"
    assert st.LANG_BCP47.startswith("de")
    st.bind_lang("fr")
    assert st.STATIC_SLUG_FR.get("privacy") == "confidentialite"


def test_fr_slug_falls_back_to_en():
    assert bt.fr_slug("not-a-known-slug") == "not-a-known-slug"


# ---------------------------------------------------------------------------
# _maps — EN URL canonicalisation + title/desc maps
# ---------------------------------------------------------------------------


def test_rewrite_en_urls_routes_known_article_slugs():
    en = next(iter(st.EN_TO_FR))
    fr = st.EN_TO_FR[en]
    html = f'<a href="/{en}/">x</a> <a href="https://sebastienrousseau.com/{en}/index.html">y</a>'
    out = _maps.rewrite_en_urls(html)
    assert f"/fr/{fr}/" in out


def test_rewrite_en_urls_no_known_slug_passthrough():
    html = '<a href="/totally-unknown-page/">x</a>'
    assert _maps.rewrite_en_urls(html) == html


def test_eyebrow_from_locale_tags_prefers_first_tag():
    out = _maps._eyebrow_from_locale_tags("payments, iso 20022")
    assert out  # non-empty label derived from the first tag
    assert _maps._eyebrow_from_locale_tags("") == ""


def test_smart_title_for_eyebrow_acronyms_and_words():
    assert _maps._smart_title_for_eyebrow("iso") == "ISO"
    assert _maps._smart_title_for_eyebrow("payments") == "Payments"


def test_title_and_description_maps_cache_per_language():
    first = _maps._ensure_fr_title_map()
    assert first is _maps._ensure_fr_title_map()
    descs = _maps._ensure_fr_description_map()
    assert isinstance(descs, dict)
    st.bind_lang("fr")  # rebinding clears (in place) and lazily refills
    assert not st._FR_DESCRIPTION_MAP  # cleared until next _ensure_* call
    assert _maps._ensure_fr_title_map() is first  # same dict object, refilled
    assert first


# ---------------------------------------------------------------------------
# _search — text extraction
# ---------------------------------------------------------------------------


def test_extract_visible_text_strips_scripts_styles_comments():
    html = (
        "<main><script>x()</script><style>.a{}</style><!-- c -->"
        "<p>Hello&nbsp;<b>world</b></p></main><footer>nope</footer>"
    )
    assert _search._extract_visible_text(html) == "Hello world"


def test_extract_visible_text_without_main_uses_whole_doc():
    assert _search._extract_visible_text("<p>Body</p>") == "Body"


def test_extract_headings_skips_empty():
    html = "<main><h1>One</h1><h2> </h2><h3><span>Two</span></h3></main>"
    assert _search._extract_headings(html) == ["One", "Two"]


def test_build_fr_search_index_missing_out_dir(monkeypatch):
    monkeypatch.setattr(st, "OUT", Path("public/__no-such-lang__"))
    assert _search._build_fr_search_index() == []


# ---------------------------------------------------------------------------
# _run — driver edge cases
# ---------------------------------------------------------------------------


def test_render_one_lang_missing_posts_dir(monkeypatch, capsys):
    real_bind = st.bind_lang

    def bind_then_point_away(code: str) -> None:
        real_bind(code)
        st.SRC = Path("_posts/__no-such-lang__")

    monkeypatch.setattr(st, "bind_lang", bind_then_point_away)
    assert _run._render_one_lang("fr") == 0
    assert "nothing to do" in capsys.readouterr().out


def test_render_translation_returns_none_without_en_shell():
    fm = {"title": "T", "description": "D", "date": "May 19, 2026"}
    assert _article.render_translation("9999-01-01-no-such-article", fm, "Body.") is None


def test_render_one_lang_legacy_en_stem_and_unrenderable_post(tmp_path, monkeypatch):
    # A dated post whose stem is NOT in FR_TO_EN takes the legacy
    # EN-slug branch; render_translation returning None skips the page.
    src = tmp_path / "_posts" / "fr"
    src.mkdir(parents=True)
    (src / "2026-01-01-not-in-slug-map.md").write_text(
        '---\ntitle: "Legacy"\n---\nBody\n', encoding="utf-8"
    )
    out = tmp_path / "public" / "fr"
    out.mkdir(parents=True)
    real_bind = st.bind_lang

    def bind_then_repoint(code: str) -> None:
        real_bind(code)
        st.SRC = src
        st.OUT = out

    monkeypatch.setattr(st, "bind_lang", bind_then_repoint)
    monkeypatch.setattr(_run, "render_translation", lambda en, fm, body: None)
    monkeypatch.setattr(_run, "render_home", lambda: None)
    monkeypatch.setattr(_run, "write_static_translations", lambda: 0)
    monkeypatch.setattr(_run, "_build_fr_search_index", lambda: [])
    assert _run._render_one_lang("fr") == 0
    assert (out / "search-index.json").is_file()


def test_render_static_translation_unknown_slug_returns_none():
    assert bt.render_static_translation("__not-a-static-page__") is None


# ---------------------------------------------------------------------------
# _article — lead / takeaway derivation edge cases
# ---------------------------------------------------------------------------


def test_french_lead_fallback_empty_and_nonempty():
    assert _article._french_lead_fallback("") == ""
    out = _article._french_lead_fallback("Une description.")
    assert "TL;DR" in out
    assert "Une description." in out


def test_collect_paragraph_skips_and_breaks_on_link_definitions():
    # Leading link-definition is skipped; one inside a paragraph ends it.
    lines = ["[1]: https://example.com", "Première phrase.", "[2]: https://example.org", "Suite."]
    assert _article._collect_paragraph(lines, 0) == ["Première phrase."]


def test_french_body_uses_shell_lead_when_no_takeaways():
    out = _article._french_body("<p>corps</p>", "desc", "<aside>EN LEAD</aside>", "", body_md="")
    assert "EN LEAD" in out
    # And the fallback path when no shell lead either:
    out2 = _article._french_body("<p>corps</p>", "desc", "", "", body_md="")
    assert "TL;DR" in out2


def test_derive_fr_takeaways_h2_then_h3():
    md = (
        "## Introduction\n\nGeneric — skipped.\n\n"
        "## Vrai sujet\n\nPremière **phrase** du sujet. Deuxième.\n\n"
        "### Sous-sujet\n\nDétail [lien](https://x) ici.\n"
    )
    out = _article._derive_fr_takeaways(md)
    assert ("Vrai sujet", "Première phrase du sujet.") in out
    assert any(h == "Sous-sujet" for h, _ in out)


# ---------------------------------------------------------------------------
# _maps — empty-state and miss branches
# ---------------------------------------------------------------------------


def test_build_en_url_rewriter_empty_map(monkeypatch):
    monkeypatch.setattr(st, "EN_TO_FR", {})
    assert _maps._build_en_url_rewriter().search("/anything/") is None


def test_map_builders_with_missing_src_dir(monkeypatch):
    monkeypatch.setattr(st, "SRC", Path("_posts/__no-such-lang__"))
    assert _maps._build_fr_title_map() == {}
    assert _maps._build_fr_description_map() == {}
    assert _maps._build_fr_excerpt_map() == {}
    assert _maps._build_fr_eyebrow_map() == {}


def test_en_subst_passes_with_no_posts(tmp_path, monkeypatch):
    # No _posts/ in cwd → empty desc/title tables → passthrough branches.
    monkeypatch.chdir(tmp_path)
    st.bind_lang("fr")  # clear the lazy caches
    html = "<p>untouched</p>"
    assert _maps.rewrite_en_descs_in_text(html) == html
    assert _maps.rewrite_en_titles_in_text(html) == html
    st.bind_lang("fr")


def test_en_subst_passes_skip_posts_without_fields(tmp_path, monkeypatch):
    posts = tmp_path / "_posts"
    posts.mkdir()
    (posts / "2026-01-01-no-fields.md").write_text("---\nlayout: post\n---\nbody\n")
    monkeypatch.chdir(tmp_path)
    st.bind_lang("fr")
    html = "<p>untouched</p>"
    assert _maps.rewrite_en_descs_in_text(html) == html
    assert _maps.rewrite_en_titles_in_text(html) == html
    st.bind_lang("fr")


def test_en_subst_passes_skip_posts_without_fr_mapping(tmp_path, monkeypatch):
    # EN post has title + description but no FR counterpart exists, so
    # the FR lookup misses and the post is skipped from both maps.
    posts = tmp_path / "_posts"
    posts.mkdir()
    (posts / "2026-01-01-unmapped.md").write_text(
        '---\ntitle: "Unmapped Title"\ndescription: "Unmapped desc"\n---\nbody\n',
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    st.bind_lang("fr")  # clear the lazy caches
    html = "<p>untouched</p>"
    assert _maps.rewrite_en_descs_in_text(html) == html
    assert _maps.rewrite_en_titles_in_text(html) == html
    st.bind_lang("fr")


def test_rewrite_fr_link_titles_missing_title_passthrough(monkeypatch):
    fr = next(iter(st.FR_TO_EN))
    html = f'<a href="/fr/{fr}/" title="EN">x</a>'
    # Non-empty title map that lacks this article → return-original branch.
    st._FR_TITLE_MAP.clear()
    st._FR_TITLE_MAP["__sentinel__"] = "x"
    try:
        assert _maps.rewrite_fr_link_titles(html) == html
    finally:
        st._FR_TITLE_MAP.clear()


def test_rewrite_newsroom_card_unknown_slug_passthrough():
    # Slug matches the href grammar but has no EN counterpart.
    html = (
        '<article class="newsroom-card"><a href="/fr/zz-unknown-slug/">x</a>'
        '<h3><a href="/fr/zz-unknown-slug/">T</a></h3></article>'
    )
    assert _maps.rewrite_newsroom_card_titles(html) == html
    # And a card with no article href at all.
    no_href = '<article class="newsroom-card"><p>no link</p></article>'
    assert _maps.rewrite_newsroom_card_titles(no_href) == no_href


def test_rewrite_related_card_unknown_and_untitled_slugs():
    unknown = '<article class="related-card"><a href="/fr/zz-unknown-slug/">x</a></article>'
    assert _maps.rewrite_related_card_titles(unknown) == unknown
    fr = next(iter(st.FR_TO_EN))
    known = f'<article class="related-card"><a href="/fr/{fr}/">x</a></article>'
    st._FR_TITLE_MAP.clear()
    st._FR_TITLE_MAP["__sentinel__"] = "x"
    try:
        assert _maps.rewrite_related_card_titles(known) == known
    finally:
        st._FR_TITLE_MAP.clear()


# ---------------------------------------------------------------------------
# _pages — shell-missing and JSON-LD branches
# ---------------------------------------------------------------------------


def test_render_articles_hub_without_shell_or_entries(monkeypatch, tmp_path):
    monkeypatch.setattr(st, "PUBLIC", tmp_path)
    assert bt.render_articles_hub([{"slug": "x"}]) is None  # no shell
    (tmp_path / "articles").mkdir()
    (tmp_path / "articles" / "index.html").write_text("<html><body></body></html>")
    assert bt.render_articles_hub([]) is None  # no entries


def test_render_home_without_shell(monkeypatch, tmp_path):
    monkeypatch.setattr(st, "PUBLIC", tmp_path)
    assert bt.render_home() is None


HOME_SHELL = (
    '<html lang="en-GB"><head><title>EN</title>'
    '<script type="application/ld+json">'
    '{"@graph":[{"@type":"WebSite","url":"https://sebastienrousseau.com/",'
    '"name":"EN","description":"EN d","inLanguage":"en-GB"},'
    '{"@type":"WebPage","url":"https://sebastienrousseau.com/",'
    '"name":"EN","description":"EN d","inLanguage":"en-GB"}]}'
    "</script></head><body><main></main></body></html>"
)


def test_render_home_patches_website_and_webpage_jsonld(monkeypatch, tmp_path):
    (tmp_path / "index.html").write_text(HOME_SHELL)
    monkeypatch.setattr(st, "PUBLIC", tmp_path)
    out = bt.render_home()
    assert out is not None
    assert '"url":"https://sebastienrousseau.com/fr/"' in out
    assert out.count('"inLanguage":"fr"') == 2
    assert 'hreflang="x-default"' in out


STATIC_SHELL = (
    '<html lang="en-GB"><head><title>EN</title>'
    '<script type="application/ld+json">'
    '{"@type":"BreadcrumbList","itemListElement":['
    '{"@type":"ListItem","position":1,"name":"Home","item":"https://sebastienrousseau.com/"},'
    '{"@type":"ListItem","position":2,"name":"About","item":"https://sebastienrousseau.com/about/"},'
    "null]}"
    "</script></head><body><main></main></body></html>"
)


def test_render_static_translation_breadcrumb_with_non_dict_item(monkeypatch, tmp_path):
    (tmp_path / "about").mkdir()
    (tmp_path / "about" / "index.html").write_text(STATIC_SHELL)
    monkeypatch.setattr(st, "PUBLIC", tmp_path)
    out = bt.render_static_translation("about")
    assert out is not None
    assert '"name":"Accueil"' in out
    assert "null" in out  # the non-dict item is preserved untouched


def test_write_static_translations_topic_subpages(monkeypatch, tmp_path, capsys):
    topics = tmp_path / "topics"
    (topics / "empty-topic").mkdir(parents=True)  # no index.html → skipped
    (topics / "some-topic").mkdir()
    (topics / "some-topic" / "index.html").write_text(
        '<html lang="en-GB"><head><title>EN</title>'
        '<script type="application/ld+json">'
        '{"@type":"BreadcrumbList","itemListElement":[null,'
        '{"@type":"ListItem","position":1,"name":"Home","item":"https://sebastienrousseau.com/"},'
        '{"@type":"ListItem","position":2,"name":"Topics","item":"https://sebastienrousseau.com/topics/"},'
        '{"@type":"ListItem","position":3,"name":"Some Topic","item":"https://sebastienrousseau.com/topics/some-topic/"}]}'
        "</script></head><body><main><h1>Some Topic</h1></main></body></html>"
    )
    (topics / "stray-file.txt").write_text("not a dir")
    monkeypatch.setattr(st, "PUBLIC", tmp_path)
    monkeypatch.setattr(st, "OUT", tmp_path / "fr")
    n = bt.write_static_translations()
    assert n == 1  # only the topic sub-page with a shell got written
    rendered = (tmp_path / "fr" / "sujets" / "some-topic" / "index.html").read_text()
    assert '"name":"Sujets"' in rendered
    assert "skip static" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# _chrome — breadcrumb items not a list
# ---------------------------------------------------------------------------


def test_swap_breadcrumb_item_list_not_a_list():
    html = (
        '<script type="application/ld+json">'
        '{"@type":"BreadcrumbList","itemListElement":"oops"}'
        "</script>"
    )
    assert _chrome._swap_breadcrumb(html, "s", "t") == html


# ---------------------------------------------------------------------------
# _run — skip-no-title branch
# ---------------------------------------------------------------------------


def test_render_one_lang_skips_posts_without_title(monkeypatch, tmp_path, capsys):
    src = tmp_path / "_posts" / "fr"
    src.mkdir(parents=True)
    (tmp_path / "out").mkdir()  # the driver assumes OUT exists (build.sh order)
    (src / "2026-01-01-untitled.md").write_text("---\nlayout: post\n---\nbody\n")
    (src / "not-dated.md").write_text('---\ntitle: "x"\n---\nbody\n')
    real_bind = st.bind_lang

    def bind_then_redirect(code: str) -> None:
        real_bind(code)
        st.SRC = src
        st.OUT = tmp_path / "out"
        st.PUBLIC = tmp_path  # no EN shells → home/static all skip

    monkeypatch.setattr(st, "bind_lang", bind_then_redirect)
    monkeypatch.setattr(st, "PUBLIC", tmp_path)
    written = _run._render_one_lang("fr")
    out = capsys.readouterr().out
    assert "skip 2026-01-01-untitled — no title" in out
    assert written == 0
    assert (tmp_path / "out" / "search-index.json").is_file()


def test_main_module_entrypoint_importable():
    import importlib

    mod = importlib.import_module("build_translations.__main__")
    assert callable(mod.main)


# ---------------------------------------------------------------------------
# Package surface — the smoke-test import contract
# ---------------------------------------------------------------------------


def test_public_api_names_resolve():
    for name in (
        "parse_frontmatter",
        "render_translation",
        "fr_slug",
        "render_static_translation",
        "render_articles_hub",
        "render_home",
        "main",
    ):
        assert callable(getattr(bt, name)), name


def test_parse_frontmatter_is_canonical():
    import _frontmatter

    assert bt.parse_frontmatter is _frontmatter.parse_frontmatter
