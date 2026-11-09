#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Render the About page's leadership and credentials from profile.yml.

``_posts/about.md`` carries the marker ``<!-- profile:about -->``. This
step replaces it, in the build copy only, with two sections: the career
timeline (one card per ``timeline`` entry, with its leadership statement
and promotion path) and the credentials list (education, languages,
memberships, certifications, awards). Nothing about the career is typed
into the page, so it cannot disagree with the profile.

``--dir`` is required, with no default (ADR-0003): build.sh passes the
build copy ``_posts_build``; the committed source keeps the marker.
"""

from __future__ import annotations

import argparse
import html
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import _profile

MARKER = "<!-- profile:about -->"
_LANGUAGE_NAMES = {"en": "English", "fr": "French", "es": "Spanish", "de": "German"}


def _e(text: str) -> str:
    return html.escape(text, quote=False)


def _card(card: dict[str, Any], statements: dict[str, str]) -> str:
    body = statements.get(card["key"], "")
    progression = ""
    if card["progression"]:
        path = " → ".join(_e(t) for t in card["progression"])
        progression = f'<p class="story-card-body">Earlier at {_e(card["org"])}: {path}.</p>'
    return (
        '<article class="story-card">'
        f'<span class="story-card-eyebrow">{_e(card["org"])} · {card["years"]}</span>'
        f'<h3 class="story-card-title">{_e(card["heading"])}</h3>'
        f'<p class="story-card-body">{_e(body)}</p>'
        f"{progression}"
        "</article>"
    )


def render_timeline(p: dict[str, Any]) -> str:
    """The Leadership section: positioning, one card per role, the
    'Earlier' line."""
    statements = {s["card"]: s["statement"] for s in p.get("leadership", [])}
    cards = "".join(_card(c, statements) for c in _profile.timeline_cards(p))
    return (
        '<section class="story-cta" aria-labelledby="about-leadership" data-reveal>'
        '<header class="story-head">'
        '<p class="story-eyebrow">Leadership</p>'
        f'<h2 id="about-leadership" class="story-title">{_e(p["experience_phrase"].capitalize())} '
        "leading payments, mobile and digital products.</h2>"
        f"<p>{_e(p['positioning'])}</p>"
        "</header>"
        f'<div class="story-grid">{cards}</div>'
        f'<p class="career-earlier">{_e(p["timeline_earlier"])}</p>'
        "</section>"
    )


def _row(term: str, values: list[str]) -> str:
    if not values:
        return ""
    items = "<br />".join(_e(v) for v in values)
    return f"<dt>{_e(term)}</dt><dd>{items}</dd>"


def render_credentials(p: dict[str, Any]) -> str:
    """Education, languages, memberships, certifications and awards."""
    education = [f"{e['org']}: {e['award']} ({e['years']})" for e in p["education"]]
    languages = [
        f"{_LANGUAGE_NAMES.get(lang['code'], lang['code'])} ({lang['level']})"
        for lang in p.get("languages", [])
    ]
    rows = "".join(
        [
            _row("Education", education),
            _row("Languages", languages),
            _row("Memberships", list(p.get("memberships", []))),
            _row("Certifications", list(p.get("certifications", []))),
            _row("Awards", list(p.get("awards", []))),
        ]
    )
    return (
        '<section class="narrative-section alt" aria-labelledby="about-credentials" data-reveal>'
        '<div class="narrative-wrap"><div>'
        '<p class="narrative-eyebrow">Credentials</p>'
        '<h2 id="about-credentials" class="narrative-head">Education, memberships and recognition.</h2>'
        f'<dl class="author-ids">{rows}</dl>'
        "</div></div></section>"
    )


def render(p: dict[str, Any] | None = None) -> str:
    profile = p or _profile.load()
    return render_timeline(profile) + "\n\n" + render_credentials(profile)


def apply(path: Path) -> bool:
    """Replace the marker in ``path``. Returns True when it was there."""
    text = path.read_text(encoding="utf-8")
    if MARKER not in text:
        return False
    path.write_text(text.replace(MARKER, render()), encoding="utf-8")
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dir", required=True, type=Path, help="posts directory (build copy)")
    args = parser.parse_args(argv)
    target = args.dir / "about.md"
    if not apply(target):
        print(f"build_about_profile: {MARKER} not found in {target}", file=sys.stderr)
        return 1
    print(f"build_about_profile: rendered leadership and credentials into {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
