"""Every pinned requirement must equal what its lock actually installs.

CI installs with `pip install --require-hashes -r requirements-dev.lock`, so
the lock — not the `.txt` — decides which versions run. Nothing checked that
the two agreed, and all four dev pins had drifted:

    ruff           .txt 0.16.2              lock 0.15.9
    mypy           .txt 2.3.0               lock 2.1.0
    types-PyYAML   .txt 6.0.12.20260724     lock 6.0.12.20260518
    cyclonedx-bom  .txt 7.3.1               lock 7.3.0

Every Dependabot bump had been landing in the `.txt` without anyone running
`scripts/security/lock-deps.sh`, so CI kept running the old versions while the
file advertised the new ones — and Dependabot kept reopening the same PRs.
A lint or type gate that claims to run ruff 0.16 while running 0.15 is worse
than no claim at all.

These tests make that drift a build failure instead of a silent divergence.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]

# `name==version` — exact pins only. Range specifiers (`>=4.2.0,<5`) are
# handled separately: the lock resolves them, so there is no single version to
# compare against, only a package that must be present.
_EXACT = re.compile(r"^([A-Za-z0-9_.\-]+)==([^\s#;\\]+)", re.MULTILINE)
_ANY_REQ = re.compile(r"^([A-Za-z0-9_.\-]+)\s*(?:[=<>!~]|$)", re.MULTILINE)

PAIRS = [
    ("requirements.txt", "requirements.lock"),
    ("requirements-dev.txt", "requirements-dev.lock"),
    ("fly/pdf-render/requirements.txt", "fly/pdf-render/requirements.lock"),
]


def _canon(name: str) -> str:
    """PEP 503 normalisation — `types-PyYAML` and `types_pyyaml` are one name."""
    return re.sub(r"[-_.]+", "-", name).lower()


def _exact_pins(path: Path) -> dict[str, str]:
    return {_canon(n): v for n, v in _EXACT.findall(path.read_text(encoding="utf-8"))}


def _declared(path: Path) -> set[str]:
    body = path.read_text(encoding="utf-8")
    lines = [ln for ln in body.splitlines() if ln.strip() and not ln.lstrip().startswith("#")]
    return {_canon(m.group(1)) for ln in lines if (m := _ANY_REQ.match(ln))}


@pytest.mark.parametrize(("src", "lock"), PAIRS)
def test_every_exact_pin_matches_the_lock(src: str, lock: str) -> None:
    """An `==` pin is a claim about what runs. The lock is what actually runs."""
    src_path, lock_path = ROOT / src, ROOT / lock
    if not src_path.is_file() or not lock_path.is_file():
        pytest.skip(f"{src} / {lock} not present")

    declared, locked = _exact_pins(src_path), _exact_pins(lock_path)
    drift = {
        name: (want, locked.get(name))
        for name, want in declared.items()
        if locked.get(name) != want
    }
    assert not drift, (
        f"{src} and {lock} disagree — CI installs the lock, so those versions "
        f"are what actually run. Regenerate with scripts/security/lock-deps.sh.\n"
        + "\n".join(
            f"  {n}: {src}={w} {lock}={g or 'ABSENT'}" for n, (w, g) in sorted(drift.items())
        )
    )


@pytest.mark.parametrize(("src", "lock"), PAIRS)
def test_every_declared_package_is_locked(src: str, lock: str) -> None:
    """Covers range specifiers too: a declared package missing from the lock
    is simply never installed, however the requirement was written."""
    src_path, lock_path = ROOT / src, ROOT / lock
    if not src_path.is_file() or not lock_path.is_file():
        pytest.skip(f"{src} / {lock} not present")

    declared = _declared(src_path)
    assert declared, f"{src} declares nothing — the parser or the file changed"
    missing = sorted(declared - set(_exact_pins(lock_path)))
    assert not missing, f"{src} declares packages absent from {lock}: {missing}"


@pytest.mark.parametrize(("src", "lock"), PAIRS)
def test_lock_is_hash_pinned(src: str, lock: str) -> None:
    """`--require-hashes` only protects what carries hashes."""
    lock_path = ROOT / lock
    if not lock_path.is_file():
        pytest.skip(f"{lock} not present")
    body = lock_path.read_text(encoding="utf-8")
    pins = len(_EXACT.findall(body))
    assert pins, f"{lock} contains no pins"
    assert body.count("--hash=sha256:") >= pins, (
        f"{lock} has {pins} pins but fewer hash lines — an unhashed entry "
        "would be rejected by `pip install --require-hashes`"
    )
