# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Unit coverage for gen_projects render helpers — Phase 1.3.

gen_projects.py builds the /projects newsroom page. It was untested. Cover the
logo heuristic and the featured/card block renderers, which decide the media
CSS class and assemble the card markup.
"""

from __future__ import annotations

import gen_projects as gp

_ITEM = (
    "Eyebrow Tag",  # eyebrow
    "PainLib",  # title
    "brand-logo.webp",  # image
    "PainLib logo",  # alt
    "A payments library.",  # summary
    "/projects/painlib/",  # href
)


# --- _is_logo --------------------------------------------------------------


def test_is_logo_webp_with_logo_or_github() -> None:
    assert gp._is_logo("brand-logo.webp") is True
    assert gp._is_logo("github-avatar.webp") is True


def test_is_logo_plain_webp_is_photo() -> None:
    assert gp._is_logo("hero-photo.webp") is False


def test_is_logo_non_webp_is_true() -> None:
    assert gp._is_logo("banner.png") is True
    assert gp._is_logo("shot.jpg") is True


# --- featured_block --------------------------------------------------------


def test_featured_block_logo_media_class_and_fields() -> None:
    out = gp.featured_block(_ITEM)
    assert 'class="newsroom-featured-media logo"' in out  # logo image
    assert "PainLib" in out and "/projects/painlib/" in out
    assert "A payments library." in out
    assert 'alt="PainLib logo"' in out
    assert "Eyebrow Tag" in out  # eyebrow shown on featured


def test_featured_block_photo_has_no_logo_class() -> None:
    item = (*_ITEM[:2], "hero-photo.webp", *_ITEM[3:])
    out = gp.featured_block(item)
    assert 'class="newsroom-featured-media"' in out
    assert "newsroom-featured-media logo" not in out


# --- card_block ------------------------------------------------------------


def test_card_block_omits_eyebrow_and_renders_fields() -> None:
    out = gp.card_block(_ITEM)
    assert 'class="newsroom-card-media logo"' in out
    assert "PainLib" in out and "A payments library." in out
    assert "Eyebrow Tag" not in out  # eyebrow intentionally unused on cards
