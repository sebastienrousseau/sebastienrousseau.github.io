# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Unit coverage for build_topics — Phase 1.3.

build_topics.py generates the /topics/ hub + per-topic cluster pages. It was
largely untested. Cover the pure date/field/card-render/shell-surgery helpers.
"""

from __future__ import annotations

import build_topics as bt

# --- _field ----------------------------------------------------------------


def test_field_default_on_missing_or_empty() -> None:
    assert bt._field({"a": "x"}, "a") == "x"
    assert bt._field({}, "a", "def") == "def"
    assert bt._field({"a": ""}, "a", "def") == "def"  # empty → default


# --- _format_date ----------------------------------------------------------


def test_format_date_various_inputs() -> None:
    assert bt._format_date("Jun 29, 2026") == "2026-06-29"
    assert bt._format_date("June 29, 2026") == "2026-06-29"
    assert bt._format_date("2026-06-29") == "2026-06-29"


def test_format_date_passthrough_unparseable() -> None:
    assert bt._format_date("not a date") == "not a date"


# --- _human_date -----------------------------------------------------------


def test_human_date_formats_iso() -> None:
    assert bt._human_date("2026-06-29") == "Jun 29, 2026"


def test_human_date_passthrough_on_bad_input() -> None:
    assert bt._human_date("2026/06/29") == "2026/06/29"


# --- render_card -----------------------------------------------------------


def test_render_card_structure_and_escaping() -> None:
    fm = {
        "title": "Quantum & <Risk>",
        "description": "A <deck>",
        "keywords": "post-quantum, cryptography, banking, extra",
        "date": "2026-06-29",
        "banner": "https://cdn/b.webp",
    }
    out = bt.render_card("2026-06-29-x", fm)
    assert 'href="/2026-06-29-x/index.html"' in out
    assert "Quantum &amp; &lt;Risk&gt;" in out  # title escaped
    assert "A &lt;deck&gt;" in out  # desc escaped
    assert '<time datetime="2026-06-29">Jun 29, 2026</time>' in out
    # eyebrow = first 3 keywords, title-cased, ' · '-joined
    assert "Post-Quantum · Cryptography · Banking" in out
    assert "extra" not in out.split("newsroom-eyebrow")[1][:80]  # 4th keyword dropped


# --- _swap_main_body -------------------------------------------------------


def test_swap_main_body_wrap_div() -> None:
    shell = '<html><main class="m"><div class="wrap report-wrap">OLD</div></main></html>'
    out = bt._swap_main_body(shell, "NEW")
    assert "OLD" not in out
    assert '<div class="wrap report-wrap">NEW</div>' in out


# --- _strip_extra_jsonld ---------------------------------------------------


def test_strip_extra_jsonld_removes_itemlist_only() -> None:
    shell = (
        '<script type="application/ld+json">{"@type":"ItemList","itemListElement":[]}</script>'
        '<script type="application/ld+json">{"@type":"WebPage"}</script>'
    )
    out = bt._strip_extra_jsonld(shell)
    assert "ItemList" not in out  # ItemList block stripped
    assert "WebPage" in out  # other JSON-LD preserved


def test_strip_extra_jsonld_noop_without_blocks() -> None:
    assert bt._strip_extra_jsonld("<html>no jsonld</html>") == "<html>no jsonld</html>"
