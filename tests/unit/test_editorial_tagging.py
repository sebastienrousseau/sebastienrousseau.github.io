# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""The two editorial tools that rewrite front matter, previously untested.

automate_tags rewrites the `tags:` line across every post in every locale.
translate_frontmatter rewrites translated titles and descriptions in place.
Both edit source files the whole site is generated from, so a wrong rewrite
does not fail a build — it silently changes what the site says.

The LLM call in translate_frontmatter is stubbed. What is worth testing is
either side of it: which locales are judged to need work (a field that still
holds the English value), and whether a translated value is written back
without corrupting the quoting.
"""

from __future__ import annotations

from pathlib import Path

import automate_tags as at
import pytest
import translate_frontmatter as tf

# ---------------------------------------------------------------------------
# automate_tags — front matter parsing
# ---------------------------------------------------------------------------


def _post(tmp: Path, body: str) -> Path:
    p = tmp / "post.md"
    p.write_text(body, encoding="utf-8")
    return p


def test_extract_frontmatter_splits_metadata_from_body(tmp_path: Path) -> None:
    p = _post(tmp_path, '---\ntitle: "T"\ntags: "a, b"\n---\nThe body.\n')
    fm, fm_text, body = at.extract_frontmatter_and_content(p)
    assert fm["title"] == "T"
    assert fm["tags"] == "a, b"
    assert body.strip() == "The body."
    assert "title" in fm_text


def test_extract_frontmatter_on_a_file_without_any(tmp_path: Path) -> None:
    """No front matter must yield the whole file as body, not a parse error."""
    p = _post(tmp_path, "Just prose, no delimiters.\n")
    fm, fm_text, body = at.extract_frontmatter_and_content(p)
    assert fm == {}
    assert fm_text == ""
    assert body.startswith("Just prose")


def test_extract_frontmatter_strips_both_quote_styles(tmp_path: Path) -> None:
    p = _post(tmp_path, "---\na: \"double\"\nb: 'single'\nc: bare\n---\nx\n")
    fm, _, _ = at.extract_frontmatter_and_content(p)
    assert fm["a"] == "double"
    assert fm["b"] == "single"
    assert fm["c"] == "bare"


def test_extract_frontmatter_keeps_colons_in_the_value(tmp_path: Path) -> None:
    """A title containing a colon must not be truncated at it."""
    p = _post(tmp_path, '---\ntitle: "ISO 20022: the migration"\n---\nx\n')
    fm, _, _ = at.extract_frontmatter_and_content(p)
    assert fm["title"] == "ISO 20022: the migration"


# ---------------------------------------------------------------------------
# automate_tags — cleaning
# ---------------------------------------------------------------------------


def test_clean_tags_drops_blanks_and_preserves_order() -> None:
    assert at.clean_tags(["alpha", "  ", "", "beta"]) == ["alpha", "beta"]


def test_clean_tags_deduplicates_case_insensitively() -> None:
    out = at.clean_tags(["Payments", "payments", "PAYMENTS"])
    assert len(out) == 1


def test_clean_tags_applies_the_canonical_map() -> None:
    """Whatever the canonical map says, the output must be canonical."""
    alias, canonical = next(iter(at.CANONICAL_MAP.items()))
    assert at.clean_tags([alias]) == [canonical]


def test_clean_tags_collapses_an_alias_and_its_canonical_form() -> None:
    alias, canonical = next(iter(at.CANONICAL_MAP.items()))
    assert at.clean_tags([alias, canonical]) == [canonical]


def test_clean_tags_on_an_empty_list() -> None:
    assert at.clean_tags([]) == []


# ---------------------------------------------------------------------------
# automate_tags — inference
# ---------------------------------------------------------------------------


def test_infer_tags_keeps_the_existing_tags() -> None:
    assert at.infer_tags("nothing to match here", ["existing"])[0] == "existing"


def test_infer_tags_adds_iso_20022_from_a_message_name() -> None:
    """pain.001 in the prose is enough; the tag need not be written out."""
    assert "ISO 20022" in at.infer_tags("We generate pain.001 files nightly.", [])


def test_infer_tags_adds_post_quantum_from_an_abbreviation() -> None:
    assert "post-quantum cryptography" in at.infer_tags("A PQC migration plan.", [])


def test_infer_tags_matches_case_insensitively() -> None:
    assert "ISO 20022" in at.infer_tags("ISO 20022 and iso 20022 alike.", [])


def test_infer_tags_respects_word_boundaries() -> None:
    """`\\bdora\\b` must not fire on 'Pandora' or 'fedora'."""
    assert "DORA" not in at.infer_tags("Opening Pandora's box wearing a fedora.", [])


def test_infer_tags_adds_nothing_for_unrelated_prose() -> None:
    assert at.infer_tags("A quiet walk by the river on Sunday.", []) == []


def test_infer_tags_never_duplicates_an_existing_tag() -> None:
    inferred = at.infer_tags("We generate pain.001 files nightly.", ["ISO 20022"])
    assert inferred.count("ISO 20022") == 1


# ---------------------------------------------------------------------------
# automate_tags — translation lookup
# ---------------------------------------------------------------------------


TRANSLATIONS = {"payments": {"fr": "paiements", "de": "Zahlungen"}}


def test_translate_tag_returns_the_translation() -> None:
    assert at.translate_tag("Payments", "fr", TRANSLATIONS) == "paiements"


def test_translate_tag_falls_back_to_the_canonical_english_form() -> None:
    """An untranslated locale gets canonical English, never an empty tag.

    Canonical, not the caller's casing: "Payments" comes back as "payments"
    because that is what CANONICAL_MAP holds. Tag slugs feed URLs, so the
    canonical form is the right fallback even though it changes the case.
    """
    assert at.translate_tag("Payments", "yo", TRANSLATIONS) == "payments"


def test_translate_tag_returns_an_unmapped_tag_unchanged() -> None:
    """Outside the canonical map there is nothing to normalise to."""
    assert at.translate_tag("Zzz Unknown", "yo", {}) == "Zzz Unknown"


def test_translate_tag_falls_back_for_an_unknown_tag() -> None:
    assert at.translate_tag("no-such-tag", "fr", TRANSLATIONS) == "no-such-tag"


# ---------------------------------------------------------------------------
# translate_frontmatter — field read/write
# ---------------------------------------------------------------------------


def test_read_field_returns_the_quoted_value() -> None:
    assert tf._read_field('title: "The Title"\n', "title") == "The Title"


def test_read_field_returns_none_when_absent() -> None:
    assert tf._read_field('title: "T"\n', "description") is None


def test_read_field_unescapes_an_embedded_quote() -> None:
    assert tf._read_field('title: "He said \\"hi\\""\n', "title") == 'He said "hi"'


def test_field_exists_distinguishes_present_from_absent() -> None:
    text = 'title: "T"\ndescription: ""\n'
    assert tf._field_exists(text, "title")
    assert tf._field_exists(text, "description"), "an empty value is still a present field"
    assert not tf._field_exists(text, "subtitle")


def test_replace_field_swaps_only_the_value() -> None:
    out = tf._replace_field('title: "Old"\nother: "Keep"\n', "title", "New")
    assert 'title: "New"' in out
    assert 'other: "Keep"' in out


def test_replace_field_escapes_quotes_in_the_new_value() -> None:
    out = tf._replace_field('title: "Old"\n', "title", 'A "quoted" thing')
    assert '\\"quoted\\"' in out
    assert tf._read_field(out, "title") == 'A "quoted" thing', "must round-trip"


def test_replace_field_round_trips_a_backslash() -> None:
    """Round-trips *and* stores the escaped form. It used to round-trip by
    accident: re.sub collapsed the doubled backslash on write and _read_field
    unescaped nothing on read, so the file held a lone backslash inside a
    YAML double-quoted scalar."""
    out = tf._replace_field('title: "Old"\n', "title", r"back\slash")
    assert r'title: "back\\slash"' in out
    assert tf._read_field(out, "title") == r"back\slash"


def test_replace_field_replaces_only_the_first_occurrence() -> None:
    out = tf._replace_field('title: "A"\ntitle: "B"\n', "title", "New")
    assert out.count('"New"') == 1


def test_replace_field_is_a_no_op_when_the_field_is_absent() -> None:
    text = 'other: "x"\n'
    assert tf._replace_field(text, "title", "New") == text


# ---------------------------------------------------------------------------
# translate_frontmatter — which locales need work
# ---------------------------------------------------------------------------


def test_en_fields_collects_only_non_empty_values() -> None:
    text = "".join(f'{f}: "value-{f}"\n' for f in tf.FIELDS)
    fields = tf._en_fields(text)
    assert set(fields) == set(tf.FIELDS)
    assert all(v.startswith("value-") for v in fields.values())


def test_en_fields_skips_an_empty_value() -> None:
    field = tf.FIELDS[0]
    assert field not in tf._en_fields(f'{field}: ""\n')


def _locale_file(tmp: Path, lang: str, body: str) -> Path:
    d = tmp / lang
    d.mkdir(parents=True, exist_ok=True)
    p = d / "post.md"
    p.write_text(body, encoding="utf-8")
    return p


def test_locales_needing_flags_a_field_still_holding_english(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    field = tf.FIELDS[0]
    fr = _locale_file(tmp_path, "fr", f'{field}: "English value"\n')
    monkeypatch.setattr(tf, "_find_locale_file", lambda slug, lang: fr if lang == "fr" else None)
    needing, paths = tf._locales_needing("slug", {field: "English value"}, ["fr", "de"])
    assert needing == {"fr": [field]}
    assert paths["fr"] == fr


def test_locales_needing_ignores_an_already_translated_field(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    field = tf.FIELDS[0]
    fr = _locale_file(tmp_path, "fr", f'{field}: "Valeur traduite"\n')
    monkeypatch.setattr(tf, "_find_locale_file", lambda slug, lang: fr)
    needing, _ = tf._locales_needing("slug", {field: "English value"}, ["fr"])
    assert needing == {}


def test_locales_needing_skips_a_locale_with_no_file(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(tf, "_find_locale_file", lambda slug, lang: None)
    needing, paths = tf._locales_needing("slug", {tf.FIELDS[0]: "x"}, ["fr", "de"])
    assert needing == {}
    assert paths == {}


def test_locales_needing_ignores_a_field_the_locale_does_not_declare(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A field absent from the locale file is not 'untranslated' — it is absent."""
    fr = _locale_file(tmp_path, "fr", 'unrelated: "x"\n')
    monkeypatch.setattr(tf, "_find_locale_file", lambda slug, lang: fr)
    needing, _ = tf._locales_needing("slug", {tf.FIELDS[0]: "English value"}, ["fr"])
    assert needing == {}
