# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""scripts/generators/build_languages.py: the /languages/ page."""

from __future__ import annotations

import _lang_registry as _lr
import build_languages as bl


def test_every_active_locale_has_one_card_linking_its_home() -> None:
    body = bl.render_body()
    active = _lr.active()
    assert body.count('<li class="story-card">') == len(active)
    assert 'href="/"' in body and 'href="/fr/"' in body and 'href="/yo/"' in body
    assert body.count("<h1") == 1


def test_rtl_locales_are_marked() -> None:
    body = bl.render_body()
    assert 'href="/ar/" lang="ar-SA" dir="rtl"' in body
    assert 'href="/fr/" lang="fr-FR" hreflang' in body


def test_description_fits_the_length_budget() -> None:
    assert 120 <= len(bl.DESC) <= 160, len(bl.DESC)
