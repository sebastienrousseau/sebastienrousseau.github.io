# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Dataset distributions are asserted by the deploy check.

A Dataset advertising a distribution.contentUrl that 404s is worse than
publishing no Dataset — it is a broken promise to the exact consumers the
markup exists for, and it is the same present-in-the-build-missing-in-
production failure verify_deploy.py was written for.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "seo_and_audit"))

import verify_deploy as vd

MANIFEST = {
    "datasets": [
        {"slug": "2026-06-02-an-index", "name": "An Index"},
        {"slug": "2026-06-29-a-scorecard", "name": "A Scorecard"},
    ]
}


def _manifest(tmp_path: Path, payload: dict) -> Path:
    path = tmp_path / "datasets.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_both_distributions_of_every_dataset_are_asserted(tmp_path, monkeypatch):
    monkeypatch.setattr(vd, "DATASETS_MANIFEST", _manifest(tmp_path, MANIFEST))
    assert vd.dataset_paths() == {
        "/data/2026-06-02-an-index.json",
        "/data/2026-06-02-an-index.csv",
        "/data/2026-06-29-a-scorecard.json",
        "/data/2026-06-29-a-scorecard.csv",
    }


def test_a_new_dataset_extends_the_check_without_editing_it(tmp_path, monkeypatch):
    """The point of deriving from the manifest rather than a literal list."""
    manifest = _manifest(tmp_path, MANIFEST)
    monkeypatch.setattr(vd, "DATASETS_MANIFEST", manifest)
    before = vd.dataset_paths()

    grown = {"datasets": [*MANIFEST["datasets"], {"slug": "2026-07-01-another"}]}
    manifest.write_text(json.dumps(grown), encoding="utf-8")
    after = vd.dataset_paths()

    assert after - before == {
        "/data/2026-07-01-another.json",
        "/data/2026-07-01-another.csv",
    }


def test_missing_manifest_is_not_an_error(tmp_path, monkeypatch):
    """A checkout without a build must not fail the deploy verifier."""
    monkeypatch.setattr(vd, "DATASETS_MANIFEST", tmp_path / "absent.json")
    assert vd.dataset_paths() == set()


def test_empty_manifest_yields_nothing(tmp_path, monkeypatch):
    monkeypatch.setattr(vd, "DATASETS_MANIFEST", _manifest(tmp_path, {"datasets": []}))
    assert vd.dataset_paths() == set()


def test_the_real_manifest_matches_the_built_files():
    """Every path the deploy check asserts must exist in public/."""
    paths = vd.dataset_paths()
    if not paths:
        return  # no build in this checkout
    public = Path(__file__).resolve().parents[2] / "public"
    if not (public / "data").is_dir():
        return
    missing = [p for p in sorted(paths) if not (public / p.lstrip("/")).is_file()]
    assert missing == []
