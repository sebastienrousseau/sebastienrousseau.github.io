#!/usr/bin/env python3
"""Guards for the Phase-2 client-side search (ADR-0010).

Pins the contract between the search runtime and the rest of the build so a
future edit can't silently break it:

  1. Every strings.json key the search-ui generator projects (``FIELDS``) exists
     in the EN reference — and therefore, via the parity gate, in all 28 locales.
  2. The locale manifest the client fetches covers every active locale and points
     each at the right ``search-index.json`` shard (EN at root, others under
     ``/<code>/``).
  3. The ``/search`` page ships its JS-off fallback and the ``#search-page`` mount.
  4. The runtime assets exist and are wired into ``build.sh`` (copy + generator),
     and the ⌘K bootstrap survives in ``main.js``.

Pure static checks — no network, no build required. Run from repo root:
``python3 tests/validation/test_search_ui_parity.py``. Exits non-zero on defect.
"""

from __future__ import annotations

import sys as _sys
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[2] / "scripts" / "lib"))
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2] / "scripts" / "generators"))

import sys
from pathlib import Path

import _lang_registry  # type: ignore[import-not-found]
import build_search_ui  # type: ignore[import-not-found]

ROOT = Path(__file__).resolve().parents[2]


def _problems() -> list[str]:
    out: list[str] = []

    # 1. FIELDS ⊆ EN strings.json keys
    en = _lang_registry.load_strings("en")
    out.extend(
        f"FIELDS[{field!r}] -> {key!r} missing from EN strings.json"
        for field, key in build_search_ui.FIELDS.items()
        if key not in en
    )

    # 2. locale manifest shape + shard URLs
    manifest = build_search_ui._locale_manifest()
    active = {lang.code for lang in _lang_registry.active()}
    codes = {m["code"] for m in manifest}
    if codes != active:
        out.append(f"manifest codes {sorted(codes)} != active locales {sorted(active)}")
    out.extend(
        f"manifest entry {m.get('code', '?')} missing {req!r}"
        for m in manifest
        for req in ("code", "label", "bcp47", "rtl", "index")
        if req not in m
    )
    by_code = {m["code"]: m["index"] for m in manifest}
    if by_code.get("en") != "/search-index.json":
        out.append(f"EN index url wrong: {by_code.get('en')!r}")
    if by_code.get("fr") != "/fr/search-index.json":
        out.append(f"FR index url wrong: {by_code.get('fr')!r}")

    # 3. /search page fallback + mount
    page = ROOT / "_posts" / "search.md"
    if not page.is_file():
        out.append("_posts/search.md missing")
    else:
        t = page.read_text(encoding="utf-8")
        if 'layout: "page"' not in t:
            out.append('_posts/search.md: expected layout "page"')
        if 'id="search-page"' not in t:
            out.append("_posts/search.md: missing #search-page mount")
        if "ss-page-fallback" not in t:
            out.append("_posts/search.md: missing ss-page-fallback (JS-off fallback)")

    # 4. runtime assets + build wiring + bootstrap
    out.extend(
        f"{asset} missing"
        for asset in ("_layouts/search.js", "_layouts/search.css")
        if not (ROOT / asset).is_file()
    )
    build = (ROOT / "build.sh").read_text(encoding="utf-8")
    out.extend(
        f"build.sh missing wiring: {needle!r}"
        for needle in (
            "cp -f _layouts/search.js public/search.js",
            "cp -f _layouts/search.css public/search.css",
            "scripts/generators/build_search_ui.py",
        )
        if needle not in build
    )
    main_js = (ROOT / "_layouts" / "main.js").read_text(encoding="utf-8")
    out.extend(
        f"main.js missing search bootstrap token: {needle!r}"
        for needle in ("SiteSearch", "ensureSearch", "search-page")
        if needle not in main_js
    )

    return out


def main() -> int:
    problems = _problems()
    if problems:
        print("search-ui contract defects:", file=sys.stderr)
        for line in problems:
            print(f"  - {line}", file=sys.stderr)
        return 1
    print("ok: search-ui contract holds (FIELDS parity, manifest, /search page, wiring)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
