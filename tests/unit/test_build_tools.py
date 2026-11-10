# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""scripts/generators/build_tools.py: the /tools/ page (G-4)."""

from __future__ import annotations

import json
import re

import build_tools as bt


def test_three_tools_each_with_a_form_and_live_output() -> None:
    body = bt.render_body()
    for tid, _, _ in bt.TOOLS:
        assert f'<form id="{tid}"' in body and f'<output aria-live="polite" for="{tid}">' in body
    assert "Nothing you paste is sent anywhere" in body
    assert body.count("<h1") == 1 and '/_csp/tools/tools.js"' in body


def test_software_application_jsonld_is_free_and_web() -> None:
    ld = json.loads(re.sub(r"^<script[^>]*>|</script>$", "", bt.jsonld()))
    apps = ld["@graph"]
    assert len(apps) == 3
    assert all(a["operatingSystem"] == "Web" and a["offers"]["price"] == 0 for a in apps)


def test_description_fits() -> None:
    assert 120 <= len(bt.DESC) <= 160, len(bt.DESC)
