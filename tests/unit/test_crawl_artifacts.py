# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Markup and robots rules that stop crawlers inventing URLs.

Search Console listed ``/*``, ``/*.pdf``, ``/contact/*`` and ``/_csp/*`` as
404s: Googlebot read the ``href_matches`` patterns of the inline
speculation rules as links. It also listed ``/cdn-cgi/l/email-protection``,
Cloudflare's address-obfuscation endpoint, which no page needs crawled.
"""

from __future__ import annotations

import json

from postbuild_lib.content_blocks import SPECULATION_RULES_BLOCK
from postbuild_lib.output import write_robots

_OPEN = '<script type="speculationrules">'
_CLOSE = "</script>"


def _rules() -> dict:
    block = SPECULATION_RULES_BLOCK
    assert block.startswith(_OPEN), "speculation rules block lost its opening tag"
    assert block.endswith(_CLOSE), "speculation rules block lost its closing tag"
    return json.loads(block[len(_OPEN) : -len(_CLOSE)])


def _strings(node) -> list[str]:
    if isinstance(node, dict):
        return [s for v in node.values() for s in _strings(v)]
    if isinstance(node, list):
        return [s for v in node for s in _strings(v)]
    return [node] if isinstance(node, str) else []


def test_speculation_rules_hold_no_path_like_string():
    """No JSON string starts with "/", so no crawler reads one as a URL."""
    paths = [s for s in _strings(_rules()) if s.startswith("/")]
    assert paths == []


def test_speculation_rules_still_exclude_the_same_targets():
    selector = _rules()["prerender"][0]["where"]["not"]["selector_matches"]
    for needle in ('"_csp/"', '".xml"', '".json"', '".txt"', '".pdf"', '"sw.js"', '"contact/"'):
        assert needle in selector, f"prerender no longer skips {needle}"


def test_speculation_rules_keep_moderate_eagerness():
    assert _rules()["prerender"][0]["eagerness"] == "moderate"


def test_robots_keeps_every_crawler_out_of_cdn_cgi(tmp_path):
    write_robots(tmp_path)
    groups = (tmp_path / "robots.txt").read_text(encoding="utf-8").split("User-agent:")[1:]
    allowing = [g for g in groups if "\nAllow: /\n" in g]
    assert allowing, "robots.txt has no allowing group"
    for group in allowing:
        assert "\nDisallow: /cdn-cgi/\n" in group, group.splitlines()[0]
