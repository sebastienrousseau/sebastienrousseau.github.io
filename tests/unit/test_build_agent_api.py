# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Unit coverage for build_agent_api — Phase 1.3.

build_agent_api.py emits the static JSON agent/crawler API (post + topic graph)
under /api/agents/. It was untested. Cover the pure keyword/word-count/topic-
index helpers and the index metadata shape.
"""

from __future__ import annotations

from pathlib import Path

import build_agent_api as api

# --- _split_keywords -------------------------------------------------------


def test_split_keywords_strips_and_drops_empty() -> None:
    assert api._split_keywords({"keywords": "a, b ,, c "}) == ["a", "b", "c"]


def test_split_keywords_missing_is_empty() -> None:
    assert api._split_keywords({}) == []
    assert api._split_keywords({"keywords": ""}) == []


# --- _word_count -----------------------------------------------------------


def test_word_count_reads_rendered_page(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(api, "PUBLIC", tmp_path)
    d = tmp_path / "2026-06-29-x"
    d.mkdir()
    (d / "index.html").write_text('<script>{"wordCount":1234}</script>', encoding="utf-8")
    assert api._word_count("2026-06-29-x") == 1234


def test_word_count_missing_file_is_none(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(api, "PUBLIC", tmp_path)
    assert api._word_count("nope") is None


def test_word_count_no_marker_is_none(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(api, "PUBLIC", tmp_path)
    d = tmp_path / "s"
    d.mkdir()
    (d / "index.html").write_text("<p>no wordcount here</p>", encoding="utf-8")
    assert api._word_count("s") is None


# --- _topic_index ----------------------------------------------------------


def test_topic_index_inverts_topics(monkeypatch) -> None:
    monkeypatch.setattr(
        api,
        "TOPICS",
        {"quantum": {"slugs": ["a", "b"]}, "payments": {"slugs": ["b"]}},
    )
    idx = api._topic_index()
    assert idx["a"] == ["quantum"]
    assert sorted(idx["b"]) == ["payments", "quantum"]  # b belongs to both


# --- build_index -----------------------------------------------------------


def test_build_index_shape() -> None:
    idx = api.build_index()
    assert idx["version"] == 1
    assert idx["base_url"].endswith("/api/agents/")
    assert idx["license"] == "https://creativecommons.org/licenses/by/4.0/"
    assert idx["name"].startswith("Sebastien Rousseau")
    assert idx["author"]["url"] == "https://sebastienrousseau.com/about/"


def test_collect_posts_emits_canonical_pretty_urls_and_word_count(
    tmp_path: Path, monkeypatch
) -> None:
    posts_dir = tmp_path / "_posts"
    pub_dir = tmp_path / "public"
    posts_dir.mkdir()
    pub_dir.mkdir()
    stem = "2026-06-29-quantum-resilience"
    (posts_dir / f"{stem}.md").write_text("---\ntitle: Quantum\n---\nbody\n", encoding="utf-8")
    art_dir = pub_dir / stem
    art_dir.mkdir()
    (art_dir / "index.html").write_text('<script>{"wordCount":850}</script>', encoding="utf-8")

    monkeypatch.setattr(api, "POSTS", posts_dir)
    monkeypatch.setattr(api, "PUBLIC", pub_dir)
    sig_dir = tmp_path / "sigstore-bundles"
    sig_dir.mkdir()
    (sig_dir / f"{stem}.sigstore.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(api, "SIGSTORE", sig_dir)
    monkeypatch.setattr(api, "TOPICS", {"pqc": {"slugs": [stem]}})
    monkeypatch.setattr(
        api,
        "read_frontmatter",
        lambda s: (
            {"title": "Quantum", "description": "Desc", "keywords": "pqc, rust"}
            if s == stem
            else {}
        ),
    )

    records = api.collect_posts()
    assert len(records) == 1
    rec = records[0]
    assert rec["url"] == f"https://sebastienrousseau.com/{stem}/"
    assert rec["wordCount"] == 850
    assert rec["topics"] == ["pqc"]
    assert rec["keywords"] == ["pqc", "rust"]
    assert isinstance(rec["content_sha256"], str) and len(str(rec["content_sha256"])) == 64
    assert rec["sigstore_bundle"] == f"https://sebastienrousseau.com/sigstore/{stem}.sigstore.json"


def test_sigstore_bundle_url_returns_none_when_absent(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(api, "SIGSTORE", tmp_path / "no-sigstore")
    monkeypatch.setattr(api, "PUBLIC", tmp_path / "no-public")
    assert api._sigstore_bundle_url("2026-06-29-none") is None
