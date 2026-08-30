# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Unit coverage for build_changelog — Phase 5 (changelog + what's-new + status).

Exercises the pure, deterministic core: entry collection, month grouping,
stable ordering, HTML escaping, the homepage-strip injection, and the
timestamp-free status JSON. Git-derived PR links are intentionally not
covered here — they are an optional, environment-dependent enrichment.
"""

from __future__ import annotations

import json
from pathlib import Path

import build_changelog as bc


def _write_post(d: Path, slug: str, title: str, desc: str = "") -> None:
    d.joinpath(f"{slug}.md").write_text(
        f'---\ntitle: "{title}"\ndescription: "{desc}"\n---\nbody\n',
        encoding="utf-8",
    )


# --- collect_entries -------------------------------------------------------


def test_collect_entries_sorted_newest_first(tmp_path: Path) -> None:
    _write_post(tmp_path, "2024-01-15-alpha", "Alpha")
    _write_post(tmp_path, "2026-07-03-gamma", "Gamma")
    _write_post(tmp_path, "2026-06-25-beta", "Beta")
    _write_post(tmp_path, "index", "Home page")  # non-dated → skipped
    _write_post(tmp_path, "README", "Readme")  # non-dated → skipped

    entries = bc.collect_entries(tmp_path)

    assert [e.slug for e in entries] == [
        "2026-07-03-gamma",
        "2026-06-25-beta",
        "2024-01-15-alpha",
    ]
    assert entries[0].iso == "2026-07-03"
    assert entries[0].title == "Gamma"


def test_collect_entries_stable_tiebreak_same_day(tmp_path: Path) -> None:
    _write_post(tmp_path, "2026-07-03-aaa", "A")
    _write_post(tmp_path, "2026-07-03-zzz", "Z")
    entries = bc.collect_entries(tmp_path)
    # Same date → slug descending, deterministic.
    assert [e.slug for e in entries] == ["2026-07-03-zzz", "2026-07-03-aaa"]


def test_collect_entries_missing_dir_is_empty(tmp_path: Path) -> None:
    assert bc.collect_entries(tmp_path / "nope") == []


# --- month grouping --------------------------------------------------------


def test_month_label() -> None:
    assert bc._month_label("2026-07-03") == "July 2026"
    assert bc._month_label("2024-01-01") == "January 2024"


def test_group_by_month_preserves_order(tmp_path: Path) -> None:
    _write_post(tmp_path, "2026-07-03-b", "B")
    _write_post(tmp_path, "2026-07-01-a", "A")
    _write_post(tmp_path, "2026-06-30-c", "C")
    grouped = bc.group_by_month(bc.collect_entries(tmp_path))

    assert [label for label, _ in grouped] == ["July 2026", "June 2026"]
    assert [e.slug for e in grouped[0][1]] == ["2026-07-03-b", "2026-07-01-a"]
    assert [e.slug for e in grouped[1][1]] == ["2026-06-30-c"]


# --- rendering / escaping --------------------------------------------------


def test_render_changelog_body_structure_and_escaping() -> None:
    entries = [
        bc.Entry("2026-07-03", "2026-07-03-x", "Quantum & <Risk>", "A <deck>"),
    ]
    out = bc.render_changelog_body(entries, "Changelog", "The lede", prs={})
    assert out.count("<h1>") == 1
    assert "<h2>July 2026</h2>" in out
    assert 'href="/2026-07-03-x/"' in out
    assert "Quantum &amp; &lt;Risk&gt;" in out  # title escaped
    assert "A &lt;deck&gt;" in out  # description escaped
    assert '<time datetime="2026-07-03"' in out
    assert 'id="changelog-count">1<' in out


def test_render_changelog_body_pr_backlink() -> None:
    entries = [bc.Entry("2026-07-03", "2026-07-03-x", "X", "")]
    out = bc.render_changelog_body(entries, "Changelog", "L", prs={"2026-07-03-x": 258})
    assert "/pull/258" in out
    assert ">#258<" in out


def test_whats_new_section_limits_and_links() -> None:
    entries = [
        bc.Entry(f"2026-07-{d:02d}", f"2026-07-{d:02d}-p{d}", f"Post {d}", "") for d in range(1, 10)
    ]
    entries.sort(key=lambda e: (e.iso, e.slug), reverse=True)
    out = bc.render_whats_new_section(
        entries, {"whatsNew.title": "What's new", "whatsNew.cta": "View the changelog"}
    )
    assert out.count("<li") == bc.WHATS_NEW_LIMIT  # capped
    assert 'href="/changelog/"' in out
    assert 'aria-labelledby="whats-new-h"' in out
    assert out.count("<h2") == 1


# --- homepage injection ----------------------------------------------------


def test_inject_whats_new_places_after_anchor() -> None:
    home = (
        '<main id="main"><div class="home-content"><section class="offer">x</section></div></main>'
    )
    section = bc.render_whats_new_section([bc.Entry("2026-07-03", "2026-07-03-x", "X", "")], {})
    out, injected = bc.inject_whats_new(home, section)
    assert injected
    anchor = '<div class="home-content">'
    assert (
        out.index(anchor) < out.index('aria-labelledby="whats-new-h"') < out.index('class="offer"')
    )


def test_inject_whats_new_is_idempotent() -> None:
    home = '<div class="home-content"><p>x</p></div>'
    section = bc.render_whats_new_section([bc.Entry("2026-07-03", "2026-07-03-x", "X", "")], {})
    once, first = bc.inject_whats_new(home, section)
    twice, second = bc.inject_whats_new(once, section)
    assert first is True and second is False
    assert once == twice


def test_inject_whats_new_failsoft_without_anchor() -> None:
    home = "<main><p>no anchor here</p></main>"
    out, injected = bc.inject_whats_new(home, "<section>x</section>")
    assert injected is False
    assert out == home


# --- status.json (deterministic, no timestamp) -----------------------------


def test_status_json_has_no_timestamp_and_is_deterministic() -> None:
    entries = [bc.Entry("2026-07-03", "2026-07-03-x", "Latest", "")]
    first = bc.render_status_json(entries)
    second = bc.render_status_json(entries)
    assert first == second  # byte-reproducible

    data = json.loads(first)
    assert data["status"] == "operational"
    assert data["content"]["articles"] == 1
    assert data["content"]["latest"]["slug"] == "2026-07-03-x"
    # No wall-clock leakage into the artifact.
    for banned in ("timestamp", "generated", "generatedAt", "now", "date"):
        assert (
            banned not in first.lower() or banned == "date"
        )  # 'latest.date' is a content field, allowed
    assert '"date": "2026-07-03"' in first


def test_status_json_empty_corpus() -> None:
    data = json.loads(bc.render_status_json([]))
    assert data["content"]["articles"] == 0
    assert data["content"]["latest"] is None


def test_status_badge_is_same_origin_svg() -> None:
    svg = bc.render_status_badge()
    assert svg.startswith("<svg")
    assert "passing" in svg
    assert "<script" not in svg  # CSP-clean, no inline JS
