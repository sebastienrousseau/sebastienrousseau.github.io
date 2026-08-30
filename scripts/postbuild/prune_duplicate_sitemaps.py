#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Delete the per-directory sitemap copies ssg scatters through ``public/``.

ssg writes a full copy of ``sitemap.xml`` and ``news-sitemap.xml`` into every
output directory it renders. On this site that is ~3,670 sitemap copies and
~3,704 news-sitemap copies — 17 MB of the deploy artifact — and each nested
copy prefixes its URLs with the containing directory, producing malformed
double-slash entries like::

    https://sebastienrousseau.com/made-with-static-site-generator//2018-01-01-…

They are not merely wasteful. They are reachable URLs: ``/fr/news-sitemap.xml``
was served in production carrying months of entries under an email address as
the publication name, because it was one of these copies left over from an
older build rather than the file ``build_lang_feeds.py`` intends to write.

#421 taught the sitemap-completeness gate to ignore them. This removes them,
so nothing downstream has to know they ever existed.

Kept:
  * ``public/sitemap.xml``                     — the one real sitemap
  * ``public/news-sitemap.xml``                — the root news sitemap
  * ``public/<lang>/news-sitemap.xml``         — per-locale, written by
                                                 build_lang_feeds.py for every
                                                 active non-English locale

Everything else matching those two names is deleted. Idempotent.
"""

from __future__ import annotations

import sys as _sys
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "lib"))

import sys
from pathlib import Path

import _lang_registry  # type: ignore[import-not-found]

PUBLIC = Path("public")
_NAMES = ("sitemap.xml", "news-sitemap.xml")


def keep_paths(public: Path) -> set[Path]:
    """Absolute-relative paths that are legitimate sitemap artefacts."""
    keep = {public / "sitemap.xml", public / "news-sitemap.xml"}
    for lang in _lang_registry.active():
        if lang.code == "en":
            continue
        keep.add(public / lang.code / "news-sitemap.xml")
    return keep


def prune(public: Path = PUBLIC) -> int:
    """Delete every stray sitemap copy. Returns the number removed."""
    if not public.is_dir():
        return 0
    keep = keep_paths(public)
    removed = 0
    for name in _NAMES:
        for path in public.rglob(name):
            if path in keep or not path.is_file():
                continue
            path.unlink()
            removed += 1
    return removed


def main() -> int:
    removed = prune()
    print(f"prune_duplicate_sitemaps: removed {removed} stray sitemap copies")
    return 0


if __name__ == "__main__":
    sys.exit(main())
