# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""scripts/seo_and_audit/cadence_check.py: crowded weeks."""

from __future__ import annotations

import datetime as dt

import cadence_check as cc


def test_weeks_over_the_limit_are_reported() -> None:
    names = [
        "2026-10-12-a.md", "2026-10-13-b.md", "2026-10-13-c.md",  # 2026-W42, three
        "2026-10-20-d.md", "2026-10-21-e.md",  # W43, two
        "2025-01-01-old.md", "about.md",
    ]  # fmt: skip
    assert cc.crowded_weeks(names, dt.date(2026, 1, 1)) == {
        "2026-W42": ["2026-10-12-a", "2026-10-13-b", "2026-10-13-c"]
    }


def test_main_never_fails() -> None:
    assert cc.main(["--since", "2026-01-01"]) == 0
