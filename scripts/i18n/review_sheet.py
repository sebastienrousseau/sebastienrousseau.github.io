#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Export machine-drafted translations to a review sheet, and import them back.

Plan A-3. The tag descriptions, the author card and the home, static and
chrome patches of each locale were drafted by machine. A native reviewer
works through one CSV per locale:

    review_sheet.py export --lang de --out review/de.csv
    review_sheet.py import review/de.csv

Columns: ``file, key, english, draft, approved_text, reviewer, notes``.
Export lists every string not yet reviewed. Import writes each row that has
``approved_text`` back to its file and marks it reviewed (``reviewer``,
``reviewed_on``); it refuses a row whose ``english`` no longer matches the
current source, so a reviewer re-checks text that changed after export.

Review state: tags carry ``reviewed`` / ``reviewer`` / ``reviewed_on`` in
``tags.json``; patches and author fields are tracked in
``_data/i18n/<lang>/review.json`` (``{"<file>::<key>": {...}}``), which
also records ``drafted_on``, the date a string was first exported, read by
``tests/validation/test_i18n_review_state.py``.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import sys
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
I18N = ROOT / "_data" / "i18n"
PATCH_FILES = ("home_patches.json", "static_patches.json", "chrome_patches.json")
COLUMNS = ("file", "key", "english", "draft", "approved_text", "reviewer", "notes")
Row = dict[str, str]


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _save(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def patch_key(pattern: str) -> str:
    """A stable key for a patch: the first 12 hex of its pattern's SHA-256."""
    return hashlib.sha256(pattern.encode("utf-8")).hexdigest()[:12]


def taxonomy_tags(root: Path = ROOT) -> dict[str, dict[str, str]]:
    data = yaml.safe_load((root / "_data" / "taxonomy.yml").read_text(encoding="utf-8")) or {}
    tags: dict[str, Any] = data.get("tags") or data
    return {k: v for k, v in tags.items() if isinstance(v, dict)}


def state_path(lang: str, base: Path = I18N) -> Path:
    return base / lang / "review.json"


def load_state(lang: str, base: Path = I18N) -> dict[str, dict[str, Any]]:
    p = state_path(lang, base)
    return _load(p) if p.is_file() else {}


def tag_rows(lang: str, base: Path = I18N, root: Path = ROOT) -> Iterator[Row]:
    p = base / lang / "tags.json"
    if not p.is_file():
        return
    english = taxonomy_tags(root)
    for slug, entry in _load(p).items():
        if slug.startswith("_") or not isinstance(entry, dict) or entry.get("reviewed"):
            continue
        for field in ("name", "description"):
            if entry.get(field):
                src = str(english.get(slug, {}).get(field, "")).strip()
                yield {
                    "file": "tags.json",
                    "key": f"{slug}.{field}",
                    "english": src,
                    "draft": entry[field],
                }


def author_rows(lang: str, state: dict[str, Any], base: Path = I18N) -> Iterator[Row]:
    p, en = base / lang / "author.json", base / "en" / "author.json"
    if not (p.is_file() and en.is_file()):
        return
    english = _load(en)
    for key, value in _load(p).items():
        if key.startswith("_") or state.get(f"author.json::{key}", {}).get("reviewed"):
            continue
        yield {
            "file": "author.json",
            "key": key,
            "english": str(english.get(key, "")),
            "draft": str(value),
        }


def patch_rows(lang: str, state: dict[str, Any], base: Path = I18N) -> Iterator[Row]:
    for name in PATCH_FILES:
        p = base / lang / name
        if not p.is_file():
            continue
        for pattern, draft in _load(p).get("patches", []):
            key = patch_key(pattern)
            if not state.get(f"{name}::{key}", {}).get("reviewed"):
                yield {"file": name, "key": key, "english": pattern, "draft": draft}


def unreviewed(lang: str, base: Path = I18N, root: Path = ROOT) -> list[Row]:
    state = load_state(lang, base)
    return [
        *tag_rows(lang, base, root),
        *author_rows(lang, state, base),
        *patch_rows(lang, state, base),
    ]


def export(lang: str, out: Path, today: str, base: Path = I18N, root: Path = ROOT) -> int:
    """Write the sheet and stamp ``drafted_on`` for strings seen the first time."""
    rows = unreviewed(lang, base, root)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows({**r, "approved_text": "", "reviewer": "", "notes": ""} for r in rows)
    state = load_state(lang, base)
    for r in rows:
        state.setdefault(f"{r['file']}::{r['key']}", {"reviewed": False, "drafted_on": today})
    _save(state_path(lang, base), dict(sorted(state.items())))
    return len(rows)


def _apply_tag(base: Path, lang: str, row: Row, stamp: dict[str, Any]) -> None:
    p = base / lang / "tags.json"
    data = _load(p)
    slug, field = row["key"].rsplit(".", 1)
    data[slug][field] = row["approved_text"]
    data[slug].update(stamp)
    _save(p, data)


def _apply_author(base: Path, lang: str, row: Row) -> None:
    p = base / lang / "author.json"
    data = _load(p)
    data[row["key"]] = row["approved_text"]
    _save(p, data)


def _apply_patch(base: Path, lang: str, row: Row) -> None:
    p = base / lang / row["file"]
    data = _load(p)
    for entry in data["patches"]:
        if patch_key(entry[0]) == row["key"]:
            entry[1] = row["approved_text"]
    _save(p, data)


def current_english(row: Row, lang: str, base: Path, root: Path) -> str | None:
    """The source text now, or None when the string no longer exists."""
    found = [
        r
        for r in unreviewed(lang, base, root)
        if (r["file"], r["key"]) == (row["file"], row["key"])
    ]
    return found[0]["english"] if found else None


def import_sheet(
    sheet: Path, lang: str, today: str, base: Path = I18N, root: Path = ROOT
) -> tuple[int, list[str]]:
    """Apply approved rows. Returns (applied, refusals)."""
    applied, refused = 0, []
    state = load_state(lang, base)
    with sheet.open(encoding="utf-8", newline="") as fh:
        rows = [r for r in csv.DictReader(fh) if r.get("approved_text", "").strip()]
    for row in rows:
        if current_english(row, lang, base, root) != row["english"]:
            refused.append(f"{row['file']}::{row['key']}: English changed since export, re-export")
            continue
        stamp = {"reviewed": True, "reviewer": row.get("reviewer", ""), "reviewed_on": today}
        if row["file"] == "tags.json":
            _apply_tag(base, lang, row, stamp)
        elif row["file"] == "author.json":
            _apply_author(base, lang, row)
        else:
            _apply_patch(base, lang, row)
        state[f"{row['file']}::{row['key']}"] = {
            **state.get(f"{row['file']}::{row['key']}", {}),
            **stamp,
        }
        applied += 1
    _save(state_path(lang, base), dict(sorted(state.items())))
    return applied, refused


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    ex = sub.add_parser("export")
    ex.add_argument("--lang", required=True)
    ex.add_argument("--out", required=True, type=Path)
    im = sub.add_parser("import")
    im.add_argument("sheet", type=Path)
    im.add_argument("--lang", help="defaults to the sheet's file name (de.csv -> de)")
    args = parser.parse_args(argv)
    today = dt.date.today().isoformat()
    if args.cmd == "export":
        n = export(args.lang, args.out, today)
        print(f"review_sheet: {n} unreviewed string(s) -> {args.out}")
        return 0
    lang = args.lang or args.sheet.stem
    applied, refused = import_sheet(args.sheet, lang, today)
    for line in refused:
        print(f"review_sheet: refused {line}", file=sys.stderr)
    print(f"review_sheet: {applied} approved string(s) written for {lang}")
    return 1 if refused else 0


if __name__ == "__main__":
    raise SystemExit(main())
