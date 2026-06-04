"""Tests for scripts/_lang_registry.py.

Covers the loaders + slug-resolution helpers used by every i18n
pipeline stage. Parity (key-set match across languages) is enforced
by the integration smoke gates in build.sh; these unit tests cover
the loader behaviour, error paths, and `LANGUAGES` invariants that
the smoke gates can't reach.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import _lang_registry as lr  # type: ignore[import-not-found]


class TestLanguagesTable:
    def test_en_present_and_active(self) -> None:
        en = next((lg for lg in lr.LANGUAGES if lg.code == "en"), None)
        assert en is not None
        assert en.active is True
        assert en.bcp47 == "en-GB"
        assert en.og_locale == "en_GB"

    def test_fr_present_and_active(self) -> None:
        fr = next((lg for lg in lr.LANGUAGES if lg.code == "fr"), None)
        assert fr is not None
        assert fr.active is True
        assert fr.rtl is False

    def test_de_present_and_active(self) -> None:
        de = next((lg for lg in lr.LANGUAGES if lg.code == "de"), None)
        assert de is not None
        assert de.active is True

    def test_rtl_flag_set_for_ar_and_he(self) -> None:
        for code in ("ar", "he"):
            lg = next((entry for entry in lr.LANGUAGES if entry.code == code), None)
            assert lg is not None, f"{code} missing"
            assert lg.rtl is True, f"{code} should carry rtl=True"

    def test_codes_are_unique(self) -> None:
        codes = [lg.code for lg in lr.LANGUAGES]
        assert len(codes) == len(set(codes))

    def test_bcp47_tags_are_unique(self) -> None:
        tags = [lg.bcp47 for lg in lr.LANGUAGES]
        assert len(tags) == len(set(tags))


class TestLoaders:
    @pytest.mark.parametrize("loader", [
        lr.load_slugs, lr.load_topics, lr.load_static_pages,
        lr.load_strings, lr.load_labels, lr.load_takeaway_labels,
        lr.load_home_patches, lr.load_static_bodies,
        lr.load_static_patches, lr.load_chrome_patches_inline,
        lr.load_author,
    ])
    def test_active_languages_load_clean(self, loader) -> None:
        for code in ("en", "fr", "de"):
            try:
                result = loader(code)
            except lr.LanguageError:
                # Some loaders intentionally don't require EN to exist
                # (e.g. static_bodies only ships for translation targets).
                # But for fr+de the active langs must load.
                if code != "en":
                    raise
                continue
            assert result, f"{loader.__name__}({code!r}) returned empty"

    def test_missing_lang_raises(self) -> None:
        with pytest.raises(lr.LanguageError):
            lr.load_slugs("zz")  # not in any data dir

    def test_strings_strips_comment_keys(self) -> None:
        strings = lr.load_strings("en")
        assert all(not k.startswith("_") for k in strings)

    def test_labels_strips_comment_keys(self) -> None:
        labels = lr.load_labels("en")
        assert all(not k.startswith("_") for k in labels)


class TestSlugResolution:
    def test_fr_slug_round_trips(self) -> None:
        # Pick one EN slug we know exists
        slugs = lr.load_slugs("fr")["articles"]
        en, fr = next(iter(slugs.items()))
        assert lr.fr_slug(en) == fr
        assert lr.en_slug(fr) == en

    def test_fr_slug_unknown_passes_through(self) -> None:
        assert lr.fr_slug("not-a-real-slug") == "not-a-real-slug"
        assert lr.en_slug("not-a-real-slug") == "not-a-real-slug"


class TestParityShapes:
    """These complement the CI gates — every parity gate's reference is EN."""

    @pytest.mark.parametrize("loader,active_only", [
        (lr.load_strings, False),
        (lr.load_labels, False),
        (lr.load_takeaway_labels, False),
        (lr.load_author, False),
    ])
    def test_en_keys_subset_of_fr(self, loader, active_only) -> None:
        en = set(loader("en"))
        fr = set(loader("fr"))
        missing = en - fr
        assert not missing, f"FR missing keys vs EN: {sorted(missing)}"

    @pytest.mark.parametrize("loader,active_only", [
        (lr.load_strings, False),
        (lr.load_labels, False),
        (lr.load_takeaway_labels, False),
        (lr.load_author, False),
    ])
    def test_en_keys_subset_of_de(self, loader, active_only) -> None:
        en = set(loader("en"))
        de = set(loader("de"))
        missing = en - de
        assert not missing, f"DE missing keys vs EN: {sorted(missing)}"


class TestChromePatchesGenerator:
    def test_build_chrome_patches_returns_pairs(self) -> None:
        patches = lr.build_chrome_patches("fr")
        assert patches
        for entry in patches:
            assert isinstance(entry, tuple) and len(entry) == 2
            assert isinstance(entry[0], str)
            assert isinstance(entry[1], str)

    def test_build_chrome_patches_en_yields_empty_set(self) -> None:
        # EN→EN means every key's value equals itself → no patches
        patches = lr.build_chrome_patches("en")
        assert patches == []

    def test_de_has_distinct_patches(self) -> None:
        fr = lr.build_chrome_patches("fr")
        de = lr.build_chrome_patches("de")
        assert fr != de
