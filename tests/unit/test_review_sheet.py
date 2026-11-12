# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""scripts/i18n/review_sheet.py: export, review, import."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "i18n"))
import review_sheet as rs


def _tree(tmp: Path) -> tuple[Path, Path]:
    base, root = tmp / "i18n", tmp
    (base / "de").mkdir(parents=True)
    (base / "en").mkdir()
    (root / "_data").mkdir()
    (root / "_data" / "taxonomy.yml").write_text(
        "ai:\n  name: AI\n  description: |\n    Applied AI.\n", encoding="utf-8"
    )
    (base / "de" / "tags.json").write_text(
        json.dumps(
            {
                "_comment": "x",
                "ai": {"name": "KI", "description": "Angewandte KI.", "reviewed": False},
            }
        ),
        encoding="utf-8",
    )
    (base / "en" / "author.json").write_text(json.dumps({"bio": "Leader."}), encoding="utf-8")
    (base / "de" / "author.json").write_text(
        json.dumps({"_reviewed": False, "bio": "Leiter."}), encoding="utf-8"
    )
    (base / "de" / "home_patches.json").write_text(
        json.dumps({"patches": [[">Hello<", ">Hallo<"]]}), encoding="utf-8"
    )
    return base, root


def _rows(sheet: Path) -> list[dict[str, str]]:
    with sheet.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _write(sheet: Path, rows: list[dict[str, str]]) -> None:
    with sheet.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=rs.COLUMNS)
        w.writeheader()
        w.writerows(rows)


def test_export_lists_every_unreviewed_string_and_stamps_drafted_on(tmp_path: Path) -> None:
    base, root = _tree(tmp_path)
    sheet = tmp_path / "de.csv"
    assert rs.export("de", sheet, "2026-11-10", base, root) == 4
    rows = _rows(sheet)
    assert {(r["file"], r["key"]) for r in rows} == {
        ("tags.json", "ai.name"),
        ("tags.json", "ai.description"),
        ("author.json", "bio"),
        ("home_patches.json", rs.patch_key(">Hello<")),
    }
    assert next(r for r in rows if r["key"] == "ai.description")["english"] == "Applied AI."
    state = json.loads((base / "de" / "review.json").read_text(encoding="utf-8"))
    assert all(v == {"reviewed": False, "drafted_on": "2026-11-10"} for v in state.values())


def test_import_writes_approved_rows_and_marks_them_reviewed(tmp_path: Path) -> None:
    base, root = _tree(tmp_path)
    sheet = tmp_path / "de.csv"
    rs.export("de", sheet, "2026-11-10", base, root)
    rows = _rows(sheet)
    for r in rows:
        r["approved_text"] = {"ai.name": "KI (Angewandt)", "bio": "Leiterin."}.get(r["key"], "")
        if r["file"] == "home_patches.json":
            r["approved_text"] = ">Guten Tag<"
        r["reviewer"] = "Native Reviewer"
    _write(sheet, rows)
    applied, refused = rs.import_sheet(sheet, "de", "2026-11-12", base, root)
    assert (applied, refused) == (3, [])
    tags = json.loads((base / "de" / "tags.json").read_text(encoding="utf-8"))
    assert tags["ai"]["name"] == "KI (Angewandt)" and tags["ai"]["reviewed"] is True
    assert tags["ai"]["reviewed_on"] == "2026-11-12"
    assert (
        json.loads((base / "de" / "author.json").read_text(encoding="utf-8"))["bio"] == "Leiterin."
    )
    patches = json.loads((base / "de" / "home_patches.json").read_text(encoding="utf-8"))["patches"]
    assert patches == [[">Hello<", ">Guten Tag<"]]
    left = rs.unreviewed("de", base, root)
    assert [r["key"] for r in left] == []  # the reviewed tag drops out whole


def test_import_refuses_rows_whose_english_changed(tmp_path: Path) -> None:
    base, root = _tree(tmp_path)
    sheet = tmp_path / "de.csv"
    rs.export("de", sheet, "2026-11-10", base, root)
    rows = _rows(sheet)
    for r in rows:
        r["approved_text"] = "neu" if r["file"] == "author.json" else ""
    _write(sheet, rows)
    (base / "en" / "author.json").write_text(json.dumps({"bio": "Changed."}), encoding="utf-8")
    applied, refused = rs.import_sheet(sheet, "de", "2026-11-12", base, root)
    assert applied == 0 and "English changed" in refused[0]


def test_missing_files_yield_nothing(tmp_path: Path) -> None:
    base, root = _tree(tmp_path)
    (base / "fr").mkdir()
    assert rs.unreviewed("fr", base, root) == []


def test_cli_requires_a_subcommand() -> None:
    with pytest.raises(SystemExit):
        rs.main([])
