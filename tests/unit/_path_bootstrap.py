# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Standalone-run sys.path wiring shared by test modules.

Mirrors tests/unit/conftest.py: puts the scripts/ domain subdirs on
sys.path so ``import build_case_studies`` etc. resolve when a test file
is executed directly (``python3 tests/unit/test_x.py``) instead of via
pytest (where conftest.py already does this). The wiring runs at import
time; callers invoke ``ensure()`` so the import is explicit real usage
(keeps both ruff F401 and CodeQL py/unused-import quiet):

    import _path_bootstrap
    _path_bootstrap.ensure()
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]

for _sub in ("lib", "editorial", "generators", "postbuild"):
    _p = _ROOT / "scripts" / _sub
    if _p.is_dir() and str(_p) not in sys.path:
        sys.path.insert(0, str(_p))


def ensure() -> None:
    """No-op confirmation hook; the wiring above ran at import time."""
