"""Tests for scripts/validate_jsonld.py — structured-data + feed validator.

We exercise the specific regression classes the validator was built to
catch, so any future change that loosens the gate breaks a test.
"""

from __future__ import annotations

import validate_jsonld as v

# ---------------------------------------------------------------------------
# Structured-data pass (HTML JSON-LD)
# ---------------------------------------------------------------------------


GOOD_HTML = """<!doctype html>
<html>
  <head>
    <meta http-equiv="Content-Security-Policy"
          content="default-src 'self'; script-src 'self' 'sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA='">
    <script type="application/ld+json">
{"@context":"https://schema.org","@type":"BlogPosting","headline":"x","author":{"@type":"Person","name":"a"},"datePublished":"2026-01-01"}
    </script>
  </head>
  <body>
    <nav class="article-tags"></nav>
    <div class="article-meta"></div>
    <aside class="author-card"></aside>
    <nav class="post-pagination"></nav>
  </body>
</html>
"""


def write(tmp_path, name, body):
    p = tmp_path / name
    p.write_text(body, encoding="utf-8")
    return p


def test_jsonld_valid_clean(tmp_path):
    p = write(tmp_path, "ok.html", GOOD_HTML)
    errors, warnings = v.validate_page(p)
    assert errors == []
    assert warnings == []


def test_jsonld_invalid_json_caught(tmp_path):
    html = GOOD_HTML.replace('"x"', '"x",,')  # extra comma
    p = write(tmp_path, "bad.html", html)
    errors, _ = v.validate_page(p)
    assert any("invalid JSON" in e for e in errors)


def test_jsonld_missing_required_caught(tmp_path):
    html = GOOD_HTML.replace('"datePublished":"2026-01-01"', '"x":"y"')
    p = write(tmp_path, "miss.html", html)
    errors, _ = v.validate_page(p)
    assert any("missing required" in e and "datePublished" in e for e in errors)


def test_jsonld_empty_url_caught(tmp_path):
    html = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"ImageObject","url":""}
</script>"""
    p = write(tmp_path, "img.html", html)
    errors, _ = v.validate_page(p)
    assert any("ImageObject.url is empty" in e for e in errors)


def test_jsonld_unresolved_template_caught(tmp_path):
    html = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BlogPosting","headline":"{{title}}","author":{"@type":"Person","name":"a"},"datePublished":"2026-01-01"}
</script>"""
    p = write(tmp_path, "tpl.html", html)
    errors, _ = v.validate_page(p)
    assert any("unresolved template" in e for e in errors)


def test_jsonld_id_only_reference_not_flagged(tmp_path):
    # {"@type":"WebPage","@id":"…"} is a pointer, not a node definition,
    # so the required-field check must not fire.
    html = """<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA='">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BlogPosting","headline":"x","author":{"@type":"Person","name":"a"},"datePublished":"2026-01-01","mainEntityOfPage":{"@type":"WebPage","@id":"https://example.com/"}}
</script>
<nav class="article-tags"></nav>
<div class="article-meta"></div>
<aside class="author-card"></aside>
<nav class="post-pagination"></nav>"""
    p = write(tmp_path, "ref.html", html)
    errors, _ = v.validate_page(p)
    assert errors == []


def test_jsonld_comments_with_script_tag_not_matched(tmp_path):
    # The build template carries a documentation comment that literally
    # contains the string "<script type="application/ld+json">". The
    # validator must strip comments before scanning, otherwise it
    # double-counts the documentation as a real block.
    html = (
        """<!-- example: <script type="application/ld+json"> -->
"""
        + GOOD_HTML
    )
    p = write(tmp_path, "doc.html", html)
    errors, _ = v.validate_page(p)
    assert errors == []


# ---------------------------------------------------------------------------
# Feed pass (XML)
# ---------------------------------------------------------------------------


RSS_GOOD = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Sebastien Rousseau</title>
    <link>https://sebastienrousseau.com</link>
    <description>AI, payments, and post-quantum cryptography research.</description>
    <item>
      <title>A Post</title>
      <link>https://sebastienrousseau.com/a-post/</link>
      <guid isPermaLink="true">https://sebastienrousseau.com/a-post/</guid>
      <description>This is a real description that's long enough.</description>
      <pubDate>Mon, 11 May 2026 06:06:06 +0000</pubDate>
    </item>
  </channel>
</rss>
"""


def test_feed_rss_clean(tmp_path):
    p = write(tmp_path, "rss.xml", RSS_GOOD)
    errors, warnings = v.validate_feed(p)
    assert errors == []
    # Warnings are content quality; the canonical fixture has none.
    assert warnings == []


def test_feed_rss_catches_localhost_url(tmp_path):
    bad = RSS_GOOD.replace("https://sebastienrousseau.com/a-post/", "http://127.0.0.1:8000/.meta/")
    p = write(tmp_path, "rss.xml", bad)
    errors, _ = v.validate_feed(p)
    assert any("localhost" in e or "dev artefact" in e for e in errors)


def test_feed_rss_catches_meta_path(tmp_path):
    bad = RSS_GOOD.replace(
        "https://sebastienrousseau.com/a-post/",
        "https://sebastienrousseau.com/.meta/index.html",
    )
    p = write(tmp_path, "rss.xml", bad)
    errors, _ = v.validate_feed(p)
    assert any("dev artefact" in e for e in errors)


def test_feed_rss_catches_duplicate_guid(tmp_path):
    duplicate = RSS_GOOD.replace(
        "</channel>",
        """    <item>
      <title>Second Post</title>
      <link>https://sebastienrousseau.com/b-post/</link>
      <guid isPermaLink="true">https://sebastienrousseau.com/a-post/</guid>
      <description>Another long-enough description for the test.</description>
    </item>
  </channel>""",
    )
    p = write(tmp_path, "rss.xml", duplicate)
    errors, _ = v.validate_feed(p)
    assert any("duplicate <guid>" in e for e in errors)


def test_feed_rss_invalid_xml_caught(tmp_path):
    # Bare `&` in title — the exact regression Static Site Generator shipped.
    bad = RSS_GOOD.replace("<title>A Post</title>", "<title>A & Post</title>")
    p = write(tmp_path, "rss.xml", bad)
    errors, _ = v.validate_feed(p)
    assert any("XML parse failed" in e for e in errors)


SITEMAP_GOOD = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://sebastienrousseau.com/</loc>
    <lastmod>2026-05-13</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
"""


def test_feed_sitemap_clean(tmp_path):
    p = write(tmp_path, "sitemap.xml", SITEMAP_GOOD)
    errors, warnings = v.validate_feed(p)
    assert errors == []
    assert warnings == []


def test_feed_sitemap_relative_url_fails(tmp_path):
    bad = SITEMAP_GOOD.replace("https://sebastienrousseau.com/", "/relative-only/")
    p = write(tmp_path, "sitemap.xml", bad)
    errors, _ = v.validate_feed(p)
    assert any("not an absolute URL" in e for e in errors)


def test_feed_sitemap_invalid_changefreq_warns(tmp_path):
    bad = SITEMAP_GOOD.replace(
        "<changefreq>weekly</changefreq>", "<changefreq>sometimes</changefreq>"
    )
    p = write(tmp_path, "sitemap.xml", bad)
    _, warnings = v.validate_feed(p)
    assert any("changefreq" in w and "spec" in w for w in warnings)


def test_feed_sitemap_priority_out_of_range_warns(tmp_path):
    bad = SITEMAP_GOOD.replace("<priority>1.0</priority>", "<priority>3.0</priority>")
    p = write(tmp_path, "sitemap.xml", bad)
    _, warnings = v.validate_feed(p)
    assert any("priority" in w and "0.0" in w for w in warnings)


def test_url_taint_helper_catches_meta_path():
    errs: list[str] = []
    v._check_url_taint("label", "https://example.com/.meta/foo", errs)
    assert any("dev artefact" in e for e in errs)


def test_url_taint_helper_passes_clean_url():
    errs: list[str] = []
    v._check_url_taint("label", "https://sebastienrousseau.com/clean/", errs)
    assert errs == []


# ---------------------------------------------------------------------------
# Meta-CSP defence-in-depth (catches the "meta CSP accidentally removed"
# failure mode that would otherwise silently allow inline scripts via the
# HTTP-header 'unsafe-inline' carve-out).
# ---------------------------------------------------------------------------


_GOOD_META_CSP_HTML = """<!doctype html>
<html><head>
<meta http-equiv="Content-Security-Policy"
      content="default-src 'self'; script-src 'self' 'sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=' https://www.googletagmanager.com; style-src 'self'">
</head><body></body></html>"""


def test_meta_csp_present_with_hash_passes():
    errs = v.validate_meta_csp(_GOOD_META_CSP_HTML)
    assert errs == []


def test_meta_csp_missing_fails(tmp_path):
    html = """<!doctype html>
<html><head><title>x</title></head><body></body></html>"""
    errs = v.validate_meta_csp(html)
    assert any("meta CSP missing" in e for e in errs)


def test_meta_csp_unsafe_inline_in_script_src_fails():
    html = _GOOD_META_CSP_HTML.replace(
        "'sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA='",
        "'unsafe-inline'",
    )
    errs = v.validate_meta_csp(html)
    assert any("'unsafe-inline'" in e for e in errs)


def test_meta_csp_without_sha256_hash_fails():
    html = _GOOD_META_CSP_HTML.replace(
        " 'sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA='",
        "",
    )
    errs = v.validate_meta_csp(html)
    assert any("sha256-" in e for e in errs)


def test_meta_csp_no_script_src_directive_fails():
    html = """<!doctype html>
<html><head>
<meta http-equiv="Content-Security-Policy" content="default-src 'self'">
</head><body></body></html>"""
    errs = v.validate_meta_csp(html)
    assert any("no script-src" in e for e in errs)


def test_meta_csp_attribute_order_does_not_matter():
    # Static Site Generator's minifier sometimes emits `content=` before `http-equiv=`.
    # Both orderings must be recognised.
    html = """<!doctype html>
<html><head>
<meta content="default-src 'self'; script-src 'self' 'sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA='"
      http-equiv="Content-Security-Policy">
</head><body></body></html>"""
    errs = v.validate_meta_csp(html)
    assert errs == []


def test_validate_page_propagates_meta_csp_failure(tmp_path):
    # A page with JSON-LD but NO meta CSP must fail validate_page (so the
    # build breaks on accidental meta-CSP removal even when JSON-LD looks
    # otherwise correct).
    html = """<!doctype html>
<html><head><title>x</title>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BlogPosting","headline":"x","author":{"@type":"Person","name":"a"},"datePublished":"2026-01-01"}
</script>
</head></html>"""
    p = tmp_path / "no-csp.html"
    p.write_text(html, encoding="utf-8")
    errors, _ = v.validate_page(p)
    assert any("meta CSP missing" in e for e in errors)


def test_validate_page_passes_when_csp_and_jsonld_both_correct(tmp_path):
    p = tmp_path / "ok.html"
    # GOOD_META_CSP_HTML + add a valid BlogPosting JSON-LD block.
    html = _GOOD_META_CSP_HTML.replace(
        "</head>",
        """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BlogPosting","headline":"x","author":{"@type":"Person","name":"a"},"datePublished":"2026-01-01"}
</script></head>""",
    ) + (
        '<nav class="article-tags"></nav>'
        '<div class="article-meta"></div>'
        '<aside class="author-card"></aside>'
        '<nav class="post-pagination"></nav>'
    )
    p.write_text(html, encoding="utf-8")
    errors, _ = v.validate_page(p)
    assert errors == []
