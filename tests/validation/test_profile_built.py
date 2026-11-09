#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Gate: every built page states the author's facts as profile.yml does.

tests/unit/test_profile_consistency.py checks the sources; this checks
what ships, after ssg, the theme and every postbuild pass:

* each ``#person`` JSON-LD node has profile.yml's job title and bio, no
  ``recognizedBy`` credential, and only schools under ``alumniOf``;
* /about/ shows the profile's experience figure, the leadership timeline
  and the credentials list;
* /speaking/ marks no talk "Delivered" that the profile does not;
* English article author cards carry the profile's credentials line.

Run from repo root: ``python3 tests/validation/test_profile_built.py``.
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
import _profile

PERSON_ID = "https://sebastienrousseau.com/#person"
_LDJSON_RE = re.compile(
    r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script\s*>', re.S | re.I
)
_DATED_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-")


def _nodes(data: object) -> list[dict]:
    if isinstance(data, dict):
        return [data] + [n for v in data.values() for n in _nodes(v)]
    if isinstance(data, list):
        return [n for v in data for n in _nodes(v)]
    return []


def person_defects(page_html: str, profile: dict) -> list[str]:
    """What is wrong with the page's #person node(s)."""
    out: list[str] = []
    for block in _LDJSON_RE.findall(page_html):
        try:
            data = json.loads(block)
        except ValueError:
            continue
        for node in _nodes(data):
            if node.get("@id") != PERSON_ID or node.get("@type") != "Person":
                continue
            if node.get("jobTitle") != profile["job_title_formal"]:
                out.append(f"jobTitle {node.get('jobTitle')!r}")
            if node.get("description") != profile["bios"]["short"]:
                out.append("description is not bios.short")
            if "recognizedBy" in json.dumps(node):
                out.append("recognizedBy credential")
            kinds = {a.get("@type") for a in node.get("alumniOf", [])}
            if kinds - {"CollegeOrUniversity"}:
                out.append(f"alumniOf types {sorted(map(str, kinds))}")
    return out


def about_defects(page_html: str, profile: dict) -> list[str]:
    out = []
    if f'data-kpi="years_payments">{_profile.experience_figure()}<' not in page_html:
        out.append(f"years tile is not {_profile.experience_figure()}")
    if 'id="about-leadership"' not in page_html:
        out.append("leadership timeline missing")
    if 'id="about-credentials"' not in page_html:
        out.append("credentials list missing")
    if html.escape(profile["timeline_earlier"], quote=False) not in page_html:
        out.append("'Earlier' line missing")
    return out


def speaking_defects(page_html: str, profile: dict) -> list[str]:
    delivered = [t for t in profile.get("talks", []) if t.get("status") == "delivered"]
    if not delivered and "Delivered" in page_html:
        return ["a talk reads 'Delivered' but profile.yml records none"]
    return []


def main() -> int:
    profile = _profile.load()
    credentials = html.escape(_profile.author_card()["credentials"], quote=False)
    problems: list[str] = []
    pages = sorted(PUBLIC.rglob("index.html"))
    if not pages:
        print(f"test_profile_built: no pages under {PUBLIC}", file=sys.stderr)
        return 1
    for page in pages:
        text = page.read_text(encoding="utf-8", errors="ignore")
        rel = page.relative_to(PUBLIC).parent.as_posix()
        problems += [f"/{rel}/: {d}" for d in person_defects(text, profile)]
        if rel == "about":
            problems += [f"/about/: {d}" for d in about_defects(text, profile)]
        if rel == "speaking":
            problems += [f"/speaking/: {d}" for d in speaking_defects(text, profile)]
        is_en_article = _DATED_RE.match(rel) and "author-card" in text
        if is_en_article and credentials not in text:
            problems.append(f"/{rel}/: author card lacks the profile credentials")
    if problems:
        print(f"✗ profile facts: {len(problems)} problem(s) across {len(pages)} pages")
        for line in problems[:40]:
            print(f"  {line}")
        return 1
    print(f"ok: profile facts consistent across {len(pages)} pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
