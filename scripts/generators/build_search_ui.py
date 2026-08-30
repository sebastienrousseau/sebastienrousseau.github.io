#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Emit per-locale ``search-ui.json`` for the client-side search runtime.

Phase 2 of the Developer-Experience plan ships a lazy-loaded, dependency-free
on-site search (see ADR-0010). The runtime (`/search.js`) needs localised UI
microcopy — placeholder, "no results", the "search all languages" toggle, aria
labels — for whichever locale the reader is on. Those strings already live in
``_data/i18n/<lang>/strings.json`` under the ``search.*`` keys (parity-enforced by
``tests/validation/test_i18n_strings.py``); this generator projects that subset
into a small static JSON the browser can fetch (``connect-src 'self'``).

It also stamps each file with the reader's locale metadata (code, bcp47, rtl) and
the full active-locale manifest, so the "search all languages" toggle and the
``/search`` page language selector know which ``/<lang>/search-index.json`` shards
exist — without hard-coding the locale list in JS.

Inputs : ``_data/i18n/<lang>/strings.json`` + :mod:`_lang_registry`.
Outputs (per active locale):
  * ``public/search-ui.json``            (EN)
  * ``public/<lang>/search-ui.json``     (every active locale ≠ EN)

Reads only ``_data`` and writes into ``public/<lang>/`` — safe to run any time
after ``ssg`` has created the locale directories (wired after
``build_translations`` in ``build.sh``). Idempotent.
"""

from __future__ import annotations

import sys as _sys  # path bootstrap — scripts reorg (scripts/lib/ on sys.path)
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "lib"))

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _lang_registry  # type: ignore[import-not-found]  # script-mode sibling import

PUBLIC = Path("public")

# The search.* keys the runtime consumes, mapped to the compact field names it
# reads. Keeping the mapping explicit (rather than dumping every search.* key)
# means an unrelated strings.json edit can't silently bloat the client payload.
FIELDS: dict[str, str] = {
    "label": "search.label",
    "placeholder": "search.placeholder",
    "title": "search.title",
    "dialogLabel": "search.dialogLabel",
    "clear": "search.clear",
    "close": "search.close",
    "noResults": "search.noResults",
    "searching": "search.searching",
    "resultsLabel": "search.resultsLabel",
    "allLocales": "search.allLocales",
    "hint": "search.hint",
    "jsRequired": "search.jsRequired",
    "pageHeading": "search.pageHeading",
    "pageDescription": "search.pageDescription",
    "kbdEsc": "search.kbdEsc",
    "kbdNavigate": "search.kbdNavigate",
    "kbdEnter": "search.kbdEnter",
}


def _locale_manifest() -> list[dict[str, object]]:
    """Every active locale as {code, label, bcp47, rtl, index} for the client.

    ``index`` is the URL of that locale's search index shard; EN lives at the
    site root, every other locale under ``/<code>/``.
    """
    out: list[dict[str, object]] = []
    for lang in _lang_registry.active():
        base = "" if lang.code == "en" else f"/{lang.code}"
        out.append(
            {
                "code": lang.code,
                "label": lang.long_label,
                "bcp47": lang.bcp47,
                "rtl": bool(lang.rtl),
                "index": f"{base}/search-index.json",
            }
        )
    return out


def build_one(lang: _lang_registry.Language, manifest: list[dict[str, object]]) -> Path | None:
    strings = _lang_registry.load_strings(lang.code)
    ui = {field: strings.get(key, "") for field, key in FIELDS.items()}
    payload = {
        "lang": lang.code,
        "bcp47": lang.bcp47,
        "rtl": bool(lang.rtl),
        "ui": ui,
        "locales": manifest,
    }
    out_dir = PUBLIC if lang.code == "en" else PUBLIC / lang.code
    if not out_dir.is_dir():
        # Locale directory not built (e.g. partial local build) — skip quietly
        # rather than fabricating a stray tree; CI builds every locale.
        return None
    dest = out_dir / "search-ui.json"
    dest.write_text(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    return dest


def main() -> int:
    if not PUBLIC.is_dir():
        print("build_search_ui: public/ not found — run ssg first", file=sys.stderr)
        return 1
    manifest = _locale_manifest()
    written = 0
    skipped = 0
    for lang in _lang_registry.active():
        dest = build_one(lang, manifest)
        if dest is None:
            skipped += 1
        else:
            written += 1
    print(f"build_search_ui: wrote {written} search-ui.json file(s), skipped {skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
