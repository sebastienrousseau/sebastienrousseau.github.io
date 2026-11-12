# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""scripts/generators/build_media_kit.py: the G-6 media kit."""

from __future__ import annotations

import _profile
import build_media_kit as mk


def test_kit_carries_every_bio_talk_and_the_disclosure() -> None:
    p = _profile.load()
    body = mk.render_body(p)
    for key in ("one_line", "short", "medium", "long"):
        assert " ".join(p["bios"][key].split())[:60].replace("&", "&amp;") in body
    assert body.count("<li>") == len(p["talks"])
    assert "French (native or bilingual)" in body
    assert "do not represent HSBC" in body and "subject=press" in body
    assert body.count("<h1") == 1


def test_description_fits() -> None:
    assert 120 <= len(mk.DESC) <= 160
