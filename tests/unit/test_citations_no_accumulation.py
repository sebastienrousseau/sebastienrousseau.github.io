"""``inject_citations`` must set the citation array, not append another.

Postbuild is re-run over an already-built tree — by the builder smoke
tests, and by anyone re-running ./build.sh without wiping public/. The
pass inserted ``,"citation":[…]`` before the ``"speakable"`` key with no
check for one already being there, so every run added a copy. Measured on
a dated article across consecutive runs: 9 -> 10 -> 11 -> 12 arrays,
about 150 bytes each, leaving duplicate keys inside a single JSON object
and no fixed point.

Its sibling ``inject_sources_list`` already guards on the marker it
writes. These tests pin the same property here, plus the healing that a
guard-and-return would not give: a page that already accumulated copies
must come back to exactly one.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "postbuild"))

from postbuild_lib import citations  # type: ignore[import-not-found]

# nist.gov is in CITATION_AUTHORITIES; example.com is not.
_CITED = "https://www.nist.gov/publications/some-standard"
_UNCITED = "https://example.com/marketing"


def _page(*urls: str) -> str:
    links = "".join(f'<a href="{u}" rel="external">ref</a>' for u in urls or (_CITED,))
    return (
        '<html><head><script type="application/ld+json">'
        '{"@type":"BlogPosting","headline":"x","speakable":{"@type":"SpeakableSpecification"}}'
        f'</script></head><body><main><div class="wrap">{links}</div></main></body></html>'
    )


def _count(html: str) -> int:
    return html.count('"citation":')


def test_a_citation_array_is_added() -> None:
    out = citations.inject_citations(_page())
    assert _count(out) == 1
    assert _CITED in out


def test_running_twice_does_not_add_a_second_array() -> None:
    once = citations.inject_citations(_page())
    twice = citations.inject_citations(once)
    assert _count(twice) == 1


def test_repeated_passes_reach_a_fixed_point() -> None:
    out = citations.inject_citations(_page())
    for _ in range(4):
        out = citations.inject_citations(out)
    assert out == citations.inject_citations(out)
    assert _count(out) == 1


def test_an_already_accumulated_page_heals_to_one_array() -> None:
    """A tree built before the fix must converge, not stay broken."""
    html = _page()
    for _ in range(6):  # simulate the old append-every-run behaviour
        html = re.sub(
            r'(,"speakable":)',
            ',"citation":[{"@type":"CreativeWork","url":"' + _CITED + '"}]' + r"\1",
            html,
            count=1,
        )
    assert _count(html) == 6
    assert _count(citations.inject_citations(html)) == 1


def test_the_array_tracks_the_body_when_links_change() -> None:
    """Replacing, not appending, means a reworked article stays accurate."""
    other = "https://www.iso.org/standard/12345.html"
    first = citations.inject_citations(_page(_CITED))
    assert _CITED in first
    # The same page, its reference swapped by an edit upstream.
    reworked = first.replace(_CITED, other)
    out = citations.inject_citations(reworked)
    assert _count(out) == 1
    assert other in out


def test_a_page_with_no_authoritative_links_gets_no_array() -> None:
    out = citations.inject_citations(_page(_UNCITED))
    assert _count(out) == 0


def test_a_non_blogposting_page_is_untouched() -> None:
    html = "<html><head></head><body><main>no jsonld</main></body></html>"
    assert citations.inject_citations(html) == html
