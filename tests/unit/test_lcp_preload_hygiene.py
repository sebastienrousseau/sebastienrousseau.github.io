# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""A page must not high-priority-fetch an image it never renders.

`/projects/` scored 0.93 against a 0.94 Lighthouse floor — identical across
all three runs, so not noise. LCP was the only imperfect metric (1.8 s, score
0.71, weight 25; FCP/TBT/CLS/SI were all perfect), and two faults compounded:

  * every image on the page was `loading="lazy"`, including the 1600x1000 card
    in the first screenful that *was* the LCP element; and
  * because there was then no non-lazy `<img>` at all, `inject_lcp_preload`
    took its "nothing to preload" path and left the layout's preload pointing
    at a portrait the page never renders — a high-priority fetch of an unused
    image, competing with the real LCP.

Fixing the first also fixes the second, since an eager card gives the pass a
candidate to realign to. These tests pin both directions, and the guard that
keeps a CSS-background hero's preload intact.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "postbuild"))
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
sys.path.insert(0, str(ROOT / "scripts" / "generators"))

import gen_projects
import postbuild_assets as pa

PRELOAD = '<link rel="preload" as="image" href="{href}" fetchpriority="high">'


def _page(preload_href: str | None, body: str) -> str:
    head = PRELOAD.format(href=preload_href) if preload_href else ""
    return f"<html><head>{head}</head><body>{body}</body></html>"


def test_first_area_card_is_eager_and_the_rest_are_lazy():
    """The LCP element must not be deferred; the below-fold cards still should."""
    imgs = re.findall(r"<img[^>]*>", gen_projects.setup_three_block())
    assert len(imgs) >= 2, imgs
    assert 'loading="eager"' in imgs[0] and 'fetchpriority="high"' in imgs[0]
    for tag in imgs[1:]:
        assert 'loading="lazy"' in tag, tag
        assert "fetchpriority" not in tag, tag


def test_preload_realigns_to_the_first_eager_image():
    """With a candidate present, a mismatched preload is corrected rather than
    left pointing at an image the page does not render."""
    html = _page(
        "https://cdn.example/portrait-1200.webp",
        '<img src="https://cdn.example/hero-1920.webp" loading="eager">',
    )
    out, n = pa.inject_lcp_preload(html)
    assert n == 1
    assert "hero-1920.webp" in re.search(r'as="image" href="([^"]+)"', out).group(1)


def test_stale_preload_is_dropped_when_no_image_can_be_the_lcp():
    """Every image lazy: the preloaded URL is fetched at high priority and
    never used. That is bandwidth taken from the real LCP."""
    html = _page(
        "https://cdn.example/portrait-1200.webp",
        '<img src="https://cdn.example/card.webp" loading="lazy">',
    )
    out, n = pa.inject_lcp_preload(html)
    assert n == 1
    assert 'as="image"' not in out


def test_css_background_hero_keeps_its_preload():
    """A hero set in CSS is a legitimate preload target with no <img> to match.
    Dropping it would slow the very paint the preload exists to accelerate."""
    href = "https://cdn.example/hero.webp"
    html = _page(href, f'<div style="background-image:url({href})"></div>')
    out, n = pa.inject_lcp_preload(html)
    assert n == 0
    assert href in out


def test_page_without_any_preload_is_untouched():
    html = _page(None, '<img src="https://cdn.example/c.webp" loading="lazy">')
    out, n = pa.inject_lcp_preload(html)
    assert (out, n) == (html, 0)
