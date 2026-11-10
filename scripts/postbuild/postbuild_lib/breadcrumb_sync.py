# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Make each BreadcrumbList name what the visible breadcrumb shows (plan F-3).

The translation pipeline localises the visible crumbs and the JSON-LD
crumb names from different sources, so a translated page could show
"Start > Themen" while its structured data said "Startseite > Themen -
Sebastien Rousseau". Search engines display the structured crumbs, so they
must say what the reader sees. When a page's visible breadcrumb has as
many crumbs as its BreadcrumbList, this pass copies the visible names, in
order, into the list. Runs before the CSP pass hashes the JSON-LD.
``tests/validation/test_breadcrumbs_match.py`` checks the result.
"""

from __future__ import annotations

import html
import json
import re

_NAV_RE = re.compile(r'<nav[^>]*aria-label="Breadcrumb"[^>]*>(.*?)</nav>', re.S | re.I)
_LI_RE = re.compile(r"<li[^>]*>(.*?)</li>", re.S)
_INLINE_RE = re.compile(r"<(?:a|span)\b[^>]*>(.*?)</(?:a|span)>", re.S)
_TAG_RE = re.compile(r"<[^>]+>")
_LD_RE = re.compile(r'(<script[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)', re.S | re.I)


def visible_names(page_html: str) -> list[str] | None:
    nav = _NAV_RE.search(page_html)
    if not nav:
        return None
    crumbs = _LI_RE.findall(nav.group(1)) or _INLINE_RE.findall(nav.group(1))
    return [" ".join(html.unescape(_TAG_RE.sub("", c)).split()) for c in crumbs]


def _lists(node: object) -> list[dict]:
    if isinstance(node, dict):
        own = [node] if node.get("@type") == "BreadcrumbList" else []
        return own + [n for v in node.values() for n in _lists(v)]
    if isinstance(node, list):
        return [n for v in node for n in _lists(v)]
    return []


def _rename(crumbs: dict, names: list[str]) -> bool:
    items = sorted(crumbs.get("itemListElement", []), key=lambda i: i.get("position", 0))
    if len(items) != len(names) or [i.get("name") for i in items] == names:
        return False
    for item, name in zip(items, names, strict=True):
        item["name"] = name
    return True


def sync_breadcrumbs(page_html: str) -> str:
    names = visible_names(page_html)
    if not names:
        return page_html

    def repl(m: re.Match[str]) -> str:
        try:
            data = json.loads(m.group(2))
        except json.JSONDecodeError:
            return m.group(0)
        changed = [_rename(c, names) for c in _lists(data)]
        if not any(changed):
            return m.group(0)
        return m.group(1) + json.dumps(data, ensure_ascii=False) + m.group(3)

    return _LD_RE.sub(repl, page_html)
