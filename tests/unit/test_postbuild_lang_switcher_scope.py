# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""postbuild_lib/lang_switcher_scope.py: indexed pages link indexed locales."""

from __future__ import annotations

from postbuild_lib.lang_switcher_scope import MORE_LABEL, is_noindex, more_item, scope_switcher

INDEXED = frozenset({"en", "fr"})


def _item(code: str) -> str:
    return f' <a class="ap-lang-item" href="/{code}/" data-lang="{code}" role="menuitem"><span aria-hidden="true">x</span> {code}</a>'


def _page(robots: str = "index, follow") -> str:
    grid = "".join(_item(c) for c in ("en", "fr", "ar", "yo"))
    return (
        f'<head><meta name="robots" content="{robots}"></head>'
        f'<div class="ap-lang-menu-grid">{grid} </div> </div>'
    )


def test_indexed_page_keeps_indexed_locales_and_adds_more() -> None:
    out = scope_switcher(_page(), "en", INDEXED)
    assert 'data-lang="en"' in out and 'data-lang="fr"' in out
    assert 'data-lang="ar"' not in out and 'data-lang="yo"' not in out
    assert out.count('href="/languages/"') == 1 and "More languages" in out
    assert out.endswith("</a> </div> </div>")


def test_more_label_follows_the_page_locale() -> None:
    assert "Autres langues" in scope_switcher(_page(), "fr", INDEXED)
    assert MORE_LABEL["en"] in more_item("yo")
    assert 'data-lang="more"' in more_item("en")


def test_noindexed_and_already_scoped_pages_are_unchanged() -> None:
    page = _page("noindex, follow")
    assert scope_switcher(page, "en", INDEXED) == page
    once = scope_switcher(_page(), "en", INDEXED)
    assert scope_switcher(once, "en", INDEXED) == once


def test_page_without_menu_is_unchanged() -> None:
    assert scope_switcher("<p>hi</p>", "en", INDEXED) == "<p>hi</p>"


def test_is_noindex() -> None:
    assert is_noindex('<meta name="robots" content="noindex, follow">')
    assert not is_noindex('<meta name="robots" content="index, follow">')
    assert not is_noindex("<p>no robots meta</p>")
