# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""scripts/release/check_releases.py: every merged version is a full release."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "release"))
import check_releases as cr

CHANGELOG = """## [0.0.36] - Unreleased
## [0.0.35] - 2026-11-09
## [0.0.34] - 2026-11-08
"""
GOOD_BODY = "## Highlights ⭐️\n* x\n\n## What's Changed\n* y\n\n**Full Changelog**: z\n"


def _release(version: str, body: str = GOOD_BODY, assets: list[str] | None = None) -> dict:
    names = assets if assets is not None else [a.format(n=cr.NAME, v=version) for a in cr.ASSETS]
    return {"name": f"{cr.NAME} {version}", "body": body, "assets": [{"name": n} for n in names]}


def test_only_dated_sections_are_released() -> None:
    assert cr.released_versions(CHANGELOG) == ["0.0.35", "0.0.34"]


def test_a_complete_release_passes() -> None:
    assert cr.release_problems("0.0.35", _release("0.0.35")) == []


def test_missing_release_wrong_title_sections_and_assets_are_reported() -> None:
    assert cr.release_problems("0.0.35", None) == ["v0.0.35: no release"]
    bad = _release("0.0.35", body="## Highlights ⭐️\n## Checksums\n", assets=[])
    bad["name"] = "v0.0.35"
    problems = cr.release_problems("0.0.35", bad)
    assert any("title 'v0.0.35'" in p for p in problems)
    assert any("What's Changed" in p for p in problems)
    assert any("Checksums" in p for p in problems)
    assert sum("asset" in p for p in problems) == len(cr.ASSETS)


def test_tags_must_be_annotated_and_signed() -> None:
    assert cr.tag_problems("0.0.35", "", "") == ["v0.0.35: no tag"]
    assert "lightweight" in cr.tag_problems("0.0.35", "commit", "")[0]
    assert "not signed" in cr.tag_problems("0.0.35", "tag", "object abc\n")[0]
    assert cr.tag_problems("0.0.35", "tag", "-----BEGIN SSH SIGNATURE-----") == []


def test_check_walks_every_released_version() -> None:
    def run(*cmd: str) -> str:
        return "tag\n" if cmd[:3] == ("git", "cat-file", "-t") else "-----BEGIN SSH SIGNATURE-----"

    releases = {"0.0.35": _release("0.0.35"), "0.0.34": None}
    problems = cr.check(CHANGELOG, gh_release=releases.get, run=run)
    assert problems == ["v0.0.34: no release"]
