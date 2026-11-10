# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""scripts/lib/_expert_block.py: one expert block for hubs and services."""

from __future__ import annotations

import _expert_block as eb
import _profile


def test_block_carries_profile_facts_and_links() -> None:
    p = _profile.load()
    html = eb.render(p, "52.8M", subject="papers")
    assert p["job_title_short"].replace("&", "&amp;") in html and p["employer"] in html
    assert p["epaa"]["short"] in html and "52.8M downloads" in html
    assert "ORCID</a>" in html and "LinkedIn</a>" in html and "GitHub</a>" in html
    assert "subject=papers" in html


def test_without_figures_or_orcid() -> None:
    p = {**_profile.load(), "orcid": ""}
    html = eb.render(p)
    assert "ORCID" not in html and p["open_source"]["role"] in html
    assert len(eb.credentials(p, None)) == 3
