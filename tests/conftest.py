"""pytest collection hook: wire scripts/ subpackages into sys.path so
test files can ``import postbuild``, ``import translate_post``, etc.
unchanged after the scripts/ reorg into domain subdirs.

Without this conftest each test file would need to know which subdir
hosts the module it's testing (postbuild moved to scripts/postbuild/,
translate_post to scripts/editorial/, etc.). Wiring once here keeps
the test fixtures stable.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"

# Subdirectory order matters when modules with identical names exist
# in different domains (none today, but lib first means _core etc.
# resolve to the canonical impl).
for sub in ("lib", "editorial", "generators", "postbuild",
            "security", "seo_and_audit", "tests"):
    p = SCRIPTS / sub
    if p.is_dir() and str(p) not in sys.path:
        sys.path.insert(0, str(p))

# Keep the root scripts/ dir on the path too so anything still doing
# ``import scripts.foo`` or relying on the legacy flat layout works.
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
