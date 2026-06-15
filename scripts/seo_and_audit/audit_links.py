#!/usr/bin/env python3
"""Audit every <a href> inside built HTML pages.

Internal links (absolute paths starting with '/') are resolved against ``public/``
and verified to point at an existing file. External links can optionally be HEAD-
or GET-checked against the live origin; HEAD-blocking hosts are auto-skipped.

Exit code is non-zero if --strict-internal is set and any internal link is broken.
"""

from __future__ import annotations

import sys as _sys  # path bootstrap — scripts reorg (scripts/lib/ on sys.path)
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "lib"))

import argparse
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HEAD_BLOCKED = {
    "twitter.com",
    "x.com",
    "linkedin.com",
    "www.linkedin.com",
    "medium.com",
    "crates.io",
    "midjourney.com",
    "www.midjourney.com",
    "spglobal.com",
    "www.spglobal.com",
    "news.bankingonquantum.com",
    "www.bmo.com",
    "chat.mistral.ai",
    "www.iso20022.org",
    "iso20022.org",
    "huggingface.co",
    "ai.google.dev",
    "www.hsbc.com",
}

# Routes that the consolidated workers/lang-router.js handles at request
# time (WS5+ scope) — no static asset exists for them in public/, so the
# strict-internal audit must not treat them as broken. They're served by
# the Edge Worker; the WS5 PR adds the route handlers + a smoke test for
# each. See ~/Drop/editorial-overhaul-plan.md §4 WS5/WS6.
WORKER_ROUTES: tuple[str, ...] = (
    "/api/pdf/",
    "/api/webmention",
    "/mcp/v1/",
)


def collect_hrefs(public: Path) -> set[str]:
    pat = re.compile(r'href="([^"#?]+)(?:[#?][^"]*)?"|href=([^ >#?]+)(?:[#?][^ >]*)?')
    links: set[str] = set()
    for html in public.rglob("*.html"):
        for a, b in pat.findall(html.read_text(errors="ignore")):
            h = a or b
            if not h or h.startswith(("mailto:", "tel:", "javascript:", "data:")):
                continue
            links.add(h)
    return links


def check_internal(href: str, public: Path) -> bool:
    if not href.startswith("/"):
        return True  # leave non-absolute alone here
    if any(href.startswith(p) for p in WORKER_ROUTES):
        return True  # served by lang-router worker at request time
    target = public / href.lstrip("/")
    if target.is_file():
        return True
    # Common static-site convention: /foo/ → /foo/index.html
    if target.is_dir() and (target / "index.html").is_file():
        return True
    return bool(target.with_suffix(".html").is_file())


def check_external(url: str) -> tuple[str, int | str]:
    try:
        req = urllib.request.Request(
            url,
            method="HEAD",
            headers={"User-Agent": "Mozilla/5.0 audit_links"},
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            return url, r.status
    except urllib.error.HTTPError as e:
        return url, e.code
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as e:
        return url, f"ERR {type(e).__name__}"


def host(url: str) -> str:
    return url.split("/", 3)[2] if "://" in url else url


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-dir", default="public")
    ap.add_argument("--strict-internal", action="store_true")
    ap.add_argument("--check-external", action="store_true")
    args = ap.parse_args()

    public = Path(args.base_dir)
    hrefs = collect_hrefs(public)
    internal = sorted(h for h in hrefs if h.startswith("/"))
    external = sorted(
        h for h in hrefs if h.startswith(("http://", "https://")) and "127.0.0.1" not in h
    )

    int_broken = [h for h in internal if not check_internal(h, public)]
    print(f"internal: {len(internal):4d} checked, {len(int_broken)} broken")
    for h in int_broken:
        print(f"  [missing] {h}")

    ext_broken: list[tuple[str, int | str]] = []
    if args.check_external:
        checkable = [u for u in external if host(u) not in HEAD_BLOCKED]
        with ThreadPoolExecutor(max_workers=12) as ex:
            for url, code in ex.map(check_external, checkable):
                if not (isinstance(code, int) and 200 <= code < 400):
                    ext_broken.append((url, code))
        print(
            f"external: {len(checkable):4d} checked (skipped {len(external) - len(checkable)} bot-blocked), {len(ext_broken)} broken"
        )
        for url, code in sorted(ext_broken):
            print(f"  [{code}] {url}")

    if args.strict_internal and int_broken:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
