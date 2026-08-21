#!/usr/bin/env python3
"""Assert the deployed site actually serves what the build produced.

Every gate in this repo runs against ``public/`` on a runner. Nothing checked
the origin afterwards, so a defect introduced between "the build wrote the
file" and "a browser can fetch it" was invisible — and one was, for months:

``actions/upload-pages-artifact`` tars the directory with ``--exclude=.[^/]*``
unless told otherwise, which silently dropped ``public/.well-known/`` from
every deploy. ``/.well-known/security.txt`` (the canonical RFC 9116 location),
``/.well-known/ai.txt`` (advertised by both robots.txt and llms.txt),
``openpgpkey/`` (WKD key discovery) and ``openapi.json`` all returned 404 in
production while sitting correctly in the build output.

This checks the classes of defect that only exist at the origin:

  * every path robots.txt and llms.txt advertise resolves (a site must not
    point crawlers at 404s);
  * the home page carries a hand-authored ``<meta name="description">`` —
    it shipped without one, so Google composed its own snippet for every
    branded query, and the og:description was a scrape of the nav that ended
    mid-sentence on a comma;
  * neither CSP delivery channel (meta tag or edge header) allows
    ``unsafe-inline`` for scripts.

Usage:  python3 scripts/seo_and_audit/verify_deploy.py [--base URL]
"""

from __future__ import annotations

import argparse
import re
import sys
import time
import urllib.error
import urllib.request
from urllib.parse import urljoin

DEFAULT_BASE = "https://sebastienrousseau.com"
TIMEOUT = 30

# A post-deploy probe races the CDN. GitHub Pages answers 200 with the
# PREVIOUS build for a short window after a deploy, so a single fetch can
# assert against content that is already superseded — which is exactly how
# this gate once reported `home page has no <meta name="description">` while
# the live page carried a perfectly good one.
#
# Retrying converts that race into a real signal: a genuine regression still
# fails, because it fails every attempt, while a propagation lag resolves.
RETRIES = 5
RETRY_DELAY = 20
_UA = "sebastienrousseau.com-deploy-verifier/1.0"

# Paths that must resolve regardless of what robots.txt happens to name.
REQUIRED_PATHS = (
    "/",
    "/robots.txt",
    "/sitemap.xml",
    "/llms.txt",
    "/.well-known/security.txt",
    "/.well-known/ai.txt",
)

_SITEMAP_LINE_RE = re.compile(r"^Sitemap:\s*(\S+)", re.MULTILINE | re.IGNORECASE)
_ADVERTISED_URL_RE = re.compile(r"https://[^\s\)\]<>\"]+")
_META_DESC_RE = re.compile(
    r'<meta\b[^>]*\bname="description"[^>]*\bcontent="([^"]*)"', re.IGNORECASE
)
_SCRIPT_SRC_RE = re.compile(r"script-src[^;]*", re.IGNORECASE)


class Failure(Exception):
    """A deployed-site assertion that did not hold."""


def fetch(url: str) -> tuple[int, str, dict[str, str]]:
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return resp.status, body, {k.lower(): v for k, v in resp.headers.items()}
    except urllib.error.HTTPError as exc:
        return exc.code, "", {k.lower(): v for k, v in (exc.headers or {}).items()}
    except (urllib.error.URLError, TimeoutError) as exc:
        raise Failure(f"{url}: unreachable ({exc})") from exc


def advertised_paths(base: str) -> set[str]:
    """Every URL robots.txt and llms.txt point at, as absolute URLs."""
    found: set[str] = set()
    for source in ("/robots.txt", "/llms.txt"):
        status, body, _ = fetch(urljoin(base, source))
        if status != 200:
            raise Failure(f"{source}: HTTP {status}")
        if source.endswith("robots.txt"):
            found.update(_SITEMAP_LINE_RE.findall(body))
            # Commented pointers in robots.txt are documentation, but a
            # documented 404 is still a broken promise to a crawler.
            found.update(
                m
                for line in body.splitlines()
                if line.lstrip().startswith("#")
                for m in _ADVERTISED_URL_RE.findall(line)
            )
        else:
            found.update(_ADVERTISED_URL_RE.findall(body))
    return {u for u in found if u.startswith(base)}


def check_paths(base: str, paths: set[str]) -> list[str]:
    problems = []
    for url in sorted(paths):
        status, _, _ = fetch(url)
        if status != 200:
            problems.append(f"{url} -> HTTP {status}")
    return problems


def check_home_description(base: str) -> list[str]:
    status, body, _ = fetch(base if base.endswith("/") else base + "/")
    if status != 200:
        return [f"home page -> HTTP {status}"]
    m = _META_DESC_RE.search(body)
    if not m:
        return ['home page has no <meta name="description">']
    desc = m.group(1).strip()
    problems = []
    if len(desc) < 50:
        problems.append(f"home meta description is only {len(desc)} chars: {desc!r}")
    if desc.rstrip().endswith((",", ";", ":")):
        problems.append(f"home meta description ends mid-sentence: {desc[-60:]!r}")
    return problems


def check_csp(base: str) -> list[str]:
    status, body, headers = fetch(base if base.endswith("/") else base + "/")
    if status != 200:
        return [f"home page -> HTTP {status}"]
    problems = []
    header_csp = headers.get("content-security-policy", "")
    if header_csp:
        script_src = _SCRIPT_SRC_RE.search(header_csp)
        if script_src and "'unsafe-inline'" in script_src.group(0):
            problems.append("edge CSP header allows 'unsafe-inline' in script-src")
    meta = re.search(
        r'<meta\b[^>]*http-equiv="Content-Security-Policy"[^>]*content="([^"]*)"',
        body,
        re.IGNORECASE | re.DOTALL,
    )
    if meta:
        script_src = _SCRIPT_SRC_RE.search(meta.group(1))
        if script_src and "'unsafe-inline'" in script_src.group(0):
            problems.append("meta CSP allows 'unsafe-inline' in script-src")
    elif not header_csp:
        problems.append("no Content-Security-Policy delivered by header or meta")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default=DEFAULT_BASE, help="origin to verify")
    parser.add_argument(
        "--skip-csp",
        action="store_true",
        help="skip the CSP assertions (edge headers are not applied on a bare origin)",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=RETRIES,
        help="attempts before a problem is treated as real (default: %(default)s)",
    )
    parser.add_argument(
        "--retry-delay",
        type=int,
        default=RETRY_DELAY,
        help="seconds between attempts (default: %(default)s)",
    )
    args = parser.parse_args(argv)
    base = args.base.rstrip("/")

    attempts = max(1, args.retries)
    problems: list[str] = []
    paths: set[str] = set()
    for attempt in range(1, attempts + 1):
        problems = []
        try:
            paths = {urljoin(base + "/", p) for p in REQUIRED_PATHS} | advertised_paths(base)
            problems += check_paths(base, paths)
            problems += check_home_description(base)
            if not args.skip_csp:
                problems += check_csp(base)
        except Failure as exc:
            problems = [str(exc)]
        if not problems:
            break
        if attempt < attempts:
            print(
                f"verify_deploy: {len(problems)} problem(s) on attempt "
                f"{attempt}/{attempts}; the origin may still be serving the "
                f"previous build — retrying in {args.retry_delay}s",
                file=sys.stderr,
            )
            time.sleep(args.retry_delay)

    if problems:
        print(
            f"verify_deploy: {len(problems)} problem(s) against {base} after {attempts} attempt(s)",
            file=sys.stderr,
        )
        for p in problems:
            print(f"  ::error::{p}", file=sys.stderr)
        return 1
    print(f"verify_deploy: OK — {len(paths)} advertised paths resolve against {base}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
