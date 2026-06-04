#!/usr/bin/env python3
"""Smoke test: every render-data file matches the FR source on shape.

build_translations.py ingests four lang-keyed data files at module
load:

    * home_patches.json   — homepage chrome patches
    * static_bodies.json  — static-page body HTML
    * static_patches.json — static-page chrome patches
    * chrome_patches.json — inline (non-strings-derived) chrome patches

The French file is the canonical reference (extracted from the
original inline literals in build_translations.py). Every other
language file must carry:

    * the same number of entries for *_patches.json files
    * the same keys for static_bodies.json

Missing/extra entries fail the build. This is what prevents a DE
home-patches file with 76 entries (vs FR's 77) from silently leaving
one EN string unmasked on /de/.

Run from repo root: ``python3 scripts/test_i18n_render_data.py``.
Exits non-zero on any defect. Wired into ``build.sh``.
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


def check_patches(code: str, name: str, loader, fr_count: int) -> list[str]:
    try:
        entries = loader(code)
    except _lang_registry.LanguageError as e:
        return [str(e)]
    if len(entries) != fr_count:
        return [
            f"[{code}/{name}] count mismatch: {len(entries)} vs FR reference {fr_count}"
        ]
    return []


def check_bodies(code: str, fr_keys: set[str]) -> list[str]:
    try:
        bodies = _lang_registry.load_static_bodies(code)
    except _lang_registry.LanguageError as e:
        return [str(e)]
    keys = set(bodies)
    problems: list[str] = [
        f"[{code}/static_bodies] missing key: {missing!r}"
        for missing in sorted(fr_keys - keys)
    ]
    problems.extend(
        f"[{code}/static_bodies] extra key (not in FR ref): {extra!r}"
        for extra in sorted(keys - fr_keys)
    )
    return problems


def main() -> int:
    # FR is the canonical reference.
    try:
        fr_home = _lang_registry.load_home_patches("fr")
        fr_static = _lang_registry.load_static_patches("fr")
        fr_chrome = _lang_registry.load_chrome_patches_inline("fr")
        fr_bodies = _lang_registry.load_static_bodies("fr")
    except _lang_registry.LanguageError as e:
        print(f"error loading FR reference: {e}", file=sys.stderr)
        return 1

    fr_body_keys = set(fr_bodies)

    targets = sorted(
        d.name for d in I18N_DIR.iterdir()
        if d.is_dir() and d.name not in ("fr", "en")
        and (d / "home_patches.json").is_file()
    )
    if not targets:
        print("warn: no non-FR languages with home_patches.json", file=sys.stderr)
        return 0

    all_problems: list[str] = []
    for code in targets:
        all_problems.extend(check_patches(code, "home_patches", _lang_registry.load_home_patches, len(fr_home)))
        all_problems.extend(check_patches(code, "static_patches", _lang_registry.load_static_patches, len(fr_static)))
        all_problems.extend(check_patches(code, "chrome_patches", _lang_registry.load_chrome_patches_inline, len(fr_chrome)))
        all_problems.extend(check_bodies(code, fr_body_keys))

    if all_problems:
        print("render-data parity defects:", file=sys.stderr)
        for line in all_problems[:50]:
            print(f"  - {line}", file=sys.stderr)
        if len(all_problems) > 50:
            print(f"  …and {len(all_problems) - 50} more", file=sys.stderr)
        return 1

    print(
        f"ok: render-data parity passes for {len(targets)} language(s) "
        f"({', '.join(targets)}); FR has home={len(fr_home)} "
        f"static={len(fr_static)} chrome={len(fr_chrome)} "
        f"bodies={len(fr_bodies)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
