# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""One place that decides what "today" means during a build.

A page that stamps the wall clock cannot be rebuilt byte-identically. The
`Reproducible build` CI job builds twice and diffs, and it caught this the
only way it could — by chance. Run 33281416595 built from 23:37:39Z to
00:09:41Z, straddling midnight, so the first build stamped 2026-08-29 and
the second stamped 2026-08-30. Every page carrying a build-time date
differed. The same branch had passed the same job twice earlier that day;
nothing about the code had changed, only the hour it ran at.

The affected pages are the ones with no `last_reviewed` in frontmatter —
category, topic, case-study and speaking listings — which fall back to
today's date. Articles carry a real reviewed date and were unaffected.

`SOURCE_DATE_EPOCH` is the reproducible-builds.org convention for pinning
a build's idea of now. When it is set, every date the build stamps comes
from it, so two builds of the same commit agree no matter when they run.
When it is unset — every normal build — behaviour is unchanged.

A malformed value raises rather than falling back to the wall clock: a
typo in CI would otherwise silently restore the flake this exists to fix.
"""

from __future__ import annotations

import os
from datetime import UTC, date, datetime

__all__ = ["build_now", "build_today", "build_today_iso"]

_ENV = "SOURCE_DATE_EPOCH"


def build_now() -> datetime:
    """Timezone-aware 'now', pinned by SOURCE_DATE_EPOCH when it is set."""
    raw = os.environ.get(_ENV)
    if raw is None or raw == "":
        return datetime.now(UTC)
    try:
        return datetime.fromtimestamp(int(raw), tz=UTC)
    except (ValueError, OverflowError, OSError) as exc:
        raise ValueError(f"{_ENV} is not a valid Unix timestamp: {raw!r}") from exc


def build_today() -> date:
    """Today's date, pinned by SOURCE_DATE_EPOCH when it is set."""
    return build_now().date()


def build_today_iso() -> str:
    """`build_today()` as YYYY-MM-DD — the form every call site stamps."""
    return build_today().isoformat()
