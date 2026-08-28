"""pytest collection hook: wire scripts/ subpackages into sys.path so
test files can ``import postbuild``, ``import translate_post``, etc.
unchanged after the scripts/ reorg into domain subdirs.

Without this conftest each test file would need to know which subdir
hosts the module it's testing (postbuild moved to scripts/postbuild/,
translate_post to scripts/editorial/, etc.). Wiring once here keeps
the test fixtures stable.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "scripts"

# Subdirectory order matters when modules with identical names exist
# in different domains (none today, but lib first means _core etc.
# resolve to the canonical impl).
for sub in ("lib", "editorial", "generators", "postbuild", "security", "seo_and_audit", "dev"):
    p = SCRIPTS / sub
    if p.is_dir() and str(p) not in sys.path:
        sys.path.insert(0, str(p))

val_path = ROOT / "tests" / "validation"
if val_path.is_dir() and str(val_path) not in sys.path:
    sys.path.insert(0, str(val_path))

# Keep the root scripts/ dir on the path too so anything still doing
# ``import scripts.foo`` or relying on the legacy flat layout works.
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


# ---------------------------------------------------------------------------
# Isolation gate — the unit suite must not mutate the working tree.
#
# It used to. ``test_builder_main_smoke`` invoked real builder ``main()``s
# against the real ``public/`` for coverage and repaired CSP/SRI at module
# teardown. Measured: 6,453 files rewritten. Any module that read the tree
# before that teardown saw an incoherent build, which is why
# ``test_csp_strict_passes`` and ``test_pages_with_eager_image_have_preload``
# passed alone and failed in a full run — order-dependence CI only hid
# because it partitions the suite.
#
# Two builders anchored on ``__file__`` rather than the CWD and wrote into
# *committed source*: ``gen_layouts`` into ``_layouts/`` and ``gen_articles``
# into ``_posts/articles.md``. A test run left the repo dirty.
#
# The tests now run against a disposable clone (see
# ``test_builder_main_smoke._sandboxed_build_tree``). This gate stops the
# property from silently regressing: it fails the run if any test wrote into
# ``public/`` or dirtied a tracked file, and names what changed.
# ---------------------------------------------------------------------------

PUBLIC = ROOT / "public"


def _public_manifest() -> dict[str, tuple[int, int]]:
    """(size, mtime_ns) per file. stat only — hashing 24k files would
    cost more than the suite it guards."""
    if not PUBLIC.is_dir():
        return {}
    out: dict[str, tuple[int, int]] = {}
    for p in PUBLIC.rglob("*"):
        if p.is_file():
            st = p.stat()
            out[str(p.relative_to(PUBLIC))] = (st.st_size, st.st_mtime_ns)
    return out


def _dirty_tracked() -> set[str]:
    """Tracked files the working tree reports as modified or deleted."""
    try:
        r = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=no"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except (OSError, subprocess.SubprocessError):  # pragma: no cover - git absent
        return set()
    return {line[3:].strip() for line in r.stdout.splitlines() if line.strip()}


@pytest.fixture(scope="session", autouse=True)
def _working_tree_is_not_mutated() -> object:
    """Fail the session if the unit suite mutated the working tree."""
    before_public, before_git = _public_manifest(), _dirty_tracked()
    yield
    after_public, after_git = _public_manifest(), _dirty_tracked()

    changed = sorted(
        k
        for k in set(before_public) | set(after_public)
        if before_public.get(k) != after_public.get(k)
    )
    newly_dirty = sorted(after_git - before_git)

    problems = []
    if changed:
        problems.append(
            f"{len(changed)} file(s) under public/ changed: "
            + ", ".join(changed[:5])
            + (" …" if len(changed) > 5 else "")
        )
    if newly_dirty:
        problems.append(
            f"{len(newly_dirty)} tracked file(s) newly dirty: "
            + ", ".join(newly_dirty[:5])
            + (" …" if len(newly_dirty) > 5 else "")
        )
    if problems:
        raise AssertionError(
            "unit tests mutated the working tree — they must run against a "
            "disposable clone instead (see test_builder_main_smoke."
            "_sandboxed_build_tree):\n  " + "\n  ".join(problems)
        )
