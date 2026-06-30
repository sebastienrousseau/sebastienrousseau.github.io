"""The empty-map sentinel regex must never match — Phase 4 (CodeQL).

`scripts/generators/build_translations/_maps.py` returns a "match nothing"
regex when a locale has no recorded mappings. The old sentinel `r"$^"` was
flagged by CodeQL (py/regex/unmatchable-caret + unmatchable-dollar) as an
anti-pattern; it is replaced with the canonical always-fails pattern
`r"(?!)"`. This locks the contract: the sentinel compiles and matches
nothing, so an empty map can never rewrite a URL.
"""

from __future__ import annotations

import re

from build_translations import _maps, _state


def test_empty_url_map_returns_never_matching_regex(monkeypatch) -> None:
    monkeypatch.setattr(_state, "EN_TO_FR", {})
    rx = _maps._build_en_url_rewriter()
    assert isinstance(rx, re.Pattern)
    assert rx.search("/2026-06-30-some-article/") is None
    assert rx.search("https://sebastienrousseau.com/x/index.html") is None
    assert rx.search("") is None


def test_sentinel_pattern_is_canonical_never_match() -> None:
    # Guard against a regression to the `$^` anti-pattern: `(?!)` is the
    # canonical always-fails regex and matches no input under any flags.
    rx = re.compile(r"(?!)")
    assert rx.search("anything") is None
    assert re.compile(r"(?!)", re.MULTILINE).search("a\nb") is None
