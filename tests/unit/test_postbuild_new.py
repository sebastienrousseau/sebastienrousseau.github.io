"""Unit tests for the postbuild passes added in the
"100% compliance with WAVE / axe / Lighthouse / WebPageTest / GTmetrix"
PR — JS+CSS minification, theme-init inlining, LCP preload, extended
SRI patching, and the inline-script CSP hash collection.

Each test exercises one function in isolation. The integration smoke
test in tests/test_build_output.py drives the full build pipeline.
"""

from __future__ import annotations

import base64
import hashlib
from pathlib import Path

import postbuild as pb
import postbuild_assets as pa
import postbuild_transforms as _pt
import pytest

# ---------------------------------------------------------------------------
# _minify_one — JS asset minification helper
# ---------------------------------------------------------------------------


def test_minify_one_saves_bytes_on_unminified_js(tmp_path: Path):
    p = tmp_path / "x.js"
    p.write_text("// hello\nfunction foo() {\n  return 42;\n}\n", encoding="utf-8")
    before, after = pb._minify_one(p)
    assert before > 0
    assert after > 0
    assert after < before
    body = p.read_text(encoding="utf-8")
    assert "// hello" not in body
    assert "function foo()" in body


def test_minify_one_idempotent_on_already_minified_with_trailing_newline(tmp_path: Path):
    """Already-minified + already-trailing-\\n → no rewrite, (0, 0)."""
    p = tmp_path / "x.js"
    p.write_text("function foo(){return 42}\n", encoding="utf-8")
    before, after = pb._minify_one(p)
    assert (before, after) == (0, 0)


def test_minify_one_stamps_trailing_newline_when_missing(tmp_path: Path):
    """Already-minified but no trailing \\n → still rewrites to add it
    so the on-disk SHA-256 matches the bytes GitHub Pages serves."""
    p = tmp_path / "x.js"
    p.write_text("function foo(){return 42}", encoding="utf-8")
    before, after = pb._minify_one(p)
    assert after == before + 1
    assert p.read_text(encoding="utf-8").endswith("\n")


def test_minify_one_returns_zero_on_missing_file(tmp_path: Path):
    # File doesn't exist → read_text raises OSError → swallowed.
    p = tmp_path / "nope.js"
    assert pb._minify_one(p) == (0, 0)


def test_minify_one_returns_zero_on_invalid_utf8(tmp_path: Path):
    p = tmp_path / "bad.js"
    p.write_bytes(b"\xff\xfe\x00bad")
    assert pb._minify_one(p) == (0, 0)


# ---------------------------------------------------------------------------
# _minify_css — CSS asset minification helper
# ---------------------------------------------------------------------------


def test_minify_css_strips_leading_indent_and_comments(tmp_path: Path):
    p = tmp_path / "x.css"
    p.write_text("      /* preamble */\n      body { color: #fff; }\n", encoding="utf-8")
    before, after = pb._minify_css(p)
    assert before > after
    body = p.read_text(encoding="utf-8")
    assert "/* preamble */" not in body
    assert "color:#fff" in body or "color: #fff" in body


def test_minify_css_idempotent_on_already_minified_with_trailing_newline(tmp_path: Path):
    """Already-minified + already-trailing-\\n → no rewrite, (0, 0)."""
    p = tmp_path / "x.css"
    p.write_text("body{color:red}\n", encoding="utf-8")
    assert pb._minify_css(p) == (0, 0)


def test_minify_css_stamps_trailing_newline_when_missing(tmp_path: Path):
    """Same as the JS case — pin \\n so SRI ≡ wire."""
    p = tmp_path / "x.css"
    p.write_text("body{color:red}", encoding="utf-8")
    before, after = pb._minify_css(p)
    assert after == before + 1
    assert p.read_text(encoding="utf-8").endswith("\n")


def test_minify_css_handles_missing_file(tmp_path: Path):
    assert pb._minify_css(tmp_path / "missing.css") == (0, 0)


def test_minify_css_handles_invalid_utf8(tmp_path: Path):
    p = tmp_path / "bad.css"
    p.write_bytes(b"\xff\xfeoops")
    assert pb._minify_css(p) == (0, 0)


# ---------------------------------------------------------------------------
# _gather_js_targets / _gather_css_targets — file discovery
# ---------------------------------------------------------------------------


def test_gather_js_targets_returns_empty_when_public_missing(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(pa, "PUBLIC", tmp_path / "nope")
    assert pb._gather_js_targets() == []


def test_gather_js_targets_excludes_labs(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(pa, "PUBLIC", tmp_path)
    (tmp_path / "labs" / "demo").mkdir(parents=True)
    (tmp_path / "labs" / "demo" / "wasm.js").write_text("// lab", encoding="utf-8")
    (tmp_path / "main.js").write_text("// app", encoding="utf-8")
    targets = {p.name for p in pb._gather_js_targets()}
    assert "main.js" in targets
    assert "wasm.js" not in targets


def test_gather_css_targets_returns_empty_when_public_missing(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(pa, "PUBLIC", tmp_path / "nope")
    assert pb._gather_css_targets() == []


def test_gather_css_targets_finds_all_css(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(pa, "PUBLIC", tmp_path)
    (tmp_path / "_csp").mkdir()
    (tmp_path / "_csp" / "a.css").write_text("body{}", encoding="utf-8")
    (tmp_path / "highlight.css").write_text(".k{}", encoding="utf-8")
    names = {p.name for p in pb._gather_css_targets()}
    assert names == {"a.css", "highlight.css"}


# ---------------------------------------------------------------------------
# fix_sri — _csp/* and top-level fingerprinted asset SRI stamping
# ---------------------------------------------------------------------------


def _stub_asset(name: str, body: bytes, monkeypatch) -> str:
    """Register a full integrity attribute value (one or more
    space-separated ``sha256-<b64>`` tokens) for ``name`` and return
    the first token's base64 digest for legacy single-token assertions."""
    integrity = pb._candidate_digests(body)
    new = dict(pb._pa.asset_hashes)
    new[name] = integrity
    monkeypatch.setattr(pb._pa, "asset_hashes", new)
    # Return just the first token's b64 (for assertions like
    # ``f"sha256-{digest}" in out``).
    return integrity.split()[0].removeprefix("sha256-")


def test_pages_trailing_newline_constant_is_single_lf():
    """GitHub Pages appends exactly one ``\\n``, no more, no less.
    Pin the constant so a regression to ``\\r\\n`` or empty doesn't
    silently re-break SRI."""
    assert pb._PAGES_TRAILING_NEWLINE == b"\n"


def test_candidate_digests_emits_both_primary_and_appended_token():
    """``_candidate_digests`` returns two space-separated SRI tokens
    so the integrity attribute covers both Pages-edge variants
    (file-as-is + file+trailing-newline)."""
    out = pb._candidate_digests(b"body{}")
    parts = out.split(" ")
    assert len(parts) == 2
    assert all(p.startswith("sha256-") for p in parts)
    # Tokens must be distinct — adding a newline must change the hash.
    assert parts[0] != parts[1]


def test_candidate_digests_collapses_when_no_difference(monkeypatch):
    """If newline-append produces the same hash (couldn't happen with
    real SHA-256, but covers the defensive branch), emit a single token."""
    monkeypatch.setattr(pb, "b64_sha256", lambda b: "FIXED")
    out = pb._candidate_digests(b"body{}")
    assert out == "sha256-FIXED"


def test_fix_sri_stamps_real_digest_on_csp_link(monkeypatch):
    digest = _stub_asset("abcd1234.css", b"body{}", monkeypatch)
    html = (
        '<link rel="stylesheet" href="/_csp/abcd1234.css" '
        'integrity="sha256-abcd1234" crossorigin="anonymous">'
    )
    out = pb.fix_sri(html)
    # Integrity now carries one or more space-separated sha256-<b64>
    # tokens (per ``_candidate_digests``). Assert the primary token
    # is present anywhere inside the integrity value.
    assert f"sha256-{digest}" in out
    assert 'sha256-abcd1234"' not in out


def test_fix_sri_stamps_digest_on_top_level_fingerprinted_js(monkeypatch):
    digest = _stub_asset("main.e1c270a6.js", b'"use strict";', monkeypatch)
    html = "<script defer src=/main.e1c270a6.js></script>"
    out = pb.fix_sri(html)
    assert f"sha256-{digest}" in out
    assert 'crossorigin="anonymous"' in out


def test_fix_sri_filename_starting_with_digit_is_matched(monkeypatch):
    """Regression guard: the original asset_path_re used `[a-z\\-_]` for
    the first char, missing files like ``3ae64e6558e84d20.css``."""
    digest = _stub_asset("3ae64e6558e84d20.css", b"body{margin:0}", monkeypatch)
    html = (
        '<link rel="stylesheet" href="/_csp/3ae64e6558e84d20.css" '
        'integrity="sha256-3ae64e6558e84d20" crossorigin="anonymous">'
    )
    out = pb.fix_sri(html)
    assert f"sha256-{digest}" in out


def test_fix_sri_no_op_when_asset_unknown(monkeypatch):
    monkeypatch.setattr(pa, "asset_hashes", {})
    html = '<link rel="stylesheet" href="/_csp/unknown.css">'
    assert pb.fix_sri(html) == html


def test_fix_sri_no_op_when_tag_doesnt_reference_an_asset():
    html = '<link rel="canonical" href="https://example.com/">'
    assert pb.fix_sri(html) == html


def test_fix_sri_collapses_duplicate_crossorigin(monkeypatch):
    digest = _stub_asset("main.abc.js", b"x", monkeypatch)
    html = (
        '<script crossorigin="anonymous" defer src=/main.abc.js '
        'crossorigin="anonymous"></script>'
    )
    out = pb.fix_sri(html)
    assert out.count('crossorigin="anonymous"') == 1
    assert f"sha256-{digest}" in out


def test_fix_sri_does_not_corrupt_unquoted_attribute_tail(monkeypatch):
    """Regression for a bug where ``stripped[-2:]`` re-appended the last
    two chars of the source URL after the new attribute, producing tags
    like ``... crossorigin=\"anonymous\"s>``."""
    digest = _stub_asset("main.e1c270a6.js", b"x", monkeypatch)
    html = "<script defer src=/main.e1c270a6.js></script>"
    out = pb.fix_sri(html)
    # Must end cleanly at `>`, not `"s>` or `"js>`.
    assert out.startswith("<script")
    tag_end = out.split("</script>", 1)[0]
    assert tag_end.rstrip().endswith(">")
    assert 'crossorigin="anonymous"s>' not in out
    assert 'crossorigin="anonymous"js>' not in out
    assert f"sha256-{digest}" in out


def test_fix_sri_handles_self_closing_link(monkeypatch):
    digest = _stub_asset("foo.css", b"body{}", monkeypatch)
    html = '<link rel="stylesheet" href="/_csp/foo.css" />'
    out = pb.fix_sri(html)
    assert f"sha256-{digest}" in out
    # The self-closing slash should still be there.
    assert out.rstrip().endswith("/>")


# ---------------------------------------------------------------------------
# inline_theme_init — replaces <script src="/theme-init.js"> with an inline
# minified bootstrap.
# ---------------------------------------------------------------------------


def test_inline_theme_init_replaces_external_script_with_inline_body():
    html = '<head><script src="/theme-init.js"></script></head>'
    out, n = pb.inline_theme_init(html)
    assert n == 1
    assert '<script src="/theme-init.js"></script>' not in out
    assert "<script>" in out
    assert "data-theme" in out  # signature substring of the minified body
    assert "</script>" in out


def test_inline_theme_init_idempotent_no_external_tag():
    html = "<head></head>"
    out, n = pb.inline_theme_init(html)
    assert n == 0
    assert out == html


def test_inline_theme_init_handles_unquoted_src():
    html = "<head><script src=/theme-init.js></script></head>"
    out, n = pb.inline_theme_init(html)
    assert n == 1
    assert "data-theme" in out


def test_inline_theme_init_no_op_when_minified_body_empty(monkeypatch):
    monkeypatch.setattr(_pt, "THEME_INIT_MINIFIED", "")
    html = '<head><script src="/theme-init.js"></script></head>'
    out, n = pb.inline_theme_init(html)
    assert (out, n) == (html, 0)


# ---------------------------------------------------------------------------
# inject_lcp_preload — auto-inject `<link rel=preload as=image>` for the
# first non-lazy <img>.
# ---------------------------------------------------------------------------


def test_inject_lcp_preload_injects_for_first_eager_image():
    html = (
        "<head><title>x</title></head>"
        '<body><img src="https://cdn.example/lcp.webp" fetchpriority="high"></body>'
    )
    out, n = pb.inject_lcp_preload(html)
    assert n == 1
    assert (
        '<link rel="preload" as="image" '
        'href="https://cdn.example/lcp.webp" fetchpriority="high">' in out
    )


def test_inject_lcp_preload_no_op_when_preload_already_matches_img():
    """Existing preload already pointing at the first <img> src — no
    rewrite needed."""
    html = (
        '<head><link rel="preload" as="image" href="/y.webp"></head>'
        '<body><img src="/y.webp"></body>'
    )
    out, n = pb.inject_lcp_preload(html)
    assert n == 0
    assert out == html


def test_inject_lcp_preload_realigns_existing_preload_to_first_img():
    """The layout may emit a preload that doesn't quite match the
    URL the <img> ends up with (different transform width, etc.) —
    inject_lcp_preload rewrites the preload's href so the browser
    can actually use it."""
    html = (
        '<head><link rel="preload" as="image" '
        'href="https://cdn.example/hero.webp?w=1200"></head>'
        '<body><img src="https://cdn.example/hero.webp?w=200"></body>'
    )
    out, n = pb.inject_lcp_preload(html)
    assert n == 1
    assert 'href="https://cdn.example/hero.webp?w=200"' in out
    assert "?w=1200" not in out


def test_inject_lcp_preload_skips_first_image_when_lazy():
    """If the first <img> is loading=lazy, it isn't an LCP candidate —
    skip rather than preload an off-screen asset."""
    html = (
        "<head><title>x</title></head>" '<body><img loading="lazy" src="/below-fold.webp"></body>'
    )
    out, n = pb.inject_lcp_preload(html)
    assert n == 0
    assert "<link" not in out


def test_inject_lcp_preload_skips_data_uri():
    html = "<head><title>x</title></head>" '<body><img src="data:image/png;base64,AAAA"></body>'
    _, n = pb.inject_lcp_preload(html)
    assert n == 0


def test_inject_lcp_preload_skips_pages_with_no_img():
    html = "<head><title>x</title></head><body><p>no images</p></body>"
    out, n = pb.inject_lcp_preload(html)
    assert n == 0
    assert out == html


# ---------------------------------------------------------------------------
# inject_jsonld_hashes — CSP script-src sha256 token injection
# ---------------------------------------------------------------------------


def _b64(s: str) -> str:
    return base64.b64encode(hashlib.sha256(s.encode("utf-8")).digest()).decode("ascii")


def test_inject_jsonld_hashes_adds_token_for_inline_jsonld():
    body = '{"@context":"https://schema.org"}'
    hash_ = _b64(body)
    html = (
        '<meta http-equiv="Content-Security-Policy" '
        "content=\"default-src 'self'; script-src 'self';\">"
        f'<script type="application/ld+json">{body}</script>'
    )
    out = pb.inject_jsonld_hashes(html)
    assert f"'sha256-{hash_}'" in out


def test_inject_jsonld_hashes_covers_speculation_rules():
    body = '{"prerender":[{"source":"document"}]}'
    hash_ = _b64(body)
    html = (
        '<meta http-equiv="Content-Security-Policy" '
        "content=\"default-src 'self'; script-src 'self';\">"
        f'<script type="speculationrules">{body}</script>'
    )
    out = pb.inject_jsonld_hashes(html)
    assert f"'sha256-{hash_}'" in out


def test_inject_jsonld_hashes_covers_bare_inline_scripts():
    """The inlined theme-init bootstrap has no type/src — it must still
    pick up a sha256 token in CSP."""
    body = '(function(){var s="x"}());'
    hash_ = _b64(body)
    html = (
        '<meta http-equiv="Content-Security-Policy" '
        "content=\"default-src 'self'; script-src 'self';\">"
        f"<script>{body}</script>"
    )
    out = pb.inject_jsonld_hashes(html)
    assert f"'sha256-{hash_}'" in out


def test_inject_jsonld_hashes_strips_unsafe_inline():
    body = '{"a":1}'
    html = (
        '<meta http-equiv="Content-Security-Policy" '
        "content=\"script-src 'self' 'unsafe-inline';\">"
        f'<script type="application/ld+json">{body}</script>'
    )
    out = pb.inject_jsonld_hashes(html)
    assert "'unsafe-inline'" not in out


def test_inject_jsonld_hashes_no_op_when_no_inline_scripts():
    html = '<meta http-equiv="Content-Security-Policy" content="script-src \'self\';">'
    assert pb.inject_jsonld_hashes(html) == html


def test_inject_jsonld_hashes_dedups_identical_bodies():
    body = '{"@type":"Article"}'
    hash_ = _b64(body)
    html = (
        '<meta http-equiv="Content-Security-Policy" '
        "content=\"script-src 'self';\">"
        f'<script type="application/ld+json">{body}</script>'
        f'<script type="application/ld+json">{body}</script>'
    )
    out = pb.inject_jsonld_hashes(html)
    # Same body → one sha256 token, not two.
    assert out.count(f"'sha256-{hash_}'") == 1


# ---------------------------------------------------------------------------
# THEME_INIT_MINIFIED — sanity that module-init actually ran rjsmin
# ---------------------------------------------------------------------------


def test_theme_init_minified_is_smaller_than_source():
    """If _layouts/theme-init.js exists, the module-init copy must be
    shorter than the on-disk source."""
    src = Path("_layouts/theme-init.js")
    if not src.is_file():
        pytest.skip("source not present in this test environment")
    assert len(_pt.THEME_INIT_MINIFIED) > 0
    assert len(_pt.THEME_INIT_MINIFIED) < src.stat().st_size
    # Must still contain the data-theme assignment that the bootstrap does.
    assert "data-theme" in _pt.THEME_INIT_MINIFIED


# ---------------------------------------------------------------------------
# Bulk minify helpers — module-init exposes _bulk_minify_js + _bulk_minify_css
# so a test can drive the count/before/after accumulators against a
# synthetic PUBLIC tree.
# ---------------------------------------------------------------------------


def test_bulk_minify_js_counts_files_that_changed(tmp_path: Path, monkeypatch):
    """Every file that ended up rewritten (whether for size reduction
    OR for the SRI-stamping trailing newline) counts as 'changed'."""
    monkeypatch.setattr(pa, "PUBLIC", tmp_path)
    (tmp_path / "a.js").write_text("// comment\nfunction a() { return 1; }\n", encoding="utf-8")
    (tmp_path / "b.js").write_text("function b(){return 2}", encoding="utf-8")  # no nl
    (tmp_path / "c.js").write_text("function c(){return 3}\n", encoding="utf-8")  # mini + nl
    count, before, after = pb._bulk_minify_js()
    # a.js (minified), b.js (newline-stamped) — c.js is left alone.
    assert count == 2
    assert before > 0 and after > 0


def test_bulk_minify_js_returns_zero_on_empty_public(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(pa, "PUBLIC", tmp_path)
    assert pb._bulk_minify_js() == (0, 0, 0)


def test_bulk_minify_css_counts_files_that_changed(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(pa, "PUBLIC", tmp_path)
    (tmp_path / "a.css").write_text("/* preamble */\n      body { margin: 0; }\n", encoding="utf-8")
    (tmp_path / "b.css").write_text("body{margin:0}", encoding="utf-8")  # no nl
    (tmp_path / "c.css").write_text("body{margin:0}\n", encoding="utf-8")  # mini + nl
    count, before, after = pb._bulk_minify_css()
    # a.css (minified), b.css (newline-stamped) — c.css is left alone.
    assert count == 2
    assert before > 0 and after > 0


def test_bulk_minify_css_returns_zero_on_empty_public(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(pa, "PUBLIC", tmp_path)
    assert pb._bulk_minify_css() == (0, 0, 0)


# ---------------------------------------------------------------------------
# wrap_cdn_images_in_transform — CloudCDN responsive-variant rewriting pass
#
# CDN policy change on 2026-06-23 closed /api/transform to public traffic
# (returns 401). Public pages now use pre-generated variants named
# <stem>-{320,640,1200,1920}.webp under /stocks/images/. wrap_cdn_images_in_
# transform now emits those variant URLs instead of transform-URLs. The
# function name is retained to minimise downstream blast radius.
# ---------------------------------------------------------------------------


def test_wrap_cdn_images_rewrites_webp_to_variant_url():
    html = '<img src="https://cloudcdn.pro/stocks/images/foo.webp" width="600">'
    out, n = pb.wrap_cdn_images_in_transform(html)
    assert n == 1
    # 600 rendered × 2 = 1200, which is itself a variant width.
    assert "src=\"https://cloudcdn.pro/stocks/images/foo-1200.webp\"" in out
    assert "/api/transform" not in out


def test_wrap_cdn_images_lcp_hero_still_picks_variant():
    """Variant quality is fixed at ingestion time, so fetchpriority=high
    no longer changes the emitted URL. The variant width is what matters."""
    html = (
        '<img src="https://cloudcdn.pro/stocks/images/hero.webp" '
        'width="400" fetchpriority="high">'
    )
    out, n = pb.wrap_cdn_images_in_transform(html)
    assert n == 1
    # 400 × 2 = 800, snapped up to the 1200 variant.
    assert "src=\"https://cloudcdn.pro/stocks/images/hero-1200.webp\"" in out


def test_wrap_cdn_images_skips_svg_sources():
    html = (
        '<img src="https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/hsbc.svg" width="120">'
    )
    out, n = pb.wrap_cdn_images_in_transform(html)
    assert n == 0
    assert "/api/transform" not in out
    assert out == html


def test_wrap_cdn_images_skips_already_wrapped_urls():
    html = '<img src="https://cloudcdn.pro/api/transform?url=/x.webp&w=400" ' 'width="200">'
    out, n = pb.wrap_cdn_images_in_transform(html)
    assert n == 0
    assert out == html


def test_wrap_cdn_images_skips_data_uri():
    html = '<img src="data:image/png;base64,AAAA" width="40">'
    out, n = pb.wrap_cdn_images_in_transform(html)
    assert (out, n) == (html, 0)


def test_wrap_cdn_images_skips_non_cdn_origin():
    html = '<img src="https://example.com/foo.webp" width="600">'
    out, n = pb.wrap_cdn_images_in_transform(html)
    assert (out, n) == (html, 0)


def test_wrap_cdn_images_defaults_to_1200_variant_when_no_width():
    """No width= attribute → default base of 600, 2× = 1200, matches the
    1200 variant exactly."""
    html = '<img src="https://cloudcdn.pro/stocks/images/foo.webp">'
    out, n = pb.wrap_cdn_images_in_transform(html)
    assert n == 1
    assert "src=\"https://cloudcdn.pro/stocks/images/foo-1200.webp\"" in out


def test_wrap_cdn_images_snaps_oversized_to_1920_variant():
    """A request for 2000×2=4000 snaps to the largest variant (1920)."""
    html = '<img src="https://cloudcdn.pro/stocks/images/banner.webp" width="2000">'
    out, n = pb.wrap_cdn_images_in_transform(html)
    assert n == 1
    assert "src=\"https://cloudcdn.pro/stocks/images/banner-1920.webp\"" in out


def test_wrap_cdn_images_tiny_widths_snap_to_320_variant():
    """Very small width attributes (e.g. icons) snap up to the smallest
    pre-generated variant (320)."""
    html = '<img src="https://cloudcdn.pro/stocks/images/icon.webp" width="40">'
    out, n = pb.wrap_cdn_images_in_transform(html)
    assert n == 1
    # 40 × 2 = 80; snap up to the 320 variant (smallest pre-gen).
    assert "src=\"https://cloudcdn.pro/stocks/images/icon-320.webp\"" in out


def test_wrap_cdn_images_handles_unquoted_attrs():
    """SSG's minifier emits unquoted attribute values for short tokens —
    the regex must handle src=/foo without quotes."""
    html = "<img src=https://cloudcdn.pro/stocks/images/foo.webp width=600>"
    out, n = pb.wrap_cdn_images_in_transform(html)
    assert n == 1
    assert "foo-1200.webp" in out
    assert "/api/transform" not in out


def test_wrap_cdn_images_strips_existing_query_string():
    html = '<img src="https://cloudcdn.pro/stocks/images/foo.webp?v=1" width="600">'
    out, n = pb.wrap_cdn_images_in_transform(html)
    assert n == 1
    assert "foo-1200.webp" in out
    assert "v=1" not in out


def test_wrap_cdn_images_skips_tag_with_no_src():
    html = '<img alt="nope" width="100">'
    out, n = pb.wrap_cdn_images_in_transform(html)
    assert (out, n) == (html, 0)


def test_wrap_cdn_images_handles_jpg_and_png_extensions():
    """Non-webp paths under /stocks/images/ don't have webp variants under
    the same naming convention. Fall back to the bare CDN URL — strictly
    better than a 404 and matches the CDN policy."""
    html = (
        '<img src="https://cloudcdn.pro/stocks/images/a.jpg" width="300">'
        '<img src="https://cloudcdn.pro/stocks/images/b.png" width="300">'
        '<img src="https://cloudcdn.pro/stocks/images/c.jpeg" width="300">'
    )
    out, n = pb.wrap_cdn_images_in_transform(html)
    assert n == 3
    # All three return the bare CDN URL.
    assert "https://cloudcdn.pro/stocks/images/a.jpg" in out
    assert "https://cloudcdn.pro/stocks/images/b.png" in out


def test_build_cdn_transform_url_emits_variant_path():
    """The renamed-in-spirit helper now emits ``<stem>-<width>.webp``.
    Width 400 → snap to 640 variant."""
    out = pa._build_cdn_transform_url("/stocks/images/foo.webp", 400, 80)
    assert out == "https://cloudcdn.pro/stocks/images/foo-640.webp"


def test_build_cdn_transform_url_idempotent_on_existing_variant():
    """A path that's already a variant (foo-1200.webp) passes through
    unchanged so the postbuild's multi-pass pipeline doesn't compound
    suffixes to foo-1200-1200.webp."""
    out = pa._build_cdn_transform_url("/stocks/images/foo-1200.webp", 600, 80)
    assert out == "https://cloudcdn.pro/stocks/images/foo-1200.webp"


def test_build_cdn_transform_url_falls_through_for_non_stocks_paths():
    """`/clients/*` paths (logos) don't have pre-gen variants — they pass
    through as the bare CDN URL."""
    out = pa._build_cdn_transform_url("/clients/v1/logos/akqa.webp", 400, 80)
    assert out == "https://cloudcdn.pro/clients/v1/logos/akqa.webp"


def test_wrap_cdn_images_also_rewrites_preload_link_href():
    """``<link rel="preload" as="image" href="...">`` carrying a bare
    CDN URL is rewritten the same way as `<img>` srcs — points at the
    pre-gen variant equivalent."""
    html = (
        '<link rel="preload" as="image" '
        'href="https://cloudcdn.pro/stocks/images/hero.webp" fetchpriority="high">'
    )
    out, n = pb.wrap_cdn_images_in_transform(html)
    assert n == 1
    assert "hero-1200.webp" in out
    assert "/api/transform" not in out


def test_wrap_cdn_preload_handles_reverse_attribute_order():
    """SSG's minifier may emit ``as=image`` before ``rel=preload``."""
    html = (
        "<link as=image fetchpriority=high "
        "href=https://cloudcdn.pro/stocks/images/hero.webp rel=preload>"
    )
    out, n = pb.wrap_cdn_images_in_transform(html)
    assert n == 1
    assert "hero-1200.webp" in out


def test_rewrite_persisted_transforms_unwraps_api_transform_urls():
    """``rewrite_persisted_transforms`` cleans up any /api/transform URLs
    that survived into rendered HTML (e.g. from markdown-persisted
    related-card srcs, OpenGraph meta) → emits the variant equivalent."""
    html = (
        '<img src="https://cloudcdn.pro/api/transform?url='
        '/stocks/images/foo.webp&w=1200&format=webp&q=80">'
    )
    out, n = pb.rewrite_persisted_transforms(html)
    assert n == 1
    assert "foo-1200.webp" in out
    assert "/api/transform" not in out


def test_wrap_cdn_preload_skips_svg_passthrough():
    html = (
        '<link rel="preload" as="image" '
        'href="https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/hsbc.svg">'
    )
    out, n = pb.wrap_cdn_images_in_transform(html)
    assert (out, n) == (html, 0)


def test_wrap_cdn_preload_skips_non_cdn_origin():
    html = '<link rel="preload" as="image" href="https://example.com/hero.webp">'
    out, n = pb.wrap_cdn_images_in_transform(html)
    assert (out, n) == (html, 0)


def test_wrap_cdn_preload_skips_already_wrapped_url():
    html = (
        '<link rel="preload" as="image" '
        'href="https://cloudcdn.pro/api/transform?url=/x.webp&w=400">'
    )
    out, n = pb.wrap_cdn_images_in_transform(html)
    assert (out, n) == (html, 0)


def test_wrap_cdn_preload_returns_unchanged_when_href_sub_fails(monkeypatch):
    """Defensive: if the inner href-rewriter's ``subn`` reports zero
    substitutions even though the outer match succeeded, the original
    <link> tag is returned untouched (postbuild.py:505)."""

    class _FakeRE:
        def __init__(self, inner):
            self._inner = inner

        def search(self, s):
            return self._inner.search(s)

        def subn(self, repl, attrs, count=1):
            return attrs, 0

    monkeypatch.setattr(pa, "_LINK_HREF_ANY_RE", _FakeRE(pa._LINK_HREF_ANY_RE))
    html = (
        '<link rel="preload" as="image" '
        'href="https://cloudcdn.pro/stocks/images/hero.webp" '
        'fetchpriority="high">'
    )
    out, n = pb.wrap_cdn_images_in_transform(html)
    assert n == 0
    assert out == html


def test_align_existing_preload_returns_unchanged_when_subn_fails(monkeypatch):
    """Same defensive bail-out path in _align_existing_preload
    (postbuild.py:313)."""

    class _FakeRE:
        def __init__(self, inner):
            self._inner = inner

        def search(self, s):
            return self._inner.search(s)

        def subn(self, repl, attrs, count=1):
            return attrs, 0

    monkeypatch.setattr(pa, "_LINK_HREF_ANY_RE", _FakeRE(pa._LINK_HREF_ANY_RE))
    html = '<link rel="preload" as="image" ' 'href="https://cdn.example/old.webp">'
    out, n = pa._align_existing_preload(html, "https://cdn.example/new.webp")
    assert n == 0
    assert out == html


def test_link_attr_href_returns_none_when_match_groups_empty(monkeypatch):
    """``_link_attr_href`` bails to None when both capture groups are
    empty — a regex theoretically can match the attr name but produce
    no value."""

    class _FakeMatch:
        def group(self, n):
            return None  # both capture groups None

    class _FakeRE:
        def search(self, s):
            return _FakeMatch()

    monkeypatch.setattr(pa, "_LINK_HREF_ANY_RE", _FakeRE())
    assert pa._link_attr_href('href="x"') is None


def test_link_attr_href_returns_none_when_search_returns_none():
    """No href attribute present at all — search() returns None
    (postbuild.py:438)."""
    assert pa._link_attr_href('rel="preload" as="image"') is None


def test_img_attr_helpers_parse_quoted_and_unquoted():
    assert pa._img_attr_src('src="foo.webp"') == "foo.webp"
    assert pa._img_attr_src("src='bar.webp'") == "bar.webp"
    assert pa._img_attr_src("src=baz.webp") == "baz.webp"
    assert pa._img_attr_src("alt=foo") is None
    assert pa._img_attr_width('width="600"') == 600
    assert pa._img_attr_width("width=400") == 400
    assert pa._img_attr_width("height=600") is None
    assert pa._img_is_high_priority('fetchpriority="high"') is True
    assert pa._img_is_high_priority("fetchpriority=high") is True
    assert pa._img_is_high_priority('fetchpriority="low"') is False
    assert pa._img_is_high_priority("") is False


def test_img_attr_width_returns_none_on_unparseable(monkeypatch):
    """The regex only matches digits, so a TypeError/ValueError on
    int() conversion is defensive. Hit the except branch by feeding
    the helper a contrived regex match via a monkeypatch."""

    class FakeMatch:
        def group(self, n):
            return "abc" if n == 1 else None  # not a digit

    fake_re = type("FakeRE", (), {"search": lambda self, s: FakeMatch()})()
    monkeypatch.setattr(pa, "_IMG_WIDTH_ANY_RE", fake_re)
    assert pa._img_attr_width('width="abc"') is None


def test_wrap_cdn_images_returns_unchanged_when_src_sub_fails(monkeypatch):
    """If _IMG_SRC_ANY_RE.subn returns 0 substitutions (defensive
    bail-out at L363), the original match is returned untouched."""

    # Patch the SRC regex to never substitute even though attribute
    # matching succeeded. This simulates a corrupted attr string the
    # outer regex matched but the inner sub couldn't replace.
    class FakeRE:
        def __init__(self, inner):
            self._inner = inner

        def search(self, s):
            return self._inner.search(s)

        def subn(self, repl, attrs, count=1):
            return attrs, 0  # report zero substitutions

    monkeypatch.setattr(pa, "_IMG_SRC_ANY_RE", FakeRE(pa._IMG_SRC_ANY_RE))
    html = '<img src="https://cloudcdn.pro/stocks/images/foo.webp" width="600">'
    out, n = pb.wrap_cdn_images_in_transform(html)
    assert n == 0
    assert out == html


# ---------------------------------------------------------------------------
# strip_redundant_link_titles — WAVE alert remediation
# ---------------------------------------------------------------------------


def test_strip_redundant_title_when_title_matches_text():
    html = '<a href="/x" title="Hello">Hello</a>'
    out, n = pb.strip_redundant_link_titles(html)
    assert n == 1
    assert out == '<a href="/x">Hello</a>'


def test_keep_title_when_it_carries_extra_signal():
    html = '<a href="/x" title="Hello world">Hello</a>'
    out, n = pb.strip_redundant_link_titles(html)
    assert n == 0
    assert 'title="Hello world"' in out


def test_strip_normalises_whitespace_and_trailing_punct():
    html = '<a href="/x" title="Hello.">Hello</a>  <a href="/y" title="Foo  bar">Foo bar</a>'
    out, n = pb.strip_redundant_link_titles(html)
    assert n == 2
    assert 'title="Hello."' not in out
    assert 'title="Foo  bar"' not in out


def test_strip_leaves_links_without_title_alone():
    html = '<a href="/x">just text</a>'
    out, n = pb.strip_redundant_link_titles(html)
    assert n == 0
    assert out == html


def test_strip_handles_multiple_attrs_around_title():
    html = '<a href="/x" class="card" title="Same" rel="external">Same</a>'
    out, n = pb.strip_redundant_link_titles(html)
    assert n == 1
    assert 'title="Same"' not in out
    assert 'class="card"' in out
    assert 'rel="external"' in out


def test_strip_skips_empty_title():
    html = '<a href="/x" title="">empty</a>'
    _out, n = pb.strip_redundant_link_titles(html)
    assert n == 0


def test_strip_skips_anchor_with_no_inner_text_match_form():
    """Anchors with nested HTML (e.g. <a><img></a>) are skipped — the
    visible-text comparison would lie."""
    html = '<a href="/x" title="alt"><img alt="alt"></a>'
    _out, n = pb.strip_redundant_link_titles(html)
    assert n == 0
