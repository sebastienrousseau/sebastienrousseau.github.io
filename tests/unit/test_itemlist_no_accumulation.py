# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""``inject_itemlist`` must set the listing graph, not append another.

Postbuild is re-run over built pages. This pass inserted a fresh
``<script type="application/ld+json">`` before ``</body>`` every time,
with nothing checking for one already there, so /projects/ gained a full
29-item ItemList graph on each run — about 18.7 KB — and never reached a
fixed point.

The strip is scoped to this pass's own signature *including the page
URL*, so an ItemList written by build_topics, build_changelog or the
case-study builder on the same page survives untouched. That scoping is
what the last test here pins.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "postbuild"))

import postbuild_transforms as pt  # type: ignore[import-not-found]

_REL = next(iter(pt.LISTING_PAGES))
_CLASSES = pt.LISTING_PAGES[_REL]
_PAGE = pt.PUBLIC / _REL


def _page(n: int = 3) -> str:
    cards = "".join(
        f'<article class="{_CLASSES[0]}">'
        f'<h3><a href="/projects/thing-{i}/">Project number {i}</a></h3>'
        f"</article>"
        for i in range(n)
    )
    return f"<html><body>{cards}</body></html>"


def _itemlists(html: str) -> list[str]:
    return re.findall(r'"@type":"ItemList"', html)


def test_an_itemlist_is_injected() -> None:
    out = pt.inject_itemlist(_PAGE, _page())
    assert len(_itemlists(out)) == 1
    assert '"numberOfItems":3' in out


def test_running_twice_does_not_add_a_second_graph() -> None:
    once = pt.inject_itemlist(_PAGE, _page())
    assert len(_itemlists(pt.inject_itemlist(_PAGE, once))) == 1


def test_repeated_passes_reach_a_fixed_point() -> None:
    out = pt.inject_itemlist(_PAGE, _page())
    for _ in range(4):
        out = pt.inject_itemlist(_PAGE, out)
    assert out == pt.inject_itemlist(_PAGE, out)
    assert len(_itemlists(out)) == 1


def test_the_graph_tracks_the_cards_when_they_change() -> None:
    first = pt.inject_itemlist(_PAGE, _page(3))
    assert '"numberOfItems":3' in first
    # Same page rebuilt with an extra card.
    second = pt.inject_itemlist(_PAGE, _page(5))
    assert '"numberOfItems":5' in second
    assert len(_itemlists(second)) == 1


def test_a_foreign_itemlist_on_the_same_page_survives() -> None:
    """Only this pass's own block, for this page's URL, may be stripped."""
    foreign = (
        '<script type="application/ld+json">'
        '{"@context":"https://schema.org","@type":"ItemList",'
        '"url":"https://sebastienrousseau.com/somewhere-else/","itemListElement":[]}'
        "</script>"
    )
    html = _page().replace("</body>", foreign + "</body>")
    out = pt.inject_itemlist(_PAGE, html)
    assert foreign in out
    assert len(_itemlists(out)) == 2


def test_a_non_listing_page_is_untouched() -> None:
    html = "<html><body><p>not a listing</p></body></html>"
    assert pt.inject_itemlist(pt.PUBLIC / "not-a-listing/index.html", html) == html
