#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Algorithmic Readability Calculator.

Calculates Flesch Reading Ease (FRE) and Flesch-Kincaid Grade Level (FKGL)
for a given markdown file.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

_VOWELS = "aeiouy"


def _vowel_groups(word: str) -> int:
    """Count runs of vowels — one syllable nucleus per run."""
    count = 0
    in_run = False
    for char in word:
        if char in _VOWELS:
            if not in_run:
                count += 1
            in_run = True
        else:
            in_run = False
    return count


def _silent_ending_adjustment(word: str) -> int:
    """English spelling adds vowels that are not pronounced. Trailing silent
    'e' ("make"), and 'es'/'ed' ("makes", "walked") — but not '-le', where the
    e carries the syllable ("table")."""
    adjust = 0
    if word.endswith("e"):
        adjust -= 1
    if word.endswith(("es", "ed")) and not word.endswith("le"):
        adjust -= 1
    return adjust


def count_syllables(word: str) -> int:
    """Rule-based English syllable count: vowel groups, less silent endings,
    floored at one for any real word."""
    word = word.lower().strip(".,;:?!'\"()[]{}*-_+=")
    if not word or not word.isalpha():
        return 0
    count = _vowel_groups(word) + _silent_ending_adjustment(word)
    return max(count, 1)


def analyze_text(text: str) -> tuple[float, float, int, int, int]:
    # Strip markdown code blocks
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    # Strip HTML tags
    text = re.sub(r"<[^>]*>", "", text)
    # Strip inline code backticks
    text = re.sub(r"`[^`]*`", "", text)
    # Strip links and image links
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
    text = re.sub(r"\[(.*?)]\(.*?\)", r"\1", text)

    # Extract sentences (simplistic sentence boundary regex)
    sentences = re.split(r"(?<=[.!?])\s+", text)
    sentences = [s.strip() for s in sentences if s.strip()]

    # Extract words
    words = re.findall(r"\b[a-zA-Z']+\b", text)

    total_sentences = len(sentences)
    total_words = len(words)

    if total_sentences == 0 or total_words == 0:
        return 0.0, 0.0, 0, 0, 0

    total_syllables = sum(count_syllables(w) for w in words)

    # Flesch Reading Ease
    # FRE = 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
    fre = 206.835 - 1.015 * (total_words / total_sentences) - 84.6 * (total_syllables / total_words)

    # Flesch-Kincaid Grade Level
    # FKGL = 0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59
    fkgl = 0.39 * (total_words / total_sentences) + 11.8 * (total_syllables / total_words) - 15.59

    return fre, fkgl, total_sentences, total_words, total_syllables


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: readability.py <file-path>")
        return 1

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"Error: {path} is not a file")
        return 1

    text = path.read_text(encoding="utf-8")
    fre, fkgl, s, w, syl = analyze_text(text)

    print(f"File: {path.name}")
    print(f"  Sentences: {s}")
    print(f"  Words: {w}")
    print(f"  Syllables: {syl}")
    print(f"  Flesch Reading Ease: {fre:.2f}")
    print(f"  Flesch-Kincaid Grade Level: {fkgl:.2f}")

    # Target validation: Ease [60.0, 70.0], Grade [8.0, 10.0]
    passes = (60.0 <= fre <= 70.0) and (8.0 <= fkgl <= 10.0)
    print(f"  Status: {'PASSED' if passes else 'FAILED'}")
    return 0 if passes else 1


if __name__ == "__main__":
    sys.exit(main())
