"""Article identity alignment (F-08) and FAQPage emission (F-12)."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "postbuild"))

from postbuild_lib.schemas import align_article_identity, inject_faq_schema

CANON = "https://sebastienrousseau.com/2026-08-04-slug/"
PAGE = Path("public/2026-08-04-slug/index.html")


def _page(head_extra: str = "", body: str = "") -> str:
    return (
        f'<html lang="en-GB"><head><link rel="canonical" href="{CANON}">{head_extra}'
        f"</head><body>{body}</body></html>"
    )


def _blocks(html: str) -> list[dict]:
    return [
        json.loads(raw)
        for raw in re.findall(r'ld\+json">(.*?)</script>', html, re.DOTALL)
    ]


def _nodes(html: str) -> list[dict]:
    flat: list[dict] = []

    def walk(o: object) -> None:
        if isinstance(o, dict):
            flat.append(o)
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    for b in _blocks(html):
        walk(b)
    return flat


# --------------------------------------------------------------------- F-08

_DIVERGENT = _page(
    body=(
        '<script type="application/ld+json">'
        '{"@context":"https://schema.org","@graph":['
        '{"@type":"BlogPosting","url":"https://sebastienrousseau.com/2026-08-04-slug",'
        '"inLanguage":"en","datePublished":"2026-08-04T07:07:07+00:00",'
        '"dateModified":"2026-08-04",'
        '"mainEntityOfPage":{"@type":"WebPage",'
        '"@id":"https://sebastienrousseau.com/2026-08-04-slug"}},'
        '{"@type":"BreadcrumbList"}]}</script>'
        '<script type="application/ld+json">'
        '{"@context":"https://schema.org","@type":"TechArticle",'
        f'"url":"{CANON}","inLanguage":"en-GB",'
        f'"mainEntityOfPage":{{"@type":"WebPage","@id":"{CANON}"}}}}</script>'
    )
)


def test_every_article_node_binds_to_the_canonical_url() -> None:
    out = align_article_identity(_DIVERGENT)
    articles = [n for n in _nodes(out) if n.get("@type") in {"BlogPosting", "TechArticle"}]
    assert len(articles) == 2
    for node in articles:
        assert node["url"] == CANON
        assert node["mainEntityOfPage"]["@id"] == CANON


def test_both_article_nodes_resolve_to_one_entity() -> None:
    """Same mainEntityOfPage @id is what merges two nodes into one entity."""
    out = align_article_identity(_DIVERGENT)
    ids = {
        n["mainEntityOfPage"]["@id"]
        for n in _nodes(out)
        if n.get("@type") in {"BlogPosting", "TechArticle"}
    }
    assert ids == {CANON}


def test_inlanguage_is_normalised_to_the_page_language() -> None:
    out = align_article_identity(_DIVERGENT)
    langs = {n["inLanguage"] for n in _nodes(out) if "inLanguage" in n}
    assert langs == {"en-GB"}


def test_date_only_datemodified_becomes_a_full_timestamp() -> None:
    out = align_article_identity(_DIVERGENT)
    blog = next(n for n in _nodes(out) if n.get("@type") == "BlogPosting")
    assert blog["dateModified"] == "2026-08-04T07:07:07+00:00"


def test_alignment_is_idempotent() -> None:
    once = align_article_identity(_DIVERGENT)
    assert align_article_identity(once) == once


def test_non_article_nodes_are_untouched() -> None:
    out = align_article_identity(_DIVERGENT)
    crumb = next(n for n in _nodes(out) if n.get("@type") == "BreadcrumbList")
    assert set(crumb) == {"@type"}


def test_page_without_canonical_is_unchanged() -> None:
    html = '<html lang="en"><body><script type="application/ld+json">{"@type":"BlogPosting"}</script></body></html>'
    assert align_article_identity(html) == html


def test_malformed_jsonld_is_left_alone() -> None:
    html = _page(body='<script type="application/ld+json">{not json}</script>')
    assert align_article_identity(html) == html


# --------------------------------------------------------------------- F-12

_FAQ_H2 = '<h2 id="frequently-asked-questions">Frequently Asked Questions</h2>'
_ANSWER = "Because the switching charge disappears entirely on that date, egress included."


def test_inline_br_shape_is_extracted() -> None:
    """<p><strong>Q?</strong><br />A</p> — what dated articles actually ship."""
    html = _page(body=f"{_FAQ_H2}<p><strong>Why January?</strong><br />{_ANSWER}</p>")
    faq = next(b for b in _blocks(inject_faq_schema(PAGE, html)) if b["@type"] == "FAQPage")
    assert faq["mainEntity"][0]["name"] == "Why January?"
    assert faq["mainEntity"][0]["acceptedAnswer"]["text"] == _ANSWER


def test_separate_paragraph_shape_is_extracted() -> None:
    html = _page(body=f"{_FAQ_H2}<p><strong>Why January?</strong></p><p>{_ANSWER}</p>")
    faq = next(b for b in _blocks(inject_faq_schema(PAGE, html)) if b["@type"] == "FAQPage")
    assert faq["mainEntity"][0]["acceptedAnswer"]["text"] == _ANSWER


def test_collapsible_details_shape_is_extracted() -> None:
    html = _page(
        body=f'{_FAQ_H2}<section class="qa-list"><details class="qa-item">'
        f'<summary class="qa-q">Why January?</summary>'
        f'<div class="qa-a"><p>{_ANSWER}</p></div></details></section>'
    )
    faq = next(b for b in _blocks(inject_faq_schema(PAGE, html)) if b["@type"] == "FAQPage")
    assert faq["mainEntity"][0]["acceptedAnswer"]["text"] == _ANSWER


def test_faq_is_scoped_to_its_own_section() -> None:
    """A bolded lead-in after the next <h2> must not become a question."""
    html = _page(
        body=f"{_FAQ_H2}<p><strong>Real question?</strong><br />{_ANSWER}</p>"
        f'<h2 id="references">References</h2>'
        f"<p><strong>Not a question?</strong><br />{_ANSWER}</p>"
    )
    faq = next(b for b in _blocks(inject_faq_schema(PAGE, html)) if b["@type"] == "FAQPage")
    assert [q["name"] for q in faq["mainEntity"]] == ["Real question?"]


def test_short_answers_are_rejected() -> None:
    html = _page(body=f"{_FAQ_H2}<p><strong>Q?</strong><br />No.</p>")
    assert "FAQPage" not in inject_faq_schema(PAGE, html)


def test_page_without_faq_section_is_unchanged() -> None:
    html = _page(body="<h2 id=\"other\">Other</h2><p><strong>Q?</strong><br />Long enough answer.</p>")
    assert inject_faq_schema(PAGE, html) == html


def test_faq_schema_is_idempotent() -> None:
    html = _page(body=f"{_FAQ_H2}<p><strong>Why January?</strong><br />{_ANSWER}</p>")
    once = inject_faq_schema(PAGE, html)
    assert inject_faq_schema(PAGE, once) == once


def test_faq_id_and_ispartof_reference_the_canonical() -> None:
    html = _page(body=f"{_FAQ_H2}<p><strong>Why January?</strong><br />{_ANSWER}</p>")
    faq = next(b for b in _blocks(inject_faq_schema(PAGE, html)) if b["@type"] == "FAQPage")
    assert faq["@id"] == CANON + "#faq"
    assert faq["isPartOf"]["@id"] == CANON


def test_html_entities_are_decoded_in_questions() -> None:
    html = _page(body=f"{_FAQ_H2}<p><strong>Isn&#39;t it done?</strong><br />{_ANSWER}</p>")
    faq = next(b for b in _blocks(inject_faq_schema(PAGE, html)) if b["@type"] == "FAQPage")
    assert faq["mainEntity"][0]["name"] == "Isn't it done?"


@pytest.mark.parametrize("anchor", ["faq", "questions", "frequently-asked-questions"])
def test_recognised_faq_anchors(anchor: str) -> None:
    html = _page(body=f'<h2 id="{anchor}">FAQ</h2><p><strong>Q here?</strong><br />{_ANSWER}</p>')
    assert "FAQPage" in inject_faq_schema(PAGE, html)


# ---------------------------------------------------- defensive branches
#
# postbuild_lib is gated at 100 % coverage, so every guard needs a case.


def test_non_dict_graph_members_are_ignored() -> None:
    """A JSON-LD array holding scalars must not crash the walker."""
    html = _page(
        body='<script type="application/ld+json">'
        '{"@context":"https://schema.org","@graph":["a string",42,null,'
        '{"@type":"BlogPosting","url":"x"}]}</script>'
    )
    out = align_article_identity(html)
    blog = next(n for n in _nodes(out) if n.get("@type") == "BlogPosting")
    assert blog["url"] == CANON


def test_string_main_entity_of_page_is_upgraded_to_a_node() -> None:
    html = _page(
        body='<script type="application/ld+json">'
        '{"@type":"BlogPosting","mainEntityOfPage":"https://sebastienrousseau.com/other"}'
        "</script>"
    )
    blog = _blocks(align_article_identity(html))[0]
    assert blog["mainEntityOfPage"] == {"@type": "WebPage", "@id": CANON}


def test_string_main_entity_already_canonical_is_untouched() -> None:
    html = _page(
        body='<script type="application/ld+json">'
        f'{{"@type":"BlogPosting","url":"{CANON}","mainEntityOfPage":"{CANON}"}}</script>'
    )
    assert align_article_identity(html) == html


def test_answer_collection_stops_at_the_next_question() -> None:
    """Shape 2: following <p>s belong to the answer until a new bold question."""
    html = _page(
        body=f"{_FAQ_H2}<p><strong>First?</strong></p><p>{_ANSWER}</p>"
        f"<p><strong>Second?</strong></p><p>{_ANSWER}</p>"
    )
    faq = next(b for b in _blocks(inject_faq_schema(PAGE, html)) if b["@type"] == "FAQPage")
    assert [q["name"] for q in faq["mainEntity"]] == ["First?", "Second?"]
    assert faq["mainEntity"][0]["acceptedAnswer"]["text"] == _ANSWER


def test_answer_collection_is_bounded() -> None:
    """A runaway section must not swallow the rest of the article."""
    paras = "".join(f"<p>Paragraph {i} of a long answer body here.</p>" for i in range(10))
    html = _page(body=f"{_FAQ_H2}<p><strong>Why?</strong></p>{paras}")
    faq = next(b for b in _blocks(inject_faq_schema(PAGE, html)) if b["@type"] == "FAQPage")
    assert faq["mainEntity"][0]["acceptedAnswer"]["text"].count("Paragraph") == 4


def test_faq_without_canonical_still_emits() -> None:
    html = (
        '<html lang="en-GB"><head></head><body>'
        f"{_FAQ_H2}<p><strong>Why January?</strong><br />{_ANSWER}</p></body></html>"
    )
    faq = next(b for b in _blocks(inject_faq_schema(PAGE, html)) if b["@type"] == "FAQPage")
    assert "@id" not in faq
    assert faq["mainEntity"][0]["name"] == "Why January?"


def test_is_article_node_rejects_non_dicts() -> None:
    """Called directly: the walker guards this, but the function is public
    enough that its contract should hold on its own."""
    from postbuild_lib.schemas import _is_article_node

    assert _is_article_node("BlogPosting") is False
    assert _is_article_node(None) is False
    assert _is_article_node({"@type": "BlogPosting"}) is True
    assert _is_article_node({"@type": ["TechArticle", "CreativeWork"]}) is True
    assert _is_article_node({"@type": "Person"}) is False
