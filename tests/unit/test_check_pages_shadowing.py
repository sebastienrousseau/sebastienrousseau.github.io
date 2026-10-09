# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""check_pages_shadowing: a project Pages site must not own a published path."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "seo_and_audit"))

import check_pages_shadowing as cps  # type: ignore[import-not-found]

SITEMAP = """<urlset>
<url><loc>https://sebastienrousseau.com/</loc></url>
<url><loc>https://sebastienrousseau.com/iso20022-mcp/</loc></url>
<url><loc>https://sebastienrousseau.com/fr/iso20022-mcp/</loc></url>
<url><loc> https://sebastienrousseau.com/Articles/index.html </loc></url>
</urlset>"""


def test_top_level_paths_takes_the_first_segment_only() -> None:
    assert cps.top_level_paths(SITEMAP) == {"iso20022-mcp", "fr", "articles"}


def test_the_2026_10_07_collision_is_reported() -> None:
    hits = cps.shadowed(
        ["iso20022-mcp", "passmcp", "sebastienrousseau.github.io"],
        cps.top_level_paths(SITEMAP),
        "sebastienrousseau.github.io",
    )
    assert hits == ["iso20022-mcp"]


def test_the_user_site_itself_is_never_a_collision() -> None:
    assert (
        cps.shadowed(
            ["sebastienrousseau.github.io"],
            {"sebastienrousseau.github.io"},
            "sebastienrousseau.github.io",
        )
        == []
    )


def test_main_fails_on_a_collision_and_passes_without(tmp_path, capsys) -> None:
    sitemap = tmp_path / "sitemap.xml"
    sitemap.write_text(SITEMAP, encoding="utf-8")
    repos = tmp_path / "repos.txt"
    repos.write_text("iso20022-mcp\nother\n", encoding="utf-8")
    assert cps.main(["--repos", str(repos), "--sitemap", str(sitemap)]) == 1
    assert "/iso20022-mcp/" in capsys.readouterr().out
    repos.write_text("other\n", encoding="utf-8")
    assert cps.main(["--repos", str(repos), "--sitemap", str(sitemap)]) == 0


def test_an_empty_sitemap_is_a_failure_not_a_pass(tmp_path) -> None:
    sitemap = tmp_path / "sitemap.xml"
    sitemap.write_text("<urlset></urlset>", encoding="utf-8")
    repos = tmp_path / "repos.txt"
    repos.write_text("x\n", encoding="utf-8")
    assert cps.main(["--repos", str(repos), "--sitemap", str(sitemap)]) == 1
