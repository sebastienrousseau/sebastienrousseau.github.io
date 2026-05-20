#!/usr/bin/env python3
"""DEPRECATED shim — use ``scripts/build_lang_feeds.py`` instead.

This wrapper kept for backwards compatibility (anything still invoking
``build_fr_feeds.py`` directly). The real implementation is now
language-agnostic and lives in :mod:`build_lang_feeds`. It builds
feeds for every active non-EN language declared in
:mod:`_lang_registry`, with channel-level metadata read from each
language's ``_data/i18n/<lang>/strings.json`` under the
``feeds.channel*`` keys.
"""
from __future__ import annotations

import sys as _sys  # path bootstrap — scripts reorg (scripts/lib/ on sys.path)
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "lib"))

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import build_lang_feeds  # type: ignore[import-not-found]


def main() -> None:
    n = build_lang_feeds.build_for_lang("fr")
    if not n:
        print("build_fr_feeds: no French entries found — nothing to do")
        return
    print(
        f"build_fr_feeds: wrote {n} entry feeds "
        f"(rss.xml + atom.xml + news-sitemap.xml + feed.json)"
    )


if __name__ == "__main__":
    main()
