# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Give every indexable page a unique ``<title>`` and meta description.

Bing Webmaster Tools flagged the site for identical titles and
descriptions, and the build confirms it: paginated listings repeat their
first page's title (``Artikel`` five times in ``/de/artikel/page/N/``),
year archives and static pages share a title across locales whose word
for it is the same (``Kontakt``, ``文章 — 2025``), and the tag, category
and year-archive descriptions are one English sentence reused by every
locale.

Two steps, both on the built output so every generator benefits:

1. *Context*, on every page. A paginated listing gets its localised
   ``Page N of M`` label (``listings.json`` ``ui.pageLabel``) in the title
   and the description; a listing page (articles, years, tags, categories,
   topics) gets the site name in its title and its own title as the lead
   of its description, so a reused English sentence is anchored to the
   localised listing it describes.
2. *Collisions*, among indexable pages only (self-canonical, not noindex,
   not a redirect stub). A value shared across locales gets the locale's
   native name appended on its non-English members; a value still shared
   inside one locale gets the page's publication date, or failing that its
   URL slug.

``og:``/``twitter:`` title and description are kept in step. JSON-LD is
not touched, so the per-page CSP hashes stay valid.
"""

from __future__ import annotations

import html as _html
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from email.utils import parsedate_to_datetime
from functools import cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import _lang_registry as _lr

SITE_NAME = "Sebastien Rousseau"
SEP = " · "
_TITLE_RE = re.compile(r"<title>([\s\S]*?)</title>", re.I)
_META_RE = re.compile(r"<meta\b[^>]*>", re.I)
_ATTR_RE = re.compile(r'([\w:-]+)\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s"\'>]+))')
_PAGED_RE = re.compile(r"/page/(\d+)/index\.html$")
_EN_PAGE_RE = re.compile(r"\s*Page \d+ of \d+\.?")
_DATE_META_RE = re.compile(
    r'<meta\s+itemprop="datePublished"\s+content="([^"]+)"\s+id="date"', re.I
)
_TITLE_KEYS = ("og:title", "twitter:title")
_DESC_KEYS = ("description", "og:description", "twitter:description")


@dataclass
class Page:
    """Head metadata of one built page, kept as unescaped text."""

    path: Path
    rel: str
    locale: str
    title: str
    desc: str
    indexable: bool
    published: str = ""
    changed: set[str] = field(default_factory=set)


def _attrs(tag: str) -> dict[str, str]:
    return {
        m.group(1).lower(): next(g for g in m.groups()[1:] if g is not None)
        for m in _ATTR_RE.finditer(tag)
    }


def _meta_key(tag: str) -> str:
    a = _attrs(tag)
    return (a.get("name") or a.get("property") or "").lower()


def read_description(head: str) -> str:
    """Unescaped ``<meta name="description">`` content, or ''."""
    for tag in _META_RE.findall(head):
        if _meta_key(tag) == "description":
            return _html.unescape(_attrs(tag).get("content", ""))
    return ""


def set_meta(html: str, keys: tuple[str, ...], value: str) -> str:
    """Rewrite the ``content`` of every meta whose name/property is in ``keys``."""
    esc = _html.escape(value, quote=True)

    def repl(m: re.Match[str]) -> str:
        tag = m.group(0)
        if _meta_key(tag) not in keys:
            return tag
        return re.sub(
            r'\bcontent\s*=\s*(?:"[^"]*"|\'[^\']*\'|[^\s"\'>]+)', f'content="{esc}"', tag, count=1
        )

    return _META_RE.sub(repl, html)


def set_title(html: str, value: str) -> str:
    """Rewrite ``<title>`` and its og/twitter mirrors."""
    out = _TITLE_RE.sub(lambda _m: f"<title>{_html.escape(value, quote=False)}</title>", html, 1)
    return set_meta(out, _TITLE_KEYS, value)


@cache
def page_label(locale: str) -> str:
    """Localised ``Page {page} of {total}`` frame (English fallback)."""
    path = _lr.I18N_DIR / locale / "listings.json"
    try:
        label = json.loads(path.read_text(encoding="utf-8"))["ui"]["pageLabel"]
    except (OSError, ValueError, KeyError):
        label = ""
    return label or "Page {page} of {total}"


@cache
def listing_roots(locale: str) -> tuple[str, ...]:
    """Path prefixes (no leading slash) of the listing trees of ``locale``."""
    statics = {} if locale == "en" else _lr.load_slugs(locale).get("static", {})
    prefix = "" if locale == "en" else f"{locale}/"
    names = [statics.get(k, k) for k in ("articles", "tags", "topics")] + ["categories"]
    return tuple(f"{prefix}{n}/" for n in names)


def is_listing(rel: str, locale: str) -> bool:
    """True for article, year, tag, category and topic listing pages."""
    return rel != "index.html" and rel.startswith(listing_roots(locale))


def _total_pages(page: Page) -> int:
    return (
        sum(1 for p in page.path.parent.parent.glob("*/index.html") if p.parent.name.isdigit()) + 1
    )


def add_context(page: Page) -> None:
    """Step 1: listing context (page number, site name, lead) on one page."""
    if not is_listing(page.rel, page.locale):
        return
    paged = _PAGED_RE.search(page.rel)
    if paged:
        label = page_label(page.locale).format(page=paged.group(1), total=_total_pages(page))
        if label not in page.title:
            page.title = f"{page.title}{SEP}{label}"
        # build_listings writes an English "Page N of M." into every
        # locale's description; swap it for the localised label.
        if not page.desc.endswith(f"{label}."):
            page.desc = f"{_EN_PAGE_RE.sub('', page.desc).rstrip()} {label}."
    if SITE_NAME not in page.title:
        page.title = f"{page.title}{SEP}{SITE_NAME}"
    head = page.title.split(SEP)[0]
    if page.desc and not page.desc.startswith(head):
        page.desc = f"{head}: {page.desc}"
    page.changed.update({"title", "desc"})


def _iso_date(raw: str) -> str:
    try:
        return parsedate_to_datetime(raw).date().isoformat()
    except (TypeError, ValueError):
        return raw[:10]


def _suffix_for(page: Page, step: int) -> str:
    if step == 0:
        return "" if page.locale == "en" else _lr.get(page.locale).long_label
    if page.published:
        return _iso_date(page.published)
    return page.rel.removesuffix("/index.html").rsplit("/", 1)[-1] or page.locale


def _collisions(pages: list[Page], attr: str) -> list[list[Page]]:
    """Groups of two or more indexable pages sharing a non-empty ``attr``."""
    groups: dict[str, list[Page]] = defaultdict(list)
    for p in pages:
        value = getattr(p, attr)
        if p.indexable and value:
            groups[value].append(p)
    return [members for members in groups.values() if len(members) > 1]


def _append(page: Page, attr: str, suffix: str) -> None:
    if not suffix:
        return
    value = getattr(page, attr)
    setattr(page, attr, f"{value}{SEP}{suffix}" if attr == "title" else f"{value} ({suffix})")
    page.changed.add(attr)


def resolve_collisions(pages: list[Page], attr: str) -> None:
    """Step 2: make ``attr`` unique among indexable pages.

    Pass 0 separates locales (native language name on non-English
    members); pass 1 separates pages within one locale (date or slug).
    """
    for step in (0, 1):
        for members in _collisions(pages, attr):
            if step == 0 and len({p.locale for p in members}) < 2:
                continue
            for p in members:
                _append(p, attr, _suffix_for(p, step))


def render(page: Page, html: str) -> str:
    """Write the page's (possibly updated) title and description back."""
    out = set_title(html, page.title) if "title" in page.changed else html
    return set_meta(out, _DESC_KEYS, page.desc) if "desc" in page.changed else out


def load_page(path: Path, rel: str, locale: str, indexable: bool) -> tuple[Page, str] | None:
    """Parse one page's head; None when it has no ``<title>``."""
    text = path.read_text(encoding="utf-8")
    m = _TITLE_RE.search(text)
    if m is None:
        return None
    date = _DATE_META_RE.search(text)
    page = Page(
        path=path,
        rel=rel,
        locale=locale,
        title=_html.unescape(m.group(1).strip()),
        desc=read_description(text[:65536]),
        indexable=indexable,
        published=date.group(1) if date and re.search(r"/\d{4}-\d{2}-\d{2}-", "/" + rel) else "",
    )
    return page, text


def make_unique(entries: list[tuple[Path, str, str, bool]]) -> int:
    """Apply both steps to ``(path, rel, locale, indexable)`` entries.

    Returns the number of pages rewritten.
    """
    loaded = [x for x in (load_page(*e) for e in entries) if x is not None]
    pages = [p for p, _ in loaded]
    for p in pages:
        add_context(p)
    resolve_collisions(pages, "title")
    resolve_collisions(pages, "desc")
    written = 0
    for page, text in loaded:
        out = render(page, text)
        if out != text:
            page.path.write_text(out, encoding="utf-8")
            written += 1
    return written
