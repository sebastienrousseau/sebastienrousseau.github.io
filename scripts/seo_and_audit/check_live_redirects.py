#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Probe the live site: renamed URLs answer one permanent redirect.

The lang-router Worker answers every source in
``worker-assets/redirects.json`` with a 301 to its final URL before origin
is touched. ``check_redirect_map.py`` proves the committed map matches the
build; this proves the deployed Worker actually serves it. A 302, a 200
(the meta-refresh stub served from origin, meaning the Worker or its
assets binding is missing) or a Location other than the mapped target all
fail.

It runs against the public hostname, so it belongs after a Worker deploy,
not in the Pages deploy job: ``verify_deploy.py`` probes the Pages origin,
where the Worker never runs. It sends ``--sample`` HEAD requests (20 by
default), one at a time with a pause between them, and never follows a
redirect. The sample is spread evenly over the sorted map; ``--seed``
rotates the starting point (default: today's date), so successive runs
cover different entries and any run can be repeated exactly.

Usage: ``python3 scripts/seo_and_audit/check_live_redirects.py [--base URL]``
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import time
import urllib.error
import urllib.request
from email.message import Message
from pathlib import Path
from typing import IO, Protocol
from urllib.parse import quote, unquote

ROOT = Path(__file__).resolve().parents[2]
MAP = ROOT / "worker-assets" / "redirects.json"
DEFAULT_BASE = "https://sebastienrousseau.com"
SAMPLE = 20
DELAY = 1.0
TIMEOUT = 20
_UA = "sebastienrousseau.com-live-content-check/1.0"


class Opener(Protocol):
    def open(self, fullurl: urllib.request.Request, /, *, timeout: float = ...) -> object:
        """Fetch ``fullurl`` without following redirects."""


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Surface every 3xx as an ``HTTPError`` instead of following it."""

    def redirect_request(
        self,
        req: urllib.request.Request,
        fp: IO[bytes] | None,
        code: int,
        msg: str,
        headers: Message,
        newurl: str,
    ) -> None:
        return None


def build_opener() -> urllib.request.OpenerDirector:
    return urllib.request.build_opener(NoRedirect())


def sample(sources: list[str], k: int, seed: int) -> list[str]:
    """``k`` sources spread evenly over ``sorted(sources)``, rotated by seed."""
    ordered = sorted(sources)
    n = len(ordered)
    if n <= k:
        return ordered
    step = n / k
    offset = seed % max(1, int(step))
    return [ordered[(offset + int(i * step)) % n] for i in range(k)]


def probe(url: str, opener: Opener) -> tuple[int, str | None]:
    """``(status, Location)`` of one HEAD request, redirects not followed."""
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": _UA})
    try:
        opener.open(req, timeout=TIMEOUT)
    except urllib.error.HTTPError as exc:
        return exc.code, exc.headers.get("Location")
    return 200, None


def check_redirect(base: str, source: str, target: str, opener: Opener) -> str | None:
    """None when ``source`` answers a 301 straight to ``target``."""
    url = base + quote(source, safe="/")
    try:
        status, location = probe(url, opener)
    except (urllib.error.URLError, TimeoutError) as exc:
        return f"{url}: unreachable ({exc})"
    if status != 301:
        return f"{url}: HTTP {status}, expected 301"
    want = base + target
    if unquote(location or "") != want:
        return f"{url}: 301 to {location}, expected {want}"
    return None


def _parse(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base", default=DEFAULT_BASE)
    parser.add_argument("--map", type=Path, default=MAP)
    parser.add_argument("--sample", type=int, default=SAMPLE)
    parser.add_argument("--seed", type=int, default=dt.date.today().toordinal())
    parser.add_argument("--delay", type=float, default=DELAY, help="seconds between requests")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse(argv)
    base = args.base.rstrip("/")
    redirects: dict[str, str] = json.loads(args.map.read_text(encoding="utf-8"))["redirects"]
    picks = sample(list(redirects), args.sample, args.seed)
    opener = build_opener()
    problems = []
    for i, source in enumerate(picks):
        if i:
            time.sleep(args.delay)
        problem = check_redirect(base, source, redirects[source], opener)
        if problem:
            problems.append(problem)
    if problems:
        print(f"check_live_redirects: {len(problems)} of {len(picks)} failed", file=sys.stderr)
        for p in problems:
            print(f"  ::error::{p}", file=sys.stderr)
        return 1
    print(
        f"check_live_redirects: OK: {len(picks)} sampled renamed URLs answer one 301 (seed {args.seed})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
