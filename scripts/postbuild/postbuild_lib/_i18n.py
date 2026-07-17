"""Shared i18n foundation: page-language detection, per-locale UI labels,
and slug-map lookups. Extracted from article_furniture (Phase 4.1) as a base
both article_furniture and hreflang import — breaking their former cycle.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import _lang_registry as _lr

_HTML_LANG_DETECT_RE = re.compile(r'<html\b[^>]*\blang="([^"]+)"', re.IGNORECASE)
LABELS_EN: dict[str, str] = {
    "Published": "Published",
    "Updated": "Updated",
    "min read": "min read",
    "Previous": "Previous",
    "Next": "Next",
    "Sources & references": "Sources & references",
    "Contents": "Contents",
    "Article pagination": "Article pagination",
    "Estimated read time": "Estimated read time",
    "Link to": "Link to",
    "Table of contents": "Table of contents",
    "Topics": "Topics",
    "Home": "Home",
    "Breadcrumb": "Breadcrumb",
}
_LABEL_CACHE: dict[str, dict[str, str]] = {}
def _labels_for_lang(code: str) -> dict[str, str]:
    """Per-language label cache. Loads from ``labels.json`` and overlays
    a handful of extra keys ``LABELS_EN`` has but the JSON glossary
    intentionally doesn't (Table of contents, Article pagination, etc.)
    so older call sites stay valid."""
    if code in _LABEL_CACHE:
        return _LABEL_CACHE[code]
    if code == "en":
        out = dict(LABELS_EN)
    else:
        try:
            base = _lr.load_labels(code)
        except _lr.LanguageError:
            base = {}
        out = dict(LABELS_EN)
        out.update(base)
    _LABEL_CACHE[code] = out
    return out
def _detect_page_lang(html: str) -> str:
    """Resolve the page's ``<html lang>`` attribute to a registry
    language code. Tries the full lowercased BCP-47 tag first so
    region/script locales (``pt-BR`` -> ``pt-br``, ``zh-Hans`` ->
    ``zh-hans``) resolve to their registry code instead of collapsing
    to a primary subtag that isn't a published language; falls back to
    the primary subtag (``fr-FR`` -> ``fr``)."""
    m = _HTML_LANG_DETECT_RE.search(html)
    if not m:
        return "en"
    tag = m.group(1).lower()
    if tag in _lr._BY_CODE:
        return tag
    return tag.split("-", 1)[0]
def _labels(html: str) -> dict[str, str]:
    return _labels_for_lang(_detect_page_lang(html))
_STRINGS_CACHE: dict[str, dict[str, str]] = {}
def _strings_for_lang(code: str) -> dict[str, str]:
    """Per-language UI-strings cache (``strings.json``). Returns {} for
    unknown codes so callers fall back to their EN literals."""
    if code not in _STRINGS_CACHE:
        try:
            _STRINGS_CACHE[code] = _lr.load_strings(code)
        except _lr.LanguageError:
            _STRINGS_CACHE[code] = {}
    return _STRINGS_CACHE[code]
def _all_active_non_en_langs() -> list[str]:
    """Return the code for every active non-EN language."""
    return [lg.code for lg in _lr.LANGUAGES if lg.active and lg.code != "en"]
def _slug_maps_for(code: str) -> dict[str, dict[str, str]]:
    """Return the article + static slug maps (both directions) for ``code``."""
    s = _lr.load_slugs(code)
    articles = s.get("articles", {})
    statics = s.get("static", {})
    return {
        "articles_en_to_lang": articles,
        "articles_lang_to_en": {v: k for k, v in articles.items()},
        "statics_en_to_lang": statics,
        "statics_lang_to_en": {v: k for k, v in statics.items()},
    }
_SLUG_MAPS_CACHE: dict[str, dict[str, dict[str, str]]] = {}
def _slug_maps(code: str) -> dict[str, dict[str, str]]:
    if code not in _SLUG_MAPS_CACHE:
        _SLUG_MAPS_CACHE[code] = _slug_maps_for(code)
    return _SLUG_MAPS_CACHE[code]
