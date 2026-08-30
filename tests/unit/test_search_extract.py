# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Coverage for search-index text extraction — Phase 1.3.

`_extract_visible_text` builds the plain-text search index from a page's
<main>: it drops <script>/<style>/comments and all tags, leaving readable
text. (The regex operates only on our own build-generated HTML; the
py/bad-tag-filter alerts on it are dismissed as not-reachable — see
project-docs/security.md.)
"""

from __future__ import annotations

from build_translations._search import _extract_visible_text


def test_strips_script_block() -> None:
    html = "<main><script>alert(1)</script><p>Visible body.</p></main>"
    out = _extract_visible_text(html)
    assert "Visible body." in out
    assert "alert(1)" not in out


def test_strips_style_block() -> None:
    html = "<main><style>.x{color:red}</style><p>Readable.</p></main>"
    out = _extract_visible_text(html)
    assert "Readable." in out
    assert "color:red" not in out


def test_strips_comments_and_tags() -> None:
    html = "<main><!-- secret --><h1>Title</h1><p>Para <em>one</em>.</p></main>"
    out = _extract_visible_text(html)
    assert "Title" in out
    assert "Para" in out and "one" in out
    assert "secret" not in out
    assert "<em>" not in out


def test_falls_back_to_full_html_without_main() -> None:
    out = _extract_visible_text("<p>No main wrapper here.</p>")
    assert "No main wrapper here." in out
