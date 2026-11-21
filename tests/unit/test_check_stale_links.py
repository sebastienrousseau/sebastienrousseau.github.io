# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Content links to retired URLs are found and rewritten in their own style."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "seo_and_audit"))

import check_stale_links as csl

MAP = {"/old/": "/new/", "/fr/ancien/": "/fr/nouveau/", "/papers/": "/research/"}


def test_markdown_link_with_index_html_keeps_its_style() -> None:
    out, found = csl.rewrite('[a](https://sebastienrousseau.com/old/index.html "t")', MAP)
    assert out == '[a](https://sebastienrousseau.com/new/index.html "t")'
    assert found == ["/old/"]


def test_href_without_trailing_slash_and_front_matter_url() -> None:
    src = '<a href="https://sebastienrousseau.com/fr/ancien">x</a>\nid: "https://sebastienrousseau.com/old"\n'
    out, found = csl.rewrite(src, MAP)
    assert 'href="https://sebastienrousseau.com/fr/nouveau"' in out
    assert 'id: "https://sebastienrousseau.com/new"' in out
    assert len(found) == 2


def test_relative_links_reference_definitions_and_trailing_slash() -> None:
    out, _ = csl.rewrite("[r]: /papers/\nsee [b](/old/) and href='/old/index.html'\n", MAP)
    assert out == "[r]: /research/\nsee [b](/new/) and href='/new/index.html'\n"


def test_prose_regex_patterns_and_unmapped_links_are_left_alone() -> None:
    src = (
        "the /old/ path in prose; "
        '"href=/papers/index\\\\.html>Papers" ; '
        "[k](/kept/) [p](/papers-and-more/)"
    )
    out, found = csl.rewrite(src, MAP)
    assert out == src
    assert found == []


def test_rewrite_is_idempotent() -> None:
    once, _ = csl.rewrite("[a](/old/index.html)", MAP)
    twice, found = csl.rewrite(once, MAP)
    assert twice == once and found == []


def test_committed_content_has_no_stale_links() -> None:
    redirects = csl.load_map()
    stale = {
        p.relative_to(ROOT).as_posix()
        for p in csl.content_files()
        if csl.rewrite(p.read_text(encoding="utf-8"), redirects)[1]
    }
    assert not stale, f"{len(stale)} file(s) link to retired URLs: {sorted(stale)[:5]}"
