# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Set every sitemap ``<lastmod>`` to the page's real modification date.

Before this pass 3,795 of the 7,679 ``<loc>`` entries in the live sitemap
carried ``2026-05-11``: ssg stamps one date on every entry it writes, and
``feeds.augment_sitemap_with_rendered_pages`` copied the first ``<lastmod>``
it found onto every page it appended. A sitemap where half the URLs share
one date tells a crawler the field is noise, and Google then ignores it.

The date for each URL, in order:

1. *Source date*: the page's own Markdown source front matter
   (``last_reviewed``, else ``last_build_date``, else ``date``), found the
   same way ``update_last_modified_date`` finds it: the URL's slug,
   reverse-mapped to the English slug for a locale page. A translation
   shares its English source's review date.
2. *Listing date*: for a listing page (the home page, article pagination,
   year archives, tags, categories, topics), the newest date among the
   article pages it links to. A listing changes when an article it lists
   changes, so this is when its content last changed. Applies on top of a
   source date when the listing also has one.
3. Neither: the ``<lastmod>`` element is removed. An absent lastmod is
   honest; the build date is not, because the build clock is pinned to the
   last commit and would stamp every unchanged page as changed.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import _lang_registry as _lr
from postbuild_lib.hreflang import _resolve_en_slug
from postbuild_lib.unique_meta import is_listing

SITE = "https://sebastienrousseau.com"
_URL_BLOCK_RE = re.compile(r"<url>[\s\S]*?</url>")
_LOC_RE = re.compile(r"<loc>\s*([^<\s]+)\s*</loc>")
_LASTMOD_RE = re.compile(r"\s*<lastmod>[^<]*</lastmod>")
_HREF_RE = re.compile(r'href=["\']?(?:https://sebastienrousseau\.com)?(/[^"\'\s>#?]*)')
_ARTICLE_RE = re.compile(r"(?:^|/)\d{4}-\d{2}-\d{2}-[^/]+/$")


def url_path(loc: str) -> str | None:
    """``https://site/fr/x/`` -> ``/fr/x/``; None for off-site URLs."""
    if loc.rstrip("/") == SITE:
        return "/"
    return unquote(loc[len(SITE) :]) if loc.startswith(SITE + "/") else None


def split_locale(path: str, codes: frozenset[str]) -> tuple[str, list[str]]:
    """``/fr/a/b/`` -> (``fr``, [``a``, ``b``]); EN paths get ``en``."""
    parts = [p for p in path.split("/") if p]
    if parts and parts[0] in codes:
        return parts[0], parts[1:]
    return "en", parts


def source_date(path: str, index: dict[str, str], codes: frozenset[str]) -> str:
    """Front-matter date of the page's own source, or ''."""
    locale, parts = split_locale(path, codes)
    if not parts:
        return index.get("index", "")
    if len(parts) != 1:
        return ""
    slug = parts[0]
    return index.get(_resolve_en_slug(slug, locale) or slug, "")


def _rel_file(path: str) -> str:
    return path.lstrip("/") + "index.html" if path.endswith("/") else path.lstrip("/")


def linked_article_dates(html: str, dated: dict[str, str]) -> list[str]:
    """Dates of the article pages ``html`` links to."""
    out = []
    for href in _HREF_RE.findall(html):
        href = href if href.endswith("/") else href + "/"
        if _ARTICLE_RE.search(href) and href in dated:
            out.append(dated[href])
    return out


def compute_lastmods(public: Path, paths: list[str], index: dict[str, str]) -> dict[str, str]:
    """``{url path: YYYY-MM-DD}`` for every path that has a real date."""
    codes = frozenset(lang.code for lang in _lr.active())
    dated = {p: d for p in paths if (d := source_date(p, index, codes))}
    out = dict(dated)
    for path in paths:
        locale, parts = split_locale(path, codes)
        rel = _rel_file(path)
        if parts and not is_listing(rel, locale):
            continue
        page = public / rel
        if not page.is_file():
            continue
        found = linked_article_dates(page.read_text(encoding="utf-8", errors="ignore"), dated)
        if path in dated:
            found.append(dated[path])
        if found:
            out[path] = max(found)
    return out


def _with_lastmod(block: str, date: str | None) -> str:
    stripped = _LASTMOD_RE.sub("", block)
    if not date:
        return stripped
    return re.sub(r"(</loc>)", rf"\1\n  <lastmod>{date}</lastmod>", stripped, count=1)


def refresh_lastmod(public: Path, index: dict[str, str]) -> tuple[int, int]:
    """Rewrite ``public/sitemap.xml`` lastmods. Returns (dated, undated)."""
    sitemap = public / "sitemap.xml"
    text = sitemap.read_text(encoding="utf-8")
    blocks = _URL_BLOCK_RE.findall(text)
    paths = [p for b in blocks if (m := _LOC_RE.search(b)) and (p := url_path(m.group(1)))]
    dates = compute_lastmods(public, paths, index)
    counts = [0, 0]

    def repl(m: re.Match[str]) -> str:
        loc = _LOC_RE.search(m.group(0))
        path = url_path(loc.group(1)) if loc else None
        date = dates.get(path) if path else None
        counts[0 if date else 1] += 1
        return _with_lastmod(m.group(0), date)

    sitemap.write_text(_URL_BLOCK_RE.sub(repl, text), encoding="utf-8")
    return counts[0], counts[1]
