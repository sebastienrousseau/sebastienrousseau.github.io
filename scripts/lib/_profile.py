# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Profile facts: the one place a page may take a title, year, role or
credential from.

``_data/profile.yml`` holds them. Layouts, posts and generators once
restated them by hand and disagreed: three experience figures, two job
titles, five wordings of the EPAA role, and credentials "recognised by"
HSBC, SWIFT and NIST that no such body issued. Everything that prints a
profile fact now asks this module, and ``tests/unit/test_profile_consistency.py``
fails when a source states one another way.
"""

from __future__ import annotations

import datetime as _dt
import re
from functools import cache
from pathlib import Path
from typing import Any

import yaml

PATH = Path(__file__).resolve().parents[2] / "_data" / "profile.yml"
REQUIRED = (
    "name",
    "career_start_year",
    "experience_phrase",
    "experience_scope",
    "job_title_formal",
    "job_title_short",
    "employer",
    "descriptor",
    "epaa",
    "career",
    "education",
    "timeline",
    "bios",
    "writes_on",
    "role_line",
)
_EARLIER = "earlier"


class ProfileError(ValueError):
    """Raised when profile.yml is incomplete or contradicts itself."""


def _check_talks(talks: list[dict[str, Any]]) -> None:
    for talk in talks:
        if talk.get("status") == "delivered" and not (talk.get("venue") and talk.get("date")):
            raise ProfileError(f"talk {talk['title']!r}: delivered needs a venue and a date")


def _check_timeline(data: dict[str, Any]) -> None:
    keys = [card["key"] for card in data["timeline"]]
    used = {row.get("card") for row in data["career"]}
    unknown = sorted(str(k) for k in used - set(keys) - {_EARLIER, None})
    if unknown:
        raise ProfileError(f"career rows name cards the timeline does not list: {unknown}")
    empty = [k for k in keys if k not in used]
    if empty:
        raise ProfileError(f"timeline cards with no career rows: {empty}")


def validate(data: dict[str, Any]) -> dict[str, Any]:
    """Return ``data`` unchanged, or raise :class:`ProfileError`."""
    missing = [k for k in REQUIRED if not data.get(k)]
    if missing:
        raise ProfileError(f"_data/profile.yml: missing {', '.join(missing)}")
    if not data["epaa"].get("wording"):
        raise ProfileError("_data/profile.yml: epaa.wording is required")
    _check_talks(data.get("talks", []))
    _check_timeline(data)
    return data


@cache
def load() -> dict[str, Any]:
    """The validated profile, read once per process."""
    data = yaml.safe_load(PATH.read_text(encoding="utf-8"))
    return validate(data)


def years(today: _dt.date | None = None) -> int:
    """Whole years since the career start (26 in 2026). Internal checks
    only: pages print ``experience_phrase``, so copy does not change every
    January."""
    today = today or _dt.date.today()
    return today.year - int(load()["career_start_year"])


def experience_sentence() -> str:
    """'more than 20 years in payments, banking and digital technology'."""
    p = load()
    return f"{p['experience_phrase']} {p['experience_scope']}"


def experience_figure() -> str:
    """The figure a stat tile prints: "20+" for "more than 20 years"."""
    m = re.search(r"\d+", load()["experience_phrase"])
    if not m:
        raise ProfileError("experience_phrase must contain a number of years")
    return f"{m.group(0)}+"


def author_card() -> dict[str, str]:
    """The English author card's two sentences (plain text, unescaped).
    ``_data/i18n/<lang>/author.json`` carries their translations."""
    p = load()
    experience = experience_sentence()
    return {
        "bio": f"{p['descriptor']} writing on {p['writes_on']}.",
        "credentials": (
            f"{experience[0].upper()}{experience[1:]}. {p['role_line']} · {p['epaa']['short']}."
        ),
    }


def _year(stamp: str) -> int:
    return int(str(stamp)[:4])


def _span(rows: list[dict[str, Any]]) -> str:
    start = min(_year(r["from"]) for r in rows)
    if any(r.get("to") is None for r in rows):
        return f"{start}–present"
    end = max(_year(r["to"]) for r in rows)
    return str(start) if start == end else f"{start}–{end}"


def timeline_cards(data: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """The About timeline: one card per ``timeline`` entry, newest first.

    Each card carries its year span across all its career rows and, when
    it has more than one row, the earlier titles oldest first, so a
    promotion path (AKQA developer to head of mobile) reads as one line.
    """
    p = data or load()
    cards = []
    for card in p["timeline"]:
        rows = [r for r in p["career"] if r.get("card") == card["key"]]
        # rows are newest first: the first is the role the heading names.
        earlier = [r["title"] for r in reversed(rows[1:])]
        cards.append({**card, "years": _span(rows), "progression": earlier})
    return cards


def _member_of(p: dict[str, Any]) -> list[dict[str, Any]]:
    epaa = p["epaa"]
    return [
        {
            "@type": "ProgramMembership",
            "programName": epaa["working_group"],
            "hostingOrganization": {
                "@type": "Organization",
                "name": epaa["organisation"],
                "url": epaa["url"],
            },
        },
        {
            "@type": "OrganizationRole",
            "roleName": "Fellow",
            "memberOf": {
                "@type": "Organization",
                "name": "Institution of Analysts and Programmers",
            },
        },
    ]


def person_fields(base: str = "https://sebastienrousseau.com") -> dict[str, Any]:
    """The Person JSON-LD properties profile.yml owns.

    Postbuild merges these over the layout's Person node, so ``knowsAbout``,
    ``sameAs``, ``image`` and ``subjectOf`` stay where the theme keeps them.
    ``alumniOf`` lists schools only: schema.org has no clean property for
    past employers, so they appear in the visible timeline instead.
    """
    p = load()
    return {
        "jobTitle": p["job_title_formal"],
        "description": p["bios"]["short"],
        "worksFor": {
            "@type": "Organization",
            "@id": "https://www.hsbc.com/#organization",
            "name": p["employer"],
            "department": {"@type": "Organization", "name": p["employer_unit"]},
            "url": "https://www.hsbc.com/",
        },
        "address": {"@type": "PostalAddress", "addressLocality": "London", "addressCountry": "GB"},
        "email": f"mailto:{p['email_public']}",
        "alumniOf": [{"@type": "CollegeOrUniversity", "name": e["org"]} for e in p["education"]],
        "memberOf": _member_of(p),
        "hasCredential": [
            {
                "@type": "EducationalOccupationalCredential",
                "name": c,
                "credentialCategory": "certificate",
            }
            for c in p.get("certifications", [])
        ],
        "award": list(p.get("awards", [])),
        "knowsLanguage": [
            {"@type": "Language", "alternateName": lang["code"]} for lang in p.get("languages", [])
        ],
        "url": f"{base}/",
    }
