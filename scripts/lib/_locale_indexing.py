# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Which locales search engines may index.

The policy lives in ``_data/seo/locale-indexing.json`` (one list, the
``indexed`` codes). Every other active locale in ``_lang_registry`` is
*published but not indexed*: its pages stay live for readers and in the
language switcher, but carry ``noindex, follow``, are absent from every
sitemap, and appear in no hreflang cluster. Keeping the list in data, not
code, means changing the policy is one edit with no code review of logic.
"""

from __future__ import annotations

import json
from functools import cache
from pathlib import Path

import _lang_registry as _lr

POLICY = Path(__file__).resolve().parents[2] / "_data" / "seo" / "locale-indexing.json"


class LocaleIndexingError(ValueError):
    """Raised when the policy file names an unknown locale or omits English."""


@cache
def indexed_codes() -> frozenset[str]:
    """Locale codes search engines may index (always includes ``en``)."""
    payload = json.loads(POLICY.read_text(encoding="utf-8"))
    codes = frozenset(payload["indexed"])
    known = {lang.code for lang in _lr.active()}
    unknown = sorted(codes - known)
    if unknown:
        raise LocaleIndexingError(f"locale-indexing.json names inactive locales: {unknown}")
    if "en" not in codes:
        raise LocaleIndexingError("locale-indexing.json must index 'en'")
    return codes


def is_indexed(code: str) -> bool:
    """True when pages in locale ``code`` may be indexed."""
    return code in indexed_codes()


def noindex_codes() -> tuple[str, ...]:
    """Active locales that are published but kept out of the index."""
    return tuple(lang.code for lang in _lr.active() if not is_indexed(lang.code))


def noindex_hreflangs() -> frozenset[str]:
    """Lower-cased hreflang values (code and BCP-47) of the noindex locales."""
    out: set[str] = set()
    for code in noindex_codes():
        out.update({code.lower(), _lr.get(code).bcp47.lower()})
    return frozenset(out)
