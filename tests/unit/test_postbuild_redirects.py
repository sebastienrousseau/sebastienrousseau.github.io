"""Unit coverage for postbuild_lib.redirects — the /papers -> /research
legacy-URL conversion (5-item nav re-architecture).

Covers: meta-refresh injection, canonical/og:url retargeting, hreflang
stripping, sitemap purge, locale-fork treatment via the slug maps, and
idempotency.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "postbuild"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "lib"))

from postbuild_lib import redirects as _redirects
from postbuild_lib.redirects import (
    _article_redirect_pairs,
    apply_article_redirects,
    apply_redirect_pages,
)

_BASE = "https://sebastienrousseau.com"


def _page(url: str, hreflang: str = "") -> str:
    return (
        "<!DOCTYPE html><html><head>"
        f'<link rel="canonical" href="{url}" />'
        f'<meta property="og:url" content="{url}" />'
        f"{hreflang}"
        "</head><body><main>old hub body</main></body></html>"
    )


def _hreflang_cluster() -> str:
    return (
        f'<link rel="alternate" hreflang="en" href="{_BASE}/papers/" />'
        f'<link rel="alternate" hreflang="fr" href="{_BASE}/fr/publications/" />'
        f'<link rel="alternate" hreflang="x-default" href="{_BASE}/papers/" />'
    )


def _make_tree(tmp_path: Path) -> Path:
    public = tmp_path / "public"
    en = public / "papers"
    fr = public / "fr" / "publications"
    en.mkdir(parents=True)
    fr.mkdir(parents=True)
    (en / "index.html").write_text(_page(f"{_BASE}/papers/", _hreflang_cluster()))
    (fr / "index.html").write_text(_page(f"{_BASE}/fr/publications/", _hreflang_cluster()))
    (public / "sitemap.xml").write_text(
        "<urlset>"
        f"<url>\n  <loc>{_BASE}/papers/</loc>\n</url>"
        f"<url>\n  <loc>{_BASE}/fr/publications/</loc>\n</url>"
        f"<url>\n  <loc>{_BASE}/research/</loc>\n</url>"
        "</urlset>"
    )
    return public


def test_en_page_becomes_redirect(tmp_path):
    public = _make_tree(tmp_path)
    converted, _purged = apply_redirect_pages(public)
    assert converted == 2
    html = (public / "papers" / "index.html").read_text()
    assert f'<meta http-equiv="refresh" content="0; url={_BASE}/research/" />' in html
    assert f'<link rel="canonical" href="{_BASE}/research/" />' in html
    assert f'<meta property="og:url" content="{_BASE}/research/" />' in html
    assert "hreflang=" not in html


def test_locale_fork_redirects_to_locale_target(tmp_path):
    public = _make_tree(tmp_path)
    apply_redirect_pages(public)
    html = (public / "fr" / "publications" / "index.html").read_text()
    assert f'content="0; url={_BASE}/fr/recherche/"' in html
    assert f'<link rel="canonical" href="{_BASE}/fr/recherche/" />' in html
    assert "hreflang=" not in html


def test_sitemap_purged_but_target_kept(tmp_path):
    public = _make_tree(tmp_path)
    _converted, purged = apply_redirect_pages(public)
    assert purged == 2
    sm = (public / "sitemap.xml").read_text()
    assert f"{_BASE}/papers/" not in sm
    assert f"{_BASE}/fr/publications/" not in sm
    assert f"{_BASE}/research/" in sm


def test_idempotent_second_run(tmp_path):
    public = _make_tree(tmp_path)
    apply_redirect_pages(public)
    first = (public / "papers" / "index.html").read_text()
    converted, purged = apply_redirect_pages(public)
    assert converted == 0
    assert purged == 0
    assert (public / "papers" / "index.html").read_text() == first
    # exactly one meta refresh tag, not stacked
    assert first.count("http-equiv=") == 1


def test_malformed_page_without_head_left_untouched(tmp_path):
    """Defensive branch: a rendered page with no <head> tag cannot take a
    meta refresh, so it is left byte-identical and not counted."""
    public = _make_tree(tmp_path)
    en = public / "papers" / "index.html"
    malformed = "<!DOCTYPE html><html><body><main>no head</main></body></html>"
    en.write_text(malformed)
    converted, _purged = apply_redirect_pages(public)
    assert converted == 1  # only the fr fork converts
    assert en.read_text() == malformed


def test_missing_pages_are_skipped(tmp_path):
    public = tmp_path / "public"
    public.mkdir()
    (public / "sitemap.xml").write_text("<urlset></urlset>")
    converted, purged = apply_redirect_pages(public)
    assert converted == 0
    assert purged == 0


# ---------------------------------------------------------------------------
# Retired article URLs (_data/redirects/articles.json).
#
# Distinct from the /papers -> /research case above: there the legacy page
# is still rendered and gets converted in place. Here the build stopped
# emitting the old path entirely, so the page has to be materialised from
# its target before the same conversion runs.
# ---------------------------------------------------------------------------


def _article_tree(tmp_path: Path) -> Path:
    """A tree with two live targets (EN + fr) and no legacy paths."""
    public = tmp_path / "public"
    for rel, url in (
        ("2024-01-08-new", f"{_BASE}/2024-01-08-new/"),
        ("fr/2024-01-08-nouveau", f"{_BASE}/fr/2024-01-08-nouveau/"),
    ):
        d = public / rel
        d.mkdir(parents=True)
        (d / "index.html").write_text(_page(url, _hreflang_cluster()))
    return public


@pytest.fixture
def _map(tmp_path, monkeypatch):
    """Point the module at a throwaway redirect map."""

    def _write(payload: dict) -> None:
        f = tmp_path / "articles.json"
        f.write_text(json.dumps(payload), encoding="utf-8")
        monkeypatch.setattr(_redirects, "ARTICLE_REDIRECTS", f)

    return _write


def test_retired_article_url_is_materialised(tmp_path, _map):
    public = _article_tree(tmp_path)
    _map({"_comment": "ignored", "en": {"2024-01-01-old": "2024-01-08-new"}})

    assert apply_article_redirects(public) == 1
    page = public / "2024-01-01-old" / "index.html"
    assert page.is_file()
    html = page.read_text()
    assert f'content="0; url={_BASE}/2024-01-08-new/"' in html
    assert f'href="{_BASE}/2024-01-08-new/"' in html
    assert "hreflang=" not in html


def test_locale_key_maps_under_its_prefix(tmp_path, _map):
    public = _article_tree(tmp_path)
    _map({"fr": {"2024-01-01-ancien": "2024-01-08-nouveau"}})

    assert apply_article_redirects(public) == 1
    html = (public / "fr" / "2024-01-01-ancien" / "index.html").read_text()
    assert f'content="0; url={_BASE}/fr/2024-01-08-nouveau/"' in html


def test_is_idempotent(tmp_path, _map):
    public = _article_tree(tmp_path)
    _map({"en": {"2024-01-01-old": "2024-01-08-new"}})

    assert apply_article_redirects(public) == 1
    before = (public / "2024-01-01-old" / "index.html").read_text()
    # A second pass must not rewrite the page — the byte-identical rebuild
    # job diffs two consecutive builds.
    assert apply_article_redirects(public) == 0
    assert (public / "2024-01-01-old" / "index.html").read_text() == before


def test_entry_with_missing_target_is_skipped(tmp_path, _map):
    """A stale map entry must not create a page pointing at a 404."""
    public = _article_tree(tmp_path)
    _map({"en": {"2024-01-01-old": "2099-01-01-never-published"}})

    assert apply_article_redirects(public) == 0
    assert not (public / "2024-01-01-old").exists()


def test_live_url_is_never_overwritten(tmp_path, _map):
    """If the source still renders it is content, not a legacy path."""
    public = _article_tree(tmp_path)
    live = public / "2024-01-08-new" / "index.html"
    original = live.read_text()
    _map({"en": {"2024-01-08-new": "2024-01-08-new"}})

    assert apply_article_redirects(public) == 0
    assert live.read_text() == original


def test_underscore_keys_are_not_treated_as_locales(tmp_path, _map):
    public = _article_tree(tmp_path)
    _map({"_comment": {"2024-01-01-old": "2024-01-08-new"}})

    assert _article_redirect_pairs(public) == []


def test_missing_map_file_is_not_an_error(tmp_path, monkeypatch):
    public = _article_tree(tmp_path)
    monkeypatch.setattr(_redirects, "ARTICLE_REDIRECTS", tmp_path / "absent.json")
    assert apply_article_redirects(public) == 0
