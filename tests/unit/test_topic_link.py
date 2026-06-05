"""Tests for scripts/topic_link.py — the internal topic-cluster linker."""

from __future__ import annotations

import topic_link as tl


def test_split_segments_protects_code_fences():
    body = """Plain text here.
```
code block with CRYSTALS-Kyber in it
```
More plain text."""
    segments = tl.split_segments(body)
    # The fenced block must be marked protected so the linker won't
    # rewrite identifiers inside it.
    fence = [seg for seg, protected in segments if "```" in seg]
    assert fence, "fenced block not segmented"
    assert all(protected for seg, protected in segments if "```" in seg)


def test_split_segments_protects_inline_code():
    body = "Use `pain001` to make payment files."
    segments = tl.split_segments(body)
    assert any(protected and "`pain001`" in seg for seg, protected in segments)


def test_split_segments_protects_existing_markdown_link():
    body = "See [pain001](https://pain001.com/) for more."
    segments = tl.split_segments(body)
    assert any(protected and "[pain001]" in seg for seg, protected in segments)


def test_split_segments_protects_headings():
    body = "Intro paragraph.\n## A heading with CRYSTALS-Kyber\nMore text."
    segments = tl.split_segments(body)
    assert any(protected and seg.startswith("## ") for seg, protected in segments)


def test_split_segments_protects_reference_link_definitions():
    # Reference-link definitions only get protected when they sit at the
    # start of a line — that's the markdown spec (whitespace-prefixed is OK
    # though). The linker should leave them alone since the URL part is not
    # something we want to rewrite.
    body = "Plain text.\n[01]: https://example.com\nMore plain text.\n"
    segments = tl.split_segments(body)
    assert any(protected and "[01]:" in seg for seg, protected in segments)


def test_link_segment_first_occurrence_only():
    entities = [(["CRYSTALS-Kyber"], "2023-11-19-crystals-kyber")]
    text = "CRYSTALS-Kyber is the new standard. CRYSTALS-Kyber is great."
    out, consumed = tl.link_segment(text, entities)
    # First occurrence linked, second stays bare.
    assert out.count("[CRYSTALS-Kyber](") == 1
    assert out.count("CRYSTALS-Kyber") == 2
    assert 0 in consumed


def test_link_segment_case_insensitive_but_preserves_case():
    entities = [(["CRYSTALS-Kyber"], "2023-11-19-crystals-kyber")]
    text = "The CRYSTALS-KYBER scheme is great."
    out, consumed = tl.link_segment(text, entities)
    assert "[CRYSTALS-KYBER](" in out  # source casing preserved in anchor
    assert 0 in consumed


def test_link_segment_no_match_returns_empty_consumed():
    entities = [(["CRYSTALS-Kyber"], "2023-11-19-crystals-kyber")]
    text = "Nothing relevant here."
    out, consumed = tl.link_segment(text, entities)
    assert out == text
    assert consumed == set()


def test_process_post_idempotent(tmp_path):
    p = tmp_path / "2024-04-22-bug-discovered-in-quantum-algorithm-for-lattice-based-crypto.md"
    p.write_text(
        """---
title: "Lattice bug"
url: "https://sebastienrousseau.com/x/index.html"
---

Some prose mentioning CRYSTALS-Kyber once in the body.
""",
        encoding="utf-8",
    )
    # First run adds a link.
    added_1 = tl.process_post(p)
    assert added_1 == 1
    # Second run is a no-op (existing link is protected by the
    # split_segments rule for existing markdown links).
    added_2 = tl.process_post(p)
    assert added_2 == 0


def test_process_post_skips_self_canonical(tmp_path):
    p = tmp_path / "2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age.md"
    p.write_text(
        """---
title: "Kyber post"
---

I am the canonical CRYSTALS-Kyber post.
""",
        encoding="utf-8",
    )
    # The post IS the canonical for CRYSTALS-Kyber — the linker must
    # not self-link.
    tl.process_post(p)
    text = p.read_text()
    assert "[CRYSTALS-Kyber](/2023-11-19-crystals-kyber" not in text
