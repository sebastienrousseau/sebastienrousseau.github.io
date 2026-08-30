# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Fallback paths in the /projects/ localizer.

The happy path — a complete catalogue swapped into a forked English shell
— is exercised end-to-end by the build. What that leaves untested is what
the module does when the catalogue and the page have drifted apart, which
is precisely the case the design is meant to survive: the English
reference is read from the built page, so a copy change on /projects/
alters the reference while the 34 catalogues still hold the old counts.

Positional arrays make that drift dangerous. If a card is added to the
English page and a catalogue is not updated, a naive pass would shift
every remaining translation by one and ship 28 confidently mislabelled
cards. So a section whose length no longer matches must keep English for
that section *and say so*, rather than silently sliding.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
sys.path.insert(0, str(ROOT / "scripts" / "generators"))

import _lang_registry  # type: ignore[import-not-found]
import pytest
from build_translations._projects import (  # type: ignore[import-not-found]
    _sub_group1,
    localize_projects_page,
    reference,
)

PUBLIC = ROOT / "public"

SKIP_IF_NO_BUILD = pytest.mark.skipif(
    not (PUBLIC / "projects" / "index.html").is_file(),
    reason="public/projects/ not built — run ./build.sh first",
)

PAGE = (
    '<main><div class="wrap">'
    '<span class="kpi-cell-label">GitHub stars</span>'
    '<span class="kpi-cell-label">Years shipping</span>'
    '<p class="cat-kicker">PAYMENTS</p>'
    '<span class="gh-txt">last commit 2mo ago</span>'
    "</div></main>"
)

# Only the generated commit age: every catalogued field is absent, which is
# what a stripped shell or a page mid-rework looks like.
BARE = '<main><div class="wrap"><span class="gh-txt">last commit 2mo ago</span></div></main>'


def test_unknown_language_returns_the_page_untouched() -> None:
    """No catalogue is a reason to ship English, not to fail the build."""
    out, problems = localize_projects_page(PAGE, "xx-not-a-language")
    assert out == PAGE
    assert problems == []


def test_a_short_catalogue_is_reported_and_leaves_that_section_english(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """One translation for two labels must not shift the second one."""
    monkeypatch.setattr(
        _lang_registry,
        "load_projects",
        lambda code: {"kpi": ["Étoiles GitHub"], "cat_kicker": ["PAIEMENTS"]},
    )
    out, problems = localize_projects_page(PAGE, "fr")

    assert any(p.startswith("kpi: catalogue has 1 entries, page has 2") for p in problems)
    # Both English labels survive: the section was skipped whole.
    assert "GitHub stars" in out
    assert "Years shipping" in out
    assert "Étoiles GitHub" not in out
    # A section that *does* match is still translated.
    assert "PAIEMENTS" in out


def test_a_section_absent_from_the_page_is_not_a_problem(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An empty section matched by an empty catalogue is simply skipped.

    Every field in the reference is present on the real page, but a
    stripped shell (a redirect stub, a page mid-rework) can leave one
    empty. Nothing to swap is not the same as a mismatch.
    """
    monkeypatch.setattr(
        _lang_registry,
        "load_projects",
        lambda code: {k: [] for k in reference(BARE)},
    )
    out, problems = localize_projects_page(BARE, "fr")
    assert problems == []
    assert out == BARE


def test_the_commit_age_is_templated_not_pinned(monkeypatch: pytest.MonkeyPatch) -> None:
    """The age comes from the page; only the wording is translated.

    GitHub push dates change between builds, so a pinned array would go
    stale and break the byte-identical-rebuild gate.
    """
    monkeypatch.setattr(
        _lang_registry,
        "load_projects",
        lambda code: (
            {k: [] for k in reference(BARE)} | {"gh_pushed_template": "dernier commit il y a {age}"}
        ),
    )
    out, problems = localize_projects_page(BARE, "fr")
    assert problems == []
    assert "dernier commit il y a 2mo" in out
    assert "last commit" not in out


def test_a_template_without_the_placeholder_is_ignored(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Dropping {age} would print the same age on every card."""
    monkeypatch.setattr(
        _lang_registry,
        "load_projects",
        lambda code: {k: [] for k in reference(BARE)} | {"gh_pushed_template": "dernier commit"},
    )
    out, _ = localize_projects_page(BARE, "fr")
    assert "last commit 2mo ago" in out


def test_an_empty_translation_leaves_that_occurrence_english() -> None:
    """A blank entry is a gap in the catalogue, not an instruction to blank the page."""
    import re

    pattern = re.compile(r"<b>([^<]+)</b>")
    html = "<b>one</b><b>two</b><b>three</b>"
    assert _sub_group1(pattern, html, ["un", "", "trois"]) == "<b>un</b><b>two</b><b>trois</b>"


def test_the_reference_deduplicates_the_repeated_card_label() -> None:
    """ "Learn more" appears on all 29 cards; one translation covers them."""
    page = (
        '<main><div class="wrap">'
        '<a href="/a/" title="A">Learn more <span aria-hidden="true"></span></a>'
        '<a href="/b/" title="B">Learn more <span aria-hidden="true"></span></a>'
        "</div></main>"
    )
    assert reference(page)["more"] == ["Learn more"]


def test_one_more_translation_covers_every_card(monkeypatch: pytest.MonkeyPatch) -> None:
    """The catalogue holds "Learn more" once; the page repeats it per card.

    ``reference`` de-duplicates the label, so the catalogue carries a
    single entry. The swap must still reach all 29 occurrences rather
    than only the first.
    """
    page = (
        '<main><div class="wrap">'
        '<a href="/a/" title="A">Learn more <span aria-hidden="true"></span></a>'
        '<a href="/b/" title="B">Learn more <span aria-hidden="true"></span></a>'
        '<a href="/c/" title="C">Learn more <span aria-hidden="true"></span></a>'
        "</div></main>"
    )
    monkeypatch.setattr(
        _lang_registry,
        "load_projects",
        lambda code: {k: [] for k in reference(page)} | {"more": ["En savoir plus"]},
    )
    out, problems = localize_projects_page(page, "fr")
    assert problems == []
    assert out.count("En savoir plus") == 3
    assert "Learn more" not in out


@SKIP_IF_NO_BUILD
def test_a_drifted_catalogue_is_announced_during_the_build(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A mismatch must reach the build log, not just the return value.

    ``localize_projects_page`` reports problems to its caller; it is
    ``render_static_translation`` that prints them. With all 34
    catalogues correct that branch never runs, so nothing would notice
    if the reporting were dropped — and the first symptom of a copy
    change would be 34 silently half-English pages.
    """
    from build_translations import _pages
    from build_translations import _state as st

    monkeypatch.setattr(_lang_registry, "load_projects", lambda code: {"kpi": ["Étoiles"]})
    st.bind_lang("fr")
    _pages.render_static_translation("projects")

    out = capsys.readouterr().out
    assert "build_translations: projects[fr]" in out
    assert "kpi: catalogue has 1 entries" in out
