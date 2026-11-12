# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""scripts/generators/build_services.py: the Work with me pages (F-4)."""

from __future__ import annotations

import html
import re

import _profile
import build_services as bs

from . import _jsonld

DATA = bs.load()


def _faq_text(body: str) -> list[tuple[str, str]]:
    pairs = re.findall(r'<summary class="qa-q">(.*?)</summary><div class="qa-a"><p>(.*?)</p>', body)
    return [(html.unescape(q), html.unescape(a)) for q, a in pairs]


def test_hub_links_speaking_and_both_detail_pages() -> None:
    body = bs.render_hub(DATA["hub"], DATA["disclosure"])
    for href in ("/speaking/", "/work-with-me/research/", "/work-with-me/open-source/"):
        assert f'href="{href}"' in body
    assert body.count("<h1") == 1 and "subject=general" in body


def test_answer_paragraphs_are_40_to_60_words() -> None:
    for page in DATA["pages"]:
        words = len(page["answer"].split())
        assert 40 <= words <= 75, (page["key"], words)


def test_each_page_has_the_full_structure_and_its_subject() -> None:
    for page in DATA["pages"]:
        body = bs.render_page(page, DATA["disclosure"], ["x"])
        for heading in (
            "Who it",
            "What you get",
            "How it works",
            "On the record",
            "Questions and answers",
        ):
            assert heading in body
        assert f"subject={page['subject']}" in body
        assert 5 <= len(page["faq"]) <= 7
        assert body.count("<li>") == len(page["steps"]) + 1


def test_faq_jsonld_matches_the_visible_text_word_for_word() -> None:
    for page in DATA["pages"]:
        visible = _faq_text(bs.render_page(page, DATA["disclosure"], []))
        ld = _jsonld.first(bs.jsonld(page))
        faq = next(n for n in ld["@graph"] if n["@type"] == "FAQPage")
        marked = [(q["name"], q["acceptedAnswer"]["text"]) for q in faq["mainEntity"]]
        assert visible == marked


def test_service_jsonld_names_the_person_and_no_offers() -> None:
    for page in DATA["pages"]:
        ld = _jsonld.first(bs.jsonld(page))
        svc = next(n for n in ld["@graph"] if n["@type"] == "Service")
        assert svc["provider"] == {"@id": "https://sebastienrousseau.com/#person"}
        assert "offers" not in svc and svc["url"].endswith(page["path"])


def test_proof_comes_from_profile_and_metrics_only() -> None:
    profile = _profile.load()
    lines = bs.proof_items(
        ["epaa", "fiap", "downloads", "trust", "nope"], {"downloads_total": "52.8M"}, profile
    )
    assert lines[0].startswith(profile["epaa"]["wording"])
    assert any("52.8M" in line for line in lines) and len(lines) == 4
    assert bs.proof_items(["downloads"], {}, profile) == []


def test_descriptions_fit_the_length_budget() -> None:
    for item in [DATA["hub"], *DATA["pages"]]:
        n = len(bs._text(item["description"]))
        assert 120 <= n <= 160, (item["path"], n)
