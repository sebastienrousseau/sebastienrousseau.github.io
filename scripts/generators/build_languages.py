#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Generate ``/languages/``: every language the site is published in.

Decision D-3 (option b): an indexed page's language menu lists only the
indexed locales and ends with "More languages", which links here
(``postbuild_lib.lang_switcher_scope``). This page lists every active
locale by its native name, linking to its home page, so each translation
stays one click from anywhere without 24 links to noindexed pages on every
indexed one.

English only and indexable, with no hreflang alternates (like ``/trust/``).
Runs from ``build.sh`` after ``build_translations`` and before ``postbuild``.

Output: ``public/languages/index.html``
Input:  ``_lang_registry`` (active locales),
        ``public/articles/index.html`` (shell template)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parent / "lib"))
import _lang_registry as _lr
from build_case_studies import _swap_into_shell
from case_studies_components import _esc

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
SHELL_SRC = PUBLIC / "articles" / "index.html"
URL = "https://sebastienrousseau.com/languages/"
TITLE = "Languages | Sebastien Rousseau"
DESC = (
    f"Read sebastienrousseau.com in {len(_lr.active())} languages: articles on payments, ISO 20022, "
    "post-quantum cryptography and applied AI, translated from the English originals."
)


def _card(lang: _lr.Language) -> str:
    home = "/" if lang.code == "en" else f"/{lang.code}/"
    rtl = ' dir="rtl"' if lang.rtl else ""
    return (
        f'<li class="story-card"><span class="story-card-eyebrow">{_esc(lang.display_label)}</span>'
        f'<h2 class="story-card-title"><a href="{home}" lang="{_esc(lang.bcp47)}"{rtl}'
        f' hreflang="{_esc(lang.bcp47)}">{_esc(lang.long_label)}</a></h2></li>'
    )


def render_body() -> str:
    cards = "".join(_card(lang) for lang in _lr.active())
    return (
        '<section class="story-cta" aria-labelledby="languages-h1">'
        '<header class="story-head"><p class="story-eyebrow">Languages</p>'
        '<h1 id="languages-h1" class="story-title">Read this site in your language.</h1>'
        "<p>Every article is written in English and translated. Choose a language to "
        "open its home page; each page's language menu then links to that page in the "
        "languages listed first.</p></header>"
        f'<ul class="story-grid" role="list">{cards}</ul>'
        "</section>"
    )


def main() -> int:
    if not SHELL_SRC.is_file():
        print(f"build_languages: shell missing at {SHELL_SRC}", file=sys.stderr)
        return 1
    out = _swap_into_shell(SHELL_SRC.read_text(encoding="utf-8"), render_body(), TITLE, DESC, URL)
    # English-only page: the copied /articles alternates do not apply here.
    out = re.sub(
        r'[ \t]*<link\s+rel="alternate"\s+hreflang="[^"]*"\s+href="[^"]*"\s*/?>\n?', "", out
    )
    target = PUBLIC / "languages" / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(out, encoding="utf-8")
    print(f"build_languages: wrote {target.relative_to(ROOT)} ({len(_lr.active())} languages)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
