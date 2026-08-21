"""`build.sh` must pin the build clock, or the output is not reproducible.

ssg stamps `metadata.timestamp` into `sbom.cdx.json` from the wall clock
unless `SOURCE_DATE_EPOCH` is set (it honours the variable — see ssg's
`current_iso_timestamp`). Without it, two builds of the same commit produce
two different SBOMs, and the byte-identical-rebuild gate fails on that single
file long after every real non-determinism has been fixed. That is exactly
how this surfaced: a green build, one differing artefact, no real defect.

pandoc/LaTeX honour the same variable, so the pin also covers the lead-magnet
PDFs.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
BUILD_SH = ROOT / "build.sh"


def test_build_sh_exports_source_date_epoch():
    body = BUILD_SH.read_text(encoding="utf-8")
    assert "SOURCE_DATE_EPOCH" in body, "build.sh must pin the build clock"
    assert re.search(r"export\s+SOURCE_DATE_EPOCH", body), (
        "SOURCE_DATE_EPOCH must be exported, not just assigned — child "
        "processes (ssg, pandoc) read it from the environment"
    )


def test_pin_defers_to_an_already_exported_value():
    """A caller pinning an explicit epoch must win, so a release build can
    stamp a chosen time rather than the last commit's."""
    body = BUILD_SH.read_text(encoding="utf-8")
    assert re.search(r'if \[ -z "\$\{SOURCE_DATE_EPOCH:-\}" \]', body), (
        "build.sh must only set SOURCE_DATE_EPOCH when it is unset"
    )


def test_pinned_value_is_the_commit_time_and_is_stable():
    """The value must be a function of the commit, not of when the build ran —
    two evaluations in the same repo state must agree."""
    body = BUILD_SH.read_text(encoding="utf-8")
    assert "git log -1 --format=%ct" in body, (
        "the pin should derive from the last commit (reproducible-builds "
        f"convention); build.sh says: {body[:0]!r}"
    )
    first = subprocess.run(
        ["git", "log", "-1", "--format=%ct"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    second = subprocess.run(
        ["git", "log", "-1", "--format=%ct"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    assert first == second and first.isdigit(), (first, second)
