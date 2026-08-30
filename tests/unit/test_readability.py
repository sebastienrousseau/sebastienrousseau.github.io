# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Unit coverage for readability — Phase 1.3.

readability.py scores article prose (Flesch Reading Ease + Flesch-Kincaid grade)
and was untested. Cover the syllable counter and the text analyzer, including
its markdown/HTML stripping and empty-input guard.
"""

from __future__ import annotations

import readability as rd

# --- count_syllables -------------------------------------------------------


def test_count_syllables_basic() -> None:
    assert rd.count_syllables("cat") == 1
    assert rd.count_syllables("hello") == 2
    assert rd.count_syllables("banana") == 3


def test_count_syllables_silent_e_clamped_to_one() -> None:
    assert rd.count_syllables("code") == 1  # silent 'e' removed
    assert rd.count_syllables("the") == 1  # would go to 0, clamped up


def test_count_syllables_strips_punctuation_and_rejects_non_alpha() -> None:
    assert rd.count_syllables("cat!") == 1  # trailing punctuation stripped
    assert rd.count_syllables("") == 0
    assert rd.count_syllables("123") == 0


# --- analyze_text ----------------------------------------------------------


def test_analyze_text_counts_sentences_and_words() -> None:
    fre, fkgl, sentences, words, syllables = rd.analyze_text("The cat sat. The dog ran.")
    assert sentences == 2
    assert words == 6
    assert syllables >= 6  # at least one per word
    assert isinstance(fre, float) and isinstance(fkgl, float)


def test_analyze_text_empty_returns_zeros() -> None:
    assert rd.analyze_text("   ") == (0.0, 0.0, 0, 0, 0)


def test_analyze_text_strips_code_html_and_links() -> None:
    text = "See `inline` and [the docs](http://x/y) plus ```\nblock\n``` here."
    _, _, _, words, _ = rd.analyze_text(text)
    # words counted: See, and, the, docs, plus, here  (inline/url/block stripped)
    assert words == 6
