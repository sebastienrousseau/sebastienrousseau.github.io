# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Feed validation — RSS, Atom and the Google News sitemap.

These run as a build gate over every published feed, in 35 languages. The
gate's own predicates were untested: main() only ever sees a clean site, so a
check that had quietly stopped matching would report success exactly like one
that works.

The error/warning split is the design worth pinning. A duplicate <guid> is an
ERROR because it breaks subscriber-state machinery — a reader that has seen
that guid will skip the new item entirely. A duplicate <link> is only a
WARNING, because it is suspicious rather than broken. Getting that boundary
backwards would either fail builds over nothing or ship a feed that silently
loses posts for every subscriber.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET

import pytest
import validate_jsonld as vj

ATOM = vj._ATOM_NS


def _rss(items: str = "", channel_extra: str = "") -> ET.Element:
    return ET.fromstring(
        "<rss><channel>"
        "<title>T</title><link>https://x/</link>"
        "<description>" + "d" * 40 + "</description>"
        f"{channel_extra}{items}</channel></rss>"
    )


def _run_rss(root: ET.Element) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    vj._validate_rss(root, errors, warnings)
    return errors, warnings


# ---------------------------------------------------------------------------
# RSS channel
# ---------------------------------------------------------------------------


def test_rss_without_a_channel_is_an_error() -> None:
    errors, _ = _run_rss(ET.fromstring("<rss></rss>"))
    assert errors == ["rss: missing <channel>"]


def test_rss_channel_missing_a_required_field_is_an_error() -> None:
    root = ET.fromstring("<rss><channel><title>T</title></channel></rss>")
    errors, _ = _run_rss(root)
    assert any("missing <link>" in e for e in errors)
    assert any("missing <description>" in e for e in errors)


def test_rss_short_channel_description_is_only_a_warning() -> None:
    """A thin description is poor, not invalid — it must not fail a build."""
    root = ET.fromstring(
        "<rss><channel><title>T</title><link>https://x/</link>"
        "<description>short</description></channel></rss>"
    )
    errors, warnings = _run_rss(root)
    assert errors == []
    assert any("very short" in w for w in warnings)


def test_a_well_formed_rss_feed_is_clean() -> None:
    item = (
        "<item><title>A title</title><link>https://sebastienrousseau.com/a/</link>"
        "<guid>https://sebastienrousseau.com/a/</guid>"
        "<description>" + "d" * 40 + "</description>"
        "<pubDate>Mon, 11 May 2026 06:06:06 +0000</pubDate></item>"
    )
    errors, warnings = _run_rss(_rss(item))
    assert errors == []
    assert warnings == []


# ---------------------------------------------------------------------------
# RSS items — required fields and uniqueness
# ---------------------------------------------------------------------------


def test_rss_item_missing_title_or_link_is_an_error() -> None:
    errors, _ = _run_rss(_rss("<item><description>d</description></item>"))
    assert any("missing <title>" in e for e in errors)
    assert any("missing <link>" in e for e in errors)


def test_duplicate_guid_is_an_error_but_duplicate_link_is_a_warning() -> None:
    """The asymmetry is deliberate: a repeated guid makes a subscriber skip
    the new item, a repeated link is merely suspicious."""
    same = "https://sebastienrousseau.com/a/"
    item = f"<item><title>T</title><link>{same}</link><guid>{same}</guid></item>"
    errors, warnings = _run_rss(_rss(item + item))
    assert any("duplicate <guid>" in e for e in errors)
    assert any("duplicate <link>" in w for w in warnings)


def test_duplicate_messages_name_the_earlier_item() -> None:
    same = "https://sebastienrousseau.com/a/"
    item = f"<item><title>T</title><link>{same}</link><guid>{same}</guid></item>"
    errors, _ = _run_rss(_rss(item + item))
    assert "item[0]" in next(e for e in errors if "duplicate <guid>" in e)


def test_rss_item_url_taint_is_an_error() -> None:
    item = "<item><title>T</title><link>http://localhost:8000/a/</link></item>"
    errors, _ = _run_rss(_rss(item))
    assert any("dev artefact" in e for e in errors)


def test_a_non_permalink_guid_skips_the_url_checks() -> None:
    """An opaque identifier is not a URL, so URL-shaped SEO rules do not
    apply to it — flagging those would be noise on a valid feed."""
    item = (
        "<item><title>T</title><link>https://sebastienrousseau.com/a/</link>"
        '<guid isPermaLink="false">http://not-a-url-really</guid></item>'
    )
    _, warnings = _run_rss(_rss(item))
    assert not any("guid" in w and "https" in w for w in warnings)


def test_a_permalink_guid_is_checked_as_a_url() -> None:
    item = (
        "<item><title>T</title><link>https://sebastienrousseau.com/a/</link>"
        "<guid>http://sebastienrousseau.com/a/</guid></item>"
    )
    _, warnings = _run_rss(_rss(item))
    assert any("guid" in w for w in warnings), "http:// guid should warn"


# ---------------------------------------------------------------------------
# RSS items — content quality, all warnings
# ---------------------------------------------------------------------------


def test_short_description_and_bad_pubdate_are_warnings_not_errors() -> None:
    item = (
        "<item><title>T</title><link>https://sebastienrousseau.com/a/</link>"
        "<description>tiny</description><pubDate>2026-05-11</pubDate></item>"
    )
    errors, warnings = _run_rss(_rss(item))
    assert errors == []
    assert any("too short" in w for w in warnings)
    assert any("not RFC 822" in w for w in warnings)


def test_a_very_long_title_is_a_warning() -> None:
    item = f"<item><title>{'t' * 250}</title><link>https://sebastienrousseau.com/a/</link></item>"
    _, warnings = _run_rss(_rss(item))
    assert any("very long" in w for w in warnings)


def test_an_absent_description_is_not_reported() -> None:
    """Absent and too-short are different; only the latter is a defect."""
    item = "<item><title>T</title><link>https://sebastienrousseau.com/a/</link></item>"
    _, warnings = _run_rss(_rss(item))
    assert not any("too short" in w for w in warnings)


# ---------------------------------------------------------------------------
# Atom
# ---------------------------------------------------------------------------


def _atom(entries: str = "", feed_updated: str = "2026-05-11T06:06:06+00:00") -> ET.Element:
    return ET.fromstring(
        f'<feed xmlns="{ATOM}"><id>urn:x</id><title>T</title>'
        f"<updated>{feed_updated}</updated>{entries}</feed>"
    )


def _run_atom(root: ET.Element) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    vj._validate_atom(root, errors, warnings)
    return errors, warnings


def test_atom_feed_missing_required_elements_is_an_error() -> None:
    errors, _ = _run_atom(ET.fromstring(f'<feed xmlns="{ATOM}"></feed>'))
    for required in ("id", "title", "updated"):
        assert any(f"missing <{required}>" in e for e in errors)


def test_atom_feed_updated_must_be_rfc3339() -> None:
    _, warnings = _run_atom(_atom(feed_updated="Mon, 11 May 2026 06:06:06 +0000"))
    assert any("not RFC 3339" in w for w in warnings)


def test_atom_duplicate_entry_id_is_an_error() -> None:
    entry = (
        "<entry><id>urn:a</id><title>T</title>"
        "<updated>2026-05-11T06:06:06+00:00</updated>"
        "<summary>s</summary></entry>"
    )
    errors, _ = _run_atom(_atom(entry + entry))
    assert any("duplicate <id>" in e for e in errors)


def test_atom_entry_without_a_summary_is_a_warning() -> None:
    entry = (
        "<entry><id>urn:a</id><title>T</title><updated>2026-05-11T06:06:06+00:00</updated></entry>"
    )
    errors, warnings = _run_atom(_atom(entry))
    assert not any("summary" in e for e in errors)
    assert any("missing <summary>" in w for w in warnings)


def test_atom_entry_updated_must_be_rfc3339() -> None:
    entry = (
        "<entry><id>urn:a</id><title>T</title><updated>11 May 2026</updated>"
        "<summary>s</summary></entry>"
    )
    _, warnings = _run_atom(_atom(entry))
    assert any("entry[0] <updated> not RFC 3339" in w for w in warnings)


def test_atom_entry_id_taint_is_an_error() -> None:
    entry = (
        "<entry><id>http://127.0.0.1/a/</id><title>T</title>"
        "<updated>2026-05-11T06:06:06+00:00</updated><summary>s</summary></entry>"
    )
    errors, _ = _run_atom(_atom(entry))
    assert any("dev artefact" in e for e in errors)


def test_an_empty_atom_id_is_not_treated_as_a_duplicate() -> None:
    """Two entries missing an id must not be reported as colliding with
    each other — that would bury the real defect under a false one."""
    entry = (
        "<entry><title>T</title><updated>2026-05-11T06:06:06+00:00</updated>"
        "<summary>s</summary></entry>"
    )
    errors, _ = _run_atom(_atom(entry + entry))
    assert not any("duplicate <id>" in e for e in errors)


# ---------------------------------------------------------------------------
# Google News sitemap
# ---------------------------------------------------------------------------


NEWS = vj._NEWS_NS


def _news(
    title: str = "A headline", publication: str | None = "<name>N</name><language>en</language>"
):
    pub = f"<publication>{publication}</publication>" if publication else ""
    return ET.fromstring(f'<news xmlns="{NEWS}">{pub}<title>{title}</title></news>')


def test_news_missing_title_is_an_error() -> None:
    errors: list[str] = []
    vj._news_title(ET.fromstring(f'<news xmlns="{NEWS}"></news>'), 0, errors, [])
    assert any("missing <news:title>" in e for e in errors)


def test_news_over_long_title_is_a_warning() -> None:
    """Google truncates past 80 characters; that is advice, not invalidity."""
    errors: list[str] = []
    warnings: list[str] = []
    vj._news_title(_news(title="t" * 100), 0, errors, warnings)
    assert errors == []
    assert any("80-char" in w for w in warnings)


def test_news_missing_publication_is_an_error() -> None:
    errors: list[str] = []
    vj._news_publication(_news(publication=None), 0, errors)
    assert any("missing <news:publication>" in e for e in errors)


def test_a_complete_news_block_is_clean() -> None:
    errors: list[str] = []
    warnings: list[str] = []
    block = _news()
    vj._news_title(block, 0, errors, warnings)
    vj._news_publication(block, 0, errors)
    assert errors == []
    assert warnings == []


# ---------------------------------------------------------------------------
# Cross-cutting: the error/warning contract
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "item",
    [
        (
            "<item><title>T</title><link>https://sebastienrousseau.com/a/</link>"
            + "<description>tiny</description></item>"
        ),
        f"<item><title>{'t' * 250}</title><link>https://sebastienrousseau.com/a/</link></item>",
        (
            "<item><title>T</title><link>https://sebastienrousseau.com/a/</link>"
            + "<pubDate>nonsense</pubDate></item>"
        ),
    ],
)
def test_content_quality_issues_never_become_errors(item: str) -> None:
    """These are all 'a worse feed', not 'an invalid feed'. Promoting any of
    them to an error would fail the build on a publishable feed."""
    errors, warnings = _run_rss(_rss(item))
    assert errors == []
    assert warnings
