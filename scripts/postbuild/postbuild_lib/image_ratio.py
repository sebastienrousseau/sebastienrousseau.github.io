# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Give every stock ``<img>`` the aspect ratio of the file it loads.

A page's hero and card images come from ``cloudcdn.pro/stocks/images/``,
and their ``width``/``height`` come from front matter or the 1200x675
default in ``seo.stamp_image_dimensions``. Neither knows the file: the
same 2584x1597 photo shipped as 1200x675, 1600x1000 and 800x800, so the
browser reserved a box of the wrong shape and the page shifted when the
image arrived.

``_data/stock_image_dims.json`` records each original's true size
(``scripts/editorial/stock_image_dims.py``). The ``-320/-640/-1200/-1920``
variants are scaled copies, so they share its ratio. This pass keeps the
declared ``width`` (it drives the srcset threshold and the layout box) and
sets ``height`` to match; ``og:image:height`` is corrected the same way.
"""

from __future__ import annotations

import json
import re
from functools import cache
from pathlib import Path

MANIFEST = Path(__file__).resolve().parents[3] / "_data" / "stock_image_dims.json"
_STEM_RE = re.compile(
    r"https://cloudcdn\.pro/stocks/images/([A-Za-z0-9_.-]+?)(?:-(?:320|640|1200|1920))?\.webp(?=[\"'?#\s>]|$)"
)
_IMG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
_SRC_RE = re.compile(r"""\bsrc=["']([^"']+)["']""", re.IGNORECASE)
_WIDTH_RE = re.compile(r"""\bwidth=["'](\d+)["']""", re.IGNORECASE)
_HEIGHT_RE = re.compile(r"""\bheight=["'](\d+)["']""", re.IGNORECASE)
_OG_IMAGE_RE = re.compile(r'<meta\s+property="og:image"\s+content="([^"]+)"', re.IGNORECASE)
_OG_WIDTH_RE = re.compile(r'(<meta\s+property="og:image:width"\s+content=")(\d+)(")', re.IGNORECASE)
_OG_HEIGHT_RE = re.compile(
    r'(<meta\s+property="og:image:height"\s+content=")(\d+)(")', re.IGNORECASE
)


@cache
def load_dims(path: Path = MANIFEST) -> dict[str, tuple[int, int]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {stem: (int(w), int(h)) for stem, (w, h) in raw.items()}


def true_height(src: str, width: int, dims: dict[str, tuple[int, int]]) -> int | None:
    """The height that gives ``width`` the real ratio of ``src``, or None
    when ``src`` is not a known stock image."""
    m = _STEM_RE.search(src)
    if not m or m.group(1) not in dims:
        return None
    w, h = dims[m.group(1)]
    return round(width * h / w)


def _fix_img(tag: str, dims: dict[str, tuple[int, int]]) -> str:
    src, width, height = _SRC_RE.search(tag), _WIDTH_RE.search(tag), _HEIGHT_RE.search(tag)
    if not (src and width and height):
        return tag
    want = true_height(src.group(1), int(width.group(1)), dims)
    if want is None or abs(want - int(height.group(1))) <= 1:
        return tag
    return tag[: height.start(1)] + str(want) + tag[height.end(1) :]


def _fix_og(html: str, dims: dict[str, tuple[int, int]]) -> str:
    image, width, height = (
        _OG_IMAGE_RE.search(html),
        _OG_WIDTH_RE.search(html),
        _OG_HEIGHT_RE.search(html),
    )
    if not (image and width and height):
        return html
    want = true_height(image.group(1), int(width.group(2)), dims)
    if want is None or abs(want - int(height.group(2))) <= 1:
        return html
    return html[: height.start(2)] + str(want) + html[height.end(2) :]


def correct_stock_image_ratio(html: str, dims: dict[str, tuple[int, int]] | None = None) -> str:
    """Correct the height of every stock ``<img>`` and of ``og:image``."""
    table = load_dims() if dims is None else dims
    if "cloudcdn.pro/stocks/images/" not in html:
        return html
    return _fix_og(_IMG_RE.sub(lambda m: _fix_img(m.group(0), table), html), table)
