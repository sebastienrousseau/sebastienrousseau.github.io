"""JSON-LD payloads must carry decoded text, not HTML entities.

A ``<script type="application/ld+json">`` body is not HTML-parsed, so an
entity inside it reaches structured-data consumers literally: a page named
``A &amp; B`` is read as those six characters, not as ``A & B``.

The layouts embed ``"name":"{{title}}"`` inside the JSON block and the
template layer fills variables HTML-escaped — right for the page, wrong here.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "postbuild"))

from postbuild_lib.html_passes import decode_entities_in_jsonld

WRAP = '<script type="application/ld+json">{}</script>'


def _body(html: str) -> str:
    return html.split(">", 1)[1].rsplit("<", 1)[0]


def test_ampersand_entity_is_decoded() -> None:
    out = decode_entities_in_jsonld(WRAP.format('{"name":"A &amp; B"}'))
    assert json.loads(_body(out))["name"] == "A & B"


def test_quote_entity_does_not_break_the_json() -> None:
    """The naive version of this pass is worse than the bug.

    Unescaping the raw block would turn ``&quot;`` into a bare quote and
    produce ``{"n":"say "hi""}`` — invalid JSON, in the name of fixing JSON.
    """
    out = decode_entities_in_jsonld(WRAP.format('{"n":"say &quot;hi&quot;"}'))
    assert json.loads(_body(out))["n"] == 'say "hi"'


def test_unparseable_block_is_left_untouched() -> None:
    src = WRAP.format('{"broken":')
    assert decode_entities_in_jsonld(src) == src


def test_block_without_entities_is_returned_verbatim() -> None:
    src = WRAP.format('{"clean":"no entities"}')
    assert decode_entities_in_jsonld(src) == src


def test_nested_values_are_decoded() -> None:
    src = WRAP.format('{"@graph":[{"name":"X &amp; Y","sub":{"d":"P &amp; Q"}}]}')
    got = json.loads(_body(decode_entities_in_jsonld(src)))
    assert got["@graph"][0]["name"] == "X & Y"
    assert got["@graph"][0]["sub"]["d"] == "P & Q"


def test_non_jsonld_script_is_not_touched() -> None:
    src = '<script type="text/javascript">var a = "x &amp; y";</script>'
    assert decode_entities_in_jsonld(src) == src
