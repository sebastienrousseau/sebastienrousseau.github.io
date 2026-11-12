# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Read the JSON-LD blocks out of an HTML fragment, for tests.

Uses the standard library's HTML parser rather than a regular
expression, so tag case and spacing (``<SCRIPT >``, ``</script >``)
cannot hide a block.
"""

from __future__ import annotations

import json
from html.parser import HTMLParser
from typing import Any


class _Collector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.blocks: list[str] = []
        self._buf: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "script" and ("type", "application/ld+json") in attrs:
            self._buf = []

    def handle_data(self, data: str) -> None:
        if self._buf is not None:
            self._buf.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._buf is not None:
            self.blocks.append("".join(self._buf))
            self._buf = None


def blocks(html: str) -> list[Any]:
    """Every JSON-LD block in ``html``, parsed, in document order."""
    collector = _Collector()
    collector.feed(html)
    collector.close()
    return [json.loads(b) for b in collector.blocks]


def first(html: str) -> Any:
    """The first JSON-LD block in ``html``; fails if there is none."""
    found = blocks(html)
    assert found, "no JSON-LD block"
    return found[0]
