#!/usr/bin/env python3
"""Fuzz the slug deriver.

derive_slug turns a translated title into a URL. A title is author-supplied
text in 34 scripts, and its output becomes a filename and a live URL, so the
invariants worth holding are that it never raises and never emits something
that cannot be a path segment.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import atheris

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

with atheris.instrument_imports():
    from lib._romanise import derive_slug, romanise, slugify

_SAFE = re.compile(r"^[a-z0-9-]*$")
_LOCALES = ("ar", "he", "hi", "bn", "ja", "zh-hans", "zh-hant", "th", "ko", "ru", "el", "fr")


def one_input(data: bytes) -> None:
    fdp = atheris.FuzzedDataProvider(data)
    locale = _LOCALES[fdp.ConsumeIntInRange(0, len(_LOCALES) - 1)]
    title = fdp.ConsumeUnicodeNoSurrogates(512)

    romanise(title, locale)

    slug = slugify(title, locale)
    assert _SAFE.match(slug), f"unsafe slug {slug!r} from {title!r} ({locale})"
    assert "--" not in slug, f"double dash in {slug!r}"
    assert not slug.endswith("-"), f"trailing dash in {slug!r}"

    # An empty result is legitimate: a title with nothing romanisable in it
    # has no slug, and the caller rejects it rather than building "…--tw".
    full = derive_slug(title, locale, "2026")
    assert _SAFE.match(full), f"unsafe derived slug {full!r}"
    assert len(full) <= 100, f"slug too long ({len(full)}): {full!r}"
    assert not full.startswith("-"), f"leading dash in {full!r}"
    assert "--" not in full, f"double dash in {full!r}"


def main() -> None:
    atheris.Setup(sys.argv, one_input)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
