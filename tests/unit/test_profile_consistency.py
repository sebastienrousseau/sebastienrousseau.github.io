# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""No source states a profile fact other than _data/profile.yml's.

Each pattern is a wording the site once used about the author and the
profile now contradicts: three experience figures, two retired job
titles, an EPAA authorship he did not hold, credentials "recognised by"
bodies that never issued them, and "senior positions" at a two-month web
developer job. Patterns name the author's own claims only, so articles
that discuss "two decades" of Bitcoin or "senior technology leaders" as
an audience pass.

Generated text is skipped: the ``<!-- enrich-start -->`` block in each post
is rewritten by post_enrich.py on every build from the profile.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]

BANNED = {
    "nearly two decades": re.compile(r"(?i)nearly two decades"),
    "19 years": re.compile(r"\b19 [Yy]ears\b"),
    "AI Leader title": re.compile(r"Wholesale Payments &(?:amp;)? AI Leader"),
    "banking technologist": re.compile(r"(?i)senior banking technologist\b"),
    "aerospace card": re.compile(r"(?i)tier-one banking, aerospace"),
    "EPAA authorship": re.compile(r"(?i)\bco-?author(?:ed)?(?: of)? the EPAA|\bauthor of the EPAA"),
    "recognizedBy credential": re.compile(r'"recognizedBy"'),
    "senior positions at Virgin": re.compile(r"(?i)senior positions at [^.]*Virgin"),
}
SOURCES = (
    "_posts/*.md",
    "_data/proof/*.md",
    "_data/proof/case-studies/*.yml",
    "_data/i18n/en/*.json",
    "_layouts/*.html",
    "scripts/**/*.py",
)
_ENRICH = re.compile(r"<!-- enrich-start -->.*?<!-- enrich-end -->", re.S)


def _files() -> list[Path]:
    return sorted({p for pattern in SOURCES for p in ROOT.glob(pattern)})


def _hits(text: str) -> list[str]:
    text = _ENRICH.sub("", text)
    return [name for name, rx in BANNED.items() if rx.search(text)]


def test_sources_state_only_profile_facts() -> None:
    found = [
        f"{p.relative_to(ROOT)}: {', '.join(hits)}"
        for p in _files()
        if (hits := _hits(p.read_text(encoding="utf-8", errors="ignore")))
    ]
    assert not found, "\n".join(found[:60])


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("He has nearly two decades across Tier-1 banks.", ["nearly two decades"]),
        ("<span>19 Years</span>", ["19 years"]),
        ("Co-author of the EPAA white paper", ["EPAA authorship"]),
        ('{"recognizedBy": {}}', ["recognizedBy credential"]),
        ("held senior positions at PayPal and Virgin Group.", ["senior positions at Virgin"]),
        ("The journey from 2008 to 2026 spans two decades.", []),
        ("The roadmap for senior technology leaders is short.", []),
        ("The question for senior banking technologists is not which rail wins.", []),
        ("<!-- enrich-start -->nearly two decades<!-- enrich-end -->", []),
    ],
)
def test_patterns_catch_claims_not_prose(text: str, expected: list[str]) -> None:
    assert _hits(text) == expected
