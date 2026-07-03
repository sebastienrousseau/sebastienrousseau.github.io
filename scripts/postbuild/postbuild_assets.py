"""Asset-processing passes (leaf): JS/CSS minification, subresource-integrity
hashes, asset fingerprinting, CDN image-transform rewriting, and LCP preload
injection. Split from postbuild (Phase 4.1).

Self-contained: stdlib + a local PUBLIC only. postbuild imports the pass
entry points back; the fingerprint map/pattern live here (move-only state).
"""

from __future__ import annotations

import base64
import hashlib
import re
from pathlib import Path

import rcssmin
import rjsmin

PUBLIC = Path("public")

def b64_sha256(data: bytes) -> str:
    return base64.b64encode(hashlib.sha256(data).digest()).decode("ascii")
def _ensure_trailing_newline(s: str) -> str:
    """GitHub Pages / Fastly append a ``\\n`` to text assets in flight,
    which silently shifts the on-the-wire SHA-256 by one byte and
    breaks any SRI tag computed against the on-disk bytes. Pin the
    newline at build time so disk == wire."""
    return s if s.endswith("\n") else s + "\n"
def _minify_one(p: Path) -> tuple[int, int]:
    """Minify ``p`` in place + ensure a trailing newline. Returns
    ``(bytes_before, bytes_after)``; ``(0, 0)`` if neither the
    minification nor the newline-stamp changed the file.

    GitHub Pages / Fastly append a ``\\n`` to text assets in flight,
    so we pin it here — otherwise SRI computed against the on-disk
    bytes diverges from what the browser fetches and the script gets
    blocked."""
    try:
        src = p.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return 0, 0
    candidate = _ensure_trailing_newline(rjsmin.jsmin(src))
    # Pick the smaller of (minified+nl) and (original+nl). If neither
    # is shorter than the source, keep the source — but still stamp the
    # trailing newline so the on-disk hash matches on-the-wire.
    out = candidate if len(candidate) < len(src) else _ensure_trailing_newline(src)
    if out == src:
        return 0, 0
    p.write_text(out, encoding="utf-8")
    return len(src), len(out)
def _gather_js_targets() -> list[Path]:
    """Top-level public/*.js + service-worker + theme bootstrap.
    Excludes /_csp/* (SSG already minifies; SRI is hash-pinned by us
    afterwards) and /labs/* (wasm-pack output, may contain non-ASCII
    identifiers)."""
    out: list[Path] = []
    if not PUBLIC.is_dir():
        return out
    for js in PUBLIC.rglob("*.js"):
        rel = js.as_posix()
        if "/labs/" in rel:
            continue
        out.append(js)
    return out
def _gather_css_targets() -> list[Path]:
    """All CSS under public/. /_csp/* is the main target — Lighthouse
    flags it as 14 KiB unminified because SSG preserves the
    leading <style>-block indentation + a multi-line vendor comment."""
    if not PUBLIC.is_dir():
        return []
    return list(PUBLIC.rglob("*.css"))
asset_hashes: dict[str, str] = {}
asset_path_re = re.compile(
    r'(?:src|href)=["\']?/(?:_csp/)?([A-Za-z0-9][A-Za-z0-9\-_.]+\.(?:js|css))',
    re.IGNORECASE,
)
_SRI_ANY_RE = re.compile(r"\s+integrity=(['\"])sha256-[^'\"]+\1")
_TAG_CLOSE_RE = re.compile(r"(\s*/?>)\s*$")
_CROSSORIGIN_RE = re.compile(
    r"\s+crossorigin=(['\"]?)(?:anonymous|use-credentials)\1", re.IGNORECASE
)
def fix_sri(html: str) -> str:
    """Stamp the right ``integrity="sha256-..."`` (and one
    ``crossorigin="anonymous"``) onto every ``<script>``/``<link>`` that
    points at an asset whose digest we know. Idempotent: stale/bogus
    integrity and any pre-existing crossorigin are stripped first so we
    don't accumulate duplicates."""
    out: list[str] = []
    last = 0
    for m in re.finditer(r"<(?:script|link)\b[^>]+>", html):
        chunk = m.group(0)
        ap = asset_path_re.search(chunk)
        if not ap:
            continue
        digest = asset_hashes.get(ap.group(1))
        if not digest:
            continue
        # Strip any existing integrity (we'll re-stamp) and any existing
        # crossorigin (we'll re-add a single canonical one). Then split
        # off the closing `>` / `/>` so we can inject before it cleanly.
        stripped = _SRI_ANY_RE.sub("", chunk)
        stripped = _CROSSORIGIN_RE.sub("", stripped)
        close_m = _TAG_CLOSE_RE.search(stripped)
        if not close_m:
            # Tag doesn't end how we expect — skip rather than corrupt.
            continue
        body = stripped[: close_m.start()]
        closer = close_m.group(1)
        # ``digest`` is the full integrity value — one or more
        # whitespace-separated ``sha256-<b64>`` tokens (see
        # ``_candidate_digests``). The SRI spec accepts a list and
        # passes the resource if any token matches the computed hash.
        replaced = body + f' integrity="{digest}" crossorigin="anonymous"' + closer
        out.append(html[last : m.start()])
        out.append(replaced)
        last = m.end()
    out.append(html[last:])
    return "".join(out)
_FIRST_IMG_RE = re.compile(
    r'<img\b(?![^>]*\b(?:loading=["\']?lazy)\b)[^>]*\bsrc=["\']([^"\']+)["\']',
    re.IGNORECASE,
)
_HEAD_CLOSE_RE = re.compile(r"</head>", re.IGNORECASE)
_LINK_TAG_RE = re.compile(r"<link\b[^>]+>", re.IGNORECASE)
_REL_PRELOAD_ATTR_RE = re.compile(r"\brel=[\"']?preload\b", re.IGNORECASE)
_AS_IMAGE_ATTR_RE = re.compile(r"\bas=[\"']?image\b", re.IGNORECASE)
def _has_image_preload(html: str) -> bool:
    for m in _LINK_TAG_RE.finditer(html):
        tag = m.group(0)
        if _REL_PRELOAD_ATTR_RE.search(tag) and _AS_IMAGE_ATTR_RE.search(tag):
            return True
    return False
def _align_existing_preload(html: str, target_src: str) -> tuple[str, int]:
    """Rewrite any existing ``<link rel=preload as=image>`` href to
    ``target_src``. Avoids the 'preloaded but not used' warning that
    fires when the layout-emitted preload uses a different transform
    width than the actual LCP <img> ends up with."""
    n = 0

    def patch(match: re.Match[str]) -> str:
        nonlocal n
        attrs = match.group(1)
        href = _link_attr_href(attrs)
        if href == target_src:
            return match.group(0)  # already aligned
        new_attrs, n_sub = _LINK_HREF_ANY_RE.subn(
            f'href="{target_src}"',
            attrs,
            count=1,
        )
        if n_sub == 0:
            return match.group(0)
        n += 1
        return f"<link{new_attrs}>"

    out = _LINK_PRELOAD_IMAGE_RE.sub(patch, html)
    return out, n
def inject_lcp_preload(html: str) -> tuple[str, int]:
    """Ensure the page has a ``<link rel="preload" as="image">``
    matching the URL the browser actually fetches for the LCP hero —
    i.e. the first non-lazy ``<img src>``.

    Three cases:
      1. No non-lazy <img> on the page → nothing to preload, no-op.
      2. Preload already exists with the same href → no-op.
      3. Preload exists with a different href (e.g. layout-emitted
         w=1200 vs actual <img> w=200 after wrap_cdn_images_in_transform
         picked a different width for each) → rewrite the existing
         preload's href so it matches the fetched URL exactly.
      4. No preload yet → inject one before ``</head>``.

    Returns ``(new_html, 1)`` on inject/rewrite, ``(html, 0)`` otherwise."""
    img_m = _FIRST_IMG_RE.search(html)
    if not img_m:
        return html, 0
    src = img_m.group(1)
    if not src or src.startswith("data:"):
        return html, 0
    if _has_image_preload(html):
        return _align_existing_preload(html, src)
    preload = f'<link rel="preload" as="image" href="{src}" fetchpriority="high">'
    new = _HEAD_CLOSE_RE.sub(preload + "</head>", html, count=1)
    if new == html:
        return html, 0
    return new, 1
_CDN_HOST = "https://cloudcdn.pro"
_RASTER_EXT_RE = re.compile(r"\.(?:webp|png|jpg|jpeg)(?:[?#]|$)", re.IGNORECASE)
_IMG_TAG_TRANSFORM_RE = re.compile(r"<img\b([^>]*)/?>", re.IGNORECASE)
_IMG_SRC_ANY_RE = re.compile(
    r"""\bsrc=(?:(["'])([^"']+)\1|([^\s>'"]+))""",
    re.IGNORECASE,
)
_IMG_WIDTH_ANY_RE = re.compile(
    r"""\bwidth=(?:["'](\d+)["']|(\d+))""",
    re.IGNORECASE,
)
_IMG_FETCHPRI_RE = re.compile(
    r"""\bfetchpriority=(?:["'](high|low|auto)["']|(high|low|auto))""",
    re.IGNORECASE,
)
_VARIANT_WIDTHS = (320, 640, 1200, 1920)
_VARIANT_PREFIXES = ("/stocks/images/",)
def _snap_to_variant(width: int) -> int:
    """Snap a requested width up to the next available pre-gen variant.

    Snapping UP rather than DOWN keeps quality good on high-DPI devices;
    the alternative (snap down to keep bandwidth low) makes large
    layouts look blurry on retina screens. The CDN serves WebP so
    bandwidth cost of going up one size is small."""
    for v in _VARIANT_WIDTHS:
        if width <= v:
            return v
    return _VARIANT_WIDTHS[-1]
_VARIANT_SUFFIX_RE = re.compile(
    r"^(.+)-(320|640|1200|1920)\.webp$"
)
def _build_cdn_transform_url(path: str, width: int, quality: int) -> str:
    """Rewrite a CDN path to its pre-generated responsive variant.

    Was previously a thin wrapper over the CDN's /api/transform endpoint
    (``?url=…&w=…&format=webp&q=…``). The CDN's 2026-06-23 hardening
    closed that endpoint to the public — every wrapped <img> on the
    public site began returning 404, with the API's own error message
    explicitly prescribing pre-gen variants as the fix:

        Public pages should use the pre-generated
        /stocks/.../-{320,640,1200,1920}.webp variants instead.

    For paths under a known variant prefix (``/stocks/images/``), snaps
    the requested width up to the nearest available pre-gen and returns
    ``<CDN-host>/stocks/images/<stem>-<width>.webp``. For everything
    else (e.g. ``/clients/…`` logos that don't have variants), returns
    the bare original URL — strictly better than a 404 and matches the
    CDN's stated policy.

    Idempotent: if ``path`` is already a variant (``foo-1200.webp``)
    pass it through unchanged so the postbuild's multiple wrap passes
    don't compound the suffix (``foo-1200-1200.webp``).

    ``quality`` is ignored — variant generation happened at ingestion
    time with the CDN's policy-set quality and is no longer per-call
    tunable. Kept in the signature for callsite compatibility."""
    del quality  # variant quality is fixed at ingestion time
    if not any(path.startswith(p) for p in _VARIANT_PREFIXES):
        return f"{_CDN_HOST}{path}"
    if not path.endswith(".webp"):
        # Non-webp paths under /stocks/images/ (e.g. .png originals)
        # don't have webp variants under the same naming convention.
        # Fall back to the bare CDN URL.
        return f"{_CDN_HOST}{path}"
    # Already a variant? Pass through.
    if _VARIANT_SUFFIX_RE.match(path[len("/stocks/images/"):]):
        return f"{_CDN_HOST}{path}"
    variant_w = _snap_to_variant(width)
    stem = path[: -len(".webp")]
    return f"{_CDN_HOST}{stem}-{variant_w}.webp"
def _img_attr_src(attrs: str) -> str | None:
    m = _IMG_SRC_ANY_RE.search(attrs)
    if not m:
        return None
    return m.group(2) or m.group(3) or None
def _img_attr_width(attrs: str) -> int | None:
    m = _IMG_WIDTH_ANY_RE.search(attrs)
    if not m:
        return None
    raw = m.group(1) or m.group(2)
    try:
        return int(raw)
    except (TypeError, ValueError):
        return None
def _img_is_high_priority(attrs: str) -> bool:
    m = _IMG_FETCHPRI_RE.search(attrs)
    if not m:
        return False
    val = (m.group(1) or m.group(2) or "").lower()
    return val == "high"
_LINK_PRELOAD_IMAGE_RE = re.compile(
    r"<link\b([^>]*?\brel=[\"']?preload[\"']?[^>]*?\bas=[\"']?image[\"']?[^>]*?|"
    r"[^>]*?\bas=[\"']?image[\"']?[^>]*?\brel=[\"']?preload[\"']?[^>]*?)>",
    re.IGNORECASE,
)
_LINK_HREF_ANY_RE = re.compile(
    r"""\bhref=(?:(["'])([^"']+)\1|([^\s>'"]+))""",
    re.IGNORECASE,
)
def _link_attr_href(attrs: str) -> str | None:
    m = _LINK_HREF_ANY_RE.search(attrs)
    if not m:
        return None
    return m.group(2) or m.group(3) or None
def _wrap_cdn_path(path: str, base_w: int, quality: int) -> str | None:
    """Return the /api/transform URL for ``path``, or ``None`` if the
    asset isn't raster or is already wrapped or isn't on the CDN."""
    if path.startswith("/api/"):
        return None
    if not _RASTER_EXT_RE.search(path):
        return None
    target_w = max(200, min(base_w * 2, 1600))
    return _build_cdn_transform_url(path, target_w, quality)
def wrap_cdn_images_in_transform(html: str) -> tuple[str, int]:
    """Rewrite every raster ``<img src="https://cloudcdn.pro/...">`` and
    every ``<link rel="preload" as="image" href="https://cloudcdn.pro/...">``
    to use the CDN's /api/transform endpoint with a width-matched WebP.

    Returns ``(new_html, n_rewrites)``. SVG sources, already-wrapped
    transform URLs, non-CDN URLs, data: URIs and images we can't size
    pass through untouched.
    """
    n = 0

    def patch_img(match: re.Match[str]) -> str:
        nonlocal n
        attrs = match.group(1)
        src = _img_attr_src(attrs)
        if not src or not src.startswith(_CDN_HOST + "/"):
            return match.group(0)
        # Strip the host + any query/fragment to isolate the on-CDN path.
        path = src[len(_CDN_HOST) :].split("?", 1)[0].split("#", 1)[0]
        base_w = _img_attr_width(attrs) or 600
        quality = 85 if _img_is_high_priority(attrs) else 80
        new_src = _wrap_cdn_path(path, base_w, quality)
        if new_src is None:
            return match.group(0)
        # Splice the new src into the attribute string, preserving quote
        # style. Match both quoted and unquoted src= forms.
        new_attrs, n_sub = _IMG_SRC_ANY_RE.subn(
            f'src="{new_src}"',
            attrs,
            count=1,
        )
        if n_sub == 0:
            return match.group(0)
        n += 1
        return f"<img{new_attrs}>"

    def patch_preload(match: re.Match[str]) -> str:
        nonlocal n
        attrs = match.group(1)
        href = _link_attr_href(attrs)
        if not href or not href.startswith(_CDN_HOST + "/"):
            return match.group(0)
        path = href[len(_CDN_HOST) :].split("?", 1)[0].split("#", 1)[0]
        # Preloads don't carry a width hint; fetchpriority="high" on a
        # preload IS the LCP hero signal, so use the LCP defaults.
        quality = 85 if _img_is_high_priority(attrs) else 80
        # Default width 600 for hero preloads (2× → 1200, capped to 1600).
        new_href = _wrap_cdn_path(path, base_w=600, quality=quality)
        if new_href is None:
            return match.group(0)
        new_attrs, n_sub = _LINK_HREF_ANY_RE.subn(
            f'href="{new_href}"',
            attrs,
            count=1,
        )
        if n_sub == 0:
            return match.group(0)
        n += 1
        return f"<link{new_attrs}>"

    out = _IMG_TAG_TRANSFORM_RE.sub(patch_img, html)
    out = _LINK_PRELOAD_IMAGE_RE.sub(patch_preload, out)
    return out, n
jsonld_re = re.compile(
    r'<script[^>]*type=["\']?application/ld\+json["\']?[^>]*>([\s\S]*?)</script\s*>',
    re.IGNORECASE,
)
speculation_re = re.compile(
    r'<script[^>]*type=["\']?speculationrules["\']?[^>]*>([\s\S]*?)</script\s*>',
    re.IGNORECASE,
)
_inline_script_re = re.compile(
    r"<script(?![^>]*\bsrc=)(?![^>]*\btype=)[^>]*>([\s\S]*?)</script\s*>",
    re.IGNORECASE,
)
csp_tag_re = re.compile(
    r'<meta\b[^>]*?http-equiv=["\']?Content-Security-Policy["\']?[^>]*?>',
    re.IGNORECASE,
)
content_attr_re = re.compile(
    r'(content=)(["\'])(.+?)(\2)',
    re.IGNORECASE | re.DOTALL,
)
def inject_jsonld_hashes(html: str) -> str:
    bodies = [m.group(1) for m in jsonld_re.finditer(html)]
    bodies.extend(m.group(1) for m in speculation_re.finditer(html))
    # Bare <script> blocks (no src, no type) — currently just the inlined
    # theme-init bootstrap, but the rule is generic.
    bodies.extend(m.group(1) for m in _inline_script_re.finditer(html))
    if not bodies:
        return html
    hashes = sorted({b64_sha256(b.encode("utf-8")) for b in bodies})
    hash_tokens = " ".join(f"'sha256-{h}'" for h in hashes)

    def patch_csp(tag_match: re.Match[str]) -> str:
        tag = tag_match.group(0)

        def patch_content(c: re.Match[str]) -> str:
            policy = c.group(3)
            new_policy = re.sub(r"(script-src[^;]*?)\s*'unsafe-inline'", r"\1", policy)
            new_policy = re.sub(
                r"(script-src)(\s+)",
                r"\1 " + hash_tokens + r"\2",
                new_policy,
                count=1,
            )
            return c.group(1) + c.group(2) + new_policy + c.group(4)

        return content_attr_re.sub(patch_content, tag, count=1)

    return csp_tag_re.sub(patch_csp, html, count=1)
_FP_ASSET_MAP: dict[str, str] = {}
def _build_fp_pattern() -> re.Pattern[str] | None:
    if not _FP_ASSET_MAP:
        return None
    bares = sorted(_FP_ASSET_MAP, key=len, reverse=True)
    alternation = "|".join(re.escape(b) for b in bares)
    return re.compile(
        r'(<(?:script|link)\b[^>]*\b(?:src|href)=["\']?)(' + alternation + r')(["\']?[^>]*>)',
        re.IGNORECASE,
    )
_FP_PATTERN = _build_fp_pattern()
def stamp_asset_fingerprints(html: str) -> tuple[str, int]:
    """Rewrite bare ``/main.js`` / ``/highlight.css`` references in
    ``<script src>`` / ``<link href>`` tags to their fingerprinted
    counterparts (``/main.b5833c97.js``, ``/highlight.a92b9694.css``).

    The bare-name aliases are kept on disk by ``build.sh`` for any
    code path that still references them (service-worker fetches,
    legacy bookmarks), but every HTML page should reference the
    fingerprinted name so that an edge cache (Cloudflare/Fastly) is
    forced to fetch fresh bytes whenever the file content changes.

    Returns ``(new_html, swaps)``."""
    if _FP_PATTERN is None:
        return html, 0
    n = 0

    def replace(m: re.Match[str]) -> str:
        nonlocal n
        n += 1
        return m.group(1) + _FP_ASSET_MAP[m.group(2)] + m.group(3)

    return _FP_PATTERN.sub(replace, html), n


# ---------------------------------------------------------------------------
# Import-time asset setup: minify, SRI hashes, fingerprint map.
# ---------------------------------------------------------------------------

_PAGES_TRAILING_NEWLINE = b"\n"
_top_fp_re = re.compile(r"^[a-z\-_]+\.[a-f0-9]+\.js$", re.IGNORECASE)


def _minify_css(p: Path) -> tuple[int, int]:
    """Minify a CSS file in place + ensure a trailing newline (SRI-vs-wire)."""
    try:
        src = p.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return 0, 0
    candidate = _ensure_trailing_newline(rcssmin.cssmin(src))
    out = candidate if len(candidate) < len(src) else _ensure_trailing_newline(src)
    if out == src:
        return 0, 0
    p.write_text(out, encoding="utf-8")
    return len(src), len(out)


def _bulk_minify_js() -> tuple[int, int, int]:
    n = before = after = 0
    for js in _gather_js_targets():
        b, a = _minify_one(js)
        if b:
            before += b
            after += a
            n += 1
    return n, before, after


def _bulk_minify_css() -> tuple[int, int, int]:
    n = before = after = 0
    for css in _gather_css_targets():
        b, a = _minify_css(css)
        if b:
            before += b
            after += a
            n += 1
    return n, before, after


def _candidate_digests(body: bytes) -> str:
    """One or two space-separated ``sha256-<b64>`` tokens covering the observed
    GitHub Pages edge-byte mutations (file-as-is + file+trailing-newline)."""
    primary = b64_sha256(body)
    appended = b64_sha256(body + _PAGES_TRAILING_NEWLINE)
    if appended == primary:
        return f"sha256-{primary}"
    return f"sha256-{primary} sha256-{appended}"


def setup_asset_state(public: Path) -> tuple[int, int, int, int, int, int]:
    """Run the import-time asset pipeline in order: minify JS/CSS, populate the
    SRI hash table, then build the fingerprint map + pattern (minify must run
    before hashing so the digests match the on-disk minified bytes). Returns
    ``(js_count, js_before, js_after, css_count, css_before, css_after)``."""
    global _FP_PATTERN
    js_count, js_before, js_after = _bulk_minify_js()
    css_count, css_before, css_after = _bulk_minify_css()
    csp_dir = public / "_csp"
    if csp_dir.is_dir():
        for asset in csp_dir.iterdir():
            if asset.is_file() and asset.suffix in (".js", ".css"):
                asset_hashes[asset.name] = _candidate_digests(asset.read_bytes())
    if public.is_dir():
        for asset in public.iterdir():
            if asset.is_file() and _top_fp_re.match(asset.name):
                asset_hashes[asset.name] = _candidate_digests(asset.read_bytes())
    for fp in public.glob("main.*.js"):
        if fp.stem.count(".") == 1:
            _FP_ASSET_MAP["/main.js"] = "/" + fp.name
    for fp in public.glob("highlight.*.css"):
        if fp.stem.count(".") == 1:
            _FP_ASSET_MAP["/highlight.css"] = "/" + fp.name
    _FP_PATTERN = _build_fp_pattern()
    return js_count, js_before, js_after, css_count, css_before, css_after
