"""``_playlist_copy.INTRO_PARAGRAPHS`` must mirror ``_posts/playlists.md``.

The /playlists/ intro is authored as the markdown body of
``_posts/playlists.md`` — that is what the generator renders. The same
three paragraphs are mirrored in ``scripts/lib/_playlist_copy.py`` so
the translation pipeline knows the exact strings to swap out of the
forked English page.

Two copies of the same prose drift. When they do, the swap silently
misses and every localized /playlists/ page keeps the English intro
while the rest of the body is translated — the exact failure this
mirror exists to prevent. This test fails first instead.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

import _playlist_copy as pl  # type: ignore[import-not-found]


def _markdown_body_paragraphs() -> list[str]:
    """The blank-line-separated paragraphs after the YAML frontmatter."""
    text = (ROOT / "_posts" / "playlists.md").read_text(encoding="utf-8")
    # Frontmatter is delimited by the first two "---" lines.
    _, _, after_open = text.partition("---\n")
    _, _, body = after_open.partition("\n---\n")
    return [p.strip() for p in body.strip().split("\n\n") if p.strip()]


def test_intro_paragraphs_match_the_markdown_source() -> None:
    assert list(pl.INTRO_PARAGRAPHS) == _markdown_body_paragraphs()
