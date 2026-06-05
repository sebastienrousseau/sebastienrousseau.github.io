"""DEPRECATED — use ``scripts/_lang_registry.py`` instead.

This module is a backward-compatibility shim. The canonical EN → FR
slug data now lives in ``_data/i18n/fr/slugs.json``; ``_lang_registry``
exposes it. New code should call ``_lang_registry.fr_slug`` /
``_lang_registry.en_slug`` directly.

Kept here so existing imports (``build_translations``, ``build_fr_feeds``,
``postbuild``) keep working unchanged while the i18n refactor lands
in stages.
"""

from __future__ import annotations

import _lang_registry  # type: ignore[import-not-found]  # script-mode sibling import


def _load() -> tuple[dict[str, str], dict[str, str]]:
    """Load the FR slug map once and expose both directions."""
    slugs = _lang_registry.load_slugs("fr")["articles"]
    return slugs, {fr: en for en, fr in slugs.items()}


EN_TO_FR, FR_TO_EN = _load()


def fr_slug(en_slug: str) -> str:
    """Return the FR slug for an EN slug, or the EN slug unchanged if
    no translation is recorded (so legacy fall-through still works)."""
    return EN_TO_FR.get(en_slug, en_slug)


def en_slug(fr_slug_str: str) -> str:
    """Reverse map (FR → EN). Returns the input unchanged if not found."""
    return FR_TO_EN.get(fr_slug_str, fr_slug_str)
