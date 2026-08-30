# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Language-switcher parity gate.

Every ACTIVE locale in the registry must appear in the header language
switcher as a LIVE anchor (``<a class="ap-lang-item" href="/<lang>/">``),
and never as a disabled "Coming soon" placeholder. This gate exists
because the six locales activated for issue #360 (and hu before them,
PR #367) shipped with their switcher entries still stuck as
``aria-disabled`` spans - pages existed, but users could not reach them
from the navigation.

The switcher list lives in ``_layouts/index.html`` (the master shell
gen_layouts derives every layout from), so asserting on that one file
covers the whole site.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

from _lang_registry import LANGUAGES

SHELL = ROOT / "_layouts" / "index.html"


def _switcher_slice(text: str) -> str:
    # The switcher menu is the run of ap-lang-item entries; slice from the
    # first entry to the line after the last so CSS rules do not match.
    items = list(re.finditer(r'class="ap-lang-item"[^>]*data-lang="([a-z-]+)"', text))
    assert items, "no ap-lang-item entries found in the shell"
    return text[items[0].start() - 200 : items[-1].end() + 200]


def test_every_active_locale_has_live_switcher_anchor() -> None:
    text = SHELL.read_text(encoding="utf-8")
    live = set(
        re.findall(
            r'<a class="ap-lang-item" href="/(?:([a-z-]+)/)?"[^>]*data-lang="([a-z-]+)"',
            text,
        )
    )
    live_langs = {dl for _href, dl in live}
    for lang in LANGUAGES:
        if not lang.active:
            continue
        code = "en" if lang.code == "en" else lang.code
        assert code in live_langs, (
            f"active locale '{lang.code}' has no live <a> switcher entry in "
            "_layouts/index.html - users cannot reach it from the navigation"
        )


def test_no_active_locale_is_a_disabled_placeholder() -> None:
    text = SHELL.read_text(encoding="utf-8")
    disabled = set(
        re.findall(
            r'class="ap-lang-item" data-lang="([a-z-]+)"[^>]*aria-disabled="true"',
            text,
        )
    )
    active = {lang.code for lang in LANGUAGES if lang.active}
    stuck = disabled & active
    assert not stuck, (
        f"active locale(s) still shown as disabled 'Coming soon' switcher "
        f"placeholders: {sorted(stuck)}"
    )
