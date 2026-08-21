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


# ── The "leave it exactly as found" guarantees ──────────────────────────
#
# The docstring promises this pass never rewrites what it cannot understand,
# and that it decodes parsed string values only. Each early return below is
# one of those promises. They are also the lines a happy-path test cannot
# reach: CI runs the coverage gate pre-build, so nothing else exercises them
# there, and the gate reported 96% on this module while a local run — where
# a built public/ lets the smoke suite walk the same code — showed 100%.


def test_non_string_scalars_survive_unchanged():
    """Numbers, booleans and null are returned as-is, not stringified.

    `_decode_json_strings` recurses through dicts and lists and unescapes
    strings; everything else falls through untouched. Coercing `42` to `"42"`
    here would silently change the type every consumer reads.
    """
    # The entity is load-bearing: without an `&` anywhere in the block the
    # pass short-circuits before it ever recurses, and the scalar branch goes
    # unexercised while the test still passes.
    payload = {
        "@type": "Article",
        "name": "Payments &amp; Rust",
        "wordCount": 1200,
        "isAccessibleForFree": True,
        "retracted": False,
        "expires": None,
        "ratings": [4, 5.5, None, True],
    }
    out = json.loads(_body(decode_entities_in_jsonld(WRAP.format(json.dumps(payload)))))
    assert out["name"] == "Payments & Rust", "the string value must still decode"
    assert isinstance(out["wordCount"], int)
    assert out["isAccessibleForFree"] is True
    assert out["retracted"] is False
    assert out["expires"] is None
    assert out["ratings"] == [4, 5.5, None, True]


def test_block_without_an_ampersand_is_untouched():
    """No `&` means nothing to decode — the block is returned byte-identical
    rather than re-serialised, so key order and spacing are preserved."""
    original = '{\n  "@type": "Article",\n  "name": "Plain title"\n}'
    html = WRAP.format(original)
    assert decode_entities_in_jsonld(html) == html


def test_unparseable_block_is_left_exactly_as_found():
    """A block that is not JSON is never rewritten. Emitting a 'repaired'
    version of something we could not parse would be worse than the bug."""
    broken = '{"@type": "Article", "name": "A &amp; B",}'  # trailing comma
    html = WRAP.format(broken)
    assert decode_entities_in_jsonld(html) == html


def test_ampersand_that_is_not_an_entity_is_a_no_op():
    """`&` alone is not an entity, so the decode changes nothing and the
    original text is kept rather than re-serialised."""
    original = '{"name": "Rock & Roll"}'
    html = WRAP.format(original)
    assert decode_entities_in_jsonld(html) == html


def test_quot_inside_a_value_does_not_break_the_json():
    """The failure mode the docstring warns about: unescaping the raw block
    would turn `&quot;` into a bare quote and destroy the JSON it was trying
    to fix. Decoding parsed values keeps the document valid."""
    payload = {"name": "He said &quot;hello&quot; &amp; left"}
    out = json.loads(_body(decode_entities_in_jsonld(WRAP.format(json.dumps(payload)))))
    assert out["name"] == 'He said "hello" & left'
