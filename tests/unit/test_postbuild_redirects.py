"""Unit coverage for postbuild_lib.redirects — the /papers -> /research
legacy-URL conversion (5-item nav re-architecture).

Covers: meta-refresh injection, canonical/og:url retargeting, hreflang
stripping, sitemap purge, locale-fork treatment via the slug maps, and
idempotency.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "postbuild"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "lib"))

from postbuild_lib.redirects import apply_redirect_pages

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
