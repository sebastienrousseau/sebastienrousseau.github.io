"""The hreflang strip must match the links the same pass emits.

Three passes strip hreflang before re-emitting it, and each had grown its
own copy of the regex. Two used ``[^/]*/>``, which can never match a real
tag — every ``https://`` href contains a slash — so the strip silently did
nothing and the whole cluster was appended again on every run. One copy
was fixed in place; ``postbuild_transforms`` kept the broken form, which
is how topic and locale-home pages reached 435 hreflang links: twelve
duplicate clusters, about 3.8 KB added per run, with no fixed point.

The regex now lives in one place. These tests pin the property that
actually matters — a stripper must match its own output — rather than the
spelling of the pattern.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "postbuild"))

from postbuild_lib.hreflang import HREFLANG_LINK_RE  # type: ignore[import-not-found]

_EMITTED = (
    '<link rel="alternate" hreflang="en" '
    'href="https://sebastienrousseau.com/topics/applied-ai-banking/" />'
)


def test_the_regex_matches_the_tag_the_passes_emit() -> None:
    """The exact regression: an href full of slashes must still match."""
    assert HREFLANG_LINK_RE.fullmatch(_EMITTED)


def test_stripping_is_complete_so_a_cluster_cannot_double() -> None:
    head = "<head>" + _EMITTED * 36 + "</head>"
    assert HREFLANG_LINK_RE.sub("", head) == "<head></head>"


def test_html5_self_close_also_matches() -> None:
    html5 = _EMITTED.replace(" />", ">")
    assert HREFLANG_LINK_RE.fullmatch(html5)


def test_attribute_order_does_not_matter() -> None:
    reordered = (
        '<link hreflang="ar" rel="alternate" '
        'href="https://sebastienrousseau.com/ar/mawadi/applied-ai-banking/" />'
    )
    assert HREFLANG_LINK_RE.fullmatch(reordered)


def test_unrelated_links_are_left_alone() -> None:
    keep = (
        '<link rel="stylesheet" href="/_csp/a.css" />'
        '<link rel="canonical" href="https://sebastienrousseau.com/x/" />'
    )
    assert HREFLANG_LINK_RE.sub("", keep) == keep


def test_the_old_broken_pattern_is_gone_from_the_transforms() -> None:
    """A fourth copy must not creep back in."""
    src = (ROOT / "scripts" / "postbuild" / "postbuild_transforms.py").read_text()
    assert "[^/]*/>" not in src


def test_topic_and_home_transforms_reach_a_fixed_point() -> None:
    """Re-running the injector must not grow the head."""
    import postbuild_transforms as pt  # type: ignore[import-not-found]

    page = "<html><head><title>x</title></head><body></body></html>"
    once = pt._topic_hreflang(page, "applied-ai-banking")
    twice = pt._topic_hreflang(once, "applied-ai-banking")
    assert twice == once
    assert len(re.findall(r"hreflang=", twice)) == len(re.findall(r"hreflang=", once))

    h1 = pt._home_hreflang(page)
    assert pt._home_hreflang(h1) == h1
