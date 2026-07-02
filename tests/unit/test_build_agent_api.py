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
    assert "creativecommons.org" in idx["license"]
    assert idx["name"].startswith("Sebastien Rousseau")
