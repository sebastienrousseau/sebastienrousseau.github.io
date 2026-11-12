# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""One "Share · Cite" menu at the top of each article (plan C-4).

Replaces the sticky share rail and action rail: a native ``<details>``
(no JavaScript needed to open it) holding the same share links as the
rail, the Save PDF button, a link to the citation formats and a link to
the reuse licence. Labels come from the locale's ``labels.json`` (the
ones the rails used), so every translation is already in place.
BlogPosting pages only; idempotent.
"""

from __future__ import annotations

from html import escape as _esc

from postbuild_lib._i18n import _labels
from postbuild_lib.article_furniture import MAIN_RE, SVG_DOWNLOAD
from postbuild_lib.sharing import _share_payload, _share_rail_items

MARKER = 'class="article-tools"'


def inject_tools_menu(html: str) -> str:
    if '"@type":"BlogPosting"' not in html or MARKER in html:
        return html
    payload = _share_payload(html)
    if payload is None:
        return html
    labels = _labels(html)
    share, cite = labels.get("Share", "Share"), labels.get("Action.cite", "Cite")
    reuse = labels.get("Reuse.heading", "Republish this article")
    items = (
        _share_rail_items(payload, labels) + f'<li><button type="button" data-print>{SVG_DOWNLOAD}'
        f"<span>{_esc(labels.get('Action.savePdf', 'Save PDF'))}</span></button></li>"
        f'<li><a href="#cite-popover">{_esc(cite)}</a></li>'
        f'<li><a href="#reuse-heading">{_esc(reuse)}</a></li>'
    )
    menu = (
        f"<details {MARKER}><summary>{_esc(share)} · {_esc(cite)}</summary>"
        f'<ul class="article-tools-list">{items}</ul></details>'
    )
    return MAIN_RE.sub(rf"\1{menu}\2\3", html, count=1)
