"""Per-language mutable state shared by every renderer module.

``main()`` drives one language at a time: ``bind_lang(code)`` rebinds
every module-level global below to the target language's data before
the render functions run. Renderer modules read the *current* values
through attribute access (``from . import _state as st`` then
``st.LANG_CODE``) so a rebind is visible everywhere instantly.

Default values target FR so module-load stays backward-compatible while
the loop drives each active non-EN language end-to-end.
"""

from __future__ import annotations

import functools
import re
from pathlib import Path

import _lang_registry

PUBLIC = Path("public")
BASE = "https://sebastienrousseau.com"

_DATED_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-")

# Lang-parametric globals — rebound per-language by ``bind_lang()``
# before the render functions are called.
LANG_CODE = "fr"
LANG_BCP47 = "fr-FR"
LANG_LOCALE = "fr_FR"
SRC = Path(f"_posts/{LANG_CODE}")
OUT = PUBLIC / LANG_CODE

# Slug maps used by the render functions and by helpers throughout.
# EN_TO_FR / FR_TO_EN / fr_slug names preserved for diff minimality;
# rebound per-language by ``bind_lang()``.
_articles_map = _lang_registry.load_slugs(LANG_CODE)["articles"]
EN_TO_FR: dict[str, str] = dict(_articles_map)
FR_TO_EN: dict[str, str] = {v: k for k, v in _articles_map.items()}


def fr_slug(en_slug: str) -> str:
    return EN_TO_FR.get(en_slug, en_slug)


# French UI strings — body-text labels for inline article chrome,
# sourced from _data/i18n/<lang>/labels.json. Kept as a frozen alias so
# any external code that imported I18N_FR keeps working through Phase
# 6a; Phase 6b will move the consumers to read by lang_code directly.
I18N_FR: dict[str, str] = _lang_registry.load_labels("fr")


@functools.cache
def _is_rtl(code: str) -> bool:
    """Return True if ``code`` is an RTL language (per
    ``_lang_registry.LANGUAGES``). Cached — the registry is immutable
    for the lifetime of a build, and this is called for every page."""
    return any(lg.code == code and lg.rtl for lg in _lang_registry.LANGUAGES)


def _is_current_rtl() -> bool:
    """Return True if the current ``LANG_CODE`` is an RTL language."""
    return _is_rtl(LANG_CODE)


# Comprehensive chrome-string translations. Applied to every French page
# after the rendered English shell is forked. Each entry is a (regex,
# replacement) pair — anchored to its HTML context so it can't match
# the same English word inside article body content.
CHROME_PATCHES: list[tuple[str, str]] = [
    *_lang_registry.build_chrome_patches("fr"),
    *_lang_registry.load_chrome_patches_inline("fr"),
]

_CHROME_PATCHES_COMPILED: list[tuple[re.Pattern[str], str]] = [
    (re.compile(p), r) for p, r in CHROME_PATCHES
]

# English month names → per-language equivalents. ``_EN_MONTH_TO_FR`` is
# rebound by ``bind_lang()`` so date-localisation uses the current
# language's names.
_LANG_MONTHS: dict[str, dict[str, str]] = {
    "fr": {
        "January": "janvier",
        "February": "février",
        "March": "mars",
        "April": "avril",
        "May": "mai",
        "June": "juin",
        "July": "juillet",
        "August": "août",
        "September": "septembre",
        "October": "octobre",
        "November": "novembre",
        "December": "décembre",
        "Jan": "janv.",
        "Feb": "févr.",
        "Mar": "mars",
        "Apr": "avr.",
        "Jun": "juin",
        "Jul": "juill.",
        "Aug": "août",
        "Sep": "sept.",
        "Sept": "sept.",
        "Oct": "oct.",
        "Nov": "nov.",
        "Dec": "déc.",
    },
    "de": {
        "January": "Januar",
        "February": "Februar",
        "March": "März",
        "April": "April",
        "May": "Mai",
        "June": "Juni",
        "July": "Juli",
        "August": "August",
        "September": "September",
        "October": "Oktober",
        "November": "November",
        "December": "Dezember",
        "Jan": "Jan.",
        "Feb": "Feb.",
        "Mar": "März",
        "Apr": "Apr.",
        "Jun": "Juni",
        "Jul": "Juli",
        "Aug": "Aug.",
        "Sep": "Sept.",
        "Sept": "Sept.",
        "Oct": "Okt.",
        "Nov": "Nov.",
        "Dec": "Dez.",
    },
}
_EN_MONTH_TO_FR: dict[str, str] = dict(_LANG_MONTHS["fr"])  # rebound per-lang

# Canonical EN → FR slug map for the static pages mirrored under /fr/.
# Visible URLs are localised (e.g. /fr/privacy/ → /fr/confidentialite/).
STATIC_SLUG_FR: dict[str, str] = _lang_registry.load_slugs("fr")["static"]
STATIC_SLUG_EN: dict[str, str] = {v: k for k, v in STATIC_SLUG_FR.items()}

# Takeaway-aside labels — sourced from
# _data/i18n/<lang>/takeaway_labels.json. Kept as a frozen alias so
# legacy consumers keep working through Phase 6b.
TAKEAWAY_LABELS_EN_TO_FR: dict[str, str] = _lang_registry.load_takeaway_labels("fr")

# Per-section EN→FR substitutions for the home page body.
HOME_FR_PATCHES: list[tuple[str, str]] = list(_lang_registry.load_home_patches("fr"))

_HOME_FR_COMPILED: list[tuple[re.Pattern[str], str]] = [
    (re.compile(p), r) for p, r in HOME_FR_PATCHES
]

# Static pages we mirror under /fr/: EN slug → FR title + meta overrides.
STATIC_PAGES_FR: dict[str, dict[str, str]] = _lang_registry.load_static_pages("fr")

# Per-page French <main> body replacements.
STATIC_BODIES_FR: dict[str, str] = dict(_lang_registry.load_static_bodies("fr"))

# Body-string patches applied to every FR static page.
STATIC_BODY_PATCHES: list[tuple[str, str]] = list(_lang_registry.load_static_patches("fr"))

_STATIC_BODY_COMPILED: list[tuple[re.Pattern[str], str]] = [
    (re.compile(p), r) for p, r in STATIC_BODY_PATCHES
]

# Per-topic French title + lede. Mirrors scripts/build_topics.py:TOPICS.
TOPIC_FR_LABELS: dict[str, dict[str, str]] = _lang_registry.load_topics("fr")

# ---------------------------------------------------------------------------
# Per-language lazy caches (filled by _maps.py, cleared by bind_lang()).
# ---------------------------------------------------------------------------

_FR_TITLE_MAP: dict[str, str] = {}
_FR_DESCRIPTION_MAP: dict[str, str] = {}
_FR_EXCERPT_MAP: dict[str, str] = {}
_FR_EYEBROW_MAP: dict[str, str] = {}
_EN_DESC_TO_FR_RE_CACHE: re.Pattern[str] | None = None
_EN_DESC_TO_FR_MAP_CACHE: dict[str, str] | None = None
_EN_TITLES_TO_FR_RE_CACHE: re.Pattern[str] | None = None
_EN_TITLE_TO_FR_MAP_CACHE: dict[str, str] | None = None


def bind_lang(code: str) -> None:
    """Rebind every per-language module-level global to ``code``'s
    values. Called by ``main()`` before each render pass.

    Globals reassigned: LANG_CODE / LANG_BCP47 / LANG_LOCALE / SRC / OUT /
    EN_TO_FR / FR_TO_EN / I18N_FR / TAKEAWAY_LABELS_EN_TO_FR /
    STATIC_SLUG_FR / STATIC_PAGES_FR / TOPIC_FR_LABELS / HOME_FR_PATCHES /
    STATIC_BODIES_FR / STATIC_BODY_PATCHES / CHROME_PATCHES /
    _CHROME_PATCHES_COMPILED / _HOME_FR_COMPILED. (Names carry the
    legacy ``_FR`` suffix for diff minimality; semantically they hold
    the current ``code``'s data.)
    """
    global LANG_CODE, LANG_BCP47, LANG_LOCALE, SRC, OUT
    global EN_TO_FR, FR_TO_EN
    global I18N_FR, TAKEAWAY_LABELS_EN_TO_FR
    global STATIC_SLUG_FR, STATIC_PAGES_FR, TOPIC_FR_LABELS
    global HOME_FR_PATCHES, STATIC_BODIES_FR, STATIC_BODY_PATCHES
    global CHROME_PATCHES, _CHROME_PATCHES_COMPILED, _HOME_FR_COMPILED, _STATIC_BODY_COMPILED
    lang = next(lg for lg in _lang_registry.LANGUAGES if lg.code == code)
    LANG_CODE = code
    LANG_BCP47 = lang.bcp47
    LANG_LOCALE = lang.og_locale
    SRC = Path(f"_posts/{code}")
    OUT = PUBLIC / code
    slugs = _lang_registry.load_slugs(code)
    articles = slugs.get("articles", {})
    EN_TO_FR = dict(articles)
    FR_TO_EN = {v: k for k, v in articles.items()}
    I18N_FR = _lang_registry.load_labels(code)
    TAKEAWAY_LABELS_EN_TO_FR = _lang_registry.load_takeaway_labels(code)
    STATIC_SLUG_FR = slugs.get("static", {})
    STATIC_PAGES_FR = _lang_registry.load_static_pages(code)
    TOPIC_FR_LABELS = _lang_registry.load_topics(code)
    HOME_FR_PATCHES = list(_lang_registry.load_home_patches(code))
    STATIC_BODIES_FR = dict(_lang_registry.load_static_bodies(code))
    STATIC_BODY_PATCHES = list(_lang_registry.load_static_patches(code))
    CHROME_PATCHES = [
        *_lang_registry.build_chrome_patches(code),
        *_lang_registry.load_chrome_patches_inline(code),
    ]
    _CHROME_PATCHES_COMPILED = [(re.compile(p), r) for p, r in CHROME_PATCHES]
    _HOME_FR_COMPILED = [(re.compile(p), r) for p, r in HOME_FR_PATCHES]
    _STATIC_BODY_COMPILED = [(re.compile(p), r) for p, r in STATIC_BODY_PATCHES]
    # Clear every per-language lazy cache so the second pass doesn't
    # inherit the first language's title / description / excerpt /
    # eyebrow / regex tables.
    global _EN_DESC_TO_FR_RE_CACHE, _EN_DESC_TO_FR_MAP_CACHE
    global _EN_TITLES_TO_FR_RE_CACHE, _EN_TITLE_TO_FR_MAP_CACHE
    _FR_TITLE_MAP.clear()
    _FR_DESCRIPTION_MAP.clear()
    _FR_EXCERPT_MAP.clear()
    _FR_EYEBROW_MAP.clear()
    _EN_DESC_TO_FR_RE_CACHE = None
    _EN_DESC_TO_FR_MAP_CACHE = None
    _EN_TITLES_TO_FR_RE_CACHE = None
    _EN_TITLE_TO_FR_MAP_CACHE = None
    # Swap month-name map to the current language so localize_en_dates
    # emits the right month form (FR "novembre", DE "November", …).
    # Languages without a month glossary get an EMPTY map — that makes
    # localize_en_dates() a no-op for them, keeping the English month
    # names. Falling back to the FR table here is what stamped French
    # dates ("4 juin 2026") onto every other locale's topic pages.
    global _EN_MONTH_TO_FR
    _EN_MONTH_TO_FR = dict(_LANG_MONTHS.get(code, {}))


def current_month_map() -> dict[str, str]:
    """The active language's EN-month-name -> localized-name map, as set
    by the most recent :func:`bind_lang`. Cross-module readers (``_chrome``)
    call this instead of importing the mutable ``_EN_MONTH_TO_FR`` global
    directly, so the read is a tracked call rather than an attribute access
    the static analyzer cannot follow."""
    return _EN_MONTH_TO_FR
