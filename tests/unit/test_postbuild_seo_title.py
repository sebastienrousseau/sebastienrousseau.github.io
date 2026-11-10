# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""postbuild_lib/seo_title.py: long <title>s take the post's seo_title."""

from __future__ import annotations

from pathlib import Path

from postbuild_lib.seo_title import SUFFIX, apply_seo_title, choose, limit_for, seo_titles

URL = "https://sebastienrousseau.com/2026-05-16-cloud"
LONG = "The Best Cloud Infrastructure Architecture in 2026: An AI-Native, Multi-Cloud Blueprint"


def _page(title: str, lang: str = "en-GB", canonical: str = URL + "/") -> str:
    return (
        f'<html lang="{lang}"><head><title>{title}</title>'
        f'<link rel="canonical" href="{canonical}"><meta property="og:title" content="{title}"></head>'
        f"<body><h1>{title}</h1></body></html>"
    )


def test_long_title_takes_the_seo_title_and_keeps_h1_and_og() -> None:
    out = apply_seo_title(_page(LONG), {URL: "Cloud Architecture for Banks: A Blueprint"})
    assert "<title>Cloud Architecture for Banks: A Blueprint</title>" in out
    assert f"<h1>{LONG}</h1>" in out and f'og:title" content="{LONG}"' in out


def test_suffix_only_when_it_fits() -> None:
    assert choose(LONG, "Short title", 60) == "Short title" + SUFFIX
    seo = "x" * 50
    assert choose(LONG, seo, 60) == seo


def test_short_titles_missing_or_overlong_seo_titles_are_kept() -> None:
    assert choose("A short title", "Other", 60) is None
    assert choose(LONG, "", 60) is None
    assert choose(LONG, "y" * 61, 60) is None
    page = _page(LONG)
    assert apply_seo_title(page, {}) == page
    short = _page("Short")
    assert apply_seo_title(short, {URL: "Other title"}) == short
    assert apply_seo_title("<p>no head</p>", {URL: "x"}) == "<p>no head</p>"


def test_cjk_and_korean_limits() -> None:
    assert limit_for("ja-JP") == 30 and limit_for("zh-Hans") == 30 and limit_for("ko-KR") == 35
    assert limit_for("fr-FR") == 60
    title = "量子安全な決済インフラストラクチャへの移行に関する実践的なガイドと今後の展望について"
    out = apply_seo_title(_page(title, "ja-JP"), {URL: "量子安全な決済への移行ガイド"})
    assert "<title>量子安全な決済への移行ガイド</title>" in out


def test_titles_are_escaped_and_matched_without_index_html() -> None:
    out = apply_seo_title(_page(LONG, canonical=URL + "/index.html"), {URL: "R&D in payments"})
    assert "<title>R&amp;D in payments" in out


def test_seo_titles_reads_front_matter(tmp_path: Path) -> None:
    (tmp_path / "fr").mkdir()
    (tmp_path / "a.md").write_text(
        f'---\ntitle: "x"\npermalink: "{URL}"\nseo_title: "Say \\"hi\\""\n---\nbody\n',
        encoding="utf-8",
    )
    (tmp_path / "fr" / "b.md").write_text(
        '---\npermalink: "https://x/fr/b"\n---\n', encoding="utf-8"
    )
    (tmp_path / "c.md").write_text("no front matter", encoding="utf-8")
    (tmp_path / "fr" / "c.md").write_text('---\nseo_title: "Court"\n---\n', encoding="utf-8")
    assert seo_titles(tmp_path) == {
        URL: 'Say "hi"',
        "https://sebastienrousseau.com/a": 'Say "hi"',
        "https://sebastienrousseau.com/fr/c": "Court",
    }
    assert seo_titles()  # the real posts carry seo_titles
