# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""postbuild_lib.blogposting: find the page's BlogPosting node."""

from __future__ import annotations

from postbuild_lib.blogposting import blogposting_node, inherited_fields


def _ld(body: str) -> str:
    return f'<script type="application/ld+json">{body}</script>'


def test_skips_unparseable_blocks_and_finds_a_nested_node() -> None:
    html = _ld("{not json") + _ld(
        '[{"@type":"Person","name":"x"},{"@graph":[1,{"@type":"BlogPosting",'
        '"datePublished":"2026-01-01","dateModified":"","image":"https://x/i.webp"}]}]'
    )
    node = blogposting_node(html)
    assert node is not None
    assert node["datePublished"] == "2026-01-01"
    # Empty values are not inherited: an empty dateModified is no date.
    assert inherited_fields(html) == {"datePublished": "2026-01-01", "image": "https://x/i.webp"}


def test_no_blogposting_means_nothing_inherited() -> None:
    html = _ld('{"@type":"WebPage","name":"x"}') + _ld('"just a string"')
    assert blogposting_node(html) is None
    assert inherited_fields(html) == {}
