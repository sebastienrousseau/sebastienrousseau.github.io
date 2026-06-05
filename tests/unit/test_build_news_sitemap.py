"""Unit tests for scripts/generators/build_news_sitemap.py."""

from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from datetime import UTC, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "generators"))
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

import _lang_registry
import build_news_sitemap as bns


def test_xml_escape():
    assert bns.xml_escape("A & B < C > D \" E ' F") == "A &amp; B &lt; C &gt; D &quot; E &apos; F"
    assert bns.xml_escape("A &amp; B") == "A &amp; B"


def test_iso8601():
    d = datetime(2026, 6, 4, 6, 6, 6, tzinfo=UTC)
    assert bns.iso8601(d) == "2026-06-04T06:06:06+00:00"


def test_main_generates_correct_sitemap(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(bns, "PUBLIC", tmp_path / "public")

    posts_dir = tmp_path / "_posts"
    posts_dir.mkdir()

    now = datetime.now(tz=UTC)
    yesterday = now - timedelta(hours=24)
    yesterday_str = yesterday.strftime("%Y-%m-%d")

    en_post = posts_dir / f"{yesterday_str}-mock-english-post.md"
    en_post.write_text(
        "---\n"
        'title: "Mock English Post"\n'
        'keywords: "crypto, banking"\n'
        "---\n"
        "Body content",
        encoding="utf-8",
    )

    five_days_ago = now - timedelta(days=5)
    five_days_ago_str = five_days_ago.strftime("%Y-%m-%d")
    old_post = posts_dir / f"{five_days_ago_str}-old-post.md"
    old_post.write_text(
        "---\n" 'title: "Old Post"\n' 'keywords: "legacy"\n' "---\n" "Body content",
        encoding="utf-8",
    )

    fr_dir = posts_dir / "fr"
    fr_dir.mkdir()

    i18n_dir = tmp_path / "_data" / "i18n" / "fr"
    i18n_dir.mkdir(parents=True)

    (i18n_dir / "slugs.json").write_text(
        "{\n"
        '  "static": {},\n'
        '  "articles": {\n'
        f'    "{yesterday_str}-mock-english-post": "{yesterday_str}-mock-french-post"\n'
        "  }\n"
        "}",
        encoding="utf-8",
    )

    (i18n_dir / "strings.json").write_text(
        "{\n" '  "feeds.channelTitle": "Sebastien Rousseau — Edition Francaise"\n' "}",
        encoding="utf-8",
    )

    fr_post = fr_dir / f"{yesterday_str}-mock-french-post.md"
    fr_post.write_text(
        "---\n" 'title: "Mock French Post"\n' 'keywords: "banque"\n' "---\n" "Contenu",
        encoding="utf-8",
    )

    monkeypatch.setattr(_lang_registry, "ROOT", tmp_path)
    monkeypatch.setattr(_lang_registry, "I18N_DIR", tmp_path / "_data" / "i18n")

    count = bns.build_news_sitemap()
    assert count == 2

    # Assert main() exits with 0 on success
    assert bns.main() == 0

    xml_path = tmp_path / "public" / "news-sitemap.xml"
    assert xml_path.is_file()

    root = ET.parse(xml_path).getroot()
    assert root.tag == "{http://www.sitemaps.org/schemas/sitemap/0.9}urlset"

    urls = root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url")
    assert len(urls) == 2

    locs = [u.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text for u in urls]
    assert f"https://sebastienrousseau.com/{yesterday_str}-mock-english-post/" in locs
    assert f"https://sebastienrousseau.com/fr/{yesterday_str}-mock-french-post/" in locs

    fr_url = next(
        u
        for u in urls
        if f"fr/{yesterday_str}-mock-french-post"
        in u.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text
    )
    news = fr_url.find("{http://www.google.com/schemas/sitemap-news/0.9}news")
    assert news is not None

    pub = news.find("{http://www.google.com/schemas/sitemap-news/0.9}publication")
    assert (
        pub.find("{http://www.google.com/schemas/sitemap-news/0.9}name").text
        == "Sebastien Rousseau — Edition Francaise"
    )
    assert pub.find("{http://www.google.com/schemas/sitemap-news/0.9}language").text == "fr"

    title = news.find("{http://www.google.com/schemas/sitemap-news/0.9}title").text
    assert title == "Mock French Post"

    keywords = news.find("{http://www.google.com/schemas/sitemap-news/0.9}keywords").text
    assert keywords == "banque"


def test_main_error_handling(monkeypatch):
    def mock_build_news_sitemap():
        raise Exception("Mock build failure")

    monkeypatch.setattr(bns, "build_news_sitemap", mock_build_news_sitemap)
    assert bns.main() == 1
