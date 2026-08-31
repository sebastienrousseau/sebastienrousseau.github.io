# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""The two LLM-backed stub translators, with the network stubbed out.

translate_stubs_ollama (127 statements) and translate_stubs_gemini (101) were
both at 0%. Neither can be smoke-tested like a builder: one needs a local
Ollama daemon, the other a paid API key. Everything either module does around
the call is ordinary logic, though, and that is what these tests exercise.

Two behaviours matter more than the rest:

  * `validate` refuses to write model output that still carries the defects
    the run was meant to fix. Without it a translation run can launder an
    untranslated stub into the tree with a fresh timestamp — the failure is
    invisible because the file looks newly worked on.
  * the Gemini retry path honours the API's own `retryDelay` on a 429. Getting
    that wrong means either hammering a rate limit or sleeping for a default
    when the server asked for less.

No test here opens a socket; `urlopen` and `sleep` are stubbed throughout.
"""

from __future__ import annotations

import http.client
import io
import json
import sys
import urllib.error
from pathlib import Path

import pytest
import translate_stubs_gemini as gem
import translate_stubs_ollama as olla

# ---------------------------------------------------------------------------
# Front matter splitting
# ---------------------------------------------------------------------------


DOC = '---\ntitle: "T"\nlang: "fr"\n---\n\nThe body.\n'


def test_split_frontmatter_separates_head_from_body() -> None:
    """Leading blank lines are stripped; the trailing newline is kept, so the
    body round-trips into a file without losing its final newline."""
    head, body = olla.split_frontmatter(DOC)
    assert head.startswith("---\n")
    assert head.rstrip().endswith("---")
    assert body == "The body.\n"


def test_split_frontmatter_rejects_a_file_without_any() -> None:
    with pytest.raises(ValueError, match="missing frontmatter"):
        olla.split_frontmatter("No front matter here.\n")


def test_split_frontmatter_rejects_an_unterminated_block() -> None:
    with pytest.raises(ValueError, match="unterminated"):
        olla.split_frontmatter('---\ntitle: "T"\n')


def test_frontmatter_map_strips_quotes_of_either_kind() -> None:
    fm = olla.frontmatter_map("---\na: \"double\"\nb: 'single'\nc: bare\n---\nbody\n")
    assert fm["a"] == "double"
    assert fm["b"] == "single"
    assert fm["c"] == "bare"


def test_frontmatter_map_ignores_a_line_without_a_colon() -> None:
    fm = olla.frontmatter_map('---\ntitle: "T"\njust-noise\n---\nbody\n')
    assert "title" in fm
    assert len(fm) == 1


def test_frontmatter_map_keeps_a_colon_inside_the_value() -> None:
    fm = olla.frontmatter_map('---\ntitle: "ISO 20022: migration"\n---\nbody\n')
    assert fm["title"] == "ISO 20022: migration"


# ---------------------------------------------------------------------------
# Extracting the translation from model output
# ---------------------------------------------------------------------------


def test_extract_takes_only_the_delimited_region() -> None:
    """Models preface their answer; the delimiters are how we ignore that."""
    raw = "Sure! Here you go:\nBEGIN_TRANSLATION\nthe content\nEND_TRANSLATION\nHope that helps!"
    assert olla.extract_translation(raw) == "the content"


def test_extract_uses_the_last_end_marker() -> None:
    raw = "BEGIN_TRANSLATION\na\nEND_TRANSLATION\nnoise\nEND_TRANSLATION"
    assert "noise" in olla.extract_translation(raw)


def test_extract_strips_a_markdown_fence() -> None:
    assert olla.extract_translation("```markdown\nthe content\n```") == "the content"


def test_extract_strips_a_bare_fence() -> None:
    assert olla.extract_translation("```\nthe content\n```") == "the content"


def test_extract_passes_through_undelimited_output() -> None:
    assert olla.extract_translation("  plain output  ") == "plain output"


def test_extract_leaves_an_inner_fence_alone() -> None:
    """A fenced code block inside the translation is content, not wrapping."""
    raw = "BEGIN_TRANSLATION\nintro\n\n```py\ncode\n```\n\noutro\nEND_TRANSLATION"
    out = olla.extract_translation(raw)
    assert "```py" in out


# ---------------------------------------------------------------------------
# Slug mapping
# ---------------------------------------------------------------------------


def test_reverse_slug_map_inverts_the_articles_map(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    d = tmp_path / "fr"
    d.mkdir()
    (d / "slugs.json").write_text(
        json.dumps({"articles": {"2026-01-01-en": "2026-01-01-fr"}}), encoding="utf-8"
    )
    monkeypatch.setattr(olla, "I18N", tmp_path)
    assert olla.reverse_slug_map("fr") == {"2026-01-01-fr": "2026-01-01-en"}


def test_reverse_slug_map_is_empty_without_a_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(olla, "I18N", tmp_path)
    assert olla.reverse_slug_map("nope") == {}


def test_english_source_resolves_via_the_slug_map(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    posts = tmp_path / "_posts"
    (posts / "fr").mkdir(parents=True)
    (posts / "2026-01-01-en.md").write_text("---\ntitle: x\n---\nbody\n", encoding="utf-8")
    loc = posts / "fr" / "2026-01-01-fr.md"
    loc.write_text("---\ntitle: x\n---\nbody\n", encoding="utf-8")
    monkeypatch.setattr(olla, "POSTS", posts)
    monkeypatch.setattr(olla, "reverse_slug_map", lambda lang: {"2026-01-01-fr": "2026-01-01-en"})
    assert olla.english_source_for(loc).name == "2026-01-01-en.md"


def test_english_source_falls_back_to_a_frontmatter_url(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """No slug mapping: recover the English stem from a canonical URL."""
    posts = tmp_path / "_posts"
    (posts / "fr").mkdir(parents=True)
    (posts / "2026-02-02-en.md").write_text("---\ntitle: x\n---\nbody\n", encoding="utf-8")
    loc = posts / "fr" / "2026-02-02-fr.md"
    loc.write_text(
        '---\nitem_link: "https://sebastienrousseau.com/2026-02-02-en/index.html"\n---\nbody\n',
        encoding="utf-8",
    )
    monkeypatch.setattr(olla, "POSTS", posts)
    monkeypatch.setattr(olla, "reverse_slug_map", lambda lang: {})
    monkeypatch.setattr(olla, "ROOT", tmp_path)
    assert olla.english_source_for(loc).name == "2026-02-02-en.md"


def test_english_source_raises_when_nothing_maps(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    posts = tmp_path / "_posts"
    (posts / "fr").mkdir(parents=True)
    loc = posts / "fr" / "orphan.md"
    loc.write_text("---\ntitle: x\n---\nbody\n", encoding="utf-8")
    monkeypatch.setattr(olla, "POSTS", posts)
    monkeypatch.setattr(olla, "reverse_slug_map", lambda lang: {})
    monkeypatch.setattr(olla, "ROOT", tmp_path)
    with pytest.raises(FileNotFoundError, match="cannot map"):
        olla.english_source_for(loc)


# ---------------------------------------------------------------------------
# Prompt assembly
# ---------------------------------------------------------------------------


def test_prompt_names_the_locale_and_protects_frontmatter_keys() -> None:
    prompt = olla.prompt_for("fr", DOC, DOC)
    assert olla.LOCALE_NAMES["fr"] in prompt
    for key in list(olla.PROTECTED_FRONTMATTER)[:3]:
        assert key in prompt


def test_prompt_carries_the_delimiters_it_later_parses() -> None:
    prompt = olla.prompt_for("fr", DOC, DOC)
    assert "BEGIN_TRANSLATION" in prompt
    assert "END_TRANSLATION" in prompt


def test_prompt_falls_back_to_the_code_for_an_unknown_locale() -> None:
    assert "xx" in olla.prompt_for("xx", DOC, DOC)


# ---------------------------------------------------------------------------
# validate — the guard that stops a run laundering an untranslated stub
# ---------------------------------------------------------------------------


def test_validate_rejects_output_without_frontmatter(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="missing frontmatter"):
        olla.validate(tmp_path / "a.md", "no front matter\n")


def test_validate_accepts_clean_output(tmp_path: Path) -> None:
    olla.validate(tmp_path / "a.md", DOC)


def test_validate_rejects_output_still_carrying_a_hard_defect(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The point of the run is to remove these; writing one back is worse
    than failing, because the file then looks freshly worked on."""
    import re as _re

    monkeypatch.setattr(
        olla.audit_translations, "HARD_PATTERNS", [("stub marker", _re.compile("STILL_ENGLISH"))]
    )
    with pytest.raises(ValueError, match=r"STILL_ENGLISH|stub marker"):
        olla.validate(tmp_path / "a.md", DOC.replace("The body.", "STILL_ENGLISH"))


# ---------------------------------------------------------------------------
# Ollama transport
# ---------------------------------------------------------------------------


class _Resp:
    def __init__(self, payload: dict) -> None:
        self._b = json.dumps(payload).encode("utf-8")

    def read(self) -> bytes:
        return self._b

    def __enter__(self):
        return self

    def __exit__(self, *_a):
        return False


def test_ollama_returns_the_extracted_translation(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        olla.urllib.request,
        "urlopen",
        lambda *a, **k: _Resp({"response": "BEGIN_TRANSLATION\nbonjour\nEND_TRANSLATION"}),
    )
    assert olla.ollama_translate("m", "p", 5) == "bonjour"


def test_ollama_raises_a_runtime_error_when_unreachable(monkeypatch: pytest.MonkeyPatch) -> None:
    """A daemon that is not running must be a clear message, not a traceback."""

    def boom(*_a, **_k):
        raise urllib.error.URLError("connection refused")

    monkeypatch.setattr(olla.urllib.request, "urlopen", boom)
    with pytest.raises(RuntimeError, match="ollama API request failed"):
        olla.ollama_translate("m", "p", 5)


def test_ollama_surfaces_an_api_level_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        olla.urllib.request, "urlopen", lambda *a, **k: _Resp({"error": "model not found"})
    )
    with pytest.raises(RuntimeError, match="model not found"):
        olla.ollama_translate("m", "p", 5)


# ---------------------------------------------------------------------------
# Gemini: key loading
# ---------------------------------------------------------------------------


def test_api_key_prefers_the_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "from-env")
    assert gem.load_api_key() == "from-env"


def test_api_key_reads_an_explicit_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    f = tmp_path / "key"
    f.write_text("  from-file  \n", encoding="utf-8")
    assert gem.load_api_key(f) == "from-file"


def test_api_key_reads_the_file_named_by_the_environment(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    f = tmp_path / "key"
    f.write_text("from-env-file\n", encoding="utf-8")
    monkeypatch.setenv("GEMINI_API_KEY_FILE", str(f))
    assert gem.load_api_key() == "from-env-file"


def test_api_key_is_empty_when_nothing_is_configured(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY_FILE", raising=False)
    assert gem.load_api_key() == ""


# ---------------------------------------------------------------------------
# Gemini: request shape
# ---------------------------------------------------------------------------


def test_request_targets_generate_content_with_the_model_in_the_path() -> None:
    req = gem._build_request("gemini-2.0-flash", "the prompt", "KEY")
    assert "gemini-2.0-flash:generateContent" in req.full_url
    assert req.method == "POST"


def test_request_url_encodes_a_model_name_with_a_slash() -> None:
    req = gem._build_request("models/x y", "p", "KEY")
    assert " " not in req.full_url


def test_request_url_encodes_the_api_key() -> None:
    req = gem._build_request("m", "p", "a key/with+chars")
    assert "a key" not in req.full_url


def test_request_body_carries_the_prompt() -> None:
    req = gem._build_request("m", "the prompt", "KEY")
    body = json.loads(req.data.decode("utf-8"))
    assert body["contents"][0]["parts"][0]["text"] == "the prompt"


# ---------------------------------------------------------------------------
# Gemini: retry policy
# ---------------------------------------------------------------------------


def test_retry_delay_uses_the_servers_own_hint() -> None:
    """Coming back before the window the server named just burns quota."""
    detail = json.dumps({"error": {"details": [{"retryDelay": "17s"}]}})
    assert gem._retry_delay_seconds(detail) == 19  # hint + 2s margin


def test_retry_delay_falls_back_on_an_unparseable_body() -> None:
    assert gem._retry_delay_seconds("not json") == 35


def test_retry_delay_falls_back_when_the_hint_is_absent() -> None:
    assert gem._retry_delay_seconds(json.dumps({"error": {}})) == 35


def _http_error(code: int, body: str = "{}") -> urllib.error.HTTPError:
    return urllib.error.HTTPError("u", code, "msg", {}, io.BytesIO(body.encode()))


def test_post_retries_a_429_then_succeeds(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = {"n": 0}

    def flaky(_req, _timeout):
        calls["n"] += 1
        if calls["n"] == 1:
            raise _http_error(429, json.dumps({"error": {"details": [{"retryDelay": "1s"}]}}))
        return "ok"

    monkeypatch.setattr(gem, "_post_json", flaky)
    monkeypatch.setattr(gem.time, "sleep", lambda _s: None)
    assert gem._post_with_retries(object(), 5, retries=2) == "ok"
    assert calls["n"] == 2


def test_post_gives_up_after_the_retry_budget(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(gem, "_post_json", lambda *_a: (_ for _ in ()).throw(_http_error(429)))
    monkeypatch.setattr(gem.time, "sleep", lambda _s: None)
    with pytest.raises(RuntimeError, match="HTTP 429"):
        gem._post_with_retries(object(), 5, retries=1)


def test_post_does_not_retry_a_non_429(monkeypatch: pytest.MonkeyPatch) -> None:
    """A 400 will fail identically next time; retrying just wastes time."""
    calls = {"n": 0}

    def always_400(*_a):
        calls["n"] += 1
        raise _http_error(400, "bad request")

    monkeypatch.setattr(gem, "_post_json", always_400)
    monkeypatch.setattr(gem.time, "sleep", lambda _s: None)
    with pytest.raises(RuntimeError, match="HTTP 400"):
        gem._post_with_retries(object(), 5, retries=3)
    assert calls["n"] == 1


def test_post_retries_a_transport_error(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = {"n": 0}

    def flaky(*_a):
        calls["n"] += 1
        if calls["n"] == 1:
            raise http.client.RemoteDisconnected("dropped")
        return "ok"

    monkeypatch.setattr(gem, "_post_json", flaky)
    monkeypatch.setattr(gem.time, "sleep", lambda _s: None)
    assert gem._post_with_retries(object(), 5, retries=2) == "ok"


# ---------------------------------------------------------------------------
# Gemini: response parsing
# ---------------------------------------------------------------------------


def test_join_candidate_text_concatenates_parts() -> None:
    body = json.dumps({"candidates": [{"content": {"parts": [{"text": "a"}, {"text": "b"}]}}]})
    assert gem._join_candidate_text(body) == "a\nb"


def test_join_candidate_text_skips_a_part_with_no_text() -> None:
    body = json.dumps({"candidates": [{"content": {"parts": [{"text": "a"}, {"inline": 1}]}}]})
    assert gem._join_candidate_text(body) == "a"


def test_join_candidate_text_raises_on_an_empty_response() -> None:
    """A safety-blocked response has candidates but no text; that is a failure."""
    with pytest.raises(RuntimeError, match="no text"):
        gem._join_candidate_text(json.dumps({"candidates": []}))


def test_gemini_generate_returns_the_extracted_translation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    body = json.dumps(
        {
            "candidates": [
                {"content": {"parts": [{"text": "BEGIN_TRANSLATION\nbonjour\nEND_TRANSLATION"}]}}
            ]
        }
    )
    monkeypatch.setattr(gem, "_post_with_retries", lambda *a, **k: body)
    assert gem.gemini_generate("m", "p", 5, "KEY") == "bonjour"


# ---------------------------------------------------------------------------
# main() for both translators.
#
# Only the model call is stubbed. defect_paths, english_source_for, validate
# and the file writes all run for real against a tmp tree, so what these
# cover is the loop that decides which files to touch and what to write —
# the part that can quietly translate the wrong file or write over a good
# translation.
# ---------------------------------------------------------------------------


TRANSLATED = '---\ntitle: "Le titre"\n---\n\nLe corps traduit.\n'


def _tree(tmp: Path, monkeypatch: pytest.MonkeyPatch, mod, *, defective: bool = True):
    """A repo-shaped tmp tree with one English post and one locale stub."""
    posts = tmp / "_posts"
    (posts / "fr").mkdir(parents=True)
    (posts / "2026-01-01-en.md").write_text(
        '---\ntitle: "The Title"\n---\n\nThe English body.\n', encoding="utf-8"
    )
    body = "Translation pending" if defective else "Le corps."
    (posts / "fr" / "2026-01-01-fr.md").write_text(
        f'---\ntitle: "T"\n---\n\n{body}\n', encoding="utf-8"
    )
    monkeypatch.setattr(mod, "ROOT", tmp)
    monkeypatch.setattr(olla, "ROOT", tmp)
    monkeypatch.setattr(olla, "POSTS", posts)
    monkeypatch.setattr(olla.audit_translations, "POSTS", posts)
    monkeypatch.setattr(olla, "reverse_slug_map", lambda lang: {"2026-01-01-fr": "2026-01-01-en"})
    return posts / "fr" / "2026-01-01-fr.md"


def test_ollama_main_translates_a_defective_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    target = _tree(tmp_path, monkeypatch, olla)
    monkeypatch.setattr(olla, "ollama_translate", lambda *a, **k: TRANSLATED)
    monkeypatch.setattr(sys, "argv", ["translate_stubs_ollama", "--model", "m"])
    assert olla.main() == 0
    assert "Le corps traduit." in target.read_text(encoding="utf-8")
    capsys.readouterr()


def test_ollama_main_reports_when_nothing_matches(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A clean tree is a success, not an error."""
    _tree(tmp_path, monkeypatch, olla, defective=False)
    monkeypatch.setattr(sys, "argv", ["translate_stubs_ollama", "--model", "m"])
    assert olla.main() == 0
    assert "No incomplete locale posts" in capsys.readouterr().out


def test_ollama_dry_run_writes_nothing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    target = _tree(tmp_path, monkeypatch, olla)
    before = target.read_text(encoding="utf-8")

    def must_not_run(*_a, **_k):
        raise AssertionError("--dry-run called the model")

    monkeypatch.setattr(olla, "ollama_translate", must_not_run)
    monkeypatch.setattr(sys, "argv", ["translate_stubs_ollama", "--model", "m", "--dry-run"])
    assert olla.main() == 0
    assert target.read_text(encoding="utf-8") == before
    capsys.readouterr()


def test_ollama_main_refuses_to_write_output_that_is_still_defective(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """The whole point of validate(): a stub must not be laundered back in
    with a fresh timestamp, looking like finished work."""
    target = _tree(tmp_path, monkeypatch, olla)
    before = target.read_text(encoding="utf-8")
    monkeypatch.setattr(
        olla, "ollama_translate", lambda *a, **k: '---\ntitle: "x"\n---\n\nTranslation pending\n'
    )
    monkeypatch.setattr(sys, "argv", ["translate_stubs_ollama", "--model", "m"])
    with pytest.raises(ValueError, match="model output still contains"):
        olla.main()
    assert target.read_text(encoding="utf-8") == before
    capsys.readouterr()


def test_ollama_main_honours_the_limit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    posts = tmp_path / "_posts"
    _tree(tmp_path, monkeypatch, olla)
    (posts / "fr" / "2026-02-02-fr.md").write_text(
        '---\ntitle: "T"\n---\n\nTranslation pending\n', encoding="utf-8"
    )
    (posts / "2026-02-02-en.md").write_text('---\ntitle: "T"\n---\n\nBody.\n', encoding="utf-8")
    monkeypatch.setattr(
        olla,
        "reverse_slug_map",
        lambda lang: {"2026-01-01-fr": "2026-01-01-en", "2026-02-02-fr": "2026-02-02-en"},
    )
    calls = {"n": 0}

    def counting(*_a, **_k):
        calls["n"] += 1
        return TRANSLATED

    monkeypatch.setattr(olla, "ollama_translate", counting)
    monkeypatch.setattr(sys, "argv", ["translate_stubs_ollama", "--model", "m", "--limit", "1"])
    assert olla.main() == 0
    assert calls["n"] == 1
    capsys.readouterr()


def test_gemini_main_requires_a_key_unless_dry_running(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _tree(tmp_path, monkeypatch, gem)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY_FILE", raising=False)
    monkeypatch.setattr(sys, "argv", ["translate_stubs_gemini"])
    with pytest.raises(SystemExit, match="GEMINI_API_KEY"):
        gem.main()


def test_gemini_dry_run_needs_no_key(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _tree(tmp_path, monkeypatch, gem)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY_FILE", raising=False)
    monkeypatch.setattr(sys, "argv", ["translate_stubs_gemini", "--dry-run"])
    assert gem.main() == 0
    capsys.readouterr()


def test_gemini_main_writes_to_out_dir_without_touching_the_source(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """--out-dir exists so a run can be reviewed before it overwrites work."""
    target = _tree(tmp_path, monkeypatch, gem)
    before = target.read_text(encoding="utf-8")
    out = tmp_path / "out"
    monkeypatch.setenv("GEMINI_API_KEY", "k")
    monkeypatch.setattr(gem, "gemini_generate", lambda *a, **k: TRANSLATED)
    monkeypatch.setattr(sys, "argv", ["translate_stubs_gemini", "--out-dir", str(out)])
    assert gem.main() == 0
    assert target.read_text(encoding="utf-8") == before, "source must be untouched"
    written = list(out.rglob("*.md"))
    assert written and "Le corps traduit." in written[0].read_text(encoding="utf-8")
    capsys.readouterr()


def test_gemini_main_overwrites_in_place_without_out_dir(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    target = _tree(tmp_path, monkeypatch, gem)
    monkeypatch.setenv("GEMINI_API_KEY", "k")
    monkeypatch.setattr(gem, "gemini_generate", lambda *a, **k: TRANSLATED)
    monkeypatch.setattr(sys, "argv", ["translate_stubs_gemini"])
    assert gem.main() == 0
    assert "Le corps traduit." in target.read_text(encoding="utf-8")
    capsys.readouterr()
