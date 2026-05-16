"""Tests for postbuild_lib.schemas — TechArticle + SoftwareSourceCode injectors.

The coverage gate requires 100% of postbuild_lib/. These tests exercise
the public functions and enough of the private helpers to exhaust every
branch (kind dispatch, fallback paths, idempotence, no-op skips).
"""
from __future__ import annotations

import json
import re

from postbuild_lib import schemas as sc


def _extract_tech_article(html: str) -> dict:
    """Pull the TechArticle JSON-LD body out of a rendered HTML page."""
    pattern = re.compile(
        r'<script[^>]*>(\{"@context":"https://schema.org","@type":"TechArticle"[^<]+)</script>'
    )
    m = pattern.search(html)
    assert m is not None, "TechArticle block not found"
    return json.loads(m.group(1))


# ---------------------------------------------------------------------------
# _parse_keywords
# ---------------------------------------------------------------------------

def test_parse_keywords_extracts_meta_keywords():
    html = (
        '<html><head>'
        '<meta name="keywords" content="Rust, ISO 20022, PQC">'
        "</head></html>"
    )
    assert sc._parse_keywords(html) == ["Rust", "ISO 20022", "PQC"]


def test_parse_keywords_returns_empty_when_no_meta():
    assert sc._parse_keywords("<html><head></head></html>") == []


def test_parse_keywords_unescapes_html_entities():
    html = (
        '<html><head>'
        '<meta name="keywords" content="Rust &amp; Open Source, blockchain">'
        "</head></html>"
    )
    assert sc._parse_keywords(html) == ["Rust & Open Source", "blockchain"]


# ---------------------------------------------------------------------------
# _detect_languages + _detect_dependencies
# ---------------------------------------------------------------------------

def test_detect_languages_finds_python_and_rust():
    langs = sc._detect_languages("rust, python, async")
    assert "Rust" in langs and "Python" in langs


def test_detect_languages_dedupes():
    # Two distinct tokens both map to WebAssembly — should appear once.
    langs = sc._detect_languages("wasm, webassembly, payments")
    assert langs.count("WebAssembly") == 1


def test_detect_languages_word_boundary_rejects_substring():
    # 'crust' contains 'rust' but shouldn't trigger Rust.
    assert sc._detect_languages("crust, bread") == []


def test_detect_dependencies_finds_iso_and_pqc():
    deps = sc._detect_dependencies("iso 20022, pqc, settlement")
    assert "ISO 20022" in deps and "Post-Quantum Cryptography" in deps


def test_detect_dependencies_dedupes():
    # 'iso 20022' substring appears in both 'iso 20022' and 'pain.001' /
    # 'pacs.008' labels; the label-set dedup keeps each unique label once.
    deps = sc._detect_dependencies("iso 20022, iso 20022, pain.001")
    assert deps == ["ISO 20022", "ISO 20022 pain.001"]


# ---------------------------------------------------------------------------
# _is_dated_article + _page_lang
# ---------------------------------------------------------------------------

def test_is_dated_article_accepts_top_level_dated_slug():
    p = sc.PUBLIC / "2025-09-01-foo" / "index.html"
    assert sc._is_dated_article(p) is True


def test_is_dated_article_accepts_localized_dated_slug():
    p = sc.PUBLIC / "fr" / "2025-09-01-foo" / "index.html"
    assert sc._is_dated_article(p) is True


def test_is_dated_article_rejects_non_dated_page():
    assert sc._is_dated_article(sc.PUBLIC / "about" / "index.html") is False


def test_is_dated_article_rejects_non_index_file():
    assert sc._is_dated_article(sc.PUBLIC / "2025-09-01-foo" / "robots.txt") is False


def test_page_lang_reads_html_lang():
    assert sc._page_lang('<html lang="fr-FR"><body></body></html>') == "fr-FR"


def test_page_lang_defaults_to_en_gb_when_no_lang_attr():
    assert sc._page_lang("<html><body></body></html>") == "en-GB"


# ---------------------------------------------------------------------------
# _tech_article_graph + inject_tech_article
# ---------------------------------------------------------------------------

def _article_html(keywords: str, title: str = "Quantum-Safe Payments — Sebastien Rousseau",
                  canonical: str = "https://sebastienrousseau.com/2025-09-01-foo/index.html") -> str:
    return (
        '<html lang="en-GB"><head>'
        f'<title>{title}</title>'
        f'<link rel="canonical" href="{canonical}">'
        f'<meta name="keywords" content="{keywords}">'
        "</head><body><main>body</main></body></html>"
    )


def test_inject_tech_article_emits_block_for_rust_post():
    page = sc.PUBLIC / "2025-09-01-foo" / "index.html"
    html = _article_html("rust, payments, pqc")
    out = sc.inject_tech_article(page, html)
    data = _extract_tech_article(out)
    assert data["programmingLanguage"] == "Rust"
    assert "Post-Quantum Cryptography" in data["dependencies"]
    assert data["headline"].startswith("Quantum-Safe Payments")
    assert data["inLanguage"] == "en-GB"


def test_inject_tech_article_skips_non_technical_post():
    page = sc.PUBLIC / "2025-09-01-foo" / "index.html"
    html = _article_html("interview, biography, leadership")
    assert sc.inject_tech_article(page, html) == html


def test_inject_tech_article_skips_when_keywords_missing():
    page = sc.PUBLIC / "2025-09-01-foo" / "index.html"
    html = '<html lang="en"><head><title>Foo — Sebastien Rousseau</title></head><body></body></html>'
    assert sc.inject_tech_article(page, html) == html


def test_inject_tech_article_skips_when_title_missing():
    page = sc.PUBLIC / "2025-09-01-foo" / "index.html"
    html = (
        '<html lang="en"><head>'
        '<link rel="canonical" href="https://example.com/x/">'
        '<meta name="keywords" content="rust">'
        "</head><body></body></html>"
    )
    assert sc.inject_tech_article(page, html) == html


def test_inject_tech_article_skips_when_canonical_missing():
    page = sc.PUBLIC / "2025-09-01-foo" / "index.html"
    html = (
        '<html lang="en"><head>'
        '<title>Foo — Sebastien Rousseau</title>'
        '<meta name="keywords" content="rust">'
        "</head><body></body></html>"
    )
    assert sc.inject_tech_article(page, html) == html


def test_inject_tech_article_skips_non_dated_pages():
    page = sc.PUBLIC / "about" / "index.html"
    html = _article_html("rust, pqc")
    assert sc.inject_tech_article(page, html) == html


def test_inject_tech_article_is_idempotent():
    page = sc.PUBLIC / "2025-09-01-foo" / "index.html"
    html = _article_html("rust")
    once = sc.inject_tech_article(page, html)
    twice = sc.inject_tech_article(page, once)
    # Second pass returns the same string — the existing block prevents reinsertion.
    assert once == twice


def test_inject_tech_article_emits_languages_list_when_multiple_match():
    page = sc.PUBLIC / "2025-09-01-foo" / "index.html"
    html = _article_html("rust, python")
    out = sc.inject_tech_article(page, html)
    data = _extract_tech_article(out)
    assert set(data["programmingLanguage"]) == {"Rust", "Python"}


# ---------------------------------------------------------------------------
# _category_label
# ---------------------------------------------------------------------------

def test_category_label_maps_section_titles():
    assert sc._category_label("PAYMENTS") == "Finance — Payments"
    assert sc._category_label("POST-QUANTUM CRYPTOGRAPHY") == "Cryptography — Post-Quantum"
    assert sc._category_label("AI AND VOICE") == "Artificial Intelligence"
    assert sc._category_label("OPEN-SOURCE RUST") == "Developer Tools — Rust"
    assert sc._category_label("WEB AND DEVELOPER ENVIRONMENT") == "Developer Tools — Web"
    assert sc._category_label("") == "Software Library"


# ---------------------------------------------------------------------------
# _languages_from_eyebrow
# ---------------------------------------------------------------------------

def test_languages_from_eyebrow_splits_on_middle_dot():
    assert sc._languages_from_eyebrow("Featured · Python · ISO 20022") == ["Python"]


def test_languages_from_eyebrow_handles_substring_match_but_exact_for_go():
    # 'JavaScript' substring matches 'javascript' token (full word in eyebrow).
    assert sc._languages_from_eyebrow("JavaScript · Security") == ["JavaScript"]
    # 'go' as a substring shouldn't trigger inside 'Go-Lang' eyebrow…
    # actually the rule is exact-match-only for 'go', so 'Go' alone matches.
    assert "Go" in sc._languages_from_eyebrow("Go · Tooling")
    # …but 'Cargo' (substring 'go') doesn't trigger Go.
    assert sc._languages_from_eyebrow("Cargo · Tooling") == []


# ---------------------------------------------------------------------------
# _parse_card + _build_software_source_code
# ---------------------------------------------------------------------------

def _card(title: str = "pain001",
          href: str = "https://pain001.com",
          eyebrow: str = "Featured · Python · ISO 20022",
          excerpt: str = "Automates ISO 20022 pain.001 file creation.") -> str:
    return (
        '<article class="newsroom-card">'
        f'<span class="newsroom-eyebrow">{eyebrow}</span>'
        f'<h3><a href="{href}">{title}</a></h3>'
        f'<p class="newsroom-excerpt">{excerpt}</p>'
        '</article>'
    )


def test_parse_card_returns_name_href_description_languages():
    parsed = sc._parse_card(_card())
    assert parsed is not None
    name, href, desc, langs = parsed
    assert name == "pain001"
    assert href == "https://pain001.com"
    assert "ISO 20022" in desc
    assert "Python" in langs


def test_parse_card_returns_none_when_h3_missing():
    body = '<article class="newsroom-card"><p class="newsroom-excerpt">x</p></article>'
    assert sc._parse_card(body) is None


def test_parse_card_returns_none_when_h3_text_empty():
    body = '<article class="newsroom-card"><h3><a href="https://x.com"></a></h3></article>'
    assert sc._parse_card(body) is None


def test_build_software_source_code_external_site_links_canonical_repo():
    rec = sc._build_software_source_code(_card(), "PAYMENTS", 1)
    assert rec is not None
    # External project site (pain001.com) → infer canonical sebastienrousseau GitHub.
    assert rec["codeRepository"] == "https://github.com/sebastienrousseau/pain001"
    assert rec["applicationCategory"] == "Finance — Payments"
    assert rec["programmingLanguage"] == "Python"


def test_build_software_source_code_github_href_used_directly():
    card = _card(title="QRC", href="https://github.com/sebastienrousseau/qrc")
    rec = sc._build_software_source_code(card, "PAYMENTS", 2)
    assert rec is not None
    assert rec["codeRepository"] == "https://github.com/sebastienrousseau/qrc"


def test_build_software_source_code_relative_href_resolves_to_site():
    card = _card(href="/projects/local/", eyebrow="Rust")
    rec = sc._build_software_source_code(card, "OPEN-SOURCE RUST", 3)
    assert rec is not None
    assert rec["url"].startswith("https://sebastienrousseau.com")


def test_build_software_source_code_returns_none_on_bad_card():
    assert sc._build_software_source_code('<article class="newsroom-card"></article>', "", 0) is None


def test_build_software_source_code_omits_languages_when_unknown():
    rec = sc._build_software_source_code(
        _card(eyebrow="Featured · Tooling"), "", 1,
    )
    assert rec is not None
    assert "programmingLanguage" not in rec


def test_build_software_source_code_emits_languages_list_when_multiple():
    rec = sc._build_software_source_code(
        _card(eyebrow="Rust · Python"), "OPEN-SOURCE RUST", 1,
    )
    assert rec is not None
    assert set(rec["programmingLanguage"]) == {"Rust", "Python"}


# ---------------------------------------------------------------------------
# build_projects_source_code (section path + flat fallback) + inject_software_source_code
# ---------------------------------------------------------------------------

def test_build_projects_source_code_walks_sections():
    html = (
        "<main>"
        '<h2 id="payments">PAYMENTS</h2>'
        + _card() + _card(title="pacs008", href="https://pacs008.com/")
        + '<h2 id="quantum">POST-QUANTUM CRYPTOGRAPHY</h2>'
        + _card(title="KyberLib", href="https://kyberlib.com/", eyebrow="Rust · Quantum")
        + "</main>"
    )
    payload = sc.build_projects_source_code(html)
    assert payload is not None
    graph = json.loads(payload)
    assert graph["@type"] == "ItemList"
    assert graph["numberOfItems"] == 3
    cats = [it["item"]["applicationCategory"] for it in graph["itemListElement"]]
    assert cats[0] == "Finance — Payments"
    assert cats[2] == "Cryptography — Post-Quantum"


def test_build_projects_source_code_falls_back_to_flat_when_no_sections():
    html = "<main>" + _card() + _card(title="qrc", href="https://github.com/sebastienrousseau/qrc") + "</main>"
    payload = sc.build_projects_source_code(html)
    assert payload is not None
    graph = json.loads(payload)
    assert graph["numberOfItems"] == 2
    assert all(it["item"]["applicationCategory"] == "Software Library" for it in graph["itemListElement"])


def test_build_projects_source_code_returns_none_on_empty_html():
    assert sc.build_projects_source_code("<main></main>") is None


def test_inject_software_source_code_only_runs_on_projects_index():
    page = sc.PUBLIC / "projects" / "index.html"
    html = "<html><body><main>" + _card() + "</main></body></html>"
    out = sc.inject_software_source_code(page, html)
    assert "SoftwareSourceCode" in out


def test_inject_software_source_code_skips_other_pages():
    page = sc.PUBLIC / "articles" / "index.html"
    html = "<html><body><main>" + _card() + "</main></body></html>"
    assert sc.inject_software_source_code(page, html) == html


def test_inject_software_source_code_skips_when_no_cards():
    page = sc.PUBLIC / "projects" / "index.html"
    html = "<html><body><main></main></body></html>"
    assert sc.inject_software_source_code(page, html) == html
