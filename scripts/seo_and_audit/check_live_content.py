#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Assert the LIVE site serves the current build, not a stale copy.

The hourly drift job used to probe ``/iso20022-mcp/`` with ``curl -I``. On
1 Nov 2026 that check stayed green while the edge served the pre-overhaul
hub (19 sections, no advisory CTA, a broken ``project-docs/sigstore.md``
link) for two days after ``main`` had shipped the new one: a 200 says the
path exists, not what is on it.

This script checks content markers instead. Each check is a pure function
over fetched text so tests/unit/test_check_live_content.py can exercise it
offline. Markers tolerate minified HTML (bare attribute values).

Exit 0 when every check passes, 1 otherwise, listing each failure.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import re
import sys
import urllib.request
from collections.abc import Callable

BASE = "https://sebastienrousseau.com"
UA = "sebastienrousseau.com deploy-drift check (+https://github.com/sebastienrousseau)"
MAX_STAMP_AGE_DAYS = 31


def _attr(name: str, value: str) -> re.Pattern[str]:
    """Match ``name="value"``, ``name='value'`` or minified ``name=value``."""
    return re.compile(rf"\b{name}\s*=\s*[\"']?{re.escape(value)}(?=[\"'\s>])", re.I)


def check_hub(html: str) -> list[str]:
    """The ISO 20022 MCP hub must be the consolidated build."""
    errors = []
    if not _attr("id", "mcp-faq").search(html):
        errors.append("/iso20022-mcp/: no #mcp-faq section (stale pre-overhaul hub?)")
    if "project-docs/sigstore" in html:
        errors.append("/iso20022-mcp/: links to project-docs/sigstore.md, which does not exist")
    sections = len(re.findall(r"<section\b", html, re.I))
    if sections > 20:
        errors.append(f"/iso20022-mcp/: {sections} <section> elements (hub cap is 15 + chrome)")
    return errors


def stylesheet_urls(html: str) -> list[str]:
    """Same-origin stylesheet hrefs, in document order."""
    out = []
    for tag in re.findall(r"<link\b[^>]*>", html, re.I):
        if not re.search(r"\brel\s*=\s*[\"']?stylesheet", tag, re.I):
            continue
        m = re.search(r"\bhref\s*=\s*[\"']?([^\"'\s>]+)", tag, re.I)
        if m and m.group(1).startswith("/") and not m.group(1).startswith("//"):
            out.append(m.group(1))
    return out


def check_design_system(css_bundle: str) -> list[str]:
    """The design-system layer must be in the shipped CSS."""
    errors = []
    if "@layer legacy" not in css_bundle:
        errors.append("CSS: legacy rules are not wrapped in @layer legacy")
    errors.extend(
        f"CSS: design-system token {token} missing"
        for token in ("--fs-display", "--fs-prose", "--measure")
        if token not in css_bundle
    )
    return errors


def check_stamp(html: str, today: _dt.date) -> list[str]:
    """The homepage proof stamp must be no older than MAX_STAMP_AGE_DAYS."""
    m = re.search(
        r"proof-updated[^>]*>[^<]*<time[^>]*\bdatetime\s*=\s*[\"']?(\d{4}-\d{2}-\d{2})",
        html,
        re.I,
    )
    if not m:
        return ["/: proof-rail 'Updated' stamp not found"]
    age = (today - _dt.date.fromisoformat(m.group(1))).days
    if age > MAX_STAMP_AGE_DAYS:
        return [f"/: proof stamp is {age} days old ({m.group(1)})"]
    return []


def newest_feed_link(rss: str) -> str | None:
    """Path of the first <item>'s <link> in an RSS feed."""
    item = re.search(r"<item\b.*?</item>", rss, re.S | re.I)
    if not item:
        return None
    link = re.search(r"<link>\s*([^<\s]+)\s*</link>", item.group(0), re.I)
    if not link:
        return None
    path = re.sub(r"^https?://[^/]+", "", link.group(1))
    return path.rstrip("/").removesuffix("/index.html")


def check_freshness(newest: str | None, home: str, articles: str) -> list[str]:
    """The newest article must appear on the homepage and the articles index."""
    if not newest:
        return ["rss.xml: no first item"]
    errors = []
    for name, html in (("/", home), ("/articles/", articles)):
        if newest not in html:
            errors.append(f"{name}: newest article {newest} not listed (stale page?)")
    return errors


def _fetch(path: str, timeout: int = 30) -> str:
    req = urllib.request.Request(
        BASE + path, headers={"User-Agent": UA, "Cache-Control": "no-cache"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def run(fetch: Callable[[str], str] = _fetch, today: _dt.date | None = None) -> list[str]:
    today = today or _dt.datetime.now(_dt.UTC).date()
    home = fetch("/")
    hub = fetch("/iso20022-mcp/")
    articles = fetch("/articles/")
    rss = fetch("/rss.xml")
    css = "".join(fetch(u) for u in stylesheet_urls(home))
    return (
        check_hub(hub)
        + check_design_system(css)
        + check_stamp(home, today)
        + check_freshness(newest_feed_link(rss), home, articles)
    )


def main(argv: list[str] | None = None) -> int:
    desc = (__doc__ or "").splitlines()[0]
    argparse.ArgumentParser(description=desc).parse_args(argv)
    errors = run()
    for e in errors:
        print(f"::error::{e}")
    if not errors:
        print("live content: hub, design system, proof stamp and freshness all current")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
