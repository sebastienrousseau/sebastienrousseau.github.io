# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Offline tests for scripts/seo_and_audit/check_live_content.py."""

from __future__ import annotations

import datetime as dt
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
_SPEC = importlib.util.spec_from_file_location(
    "check_live_content", ROOT / "scripts" / "seo_and_audit" / "check_live_content.py"
)
assert _SPEC is not None and _SPEC.loader is not None
clc = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(clc)

TODAY = dt.date(2026, 11, 1)


def test_hub_current_passes_quoted_and_minified() -> None:
    assert clc.check_hub('<section id="mcp-faq"></section>') == []
    assert clc.check_hub("<section id=mcp-faq></section>") == []


def test_hub_stale_is_caught() -> None:
    stale = '<a href="https://github.com/x/blob/main/project-docs/sigstore.md">' + "<section>" * 21
    errors = clc.check_hub(stale)
    assert any("mcp-faq" in e for e in errors)
    assert any("project-docs" in e for e in errors)
    assert any("21 <section>" in e for e in errors)


def test_stylesheet_urls_same_origin_only() -> None:
    html = (
        '<link rel="stylesheet" href="/_csp/a.css">'
        "<link rel=stylesheet href=/_csp/b.css>"
        '<link rel="stylesheet" href="https://fonts.googleapis.com/x.css">'
        '<link rel="preload" href="/f.woff2">'
    )
    assert clc.stylesheet_urls(html) == ["/_csp/a.css", "/_csp/b.css"]


def test_design_system_detection() -> None:
    assert (
        clc.check_design_system("@layer legacy{} :root{--fs-display:0;--fs-prose:0;--measure:0}")
        == []
    )
    assert len(clc.check_design_system(".a{}")) == 4


def test_stamp_age() -> None:
    fresh = (
        '<span class="proof-updated">Updated <time datetime="2026-10-30">30 Oct 2026</time>.</span>'
    )
    stale = "<span class=proof-updated>Updated <time datetime=2026-09-15>15 Sep 2026</time></span>"
    assert clc.check_stamp(fresh, TODAY) == []
    assert "47 days old" in clc.check_stamp(stale, TODAY)[0]
    assert clc.check_stamp("<p>none</p>", TODAY)


def test_freshness() -> None:
    rss = "<rss><item><link>https://sebastienrousseau.com/2026-10-28-fca/</link></item></rss>"
    newest = clc.newest_feed_link(rss)
    assert newest == "/2026-10-28-fca"
    home = '<a href="/2026-10-28-fca/index.html">'
    assert clc.check_freshness(newest, home, home) == []
    errs = clc.check_freshness(newest, home, '<a href="/2026-10-24-old/">')
    assert errs == ["/articles/: newest article /2026-10-28-fca not listed (stale page?)"]


def test_feed_language_flags_translations() -> None:
    english = "<item><link>https://sebastienrousseau.com/2026-10-28-fca</link></item>"
    assert clc.check_feed_language(english) == []
    mixed = (
        "<item><link>https://sebastienrousseau.com/ta/2026-10-28-x/index.html</link></item>"
        + english
        + "<item><link>https://sebastienrousseau.com/fr/2026-10-28-y/</link></item>"
    )
    assert clc.check_feed_language(mixed) == [
        "rss.xml: 2 non-English item(s), first /ta/2026-10-28-x/index.html"
    ]
    # An English article whose slug does not start with a date is English.
    whitepaper = "<item><link>https://sebastienrousseau.com/2026-banking-whitepaper</link></item>"
    assert clc.check_feed_language(whitepaper + english) == []
    regional = "<item><link>https://sebastienrousseau.com/pt-br/x/</link></item>"
    assert clc.check_feed_language(regional) == ["rss.xml: 1 non-English item(s), first /pt-br/x/"]
    # The channel <link> is not an item.
    channel = "<channel><link>https://sebastienrousseau.com</link>" + english
    assert clc.check_feed_language(channel) == []


def test_run_wires_every_check() -> None:
    pages = {
        "/": '<link rel="stylesheet" href="/_csp/s.css">'
        '<span class="proof-updated">Updated <time datetime="2026-10-30">x</time></span>'
        '<a href="/2026-10-28-fca/">',
        "/iso20022-mcp/": '<section id="mcp-faq"></section>',
        "/articles/": '<a href="/2026-10-28-fca/">',
        "/rss.xml": "<item><link>https://sebastienrousseau.com/2026-10-28-fca/</link></item>",
        "/_csp/s.css": "@layer legacy{} --fs-display --fs-prose --measure",
    }
    assert clc.run(fetch=pages.__getitem__, today=TODAY) == []


def test_main_exit_code_and_edges(monkeypatch) -> None:
    assert clc.newest_feed_link("<rss></rss>") is None
    assert clc.newest_feed_link("<rss><item><title>x</title></item></rss>") is None
    assert clc.check_freshness(None, "", "") == ["rss.xml: no first item"]
    monkeypatch.setattr(clc, "run", lambda: [])
    assert clc.main([]) == 0
    monkeypatch.setattr(clc, "run", lambda: ["boom"])
    assert clc.main([]) == 1
