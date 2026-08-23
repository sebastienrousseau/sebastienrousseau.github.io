"""Unit coverage for build_case_studies — Phase 1.3 / de-risks Phase 4.1.

build_case_studies.py (1.5k LOC, a Phase 4.1 split target) generates the
/case-studies/ hub + per-study pages across locales, with a per-locale
overlay-merge system, and had no unit tests. Cover the pure overlay-merge
logic and URL builders — the parts a split must preserve exactly.
"""

from __future__ import annotations

import build_case_studies as cs
import case_studies_components as csc
import case_studies_schema as css

# --- _esc ------------------------------------------------------------------


def test_esc_escapes_and_quotes() -> None:
    assert cs._esc('a & <b> "c"') == "a &amp; &lt;b&gt; &quot;c&quot;"


def test_esc_none_is_empty() -> None:
    assert cs._esc(None) == ""
    assert cs._esc("") == ""


# --- _merge_list_of_dicts --------------------------------------------------


def test_merge_list_zips_overlay_over_base() -> None:
    base = [{"value": "42%", "label": "uptime"}, {"value": "3x", "label": "throughput"}]
    overlay = [{"label": "disponibilité"}]  # only first row, only label
    out = cs._merge_list_of_dicts(base, overlay)
    assert out[0] == {"value": "42%", "label": "disponibilité"}  # value kept, label overridden
    assert out[1] == {"value": "3x", "label": "throughput"}  # untouched


def test_merge_list_handles_empty_base() -> None:
    assert cs._merge_list_of_dicts([], [{"label": "x"}]) == []


# --- _merge_overlay --------------------------------------------------------


def test_merge_overlay_empty_returns_same() -> None:
    study = {"title": "T", "slug": "s"}
    assert cs._merge_overlay(study, {}) is study


def test_merge_overlay_keeps_en_canonical_fields() -> None:
    study = {"title": "T", "slug": "en-slug", "banner": "en.webp"}
    out = cs._merge_overlay(study, {"slug": "fr-slug", "banner": "fr.webp", "title": "Titre"})
    assert out["slug"] == "en-slug"  # slug stays EN-canonical
    assert out["banner"] == "en.webp"  # banner stays EN-canonical
    assert out["title"] == "Titre"  # prose field replaced


def test_merge_overlay_zips_list_fields() -> None:
    study = {"outcome_highlights": [{"value": "9", "label": "a"}, {"value": "8", "label": "b"}]}
    out = cs._merge_overlay(study, {"outcome_highlights": [{"label": "A"}]})
    assert out["outcome_highlights"][0] == {"value": "9", "label": "A"}
    assert out["outcome_highlights"][1] == {"value": "8", "label": "b"}


# --- URL builders ----------------------------------------------------------


def test_hub_url_en_vs_locale() -> None:
    assert css._hub_url("en", "etudes-de-cas") == "/case-studies/"
    assert css._hub_url("fr", "etudes-de-cas") == "/fr/etudes-de-cas/"


def test_study_url_en_vs_locale() -> None:
    assert css._study_url("en", "seg", "acme") == "/case-studies/acme/"
    assert css._study_url("ja", "jirei", "acme") == "/ja/jirei/acme/"


def test_related_article_href_en_uses_plain_slug() -> None:
    assert csc._related_article_href("my-post", "en", {"my-post": "mon-article"}) == "/my-post/"


def test_related_article_href_locale_uses_slug_map() -> None:
    out = csc._related_article_href("my-post", "fr", {"my-post": "mon-article"})
    assert out == "/fr/mon-article/"


def test_related_article_href_locale_falls_back_to_en_slug() -> None:
    # slug absent from the map → fall back to the EN slug under the /<lang>/ path
    assert csc._related_article_href("my-post", "fr", {}) == "/fr/my-post/"
