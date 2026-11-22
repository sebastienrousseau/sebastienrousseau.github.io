# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Link an English article to its Medium copy.

Articles syndicated to Medium (``_data/medium/publications.json``) get one
line under the byline naming the publication that carries them, so a
reader who follows the author there can find the same piece, and the
publication gets a link from the canonical source. The Medium copy's own
canonical link points here, so this adds no duplicate-content signal.
"""

from __future__ import annotations

import sys
from html import escape as _esc
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
import _medium
from postbuild_lib.article_furniture import BASE_URL, CANONICAL_RE, WRAP_CLOSE_RE

_MARK = "medium-xpost"


def _english_slug(html: str) -> str | None:
    """The article slug when the page's canonical is a root (English) URL."""
    m = CANONICAL_RE.search(html)
    if not m or not m.group(1).startswith(BASE_URL + "/"):
        return None
    path = m.group(1)[len(BASE_URL) + 1 :].removesuffix("index.html").strip("/")
    return path if path and "/" not in path else None


def inject_medium_xpost(html: str) -> str:
    """Add the "Also published on Medium" line to a syndicated article.

    BlogPosting pages only, English only (Medium carries the English
    text); idempotent.
    """
    if '"@type":"BlogPosting"' not in html or f' {_MARK}"' in html:
        return html
    slug = _english_slug(html)
    entry = _medium.story(slug) if slug else None
    if entry is None:
        return html
    pub = _medium.publications().get(entry["publication"])
    where = f"in {_esc(pub['name'])} " if pub else ""
    line = (
        f'<p class="byline-strap {_MARK}">Also published {where}on '
        f'<a href="{_esc(entry["url"], quote=True)}" rel="noopener">Medium</a>.</p>'
    )
    return WRAP_CLOSE_RE.sub(line + r"\1", html, count=1)
