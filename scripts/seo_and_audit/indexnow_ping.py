#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Tell IndexNow engines which URLs changed in this deploy (plan B-4).

Bing (and Yandex, Seznam, Naver) accept IndexNow pings; Bing feeds Copilot
and ChatGPT search. After a deploy, this compares the new sitemap with the
previous deploy's (kept as a CI artefact), takes every URL that is new or
whose ``<lastmod>`` changed, and POSTs up to 10,000 of them to
``api.indexnow.org``. It never fails the deploy: a non-2xx answer is logged.

The key comes from the ``INDEXNOW_KEY`` environment variable (a repository
secret); without it the script does nothing. ``write_key_file`` publishes
``public/<key>.txt``, which IndexNow fetches to prove the site owns the key.

    indexnow_ping.py --sitemap public/sitemap.xml --previous prev/sitemap.xml
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.request
from collections.abc import Callable
from pathlib import Path

HOST = "sebastienrousseau.com"
ENDPOINT = "https://api.indexnow.org/indexnow"
MAX_URLS = 10_000
_URL_RE = re.compile(r"<url>\s*<loc>([^<]+)</loc>(?:\s*<lastmod>([^<]*)</lastmod>)?", re.S)
Transport = Callable[[str, bytes], int]


def entries(xml: str) -> dict[str, str]:
    """``{loc: lastmod}`` from a urlset sitemap (lastmod empty when absent)."""
    return {loc.strip(): (mod or "").strip() for loc, mod in _URL_RE.findall(xml)}


def read_entries(path: Path) -> dict[str, str]:
    """Entries of a sitemap, following a sitemap index to its local children."""
    if not path.is_file():
        return {}
    xml = path.read_text(encoding="utf-8")
    if "<sitemapindex" not in xml:
        return entries(xml)
    out: dict[str, str] = {}
    for loc in re.findall(r"<sitemap>\s*<loc>([^<]+)</loc>", xml):
        out.update(read_entries(path.parent / loc.strip().rsplit("/", 1)[-1]))
    return out


def changed(new: dict[str, str], old: dict[str, str]) -> list[str]:
    """URLs that are new, or whose lastmod moved, sorted."""
    return sorted(loc for loc, mod in new.items() if old.get(loc) != mod)


def payload(key: str, urls: list[str]) -> bytes:
    body = {
        "host": HOST,
        "key": key,
        "keyLocation": f"https://{HOST}/{key}.txt",
        "urlList": urls[:MAX_URLS],
    }
    return json.dumps(body).encode("utf-8")


def http_post(url: str, data: bytes) -> int:  # pragma: no cover - network
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json; charset=utf-8"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return int(resp.status)
    except urllib.error.HTTPError as exc:
        return int(exc.code)
    except OSError:
        return 0


def ping(key: str, urls: list[str], post: Transport = http_post) -> int:
    """Send the ping; returns the HTTP status (0 when nothing was sent or the network failed)."""
    if not key or not urls:
        return 0
    return post(ENDPOINT, payload(key, urls))


def write_key_file(public: Path, key: str) -> Path | None:
    if not key:
        return None
    target = public / f"{key}.txt"
    target.write_text(key, encoding="utf-8")
    return target


def main(argv: list[str] | None = None, post: Transport = http_post) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--sitemap", type=Path, required=True)
    parser.add_argument("--previous", type=Path, required=True)
    parser.add_argument("--write-key", type=Path, help="public/ dir: write <key>.txt and exit")
    args = parser.parse_args(argv)
    key = os.environ.get("INDEXNOW_KEY", "").strip()
    if not key:
        print("indexnow: INDEXNOW_KEY unset, skipping")
        return 0
    if args.write_key:
        print(f"indexnow: wrote {write_key_file(args.write_key, key)}")
        return 0
    urls = changed(read_entries(args.sitemap), read_entries(args.previous))
    status = ping(key, urls, post)
    level = "ok" if 200 <= status < 300 else "warning"
    print(
        f"indexnow {level}: {len(urls)} changed URL(s), HTTP {status}",
        file=sys.stdout if level == "ok" else sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
