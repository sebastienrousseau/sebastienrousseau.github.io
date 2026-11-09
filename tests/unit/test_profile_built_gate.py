# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""tests/validation/test_profile_built.py: the checks it runs on public/."""

from __future__ import annotations

import json

import _profile

from tests.validation import test_profile_built as gate

PROFILE = _profile.load()


def _page(node: dict) -> str:
    return f'<script type="application/ld+json">{json.dumps({"@graph": [node]})}</script>'


def _person(**overrides: object) -> dict:
    node = {
        "@type": "Person",
        "@id": gate.PERSON_ID,
        "name": "Sebastien Rousseau",
        "jobTitle": PROFILE["job_title_formal"],
        "description": PROFILE["bios"]["short"],
        "alumniOf": [{"@type": "CollegeOrUniversity", "name": "University of Westminster"}],
    }
    return node | overrides


def test_current_person_passes() -> None:
    assert gate.person_defects(_page(_person()), PROFILE) == []


def test_stale_person_is_reported() -> None:
    stale = _person(
        jobTitle="Wholesale Payments & AI Leader",
        description="nearly two decades",
        alumniOf=[{"@type": "Organization", "name": "Virgin Group"}],
        hasCredential=[{"recognizedBy": {"name": "SWIFT"}}],
    )
    defects = gate.person_defects(_page(stale), PROFILE)
    assert len(defects) == 4


def test_other_nodes_and_bad_json_are_ignored() -> None:
    other = _page({"@type": "Person", "@id": "https://example.com/#x", "jobTitle": "Editor"})
    assert (
        gate.person_defects(other + '<script type="application/ld+json">{</script>', PROFILE) == []
    )


def test_about_needs_figure_timeline_and_credentials() -> None:
    assert len(gate.about_defects("<html></html>", PROFILE)) == 4


def test_speaking_flags_unrecorded_delivery() -> None:
    assert gate.speaking_defects("<b>Delivered</b>", PROFILE)
    assert gate.speaking_defects("<b>Available to book</b>", PROFILE) == []


def test_reference_stubs_are_not_judged() -> None:
    stub = {"@type": "Person", "@id": gate.PERSON_ID}
    assert gate.person_defects(_page(stub), PROFILE) == []
