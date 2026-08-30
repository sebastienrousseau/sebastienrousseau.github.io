# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""The home page's social card comes from its authored banner (F-02).

The home page uses the ``index`` layout, which emits no ``banner-src`` marker
and carries no BlogPosting node, so ``fix_social_image`` could not reach it and
ssg's scrape stood: a 1597x1597 square portrait on a ``summary_large_image``
card, with no ``og:image:width``/``og:image:height`` for platforms to lay out
against. Every other page type sources its card from the front-matter banner.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "postbuild"))

from postbuild_lib import seo

BANNER = "https://cloudcdn.pro/stocks/images/alesia-kazantceva.webp"

FRONT_MATTER = f"""---
banner: "{BANNER}"
banner_width: "1425"
banner_height: "571"
description: "AI, banking and payments expert covering ISO 20022 and PQC."
---
"""

HOME_HTML = (
    "<html><head>"
    '<meta property="og:image" content="https://cloudcdn.pro/stocks/images/portrait.webp">'
    '<meta name="twitter:image" content="https://cloudcdn.pro/stocks/images/portrait.webp">'
    "</head><body></body></html>"
)


@pytest.fixture
def home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    public = tmp_path / "public"
    posts = tmp_path / "_posts"
    public.mkdir()
    posts.mkdir()
    (posts / "index.md").write_text(FRONT_MATTER, encoding="utf-8")
    monkeypatch.setattr(seo, "PUBLIC", public)
    monkeypatch.setattr(seo, "POSTS", posts)
    return public / "index.html"


def _content(html: str, prop: str) -> str | None:
    m = re.search(rf'{re.escape(prop)}"\s+content="([^"]*)"', html)
    return m.group(1) if m else None


def test_og_image_becomes_the_authored_banner(home: Path) -> None:
    out = seo.fix_home_social_image(home, HOME_HTML)
    assert _content(out, "og:image") == BANNER


def test_twitter_image_matches(home: Path) -> None:
    out = seo.fix_home_social_image(home, HOME_HTML)
    assert _content(out, "twitter:image") == BANNER


def test_dimensions_are_declared(home: Path) -> None:
    """Platforms need width/height to lay the card out without a fetch."""
    out = seo.fix_home_social_image(home, HOME_HTML)
    assert _content(out, "og:image:width") == "1425"
    assert _content(out, "og:image:height") == "571"


def test_existing_dimension_tags_are_overwritten_not_duplicated(home: Path) -> None:
    html = HOME_HTML.replace(
        "</head>",
        '<meta property="og:image:width" content="162">'
        '<meta property="og:image:height" content="162"></head>',
    )
    out = seo.fix_home_social_image(home, html)
    assert out.count('property="og:image:width"') == 1
    assert _content(out, "og:image:width") == "1425"


def test_pass_is_idempotent(home: Path) -> None:
    once = seo.fix_home_social_image(home, HOME_HTML)
    assert seo.fix_home_social_image(home, once) == once


def test_non_home_pages_are_untouched(home: Path) -> None:
    other = home.parent / "about" / "index.html"
    assert seo.fix_home_social_image(other, HOME_HTML) == HOME_HTML


def test_page_outside_public_is_untouched(home: Path) -> None:
    assert seo.fix_home_social_image(Path("/elsewhere/index.html"), HOME_HTML) == HOME_HTML


def test_missing_source_is_untouched(home: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(seo, "POSTS", home.parent / "no-posts-here")
    assert seo.fix_home_social_image(home, HOME_HTML) == HOME_HTML


def test_non_raster_banner_is_rejected(home: Path, tmp_path: Path) -> None:
    """An SVG or a divider placeholder must not become a large card image."""
    (tmp_path / "_posts" / "index.md").write_text(
        '---\nbanner: "https://cloudcdn.pro/logos/logo.svg"\n---\n', encoding="utf-8"
    )
    assert seo.fix_home_social_image(home, HOME_HTML) == HOME_HTML


def test_banner_without_dimensions_still_sets_the_image(home: Path, tmp_path: Path) -> None:
    (tmp_path / "_posts" / "index.md").write_text(
        f'---\nbanner: "{BANNER}"\n---\n', encoding="utf-8"
    )
    out = seo.fix_home_social_image(home, HOME_HTML)
    assert _content(out, "og:image") == BANNER
    assert _content(out, "og:image:width") is None


def test_front_matter_without_a_banner_is_untouched(home: Path, tmp_path: Path) -> None:
    (tmp_path / "_posts" / "index.md").write_text('---\ntitle: "Home"\n---\n', encoding="utf-8")
    assert seo.fix_home_social_image(home, HOME_HTML) == HOME_HTML
