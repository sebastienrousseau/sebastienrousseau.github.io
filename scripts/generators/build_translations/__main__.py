#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""CLI entry point — ``python3 scripts/generators/build_translations/__main__.py``
(direct-file invocation from build.sh) or ``python3 -m build_translations``.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Direct-file invocation puts *this* directory on sys.path, not the
# parent — add scripts/generators/ so ``import build_translations``
# resolves to the package.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from build_translations import main

if __name__ == "__main__":  # pragma: no cover — exercised via build.sh
    main()
