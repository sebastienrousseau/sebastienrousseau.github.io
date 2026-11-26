#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Fetch authority-proof metrics at build time and write
``_data/proof/metrics.json`` so the homepage + case-study templates
can render aggregate-not-vanity numbers.

Authority is conferred, not claimed. Every number this script emits is
either (a) externally verifiable via the URL recorded next to it, or
(b) derived from the local archive (article count, years active). We
never invent adopter counts. Downloads, stars and packages come from the
GitHub profile's profile.json, so both pages agree. If a remote fetch
errors, we fall back to the last committed `_data/proof/metrics.json`
rather than ship zeros: better stale than fabricated.

Run from repo root::

    python3 scripts/seo_and_audit/fetch_metrics.py

Pipeline-friendly: prints a one-line summary on stdout, exits 0 even
when individual fetches fail (graceful degradation), exits non-zero
only on a structural error.

The JSON shape is stable so the template doesn't need to know which
sub-fetch succeeded::

    {
      "$generated_at": "2026-06-16T17:42:00Z",
      "stats": [
        {
          "key":   "downloads_total",
          "label": "Package downloads",
          "value": 12345,
          "format": "compact",
          "source": "github.com/sebastienrousseau/sebastienrousseau (profile.json)"
        },
        ...
      ]
    }
"""

from __future__ import annotations

import datetime as _dt
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
import _profile

OUT_PATH = ROOT / "_data" / "proof" / "metrics.json"

# The four headline figures (all-time downloads, the last 30 days, GitHub
# stars, packages published) come from the GitHub profile's profile.json,
# which tools/metrics.py in sebastienrousseau/sebastienrousseau refreshes
# every three hours from crates.io, PyPI (clickpy) and npm. One pipeline
# for both pages, so the homepage and the profile show the same numbers.
# This script used to count them itself: PyPI last-month downloads for
# three pinned packages added to crates.io all-time totals for the first
# 100 crates, no npm, and max() against the snapshot, which froze the
# 30-day figure at 3.7M and the package count at 179.
PROFILE_JSON_URL = (
    "https://raw.githubusercontent.com/sebastienrousseau/sebastienrousseau/"
    "profile-data/profile.json"
)
PROFILE_KEYS = ("all_time_downloads", "recent_downloads", "github_stars", "packages")
# metrics.json key -> profile.json numbers key, for the four shared figures.
PROFILE_PAIRS = {
    "downloads_total": "all_time_downloads",
    "downloads_30d": "recent_downloads",
    "github_stars": "github_stars",
    "packages_published": "packages",
}
# A printed figure from the profile's numbers panel: "54.8M", "2.5M", "758".
_FIGURE_RE = re.compile(r"^\d{1,9}(\.\d)?[KM]?$")
GITHUB_USER = "sebastienrousseau"

_TIMEOUT = 10
_HEADERS = {"User-Agent": "sebastienrousseau-site-build/1.0"}


def _http_get_json(url: str) -> dict | None:
    """GET ``url``, parse JSON. Returns None on any failure (network,
    HTTP non-200, malformed JSON). Caller decides whether to fall back."""
    try:
        req = urllib.request.Request(url, headers=_HEADERS)
        with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:
            if resp.status != 200:
                return None
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, OSError, ValueError):
        return None


def _profile_numbers() -> dict | None:
    """The profile's ``numbers`` block, or None unless every figure is a
    positive integer, so a half-written file never reaches the page."""
    numbers = (_http_get_json(PROFILE_JSON_URL) or {}).get("numbers")
    if not isinstance(numbers, dict):
        return None
    for key in PROFILE_KEYS:
        value = numbers.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            return None
    return numbers


def _github_forks() -> int:
    """Forks across the user's owned non-fork repos, all pages."""
    forks = 0
    for page in range(1, 11):
        data = _http_get_json(
            f"https://api.github.com/users/{GITHUB_USER}/repos?per_page=100&type=owner&sort=updated&page={page}"
        )
        if not isinstance(data, list) or not data:
            break
        forks += sum(int(r.get("forks_count") or 0) for r in data if not r.get("fork"))
        if len(data) < 100:
            break
    return forks


def _articles_count() -> int:
    """Count dated _posts/*.md — local, never fails."""
    return sum(
        1 for p in (ROOT / "_posts").glob("*.md") if p.name[:4].isdigit() and "-" in p.name[4:5]
    )


def _years_active() -> str:
    """The experience figure ("20+") from _data/profile.yml. It used to
    count from 2007, a start year the career history does not support,
    and printed 19 beside copy that said "20+"."""
    return _profile.experience_figure()


def _format_compact(n: int) -> str:
    """Convert 12345 → '12.3K', 1234567 → '1.2M' etc.
    Used by the template helper if it can't run formatting itself."""
    if n < 1_000:
        return str(n)
    if n < 1_000_000:
        return f"{n / 1_000:.1f}K".replace(".0K", "K")
    return f"{n / 1_000_000:.1f}M".replace(".0M", "M")


def _load_existing() -> dict:
    """Read the previously committed metrics.json so we can fall back
    when fetches fail. Returns an empty dict when the file doesn't
    exist yet (first run)."""
    if not OUT_PATH.is_file():
        return {}
    try:
        return json.loads(OUT_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _previous(key: str, fallback: dict) -> int:
    """The committed snapshot's value for ``key``, 0 when it has none."""
    for stat in fallback.get("stats", []):
        if stat.get("key") == key:
            return int(stat.get("value") or 0)
    return 0


def _max_value(key: str, computed: int, fallback: dict) -> int:
    """Return whichever is higher: this run's computed value or the
    previously committed value. Prevents a flaky API regressing a real
    number to zero on a single bad poll. Forks only: the profile figures
    are taken as they are, since a 30-day window falls as well as rises."""
    return max(computed, _previous(key, fallback))


def _display_strings(numbers: dict) -> dict[str, str]:
    """The profile's printed figures (``numbers.display``), keyed as
    metrics.json names them; {} unless all four look like figures."""
    display = numbers.get("display")
    if not isinstance(display, dict):
        return {}
    out: dict[str, str] = {}
    for ours, theirs in PROFILE_PAIRS.items():
        value = display.get(theirs)
        if not isinstance(value, str) or not _FIGURE_RE.match(value):
            return {}
        out[ours] = value
    return out


def _previous_display(fallback: dict) -> dict[str, str]:
    """The committed snapshot's printed figures for the shared keys."""
    return {
        s["key"]: s["display"]
        for s in fallback.get("stats", [])
        if s.get("key") in PROFILE_PAIRS and isinstance(s.get("display"), str)
    }


def _headline_figures(fallback: dict) -> tuple[dict[str, int], dict[str, str]]:
    """The four profile figures and their printed forms, keyed as
    metrics.json names them; the committed snapshot's when profile.json
    cannot be read."""
    numbers = _profile_numbers()
    if numbers is None:
        print("fetch_metrics: profile.json unreadable, keeping the committed figures")
        figures = {ours: _previous(ours, fallback) for ours in PROFILE_PAIRS}
        return figures, _previous_display(fallback)
    figures = {ours: numbers[theirs] for ours, theirs in PROFILE_PAIRS.items()}
    return figures, _display_strings(numbers)


# Opt out of the network fetch and keep the committed snapshot.
#
# Set by the reproducible-build CI job, which builds twice and requires
# byte-identical output. Every number below is fetched live, so the two
# builds saw different values whenever a counter moved between them —
# github_stars and github_forks render in `plain` format, so a single
# star was enough. That rewrote the KPI figure on /, /about/, /projects/
# and /speaking/ plus all 34 locale forks, and search-index.json with
# them, failing a job whose stated purpose is to catch a build pass that
# is not idempotent. It was measuring the network, not the build.
SKIP_ENV = "SKIP_METRICS_FETCH"


_PROFILE_SOURCE = "github.com/sebastienrousseau/sebastienrousseau (profile.json)"
# key, label, format, source: the order metrics.json lists its stats in.
_STATS = (
    (
        "years_payments",
        "Years in payments, banking and digital technology",
        "plain",
        "_data/profile.yml (experience_phrase)",
    ),
    (
        "articles_signed",
        "Signed, dated articles published",
        "plain",
        "_posts/: every article Sigstore-signed",
    ),
    (
        "downloads_total",
        "All-time open-source package downloads (crates.io + PyPI + npm)",
        "compact",
        _PROFILE_SOURCE,
    ),
    (
        "downloads_30d",
        "Downloads in the last 30 days (crates.io + PyPI + npm)",
        "compact",
        _PROFILE_SOURCE,
    ),
    ("github_stars", "GitHub stars across owned repositories", "compact", _PROFILE_SOURCE),
    (
        "packages_published",
        "Packages published across crates.io, PyPI, and npm",
        "compact",
        _PROFILE_SOURCE,
    ),
    (
        "github_forks",
        "GitHub forks across owned repositories",
        "compact",
        "api.github.com/users/sebastienrousseau/repos",
    ),
)


def _stats(values: dict[str, object], display: dict[str, str]) -> list[dict[str, object]]:
    """metrics.json's stats. The profile's printed form travels with each
    shared figure, so the build prints exactly what the profile prints."""
    stats: list[dict[str, object]] = []
    for key, label, fmt, source in _STATS:
        stat: dict[str, object] = {
            "key": key,
            "label": label,
            "value": values[key],
            "format": fmt,
            "source": source,
        }
        if key in display:
            stat["display"] = display[key]
        stats.append(stat)
    return stats


def _keep_snapshot() -> int:
    """SKIP_ENV path: leave the committed snapshot as it is."""
    existing = _load_existing()
    if not existing:
        print(f"fetch_metrics: {SKIP_ENV} set but no committed snapshot, nothing to keep")
        return 0
    summary = "  ".join(f"{s['key']}={s['value']}" for s in existing.get("stats", []))
    print(f"fetch_metrics: {SKIP_ENV} set, keeping committed snapshot  {summary}")
    return 0


def main() -> int:
    if os.environ.get(SKIP_ENV):
        return _keep_snapshot()

    fallback = _load_existing()
    figures, display = _headline_figures(fallback)
    values: dict[str, object] = {
        **figures,
        "github_forks": _max_value("github_forks", _github_forks(), fallback),
        "articles_signed": _articles_count(),
        "years_payments": _years_active(),
    }
    stats = _stats(values, display)
    payload = {
        "$generated_at": _dt.datetime.now(tz=_dt.UTC).isoformat(timespec="seconds"),
        "stats": stats,
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    summary = "  ".join(f"{s['key']}={s['value']}" for s in stats)
    print(f"fetch_metrics: {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
