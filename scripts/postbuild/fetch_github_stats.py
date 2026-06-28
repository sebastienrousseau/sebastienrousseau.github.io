#!/usr/bin/env python3
"""Fetch per-repository GitHub stats and persist to ``public/_data/gh-stats.json``.

Build-time fetch beats an Edge Function for a static site: same freshness
on a nightly cron, zero runtime cost, no API rate-limit risk on the
request path. The output JSON is consumed by ``scripts/postbuild.py``
which injects the values into project cards before the page is written.

Runs in CI on a nightly schedule (``.github/workflows/refresh-gh-stats.yml``)
and on every push that touches ``scripts/fetch_github_stats.py``.

Auth: reads ``GH_TOKEN`` env var if set (raises the rate limit from 60
to 5000 requests/hour and surfaces private-repo metadata where
permission has been granted). Unauthenticated requests work for public
repos but are rate-limited.

Failure mode: if the API call fails for any repo, keep the previously
cached value so the build doesn't fail. Only repos with FRESH data get
updated. Stale data is logged but tolerated.
"""

from __future__ import annotations

import sys as _sys  # path bootstrap — scripts reorg (scripts/lib/ on sys.path)
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "lib"))

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

# Canonical list of repos to track. Order matters only for the report
# at the end of the run.
REPOS: tuple[str, ...] = (
    "sebastienrousseau/pain001",
    "sebastienrousseau/pacs008",
    "sebastienrousseau/bankstatementparser",
    "sebastienrousseau/nalufx",
    "sebastienrousseau/qrc",
    "sebastienrousseau/kyberlib",
    "sebastienrousseau/hsh",
    "sebastienrousseau/cmn",
    "sebastienrousseau/dtt",
    "sebastienrousseau/libmake",
    "sebastienrousseau/rlg",
    "sebastienrousseau/static-site-generator",
    "sebastienrousseau/euxis",
    "sebastienrousseau/noyalib",
    "sebastienrousseau/serde_yml",
    "sebastienrousseau/crypto-service",
    "sebastienrousseau/kaishi.github.io",
    "sebastienrousseau/skeletonic-stylus",
    "sebastienrousseau/dotfiles",
    "sebastienrousseau/vrd",
    "sebastienrousseau/mini-functions",
)

OUTPUT = Path("_data/gh-stats.json")
API = "https://api.github.com"
USER_AGENT = "sebastienrousseau.com/build (https://github.com/sebastienrousseau)"


def fetch_repo(slug: str, token: str | None) -> dict | None:
    """Hit /repos/{owner}/{name} and return a slim dict, or None on
    failure. Network errors are logged to stderr but don't abort."""
    url = f"{API}/repos/{slug}"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": USER_AGENT,
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"  ✗ {slug}: HTTP {e.code} — {e.reason}", file=sys.stderr)
        return None
    except urllib.error.URLError as e:
        print(f"  ✗ {slug}: {e.reason}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  ✗ {slug}: {e}", file=sys.stderr)
        return None

    return {
        "slug": slug,
        "name": data.get("name", ""),
        "description": data.get("description", "") or "",
        "homepage": data.get("homepage", "") or "",
        "stars": data.get("stargazers_count", 0),
        "forks": data.get("forks_count", 0),
        "watchers": data.get("subscribers_count", 0),
        "open_issues": data.get("open_issues_count", 0),
        "language": data.get("language", "") or "",
        "license": (data.get("license") or {}).get("spdx_id") or "",
        "default_branch": data.get("default_branch", "main"),
        "pushed_at": data.get("pushed_at", ""),
        "created_at": data.get("created_at", ""),
        "archived": bool(data.get("archived", False)),
        "html_url": data.get("html_url", f"https://github.com/{slug}"),
    }


def load_existing() -> dict[str, dict]:
    if not OUTPUT.is_file():
        return {}
    try:
        data = json.loads(OUTPUT.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return {entry["slug"]: entry for entry in data.get("repos", []) if "slug" in entry}


def main() -> int:
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        print("warn: no GH_TOKEN — unauthenticated, 60 req/hour limit", file=sys.stderr)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    existing = load_existing()
    fresh: dict[str, dict] = {}
    failed: list[str] = []

    # Network-bound — fan out across a thread pool. GH API tolerates 10
    # concurrent requests from a single client comfortably; this brings
    # the total runtime down from N × (slowest-round-trip) to roughly
    # one slowest-round-trip.
    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor(max_workers=10) as pool:
        results = list(pool.map(lambda s: (s, fetch_repo(s, token)), REPOS))

    for slug, info in results:
        if info:
            fresh[slug] = info
        elif slug in existing:
            # Keep last-known data so the build doesn't lose information.
            fresh[slug] = existing[slug]
            fresh[slug]["stale"] = True
            failed.append(slug)
        else:
            failed.append(slug)

    payload = {
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "repos": [fresh[slug] for slug in REPOS if slug in fresh],
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    total_stars = sum(r.get("stars", 0) for r in payload["repos"])
    total_forks = sum(r.get("forks", 0) for r in payload["repos"])
    print(
        f"fetch_github_stats: wrote {len(payload['repos'])} repo(s), "
        f"{total_stars} stars, {total_forks} forks "
        f"({len(failed)} failed)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
