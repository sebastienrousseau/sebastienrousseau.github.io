#!/usr/bin/env python3
"""Locale slugs must be *derivable* from their translated title.

ADR-0012 says every locale localises its article slug, following the
translated title, and ``test_slug_policy.py`` enforces that no slug is left
in English. This gate enforces the other half: that the slug was **derived**
rather than typed, by recomputing it and comparing.

``scripts/lib/_romanise.py`` does the derivation. The scripts it covers vary
in how much a character table can do — Arabic and Hebrew do not write short
vowels, Thai writes no word boundaries, Japanese and Chinese need readings —
so the table is backed by ``_data/i18n/romanisation-lexicon.json``, whose
longest-match lookup supplies the missing vowels and the missing word
boundaries in one mechanism.

Ratchet, same shape as the slug-policy gate: each locale's current derivable
count is recorded as a baseline and the gate FAILS only if a locale goes
backwards. Most of the archive predates the deriver and is not reproducible
— renaming those URLs to satisfy a test would be the tail wagging the dog —
so the backlog is printed every run rather than silently tolerated, and new
work is expected to be derivable. ``--strict`` requires every slug to derive.

Usage:  python3 tests/validation/test_slug_derivable.py [--strict]
        python3 tests/validation/test_slug_derivable.py --update-baseline
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from lib._romanise import derive_slug

POSTS = ROOT / "_posts"
BASELINE = Path(__file__).with_name("slug-derivable-baseline.json")
_TITLE_RE = re.compile(r'^title:\s*"(.*?)"\s*$', re.M)


def locale_report() -> dict[str, dict[str, int]]:
    """Per locale: dated posts, and how many slugs re-derive from the title."""
    out: dict[str, dict[str, int]] = {}
    for d in sorted(POSTS.iterdir()):
        if not d.is_dir() or d.name.startswith((".", "_")):
            continue
        total = derivable = 0
        for p in sorted(d.glob("20*.md")):
            m = _TITLE_RE.search(p.read_text(encoding="utf-8"))
            if m is None:
                continue
            total += 1
            date = p.stem[:10]
            if p.stem == f"{date}-{derive_slug(m.group(1), d.name, date[:4])}":
                derivable += 1
        if total:
            out[d.name] = {"total": total, "derivable": derivable}
    return out


def _base_ref() -> str | None:
    """The ref this branch is measured against, if one is resolvable."""
    candidates = []
    if os.environ.get("GITHUB_BASE_REF"):
        candidates.append(f"origin/{os.environ['GITHUB_BASE_REF']}")
    candidates += ["origin/main", "main"]
    for ref in candidates:
        proc = subprocess.run(
            ["git", "rev-parse", "--verify", "--quiet", ref],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode == 0:
            return ref
    return None


def changed_posts(base: str) -> list[Path]:
    """Posts added or renamed since ``base``.

    The ratchet compares a per-locale *count*, so a new post with a
    hand-typed slug slips through as long as some other post becomes
    derivable — verified by seeding exactly that and watching the ratchet
    pass. New work has no archive to excuse it, so it is held to the
    deriver exactly.
    """
    proc = subprocess.run(
        ["git", "diff", "--name-status", "--diff-filter=AR", f"{base}...HEAD", "--", "_posts"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return []
    paths = []
    for line in proc.stdout.splitlines():
        path = line.split("\t")[-1]  # for a rename this is the destination
        if path.endswith(".md"):
            paths.append(ROOT / path)
    return [p for p in paths if p.is_file()]


def check_changed(paths: list[Path]) -> list[str]:
    """Every added or renamed locale post must re-derive from its title."""
    problems = []
    for post in paths:
        parts = post.relative_to(ROOT).parts
        if len(parts) < 3:
            continue  # EN posts live at _posts/*.md and are not localised
        locale = parts[1]
        match = _TITLE_RE.search(post.read_text(encoding="utf-8"))
        if match is None:
            continue
        date = post.stem[:10]
        want = f"{date}-{derive_slug(match.group(1), locale, date[:4])}"
        if post.stem != want:
            problems.append(
                f"{post.relative_to(ROOT)}: slug is not derivable — expected {want!r}. "
                f"Rename it, or add the missing words to "
                f"_data/i18n/romanisation-lexicon.json."
            )
    return problems


def evaluate(
    report: dict[str, dict[str, int]], baseline: dict[str, int]
) -> tuple[list[str], list[str]]:
    """Returns (failures, backlog). A failure is a locale that regressed."""
    failures: list[str] = []
    backlog: list[str] = []
    for lang, counts in sorted(report.items()):
        total, derivable = counts["total"], counts["derivable"]
        prior = baseline.get(lang)
        if prior is not None and derivable < prior:
            failures.append(
                f"{lang}: slug derivation went backwards — {derivable} derivable now "
                f"vs {prior} at baseline. Rename the post to match "
                f"derive_slug(title, '{lang}'), or add the missing words to "
                f"_data/i18n/romanisation-lexicon.json."
            )
        elif derivable < total:
            pct = round(100 * derivable / total)
            backlog.append(f"{lang}: {derivable}/{total} ({pct}%) derive from the title")
    return failures, backlog


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--strict", action="store_true", help="every slug must derive")
    ap.add_argument("--update-baseline", action="store_true", help="rewrite the baseline")
    args = ap.parse_args(argv)

    report = locale_report()
    if args.update_baseline:
        BASELINE.write_text(
            json.dumps(
                {lang: c["derivable"] for lang, c in sorted(report.items())},
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"slug-derivable: baseline written for {len(report)} locales")
        return 0

    baseline = json.loads(BASELINE.read_text(encoding="utf-8")) if BASELINE.exists() else {}
    failures, backlog = evaluate(report, baseline)

    # New work is held to the deriver exactly; the archive stays on the ratchet.
    base = _base_ref()
    if base:
        changed = changed_posts(base)
        if changed:
            print(f"  strict: {len(changed)} post(s) added or renamed since {base}")
        failures.extend(check_changed(changed))

    for line in backlog:
        print(f"  backlog: {line}")
    if failures:
        for line in failures:
            print(f"FAIL {line}", file=sys.stderr)
        return 1
    if args.strict and backlog:
        print("slug-derivable: --strict and the backlog is non-empty", file=sys.stderr)
        return 1

    total = sum(c["total"] for c in report.values())
    derivable = sum(c["derivable"] for c in report.values())
    print(
        f"slug-derivable: OK — no locale regressed "
        f"({derivable}/{total} slugs re-derive from their title)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
