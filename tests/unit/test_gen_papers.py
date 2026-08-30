# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Unit coverage for gen_papers render helpers — Phase 1.3.

gen_papers.py builds the /papers newsroom page. It was untested. Cover the
research-note card renderer and the two featured book-card blocks (which pull
from the FEATURED / PREVIOUS_PUBLICATION module dicts).
"""

from __future__ import annotations

import gen_papers as gp


def test_card_block_renders_all_fields() -> None:
    out = gp.card_block(
        "2026-06-01",
        "June 1, 2026",
        "RESEARCH NOTE",
        "Quantum Settlement",
        "/img/q.webp",
        "Quantum settlement diagram",
        "A short excerpt.",
        "/papers/quantum-settlement/",
    )
    assert 'class="newsroom-card"' in out
    assert "Quantum Settlement" in out
    assert "/papers/quantum-settlement/" in out
    assert 'src="/img/q.webp"' in out
    assert 'alt="Quantum settlement diagram"' in out
    assert "A short excerpt." in out
    assert 'datetime="2026-06-01"' in out and "June 1, 2026" in out
    assert "RESEARCH NOTE" in out


def test_epaa_card_block_uses_featured_dict() -> None:
    out = gp.epaa_card_block()
    f = gp.FEATURED
    assert f["title"] in out
    assert f["read_url"] in out
    assert f["publisher_url"] in out
    assert "About EPAA" in out


def test_whisper_card_block_uses_previous_publication_dict() -> None:
    out = gp.whisper_card_block()
    p = gp.PREVIOUS_PUBLICATION
    assert p["title"] in out
    assert p["href"] in out
    assert p["price"] in out
    assert "Read the article" in out
