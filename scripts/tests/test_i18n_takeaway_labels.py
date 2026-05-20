#!/usr/bin/env python3
"""Smoke test: every takeaway-labels JSON has the same key set as EN.

The English file at ``_data/i18n/en/takeaway_labels.json`` is the
canonical reference. Every other language under
``_data/i18n/<code>/takeaway_labels.json`` must carry the exact same
key set with that language's translations. Missing key → build fails.
Extra key → build fails.

Distinct from :mod:`scripts.test_i18n_strings` (global UI chrome) and
:mod:`scripts.test_i18n_labels` (inline article body labels);
``takeaway_labels.json`` covers the section labels in the "Key
takeaways" aside (Idea / Impact / Insight / …).

Run from repo root: ``python3 scripts/test_i18n_takeaway_labels.py``.
Exits non-zero on any defect. Wired into ``build.sh`` so shape can't
drift silently between languages.
"""
from __future__ import annotations

import sys as _sys  # path bootstrap — scripts reorg (scripts/lib/ on sys.path)
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "lib"))

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _lang_registry  # type: ignore[import-not-found]

ROOT = Path(__file__).resolve().parents[2]
I18N_DIR = ROOT / "_data" / "i18n"


def check_language(code: str, reference_keys: set[str]) -> list[str]:
    problems: list[str] = []
    try:
        labels = _lang_registry.load_takeaway_labels(code)
    except _lang_registry.LanguageError as e:
        return [str(e)]

    keys = set(labels)
    missing = reference_keys - keys
    extra = keys - reference_keys

    problems.extend(
        f"[{code}] missing key: {key!r}" for key in sorted(missing)
    )
    problems.extend(
        f"[{code}] extra key (not in EN reference): {key!r}"
        for key in sorted(extra)
    )
    problems.extend(
        f"[{code}] key {key!r} has null value (use \"\" if intentional)"
        for key, value in labels.items()
        if value is None
    )
    return problems


def main() -> int:
    try:
        reference = _lang_registry.load_takeaway_labels("en")
    except _lang_registry.LanguageError as e:
        print(f"error loading EN reference: {e}", file=sys.stderr)
        return 1
    if not reference:
        print("error: EN takeaway-labels file is empty", file=sys.stderr)
        return 1

    reference_keys = set(reference)

    lang_dirs = sorted(
        d.name for d in I18N_DIR.iterdir()
        if d.is_dir() and d.name != "en"
        and (d / "takeaway_labels.json").is_file()
    )
    if not lang_dirs:
        print("warn: no non-EN takeaway_labels.json files found", file=sys.stderr)
        return 0

    all_problems: list[str] = []
    for code in lang_dirs:
        all_problems.extend(check_language(code, reference_keys))

    if all_problems:
        print("takeaway-labels parity defects:", file=sys.stderr)
        for line in all_problems[:50]:
            print(f"  - {line}", file=sys.stderr)
        if len(all_problems) > 50:
            print(f"  …and {len(all_problems) - 50} more", file=sys.stderr)
        return 1

    print(
        f"ok: takeaway-labels parity passes for {len(lang_dirs)} language(s) "
        f"({', '.join(lang_dirs)}); EN reference has {len(reference_keys)} keys"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
