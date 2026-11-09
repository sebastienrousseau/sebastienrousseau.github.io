# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""postbuild_lib/profile_person.py: Person JSON-LD rebuilt from profile.yml."""

from __future__ import annotations

import json
import re

import _profile
from postbuild_lib.profile_person import apply_person_profile

_STALE_GRAPH = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "Person",
            "@id": "https://sebastienrousseau.com/#person",
            "name": "Sebastien Rousseau",
            "jobTitle": "Wholesale Payments & AI Leader",
            "description": "Senior payments leader with nearly two decades across Tier-1 banks.",
            "alumniOf": [{"@type": "Organization", "name": "Virgin Group"}],
            "hasCredential": [
                {
                    "@type": "EducationalOccupationalCredential",
                    "name": "Nearly two decades across Tier-1 banks",
                    "recognizedBy": {"@type": "Organization", "name": "HSBC"},
                }
            ],
            "knowsAbout": [{"@type": "DefinedTerm", "name": "ISO 20022"}],
            "sameAs": ["https://github.com/sebastienrousseau"],
        },
        {
            "@type": "WebSite",
            "@id": "https://sebastienrousseau.com/#website",
            "description": "AI, banking and financial services expert.",
        },
    ],
}


def _page(graph: object, pretty: bool = True) -> str:
    body = json.dumps(graph, indent=2) if pretty else json.dumps(graph, separators=(",", ":"))
    return f'<html><head><script type="application/ld+json">{body}</script></head></html>'


def _graph(html: str) -> list[dict]:
    body = re.search(r"<script[^>]*>(.*?)</script\s*>", html, re.S | re.I)
    assert body
    return json.loads(body.group(1))["@graph"]


def test_person_takes_profile_facts_and_keeps_theme_fields() -> None:
    person, site = _graph(apply_person_profile(_page(_STALE_GRAPH)))
    profile = _profile.load()
    assert person["jobTitle"] == profile["job_title_formal"]
    assert person["description"] == profile["bios"]["short"]
    assert [a["@type"] for a in person["alumniOf"]] == ["CollegeOrUniversity"] * 3
    assert "recognizedBy" not in json.dumps(person)
    assert "two decades" not in json.dumps(person)
    assert person["knowsAbout"] == [{"@type": "DefinedTerm", "name": "ISO 20022"}]
    assert person["sameAs"] == ["https://github.com/sebastienrousseau"]
    assert site["description"] == profile["bios"]["one_line"]


def test_current_page_is_left_byte_identical() -> None:
    once = apply_person_profile(_page(_STALE_GRAPH, pretty=False))
    assert apply_person_profile(once) == once


def test_page_without_person_is_untouched() -> None:
    html = _page({"@type": "BlogPosting", "headline": "x"})
    assert apply_person_profile(html) == html


def test_invalid_json_block_is_untouched() -> None:
    html = '<script type="application/ld+json">{"@id": "https://sebastienrousseau.com/#person",</script>'
    assert apply_person_profile(html) == html


def test_other_person_nodes_are_untouched() -> None:
    other = {"@type": "Person", "@id": "https://example.com/#someone", "jobTitle": "Editor"}
    html = _page({"@graph": [other, {"@id": "https://sebastienrousseau.com/#website"}]})
    assert _graph(apply_person_profile(html))[0] == other
