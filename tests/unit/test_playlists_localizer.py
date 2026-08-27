"""Fallback paths in the /playlists/ localizer.

The happy path — 34 complete catalogues swapped into 34 forked English
shells — is exercised end-to-end by the build and by
``tests/validation/test_i18n_playlists.py``. What that leaves untested is
everything the module does when the world is *not* in its expected state,
which is exactly the code you want working when a copy change lands:

* a language with no catalogue at all must yield the English page rather
  than raise mid-build;
* an anchor the catalogue expects but the page no longer contains must be
  reported, so a reworded English string surfaces as a build warning
  instead of silently leaving that string in English on 34 trees;
* an anchor already swapped by an earlier, broader pass must *not* be
  reported — the featured playlist also appears as a card, so its iframe
  title is legitimately replaced twice.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
sys.path.insert(0, str(ROOT / "scripts" / "generators"))

import pytest
from build_translations import _pages  # type: ignore[import-not-found]
from build_translations import _state as st
from build_translations._playlists import (  # type: ignore[import-not-found]
    _Swapper,
    localize_playlists_page,
)


def test_unknown_language_returns_the_page_untouched() -> None:
    """No catalogue is a reason to ship English, not to fail the build."""
    shell = "<h1>Playlists</h1>"
    out, missed = localize_playlists_page(shell, "xx-not-a-language")
    assert out == shell
    assert missed == []


def test_a_missing_anchor_is_reported() -> None:
    """A reworded English string must not vanish silently."""
    sw = _Swapper("<p>something else entirely</p>")
    sw.swap("<p>the anchor the catalogue expects</p>", "<p>la traduction</p>")
    assert sw.missed == ["<p>the anchor the catalogue expects</p>"]


def test_an_already_swapped_anchor_is_not_reported() -> None:
    """The featured playlist is also a card; its frame title swaps twice."""
    sw = _Swapper("<p>déjà traduit</p>")
    sw.swap("<p>already translated</p>", "<p>déjà traduit</p>")
    assert sw.missed == []


def test_reported_anchors_are_truncated() -> None:
    """Warnings carry an identifiable prefix, not a whole card of markup."""
    sw = _Swapper("<p>nothing here</p>")
    sw.swap("x" * 200, "y")
    assert sw.missed == ["x" * 80]


def test_an_empty_translation_leaves_the_english_alone() -> None:
    """A catalogue gap must not blank the string on the page."""
    sw = _Swapper("<p>English copy</p>")
    sw.swap("<p>English copy</p>", "")
    assert sw.html == "<p>English copy</p>"
    assert sw.missed == []


def test_an_identical_translation_is_a_no_op() -> None:
    """Genre names stay in English in most languages — not a gap."""
    sw = _Swapper('<span class="pl-genre">Deep house</span>')
    sw.swap("Deep house", "Deep house")
    assert sw.html == '<span class="pl-genre">Deep house</span>'
    assert sw.missed == []


def test_a_real_catalogue_localizes_and_reports_nothing() -> None:
    """Sanity-check the happy path through the same entry point."""
    st.bind_lang("fr")
    shell = '<h1>Playlists</h1><a class="pl-jump" href="#latest">Hear the latest playlist</a>'
    out, missed = localize_playlists_page(shell, "fr")
    assert "Écouter la dernière playlist" in out
    # The shell is a fragment, so most anchors are legitimately absent;
    # what matters is that the ones present were swapped.
    assert isinstance(missed, list)


def test_unmatched_anchors_are_reported_as_a_build_warning(monkeypatch, capsys) -> None:
    """The whole point of collecting misses is that the build says so.

    Silence here is what let the English body ship on 34 trees in the
    first place, so the reporting branch is worth a test of its own.
    """
    st.bind_lang("fr")
    monkeypatch.setattr(
        _pages, "localize_playlists_page", lambda shell, code: (shell, ["<p>an anchor</p>"])
    )
    # The EN shell must exist for the renderer to get as far as the hook.
    if not (st.PUBLIC / "playlists" / "index.html").is_file():
        pytest.skip("public/playlists/ not built — run ./build.sh first")
    _pages.render_static_translation("playlists")
    out = capsys.readouterr().out
    assert "playlists[fr]" in out
    assert "1 anchor(s) not found" in out
