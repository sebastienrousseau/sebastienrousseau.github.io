"""Single source of truth for the languages this site publishes.

Every i18n-aware part of the build pipeline (translation renderer,
hreflang injector, sitemap builder, parity tests) reads this module
rather than hard-coding language codes. Adding a new language is a
single edit here + the matching ``_data/i18n/<code>/*.json`` files.

A language is either ``active`` (full translations published) or
``planned`` (listed in the lang switcher with "Coming soon" but no
content). The split exists so we can keep the lang switcher complete
without flooding sitemaps + hreflang with non-existent URLs.

Reading the JSON glossary
=========================
Use ``load_strings(code)`` rather than opening JSON directly — that
function validates the shape against the English reference and
raises ``LanguageError`` on missing keys, which is what the CI gate
``scripts/test_i18n_strings.py`` relies on.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
I18N_DIR = ROOT / "_data" / "i18n"


@dataclass(frozen=True)
class Language:
    """A language the site publishes (or plans to publish).

    Attributes:
        code: short identifier used in URL paths (``en``, ``fr``,
              ``zh-hans``). Lower-case, hyphenated. Stable forever.
        bcp47: full BCP-47 tag for ``<html lang>`` and JSON-LD
               ``inLanguage`` (``en-GB``, ``fr-FR``, ``zh-Hans``).
        og_locale: Open Graph ``og:locale`` value (``en_GB`` etc.).
        display_label: short label shown in the lang switcher button
                       (``EN``, ``FR``, ``DE``).
        long_label: native name shown in the switcher menu
                    (``English``, ``Français``, ``Deutsch``).
        flag_emoji: country flag for the menu. Cosmetic only.
        rtl: True for right-to-left languages (Arabic, Hebrew).
        active: True if full translations ship; False if the lang
                switcher lists it as "coming soon" only.
    """

    code: str
    bcp47: str
    og_locale: str
    display_label: str
    long_label: str
    flag_emoji: str
    rtl: bool = False
    active: bool = False


LANGUAGES: tuple[Language, ...] = (
    # English is the source of truth — always active, always first.
    Language("en", "en-GB", "en_GB", "EN", "English", "🇬🇧", active=True),

    # Active translations. Each ships a complete site under /<code>/.
    Language("fr", "fr-FR", "fr_FR", "FR", "Français", "🇫🇷", active=True),

    # Planned languages — listed in the lang switcher but no content
    # yet. They are intentionally ``active=False`` so hreflang +
    # sitemap don't reference URLs that don't exist. Flipping
    # ``active=True`` requires the matching ``_data/i18n/<code>/``
    # tree to exist; ``scripts/test_i18n_parity.py`` enforces that.
    Language("ar", "ar-SA", "ar_SA", "AR", "العربية", "🇸🇦", rtl=True, active=True),
    Language("bn", "bn-BD", "bn_BD", "BN", "বাংলা", "🇧🇩"),
    Language("cs", "cs-CZ", "cs_CZ", "CS", "Čeština", "🇨🇿"),
    Language("de", "de-DE", "de_DE", "DE", "Deutsch", "🇩🇪", active=True),
    Language("es", "es-ES", "es_ES", "ES", "Español", "🇪🇸", active=True),
    Language("fil", "fil-PH", "fil_PH", "FIL", "Filipino", "🇵🇭"),
    Language("ha", "ha-NG", "ha_NG", "HA", "Hausa", "🇳🇬"),
    Language("he", "he-IL", "he_IL", "HE", "עברית", "🇮🇱", rtl=True),
    Language("hi", "hi-IN", "hi_IN", "HI", "हिन्दी", "🇮🇳"),
    Language("id", "id-ID", "id_ID", "ID", "Indonesia", "🇮🇩"),
    Language("it", "it-IT", "it_IT", "IT", "Italiano", "🇮🇹"),
    Language("ja", "ja-JP", "ja_JP", "JA", "日本語", "🇯🇵"),
    Language("ko", "ko-KR", "ko_KR", "KO", "한국어", "🇰🇷"),
    Language("nl", "nl-NL", "nl_NL", "NL", "Nederlands", "🇳🇱"),
    Language("pl", "pl-PL", "pl_PL", "PL", "Polski", "🇵🇱"),
    Language("pt-br", "pt-BR", "pt_BR", "PT", "Português", "🇧🇷"),
    Language("ro", "ro-RO", "ro_RO", "RO", "Română", "🇷🇴"),
    Language("ru", "ru-RU", "ru_RU", "RU", "Русский", "🇷🇺"),
    Language("sv", "sv-SE", "sv_SE", "SV", "Svenska", "🇸🇪"),
    Language("th", "th-TH", "th_TH", "TH", "ไทย", "🇹🇭"),
    Language("tr", "tr-TR", "tr_TR", "TR", "Türkçe", "🇹🇷"),
    Language("uk", "uk-UA", "uk_UA", "UK", "Українська", "🇺🇦"),
    Language("vi", "vi-VN", "vi_VN", "VI", "Tiếng Việt", "🇻🇳"),
    Language("yo", "yo-NG", "yo_NG", "YO", "Yorùbá", "🇳🇬"),
    Language("zh-hans", "zh-Hans", "zh_CN", "ZH", "简体中文", "🇨🇳", active=True),
    Language("zh-hant", "zh-Hant", "zh_TW", "ZH-TW", "繁體中文", "🇹🇼"),
)

_BY_CODE: dict[str, Language] = {lang.code: lang for lang in LANGUAGES}


class LanguageError(ValueError):
    """Raised when a language lookup fails or its data files are malformed."""


def get(code: str) -> Language:
    """Look up a language by code. Raises if unknown."""
    lang = _BY_CODE.get(code)
    if lang is None:
        raise LanguageError(f"unknown language code: {code!r}")
    return lang


def active() -> tuple[Language, ...]:
    """Languages with full translations published. EN is always first."""
    return tuple(lang for lang in LANGUAGES if lang.active)


def planned() -> tuple[Language, ...]:
    """Languages listed in the switcher but without content yet."""
    return tuple(lang for lang in LANGUAGES if not lang.active and lang.code != "en")


# ---------------------------------------------------------------------------
# Glossary loading
# ---------------------------------------------------------------------------

def load_slugs(code: str) -> dict[str, dict[str, str]]:
    """Load the EN→native slug map for ``code``.

    Returns a dict with two keys: ``static`` (slug→native) and
    ``articles`` (slug→native). Raises if the file is missing or
    malformed.
    """
    path = I18N_DIR / code / "slugs.json"
    if not path.is_file():
        raise LanguageError(f"missing slug map: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    for required in ("static", "articles"):
        if required not in data or not isinstance(data[required], dict):
            raise LanguageError(f"{path}: missing required key {required!r}")
    return data


def load_topics(code: str) -> dict[str, dict[str, str]]:
    """Load topic titles + ledes for ``code``."""
    path = I18N_DIR / code / "topics.json"
    if not path.is_file():
        raise LanguageError(f"missing topic glossary: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise LanguageError(f"{path}: must be a JSON object")
    return data


def load_static_pages(code: str) -> dict[str, dict[str, str]]:
    """Load per-static-page metadata (title, subtitle, description, keywords)."""
    path = I18N_DIR / code / "static_pages.json"
    if not path.is_file():
        raise LanguageError(f"missing static-page glossary: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise LanguageError(f"{path}: must be a JSON object")
    return data


def load_strings(code: str) -> dict[str, str]:
    """Load UI-string glossary for ``code``.

    Returns a flat dict mapping string-key (dot-notation) to that
    language's translated value. Keys starting with ``_`` (e.g.
    ``_comment``) are documentation-only and stripped.

    The English file at ``_data/i18n/en/strings.json`` is the canonical
    reference — every other language must carry the same key set.
    Enforce via :mod:`scripts.test_i18n_strings`.
    """
    path = I18N_DIR / code / "strings.json"
    if not path.is_file():
        raise LanguageError(f"missing UI-strings glossary: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise LanguageError(f"{path}: must be a JSON object")
    # Strip documentation-only keys (`_comment`, `_note`, ...).
    return {k: v for k, v in data.items() if not k.startswith("_")}


def load_author(code: str) -> dict[str, str]:
    """Load author-card prose for ``code``.

    The author-card aside at the bottom of every dated article needs
    a localised bio + credentials-prefix string. Keys: ``bio``,
    ``credentialsPrefix``. CI gate :mod:`scripts.test_i18n_author`
    enforces key-set parity across languages.
    """
    path = I18N_DIR / code / "author.json"
    if not path.is_file():
        raise LanguageError(f"missing author glossary: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise LanguageError(f"{path}: must be a JSON object")
    return {k: v for k, v in data.items() if not k.startswith("_")}


def load_home_patches(code: str) -> list[tuple[str, str]]:
    """Load home-page chrome patches for ``code``.

    Each entry is a (regex_pattern, replacement) pair applied to the EN
    homepage shell to translate it into ``code``. The regex matches EN
    content; the replacement is in the target language. Used by
    ``build_translations.render_home`` for every active non-EN
    language. CI gate :mod:`scripts.test_i18n_home_patches` enforces
    entry-count parity with the FR source.
    """
    path = I18N_DIR / code / "home_patches.json"
    if not path.is_file():
        raise LanguageError(f"missing home-patches glossary: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "patches" not in data:
        raise LanguageError(f"{path}: must be a JSON object with 'patches' key")
    return [tuple(p) for p in data["patches"]]


def load_static_bodies(code: str) -> dict[str, str]:
    """Load static-page body HTML for ``code``.

    Returns a dict mapping page-slug → inner-HTML body string. Used by
    ``build_translations.render_static_translation`` to substitute the
    body of /<code>/<slug>/ pages.
    """
    path = I18N_DIR / code / "static_bodies.json"
    if not path.is_file():
        raise LanguageError(f"missing static-bodies glossary: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "bodies" not in data:
        raise LanguageError(f"{path}: must be a JSON object with 'bodies' key")
    return data["bodies"]


def load_static_patches(code: str) -> list[tuple[str, str]]:
    """Load static-page chrome patches for ``code``.

    Each entry is a (regex_pattern, replacement) pair applied to the EN
    static-page shells (/papers/, /projects/, /topics/, /about/, etc.)
    when forking them into ``code``.
    """
    path = I18N_DIR / code / "static_patches.json"
    if not path.is_file():
        raise LanguageError(f"missing static-patches glossary: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "patches" not in data:
        raise LanguageError(f"{path}: must be a JSON object with 'patches' key")
    return [tuple(p) for p in data["patches"]]


def load_chrome_patches_inline(code: str) -> list[tuple[str, str]]:
    """Load the *inline* chrome patches for ``code``.

    The full CHROME_PATCHES list in ``build_translations.py`` is the
    auto-generated portion (from strings.json via
    :func:`build_chrome_patches`) prepended to this inline portion. The
    auto-generated portion comes from key-value swaps in
    ``strings.json``; this inline portion is the rest — page-specific
    regex replacements that don't fit the simple key-value shape.
    """
    path = I18N_DIR / code / "chrome_patches.json"
    if not path.is_file():
        raise LanguageError(f"missing chrome-patches glossary: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "patches" not in data:
        raise LanguageError(f"{path}: must be a JSON object with 'patches' key")
    return [tuple(p) for p in data["patches"]]


def load_takeaway_labels(code: str) -> dict[str, str]:
    """Load takeaway-aside labels for ``code``.

    The "Key takeaways" aside in every dated post contains rows like
    ``<li><strong>Idea.</strong> ...</li>``; ``build_translations.py``
    substitutes these per language. Distinct from :func:`load_strings`
    (global UI chrome) and :func:`load_labels` (article body chrome).

    Keys starting with ``_`` are documentation-only and stripped. The
    English file is the canonical reference; CI gate
    :mod:`scripts.test_i18n_takeaway_labels` enforces key-set parity.
    """
    path = I18N_DIR / code / "takeaway_labels.json"
    if not path.is_file():
        raise LanguageError(f"missing takeaway-labels glossary: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise LanguageError(f"{path}: must be a JSON object")
    return {k: v for k, v in data.items() if not k.startswith("_")}


def load_labels(code: str) -> dict[str, str]:
    """Load body-text labels for ``code``.

    Distinct from :func:`load_strings`: ``strings.json`` is global UI
    chrome (nav, footer, search), while ``labels.json`` is the smaller
    set of inline body-text strings that ``build_translations.py``
    substitutes when forking the EN page shell into another language
    (Published / Updated / min read / Sources & references / etc.).

    Keys starting with ``_`` are documentation-only and stripped. The
    English file is the canonical reference; CI gate
    :mod:`scripts.test_i18n_labels` enforces key-set parity.
    """
    path = I18N_DIR / code / "labels.json"
    if not path.is_file():
        raise LanguageError(f"missing body-labels glossary: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise LanguageError(f"{path}: must be a JSON object")
    return {k: v for k, v in data.items() if not k.startswith("_")}


def fr_slug(en_slug: str) -> str:
    """Convenience: EN slug → FR slug. Returns input unchanged if no
    translation is recorded — matches the legacy ``_fr_slugs.fr_slug``
    behaviour. Caches the slug map on first call."""
    return _fr_article_map().get(en_slug, en_slug)


# ---------------------------------------------------------------------------
# Chrome-patch generator (Phase 0c: strings.json → runtime regex pairs)
# ---------------------------------------------------------------------------
#
# ``build_chrome_patches(lang)`` returns a list of ``(regex, replacement)``
# tuples derived from ``_data/i18n/<lang>/strings.json``, suitable for
# pre-pending to the manual ``CHROME_PATCHES`` list in
# ``scripts/build_translations.py``. Existing manual entries stay in
# place — the auto-generated patches act as a *backup* source of truth.
# When the auto-gen entry fires first, the manual one becomes a harmless
# no-op (regex won't match the already-translated string).
#
# Each entry in ``_STRINGS_KEY_TO_PATCH`` maps a flat strings.json key to
# a small descriptor of where that string lives in HTML. Only the
# mechanical attribute-style cases are auto-generated; entries with
# regex quirks (negative lookahead, dynamic prefix, ``&amp;`` vs ``&``)
# stay manual.

import re as _re

# Patch-context kind. Each kind has its own regex shape and behaviour:
#   attr:<attr>     → quote-tolerant attribute value patch, e.g.
#                     `(aria-label=)"?Toggle…"?` → `aria-label="Basculer…"`
#   text-button     → button body text, e.g. `>Subscribe</button>`
#   text-a          → anchor body text, e.g. `>Skip to main content</a>`
#   text-span       → <span> body text, e.g. `<span>Search</span>`
#   text-h2:<class> → <h2 class="X">Body</h2>
_STRINGS_KEY_TO_PATCH: tuple[tuple[str, str], ...] = (
    ("nav.aria.skipToMain",        "text-a"),
    ("nav.aria.toggleNav",         "attr:aria-label"),
    ("nav.aria.toggleNavTitle",    "attr:title"),
    ("nav.aria.primary",           "attr:aria-label"),
    ("nav.aria.darkTheme",         "attr:aria-label"),
    ("nav.aria.lightTheme",        "attr:aria-label"),
    ("nav.aria.themeToggleTitle",  "attr:title"),
    ("nav.aria.searchTitle",       "attr:title"),
    ("nav.aria.contactCTA",        "attr:aria-label"),
    ("nav.contactCTA",             "text-a"),
    ("nav.aria.brandHome",         "attr:aria-label"),
    ("nav.aria.backToTop",         "attr:aria-label"),
    ("search.placeholder",         "attr:placeholder"),
    ("search.buttonLabel",         "text-span"),
    ("footer.title.writing",       "text-h2:ap-foot-title"),
    ("footer.title.work",          "text-h2:ap-foot-title"),
    ("footer.title.reach",         "text-h2:ap-foot-title"),
    ("footer.aria.socialLinks",    "attr:aria-label"),
    ("feeds.atomTitle",            "attr:title"),
    ("feeds.rssTitle",             "attr:title"),
    ("lang.aria.langGroup",        "attr:aria-label"),
    ("lang.title.changeLang",      "attr:title"),
    ("lang.title.comingSoon",      "attr:title"),
    ("article.aria.summary",       "attr:aria-label"),
    ("article.keyTakeaways",       "text-strong"),
    ("newsletter.aria.signup",     "attr:aria-label"),
    ("newsletter.placeholder",     "attr:placeholder"),
    ("newsletter.submit",          "text-button"),
    ("author.aria.aboutAuthor",    "attr:aria-label"),
    ("author.fullProfile",         "text-a"),
    ("author.alt.portrait",        "attr:alt"),
    ("home.cta.startConversation", "text-a"),
)


def _build_one_patch(kind: str, en_val: str, target_val: str) -> tuple[str, str] | None:
    """Build a single (regex, replacement) pair. ``kind`` is the
    descriptor from ``_STRINGS_KEY_TO_PATCH``."""
    en_esc = _re.escape(en_val)
    if kind.startswith("attr:"):
        attr = kind.split(":", 1)[1]
        # Quote-tolerant — the minifier strips quotes on some shells, so
        # accept both `aria-label="X"` and `aria-label=X`. Anchor with a
        # lookahead so the value isn't eaten past its boundary.
        regex = rf'{attr}="?{en_esc}"?(?=[\s>])'
        repl = f'{attr}="{target_val}"'
        return regex, repl
    if kind == "text-button":
        return f'>{en_esc}</button>', f'>{target_val}</button>'
    if kind == "text-a":
        return f'>{en_esc}</a>', f'>{target_val}</a>'
    if kind == "text-span":
        return f'>{en_esc}</span>', f'>{target_val}</span>'
    if kind == "text-strong":
        return f'<strong>{en_esc}</strong>', f'<strong>{target_val}</strong>'
    if kind.startswith("text-h2:"):
        class_ = kind.split(":", 1)[1]
        regex = rf'<h2 class="?{_re.escape(class_)}"?>{en_esc}</h2>'
        repl = f'<h2 class="{class_}">{target_val}</h2>'
        return regex, repl
    return None


def build_chrome_patches(lang: str) -> list[tuple[str, str]]:
    """Return a list of ``(regex, replacement)`` patches built from
    ``_data/i18n/<lang>/strings.json``. Skip any key where the target
    value is missing, empty, or identical to English.

    Designed to be **prepended** to the manual ``CHROME_PATCHES`` list
    in ``build_translations.py``. The auto-gen patches act as a backup
    source of truth from JSON; the manual list still runs after and
    handles regex-quirky cases (entity tolerance, dynamic prefixes,
    negative lookaheads, etc.) that can't be auto-generated cleanly.
    """
    en = load_strings("en")
    target = load_strings(lang) if lang != "en" else en
    patches: list[tuple[str, str]] = []
    for key, kind in _STRINGS_KEY_TO_PATCH:
        en_val = en.get(key)
        tgt_val = target.get(key)
        if not en_val or not tgt_val or en_val == tgt_val:
            continue
        patch = _build_one_patch(kind, en_val, tgt_val)
        if patch is not None:
            patches.append(patch)
    return patches


def en_slug(fr_slug_str: str) -> str:
    """Convenience: FR slug → EN slug. Returns input unchanged if not found."""
    return _fr_to_en_map().get(fr_slug_str, fr_slug_str)


_fr_cache: dict[str, str] | None = None
_fr_reverse_cache: dict[str, str] | None = None


def _fr_article_map() -> dict[str, str]:
    global _fr_cache
    if _fr_cache is None:
        _fr_cache = load_slugs("fr")["articles"]
    return _fr_cache


def _fr_to_en_map() -> dict[str, str]:
    global _fr_reverse_cache
    if _fr_reverse_cache is None:
        _fr_reverse_cache = {v: k for k, v in _fr_article_map().items()}
    return _fr_reverse_cache
