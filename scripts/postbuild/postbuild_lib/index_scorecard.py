"""Interactive index-scorecard injection (progressive enhancement).

An article authors a single mount marker where the interactive self-assessment
should appear::

    <div class="index-scorecard" data-index="agentic-ai-index-banks-2026"></div>

This pass upgrades that marker, at build time, into an inert ``<index-scorecard>``
custom element that carries:

* a light-DOM fallback paragraph (shown when JS is off — the article's static
  maturity tables above remain the real baseline), and
* a ``<script type="application/json">`` data island holding the per-index JSON
  spec (from ``_data/indices/<slug>.json``) plus the page-language UI strings
  (the ``scorecard.*`` namespace of ``_data/i18n/<lang>/strings.json``),

followed by one ``<script type="module" src="/_csp/index-scorecard.js">`` tag.
The component hydrates entirely client-side; nothing here executes.

CSP/SRI notes:

* The data island is ``type="application/json"`` — not executable, and not
  matched by any of postbuild's inline-script hash regexes, so it needs no CSP
  hash. Its content is unicode-escaped (``<``/``>``/``&``) so a stray
  ``</script>`` in the copy can never break out of the block.
* The module ``<script>`` is same-origin (allowed by ``script-src 'self'``) and
  is stamped with the real Subresource-Integrity digest that the asset pipeline
  computed for ``/_csp/index-scorecard.js`` (``postbuild_assets.asset_hashes``).
  This pass runs *after* ``fix_sri`` in the per-page sequence, so it stamps the
  integrity itself rather than relying on that earlier pass.

The pass is data-driven and idempotent: it does nothing on pages without the
marker, on pages already hydrated, or when the referenced spec is absent.
"""

from __future__ import annotations

import json
import re
from html import escape as _esc
from pathlib import Path

# Authoring source of truth. Overridable in tests.
INDICES_DIR = Path("_data/indices")
I18N_DIR = Path("_data/i18n")

# The component asset ships into public/_csp/ (see build.sh); reference it by
# its stable, unfingerprinted name.
COMPONENT_SRC = "/_csp/index-scorecard.js"
COMPONENT_ASSET = "index-scorecard.js"

# Right-to-left page languages we localise for.
_RTL_LANGS = {"ar", "he", "fa", "ur"}

_MARKER_RE = re.compile(
    r'<div\b[^>]*\bclass="index-scorecard"[^>]*></div>',
    re.IGNORECASE,
)
_DATA_INDEX_RE = re.compile(r'data-index="([A-Za-z0-9_-]+)"')
_HTML_LANG_RE = re.compile(r'<html\b[^>]*\blang="([A-Za-z-]+)"', re.IGNORECASE)


def _page_lang(html: str) -> str:
    """The page's ``<html lang>`` (lowercased), or ``en`` if absent."""
    m = _HTML_LANG_RE.search(html)
    return m.group(1).lower() if m else "en"


def _load_spec(slug: str) -> dict | None:
    """Parse ``_data/indices/<slug>.json``; return ``None`` if missing/invalid."""
    path = INDICES_DIR / f"{slug}.json"
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return None


def _load_strings(lang: str) -> dict[str, str]:
    """The ``scorecard.*`` UI strings for ``lang`` (falling back to ``en`` when
    that locale's strings file is missing). Only the scorecard namespace is
    inlined — the parity gate guarantees every locale carries the same keys."""
    for candidate in (lang, "en"):
        path = I18N_DIR / candidate / "strings.json"
        if not path.is_file():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        return {
            k: v for k, v in data.items() if k.startswith("scorecard.")
        }
    return {}


def _integrity_attr() -> str:
    """`` integrity="…" crossorigin="anonymous"`` for the component asset, or
    ``""`` when its digest is not (yet) known (e.g. in unit tests where the
    asset pipeline has not run)."""
    # Imported lazily so the module is importable without the asset pipeline
    # having populated the hash table, and so tests can monkeypatch it.
    from postbuild_assets import asset_hashes

    digest = asset_hashes.get(COMPONENT_ASSET)
    if not digest:
        return ""
    return f' integrity="{digest}" crossorigin="anonymous"'


def _data_island(spec: dict, strings: dict[str, str], lang: str, direction: str) -> str:
    """The ``<script type="application/json">`` payload, unicode-escaped so a
    literal ``</script>`` in the copy cannot terminate the block early."""
    payload = {"spec": spec, "strings": strings, "lang": lang, "dir": direction}
    text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return text.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def _build_block(spec: dict, strings: dict[str, str], lang: str) -> str:
    """The full replacement markup for one mount marker."""
    direction = "rtl" if lang in _RTL_LANGS else "ltr"
    fallback = strings.get(
        "scorecard.fallback",
        "The maturity dimensions are tabulated above. Enable JavaScript to "
        "score your institution interactively and export the result.",
    )
    island = _data_island(spec, strings, lang, direction)
    slug = _esc(str(spec.get("slug", "")), quote=True)
    return (
        f'<index-scorecard data-index="{slug}" dir="{direction}">'
        f'<p class="index-scorecard__fallback">{_esc(fallback)}</p>'
        f'<script type="application/json" class="index-scorecard-data">{island}</script>'
        f"</index-scorecard>"
        f'<script type="module" src="{COMPONENT_SRC}"{_integrity_attr()}></script>'
    )


def inject_index_scorecard(html: str) -> str:
    """Replace every index-scorecard mount marker with the hydrated component.

    No-op when: there is no marker, the page is already hydrated, the marker
    carries no resolvable ``data-index``, or the referenced spec is absent."""
    if "index-scorecard" not in html:
        return html
    if "<index-scorecard" in html:
        return html  # already hydrated — idempotent

    lang = _page_lang(html)

    def replace(match: re.Match[str]) -> str:
        di = _DATA_INDEX_RE.search(match.group(0))
        if not di:
            return match.group(0)
        spec = _load_spec(di.group(1))
        if spec is None:
            return match.group(0)
        strings = _load_strings(lang)
        return _build_block(spec, strings, lang)

    return _MARKER_RE.sub(replace, html)
