"""llms.txt advertises the index datasets.

llms.txt is where this site tells a crawler which surfaces are
machine-readable. A dataset nobody is pointed at is a dataset nobody
retrieves, and listing them also brings the paths under verify_deploy.py,
which asserts every path llms.txt advertises resolves.
"""

from __future__ import annotations

import json
from pathlib import Path

from postbuild_lib import output

BASE = "https://example.test"

MANIFEST = {
    "datasets": [
        {"slug": "2026-06-02-an-index", "name": "An Index", "variables": [{}, {}, {}]},
        {"slug": "2026-06-29-a-scorecard", "name": "A Scorecard", "variables": [{}]},
    ]
}


def _manifest(tmp_path: Path, payload: dict) -> Path:
    path = tmp_path / "datasets.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_every_dataset_is_advertised(tmp_path, monkeypatch):
    monkeypatch.setattr(output, "_DATASETS_MANIFEST", _manifest(tmp_path, MANIFEST))
    lines = output._dataset_lines(BASE)
    assert len(lines) == 3  # one summary + one per dataset
    assert f"{BASE}/data/2026-06-02-an-index.json" in lines[1]
    assert f"{BASE}/data/2026-06-29-a-scorecard.json" in lines[2]


def test_the_summary_line_states_how_many(tmp_path, monkeypatch):
    monkeypatch.setattr(output, "_DATASETS_MANIFEST", _manifest(tmp_path, MANIFEST))
    assert "(2 today)" in output._dataset_lines(BASE)[0]


def test_each_entry_reports_its_variable_count(tmp_path, monkeypatch):
    monkeypatch.setattr(output, "_DATASETS_MANIFEST", _manifest(tmp_path, MANIFEST))
    lines = output._dataset_lines(BASE)
    assert "3 measured variables" in lines[1]
    assert "1 measured variables" in lines[2]


def test_no_manifest_advertises_nothing(tmp_path, monkeypatch):
    """A tree that has not been built must not emit a broken pointer."""
    monkeypatch.setattr(output, "_DATASETS_MANIFEST", tmp_path / "absent.json")
    assert output._dataset_lines(BASE) == []


def test_an_empty_manifest_advertises_nothing(tmp_path, monkeypatch):
    monkeypatch.setattr(output, "_DATASETS_MANIFEST", _manifest(tmp_path, {"datasets": []}))
    assert output._dataset_lines(BASE) == []
