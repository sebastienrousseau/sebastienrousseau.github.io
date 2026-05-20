"""scripts/postbuild package — re-exports the public surface of
postbuild.py so legacy ``import postbuild`` and ``postbuild.main()``
calls keep working after the scripts/ reorg.
"""
from __future__ import annotations

from .postbuild import *  # noqa: F403
