# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""``script-src`` must not accumulate hashes for scripts that changed.

Sibling of ``test_csp_hash_dedupe``, which covers *repeated* tokens. This
one covers *stale* ones, which dedupe cannot see: two different hashes are
not duplicates.

``inject_jsonld_hashes`` prepends the page's inline-script hashes into
``script-src``. Postbuild runs over a page more than once, and later passes
rewrite inline JSON-LD (a counter, a date, an enriched graph). When a block
changes, its new hash is prepended while the old one stays — so the
directive grew by one token every pass. Measured on the real tree,
re-running the builder smoke tests took a dated article from 11 hash tokens
to 12 to 13, roughly 54 bytes per page per run across ~6,900 pages, with no
fixed point.

The fix replaces the hash set instead of merging into it. These tests pin
that: a changed script converges, and an already-polluted policy heals.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "postbuild"))

import postbuild_assets as pba  # type: ignore[import-not-found]

_SHA = re.compile(r"'sha256-[^']+'")

_CSP_HEAD = (
    '<html><head><meta http-equiv="Content-Security-Policy" '
    "content=\"default-src 'self'; script-src 'self' https://cdn.jsdelivr.net;\" />"
)


def _page(jsonld: str, policy_extra: str = "") -> str:
    head = _CSP_HEAD
    if policy_extra:
        head = head.replace("script-src 'self'", f"script-src {policy_extra} 'self'")
    return f'{head}</head><body><script type="application/ld+json">{jsonld}</script></body></html>'


def _script_src(html: str) -> str:
    policy = re.search(r'content="([^"]*)"', html).group(1)
    return policy.split("script-src", 1)[1].split(";", 1)[0]


def _hashes(html: str) -> list[str]:
    return _SHA.findall(_script_src(html))


def test_one_hash_per_inline_script() -> None:
    out = pba.inject_jsonld_hashes(_page('{"a":1}'))
    assert len(_hashes(out)) == 1


def test_rewriting_the_script_replaces_its_hash_rather_than_adding_one() -> None:
    """The regression: a changed JSON-LD body must not leave its old hash."""
    first = pba.inject_jsonld_hashes(_page('{"a":1}'))
    before = _hashes(first)

    # Same page, JSON-LD rewritten by a later pass, CSP already stamped.
    rewritten = first.replace('{"a":1}', '{"a":2}')
    second = pba.inject_jsonld_hashes(rewritten)
    after = _hashes(second)

    assert len(after) == 1, f"stale hash retained: {after}"
    assert after != before, "hash should track the new script body"


def test_repeated_passes_reach_a_fixed_point() -> None:
    """Running the pass again on its own output must change nothing."""
    once = pba.inject_jsonld_hashes(_page('{"a":1}'))
    twice = pba.inject_jsonld_hashes(once)
    assert twice == once


def test_an_already_polluted_policy_is_healed() -> None:
    """A tree that accumulated stale hashes converges on the next run."""
    stale = "'sha256-AAAA=' 'sha256-BBBB=' 'sha256-CCCC='"
    out = pba.inject_jsonld_hashes(_page('{"a":1}', policy_extra=stale))
    hashes = _hashes(out)
    assert len(hashes) == 1
    assert "'sha256-AAAA='" not in hashes
