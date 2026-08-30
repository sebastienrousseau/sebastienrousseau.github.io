# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Localize the /playlists/ page body.

Every other static page is either short enough to carry a curated
``static_bodies.json`` body or generic enough that the chrome patches
cover it. /playlists/ is neither: 39 playlist cards, a featured band,
five genre lanes, a seven-question FAQ and a device aside, all emitted
by ``gen_layouts.py`` from ``scripts/lib/_playlist_copy.py``. Forking
the English shell and running the usual chrome pass left the whole body
in English on all 34 localized trees.

This module closes that gap. It takes the English strings straight from
the same source module the generator renders from, and swaps each one
for the matching entry in ``_data/i18n/<code>/playlists.json`` — keyed
by Spotify playlist id, lane key and FAQ index, so re-ordering the page
never invalidates a translation.

Every swap is an exact, HTML-anchored ``str.replace``. Anything the
catalogue omits is left in English rather than half-translated, and
:func:`localize_playlists_page` reports how many anchors it failed to
find so a copy change on the English page surfaces as a build warning
instead of silent English leakage.
"""

from __future__ import annotations

import _lang_registry
import _playlist_copy as _pl

from . import _state as st

# Playlist names are proper nouns ("ETERNAL GROOVE 🪩", "Lōkahi 🌺") and
# are never translated — but they are interpolated into strings that
# are ("Cover artwork for the {title} playlist"), so the renderer needs
# them alongside the catalogue.
_CARD_TITLES: dict[str, str] = {
    pid: title
    for _key, _t, _kicker, _sub, items in _pl.PLAYLISTS_SECTIONS
    for title, _eyebrow, _desc, pid, _art in items
}

_LANE_COUNTS: dict[str, int] = {
    key: len(items) for key, _t, _kicker, _sub, items in _pl.PLAYLISTS_SECTIONS
}


class _Swapper:
    """Exact-string replacer that keeps a tally of anchors it missed."""

    def __init__(self, html: str) -> None:
        self.html = html
        self.missed: list[str] = []

    def swap(self, old: str, new: str, *, count: int = 1) -> None:
        """Replace ``old`` with ``new``. A no-op when the two are equal
        (a language that legitimately keeps the English wording) or when
        ``new`` is empty (catalogue gap — leave the English in place)."""
        if not new or old == new:
            return
        if old not in self.html:
            # Already swapped by an earlier, broader pass (the featured
            # playlist also appears as a card, so its iframe title is
            # replaced twice) — not a gap.
            if new not in self.html:
                self.missed.append(old[:80])
            return
        self.html = self.html.replace(old, new, count)


def _lane_sub(sub: str, key: str, cat_ui: dict[str, str]) -> str:
    """``"House, disco and French touch · 9 playlists"`` — the lane
    subhead, whose count noun agrees with the number of cards."""
    n = _LANE_COUNTS[key]
    noun = cat_ui["countOne"] if n == 1 else cat_ui["countOther"]
    return f"{sub} · {n} {noun}"


def localize_playlists_page(shell: str, code: str) -> tuple[str, list[str]]:
    """Return ``(html, missed_anchors)`` for the /playlists/ page in
    ``code``.

    Call this on the forked English shell *before* the generic chrome
    pass runs, while the English strings are still intact.
    """
    en = _lang_registry.playlist_reference()
    try:
        cat = _lang_registry.load_playlists(code)
    except _lang_registry.LanguageError:
        return shell, []

    ui = {**en["ui"], **cat.get("ui", {})}
    sw = _Swapper(shell)

    # --- Hero -------------------------------------------------------
    sw.swap(f"<h1>{en['ui']['h1']}</h1>", f"<h1>{ui['h1']}</h1>")
    sw.swap(
        f'<a class="pl-jump" href="#latest">{en["ui"]["jump"]}</a>',
        f'<a class="pl-jump" href="#latest">{ui["jump"]}</a>',
    )

    # --- Intro (the rendered body of _posts/playlists.md) -----------
    for src, dst in zip(en["intro"], cat.get("intro", []), strict=False):
        sw.swap(f"<p>{src}</p>", f"<p>{dst}</p>")
    sw.swap('<div lang="en">', f'<div lang="{st.LANG_BCP47}">')

    # --- Apple Music badge + platforms label ------------------------
    sw.swap(
        f'<p class="playlist-platforms-label">{en["ui"]["platformsLabel"]}</p>',
        f'<p class="playlist-platforms-label">{ui["platformsLabel"]}</p>',
    )
    apple = ui["apple"]
    sw.swap(f'aria-label="{en["ui"]["apple"]}"', f'aria-label="{apple}"', count=-1)
    sw.swap(f'alt="{en["ui"]["apple"]}"', f'alt="{apple}"', count=-1)

    # --- Featured band ----------------------------------------------
    feat, feat_en = {**en["featured"], **cat.get("featured", {})}, en["featured"]
    sw.swap(
        f'<p class="pl-hero-kicker">{feat_en["kicker"]}</p>',
        f'<p class="pl-hero-kicker">{feat["kicker"]}</p>',
    )
    sw.swap(
        f'<p class="pl-hero-desc" itemprop="description">{feat_en["desc"]}</p>',
        f'<p class="pl-hero-desc" itemprop="description">{feat["desc"]}</p>',
    )
    sw.swap(
        f'<time datetime="{_pl.FEATURED_DATETIME}">{feat_en["date"]}</time> · {feat_en["genres"]}',
        f'<time datetime="{_pl.FEATURED_DATETIME}">{feat["date"]}</time> · {feat["genres"]}',
    )

    # --- Genre nav + lane heads -------------------------------------
    sw.swap(
        f'<nav class="pl-nav" aria-label="{en["ui"]["navLabel"]}">',
        f'<nav class="pl-nav" aria-label="{ui["navLabel"]}">',
    )
    for key, lane_en in en["lanes"].items():
        lane = {**lane_en, **cat.get("lanes", {}).get(key, {})}
        sw.swap(
            f'<a class="pl-chip" href="#lane-{key}">{lane_en["title"]}</a>',
            f'<a class="pl-chip" href="#lane-{key}">{lane["title"]}</a>',
        )
        sw.swap(
            f'<h2 class="pl-lane-title" id="lane-{key}-h">{lane_en["title"]}</h2>',
            f'<h2 class="pl-lane-title" id="lane-{key}-h">{lane["title"]}</h2>',
        )
        sw.swap(
            f'<p class="pl-lane-sub">{_lane_sub(lane_en["sub"], key, en["ui"])}</p>',
            f'<p class="pl-lane-sub">{_lane_sub(lane["sub"], key, ui)}</p>',
        )

    # --- Cards ------------------------------------------------------
    for pid, card_en in en["cards"].items():
        card = {**card_en, **cat.get("cards", {}).get(pid, {})}
        title = _CARD_TITLES[pid]
        sw.swap(
            f'<span class="pl-genre">{card_en["eyebrow"]}</span>',
            f'<span class="pl-genre">{card["eyebrow"]}</span>',
        )
        sw.swap(
            f'<p class="pl-desc" itemprop="description">{card_en["desc"]}</p>',
            f'<p class="pl-desc" itemprop="description">{card["desc"]}</p>',
        )
        sw.swap(
            f'aria-label="{en["ui"]["openAria"].format(title=title)}"',
            f'aria-label="{ui["openAria"].format(title=title)}"',
        )
        sw.swap(
            f'alt="{en["ui"]["coverAlt"].format(title=title)}"',
            f'alt="{ui["coverAlt"].format(title=title)}"',
        )
        sw.swap(
            f'title="{en["ui"]["frameTitle"].format(title=title)}"',
            f'title="{ui["frameTitle"].format(title=title)}"',
            count=-1,
        )

    # The featured band reuses the newest playlist's frame title.
    feat_title = _pl.PLAYLISTS_FEATURED[0]
    sw.swap(
        f'title="{en["ui"]["frameTitle"].format(title=feat_title)}"',
        f'title="{ui["frameTitle"].format(title=feat_title)}"',
        count=-1,
    )

    # --- Call-to-action labels --------------------------------------
    sw.swap(f"</svg>{en['ui']['play']}</a>", f"</svg>{ui['play']}</a>", count=-1)
    sw.swap(
        f'rel="me noopener">{en["ui"]["follow"]}</a>',
        f'rel="me noopener">{ui["follow"]}</a>',
    )

    # --- FAQ --------------------------------------------------------
    faq_en, faq = en["faq"], {**en["faq"], **cat.get("faq", {})}
    sw.swap(
        f'<h2 id="pl-faq-h">{faq_en["heading"]}</h2>',
        f'<h2 id="pl-faq-h">{faq["heading"]}</h2>',
    )
    sw.swap(
        f'<p class="pl-faq-sub">{faq_en["sub"]}</p>',
        f'<p class="pl-faq-sub">{faq["sub"]}</p>',
    )
    for src, dst in zip(faq_en["items"], faq.get("items", []), strict=False):
        sw.swap(
            f'<summary itemprop="name">{src["q"]}</summary>',
            f'<summary itemprop="name">{dst["q"]}</summary>',
        )
        sw.swap(
            f'<p itemprop="text">{src["a"]}</p>',
            f'<p itemprop="text">{dst["a"]}</p>',
        )

    # --- "Listen on every device" aside -----------------------------
    ev_en = en["everywhere"]
    ev = {**ev_en, **cat.get("everywhere", {})}
    sw.swap(f"<h2>{ev_en['heading']}</h2>", f"<h2>{ev['heading']}</h2>")
    sw.swap(f"<p>{ev_en['body']}</p>", f"<p>{ev['body']}</p>")
    for src, dst in zip(ev_en["devices"], ev.get("devices", []), strict=False):
        sw.swap(f"<li>{src}</li>", f"<li>{dst}</li>")

    return sw.html, sw.missed
