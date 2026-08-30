# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""``inject_word_count`` must set wordCount, not add another copy.

The pass carried a comment saying the key was inserted "if not already
present" — but nothing checked. Postbuild is re-run over built pages, so
each run inserted another ``"wordCount":N,`` right after the ``@type``:

    "@type":"BlogPosting","wordCount":2127,"wordCount":2656,"wordCount":2656,…

17 bytes a run across ~1,600 dated pages, duplicate keys inside one JSON
object, and no fixed point. Sibling of
``test_citations_no_accumulation`` — same defect, same shape, different
pass.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "postbuild"))

from postbuild_lib import seo  # type: ignore[import-not-found]

_BODY = " ".join(f"word{i}" for i in range(120))


def _page(body: str = _BODY) -> str:
    return (
        '<html><head><script type="application/ld+json">'
        '{"@type":"BlogPosting","headline":"x"}'
        f"</script></head><body><main>{body}</main></body></html>"
    )


def _counts(html: str) -> list[str]:
    return re.findall(r'"wordCount":(\d+)', html)


def test_word_count_is_injected() -> None:
    assert _counts(seo.inject_word_count(_page())) == ["120"]


def test_running_twice_does_not_add_a_second_key() -> None:
    once = seo.inject_word_count(_page())
    assert len(_counts(seo.inject_word_count(once))) == 1


def test_repeated_passes_reach_a_fixed_point() -> None:
    out = seo.inject_word_count(_page())
    for _ in range(4):
        out = seo.inject_word_count(out)
    assert out == seo.inject_word_count(out)
    assert len(_counts(out)) == 1


def test_an_already_accumulated_page_heals_to_one_key() -> None:
    html = _page().replace(
        '"@type":"BlogPosting",',
        '"@type":"BlogPosting","wordCount":11,"wordCount":22,"wordCount":33,',
    )
    assert len(_counts(html)) == 3
    assert _counts(seo.inject_word_count(html)) == ["120"]


def test_the_value_tracks_the_body_when_it_grows() -> None:
    """Later passes add content to <main>; the count must follow."""
    first = seo.inject_word_count(_page())
    assert _counts(first) == ["120"]
    grown = first.replace("</main>", " extra words here</main>")
    assert _counts(seo.inject_word_count(grown)) == ["123"]


def test_a_page_with_no_main_is_untouched() -> None:
    html = "<html><head></head><body><p>no main</p></body></html>"
    assert seo.inject_word_count(html) == html
