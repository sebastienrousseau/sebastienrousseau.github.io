# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""scripts/seo_and_audit/indexnow_ping.py, with a fake transport."""

from __future__ import annotations

import json
from pathlib import Path

import indexnow_ping as ix
import pytest

OLD = "<urlset><url><loc>https://sebastienrousseau.com/a/</loc><lastmod>2026-11-01</lastmod></url><url><loc>https://sebastienrousseau.com/b/</loc><lastmod>2026-11-01</lastmod></url></urlset>"
NEW = "<urlset><url><loc>https://sebastienrousseau.com/a/</loc><lastmod>2026-11-01</lastmod></url><url><loc>https://sebastienrousseau.com/b/</loc><lastmod>2026-11-09</lastmod></url><url><loc>https://sebastienrousseau.com/c/</loc></url></urlset>"


class Fake:
    def __init__(self, status: int = 200) -> None:
        self.status, self.calls = status, []

    def __call__(self, url: str, data: bytes) -> int:
        self.calls.append((url, json.loads(data)))
        return self.status


def test_changed_takes_new_and_moved_urls() -> None:
    assert ix.changed(ix.entries(NEW), ix.entries(OLD)) == [
        "https://sebastienrousseau.com/b/",
        "https://sebastienrousseau.com/c/",
    ]


def test_ping_posts_the_key_location_and_urls() -> None:
    fake = Fake()
    assert ix.ping("k123", ["https://sebastienrousseau.com/c/"], fake) == 200
    url, body = fake.calls[0]
    assert url == ix.ENDPOINT and body["keyLocation"] == "https://sebastienrousseau.com/k123.txt"
    assert body["host"] == "sebastienrousseau.com" and body["urlList"] == [
        "https://sebastienrousseau.com/c/"
    ]
    assert ix.ping("", ["x"], fake) == 0 and ix.ping("k", [], fake) == 0


def test_payload_caps_the_list() -> None:
    body = json.loads(ix.payload("k", [f"u{i}" for i in range(ix.MAX_URLS + 5)]))
    assert len(body["urlList"]) == ix.MAX_URLS


def test_sitemap_index_is_followed(tmp_path: Path) -> None:
    (tmp_path / "sitemap-en.xml").write_text(NEW, encoding="utf-8")
    (tmp_path / "sitemap.xml").write_text(
        "<sitemapindex><sitemap><loc>https://sebastienrousseau.com/sitemap-en.xml</loc></sitemap></sitemapindex>",
        encoding="utf-8",
    )
    assert len(ix.read_entries(tmp_path / "sitemap.xml")) == 3
    assert ix.read_entries(tmp_path / "missing.xml") == {}


def test_main_skips_without_a_key_and_never_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    new, old = tmp_path / "new.xml", tmp_path / "old.xml"
    new.write_text(NEW, encoding="utf-8")
    old.write_text(OLD, encoding="utf-8")
    monkeypatch.delenv("INDEXNOW_KEY", raising=False)
    fake = Fake()
    assert ix.main(["--sitemap", str(new), "--previous", str(old)], fake) == 0 and fake.calls == []
    monkeypatch.setenv("INDEXNOW_KEY", "k123")
    bad = Fake(500)
    assert ix.main(["--sitemap", str(new), "--previous", str(old)], bad) == 0
    assert len(bad.calls[0][1]["urlList"]) == 2
    assert (
        ix.main(["--sitemap", str(new), "--previous", str(old), "--write-key", str(tmp_path)]) == 0
    )
    assert (tmp_path / "k123.txt").read_text(encoding="utf-8") == "k123"
    assert ix.write_key_file(tmp_path, "") is None
