"""Case-study URLs + structured data (JSON-LD).

Leaf module split from build_case_studies (Phase 4.1): owns the site base URL,
the hub/study URL builders, the SoftwareSourceCode entity, and the Article /
Collection / Breadcrumb JSON-LD builders. Imports only the standard library, so
build_case_studies imports these back with no import cycle.
"""

from __future__ import annotations

import re

_BASE_URL = "https://sebastienrousseau.com"
def _hub_url(lang: str, url_segment: str) -> str:
    return "/case-studies/" if lang == "en" else f"/{lang}/{url_segment}/"
def _study_url(lang: str, url_segment: str, slug: str) -> str:
    return (
        f"/case-studies/{slug}/"
        if lang == "en"
        else f"/{lang}/{url_segment}/{slug}/"
    )
def _build_breadcrumb_jsonld(
    lbl: dict[str, str], lang: str, url_segment: str,
    study: dict | None = None,
) -> dict:
    bcp47 = {
        "en": "en-GB", "fr": "fr-FR", "de": "de-DE", "es": "es-ES",
        "it": "it-IT", "ja": "ja-JP", "ko": "ko-KR", "ru": "ru-RU",
    }.get(lang, lang)
    home_url = _BASE_URL + ("/" if lang == "en" else f"/{lang}/")
    hub_url = _BASE_URL + _hub_url(lang, url_segment)
    items = [
        {"@type": "ListItem", "position": 1, "name": lbl["Home"], "item": home_url},
        {"@type": "ListItem", "position": 2, "name": lbl["Case studies"], "item": hub_url},
    ]
    if study is not None:
        items.append({
            "@type": "ListItem", "position": 3,
            "name": study.get("title", study["slug"]),
            "item": _BASE_URL + _study_url(lang, url_segment, study["slug"]),
        })
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items,
        "inLanguage": bcp47,
    }
_BCP47_OVERRIDES = {
    "en": "en-GB", "fr": "fr-FR", "de": "de-DE", "es": "es-ES",
    "it": "it-IT", "ja": "ja-JP", "ko": "ko-KR", "ru": "ru-RU",
}
def _source_code_entity(study: dict, links: dict, person_id: str) -> dict | None:
    """Schema.org SoftwareSourceCode node for a repo-linked study."""
    if not (links.get("repo") or links.get("crates") or links.get("pypi")):
        return None
    language = "Rust" if links.get("crates") else ("Python" if links.get("pypi") else None)
    entity = {
        "@type": "SoftwareSourceCode",
        "name": study.get("title", study["slug"]),
        "codeRepository": links.get("repo"),
        "programmingLanguage": language,
        "license": "https://www.apache.org/licenses/LICENSE-2.0",
        "author": {"@type": "Person", "@id": person_id},
    }
    return {k: v for k, v in entity.items() if v is not None}
def _build_article_jsonld(
    study: dict, lbl: dict[str, str], lang: str, url_segment: str,
) -> dict:
    bcp47 = _BCP47_OVERRIDES.get(lang, lang)
    url = _BASE_URL + _study_url(lang, url_segment, study["slug"])
    person_id = f"{_BASE_URL}/#person"
    links = study.get("links", {}) or {}
    main_entity = _source_code_entity(study, links, person_id)
    about = [{
        "@type": "Organization",
        "name": "HSBC Holdings plc",
        "url": links["bank"],
    }] if "bank" in links else []
    # Collapse YAML folded-scalar newlines so JSON-LD stays a single
    # logical line. Postbuild HTML transforms apply unescape passes that
    # turn json.dumps's \n back into a literal newline, which breaks
    # test_page_inline_jsonld_is_valid_json.
    description = " ".join((study.get("problem", "") or "").split())[:200]
    # Schema.org Article requires datePublished. Case studies don't carry
    # a single launch date so derive one from the YAML ``period`` start
    # year (e.g. "2023 – present" → "2023-01-01"). Falls back to the
    # case-studies hub launch date when period is non-numeric.
    period = str(study.get("period", "")).strip()
    period_year_match = re.match(r"\s*(\d{4})", period)
    date_published = (
        f"{period_year_match.group(1)}-01-01" if period_year_match else "2025-09-01"
    )
    article: dict = {
        "@context": "https://schema.org",
        "@type": "Article",
        "@id": url + "#article",
        "headline": study.get("title", study["slug"]),
        "description": description,
        "url": url,
        "articleSection": lbl["Case study"],
        "inLanguage": bcp47,
        "datePublished": date_published,
        "dateModified": "2026-06-17",
        "isPartOf": {
            "@type": "CollectionPage",
            "@id": _BASE_URL + _hub_url(lang, url_segment) + "#collection",
        },
        "author": {"@type": "Person", "@id": person_id},
        "creator": {"@type": "Person", "@id": person_id},
        "publisher": {"@type": "Person", "@id": person_id},
        "license": "https://creativecommons.org/licenses/by/4.0/",
    }
    if study.get("banner"):
        article["image"] = study["banner"]
    if main_entity:
        article["mainEntity"] = main_entity
    if about:
        article["about"] = about
    return article
def _build_collection_jsonld(
    studies: list[dict], lbl: dict[str, str], lang: str, url_segment: str,
) -> dict:
    bcp47 = {
        "en": "en-GB", "fr": "fr-FR", "de": "de-DE", "es": "es-ES",
        "it": "it-IT", "ja": "ja-JP", "ko": "ko-KR", "ru": "ru-RU",
    }.get(lang, lang)
    hub_url = _BASE_URL + _hub_url(lang, url_segment)
    items = []
    for i, study in enumerate(studies, start=1):
        items.append({
            "@type": "ListItem",
            "position": i,
            "url": _BASE_URL + _study_url(lang, url_segment, study["slug"]),
            "name": study.get("title", study["slug"]),
        })
    return {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "@id": hub_url + "#collection",
        "name": lbl["Case studies"],
        "description": lbl["deck"],
        "url": hub_url,
        "inLanguage": bcp47,
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(studies),
            "itemListElement": items,
        },
    }
