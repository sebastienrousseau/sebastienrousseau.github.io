# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Unit coverage for build_rag_corpus — Phase 1.3.

build_rag_corpus.py emits the RAG/MCP corpus (/feed.jsonl + per-tag feeds +
MCP manifest) consumed by AI retrieval; a regression silently corrupts what
crawlers ingest. It had no unit tests. Cover the pure text-extraction and
tag-resolution helpers.
"""

from __future__ import annotations

from pathlib import Path

import build_rag_corpus as rc

# --- _alias_map ------------------------------------------------------------


def test_alias_map_lowercases_slug_and_aliases() -> None:
    tax = {"post-quantum-cryptography": {"category": "infra", "aliases": ["PQC", "Post-Quantum"]}}
    amap = rc._alias_map(tax)
    assert amap["post-quantum-cryptography"] == "post-quantum-cryptography"
    assert amap["pqc"] == "post-quantum-cryptography"
    assert amap["post-quantum"] == "post-quantum-cryptography"


# --- _strip_frontmatter ----------------------------------------------------


def test_strip_frontmatter_removes_block() -> None:
    text = '---\ntitle: "X"\n---\n# Heading\n\nBody.\n'
    assert rc._strip_frontmatter(text) == "# Heading\n\nBody.\n"


def test_strip_frontmatter_passthrough_without_block() -> None:
    text = "# Just a heading\n\nNo frontmatter.\n"
    assert rc._strip_frontmatter(text) == text


# --- _html_to_plaintext ----------------------------------------------------


def test_html_to_plaintext_extracts_main_strips_tags(tmp_path: Path) -> None:
    p = tmp_path / "index.html"
    p.write_text(
        "<html><body><nav>skip me</nav>"
        "<main><h1>Title</h1>  <p>Para <em>one</em>.</p></main>"
        "<footer>skip</footer></body></html>",
        encoding="utf-8",
    )
    out = rc._html_to_plaintext(p)
    assert "Title" in out and "Para" in out and "one" in out
    assert "skip me" not in out and "footer" not in out.lower()
    assert "  " not in out  # whitespace collapsed


def test_html_to_plaintext_missing_file_is_empty(tmp_path: Path) -> None:
    assert rc._html_to_plaintext(tmp_path / "nope.html") == ""


# --- _parse_tags_line ------------------------------------------------------

_TAX = {
    "agentic-ai": {"category": "ai"},
    "iso-20022": {"category": "payments"},
    "rust": {"category": "open-source"},
}
_AMAP = rc._alias_map(_TAX)


def test_parse_tags_line_none_is_empty() -> None:
    assert rc._parse_tags_line(None, _TAX, _AMAP) == ([], [])


def test_parse_tags_line_raw_and_pillars() -> None:
    raw, pillars = rc._parse_tags_line("agentic-ai, iso-20022, unknown-tag", _TAX, _AMAP)
    assert raw == ["agentic-ai", "iso-20022", "unknown-tag"]  # all raw kept
    assert pillars == ["ai", "payments"]  # sorted unique pillar categories; unknown dropped


def test_parse_tags_line_dedupes_pillars_and_sorts() -> None:
    # two tags in the same pillar → one pillar entry
    tax = {"a": {"category": "ai"}, "b": {"category": "ai"}}
    _, pillars = rc._parse_tags_line("a, b", tax, rc._alias_map(tax))
    assert pillars == ["ai"]
