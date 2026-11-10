# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""scripts/seo_and_audit/content_audit.py: the B-3 audit sheet."""

from __future__ import annotations

import csv
import datetime as dt
from pathlib import Path

import content_audit as ca

TAXONOMY = "ai:\n  name: AI\n  category: ai\n  aliases: [Artificial Intelligence]\niso-20022:\n  name: ISO 20022\n  category: payments\n"
TODAY = dt.date(2026, 11, 10)


def _row(**kw: object) -> dict[str, object]:
    base = {"similarity": 0.0, "nearest_pillar": "", "nearest_duplicate": "", "pillar": "ai",
            "words": 900, "impressions_28d": "", "date": dt.date(2026, 10, 1)}  # fmt: skip
    return {**base, **kw}


def test_pillar_resolves_names_and_aliases() -> None:
    index = ca.tag_index(
        {"ai": {"name": "AI", "category": "ai", "aliases": ["Artificial Intelligence"]}, "x": {}}
    )
    assert ca.pillar_of("Artificial Intelligence, AI, other", index) == "ai"
    assert ca.pillar_of(["unknown"], index) == "none"


def test_shingle_similarity() -> None:
    a = ca.shingles(ca.words_of("<p>one two three four five six</p>"))
    assert ca.jaccard(a, a) == 1.0 and ca.jaccard(a, frozenset()) == 0.0


def test_suggestions() -> None:
    assert (
        ca.suggest(_row(similarity=0.4, nearest_pillar="ai", nearest_duplicate="/x/"), TODAY)
        == "merge->/x/"
    )
    assert ca.suggest(_row(pillar="none", words=300, impressions_28d="0"), TODAY) == "noindex"
    assert ca.suggest(_row(date=dt.date(2025, 1, 1)), TODAY) == "refresh"
    assert ca.suggest(_row(), TODAY) == "keep"
    assert ca.suggest(_row(pillar="none"), TODAY) == "review"


def test_audit_end_to_end(tmp_path: Path) -> None:
    (tmp_path / "_data").mkdir()
    (tmp_path / "_data" / "taxonomy.yml").write_text(TAXONOMY, encoding="utf-8")
    posts = tmp_path / "_posts"
    posts.mkdir()
    body = " ".join(f"word{i}" for i in range(80))
    for name in ("2026-10-01-a-2026", "2026-10-02-b"):
        (posts / f"{name}.md").write_text(
            f'---\ntitle: "{name}"\ntags: "AI"\n---\n{body}\n', encoding="utf-8"
        )
    (posts / "about.md").write_text("---\ntitle: About\n---\nx\n", encoding="utf-8")
    (tmp_path / "public" / "2026-10-02-b").mkdir(parents=True)
    (tmp_path / "public" / "2026-10-02-b" / "index.html").write_text(
        '<a href="/2026-10-01-a-2026/">', encoding="utf-8"
    )
    search = {"https://sebastienrousseau.com/2026-10-01-a-2026": ("12", "1")}
    rows = ca.audit(tmp_path, TODAY, search)
    a = rows[0]
    assert a["slug_has_year"] and a["inbound_internal_links"] == 1 and a["impressions_28d"] == "12"
    assert a["similarity"] == 1.0 and a["suggested_action"] == "merge->/2026-10-02-b/"
    gsc = tmp_path / "gsc.csv"
    with gsc.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerows([["url", "impressions", "clicks"], ["https://x/a/", "5", "0"]])
    assert ca.load_search(gsc) == {"https://x/a": ("5", "0")} and ca.load_search(None) == {}
    assert ca.split_post("no front matter") == ({}, "no front matter")
