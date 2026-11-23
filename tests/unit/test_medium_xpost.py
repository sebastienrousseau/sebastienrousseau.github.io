# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""The "Also published on Medium" line and the publications data behind it."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
sys.path.insert(0, str(ROOT / "scripts" / "postbuild"))

import _medium
from postbuild_lib.medium_xpost import inject_medium_xpost

_SLUG = "2026-05-16-best-cloud-infrastructure-architecture-2026"


def _page(canonical: str, schema: str = '"@type":"BlogPosting"') -> str:
    return (
        f'<html><head><link rel="canonical" href="{canonical}">'
        f'<script>{{{schema}}}</script></head><body><main><div class="wrap">'
        "<p>Body</p></div></main></body></html>"
    )


def test_syndicated_english_article_gets_one_line() -> None:
    out = inject_medium_xpost(_page(f"https://sebastienrousseau.com/{_SLUG}/"))
    assert 'class="byline-strap medium-xpost"' in out
    assert "Also published in Banking On Cloud Native on" in out
    assert 'href="https://medium.com/p/7eeacfc00973"' in out
    assert out.index("medium-xpost") < out.index("</div></main>")
    assert inject_medium_xpost(out) == out


def test_index_html_canonical_resolves_the_slug() -> None:
    out = inject_medium_xpost(_page(f"https://sebastienrousseau.com/{_SLUG}/index.html"))
    assert "medium-xpost" in out


def test_untouched_pages() -> None:
    for page in (
        _page("https://sebastienrousseau.com/2099-01-01-not-on-medium/"),
        _page(f"https://sebastienrousseau.com/fr/{_SLUG}/"),
        _page(f"https://sebastienrousseau.com/{_SLUG}/", schema='"@type":"WebPage"'),
        _page("https://example.com/x/"),
        "<html><head></head><body></body></html>",
    ):
        assert inject_medium_xpost(page) == page


def test_profile_story_names_no_publication() -> None:
    slug = next(
        s for s, e in _medium._payload()["stories"].items() if e["publication"] == "profile"
    )
    out = inject_medium_xpost(_page(f"https://sebastienrousseau.com/{slug}/"))
    assert "Also published on <a" in out


def test_data_is_consistent() -> None:
    pubs = _medium.publications()
    assert list(pubs) == ["ai", "quantum", "cloud-native"]
    posts = {p.stem for p in (ROOT / "_posts").glob("*.md")}
    stories = _medium._payload()["stories"]
    allowed = {*pubs, "profile", "generative-ai"}
    assert [s for s in stories if s not in posts] == []
    assert [s for s, e in stories.items() if e["publication"] not in allowed] == []
    ids = [e["id"] for e in stories.values()]
    assert len(ids) == len(set(ids))
    assert all(len(i) == 12 and int(i, 16) >= 0 for i in ids)
    by_pub = _medium.slugs_by_publication()
    assert by_pub["cloud-native"][0] == "2026-06-28-open-source-finos-cloud-native-cib-stack-2026"
    assert _medium.story("nope") is None


def test_listing_row_and_publication_archive_body() -> None:
    sys.path.insert(0, str(ROOT / "scripts" / "generators"))
    import build_listings as bl

    row = bl._publications_row()
    for slug in ("banking-on-ai", "banking-on-quantum", "banking-on-cloud-native"):
        assert f'href="/articles/medium/{slug}/"' in row
    pub = _medium.publications()["cloud-native"]
    post = ("A title", "2026-05-16", _SLUG, "An excerpt", ["infra"], "/b.webp", "Alt")
    body = bl._render_publication_body(pub, [post])
    assert "<h1>Banking On Cloud Native</h1>" in body
    assert "1 article ·" in body
    assert f'href="/{_SLUG}/"' in body
