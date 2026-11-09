# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Rebuild the site's Person JSON-LD from ``_data/profile.yml``.

Every layout carries a ``@graph`` with the ``#person`` node. Its job title,
description, employer, schools, memberships, credentials and awards come
from :func:`_profile.person_fields`, merged over the layout's node, so a
page can never state a profile fact the profile does not. The properties
the theme owns (``knowsAbout``, ``sameAs``, ``image``, ``identifier``,
``subjectOf``) are left as they are. The ``#website`` description takes
the profile's one-line bio for the same reason.

Runs before ``inject_jsonld_hashes`` so the CSP hash covers the new bytes.
"""

from __future__ import annotations

import json
import re
from typing import Any

import _profile

BASE = "https://sebastienrousseau.com"
PERSON_ID = f"{BASE}/#person"
WEBSITE_ID = f"{BASE}/#website"
_LDJSON_BLOCK_RE = re.compile(
    r'(<script[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)',
    re.IGNORECASE | re.DOTALL,
)


def _merge(node: dict[str, Any], fields: dict[str, Any]) -> bool:
    changed = False
    for key, value in fields.items():
        if node.get(key) != value:
            node[key] = value
            changed = True
    return changed


def _patch_node(node: dict[str, Any], person: dict[str, Any], site: dict[str, Any]) -> bool:
    if node.get("@id") == PERSON_ID and node.get("@type") == "Person":
        return _merge(node, person)
    if node.get("@id") == WEBSITE_ID:
        return _merge(node, site)
    return False


def _walk(data: object, person: dict[str, Any], site: dict[str, Any]) -> bool:
    changed = False
    if isinstance(data, dict):
        changed |= _patch_node(data, person, site)
        for value in data.values():
            changed |= _walk(value, person, site)
    elif isinstance(data, list):
        for item in data:
            changed |= _walk(item, person, site)
    return changed


def apply_person_profile(html: str) -> str:
    """Merge profile.yml's facts into the page's #person and #website
    nodes. Pages without them, and blocks that are not valid JSON, pass
    through unchanged."""
    if PERSON_ID not in html and WEBSITE_ID not in html:
        return html
    person = _profile.person_fields(BASE)
    site = {"description": _profile.load()["bios"]["one_line"]}

    def _patch(m: re.Match[str]) -> str:
        body = m.group(2)
        try:
            data = json.loads(body)
        except ValueError:
            return m.group(0)
        if not _walk(data, person, site):
            return m.group(0)
        separators = (",", ":") if '", "' not in body[:200] else (", ", ": ")
        return m.group(1) + json.dumps(data, separators=separators, ensure_ascii=False) + m.group(3)

    return _LDJSON_BLOCK_RE.sub(_patch, html)
