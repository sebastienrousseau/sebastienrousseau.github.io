# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""The unit sandbox must cover a module the moment it is imported.

``conftest.py`` runs the session in a clone and repoints the absolute
``Path`` constants of every ``scripts/`` module into it. It used to do that
once per module *name*, at the *next* test's setup. Two ordinary patterns
escaped it: a module imported and run inside one test body
(``test_gen_layouts_main_runs``), and a module force-reimported by
``test_cli_smoke._import_fresh``, whose fresh object kept the real paths
because its name was already marked done. ``gen_layouts.main()`` then wrote
into the real ``_layouts/``. That went unseen while its output equalled the
committed layouts; once the layouts came from the theme (ADR-0014), it
rewrote twelve of them on every run.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def _under(p: Path, root: Path) -> bool:
    try:
        p.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


@pytest.fixture
def sandbox(_sandboxed_working_tree: Path | None) -> Path:
    if _sandboxed_working_tree is None:
        pytest.skip("no public/ build, so the session runs unsandboxed")
    return _sandboxed_working_tree


def test_a_module_imported_inside_a_test_is_repointed_at_once(sandbox: Path) -> None:
    sys.modules.pop("gen_layouts", None)
    mod = importlib.import_module("gen_layouts")
    assert _under(mod.LAYOUTS, sandbox), mod.LAYOUTS
    assert not _under(mod.LAYOUTS, ROOT) or _under(ROOT, sandbox)


def test_a_force_reimported_module_is_repointed_again(sandbox: Path) -> None:
    first = importlib.import_module("gen_layouts")
    sys.modules.pop("gen_layouts", None)
    second = importlib.import_module("gen_layouts")
    assert second is not first
    assert _under(second.LAYOUTS, sandbox), second.LAYOUTS
