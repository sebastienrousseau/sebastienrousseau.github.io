# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""The expert block (plan G-6): who stands behind a hub or service page.

Portrait, name, short title and employer, one sentence and three
credentials from ``profile.yml``, the open-source figure from the metrics,
the ORCID, LinkedIn and GitHub links, and "Get in touch". One function, so
every hub and service page shows the same facts in the same words.
"""

from __future__ import annotations

import html
from typing import Any

PORTRAIT = "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp"
GITHUB = "https://github.com/sebastienrousseau"


def _e(text: object) -> str:
    return html.escape(" ".join(str(text).split()), quote=False)


def credentials(profile: dict[str, Any], downloads: str | None) -> list[str]:
    """Three credentials: the EPAA role, FIAP, and the open-source figure."""
    out = [profile["epaa"]["short"], "Fellow of the Institution of Analysts and Programmers (FIAP)"]
    if downloads:
        out.append(
            f"Maintainer of open-source payments and cryptography libraries ({downloads} downloads)"
        )
    else:
        out.append(profile["open_source"]["role"])
    return out


def render(profile: dict[str, Any], downloads: str | None = None, subject: str = "general") -> str:
    """The block's HTML: an ``<aside>`` with the portrait, bio and links."""
    creds = "".join(f"<li>{_e(c)}</li>" for c in credentials(profile, downloads))
    orcid = profile.get("orcid", "")
    links = [f'<a href="{_e(orcid)}" rel="external me noopener">ORCID</a>'] if orcid else []
    links += [
        f'<a href="{_e(profile["linkedin"])}" rel="external me noopener">LinkedIn</a>',
        f'<a href="{GITHUB}" rel="external me noopener">GitHub</a>',
    ]
    return (
        '<aside class="expert-block" aria-label="About the author">'
        f'<img src="{PORTRAIT}" alt="Portrait of {_e(profile["name"])}" width="96" height="96" '
        'loading="lazy" decoding="async" />'
        '<div class="expert-block-body">'
        f'<p class="expert-block-name"><a href="/about/index.html">{_e(profile["name"])}</a></p>'
        f'<p class="expert-block-role">{_e(profile["job_title_short"])} · {_e(profile["employer"])}</p>'
        f"<p>{_e(profile['bios']['one_line'])}</p>"
        f'<ul class="expert-block-creds">{creds}</ul>'
        f'<p class="expert-block-links">{" · ".join(links)}</p>'
        f'<p><a class="pill" href="/contact/index.html?subject={_e(subject)}">Get in touch</a></p>'
        "</div></aside>"
    )
