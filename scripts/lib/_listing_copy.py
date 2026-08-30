# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""English source copy for generator-emitted listing bodies.

``build_listings`` and its siblings fork the English shell and run
``_translate_chrome_for``, which — as its own docstring says — translates
nav, footer, search and aria, and leaves "body content (which we emit
ourselves)" alone. Nothing ever translated that body, so every locale's
paged article listing shipped ``FEED``, ``Page 1 of 5``, ``24 visible``,
``Category``, ``All categories``, ``Year``, ``All years`` and the six
pillar names in English.

The catalogue is small and structural — labels and one count template —
rather than prose, so it lives here as a single source of truth shared
by the generator and by ``_data/i18n/<code>/listings.json``.

``{page}``/``{total}``/``{count}`` are placeholders the renderer fills;
a translation must keep the ones its string carries.
"""

from __future__ import annotations

# Section eyebrow above the listing title.
EYEBROW = "FEED"

# "Page 2 of 5" — both placeholders required.
PAGE_LABEL = "Page {page} of {total}"

# Follows the page label: "… · 24 visible".
VISIBLE = "visible"

# The two filter selects and their "no filter" options.
CATEGORY_LABEL = "Category"
YEAR_LABEL = "Year"
ALL_CATEGORIES = "All categories"
ALL_YEARS = "All years"

# Landmark labels — announced by screen readers, never shown.
FILTER_ARIA = "Filter articles"
LIST_ARIA = "Article cards"
PAGINATION_ARIA = "Pagination"

# Shown when the category filter matches nothing on the current page.
EMPTY_STATE = "No articles match the current filters."

# Pagination controls. The arrows are decorative and stay put; only the
# words are translated.
PREVIOUS = "Previous"
NEXT = "Next"

# The six editorial pillars, in the order the category select lists them.
# Keys match build_listings.PILLAR_ORDER.
PILLARS: dict[str, str] = {
    "ai": "Applied AI",
    "payments": "Payments & money",
    "infra": "Infra & cryptography",
    "policy": "Policy & resilience",
    "open-source": "Open source",
    "leadership": "Banking leadership",
}

# Flat UI keys, in the order a translator meets them on the page.
UI_KEYS: tuple[str, ...] = (
    "eyebrow",
    "pageLabel",
    "visible",
    "categoryLabel",
    "yearLabel",
    "allCategories",
    "allYears",
    "filterAria",
    "listAria",
    "paginationAria",
    "emptyState",
    "previous",
    "next",
)

UI: dict[str, str] = {
    "eyebrow": EYEBROW,
    "pageLabel": PAGE_LABEL,
    "visible": VISIBLE,
    "categoryLabel": CATEGORY_LABEL,
    "yearLabel": YEAR_LABEL,
    "allCategories": ALL_CATEGORIES,
    "allYears": ALL_YEARS,
    "filterAria": FILTER_ARIA,
    "listAria": LIST_ARIA,
    "paginationAria": PAGINATION_ARIA,
    "emptyState": EMPTY_STATE,
    "previous": PREVIOUS,
    "next": NEXT,
}

# Placeholders each UI string must preserve when translated.
REQUIRED_PLACEHOLDERS: dict[str, tuple[str, ...]] = {
    "pageLabel": ("{page}", "{total}"),
}
