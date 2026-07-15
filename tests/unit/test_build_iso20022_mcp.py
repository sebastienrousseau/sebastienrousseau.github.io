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

import sys
import tempfile
from pathlib import Path

# Mirror tests/unit/conftest.py wiring so the file also runs standalone.
_ROOT = Path(__file__).resolve().parents[2]
for _sub in ("lib", "editorial", "generators", "postbuild"):
    _p = _ROOT / "scripts" / _sub
    if _p.is_dir() and str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

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


def _run_build(shell_text: str) -> str:
    """Run mcp.main() against ``shell_text`` in a temp tree, returning the
    written page. Restores the module's real paths afterwards."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        shell_path = tmp_path / "articles" / "index.html"
        shell_path.parent.mkdir(parents=True)
        shell_path.write_text(shell_text, encoding="utf-8")
        out_path = tmp_path / "iso20022-mcp" / "index.html"
        old_shell, old_out = mcp.SHELL_SRC, mcp.OUT
        mcp.SHELL_SRC, mcp.OUT = shell_path, out_path
        try:
            rc = mcp.main()
            assert rc == 0
            return out_path.read_text(encoding="utf-8")
        finally:
            mcp.SHELL_SRC, mcp.OUT = old_shell, old_out


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


def test_full_build_nav_has_nine_items_with_suite_active() -> None:
    out = _run_build(_fake_shell())
    assert 'aria-current="page" class="active">Suite</a>' in out
    nav = out.split('<ul class="ap-menu">', 1)[1].split("</ul>", 1)[0]
    assert nav.count("<li>") == 9
    for label in (
        "About", "Articles", "Papers", "Case studies", "Topics",
        "Projects", "Playlists", "Speaking", "Suite",
    ):
        assert f">{label}</a>" in nav


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
    # CLS guards: dimensions match the CSS aspect-ratios (16/8, 16/6).
    assert 'class="mcp-hero-img" width="1920" height="960"' in out
    assert 'class="mcp-band-img" width="1920" height="720"' in out
    # Commands are <code>, arrows are hidden from AT, CTAs carry card names.
    assert '<code class="spk-mono">' in out
    assert '<span class="spk-arw" aria-hidden="true">' in out
    assert 'aria-label="Read the docs: The gateway"' in out


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
