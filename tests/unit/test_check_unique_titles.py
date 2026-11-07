# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Unit tests for scripts/seo_and_audit/check_unique_titles.py."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "check_unique_titles",
    ROOT / "scripts" / "seo_and_audit" / "check_unique_titles.py",
)
assert SPEC and SPEC.loader
cut = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cut)


def _write_page(
    base: Path,
    rel: str,
    title: str,
    desc: str,
    *,
    robots: str = "index, follow",
    refresh: bool = False,
    canonical: str | None = None,
) -> None:
    p = base / rel / "index.html" if rel else base / "index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    url = f"https://sebastienrousseau.com/{rel}/" if rel else "https://sebastienrousseau.com/"
    canon = canonical or url
    ref_tag = f'<meta http-equiv="refresh" content="0; url={canon}">' if refresh else ""
    p.write_text(
        f"<!DOCTYPE html><html><head>"
        f"<title>{title}</title>"
        f'<meta name="description" content="{desc}">'
        f'<meta name="robots" content="{robots}">'
        f'<link rel="canonical" href="{canon}">'
        f"{ref_tag}</head><body></body></html>",
        encoding="utf-8",
    )


def test_unique_pages_pass(tmp_path: Path) -> None:
    _write_page(tmp_path, "articles", "Articles · Sebastien Rousseau", "Page 1.")
    _write_page(
        tmp_path,
        "articles/page/2",
        "Articles, page 2 of 5 · Sebastien Rousseau",
        "Page 2.",
    )
    assert cut.scan_tree(tmp_path) == []
    assert cut.main(["--base-dir", str(tmp_path)]) == 0


def test_duplicate_title_and_description_fail(tmp_path: Path) -> None:
    _write_page(tmp_path, "articles", "Same Title", "Same Description")
    _write_page(tmp_path, "articles/page/2", "Same Title", "Same Description")
    errors = cut.scan_tree(tmp_path)
    assert len(errors) == 2
    assert any("duplicate <title>" in e for e in errors)
    assert any("duplicate description" in e for e in errors)
    assert cut.main(["--base-dir", str(tmp_path)]) == 1


def test_noindex_refresh_labs_and_cross_locale_are_exempt(tmp_path: Path) -> None:
    _write_page(tmp_path, "articles", "Articles", "Desc")
    _write_page(tmp_path, "fr/articles", "Articles", "Desc")
    _write_page(tmp_path, "labs/demo", "Articles", "Desc")
    _write_page(tmp_path, "draft", "Articles", "Desc", robots="noindex, nofollow")
    _write_page(tmp_path, "old", "Articles", "Desc", refresh=True)
    _write_page(
        tmp_path,
        "alias",
        "Articles",
        "Desc",
        canonical="https://sebastienrousseau.com/articles/",
    )
    assert cut.scan_tree(tmp_path) == []
