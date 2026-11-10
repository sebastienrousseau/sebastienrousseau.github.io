#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Write the content-audit sheet: one row per English article (plan B-3).

Columns: url, title, date, last_reviewed, words, pillar, slug_has_year,
inbound_internal_links, nearest_duplicate, similarity, impressions_28d,
clicks_28d, suggested_action.

* ``pillar`` is the most common ``taxonomy.yml`` category among the
  article's resolved tags, or ``none``.
* ``inbound_internal_links`` counts English pages in ``public/`` that link
  to the article (run after ``./build.sh``).
* ``nearest_duplicate`` / ``similarity``: the closest other article by
  Jaccard similarity of 5-word shingles of the body text.
* ``impressions_28d`` / ``clicks_28d`` come from ``--search-csv`` (a
  ``url,impressions,clicks`` export) when given, otherwise blank.

``suggested_action`` is a starting point for a human decision, recorded in
``_data/seo/content-decisions.yml``: keep, refresh, merge-><url>, noindex or
review. Nothing is applied from this sheet directly.

    content_audit.py --out reports/content-audit.csv [--search-csv gsc.csv]
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import re
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
BASE = "https://sebastienrousseau.com"
_DATED_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-")
_YEAR_SLUG_RE = re.compile(r"-20\d\d$")
_TAG_RE = re.compile(r"<[^>]+>")
COLUMNS = (
    "url", "title", "date", "last_reviewed", "words", "pillar", "slug_has_year",
    "inbound_internal_links", "nearest_duplicate", "similarity",
    "impressions_28d", "clicks_28d", "suggested_action",
)  # fmt: skip


def split_post(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---"):
        return {}, text
    _, fm, body = text.split("---", 2)
    return yaml.safe_load(fm) or {}, body


def words_of(body: str) -> list[str]:
    return re.findall(r"[a-z0-9']+", _TAG_RE.sub(" ", body).lower())


def shingles(words: list[str], n: int = 5) -> frozenset[str]:
    return frozenset(" ".join(words[i : i + n]) for i in range(max(len(words) - n + 1, 0)))


def jaccard(a: frozenset[str], b: frozenset[str]) -> float:
    return len(a & b) / len(a | b) if a and b else 0.0


def tag_index(taxonomy: dict[str, Any]) -> dict[str, str]:
    """Lower-case tag name or alias -> category."""
    out: dict[str, str] = {}
    for slug, entry in taxonomy.items():
        if not isinstance(entry, dict) or not entry.get("category"):
            continue
        for name in [slug, entry.get("name", ""), *entry.get("aliases", [])]:
            out[str(name).strip().lower()] = entry["category"]
    return out


def pillar_of(tags: str | list[str], index: dict[str, str]) -> str:
    names = tags.split(",") if isinstance(tags, str) else tags
    cats = Counter(index[n.strip().lower()] for n in names if n.strip().lower() in index)
    return cats.most_common(1)[0][0] if cats else "none"


def inbound_links(public: Path, slugs: list[str]) -> Counter[str]:
    """How many English pages link to each slug (locale trees excluded)."""
    counts: Counter[str] = Counter()
    wanted = set(slugs)
    link_re = re.compile(r'href="(?:https://sebastienrousseau\.com)?/(\d{4}-\d{2}-\d{2}-[^/"#?]+)')
    for page in public.glob("*/index.html"):
        found = set(link_re.findall(page.read_text(encoding="utf-8", errors="ignore"))) & wanted
        counts.update(s for s in found if s != page.parent.name)
    return counts


def _merge_candidate(row: dict[str, Any]) -> bool:
    return row["similarity"] >= 0.35 and row["nearest_pillar"] == row["pillar"]


def _thin_and_unseen(row: dict[str, Any]) -> bool:
    return row["pillar"] == "none" and row["words"] < 600 and row["impressions_28d"] in ("0", 0)


def suggest(row: dict[str, Any], today: dt.date) -> str:
    """keep | refresh | merge-><url> | noindex | review, by the plan's rules."""
    if _merge_candidate(row):
        return f"merge->{row['nearest_duplicate']}"
    if _thin_and_unseen(row):
        return "noindex"
    if row["pillar"] == "none":
        return "review"
    if (today - row["date"]).days > 182:
        return "refresh"
    seen = row["impressions_28d"] == "" or int(row["impressions_28d"]) > 0
    return "keep" if seen else "review"


def load_search(path: Path | None) -> dict[str, tuple[str, str]]:
    if not path:
        return {}
    with path.open(encoding="utf-8", newline="") as fh:
        return {
            r["url"].rstrip("/"): (r.get("impressions", ""), r.get("clicks", ""))
            for r in csv.DictReader(fh)
        }


def _article(path: Path, index: dict[str, str]) -> dict[str, Any]:
    fm, body = split_post(path.read_text(encoding="utf-8"))
    words = words_of(body)
    return {
        "slug": path.stem,
        "title": fm.get("title", ""),
        "date": dt.date.fromisoformat(path.stem[:10]),
        "last_reviewed": fm.get("last_reviewed", ""),
        "words": len(words),
        "pillar": pillar_of(fm.get("tags", ""), index),
        "shingles": shingles(words),
    }


def _nearest(
    a: dict[str, Any], others: list[dict[str, Any]]
) -> tuple[dict[str, Any] | None, float]:
    best, score = None, 0.0
    for b in others:
        if b is not a and (s := jaccard(a["shingles"], b["shingles"])) > score:
            best, score = b, s
    return best, score


def audit(root: Path, today: dt.date, search: dict[str, tuple[str, str]]) -> list[dict[str, Any]]:
    index = tag_index(yaml.safe_load((root / "_data" / "taxonomy.yml").read_text(encoding="utf-8")))
    arts = [
        _article(p, index)
        for p in sorted((root / "_posts").glob("*.md"))
        if _DATED_RE.match(p.name)
    ]
    inbound = inbound_links(root / "public", [a["slug"] for a in arts])
    rows = []
    for a in arts:
        near, score = _nearest(a, arts)
        url = f"{BASE}/{a['slug']}/"
        imp, clk = search.get(url.rstrip("/"), ("", ""))
        row = {
            **{k: a[k] for k in ("title", "date", "last_reviewed", "words", "pillar")},
            "url": url,
            "slug_has_year": bool(_YEAR_SLUG_RE.search(a["slug"])),
            "inbound_internal_links": inbound[a["slug"]],
            "nearest_duplicate": f"/{near['slug']}/" if near else "",
            "nearest_pillar": near["pillar"] if near else "",
            "similarity": round(score, 3),
            "impressions_28d": imp,
            "clicks_28d": clk,
        }
        row["suggested_action"] = suggest(row, today)
        rows.append(row)
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=ROOT / "reports" / "content-audit.csv")
    parser.add_argument("--search-csv", type=Path)
    args = parser.parse_args(argv)
    rows = audit(ROOT, dt.date.today(), load_search(args.search_csv))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    actions = Counter(r["suggested_action"].split("->")[0] for r in rows)
    print(f"content_audit: {len(rows)} articles -> {args.out} ({dict(actions)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
