# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""add_responsive_srcset: which /stocks/ images get a WebP srcset.

Lighthouse mobile flagged "Properly size images" on /about/, /projects/,
/research/, /articles/ and article heroes: each shipped a -1200 or -1920
variant to a ~400px viewport. The causes were a width floor that left
cards and inline photos without a srcset, a hero skip that assumed a
preload existed when it did not, and a self-closing tag that put the new
attribute after its slash.
"""

from __future__ import annotations

import postbuild_assets as pa

_CDN = "https://cloudcdn.pro/stocks/images/"


def _img(src: str, width: int, extra: str = "", close: str = ">") -> str:
    return f'<img src="{_CDN}{src}" alt="a" width="{width}" height="400"{extra}{close}'


def test_card_image_narrower_than_a_banner_gets_a_srcset() -> None:
    out, n = pa.add_responsive_srcset(_img("card-1200.webp", 600))
    assert n == 1
    assert f"{_CDN}card-640.webp 640w" in out


def test_small_icon_keeps_its_single_source() -> None:
    html = _img("icon-320.webp", 36)
    assert pa.add_responsive_srcset(html) == (html, 0)


def test_hero_without_a_preload_gets_a_srcset() -> None:
    html = _img("hero-1920.webp", 1600, ' fetchpriority="high"')
    out, n = pa.add_responsive_srcset(html)
    assert n == 1
    assert "srcset=" in out


def test_hero_with_a_matching_preload_is_left_alone() -> None:
    """The preload names one file; a srcset could pick another and waste it."""
    html = (
        f'<link rel="preload" as="image" href="{_CDN}hero-1200.webp" fetchpriority="high">'
        + _img("hero-1200.webp", 1600, ' fetchpriority="high"')
    )
    assert pa.add_responsive_srcset(html) == (html, 0)


def test_self_closing_tag_keeps_the_slash_last() -> None:
    out, _ = pa.add_responsive_srcset(_img("photo-1920.webp", 800, close=" />"))
    assert " / srcset=" not in out
    assert out.endswith('1100px" />')


def test_hero_srcset_assumes_full_viewport_width() -> None:
    """Heroes run full-bleed; capping sizes at 1100px would serve a 1200w
    file to a 1440px desktop and blur it."""
    out, _ = pa.add_responsive_srcset(_img("hero-1920.webp", 1600, ' fetchpriority="high"'))
    assert 'sizes="100vw"' in out
