# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Coverage for postbuild_lib/_i18n — the shared i18n foundation (Phase 4.1).

_i18n was extracted from article_furniture as a base module (breaking the
label/slug-map cycle so hreflang can split out next). These pin the page-lang
detection, label lookup + cache, active-locale list, and slug-map shape.
"""

from __future__ import annotations

import postbuild_lib._i18n as i18n

# --- _detect_page_lang -----------------------------------------------------


def test_detect_page_lang_from_html_tag() -> None:
    assert i18n._detect_page_lang('<html lang="fr-FR"><body>') == "fr"
    assert i18n._detect_page_lang('<html lang="id"><body>') == "id"


def test_detect_page_lang_defaults_to_en() -> None:
    assert i18n._detect_page_lang("<body>no html tag</body>") == "en"


# --- _labels_for_lang ------------------------------------------------------


def test_labels_for_lang_en_is_labels_en() -> None:
    out = i18n._labels_for_lang("en")
    assert out == i18n.LABELS_EN
    assert out is not i18n.LABELS_EN  # a copy, not the shared dict


def test_labels_for_lang_is_cached() -> None:
    a = i18n._labels_for_lang("en")
    b = i18n._labels_for_lang("en")
    assert a is b  # second call returns the cached object


def test_labels_combines_detect_and_lookup() -> None:
    assert i18n._labels('<html lang="en">')["Home"] == "Home"


# --- _all_active_non_en_langs ----------------------------------------------


def test_all_active_non_en_langs_excludes_en() -> None:
    langs = i18n._all_active_non_en_langs()
    assert isinstance(langs, list) and langs
    assert "en" not in langs
    assert "fr" in langs


# --- _slug_maps ------------------------------------------------------------


def test_slug_maps_shape_and_cache() -> None:
    m = i18n._slug_maps("fr")
    assert set(m) == {
        "articles_en_to_lang",
        "articles_lang_to_en",
        "statics_en_to_lang",
        "statics_lang_to_en",
    }
    # both directions are inverses
    for en, loc in m["articles_en_to_lang"].items():
        assert m["articles_lang_to_en"][loc] == en
    assert i18n._slug_maps("fr") is m  # cached


def test_strings_for_lang_unknown_code_returns_empty():
    # An unloadable locale raises LanguageError, which is caught so the
    # caller falls back to its EN literal instead of crashing. Covers the
    # except branch in _strings_for_lang.
    assert i18n._strings_for_lang("zzzz-nonexistent") == {}
