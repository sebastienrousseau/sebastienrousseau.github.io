"""`news_publication_date` must be derived, never left to the clock.

ssg's news-sitemap generator falls back to the CURRENT TIME when the field is
blank, stamping a build timestamp onto an article as its publication date
(#433). Only 141 of 3,640 dated posts declared it; the other 3,499 logged a
parse warning every build — 3,556 lines in a 6.3 MB log.

The property that matters most here is determinism: the value is a function of
the post's own `date:`, never of when the build ran. If that ever stopped being
true the byte-identical rebuild gate would fail across thousands of files.
"""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "postbuild"))

import backfill_news_date as bnd

POST = '---\ntitle: "T"\ndate: "{date}"\nlayout: post\n---\n\nBody.\n'


def _post(tmp_path: Path, name: str, date: str) -> Path:
    p = tmp_path / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(POST.format(date=date), encoding="utf-8")
    return p


def _field(p: Path) -> str | None:
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.startswith("news_publication_date:"):
            return line.split(":", 1)[1].strip().strip('"')
    return None


def test_long_and_abbreviated_months_both_parse():
    """Both spellings occur in this corpus and look alike enough that a survey
    regex counts them as one. Accepting only the full name silently skipped
    539 posts — each keeping the build-time fallback."""
    assert bnd.parse_date("January 1, 2018") == dt.datetime(2018, 1, 1, tzinfo=dt.UTC)
    assert bnd.parse_date("Jan 01, 2018") == dt.datetime(2018, 1, 1, tzinfo=dt.UTC)


def test_iso_and_rfc_forms_parse():
    assert bnd.parse_date("2026-07-01") == dt.datetime(2026, 7, 1, tzinfo=dt.UTC)
    assert bnd.parse_date("Wed, 01 Jul 2026 07:07:07 +0000") is not None


def test_unparseable_date_returns_none_rather_than_guessing():
    """The worst case must be the status quo, not a wrong publication date."""
    for bad in ("", "   ", "le 3 février", "not a date", '""'):
        assert bnd.parse_date(bad) is None, bad


def test_stamp_is_derived_from_the_post_not_the_clock(tmp_path):
    _post(tmp_path, "2018-01-01-a.md", "January 1, 2018")
    added, unparsed = bnd.backfill(tmp_path)
    assert (added, unparsed) == (1, 0)
    assert _field(tmp_path / "2018-01-01-a.md") == "Mon, 01 Jan 2018 00:00:00 +0000"


def test_two_runs_over_identical_input_agree(tmp_path):
    """The byte-identical rebuild gate depends on this."""
    a, b = tmp_path / "a", tmp_path / "b"
    for root in (a, b):
        _post(root, "2026-04-11-x.md", "Apr 11, 2026")
        _post(root, "fr/2026-04-11-y.md", "April 11, 2026")
        bnd.backfill(root)
    for name in ("2026-04-11-x.md", "fr/2026-04-11-y.md"):
        assert (a / name).read_bytes() == (b / name).read_bytes(), name


def test_existing_field_is_never_overwritten(tmp_path):
    p = tmp_path / "2024-03-18-a.md"
    original = '---\ntitle: "T"\nnews_publication_date: "Mon, 18 Mar 2024 06:06:06 +0000"\ndate: "March 18, 2024"\n---\n\nB.\n'
    p.write_text(original, encoding="utf-8")
    added, _ = bnd.backfill(tmp_path)
    assert added == 0
    assert p.read_text(encoding="utf-8") == original


def test_undated_and_readme_files_are_skipped(tmp_path):
    _post(tmp_path, "README.md", "January 1, 2018")
    _post(tmp_path, "about.md", "January 1, 2018")  # no date prefix in the name
    added, unparsed = bnd.backfill(tmp_path)
    assert (added, unparsed) == (0, 0)


def test_post_with_unparseable_date_is_left_alone(tmp_path):
    p = _post(tmp_path, "2018-01-01-a.md", "le 1 janvier 2018")
    before = p.read_text(encoding="utf-8")
    added, unparsed = bnd.backfill(tmp_path)
    assert (added, unparsed) == (0, 1)
    assert p.read_text(encoding="utf-8") == before
