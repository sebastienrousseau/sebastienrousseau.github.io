#!/usr/bin/env python3
"""Locale slug-policy conformance — ADR-0012.

Every locale localises the article slug, following its translated title. There
is no script-based carve-out: `ja`, `ko`, `zh-*`, `th`, `hi`, `ru` and `uk`
already localise roughly 43 % of theirs, so a "non-Latin keeps English" rule
would declare live URLs violations to fit a table.

Slugs were localised inconsistently and nothing recorded why — 14 locales at
100 % English, most of the rest near half, `fr` at 33 %. The ratchet below made
that gap measurable and stopped it widening while it was worked through.

The backlog is now closed: all 34 locales are at 0 % English slugs, the
baseline records 0 for every locale, and `build.sh` runs this gate with
`--strict`, so a single English slug fails the build rather than being
absorbed as backlog. The ratchet remains — each locale's rate is recorded as a
baseline and the gate FAILS if a locale goes backwards — but with a zero
baseline and `--strict` the two conditions coincide.

The last 71 files were English-slugged because their `title:` frontmatter had
never been translated (bodies and `seo_title` had been), so there was no
localised title for the slug to follow. Fixing the titles is what made the
slugs derivable.

Usage:  python3 tests/validation/test_slug_policy.py [--strict]
        python3 tests/validation/test_slug_policy.py --update-baseline
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POSTS = ROOT / "_posts"
BASELINE = Path(__file__).with_name("slug-policy-baseline.json")


def english_stems() -> set[str]:
    return {p.stem for p in POSTS.glob("20*.md")}


def locale_report() -> dict[str, dict[str, int]]:
    """Per locale: total dated posts and how many keep the English slug."""
    en = english_stems()
    out: dict[str, dict[str, int]] = {}
    for d in sorted(POSTS.iterdir()):
        if not d.is_dir() or d.name.startswith((".", "_")):
            continue
        stems = {p.stem for p in d.glob("20*.md")}
        if not stems:
            continue
        out[d.name] = {"total": len(stems), "english": len(stems & en)}
    return out


def evaluate(
    report: dict[str, dict[str, int]], baseline: dict[str, int]
) -> tuple[list[str], list[str]]:
    """Returns (failures, backlog). A failure is a locale that regressed."""
    failures: list[str] = []
    backlog: list[str] = []
    for lang, counts in sorted(report.items()):
        total, english = counts["total"], counts["english"]
        pct_english = round(100 * english / total)
        prior = baseline.get(lang)
        if prior is not None and pct_english > prior:
            failures.append(
                f"{lang}: slug localisation went backwards — "
                f"{pct_english}% English now vs {prior}% at baseline (ADR-0012)"
            )
        elif pct_english > 0:
            backlog.append(f"{lang}: {english}/{total} ({pct_english}%) still use the English slug")
    return failures, backlog


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--strict", action="store_true", help="treat backlog warnings as failures")
    ap.add_argument("--update-baseline", action="store_true", help="rewrite the recorded baseline")
    args = ap.parse_args(argv)

    report = locale_report()
    if args.update_baseline:
        data = {lang: round(100 * c["english"] / c["total"]) for lang, c in report.items()}
        BASELINE.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"slug-policy: baseline written for {len(data)} locales")
        return 0

    baseline = json.loads(BASELINE.read_text(encoding="utf-8")) if BASELINE.is_file() else {}
    failures, backlog = evaluate(report, baseline)

    for item in backlog:
        print(f"  backlog: {item}")
    for f in failures:
        print(f"  ::error::{f}", file=sys.stderr)

    if failures or (args.strict and backlog):
        print(
            f"slug-policy: {len(failures)} regression(s), {len(backlog)} backlog item(s)",
            file=sys.stderr,
        )
        return 1
    print(
        f"slug-policy: OK — no locale regressed against ADR-0012 "
        f"({len(backlog)} of {len(report)} locales still have English slugs to localise)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
