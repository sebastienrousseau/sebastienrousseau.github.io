# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Fit titles and descriptions to what search results show (plan F-2).

Posts carry a ``seo_title`` and a description written to length
(``seo_title.py`` uses them). Generated pages do not: tag, category and topic
landings take their description from ``tags.json`` or ``taxonomy.yml`` (up
to 320 characters) and ``unique_meta`` appends the site name to titles,
so search engines cut them mid-word. ``finalize_seo`` runs this pass twice:
descriptions before ``make_unique``, whose page labels must survive to keep
listing pages distinct, and titles after it, so the site name it appends is
dropped again where it does not fit. Every indexable page is fitted:

* a title over its limit loses the site-name suffix (" | Sebastien
  Rousseau" or " — Sebastien Rousseau"), and nothing else;
* a description over its limit is cut after the last full sentence that
  fits, or else at the last word boundary, ending with an ellipsis.

The og:/twitter: mirrors follow. Limits: 60 / 160 characters for
alphabetic scripts, 30 / 80 for Chinese and Japanese, 35 / 100 for Korean.
"""

from __future__ import annotations

import html as _html
import re
from collections.abc import Callable
from pathlib import Path

SUFFIXES = (" | Sebastien Rousseau", " — Sebastien Rousseau")
_LANG_RE = re.compile(r'<html[^>]*\blang="([^"]+)"', re.I)
_TITLE_RE = re.compile(r"<title>([\s\S]*?)</title>", re.I)
_DESC_RE = re.compile(
    r'(<meta\s+(?:name|property)="(?:description|og:description|twitter:description)"\s+content=")([^"]*)(")',
    re.I,
)
_OG_TITLE_RE = re.compile(
    r'(<meta\s+(?:name|property)="(?:og:title|twitter:title)"\s+content=")([^"]*)(")', re.I
)
_SENTENCE_END_RE = re.compile(r"[.!?。！？](?=\s|$)")


def limits(lang: str) -> tuple[int, int]:
    primary = lang.lower().split("-")[0]
    if primary in ("zh", "ja"):
        return 30, 80
    if primary == "ko":
        return 35, 100
    return 60, 160


def fit_title(title: str, limit: int) -> str:
    if len(title) <= limit:
        return title
    for suffix in SUFFIXES:
        if title.endswith(suffix):
            return title[: -len(suffix)]
    return title


def fit_description(desc: str, limit: int) -> str:
    if len(desc) <= limit:
        return desc
    head = desc[:limit]
    ends = [m.end() for m in _SENTENCE_END_RE.finditer(head)]
    if ends and ends[-1] >= limit // 2:
        return head[: ends[-1]].strip()
    cut = head[: limit - 1].rsplit(" ", 1)[0] if " " in head else head[: limit - 1]
    return cut.rstrip(" ,;:") + "…"


def _sub_attr(rx: re.Pattern[str], html: str, fit: Callable[[str], str]) -> str:
    def repl(m: re.Match[str]) -> str:
        value = _html.unescape(m.group(2))
        new = fit(value)
        return m.group(0) if new == value else m.group(1) + _html.escape(new) + m.group(3)

    return rx.sub(repl, html)


def fit_meta(html: str, titles: bool = True, descriptions: bool = True) -> str:
    """Fit the page's title and descriptions to its script's limits."""
    lang = _LANG_RE.search(html)
    t_max, d_max = limits(lang.group(1) if lang else "en")
    title = _TITLE_RE.search(html)
    out = html
    if title and titles:
        value = _html.unescape(title.group(1).strip())
        new = fit_title(value, t_max)
        if new != value:
            out = out[: title.start(1)] + _html.escape(new, quote=False) + out[title.end(1) :]
            out = _sub_attr(_OG_TITLE_RE, out, lambda v: fit_title(v, t_max))
    if not descriptions:
        return out
    return _sub_attr(_DESC_RE, out, lambda v: fit_description(v, d_max))


_NOINDEX_RE = re.compile(r'<meta\s+name="robots"\s+content="[^"]*noindex', re.I)


def apply_meta_length(public: Path, titles: bool = True, descriptions: bool = True) -> int:
    """Fit every indexable page under ``public``. Returns pages changed."""
    changed = 0
    for page in public.rglob("index.html"):
        html = page.read_text(encoding="utf-8")
        if _NOINDEX_RE.search(html):
            continue
        out = fit_meta(html, titles, descriptions)
        if out != html:
            page.write_text(out, encoding="utf-8")
            changed += 1
    return changed
