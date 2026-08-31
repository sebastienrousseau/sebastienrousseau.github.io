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

import json
import subprocess
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


# ---------------------------------------------------------------------------
# automate_tags — writing the tags line back
# ---------------------------------------------------------------------------


def _md(tmp: Path, name: str, body: str) -> Path:
    p = tmp / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def test_update_tags_replaces_an_existing_line(tmp_path: Path) -> None:
    p = _md(tmp_path, "a.md", '---\ntitle: "T"\ntags: "old, tags"\n---\nbody\n')
    assert at.update_tags_in_file(p, ["new", "set"]) is True
    assert 'tags: "new, set"' in p.read_text(encoding="utf-8")


def test_update_tags_preserves_the_other_lines(tmp_path: Path) -> None:
    p = _md(tmp_path, "a.md", '---\ntitle: "T"\ntags: "old"\nbanner: "b.webp"\n---\nbody\n')
    at.update_tags_in_file(p, ["new"])
    text = p.read_text(encoding="utf-8")
    assert 'title: "T"' in text
    assert 'banner: "b.webp"' in text
    assert text.endswith("body\n")


def test_update_tags_handles_single_quotes_and_bare_values(tmp_path: Path) -> None:
    for raw in ("tags: 'old'", "tags: old, bare"):
        p = _md(tmp_path, "a.md", f'---\ntitle: "T"\n{raw}\n---\nbody\n')
        assert at.update_tags_in_file(p, ["new"]) is True
        assert 'tags: "new"' in p.read_text(encoding="utf-8")


def test_update_tags_injects_after_the_title_when_absent(tmp_path: Path) -> None:
    p = _md(tmp_path, "a.md", '---\ntitle: "T"\nbanner: "b"\n---\nbody\n')
    assert at.update_tags_in_file(p, ["new"]) is True
    lines = p.read_text(encoding="utf-8").splitlines()
    assert lines[lines.index('title: "T"') + 1] == 'tags: "new"'


def test_update_tags_is_a_no_op_when_the_value_is_unchanged(tmp_path: Path) -> None:
    """Rewriting an identical file would churn mtimes for nothing."""
    p = _md(tmp_path, "a.md", '---\ntitle: "T"\ntags: "same"\n---\nbody\n')
    before = p.stat().st_mtime_ns
    assert at.update_tags_in_file(p, ["same"]) is False
    assert p.stat().st_mtime_ns == before


def test_update_tags_returns_false_without_tags_or_title(tmp_path: Path) -> None:
    """Nowhere to put them; the file must be left exactly as it was."""
    p = _md(tmp_path, "a.md", '---\nbanner: "b"\n---\nbody\n')
    original = p.read_text(encoding="utf-8")
    assert at.update_tags_in_file(p, ["new"]) is False
    assert p.read_text(encoding="utf-8") == original


# ---------------------------------------------------------------------------
# automate_tags — translation catalogue
# ---------------------------------------------------------------------------


def test_load_translations_is_empty_without_the_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(at, "TRANSLATIONS_FILE", tmp_path / "absent.json")
    assert at.load_translations() == {}


def test_load_translations_reads_the_catalogue(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    f = tmp_path / "t.json"
    f.write_text('{"payments": {"fr": "paiements"}}', encoding="utf-8")
    monkeypatch.setattr(at, "TRANSLATIONS_FILE", f)
    assert at.load_translations()["payments"]["fr"] == "paiements"


def test_load_translations_degrades_on_malformed_json(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A broken catalogue must not stop the run; it just translates nothing."""
    f = tmp_path / "t.json"
    f.write_text("{not json", encoding="utf-8")
    monkeypatch.setattr(at, "TRANSLATIONS_FILE", f)
    assert at.load_translations() == {}
    assert "Error loading" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# automate_tags — post discovery
# ---------------------------------------------------------------------------


def test_english_posts_exclude_the_index_pages(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """tags.md, articles.md and friends are listings, not articles."""
    for name in ("2026-01-01-real.md", "tags.md", "articles.md", "privacy.md", "notes.txt"):
        _md(tmp_path, name, "x")
    monkeypatch.setattr(at, "POSTS_DIR", tmp_path)
    assert at.get_english_posts() == ["2026-01-01-real.md"]


def test_english_drafts_are_empty_without_the_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(at, "DRAFTS_DIR", tmp_path / "absent")
    assert at.get_english_drafts() == []


def test_english_drafts_lists_markdown_only(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    for name in ("draft.md", "index.md", "notes.txt"):
        _md(tmp_path, name, "x")
    monkeypatch.setattr(at, "DRAFTS_DIR", tmp_path)
    assert at.get_english_drafts() == ["draft.md"]


def test_declared_tags_splits_and_strips() -> None:
    assert at._declared_tags({"tags": " a , b ,, c "}) == ["a", "b", "c"]
    assert at._declared_tags({}) == []


# ---------------------------------------------------------------------------
# automate_tags — the English pass and locale propagation
# ---------------------------------------------------------------------------


def test_optimise_english_returns_tags_even_when_nothing_is_written(
    tmp_path: Path,
) -> None:
    """Locale copies propagate from the returned list, so it must be
    returned whether or not the English file needed a rewrite."""
    p = _md(tmp_path, "a.md", '---\ntitle: "T"\ntags: "payments"\n---\nbody\n')
    tags, written = at._optimise_english(p, "EN")
    assert tags == at.clean_tags(["payments"])
    assert written == 0


def test_optimise_english_writes_and_counts_an_inferred_tag(tmp_path: Path) -> None:
    p = _md(tmp_path, "a.md", '---\ntitle: "T"\ntags: "payments"\n---\nWe emit pain.001 files.\n')
    tags, written = at._optimise_english(p, "EN")
    assert "ISO 20022" in tags
    assert written == 1


def test_propagate_skips_a_locale_without_the_post(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(at, "POSTS_DIR", tmp_path)
    assert at._propagate_to_locale("missing.md", "fr", ["payments"], {}) == 0


def test_propagate_translates_and_writes_the_locale_copy(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _md(tmp_path, "fr/a.md", '---\ntitle: "T"\ntags: "old"\n---\nbody\n')
    monkeypatch.setattr(at, "POSTS_DIR", tmp_path)
    n = at._propagate_to_locale("a.md", "fr", ["payments"], {"payments": {"fr": "paiements"}})
    assert n == 1
    assert "paiements" in (tmp_path / "fr" / "a.md").read_text(encoding="utf-8")


def test_propagate_is_a_no_op_when_the_locale_already_matches(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _md(tmp_path, "fr/a.md", '---\ntitle: "T"\ntags: "paiements"\n---\nbody\n')
    monkeypatch.setattr(at, "POSTS_DIR", tmp_path)
    n = at._propagate_to_locale("a.md", "fr", ["payments"], {"payments": {"fr": "paiements"}})
    assert n == 0


def test_process_single_post_counts_english_plus_locales(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _md(tmp_path, "a.md", '---\ntitle: "T"\ntags: "payments"\n---\nWe emit pain.001 files.\n')
    _md(tmp_path, "fr/a.md", '---\ntitle: "T"\ntags: "old"\n---\nbody\n')
    monkeypatch.setattr(at, "POSTS_DIR", tmp_path)
    assert at.process_single_post("a.md", ["fr"], {}) == 2


# ---------------------------------------------------------------------------
# automate_tags — the tags index page
# ---------------------------------------------------------------------------


def test_optimise_tags_page_is_a_no_op_when_absent(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(at, "POSTS_DIR", tmp_path)
    at._optimise_tags_page()  # must not raise


def test_optimise_tags_page_sets_the_canonical_title(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _md(tmp_path, "tags.md", '---\ntitle: "Something else"\n---\nbody\n')
    monkeypatch.setattr(at, "POSTS_DIR", tmp_path)
    at._optimise_tags_page()
    assert "Tags Index" in (tmp_path / "tags.md").read_text(encoding="utf-8")
    capsys.readouterr()


# ---------------------------------------------------------------------------
# translate_frontmatter — the translator call and its retry policy.
#
# `claude -p` is stubbed at the subprocess boundary; nothing is executed.
# What these cover is the failure policy: a translation that cannot be
# produced must not abort a run that is part-way through 34 locales, and a
# reply that arrives malformed must not be written as if it were a
# translation.
# ---------------------------------------------------------------------------


class _Proc:
    def __init__(self, stdout: str = "", stderr: str = "") -> None:
        self.stdout = stdout
        self.stderr = stderr


def test_invoke_translator_parses_a_json_reply(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        tf.subprocess, "run", lambda *a, **k: _Proc('{"fr": {"title": "Le titre"}}')
    )
    assert tf._invoke_translator("p")["fr"]["title"] == "Le titre"


def test_invoke_translator_strips_a_markdown_fence(monkeypatch: pytest.MonkeyPatch) -> None:
    """Models wrap JSON in ```json fences; the parse must survive that."""
    monkeypatch.setattr(
        tf.subprocess, "run", lambda *a, **k: _Proc('```json\n{"fr": {"title": "T"}}\n```')
    )
    assert tf._invoke_translator("p") == {"fr": {"title": "T"}}


def test_invoke_translator_raises_on_an_empty_reply(monkeypatch: pytest.MonkeyPatch) -> None:
    """Empty is not an empty translation — it is a failed call, and the
    retry loop above needs to see the difference."""
    monkeypatch.setattr(tf.subprocess, "run", lambda *a, **k: _Proc("", "boom"))
    with pytest.raises(ValueError, match="Empty response"):
        tf._invoke_translator("p")


def test_invoke_translator_raises_on_unparseable_output(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(tf.subprocess, "run", lambda *a, **k: _Proc("not json at all"))
    with pytest.raises(json.JSONDecodeError):
        tf._invoke_translator("p")


def test_translate_batch_short_circuits_with_nothing_to_do(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def must_not_run(*_a, **_k):
        raise AssertionError("called the translator with no locales needing work")

    monkeypatch.setattr(tf, "_invoke_translator", must_not_run)
    assert tf._translate_batch({"title": "T"}, {}) == {}


def test_translate_batch_returns_the_first_successful_attempt(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    calls = {"n": 0}

    def flaky(_prompt):
        calls["n"] += 1
        if calls["n"] == 1:
            raise json.JSONDecodeError("bad", "", 0)
        return {"fr": {"title": "Le titre"}}

    monkeypatch.setattr(tf, "_invoke_translator", flaky)
    monkeypatch.setattr(tf.time, "sleep", lambda _s: None)
    assert tf._translate_batch({"title": "T"}, {"fr": ["title"]}) == {"fr": {"title": "Le titre"}}
    assert calls["n"] == 2
    capsys.readouterr()


def test_translate_batch_gives_up_after_three_attempts_without_raising(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """The behaviour that matters: a failed translation returns {} so the
    run continues. Raising here would abandon every locale still queued."""
    calls = {"n": 0}

    def always_fails(_prompt):
        calls["n"] += 1
        raise json.JSONDecodeError("bad", "", 0)

    monkeypatch.setattr(tf, "_invoke_translator", always_fails)
    monkeypatch.setattr(tf.time, "sleep", lambda _s: None)
    assert tf._translate_batch({"title": "T"}, {"fr": ["title"]}) == {}
    assert calls["n"] == 3, "exactly three attempts, then give up"
    capsys.readouterr()


@pytest.mark.parametrize(
    "exc",
    [
        subprocess.TimeoutExpired(cmd="claude", timeout=300),
        OSError("claude: command not found"),
        ValueError("Empty response"),
    ],
)
def test_translate_batch_retries_every_expected_failure(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], exc: Exception
) -> None:
    """A missing binary, a timeout and an empty reply are all retryable —
    none of them may escape as a traceback mid-run."""

    def boom(_prompt):
        raise exc

    monkeypatch.setattr(tf, "_invoke_translator", boom)
    monkeypatch.setattr(tf.time, "sleep", lambda _s: None)
    assert tf._translate_batch({"title": "T"}, {"fr": ["title"]}) == {}
    capsys.readouterr()


def test_translate_batch_lets_an_unexpected_error_traceback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Only the named failure modes are swallowed; anything else is a bug
    worth surfacing rather than retrying blindly."""

    def boom(_prompt):
        raise KeyboardInterrupt

    monkeypatch.setattr(tf, "_invoke_translator", boom)
    with pytest.raises(KeyboardInterrupt):
        tf._translate_batch({"title": "T"}, {"fr": ["title"]})


# ---------------------------------------------------------------------------
# translate_frontmatter — writing the translated fields back
# ---------------------------------------------------------------------------


def _fm_file(tmp_path: Path, body: str) -> Path:
    """A bare front-matter fragment for the apply-path tests.

    Named distinctly from _locale_file above, which builds a locale-directory
    post for the _locales_needing tests — shadowing it silently broke three
    of those.
    """
    p = tmp_path / "post.md"
    p.write_text(body, encoding="utf-8")
    return p


def test_apply_translations_writes_and_reports_the_fields(tmp_path: Path) -> None:
    p = _fm_file(tmp_path, 'title: "English"\ndescription: "English desc"\n')
    applied = tf._apply_translations(p, {"title": "Le titre", "description": "La description"})
    assert set(applied) == {"title", "description"}
    assert "Le titre" in p.read_text(encoding="utf-8")


def test_apply_translations_skips_an_empty_or_non_string_value(tmp_path: Path) -> None:
    """A model can return null or a nested object for a field; neither is a
    translation, and writing one would corrupt the front matter."""
    p = _fm_file(tmp_path, 'title: "English"\n')
    before = p.read_text(encoding="utf-8")
    assert tf._apply_translations(p, {"title": ""}) == []
    assert tf._apply_translations(p, {"title": None}) == []
    assert tf._apply_translations(p, {"title": {"nested": "x"}}) == []
    assert p.read_text(encoding="utf-8") == before


def test_apply_translations_does_not_write_when_nothing_changes(tmp_path: Path) -> None:
    p = _fm_file(tmp_path, 'title: "Le titre"\n')
    before = p.stat().st_mtime_ns
    assert tf._apply_translations(p, {"title": "Le titre"}) == []
    assert p.stat().st_mtime_ns == before, "an identical value must not rewrite the file"


def test_apply_translations_ignores_a_field_absent_from_the_file(tmp_path: Path) -> None:
    p = _fm_file(tmp_path, 'title: "English"\n')
    assert tf._apply_translations(p, {"subtitle": "Sous-titre"}) == []
