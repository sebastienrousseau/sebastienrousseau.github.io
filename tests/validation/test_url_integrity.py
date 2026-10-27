#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""No post may contain a URL the translation pipeline has rewritten.

Translating an article translated words *inside* its URLs. 73 URLs across 18
posts in hi, it, pt-br and nl had been rewritten this way and shipped:

    en.wikipedia.org        -> em.wikipedia.org, in.wikipedia.org
    devblogs.microsoft.com  -> devblogs.microsvaak.com
    web.archive.org/web/    -> xn--p2br8c.archive.org/वेब/
    andrea-de-santis-*.webp -> andrea-का-santis-*.webp   (a broken image)
    csrc.nist.gov/…/final   -> csrc.nist.gov/…/अंतिम
    sebastienrousseau.com/2018-01-24-the-erc-20-token-standard/
                            -> …-the-erc-20-टोकन-standard/   (a broken internal link)

It went unnoticed because the external link audit is not part of CI — it
needs RUN_NETWORK_TESTS=1 — and when run it aborted on the first malformed
URL rather than reporting it. On a site whose authority rests on its
citations, a source link that 404s is a broken claim.

The rule is deliberately blunt: a URL in a post carries no non-ASCII, and no
host that is a known artefact of the rewrite. Nothing legitimate on this site
needs either today (0 of 10441 external URLs), and a link to a genuinely
non-ASCII URL can be added to ALLOW with a note rather than by loosening the
check.

A link to an English article (``sebastienrousseau.com/<date>-<slug>``, no
locale prefix) must also name a live English post or a retired slug that
``_data/redirects/articles.json`` redirects. 384 links across 169 posts named
five English slugs that never existed (a guessed ``-vs-`` slug, a typo, a
Polish slug without its ``/pl/`` prefix) and served a 404.

Usage:  python3 tests/validation/test_url_integrity.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POSTS = ROOT / "_posts"
REDIRECTS = ROOT / "_data" / "redirects" / "articles.json"

# An English article URL: the site root followed directly by a dated slug.
_EN_ARTICLE = re.compile(r"https://sebastienrousseau\.com/(\d{4}-\d{2}-\d{2}-[a-z0-9-]+)")

_URL = re.compile(r"https?://[^\s\)\]\"'<>]+")

# Hosts produced by translating a real host. Punycode here is never
# legitimate: it is the pipeline having translated a subdomain.
BAD_HOSTS = (
    "microsvaak",
    "prowidesvaakware",
    "nieuwrons-lab",
    "spwereldwijd",
    "news.met.edu",
    "www.met.edu",
    "xn--",
    "em.wikipedia.org",
    "in.wikipedia.org",
)

# Path tokens produced by translating English words inside a URL slug.
BAD_PATH_TOKENS = (
    "internationaal",
    "financial-settore",
    "casuoudy",
    "generatieve-ai",
    "2026-globale-threat",
    "2026-wereldwijd-threat",
    "cap-ideia-expand",
    "first-o-s-registered",
)

# Legitimately non-ASCII URLs, if one is ever needed. Empty today.
ALLOW: frozenset[str] = frozenset()

# The same rewrite in Latin script, which the non-ASCII rule cannot see: the
# /en/ path segment translated into the locale's own word — "em" (pt-br, it),
# "in" (id, ms, it). Host-scoped on purpose. linkedin.com/in/<profile> is a real
# path, and a blanket /in/ rule proposed rewriting 1798 correct URLs
# including every LinkedIn link on the site.
_EN_SEGMENT_HOSTS = (
    "banking.vision",
    "informedclearly.com",
    "mambu.com",
    "www.cgi.com",
    "www.cov.com",
    "www.deloitte.com",
    "www.europarl.europa.eu",
    "www.ingwb.com",
    "www.lw.com",
    "www.santander.com",
    "www.sc.com",
    "www.spglobal.com",
    "www.tsinghua.edu.cn",
)
_MANGLED_SEGMENT = re.compile(r"/(?:em|in)(?:-gb)?/")


def offences(text: str) -> list[str]:
    found = []
    for raw in _URL.findall(text):
        url = raw.rstrip(".,;:")
        if url in ALLOW:
            continue
        if any(ord(ch) > 127 for ch in url):
            found.append(f"non-ASCII in URL: {url}")
        elif any(bad in url for bad in BAD_HOSTS):
            found.append(f"host rewritten by translation: {url}")
        elif any(tok in url for tok in BAD_PATH_TOKENS):
            found.append(f"path token rewritten by translation: {url}")
        elif any(h in url for h in _EN_SEGMENT_HOSTS) and _MANGLED_SEGMENT.search(url):
            found.append(f"/en/ path segment rewritten by translation: {url}")
    return found


def dead_article_links(text: str, live: frozenset[str]) -> list[str]:
    """English article URLs whose slug is neither a post nor redirected."""
    dead = sorted({slug for slug in _EN_ARTICLE.findall(text) if slug not in live})
    return [f"no such English article: {slug}" for slug in dead]


def live_english_slugs() -> frozenset[str]:
    """English post slugs plus the retired English slugs that redirect."""
    redirects = json.loads(REDIRECTS.read_text(encoding="utf-8")).get("en", {})
    return frozenset(p.stem for p in POSTS.glob("*.md")) | frozenset(redirects)


def main() -> int:
    failures: list[str] = []
    scanned = 0
    live = live_english_slugs()
    for post in sorted(POSTS.rglob("*.md")):
        scanned += 1
        text = post.read_text(encoding="utf-8")
        failures.extend(
            f"{post.relative_to(ROOT)}: {offence}"
            for offence in offences(text) + dead_article_links(text, live)
        )

    if failures:
        for line in failures[:40]:
            print(f"FAIL {line}", file=sys.stderr)
        if len(failures) > 40:
            print(f"  …and {len(failures) - 40} more", file=sys.stderr)
        print(
            f"\nurl-integrity: {len(failures)} rewritten URL(s) in {scanned} posts. "
            f"Restore the original URL — the English post is the reference.",
            file=sys.stderr,
        )
        return 1
    print(f"ok: no translation-rewritten URLs in {scanned} posts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
