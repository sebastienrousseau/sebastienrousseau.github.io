"""Unit coverage for build_iso20022_mcp (+ the shared _swap_into_shell it
uses from build_case_studies).

The generator forks the built /articles/ shell into the /iso20022-mcp/ hub.
Cover the three failure classes a review found there:

* the full swap pipeline against a minimal fake shell (hub metadata in,
  articles CollectionPage / hreflang / share-icon metadata out);
* anti-silent-no-op behaviour — a shell missing an anchor must abort the
  build (SystemExit) instead of shipping /articles metadata;
* replacement-template injection — body/title text containing ``\\g<0>`` or
  lone backslashes must land verbatim, never be re-interpreted by re.sub.

Standalone run: ``python3 tests/unit/test_build_iso20022_mcp.py``
(or ``python3 -m pytest tests/unit/test_build_iso20022_mcp.py``).
"""

from __future__ import annotations

import tempfile
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]

if __package__ in (None, ""):  # standalone run; under pytest conftest.py wires sys.path
    import _path_bootstrap

    _path_bootstrap.ensure()

import build_case_studies as cs
import build_iso20022_mcp as mcp
import pytest

# --- fixtures ----------------------------------------------------------------


def _fake_shell() -> str:
    """A minimal /articles/ shell carrying every anchor the generator swaps:
    head metas, hreflang alternates, primary nav, language switcher, the
    <main> content wrap, and the articles CollectionPage JSON-LD block."""
    return """<!DOCTYPE html>
<html lang="en-GB">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
    <title>Articles</title>
    <meta name="description" content="Articles listing description. Page 1 of 4.">
    <meta property="og:title" content="Articles">
    <meta property="og:description" content="Articles listing description. Page 1 of 4.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://sebastienrousseau.com/articles/">
    <meta property="og:image" content="https://cloudcdn.pro/clients/common/images/buttons/x-black.svg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="Discover How Technology Is Changing Banking and Finance">
    <meta name="twitter:description" content="Articles listing description. Page 1 of 4.">
    <meta name="twitter:image" content="https://cloudcdn.pro/clients/common/images/buttons/x-black.svg">
    <link rel="canonical" href="https://sebastienrousseau.com/articles/">
    <link rel="alternate" hreflang="en" href="https://sebastienrousseau.com/articles/" />
    <link rel="alternate" hreflang="fr" href="https://sebastienrousseau.com/fr/articles/" />
    <link rel="alternate" hreflang="x-default" href="https://sebastienrousseau.com/articles/" />
    <meta name="theme-color" content="#fbfbfd" media="(prefers-color-scheme: light)" />
    <meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)" />
  </head>
  <body>
    <nav><ul class="ap-menu"><li><a href="/articles/index.html" aria-current="page" class="active">Articles</a></li></ul></nav>
    <div class="ap-lang-menu" role="menu">
      <a class="ap-lang-item" href="/articles/" data-lang="en" role="menuitem">English</a>
      <a class="ap-lang-item" href="/fr/articles/" data-lang="fr" role="menuitem">Français</a>
    </div>
    <main id="main" class="content ap-section">
      <div class="wrap articles-wrap"><p>OLD LISTING BODY</p></div>
    </main>
    <footer>footer chrome</footer>
    <script type="application/ld+json">
{"@context":"https://schema.org","@graph":[{"@type":"CollectionPage","name":"Discover How Technology Is Changing Banking and Finance","url":"https://sebastienrousseau.com/articles"},{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://sebastienrousseau.com/"},{"@type":"ListItem","position":2,"name":"Discover How Technology Is Changing Banking and Finance","item":"https://sebastienrousseau.com/articles"}]}]}
    </script>
  </body>
</html>
"""


def _run_build(shell_text: str, schemas_src: Path | None = None) -> str:
    """Run mcp.main() against ``shell_text`` in a temp tree, returning the
    written page. Restores the module's real paths afterwards.

    ``schemas_src`` overrides the captured tool-schema snapshot the schema
    viewer renders from (pass a missing path to exercise the graceful skip);
    by default the committed ``_data/mcp/tool_schemas.json`` is used."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        shell_path = tmp_path / "articles" / "index.html"
        shell_path.parent.mkdir(parents=True)
        shell_path.write_text(shell_text, encoding="utf-8")
        out_path = tmp_path / "iso20022-mcp" / "index.html"
        old_shell, old_out = mcp.SHELL_SRC, mcp.OUT
        old_schemas = mcp.SCHEMAS_SRC
        mcp.SHELL_SRC, mcp.OUT = shell_path, out_path
        if schemas_src is not None:
            mcp.SCHEMAS_SRC = schemas_src
        try:
            rc = mcp.main()
            assert rc == 0
            return out_path.read_text(encoding="utf-8")
        finally:
            mcp.SHELL_SRC, mcp.OUT = old_shell, old_out
            mcp.SCHEMAS_SRC = old_schemas


# --- (a) full page build against the fake shell ------------------------------


def test_full_build_swaps_hub_metadata_in() -> None:
    out = _run_build(_fake_shell())
    assert f"<title>{mcp.C['meta_title']}</title>" in out
    assert 'content="' + mcp.C["meta_description"].replace('"', "&quot;") in out
    assert '<link rel="canonical" href="https://sebastienrousseau.com/iso20022-mcp"' in out
    # Social card = the hub hero photo, large-image card.
    assert f'<meta property="og:image" content="{mcp.HERO_OG_IMAGE}"' in out
    assert f'<meta name="twitter:image" content="{mcp.HERO_OG_IMAGE}">' in out
    assert '<meta name="twitter:card" content="summary_large_image">' in out
    assert f'<meta name="twitter:title" content="{mcp.C["meta_title"]}">' in out
    assert "x-black.svg" not in out.split("</head>")[0]  # no share icon in head


def test_full_build_nav_has_five_top_items_with_dropdowns() -> None:
    out = _run_build(_fake_shell())
    # Nav ends at the </ul> directly before </nav> (nested ap-sub lists).
    nav = out.split('<ul class="ap-menu">', 1)[1].split("</ul></nav>", 1)[0]
    # 5 top-level items; 4 carry a dropdown (Articles is a plain link).
    assert nav.count('<li class="has-sub">') == 4
    assert nav.count('class="ap-sub"') == 4
    for label in (
        "About", "Articles", "Library", "Research", "Suite",
    ):
        assert f">{label}</a>" in nav
    # Each dropdown carries a disclosure button wired to its panel id.
    for item_id, label in (
        ("about", "About"),
        ("library", "Library"),
        ("research", "Research"),
        ("suite", "Suite"),
    ):
        assert (
            f'<button type="button" class="ap-sub-toggle" aria-expanded="false" '
            f'aria-controls="sub-{item_id}" aria-label="Toggle {label} submenu">'
        ) in nav
        assert f'<ul id="sub-{item_id}" class="ap-sub">' in nav
    # Sub-items present with their canonical hrefs. Whitepapers & Reports
    # deliberately targets the canonical /research/ hub, not the /papers/
    # redirect page.
    for href, label in (
        ("/trust/index.html", "Trust &amp; Compliance"),
        ("/speaking/index.html", "Public Speaking"),
        ("/contact/index.html", "Contact"),
        ("/topics/index.html", "Browse by Topic"),
        ("/projects/index.html", "Open Source Projects"),
        ("/playlists/index.html", "Playlists"),
        ("/research/index.html", "Whitepapers &amp; Reports"),
        ("/case-studies/index.html", "Real-World Case Studies"),
        ("/iso20022-mcp/index.html", "ISO 20022 MCP Suite"),
        ("/iso20022-mcp-docs/index.html", "Documentation"),
        ("/iso20022-mcp-reference/index.html", "API Reference"),
        ("/iso20022-mcp-recipes/index.html", "Integration Recipes"),
    ):
        assert f'<li><a href="{href}">{label}</a></li>' in nav
    # No nav link points at the /papers/ redirect page.
    assert "/papers/" not in nav
    # F-shape ordering: About leftmost, Suite rightmost.
    assert nav.index(">About</a>") < nav.index(">Articles</a>") < nav.index(
        ">Library</a>") < nav.index(">Research</a>") < nav.index(">Suite</a>")
    # No baked active marker — postbuild's inject_nav_active marks the
    # /iso20022-mcp/ sub-item on the final page.
    assert "aria-current" not in nav


def test_full_build_replaces_collectionpage_jsonld() -> None:
    out = _run_build(_fake_shell())
    assert "CollectionPage" not in out
    assert '"@type":"WebPage"' in out
    assert '"@type":"BreadcrumbList"' in out
    assert '"name":"ISO 20022 MCP Suite"' in out
    # No JSON-LD may still point at the articles listing.
    assert '"url":"https://sebastienrousseau.com/articles"' not in out


def test_full_build_is_en_only_no_hreflang() -> None:
    out = _run_build(_fake_shell())
    assert "hreflang=" not in out
    # Switcher degrades to locale homepages, not the /articles forks.
    assert '<a class="ap-lang-item" href="/" data-lang="en"' in out
    assert '<a class="ap-lang-item" href="/fr/" data-lang="fr"' in out
    assert 'href="/fr/articles/"' not in out


def test_full_build_head_hygiene_and_copy() -> None:
    out = _run_build(_fake_shell())
    assert out.count('<meta name="description"') == 1
    assert out.count('<meta name="viewport"') == 1
    body = out.split("<body", 1)[1]
    assert "`" not in body  # no literal backticks in rendered copy
    assert "Nine servers, one payment lifecycle." in out
    assert "Eight" not in out
    # CLS guard: dimensions match the CSS aspect-ratio (16/6).
    assert 'class="mcp-band-img" width="1920" height="720"' in out
    # Commands are <code>, arrows are hidden from AT, CTAs carry card names.
    assert '<code class="spk-mono">' in out
    assert '<span class="spk-arw" aria-hidden="true">' in out
    assert 'aria-label="Read the docs: The gateway"' in out


def test_hero_terminal_replaces_hero_image() -> None:
    """The hero media slot is the animated terminal session, not a photo."""
    out = _run_build(_fake_shell())
    # No hero webp remains (the og:image constant is head-only).
    assert 'class="mcp-hero-img"' not in out
    body = out.split("<body", 1)[1]
    assert "modern-corporate-office-with-technological-displays" not in body
    # Split hero: the terminal is a hero-grid cell (above the fold), not a
    # standalone media section below the hero.
    assert 'class="mcp-hero-media"' not in body
    header = body.split('<header class="spk-hero"', 1)[1].split("</header>", 1)[0]
    assert '<div class="mcp-hero-term"><figure class="mcp-term">' in header
    # Order inside the hero: copy + CTA row, then terminal, then stats band.
    assert (
        header.index('class="spk-cta-row"')
        < header.index('class="mcp-hero-term"')
        < header.index('class="spk-microproof"')
    )
    # Terminal chrome + real selectable session text.
    hero = body.split('<figure class="mcp-term">', 1)[1].split("</figure>", 1)[0]
    assert '<pre class="mcp-term-body">' in hero
    assert (
        'claude mcp add iso20022 -- uvx --from &quot;iso20022-mcp[all]&quot; '
        "iso20022-mcp" in hero
    )
    assert "schema-valid pain.001.001.03 returned" in hero
    # Typed lines carry the ch-count timing classes documented in
    # gen_layouts.SPEAKING_MCP_HUB_CSS (72ch / 17ch / 83ch).
    for cls in ("mcp-tl-t1", "mcp-tl-t2", "mcp-tl-t4"):
        assert cls in hero
    # The ch counts themselves stay in sync with the emitted text.
    for (_, timing, glyph, text), n in zip(
        mcp._TERM_LINES, (72, 17, 20, 8, 83, 52, 39), strict=True
    ):
        if "mcp-tl-typed" in timing:
            assert len(glyph + text) == n


# --- enterprise sections: flow / security / clients / tabs / schemas ---------


def test_flow_has_four_steps_with_one_approval_gate() -> None:
    out = _run_build(_fake_shell())
    flow = out.split('<ol class="mcp-flow">', 1)[1].split("</ol>", 1)[0]
    assert flow.count('<li class="mcp-step') == 4
    assert flow.count("mcp-step-gate") == 1
    assert flow.count('<span class="mcp-gate-badge">Approval wall</span>') == 1
    # The dispatch stage stays out of the servers' hands.
    assert "never move money" in flow
    assert "A human approves." in flow


def test_security_strip_has_four_verified_claims() -> None:
    out = _run_build(_fake_shell())
    strip = out.split('<div class="mcp-sec">', 1)[1].split("</div></div></section>", 1)[0]
    assert strip.count('<div class="mcp-sec-cell">') == 4
    assert "Zero data retention." in strip
    assert "no outbound network calls" in strip
    assert "Apache-2.0" in strip
    assert "100% branch-tested." in strip


def test_clients_grid_covers_stdio_and_remote_accurately() -> None:
    out = _run_build(_fake_shell())
    sec = out.split('id="mcp-clients"', 1)[1].split("</section>", 1)[0]
    for name in (
        "Claude Code", "Claude Desktop", "Cursor", "Windsurf",
        "VS Code + GitHub Copilot", "Google Gemini CLI",
        "OpenAI Codex CLI", "OpenAI", "Microsoft Copilot Studio",
        "Zapier MCP",
    ):
        assert f"<h3>{name}</h3>" in sec
    # Each documented stdio config carries the proven uvx entry.
    assert sec.count("&quot;--from&quot;, &quot;iso20022-mcp[all]&quot;") >= 5
    # VS Code's shape differs: top-level "servers", not "mcpServers".
    assert "&quot;servers&quot;:" in sec
    assert sec.count("&quot;mcpServers&quot;:") >= 3
    # Remote-first platforms get a sentence, never a fake local command.
    zapier = sec.split("<h3>Zapier MCP</h3>", 1)[1].split("</div>", 1)[0]
    assert "mcp-code" not in zapier
    copilot = sec.split("<h3>Microsoft Copilot Studio</h3>", 1)[1].split("</div>", 1)[0]
    assert "mcp-code" not in copilot
    # OpenAI is framed both ways: local stdio via the Agents SDK class,
    # remote-only for ChatGPT connectors.
    assert "MCPServerStdio" in sec
    assert "Streamable HTTP" in sec
    # Every card that shows a config gets its own copy button wired to
    # that card's code element (7 stdio + the OpenAI Agents SDK snippet).
    for slug in (
        "claude-code", "claude-desktop", "cursor", "windsurf",
        "vscode", "gemini", "codex", "openai",
    ):
        assert f'data-copy="#mcp-code-client-{slug}"' in sec
    assert sec.count("data-copy=") == 8
    # Codex CLI: the documented ~/.codex/config.toml table shape
    # ([mcp_servers.<name>] with command/args), verified against OpenAI's
    # official Codex MCP docs on 2026-07-16.
    codex = sec.split("<h3>OpenAI Codex CLI</h3>", 1)[1].split("</div>", 1)[0]
    assert "[mcp_servers.iso20022]" in codex
    assert "command = &quot;uvx&quot;" in codex
    assert "args = [&quot;--from&quot;, &quot;iso20022-mcp[all]&quot;" in codex
    assert "~/.codex/config.toml" in codex


def test_install_tabs_are_css_only_radio_pattern() -> None:
    out = _run_build(_fake_shell())
    tabs = out.split('<div class="mcp-tabs">', 1)[1].split("</section>", 1)[0]
    assert tabs.count('name="mcp-install-tab"') == 6
    assert tabs.count("checked") == 1
    for tid in ("uvx", "pip", "json", "cursor", "vscode", "agents"):
        assert f'id="mcp-tab-{tid}"' in tabs
        assert f'<label for="mcp-tab-{tid}">' in tabs
        assert f'id="mcp-panel-{tid}"' in tabs
        # Copy buttons ride main.js's [data-copy] delegate (CSP-safe).
        assert f'data-copy="#mcp-code-{tid}"' in tabs
    # Only verified shapes: the Agents SDK tab carries the documented
    # MCPServerStdio snippet, never an invented CLI command.
    assert "MCPServerStdio" in tabs
    # Radios precede labels and panels so the CSS ~ combinator can reach them.
    assert tabs.find('id="mcp-tab-uvx"') < tabs.find('<div class="mcp-tab-labels">')
    assert tabs.find('<div class="mcp-tab-labels">') < tabs.find('id="mcp-panel-uvx"')


def test_schema_viewer_renders_captured_tools() -> None:
    out = _run_build(_fake_shell())
    sec = out.split('id="mcp-schemas"', 1)[1].split("</section>", 1)[0]
    # Canonical .qa accordion rows with the hub's schema modifier.
    assert sec.count('<details class="qa-item mcp-schema">') == 7
    assert '<div class="qa-list mcp-schemas">' in sec
    # The canonical marker is CSS-generated; no hand-rolled icon span.
    assert "spk-ic" not in sec
    for tool in (
        "search", "list_families", "list_servers", "describe",
        "validate", "generate", "parse",
    ):
        assert f'<code class="spk-mono">{tool}</code>' in sec
    # Input properties come from the live capture, not hand-written copy.
    assert '<code class="spk-mono">message_type</code>' in sec
    assert "read-only, idempotent and closed-world" in sec


def test_schema_viewer_skips_gracefully_when_snapshot_missing() -> None:
    out = _run_build(_fake_shell(), schemas_src=Path("/nonexistent/tool_schemas.json"))
    assert 'id="mcp-schemas"' not in out
    # The rest of the page still builds.
    assert 'id="mcp-clients"' in out


def test_committed_tool_schema_snapshot_is_sound() -> None:
    """The committed tools/list capture stays parseable and read-only."""
    import json

    data = json.loads(
        (_ROOT / "_data" / "mcp" / "tool_schemas.json").read_text(encoding="utf-8")
    )
    tools = data["tools"]
    assert [t["name"] for t in tools] == [
        "search", "list_families", "list_servers", "describe",
        "validate", "generate", "parse",
    ]
    for t in tools:
        assert t["description"]
        assert t["inputSchema"]["type"] == "object"
        ann = t["annotations"]
        assert ann["readOnlyHint"] is True
        assert ann["destructiveHint"] is False


def test_what_section_has_outcome_card() -> None:
    out = _run_build(_fake_shell())
    sec = out.split('id="mcp-what"', 1)[1].split("</section>", 1)[0]
    assert sec.count('<div class="spk-path">') == 4
    assert "Build the next era of your enterprise." in sec
    assert ">THE OUTCOME</span>" in sec
    assert sec.count('<span class="mcp-icon"') == 4


def test_start_has_four_steps_with_human_loop() -> None:
    out = _run_build(_fake_shell())
    sec = out.split('id="mcp-start"', 1)[1].split("</section>", 1)[0]
    assert sec.count('<div class="spk-path">') == 4
    assert "Keep humans in the loop." in sec
    assert "never moves money directly" in sec
    assert "final human approval and settlement" in sec


def test_clock_band_uses_tall_crop() -> None:
    out = _run_build(_fake_shell())
    assert 'class="mcp-band-img-tall" width="1920" height="1080"' in out
    assert "ocean-ng-L0xOtAnv94Y-1920.webp" in out
    # The other band keeps the standard 16/6 strip.
    assert 'class="mcp-band-img" width="1920" height="720"' in out


def test_safety_section_has_four_cards_from_verified_copy() -> None:
    out = _run_build(_fake_shell())
    sec = out.split('id="mcp-safety"', 1)[1].split("</section>", 1)[0]
    assert sec.count('<div class="spk-path">') == 4
    for eyebrow in ("VALIDATED", "GUARDED", "READ-ONLY", "OPEN"):
        assert f">{eyebrow}</span>" in sec
    # The fourth card restates the docs page's verified read-only claim.
    assert "Read-only where it counts." in sec
    assert "read-only, idempotent and closed-world" in sec
    # Every card carries its icon slot (check / shield / eye / lock).
    assert sec.count('<span class="mcp-icon"') == 4


def test_body_ships_no_inline_styles_or_em_dashes() -> None:
    out = _run_build(_fake_shell())
    body = out.split("<body", 1)[1]
    assert "style=" not in body  # strict CSP: zero inline styles
    assert "—" not in body  # no em dashes anywhere in rendered copy


# --- benchmark sections: audience lens / board / regulators / receipts -------


def test_audience_selector_and_lens_tags() -> None:
    """PR #338 pattern on the hub: the Read as… control ships [hidden]
    for JS-off, and every content section carries data-audience tags."""
    out = _run_build(_fake_shell())
    body = out.split("<body", 1)[1]
    # The control: hidden by default, four lenses, a polite status region.
    assert '<section class="read-as"' in body
    assert "hidden>" in body.split('<section class="read-as"', 1)[1][:200]
    for lens in ("", "boards", "engineers", "regulators"):
        assert f'data-read="{lens}"' in body
    assert 'data-read-status role="status" aria-live="polite"' in body
    # Every AUDIENCES entry that renders is stamped; the hero header and
    # the selector itself stay untagged.
    hub = body.split('<div class="speaking-page iso20022-mcp-page">', 1)[1]
    import re

    tagged = re.findall(r'<section data-audience="([^"]+)"', hub)
    # All rendered content sections carry tags with only known lenses.
    assert len(tagged) >= 18
    for tags in tagged:
        assert set(tags.split()) <= {"boards", "engineers", "regulators"}
    # The mapping itself stays lens-mapped per the competitive analysis.
    assert mcp.AUDIENCES["mcp-flow"] == "boards regulators"
    assert mcp.AUDIENCES["mcp-security"] == "boards regulators"
    assert mcp.AUDIENCES["mcp-install"] == "engineers"
    assert mcp.AUDIENCES["mcp-clients"] == "engineers"
    assert mcp.AUDIENCES["mcp-regulators"] == "regulators"
    assert '<header class="spk-hero" id="spk-top">' in hub  # untagged hero


def test_board_section_is_qualitative_and_first_after_hero() -> None:
    out = _run_build(_fake_shell())
    sec = out.split('id="mcp-board"', 1)[1].split("</section>", 1)[0]
    assert sec.count('<div class="spk-path">') == 3
    for eyebrow in ("WHAT IT COSTS", "WHAT IT RISKS", "WHAT IT REPLACES"):
        assert f">{eyebrow}</span>" in sec
    assert "Free. Apache-2.0." in sec
    assert "Money never moves without a human." in sec
    assert "Bespoke ISO 20022 integration work." in sec
    # Qualitative only: no invented savings figures anywhere in the tiles.
    for token in ("$", "€", "£", "%", "ROI", "save", "saving"):
        assert token not in sec
    # Placement: the board tiles precede the benefits section.
    body = out.split("<body", 1)[1]
    assert body.index('id="mcp-board"') < body.index('id="mcp-benefits"')


def test_regulators_section_cites_captured_tools_and_hedges_dora() -> None:
    out = _run_build(_fake_shell())
    sec = out.split('id="mcp-regulators"', 1)[1].split("</section>", 1)[0]
    assert sec.count('<div class="spk-path">') == 4
    # Tool names exactly as captured in _data/mcp/*.tools.json.
    for tool in (
        "cite_rulebook", "list_rulebook_clauses", "get_cbpr_cutover_date",
        "check_cbpr_readiness", "classify_address", "validate_address",
        "repair_address", "validate_addresses",
    ):
        assert f'<code class="spk-mono">{tool}</code>' in sec
    # Dates as the tools themselves state them.
    assert "2026-11-16" in sec
    assert "14-16 November 2026" in sec
    assert "14 November 2026" in sec
    assert "SEPA, CBPR+ and HVPS+" in sec
    # DORA: control mapping only, certification disclaimed outright.
    assert "A note on DORA." in sec
    assert "not certified" in sec
    assert "no such product certification exists" in sec
    assert "your assessment to make" in sec


def test_capability_strip_counts_match_committed_captures() -> None:
    import json

    out = _run_build(_fake_shell())
    sec = out.split('id="mcp-capability"', 1)[1].split("</section>", 1)[0]
    # The published tool count is computed from the committed captures.
    data_dir = _ROOT / "_data" / "mcp"
    expected = len(
        json.loads((data_dir / "tool_schemas.json").read_text(encoding="utf-8"))[
            "tools"
        ]
    )
    for f in sorted(data_dir.glob("*.tools.json")):
        expected += len(json.loads(f.read_text(encoding="utf-8"))["tools"])
    assert f'<p class="spk-num">{expected}</p>' in sec
    assert '<p class="spk-num">9</p>' in sec
    assert "does the work, not just the docs" in sec
    assert "tools, captured live" in sec
    # Factual contrast, no competitor names.
    for vendor in ("mybanx", "HSBC"):
        assert vendor not in out


def test_free_three_ways_strip() -> None:
    out = _run_build(_fake_shell())
    sec = out.split('id="mcp-free"', 1)[1].split("</section>", 1)[0]
    assert sec.count('<div class="mcp-sec-cell">') == 3
    for eyebrow, title in (
        ("BOARDS", "Free to adopt."),
        ("ENGINEERS", "Free to run."),
        ("REGULATORS", "Free to audit."),
    ):
        assert f">{eyebrow}</span>" in sec
        assert title in sec
    assert 'class="mcp-sec mcp-3col"' in sec


def test_proof_strip_publishes_measured_timings() -> None:
    import json

    out = _run_build(_fake_shell())
    metrics = json.loads(
        (_ROOT / "_data" / "mcp" / "verified_metrics.json").read_text(
            encoding="utf-8"
        )
    )
    tp = metrics["timed_proof"]
    sec = out.split('id="mcp-proof"', 1)[1].split("</section>", 1)[0]
    # The real measured numbers with their date, not a slogan.
    assert f'{tp["cold_seconds"]}s' in sec
    assert f'{tp["warm_seconds"]}s' in sec
    assert tp["date_human"] in sec
    assert "cold cache to validated pain.001" in sec
    assert "Method:" in sec and "Machine:" in sec


def test_prompts_render_committed_transcripts_verbatim() -> None:
    import json

    out = _run_build(_fake_shell())
    data = json.loads(
        (_ROOT / "_data" / "mcp" / "hub_transcripts.json").read_text(
            encoding="utf-8"
        )
    )
    sec = out.split('id="mcp-prompts"', 1)[1].split("</section>", 1)[0]
    assert sec.count('<article class="mcp-prompt">') == len(data["prompts"]) == 3
    for p in data["prompts"]:
        # Prompt is copyable; excerpt lands escaped but verbatim.
        assert f'id="mcp-prompt-{p["id"]}"' in sec
        assert f'data-copy="#mcp-prompt-{p["id"]}"' in sec
        first_line = p["excerpt"].splitlines()[0]
        esc = (
            first_line.replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;")
        )
        assert esc in sec
        assert f'tool: {p["tool"]}' in sec
    assert f'captured {data["_meta"]["captured"]}' in sec
    # Real capabilities only: gateway generate, rulebook citation, sandbox.
    assert "run_sandbox_scenario" in sec
    assert "cite_rulebook" in sec


def test_sandbox_card_names_tools_and_links_docs_chapter() -> None:
    out = _run_build(_fake_shell())
    sec = out.split('id="mcp-sandbox"', 1)[1].split("</section>", 1)[0]
    # Tool names exactly as captured in reconcile-mcp.tools.json.
    for tool in (
        "list_sandbox_scenarios", "load_sandbox_scenario",
        "run_sandbox_scenario",
    ):
        assert f'<code class="spk-mono">{tool}</code>' in sec
    assert "Try it with zero real data." in sec
    assert 'href="/iso20022-mcp-docs/index.html#chapter-3"' in sec
    assert 'href="/iso20022-mcp-reference/index.html#reconcile"' in sec


def test_adoption_strip_matches_verified_metrics() -> None:
    import json

    out = _run_build(_fake_shell())
    metrics = json.loads(
        (_ROOT / "_data" / "mcp" / "verified_metrics.json").read_text(
            encoding="utf-8"
        )
    )
    ad = metrics["adoption"]
    sec = out.split('id="mcp-adoption"', 1)[1].split("</section>", 1)[0]
    assert f'<p class="spk-num">{ad["suite_last_month_total"]:,}</p>' in sec
    assert f'<p class="spk-num">{ad["registry_listed"]}</p>' in sec
    assert ad["date_human"] in sec
    assert sec.count("pypistats.org last-30-day counts for the nine suite packages") == 1
    assert sec.count("live listing count for this account on registry.modelcontextprotocol.io") == 1
    # The committed figure is itself the sum of the committed per-package
    # counts (nine suite packages, no more, no less).
    per = ad["suite_last_month_by_package"]
    assert len(per) == 9
    assert sum(per.values()) == ad["suite_last_month_total"]


def test_verified_sections_skip_gracefully_without_metrics() -> None:
    """Same policy as the schema viewer: missing evidence files drop their
    sections instead of failing the build or inventing numbers."""
    old_metrics = mcp.METRICS_SRC
    old_tx = mcp.TRANSCRIPTS_SRC
    mcp.METRICS_SRC = Path("/nonexistent/verified_metrics.json")
    mcp.TRANSCRIPTS_SRC = Path("/nonexistent/hub_transcripts.json")
    try:
        out = _run_build(_fake_shell())
    finally:
        mcp.METRICS_SRC = old_metrics
        mcp.TRANSCRIPTS_SRC = old_tx
    assert 'id="mcp-proof"' not in out
    assert 'id="mcp-adoption"' not in out
    assert 'id="mcp-prompts"' not in out
    # The rest of the page still builds, selector included.
    assert 'id="mcp-clients"' in out
    assert '<section class="read-as"' in out


# --- (b) anti-silent-no-op: a missing anchor must abort ----------------------


def _assert_build_aborts(shell_text: str) -> None:
    with pytest.raises(SystemExit) as excinfo:
        _run_build(shell_text)
    # SystemExit with a message string exits non-zero.
    assert excinfo.value.code not in (0, None)


def test_missing_nav_anchor_exits_nonzero() -> None:
    _assert_build_aborts(_fake_shell().replace('class="ap-menu"', 'class="other-menu"'))


def test_missing_main_wrap_exits_nonzero() -> None:
    _assert_build_aborts(_fake_shell().replace('<div class="wrap articles-wrap">', "<div>"))


def test_missing_collectionpage_jsonld_exits_nonzero() -> None:
    _assert_build_aborts(_fake_shell().replace('"@type":"CollectionPage"', '"@type":"Other"'))


def test_missing_og_title_exits_nonzero() -> None:
    _assert_build_aborts(_fake_shell().replace('property="og:title"', 'property="og:nope"'))


# --- (c) _swap_into_shell replacement-template regression --------------------


def test_swap_into_shell_body_with_backslashes_lands_verbatim() -> None:
    body = r'<div class="x">literal \g<0> then \1 and a lone backslash \ end</div>'
    # \w and a trailing lone backslash are invalid re replacement templates —
    # they must pass through untouched (title is HTML-escaped, not re-parsed).
    title = "Title \\with backslashes \\"
    out = cs._swap_into_shell(_fake_shell(), body, title, "Desc", "https://example.com/x/")
    assert body in out  # not duplicated shell content, no re.error
    assert f"<title>{title}</title>" in out
    assert "OLD LISTING BODY" not in out


def test_unescape_head_metas_is_head_bounded() -> None:
    html = (
        "<head>&lt;meta name=\"a\" content=\"b\"&gt;</head>"
        "<body><p>quoted markup: &lt;meta name=\"c\"&gt;</p></body>"
    )
    out = cs._unescape_head_metas(html)
    assert '<meta name="a" content="b">' in out
    assert '&lt;meta name="c"&gt;' in out  # body prose stays escaped


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
