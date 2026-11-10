# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""scripts/generators/build_topic_hubs.py: the G-1 topic hubs."""

from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path

import build_topic_hubs as th

TODAY = dt.date(2026, 11, 10)
HUB = {
    "path": "/iso-20022/",
    "title": "t",
    "description": "d",
    "h1": "ISO 20022",
    "answer": "An answer.",
    "at_a_glance": [
        {"text": "Fact one.", "source": "https://www.iso20022.org/", "last_verified": "2026-11-10"}
    ],
    "paths": [{"audience": "Engineers and architects", "slugs": ["2026-01-01-a"]}],
    "tags": ["iso-20022"],
    "faq": [{"q": "What is it?", "a": "A standard."}],
    "roadmap": [
        {
            "date": "2026-11",
            "text": "Milestone.",
            "source": "https://www.swift.com/",
            "last_verified": "2026-11-10",
        }
    ],
}


def _arts(n: int) -> list[dict]:
    return [
        {"slug": f"2026-01-{i:02d}-a", "title": f"A{i}", "tags": {"iso-20022"}}
        for i in range(1, n + 1)
    ]


def test_render_has_every_block_and_valid_jsonld() -> None:
    html = th.render_hub("iso-20022", HUB, _arts(8), "<aside>expert</aside>")
    for marker in ('id="hub-h1"', 'id="hub-glance"', 'id="hub-paths"', 'id="hub-roadmap"', 'id="hub-tools"',
                   'id="hub-latest"', 'id="hub-faq"', "<aside>expert</aside>", "All 8 articles"):  # fmt: skip
        assert marker in html
    ld = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', html).group(1))
    types = [n["@type"] for n in ld["@graph"]]
    assert types == ["CollectionPage", "FAQPage", "BreadcrumbList"]
    assert len(ld["@graph"][0]["hasPart"]) == 8


def test_hubs_without_roadmap_tools_or_older_articles() -> None:
    hub = {k: v for k, v in HUB.items() if k != "roadmap"}
    html = th.render_hub("unknown", hub, _arts(3), "")
    assert (
        'id="hub-roadmap"' not in html
        and 'id="hub-tools"' not in html
        and "<details><summary>All" not in html
    )


def test_check_counts_articles_sources_and_age() -> None:
    assert th.check("iso-20022", HUB, _arts(20), TODAY) == ([], [])
    errors, _ = th.check("iso-20022", HUB, _arts(5), TODAY)
    assert "5 linked articles" in errors[0]
    stale = {
        **HUB,
        "at_a_glance": [
            {"text": "Old.", "source": "s", "last_verified": "2026-06-01"},
            {"text": "No source."},
        ],
    }
    errors, _ = th.check("iso-20022", stale, _arts(20), TODAY)
    assert any("162 days" in e for e in errors) and any("without source" in e for e in errors)
    due = {**HUB, "at_a_glance": [{"text": "Due.", "source": "s", "last_verified": "2026-08-01"}]}
    assert th.check("iso-20022", due, _arts(20), TODAY)[1]


def test_articles_resolve_tags_through_aliases(tmp_path: Path) -> None:
    (tmp_path / "2026-01-02-b.md").write_text(
        '---\ntitle: "B"\ntags: "ISO 20022, other"\n---\nx\n', encoding="utf-8"
    )
    (tmp_path / "2026-01-01-a.md").write_text(
        "---\ntitle: A\ntags: [AI]\n---\nx\n", encoding="utf-8"
    )
    (tmp_path / "about.md").write_text("---\ntitle: About\n---\n", encoding="utf-8")
    index = th.tag_slugs(
        {"iso-20022": {"name": "ISO 20022", "aliases": []}, "ai": {"name": "AI"}, "x": "y"}
    )
    arts = th.articles(tmp_path, index)
    assert [a["slug"] for a in arts] == ["2026-01-02-b", "2026-01-01-a"]
    assert arts[0]["tags"] == {"iso-20022"} and arts[1]["tags"] == {"ai"}
    assert [a["slug"] for a in th.hub_articles(HUB, arts)] == ["2026-01-02-b"]
