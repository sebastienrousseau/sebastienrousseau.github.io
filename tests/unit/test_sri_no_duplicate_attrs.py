# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""`fix_sri` must leave exactly one `integrity` attribute per tag.

ssg writes its own `integrity` on the stylesheet link it emits, using the
configured `sri_algorithm` — which defaults to **SHA-384**. `fix_sri` then
stamps its own digest, and its docstring has always promised that "stale/bogus
integrity ... [is] stripped first so we don't accumulate duplicates".

The strip regex matched `sha256-` only. So on any ssg emitting sha384, nothing
was stripped and every page shipped two integrity attributes:

    <link ... integrity="sha384-2x89..." integrity="sha256-ObNF... sha256-ldKU...">

HTML parsers take the first attribute and drop the rest, so SRI still held via
the sha384 value — which is precisely why it went unnoticed. The markup was
invalid, the second attribute was dead, and 6,854 of 6,856 pages carried it.

It was invisible for as long as ssg happened to emit sha256, which is what the
version this site was pinned to did. Moving to the current release surfaced it.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "postbuild"))

import postbuild_assets as pba

_INTEGRITY = re.compile(r"\bintegrity=")


@pytest.mark.parametrize("algorithm", ["sha256", "sha384", "sha512"])
def test_existing_integrity_is_stripped_whatever_the_algorithm(algorithm: str) -> None:
    tag = (
        f'<link rel="stylesheet" href="/_csp/a.css" '
        f'integrity="{algorithm}-AAAA" crossorigin="anonymous">'
    )
    assert not _INTEGRITY.search(pba._SRI_ANY_RE.sub("", tag)), (
        f"a pre-existing {algorithm} integrity must be stripped before re-stamping"
    )


def test_strip_leaves_the_rest_of_the_tag_intact() -> None:
    tag = '<link rel="stylesheet" href="/_csp/a.css" integrity="sha384-AAAA" media="print">'
    out = pba._SRI_ANY_RE.sub("", tag)
    for keep in ('rel="stylesheet"', 'href="/_csp/a.css"', 'media="print"'):
        assert keep in out


def test_single_quoted_integrity_is_also_stripped() -> None:
    tag = "<link href='/_csp/a.css' integrity='sha384-AAAA'>"
    assert not _INTEGRITY.search(pba._SRI_ANY_RE.sub("", tag))


def test_a_tag_without_integrity_is_untouched() -> None:
    tag = '<link rel="stylesheet" href="/_csp/a.css">'
    assert pba._SRI_ANY_RE.sub("", tag) == tag


def test_unknown_algorithm_is_left_alone() -> None:
    """Only the SRI algorithms the spec defines are stripped. Anything else is
    not ours to remove, and silently deleting it would hide a real problem."""
    tag = '<link href="/_csp/a.css" integrity="md5-AAAA">'
    assert pba._SRI_ANY_RE.sub("", tag) == tag
