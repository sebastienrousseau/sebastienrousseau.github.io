# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Use the post's ``seo_title`` for ``<title>`` when the title is too long.

ssg writes the front matter ``title`` into ``<title>``, ``og:title`` and the
H1, and ignores ``seo_title``, so a 120-character headline became a
120-character search title that Google cuts off. This pass maps each page's
canonical URL to its source ``seo_title`` (English and translated posts
alike) and, when the ``<title>`` is longer than its script's limit, puts the
``seo_title`` there instead, adding " | Sebastien Rousseau" only when the
result still fits. The H1 and the social titles keep the full headline.

Limits: 60 characters for Latin and other alphabetic scripts, 30 for
Chinese and Japanese, 35 for Korean (plan F-2).
"""

from __future__ import annotations

import html as _html
import re
from functools import cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SITE = "https://sebastienrousseau.com"
SUFFIX = " | Sebastien Rousseau"
_LIMITS = {"zh": 30, "ja": 30, "ko": 35}
_DEFAULT_LIMIT = 60
_FM_RE = re.compile(r"\A---\n(.*?)\n---", re.S)
_PERMALINK_RE = re.compile(r'^(?:permalink|url):\s*"?([^"\n]+)"?\s*$', re.M)
_SEO_TITLE_RE = re.compile(r'^seo_title:\s*"((?:[^"\\]|\\.)*)"\s*$', re.M)
_CANONICAL_RE = re.compile(r'<link rel="canonical" href="([^"]+)"', re.I)
_TITLE_RE = re.compile(r"<title>([\s\S]*?)</title>", re.I)
_LANG_RE = re.compile(r'<html[^>]*\blang="([^"]+)"', re.I)


def _key(url: str) -> str:
    return url.strip().removesuffix("index.html").rstrip("/")


def _unescape_yaml(value: str) -> str:
    return value.replace('\\"', '"').replace("\\\\", "\\")


@cache
def seo_titles(posts: Path = ROOT / "_posts") -> dict[str, str]:
    """Canonical URL (no trailing slash) -> seo_title, by permalink and by path."""
    out: dict[str, str] = {}
    for path in posts.rglob("*.md"):
        fm = _FM_RE.match(path.read_text(encoding="utf-8"))
        if not fm:
            continue
        link, seo = _PERMALINK_RE.search(fm.group(1)), _SEO_TITLE_RE.search(fm.group(1))
        if not seo:
            continue
        title = _unescape_yaml(seo.group(1))
        # The builder serves _posts/<lang>/<slug>.md at /<lang>/<slug>/, so a
        # translation is keyed by its path only: some copied the English
        # permalink into their front matter, which must not carry their
        # title onto the English page. English posts are keyed by both.
        rel = path.relative_to(posts).with_suffix("").as_posix()
        out[_key(f"{SITE}/{rel}")] = title
        if link and "/" not in rel:
            out[_key(link.group(1))] = title
    return out


def limit_for(lang: str) -> int:
    """Title limit for a BCP-47 tag (``ja-JP``, ``zh-Hans``, ``ko-KR``)."""
    return _LIMITS.get(lang.lower().split("-")[0], _DEFAULT_LIMIT)


def choose(title: str, seo: str, limit: int) -> str | None:
    """The new title text, or None to keep ``title``."""
    if len(title) <= limit or not seo or len(seo) > limit:
        return None
    return seo + SUFFIX if len(seo) + len(SUFFIX) <= limit else seo


def apply_seo_title(html: str, table: dict[str, str] | None = None) -> str:
    """Rewrite ``<title>`` from the page's ``seo_title`` when it is too long."""
    canonical, title = _CANONICAL_RE.search(html), _TITLE_RE.search(html)
    if not (canonical and title):
        return html
    seo = (seo_titles() if table is None else table).get(_key(canonical.group(1)))
    if not seo:
        return html
    lang = _LANG_RE.search(html)
    current = _html.unescape(title.group(1).strip())
    new = choose(current, seo, limit_for(lang.group(1) if lang else "en"))
    if new is None:
        return html
    return html[: title.start(1)] + _html.escape(new, quote=False) + html[title.end(1) :]
