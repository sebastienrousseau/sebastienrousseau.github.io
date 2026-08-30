# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""`script-src` must not accumulate duplicate inline-script hashes.

inject_jsonld_hashes prepends the page's hashes into script-src, and runs
more than once over a page as later passes add content. Each run re-prepended
the same tokens: a shipped article carried 19 tokens for 11 distinct scripts,
a local build 31 for 15. Duplicates are inert to a browser but they are a
redundant kilobyte in the head of every page and they mean the pass is not
idempotent — which a byte-identical-rebuild gate cares about.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "postbuild"))

import postbuild_assets as pba

_SHA = re.compile(r"'sha256-[^']+'")


def _script_src(policy: str) -> str:
    return policy.split("script-src", 1)[1].split(";", 1)[0]


def test_repeated_hashes_collapse_to_one_each() -> None:
    policy = (
        "default-src 'self'; script-src 'sha256-A=' 'sha256-B=' 'sha256-A=' "
        "'sha256-C=' 'sha256-B=' 'self';"
    )
    out = pba._dedupe_script_hashes(policy)
    tokens = _SHA.findall(_script_src(out))
    assert tokens == ["'sha256-A='", "'sha256-B='", "'sha256-C='"]


def test_first_occurrence_order_is_preserved() -> None:
    """Token order must be stable so rebuilds stay byte-identical."""
    policy = "script-src 'sha256-Z=' 'sha256-A=' 'sha256-Z=' 'self';"
    assert _SHA.findall(_script_src(pba._dedupe_script_hashes(policy))) == [
        "'sha256-Z='",
        "'sha256-A='",
    ]


def test_non_hash_tokens_survive() -> None:
    policy = "script-src 'sha256-A=' 'sha256-A=' 'self' 'inline-speculation-rules' https://x.dev;"
    out = _script_src(pba._dedupe_script_hashes(policy))
    for token in ("'self'", "'inline-speculation-rules'", "https://x.dev"):
        assert token in out


def test_other_directives_are_untouched() -> None:
    policy = "script-src 'sha256-A=' 'sha256-A=';style-src 'self' 'sha256-A=' 'sha256-A=';"
    out = pba._dedupe_script_hashes(policy)
    assert out.split("style-src", 1)[1].count("'sha256-A='") == 2


def test_is_idempotent() -> None:
    policy = "default-src 'self'; script-src 'sha256-A=' 'sha256-A=' 'self';"
    once = pba._dedupe_script_hashes(policy)
    assert pba._dedupe_script_hashes(once) == once


def test_no_collapsed_whitespace_left_behind() -> None:
    policy = "script-src 'sha256-A=' 'sha256-A=' 'sha256-A=' 'self';"
    assert "  " not in pba._dedupe_script_hashes(policy)


def test_policy_without_script_src_is_returned_unchanged() -> None:
    policy = "default-src 'self'; style-src 'self';"
    assert pba._dedupe_script_hashes(policy) == policy


def test_already_unique_policy_is_unchanged() -> None:
    policy = "script-src 'sha256-A=' 'sha256-B=' 'self';"
    assert pba._dedupe_script_hashes(policy) == policy


def test_layouts_carry_no_empty_string_style_hash() -> None:
    """47DEQpj8… is SHA-256 of "" — a hash for an inline <style></style> no
    rendered page has. It shipped in every layout's style-src."""
    for layout in (ROOT / "_layouts").glob("*.html"):
        assert "47DEQpj8HBSa" not in layout.read_text(encoding="utf-8"), layout.name
