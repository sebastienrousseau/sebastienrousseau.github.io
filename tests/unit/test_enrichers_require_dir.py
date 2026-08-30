# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Guard: the in-place enrichers MUST refuse to run without an explicit
``--dir`` (ADR-0003). A bare invocation previously defaulted to ``_posts``
and silently rewrote committed source — this test locks that door.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "postbuild"))


@pytest.mark.parametrize("module_name", ["post_enrich", "topic_link"])
def test_enricher_refuses_without_dir(module_name, monkeypatch):
    monkeypatch.setattr("sys.argv", [module_name])
    mod = __import__(module_name)
    # argparse exits non-zero (code 2) when a required argument is missing.
    with pytest.raises(SystemExit) as exc:
        mod.main()
    assert exc.value.code not in (0, None), (
        f"{module_name}.main() must fail without --dir, not default to _posts"
    )
