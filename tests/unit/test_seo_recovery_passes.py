# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Unit coverage for the v0.0.30 SEO passes on hand-made fixtures:
locale indexing, unique head metadata, sitemap lastmod and the Worker
redirect map."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
sys.path.insert(0, str(ROOT / "scripts" / "postbuild"))
sys.path.insert(0, str(ROOT / "scripts"))

import _locale_indexing as li
import build_worker_assets as bwa
from postbuild_lib import locale_indexing as lx
from postbuild_lib import sitemap_lastmod as sl
from postbuild_lib import unique_meta as um

SITE = "https://sebastienrousseau.com"


# -- Policy -----------------------------------------------------------------


def test_policy_keeps_english_and_ten_locales() -> None:
    assert li.indexed_codes() == frozenset(
        {"en", "zh-hans", "zh-hant", "fr", "ko", "es", "ru", "ja", "it", "cs", "de"}
    )
    assert len(li.noindex_codes()) == 24
    assert {"ar", "pt-br", "yo"} <= set(li.noindex_codes())
    assert {"pt-br", "pt-BR".lower(), "ar-sa"} <= li.noindex_hreflangs()


@pytest.mark.parametrize(
    ("codes", "message"), [(["en", "xx"], "inactive"), (["fr"], "must index 'en'")]
)
def test_policy_rejects_unknown_locale_or_missing_english(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, codes: list[str], message: str
) -> None:
    policy = tmp_path / "policy.json"
    policy.write_text(json.dumps({"indexed": codes}), encoding="utf-8")
    monkeypatch.setattr(li, "POLICY", policy)
    li.indexed_codes.cache_clear()
    try:
        with pytest.raises(li.LocaleIndexingError, match=message):
            li.indexed_codes()
    finally:
        li.indexed_codes.cache_clear()


# -- Locale indexing ----------------------------------------------------------

_SSG = '<meta name="robots" content="max-snippet:-1, max-image-preview:large">'


def test_merge_noindex_keeps_snippet_directives_in_one_tag() -> None:
    out = lx.merge_noindex(f"<html><head>{_SSG}<title>x</title></head></html>")
    assert out.count('name="robots"') == 1
    assert 'content="noindex, follow, max-snippet:-1, max-image-preview:large"' in out


def test_merge_noindex_collapses_several_tags_and_keeps_nofollow() -> None:
    html = (
        '<head><meta name="robots" content="index, follow">'
        "<meta content=nofollow name=robots></head>"
    )
    out = lx.merge_noindex(html)
    assert out == '<head><meta name="robots" content="noindex, nofollow"></head>'


def test_merge_noindex_adds_a_tag_when_none_exists_and_is_idempotent() -> None:
    out = lx.merge_noindex("<html><head><title>x</title></head></html>")
    assert out.startswith('<html><head><meta name="robots" content="noindex, follow">')
    assert lx.merge_noindex(out) == out
    assert lx.merge_noindex("<p>no head</p>") == "<p>no head</p>"


_ALTS = (
    '<link rel="alternate" hreflang="en" href="https://sebastienrousseau.com/a/">'
    '<link rel="alternate" hreflang="fr" href="https://sebastienrousseau.com/fr/a/">'
    '<link rel="alternate" hreflang="ar" href="https://sebastienrousseau.com/ar/a/">'
    '<link rel="alternate" hreflang="pt-BR" href="/pt-br/a/">'
    '<link rel="alternate" hreflang="x-default" href="https://sebastienrousseau.com/a/">'
)


def test_strip_hreflang_on_an_indexed_page_drops_only_noindex_targets() -> None:
    out, removed = lx.strip_hreflang(_ALTS, drop_all=False, dropped=li.noindex_codes())
    assert removed == 2
    assert 'hreflang="fr"' in out and 'hreflang="x-default"' in out
    assert "/ar/" not in out and "pt-br" not in out


def test_strip_hreflang_on_a_noindex_page_drops_everything() -> None:
    out, removed = lx.strip_hreflang(_ALTS, drop_all=True, dropped=li.noindex_codes())
    assert (out, removed) == ("", 5)


def test_page_locale() -> None:
    codes = frozenset({"fr", "pt-br"})
    assert lx.page_locale("pt-br/x/index.html", codes) == "pt-br"
    assert lx.page_locale("index.html", codes) == "en"
    assert lx.page_locale("about/index.html", codes) == "en"


def test_apply_locale_indexing_on_a_tree(tmp_path: Path) -> None:
    head = f"<html><head>{_SSG}{_ALTS}</head></html>"
    for rel in ("a/index.html", "fr/a/index.html", "ar/a/index.html"):
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_text(head, encoding="utf-8")
    assert lx.apply_locale_indexing(tmp_path) == (1, 2 + 2 + 5)
    assert "noindex" in (tmp_path / "ar/a/index.html").read_text()
    assert "noindex" not in (tmp_path / "fr/a/index.html").read_text()
    assert lx.apply_locale_indexing(tmp_path) == (0, 0)


# -- Unique titles and descriptions --------------------------------------------


def _write_page(root: Path, rel: str, title: str, desc: str, extra: str = "") -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f'<html><head><title>{title}</title><meta name="description" content="{desc}">'
        f'<meta property="og:title" content="{title}"><meta content="{desc}" '
        f"name=twitter:description>{extra}</head><body></body></html>",
        encoding="utf-8",
    )
    return path


def test_paged_listing_gets_localised_page_label_and_site_name(tmp_path: Path) -> None:
    root = tmp_path
    for n in (2, 3):
        _write_page(
            root, f"de/artikel/page/{n}/index.html", "Artikel", f"Alle Artikel. Page {n} of 3."
        )
    entries = [
        (root / f"de/artikel/page/{n}/index.html", f"de/artikel/page/{n}/index.html", "de", True)
        for n in (2, 3)
    ]
    assert um.make_unique(entries) == 2
    html = (root / "de/artikel/page/2/index.html").read_text()
    assert "<title>Artikel · Seite 2 von 3 · Sebastien Rousseau</title>" in html
    assert 'og:title" content="Artikel · Seite 2 von 3 · Sebastien Rousseau"' in html
    assert 'content="Artikel: Alle Artikel. Seite 2 von 3." name=twitter:description' in html


def test_cross_locale_collision_gets_native_language_name(tmp_path: Path) -> None:
    a = _write_page(tmp_path, "cs/kontakt/index.html", "Kontakt — Sebastien Rousseau", "K.")
    b = _write_page(tmp_path, "de/kontakt/index.html", "Kontakt — Sebastien Rousseau", "K.")
    um.make_unique(
        [(a, "cs/kontakt/index.html", "cs", True), (b, "de/kontakt/index.html", "de", True)]
    )
    assert "<title>Kontakt — Sebastien Rousseau · Čeština</title>" in a.read_text()
    assert "<title>Kontakt — Sebastien Rousseau · Deutsch</title>" in b.read_text()
    assert 'content="K. (Deutsch)"' in b.read_text()


def test_same_locale_collision_gets_publication_date_or_slug(tmp_path: Path) -> None:
    date = '<meta itemprop="datePublished" content="Sun, 26 Jul 2026 07:07:07 +0000" id="date" />'
    a = _write_page(tmp_path, "2026-07-26-truth/index.html", "Truth", "D1", date)
    b = _write_page(tmp_path, "about-x/index.html", "Truth", "D2")
    c = _write_page(tmp_path, "noindex/index.html", "Truth", "D3")
    um.make_unique(
        [
            (a, "2026-07-26-truth/index.html", "en", True),
            (b, "about-x/index.html", "en", True),
            (c, "noindex/index.html", "en", False),
        ]
    )
    assert "<title>Truth · 2026-07-26</title>" in a.read_text()
    assert "<title>Truth · about-x</title>" in b.read_text()
    assert "<title>Truth</title>" in c.read_text(), "non-indexable pages are left alone"


def test_unique_meta_helpers() -> None:
    assert um.page_label("xx-none") == "Page {page} of {total}"
    assert um.is_listing("articles/2025/index.html", "en")
    assert um.is_listing("fr/articles/page/2/index.html", "fr")
    assert not um.is_listing("index.html", "en")
    assert not um.is_listing("about/index.html", "en")
    assert um.read_description("<meta name=description content='a &amp; b'>") == "a & b"
    assert um.read_description("<title>x</title>") == ""
    assert um._iso_date("garbage-date") == "garbage-da"
    assert um.load_page(Path(__file__).with_name("conftest.py"), "x", "en", True) is None
    page = um.Page(Path("x"), "x/index.html", "en", "T", "D", True)
    um._append(page, "title", "")
    assert (page.title, page.changed) == ("T", set())


# -- Sitemap lastmod --------------------------------------------------------------


def _sitemap(root: Path, paths: list[str], lastmod: str = "2026-05-11") -> None:
    blocks = "".join(
        f"<url>\n  <loc>{SITE}{p}</loc>\n  <lastmod>{lastmod}</lastmod>\n</url>\n" for p in paths
    )
    (root / "sitemap.xml").write_text(f"<urlset>\n{blocks}</urlset>\n", encoding="utf-8")


def test_lastmod_uses_source_then_listing_then_nothing(tmp_path: Path) -> None:
    root = tmp_path
    paths = ["/", "/2026-01-02-a/", "/2026-03-04-b/", "/tags/x/", "/about/", "/mystery/"]
    _sitemap(root, paths)
    _write_page(root, "tags/x/index.html", "X", "x", '<a href="/2026-01-02-a/">a</a>')
    _write_page(root, "index.html", "Home", "h", f'<a href="{SITE}/2026-03-04-b/">b</a>')
    index = {"2026-01-02-a": "2026-02-01", "2026-03-04-b": "2026-03-04", "about": "2026-05-14"}
    index["index"] = "2026-01-01"
    assert sl.refresh_lastmod(root, index) == (5, 1)
    xml = (root / "sitemap.xml").read_text()
    for path, date in (
        ("/", "2026-03-04"),
        ("/2026-01-02-a/", "2026-02-01"),
        ("/tags/x/", "2026-02-01"),
        ("/about/", "2026-05-14"),
    ):
        assert f"<loc>{SITE}{path}</loc>\n  <lastmod>{date}</lastmod>" in xml
    assert f"<loc>{SITE}/mystery/</loc>\n</url>" in xml
    assert "2026-05-11" not in xml


def test_lastmod_helpers() -> None:
    codes = frozenset({"fr"})
    assert sl.url_path(SITE) == "/"
    assert sl.url_path("https://elsewhere.example/x/") is None
    assert sl.split_locale("/fr/a/", codes) == ("fr", ["a"])
    assert sl.source_date("/a/b/", {"a": "2026-01-01"}, codes) == ""


def test_lastmod_skips_a_listing_that_was_not_built(tmp_path: Path) -> None:
    assert sl.compute_lastmods(tmp_path, ["/tags/gone/"], {}) == {}


# -- Worker redirect map -------------------------------------------------------------


def _stub(root: Path, rel: str, target: str) -> None:
    path = root / rel / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f'<html><head><meta http-equiv="refresh" content="0; url={target}" /></head></html>',
        encoding="utf-8",
    )


def test_stub_redirects_and_chain_collapse(tmp_path: Path) -> None:
    _stub(tmp_path, "zh-hant/old", f"{SITE}/zh-hant/mid/")
    _stub(tmp_path, "zh-hant/mid", "/zh-hant/new/")
    (tmp_path / "zh-hant/new").mkdir(parents=True)
    (tmp_path / "zh-hant/new/index.html").write_text("<html><head></head></html>")
    found = bwa.stub_redirects(tmp_path)
    assert found == {"/zh-hant/old/": "/zh-hant/mid/", "/zh-hant/mid/": "/zh-hant/new/"}
    assert bwa.collapse_chains(found) == {
        "/zh-hant/old/": "/zh-hant/new/",
        "/zh-hant/mid/": "/zh-hant/new/",
    }


def test_redirect_loop_and_offsite_target_raise(tmp_path: Path) -> None:
    with pytest.raises(bwa.RedirectMapError, match="loop"):
        bwa.collapse_chains({"/a/": "/b/", "/b/": "/a/"})
    _stub(tmp_path, "x", "https://evil.example/")
    with pytest.raises(bwa.RedirectMapError, match="not on"):
        bwa.stub_redirects(tmp_path)


def test_emit_redirects_writes_sorted_map_or_skips_unbuilt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(bwa, "OUT_DIR", tmp_path / "assets")
    (tmp_path / "assets").mkdir()
    assert bwa.emit_redirects(tmp_path / "missing") is None
    public = tmp_path / "public"
    _stub(public, "b", "/c/")
    _stub(public, "a", "/c/")
    (public / "index.html").write_text("<html></html>")
    out = bwa.emit_redirects(public)
    assert out is not None
    assert json.loads(out.read_text()) == {"version": 1, "redirects": {"/a/": "/c/", "/b/": "/c/"}}
