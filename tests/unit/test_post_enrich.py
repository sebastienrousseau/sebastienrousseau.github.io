"""Unit coverage for post_enrich text helpers — Phase 1.3.

post_enrich.py auto-derives each post's lead block (TL;DR + key takeaways) from
the Markdown body. It was untested. Cover the pure text helpers: markdown
stripping, excerpt/takeaway derivation, H1 detection, URL, and inline→HTML.
"""

from __future__ import annotations

from pathlib import Path

import post_enrich as pe

# --- strip_md --------------------------------------------------------------


def test_strip_md_removes_all_inline_syntax() -> None:
    s = pe.strip_md("**bold** *it* [txt](u) [ref][1] `code`")
    assert s == "bold it txt ref code"


# --- derive_excerpt --------------------------------------------------------


def test_derive_excerpt_first_prose_paragraph() -> None:
    body = "# Heading\n\n<div>\n\nThe **first** real sentence.\n"
    assert pe.derive_excerpt(body) == "The first real sentence."


def test_derive_excerpt_truncates_long_line() -> None:
    body = "word " * 60  # > 200 chars, no headings
    out = pe.derive_excerpt(body)
    assert out.endswith("…")
    assert len(out) <= 200


def test_derive_excerpt_empty_when_no_prose() -> None:
    assert pe.derive_excerpt("# Only\n## Headings\n") == ""


# --- derive_key_takeaways --------------------------------------------------


def test_derive_key_takeaways_from_h2() -> None:
    body = "## Real Section\n\nA substantive sentence about it. More text.\n"
    out = pe.derive_key_takeaways(body)
    assert out == ["**Real Section.** A substantive sentence about it."]


def test_derive_key_takeaways_respects_max_items() -> None:
    body = "".join(f"## Section {i}\n\nSentence {i} here.\n\n" for i in range(6))
    assert len(pe.derive_key_takeaways(body, max_items=2)) == 2


# --- first_h1 --------------------------------------------------------------


def test_first_h1_returns_heading_and_index() -> None:
    res = pe.first_h1("intro line\n# Title\nrest")
    assert res is not None
    heading, idx = res
    assert heading == "Title"
    assert idx > 0


def test_first_h1_ignores_code_blocks_and_absent() -> None:
    assert pe.first_h1("```\n# not a heading\n```\n") is None
    assert pe.first_h1("no heading here") is None


# --- post_url --------------------------------------------------------------


def test_post_url_prefers_explicit_url() -> None:
    assert pe.post_url({"url": "/custom/", "path": Path("x.md")}) == "/custom/"


def test_post_url_derives_from_path_stem() -> None:
    assert pe.post_url({"url": "", "path": Path("2026-06-29-slug.md")}) == "/2026-06-29-slug/index.html"


# --- md_inline_to_html -----------------------------------------------------


def test_md_inline_to_html_converts_subset() -> None:
    out = pe.md_inline_to_html("**b** *i* `c` [t](u)")
    assert "<strong>b</strong>" in out
    assert "<em>i</em>" in out
    assert "<code>c</code>" in out
    assert '<a href="u">t</a>' in out
