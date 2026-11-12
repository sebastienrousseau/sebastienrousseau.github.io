# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Article furniture switches from ``_data/article_furniture.yml`` (plan C-4).

``flagged(name, fn)`` returns ``fn`` when the flag is on (or absent) and a
pass-through otherwise, so the postbuild article passes keep their order
and counters and a flag only decides whether a panel is added.
"""

from __future__ import annotations

from collections.abc import Callable
from functools import cache
from pathlib import Path

import yaml

FLAGS = Path(__file__).resolve().parents[3] / "_data" / "article_furniture.yml"


@cache
def load(path: Path = FLAGS) -> dict[str, bool]:
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return {str(k): bool(v) for k, v in data.items()}


def _unchanged(html: str) -> str:
    return html


def flagged(
    name: str, fn: Callable[[str], str], flags: dict[str, bool] | None = None
) -> Callable[[str], str]:
    table = load() if flags is None else flags
    return fn if table.get(name, True) else _unchanged
