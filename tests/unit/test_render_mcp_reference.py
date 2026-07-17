"""Unit coverage for render_mcp_reference (the generated MCP tool catalog).

The reference page's tool catalog is generated from the captured
``tools/list`` snapshots in ``_data/mcp/``. Cover the contract that keeps it
honest:

* drift: the committed ``_posts/iso20022-mcp-reference.md`` matches what the
  script would generate from the committed captures (and regeneration is
  idempotent);
* completeness: every captured server, and every captured tool of every
  server, appears in the page;
* house style: the generated block ships no em dashes and no inline styles,
  and required/optional parameter flags mirror the captured JSON Schema;
* failure modes: missing markers and uncatalogued snapshot files abort
  instead of silently shipping a partial catalog.

Standalone run: ``python3 -m pytest tests/unit/test_render_mcp_reference.py``
"""

from __future__ import annotations

import json

if __package__ in (None, ""):  # standalone run; under pytest conftest.py wires sys.path
    import _path_bootstrap  # noqa: F401

import pytest
import render_mcp_reference as ref

PAGE_TEXT = ref.PAGE.read_text(encoding="utf-8")


def _generated_block() -> str:
    start = PAGE_TEXT.index(ref.BEGIN)
    end = PAGE_TEXT.index(ref.END) + len(ref.END)
    return PAGE_TEXT[start:end]


def _load(meta: dict) -> dict:
    return json.loads((ref.DATA / meta["file"]).read_text(encoding="utf-8"))


# --- drift: committed page == generated-from-capture --------------------------


def test_committed_catalog_matches_capture_no_drift() -> None:
    assert ref.apply(PAGE_TEXT) == PAGE_TEXT, (
        "committed reference page is stale; run "
        "python3 scripts/generators/render_mcp_reference.py"
    )


def test_check_mode_exits_zero_when_in_sync() -> None:
    assert ref.main(["--check"]) == 0


def test_regeneration_is_idempotent() -> None:
    once = ref.apply(PAGE_TEXT)
    assert ref.apply(once) == once


# --- completeness: every server, every tool -----------------------------------


def test_every_captured_server_appears() -> None:
    block = _generated_block()
    for meta in ref.SERVERS:
        assert f'id="{meta["id"]}"' in block, f"missing section for {meta['pkg']}"
        assert meta["pkg"] in block, f"missing package name {meta['pkg']}"


def test_every_captured_tool_appears_with_anchor() -> None:
    block = _generated_block()
    total = 0
    for meta in ref.SERVERS:
        for tool in _load(meta)["tools"]:
            anchor = f'id="{meta["id"]}-{tool["name"]}"'
            assert anchor in block, f"missing tool {meta['pkg']}/{tool['name']}"
            total += 1
    # The suite currently captures 9 servers; a wholesale drop would still
    # pass the per-tool loop, so pin a sane floor.
    assert total >= 80
    assert f"{len(ref.SERVERS)} servers · {total} tools" in block


def test_required_and_optional_flags_mirror_schema() -> None:
    """Spot-check against the gateway capture: describe(message_type) is
    required; search(query) is optional."""
    block = _generated_block()
    describe = block.split('id="gateway-describe"', 1)[1].split("</details>", 1)[0]
    assert "<td><code>message_type</code></td>" in describe
    assert "ref-req-required" in describe
    search = block.split('id="gateway-search"', 1)[1].split("</details>", 1)[0]
    assert "<td><code>query</code></td>" in search
    assert "ref-req-optional" in search


# --- house style ---------------------------------------------------------------


def test_generated_block_has_no_em_dashes_or_inline_styles() -> None:
    block = _generated_block()
    assert "—" not in block
    assert "style=" not in block


def test_whole_page_has_no_em_dashes() -> None:
    assert "—" not in PAGE_TEXT


def test_render_normalises_em_dashes_from_captures() -> None:
    assert ref._strip_em_dashes("a — b—c") == "a - b-c"


# --- failure modes -------------------------------------------------------------


def test_missing_markers_abort() -> None:
    with pytest.raises(SystemExit):
        ref.apply("<p>no markers here</p>")


def test_uncatalogued_snapshot_aborts(tmp_path, monkeypatch) -> None:
    """A capture landing in _data/mcp/ without a SERVERS entry must abort,
    never ship a catalog that silently omits a server."""
    data = tmp_path / "mcp"
    data.mkdir()
    for meta in ref.SERVERS:
        src = ref.DATA / meta["file"]
        (data / meta["file"]).write_text(src.read_text(encoding="utf-8"))
    (data / "newserver-mcp.tools.json").write_text('{"_meta": {}, "tools": []}')
    monkeypatch.setattr(ref, "DATA", data)
    with pytest.raises(SystemExit):
        ref.render_catalog()


def test_missing_capture_aborts(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(ref, "DATA", tmp_path)
    with pytest.raises(SystemExit):
        ref.render_catalog()
