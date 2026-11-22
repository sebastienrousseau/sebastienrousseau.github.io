# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""The Medium publications that syndicate this site's articles.

``_data/medium/publications.json`` holds the three publications (Banking On
AI, Banking On Quantum, Banking On Cloud Native) and which Medium story
copies which English article. Each Medium copy carries a canonical link
back to the article here, so search engines credit this site; these
helpers let the build link the other way.
"""

from __future__ import annotations

import json
from functools import cache
from pathlib import Path
from typing import Any

DATA = Path(__file__).resolve().parents[2] / "_data" / "medium" / "publications.json"
STORY_URL = "https://medium.com/p/{id}"
PUBLICATION_ORDER = ("ai", "quantum", "cloud-native")


@cache
def _payload() -> dict[str, Any]:
    data: dict[str, Any] = json.loads(DATA.read_text(encoding="utf-8"))
    return data


def publications() -> dict[str, dict[str, str]]:
    """The three publications, in display order."""
    pubs = _payload()["publications"]
    return {key: pubs[key] for key in PUBLICATION_ORDER}


def story(slug: str) -> dict[str, str] | None:
    """The Medium story for an English article slug, with its ``url``."""
    entry = _payload()["stories"].get(slug)
    if entry is None:
        return None
    return {**entry, "url": STORY_URL.format(id=entry["id"])}


def slugs_by_publication() -> dict[str, list[str]]:
    """Article slugs per publication key, newest first."""
    out: dict[str, list[str]] = {key: [] for key in PUBLICATION_ORDER}
    for slug, entry in sorted(_payload()["stories"].items(), reverse=True):
        if entry["publication"] in out:
            out[entry["publication"]].append(slug)
    return out
