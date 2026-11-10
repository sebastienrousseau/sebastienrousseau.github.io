#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Report the target queries from a Search Console export (plan G-9).

Reads ``_data/seo/target-queries.yml`` and a Search Console "Queries" CSV
export (columns ``Top queries`` or ``query``, ``Clicks``, ``Impressions``,
``Position``) and prints a markdown table per hub: clicks, impressions and
average position, or "not ranking" when the query is absent. Feeds the
weekly report once the Search Console secret exists (A-4); runs on a saved
export until then.

    target_queries.py --export Queries.csv [--out reports/target-queries.md]
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
TARGETS = ROOT / "_data" / "seo" / "target-queries.yml"


def load_export(path: Path) -> dict[str, tuple[str, str, str]]:
    """Lower-case query -> (clicks, impressions, position)."""
    out = {}
    with path.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            query = (row.get("Top queries") or row.get("query") or "").strip().lower()
            if query:
                out[query] = (
                    row.get("Clicks", ""),
                    row.get("Impressions", ""),
                    row.get("Position", ""),
                )
    return out


def render(targets: dict[str, list[str]], data: dict[str, tuple[str, str, str]]) -> str:
    lines = ["# Target queries", ""]
    for hub, queries in targets.items():
        lines += [
            f"## {hub}",
            "",
            "| Query | Clicks | Impressions | Position |",
            "| --- | --- | --- | --- |",
        ]
        for q in queries:
            clicks, imps, pos = data.get(q.lower(), ("", "", ""))
            lines.append(f"| {q} | {clicks or 0} | {imps or 0} | {pos or 'not ranking'} |")
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--export", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    targets = yaml.safe_load(TARGETS.read_text(encoding="utf-8"))
    text = render(targets, load_export(args.export))
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
