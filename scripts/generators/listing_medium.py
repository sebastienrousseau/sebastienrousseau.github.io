# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""The Medium side of the English article listings.

The "Medium" select beside Category and Year, one archive per publication
at ``/articles/medium/<slug>/``, and the hub at ``/articles/medium/`` that
"All publications" opens. English only: the Medium copies are the English
text.

Split from build_listings so that file stops growing. build_listings hands
this module its renderers through ``Kit``, so the import runs one way.
"""

from __future__ import annotations

import html
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import _medium

Post = tuple[str, str, str, str, list[str], str, str]

PUBS_BASE = "/articles/medium"
HUB_NAME = "All publications"


@dataclass(frozen=True)
class Kit:
    """What an archive page needs from build_listings.

    ``card`` renders one post card, ``filter_form(years)`` the Category and
    Year bar, and ``page(name, desc, canonical, body)`` the full document
    around a ``<main>`` body. ``public`` is the build output root.
    """

    card: Callable[..., str]
    filter_form: Callable[[list[str]], str]
    page: Callable[[str, str, str, str], str]
    public: Path
    base_url: str


def _esc(s: str) -> str:
    return html.escape(s, quote=True)


def medium_filter(current: str = "") -> str:
    """The Medium <select>, in navigate mode like Year.

    Each publication opens its archive; "All publications" has no value,
    so main.js navigates to the base itself, the hub.
    """
    opts = '<option value="">All publications</option>' + "".join(
        f'<option value="{pub["slug"]}"{" selected" if pub["slug"] == current else ""}>'
        f"{_esc(pub['name'])}</option>"
        for pub in _medium.publications().values()
    )
    return (
        "<label>Medium"
        f'<select data-filter-target="publication" data-filter-mode="navigate" '
        f'data-navigate-base="{PUBS_BASE}" name="publication">{opts}</select>'
        "</label>"
    )


def with_medium_filter(page: str, current: str = "") -> str:
    """Append the Medium <select> to the page's filter bar, if it has one."""
    start = page.find('<div class="listing-filters"')
    if start < 0:
        return page
    end = page.find("</div>", start)
    return page[:end] + medium_filter(current) + page[end:]


def _count(n: int) -> str:
    return f"{n} article{'s' if n != 1 else ''}"


def _years(posts: list[Post]) -> list[str]:
    return sorted({p[1][:4] for p in posts}, reverse=True)


def _archive_body(
    kit: Kit, name: str, meta: str, current: str, shown: list[Post], all_posts: list[Post]
) -> str:
    """Hero, the full filter bar with ``current`` chosen, and the cards."""
    form = with_medium_filter(kit.filter_form(_years(all_posts or shown)), current)
    return (
        f'<div class="wrap report-wrap">'
        f'<header class="tag-landing-hero">'
        f'<p class="eyebrow"><a href="/articles/">&larr; All articles</a></p>'
        f"<h1>{_esc(name)}</h1>"
        f'<p class="tag-landing-meta">{meta}</p>'
        f"</header>"
        f"{form}"
        f'<section class="tag-landing-list" aria-label="Articles in {_esc(name)}">'
        f"{''.join(kit.card(*p) for p in shown)}"
        f"</section>"
        f'<p class="listing-empty" role="status">No articles match the current filters.</p>'
        f"</div>"
    )


def publication_body(
    kit: Kit, pub: dict[str, str], shown: list[Post], all_posts: list[Post] | None = None
) -> str:
    meta = (
        f"{_esc(pub['tagline'])} · {_count(len(shown))}"
        f' · <a href="{pub["url"]}" rel="noopener">Read it on Medium</a>'
    )
    return _archive_body(kit, pub["name"], meta, pub["slug"], shown, all_posts or [])


def hub_posts(posts: list[Post]) -> list[Post]:
    """The articles any of the three publications carries, in listing order."""
    carried = {s for slugs in _medium.slugs_by_publication().values() for s in slugs}
    return [p for p in posts if p[2] in carried]


def hub_body(kit: Kit, shown: list[Post], all_posts: list[Post]) -> str:
    """``/articles/medium/``: every publication article, linking each archive."""
    links = ", ".join(
        f'<a href="{PUBS_BASE}/{pub["slug"]}/">{_esc(pub["name"])}</a>'
        for pub in _medium.publications().values()
    )
    return _archive_body(kit, HUB_NAME, f"{links} · {_count(len(shown))}", "", shown, all_posts)


def _write(kit: Kit, name: str, desc: str, rel: str, body: str) -> None:
    out = kit.page(name, desc, f"{kit.base_url}{PUBS_BASE}/{rel}", body)
    out_path = kit.public / "articles" / "medium" / rel / "index.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(out, encoding="utf-8")


def write_archives(kit: Kit, posts: list[Post]) -> int:
    """Write each publication archive and the hub; return the page count."""
    by_slug = {p[2]: p for p in posts}
    written = 0
    for key, pub in _medium.publications().items():
        shown = [by_slug[s] for s in _medium.slugs_by_publication()[key] if s in by_slug]
        desc = (
            f"{pub['name']}, Sebastien Rousseau's Medium publication: {pub['summary']} "
            f"The {len(shown)} articles it carries, each first published here."
        )
        _write(kit, pub["name"], desc, f"{pub['slug']}/", publication_body(kit, pub, shown, posts))
        written += 1
    shown = hub_posts(posts)
    desc = (
        "Sebastien Rousseau's three Medium publications, Banking On AI, Banking On "
        f"Quantum and Banking On Cloud Native: the {len(shown)} articles they carry, "
        "each first published here."
    )
    _write(kit, HUB_NAME, desc, "", hub_body(kit, shown, posts))
    return written + 1
