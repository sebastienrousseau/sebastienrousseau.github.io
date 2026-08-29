#!/usr/bin/env python3
"""A localised page must not serve an English <title>.

Every locale page is self-canonical and declares its own ``lang`` — ``ms``
pages say ``lang="ms-MY"``, ``zh-hans`` pages say ``lang="zh-hans"``. 2154 of
the 7004 non-EN pages nonetheless serve a ``<title>`` byte-identical to an
English page's, from 64 distinct strings repeated across all 34 locales: the
locale home, the article listing and its pagination, and the tag landings,
whose title is built as ``f"{name} — Articles by topic"`` in
scripts/generators/tag_landing_render.py.

It matters more than a cosmetic slip. The title is the strongest on-page
signal a search engine has, and a page promising ``lang="ms-MY"`` while
titling itself in English is both a duplicate-title cluster (35 locales
sharing one string) and a language mismatch.

test_lang_no_leakage.py does not see this: it compares chrome *content*
against the EN UI-string glossary, and these titles are page titles rather
than glossary strings.

Closing the backlog is a translation job of roughly 64 strings per locale,
not a code change, so this gate does what the slug-derivable gate does:
enumerates the current offenders in ``localised-titles-frozen.json`` and
fails on anything new. The set can only shrink — a page that gets a
translated title must be removed from it.

Usage:  python3 tests/validation/test_localised_titles.py [--strict]
        python3 tests/validation/test_localised_titles.py --update-frozen
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

import _lang_registry  # type: ignore[import-not-found]

PUBLIC = ROOT / "public"
FROZEN = Path(__file__).with_name("localised-titles-frozen.json")
_TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S)
_REFRESH = 'http-equiv="refresh"'


def _locales() -> set[str]:
    return {lang.code for lang in _lang_registry.LANGUAGES if lang.code != "en"}


def scan() -> tuple[set[str], dict[str, str]]:
    """Returns (English titles, {locale page path: its English title})."""
    locales = _locales()
    english: set[str] = set()
    localised: list[tuple[str, str, str]] = []
    for page in sorted(PUBLIC.rglob("index.html")):
        rel = page.relative_to(PUBLIC)
        html = page.read_text(encoding="utf-8", errors="ignore")
        if _REFRESH in html:
            continue  # redirect stubs copy their target's title by design
        match = _TITLE_RE.search(html)
        if match is None:
            continue
        title = match.group(1).strip()
        locale = rel.parts[0] if len(rel.parts) > 1 and rel.parts[0] in locales else "en"
        if locale == "en":
            english.add(title)
        else:
            localised.append((str(rel), locale, title))
    offenders = {path: title for path, _loc, title in localised if title in english}
    return english, offenders


def load_frozen() -> set[str]:
    if not FROZEN.exists():
        return set()
    raw = json.loads(FROZEN.read_text(encoding="utf-8"))
    return set(raw.get("pages", []))


def evaluate(offenders: dict[str, str], frozen: set[str]) -> tuple[list[str], list[str]]:
    """Returns (failures, stale). New offenders fail; healed entries are stale."""
    failures = [
        f"{path}: <title> is the English {title!r}"
        for path, title in sorted(offenders.items())
        if path not in frozen
    ]
    stale = sorted(frozen - set(offenders))
    return failures, stale


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--strict", action="store_true", help="allow no frozen pages at all")
    ap.add_argument("--update-frozen", action="store_true", help="rewrite the frozen set")
    args = ap.parse_args(argv)

    if not PUBLIC.is_dir():
        print("localised-titles: no public/ — run after a build", file=sys.stderr)
        return 0

    _english, offenders = scan()
    if args.update_frozen:
        FROZEN.write_text(
            json.dumps(
                {
                    "$comment": (
                        "Locale pages still serving an English <title>. Frozen so the "
                        "backlog is enumerable and cannot grow; closing it is a "
                        "translation job, not a code change. A page that gets a "
                        "translated title must be removed from this list — the gate "
                        "fails on a stale entry, so the set can only shrink."
                    ),
                    "pages": sorted(offenders),
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"localised-titles: froze {len(offenders)} page(s)")
        return 0

    frozen = load_frozen()
    failures, stale = evaluate(offenders, frozen)

    for path in stale:
        print(
            f"FAIL {path}: now has a localised title — remove it from {FROZEN.name} "
            f"(run --update-frozen)",
            file=sys.stderr,
        )
    for line in failures:
        print(f"FAIL {line}", file=sys.stderr)
    if failures or stale:
        return 1
    if args.strict and frozen:
        print(f"localised-titles: --strict and {len(frozen)} frozen page(s)", file=sys.stderr)
        return 1
    print(f"ok: no new page serves an English <title> ({len(frozen)} frozen, awaiting translation)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
