"""Search index (per-language) — walks the rendered language tree and
builds the entries consumed by the Static Site Generator search palette."""

from __future__ import annotations

import html as _html
import re

from . import _state as st

_TAG_RE = re.compile(r"<[^>]+>")
_WHITESPACE_RE = re.compile(r"\s+")
_TITLE_TAG_RE = re.compile(r"<title>([^<]+)</title>", re.IGNORECASE)
_MAIN_TAG_RE = re.compile(r"<main\b[\s\S]*?</main>", re.IGNORECASE)
_HEADING_RE = re.compile(r"<h[1-6]\b[^>]*>([\s\S]*?)</h[1-6]>", re.IGNORECASE)


def _extract_visible_text(html: str) -> str:
    """Strip every tag inside <main>, collapse whitespace, return plain text."""
    m = _MAIN_TAG_RE.search(html)
    body = m.group(0) if m else html
    # Drop <script> and <style> blocks first. The closing tag tolerates
    # whitespace (`</script >`) so a stray-space end tag can't smuggle script
    # text into the search index (py/bad-tag-filter).
    body = re.sub(r"<script[\s\S]*?</script\s*>", " ", body, flags=re.IGNORECASE)
    body = re.sub(r"<style[\s\S]*?</style\s*>", " ", body, flags=re.IGNORECASE)
    # Drop HTML comments.
    body = re.sub(r"<!--[\s\S]*?-->", " ", body)
    text = _TAG_RE.sub(" ", body)
    text = _html.unescape(text)
    return _WHITESPACE_RE.sub(" ", text).strip()


def _extract_headings(html: str) -> list[str]:
    """Pull h1-h6 text from <main>. Required by the search widget — every
    entry must have a `headings` array or the runtime trips a TypeError."""
    m = _MAIN_TAG_RE.search(html)
    body = m.group(0) if m else html
    out: list[str] = []
    for hm in _HEADING_RE.finditer(body):
        inner = _TAG_RE.sub(" ", hm.group(1))
        inner = _WHITESPACE_RE.sub(" ", _html.unescape(inner)).strip()
        if inner:
            out.append(inner)
    return out


def _build_fr_search_index() -> list[dict[str, object]]:
    """Walk public/fr/ for rendered HTML and build search entries."""
    entries: list[dict[str, object]] = []
    if not st.OUT.is_dir():
        return entries
    for path in sorted(st.OUT.rglob("index.html")):
        rel = path.relative_to(st.PUBLIC).as_posix()  # e.g. "fr/about/index.html"
        url = "/" + rel
        html = path.read_text(encoding="utf-8")
        title_m = _TITLE_TAG_RE.search(html)
        title = _html.unescape(title_m.group(1).strip()) if title_m else url
        text = _extract_visible_text(html)
        # Trim — the EN index keeps ~2KB per entry. Match that.
        if len(text) > 2200:
            text = text[:2200]
        entries.append(
            {
                "title": title,
                "url": url,
                "content": text,
                "headings": _extract_headings(html),
            }
        )
    return entries
