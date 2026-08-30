# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Per-locale news sitemaps: 48-hour window and a real publication name.

`/fr/news-sitemap.xml` shipped 84 KB of months-old entries naming the
publication "contact@sebastienrousseau.com (Sebastien Rousseau)" — the author
front-matter string, hard-coded in the renderer. A Google News sitemap must
carry only the last 48 hours, and <news:name> is the publication's name, not
a contact address.
"""

from __future__ import annotations

import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
sys.path.insert(0, str(ROOT / "scripts" / "generators"))

import build_lang_feeds as feeds

NOW = datetime(2026, 8, 19, 12, 0, 0, tzinfo=UTC)


def _entry(hours_old: float, url: str = "/x", title: str = "T") -> dict[str, object]:
    return {"url": url, "date": NOW - timedelta(hours=hours_old), "title": title}


@pytest.mark.parametrize(
    ("hours_old", "expected"),
    [
        (0, True),  # published now
        (47.9, True),  # just inside the window
        (48.1, False),  # just outside
        (360, False),  # 15 days — the real /fr/ regression
        (-1, True),  # 1 h in the future: tolerated timezone skew
        (-3, False),  # 3 h in the future: beyond tolerance
    ],
)
def test_only_the_last_48_hours_are_emitted(hours_old: float, expected: bool) -> None:
    xml = feeds.render_news_sitemap([_entry(hours_old)], "fr-FR", "Pub", now=NOW)
    assert ("<loc>/x</loc>" in xml) is expected


def test_publication_name_is_a_brand_not_an_email() -> None:
    xml = feeds.render_news_sitemap(
        [_entry(1)], "fr-FR", "Sebastien Rousseau — Édition française", now=NOW
    )
    assert "<news:name>Sebastien Rousseau — Édition française</news:name>" in xml
    assert "@" not in xml.split("<news:name>")[1].split("</news:name>")[0]


def test_publication_name_is_xml_escaped() -> None:
    xml = feeds.render_news_sitemap([_entry(1)], "en-GB", "Rousseau & Co <Research>", now=NOW)
    assert "<news:name>Rousseau &amp; Co &lt;Research&gt;</news:name>" in xml


def test_empty_window_still_renders_a_valid_document() -> None:
    """Nothing published in 48 h is the correct state, not an error."""
    xml = feeds.render_news_sitemap([_entry(500)], "fr-FR", "Pub", now=NOW)
    assert xml.startswith('<?xml version="1.0" encoding="UTF-8"?>')
    assert "</urlset>" in xml
    assert "<url>" not in xml


def test_resolve_pub_name_falls_back_to_the_brand(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        feeds._lang_registry, "load_strings", lambda _c: (_ for _ in ()).throw(OSError)
    )
    assert feeds._resolve_pub_name("xx") == "Sebastien Rousseau Research"


def test_resolve_pub_name_prefers_the_localised_channel_title(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        feeds._lang_registry, "load_strings", lambda _c: {"feeds.channelTitle": "Édition"}
    )
    assert feeds._resolve_pub_name("fr") == "Édition"


def test_entry_without_a_datetime_is_dropped_not_crashed() -> None:
    xml = feeds.render_news_sitemap([{"url": "/x", "date": None, "title": "T"}], "en-GB", "P", NOW)
    assert "<url>" not in xml
