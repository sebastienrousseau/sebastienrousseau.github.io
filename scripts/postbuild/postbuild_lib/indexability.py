# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Keep pages that must not rank out of the index and out of the sitemaps.

Two passes, run last in postbuild, after every pass that writes a page or
a sitemap entry.

*Utility pages* (``404``, ``offline``, ``thanks``) exist in EN and in every
active locale under the locale's static slug (``/fr/hors-ligne/``,
``/de/danke/``). GitHub Pages serves ``/404/`` and ``/<lang>/404/`` with a
200, and ssg stamps every page ``max-snippet:-1, ...`` with no ``noindex``,
so Search Console filed five of them as Soft 404. Each one gets
``<meta name="robots" content="noindex, follow">`` instead.

*Sitemaps* list only URLs a crawler should index. A ``<loc>`` is dropped
when its page is not in ``public/``, is a meta-refresh redirect page,
carries ``noindex``, or canonicalises to a different URL. Before this pass
the root sitemap listed all 34 locale ``/404/`` pages and every locale
``offline`` / ``thanks`` fork, because the exclusion list in
``feeds._SITEMAP_EXCLUDE_TAILS`` only named the EN and FR paths.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import _lang_registry as _lr
from postbuild_lib._i18n import _all_active_non_en_langs
from postbuild_lib.article_furniture import BASE_URL, PUBLIC

# Static-page keys that are utility pages, not content. Locale slugs come
# from each locale's slug map (``static`` section).
UTILITY_KEYS = ("404", "offline", "thanks")
NOINDEX_META = '<meta name="robots" content="noindex, follow">'

_ROBOTS_META_RE = re.compile(r'<meta\s+name=["\']robots["\'][^>]*>', re.IGNORECASE)
_NOINDEX_RE = re.compile(
    r'<meta\s+name=["\']robots["\']\s+content=["\'][^"\']*noindex', re.IGNORECASE
)
_REFRESH_RE = re.compile(r'<meta\s+http-equiv=["\']?refresh', re.IGNORECASE)
_CANONICAL_RE = re.compile(
    r'<link\b[^>]*\brel=["\']?canonical["\']?[^>]*\bhref=["\']?([^"\'\s>]+)', re.IGNORECASE
)
_HEAD_OPEN_RE = re.compile(r"<head\b[^>]*>", re.IGNORECASE)
_URL_BLOCK_RE = re.compile(r"<url>[\s\S]*?</url>")
_LOC_RE = re.compile(r"<loc>([^<]+)</loc>")
_HEAD_BYTES = 65536


def utility_pages(public: Path = PUBLIC) -> list[Path]:
    """Every rendered utility page, EN first, then each active locale."""
    pages = [public / key / "index.html" for key in UTILITY_KEYS]
    for code in _all_active_non_en_langs():
        statics = _lr.load_slugs(code).get("static", {})
        pages.extend(public / code / statics.get(key, key) / "index.html" for key in UTILITY_KEYS)
    return [p for p in pages if p.is_file()]


def set_noindex(html: str) -> str:
    """Replace every robots meta with ``noindex, follow``, or add one."""
    if _ROBOTS_META_RE.search(html):
        out = _ROBOTS_META_RE.sub(NOINDEX_META, html, count=1)
        # Drop any further robots metas so no ``index`` directive survives.
        head, sep, tail = out.partition(NOINDEX_META)
        return head + sep + _ROBOTS_META_RE.sub("", tail)
    m = _HEAD_OPEN_RE.search(html)
    if not m:
        return html
    return html[: m.end()] + NOINDEX_META + html[m.end() :]


def apply_noindex_utility_pages(public: Path = PUBLIC) -> int:
    """Mark every utility page ``noindex``. Returns pages changed."""
    changed = 0
    for page in utility_pages(public):
        html = page.read_text(encoding="utf-8")
        out = set_noindex(html)
        if out != html:
            page.write_text(out, encoding="utf-8")
            changed += 1
    return changed


def _norm(url: str) -> str:
    url = unquote(url.strip())
    if url.endswith("/index.html"):
        url = url[: -len("index.html")]
    return url.rstrip("/")


def _page_for(loc: str, public: Path) -> Path | None:
    """Map an absolute ``<loc>`` onto its file in ``public/``."""
    if loc == BASE_URL:
        loc += "/"
    if not loc.startswith(BASE_URL + "/"):
        return None
    rel = unquote(loc[len(BASE_URL) + 1 :])
    if rel == "" or rel.endswith("/"):
        rel += "index.html"
    return public / rel


def _read_head(page: Path) -> str:
    with page.open("r", encoding="utf-8", errors="ignore") as fh:
        return fh.read(_HEAD_BYTES)


def is_indexable(loc: str, public: Path = PUBLIC) -> bool:
    """True when ``loc`` renders, is not a redirect, is not ``noindex``,
    and canonicalises to itself."""
    page = _page_for(loc, public)
    if page is None or not page.is_file():
        return False
    if page.suffix != ".html":
        return True
    head = _read_head(page)
    if _REFRESH_RE.search(head) or _NOINDEX_RE.search(head):
        return False
    m = _CANONICAL_RE.search(head)
    return m is None or _norm(m.group(1)) == _norm(loc)


def _sitemaps(public: Path) -> list[Path]:
    """Root sitemaps plus the per-locale news sitemaps."""
    roots = sorted(public.glob("*sitemap*.xml"))
    return roots + sorted(public.glob("*/news-sitemap.xml"))


def prune_sitemaps(public: Path = PUBLIC) -> int:
    """Drop every ``<url>`` whose ``<loc>`` is not indexable. Returns the
    number of entries removed across all sitemaps."""
    removed = 0
    for sm in _sitemaps(public):
        text = sm.read_text(encoding="utf-8")

        def keep(m: re.Match[str]) -> str:
            nonlocal removed
            loc = _LOC_RE.search(m.group(0))
            if loc and not is_indexable(loc.group(1).strip(), public):
                removed += 1
                return ""
            return m.group(0)

        new = _URL_BLOCK_RE.sub(keep, text)
        if new != text:
            sm.write_text(new, encoding="utf-8")
    return removed
