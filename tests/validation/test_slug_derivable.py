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

Most of the archive predates the deriver. Those slugs are readable and
correct; renaming ~2540 live URLs so a test can regenerate their exact
spelling would be the tail wagging the dog. So they are frozen as named
exceptions rather than fixed, in ``slug-derivable-frozen.json`` — the same
shape as the complexity allowlist and the mypy tier.

This replaced a per-locale *count* baseline, which had a hole: a title edited
in place could stop deriving and still pass, so long as some other post in
that locale started deriving and kept the count level. Naming the exceptions
closes that — the gate fails on any post outside the set — and makes the
backlog enumerable rather than a percentage. A frozen entry that starts
deriving must be removed, so the set can only shrink.

Posts added or renamed against the base ref are held to the deriver exactly
and cannot be frozen: new work has no archive to excuse it.

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
FROZEN = Path(__file__).with_name("slug-derivable-frozen.json")
_TITLE_RE = re.compile(r'^title:\s*"(.*?)"\s*$', re.M)


def non_derivable() -> dict[str, list[str]]:
    """Every locale post whose slug does not re-derive from its title."""
    out: dict[str, list[str]] = {}
    for directory in sorted(POSTS.iterdir()):
        if not directory.is_dir() or directory.name.startswith((".", "_")):
            continue
        stems = []
        for post in sorted(directory.glob("20*.md")):
            match = _TITLE_RE.search(post.read_text(encoding="utf-8"))
            if match is None:
                continue
            date = post.stem[:10]
            if post.stem != f"{date}-{derive_slug(match.group(1), directory.name, date[:4])}":
                stems.append(post.stem)
        if stems:
            out[directory.name] = stems
    return out


def load_frozen() -> dict[str, set[str]]:
    if not FROZEN.exists():
        return {}
    raw = json.loads(FROZEN.read_text(encoding="utf-8"))
    return {k: set(v) for k, v in raw.items() if not k.startswith("$")}


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
    current: dict[str, list[str]], frozen: dict[str, set[str]]
) -> tuple[list[str], list[str]]:
    """Returns (failures, stale). New offenders fail; healed entries are stale."""
    failures: list[str] = []
    for locale, stems in sorted(current.items()):
        allowed = frozen.get(locale, set())
        failures.extend(
            f"{locale}/{stem}.md: slug does not derive from its title and is not "
            f"a frozen exception. Rename it to match derive_slug(title, "
            f"'{locale}'), or add the missing words to "
            f"_data/i18n/romanisation-lexicon.json."
            for stem in sorted(set(stems) - allowed)
        )

    stale: list[str] = []
    for locale, stems in sorted(frozen.items()):
        healed = stems - set(current.get(locale, []))
        stale.extend(f"{locale}/{stem}.md" for stem in sorted(healed))
    return failures, stale


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--strict", action="store_true", help="allow no frozen exceptions at all")
    ap.add_argument("--update-frozen", action="store_true", help="rewrite the frozen set")
    args = ap.parse_args(argv)

    current = non_derivable()
    if args.update_frozen:
        FROZEN.write_text(
            json.dumps(
                {
                    "$comment": (
                        "Locale posts whose slug predates scripts/lib/_romanise.py and "
                        "does not re-derive from its title. Frozen, not fixed: the slugs "
                        "are correct and renaming live URLs to satisfy a test is not a "
                        "trade worth making. The gate fails on any post outside this set, "
                        "and on an entry that has started deriving — so it can only "
                        "shrink. Never add a new post here; new work is held to the "
                        "deriver exactly."
                    ),
                    **{k: sorted(v) for k, v in sorted(current.items())},
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        total = sum(len(v) for v in current.values())
        print(f"slug-derivable: froze {total} exception(s) across {len(current)} locales")
        return 0

    frozen = load_frozen()
    failures, stale = evaluate(current, frozen)

    base = _base_ref()
    if base:
        changed = changed_posts(base)
        if changed:
            print(f"  strict: {len(changed)} post(s) added or renamed since {base}")
        failures.extend(check_changed(changed))

    for line in stale:
        print(
            f"FAIL {line}: now derives from its title — remove it from "
            f"{FROZEN.name} (run --update-frozen)",
            file=sys.stderr,
        )
    for line in failures:
        print(f"FAIL {line}", file=sys.stderr)
    if failures or stale:
        return 1

    frozen_total = sum(len(v) for v in frozen.values())
    if args.strict and frozen_total:
        print(f"slug-derivable: --strict and {frozen_total} frozen exception(s)", file=sys.stderr)
        return 1
    print(
        f"slug-derivable: OK — every locale slug derives from its title, "
        f"except {frozen_total} frozen exception(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
