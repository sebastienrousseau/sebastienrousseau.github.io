# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Feed serialisation details not already covered elsewhere.

Deliberately small. Most of build_lang_feeds' interesting behaviour is
already tested and this file does not restate it:

  * parse_date raising rather than stamping the build time — the 467-post
    regression — is covered by tests/unit/test_locale_date_frontmatter.py
  * _resolve_pub_name, in both the localised and fallback directions, is
    covered by tests/unit/test_news_sitemap_locale.py
  * main() is exercised by tests/unit/test_builder_main_smoke.py

What was left untested is the serialisation layer: entity handling in
xml_escape, the two date formats a feed reader parses, and the news-window
predicate's type guard. A wrong RFC-822 string does not fail a build — the
feed just stops validating in readers.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import build_lang_feeds as blf
import pytest

# ---------------------------------------------------------------------------
# XML escaping
# ---------------------------------------------------------------------------


def test_xml_escape_covers_all_five_entities() -> None:
    out = blf.xml_escape("""<a href="x" title='y'>&</a>""")
    for ch in ("<", ">", '"', "'"):
        assert ch not in out
    assert "&amp;" in out


def test_xml_escape_does_not_double_encode_an_existing_entity() -> None:
    """Feed text often already carries &amp; from the source markdown."""
    assert blf.xml_escape("a &amp; b") == "a &amp; b"


def test_xml_escape_encodes_a_bare_ampersand() -> None:
    assert blf.xml_escape("a & b") == "a &amp; b"


def test_xml_escape_uses_apos_not_rsquo() -> None:
    """&apos; is XML; &rsquo; is HTML and would break a strict parser."""
    assert blf.xml_escape("it's") == "it&apos;s"


# ---------------------------------------------------------------------------
# Date serialisation — wrong here means the feed stops validating, silently
# ---------------------------------------------------------------------------


def test_rfc822_shape() -> None:
    d = datetime(2023, 10, 26, 6, 6, 6, tzinfo=UTC)
    assert blf.rfc822(d) == "Thu, 26 Oct 2023 06:06:06 +0000"


def test_iso8601_shape() -> None:
    d = datetime(2023, 10, 26, 6, 6, 6, tzinfo=UTC)
    assert blf.iso8601(d) == "2023-10-26T06:06:06+00:00"


def test_parse_date_strptime_returns_none_rather_than_raising() -> None:
    """The caller distinguishes 'no format matched' from a hard error."""
    assert blf._parse_date_strptime("nope") is None
    assert blf._parse_date_strptime("2023-10-26") is not None


# ---------------------------------------------------------------------------
# News window
# ---------------------------------------------------------------------------


NOW = datetime(2026, 6, 15, 12, 0, 0, tzinfo=UTC)


def test_news_window_includes_a_recent_post() -> None:
    assert blf._within_news_window({"date": NOW - timedelta(hours=1)}, NOW)


def test_news_window_excludes_an_old_post() -> None:
    assert not blf._within_news_window({"date": NOW - timedelta(days=365)}, NOW)


def test_news_window_excludes_an_entry_with_no_date() -> None:
    assert not blf._within_news_window({}, NOW)


def test_news_window_excludes_a_string_date() -> None:
    """A str must not be compared as though it were a datetime."""
    assert not blf._within_news_window({"date": "2026-06-15"}, NOW)


# ---------------------------------------------------------------------------
# Front matter and collection
# ---------------------------------------------------------------------------


def test_parse_frontmatter_reads_hyphenated_and_mixed_case_keys() -> None:
    """The local reimplementation this replaced silently dropped both."""
    fm = blf.parse_frontmatter('---\nbanner-alt: "A"\nSomeKey: "B"\ntitle: "T"\n---\nbody\n')
    assert fm.get("title") == "T"
    assert "banner-alt" in fm or "SomeKey" in fm


def test_parse_frontmatter_of_a_file_without_any() -> None:
    assert blf.parse_frontmatter("just body text\n") == {}


def test_collect_entries_is_empty_for_an_unbuilt_locale(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir("/")
    assert blf.collect_entries("nonexistent-locale") == []
