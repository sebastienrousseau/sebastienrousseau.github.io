# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""postbuild_lib/sharing.py: the syndication panel's missing-metadata guard.

The panel is now off by default (``_data/article_furniture.yml``), so the
pipeline tests no longer reach this branch; it is tested directly here.
"""

from __future__ import annotations

from postbuild_lib.sharing import inject_syndication_panel

LD = '<script type="application/ld+json">{"@type":"BlogPosting"}</script>'
WRAP = '<div class="wrap"><article><p>Body</p></article></div>'


def test_blogposting_without_canonical_is_unchanged():
    page = f'<head><meta property="og:title" content="T">{LD}</head><body>{WRAP}</body>'
    assert inject_syndication_panel(page) == page


def test_blogposting_without_title_is_unchanged():
    page = (
        '<head><link rel="canonical" href="https://sebastienrousseau.com/a/">'
        f"{LD}</head><body>{WRAP}</body>"
    )
    assert inject_syndication_panel(page) == page
