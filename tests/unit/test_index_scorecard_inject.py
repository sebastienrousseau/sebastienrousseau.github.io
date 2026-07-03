"""Unit tests for the index-scorecard postbuild injection pass.

Covers every branch of ``postbuild_lib.index_scorecard`` (the build gates the
``postbuild_lib`` package at 100% coverage): marker detection, idempotency,
spec/strings resolution with locale fallback, SRI stamping, and the
``</script>``-safe unicode escaping of the inlined JSON data island.
"""

from __future__ import annotations

import json

import postbuild_assets
import pytest
from postbuild_lib import index_scorecard as isc

SLUG = "demo-index"

SPEC = {
    "slug": SLUG,
    "scale": {"min": 0, "max": 100, "round": 0},
    "dimensions": [{"id": "a", "label": "A", "weight": 1.0, "default": 0}],
    "bands": [{"id": "low", "min": 0, "max": 100, "label": "Low"}],
}

MARKER = f'<div class="index-scorecard" data-index="{SLUG}"></div>'


@pytest.fixture
def data_dirs(tmp_path, monkeypatch):
    """Point the pass at an isolated _data/indices + _data/i18n tree."""
    indices = tmp_path / "indices"
    i18n = tmp_path / "i18n"
    indices.mkdir()
    (i18n / "en").mkdir(parents=True)
    (indices / f"{SLUG}.json").write_text(json.dumps(SPEC), encoding="utf-8")
    (i18n / "en" / "strings.json").write_text(
        json.dumps(
            {
                "scorecard.heading": "Score it",
                "scorecard.fallback": "Enable JS to score interactively.",
                "nav.aria.other": "not a scorecard key",
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(isc, "INDICES_DIR", indices)
    monkeypatch.setattr(isc, "I18N_DIR", i18n)
    monkeypatch.setattr(postbuild_assets, "asset_hashes", {}, raising=False)
    return {"indices": indices, "i18n": i18n}


def _page(body: str, lang: str | None = "en") -> str:
    head = f'<html lang="{lang}">' if lang is not None else "<html>"
    return f"{head}<body>{body}</body></html>"


# --- marker-level behaviour --------------------------------------------------


def test_no_marker_is_noop(data_dirs):
    html = "<html lang='en'><body><p>nothing here</p></body></html>"
    assert isc.inject_index_scorecard(html) == html


def test_already_hydrated_is_idempotent(data_dirs):
    html = _page("<index-scorecard>already</index-scorecard>" + MARKER)
    # The substring guard short-circuits — no second element is added.
    assert isc.inject_index_scorecard(html) == html


def test_marker_without_data_index_left_untouched(data_dirs):
    html = _page('<div class="index-scorecard"></div>')
    out = isc.inject_index_scorecard(html)
    assert out == html  # nothing to resolve


def test_missing_spec_leaves_marker(data_dirs):
    html = _page('<div class="index-scorecard" data-index="does-not-exist"></div>')
    assert isc.inject_index_scorecard(html) == html


def test_happy_path_injects_element_island_and_script(data_dirs):
    out = isc.inject_index_scorecard(_page(MARKER))
    assert '<index-scorecard data-index="demo-index" dir="ltr">' in out
    assert 'class="index-scorecard__fallback">Enable JS to score interactively.' in out
    assert '<script type="application/json" class="index-scorecard-data">' in out
    assert '<script type="module" src="/_csp/index-scorecard.js">' in out
    # Data island parses back and carries only the scorecard.* strings.
    island = out.split('class="index-scorecard-data">', 1)[1].split("</script>", 1)[0]
    # Undo the </script>-safe unicode escaping before parsing.
    payload = json.loads(
        island.replace("\\u003c", "<").replace("\\u003e", ">").replace("\\u0026", "&")
    )
    assert payload["spec"]["slug"] == SLUG
    assert payload["lang"] == "en"
    assert payload["dir"] == "ltr"
    assert payload["strings"] == {
        "scorecard.heading": "Score it",
        "scorecard.fallback": "Enable JS to score interactively.",
    }


# --- locale + direction ------------------------------------------------------


def test_rtl_language_sets_dir_rtl(data_dirs):
    (data_dirs["i18n"] / "ar").mkdir()
    (data_dirs["i18n"] / "ar" / "strings.json").write_text(
        json.dumps({"scorecard.heading": "قيّم"}), encoding="utf-8"
    )
    out = isc.inject_index_scorecard(_page(MARKER, lang="ar"))
    assert 'dir="rtl"' in out
    assert '"lang":"ar"' in out


def test_missing_lang_defaults_to_en(data_dirs):
    out = isc.inject_index_scorecard(_page(MARKER, lang=None))
    assert '"lang":"en"' in out


def test_strings_fall_back_to_en_when_locale_missing(data_dirs):
    # 'de' has no strings.json — loader falls through to en.
    assert isc._load_strings("de") == {
        "scorecard.heading": "Score it",
        "scorecard.fallback": "Enable JS to score interactively.",
    }


def test_default_fallback_used_when_key_absent(data_dirs):
    (data_dirs["i18n"] / "en" / "strings.json").write_text(
        json.dumps({"scorecard.heading": "Only heading"}), encoding="utf-8"
    )
    out = isc.inject_index_scorecard(_page(MARKER))
    assert "The maturity dimensions are tabulated above." in out


# --- resilience of loaders ---------------------------------------------------


def test_load_spec_handles_invalid_json(data_dirs):
    (data_dirs["indices"] / "broken.json").write_text("{ not json", encoding="utf-8")
    assert isc._load_spec("broken") is None


def test_load_strings_skips_invalid_json_then_uses_en(data_dirs):
    (data_dirs["i18n"] / "it").mkdir()
    (data_dirs["i18n"] / "it" / "strings.json").write_text("{bad", encoding="utf-8")
    # it is invalid -> continue -> en is valid and returned.
    assert "scorecard.heading" in isc._load_strings("it")


def test_load_strings_empty_when_nothing_resolves(data_dirs, monkeypatch):
    empty = data_dirs["i18n"].parent / "empty-i18n"
    empty.mkdir()
    monkeypatch.setattr(isc, "I18N_DIR", empty)
    assert isc._load_strings("en") == {}


# --- SRI stamping ------------------------------------------------------------


def test_integrity_stamped_when_digest_known(data_dirs, monkeypatch):
    monkeypatch.setattr(
        postbuild_assets,
        "asset_hashes",
        {"index-scorecard.js": "sha256-AAA sha256-BBB"},
        raising=False,
    )
    out = isc.inject_index_scorecard(_page(MARKER))
    assert (
        '<script type="module" src="/_csp/index-scorecard.js" '
        'integrity="sha256-AAA sha256-BBB" crossorigin="anonymous"></script>'
    ) in out


# --- data-island escaping ----------------------------------------------------


def test_data_island_escapes_script_breakout(data_dirs):
    hostile = dict(SPEC)
    hostile["title"] = "</script><script>alert(1)</script>"
    (data_dirs["indices"] / "hostile.json").write_text(
        json.dumps(hostile), encoding="utf-8"
    )
    html = _page('<div class="index-scorecard" data-index="hostile"></div>')
    out = isc.inject_index_scorecard(html)
    # No literal </script> from the payload survives inside the JSON island.
    island = out.split('class="index-scorecard-data">', 1)[1].split("</script>", 1)[0]
    assert "</script>" not in island
    assert "\\u003c/script\\u003e" in island
