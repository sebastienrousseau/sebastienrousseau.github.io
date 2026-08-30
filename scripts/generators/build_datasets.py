#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Publish the index and scorecard articles as machine-readable datasets.

Eleven articles are named as an Index or a Scorecard and carry the scoring
framework that earns the name — layers, readiness metrics, weights. All of it
lived in HTML tables only, so the thing that makes the article citable was
invisible to anything that does not read prose. The pages already emit
BlogPosting, TechArticle, FAQPage and BreadcrumbList; what was missing was
``Dataset``, the type Google Dataset Search indexes and the one an answer
engine can attribute.

Each article names its own index table in frontmatter (``dataset_table``)
rather than the table being inferred. Inference would have taken the first
table everywhere, which is a Signal table in
``2026-07-01-agentic-ai-index-banks-measuring-autonomy-2026`` (the real one is
table 8) and would have invented a dataset for the 2026-06-27 article, which
has no index table at all.

Writes, for each declared article:
  public/data/<slug>.json  — rows as objects, plus the index metadata
  public/data/<slug>.csv   — the same rows, flat
  _data/datasets.json      — manifest the postbuild Dataset pass reads

The frameworks are qualitative, so the rows become ``variableMeasured``
(what the index measures) rather than a ranked ItemList: representing a
measurement framework as a leaderboard would be a claim the article does not
make.

Run from repo root: ``python3 scripts/generators/build_datasets.py``.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POSTS = ROOT / "_posts"
OUT_DIR = ROOT / "public" / "data"
MANIFEST = ROOT / "_data" / "datasets.json"
SITE = "https://sebastienrousseau.com"

_FM = re.compile(r'^(\w[\w-]*):\s*"(.*?)"\s*$', re.M)
_TABLE = re.compile(r"((?:^\|.*\|\s*$\n)+)", re.M)
_LINK = re.compile(r"\[([^\]]+)\]\([^)]*\)")
_TAGS = re.compile(r"<[^>]+>")


def _clean(cell: str) -> str:
    """Markdown cell to plain text: links to their label, no emphasis."""
    text = _LINK.sub(r"\1", cell)
    text = _TAGS.sub("", text)
    text = text.replace("**", "").replace("`", "").replace("⧉", "")
    return " ".join(text.split())


def _tables(body: str) -> list[list[list[str]]]:
    """Every pipe table in the body, as a list of rows of cells."""
    out = []
    for block in _TABLE.findall(body):
        rows = [r.strip() for r in block.strip().splitlines()]
        cells = [[_clean(c) for c in r.strip("|").split("|")] for r in rows]
        if len(cells) >= 3 and all(set(c) <= set("-: ") for c in cells[1]):
            out.append([cells[0], *cells[2:]])
    return out


def _frontmatter(text: str) -> dict[str, str]:
    head = text.split("---", 2)[1]
    return dict(_FM.findall(head))


def build() -> list[dict]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = []
    for post in sorted(POSTS.glob("20*.md")):
        text = post.read_text(encoding="utf-8")
        fm = _frontmatter(text)
        if "dataset_table" not in fm:
            continue
        wanted = int(fm["dataset_table"])
        tables = _tables(text.split("---", 2)[2])
        if wanted > len(tables):
            print(
                f"error: {post.name} declares table {wanted}, found {len(tables)}",
                file=sys.stderr,
            )
            return []
        header, *rows = tables[wanted - 1]
        records = [dict(zip(header, row, strict=False)) for row in rows]

        (OUT_DIR / f"{post.stem}.json").write_text(
            json.dumps(
                {
                    "name": fm.get("title", post.stem),
                    "description": fm.get("description", ""),
                    "url": f"{SITE}/{post.stem}",
                    "measures": header[0],
                    "records": records,
                },
                indent=2,
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        with (OUT_DIR / f"{post.stem}.csv").open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=header)
            writer.writeheader()
            writer.writerows(records)

        manifest.append(
            {
                "slug": post.stem,
                "name": fm.get("title", post.stem),
                "description": fm.get("description", ""),
                "keywords": fm.get("keywords", ""),
                "date": fm.get("date", ""),
                "measures": header[0],
                "variables": [
                    {
                        "name": row[0],
                        "description": "; ".join(
                            f"{h}: {v}" for h, v in zip(header[1:], row[1:], strict=False) if v
                        ),
                    }
                    for row in rows
                    if row and row[0]
                ],
            }
        )

    MANIFEST.write_text(
        json.dumps({"$comment": __doc__.splitlines()[0], "datasets": manifest}, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> int:
    manifest = build()
    if not manifest:
        print("build_datasets: no datasets declared", file=sys.stderr)
        return 1
    rows = sum(len(d["variables"]) for d in manifest)
    print(f"build_datasets: {len(manifest)} dataset(s), {rows} measured variable(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
