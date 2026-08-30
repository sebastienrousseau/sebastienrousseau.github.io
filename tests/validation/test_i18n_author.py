#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Smoke test: every author-card JSON has the same key set as English.

EN file at ``_data/i18n/en/author.json`` is the canonical reference.
Every other language under ``_data/i18n/<code>/author.json`` must
carry the same keys with that language's translations. Missing /
extra / null fails the build.

Run from repo root: ``python3 scripts/test_i18n_author.py``.
"""

from __future__ import annotations

import sys as _sys  # path bootstrap — scripts reorg (scripts/lib/ on sys.path)
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[2] / "scripts" / "lib"))

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _lang_registry  # type: ignore[import-not-found]

ROOT = Path(__file__).resolve().parents[2]
I18N_DIR = ROOT / "_data" / "i18n"


def check_language(code: str, reference_keys: set[str]) -> list[str]:
    try:
        data = _lang_registry.load_author(code)
    except _lang_registry.LanguageError as e:
        return [str(e)]
    keys = set(data)
    problems: list[str] = [
        f"[{code}] missing key: {key!r}" for key in sorted(reference_keys - keys)
    ]
    problems.extend(
        f"[{code}] extra key (not in EN reference): {key!r}"
        for key in sorted(keys - reference_keys)
    )
    problems.extend(
        f'[{code}] key {key!r} has null value (use "" if intentional)'
        for key, value in data.items()
        if value is None
    )
    return problems


def main() -> int:
    try:
        reference = _lang_registry.load_author("en")
    except _lang_registry.LanguageError as e:
        print(f"error loading EN reference: {e}", file=sys.stderr)
        return 1
    if not reference:
        print("error: EN author file is empty", file=sys.stderr)
        return 1

    reference_keys = set(reference)

    lang_dirs = sorted(
        d.name
        for d in I18N_DIR.iterdir()
        if d.is_dir() and d.name != "en" and (d / "author.json").is_file()
    )
    if not lang_dirs:
        print("warn: no non-EN author.json files found", file=sys.stderr)
        return 0

    all_problems: list[str] = []
    for code in lang_dirs:
        all_problems.extend(check_language(code, reference_keys))

    if all_problems:
        print("author parity defects:", file=sys.stderr)
        for line in all_problems[:50]:
            print(f"  - {line}", file=sys.stderr)
        return 1

    print(
        f"ok: author-card parity passes for {len(lang_dirs)} language(s) "
        f"({', '.join(lang_dirs)}); EN reference has {len(reference_keys)} keys"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
