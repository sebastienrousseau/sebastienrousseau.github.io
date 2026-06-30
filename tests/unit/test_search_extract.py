"""Search-index text extraction must strip scripts even with a spaced end
tag — Phase 4 (CodeQL py/bad-tag-filter).

`_extract_visible_text` builds the plain-text search index from a page's
<main>. The script/style strip regexes now tolerate whitespace in the
closing tag (`</script >`), so a stray-space end tag can't smuggle script
text into the index.
"""

from __future__ import annotations

from build_translations._search import _extract_visible_text


def test_strips_script_with_spaced_closing_tag() -> None:
    html = "<main><script>alert(1)</script ><p>Visible body.</p></main>"
    out = _extract_visible_text(html)
    assert "Visible body." in out
    assert "alert(1)" not in out


def test_strips_style_with_spaced_closing_tag() -> None:
    html = "<main><style>.x{color:red}</style ><p>Readable.</p></main>"
    out = _extract_visible_text(html)
    assert "Readable." in out
    assert "color:red" not in out


def test_plain_text_passthrough() -> None:
    html = "<main><h1>Title</h1><p>Para one.</p></main>"
    out = _extract_visible_text(html)
    assert "Title" in out
    assert "Para one." in out
