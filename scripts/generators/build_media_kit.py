#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Generate ``/about/media-kit/`` from ``_data/profile.yml`` (plan G-6).

What an event organiser or journalist needs in one place: the short,
medium and long bios, the approved portrait, the talks available to book,
the languages, how to request comment and the views disclosure. Every fact
comes from the profile, so the kit cannot disagree with the About page.

English only, indexable, same shell and slot as ``build_trust.py``.
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path
from typing import Any

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parent / "lib"))
import _profile
from build_case_studies import _swap_into_shell

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
SHELL_SRC = PUBLIC / "articles" / "index.html"
URL = "https://sebastienrousseau.com/about/media-kit/"
TITLE = "Media kit | Sebastien Rousseau"
DESC = (
    "Bios, an approved portrait, talks available to book and how to request comment from "
    "Sebastien Rousseau, a senior payments and financial services leader."
)
PORTRAIT = "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp"
LANGUAGE_NAMES = {"en": "English", "fr": "French", "es": "Spanish", "de": "German"}
_ALT_RE = re.compile(r'[ \t]*<link\s+rel="alternate"\s+hreflang="[^"]*"\s+href="[^"]*"\s*/?>\n?')


def _e(text: str) -> str:
    return html.escape(" ".join(str(text).split()), quote=False)


def _section(heading_id: str, heading: str, inner: str) -> str:
    return (
        f'<section class="narrative-section" aria-labelledby="{heading_id}">'
        '<div class="narrative-wrap"><div>'
        f'<h2 id="{heading_id}" class="narrative-head">{_e(heading)}</h2>'
        f"{inner}</div></div></section>"
    )


def render_body(p: dict[str, Any]) -> str:
    bios = "".join(
        f"<h3>{label}</h3><p>{_e(p['bios'][key])}</p>"
        for key, label in (
            ("one_line", "One line"),
            ("short", "Short"),
            ("medium", "Medium"),
            ("long", "Long"),
        )
    )
    talks = "".join(f"<li>{_e(t['title'])}</li>" for t in p.get("talks", []))
    langs = ", ".join(
        f"{LANGUAGE_NAMES.get(lang['code'], lang['code'])} ({_e(lang['level'])})"
        for lang in p.get("languages", [])
    )
    photo = (
        f'<p><img src="{PORTRAIT}" alt="Portrait of Sebastien Rousseau" width="162" height="162" '
        'loading="lazy" decoding="async" /></p>'
        f'<p><a href="{PORTRAIT}" download>Download the portrait (WebP)</a>.</p>'
    )
    contact = (
        "<p>For comment, interviews or a talk, use the "
        '<a href="/contact/index.html?subject=press">contact form</a> and choose '
        '"Press, podcast or speaking". The typical first response is within 48 hours.</p>'
        "<p>Personal site. Views are my own and do not represent HSBC.</p>"
    )
    return (
        '<div class="media-kit-page">'
        '<section class="story-cta" aria-labelledby="mk-h1"><header class="story-head">'
        '<p class="story-eyebrow">Media kit</p>'
        f'<h1 id="mk-h1" class="story-title">{_e(p["name"])}</h1>'
        f"<p>{_e(p['job_title_short'])} · {_e(p['employer'])}</p></header></section>"
        + _section("mk-bios", "Bios", bios)
        + _section("mk-photo", "Portrait", photo)
        + _section("mk-talks", "Talks available to book", f"<ul>{talks}</ul>")
        + _section("mk-languages", "Languages", f"<p>{langs}.</p>")
        + _section("mk-contact", "Requesting comment", contact)
        + "</div>"
    )


def main() -> int:
    if not SHELL_SRC.is_file():
        print(f"build_media_kit: shell missing at {SHELL_SRC}", file=sys.stderr)
        return 1
    body = render_body(_profile.load())
    out = _ALT_RE.sub(
        "", _swap_into_shell(SHELL_SRC.read_text(encoding="utf-8"), body, TITLE, DESC, URL)
    )
    target = PUBLIC / "about" / "media-kit" / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(out, encoding="utf-8")
    print(f"build_media_kit: wrote {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
