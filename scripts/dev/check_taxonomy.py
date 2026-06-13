#!/usr/bin/env python3
"""Validate the canonical tag taxonomy + report coverage against posts.

Walks every ``_posts/*.md`` and resolves each comma-separated
frontmatter tag through the alias table in ``_data/taxonomy.yml``.
Reports:

* Total taxonomy size (canonical tag count + alias count).
* Coverage — how many tag occurrences across all posts resolve to a
  canonical via aliases vs how many are orphan.
* Per-canonical post counts after alias collapse.
* Top orphan tags (frequency-sorted) — these are the ones to either
  add to the taxonomy as canonicals/aliases, or to clean up in post
  frontmatter.
* Landing eligibility: per the editorial-overhaul plan, only
  canonicals with **≥ 3 posts** get a ``/tags/<slug>/`` landing
  page; the rest are surfaced as anchors on the ``/tags/`` cover.

**Lenient by default.** Exits 0 even with orphans so the build pipeline
keeps moving while the editorial sweep happens. Pass ``--strict`` to
fail on any orphan — wire that into CI once frontmatter is cleaned up
(WS3 commit 10 follow-up).

Run from repo root::

    python3 scripts/dev/check_taxonomy.py            # lenient
    python3 scripts/dev/check_taxonomy.py --strict   # CI mode
"""

from __future__ import annotations

import argparse
import collections
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("error: PyYAML not installed — pip install pyyaml", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[2]
TAXONOMY = ROOT / "_data" / "taxonomy.yml"
POSTS = ROOT / "_posts"

_PILLARS = ("ai", "payments", "infra", "policy", "open-source", "leadership")
_TAG_FM_RE = re.compile(r'^tags:\s*"?([^"\n]+)"?', re.MULTILINE)
_LANDING_THRESHOLD = 3


def load_taxonomy() -> dict:
    if not TAXONOMY.is_file():
        print(f"error: {TAXONOMY} missing", file=sys.stderr)
        sys.exit(2)
    with TAXONOMY.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


_REQUIRED_FIELDS = ("name", "plural", "description", "category")


def _validate_entry(slug: str, entry: object) -> list[str]:
    if not isinstance(entry, dict):
        return [f"{slug}: entry is not a mapping"]
    problems = [
        f"{slug}: missing required field '{f}'" for f in _REQUIRED_FIELDS if f not in entry
    ]
    if entry.get("category") not in _PILLARS:
        problems.append(
            f"{slug}: category '{entry.get('category')}' not in allowed pillars {_PILLARS}"
        )
    return problems


def _check_alias_collisions(
    slug: str, entry: dict, seen_aliases: dict[str, str]
) -> list[str]:
    problems: list[str] = []
    aliases = entry.get("aliases", []) or []
    for alias in [slug, *aliases]:
        key = alias.strip().lower()
        if key in seen_aliases and seen_aliases[key] != slug:
            problems.append(
                f"{slug}: alias '{alias}' already maps to '{seen_aliases[key]}'"
            )
        seen_aliases[key] = slug
    return problems


def validate_taxonomy(taxonomy: dict) -> list[str]:
    """Structural checks on the taxonomy itself, regardless of posts."""
    problems: list[str] = []
    seen_aliases: dict[str, str] = {}
    for slug, entry in taxonomy.items():
        problems.extend(_validate_entry(slug, entry))
        if isinstance(entry, dict):
            problems.extend(_check_alias_collisions(slug, entry, seen_aliases))
    return problems


def alias_map(taxonomy: dict) -> dict[str, str]:
    out: dict[str, str] = {}
    for slug, entry in taxonomy.items():
        out[slug.strip().lower()] = slug
        for a in entry.get("aliases", []) or []:
            out[a.strip().lower()] = slug
    return out


def walk_posts(amap: dict[str, str]) -> tuple[collections.Counter[str], collections.Counter[str]]:
    resolved: collections.Counter[str] = collections.Counter()
    orphan: collections.Counter[str] = collections.Counter()
    for path in sorted(POSTS.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        m = _TAG_FM_RE.search(text)
        if not m:
            continue
        for raw in m.group(1).split(","):
            tag = raw.strip().strip('"').strip("'").strip()
            if not tag:
                continue
            canon = amap.get(tag.lower())
            if canon:
                resolved[canon] += 1
            else:
                orphan[tag] += 1
    return resolved, orphan


def _print_taxonomy_summary(taxonomy: dict) -> None:
    by_pillar: collections.Counter[str] = collections.Counter()
    for entry in taxonomy.values():
        by_pillar[entry["category"]] += 1
    alias_count = sum(len(e.get("aliases", []) or []) for e in taxonomy.values())
    print(f"Taxonomy: {len(taxonomy)} canonical tags, {alias_count} aliases")
    for pillar in _PILLARS:
        print(f"  {pillar:14s} {by_pillar.get(pillar, 0)}")
    print()


def _print_coverage(
    resolved: collections.Counter[str], orphan: collections.Counter[str]
) -> None:
    total = sum(resolved.values()) + sum(orphan.values())
    pct = (100 * sum(resolved.values()) / total) if total else 100.0
    landing = sum(1 for n in resolved.values() if n >= _LANDING_THRESHOLD)
    anchor = sum(1 for n in resolved.values() if n < _LANDING_THRESHOLD)
    print(f"Coverage: {sum(resolved.values())}/{total} tag occurrences resolve ({pct:.1f}%)")
    print(f"  {len(resolved)} canonicals hit at least once")
    print(f"  {landing} eligible for /tags/<slug>/ landing (>={_LANDING_THRESHOLD} posts)")
    print(f"  {anchor} cover-anchor only (<{_LANDING_THRESHOLD} posts)")
    print()


def _print_orphans(orphan: collections.Counter[str]) -> None:
    print(
        f"{sum(orphan.values())} orphan tag occurrences across {len(orphan)} distinct strings."
    )
    print("Top 15 orphan tags (add alias to taxonomy.yml OR fix post frontmatter):")
    for tag, n in orphan.most_common(15):
        print(f"  {n:>3}  {tag}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if any post tag fails to resolve through aliases.",
    )
    args = parser.parse_args()

    taxonomy = load_taxonomy()
    problems = validate_taxonomy(taxonomy)
    if problems:
        print("Taxonomy structural problems:")
        for p in problems:
            print(f"  - {p}")
        return 2

    resolved, orphan = walk_posts(alias_map(taxonomy))
    _print_taxonomy_summary(taxonomy)
    _print_coverage(resolved, orphan)
    if not orphan:
        print("All post tags resolve through aliases. 🎯")
        return 0
    _print_orphans(orphan)
    if args.strict:
        print("\nstrict mode: failing build on orphan tags", file=sys.stderr)
        return 1
    print("\nlenient mode: build continues. Pass --strict in CI when ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
