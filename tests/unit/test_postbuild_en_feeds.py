# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""The root feeds carry English articles only, every one of them.

ssg's root rss.xml held the 50 newest posts across 35 languages, so English
readers got one or two English items, and which translation came first
followed ssg's file-walk order. feed.json parsed short month names only and
dropped every post dated "October 28, 2026". These tests pin both.
"""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
from postbuild_lib import en_feeds
from postbuild_lib.en_feeds import write_json_feed

BASE = "https://sebastienrousseau.com"

SSG_RSS = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Site &amp; title</title>
    <link>https://sebastienrousseau.com</link>
    <atom:link href="https://sebastienrousseau.com/rss.xml" rel="self" type="application/rss+xml"/>
    <item>
      <title>FCA (ta)</title>
      <link>https://sebastienrousseau.com/ta/2026-10-28-x/index.html</link>
    </item>
    <item>
      <title>FCA</title>
      <link>https://sebastienrousseau.com/2026-10-28-fca</link>
    </item>
  </channel>
</rss>
"""

SSG_ATOM = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>MySsgSite</title>
  <entry>
    <title>FCA (fr)</title>
    <link href="https://sebastienrousseau.com/fr/2026-10-28-y/"/>
  </entry>
</feed>
"""


def _post(posts: Path, stem: str, date: str, title: str = "T", extra: str = "") -> None:
    url = f'url: "{BASE}/{stem}"\n' if stem[:1].isdigit() else ""
    (posts / f"{stem}.md").write_text(
        f'---\ntitle: "{title}"\ndate: "{date}"\n{url}{extra}---\nBody.\n', encoding="utf-8"
    )


@pytest.fixture
def site(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.chdir(tmp_path)
    posts = tmp_path / "_posts"
    (posts / "ta").mkdir(parents=True)
    _post(posts, "2026-10-28-fca", "October 28, 2026", "FCA & AI", 'banner: "https://x/b.webp"\n')
    _post(posts, "2026-10-28-other", "Oct 28, 2026", "Other")
    _post(posts, "2026-06-02-june", "June 2, 2026", "June")
    _post(posts, "2026-05-12-may", "2026-05-12", "May", 'keywords: "AI, ai, AI, risk"\n')
    _post(posts, "about", "May 1, 2026", "About")  # undated page, not an article
    _post(posts / "ta", "2026-10-28-x", "October 28, 2026", "FCA (ta)")
    (posts / "2026-01-01-untitled.md").write_text('---\ndate: "Jan 1, 2026"\n---\n')
    public = tmp_path / "public"
    public.mkdir()
    (public / "rss.xml").write_text(SSG_RSS, encoding="utf-8")
    (public / "atom.xml").write_text(SSG_ATOM, encoding="utf-8")
    return public


def test_entries_are_english_dated_titled_and_ordered(site: Path) -> None:
    entries = en_feeds.english_entries(Path("_posts"))
    assert [e.stem for e in entries] == [
        "2026-10-28-other",
        "2026-10-28-fca",
        "2026-06-02-june",
        "2026-05-12-may",
    ]
    may = entries[-1]
    assert may.keywords == ("AI", "ai", "risk")
    assert may.url == f"{BASE}/2026-05-12-may"


def test_unparseable_date_stops_the_build(site: Path) -> None:
    _post(Path("_posts"), "2026-02-02-bad", "2nd Feb 2026")
    with pytest.raises(ValueError, match=r"2026-02-02-bad\.md: unparseable"):
        en_feeds.english_entries(Path("_posts"))


def test_root_rss_and_atom_carry_every_english_article_only(site: Path) -> None:
    assert en_feeds.write_en_xml_feeds(site, en_feeds.english_entries(Path("_posts"))) == 2
    rss = (site / "rss.xml").read_text(encoding="utf-8")
    channel = ET.fromstring(rss).find("channel")
    assert channel is not None
    assert channel.findtext("title") == "Site & title"  # ssg's header is kept
    links = [i.findtext("link") for i in channel.iter("item")]
    assert links == [
        f"{BASE}/2026-10-28-other",
        f"{BASE}/2026-10-28-fca",
        f"{BASE}/2026-06-02-june",
        f"{BASE}/2026-05-12-may",
    ]
    fca = channel.findall("item")[1]
    assert fca.findtext("title") == "FCA & AI"
    assert fca.findtext("guid") == f"{BASE}/2026-10-28-fca"
    assert fca.findtext("pubDate") == "Wed, 28 Oct 2026 00:00:00 +0000"
    enclosure = fca.find("enclosure")
    assert enclosure is not None and enclosure.get("url") == "https://x/b.webp"
    atom = ET.fromstring((site / "atom.xml").read_text(encoding="utf-8"))
    ns = {"a": "http://www.w3.org/2005/Atom"}
    hrefs = [link.get("href") for link in atom.findall("a:entry/a:link", ns)]
    assert hrefs == links
    assert "/ta/" not in rss and "/fr/" not in (site / "atom.xml").read_text()


def test_a_missing_feed_is_skipped_and_a_broken_one_refused(site: Path) -> None:
    (site / "atom.xml").unlink()
    assert en_feeds.write_en_xml_feeds(site, []) == 1
    assert re.search(r"<item>", (site / "rss.xml").read_text()) is None
    (site / "rss.xml").write_text("<rss><channel>", encoding="utf-8")
    with pytest.raises(ValueError, match="no </channel>"):
        en_feeds.write_en_xml_feeds(site, [])


def test_json_feed_has_the_same_articles(site: Path) -> None:
    write_json_feed(site)
    feed = json.loads((site / "feed.json").read_text(encoding="utf-8"))
    assert [i["url"] for i in feed["items"]] == [
        f"{BASE}/2026-10-28-other/",
        f"{BASE}/2026-10-28-fca/",
        f"{BASE}/2026-06-02-june/",
        f"{BASE}/2026-05-12-may/",
    ]
    assert feed["items"][1]["date_published"] == "2026-10-28T00:00:00+00:00"


def test_write_en_feeds_writes_all_three_from_one_set(site: Path) -> None:
    en_feeds.write_en_feeds(site)
    rss = (site / "rss.xml").read_text(encoding="utf-8")
    feed = json.loads((site / "feed.json").read_text(encoding="utf-8"))
    assert rss.count("<item>") == len(feed["items"]) == 4
    assert (site / "atom.xml").read_text(encoding="utf-8").count("<entry>") == 4
