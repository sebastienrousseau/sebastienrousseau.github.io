# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""The author card at the foot of every dated article, in one place.

``post_enrich.py`` writes the English card and the translation builder
writes each locale's; both render through :func:`render`, so the markup
cannot drift between them. The English sentences come from profile.yml
(:func:`_profile.author_card`); each locale's from its ``author.json``.
"""

from __future__ import annotations

import html

import _profile

PORTRAIT = "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp"
LINKEDIN = "https://www.linkedin.com/in/sebastienrousseau/"
GITHUB = "https://github.com/sebastienrousseau"


def render(
    *,
    bio: str,
    credentials: str,
    about_href: str,
    aria: str = "About the author",
    portrait_alt: str = "Portrait of Sebastien Rousseau",
    full_profile: str = "Full profile",
) -> str:
    """One ``<aside class="author-card">``. ``bio`` and ``credentials`` are
    HTML text (already escaped, as author.json stores them)."""
    return (
        f'<aside class="author-card" aria-label="{aria}">'
        f'<img alt="{portrait_alt}" src="{PORTRAIT}" '
        'width="64" height="64" loading="lazy" decoding="async" />'
        '<span class="author-card-body">'
        '<strong class="author-card-name">'
        f'<a href="{about_href}">Sebastien Rousseau</a></strong>'
        f'<span class="author-card-bio">{bio}</span>'
        '<span class="author-credentials">'
        f"{credentials} "
        f'<a href="{about_href}">{full_profile}</a> &middot; '
        f'<a href="{LINKEDIN}" rel="external noopener">LinkedIn</a> &middot; '
        f'<a href="{GITHUB}" rel="external noopener">GitHub</a>'
        "</span></span></aside>"
    )


def english() -> str:
    """The English card, from profile.yml."""
    card = _profile.author_card()
    return render(
        bio=html.escape(card["bio"], quote=False),
        credentials=html.escape(card["credentials"], quote=False),
        about_href="/about/index.html",
    )
