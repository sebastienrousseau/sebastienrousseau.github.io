#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Rewrite the in-page language switcher so each ``.ap-lang-item`` link
points to **the localised URL of the current page** instead of the
locale homepage.

Why this exists
---------------

``_layouts/report.html`` (and every other page layout that embeds the
language switcher) hard-codes the switcher hrefs as ``/<lang>/`` — the
locale **homepage**. A user reading
``/2026-05-23-agentic-payments-banking-...`` who clicks "🇫🇷 Français"
in the switcher is therefore sent to ``/fr/`` instead of
``/fr/2026-05-23-agentique-paiements-banking-...``. That's wrong: the
user wanted the French translation of *this article*, not a fresh trip
to the French landing page.

A small chunk of JS in ``_layouts/main.js`` (``langSelector``) tries to
correct this at runtime by reading the page's ``<link rel="alternate"
hreflang="<lang>">`` head links and overwriting each switcher item's
href. That works for users with JavaScript enabled. It does **not**
work for:

* search engine crawlers that don't execute JS (SEO signal is wrong)
* users who right-click a switcher item and choose "open in new tab"
  (the browser uses the SSR href, not the JS-patched one)
* users on slow connections who click before JS hydrates
* anyone with JavaScript disabled

The fix is to do at **build time** what the JS does at runtime: read
each rendered HTML page's own ``<link rel="alternate" hreflang>`` head
links, and rewrite every ``.ap-lang-item`` element's ``href`` to match.
After this script runs the SSR output is already correct; the JS
becomes a redundant safety-net rather than the primary mechanism.

The rewrite is idempotent — running this script twice on the same
output produces no further changes.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"

# Match `<link rel="alternate" hreflang="<lang>" href="<url>" />`.
# Tolerant of attribute order and quote style so a future layout tweak
# doesn't silently disable the rewrite.
_HREFLANG_RE = re.compile(
    r"""<link\s+(?=[^>]*\brel\s*=\s*["']alternate["'])"""
    r"""(?=[^>]*\bhreflang\s*=\s*["']([^"']+)["'])"""
    r"""(?=[^>]*\bhref\s*=\s*["']([^"']+)["'])"""
    r"""[^>]*/?>""",
    re.IGNORECASE,
)

# Match a single switcher item:
#   <a class="ap-lang-item" href="/fr/" data-lang="fr" role="menuitem">…</a>
# Capture the existing href and the data-lang so we know which locale
# to swap to. Attribute order in the layout is fixed, but tolerate
# either single or double quotes.
_SWITCHER_RE = re.compile(
    r"""(<a\s+class\s*=\s*["']ap-lang-item["']\s+)"""
    r"""href\s*=\s*["']([^"']*)["']"""
    r"""(\s+data-lang\s*=\s*["']([^"']+)["'])""",
    re.IGNORECASE,
)


def _alternates(html: str) -> dict[str, str]:
    """Return ``{hreflang: pathname-with-query-and-hash}`` from the
    page's ``<link rel="alternate" hreflang>`` head links. Absolute
    URLs get stripped down to their path component so the rewrite stays
    origin-relative — a localhost preview shouldn't navigate to prod
    when JS-rewriting these in a browser, and the build output should
    match the JS contract."""
    out: dict[str, str] = {}
    for m in _HREFLANG_RE.finditer(html):
        lang = m.group(1).strip()
        href = m.group(2).strip()
        if not lang or not href or lang.lower() == "x-default":
            continue
        out[lang] = _path_of(href)
    return out


def _path_of(href: str) -> str:
    """Strip the absolute URL down to path + query + fragment. We do
    this with string ops rather than urllib because all of our hreflang
    links use the same origin (``sebastienrousseau.com``) and the
    standard library import is heavier than it's worth here."""
    if href.startswith("http://") or href.startswith("https://"):
        # Drop scheme + host.
        after_scheme = href.split("://", 1)[1]
        slash = after_scheme.find("/")
        if slash < 0:
            return "/"
        return after_scheme[slash:]
    return href


def _rewrite(html: str, alternates: dict[str, str]) -> tuple[str, int]:
    """Apply the per-page alternates to the switcher block. Returns
    ``(new_html, num_replaced)``. Items whose ``data-lang`` doesn't
    appear in the page's alternates are left alone — those would be
    placeholder languages for which no live translation exists."""
    count = [0]

    def _sub(m: re.Match[str]) -> str:
        prefix = m.group(1)
        old_href = m.group(2)
        data_attr = m.group(3)
        lang = m.group(4).strip()
        new_href = alternates.get(lang)
        if not new_href or new_href == old_href:
            return m.group(0)
        count[0] += 1
        return f'{prefix}href="{new_href}"{data_attr}'

    new_html = _SWITCHER_RE.sub(_sub, html)
    return new_html, count[0]


def _fix_one(path: Path) -> int:
    """Rewrite one HTML file in place. Returns the count of switcher
    items rewired."""
    text = path.read_text(encoding="utf-8")
    if "ap-lang-item" not in text:
        return 0
    alternates = _alternates(text)
    if not alternates:
        return 0
    new_text, n = _rewrite(text, alternates)
    if n == 0:
        return 0
    path.write_text(new_text, encoding="utf-8")
    return n


def main() -> int:
    if not PUBLIC.is_dir():
        print(
            "fix_lang_switcher: public/ not found; run ssg first.",
            file=sys.stderr,
        )
        return 0
    total_files = 0
    total_links = 0
    for path in PUBLIC.rglob("index.html"):
        n = _fix_one(path)
        if n > 0:
            total_files += 1
            total_links += n
    print(f"fix_lang_switcher: rewrote {total_links} switcher link(s) across {total_files} page(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
