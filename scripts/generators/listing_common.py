"""Shared listing helpers (leaf): frontmatter regexes, pillar order, default
banner, and the locale slug/post-index loaders used by the listing generators.

Split from build_listings (Phase 4.1). Imports only the standard library and
defines its own ROOT, so build_listings imports these back with no cycle.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

_TITLE_FM_RE = re.compile(r'^title:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)
_EXCERPT_FM_RE = re.compile(r'^excerpt:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)
_DESC_FM_RE = re.compile(r'^description:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)
_BANNER_FM_RE = re.compile(r'^banner:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)
_TAG_FM_RE = re.compile(r'^tags:\s*"?([^"\n]+)"?', re.MULTILINE)


def _strip_fm_quotes(value: str) -> str:
    """Strip one matching pair of surrounding single OR double quotes.

    The ``_*_FM_RE`` field regexes above only strip a *double*-quote pair
    (``"?…"?``); a single-quoted YAML value (used by the ``vi`` corpus,
    e.g. ``banner: 'https://…webp'`` or ``title: 'Bitcoin…'``) is captured
    *with* its surrounding apostrophes, which then leak into rendered card
    ``<img src>`` / titles as literal quotes + ``&#x27;`` entities.

    This peels exactly one matching leading+trailing quote pair, and only
    when *both* ends match the same quote char. That leaves untouched:
    - unquoted values (``Bitcoin standard``),
    - already-stripped double-quoted values,
    - double-quoted values that legitimately contain an apostrophe
      (``"Bitcoin's year in review"`` → the regex already yields
      ``Bitcoin's year in review``; first/last chars are ``B``/``w``, so
      no pair is peeled and the apostrophe survives).
    """
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value
PILLAR_ORDER = ("ai", "payments", "infra", "policy", "open-source", "leadership")
def _alias_map(taxonomy: dict) -> dict[str, str]:
    out: dict[str, str] = {}
    for slug, entry in taxonomy.items():
        out[slug.strip().lower()] = slug
        for alias in entry.get("aliases", []) or []:
            out[alias.strip().lower()] = slug
    return out
def _post_pillars(text: str, taxonomy: dict, amap: dict[str, str]) -> list[str]:
    """Return the deduplicated pillars (categories) a post belongs to,
    derived from its frontmatter `tags:` line resolved through aliases."""
    m = _TAG_FM_RE.search(text)
    if not m:
        return []
    pillars: set[str] = set()
    for raw in m.group(1).split(","):
        tag = raw.strip().strip('"').strip("'").strip()
        canon = amap.get(tag.lower())
        if not canon:
            continue
        cat = taxonomy.get(canon, {}).get("category")
        if cat:
            pillars.add(cat)
    # Stable order — same as the pillar nav.
    return [p for p in PILLAR_ORDER if p in pillars]
_DEFAULT_BANNER = "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp"
def _load_fr_to_en_slug_map(lang: str) -> dict[str, str]:
    """Return ``{locale_slug: en_slug}`` from
    ``_data/i18n/<lang>/slugs.json``. Returns {} when the file is
    missing or malformed; locale forks then key off the bare stem."""
    slugs_path = ROOT / "_data" / "i18n" / lang / "slugs.json"
    if not slugs_path.is_file():
        return {}
    try:
        data = json.loads(slugs_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return {
        locale_slug: en_slug
        for en_slug, locale_slug in (data.get("articles") or {}).items()
        if isinstance(locale_slug, str) and locale_slug
    }
def _locale_post_card_fields(
    path: Path,
) -> tuple[str, str, str, str] | None:
    """Extract (stem, title, excerpt, banner) from one locale post.
    Returns None when the post has no `title:` frontmatter (incomplete
    translation)."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    title_m = _TITLE_FM_RE.search(text)
    if not title_m:
        return None
    excerpt_m = _EXCERPT_FM_RE.search(text)
    desc_m = _DESC_FM_RE.search(text)
    banner_m = _BANNER_FM_RE.search(text)
    title = _strip_fm_quotes(title_m.group(1))
    excerpt = _strip_fm_quotes(
        excerpt_m.group(1)
        if excerpt_m
        else (desc_m.group(1) if desc_m else "")
    )
    banner = _strip_fm_quotes(banner_m.group(1)) if banner_m else _DEFAULT_BANNER
    return path.stem, title, excerpt, banner
def _load_locale_post_index(
    lang: str,
) -> dict[str, tuple[str, str, str, str]]:
    """Return ``{en_slug: (locale_slug, locale_title, locale_excerpt,
    locale_banner)}`` for every dated post in ``_posts/<lang>/``. The
    EN slug is the source-of-truth join key; build_translations writes
    the locale-slug map into `_data/i18n/<lang>/slugs.json`, so we
    reuse that for the reverse lookup. Posts present in `_posts/<lang>/`
    take their frontmatter directly; everything else falls back to the
    EN card (handled at render time by the caller)."""
    src = ROOT / "_posts" / lang
    if not src.is_dir():
        return {}
    fr_to_en = _load_fr_to_en_slug_map(lang)
    out: dict[str, tuple[str, str, str, str]] = {}
    for path in sorted(src.glob("*.md")):
        fields = _locale_post_card_fields(path)
        if fields is None:
            continue
        stem, title, excerpt, banner = fields
        en_slug = fr_to_en.get(stem, stem)
        out[en_slug] = (stem, title, excerpt, banner)
    return out
def _load_locale_article_slugs(lang: str) -> dict[str, str]:
    path = ROOT / "_data" / "i18n" / lang / "slugs.json"
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    arts = data.get("articles") or {}
    return {k: v for k, v in arts.items() if isinstance(v, str) and v}
def _translate_chrome_for(lang: str, html: str) -> str:
    """Apply build_translations.translate_chrome bound to ``lang`` —
    translates nav, footer, search labels, aria attributes, language
    menu, dates. Body content (which we emit ourselves) is left alone.
    Raises ``RuntimeError`` if the package isn't importable so silent
    EN-chrome leaks don't ship."""
    # Ensure repo root is on sys.path even when this module is invoked
    # as a script (`python3 scripts/generators/build_listings.py`) —
    # otherwise the `scripts.generators...` package path won't resolve
    # and the import would have to fall back to untranslated chrome.
    import sys as _sys
    if str(ROOT) not in _sys.path:
        _sys.path.insert(0, str(ROOT))
    from scripts.generators.build_translations import _state as _bt_state
    from scripts.generators.build_translations._chrome import translate_chrome
    _bt_state.bind_lang(lang)
    return translate_chrome(html)
