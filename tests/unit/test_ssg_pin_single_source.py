"""The ssg version policy must have exactly one value across the repo.

`.github/workflows/ci.yml` is the single source of truth (ADR-0002): it is
what actually builds the deployed site. Every other mention — the Makefile
bootstrap target, the README quick-start, the mise.toml policy note — is
documentation of that value and must agree with it.

This drifted in production. The Makefile installed 0.0.46 while CI built
with 0.0.39 and README documented 0.0.39, so `make bootstrap` handed new
contributors a toolchain CI would reject. A skipped `cargo install` prints
nothing, so nobody noticed. These tests make the drift a build failure.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]

# Any "0.0.x"-style ssg version literal, wherever it appears.
_SSG_VERSION_LITERAL = re.compile(r"\bssg\b[^\n]{0,80}?(\d+\.\d+\.\d+)", re.IGNORECASE)


def _ci_pin() -> str:
    text = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    m = re.search(r'^\s*SSG_VERSION:\s*"([^"]+)"', text, re.MULTILINE)
    assert m, "ci.yml must declare SSG_VERSION — it is the single source of truth"
    return m.group(1)


def test_ci_declares_a_version_policy() -> None:
    """Either `latest` (track every release) or an exact version (hold one
    back). A range or a partial version would reintroduce the drift this
    file exists to prevent."""
    assert _ci_pin() == "latest" or re.fullmatch(r"\d+\.\d+\.\d+", _ci_pin())


def test_mise_tracks_the_same_policy_as_ci() -> None:
    """mise.toml decides which ssg a *developer* build uses. When it and CI
    disagree, local output silently stops matching CI — which is exactly how
    a 14,045-page tree got measured as if it were production's 6,856."""
    mise = (ROOT / "mise.toml").read_text(encoding="utf-8")
    m = re.search(r'^"cargo:ssg"\s*=\s*"([^"]+)"', mise, re.MULTILINE)
    assert m, "mise.toml must declare cargo:ssg so a global mise config cannot shadow it"
    assert m.group(1) == _ci_pin(), (
        f"mise.toml tracks ssg {m.group(1)} but ci.yml says {_ci_pin()}"
    )


# A version number is *binding* when its line reads as an instruction to
# install or a statement of what is pinned. Versions quoted as history
# ("ssg 0.0.45 emits a known lang-leakage false positive", "0.0.48+ altered
# the CSP") are legitimate prose and must stay writable.
_BINDING_LINE = re.compile(r"cargo install|--version|\bpinned\b|\bHeld at\b", re.IGNORECASE)


def _binding_versions(text: str) -> set[str]:
    return {
        m.group(1)
        for line in text.splitlines()
        if _BINDING_LINE.search(line) and "SSG_VERSION" not in line
        for m in _SSG_VERSION_LITERAL.finditer(line)
    }


def test_makefile_derives_the_pin_rather_than_restating_it() -> None:
    """The Makefile must parse ci.yml, not hard-code a version."""
    text = (ROOT / "Makefile").read_text(encoding="utf-8")
    assert "SSG_VERSION := $(shell" in text, "Makefile must derive SSG_VERSION from ci.yml"
    stray = _binding_versions(text)
    assert not stray, (
        f"Makefile hard-codes ssg {sorted(stray)} on a binding line; "
        f"it must use $(SSG_VERSION), derived from ci.yml ({_ci_pin()})"
    )


@pytest.mark.parametrize("relpath", ["README.md", "mise.toml"])
def test_docs_agree_with_the_ci_pin(relpath: str) -> None:
    pin = _ci_pin()
    text = (ROOT / relpath).read_text(encoding="utf-8")
    drift = _binding_versions(text) - {pin}
    assert not drift, (
        f"{relpath} states ssg {sorted(drift)} as the pin; ci.yml pins {pin}"
    )
