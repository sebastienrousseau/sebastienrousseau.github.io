# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Read the page's own BlogPosting node out of its JSON-LD.

Every dated article carries a BlogPosting from its layout and, from
``schemas.inject_tech_article``, a TechArticle or ScholarlyArticle sibling.
The sibling is a second Article entity for the same page, so it needs the
same publication dates and lead image; this is where it gets them, rather
than re-deriving values the layout already settled.
"""

from __future__ import annotations

import json
import re

_LD_RE = re.compile(r'<script type="application/ld\+json"[^>]*>([\s\S]*?)</script>', re.I)
INHERITED = ("datePublished", "dateModified", "image")
_DIMENSIONS = ("width", "height")


def _find(data: object) -> dict | None:
    if isinstance(data, list):
        return next((n for n in map(_find, data) if n is not None), None)
    if not isinstance(data, dict):
        return None
    if data.get("@type") == "BlogPosting":
        return data
    return _find(list(data.values()))


def blogposting_node(html: str) -> dict | None:
    """The first BlogPosting node on the page, or None."""
    for raw in _LD_RE.findall(html):
        try:
            node = _find(json.loads(raw))
        except ValueError:
            continue
        if node is not None:
            return node
    return None


def inherited_fields(html: str) -> dict[str, object]:
    """The BlogPosting's dates and image, for an Article-family sibling."""
    node = blogposting_node(html) or {}
    return {key: node[key] for key in INHERITED if node.get(key)}


def drop_css_dimensions(node: dict) -> bool:
    """Remove image ``width``/``height`` values that are not pixel counts.

    ``banner_width: "100vw"`` front matter reached the layout's ImageObject
    as ``"width":"100vw","height":"100vh"``. Dropping a CSS unit is safe;
    guessing a pixel size is not. Returns True when anything was removed."""
    image = node.get("image")
    if not isinstance(image, dict):
        return False
    bad = [key for key in _DIMENSIONS if key in image and not str(image[key]).isdigit()]
    for key in bad:
        del image[key]
    return bool(bad)
