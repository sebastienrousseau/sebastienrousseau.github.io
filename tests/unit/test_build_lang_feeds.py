"""Unit coverage for build_lang_feeds — Phase 1.3.

build_lang_feeds.py emits per-language RSS/Atom/news-sitemap/JSON feeds. It was
untested. Cover the pure frontmatter/date-parsing and XML-escaping helpers that
determine feed correctness.
"""

from __future__ import annotations

from datetime import UTC, datetime

import build_lang_feeds as blf

# --- parse_frontmatter -----------------------------------------------------


def test_parse_frontmatter_quoted_values() -> None:
    # _FM_KEY_RE is quoted-only (real frontmatter always quotes values).
    fm = blf.parse_frontmatter('---\ntitle: "Hello"\ndate: "2026-06-29"\nx: \'sq\'\n---\nbody\n')
    assert fm["title"] == "Hello"
    assert fm["date"] == "2026-06-29"
    assert fm["x"] == "sq"  # single-quoted captured too


def test_parse_frontmatter_ignores_bare_values() -> None:
    fm = blf.parse_frontmatter('---\ntitle: "T"\nbare: unquoted\n---\n')
    assert "bare" not in fm  # only quoted values are captured


# --- date parsing ----------------------------------------------------------


def test_parse_date_strptime_formats() -> None:
    assert blf._parse_date_strptime("2023-10-26") == datetime(2023, 10, 26)
    assert blf._parse_date_strptime("October 26, 2023") == datetime(2023, 10, 26)
    assert blf._parse_date_strptime("Oct 26, 2023") == datetime(2023, 10, 26)
    assert blf._parse_date_strptime("not a date") is None


def test_parse_date_sets_rss_time_utc() -> None:
    d = blf.parse_date("2023-10-26")
    assert (d.year, d.month, d.day) == (2023, 10, 26)
    assert (d.hour, d.minute, d.second) == (6, 6, 6)
    assert d.tzinfo == UTC


def test_parse_date_raises_instead_of_stamping_now() -> None:
    """This test previously asserted the opposite, and that is the point.

    It read `test_parse_date_empty_falls_back_to_now` and asserted that an
    unparseable date silently became `datetime.now()`. The fallback was not an
    oversight — it was specified and covered, which is why nothing questioned
    it while 467 posts across 27 locale feeds advertised themselves as
    published at build time. A <pubDate> was always present and always
    plausible. Failing loudly is the only thing that makes a wrong date
    findable. See #433.
    """
    for bad in ("", "28 juin 2026", "2026年6月27日", "garbage string"):
        try:
            blf.parse_date(bad)
        except ValueError:
            continue
        raise AssertionError(f"parse_date({bad!r}) must raise, not invent a date")


def test_xml_escape_bare_ampersand_only() -> None:
    assert blf.xml_escape("a & b") == "a &amp; b"


def test_xml_escape_preserves_existing_entities() -> None:
    assert blf.xml_escape("a &amp; b &#233; c") == "a &amp; b &#233; c"  # not double-escaped


def test_xml_escape_angle_brackets_and_quotes() -> None:
    assert blf.xml_escape('<x> "y" \'z\'') == "&lt;x&gt; &quot;y&quot; &apos;z&apos;"


# --- date formatting -------------------------------------------------------


def test_rfc822_and_iso8601() -> None:
    d = datetime(2026, 6, 29, 6, 6, 6, tzinfo=UTC)
    assert blf.rfc822(d) == "Mon, 29 Jun 2026 06:06:06 +0000"
    assert blf.iso8601(d) == "2026-06-29T06:06:06+00:00"
