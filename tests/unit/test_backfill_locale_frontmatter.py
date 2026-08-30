# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Coverage for backfill_locale_frontmatter — Phase 1.3 + Phase 4.1 guard.

The 500-line per-locale stop-word table was extracted to
_data/i18n/locale-stopwords.json. This pins the data contract and covers the
pure locale-detection helpers that consume it.
"""

from __future__ import annotations

import json
from pathlib import Path

import backfill_locale_frontmatter as bf

SW_PATH = Path(__file__).resolve().parents[2] / "_data" / "i18n" / "locale-stopwords.json"


# --- stop-word extraction guard --------------------------------------------


def test_stopwords_json_loads_as_frozensets() -> None:
    raw = json.loads(SW_PATH.read_text(encoding="utf-8"))
    assert len(raw) >= 16
    for lang, words in raw.items():
        assert isinstance(bf._LOCALE_STOPWORDS[lang], frozenset)
        assert set(words) == bf._LOCALE_STOPWORDS[lang]


def test_stopwords_have_known_locale() -> None:
    assert "le" in bf._LOCALE_STOPWORDS["fr"]  # French article


# --- _tokenize -------------------------------------------------------------


def test_tokenize_lowercases_letter_runs_only() -> None:
    assert bf._tokenize("Hello, World! 123") == ["hello", "world"]
    assert bf._tokenize("café déjà") == ["café", "déjà"]  # keeps accented letters


# --- _is_in_target_locale --------------------------------------------------


def test_is_in_target_locale_empty_is_false() -> None:
    assert bf._is_in_target_locale("", "fr") is False
    assert bf._is_in_target_locale("   ", "fr") is False


def test_is_in_target_locale_non_latin_script() -> None:
    # Bengali script text is in-locale for bn; Latin text is not.
    assert bf._is_in_target_locale("বাংলা লেখা", "bn") is True
    assert bf._is_in_target_locale("plain english text", "bn") is False


def test_is_in_target_locale_french_stopwords() -> None:
    # French stop-words + diacritic → detected as fr.
    assert bf._is_in_target_locale("le crédit à la banque française", "fr") is True


def test_is_in_target_locale_english_not_flagged_as_french() -> None:
    assert bf._is_in_target_locale("the quick brown fox jumps", "fr") is False
