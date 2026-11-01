# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Unit coverage for postbuild_lib.indexability: utility pages are noindex
and sitemaps list only indexable, self-canonical URLs."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "postbuild"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "lib"))

from postbuild_lib import indexability as ix

_BASE = "https://sebastienrousseau.com"
_SSG_ROBOTS = '<meta name="robots" content="max-snippet:-1, max-image-preview:large">'


def _page(path: str, head: str = _SSG_ROBOTS, canonical: str | None = None) -> str:
    canon = canonical if canonical is not None else f"{_BASE}{path}"
    return (
        f'<!DOCTYPE html><html><head>{head}<link rel="canonical" href="{canon}">'
        "</head><body><main>x</main></body></html>"
    )


def _write(public: Path, path: str, html: str) -> None:
    target = public / path.lstrip("/") / "index.html" if path.endswith("/") else public / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")


@pytest.fixture
def public(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(ix, "_all_active_non_en_langs", lambda: ["de", "fr"])
    slugs = {
        "de": {"static": {"404": "404", "offline": "offline", "thanks": "danke"}},
        "fr": {"static": {"404": "404", "offline": "hors-ligne"}},
    }
    monkeypatch.setattr(ix._lr, "load_slugs", lambda code: slugs[code])
    root = tmp_path / "public"
    for path in ("/", "/404/", "/offline/", "/de/404/", "/de/danke/", "/fr/hors-ligne/"):
        _write(root, path, _page(path))
    return root


def test_utility_pages_follow_each_locale_static_slug(public: Path) -> None:
    got = {p.relative_to(public).as_posix() for p in ix.utility_pages(public)}
    assert got == {
        "404/index.html",
        "offline/index.html",
        "de/404/index.html",
        "de/danke/index.html",
        "fr/hors-ligne/index.html",
    }


def test_set_noindex_replaces_every_robots_meta() -> None:
    html = f'<html><head>{_SSG_ROBOTS}<meta name="robots" content="index"></head></html>'
    out = ix.set_noindex(html)
    assert out.count('name="robots"') == 1
    assert ix.NOINDEX_META in out


def test_set_noindex_inserts_when_absent_and_skips_headless() -> None:
    assert ix.set_noindex("<html><head></head></html>") == (
        f"<html><head>{ix.NOINDEX_META}</head></html>"
    )
    assert ix.set_noindex("<p>no head</p>") == "<p>no head</p>"


def test_apply_noindex_is_idempotent(public: Path) -> None:
    assert ix.apply_noindex_utility_pages(public) == 5
    assert ix.NOINDEX_META in (public / "de" / "404" / "index.html").read_text()
    assert ix.NOINDEX_META not in (public / "index.html").read_text()
    assert ix.apply_noindex_utility_pages(public) == 0


def test_is_indexable_rules(public: Path) -> None:
    _write(public, "/moved/", '<html><head><meta http-equiv="refresh" content="0; url=/"></head>')
    _write(public, "/dup/", _page("/dup/", canonical=f"{_BASE}/other/"))
    _write(public, "/feed.xml", "<rss/>")
    ix.apply_noindex_utility_pages(public)
    assert ix.is_indexable(f"{_BASE}/", public)
    assert ix.is_indexable(_BASE, public)
    assert ix.is_indexable(f"{_BASE}/feed.xml", public)
    assert not ix.is_indexable(f"{_BASE}/404/", public)
    assert not ix.is_indexable(f"{_BASE}/moved/", public)
    assert not ix.is_indexable(f"{_BASE}/dup/", public)
    assert not ix.is_indexable(f"{_BASE}/missing/", public)
    assert not ix.is_indexable("https://example.com/", public)


def test_prune_sitemaps_keeps_only_indexable_urls(public: Path) -> None:
    ix.apply_noindex_utility_pages(public)
    locs = ("/", "/404/", "/de/danke/", "/gone/")
    body = "".join(f"<url><loc>{_BASE}{p}</loc></url>" for p in locs)
    (public / "sitemap.xml").write_text(f"<urlset>{body}</urlset>")
    (public / "de" / "news-sitemap.xml").write_text(
        f"<urlset><url><loc>{_BASE}/de/404/</loc></url></urlset>"
    )
    assert ix.prune_sitemaps(public) == 4
    sm = (public / "sitemap.xml").read_text()
    assert f"<loc>{_BASE}/</loc>" in sm
    assert "/404/" not in sm and "/danke/" not in sm and "/gone/" not in sm
    assert "<url>" not in (public / "de" / "news-sitemap.xml").read_text()
    assert ix.prune_sitemaps(public) == 0
