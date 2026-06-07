"""scripts/postbuild package — replaces itself in sys.modules with the
postbuild.py module so legacy ``import postbuild`` returns the real
module (with all public + underscore-prefixed names + editable
globals), not this thin package shim.

Tests written before the reorg both
  - poke at private names (``postbuild._FOO``), and
  - monkeypatch module-level state (``postbuild.PUBLIC = tmp_path``).
Both behaviours require ``postbuild`` in sys.modules to BE the
postbuild.py module. ``from .postbuild import *`` would only re-
export public names and would create a separate package object
whose attributes drift from the underlying module's.
"""

from __future__ import annotations

import sys as _sys

from . import postbuild as _impl

# Preserve the package's __path__ on the swap target so importlib.reload
# (which walks parent.__path__ via the module spec) keeps working after
# sys.modules['postbuild'] is rebound to the postbuild.postbuild module.
_impl.__path__ = __path__  # type: ignore[attr-defined]
_sys.modules[__name__] = _impl
