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
    Language("ar", "ar-SA", "ar_SA", "AR", "العربية", "🇸🇦", rtl=True),
    Language("bn", "bn-BD", "bn_BD", "BN", "বাংলা", "🇧🇩"),
    Language("cs", "cs-CZ", "cs_CZ", "CS", "Čeština", "🇨🇿"),
    Language("de", "de-DE", "de_DE", "DE", "Deutsch", "🇩🇪"),
    Language("es", "es-ES", "es_ES", "ES", "Español", "🇪🇸"),
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
    Language("zh-hans", "zh-Hans", "zh_CN", "ZH", "简体中文", "🇨🇳"),
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


def fr_slug(en_slug: str) -> str:
    """Convenience: EN slug → FR slug. Returns input unchanged if no
    translation is recorded — matches the legacy ``_fr_slugs.fr_slug``
    behaviour. Caches the slug map on first call."""
    return _fr_article_map().get(en_slug, en_slug)


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
