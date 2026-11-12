# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""postbuild_lib/meta_length.py: titles and descriptions fit search results."""

from __future__ import annotations

from pathlib import Path

from postbuild_lib.meta_length import (
    apply_meta_length,
    fit_description,
    fit_meta,
    fit_title,
    limits,
)

LONG = "First sentence about payments and ISO 20022 migration. " * 4


def _page(title: str, desc: str, lang: str = "en-GB", robots: str = "index, follow") -> str:
    return (
        f'<html lang="{lang}"><head><title>{title}</title><meta name="robots" content="{robots}">'
        f'<meta name="description" content="{desc}"><meta property="og:description" content="{desc}">'
        f'<meta property="og:title" content="{title}"></head></html>'
    )


def test_limits_by_script() -> None:
    assert limits("en-GB") == (60, 160) and limits("ja-JP") == (30, 80)
    assert limits("zh-Hant") == (30, 80) and limits("ko-KR") == (35, 100)


def test_title_drops_only_the_site_suffix() -> None:
    assert fit_title("A" * 50 + " | Sebastien Rousseau", 60) == "A" * 50
    assert fit_title("AI 标签 — Sebastien Rousseau", 12) == "AI 标签"
    assert fit_title("Short | Sebastien Rousseau", 60) == "Short | Sebastien Rousseau"
    assert fit_title("X" * 70, 60) == "X" * 70


def test_description_cuts_at_a_sentence_then_a_word() -> None:
    out = fit_description(LONG, 160)
    assert len(out) <= 160 and out.endswith("migration.")
    words = fit_description("word " * 60, 160)
    assert len(words) <= 160 and words.endswith("word…")
    assert fit_description("短" * 90, 80) == "短" * 79 + "…"
    assert fit_description("ok.", 160) == "ok."


def test_description_without_spaces_cuts_at_the_character() -> None:
    # A label before the only space must not swallow the description.
    out = fit_description("资金管理 — 按主题分类的文章: " + "短" * 90, 80)
    assert len(out) == 80 and out.endswith("短…")


def test_fit_meta_rewrites_title_mirrors_and_descriptions() -> None:
    title = "T" * 50 + " | Sebastien Rousseau"
    out = fit_meta(_page(title, LONG))
    assert "<title>" + "T" * 50 + "</title>" in out
    assert f'og:title" content="{"T" * 50}"' in out
    assert LONG not in out and out.count('migration."') == 2
    same = _page("Fine title", "Fine.")
    assert fit_meta(same) == same
    assert fit_meta("<p>no head</p>") == "<p>no head</p>"
    only_titles = fit_meta(_page(title, LONG), descriptions=False)
    assert LONG in only_titles and "<title>" + "T" * 50 + "</title>" in only_titles
    only_desc = fit_meta(_page(title, LONG), titles=False)
    assert f"<title>{title}</title>" in only_desc and LONG not in only_desc


def test_apply_skips_noindex_pages(tmp_path: Path) -> None:
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    (tmp_path / "a" / "index.html").write_text(_page("x", LONG), encoding="utf-8")
    hidden = _page("x", LONG, robots="noindex, follow")
    (tmp_path / "b" / "index.html").write_text(hidden, encoding="utf-8")
    assert apply_meta_length(tmp_path) == 1
    assert (tmp_path / "b" / "index.html").read_text(encoding="utf-8") == hidden
