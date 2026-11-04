# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Pillar-hub links and redirect-stub link repair (plan item 2.5).

The v0.0.31 build had no article linking to its pillar hub, and 41 article
pages linking to a meta-refresh stub (two of them across locales)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
sys.path.insert(0, str(ROOT / "scripts" / "postbuild"))

from postbuild_lib import hub_links as hl

# A real English post (tags lead with "EU Data Act" -> pillar "policy") and
# its real French and Japanese translations, so the slug maps resolve.
EN_STEM = "2026-08-04-data-act-cloud-switching-dora-exit-strategies-2026"
FR_STEM = "2026-08-04-votre-plan-de-sortie-dora-ete"
BLOG = '<script type="application/ld+json">{"@type":"BlogPosting"}</script>'
CLUSTER = (
    '<nav class="cluster-links" aria-labelledby="cluster-links-heading">'
    '<h2 id="cluster-links-heading">Related</h2><ul class="cluster-links-list"></ul></nav>'
)


def _page(lang: str, path: str, body: str = CLUSTER) -> str:
    return (
        f'<html lang="{lang}"><head>'
        f'<link rel="canonical" href="https://sebastienrousseau.com{path}">'
        f"</head><body><main><article><p>Body.</p>{body}</article></main>{BLOG}</body></html>"
    )


@pytest.fixture
def public(tmp_path: Path) -> Path:
    for prefix in ("", "fr/", "ja/"):
        hub = tmp_path / f"{prefix}categories" / "policy" / "index.html"
        hub.parent.mkdir(parents=True)
        hub.write_text("<html></html>", encoding="utf-8")
    return tmp_path


# ---------------------------------------------------------------------------
# inject_pillar_hub_link
# ---------------------------------------------------------------------------


def test_english_article_links_its_pillar_hub_inside_the_cluster_block(public: Path) -> None:
    out = hl.inject_pillar_hub_link(_page("en-GB", f"/{EN_STEM}/"), public)
    hub = (
        '<p class="cluster-links-hub">Category: '
        '<a href="/categories/policy/">Policy &amp; resilience</a></p></nav>'
    )
    assert hub in out


def test_locale_article_links_the_locale_hub_in_its_own_words(public: Path) -> None:
    out = hl.inject_pillar_hub_link(_page("fr", f"/fr/{FR_STEM}/"), public)
    assert (
        '<p class="cluster-links-hub">Catégorie&#160;: '
        '<a href="/fr/categories/policy/">Politique &amp; résilience</a></p>'
    ) in out


def test_cjk_locale_uses_a_full_width_separator(public: Path) -> None:
    ja = hl._slug_maps("ja")["articles_en_to_lang"][EN_STEM]
    out = hl.inject_pillar_hub_link(_page("ja", f"/ja/{ja}/"), public)
    assert '：<a href="/ja/categories/policy/">' in out


def test_without_a_cluster_block_the_link_closes_the_article(public: Path) -> None:
    out = hl.inject_pillar_hub_link(_page("en-GB", f"/{EN_STEM}/", body=""), public)
    assert '<a href="/categories/policy/">Policy &amp; resilience</a></p></article>' in out


def test_no_body_close_and_no_cluster_block_is_a_no_op(public: Path) -> None:
    html = _page("en-GB", f"/{EN_STEM}/", body="").replace("</article></main>", "")
    assert hl.inject_pillar_hub_link(html, public) == html


def test_missing_hub_page_is_a_no_op(tmp_path: Path) -> None:
    html = _page("en-GB", f"/{EN_STEM}/")
    assert hl.inject_pillar_hub_link(html, tmp_path) == html


def test_article_without_a_pillar_is_a_no_op(public: Path) -> None:
    html = _page("en-GB", "/2099-01-01-no-such-post/")
    assert hl.inject_pillar_hub_link(html, public) == html


def test_non_article_pages_are_left_alone(public: Path) -> None:
    html = _page("en-GB", f"/{EN_STEM}/").replace(BLOG, "")
    assert hl.inject_pillar_hub_link(html, public) == html


def test_pillar_hub_link_is_idempotent(public: Path) -> None:
    once = hl.inject_pillar_hub_link(_page("en-GB", f"/{EN_STEM}/"), public)
    assert hl.inject_pillar_hub_link(once, public) == once


def test_pillar_copy_falls_back_to_english(monkeypatch: pytest.MonkeyPatch) -> None:
    real = hl.load_listings

    def fake(code: str) -> dict:
        if code == "xx":
            raise hl.LanguageError("no listings")
        if code == "yy":
            return {"ui": {}, "pillars": {}}
        return real(code)

    monkeypatch.setattr(hl, "load_listings", fake)
    assert hl._pillar_copy("xx", "ai") == ("Category", "Applied AI")
    assert hl._pillar_copy("yy", "payments") == ("Category", "Payments & money")


# ---------------------------------------------------------------------------
# Redirect-stub links
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("url", "key"),
    [
        ("/papers/", "/papers/"),
        ("/papers", "/papers/"),
        ("/papers/index.html", "/papers/"),
        ("https://sebastienrousseau.com/papers/", "/papers/"),
        ("https://sebastienrousseau.com", "/"),
        ("https://example.com/papers/", None),
        ("//example.com/papers/", None),
        ("", None),
    ],
)
def test_stub_key(url: str, key: str | None) -> None:
    assert hl._stub_key(url) == key


def test_localise_target_maps_english_articles_into_the_page_locale() -> None:
    assert hl.localise_target(f"/{EN_STEM}/", "fr") == f"/fr/{FR_STEM}/"
    assert hl.localise_target(f"/{EN_STEM}/", "en") == f"/{EN_STEM}/"
    assert hl.localise_target("/research/", "fr") == "/research/"
    assert hl.localise_target("/2099-01-01-untranslated/", "fr") == "/2099-01-01-untranslated/"


def test_localise_target_survives_a_missing_slug_map(monkeypatch: pytest.MonkeyPatch) -> None:
    def boom(lang: str) -> dict:
        raise FileNotFoundError(lang)

    monkeypatch.setattr(hl, "_slug_maps", boom)
    assert hl.localise_target(f"/{EN_STEM}/", "fr") == f"/{EN_STEM}/"


REDIRECTS = {"/papers/": "/research/", "/2026-old-slug/": f"/{EN_STEM}/"}


def test_rewrite_stub_links_points_anchors_at_the_final_target() -> None:
    html = (
        '<a class="x" href="/papers/#faq">P</a>'
        '<a href="https://sebastienrousseau.com/2026-old-slug">A</a>'
        '<a href="/research/">R</a>'
        '<link rel="alternate" href="/papers/">'
    )
    out, count = hl.rewrite_stub_links(html, "fr", REDIRECTS)
    assert count == 2
    assert '<a class="x" href="/research/#faq">P</a>' in out
    assert f'<a href="/fr/{FR_STEM}/">A</a>' in out
    assert '<a href="/research/">R</a>' in out
    assert '<link rel="alternate" href="/papers/">' in out


def test_rewrite_stub_links_without_stubs_is_unchanged() -> None:
    html = '<a href="/research/">R</a><a href="mailto:x@y">M</a>'
    assert hl.rewrite_stub_links(html, "en", REDIRECTS) == (html, 0)


def _stub(target: str) -> str:
    return (
        f'<html lang="en-GB"><head><meta http-equiv="refresh" content="0; url={target}" />'
        f'</head><body><a href="/papers/">self</a></body></html>'
    )


def test_repair_stub_links_rewrites_pages_but_never_the_stubs(tmp_path: Path) -> None:
    (tmp_path / "papers").mkdir()
    stub = tmp_path / "papers" / "index.html"
    stub.write_text(_stub("https://sebastienrousseau.com/research/"), encoding="utf-8")
    linking = tmp_path / "index.html"
    linking.write_text('<html lang="en-GB"><a href="/papers/">P</a></html>', encoding="utf-8")
    plain = tmp_path / "about.html"
    plain.write_text('<html lang="en-GB"><a href="/about/">A</a></html>', encoding="utf-8")

    assert hl.repair_stub_links(tmp_path) == 1
    assert '<a href="/research/">P</a>' in linking.read_text(encoding="utf-8")
    assert stub.read_text(encoding="utf-8") == _stub("https://sebastienrousseau.com/research/")
    assert hl.repair_stub_links(tmp_path) == 0


def test_repair_stub_links_without_stubs_does_nothing(tmp_path: Path) -> None:
    (tmp_path / "index.html").write_text('<a href="/papers/">P</a>', encoding="utf-8")
    assert hl.repair_stub_links(tmp_path) == 0
