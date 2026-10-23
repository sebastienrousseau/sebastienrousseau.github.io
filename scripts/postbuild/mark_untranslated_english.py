#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Mark English text left untranslated on translated pages as ``lang="en"``.

Why this exists
---------------

A translated page declares its language once, on ``<html lang>``. Parts
of its body are still English: the tags page body, the "Articles in this
topic" heading and English article cards on topic pages, a few home-page
strings. A screen reader then reads that English with the page
language's voice, which fails WCAG 3.1.2 (Language of Parts).

Until ssg 0.0.69 every Markdown body sat in ``<div lang="en">``, which
hid this, but it also marked the *translated* bodies as English.
staticdatagen dropped that wrapper (staticdatagen #139), so the parts
that really are English now have to be marked on their own.

The rule
--------

Text that appears verbatim in ``<main>`` of any English page was not
translated. Every such text node of at least three words, inside
``<main>`` and outside code, ``pre``, scripts, styles and SVG, gets
``lang="en"``: on its parent element when the text is the parent's whole
content, otherwise on a ``<span>`` around the text. Text already inside
an element marked English is left alone, so a second run changes
nothing.

The whole English site is the reference, not only the page's own
counterpart, because translated listings quote English excerpts and
headings from other pages. Known gap: the topic pages' tag eyebrows
("AI · Research · Innovation") are assembled from tag names and appear
on no English page, so they stay unmarked.
"""

from __future__ import annotations

import html
import re
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"

_SKIP_TAGS = frozenset({"script", "style", "code", "pre", "svg", "template", "textarea"})
_VOID_TAGS = frozenset(
    {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "source",
        "track",
        "wbr",
    }
)
_WORD_RE = re.compile(r"[^\W\d_]{2,}")
_MIN_WORDS = 3
_HTML_LANG_RE = re.compile(r'<html\b[^>]*\blang=["\']?([A-Za-z0-9-]+)', re.IGNORECASE)


def _normalise(text: str) -> str:
    return " ".join(html.unescape(text).split())


def _is_candidate(text: str) -> bool:
    return len(_WORD_RE.findall(text)) >= _MIN_WORDS


def _is_english(lang: str | None) -> bool:
    return lang is not None and lang.lower().split("-")[0] == "en"


@dataclass
class _Element:
    tag: str
    start: int  # offset of "<"
    tag_end: int  # offset just past the start tag's ">"
    english: bool  # this element or an ancestor is marked English
    skipped: bool  # inside code, pre, script, style or SVG
    texts: list[tuple[int, int]] = field(default_factory=list)
    has_children: bool = False


@dataclass
class _Text:
    start: int
    end: int
    parent: _Element


class _MainScanner(HTMLParser):
    """Collect the text nodes inside ``<main>`` with their source offsets.

    With *include_english* the scan also returns text inside elements
    marked English, which is what reading the English page itself needs.
    """

    def __init__(self, source: str, include_english: bool = False) -> None:
        super().__init__(convert_charrefs=False)
        self.source = source
        self.include_english = include_english
        self._line_starts = [0] + [i + 1 for i, ch in enumerate(source) if ch == "\n"]
        self.stack: list[_Element] = []
        self.texts: list[_Text] = []
        self._in_main = 0
        self._run: tuple[int, int] | None = None

    def _offset(self) -> int:
        line, col = self.getpos()
        return self._line_starts[line - 1] + col

    def _flush(self) -> None:
        """Close the current text run: data and entities between two tags."""
        run, self._run = self._run, None
        if not run or not self.stack or not self.source[run[0] : run[1]].strip():
            return
        parent = self.stack[-1]
        parent.texts.append(run)
        wanted = self.include_english or not parent.english
        if self._in_main and wanted and not parent.skipped:
            self.texts.append(_Text(run[0], run[1], parent))

    def _extend(self, length: int) -> None:
        start = self._offset()
        if self._run and self._run[1] == start:
            self._run = (self._run[0], start + length)
        else:
            self._flush()
            self._run = (start, start + length)

    def handle_data(self, data: str) -> None:
        self._extend(len(data))

    def handle_entityref(self, name: str) -> None:
        self._extend(len(name) + 2)

    def handle_charref(self, name: str) -> None:
        self._extend(len(name) + 3)

    def handle_comment(self, data: str) -> None:
        self._flush()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._flush()
        start = self._offset()
        tag_end = start + len(self.get_starttag_text() or "")
        if tag == "main":
            self._in_main += 1
        parent = self.stack[-1] if self.stack else None
        if parent:
            parent.has_children = True
        if tag in _VOID_TAGS:
            return
        lang = dict(attrs).get("lang")
        english = _is_english(lang) if lang else bool(parent and parent.english)
        skipped = tag in _SKIP_TAGS or bool(parent and parent.skipped)
        self.stack.append(_Element(tag, start, tag_end, english, skipped))

    def handle_endtag(self, tag: str) -> None:
        self._flush()
        if tag == "main" and self._in_main:
            self._in_main -= 1
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def close(self) -> None:
        super().close()
        self._flush()


def english_phrases(source: str) -> set[str]:
    """Every candidate text node inside ``<main>`` of an English page."""
    scanner = _MainScanner(source, include_english=True)
    scanner.feed(source)
    scanner.close()
    phrases = (_normalise(source[t.start : t.end]) for t in scanner.texts)
    return {p for p in phrases if _is_candidate(p)}


def _edit_for(source: str, text: _Text) -> tuple[int, int, str]:
    parent = text.parent
    sole = not parent.has_children and len(parent.texts) == 1
    if sole:
        at = parent.tag_end - (2 if source[parent.tag_end - 2] == "/" else 1)
        return at, at, ' lang="en"'
    raw = source[text.start : text.end]
    return text.start, text.end, f'<span lang="en">{raw}</span>'


def mark_untranslated(source: str, english: set[str]) -> tuple[str, int]:
    """Return *source* with English text nodes marked, and how many."""
    scanner = _MainScanner(source)
    scanner.feed(source)
    scanner.close()
    edits = [
        _edit_for(source, t)
        for t in scanner.texts
        if _normalise(source[t.start : t.end]) in english
    ]
    for start, end, replacement in sorted(edits, reverse=True):
        source = source[:start] + replacement + source[end:]
    return source, len(edits)


def _page_lang(source: str) -> str | None:
    match = _HTML_LANG_RE.search(source)
    return match.group(1) if match else None


def process(public: Path) -> tuple[int, int]:
    """Mark every translated page under *public*; return (pages, nodes)."""
    translated: list[Path] = []
    english: set[str] = set()
    for page in sorted(public.rglob("index.html")):
        source = page.read_text(encoding="utf-8")
        lang = _page_lang(source)
        if _is_english(lang):
            english |= english_phrases(source)
        elif lang:
            translated.append(page)
    pages = nodes = 0
    for page in translated:
        marked, count = mark_untranslated(page.read_text(encoding="utf-8"), english)
        if count:
            page.write_text(marked, encoding="utf-8")
            pages += 1
            nodes += count
    return pages, nodes


def main() -> int:
    if not PUBLIC.is_dir():
        print(f"mark_untranslated_english: {PUBLIC} not found", file=sys.stderr)
        return 1
    pages, nodes = process(PUBLIC)
    print(
        f"mark_untranslated_english: marked {nodes} English text nodes on {pages} translated pages"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
