# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Two postbuild repairs that rewrite shipped HTML, both previously untested.

fix_escaped_ssg_html unescapes markup that ssg escaped by mistake. It is the
riskier of the two: unescape too eagerly and a `<pre>` sample of markup in an
article becomes live HTML on the page. The `<pre>`/`<code>` exclusion is the
whole safety property, and nothing checked it.

fix_lang_switcher rewrites the language menu's hrefs from the page's own
hreflang links. Get it wrong and every locale switch on the site points at the
wrong page — silently, since the links still resolve.
"""

from __future__ import annotations

import html as _html

import fix_escaped_ssg_html as esc
import fix_lang_switcher as sw

# ---------------------------------------------------------------------------
# fix_escaped_ssg_html — head
# ---------------------------------------------------------------------------


def test_repair_head_unescapes_an_escaped_meta() -> None:
    head = '<head>&lt;meta name="description" content="x"&gt;'
    out = esc._repair_head(head)
    assert '<meta name="description" content="x">' in out


def test_repair_head_keeps_the_first_of_a_leaked_duplicate() -> None:
    """Page-specific meta precedes the revived generic one; keep the first."""
    head = (
        '<head><meta name="description" content="page specific">'
        '<meta name="description" content="generic site bio">'
    )
    out = esc._repair_head(head)
    assert out.count('name="description"') == 1
    assert "page specific" in out
    assert "generic site bio" not in out


def test_repair_head_does_not_dedupe_legitimately_repeating_metas() -> None:
    """theme-color appears twice on purpose — light and dark."""
    head = (
        "<head>"
        '<meta name="theme-color" content="#fff" media="(prefers-color-scheme: light)">'
        '<meta name="theme-color" content="#000" media="(prefers-color-scheme: dark)">'
    )
    out = esc._repair_head(head)
    assert out.count('name="theme-color"') == 2


def test_repair_head_leaves_property_metas_alone() -> None:
    head = (
        '<head><meta property="og:title" content="a"><meta property="og:description" content="b">'
    )
    assert esc._repair_head(head) == head


# ---------------------------------------------------------------------------
# fix_escaped_ssg_html — body
# ---------------------------------------------------------------------------


def test_repair_body_is_a_no_op_without_the_marker() -> None:
    body = "<p>Nothing escaped here &amp; nothing to do.</p>"
    assert esc._repair_body(body) == body


def test_repair_body_unescapes_a_marked_fragment() -> None:
    body = '</head><body>&lt;div lang="en"&gt;&lt;p&gt;hi&lt;/p&gt;<p>real</p>'
    out = esc._repair_body(body)
    assert '<div lang="en">' in out
    assert "<p>hi</p>" in out


def test_repair_body_restores_escaped_json_inside_the_fragment() -> None:
    """Tag-by-tag unescaping revives the script shell but not its JSON."""
    body = '&lt;div lang="en"&gt;&lt;script&gt;{&quot;a&quot;: 1}&lt;/script&gt;<p>x</p>'
    out = esc._repair_body(body)
    assert '{"a": 1}' in out
    assert "&quot;" not in out.split("<p>")[0]


def test_repair_body_never_touches_a_pre_block() -> None:
    """Escaped markup inside <pre> is content a reader asked to see."""
    body = '<pre>&lt;div lang="en"&gt;example&lt;/div&gt;</pre>'
    assert esc._repair_body(body) == body


def test_repair_body_never_touches_a_code_block() -> None:
    body = '<code>&lt;div lang="fr"&gt;sample&lt;/div&gt;</code>'
    assert esc._repair_body(body) == body


def test_repair_body_fixes_outside_a_pre_but_not_inside_it() -> None:
    body = (
        '<pre>&lt;div lang="en"&gt;kept escaped&lt;/div&gt;</pre>'
        '&lt;div lang="en"&gt;&lt;em&gt;repaired&lt;/em&gt;<p>end</p>'
    )
    out = esc._repair_body(body)
    assert "&lt;div lang=" in out, "the <pre> sample must survive untouched"
    assert "<em>repaired</em>" in out


# ---------------------------------------------------------------------------
# fix_escaped_ssg_html — whole document
# ---------------------------------------------------------------------------


def test_repair_returns_input_unchanged_without_a_head() -> None:
    fragment = "<p>no head element here</p>"
    assert esc.repair(fragment) == fragment


def test_repair_handles_head_and_body_together() -> None:
    doc = (
        '<html><head>&lt;meta name="keywords" content="k"&gt;</head>'
        '<body>&lt;div lang="en"&gt;&lt;p&gt;b&lt;/p&gt;<p>real</p></body></html>'
    )
    out = esc.repair(doc)
    assert '<meta name="keywords" content="k">' in out
    assert "<p>b</p>" in out


def test_repair_is_idempotent() -> None:
    """Running the repair twice must not double-unescape entities."""
    doc = (
        '<html><head>&lt;meta name="author" content="A &amp;amp; B"&gt;</head>'
        "<body><p>x</p></body></html>"
    )
    once = esc.repair(doc)
    assert esc.repair(once) == once


# ---------------------------------------------------------------------------
# fix_lang_switcher — path extraction
# ---------------------------------------------------------------------------


def test_path_of_strips_scheme_and_host() -> None:
    assert sw._path_of("https://sebastienrousseau.com/fr/a/") == "/fr/a/"
    assert sw._path_of("http://sebastienrousseau.com/de/b/") == "/de/b/"


def test_path_of_keeps_query_and_fragment() -> None:
    assert sw._path_of("https://sebastienrousseau.com/a/?q=1#top") == "/a/?q=1#top"


def test_path_of_returns_root_for_a_bare_origin() -> None:
    assert sw._path_of("https://sebastienrousseau.com") == "/"


def test_path_of_passes_through_a_relative_href() -> None:
    assert sw._path_of("/already/relative/") == "/already/relative/"


# ---------------------------------------------------------------------------
# fix_lang_switcher — alternates
# ---------------------------------------------------------------------------


HEAD = (
    '<link rel="alternate" hreflang="en" href="https://sebastienrousseau.com/a/">'
    '<link rel="alternate" hreflang="fr" href="https://sebastienrousseau.com/fr/a/">'
    '<link rel="alternate" hreflang="x-default" href="https://sebastienrousseau.com/a/">'
)


def test_alternates_collects_langs_as_relative_paths() -> None:
    alts = sw._alternates(HEAD)
    assert alts["en"] == "/a/"
    assert alts["fr"] == "/fr/a/"


def test_alternates_excludes_x_default() -> None:
    """x-default is a routing hint, not a language the switcher offers."""
    assert "x-default" not in sw._alternates(HEAD)


def test_alternates_on_a_page_with_no_hreflang_links() -> None:
    assert sw._alternates("<head></head>") == {}


# ---------------------------------------------------------------------------
# fix_lang_switcher — rewrite
# ---------------------------------------------------------------------------


SWITCHER = (
    '<a class="ap-lang-item" href="/wrong/" data-lang="fr" role="menuitem">Français</a>'
    '<a class="ap-lang-item" href="/also-wrong/" data-lang="de" role="menuitem">Deutsch</a>'
)


def test_rewrite_replaces_only_langs_the_page_actually_has() -> None:
    """A language with no live translation keeps its existing href."""
    out, n = sw._rewrite(SWITCHER, {"fr": "/fr/a/"})
    assert 'href="/fr/a/"' in out
    assert 'href="/also-wrong/"' in out, "de has no alternate; leave it alone"
    assert n == 1


def test_rewrite_counts_nothing_when_the_href_already_matches() -> None:
    html = '<a class="ap-lang-item" href="/fr/a/" data-lang="fr" role="menuitem">Français</a>'
    out, n = sw._rewrite(html, {"fr": "/fr/a/"})
    assert out == html
    assert n == 0


def test_rewrite_with_no_alternates_changes_nothing() -> None:
    out, n = sw._rewrite(SWITCHER, {})
    assert out == SWITCHER
    assert n == 0


def test_rewrite_is_idempotent() -> None:
    alts = {"fr": "/fr/a/", "de": "/de/a/"}
    once, first = sw._rewrite(SWITCHER, alts)
    twice, second = sw._rewrite(once, alts)
    assert twice == once
    assert first == 2
    assert second == 0


def test_alternates_and_rewrite_compose_on_a_whole_page() -> None:
    page = f"<html><head>{HEAD}</head><body>{SWITCHER}</body></html>"
    out, n = sw._rewrite(page, sw._alternates(page))
    assert 'href="/fr/a/"' in out
    assert n == 1
    assert _html.unescape(out) == out, "the rewrite must not introduce entities"
