# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""The article author card: one renderer, profile.yml's facts."""

from __future__ import annotations

import json
import unicodedata
from pathlib import Path

import _author_card
import _profile
import pytest

ROOT = Path(__file__).resolve().parents[2]
_LOCALES = sorted(p.parent.name for p in (ROOT / "_data" / "i18n").glob("*/author.json"))


def _author(code: str) -> dict[str, object]:
    return json.loads((ROOT / "_data" / "i18n" / code / "author.json").read_text(encoding="utf-8"))


def test_english_card_states_the_profile() -> None:
    html = _author_card.english()
    card = _profile.author_card()
    assert card["credentials"] in html
    assert card["bio"] in html
    assert html.count("<aside") == 1 and html.endswith("</aside>")


def test_english_author_json_matches_the_profile() -> None:
    en = _author("en")
    card = _profile.author_card()
    assert (en["bio"], en["credentialsPrefix"]) == (card["bio"], card["credentials"])


def test_render_escapes_nothing_twice() -> None:
    html = _author_card.render(
        bio="A &amp; B", credentials="C", about_href="/fr/a-propos/index.html"
    )
    assert "A &amp; B" in html and "&amp;amp;" not in html
    assert html.count('href="/fr/a-propos/index.html"') == 2


@pytest.mark.parametrize("code", _LOCALES)
def test_locale_card_drops_retired_facts(code: str) -> None:
    """Every edition carries the current facts: no employer roll-call from
    the old card, the 20-year figure, and the HSBC and EPAA roles."""
    data = _author(code)
    cred = str(data["credentialsPrefix"])
    assert "Virgin" not in cred and "Shazam" not in cred, code
    # Bengali and Persian write the figure in their own digits.
    ascii_digits = "".join(str(unicodedata.digit(c)) if c.isdigit() else c for c in cred)
    assert "20" in ascii_digits, code
    assert "HSBC" in cred and "EPAA" in cred, code
    if code != "en":
        assert data["_reviewed"] is False
