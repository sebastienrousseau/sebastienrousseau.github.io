#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Every version merged to main is a release in the dotfiles format.

For each dated ``## [X.Y.Z] - YYYY-MM-DD`` section of CHANGELOG.md (a
version that reached main), check that:

* tag ``vX.Y.Z`` exists, annotated and signed;
* a release exists for it, titled ``sebastienrousseau.github.io X.Y.Z``;
* its notes have the dotfiles sections (Highlights, What's Changed, Full
  Changelog) and nothing the dotfiles notes lack (no Checksums section:
  checksums ship as the SHA256SUMS asset);
* the deployment artefacts are attached: the site as tar.gz and zip, a
  sigstore bundle for each, the CycloneDX SBOM and SHA256SUMS.

Versions listed in ``KNOWN_WITHOUT_ARTEFACTS`` are the historical releases
whose tagged source can no longer be built; they must still be tagged,
titled and noted correctly. The list may only shrink.

Run from the repo root: ``python3 scripts/release/check_releases.py``.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

REPO = "sebastienrousseau/sebastienrousseau.github.io"
NAME = "sebastienrousseau.github.io"
ROOT = Path(__file__).resolve().parents[2]
_DATED_RE = re.compile(r"^## \[(\d+\.\d+\.\d+)\] - \d{4}-\d{2}-\d{2}\s*$", re.M)
SECTIONS = ("## Highlights ⭐️", "## What's Changed", "**Full Changelog**:")
FORBIDDEN = ("## Checksums",)
ASSETS = (
    "{n}-{v}.tar.gz",
    "{n}-{v}.zip",
    "{n}-{v}.tar.gz.sigstore.json",
    "{n}-{v}.zip.sigstore.json",
    "{n}-{v}.cyclonedx.json",
    "SHA256SUMS",
)
# v0.0.1 to v0.0.19 predate the build pipeline release.yml runs (no
# setup-ssg action, no SSG_VERSION): their tagged source cannot be built.
KNOWN_WITHOUT_ARTEFACTS: frozenset[str] = frozenset(f"0.0.{i}" for i in range(1, 20))


def released_versions(changelog: str) -> list[str]:
    """Versions with a dated CHANGELOG section, newest first."""
    return _DATED_RE.findall(changelog)


def release_problems(version: str, release: dict | None) -> list[str]:
    """What is wrong with ``release`` (gh release view JSON) for ``version``."""
    if release is None:
        return [f"v{version}: no release"]
    out = []
    if release.get("name") != f"{NAME} {version}":
        out.append(f"v{version}: title {release.get('name')!r}, expected '{NAME} {version}'")
    body = release.get("body") or ""
    out += [f"v{version}: notes lack {s!r}" for s in SECTIONS if s not in body]
    out += [f"v{version}: notes carry {s!r}" for s in FORBIDDEN if s in body]
    if version not in KNOWN_WITHOUT_ARTEFACTS:
        names = {a["name"] for a in release.get("assets", [])}
        want = [a.format(n=NAME, v=version) for a in ASSETS]
        out += [f"v{version}: asset {a} missing" for a in want if a not in names]
    return out


def tag_problems(version: str, tag_type: str, tag_body: str) -> list[str]:
    """``tag_type`` is ``git cat-file -t``; ``tag_body`` is ``git cat-file tag``."""
    if not tag_type:
        return [f"v{version}: no tag"]
    if tag_type != "tag":
        return [f"v{version}: lightweight tag (must be annotated and signed)"]
    if not re.search(r"BEGIN (PGP|SSH) SIGNATURE", tag_body):
        return [f"v{version}: tag is not signed"]
    return []


def _run(*cmd: str) -> str:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def _gh_release(version: str) -> dict | None:
    out = _run("gh", "release", "view", f"v{version}", "-R", REPO, "--json", "name,body,assets")
    return json.loads(out) if out else None


def check(
    changelog: str,
    gh_release: Callable[[str], dict | None] = _gh_release,
    run: Callable[..., str] = _run,
) -> list[str]:
    problems: list[str] = []
    for v in released_versions(changelog):
        tag_type = run("git", "cat-file", "-t", f"v{v}").strip()
        tag_body = run("git", "cat-file", "tag", f"v{v}") if tag_type == "tag" else ""
        problems += tag_problems(v, tag_type, tag_body)
        problems += release_problems(v, gh_release(v))
    return problems


def main() -> int:
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    problems = check(changelog)
    n = len(released_versions(changelog))
    if problems:
        print(f"release drift: {len(problems)} problem(s) across {n} released versions")
        for p in problems:
            print(f"  {p}")
        return 1
    print(f"ok: {n} released versions are signed, titled, noted and carry their artefacts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
