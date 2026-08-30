# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Regression: quote-agnostic frontmatter field extraction (P1-1).

The ``_*_FM_RE`` field regexes in ``listing_common`` only strip a
*double*-quote pair. The ``vi`` corpus writes SINGLE-quoted YAML values
(``banner: 'https://…webp'``, ``title: 'Bitcoin…'``), so the captured
value used to keep its surrounding apostrophes — rendering
``<img src="'https://…webp'">`` (image 404) and literal ``&#x27;`` quote
entities in card titles on ``public/vi/the/<tag>/index.html``.

These pin ``_strip_fm_quotes`` and the two ``_locale_post_card_fields``
copies (listing_common + tag_landing_render, the latter is what
build_tag_landings uses to localise per-tag landing cards) across the
four shapes that matter:

* single-quoted   → surrounding apostrophes stripped
* double-quoted   → unchanged (regex already handled it)
* unquoted        → unchanged
* double-quoted value containing an apostrophe → apostrophe preserved
"""

from __future__ import annotations

from pathlib import Path

import listing_common as lc
import tag_landing_render as tlr

# --- _strip_fm_quotes ------------------------------------------------------


def test_strip_fm_quotes_single_quoted_value() -> None:
    assert lc._strip_fm_quotes("'https://cloudcdn.pro/x.webp'") == ("https://cloudcdn.pro/x.webp")
    assert lc._strip_fm_quotes("'Bitcoin: A Peer-to-Peer System'") == (
        "Bitcoin: A Peer-to-Peer System"
    )


def test_strip_fm_quotes_double_quoted_value() -> None:
    # A double-quoted value that the regex hasn't already peeled still
    # loses exactly one surrounding pair.
    assert lc._strip_fm_quotes('"already double"') == "already double"


def test_strip_fm_quotes_unquoted_value_unchanged() -> None:
    assert lc._strip_fm_quotes("Bitcoin standard") == "Bitcoin standard"


def test_strip_fm_quotes_preserves_internal_apostrophe() -> None:
    # This is the string the double-quote regex yields for
    # ``title: "Bitcoin's year in review"``. First/last chars are B/w,
    # so no pair is peeled and the apostrophe must survive.
    assert lc._strip_fm_quotes("Bitcoin's year in review") == ("Bitcoin's year in review")


def test_strip_fm_quotes_leaves_unmatched_leading_quote() -> None:
    # Only a *matching* pair is peeled: a value that starts (but doesn't
    # end) with a quote keeps it.
    assert lc._strip_fm_quotes("'tis the season") == "'tis the season"


def _write_post(tmp: Path, body: str) -> Path:
    p = tmp / "2018-01-24-example.md"
    p.write_text(body, encoding="utf-8")
    return p


_SINGLE_QUOTED = (
    "---\n"
    "title: 'Bitcoin: A Peer-to-Peer System'\n"
    "excerpt: 'A short single-quoted excerpt'\n"
    "banner: 'https://cloudcdn.pro/stocks/images/x.webp'\n"
    "---\n"
    "body\n"
)

_DOUBLE_QUOTED_APOSTROPHE = (
    "---\n"
    'title: "Bitcoin\'s year in review"\n'
    'excerpt: "It\'s complicated"\n'
    'banner: "https://cloudcdn.pro/stocks/images/y.webp"\n'
    "---\n"
    "body\n"
)


def test_listing_common_extracts_single_quoted_cleanly(tmp_path: Path) -> None:
    path = _write_post(tmp_path, _SINGLE_QUOTED)
    _stem, title, excerpt, banner = lc._locale_post_card_fields(path)
    assert title == "Bitcoin: A Peer-to-Peer System"
    assert excerpt == "A short single-quoted excerpt"
    assert banner == "https://cloudcdn.pro/stocks/images/x.webp"
    # No stray surrounding quotes that would 404 the <img src> / show &#x27;.
    assert "'" not in banner
    assert not title.startswith("'") and not title.endswith("'")


def test_tag_landing_render_extracts_single_quoted_cleanly(tmp_path: Path) -> None:
    # This copy is the one build_tag_landings imports to localise per-tag
    # landing cards — the direct source of the vi <img src="'…'"> defect.
    path = _write_post(tmp_path, _SINGLE_QUOTED)
    _stem, title, excerpt, banner = tlr._locale_post_card_fields(path)
    assert banner == "https://cloudcdn.pro/stocks/images/x.webp"
    assert title == "Bitcoin: A Peer-to-Peer System"
    assert excerpt == "A short single-quoted excerpt"


def test_double_quoted_with_apostrophe_preserved(tmp_path: Path) -> None:
    path = _write_post(tmp_path, _DOUBLE_QUOTED_APOSTROPHE)
    for extractor in (lc._locale_post_card_fields, tlr._locale_post_card_fields):
        _stem, title, excerpt, banner = extractor(path)
        assert title == "Bitcoin's year in review", extractor
        assert excerpt == "It's complicated", extractor
        assert banner == "https://cloudcdn.pro/stocks/images/y.webp", extractor
