"""Unit tests for scripts/translate_post.py — the per-locale stub
scaffolder used by the daily-publishing flow. Body translation itself
runs in Claude Code; this script does the deterministic part
(localised slug, frontmatter rewrite, slug-map update, marker-aware
idempotence)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import translate_post as tp  # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_EN_SAMPLE = """---
title: "Sample headline"
subtitle: "Sample subtitle"
description: "Sample description."
date: "May 19, 2026"
keywords: "a, b, c"
banner: "https://cloudcdn.pro/stocks/images/x.webp"
banner_alt: "alt"
banner_width: "1425"
banner_height: "571"
layout: "report"
schema: "FAQPage, Article"
language: "en-GB"
locale: "en_GB"
hreflang: "en"
url: "https://sebastienrousseau.com/2026-05-19-sample"
permalink: "https://sebastienrousseau.com/2026-05-19-sample"
id: "https://sebastienrousseau.com/2026-05-19-sample"
---

# Sample headline

Body paragraph.
"""


@pytest.fixture
def fake_repo(tmp_path, monkeypatch):
    """Build a minimal _posts/ + _data/i18n/<lang>/slugs.json tree
    and re-anchor translate_post's ROOT-derived paths at tmp_path."""
    posts = tmp_path / "_posts"
    i18n = tmp_path / "_data" / "i18n"
    posts.mkdir()
    (tmp_path / "_drafts").mkdir()
    # Seed three locales; the rest of the active-non-EN set is
    # patched via monkeypatching active_non_en_locales below.
    for lang in ("fr", "de", "es"):
        (i18n / lang).mkdir(parents=True)
        (i18n / lang / "slugs.json").write_text(
            json.dumps({"_comment": "", "static": {}, "articles": {}}),
            encoding="utf-8",
        )
    monkeypatch.setattr(tp, "ROOT", tmp_path)
    monkeypatch.setattr(tp, "POSTS", posts)
    monkeypatch.setattr(tp, "I18N", i18n)
    monkeypatch.setattr(tp, "active_non_en_locales", lambda: ["fr", "de", "es"])
    return tmp_path


def _seed_en(repo: Path, slug: str = "2026-05-19-sample") -> Path:
    p = repo / "_posts" / f"{slug}.md"
    p.write_text(_EN_SAMPLE, encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# Frontmatter parse/emit
# ---------------------------------------------------------------------------


def test_parse_frontmatter_extracts_keys():
    fm, body = tp.parse_frontmatter(_EN_SAMPLE)
    assert fm["title"] == "Sample headline"
    assert fm["language"] == "en-GB"
    assert body.startswith("# Sample headline")


def test_parse_frontmatter_no_delimiter_returns_empty():
    fm, body = tp.parse_frontmatter("plain text, no frontmatter")
    assert fm == {}
    assert body == "plain text, no frontmatter"


def test_parse_frontmatter_unclosed_delimiter_returns_empty():
    fm, body = tp.parse_frontmatter("---\ntitle: 'x'\n\nbody")
    assert fm == {}


def test_parse_frontmatter_ignores_blank_and_comment_lines():
    src = "---\n\n# this is a comment\ntitle: 'a'\nnotkey\n---\nbody\n"
    fm, body = tp.parse_frontmatter(src)
    assert fm == {"title": "a"}
    assert body == "body\n"


def test_emit_frontmatter_roundtrips_to_parse():
    fm_in = {"title": "X", "language": "fr"}
    out = tp.emit_frontmatter(fm_in)
    fm_out, body = tp.parse_frontmatter(out + "body")
    assert fm_out == fm_in
    assert body == "body"


# ---------------------------------------------------------------------------
# Slug localisation
# ---------------------------------------------------------------------------


def test_localized_slug_token_substitutes_known_dict():
    out = tp.localized_slug("2026-05-19-global-wholesale-payments-economics-2026", "fr")
    # 'global' → 'mondiaux', 'wholesale' → 'de-gros', 'payments' → 'paiements',
    # 'economics' → 'economie'.
    assert "mondiaux" in out
    assert "paiements" in out
    assert "economie" in out


def test_localized_slug_unknown_lang_falls_back_to_en_slug():
    en = "2026-05-19-global-wholesale-payments-economics-2026"
    assert tp.localized_slug(en, "ja") == en
    assert tp.localized_slug(en, "ar") == en
    assert tp.localized_slug(en, "yo") == en


def test_localized_slug_passes_unknown_tokens_through():
    # 'sample' isn't in the FR dict — keeps its EN form alongside the
    # translated 'paiements' for 'payments'.
    out = tp.localized_slug("2026-05-19-sample-payments-thing", "fr")
    assert "sample" in out
    assert "paiements" in out
    assert "thing" in out


# ---------------------------------------------------------------------------
# scaffold_one — the core per-locale writer
# ---------------------------------------------------------------------------


def test_scaffold_one_writes_localised_post_and_updates_slugs(fake_repo):
    _seed_en(fake_repo)
    status = tp.scaffold_one(
        "2026-05-19-sample", _EN_SAMPLE, "fr", dry_run=False,
    )
    assert "scaffolded" in status
    # File on disk
    out_files = list((fake_repo / "_posts" / "fr").glob("*.md"))
    assert len(out_files) == 1
    body = out_files[0].read_text(encoding="utf-8")
    assert tp.STUB_MARKER in body
    fm, _ = tp.parse_frontmatter(body)
    assert fm["language"] == "fr"
    assert fm["locale"] == "fr_FR"
    assert fm["hreflang"] == "fr"
    assert fm["url"].startswith("https://sebastienrousseau.com/fr/")
    # slug-map update
    data = json.loads((fake_repo / "_data" / "i18n" / "fr" / "slugs.json").read_text())
    assert "2026-05-19-sample" in data["articles"]


def test_scaffold_one_dry_run_reports_without_writing(fake_repo):
    _seed_en(fake_repo)
    status = tp.scaffold_one(
        "2026-05-19-sample", _EN_SAMPLE, "fr", dry_run=True,
    )
    assert "would scaffold" in status
    assert not list((fake_repo / "_posts" / "fr").glob("*.md"))


def test_scaffold_one_skips_existing_real_translation(fake_repo):
    _seed_en(fake_repo)
    target = fake_repo / "_posts" / "fr" / "2026-05-19-sample.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    # Use the EN-fallback slug so we don't need to predict the FR slug.
    real_body = "---\nlanguage: 'fr'\n---\n\nreal translated body"
    target.write_text(real_body, encoding="utf-8")
    # The scaffolder uses the localized slug for FR, so this file at
    # the EN slug doesn't collide. Use DE (which has no slug-dict
    # entry for 'sample') so the path matches.
    target_de = fake_repo / "_posts" / "de" / "2026-05-19-sample.md"
    target_de.parent.mkdir(parents=True, exist_ok=True)
    target_de.write_text(real_body, encoding="utf-8")
    status = tp.scaffold_one(
        "2026-05-19-sample", _EN_SAMPLE, "de", dry_run=False,
    )
    assert "keep" in status
    assert target_de.read_text(encoding="utf-8") == real_body


def test_scaffold_one_raises_on_unparseable_en(fake_repo):
    with pytest.raises(SystemExit):
        tp.scaffold_one("bad", "no frontmatter here", "fr", dry_run=False)


def test_scaffold_one_uses_fallback_locale_when_unknown(fake_repo):
    """The _LOCALE_CODES dict covers every active locale but defensively
    falls back to ``<code>_<CODE>``."""
    _seed_en(fake_repo)
    # Patch the locale map to drop an entry → exercise the fallback.
    import copy
    new_codes = copy.deepcopy(tp._LOCALE_CODES)
    new_codes.pop("fr")
    monkey_codes = new_codes
    tp._LOCALE_CODES.clear()
    tp._LOCALE_CODES.update(monkey_codes)
    try:
        status = tp.scaffold_one(
            "2026-05-19-sample", _EN_SAMPLE, "fr", dry_run=False,
        )
        assert "scaffolded" in status
        out = list((fake_repo / "_posts" / "fr").glob("*.md"))[0]
        fm, _ = tp.parse_frontmatter(out.read_text(encoding="utf-8"))
        assert fm["locale"] == "fr_FR"  # fallback path
    finally:
        tp._LOCALE_CODES["fr"] = "fr_FR"


# ---------------------------------------------------------------------------
# find_stub_locales
# ---------------------------------------------------------------------------


def test_find_stub_locales_lists_pending_after_scaffold(fake_repo):
    _seed_en(fake_repo)
    for lang in ("fr", "de", "es"):
        tp.scaffold_one("2026-05-19-sample", _EN_SAMPLE, lang, dry_run=False)
    pending = tp.find_stub_locales("2026-05-19-sample")
    assert {lang for lang, _ in pending} == {"fr", "de", "es"}


def test_find_stub_locales_excludes_translated(fake_repo):
    _seed_en(fake_repo)
    for lang in ("fr", "de", "es"):
        tp.scaffold_one("2026-05-19-sample", _EN_SAMPLE, lang, dry_run=False)
    # Pretend FR got translated — strip the marker.
    fr_file = list((fake_repo / "_posts" / "fr").glob("*.md"))[0]
    fr_file.write_text(
        fr_file.read_text(encoding="utf-8").replace(tp.STUB_MARKER, ""),
        encoding="utf-8",
    )
    pending = tp.find_stub_locales("2026-05-19-sample")
    assert {lang for lang, _ in pending} == {"de", "es"}


def test_find_stub_locales_skips_missing_files(fake_repo):
    _seed_en(fake_repo)
    # No scaffolds yet — nothing pending because the lang files don't
    # exist (the loop's `p.is_file()` guards covers it).
    assert tp.find_stub_locales("2026-05-19-sample") == []


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def test_main_reports_missing_slug(fake_repo, capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["translate_post.py", "nope"])
    rc = tp.main()
    assert rc == 1
    assert "not found" in capsys.readouterr().err


def test_main_dry_run_lists_targets(fake_repo, capsys, monkeypatch):
    _seed_en(fake_repo)
    monkeypatch.setattr(
        sys, "argv",
        ["translate_post.py", "2026-05-19-sample", "--dry-run", "--langs", "fr", "de"],
    )
    rc = tp.main()
    assert rc == 0
    out = capsys.readouterr().out
    assert "2 locale(s)" in out
    assert "would scaffold" in out


def test_main_scaffolds_when_not_dry_run(fake_repo, capsys, monkeypatch):
    _seed_en(fake_repo)
    monkeypatch.setattr(
        sys, "argv",
        ["translate_post.py", "2026-05-19-sample", "--langs", "fr"],
    )
    rc = tp.main()
    assert rc == 0
    assert "scaffolded" in capsys.readouterr().out
    assert (fake_repo / "_posts" / "fr").glob("*.md")


def test_main_list_stubs_reports_pending(fake_repo, capsys, monkeypatch):
    _seed_en(fake_repo)
    for lang in ("fr", "de", "es"):
        tp.scaffold_one("2026-05-19-sample", _EN_SAMPLE, lang, dry_run=False)
    monkeypatch.setattr(
        sys, "argv",
        ["translate_post.py", "2026-05-19-sample", "--list-stubs"],
    )
    rc = tp.main()
    assert rc == 0
    out = capsys.readouterr().out
    assert "3 locale(s) still pending" in out


def test_main_list_stubs_reports_done_when_all_translated(fake_repo, capsys, monkeypatch):
    _seed_en(fake_repo)
    for lang in ("fr", "de", "es"):
        tp.scaffold_one("2026-05-19-sample", _EN_SAMPLE, lang, dry_run=False)
        # Strip the marker to simulate a completed translation.
        f = next((fake_repo / "_posts" / lang).glob("*.md"))
        f.write_text(
            f.read_text(encoding="utf-8").replace(tp.STUB_MARKER, ""),
            encoding="utf-8",
        )
    monkeypatch.setattr(
        sys, "argv",
        ["translate_post.py", "2026-05-19-sample", "--list-stubs"],
    )
    rc = tp.main()
    assert rc == 0
    assert "all 27 locales translated" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# active_non_en_locales — registry plumbing
# ---------------------------------------------------------------------------


def test_active_non_en_locales_excludes_en(monkeypatch):
    """The function under test — verify it filters EN out."""
    import _lang_registry as lr

    class _Stub:
        def __init__(self, code):
            self.code = code

    monkeypatch.setattr(lr, "active", lambda: [_Stub("en"), _Stub("fr"), _Stub("de")])
    result = tp.active_non_en_locales()
    assert "en" not in result
    assert set(result) == {"fr", "de"}
