"""Slug derivation — scripts/lib/_romanise.py (ADR-0012)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from lib._romanise import derive_slug, lexicon, romanise, slugify


def test_lexicon_supplies_arabic_short_vowels():
    """Arabic is an abjad: the table alone gives a consonant skeleton."""
    assert lexicon()["ar"]["التقنية"] == "altiqniya"
    assert "altiqniya" in romanise("التقنية", "ar")


def test_lexicon_segments_thai():
    """Thai writes no word boundaries, so lexicon entries are the boundaries."""
    out = slugify("การอ่านขอบฟ้าความเสี่ยง", "th")
    assert "khopfa" in out and "khwamsiang" in out
    assert "khopfakhwamsiang" not in out


def test_lexicon_reads_cjk():
    """Chinese and Japanese have no table at all; readings come from data."""
    assert slugify("读懂银行", "zh-hans") == "dudong-yinhang"
    assert "ginko" in slugify("銀行の新興技術", "ja")


def test_longest_match_wins():
    """A longer entry must beat the shorter one it starts with."""
    assert "xinxing-jishu" in slugify("新兴技术风险", "zh-hans")


def test_zh_hant_gets_the_tw_suffix():
    """All 105 zh-hant posts mark the script variant in the URL."""
    assert derive_slug("讀懂銀行", "zh-hant").endswith("-tw")
    assert not derive_slug("读懂银行", "zh-hans").endswith("-tw")


def test_suffix_is_not_doubled():
    out = derive_slug("讀懂銀行", "zh-hant")
    assert out.count("-tw") == 1


def test_year_is_dropped_because_the_filename_already_carries_it():
    """ "2026'da bankalar…" would otherwise give 2026-07-03-2026-…"""
    assert not derive_slug("2026'da bankalar için risk", "tr", "2026").startswith("2026")


def test_year_dropped_for_locale_digits():
    """Bengali writes its own digits; the check is on the derived token."""
    assert not derive_slug("২০২৬ সালে ব্যাংকগুলির জন্য", "bn", "2026").startswith("2026")


def test_slug_does_not_open_on_a_stopword():
    """Dropping a leading year used to leave "da-bankalar…", "men-bainkon…"."""
    assert not slugify("De los mensajes al mapa corporativo", "es").startswith("de-")


def test_slug_does_not_end_on_a_stopword():
    assert not slugify("Odczytywanie horyzontu ryzyk dla", "pl").endswith("-dla")


def test_vietnamese_capital_d_stroke_folds():
    """NFKD leaves Đ intact, so "Đọc" romanised to "oc"."""
    assert slugify("Đọc chân trời rủi ro", "vi").startswith("doc-")


def test_greek_capitals_survive():
    """Tables are keyed lowercase; without folding "Μια" became "ia"."""
    assert romanise("Μια", "el").strip().startswith("m")


def test_repeated_tokens_are_dropped_once():
    assert slugify("Risk risk horizon banks", "en") == "risk-horizon-banks"


def test_word_cap_and_length_bound():
    out = slugify(
        "A very long headline about programmable liquidity and tokenised deposits "
        "and real time treasury orchestration in twenty twenty six",
        "en",
    )
    assert len(out.split("-")) <= 6
    assert len(out) <= 76


def test_min_words_fallback():
    """A title that is almost all stopwords still yields a usable slug."""
    assert len(slugify("De la el los", "es").split("-")) >= 2


def test_unknown_locale_passes_through():
    assert slugify("Plain English Title", "xx") == "plain-english-title"
