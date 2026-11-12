# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""postbuild_lib/breadcrumb_sync.py: structured crumbs say what readers see."""

from __future__ import annotations

import json

from postbuild_lib.breadcrumb_sync import sync_breadcrumbs, visible_names

from . import _jsonld

LD = {
    "@context": "https://schema.org",
    "@graph": [
        {"@type": "WebPage"},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 2, "name": "Themen - Sebastien Rousseau", "item": "x"},
            {"@type": "ListItem", "position": 1, "name": "Startseite", "item": "y"},
        ]},
    ],
}  # fmt: skip


def _page(nav: str, ld: object = LD) -> str:
    return f'<nav aria-label="Breadcrumb" class="c">{nav}</nav><script type="application/ld+json">{json.dumps(ld)}</script>'


def _names(html: str) -> list[str]:
    data = _jsonld.first(html)
    items = sorted(data["@graph"][1]["itemListElement"], key=lambda i: i["position"])
    return [i["name"] for i in items]


def test_inline_crumbs_rename_the_list_in_position_order() -> None:
    out = sync_breadcrumbs(_page('<a href="/de/">Start</a> &middot; <span>Themen</span>'))
    assert _names(out) == ["Start", "Themen"]


def test_list_crumbs_and_unchanged_cases() -> None:
    page = _page("<ol><li><a>Start</a></li><li>Themen</li></ol>")
    assert _names(sync_breadcrumbs(page)) == ["Start", "Themen"]
    same = sync_breadcrumbs(page)
    assert sync_breadcrumbs(same) == same
    three = _page("<ol><li>a</li><li>b</li><li>c</li></ol>")
    assert sync_breadcrumbs(three) == three
    assert sync_breadcrumbs("<p>no nav</p>") == "<p>no nav</p>"
    broken = '<nav aria-label="Breadcrumb"><span>a</span></nav><script type="application/ld+json">{oops</script>'
    assert sync_breadcrumbs(broken) == broken
    other = _page("<span>a</span>", {"@type": "WebPage", "items": [1, 2]})
    assert sync_breadcrumbs(other) == other


def test_visible_names() -> None:
    assert visible_names("<p>x</p>") is None
    assert visible_names(
        '<nav aria-label="Breadcrumb"><a>A &amp; B</a> · <span> C </span></nav>'
    ) == ["A & B", "C"]
