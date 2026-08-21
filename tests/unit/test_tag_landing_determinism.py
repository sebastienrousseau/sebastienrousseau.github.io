"""The tag landings must not depend on Python's per-process hash seed.

`_ingest_post` built its co-occurrence counter by iterating a `set`, whose
order Python randomises per process, and `_render_related_tags` consumed it
with `Counter.most_common()` — which breaks ties by INSERTION order. Tied
co-occurrence counts are the common case in this corpus, so the "related
tags" chips came out in a different order on every build.

That made `./build.sh` non-idempotent and failed the byte-identical rebuild
gate on the locale tag landings (`ar/wusum/…`, `bn/tag/…`) and, downstream,
the locale search indexes built from them.

These tests pin the property directly rather than by rebuilding: feed
counters that carry IDENTICAL counts in DIFFERENT insertion orders, and
require one single rendering.
"""

from __future__ import annotations

import collections

import tag_landing_render as tlr

_NAMES = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot"]


def _taxonomy() -> dict:
    return {n: {"name": n.title(), "category": "ai"} for n in _NAMES}


def _posts() -> dict:
    # Every tag is comfortably over the landing threshold so none is filtered.
    return {n: [("t", "2026-01-01", "s", "e", [], "b", "a")] * 5 for n in _NAMES}


def _counter(order: list[str], count: int = 3) -> collections.Counter[str]:
    """A counter with identical counts, populated in the given order."""
    c: collections.Counter[str] = collections.Counter()
    for n in order:
        c[n] += count
    return c


def test_related_tags_ignore_counter_insertion_order():
    orders = [
        _NAMES,
        list(reversed(_NAMES)),
        [_NAMES[i] for i in (3, 0, 5, 1, 4, 2)],
    ]
    rendered = {
        tlr._render_related_tags(_counter(o), _taxonomy(), "slug", _posts()) for o in orders
    }
    assert len(rendered) == 1, (
        "related-tag chips must not depend on how the counter was populated; "
        f"got {len(rendered)} distinct renderings from {len(orders)} orders"
    )


def test_related_tags_are_ordered_by_count_then_slug():
    counts = collections.Counter({"alpha": 1, "bravo": 5, "charlie": 5, "delta": 2})
    html = tlr._render_related_tags(counts, _taxonomy(), "slug", _posts())
    order = [chunk.split('"')[1] for chunk in html.split("<a href=")[1:]]
    assert order == [
        "/tags/bravo/",
        "/tags/charlie/",
        "/tags/delta/",
        "/tags/alpha/",
    ], f"expected descending count with slug as the tiebreak, got {order}"


def test_related_tags_still_filter_below_threshold():
    """The determinism fix must not quietly widen what gets linked: tags
    without a landing page would 404 and fail the strict-internal audit."""
    posts = _posts()
    posts["bravo"] = []  # no landing page for this one
    html = tlr._render_related_tags(_counter(_NAMES), _taxonomy(), "slug", posts)
    assert "/tags/bravo/" not in html, html
