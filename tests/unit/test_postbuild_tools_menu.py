# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""postbuild_lib/tools_menu.py and article_flags.py (plan C-4)."""

from __future__ import annotations

from pathlib import Path

from postbuild_lib.article_flags import flagged, load
from postbuild_lib.tools_menu import inject_tools_menu

HEAD = (
    '<link rel="canonical" href="https://sebastienrousseau.com/2026-01-01-my-post/">'
    '<meta property="og:title" content="My Post: A Subtitle">'
    '<meta name="description" content="A brief description of the article.">'
    '<script type="application/ld+json">{"@type":"BlogPosting"}</script>'
)
BODY = (
    '<section class="ap-hero"><h1>My Post</h1></section>'
    '<main id="main" class="content ap-section"><div class="wrap report-wrap"><p>body</p></div></main>'
)


def _ws2_page() -> str:
    return f'<html lang="en-GB"><head>{HEAD}</head><body>{BODY}</body></html>'


def test_menu_holds_share_links_save_pdf_cite_and_reuse() -> None:
    out = inject_tools_menu(_ws2_page())
    assert '<details class="article-tools"><summary>Share · Cite</summary>' in out
    assert "linkedin.com/feed/?shareActive=true" in out and "data-print" in out
    assert 'href="#cite-popover"' in out and 'href="#reuse-heading"' in out
    assert out.index("article-tools") < out.index("<p>body</p>")
    assert inject_tools_menu(out) == out


def test_menu_skips_other_pages_and_pages_without_a_canonical() -> None:
    assert inject_tools_menu("<p>plain page</p>") == "<p>plain page</p>"
    page = _ws2_page().replace('<link rel="canonical"', '<link rel="x"')
    assert inject_tools_menu(page) == page


def test_flags_switch_passes_off_and_default_on(tmp_path: Path) -> None:
    def add(html: str) -> str:
        return html + "!"

    assert flagged("share_rail", add, {"share_rail": False})("x") == "x"
    assert flagged("tools_menu", add, {"tools_menu": True})("x") == "x!"
    assert flagged("unknown", add, {})("x") == "x!"
    f = tmp_path / "f.yml"
    f.write_text("share_rail: false\ntools_menu: yes\n", encoding="utf-8")
    assert load(f) == {"share_rail": False, "tools_menu": True}
    assert load(tmp_path / "none.yml") == {}
    assert load()["tools_menu"] is True
    assert flagged("share_rail", add)("x") == "x"
