"""Unit coverage for build_oembed — Phase 1.3.

build_oembed.py emits per-article /oembed/<slug>.json (rich link previews for
Notion/Slack/Discord/etc.). It had no tests. Cover the pure escaping, embed-
HTML, oEmbed-doc, and frontmatter-extraction helpers.
"""

from __future__ import annotations

from pathlib import Path

import build_oembed as oe

# --- _esc_html -------------------------------------------------------------


def test_esc_html_escapes_metacharacters() -> None:
    assert oe._esc_html('a & b < c > d "e"') == "a &amp; b &lt; c &gt; d &quot;e&quot;"


# --- _embed_html -----------------------------------------------------------


def test_embed_html_links_and_escapes() -> None:
    out = oe._embed_html('Title & <b>', "2026-06-29-x", "Excerpt <em>")
    assert 'href="https://sebastienrousseau.com/2026-06-29-x/"' in out
    assert "Title &amp; &lt;b&gt;" in out  # title escaped
    assert "Excerpt &lt;em&gt;" in out  # excerpt escaped
    assert out.startswith("<blockquote")


def test_embed_html_omits_empty_excerpt() -> None:
    out = oe._embed_html("Title", "s", "")
    assert "<p></p>" not in out  # no empty excerpt paragraph


# --- _oembed_doc -----------------------------------------------------------


def test_oembed_doc_shape() -> None:
    doc = oe._oembed_doc("Title", "2026-06-29-x", "Summary", "https://cdn/img.webp")
    assert doc["version"] == "1.0"
    assert doc["type"] == "rich"
    assert doc["title"] == "Title"
    assert doc["thumbnail_url"] == "https://cdn/img.webp"
    assert doc["author_name"] == oe._AUTHOR_NAME
    assert doc["provider_url"] == "https://sebastienrousseau.com/"
    assert isinstance(doc["width"], int) and isinstance(doc["height"], int)
    assert "<blockquote" in doc["html"]


# --- _post_meta ------------------------------------------------------------


def test_post_meta_extracts_fields(tmp_path: Path) -> None:
    p = tmp_path / "2026-06-29-x.md"
    p.write_text(
        '---\ntitle: "Hello"\nexcerpt: "A short summary"\n'
        'banner: "https://cdn/banner.webp"\n---\nbody\n',
        encoding="utf-8",
    )
    title, slug, excerpt, banner = oe._post_meta(p)
    assert title == "Hello"
    assert slug == "2026-06-29-x"
    assert excerpt == "A short summary"
    assert banner == "https://cdn/banner.webp"


def test_post_meta_none_without_title(tmp_path: Path) -> None:
    p = tmp_path / "2026-06-29-x.md"
    p.write_text('---\nexcerpt: "no title here"\n---\nbody\n', encoding="utf-8")
    assert oe._post_meta(p) is None


def test_post_meta_default_banner(tmp_path: Path) -> None:
    p = tmp_path / "2026-06-29-x.md"
    p.write_text('---\ntitle: "T"\n---\nbody\n', encoding="utf-8")
    _title, _slug, _excerpt, banner = oe._post_meta(p)
    assert banner == oe._DEFAULT_THUMBNAIL
