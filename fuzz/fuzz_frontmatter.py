#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Fuzz the front-matter parser.

Every post is parsed by this before anything else in the build touches it, so
a malformed document must return something the caller can reason about rather
than raise from deep inside the pipeline.
"""

from __future__ import annotations

import sys
from pathlib import Path

import atheris

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

with atheris.instrument_imports():
    from lib._frontmatter import parse_frontmatter


def one_input(data: bytes) -> None:
    fdp = atheris.FuzzedDataProvider(data)
    text = fdp.ConsumeUnicodeNoSurrogates(4096)
    try:
        fm, body = parse_frontmatter(text)
    except (ValueError, KeyError):
        return  # a malformed document may be rejected; it must not crash
    assert isinstance(fm, dict), type(fm)
    assert isinstance(body, str), type(body)


def main() -> None:
    atheris.Setup(sys.argv, one_input)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
