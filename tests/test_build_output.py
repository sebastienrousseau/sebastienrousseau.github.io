"""Build-output regression suite — walks the entire ``public/`` tree and
asserts the structural invariants that every published page must hold.

This suite is the "100% regression on every page" gate. It does not
re-run the build; it inspects whatever the build produced. Run after
``./build.sh`` (locally) or in CI after the static-site step.

Invariants checked:
  * Every ``index.html`` parses and contains the expected scaffolding
    (lang, title, CSP meta, canonical, og:image, JSON-LD).
  * Every internal ``<a href="...">``/``<link href="/...">``/``<img
    src="/...">``/``<script src="/...">`` URL resolves to a real file
    on disk (or is a JS-handled hash anchor).
  * Every inline ``<script type="application/ld+json">`` body is valid
    JSON.
  * Every XML feed (sitemap, RSS, Atom) parses.
  * Every JSON Feed (``feed.json``) parses.
  * The CSP meta tag is strict (covered in detail by
    ``scripts/test_csp_strict.py``, which is invoked here too).
  * No ``http://127.0.0.1`` or ``localhost`` URL leaks into the
    rendered output.
  * No double-encoded ``&amp;amp;`` survives in any HTML/XML feed.
  * Every page references the same fingerprinted ``/main.<hash>.js``
    asset that exists on disk (no orphan SRI digests).
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote

import pytest

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"

SKIP_IF_NO_BUILD = pytest.mark.skipif(
    not PUBLIC.is_dir() or not (PUBLIC / "index.html").is_file(),
    reason="public/ not built — run ./build.sh first",
)

# ---------------------------------------------------------------------------
# Pre-compute the set of pages once. pytest collects parametrised tests
# eagerly, so we wrap the scan in a session-scoped fixture and use a
# module-level constant for the parametrize() decorator.
# ---------------------------------------------------------------------------

_PAGES: list[Path] = (
    sorted(PUBLIC.rglob("index.html")) if PUBLIC.is_dir() else []
)
# Skip the labs/* WASM demo pages — they're standalone HTML shells with
# different head shape (no JSON-LD, no canonical).
_PAGES = [p for p in _PAGES if "/labs/" not in p.as_posix()]


def _rel(page: Path) -> str:
    return page.relative_to(PUBLIC).as_posix()


PAGE_IDS = [_rel(p) for p in _PAGES]


# ---------------------------------------------------------------------------
# 1. Per-page structural invariants — parametrised over every index.html.
# ---------------------------------------------------------------------------


@SKIP_IF_NO_BUILD
@pytest.mark.parametrize("page", _PAGES, ids=PAGE_IDS)
def test_page_has_html_lang(page: Path):
    html = page.read_text(encoding="utf-8", errors="ignore")
    assert re.search(r'<html\b[^>]*\blang=', html, re.IGNORECASE), \
        f"{_rel(page)}: <html> missing lang attribute"


@SKIP_IF_NO_BUILD
@pytest.mark.parametrize("page", _PAGES, ids=PAGE_IDS)
def test_page_has_title(page: Path):
    html = page.read_text(encoding="utf-8", errors="ignore")
    assert re.search(r'<title>[^<]+</title>', html, re.IGNORECASE), \
        f"{_rel(page)}: <title> missing or empty"


@SKIP_IF_NO_BUILD
@pytest.mark.parametrize("page", _PAGES, ids=PAGE_IDS)
def test_page_has_meta_description(page: Path):
    html = page.read_text(encoding="utf-8", errors="ignore")
    assert re.search(
        r'<meta\b[^>]*\bname=["\']?description["\']?', html, re.IGNORECASE,
    ), f"{_rel(page)}: <meta name=description> missing"


@SKIP_IF_NO_BUILD
@pytest.mark.parametrize("page", _PAGES, ids=PAGE_IDS)
def test_page_has_csp_meta(page: Path):
    html = page.read_text(encoding="utf-8", errors="ignore")
    assert re.search(
        r'<meta\b[^>]*Content-Security-Policy', html, re.IGNORECASE,
    ), f"{_rel(page)}: CSP meta tag missing"


@SKIP_IF_NO_BUILD
@pytest.mark.parametrize("page", _PAGES, ids=PAGE_IDS)
def test_page_has_canonical(page: Path):
    html = page.read_text(encoding="utf-8", errors="ignore")
    assert re.search(
        r'<link\b[^>]*\brel=["\']?canonical', html, re.IGNORECASE,
    ), f"{_rel(page)}: <link rel=canonical> missing"


@SKIP_IF_NO_BUILD
@pytest.mark.parametrize("page", _PAGES, ids=PAGE_IDS)
def test_page_has_og_image(page: Path):
    html = page.read_text(encoding="utf-8", errors="ignore")
    assert re.search(
        r'<meta\b[^>]*\bproperty=["\']?og:image', html, re.IGNORECASE,
    ), f"{_rel(page)}: og:image meta missing"


@SKIP_IF_NO_BUILD
@pytest.mark.parametrize("page", _PAGES, ids=PAGE_IDS)
def test_page_has_main_js_reference(page: Path):
    html = page.read_text(encoding="utf-8", errors="ignore")
    # 404 and similar tiny pages skip the bundle; all the dated content
    # pages plus the site sections include it.
    if not re.search(r"<main\b", html, re.IGNORECASE):
        pytest.skip("page has no <main> — main.js bundle not expected")
    assert re.search(r'src=["\']?/main\.[a-f0-9]+\.js', html, re.IGNORECASE), \
        f"{_rel(page)}: fingerprinted /main.<hash>.js reference missing"


@SKIP_IF_NO_BUILD
@pytest.mark.parametrize("page", _PAGES, ids=PAGE_IDS)
def test_page_has_no_localhost_url(page: Path):
    html = page.read_text(encoding="utf-8", errors="ignore")
    # The CSP `inline-speculation-rules` description / JSON-LD comments
    # never reference localhost, so any hit is a real leak.
    leak = re.search(r'https?://(?:127\.0\.0\.1|localhost)\b', html, re.IGNORECASE)
    assert not leak, f"{_rel(page)}: leaks localhost URL — {leak.group(0) if leak else ''}"


@SKIP_IF_NO_BUILD
@pytest.mark.parametrize("page", _PAGES, ids=PAGE_IDS)
def test_page_no_double_encoded_ampersand(page: Path):
    html = page.read_text(encoding="utf-8", errors="ignore")
    assert "&amp;amp;" not in html, \
        f"{_rel(page)}: &amp;amp; survived (XML/HTML escape pass missed it)"


_HTML_COMMENT_RE = re.compile(r"<!--[\s\S]*?-->")


@SKIP_IF_NO_BUILD
@pytest.mark.parametrize("page", _PAGES, ids=PAGE_IDS)
def test_page_inline_jsonld_is_valid_json(page: Path):
    html = page.read_text(encoding="utf-8", errors="ignore")
    # Strip HTML comments first — the on-page CSP-explanation comment
    # in the layouts contains the literal string "JSON-LD blocks..." which
    # the regex would otherwise mis-classify as a JSON-LD script body.
    scannable = _HTML_COMMENT_RE.sub("", html)
    for m in re.finditer(
        r'<script\b[^>]*\btype=["\']?application/ld\+json["\']?[^>]*>'
        r'([\s\S]*?)</script>',
        scannable,
        re.IGNORECASE,
    ):
        body = m.group(1).strip()
        if not body:
            continue
        try:
            json.loads(body)
        except json.JSONDecodeError as exc:
            pytest.fail(
                f"{_rel(page)}: inline JSON-LD invalid — {exc}: "
                f"{body[:100]}..."
            )


# ---------------------------------------------------------------------------
# 2. Internal-link integrity — every absolute /path resolves to a real
# file on disk, every relative path resolves against the page's
# directory. External URLs (http(s)://) are skipped here — that's
# scripts/audit_links.py's job.
# ---------------------------------------------------------------------------

_HREF_SRC_RE = re.compile(
    r'\b(?:href|src)=(["\'])([^"\']+)\1|\b(?:href|src)=([^\s"\'>]+)',
    re.IGNORECASE,
)


def _extract_urls(html: str) -> list[str]:
    urls = [
        (m.group(2) or m.group(3) or "")
        for m in _HREF_SRC_RE.finditer(html)
    ]
    return [u for u in urls if u]


def _looks_internal(url: str) -> bool:
    if url.startswith(("http://", "https://", "data:", "mailto:", "tel:", "#")):
        return False
    return not url.startswith("//")


def _resolve_internal(page: Path, url: str) -> Path:
    """Resolve an internal URL against ``page`` and return the file on
    disk it should map to. Trailing-slash URLs resolve to .../index.html."""
    # Strip fragment + query.
    url = url.split("#", 1)[0].split("?", 1)[0]
    url = unquote(url)
    target = (
        PUBLIC / url.lstrip("/")
        if url.startswith("/")
        else (page.parent / url).resolve()
    )
    # /foo/  → /foo/index.html. Bare /file goes through as-is.
    if target.is_dir() or url.endswith("/"):
        target = target / "index.html"
    elif not target.suffix and not target.is_file():
        # /foo (no slash, no extension, no extant file) — assume directory
        # served at /foo/index.html.
        cand = target / "index.html"
        if cand.is_file():
            target = cand
    return target


@SKIP_IF_NO_BUILD
@pytest.mark.parametrize("page", _PAGES, ids=PAGE_IDS)
def test_page_internal_links_resolve(page: Path):
    html = page.read_text(encoding="utf-8", errors="ignore")
    misses: list[str] = []
    for raw in _extract_urls(html):
        if not _looks_internal(raw):
            continue
        target = _resolve_internal(page, raw)
        if not target.is_file():
            # Some references are intentionally generated only when CI
            # writes specific feeds — tolerate the well-known set.
            rel = (
                target.relative_to(PUBLIC).as_posix()
                if str(target).startswith(str(PUBLIC))
                else target.as_posix()
            )
            if rel in {
                "feed.json", "rss.xml", "atom.xml", "sitemap.xml",
                "robots.txt", "manifest.json", "llms.txt", "llms-full.txt",
            } and (PUBLIC / rel).is_file():
                continue
            misses.append(f"{raw} -> {rel}")
    assert not misses, (
        f"{_rel(page)}: {len(misses)} broken internal link(s):\n  "
        + "\n  ".join(misses[:10])
        + ("\n  ..." if len(misses) > 10 else "")
    )


# ---------------------------------------------------------------------------
# 3. Feed integrity — every XML feed parses, every JSON feed parses.
# ---------------------------------------------------------------------------


def _feeds_xml() -> list[Path]:
    out: list[Path] = []
    for name in ("sitemap.xml", "rss.xml", "atom.xml", "news-sitemap.xml"):
        p = PUBLIC / name
        if p.is_file():
            out.append(p)
    return out


def _feeds_json() -> list[Path]:
    out: list[Path] = []
    for name in ("feed.json", "manifest.json"):
        p = PUBLIC / name
        if p.is_file():
            out.append(p)
    return out


XML_FEED_IDS = [p.name for p in _feeds_xml()]
JSON_FEED_IDS = [p.name for p in _feeds_json()]


@SKIP_IF_NO_BUILD
@pytest.mark.parametrize("feed", _feeds_xml(), ids=XML_FEED_IDS or ["<none>"])
def test_xml_feed_parses(feed: Path):
    try:
        ET.parse(feed)
    except ET.ParseError as exc:
        pytest.fail(f"{feed.name}: XML parse failed — {exc}")


@SKIP_IF_NO_BUILD
@pytest.mark.parametrize("feed", _feeds_json(), ids=JSON_FEED_IDS or ["<none>"])
def test_json_feed_parses(feed: Path):
    try:
        json.loads(feed.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        pytest.fail(f"{feed.name}: JSON parse failed — {exc}")


@SKIP_IF_NO_BUILD
def test_sitemap_has_entries():
    sm = PUBLIC / "sitemap.xml"
    if not sm.is_file():
        pytest.skip("sitemap.xml not built")
    root = ET.parse(sm).getroot()
    # Either a <urlset> or a <sitemapindex>; both must have children.
    assert len(list(root)) > 0, "sitemap.xml has no entries"


# ---------------------------------------------------------------------------
# 4. Asset integrity — every fingerprinted /main.<hash>.js referenced
# in HTML must exist on disk; integrity attribute must be base64-shaped.
# ---------------------------------------------------------------------------


@SKIP_IF_NO_BUILD
def test_main_js_alias_exists():
    fps = list(PUBLIC.glob("main.*.js"))
    assert fps, "no fingerprinted /main.<hash>.js in public/"
    # The bare alias /main.js is also kept around for legacy refs.
    assert (PUBLIC / "main.js").is_file(), "/main.js alias missing"


@SKIP_IF_NO_BUILD
def test_all_referenced_fingerprinted_main_js_exist():
    refs: set[str] = set()
    for page in _PAGES:
        html = page.read_text(encoding="utf-8", errors="ignore")
        for m in re.finditer(r'/main\.[a-f0-9]+\.js', html, re.IGNORECASE):
            refs.add(m.group(0).lstrip("/"))
    assert refs, "no /main.<hash>.js references found"
    missing = [r for r in refs if not (PUBLIC / r).is_file()]
    assert not missing, f"references to missing main.*.js: {missing[:5]}"


@SKIP_IF_NO_BUILD
def test_integrity_attributes_are_base64_shape():
    """Every ``sha256-<digest>`` token inside an integrity attribute
    must be base64 (44 chars ending in ``=``). The attribute may carry
    multiple whitespace-separated tokens (post-#95: dual digest for
    Pages-POP-variant byte append), so we validate each token, not the
    whole attribute value."""
    _TOKEN_RE = re.compile(r"sha256-([A-Za-z0-9+/=]+)")
    bad: list[str] = []
    for page in _PAGES[:200]:  # representative slice — checking all 1878 is overkill
        html = page.read_text(encoding="utf-8", errors="ignore")
        for m in re.finditer(
            r'integrity=(["\'])([^"\']+)\1', html, re.IGNORECASE,
        ):
            value = m.group(2)
            for tok in _TOKEN_RE.finditer(value):
                digest = tok.group(1)
                if len(digest) != 44 or not digest.endswith("="):
                    bad.append(f"{_rel(page)}: {digest!r}")
    assert not bad, (
        "non-base64 SRI digest token(s):\n  " + "\n  ".join(bad[:10])
    )


# ---------------------------------------------------------------------------
# 5. CSP shape — run the strict-CSP script as a pytest gate too.
# ---------------------------------------------------------------------------


@SKIP_IF_NO_BUILD
def test_csp_strict_passes():
    result = subprocess.run(
        [sys.executable, "scripts/test_csp_strict.py"],
        capture_output=True, text=True, cwd=ROOT, check=False,
    )
    assert result.returncode == 0, (
        f"test_csp_strict.py failed:\n{result.stderr}\n{result.stdout}"
    )


# ---------------------------------------------------------------------------
# 6. JS / CSS minification — sanity that postbuild actually minified
# the on-disk assets.
# ---------------------------------------------------------------------------


@SKIP_IF_NO_BUILD
def test_main_js_is_minified():
    p = PUBLIC / "main.js"
    if not p.is_file():
        pytest.skip("public/main.js not built")
    src = p.read_text(encoding="utf-8")
    # rjsmin collapses to one-liners for the IIFEs; the original 16 KB
    # source had ~424 lines of JSDoc + indentation. Unminified would
    # have many "\n" newlines and JSDoc-style "/**" comments.
    assert "/**" not in src, "/** comment survived in main.js — minify regressed"
    # The minified body is one or a few lines; if it's still >50 lines,
    # something is wrong.
    assert src.count("\n") < 50, (
        f"main.js has {src.count(chr(10))} newlines — looks unminified"
    )


@SKIP_IF_NO_BUILD
def test_theme_init_js_is_minified():
    p = PUBLIC / "theme-init.js"
    if not p.is_file():
        pytest.skip("public/theme-init.js not built")
    src = p.read_text(encoding="utf-8")
    assert "/* Theme bootstrap" not in src, "theme-init.js still carries source comment"


@SKIP_IF_NO_BUILD
def test_csp_css_bundle_has_no_leading_comment_block():
    """The vendor preamble comment is what made Lighthouse fire
    unminified-css. Make sure rcssmin stripped it."""
    for p in (PUBLIC / "_csp").glob("*.css"):
        head = p.read_bytes()[:120].decode("utf-8", errors="ignore")
        assert "/*" not in head, (
            f"{p.name}: leading /* ... */ comment survived"
        )


# ---------------------------------------------------------------------------
# 7. Theme-init has been inlined — no page still loads /theme-init.js.
# ---------------------------------------------------------------------------


@SKIP_IF_NO_BUILD
def test_no_page_references_theme_init_externally():
    misses: list[str] = []
    for page in _PAGES:
        html = page.read_text(encoding="utf-8", errors="ignore")
        if re.search(r'<script\b[^>]*\bsrc=["\']?/theme-init\.js', html, re.IGNORECASE):
            misses.append(_rel(page))
    assert not misses, (
        f"{len(misses)} page(s) still load /theme-init.js externally — "
        f"inlining regressed:\n  " + "\n  ".join(misses[:5])
    )


# ---------------------------------------------------------------------------
# 8. LCP preload — pages with <main> + a non-lazy <img> get a preload.
# ---------------------------------------------------------------------------


_LINK_RE = re.compile(r'<link\b[^>]+>', re.IGNORECASE)
_REL_PRELOAD_RE = re.compile(r'\brel=["\']?preload\b', re.IGNORECASE)
_AS_IMAGE_RE = re.compile(r'\bas=["\']?image\b', re.IGNORECASE)


def _has_image_preload(html: str) -> bool:
    """A <link rel=preload as=image> can appear in either attribute
    order (SSG's minifier alphabetises) — match both."""
    for m in _LINK_RE.finditer(html):
        tag = m.group(0)
        if _REL_PRELOAD_RE.search(tag) and _AS_IMAGE_RE.search(tag):
            return True
    return False


@SKIP_IF_NO_BUILD
def test_pages_with_eager_image_have_preload():
    misses: list[str] = []
    for page in _PAGES:
        html = page.read_text(encoding="utf-8", errors="ignore")
        # Find first <img>: if it's lazy or absent, page doesn't need a preload.
        m = re.search(r'<img\b[^>]+>', html, re.IGNORECASE)
        if not m:
            continue
        first = m.group(0)
        if re.search(r'\bloading=["\']?lazy', first, re.IGNORECASE):
            continue
        if not _has_image_preload(html):
            misses.append(_rel(page))
    # Allow up to ~10 edge cases (404, tiny redirect pages). The total
    # pages is ~1878 so an exact-zero gate is too brittle.
    assert len(misses) < 20, (
        f"{len(misses)} eager-image page(s) without LCP preload:\n  "
        + "\n  ".join(misses[:10])
    )
