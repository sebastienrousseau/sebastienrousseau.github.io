#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Per-locale /speaking/ overlays must stay aligned with the English source.

``build_speaking._load_overlay`` merges ``_data/proof/i18n/<lang>/speaking.md``
over the English frontmatter **one top-level key at a time**. That shallow
merge is what makes progressive backfill possible — a locale with no overlay
ships English — but it also means any key an overlay *does* supply replaces
the English one wholesale. Drop a sub-key and it does not fall back: it
vanishes from the page.

The generator is deliberately forgiving here: a malformed overlay warns and
ships English rather than failing the build, because a half-finished
translation should never take the site down. That forgiveness is exactly why
this gate exists — without it, a broken overlay is a warning in a 50,000-line
build log and an English page in production.

Three classes of defect are checked:

* **Shape drift.** A supplied key whose nested shape no longer matches
  English, in either direction.
* **Frozen fields.** Four values are resolved by identity, not read as
  prose: ``stats[].kpi`` (looked up in metrics.json — a wrong id silently
  drops the stat row), ``paths.items[].cta_target`` (an in-page anchor),
  ``keynotes.talks[].new`` (a boolean flag) and ``biography.portrait`` (an
  image URL). These are compared as *ordered pairs*, not as a mapping: the
  path notation collapses list indices, so a dict comparison would wave
  through a corrupted first entry as long as the last one still matched.
* **booking_url.** Must be inherited. ``_localize_static_hrefs`` already
  rewrites ``/contact/`` to the locale's own slug, so an overlay that sets
  it defeats the localisation rather than adding to it.

Locales without an overlay are reported as backlog, not failure.

Usage:  python3 tests/validation/test_i18n_speaking.py [--strict]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

import _lang_registry  # type: ignore[import-not-found]

SOURCE = ROOT / "_data" / "proof" / "speaking.md"
OVERLAY_DIR = ROOT / "_data" / "proof" / "i18n"
FM_RE = re.compile(r"^---\n([\s\S]*?)\n---\n([\s\S]*)$")

FROZEN = {
    "stats[].kpi",
    "paths.items[].cta_target",
    "keynotes.talks[].new",
    "biography.portrait",
}


def leaves(obj: object, prefix: str = "") -> list[tuple[str, object]]:
    """Flatten to (path, value) pairs; list indices collapse to ``[]``."""
    if isinstance(obj, dict):
        out: list[tuple[str, object]] = []
        for k, v in obj.items():
            out.extend(leaves(v, f"{prefix}{k}."))
        return out
    if isinstance(obj, list):
        out = []
        for v in obj:
            out.extend(leaves(v, f"{prefix[:-1]}[]."))
        return out
    return [(prefix[:-1], obj)]


def frozen_pairs(data: dict) -> list[tuple[str, object]]:
    return [(k, v) for k, v in leaves(data) if k in FROZEN]


def _shape_problems(code: str, en: dict, overlay: dict) -> list[str]:
    """Keys the overlay supplies whose nested shape no longer matches English."""
    problems = [f"{code}/{k}: not present in the English source" for k in overlay if k not in en]
    for key, en_val in en.items():
        if key not in overlay:
            continue
        en_shape = {k for k, _ in leaves({key: en_val})}
        got_shape = {k for k, _ in leaves({key: overlay[key]})}
        problems.extend(
            f"{code}/{p}: missing from the overlay" for p in sorted(en_shape - got_shape)
        )
        problems.extend(
            f"{code}/{p}: not present in the English source" for p in sorted(got_shape - en_shape)
        )
    return problems


def _frozen_problems(code: str, en: dict, overlay: dict) -> list[str]:
    """Structural values that were translated as if they were prose."""
    en_frozen, got_frozen = frozen_pairs(en), frozen_pairs({**en, **overlay})
    if len(en_frozen) != len(got_frozen):
        return [f"{code}: frozen field count changed ({len(en_frozen)} -> {len(got_frozen)})"]
    return [
        f"{code}/{ek}: structural value changed ({ev!r} -> {gv!r})"
        for (ek, ev), (_, gv) in zip(en_frozen, got_frozen, strict=True)
        if ev != gv
    ]


def check(code: str, en: dict) -> list[str]:
    path = OVERLAY_DIR / code / "speaking.md"
    if not path.is_file():
        return []
    m = FM_RE.match(path.read_text(encoding="utf-8"))
    if not m:
        return [f"{code}: frontmatter delimiters not found"]
    try:
        overlay = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as exc:
        return [f"{code}: invalid YAML — {exc}"]
    if not isinstance(overlay, dict):
        return [f"{code}: frontmatter is not a mapping"]

    problems: list[str] = []
    if not m.group(2).strip():
        problems.append(f"{code}: empty biography body")
    if "booking_url" in overlay:
        problems.append(
            f"{code}: sets booking_url — it must be inherited so "
            "_localize_static_hrefs can point it at this locale's contact slug"
        )
    problems.extend(_shape_problems(code, en, overlay))
    problems.extend(_frozen_problems(code, en, overlay))
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="fail on locales with no overlay")
    args = ap.parse_args()

    m = FM_RE.match(SOURCE.read_text(encoding="utf-8"))
    if not m:
        print(f"{SOURCE}: frontmatter delimiters not found", file=sys.stderr)
        return 1
    en = yaml.safe_load(m.group(1)) or {}

    codes = [lg.code for lg in _lang_registry.active() if lg.code != "en"]
    problems: list[str] = []
    missing: list[str] = []
    for code in codes:
        if not (OVERLAY_DIR / code / "speaking.md").is_file():
            missing.append(code)
        problems.extend(check(code, en))

    if problems:
        print("speaking overlay defects:", file=sys.stderr)
        for line in problems[:60]:
            print(f"  - {line}", file=sys.stderr)
        if len(problems) > 60:
            print(f"  …and {len(problems) - 60} more", file=sys.stderr)
        return 1

    written = len(codes) - len(missing)
    if missing:
        print(f"  backlog: speaking: {len(missing)} locale(s) ship English — {' '.join(missing)}")
    if missing and args.strict:
        print(f"speaking: {len(missing)} locale(s) still without an overlay", file=sys.stderr)
        return 1
    print(f"ok: /speaking/ overlays valid for {written} of {len(codes)} language(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
