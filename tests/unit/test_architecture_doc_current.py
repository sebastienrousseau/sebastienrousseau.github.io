"""Guard: every generator/postbuild script `build.sh` runs must be documented
in `project-docs/architecture.md` — improvement-plan-2026 Phase 5.4.

The architecture doc had drifted (it described "seven build stages" while
`build.sh` actually runs nineteen generator/postbuild scripts). This test
keeps the doc honest going forward: add a `python3 scripts/...py` step to
`build.sh` without naming it in architecture.md and CI fails.

Doc token per script:
- `.../build_translations/__main__.py`  -> the package name `build_translations`
- everything else                       -> the filename, e.g. `build_topics.py`
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BUILD_SH = ROOT / "build.sh"
ARCH_DOC = ROOT / "project-docs" / "architecture.md"

_INVOCATION = re.compile(r"python3 scripts/(\S+\.py)")


def _doc_token(rel_path: str) -> str:
    """Map a `scripts/`-relative path to the token expected in the doc."""
    p = Path(rel_path)
    if p.name == "__main__.py":
        return p.parent.name
    return p.name


def _build_scripts() -> list[str]:
    text = BUILD_SH.read_text(encoding="utf-8")
    # Preserve order, drop duplicates.
    seen: dict[str, None] = {}
    for m in _INVOCATION.finditer(text):
        seen.setdefault(m.group(1), None)
    return list(seen)


def test_every_build_script_is_documented() -> None:
    doc = ARCH_DOC.read_text(encoding="utf-8")
    scripts = _build_scripts()
    assert scripts, "no `python3 scripts/...py` invocations found in build.sh"

    missing = sorted(rel for rel in scripts if _doc_token(rel) not in doc)
    assert not missing, (
        "architecture.md is missing build-pipeline scripts (Phase 5.4): "
        + ", ".join(missing)
        + ". Document each in project-docs/architecture.md."
    )
