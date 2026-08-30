# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Unit tests for gen_layouts' banner-src emission.

PR #396 added `<meta name="banner-src" content="{{banner}}">` to the about
and page layouts so postbuild_lib.seo can rebuild og:image from the real
banner — without it ssg scrapes the first body <img>, a share-button icon,
and the social card renders small.

But those two layouts are *generated*. Hand-editing them meant the next
`gen_layouts.py` run silently deleted both lines, so the fix regressed on
every publish run and only survived because someone noticed and reverted.
The generator has to emit the meta itself.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
_SPEC = importlib.util.spec_from_file_location(
    "gen_layouts_under_test", ROOT / "scripts" / "generators" / "gen_layouts.py"
)
gl = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = gl
_SPEC.loader.exec_module(gl)

CANONICAL = '    <link rel="canonical" href="{{url}}" />'


def test_inserts_meta_before_canonical():
    out = gl.with_banner_src(f"<head>\n{CANONICAL}\n</head>")
    assert '<meta name="banner-src" content="{{banner}}" />' in out
    assert out.index("banner-src") < out.index('rel="canonical"')


def test_is_idempotent():
    once = gl.with_banner_src(f"<head>\n{CANONICAL}\n</head>")
    assert gl.with_banner_src(once) == once


def test_raises_when_anchor_missing():
    """Fail loudly rather than silently emitting a layout without the meta."""
    try:
        gl.with_banner_src("<head></head>")
    except RuntimeError:
        return
    raise AssertionError("expected RuntimeError when the canonical link is absent")


def test_scope_is_about_and_page():
    """seo.py documents this contract for the non-BlogPosting layouts."""
    assert sorted(gl._NEEDS_BANNER_SRC) == ["about.html", "page.html"]


def test_main_writes_the_meta_into_about_and_page(monkeypatch):
    """The regression test that matters.

    Exercises main()'s own wiring rather than calling with_banner_src()
    directly — otherwise the helper can be perfectly correct while nothing
    calls it, which is precisely the bug: the meta existed in the committed
    layouts and the generator quietly dropped it on every run.
    """
    written: dict[str, str] = {}
    monkeypatch.setattr(gl, "write", lambda name, html: written.update({name: html}))
    gl.main()

    assert written, "main() wrote no layouts"
    for name in sorted(gl._NEEDS_BANNER_SRC):
        assert name in written, f"{name} was not generated"
        assert 'name="banner-src"' in written[name], (
            f"{name} was generated without the banner-src meta — "
            "og:image will fall back to a share-button icon"
        )


def test_main_does_not_add_the_meta_to_other_layouts(monkeypatch):
    """Scope stays where seo.py documents it; no silent widening."""
    written: dict[str, str] = {}
    monkeypatch.setattr(gl, "write", lambda name, html: written.update({name: html}))
    gl.main()

    for name, html in written.items():
        if name in gl._NEEDS_BANNER_SRC:
            continue
        assert 'name="banner-src"' not in html, f"{name} unexpectedly carries banner-src"
