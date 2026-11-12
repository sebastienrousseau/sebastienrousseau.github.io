# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Each locale's slug map points at the translation of the right article.

``_data/i18n/<lang>/slugs.json`` maps every English article slug to its
translated file, and hreflang, the language menu and the translation tools
all follow it. Two articles published on the same day were cross-mapped in
most locales (62 pairs, found in v0.0.36), so a reader switching language
landed on the other article. Titles are translated, so the check compares
what translation leaves alone: the external links in the body. A
translation must share more of them with its own English article than
with any other article of the same date.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from functools import cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POSTS = ROOT / "_posts"
_URL_RE = re.compile(r'https?://[^\s"\)<>\]]+')
_OWN = ("sebastienrousseau.com", "cloudcdn.pro")
MARGIN = 0.2


@cache
def links(path: Path) -> frozenset[str]:
    if not path.is_file():
        return frozenset()
    text = path.read_text(encoding="utf-8")
    body = text.split("---", 2)[2] if text.startswith("---") else text
    return frozenset(u for u in _URL_RE.findall(body) if not any(o in u for o in _OWN))


def jaccard(a: frozenset[str], b: frozenset[str]) -> float:
    union = a | b
    return len(a & b) / len(union) if a and b else 0.0


def cross_mapped(lang: str, articles: dict[str, str], posts: Path = POSTS) -> list[str]:
    by_date: dict[str, list[str]] = defaultdict(list)
    for slug in articles:
        by_date[slug[:10]].append(slug)
    bad: list[str] = []
    for en_slug, native in articles.items():
        target = links(posts / lang / f"{native}.md")
        own = jaccard(links(posts / f"{en_slug}.md"), target)
        bad.extend(
            f"{lang}: {en_slug} -> {native} reads like {other}"
            for other in by_date[en_slug[:10]]
            if other != en_slug and jaccard(links(posts / f"{other}.md"), target) > own + MARGIN
        )
    return bad


def test_slug_maps_point_at_their_own_translation() -> None:
    bad: list[str] = []
    for slugs in sorted((ROOT / "_data" / "i18n").glob("*/slugs.json")):
        articles = json.loads(slugs.read_text(encoding="utf-8")).get("articles", {})
        bad += cross_mapped(slugs.parent.name, articles)
    assert not bad, "\n".join(bad[:20])


def test_detector_flags_a_swap(tmp_path: Path) -> None:
    (tmp_path / "xx").mkdir()
    for name, url in (
        ("2026-01-01-a", "https://a.example/1"),
        ("2026-01-01-b", "https://b.example/2"),
    ):
        (tmp_path / f"{name}.md").write_text(f"---\nt: 1\n---\n{url}\n", encoding="utf-8")
        (tmp_path / "xx" / f"{name}-xx.md").write_text(f"---\nt: 1\n---\n{url}\n", encoding="utf-8")
    swapped = {"2026-01-01-a": "2026-01-01-b-xx", "2026-01-01-b": "2026-01-01-a-xx"}
    assert len(cross_mapped("xx", swapped, tmp_path)) == 2
    right = {"2026-01-01-a": "2026-01-01-a-xx", "2026-01-01-b": "2026-01-01-b-xx"}
    assert cross_mapped("xx", right, tmp_path) == []
