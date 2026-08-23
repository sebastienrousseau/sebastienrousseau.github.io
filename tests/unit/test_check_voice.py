"""Unit coverage for the publishing voice/structure gate — Phase 1.3.

`scripts/editorial/check_voice.py` gates every article before the 27-locale
translation + build pipeline runs, but had no unit tests. These cover its
pure, network-free check functions (the banner/external-link checks hit the
network and are exercised separately). Each check returns a `list[str]` of
defects, empty when the input is clean.
"""

from __future__ import annotations

import datetime as _dt
from pathlib import Path

import check_voice

# A minimal article body that satisfies every EN structural rule.
_GOOD_BODY = """# An Example Title

<!-- lead-start -->
<aside class="post-lead">
> **Executive Summary**
TL;DR of the piece.
</aside>
<!-- lead-end -->

Intro paragraph with a citation ([Source, 2026](https://example.com "Source title")).

## Section One

Body.

## Section Two

Body.

## Frequently Asked Questions

**Is this a question?**
Yes.

## References

1. [Source, 2026](https://example.com "Source title")
"""


def _full_frontmatter() -> dict[str, str]:
    return {k: "x" for k in check_voice._REQUIRED_FM}


# --- check_frontmatter -----------------------------------------------------


def test_frontmatter_complete_passes() -> None:
    assert check_voice.check_frontmatter(_full_frontmatter()) == []


def test_frontmatter_missing_keys_flagged() -> None:
    fm = _full_frontmatter()
    del fm["title"]
    fm["excerpt"] = ""  # empty counts as missing
    defects = check_voice.check_frontmatter(fm)
    assert any("title" in d for d in defects)
    assert any("excerpt" in d for d in defects)
    assert len(defects) == 2


# --- check_filler ----------------------------------------------------------


def test_filler_clean_body_passes() -> None:
    assert check_voice.check_filler("A clean, direct sentence.") == []


def test_filler_detects_banned_phrase_case_insensitive() -> None:
    defects = check_voice.check_filler("In Conclusion, we synergy the paradigm shift.")
    # "in conclusion,", "synergy", "paradigm shift"
    assert len(defects) >= 3


# --- check_structure (EN) --------------------------------------------------


def test_structure_good_body_passes() -> None:
    assert check_voice.check_structure(_GOOD_BODY, lang="en") == []


def test_structure_bare_body_reports_defects() -> None:
    defects = check_voice.check_structure("# Title\n\nJust prose.\n", lang="en")
    joined = " ".join(defects)
    assert "lead" in joined
    assert "H2" in joined
    assert "citation" in joined
    assert "FAQ" in joined
    assert "References" in joined


def test_structure_accepts_manual_lead_marker() -> None:
    body = _GOOD_BODY.replace("<!-- lead-start -->", "<!-- lead-start: manual -->")
    assert check_voice.check_structure(body, lang="en") == []


# --- check_markdown_discipline ---------------------------------------------


def test_markdown_single_h1_passes() -> None:
    assert check_voice.check_markdown_discipline("# Only One\n\nBody.\n") == []


def test_markdown_flags_zero_and_multiple_h1() -> None:
    assert check_voice.check_markdown_discipline("No heading.\n")
    assert check_voice.check_markdown_discipline("# A\n# B\n")


def test_markdown_flags_broken_citation() -> None:
    defects = check_voice.check_markdown_discipline("# T\n\nbroken ](] link\n")
    assert any("broken citation" in d for d in defects)


# --- check_date_consistency ------------------------------------------------


def _today() -> str:
    return _dt.datetime.now(_dt.UTC).strftime("%Y-%m-%d")


def test_date_consistent_passes() -> None:
    today_iso = _today()
    display = _dt.datetime.now(_dt.UTC).strftime("%B %d, %Y")
    path = Path(f"_posts/{today_iso}-example-article.md")
    assert check_voice.check_date_consistency(path, {"date": display}) == []


def test_date_non_dated_filename_flagged() -> None:
    defects = check_voice.check_date_consistency(Path("_posts/about.md"), {})
    assert defects and "does not begin with YYYY-MM-DD" in defects[0]


def test_date_frontmatter_mismatch_flagged() -> None:
    today_iso = _today()
    path = Path(f"_posts/{today_iso}-example-article.md")
    # A clearly wrong frontmatter date in the right format.
    defects = check_voice.check_date_consistency(path, {"date": "January 01, 2020"})
    assert any("frontmatter" in d for d in defects)
