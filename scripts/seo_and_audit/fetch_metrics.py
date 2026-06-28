#!/usr/bin/env python3
"""Fetch authority-proof metrics at build time and write
``_data/proof/metrics.json`` so the homepage + case-study templates
can render aggregate-not-vanity numbers.

Authority is conferred, not claimed. Every number this script emits is
either (a) externally verifiable via the URL recorded next to it, or
(b) derived from the local archive (article count, years active). We
never invent adopter counts. If a remote fetch errors, we fall back to
the last committed `_data/proof/metrics.json` rather than ship zeros —
better stale than fabricated.

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
          "source": "pypistats.org + crates.io"
        },
        ...
      ]
    }
"""

from __future__ import annotations

import datetime as _dt
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_PATH = ROOT / "_data" / "proof" / "metrics.json"

# Pinned PyPI package list — pypistats has no per-account rollup, so we
# enumerate. Adding a package means: add the slug here, ensure it's live.
PYPI_PACKAGES = (
    "pain001",
    "bankstatementparser",
    "pacs008",
)
# crates.io downloads are summed across EVERY crate owned by the account
# (discovered via the users endpoint), so serde_yml and libyml — which
# dominate the total at ~18M each — are never missed. No hand-maintained
# crate list to drift out of date.
GITHUB_USER = "sebastienrousseau"
CRATES_USER = "sebastienrousseau"

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


def _pypi_downloads(pkg: str) -> int:
    """Return last-month downloads from pypistats.org (a free public API
    backed by Linehan Software with no key). 0 on fetch failure."""
    data = _http_get_json(f"https://pypistats.org/api/packages/{pkg}/recent")
    if not data:
        return 0
    return int(data.get("data", {}).get("last_month") or 0)


def _crates_downloads_all() -> int:
    """Sum all-time downloads across every crate owned by the account.

    Resolves the account's numeric user id, then lists their crates and
    sums each crate's all-time download count. 0 on any fetch failure so
    `_max_value` falls back to the last committed total."""
    user = _http_get_json(f"https://crates.io/api/v1/users/{CRATES_USER}")
    uid = (user or {}).get("user", {}).get("id")
    if not uid:
        return 0
    data = _http_get_json(
        f"https://crates.io/api/v1/crates?user_id={uid}&per_page=100"
    )
    if not data:
        return 0
    return sum(int(c.get("downloads") or 0) for c in data.get("crates", []))


def _github_repos() -> tuple[int, int]:
    """Sum stars + forks across the user's repos. (0, 0) on failure."""
    data = _http_get_json(
        f"https://api.github.com/users/{GITHUB_USER}/repos"
        f"?per_page=100&type=owner&sort=updated"
    )
    if not isinstance(data, list):
        return 0, 0
    stars = sum(int(r.get("stargazers_count") or 0) for r in data)
    forks = sum(int(r.get("forks_count") or 0) for r in data)
    return stars, forks


def _articles_count() -> int:
    """Count dated _posts/*.md — local, never fails."""
    return sum(
        1 for p in (ROOT / "_posts").glob("*.md")
        if p.name[:4].isdigit() and "-" in p.name[4:5]
    )


def _years_active() -> int:
    """Earliest dated post is 2018-01-01 — use that as 'years writing'.
    Earliest commercial role started 2007 (per About page) — use that
    as 'years in payments / banking technology'."""
    return _dt.date.today().year - 2007


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


def _max_value(key: str, computed: int, fallback: dict) -> int:
    """Return whichever is higher: this run's computed value or the
    previously committed value. Prevents a flaky API regressing a real
    number to zero on a single bad poll."""
    for stat in fallback.get("stats", []):
        if stat.get("key") == key:
            previous = int(stat.get("value") or 0)
            return max(computed, previous)
    return computed


def main() -> int:
    fallback = _load_existing()

    pypi_total = sum(_pypi_downloads(p) for p in PYPI_PACKAGES)
    crates_total = _crates_downloads_all()
    downloads_total = _max_value("downloads_total", pypi_total + crates_total, fallback)

    stars, forks = _github_repos()
    stars_total = _max_value("github_stars", stars, fallback)
    forks_total = _max_value("github_forks", forks, fallback)

    articles = _articles_count()
    years_payments = _years_active()

    payload = {
        "$generated_at": _dt.datetime.now(tz=_dt.UTC).isoformat(timespec="seconds"),
        "stats": [
            {
                "key": "years_payments",
                "label": "Years in payments and banking technology",
                "value": years_payments,
                "format": "plain",
                "source": "About page — HSBC / PayPal / Barclays / Shazam / AKQA / Virgin Group",
            },
            {
                "key": "articles_signed",
                "label": "Signed, dated articles published",
                "value": articles,
                "format": "plain",
                "source": "_posts/ — every article Sigstore-signed",
            },
            {
                "key": "downloads_total",
                "label": "Open-source package downloads (PyPI + crates.io)",
                "value": downloads_total,
                "format": "compact",
                "source": "pypistats.org + crates.io",
            },
            {
                "key": "github_stars",
                "label": "GitHub stars across owned repositories",
                "value": stars_total,
                "format": "compact",
                "source": "api.github.com/users/sebastienrousseau/repos",
            },
            {
                "key": "github_forks",
                "label": "GitHub forks across owned repositories",
                "value": forks_total,
                "format": "compact",
                "source": "api.github.com/users/sebastienrousseau/repos",
            },
        ],
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    summary = "  ".join(
        f"{s['key']}={s['value']}" for s in payload["stats"]
    )
    print(f"fetch_metrics: {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
