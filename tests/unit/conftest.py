"""pytest collection hook: wire scripts/ subpackages into sys.path so
test files can ``import postbuild``, ``import translate_post``, etc.
unchanged after the scripts/ reorg into domain subdirs.

Without this conftest each test file would need to know which subdir
hosts the module it's testing (postbuild moved to scripts/postbuild/,
translate_post to scripts/editorial/, etc.). Wiring once here keeps
the test fixtures stable.
"""

from __future__ import annotations

import shutil
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
# Isolation: the unit suite runs against a disposable clone of the build tree.
#
# Several modules invoke real builder / postbuild entry points for coverage,
# and those write. They used to write into the real ``public/``: measured at
# 6,497 files rewritten across a full run. That made the suite
# order-dependent — a module reading ``public/`` after another had rewritten
# it saw an incoherent build, which is why ``test_csp_strict_passes`` and
# ``test_pages_with_eager_image_have_preload`` passed alone and failed in a
# full run. CI hid it by partitioning the suite across shards.
#
# Two builders were worse: ``gen_layouts`` and ``gen_articles`` anchor paths
# on ``__file__`` rather than the CWD, so they wrote into committed source
# (``_layouts/``, ``_posts/articles.md``) and left the repo dirty.
#
# So the whole session runs inside a clone:
#
#   * ``chdir`` redirects everything that resolves a CWD-relative path
#     (``Path("public")`` and friends — the common case by far).
#   * ``__file__``-anchored constants are absolute by import time, so every
#     Path attribute on a ``scripts/`` module is repointed into the sandbox
#     as that module appears in ``sys.modules``. Walking attributes rather
#     than keeping a list matters: a list goes stale, and the first version
#     of this work missed ``gen_articles`` for exactly that reason.
#
# The gate below then fails the run if anything still escaped, naming it.
# ---------------------------------------------------------------------------

PUBLIC = ROOT / "public"
_CLONED = ("public", "_posts", "_data", "_layouts")
_sandbox: Path | None = None
_repointed: set[str] = set()


def _clone_tree(src: Path, dst: Path) -> None:
    """Copy ``src`` to ``dst``, preferring a filesystem copy-on-write clone.

    ``public/`` is ~1.1 GB over 24k files. APFS and btrfs/xfs clone that in
    seconds at near-zero disk; elsewhere it degrades to a real copy, which is
    still the right trade against an order-dependent suite.
    """
    for cmd in (["cp", "--reflink=auto", "-R"], ["cp", "-c", "-R"], ["cp", "-R"]):
        try:
            if (
                subprocess.run(
                    [*cmd, str(src), str(dst)], capture_output=True, timeout=1800
                ).returncode
                == 0
            ):
                return
        except (OSError, subprocess.SubprocessError):
            continue
    shutil.copytree(src, dst)


def _repoint(mod: object, sandbox: Path, mp: pytest.MonkeyPatch) -> None:
    """Redirect absolute Path constants on ``mod`` that point into the repo."""
    for attr, val in list(vars(mod).items()):
        if attr.startswith("__") or not isinstance(val, Path) or not val.is_absolute():
            continue
        try:
            rel = val.resolve().relative_to(ROOT)
        except ValueError:
            continue
        mp.setattr(mod, attr, sandbox if rel == Path(".") else sandbox / rel, raising=False)


@pytest.fixture(scope="session", autouse=True)
def _sandboxed_working_tree(tmp_path_factory):
    """Run the whole unit session inside a disposable clone of the tree."""
    global _sandbox
    if not PUBLIC.is_dir():
        yield None
        return
    sandbox = tmp_path_factory.mktemp("worktree")
    for name in _CLONED:
        src = ROOT / name
        if src.is_dir():
            _clone_tree(src, sandbox / name)
    mp = pytest.MonkeyPatch()
    mp.chdir(sandbox)
    _sandbox = sandbox
    try:
        yield sandbox
    finally:
        _sandbox = None
        _repointed.clear()
        mp.undo()


@pytest.hookimpl(trylast=True)
def pytest_runtest_setup(item: pytest.Item) -> None:
    """Repoint any ``scripts/`` module imported since the last test.

    Modules are imported lazily inside tests, so this cannot be done once up
    front. Each module is processed only on the run in which it first
    appears, so the cost is bounded by the number of modules, not tests.
    """
    if _sandbox is None:
        return
    scripts_dir = str(SCRIPTS)
    mp = item.config._sandbox_mp  # type: ignore[attr-defined]
    for name, mod in list(sys.modules.items()):
        if name in _repointed or mod is None:
            continue
        f = getattr(mod, "__file__", None)
        if not f or not f.startswith(scripts_dir):
            continue
        _repointed.add(name)
        _repoint(mod, _sandbox, mp)


def pytest_configure(config: pytest.Config) -> None:
    config._sandbox_mp = pytest.MonkeyPatch()  # type: ignore[attr-defined]


def pytest_unconfigure(config: pytest.Config) -> None:
    mp = getattr(config, "_sandbox_mp", None)
    if mp is not None:
        mp.undo()


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
# The session now runs inside a clone (above). This gate stops the property
# from regressing silently: it fails the run if any test wrote into the real
# ``public/`` or dirtied a tracked file, and names what changed.
# ---------------------------------------------------------------------------


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
