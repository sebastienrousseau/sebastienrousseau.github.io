# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""scripts/lib/_profile.py: the profile loader and what it derives."""

from __future__ import annotations

import copy
import datetime as dt
from typing import Any

import _profile
import pytest


def _profile_copy() -> dict[str, Any]:
    return copy.deepcopy(_profile.load())


def test_committed_profile_is_valid() -> None:
    assert _profile.load()["name"] == "Sebastien Rousseau"


def test_missing_key_is_named() -> None:
    data = _profile_copy()
    del data["job_title_formal"]
    with pytest.raises(_profile.ProfileError, match="job_title_formal"):
        _profile.validate(data)


def test_epaa_needs_wording() -> None:
    data = _profile_copy()
    data["epaa"]["wording"] = ""
    with pytest.raises(_profile.ProfileError, match=r"epaa\.wording"):
        _profile.validate(data)


def test_delivered_talk_needs_venue_and_date() -> None:
    data = _profile_copy()
    data["talks"] = [{"title": "T", "status": "delivered", "venue": "Sibos"}]
    with pytest.raises(_profile.ProfileError, match="venue and a date"):
        _profile.validate(data)
    data["talks"][0]["date"] = "2026-10"
    assert _profile.validate(data) is data


def test_career_row_with_unknown_card_fails() -> None:
    data = _profile_copy()
    data["career"][0]["card"] = "nowhere"
    with pytest.raises(_profile.ProfileError, match="nowhere"):
        _profile.validate(data)


def test_timeline_card_without_rows_fails() -> None:
    data = _profile_copy()
    data["timeline"].append({"key": "ghost", "org": "Ghost", "heading": "Nobody"})
    with pytest.raises(_profile.ProfileError, match="ghost"):
        _profile.validate(data)


def test_years_on_a_fixed_date() -> None:
    assert _profile.years(dt.date(2026, 11, 9)) == 26
    assert _profile.years() >= 26


def test_experience_sentence() -> None:
    assert (
        _profile.experience_sentence()
        == "more than 20 years in payments, banking and digital technology"
    )


def test_timeline_merges_and_orders_cards() -> None:
    cards = {c["key"]: c for c in _profile.timeline_cards()}
    assert list(cards) == ["hsbc", "reedia", "paypal", "barclays", "shazam", "akqa"]
    assert cards["hsbc"]["years"] == "2016–present"
    assert cards["akqa"]["years"] == "2005–2012"
    assert cards["akqa"]["progression"] == [
        "Technical Web Architect / Senior Web Developer",
        "Java Software Engineer",
        "Technical Manager",
    ]
    assert cards["shazam"]["years"] == "2012"
    assert cards["shazam"]["progression"] == []


def test_person_fields_carry_no_invented_credentials() -> None:
    person = _profile.person_fields()
    assert person["jobTitle"] == _profile.load()["job_title_formal"]
    assert all(a["@type"] == "CollegeOrUniversity" for a in person["alumniOf"])
    assert "recognizedBy" not in repr(person)
    assert {c["credentialCategory"] for c in person["hasCredential"]} == {"certificate"}
    assert person["memberOf"][0]["programName"] == "Quantum-Safe Cryptography Working Group"
