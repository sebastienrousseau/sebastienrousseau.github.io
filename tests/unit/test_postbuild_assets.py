"""Tests for the postbuild asset passes — stylesheet sanitising,
image dimensions, asset fingerprints, speculation rules, and the
hero banner.

Split out of test_postbuild.py; tests are verbatim copies.
"""

from __future__ import annotations

import postbuild as pb

# ---------------------------------------------------------------------------
# Stylesheet sanitizer — `_sanitize_link_tag` + `hoist_body_link_stylesheets`
# ---------------------------------------------------------------------------


def test_sanitize_link_tag_collapses_duplicate_crossorigin():
    from postbuild_lib.html_passes import _sanitize_link_tag

    tag = '<link rel="stylesheet" href="/x.css" crossorigin="anonymous" crossorigin="anonymous">'
    out = _sanitize_link_tag(tag)
    assert out.count('crossorigin="anonymous"') == 1


def test_sanitize_link_tag_strips_trailing_double_quote():
    from postbuild_lib.html_passes import _sanitize_link_tag

    tag = '<link rel="stylesheet" href="/x.css" crossorigin="anonymous"">'
    out = _sanitize_link_tag(tag)
    # Two adjacent quotes before `>` are collapsed to one
    assert '""' not in out


def test_hoist_body_link_stylesheets_moves_to_head():
    from postbuild_lib.html_passes import hoist_body_link_stylesheets

    html = (
        '<head><meta charset="utf-8"></head>'
        '<body><main><link rel="stylesheet" href="/widget.css"></main></body>'
    )
    out, n = hoist_body_link_stylesheets(html)
    assert n == 1
    # Stylesheet now in head, not in body
    head_end = out.find("</head>")
    body_start = out.find("<body>")
    sheet = out.find('href="/widget.css"')
    assert sheet < head_end < body_start


def test_hoist_body_link_stylesheets_no_op_when_already_in_head():
    from postbuild_lib.html_passes import hoist_body_link_stylesheets

    html = '<head><link rel="stylesheet" href="/x.css"></head><body><main></main></body>'
    _, n = hoist_body_link_stylesheets(html)
    assert n == 0


def test_hoist_body_link_stylesheets_no_op_without_head_tag():
    """A page without ``</head>`` → no hoisting possible (line 853)."""
    from postbuild_lib.html_passes import hoist_body_link_stylesheets

    html = '<body><link rel="stylesheet" href="/x.css"></body>'
    out, n = hoist_body_link_stylesheets(html)
    assert n == 0
    assert out == html


# ---------------------------------------------------------------------------
# inject_speculation_rules
# ---------------------------------------------------------------------------


def test_inject_speculation_rules_no_op_when_already_present():
    from postbuild_lib.content_blocks import inject_speculation_rules

    html = '<head><script type="speculationrules">{}</script></head>'
    assert inject_speculation_rules(html) == html


def test_inject_speculation_rules_inserts_when_missing():
    from postbuild_lib.content_blocks import inject_speculation_rules

    html = '<head><meta charset="utf-8"></head><body></body>'
    out = inject_speculation_rules(html)
    assert '<script type="speculationrules">' in out


# ---------------------------------------------------------------------------
# stamp_image_dimensions — width/height + fetchpriority for LCP / lazy below
# ---------------------------------------------------------------------------


def test_stamp_image_dimensions_first_image_gets_fetchpriority_high():
    html = '<body><img src="https://example.com/banner.webp" alt="x"></body>'
    out, n = pb.stamp_image_dimensions(html)
    assert n == 1
    assert 'fetchpriority="high"' in out
    assert 'width="' in out
    assert 'height="' in out


def test_stamp_image_dimensions_subsequent_images_get_lazy_async():
    html = (
        '<img src="https://example.com/1.webp" alt="hero">'
        '<img src="https://example.com/2.webp" alt="below">'
    )
    out, n = pb.stamp_image_dimensions(html)
    assert n == 2
    first_img = out[: out.find("<img", 5)]
    second_img = out[out.find("<img", 5) :]
    assert 'fetchpriority="high"' in first_img
    assert 'fetchpriority="high"' not in second_img
    assert 'loading="lazy"' in second_img
    assert 'decoding="async"' in second_img


def test_stamp_image_dimensions_uses_known_size_for_personal_portrait():
    """The personal portrait is registered in _IMG_DIMS as 162×162."""
    html = '<img src="https://cloudcdn.pro/stocks/images/sebastienrousseau.webp" alt="x">'
    out, _ = pb.stamp_image_dimensions(html)
    assert 'width="162"' in out
    assert 'height="162"' in out


def test_stamp_image_dimensions_idempotent_when_attrs_already_present():
    """Images that already have w/h/loading/decoding aren't rewritten."""
    html = (
        '<img src="https://cloudcdn.pro/stocks/images/sebastienrousseau.webp" '
        'width="162" height="162" loading="lazy" decoding="async" '
        'fetchpriority="high" alt="x">'
    )
    out, _ = pb.stamp_image_dimensions(html)
    # First-pass idempotent: no duplicated attributes
    assert out.count('width="162"') == 1


def test_stamp_image_dimensions_prefix_map_match():
    """Image whose src matches an ``_IMG_DIMS_PREFIX`` gets that group's size."""
    html = '<img src="https://cloudcdn.pro/clients/alienstudio/portrait.webp">'
    out, _ = pb.stamp_image_dimensions(html)
    assert 'width="800"' in out
    assert 'height="800"' in out


def test_stamp_image_dimensions_default_dimensions_for_unknown_src():
    """Image with a src that matches nothing falls back to _IMG_DEFAULT (1200×675)."""
    html = '<img src="https://example.com/random/photo.webp">'
    out, _ = pb.stamp_image_dimensions(html)
    assert 'width="1200"' in out
    assert 'height="675"' in out


def test_stamp_image_dimensions_first_image_with_fetchpri_no_loading_unchanged():
    """First image with all attrs except ``loading`` set — extras list is empty
    (the LCP image legitimately doesn't need loading), so the tag is returned
    untouched (covers the ``if not extras: return m.group(0)`` branch)."""
    html = (
        '<img src="https://x/banner.webp" width="1200" height="675" '
        'decoding="async" fetchpriority="high">'
    )
    out, n = pb.stamp_image_dimensions(html)
    assert out == html
    assert n == 0


# ---------------------------------------------------------------------------
# Asset-URL fingerprint stamping — guards stale CDN cache after a content change
# ---------------------------------------------------------------------------


def test_stamp_asset_fingerprints_rewrites_main_js():
    """Unquoted ``src=/main.js`` gets rewritten to the fingerprinted name."""
    from unittest.mock import patch

    import postbuild as _pb

    fake_map = {"/main.js": "/main.abc123.js"}
    fake_pat = _pb.re.compile(
        r'(<(?:script|link)\b[^>]*\b(?:src|href)=["\']?)(/main\.js)(["\']?[^>]*>)',
        _pb.re.IGNORECASE,
    )
    with patch.object(_pb, "_FP_ASSET_MAP", fake_map), patch.object(_pb, "_FP_PATTERN", fake_pat):
        out, n = _pb.stamp_asset_fingerprints("<script defer src=/main.js></script>")
        assert n == 1
        assert "/main.abc123.js" in out
        assert "src=/main.js" not in out


def test_stamp_asset_fingerprints_rewrites_quoted_form():
    """Quoted ``src="/main.js"`` also gets rewritten."""
    from unittest.mock import patch

    import postbuild as _pb

    fake_map = {"/main.js": "/main.abc123.js"}
    fake_pat = _pb.re.compile(
        r'(<(?:script|link)\b[^>]*\b(?:src|href)=["\']?)(/main\.js)(["\']?[^>]*>)',
        _pb.re.IGNORECASE,
    )
    with patch.object(_pb, "_FP_ASSET_MAP", fake_map), patch.object(_pb, "_FP_PATTERN", fake_pat):
        out, n = _pb.stamp_asset_fingerprints('<script src="/main.js" defer></script>')
        assert n == 1
        assert 'src="/main.abc123.js"' in out


def test_stamp_asset_fingerprints_leaves_inline_js_untouched():
    """A literal ``/main.js`` inside JS code (not a <script src>) is NOT rewritten."""
    from unittest.mock import patch

    import postbuild as _pb

    fake_map = {"/main.js": "/main.abc123.js"}
    fake_pat = _pb.re.compile(
        r'(<(?:script|link)\b[^>]*\b(?:src|href)=["\']?)(/main\.js)(["\']?[^>]*>)',
        _pb.re.IGNORECASE,
    )
    with patch.object(_pb, "_FP_ASSET_MAP", fake_map), patch.object(_pb, "_FP_PATTERN", fake_pat):
        out, n = _pb.stamp_asset_fingerprints(
            "<script>navigator.serviceWorker.register('/main.js');</script>"
        )
        assert n == 0
        assert "/main.js" in out  # untouched


def test_stamp_asset_fingerprints_no_op_when_pattern_missing():
    """Without a fingerprint map, the pass is a no-op."""
    from unittest.mock import patch

    import postbuild as _pb

    with patch.object(_pb, "_FP_PATTERN", None):
        out, n = _pb.stamp_asset_fingerprints("<script src=/main.js></script>")
        assert n == 0
        assert out == "<script src=/main.js></script>"


def _make_blogposting_with_og(
    *,
    og_image: str = "https://cloudcdn.pro/api/transform?url=/stocks/images/sample.webp&w=1425&format=webp&q=80",
    og_image_alt: str | None = "An editorial banner photograph",
    og_image_width: int | None = 1425,
    og_image_height: int | None = 571,
    h1: str = "Banking Infrastructure Index 2026",
    extra: str = "",
) -> str:
    """Helper: build a minimal page that ``inject_hero_banner`` accepts.

    og:image:width / og:image:height are emitted by the SSG on every
    BlogPosting page from the frontmatter ``banner_width`` / ``banner_height``
    fields. Tests can override the defaults to exercise the natural-aspect
    branch and the fallback-to-canonical branch.
    """
    alt_meta = f'<meta name="twitter:image:alt" content="{og_image_alt}" />' if og_image_alt else ""
    width_meta = (
        f'<meta property="og:image:width" content="{og_image_width}" />'
        if og_image_width is not None
        else ""
    )
    height_meta = (
        f'<meta property="og:image:height" content="{og_image_height}" />'
        if og_image_height is not None
        else ""
    )
    return (
        '<html lang="en-GB"><head>'
        f'<meta property="og:image" content="{og_image}" />'
        f"{width_meta}{height_meta}{alt_meta}"
        "</head><body>"
        '<script type="application/ld+json">'
        '{"@type":"BlogPosting","headline":"X"}'
        "</script>"
        f'<section class="ap-hero"><h1>{h1}</h1></section>'
        f"{extra}"
        '<main><div class="wrap"><p>body</p></div></main>'
        "</body></html>"
    )


def test_inject_hero_banner_happy_path():
    """A BlogPosting with og:image + dims + alt gets a <figure
    class=article-banner> with width/height matching og:image:width/height
    inserted immediately after the closing </section> of ap-hero. The
    natural-aspect reservation is what fixes the lighthouse CLS regression
    on banners that aren't 16:9."""
    from postbuild_lib.content_blocks import inject_hero_banner

    html = _make_blogposting_with_og()  # defaults: 1425×571 = 2.5:1
    out = inject_hero_banner(html)
    assert 'class="article-banner"' in out
    assert 'fetchpriority="high"' in out
    assert 'decoding="async"' in out
    # Banner URL passes through unchanged — postbuild's CDN-transform
    # wrapper later in the pipeline picks the right width from the
    # rendered <img width="..."> attribute.
    figure = out.split('class="article-banner"', 1)[1].split("</figure>", 1)[0]
    assert "w=1425" in figure  # original URL preserved
    # Alt taken from twitter:image:alt meta.
    assert 'alt="An editorial banner photograph"' in out
    # Width/height from og:image:width/og:image:height — natural 2.5:1.
    assert 'width="1425"' in out
    assert 'height="571"' in out


def test_inject_hero_banner_falls_back_to_canonical_dims_when_og_dims_absent():
    """No og:image:width / og:image:height meta → 1200×675 fallback (16:9).
    Older articles without explicit dimensions still get a deterministic
    box reservation."""
    from postbuild_lib.content_blocks import inject_hero_banner

    html = _make_blogposting_with_og(og_image_width=None, og_image_height=None)
    out = inject_hero_banner(html)
    assert 'width="1200"' in out
    assert 'height="675"' in out


def test_inject_hero_banner_falls_back_when_og_dims_are_zero():
    """og:image:width=0 / og:image:height=0 → fallback. Covers the
    ``w > 0 and h > 0`` guard's False branch."""
    from postbuild_lib.content_blocks import _banner_dimensions

    html_zero = (
        '<meta property="og:image:width" content="0" />'
        '<meta property="og:image:height" content="0" />'
    )
    assert _banner_dimensions(html_zero) == (1200, 675)


def test_inject_hero_banner_falls_back_when_only_one_og_dim_present():
    """og:image:width present without og:image:height (or vice versa)
    → fallback. Covers the ``if w_m and h_m:`` guard's False branch
    when only one side of the pair matches."""
    from postbuild_lib.content_blocks import _banner_dimensions

    html_width_only = '<meta property="og:image:width" content="1200" />'
    assert _banner_dimensions(html_width_only) == (1200, 675)
    html_height_only = '<meta property="og:image:height" content="675" />'
    assert _banner_dimensions(html_height_only) == (1200, 675)


def test_inject_hero_banner_falls_back_to_h1_when_alt_missing():
    """No twitter:image:alt meta → use 'Banner for: <H1 title>'."""
    from postbuild_lib.content_blocks import inject_hero_banner

    html = _make_blogposting_with_og(og_image_alt=None, h1="ISO 20022 After Migration")
    out = inject_hero_banner(html)
    assert 'alt="Banner for: ISO 20022 After Migration"' in out


def test_inject_hero_banner_idempotent_when_banner_already_present():
    """A page that already carries ``class="article-banner"`` is left alone."""
    from postbuild_lib.content_blocks import inject_hero_banner

    html = _make_blogposting_with_og(
        extra='<figure class="article-banner"><img src="x.webp" /></figure>',
    )
    out = inject_hero_banner(html)
    assert out == html


def test_inject_hero_banner_no_op_without_blogposting_jsonld():
    """Non-BlogPosting pages (listings, static pages) are skipped."""
    from postbuild_lib.content_blocks import inject_hero_banner

    html = (
        '<html><head><meta property="og:image" content="x.webp" /></head>'
        '<body><section class="ap-hero"><h1>Listings</h1></section>'
        '<main><div class="wrap"></div></main></body></html>'
    )
    out = inject_hero_banner(html)
    assert out == html
    assert 'class="article-banner"' not in out


def test_inject_hero_banner_no_op_when_og_image_missing():
    """BlogPosting page without an og:image meta is left alone."""
    from postbuild_lib.content_blocks import inject_hero_banner

    html = (
        "<html><body>"
        '<script type="application/ld+json">{"@type":"BlogPosting"}</script>'
        '<section class="ap-hero"><h1>X</h1></section>'
        '<main><div class="wrap"></div></main></body></html>'
    )
    out = inject_hero_banner(html)
    assert out == html


def test_inject_hero_banner_non_cdn_url_passes_through_unchanged():
    """Banner URLs that aren't CDN-transform endpoints are still
    inserted into the figure without modification. Width / height come
    from the og:image:* meta tags or the canonical fallback."""
    from postbuild_lib.content_blocks import inject_hero_banner

    raw_url = "https://example.com/static/banner.webp"
    html = _make_blogposting_with_og(og_image=raw_url)
    out = inject_hero_banner(html)
    assert raw_url in out


def test_inject_hero_banner_uses_og_alt_when_twitter_alt_absent():
    """If twitter:image:alt is missing but og:image:alt is present, prefer
    twitter (the helper's default) — and when neither, fall back to H1."""
    from postbuild_lib.content_blocks import inject_hero_banner

    html = (
        "<html><head>"
        '<meta property="og:image" content="https://example.com/x.webp" />'
        '<meta property="og:image:alt" content="The OG alt" />'
        "</head><body>"
        '<script type="application/ld+json">{"@type":"BlogPosting"}</script>'
        '<section class="ap-hero"><h1>Article H1</h1></section>'
        '<main><div class="wrap"></div></main></body></html>'
    )
    out = inject_hero_banner(html)
    assert 'alt="The OG alt"' in out


def test_inject_hero_banner_returns_unchanged_when_anchor_missing():
    """og:image present + BlogPosting marker present, but no </section>
    followed by a sibling element to anchor against → no insertion."""
    from postbuild_lib.content_blocks import inject_hero_banner

    html = (
        "<html><head>"
        '<meta property="og:image" content="https://example.com/x.webp" />'
        "</head><body>"
        '<script type="application/ld+json">{"@type":"BlogPosting"}</script>'
        # NB: no <section class="ap-hero">…</section> at all — the
        # _HERO_BANNER_INSERT_RE anchor can't match.
        "</body></html>"
    )
    out = inject_hero_banner(html)
    assert out == html


def test_inject_hero_banner_strips_legacy_inline_duplicate():
    """Legacy authoring pattern: article whose first body element is a
    ``<p><img></p>`` wrapper carrying the same image as og:image.
    inject_hero_banner injects the figure at the top AND removes the
    inline body duplicate, keeping the new design and dropping the old."""
    from postbuild_lib.content_blocks import inject_hero_banner

    html = (
        "<html><head>"
        '<meta property="og:image" content="https://cloudcdn.pro/stocks/images/traxer-AIKjbZdNOlw.webp" />'
        "</head><body>"
        '<script type="application/ld+json">{"@type":"BlogPosting"}</script>'
        '<section class="ap-hero"><h1>Bitcoin</h1></section>'
        '<main><div class="wrap">'
        '<p><img src="https://cloudcdn.pro/stocks/images/traxer-AIKjbZdNOlw.webp" alt="..." /></p>'
        "<h2>Insight</h2><p>body</p>"
        "</div></main></body></html>"
    )
    out = inject_hero_banner(html)
    # The auto-injected figure is present.
    assert 'class="article-banner"' in out
    # The inline `<p><img></p>` duplicate has been removed.
    assert '<p><img src="https://cloudcdn.pro/stocks/images/traxer-AIKjbZdNOlw.webp"' not in out
    # The image still appears via the article-banner figure; check the
    # path occurs exactly twice (og:image meta + article-banner figure src).
    assert out.count("traxer-AIKjbZdNOlw") == 2


def test_inject_hero_banner_leaves_unrelated_body_images_alone():
    """A `<p><img></p>` whose src is NOT the banner is left in place.
    The strip only fires when the body img matches the og:image path."""
    from postbuild_lib.content_blocks import inject_hero_banner

    html = (
        "<html><head>"
        '<meta property="og:image" content="https://cloudcdn.pro/stocks/images/banner-A.webp" />'
        "</head><body>"
        '<script type="application/ld+json">{"@type":"BlogPosting"}</script>'
        '<section class="ap-hero"><h1>X</h1></section>'
        '<main><div class="wrap">'
        '<p><img src="https://cloudcdn.pro/stocks/images/some-diagram.webp" alt="d" /></p>'
        "</div></main></body></html>"
    )
    out = inject_hero_banner(html)
    assert 'class="article-banner"' in out
    assert "banner-A.webp" in out
    # The unrelated body img survives.
    assert "some-diagram.webp" in out


def test_strip_legacy_inline_banner_helper_branches():
    """_strip_legacy_inline_banner returns the input unchanged on inputs
    that don't have the structure it needs: a URL without a path, no
    </figure> anchor, no <p><img></p> in the body window, or the body
    img doesn't match the banner path. Each False/no-op branch needs
    coverage."""
    from postbuild_lib.content_blocks import _banner_path, strip_legacy_inline_banner

    # Malformed banner URL.
    assert _banner_path("not-a-url") is None
    assert (
        strip_legacy_inline_banner("<figure></figure><p><img src='x' /></p>", "not-a-url")
        == "<figure></figure><p><img src='x' /></p>"
    )
    # No </figure> anchor at all.
    assert (
        strip_legacy_inline_banner(
            "<p><img src='/stocks/images/foo.webp' /></p>",
            "https://cloudcdn.pro/stocks/images/foo.webp",
        )
        == "<p><img src='/stocks/images/foo.webp' /></p>"
    )
    # </figure> present but no <p><img></p> in the window.
    in_html = "<figure></figure><h2>heading</h2><p>no image here</p>"
    assert (
        strip_legacy_inline_banner(
            in_html,
            "https://cloudcdn.pro/stocks/images/foo.webp",
        )
        == in_html
    )
    # </figure> present + <p><img></p> present but src doesn't match.
    in_html = '<figure></figure><p><img src="https://cloudcdn.pro/stocks/images/other.webp" /></p>'
    assert (
        strip_legacy_inline_banner(
            in_html,
            "https://cloudcdn.pro/stocks/images/foo.webp",
        )
        == in_html
    )
