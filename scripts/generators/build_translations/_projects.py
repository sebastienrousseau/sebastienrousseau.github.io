# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Localize the /projects/ page body.

/projects/ carries 1,583 visible words in its ``<main>``: a KPI rail, six
section headings, five category ledes, 29 project cards (each an excerpt
and a banner alt) and a six-question FAQ. All of it is page copy written
for that page — none of it is article data — so the body-translation gate
scored it 0.848 on the worst locale with every locale above threshold.

A curated ``static_bodies`` entry would mean hand-writing 4 KB of markup
per locale, including 29 card images and their GitHub stat rails. The
markup is generated and identical across locales; only the text differs.
So this pass keeps the generated markup and swaps the text, the same way
:mod:`._playlists` does for /playlists/.

The English reference is read from the built page rather than duplicated
in a source module, so it cannot drift. Catalogues are positional arrays
— repeating 29 long English excerpts in 34 files would add 200 KB of
duplication — and ``tests/validation/test_i18n_projects`` pins the counts
so a copy change on the English page fails loudly instead of silently
shifting every translation by one.
"""

from __future__ import annotations

import re

import _lang_registry

# Each entry: catalogue key -> (regex over the page, group-1 is the text).
# Anchored to the class the generator emits, so a match cannot stray.
_FIELDS: dict[str, re.Pattern[str]] = {
    "kpi": re.compile(r'<span class="kpi-cell-label">([^<]+)</span>'),
    "setup_kicker": re.compile(r'<p class="setup-three-kicker">([^<]+)</p>'),
    "setup_headline": re.compile(r'class="setup-three-headline">([^<]+)<span'),
    "setup_soft": re.compile(r'<span class="setup-three-headline-soft">([^<]+)</span>'),
    "area_alt": re.compile(r'<img alt="([^"]+)" src="https://cloudcdn\.pro/stocks'),
    "area_kicker": re.compile(r'<p class="area-card-kicker">([^<]+)</p>'),
    "area_headline": re.compile(r'<h3 class="area-card-headline">([\s\S]*?)</h3>'),
    "area_text": re.compile(r'<p class="area-card-text">([\s\S]*?)</p>'),
    "area_cta": re.compile(r'<p class="area-card-cta"><a href="[^"]*">([^<]+?) <span aria-hidden'),
    "cat_kicker": re.compile(r'<p class="cat-kicker">([^<]+)</p>'),
    "finale_eyebrow": re.compile(r'<p class="setup-finale-eyebrow">([^<]+)</p>'),
    "finale_lede": re.compile(r'<p class="setup-finale-lede">([^<]+)</p>'),
    "finale_cta": re.compile(
        r'<p class="setup-finale-cta"><a class="pill" href="[^"]*">([^<]+)</a>'
    ),
    "h2": re.compile(r"<h2[^>]*>([^<]+)</h2>"),
    "lede": re.compile(r'<p class="cat-lede">([^<]+)</p>'),
    "alt": re.compile(r'<img alt="([^"]+)" src="https://cloudcdn\.pro/clients'),
    "excerpt": re.compile(r'<p class="newsroom-excerpt">([^<]+)</p>'),
    "more": re.compile(r'<a href="[^"]*" title="[^"]*">([^<]+?) <span aria-hidden'),
    "faq_q": re.compile(r"<summary[^>]*>([^<]+)</summary>"),
    "faq_a": re.compile(r'<section class="qa-a"><p>([\s\S]*?)</p>'),
}


def _sub_group1(pattern: re.Pattern[str], html: str, values: list[str]) -> str:
    """Replace capture group 1 of each successive match, in order.

    Span-based rather than ``re.sub`` so a field whose text contains
    inline markup (``area_text`` carries ``<strong>`` tags) is swapped
    whole, and so the surrounding markup is never rewritten. An empty or
    missing value leaves that occurrence in English.
    """
    out: list[str] = []
    last = 0
    for i, match in enumerate(pattern.finditer(html)):
        value = values[i] if i < len(values) else None
        if not value:
            continue
        out.append(html[last : match.start(1)])
        out.append(value)
        last = match.end(1)
    out.append(html[last:])
    return "".join(out)


_GH_PUSHED_RE = re.compile(r'<span class="gh-txt">(last commit ([^<]+))</span>')

_WRAP_RE = re.compile(
    r'(<main\b[^>]*>\s*<div class="wrap[^"]*"[^>]*>)([\s\S]*?)(</div>\s*</main>)',
    re.IGNORECASE,
)


def reference(html: str) -> dict[str, list[str]]:
    """The English strings on the /projects/ page, in document order.

    ``more`` is de-duplicated: the same "Learn more" label appears on all
    29 cards, so one translation covers them.
    """
    m = _WRAP_RE.search(html)
    body = m.group(2) if m else html
    out: dict[str, list[str]] = {}
    for key, pattern in _FIELDS.items():
        found = [x.group(1) for x in pattern.finditer(body)]
        out[key] = sorted(set(found)) if key == "more" else found
    return out


def localize_projects_page(shell: str, code: str) -> tuple[str, list[str]]:
    """Return ``(html, problems)`` for the /projects/ page in ``code``.

    A locale with no catalogue, or a section whose length no longer
    matches the English page, keeps the English for that section rather
    than shifting every string by one. Both are reported.
    """
    en = reference(shell)
    try:
        cat = _lang_registry.load_projects(code)
    except _lang_registry.LanguageError:
        return shell, []

    problems: list[str] = []
    out = shell
    for key, en_values in en.items():
        translations = cat.get(key) or []
        if len(translations) != len(en_values):
            problems.append(
                f"{key}: catalogue has {len(translations)} entries, page has {len(en_values)}"
            )
            continue
        if not en_values:
            continue
        if key == "more":
            # One label reused on every card.
            values = [translations[0]] * len(_FIELDS[key].findall(out))
        else:
            values = translations
        out = _sub_group1(_FIELDS[key], out, values)

    # "last commit 2mo ago" is generated from the GitHub push date, so it
    # changes between builds. A positional list would go stale and break
    # the byte-identical-rebuild gate; a template keeps it translated and
    # stable. {age} receives the untranslated relative age ("2mo").
    template = cat.get("gh_pushed_template")
    if template and "{age}" in template:
        out = _GH_PUSHED_RE.sub(
            lambda m: m.group(0).replace(m.group(1), template.replace("{age}", m.group(2))),
            out,
        )
    return out, problems
