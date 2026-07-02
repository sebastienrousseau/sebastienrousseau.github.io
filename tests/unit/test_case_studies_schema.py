"""Unit coverage for case_studies_schema — Phase 4.1 + 1.3.

Leaf module split from build_case_studies: URL builders + JSON-LD (Article,
Collection, Breadcrumb) + the SoftwareSourceCode entity. The URL builders are
covered in test_build_case_studies; this pins the previously-untested JSON-LD
builders and the repo-entity heuristic.
"""

from __future__ import annotations

import case_studies_schema as s

_LBL = {
    "Home": "Home",
    "Case studies": "Case studies",
    "Case study": "Case study",
    "deck": "Proof of work.",
}
_STUDY = {"slug": "acme", "title": "Acme", "problem": "Big\n  problem here.", "period": "2023 – present"}


# --- _source_code_entity ---------------------------------------------------


def test_source_code_entity_none_without_repo_links() -> None:
    assert s._source_code_entity(_STUDY, {}, "pid") is None


def test_source_code_entity_rust_for_crates() -> None:
    e = s._source_code_entity(_STUDY, {"repo": "https://gh/x", "crates": "y"}, "pid")
    assert e["programmingLanguage"] == "Rust"
    assert e["codeRepository"] == "https://gh/x"
    assert e["@type"] == "SoftwareSourceCode"


def test_source_code_entity_python_for_pypi_and_drops_none() -> None:
    e = s._source_code_entity(_STUDY, {"pypi": "z"}, "pid")
    assert e["programmingLanguage"] == "Python"
    assert "codeRepository" not in e  # repo was None → dropped


# --- _build_breadcrumb_jsonld ----------------------------------------------


def test_breadcrumb_two_items_without_study() -> None:
    out = s._build_breadcrumb_jsonld(_LBL, "en", "etudes-de-cas")
    assert out["@type"] == "BreadcrumbList"
    assert out["inLanguage"] == "en-GB"
    assert len(out["itemListElement"]) == 2


def test_breadcrumb_three_items_with_study_and_lang() -> None:
    out = s._build_breadcrumb_jsonld(_LBL, "fr", "etudes-de-cas", study=_STUDY)
    assert out["inLanguage"] == "fr-FR"
    assert len(out["itemListElement"]) == 3
    assert out["itemListElement"][2]["item"].endswith("/fr/etudes-de-cas/acme/")


# --- _build_article_jsonld -------------------------------------------------


def test_article_jsonld_core_fields_and_date_from_period() -> None:
    out = s._build_article_jsonld(_STUDY, _LBL, "en", "seg")
    assert out["@type"] == "Article"
    assert out["datePublished"] == "2023-01-01"  # from period start year
    assert out["url"].endswith("/case-studies/acme/")
    assert out["inLanguage"] == "en-GB"
    assert out["description"] == "Big problem here."  # folded newlines collapsed


def test_article_jsonld_date_fallback_and_banner_and_about() -> None:
    study = {"slug": "b", "title": "B", "period": "ongoing", "banner": "/b.webp",
             "links": {"bank": "https://hsbc.example"}}
    out = s._build_article_jsonld(study, _LBL, "en", "seg")
    assert out["datePublished"] == "2025-09-01"  # non-numeric period → fallback
    assert out["image"] == "/b.webp"
    assert out["about"][0]["name"] == "HSBC Holdings plc"


def test_article_jsonld_includes_main_entity_for_repo_study() -> None:
    study = {"slug": "c", "title": "C", "period": "2024", "links": {"crates": "x"}}
    out = s._build_article_jsonld(study, _LBL, "en", "seg")
    assert out["mainEntity"]["programmingLanguage"] == "Rust"


# --- _build_collection_jsonld ----------------------------------------------


def test_collection_jsonld_lists_all_studies() -> None:
    studies = [{"slug": "a", "title": "A"}, {"slug": "b", "title": "B"}]
    out = s._build_collection_jsonld(studies, _LBL, "ja", "jirei")
    assert out["@type"] == "CollectionPage"
    assert out["inLanguage"] == "ja-JP"
    assert out["mainEntity"]["numberOfItems"] == 2
    assert out["mainEntity"]["itemListElement"][1]["url"].endswith("/ja/jirei/b/")
