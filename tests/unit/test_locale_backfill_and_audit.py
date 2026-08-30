# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""The translation defect scanner and the locale front-matter backfiller.

audit_translations is the scanner every other translation tool defers to —
translate_stubs_ollama.validate() calls straight into its HARD_PATTERNS. If a
pattern stopped matching, a stub would pass validation and ship as a finished
translation, so the patterns are asserted individually rather than in bulk.

backfill_locale_frontmatter decides, per field, whether an existing value
looks English enough to overwrite and whether the proposed replacement is
really in the target locale. Both directions are heuristics over natural
language, and both can be wrong in a way no build gate would catch: too eager
and it overwrites a good translation with a worse one; too shy and the
English stays. The decision rules are the tests.
"""

from __future__ import annotations

from pathlib import Path

import audit_translations as aud
import backfill_locale_frontmatter as bf
import pytest

# ---------------------------------------------------------------------------
# audit_translations — the patterns every other tool trusts
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("name", "sample"),
    [
        ("stub_marker", "class=translation-stub"),
        ("translation_pending", "Translation pending review"),
        ("draft_translation", "This is a DRAFT translation"),
        ("english_body_stub", "Body text is intentionally left in English"),
        ("native_review_stub", "until a native reviewer signs off"),
        ("editorial_note", "Editorial note: replace this block"),
        ("draft_title", "[FR DRAFT] Le titre"),
    ],
)
def test_each_hard_pattern_matches_its_marker(name: str, sample: str) -> None:
    """One test per pattern: a bulk assertion would hide a dead one."""
    hits = [n for n, p in aud.HARD_PATTERNS if p.search(sample)]
    assert name in hits


def test_patterns_are_case_insensitive_where_they_should_be() -> None:
    hits = [n for n, p in aud.HARD_PATTERNS if p.search("TRANSLATION PENDING")]
    assert "translation_pending" in hits


def test_draft_title_requires_the_bracketed_uppercase_form() -> None:
    """`[FR DRAFT]` is the marker; the word 'draft' in prose is not."""
    assert not any(
        p.search("a draft of the piece") for n, p in aud.HARD_PATTERNS if n == "draft_title"
    )
    assert any(p.search("[PT-BR DRAFT] x") for n, p in aud.HARD_PATTERNS if n == "draft_title")


def test_clean_translated_prose_matches_nothing() -> None:
    assert [n for n, p in aud.HARD_PATTERNS if p.search("Un article traduit correctement.")] == []


def test_scan_returns_the_defect_names_found(tmp_path: Path) -> None:
    p = tmp_path / "a.md"
    p.write_text("Translation pending. Also a translation-stub marker.\n", encoding="utf-8")
    found = aud.scan(p)
    assert "translation_pending" in found
    assert "stub_marker" in found


def test_scan_of_a_clean_file_is_empty(tmp_path: Path) -> None:
    p = tmp_path / "a.md"
    p.write_text("Texte entièrement traduit.\n", encoding="utf-8")
    assert aud.scan(p) == []


def test_iter_locale_posts_only_walks_locale_directories(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Root-level English posts are not translations and must not be scanned."""
    (tmp_path / "fr").mkdir()
    (tmp_path / "fr" / "a.md").write_text("x", encoding="utf-8")
    (tmp_path / "root-post.md").write_text("x", encoding="utf-8")
    monkeypatch.setattr(aud, "POSTS", tmp_path)
    names = [p.name for p in aud.iter_locale_posts()]
    assert names == ["a.md"]


# ---------------------------------------------------------------------------
# backfill — is this text in the target locale?
# ---------------------------------------------------------------------------


def test_non_latin_locale_needs_one_in_script_character() -> None:
    assert bf._is_in_target_locale("Русский текст", "ru")
    assert not bf._is_in_target_locale("Plain English text", "ru")


def test_locales_without_diacritics_rely_on_stopwords_alone() -> None:
    """id and fil write plain Latin with no diacritics, so the diacritic
    signal can never fire for them and the stop-word list is the only
    evidence available. Worth pinning: dropping those stop-words would
    silently make every Indonesian and Filipino field unverifiable."""
    bare = [
        loc
        for loc in bf.LOCALES
        if loc not in bf._SCRIPT_RANGES and loc not in bf._LATIN_DIACRITICS
    ]
    assert bare == ["id", "fil"]
    for loc in bare:
        assert bf._LOCALE_STOPWORDS.get(loc), f"{loc} has no other signal to fall back on"


def test_empty_text_is_never_in_the_target_locale() -> None:
    assert not bf._is_in_target_locale("", "fr")
    assert not bf._is_in_target_locale("   ", "fr")


def test_latin_locale_accepts_diacritic_plus_a_stopword() -> None:
    """Neither signal proves anything alone; together they do."""
    assert bf._is_in_target_locale("Le système de paiement à évoluer", "fr")


def test_latin_locale_rejects_plain_english() -> None:
    assert not bf._is_in_target_locale("The payment system has evolved over the years", "fr")


def test_latin_locale_rejects_text_with_no_word_tokens() -> None:
    assert not bf._is_in_target_locale("--- 123 ---", "fr")


def test_stopword_hits_counts_only_matches() -> None:
    assert bf._stopword_hits(["le", "the", "de"], frozenset({"le", "de"})) == 2
    assert bf._stopword_hits(["the"], frozenset({"le"})) == 0


def test_tokenize_drops_punctuation_and_lowercases() -> None:
    assert bf._tokenize("Le Système, à 20022!") == ["le", "système", "à"]


def test_tokenize_keeps_accented_letters() -> None:
    assert "évolué" in bf._tokenize("Évolué")


# ---------------------------------------------------------------------------
# backfill — does the existing value look English enough to overwrite?
# ---------------------------------------------------------------------------


def test_english_marker_phrase_flags_the_field() -> None:
    assert bf._looks_english_field("The future of the payment system")


def test_two_english_stopwords_flag_the_field() -> None:
    assert bf._looks_english_field("Payments that are settled")


def test_translated_text_is_not_flagged() -> None:
    """Overwriting a good translation is the expensive direction of error."""
    assert not bf._looks_english_field("Le système de paiement")


def test_empty_or_missing_field_is_not_flagged() -> None:
    assert not bf._looks_english_field(None)
    assert not bf._looks_english_field("")


def test_field_with_no_word_tokens_is_not_flagged() -> None:
    assert not bf._looks_english_field("--- 2026 ---")


# ---------------------------------------------------------------------------
# backfill — front-matter surgery
# ---------------------------------------------------------------------------


FM = 'title: "Le titre"\ndescription: "La description"\n'


def test_read_field_returns_the_value() -> None:
    assert bf._read_field(FM, "title") == "Le titre"


def test_read_field_returns_none_when_absent() -> None:
    assert bf._read_field(FM, "excerpt") is None


def test_replace_field_changes_only_the_named_field() -> None:
    out = bf._replace_field(FM, "title", "Nouveau titre")
    assert 'title: "Nouveau titre"' in out
    assert 'description: "La description"' in out


def test_replace_field_escapes_a_quote_in_the_written_value() -> None:
    """The file must stay parseable, so the quote is escaped on the way in."""
    out = bf._replace_field(FM, "title", 'Un « vrai » "titre"')
    assert 'title: "Un « vrai » \\"titre\\""' in out


def test_read_field_does_not_unescape_and_that_is_safe_here() -> None:
    """_read_field returns the raw stored form, so read(write(x)) != x.

    That asymmetry would be a bug if a read value were ever written back —
    the escaping would compound on each pass. It is not: _read_field feeds
    only _looks_english_field and a None check, while everything written
    comes from _extract_h1 / _extract_tldr, i.e. raw body text. Pinning it
    so a future refactor that starts round-tripping has to notice.
    """
    out = bf._replace_field(FM, "title", 'a "q"')
    assert bf._read_field(out, "title") == 'a \\"q\\"'


def test_replace_field_escapes_a_backslash() -> None:
    """re.sub processes escapes in a *string* replacement, which silently
    undid the doubling and wrote a lone backslash into a YAML double-quoted
    scalar — where \\b means backspace. Fixed by using a callable
    replacement; this pins it so the regression cannot come back."""
    out = bf._replace_field(FM, "title", r"a\b")
    assert r'title: "a\\b"' in out


def test_insert_excerpt_lands_directly_after_the_title() -> None:
    out = bf._insert_excerpt_after_title(FM, "Un extrait")
    lines = [ln for ln in out.splitlines() if ln.strip()]
    assert lines[0].startswith("title:")
    assert lines[1].startswith("excerpt:")


def test_insert_excerpt_escapes_its_value() -> None:
    out = bf._insert_excerpt_after_title(FM, 'has a "quote"')
    assert 'excerpt: "has a \\"quote\\""' in out


# ---------------------------------------------------------------------------
# backfill — document structure
# ---------------------------------------------------------------------------


def test_split_frontmatter_returns_head_and_body() -> None:
    head, body = bf._split_frontmatter('---\ntitle: "T"\n---\nThe body.\n')
    assert head.endswith("---\n")
    assert body.strip() == "The body."


def test_split_frontmatter_returns_none_without_two_delimiters() -> None:
    assert bf._split_frontmatter('---\ntitle: "T"\n') is None
    assert bf._split_frontmatter("no front matter\n") is None


def test_extract_h1_takes_the_first_heading() -> None:
    assert bf._extract_h1("intro\n\n# Le titre\n\n# Second\n") == "Le titre"


def test_extract_h1_ignores_an_h2() -> None:
    assert bf._extract_h1("## Sous-titre\n") is None


def test_extract_h1_returns_none_when_absent() -> None:
    assert bf._extract_h1("just prose\n") is None


def test_extract_tldr_strips_the_bold_label() -> None:
    body = '<p class="post-lead-tldr"><strong>TL;DR</strong> Le résumé ici.</p>'
    assert bf._extract_tldr(body) == "Le résumé ici."


def test_extract_tldr_collapses_whitespace() -> None:
    body = '<p class="post-lead-tldr">Le\n   résumé\tici.</p>'
    assert bf._extract_tldr(body) == "Le résumé ici."


def test_extract_tldr_returns_none_when_absent() -> None:
    assert bf._extract_tldr("<p>ordinary paragraph</p>") is None


def test_extract_tldr_returns_none_for_a_label_only_block() -> None:
    """A TL;DR containing only its own label carries no summary."""
    assert bf._extract_tldr('<p class="post-lead-tldr"><strong>TL;DR</strong></p>') is None
