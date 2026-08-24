#!/usr/bin/env python3
"""Gate: every active language ships a complete listing-body catalogue.

``build_listings`` forks the English shell and calls
``_translate_chrome_for``, which by its own docstring leaves "body
content (which we emit ourselves)" alone. Nothing else translated it, so
every locale's paged article listing shipped FEED / Page N of M /
N visible / Category / Year / All categories / All years and the six
pillar names in English — the body-translation gate scored /articles/ at
1.000 across all 34 locales.

This checks ``_data/i18n/<code>/listings.json`` against the English
reference in ``scripts/lib/_listing_copy.py``: same keys, placeholders
preserved, values safe to splice into HTML, and prose actually
translated. "Open source" and "FEED" are exempt from the last check —
both are borrowed verbatim in many languages.

Run from repo root: ``python3 tests/validation/test_i18n_listings.py``.
"""

from __future__ import annotations

import sys as _sys
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[2] / "scripts" / "lib"))

import sys

import _lang_registry  # type: ignore[import-not-found]
import _listing_copy  # type: ignore[import-not-found]

# Terms many languages keep verbatim; identical-to-English is a choice,
# not a gap. "FEED" is a borrowed word in most of the Latin-script
# locales, and "Pagination" is simply the French, German and Dutch word —
# it is also an aria-label, never shown.
_TRANSLATION_OPTIONAL = frozenset({"eyebrow", "paginationAria"})
_PILLARS_OPTIONAL = frozenset({"open-source"})


def _shape_problems(code: str, cat: dict, ref: dict) -> list[str]:
    """Key-set checks against the English reference."""
    problems = [
        f"[{code}/listings] missing section: {section!r}"
        for section in ("ui", "pillars")
        if section not in cat
    ]
    if problems:
        return problems
    for section in ("ui", "pillars"):
        want, got = set(ref[section]), set(cat[section])
        problems.extend(
            f"[{code}/listings] {section}: missing key {k!r}" for k in sorted(want - got)
        )
        problems.extend(f"[{code}/listings] {section}: extra key {k!r}" for k in sorted(got - want))
    return problems


def _value_problems(code: str, cat: dict) -> list[str]:
    """Placeholders preserved, values non-empty and HTML-safe."""
    problems = [
        f"[{code}/listings] ui.{key}: lost the {token} placeholder"
        for key, placeholders in _listing_copy.REQUIRED_PLACEHOLDERS.items()
        for token in placeholders
        if token not in cat["ui"][key]
    ]
    for section in ("ui", "pillars"):
        for key, value in cat[section].items():
            if not isinstance(value, str) or not value.strip():
                problems.append(f"[{code}/listings] {section}.{key}: empty")
            elif "<" in value or '"' in value:
                problems.append(f'[{code}/listings] {section}.{key}: raw < or " breaks the markup')
    return problems


def _untranslated(code: str, cat: dict, ref: dict) -> list[str]:
    """Values left byte-identical to the English source."""
    out = [
        f"[{code}/listings] untranslated: ui.{k}"
        for k, v in ref["ui"].items()
        if k not in _TRANSLATION_OPTIONAL and cat["ui"].get(k) == v
    ]
    out.extend(
        f"[{code}/listings] untranslated: pillars.{k}"
        for k, v in ref["pillars"].items()
        if k not in _PILLARS_OPTIONAL and cat["pillars"].get(k) == v
    )
    return out


def check(code: str, ref: dict) -> list[str]:
    try:
        cat = _lang_registry.load_listings(code)
    except _lang_registry.LanguageError as e:
        return [str(e)]
    # Shape first: the later passes index into the catalogue.
    problems = _shape_problems(code, cat, ref)
    if problems:
        return problems
    return _value_problems(code, cat) + _untranslated(code, cat, ref)


# Pages another generator owns. Declaring one here makes
# build_translations fork the English page over the top of the generator's
# localised output — /articles/ shipped English on the 22 locales that
# listed it, because build_translations runs after build_listings.
_GENERATOR_OWNED = ("articles",)


def check_no_static_page_conflict(code: str) -> list[str]:
    """A generator-owned page must not also be a static-page mirror."""
    try:
        pages = _lang_registry.load_static_pages(code)
    except _lang_registry.LanguageError as e:
        return [str(e)]
    return [
        f"[{code}/static_pages] {slug!r} is owned by its own generator — "
        f"listing it here makes build_translations overwrite the localised page"
        for slug in _GENERATOR_OWNED
        if slug in pages
    ]


def main() -> int:
    ref = _lang_registry.listings_reference()
    codes = [lg.code for lg in _lang_registry.active() if lg.code != "en"]
    problems: list[str] = []
    for code in codes:
        problems.extend(check(code, ref))
        problems.extend(check_no_static_page_conflict(code))
    if problems:
        print("listings catalogue defects:", file=sys.stderr)
        for line in problems[:60]:
            print(f"  - {line}", file=sys.stderr)
        if len(problems) > 60:
            print(f"  …and {len(problems) - 60} more", file=sys.stderr)
        return 1
    print(
        f"ok: listing-body catalogue complete for {len(codes)} language(s) "
        f"({len(ref['ui'])} UI strings, {len(ref['pillars'])} pillars each)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
