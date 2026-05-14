#!/usr/bin/env python3
"""Post-build pass on Static Site Generator's ``public/`` output.

Tasks performed:
1. **Real SRI** — replace every ``integrity="sha256-<short-hex>"`` placeholder
   that Static Site Generator emits on its ``/_csp/*`` assets with a real base64-encoded
   SHA-256 of the asset's actual byte content. Browsers will now enforce SRI.

2. **CSP for inline JSON-LD** — compute the SHA-256 of every
   ``<script type="application/ld+json">`` block inside each HTML page and
   inject those hashes into that page's ``script-src`` directive. The previous
   ``'unsafe-inline'`` carve-out is removed.
"""
from __future__ import annotations

import base64
import hashlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _fr_slugs import EN_TO_FR, FR_TO_EN
from _fr_slugs import en_slug as _en_slug
from _fr_slugs import fr_slug as _fr_slug

PUBLIC = Path("public")


def b64_sha256(data: bytes) -> str:
    return base64.b64encode(hashlib.sha256(data).digest()).decode("ascii")


# ---------------------------------------------------------------------------
# 1. /_csp/* SRI fix
# ---------------------------------------------------------------------------

_csp_dir = PUBLIC / "_csp"
asset_hashes: dict[str, str] = {}
if _csp_dir.is_dir():
    for asset in _csp_dir.iterdir():
        if asset.is_file() and asset.suffix in (".js", ".css"):
            asset_hashes[asset.name] = b64_sha256(asset.read_bytes())

bogus_re = re.compile(r' integrity="sha256-[a-f0-9]+"')
asset_path_re = re.compile(r'(?:src|href)=["\']?/_csp/([^"\' ]+)')


def fix_sri(html: str) -> str:
    out: list[str] = []
    last = 0
    # Walk every <script>/<link> opening tag, look at its asset path + integrity.
    for m in re.finditer(r'<(?:script|link)[^>]+>', html):
        chunk = m.group(0)
        ap = asset_path_re.search(chunk)
        if not ap:
            continue
        digest = asset_hashes.get(ap.group(1))
        if not digest:
            continue
        # Strip any existing (bogus) integrity, then inject the real one.
        stripped = bogus_re.sub('', chunk)
        if 'integrity=' not in stripped:
            replaced = stripped.rstrip(' />') + f' integrity="sha256-{digest}" crossorigin="anonymous"' + stripped[-2:]
        else:
            replaced = stripped
        out.append(html[last:m.start()])
        out.append(replaced)
        last = m.end()
    out.append(html[last:])
    return "".join(out)


# ---------------------------------------------------------------------------
# 2. CSP hash for inline JSON-LD
# ---------------------------------------------------------------------------

# Capture the literal inline body of every <script type="application/ld+json"> tag.
# (Static Site Generator may emit either single- or double-quoted type attribute and may have
# attribute order vary, so the regex is intentionally loose.)
jsonld_re = re.compile(
    r'<script[^>]*type=["\']?application/ld\+json["\']?[^>]*>([\s\S]*?)</script>',
    re.IGNORECASE,
)
# Match the CSP meta tag whether attributes are quoted or not, in either order
# (Static Site Generator's minifier emits `<meta content="..." http-equiv=Content-Security-Policy>`).
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


# ---------------------------------------------------------------------------
# 3. ItemList JSON-LD on listing pages
# ---------------------------------------------------------------------------

import html as _html
import json as _json

# Listing pages we know about. The key is the relative path; the value is the
# CSS-selector-style article class pattern that identifies an item card on
# that page. Cards we'd otherwise pick up (e.g. "newsroom-featured" on the
# /articles/ page) are folded in via wildcard prefix matching below.
LISTING_PAGES = {
    "articles/index.html": ("newsroom-card", "newsroom-featured"),
    "papers/index.html":   ("newsroom-card", "book"),
    "projects/index.html": ("newsroom-card",),
    # Playlists embed Spotify iframes per card, not internal links, so an
    # ItemList over those is semantically wrong — Schema.org's ItemList is
    # for an enumerated list of items addressable by URL on this site.
}

SITE = "https://sebastienrousseau.com"

# Parse one <article class="..."> ... </article> block and extract (title, url).
# The card markup varies but always includes the canonical link as the first
# <a href="..."> with text content matching the card's H2/H3 title.
_card_block_re = re.compile(
    r'<article\b[^>]*\bclass="([^"]+)"[^>]*>([\s\S]*?)</article>',
    re.IGNORECASE,
)
_first_link_re = re.compile(
    r'<a\b[^>]*\bhref="([^"]+)"[^>]*>([\s\S]*?)</a>',
    re.IGNORECASE,
)
_strip_tags_re = re.compile(r'<[^>]+>')
_ws_re = re.compile(r'\s+')


def _strip_tags(s: str) -> str:
    return _ws_re.sub(' ', _strip_tags_re.sub('', s)).strip()


def build_itemlist(html: str, classes: tuple[str, ...], page_url: str) -> str | None:
    items: list[tuple[str, str]] = []
    for m in _card_block_re.finditer(html):
        card_classes = m.group(1).split()
        if not any(c in card_classes for c in classes):
            continue
        body = m.group(2)
        # Walk every <a href> in the card and pick the one with the longest
        # visible text. Media links (the wrapping <a> around an <img>) carry
        # the URL but no text; the H3 title link carries the canonical name.
        best: tuple[int, str, str] | None = None
        for lm in _first_link_re.finditer(body):
            href = _html.unescape(lm.group(1))
            text = _strip_tags(lm.group(2))
            if not href or href.startswith('#') or len(text) < 3:
                continue
            if href.startswith('/'):
                href = SITE + href
            cand = (len(text), text, href)
            if best is None or cand[0] > best[0]:
                best = cand
        if best is not None:
            items.append((best[1], best[2]))
    if not items:
        return None
    graph = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "url": page_url,
        "numberOfItems": len(items),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "url": url,
                "name": title,
            }
            for i, (title, url) in enumerate(items)
        ],
    }
    return _json.dumps(graph, separators=(',', ':'), ensure_ascii=False)


def inject_itemlist(page: Path, html: str) -> str:
    rel = page.relative_to(PUBLIC).as_posix()
    classes = LISTING_PAGES.get(rel)
    if not classes:
        return html
    page_url = f"{SITE}/{rel.replace('index.html', '').rstrip('/')}/"
    payload = build_itemlist(html, classes, page_url)
    if not payload:
        return html
    block = (
        '<script type="application/ld+json">'
        + payload +
        '</script>'
    )
    # Insert just before </body> so the existing CSP-hash pass picks it up.
    return re.sub(r'(?i)</body>', block + '</body>', html, count=1)


# ---------------------------------------------------------------------------
# 4. og:image / twitter:image rewrite
# ---------------------------------------------------------------------------

# Shokunin's auto-generated og:image scans the body and picks up the first
# <img> tag, which is often a decorative divider.svg or a body inline image
# rather than the article banner. The result: link previews on Twitter,
# LinkedIn, Slack, etc. show a one-pixel line instead of the article's
# headline image. Rebuild og:image + twitter:image from the BlogPosting
# graph's ImageObject (which we control: it reads from {{banner}} in the
# layout).

_blogposting_image_re = re.compile(
    r'"@type":"BlogPosting"[^{}]*'
    r'"image":\{[^{}]*?"url":"([^"]+)"'
    r'(?:[^{}]*?"width":"([^"]*)")?'
    r'(?:[^{}]*?"height":"([^"]*)")?',
    re.DOTALL,
)


# ---------------------------------------------------------------------------
# 4b. about / mentions — link the post to canonical entities so AI engines
#     can ground the article inside their knowledge graphs.
# ---------------------------------------------------------------------------

# Entity name (matched case-insensitively against keywords) -> tuple of
#   (authoritative_external_url, optional_wikidata_qid, optional_canonical_post_stem)
# Wikipedia URL grounds AI overviews. Wikidata Q-number is added as a second
# sameAs entry so engines that reconcile on the Wikidata knowledge graph
# (Google KG, SPARQL, AI agents) can pin the entity precisely. Canonical
# post stem points at the post on this site that is the authoritative
# write-up — also added to sameAs so the site is treated as a co-authority.
# A page never self-anchors.
ENTITY_AUTHORITY: dict[str, tuple[str, str | None, str | None]] = {
    "CRYSTALS-Kyber":               ("https://en.wikipedia.org/wiki/Kyber", "Q116727584",
                                     "2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age"),
    "post-quantum cryptography":    ("https://en.wikipedia.org/wiki/Post-quantum_cryptography", "Q1364608",
                                     "2025-09-01-quantum-safe-payments-epaa"),
    "lattice-based cryptography":   ("https://en.wikipedia.org/wiki/Lattice-based_cryptography", "Q6499614",
                                     "2024-04-15-quantum-algorithm-challenges-lattice-based-cryptography"),
    "Quantum key distribution":     ("https://en.wikipedia.org/wiki/Quantum_key_distribution", "Q768051",
                                     "2023-12-11-quantum-key-distribution-revolutionising-security-in-banking"),
    "Shor's algorithm":             ("https://en.wikipedia.org/wiki/Shor%27s_algorithm", "Q717409",
                                     "2026-04-11-quantum-thresholds-are-moving-again"),
    "homomorphic encryption":       ("https://en.wikipedia.org/wiki/Homomorphic_encryption", "Q2154943",
                                     "2024-03-25-fully-homomorphic-encryption-in-a-banking-quantum-era"),
    "Quantum computing":            ("https://en.wikipedia.org/wiki/Quantum_computing", "Q484641", None),
    "NIST PQC":                     ("https://csrc.nist.gov/projects/post-quantum-cryptography", None, None),
    "ISO 20022":                    ("https://www.iso20022.org/", "Q15727611",
                                     "2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001"),
    "SWIFT gpi":                    ("https://www.swift.com/our-solutions/swift-gpi", None, None),
    "SEPA":                         ("https://en.wikipedia.org/wiki/Single_Euro_Payments_Area", "Q286094", None),
    "Large language model":         ("https://en.wikipedia.org/wiki/Large_language_model", "Q115305900",
                                     "2026-05-11-lucy-besson-knowledge-transfer-ai-quantum"),
    "Generative AI":                ("https://en.wikipedia.org/wiki/Generative_artificial_intelligence", "Q108766533",
                                     "2023-11-12-exploring-generative-ai"),
    "Artificial intelligence":      ("https://en.wikipedia.org/wiki/Artificial_intelligence", "Q11660", None),
    "Multimodal learning":          ("https://en.wikipedia.org/wiki/Multimodal_learning", "Q117259025",
                                     "2024-03-18-advancing-ai-with-multimodal-llms-insights-from-mm1"),
    "Rust":                         ("https://en.wikipedia.org/wiki/Rust_(programming_language)", "Q575650", None),
    "Python":                       ("https://en.wikipedia.org/wiki/Python_(programming_language)", "Q28865", None),
    "Blockchain":                   ("https://en.wikipedia.org/wiki/Blockchain", "Q20514253",
                                     "2018-01-02-blockchain-the-technology-that-matters-in-2018"),
    "Bitcoin":                      ("https://en.wikipedia.org/wiki/Bitcoin", "Q131723",
                                     "2018-01-01-bitcoin-the-year-in-review"),
    "Ethereum":                     ("https://en.wikipedia.org/wiki/Ethereum", "Q21825854",
                                     "2018-01-24-the-erc-20-token-standard"),
    "ERC-20":                       ("https://en.wikipedia.org/wiki/Ethereum#Tokens", None,
                                     "2018-01-24-the-erc-20-token-standard"),
}

SITE_ROOT = "https://sebastienrousseau.com"


_keywords_re = re.compile(
    r'"@type":"BlogPosting"[\s\S]*?"keywords":"([^"]*)"',
)
_blogposting_url_re = re.compile(
    # The BlogPosting-level url is followed by ",datePublished":,
    # which lets us distinguish it from the image-object's nested url.
    r'"url":"([^"]+)","datePublished":',
)


def _current_stem(html: str) -> str | None:
    m = _blogposting_url_re.search(html)
    if not m:
        return None
    url = m.group(1)
    # Strip trailing /index.html or trailing slash to reach the bare path.
    for suffix in ("/index.html", "/"):
        if url.endswith(suffix):
            url = url[: -len(suffix)]
    return url.rsplit("/", 1)[-1] if "/" in url else None


def build_about_graph(html: str) -> str | None:
    m = _keywords_re.search(html)
    if not m:
        return None
    keywords_raw = m.group(1)
    if not keywords_raw:
        return None
    keywords = [k.strip() for k in keywords_raw.split(",") if k.strip()]
    own_stem = _current_stem(html)
    seen: set[str] = set()
    matches: list[dict[str, object]] = []
    for kw in keywords:
        kwl = kw.lower()
        for entity, (ext_url, qid, canonical_stem) in ENTITY_AUTHORITY.items():
            ent_l = entity.lower()
            if (kwl == ent_l or ent_l in kwl or kwl in ent_l) and entity not in seen:
                seen.add(entity)
                same_as: list[str] = [ext_url]
                # Wikidata Q-number as a second sameAs anchor — gives engines
                # that reconcile on the Wikidata knowledge graph a precise pin.
                if qid:
                    same_as.append(f"https://www.wikidata.org/wiki/{qid}")
                # The user's own canonical post as a third sameAs anchor —
                # tells crawlers this site is also an authority. Skipped when
                # the current page IS the canonical post (no self-link).
                if canonical_stem and canonical_stem != own_stem:
                    same_as.append(f"{SITE_ROOT}/{canonical_stem}/index.html")
                node: dict[str, object] = {
                    "@type": "Thing",
                    "name": entity,
                    "sameAs": same_as if len(same_as) > 1 else same_as[0],
                }
                matches.append(node)
                break
    if not matches:
        return None
    # First match is the primary "about" subject; the rest land in "mentions".
    import json as _json
    primary = matches[0]
    rest = matches[1:6]  # cap secondary entities at 5 to keep schema lean
    fragment_parts = [f'"about":{_json.dumps(primary, separators=(",", ":"))}']
    if rest:
        fragment_parts.append(f'"mentions":{_json.dumps(rest, separators=(",", ":"))}')
    return ",".join(fragment_parts)


def inject_about(html: str) -> str:
    fragment = build_about_graph(html)
    if not fragment:
        return html
    # Insert after "wordCount" (or after "headline" if wordCount was skipped),
    # so the entity graph sits at a stable position in the BlogPosting.
    return re.sub(
        r'("@type":"BlogPosting"[^{]*?)("headline":)',
        rf'\1{fragment},\2',
        html,
        count=1,
    )


# ---------------------------------------------------------------------------
# 5. wordCount injection into BlogPosting
# ---------------------------------------------------------------------------

_main_re = re.compile(r'<main\b[^>]*>([\s\S]*?)</main>', re.IGNORECASE)
_aside_re = re.compile(r'<aside\b[^>]*>([\s\S]*?)</aside>', re.IGNORECASE)
_html_tag_re = re.compile(r'<[^>]+>')
_whitespace_re = re.compile(r'\s+')


def compute_word_count(html: str) -> int | None:
    main_m = _main_re.search(html)
    if not main_m:
        return None
    content = main_m.group(1)
    # Drop asides (lead block, related-cards, etc.) — they're already
    # represented by speakable + isPartOf and aren't the article body.
    content = _aside_re.sub('', content)
    text = _html_tag_re.sub(' ', content)
    text = _whitespace_re.sub(' ', text).strip()
    if not text:
        return None
    return len(text.split())


def inject_word_count(html: str) -> str:
    n = compute_word_count(html)
    if not n:
        return html
    # Insert "wordCount":N into the BlogPosting object if not already present.
    return re.sub(
        r'("@type":"BlogPosting"[^{]*?)("headline":)',
        rf'\1"wordCount":{n},\2',
        html,
        count=1,
    )


def fix_social_image(html: str) -> str:
    m = _blogposting_image_re.search(html)
    if not m:
        return html
    banner = m.group(1)
    width = m.group(2) or ""
    height = m.group(3) or ""
    if not banner or "divider" in banner:
        return html  # Don't propagate a placeholder/divider value

    def sub_attr(pattern: str, value: str, text: str) -> str:
        return re.sub(pattern, lambda m: m.group(1) + f'"{value}"', text)

    html = sub_attr(r'(<meta\s+property="og:image"\s+content=)"[^"]*"', banner, html)
    html = sub_attr(r'(<meta\s+name="twitter:image"\s+content=)"[^"]*"', banner, html)
    if width:
        html = sub_attr(r'(<meta\s+property="og:image:width"\s+content=)"[^"]*"', width, html)
    if height:
        html = sub_attr(r'(<meta\s+property="og:image:height"\s+content=)"[^"]*"', height, html)
    # Force summary_large_image on real BlogPosting pages. Shokunin emits
    # `summary` for some posts despite the frontmatter saying otherwise,
    # losing the large banner preview on every share.
    html = sub_attr(
        r'(<meta\s+name="twitter:card"\s+content=)"summary"',
        "summary_large_image", html,
    )
    return html


# ---------------------------------------------------------------------------
# 4d. HowTo JSON-LD for practical articles
# ---------------------------------------------------------------------------
#
# Articles that walk through a procedure (CLI usage, migration steps,
# governance checklist) get a HowTo schema so Google can render them
# as a numbered rich result. The data is curated per-article — the
# steps are explicit, in the right order, and decoupled from heading
# styling so we can refactor the article without breaking the schema.

HOWTO_SCHEMAS: dict[str, dict] = {
    "2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001": {
        "name": "Generate an ISO 20022 pain.001 payment file with pain001",
        "description": (
            "Step-by-step procedure to install pain001, supply a CSV "
            "instruction set and an XML template, and emit a validated "
            "ISO 20022 pain.001.001.09 payment-initiation file."
        ),
        "totalTime": "PT15M",
        "supply": ["Python 3.9+", "pain001 PyPI package", "ISO 20022 XML template",
                   "Input CSV of payment instructions"],
        "tool": ["pip", "Terminal", "lxml validator"],
        "steps": [
            ("Install pain001", "Install the package from PyPI with `pip install pain001`."),
            ("Prepare your inputs",
             "Place your payment-instruction CSV and your ISO 20022 XML template "
             "in the same directory; both must follow the column layout documented "
             "in the README."),
            ("Run pain001",
             "Invoke `pain001 -t template.xml -i instructions.csv -o pain001.xml`."),
            ("Validate the output",
             "Open the generated XML in lxml or your bank's validator; the file "
             "should parse against the pain.001.001.09 schema with zero errors."),
        ],
    },
    "2026-05-12-iso-20022-pacs008-structured-address-deadline": {
        "name": "Migrate your pacs.008 messages to structured addresses",
        "description": (
            "How wholesale-payments operators bring their cross-border "
            "messaging into compliance with the SWIFT/ISO 20022 "
            "structured-address mandate."
        ),
        "totalTime": "PT3M",
        "supply": ["pacs.008 sample messages", "Current address-quality metrics",
                   "Mapping rules to ISO 20022 PostalAddress components"],
        "tool": ["pacs008 parser", "ISO 20022 XML validator"],
        "steps": [
            ("Inventory unstructured addresses",
             "Audit your outbound pacs.008 traffic. Any address still in a single "
             "free-text field is in scope."),
            ("Map fields to structured components",
             "Decompose the address into Town, PostCode, Country, BuildingNumber, "
             "Street and other ISO 20022 PostalAddress slots."),
            ("Update your message generator",
             "Patch the pacs.008 templating layer so every new message emits "
             "structured fields by default; keep a fallback for receivers that "
             "haven't migrated."),
            ("Test against the deadline",
             "Run end-to-end tests against your scheme's test harness before the "
             "November 2026 enforcement date."),
        ],
    },
}


def _build_howto_jsonld(spec: dict) -> str:
    steps_json = []
    for i, (name, text) in enumerate(spec["steps"], 1):
        steps_json.append({
            "@type": "HowToStep",
            "position": i,
            "name": name,
            "text": text,
        })
    payload = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": spec["name"],
        "description": spec["description"],
        "totalTime": spec.get("totalTime", "PT10M"),
        "supply": [{"@type": "HowToSupply", "name": s} for s in spec.get("supply", [])],
        "tool": [{"@type": "HowToTool", "name": t} for t in spec.get("tool", [])],
        "step": steps_json,
    }
    return f'<script type="application/ld+json">{_json.dumps(payload, separators=(",",":"))}</script>'


def inject_howto(page: Path, html: str) -> str:
    """Append a curated HowTo JSON-LD block to opt-in articles."""
    slug = page.parent.name
    spec = HOWTO_SCHEMAS.get(slug)
    if not spec:
        return html
    if '"@type":"HowTo"' in html or '"@type": "HowTo"' in html:
        return html  # Already injected — idempotent.
    block = _build_howto_jsonld(spec)
    return re.sub(r'</body>', block + '</body>', html, count=1)


# ---------------------------------------------------------------------------
# 4c. Image width/height — eliminate CLS
# ---------------------------------------------------------------------------
#
# Browser allocates a placeholder of size width×height before the
# bytes arrive; without those attrs the layout reflows once the
# image lands → cumulative layout shift. Shokunin's Markdown
# pipeline doesn't probe remote dimensions, so every Markdown img
# ships unsized. Stamp them at postbuild time.
#
# We don't need exact dimensions — the browser uses the ratio. A
# manifest pins the common assets to their real size; everything
# else gets a 16:9 (1200×675) default which matches the dominant
# banner shape used across the site.

_IMG_TAG_RE = re.compile(r'<img\b([^>]*?)/?>', re.IGNORECASE)
_IMG_SRC_RE = re.compile(r'''\bsrc=["']?([^"'\s>]+)''', re.IGNORECASE)

# Known dimensions for high-frequency assets. Keep this short — the
# default below catches everything else.
_IMG_DIMS: dict[str, tuple[int, int]] = {
    "https://cloudcdn.pro/clients/common/images/elements/divider.svg": (40, 6),
    "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg": (160, 40),
    "https://cloudcdn.pro/clients/shokunin/v1/banners/banner-shokunin.svg": (1200, 675),
    # Personal portrait — 162×162 native, used at small sizes everywhere.
    "https://cloudcdn.pro/stocks/images/sebastien-rousseau.png": (162, 162),
}

# URL-prefix → (width, height). Lets us pin entire CDN folders without
# enumerating every asset (e.g. all Alien Studio collection thumbnails
# are 800×800; all GitHub banner SVGs are 1000×400).
_IMG_DIMS_PREFIX: tuple[tuple[str, tuple[int, int]], ...] = (
    ("https://cloudcdn.pro/clients/alienstudio/", (800, 800)),
    ("https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/", (240, 60)),
    ("https://cloudcdn.pro/clients/common/images/buttons/", (18, 18)),
    ("https://cloudcdn.pro/stocks/diagrams/", (1200, 800)),
)
_IMG_DEFAULT = (1200, 675)  # 16:9 — matches the dominant banner ratio.


def stamp_image_dimensions(html: str) -> tuple[str, int]:  # noqa: C901 — per-attr conditional ladder
    """Add width/height + LCP/lazy hints to every <img>. Returns (html, n_patched).

    First image on the page is treated as the LCP candidate and gets
    ``fetchpriority="high"``. Everything after gets ``loading="lazy"`` +
    ``decoding="async"`` (the divider/icon SVGs included — being decorative,
    deferring them is harmless and saves main-thread work)."""
    n = 0
    seen_first = False

    def patch(m: re.Match[str]) -> str:
        nonlocal n, seen_first
        attrs = m.group(1)
        is_first = not seen_first
        seen_first = True
        has_w = bool(re.search(r'\bwidth=', attrs, re.IGNORECASE))
        has_h = bool(re.search(r'\bheight=', attrs, re.IGNORECASE))
        has_loading = bool(re.search(r'\bloading=', attrs, re.IGNORECASE))
        has_decoding = bool(re.search(r'\bdecoding=', attrs, re.IGNORECASE))
        has_fetchpri = bool(re.search(r'\bfetchpriority=', attrs, re.IGNORECASE))

        if has_w and has_h and has_loading and has_decoding and (has_fetchpri or not is_first):
            return m.group(0)

        extras: list[str] = []
        if not has_w or not has_h:
            src_m = _IMG_SRC_RE.search(attrs)
            src = src_m.group(1) if src_m else ""
            if src in _IMG_DIMS:
                w, h = _IMG_DIMS[src]
            else:
                w, h = _IMG_DEFAULT
                for prefix, dims in _IMG_DIMS_PREFIX:
                    if src.startswith(prefix):
                        w, h = dims
                        break
            if not has_w:
                extras.append(f'width="{w}"')
            if not has_h:
                extras.append(f'height="{h}"')
        if not has_decoding:
            extras.append('decoding="async"')
        if is_first and not has_fetchpri:
            extras.append('fetchpriority="high"')
        elif not is_first and not has_loading:
            extras.append('loading="lazy"')
        if not extras:
            return m.group(0)
        n += 1
        return f'<img{attrs} {" ".join(extras)}>'

    return _IMG_TAG_RE.sub(patch, html), n


# ---------------------------------------------------------------------------
# 4b. Open Graph completeness
# ---------------------------------------------------------------------------
#
# Shokunin emits `og:title`, `og:description`, `og:type` but skips
# `og:image`, `og:url`, `og:locale`, `og:site_name` — every social
# share renders without a preview image and without locale routing.
# Back-fill them from data the page already carries: the BlogPosting
# image (where present), the page's own URL, and the <html lang>.

BASE_URL = "https://sebastienrousseau.com"
SITE_NAME = "Sebastien Rousseau"

_HTML_LANG_RE = re.compile(r'<html\b[^>]*\blang=["\']?([a-zA-Z-]+)', re.IGNORECASE)
_HEAD_END_RE = re.compile(r'</head>', re.IGNORECASE)
_OG_TAG_RE = re.compile(
    r'<meta\s+(?:property|name)=["\']?(og:[a-z_]+|twitter:[a-z_]+)["\']?',
    re.IGNORECASE,
)


def _lang_to_og_locale(lang: str) -> str:
    """Map a BCP-47 tag to an Open Graph locale (`en_GB`, `fr_FR`)."""
    lang = (lang or "").strip()
    if not lang:
        return "en_GB"
    if "-" in lang:
        a, b = lang.split("-", 1)
        return f"{a.lower()}_{b.upper()}"
    return f"{lang.lower()}_{lang.upper()}"


def inject_og_completeness(page: Path, html: str) -> str:
    """Ensure og:image / og:url / og:locale / og:site_name are present."""
    rel = page.relative_to(PUBLIC).as_posix()
    page_url = f"{BASE_URL}/{rel}" if rel != "index.html" else f"{BASE_URL}/"

    lm = _HTML_LANG_RE.search(html)
    locale = _lang_to_og_locale(lm.group(1) if lm else "en-GB")

    present = {m.group(1).lower() for m in _OG_TAG_RE.finditer(html)}
    additions: list[str] = []

    if "og:url" not in present:
        additions.append(f'<meta property="og:url" content="{page_url}">')
    if "og:locale" not in present:
        additions.append(f'<meta property="og:locale" content="{locale}">')
    if "og:site_name" not in present:
        additions.append(f'<meta property="og:site_name" content="{SITE_NAME}">')

    if "og:image" not in present:
        # Try to lift the banner from the BlogPosting graph; fall back to
        # the site default portrait.
        img_m = _blogposting_image_re.search(html)
        banner = (img_m.group(1) if img_m else "") or \
            "https://cloudcdn.pro/stocks/images/sebastien-rousseau.png"
        additions.append(f'<meta property="og:image" content="{banner}">')
        if "twitter:image" not in present:
            additions.append(f'<meta name="twitter:image" content="{banner}">')

    if not additions:
        return html
    block = "\n".join(additions) + "\n"
    return _HEAD_END_RE.sub(block + "</head>", html, count=1)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 6a. robots.txt — explicit AI crawler rules
# ---------------------------------------------------------------------------

# Default robots.txt that SSG emits is just "User-agent: *" + Sitemap. The
# spec for major AI crawlers is to keep separate User-agent blocks rather
# than rely on the wildcard, so each ML team can be addressed independently
# in future without rewriting the whole file. We allow all AI crawlers
# because the goal is broad LLM citation; flip any line to `Disallow: /`
# to opt out of that specific bot.
ROBOTS_BODY = """User-agent: *
Allow: /

# Web search + general-purpose crawlers
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: DuckDuckBot
Allow: /

# AI training + retrieval crawlers
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: Applebot
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: CCBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: Bytespider
Allow: /

User-agent: Amazonbot
Allow: /

User-agent: Meta-ExternalAgent
Allow: /

Sitemap: https://sebastienrousseau.com/sitemap.xml
Sitemap: https://sebastienrousseau.com/news-sitemap.xml
Sitemap: https://sebastienrousseau.com/fr/news-sitemap.xml

# AI-crawler directory (proposed convention, RFC pending).
# See https://llmstxt.org/ — both files are CC BY 4.0 with attribution.
LLMs: https://sebastienrousseau.com/llms.txt
LLMs-Full: https://sebastienrousseau.com/llms-full.txt
"""


def write_robots(public: Path) -> bool:
    target = public / "robots.txt"
    cur = target.read_text(encoding="utf-8") if target.is_file() else ""
    if cur.strip() == ROBOTS_BODY.strip():
        return False
    target.write_text(ROBOTS_BODY, encoding="utf-8")
    return True


# ---------------------------------------------------------------------------
# 6b. llms.txt — structured directory for AI crawlers
# ---------------------------------------------------------------------------

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _frontmatter import read_fm as _read_fm


def build_llms_txt() -> str:
    site = "https://sebastienrousseau.com"
    posts: list[dict[str, str]] = []
    if POSTS_DIR.is_dir():
        for md in sorted(POSTS_DIR.glob("2*.md"), reverse=True):
            fm = _read_fm(md)
            posts.append({
                "stem": md.stem,
                "title": fm.get("title", md.stem),
                "description": fm.get("description", ""),
                "date": md.name[:10],
            })

    lines = [
        "# Sebastien Rousseau",
        "",
        "> AI, payments and quantum-safe cryptography for financial services. "
        "Senior banking technologist writing on applied AI, ISO 20022 migration, "
        "post-quantum cryptography, and the structural transformation of wholesale payments.",
        "",
        "Language: en-GB",
        "Author: Sebastien Rousseau",
        "Canonical: https://sebastienrousseau.com/",
        "",
        "## About",
        "",
        f"- [About the author]({site}/about/index.html): biography, experience, and entity links.",
        f"- [Contact]({site}/contact/index.html): how to get in touch.",
        "",
        "## Topic clusters",
        "",
        "- **Payments & ISO 20022.** Migration from MT/MX to structured messages, "
        "pain.001 + pacs.008 toolkits, cross-border settlement.",
        "- **Post-quantum cryptography.** CRYSTALS-Kyber, lattice-based schemes, "
        "Quantum Key Distribution, Shor's algorithm threshold tracking, payment-rail readiness.",
        "- **Applied AI.** Generative AI for finance, LLM tooling, prompt engineering, "
        "voice cloning, multimodal model evaluation.",
        "- **Open source.** Python (pain001, pacs008, Bank Statement Parser), "
        "Rust (KyberLib, HSH, DTT, libmake, Shokunin SSG, NaluFX, QRC).",
        "",
        "## Listings",
        "",
        f"- [Articles]({site}/articles/index.html): all dated posts.",
        f"- [Papers]({site}/papers/index.html): research publications + white papers.",
        f"- [Projects]({site}/projects/index.html): open-source libraries and tools.",
        f"- [Playlists]({site}/playlists/index.html): curated Spotify playlists.",
        f"- [Tags]({site}/tags/index.html): topic index across all posts.",
        "",
        "## Recent posts",
        "",
    ]
    for p in posts[:10]:
        url = f"{site}/{p['stem']}/index.html"
        desc = p["description"][:200]
        if desc and not desc.endswith("."):
            desc += "."
        lines.append(f"- [{p['title']}]({url}): {desc}")
    lines.append("")
    lines.append(f"## All posts ({len(posts)})")
    lines.append("")
    for p in posts:
        url = f"{site}/{p['stem']}/index.html"
        lines.append(f"- [{p['title']}]({url}) — {p['date']}")
    lines.append("")
    return "\n".join(lines)


def write_llms_txt(public: Path) -> bool:
    target = public / "llms.txt"
    new = build_llms_txt()
    cur = target.read_text(encoding="utf-8") if target.is_file() else ""
    if cur.strip() == new.strip():
        return False
    target.write_text(new, encoding="utf-8")
    return True


def build_llms_full_txt(public: Path) -> str:
    """Emit a single plain-text dump of every published article — the
    AI-crawler equivalent of an article archive. Perplexity, ChatGPT
    Search and Anthropic's web fetcher use this to ground citations
    without needing to crawl the HTML.
    """
    posts_dir = Path("_posts")
    if not posts_dir.is_dir():
        return ""

    lines: list[str] = []
    lines.append("# Sebastien Rousseau — Full article corpus (EN)")
    lines.append("")
    lines.append(
        "> Plain-text dump of every dated article on https://sebastienrousseau.com/, "
        "ordered most-recent first. Each article is delimited by a header line."
    )
    lines.append("")
    lines.append("Author: Sebastien Rousseau")
    lines.append("Site: https://sebastienrousseau.com/")
    lines.append("License: CC BY 4.0 with attribution — please cite the canonical URL.")
    lines.append("")

    # Date prefix sort, most-recent first.
    md_files = sorted(posts_dir.glob("2*.md"), reverse=True)
    for md in md_files:
        text = md.read_text(encoding="utf-8")
        # Split frontmatter / body.
        parts = text.split("---", 2)
        if len(parts) < 3:
            continue
        body = parts[2].strip()
        # Extract frontmatter title + url.
        fm = parts[1]
        m_title = re.search(r'^title:\s*"((?:[^"\\]|\\.)*)"', fm, re.MULTILINE)
        m_date = re.search(r'^date:\s*"((?:[^"\\]|\\.)*)"', fm, re.MULTILINE)
        title = m_title.group(1) if m_title else md.stem
        date = m_date.group(1) if m_date else ""
        url = f"https://sebastienrousseau.com/{md.stem}/"
        # Strip Shokunin's `.class="…"` image-suffix syntax + reference-link
        # definitions so the dump reads as clean prose.
        body = re.sub(r'\.class=\\?"[^"\n]*"', "", body)
        body = re.sub(r'^\[\d+\]:\s+\S+(?:\s+"[^"]*")?\s*$', "", body, flags=re.MULTILINE)
        # Collapse 3+ blank lines.
        body = re.sub(r"\n{3,}", "\n\n", body).strip()

        lines.append("=" * 72)
        lines.append(f"## {title}")
        lines.append("")
        lines.append(f"Date: {date}")
        lines.append(f"URL: {url}")
        lines.append("")
        lines.append(body)
        lines.append("")

    lines.append("")
    return "\n".join(lines)


def write_llms_full_txt(public: Path) -> bool:
    target = public / "llms-full.txt"
    new = build_llms_full_txt(public)
    if not new:
        return False
    cur = target.read_text(encoding="utf-8") if target.is_file() else ""
    if cur == new:
        return False
    target.write_text(new, encoding="utf-8")
    return True


# ---------------------------------------------------------------------------
# 6d. XML feed URL rewrite
# ---------------------------------------------------------------------------

# Shokunin's RSS, Atom and news-sitemap output writes every per-entry link /
# guid / id as `http://127.0.0.1:8000/.meta/` instead of the post's
# canonical URL. sitemap.xml is unaffected — it derives URLs from a
# different code path. The rewrite below repairs the three broken feeds:
#
#   1. Build a (post_title -> post_url) map from _posts/<stem>.md
#      frontmatter (title + url fields).
#   2. For each <item> (RSS) / <entry> (Atom) / <url> (news-sitemap) block,
#      pull the title and look up the canonical URL.
#   3. Rewrite every localhost-or-.meta URL inside that block to the
#      canonical URL — covers <link>, <guid>, <id>, news:loc, etc.
#
# The site root URL is also rewritten generically (any
# http://127.0.0.1:8000 → https://sebastienrousseau.com) so per-feed
# top-level <link> / channel-level URLs come along for the ride.

_TITLE_INSIDE_RE = re.compile(
    r'<(?:title|news:title)[^>]*>([\s\S]*?)</(?:title|news:title)>',
    re.IGNORECASE,
)
_RSS_ITEM_RE   = re.compile(r'<item>[\s\S]*?</item>', re.IGNORECASE)
_ATOM_ENTRY_RE = re.compile(r'<entry>[\s\S]*?</entry>', re.IGNORECASE)
_NEWS_URL_RE   = re.compile(r'<url>[\s\S]*?</url>', re.IGNORECASE)


def _build_title_index() -> dict[str, str]:
    """title -> canonical https://… URL, derived from _posts frontmatter."""
    idx: dict[str, str] = {}
    if not POSTS_DIR.is_dir():
        return idx
    for md in POSTS_DIR.glob("*.md"):
        fm = _read_fm(md)
        title = fm.get("title")
        url = fm.get("url")
        if title and url:
            idx[title.strip()] = url.strip()
            # Some feeds emit XML-escaped titles. Pre-compute both forms so
            # the lookup hits either way.
            idx[title.replace("&", "&amp;").strip()] = url.strip()
    return idx


def _decode_entities(s: str) -> str:
    return (s.replace("&amp;", "&")
             .replace("&lt;", "<")
             .replace("&gt;", ">")
             .replace("&quot;", '"')
             .replace("&apos;", "'")
             .strip())


def _patch_block(block: str, title_index: dict[str, str]) -> str:
    tm = _TITLE_INSIDE_RE.search(block)
    if not tm:
        return block
    title_raw = tm.group(1)
    title_clean = _decode_entities(title_raw)
    url = title_index.get(title_clean) or title_index.get(title_raw.strip())
    if not url:
        return block

    # Replace any URL inside this block that either has a localhost host or
    # has /.meta/ anywhere in its path — that's the Shokunin bug signature.
    bad_url = (
        r'https?://'
        r'(?:'
        # localhost host (any path)
        r'(?:127\.0\.0\.1|localhost)(?::\d+)?[^<\s"]*'
        # OR any host with a /.meta/ path segment
        r'|[^<\s"]*?/\.meta(?:/[^<\s"]*)?'
        r')'
    )

    def rewrite_url(m: re.Match[str]) -> str:
        return m.group(1) + url + m.group(3)

    block = re.sub(rf'(>\s*)({bad_url})(\s*<)', rewrite_url, block)
    block = re.sub(rf'(="\s*)({bad_url})(\s*")', rewrite_url, block)
    return block


def fix_xml_feed_urls(public: Path) -> int:
    title_index = _build_title_index()
    if not title_index:
        return 0
    patched = 0
    for xml in public.glob("*.xml"):
        original = xml.read_text(encoding="utf-8", errors="ignore")
        text = original

        # Per-item / per-entry / per-url URL rewrites.
        if "<item>" in text.lower():
            text = _RSS_ITEM_RE.sub(lambda m: _patch_block(m.group(0), title_index), text)
        if "<entry>" in text.lower():
            text = _ATOM_ENTRY_RE.sub(lambda m: _patch_block(m.group(0), title_index), text)
        if "<news:" in text.lower():
            text = _NEWS_URL_RE.sub(lambda m: _patch_block(m.group(0), title_index), text)

        # Strip any residual <url>…</url> block whose <loc> still has the
        # dev-artefact /.meta/ path — those entries come from Shokunin
        # processing the nested _posts/fr/ directory and don't belong in
        # the news-sitemap.
        text = re.sub(
            r'<url>\s*<loc>[^<]*\/\.meta\/[^<]*</loc>[\s\S]*?</url>\s*',
            '',
            text,
        )

        # Top-of-feed cleanup: any residual localhost reference becomes the
        # production root. Done last so it doesn't shadow per-block matches.
        text = re.sub(
            r'https?://(?:127\.0\.0\.1|localhost)(?::\d+)?',
            "https://sebastienrousseau.com",
            text,
        )

        if text != original:
            xml.write_text(text, encoding="utf-8")
            patched += 1
    return patched


# ---------------------------------------------------------------------------
# 6c. XML feed entity-escape pass
# ---------------------------------------------------------------------------

# Shokunin's RSS + news-sitemap output forgets to escape bare `&` characters
# inside <title> / <description> / <news:title> elements (e.g. "AI, Quantum
# & Knowledge"), which produces invalid XML and breaks any feed reader doing
# strict parsing. Atom is clean; sitemap is clean. We scrub all XML feeds
# defensively: every `&` that isn't already part of a valid XML entity
# reference is rewritten to `&amp;`.

# Pre-existing valid entities. Anything else after `&` (including `& ` or
# `&Q` etc.) becomes `&amp;`.
_VALID_ENTITY_RE = re.compile(r'&(amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);')


# Shokunin over-escapes the RSS channel <title> when the source frontmatter
# uses `&`. The signature is &amp;<entity-name>; — un-escape one layer.
_DOUBLE_ESCAPE_RE = re.compile(r'&amp;(amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);')


def escape_xml_ampersands(text: str) -> str:
    """Repair XML feed ampersands two ways:

    1. Un-double-escape `&amp;<entity>;` back to `&<entity>;` (Shokunin's bug
       on the RSS channel-level <title>).
    2. Replace bare `&` with `&amp;`, leaving valid entity references alone.

    Walks the string in one pass after the double-escape repair.
    """
    text = _DOUBLE_ESCAPE_RE.sub(r'&\1;', text)
    out: list[str] = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch == '&':
            m = _VALID_ENTITY_RE.match(text, i)
            if m:
                out.append(m.group(0))
                i = m.end()
                continue
            out.append('&amp;')
            i += 1
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def fix_xml_feeds(public: Path) -> int:
    patched = 0
    for xml in public.glob("*.xml"):
        original = xml.read_text(encoding="utf-8", errors="ignore")
        # XML declaration must stay first. Don't touch it.
        if original.startswith("<?xml"):
            decl_end = original.find("?>") + 2
            head = original[:decl_end]
            body = original[decl_end:]
        else:
            head = ""
            body = original
        body_fixed = escape_xml_ampersands(body)
        new = head + body_fixed
        if new != original:
            xml.write_text(new, encoding="utf-8")
            patched += 1
    return patched


# ---------------------------------------------------------------------------
# 6. sitemap.xml lastmod refresh
# ---------------------------------------------------------------------------

POSTS_DIR = Path("_posts")
_lastmod_block_re = re.compile(
    r'<url>([\s\S]*?)</url>',
    re.IGNORECASE,
)
_loc_re = re.compile(r'<loc>\s*(https?://[^<]+?)\s*</loc>', re.IGNORECASE)
_lastmod_re = re.compile(r'<lastmod>\s*([0-9-]+)\s*</lastmod>', re.IGNORECASE)
_fm_last_reviewed_re = re.compile(r'^last_reviewed:\s*"?([0-9-]+)"?', re.MULTILINE)
_fm_date_re = re.compile(r'^date:\s*"([^"]+)"', re.MULTILINE)
_post_stem_from_url_re = re.compile(r'/(\d{4}-\d{2}-\d{2}-[a-z0-9-]+)(?:/(?:index\.html)?)?$')


def build_lastmod_index() -> dict[str, str]:
    """For every dated post in _posts/, build a stem -> last_reviewed map."""
    out: dict[str, str] = {}
    if not POSTS_DIR.is_dir():
        return out
    for md in POSTS_DIR.glob("2*.md"):
        stem = md.stem
        text = md.read_text(encoding="utf-8", errors="ignore")
        m = _fm_last_reviewed_re.search(text)
        if m:
            out[stem] = m.group(1)
            continue
        # Fallback: parse `date:` (e.g. "Apr 11, 2026") → ISO.
        dm = _fm_date_re.search(text)
        if dm:
            try:
                from datetime import datetime as _dt
                d = _dt.strptime(dm.group(1), "%b %d, %Y")
                out[stem] = d.strftime("%Y-%m-%d")
            except ValueError:
                pass
    return out


def refresh_sitemap_lastmod(sitemap_path: Path, index: dict[str, str]) -> int:
    if not sitemap_path.is_file():
        return 0
    xml = sitemap_path.read_text(encoding="utf-8")
    patched = 0

    def patch_url(block_match: re.Match[str]) -> str:
        nonlocal patched
        block = block_match.group(1)
        loc_m = _loc_re.search(block)
        if not loc_m:
            return block_match.group(0)
        url = loc_m.group(1)
        stem_m = _post_stem_from_url_re.search(url)
        if not stem_m:
            return block_match.group(0)
        stem = stem_m.group(1)
        new_date = index.get(stem)
        if not new_date:
            return block_match.group(0)
        new_block = _lastmod_re.sub(f'<lastmod>{new_date}</lastmod>', block, count=1)
        if new_block != block:
            patched += 1
        return f'<url>{new_block}</url>'

    new_xml = _lastmod_block_re.sub(patch_url, xml)

    # Append the French URL set if not already present. Shokunin's sitemap
    # only enumerates _posts/ (English); FR pages are added by
    # build_translations.py after ssg has run, so they never make it into
    # the sitemap unless we splice them in here.
    new_xml = _splice_fr_urls(new_xml, index)

    if new_xml != xml:
        sitemap_path.write_text(new_xml, encoding="utf-8")
    return patched


def _splice_fr_urls(xml: str, lastmod_index: dict[str, str]) -> str:
    """Ensure the sitemap contains every EN + FR article + the static
    landing pages. Shokunin's sitemap.xml ships empty (regression) so we
    repopulate it from authoritative sources here:

    * EN dated posts → ``_posts/*.md`` stems
    * FR dated posts → :data:`EN_TO_FR` values
    * Static pages   → known top-level dirs in ``public/``
    """
    base = "https://sebastienrousseau.com"
    new_blocks: list[str] = []
    seen = set(_loc_re.findall(xml))

    def _add(url: str, priority: str, changefreq: str, lastmod: str = "") -> None:
        if url in seen:
            return
        seen.add(url)
        lm_line = f"\n  <lastmod>{lastmod}</lastmod>" if lastmod else ""
        new_blocks.append(
            f"<url>\n  <loc>{url}</loc>{lm_line}\n"
            f"  <changefreq>{changefreq}</changefreq>\n"
            f"  <priority>{priority}</priority>\n</url>"
        )

    # Landing + static pages
    _add(f"{base}/", "1.0", "daily")
    for slug in (
        "about", "articles", "papers", "projects", "topics", "tags",
        "playlists", "contact", "accessibility", "privacy", "terms",
        "made-with-shokunin", "made-with-static-site-generator",
    ):
        _add(f"{base}/{slug}/", "0.6", "monthly")

    # EN dated posts
    if POSTS_DIR.is_dir():
        for md in sorted(POSTS_DIR.glob("2*.md")):
            stem = md.stem
            lastmod = lastmod_index.get(stem, "")
            _add(f"{base}/{stem}/", "0.8", "weekly", lastmod)

    # FR hub + FR dated posts + FR static pages + FR topic sub-pages.
    # Static slugs are localised (privacy → confidentialite, etc.).
    _add(f"{base}/fr/", "0.8", "weekly")
    _add(f"{base}/fr/articles/", "0.7", "weekly")
    for slug in (
        "a-propos", "publications", "projets", "sujets", "etiquettes",
        "contact", "accessibilite", "confidentialite", "conditions", "playlists",
        "concu-avec-shokunin", "concu-avec-static-site-generator",
    ):
        _add(f"{base}/fr/{slug}/", "0.5", "monthly")
    for topic in (
        "post-quantum-cryptography", "iso-20022-payments",
        "applied-ai-banking", "rust-open-source", "blockchain-digital-assets",
    ):
        _add(f"{base}/fr/sujets/{topic}/", "0.6", "monthly")
    for en, fr in EN_TO_FR.items():
        _add(f"{base}/fr/{fr}/", "0.7", "monthly", lastmod_index.get(en, ""))

    if not new_blocks:
        return xml
    insertion = "\n" + "\n".join(new_blocks) + "\n"
    return xml.replace("</urlset>", insertion + "</urlset>", 1)


# ---------------------------------------------------------------------------
# 7. Article UI furniture
#    - tag badges + meta bar (author / dates / read time) after the H1
#    - anchor links on every H2/H3 inside <main>
#    - table-of-contents sidebar for posts with ≥5 H2 sections
#    - citation graph in BlogPosting JSON-LD for outbound links to known
#      authoritative domains
# ---------------------------------------------------------------------------

# Domains we accept as primary-source citations for AI grounding.
CITATION_AUTHORITIES = (
    "iso20022.org", "swift.com", "iso.org", "ietf.org", "w3.org",
    "nist.gov", "csrc.nist.gov", "bis.org", "ecb.europa.eu", "imf.org",
    "wikipedia.org", "wikidata.org",
    "arxiv.org", "ieee.org", "acm.org", "doi.org",
    "blackrock.com", "sec.gov", "treasury.gov", "ofac.treasury.gov",
    "hsbc.com", "jpmorgan.com", "santander.com", "bmo.com",
    "google.com", "openai.com", "anthropic.com", "deepmind.com",
    "github.com",
    "emergingpaymentsasia.org",
)

# Author meta shared across every dated post. Single source of truth.
AUTHOR_NAME = "Sebastien Rousseau"
AUTHOR_AVATAR = "https://cloudcdn.pro/stocks/images/sebastien-rousseau.png"
AUTHOR_URL = "/about/index.html"

_HERO_RE = re.compile(
    r'(<section class="ap-hero">\s*<h1>[^<]*</h1>\s*(?:<p class="sub">[^<]*</p>\s*)?)(</section>)',
    re.IGNORECASE,
)
_MAIN_RE = re.compile(
    r'(<main\b[^>]*>\s*<div class="wrap[^"]*">)([\s\S]*?)(</div>\s*</main>)',
    re.IGNORECASE,
)
_BLOGPOSTING_DATES_RE = re.compile(
    r'"datePublished":"([^"]+)"[^"]*"dateModified":"([^"]+)"',
)
_WORDCOUNT_RE = re.compile(r'"wordCount":(\d+)')
_HEADING_RE = re.compile(r'<(h[23])(?:\s+id="[^"]*")?>([\s\S]*?)</\1>', re.IGNORECASE)
_OUTBOUND_LINK_RE = re.compile(r'<a\b[^>]*\bhref="(https?://[^"]+)"', re.IGNORECASE)
_DATED_SLUG_RE = re.compile(r'^(\d{4}-\d{2}-\d{2})-')
_H1_RE = re.compile(r'<section class="ap-hero">\s*<h1>([^<]+)</h1>', re.IGNORECASE)
_HTML_LANG_DETECT_RE = re.compile(r'<html\b[^>]*\blang="([^"]+)"', re.IGNORECASE)


def _is_french(html: str) -> bool:
    m = _HTML_LANG_DETECT_RE.search(html)
    return bool(m and m.group(1).lower().startswith("fr"))


# Furniture string tables — labels emitted in <main>'s reader-facing chrome.
# English defaults stay verbatim; the French dict mirrors I18N_FR in
# build_translations.py.
LABELS_EN: dict[str, str] = {
    "Published": "Published",
    "Updated": "Updated",
    "min read": "min read",
    "Previous": "Previous",
    "Next": "Next",
    "Sources & references": "Sources & references",
    "Contents": "Contents",
    "Article pagination": "Article pagination",
    "Estimated read time": "Estimated read time",
    "Link to": "Link to",
    "Table of contents": "Table of contents",
    "Topics": "Topics",
}
LABELS_FR: dict[str, str] = {
    "Published": "Publié le",
    "Updated": "Mis à jour le",
    "min read": "min de lecture",
    "Previous": "Précédent",
    "Next": "Suivant",
    "Sources & references": "Sources et références",
    "Contents": "Sommaire",
    "Article pagination": "Pagination des articles",
    "Estimated read time": "Temps de lecture estimé",
    "Link to": "Lien vers",
    "Table of contents": "Table des matières",
    "Topics": "Sujets",
}


def _labels(html: str) -> dict[str, str]:
    return LABELS_FR if _is_french(html) else LABELS_EN


def slugify(s: str) -> str:
    import unicodedata as _ud
    s = re.sub(r"<[^>]+>", "", s).strip().lower()
    s = re.sub(r"&[a-z0-9#]+;", " ", s)
    # Fold accented letters to ASCII so "Références" -> "references", not
    # "r-f-rences". NFKD normalization decomposes é -> e + combining
    # acute; the combining mark is dropped by the [^a-z0-9]+ pass below.
    s = _ud.normalize("NFKD", s)
    s = s.encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:80]


_FR_MONTHS = {
    1: "janv.", 2: "févr.", 3: "mars", 4: "avr.", 5: "mai", 6: "juin",
    7: "juil.", 8: "août", 9: "sept.", 10: "oct.", 11: "nov.", 12: "déc.",
}


def _fmt_date(iso_or_rfc: str, french: bool = False) -> str:
    """Render a date string as 'D Mon YYYY' (English) or 'D mois YYYY'
    (French). Accepts ISO 8601 or RFC 822. Returns input unchanged on
    parse failure."""
    iso_or_rfc = iso_or_rfc.strip()
    from datetime import datetime as _dt
    for fmt in (
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%d",
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S %Z",
    ):
        try:
            dt = _dt.strptime(iso_or_rfc, fmt)
        except ValueError:
            continue
        if french:
            return f"{dt.day} {_FR_MONTHS[dt.month]} {dt.year}"
        return dt.strftime("%-d %b %Y")
    return iso_or_rfc


def _render_tag_badges(keywords: list[str], labels: dict[str, str], lang: str = "en") -> str:
    if not keywords:
        return ""
    prefix = "/fr/etiquettes/index.html" if lang == "fr" else "/tags/index.html"
    badges = "".join(
        f'<a href="{prefix}#h3-{slugify(k)}" class="article-tag" rel="tag">{k}</a>'
        for k in keywords
    )
    aria = labels.get("Topics", "Topics")
    return f'<nav class="article-tags" aria-label="{aria}">{badges}</nav>'


def _render_meta_bar(date_pub: str, date_mod: str, word_count: int | None, labels: dict[str, str], lang: str = "en") -> str:
    parts: list[str] = []
    french = labels is LABELS_FR
    author_url = "/fr/a-propos/index.html" if lang == "fr" else AUTHOR_URL
    parts.append(
        f'<a href="{author_url}" class="article-author" rel="author">'
        f'<img alt="Portrait of {AUTHOR_NAME}" src="{AUTHOR_AVATAR}" '
        f'width="36" height="36" loading="lazy" decoding="async" />'
        f'<span>{AUTHOR_NAME}</span></a>'
    )
    if date_pub:
        parts.append(
            f'<time datetime="{date_pub}" class="meta-pub">'
            f'{labels["Published"]} {_fmt_date(date_pub, french)}</time>'
        )
    # Suppress "Updated" when the modification date is the same as or
    # earlier than the publication date — otherwise a post scheduled into
    # the future shows a nonsensical "Updated before Published" stamp.
    if date_mod and date_mod[:10] > date_pub[:10]:
        parts.append(
            f'<time datetime="{date_mod}" class="meta-rev">'
            f'{labels["Updated"]} {_fmt_date(date_mod, french)}</time>'
        )
    if word_count:
        read_min = max(1, round(word_count / 220))
        parts.append(
            f'<span class="meta-read" aria-label="{labels["Estimated read time"]}">'
            f'{read_min} {labels["min read"]}</span>'
        )
    return '<div class="article-meta">' + ' <span aria-hidden="true">·</span> '.join(parts) + '</div>'


def inject_article_furniture(html: str) -> str:
    """Insert tag badges + meta bar between the H1 hero and the main body.

    Only fires when the page carries a BlogPosting JSON-LD graph — listing /
    static pages are left alone.
    """
    if '"@type":"BlogPosting"' not in html:
        return html
    # Don't double-inject if a previous postbuild run already added them.
    if 'class="article-tags"' in html:
        return html
    keywords = []
    m = _keywords_re.search(html)
    if m and m.group(1):
        keywords = [k.strip() for k in m.group(1).split(",") if k.strip()]
    dm = _BLOGPOSTING_DATES_RE.search(html)
    date_pub, date_mod = (dm.group(1), dm.group(2)) if dm else ("", "")
    wm = _WORDCOUNT_RE.search(html)
    word_count = int(wm.group(1)) if wm else None
    labels = _labels(html)
    lang = "fr" if _is_french(html) else "en"
    badges = _render_tag_badges(keywords, labels, lang)
    meta = _render_meta_bar(date_pub, date_mod, word_count, labels, lang)
    fragment = badges + meta
    if not fragment:
        return html
    return _HERO_RE.sub(rf'\1{fragment}\2', html, count=1)


def inject_anchor_links_and_toc(html: str) -> str:
    """Add id="…" + a click-to-copy anchor link icon to every H2/H3 inside
    <main>. If the post has ≥5 H2 headings, build a table-of-contents card
    and insert it at the top of <main>."""
    if '"@type":"BlogPosting"' not in html:
        return html
    m = _MAIN_RE.search(html)
    if not m:
        return html
    pre, body, post = m.group(1), m.group(2), m.group(3)
    h2_titles: list[tuple[str, str]] = []
    labels = _labels(html)

    def patch_heading(hm: re.Match[str]) -> str:
        level = hm.group(1).lower()
        inner = hm.group(2)
        text = re.sub(r'<[^>]+>', '', inner).strip()
        if not text:
            return hm.group(0)
        slug = slugify(text)
        if level == "h2":
            h2_titles.append((slug, text))
        return (
            f'<{level} id="{slug}">{inner} '
            f'<a class="heading-anchor" href="#{slug}" aria-label="{labels["Link to"]} {text}">#</a>'
            f'</{level}>'
        )

    new_body = _HEADING_RE.sub(patch_heading, body)
    toc_html = ""
    if len(h2_titles) >= 5:
        items = "".join(
            f'<li><a href="#{slug}">{text}</a></li>' for slug, text in h2_titles
        )
        toc_html = (
            f'<aside class="article-toc" aria-label="{labels["Table of contents"]}">'
            f'<h2>{labels["Contents"]}</h2>'
            f'<ol>{items}</ol></aside>'
        )
    return html[: m.start()] + pre + toc_html + new_body + post + html[m.end():]


_NON_BODY_ASIDE_RE = re.compile(
    r'<aside\s+class="(?:author-card|related-posts|post-lead|article-sources|article-toc)\b[^"]*"[\s\S]*?</aside>',
    re.IGNORECASE,
)


def _extract_citations(html: str) -> list[dict[str, str]]:
    """Return at most 12 distinct authoritative outbound links from the
    article body. Strips author-card / related-posts / post-lead / ToC /
    article-sources asides first so the author's own profile links and
    nav chrome don't pollute the citation graph."""
    main_m = _MAIN_RE.search(html)
    if not main_m:
        return []
    body = _NON_BODY_ASIDE_RE.sub('', main_m.group(2))
    seen: set[str] = set()
    out: list[dict[str, str]] = []
    for lm in _OUTBOUND_LINK_RE.finditer(body):
        url = lm.group(1)
        if url in seen:
            continue
        seen.add(url)
        host = url.split("/", 3)[2].lower() if url.count("/") >= 2 else ""
        if not any(host == d or host.endswith("." + d) for d in CITATION_AUTHORITIES):
            continue
        out.append({"@type": "CreativeWork", "url": url})
        if len(out) >= 12:
            break
    return out


def build_post_nav_index(pages: list[Path]) -> dict[str, tuple[tuple[str, str] | None, tuple[str, str] | None]]:
    """Build a slug -> (prev, next) lookup over every dated post in pages.

    A dated post is one whose parent directory name matches ``YYYY-MM-DD-…``.
    Order is chronological (oldest first); 'prev' is older, 'next' is newer.
    Each entry is (slug, title) so the renderer can localize labels per
    target page.
    """
    dated: list[tuple[str, str, str]] = []
    for p in pages:
        slug = p.parent.name
        if not _DATED_SLUG_RE.match(slug):
            continue
        # Skip French translations — they share the slug with the English
        # original. Including both would double-count and yield wrong nav.
        if p.parent.parent.name == "fr":
            continue
        html = p.read_text(encoding="utf-8", errors="ignore")
        if '"@type":"BlogPosting"' not in html:
            continue
        m = _H1_RE.search(html)
        title = m.group(1).strip() if m else slug
        dated.append((slug[:10], slug, title))
    dated.sort(key=lambda t: t[0])
    out: dict[str, tuple[tuple[str, str] | None, tuple[str, str] | None]] = {}
    for i, entry in enumerate(dated):
        prev_e = (dated[i - 1][1], dated[i - 1][2]) if i > 0 else None
        next_e = (dated[i + 1][1], dated[i + 1][2]) if i < len(dated) - 1 else None
        out[entry[1]] = (prev_e, next_e)
    return out


def build_fr_title_index(pages: list[Path]) -> dict[str, str]:
    """Walk rendered FR pages, return ``en_slug -> FR H1 title`` so the
    prev/next nav on a FR page can advertise the FR title for the
    neighbouring article instead of the English H1.
    """
    out: dict[str, str] = {}
    for p in pages:
        if p.parent.parent.name != "fr":
            continue
        slug = p.parent.name  # FR slug
        if not _DATED_SLUG_RE.match(slug):
            continue
        en = _en_slug(slug)
        if en == slug:  # not in slug map
            continue
        html = p.read_text(encoding="utf-8", errors="ignore")
        m = _H1_RE.search(html)
        if m:
            out[en] = m.group(1).strip()
    return out


_FAQ_H2_RE = re.compile(
    r'<h2 id="(frequently-asked-questions|foire-aux-questions)"[^>]*>'
    r'([\s\S]+?)</h2>'
    r'([\s\S]+?)'
    r'(?=<h2|<aside|</main>|<hr|<footer)',
)


def _convert_faq_to_qa(html: str) -> str:
    """Convert the plain ``<p><strong>Q?</strong></p><p>A</p>…`` FAQ
    structure inside articles into the collapsible ``<details class="qa-item">``
    pattern used by ``/projects/`` and ``/papers/`` for UX/UI consistency.
    """
    is_fr = _is_french(html)
    headline = "Questions ?" if is_fr else "Questions?"
    soft = "Réponses." if is_fr else "Answers."

    def patch(m: re.Match[str]) -> str:
        faq_id = m.group(1)  # preserve original anchor so TOC links stay valid
        body = m.group(3)
        # Strip the trailing "<a class='heading-anchor'>#</a>" inside H2.
        # Walk for Q/A pairs: <p><strong>Q?</strong></p><p>A</p>
        qa_pairs: list[tuple[str, str]] = []
        # Capture Q + multiple following <p>…</p> until next <p><strong>...?</strong></p>.
        # Build a list of P-segments first, then pair Q with the answer chunk.
        segments: list[str] = [
            sm.group(1).strip()
            for sm in re.finditer(r'<p>([\s\S]*?)</p>', body)
        ]
        i = 0
        while i < len(segments):
            seg = segments[i]
            # Q heuristic: starts with <strong> and ends with ? (or French ?)
            qm = re.match(r'^<strong>([\s\S]+?)</strong>\s*$', seg)
            if qm:
                question = qm.group(1).strip()
                # Collect answer paragraphs until next strong-only paragraph
                ans_parts: list[str] = []
                j = i + 1
                while j < len(segments):
                    nxt = segments[j]
                    if re.match(r'^<strong>[\s\S]+?</strong>\s*$', nxt):
                        break
                    ans_parts.append(nxt)
                    j += 1
                qa_pairs.append((question, "</p><p>".join(ans_parts)))
                i = j
            else:
                i += 1

        if not qa_pairs:
            return m.group(0)

        new_h2 = (
            f'<h2 id="{faq_id}" class="qa-headline">{headline} '
            f'<span class="qa-headline-soft">{soft}</span></h2>'
        )
        out_parts: list[str] = [new_h2, f'<section class="qa-list" aria-labelledby="{faq_id}">']
        for q, a in qa_pairs:
            out_parts.append(
                f'<details class="qa-item"><summary class="qa-q">{q}</summary>'
                f'<section class="qa-a"><p>{a}</p></section></details>'
            )
        out_parts.append('</section>')
        return "".join(out_parts)

    return _FAQ_H2_RE.sub(patch, html)


def inject_prev_next_nav(
    html: str,
    slug: str,
    nav_index: dict[str, tuple[tuple[str, str] | None, tuple[str, str] | None]],
    is_fr: bool = False,
    fr_titles: dict[str, str] | None = None,
) -> str:
    """Inject a <nav class="post-pagination"> with prev/next links just
    before the closing ``</div></main>`` of any dated BlogPosting page.
    Localized via _labels(html); French pages get French labels and links
    pointing to the matching FR slug under ``/fr/``."""
    if '"@type":"BlogPosting"' not in html:
        return html
    # For FR pages the page's slug is the FR slug — look up by EN counterpart.
    lookup_slug = _en_slug(slug) if is_fr else slug
    if lookup_slug not in nav_index:
        return html
    if 'class="post-pagination"' in html:
        return html
    prev_e, next_e = nav_index[lookup_slug]
    if not prev_e and not next_e:
        return html
    labels = _labels(html)
    fr_titles = fr_titles or {}

    def render(entry: tuple[str, str] | None, direction: str, label: str) -> str:
        if not entry:
            return '<span class="post-pagination-stub" aria-hidden="true"></span>'
        s, t = entry
        # On FR pages, point at the FR sibling under /fr/<fr-slug>/.
        # Look up the FR title from fr_titles so prev/next advertises in French.
        if is_fr and s in EN_TO_FR:
            href = f"/fr/{EN_TO_FR[s]}/"
            t = fr_titles.get(s, t)
        else:
            href = f"/{s}/"
        return (
            f'<a class="post-pagination-{direction}" href="{href}">'
            f'<span class="post-pagination-label">{label}</span>'
            f'<span class="post-pagination-title">{t}</span>'
            f'</a>'
        )

    inner = render(prev_e, "prev", labels["Previous"]) + render(next_e, "next", labels["Next"])
    nav = f'<nav class="post-pagination" aria-label="{labels["Article pagination"]}">{inner}</nav>'
    return re.sub(r'(</div>\s*</main>)', nav + r'\1', html, count=1)


def inject_citations(html: str) -> str:
    """Append a "citation" array to the BlogPosting JSON-LD listing the
    authoritative outbound URLs the post references. AI engines extract
    citation graphs from this property to build provenance chains."""
    if '"@type":"BlogPosting"' not in html:
        return html
    cites = _extract_citations(html)
    if not cites:
        return html
    import json as _json
    fragment = ',"citation":' + _json.dumps(cites, separators=(",", ":"))
    # Insert just before the "speakable" key in the BlogPosting object.
    return re.sub(
        r'(,"speakable":)',
        fragment + r'\1',
        html,
        count=1,
    )


_MERMAID_BLOCK_RE = re.compile(
    r'<pre[^>]*>\s*<code\s+class="language-mermaid"[^>]*>([\s\S]*?)</code>\s*</pre>',
    re.IGNORECASE,
)


def inject_mermaid(html: str) -> str:
    """Convert ```mermaid fenced blocks into <pre class="mermaid"> containers
    so main.js can lazy-load the Mermaid library and render them. Also
    widens the meta-CSP script-src to allow the cdn.jsdelivr.net import,
    but only on pages that actually contain a Mermaid block."""
    if 'language-mermaid' not in html:
        return html
    import html as _h

    def replace(m: re.Match[str]) -> str:
        # Strip <span> wrappers a syntax highlighter may have added,
        # then unescape entities — Mermaid wants the raw source.
        inner = re.sub(r'<[^>]+>', '', m.group(1))
        return f'<pre class="mermaid">{_h.escape(_h.unescape(inner))}</pre>'

    new_html = _MERMAID_BLOCK_RE.sub(replace, html)
    if new_html == html:
        return html

    # Widen the meta-CSP for this page so the dynamic import resolves.
    def patch_csp(tag_match: re.Match[str]) -> str:
        tag = tag_match.group(0)

        def patch_content(c: re.Match[str]) -> str:
            policy = c.group(3)
            if "cdn.jsdelivr.net" in policy:
                return c.group(0)
            new_policy = re.sub(
                r"(script-src)(\s+)",
                r"\1 https://cdn.jsdelivr.net\2",
                policy,
                count=1,
            )
            return c.group(1) + c.group(2) + new_policy + c.group(4)

        return content_attr_re.sub(patch_content, tag, count=1)

    return csp_tag_re.sub(patch_csp, new_html, count=1)


def inject_sources_list(html: str) -> str:
    """Mirror the JSON-LD citation array as a human-visible <aside> so the
    primary-source references are visible to readers, not just AI crawlers.
    Inserted just before the prev/next nav so it sits at the foot of every
    dated post. Idempotent."""
    if '"@type":"BlogPosting"' not in html:
        return html
    if 'class="article-sources"' in html:
        return html
    cites = _extract_citations(html)
    if not cites:
        return html
    items: list[str] = []
    for c in cites:
        url = c["url"]
        parts = url.split("/", 3)
        host = parts[2] if len(parts) > 2 else url
        path = "/" + parts[3] if len(parts) > 3 else ""
        display = path if len(path) <= 80 else path[:77] + "…"
        items.append(
            f'<li><a href="{url}" rel="external noopener nofollow">'
            f'<span class="source-host">{host}</span>'
            f'<span class="source-path">{display}</span>'
            f'</a></li>'
        )
    heading = _labels(html)["Sources & references"]
    fragment = (
        '<aside class="article-sources" aria-labelledby="sources-heading">'
        f'<h2 id="sources-heading" class="article-sources-heading">{heading}</h2>'
        f'<ol class="article-sources-list">{"".join(items)}</ol>'
        '</aside>'
    )
    # Insert before the prev/next nav if it's already there, else before
    # the closing </div></main>.
    if 'class="post-pagination"' in html:
        return re.sub(r'(<nav class="post-pagination")', fragment + r'\1', html, count=1)
    return re.sub(r'(</div>\s*</main>)', fragment + r'\1', html, count=1)


_HEAD_END_RE = re.compile(r'</head>', re.IGNORECASE)
_HREFLANG_RE = re.compile(r'<link\s+rel="alternate"\s+hreflang="[^"]+"[^/]*/>', re.IGNORECASE)


# Speculation Rules API — prerender same-origin pages on hover so any
# navigation feels instant. The CSP allows it via 'inline-speculationrules'
# in script-src; no per-page hash needed.
SPECULATION_RULES_BLOCK = (
    '<script type="speculationrules">'
    '{"prerender":[{'
    '"where":{"and":['
    '{"href_matches":"/*"},'
    '{"not":{"href_matches":"/_csp/*"}},'
    '{"not":{"href_matches":"/*.xml"}},'
    '{"not":{"href_matches":"/*.json"}},'
    '{"not":{"href_matches":"/*.txt"}},'
    '{"not":{"href_matches":"/*.pdf"}},'
    '{"not":{"href_matches":"/manifest.json"}},'
    '{"not":{"href_matches":"/sw.js"}},'
    '{"not":{"href_matches":"/contact/*"}},'
    '{"not":{"href_matches":"/fr/contact/*"}}'
    ']},'
    '"eagerness":"moderate"'
    '}]}'
    '</script>'
)


_BODY_LINK_STYLESHEET_RE = re.compile(
    r'<link\b[^>]*\brel=(?:"stylesheet"|stylesheet)[^>]*>',
    re.IGNORECASE,
)
_BODY_END_RE = re.compile(r'</head>', re.IGNORECASE)


def hoist_body_link_stylesheets(html: str) -> tuple[str, int]:
    """SSG's inline search widget renders ``<link rel=stylesheet>`` *inside*
    ``<body>`` next to ``#ssg-search-widget``. That's an HTML5 spec violation
    (link in body) and pa11y AAA flags it on every page that ships the widget.
    Hoist any in-body stylesheet ``<link>`` up into ``<head>`` so the document
    parses cleanly."""
    head_end_m = _BODY_END_RE.search(html)
    if not head_end_m:
        return html, 0
    head_end = head_end_m.start()
    head, body = html[:head_end], html[head_end:]
    matches = list(_BODY_LINK_STYLESHEET_RE.finditer(body))
    if not matches:
        return html, 0
    # Strip from body in reverse so offsets stay valid; collect for hoisting.
    extracted: list[str] = []
    new_body = body
    for m in reversed(matches):
        extracted.insert(0, m.group(0))
        new_body = new_body[:m.start()] + new_body[m.end():]
    return head + "".join(extracted) + new_body, len(extracted)


def inject_speculation_rules(html: str) -> str:
    """Inject the Speculation Rules API block before </head>. Idempotent."""
    if 'type="speculationrules"' in html:
        return html
    return _HEAD_END_RE.sub(SPECULATION_RULES_BLOCK + '</head>', html, count=1)


# ---------------------------------------------------------------------------
# Live GitHub repo stats — injected into project cards on /projects/ and
# the home page. Source data: public/_data/gh-stats.json (refreshed
# nightly by .github/workflows/refresh-gh-stats.yml). Build-time
# injection beats a runtime fetch: zero JS, zero CLS, zero rate-limit
# risk.
# ---------------------------------------------------------------------------

import json as _gh_json
from datetime import UTC
from datetime import datetime as _gh_dt

_GH_STATS_PATH = Path("_data/gh-stats.json")
_GH_CARD_RE = re.compile(
    r'(<article class=(?:"(?:newsroom-card|proj-card)[^"]*"|(?:newsroom-card|proj-card))[^>]*>)'
    r'([\s\S]+?)(</article>)',
)
_GH_REPO_HREF_RE = re.compile(
    r'href=["\']?https?://github\.com/(sebastienrousseau/[a-zA-Z0-9._-]+)/?["\']?',
)
_GH_HREF_RE = re.compile(r'href=(?:"([^"]+)"|([^\s>]+))')


def _gh_stats_index() -> dict[str, dict]:
    if not _GH_STATS_PATH.is_file():
        return {}
    try:
        data = _gh_json.loads(_GH_STATS_PATH.read_text(encoding="utf-8"))
    except _gh_json.JSONDecodeError:
        return {}
    return {entry["slug"]: entry for entry in data.get("repos", []) if "slug" in entry}


_GH_RELATIVE_LIMITS = (
    (60, "il y a {n} s", "{n}s ago"),
    (3600, "il y a {n} min", "{n}m ago"),
    (86400, "il y a {n} h", "{n}h ago"),
    (604800, "il y a {n} j", "{n}d ago"),
    (2629800, "il y a {n} sem.", "{n}w ago"),
    (31557600, "il y a {n} mois", "{n}mo ago"),
)


def _relative_time(iso_ts: str, fr: bool = False) -> str:
    """Render an ISO-8601 timestamp as a 'N units ago' label."""
    if not iso_ts:
        return ""
    try:
        # GH returns "2026-05-15T16:34:21Z"
        ts = _gh_dt.fromisoformat(iso_ts.replace("Z", "+00:00"))
    except ValueError:
        return ""
    delta = (_gh_dt.now(tz=UTC) - ts).total_seconds()
    if delta < 0:
        delta = 0
    if delta < 60:
        n = int(delta)
        return f"il y a {n} s" if fr else f"{n}s ago"
    if delta < 3600:
        n = int(delta // 60)
        return f"il y a {n} min" if fr else f"{n}m ago"
    if delta < 86400:
        n = int(delta // 3600)
        return f"il y a {n} h" if fr else f"{n}h ago"
    if delta < 604800:
        n = int(delta // 86400)
        return f"il y a {n} j" if fr else f"{n}d ago"
    if delta < 2629800:
        n = int(delta // 604800)
        return f"il y a {n} sem." if fr else f"{n}w ago"
    if delta < 31557600:
        n = int(delta // 2629800)
        return f"il y a {n} mois" if fr else f"{n}mo ago"
    n = int(delta // 31557600)
    return f"il y a {n} an{'s' if n > 1 else ''}" if fr else f"{n}y ago"


def _format_count(n: int) -> str:
    """1234 -> 1.2k, 1234567 -> 1.2M."""
    if n >= 1000000:
        return f"{n / 1000000:.1f}M".replace(".0M", "M")
    if n >= 1000:
        return f"{n / 1000:.1f}k".replace(".0k", "k")
    return str(n)


def _render_gh_badges(info: dict, fr: bool) -> str:
    stars = info.get("stars", 0)
    forks = info.get("forks", 0)
    license_id = info.get("license", "")
    pushed = info.get("pushed_at", "")
    pushed_rel = _relative_time(pushed, fr=fr)
    label_last = "dernier commit" if fr else "last commit"
    aria_stars = (f"{stars} étoiles" if fr else f"{stars} stars") if stars else ""
    aria_forks = f"{forks} forks" if forks else ""
    parts: list[str] = []
    if stars:
        parts.append(
            f'<span class="gh-stat gh-stars" aria-label="{aria_stars}">'
            f'<span class="gh-ico" aria-hidden="true">★</span>'
            f'<span class="gh-num">{_format_count(stars)}</span></span>'
        )
    if forks:
        parts.append(
            f'<span class="gh-stat gh-forks" aria-label="{aria_forks}">'
            f'<span class="gh-ico" aria-hidden="true">⑂</span>'
            f'<span class="gh-num">{_format_count(forks)}</span></span>'
        )
    if license_id and license_id not in ("NOASSERTION", "", "OTHER"):
        parts.append(
            f'<span class="gh-stat gh-license">'
            f'<span class="gh-txt">{license_id}</span></span>'
        )
    if pushed_rel:
        parts.append(
            f'<span class="gh-stat gh-pushed" title="{pushed[:10]}">'
            f'<span class="gh-txt">{label_last} {pushed_rel}</span></span>'
        )
    if not parts:
        return ""
    aria = "Statistiques du dépôt" if fr else "Repository stats"
    return f'<p class="gh-stats-row" aria-label="{aria}">{"".join(parts)}</p>'


def _normalise_url(u: str) -> str:
    """Normalise a URL for equality: drop scheme, www., trailing slash, lower-case."""
    u = u.strip().lower()
    u = re.sub(r'^https?://', '', u)
    u = re.sub(r'^www\.', '', u)
    return u.rstrip('/')


def _gh_lookup(inner: str, stats_index: dict[str, dict]) -> dict | None:
    """Resolve a card to its repo entry using, in order:
       1) any github.com/sebastienrousseau/<slug> href
       2) the homepage URL recorded in the stats payload
          (scheme / www / trailing-slash insensitive)
       3) the card's <h3> text matching the repo name (case-insensitive).
    """
    if not stats_index:
        return None
    # 1) direct GH link
    m = _GH_REPO_HREF_RE.search(inner)
    if m and m.group(1) in stats_index:
        return stats_index[m.group(1)]
    # 2 + 3) build small lookup helpers
    homepage_idx = {
        _normalise_url(e.get("homepage") or ""): e
        for e in stats_index.values()
        if e.get("homepage")
    }
    name_idx = {(e.get("name") or "").lower(): e for e in stats_index.values()}
    # 2) homepage match (handle quoted + unquoted href on the home shell)
    for hm in _GH_HREF_RE.finditer(inner):
        href = (hm.group(1) or hm.group(2) or "").strip()
        if not href.startswith(("http://", "https://")):
            continue
        key = _normalise_url(href)
        if key in homepage_idx:
            return homepage_idx[key]
    # 3) h3 text match
    h3 = re.search(r'<h3[^>]*>\s*<a[^>]*>([^<]+)</a>', inner)
    if h3:
        title = h3.group(1).strip().lower()
        if title in name_idx:
            return name_idx[title]
    return None


def inject_github_stats(html: str, stats_index: dict[str, dict]) -> str:
    """Inject star / fork / last-commit badges into every newsroom-card
    on the page whose first GitHub anchor or project homepage URL
    matches a tracked repo."""
    if not stats_index or 'newsroom-card' not in html:
        return html
    is_fr = _is_french(html)

    def patch(m: re.Match[str]) -> str:
        open_tag, inner, close_tag = m.group(1), m.group(2), m.group(3)
        # Skip if badges already injected.
        if 'class="gh-stats-row"' in inner:
            return m.group(0)
        info = _gh_lookup(inner, stats_index)
        if not info:
            return m.group(0)
        badges = _render_gh_badges(info, fr=is_fr)
        if not badges:
            return m.group(0)
        # Insert before </div></article> (after the body, inside the card).
        inner_new = re.sub(
            r'(</div>\s*)$',
            badges + r'\1',
            inner,
            count=1,
        )
        if inner_new == inner:
            inner_new = inner + badges
        return open_tag + inner_new + close_tag

    return _GH_CARD_RE.sub(patch, html)


def _translated_slugs() -> tuple[set[str], set[str]]:
    """Discover which EN and FR slugs have rendered counterparts under
    ``public/``. Returns ``(en_slugs_with_fr, fr_slugs_with_en)``.
    """
    fr_dir = PUBLIC / "fr"
    if not fr_dir.is_dir():
        return set(), set()
    rendered_fr = {p.parent.name for p in fr_dir.glob("*/index.html")}
    en_with_fr = {en for en, fr in EN_TO_FR.items() if fr in rendered_fr}
    fr_with_en = rendered_fr & set(FR_TO_EN.keys())
    return en_with_fr, fr_with_en


# Top-level EN static pages with FR mirrors. Synced with
# scripts/build_translations.py::STATIC_SLUG_FR — kept here as a flat
# dict for postbuild's hreflang injector.
_STATIC_EN_TO_FR: dict[str, str] = {
    "about": "a-propos",
    "papers": "publications",
    "projects": "projets",
    "topics": "sujets",
    "tags": "etiquettes",
    "contact": "contact",
    "accessibility": "accessibilite",
    "privacy": "confidentialite",
    "terms": "conditions",
    "playlists": "playlists",
    "made-with-static-site-generator": "concu-avec-static-site-generator",
    "made-with-shokunin": "concu-avec-shokunin",
    "404": "404",
    "offline": "hors-ligne",
    "thanks": "merci",
    "articles": "articles",
}


def inject_hreflang(
    html: str,
    slug: str,
    lang: str,
    en_with_fr: set[str],
    fr_with_en: set[str],
) -> str:
    """Inject reciprocal hreflang links so Google + crawlers (and the
    language-selector JS) pair the two language versions. Translates
    EN ↔ FR slug via :mod:`_fr_slugs` for articles, and via
    :data:`_STATIC_EN_TO_FR` for top-level static pages.
    """
    if lang == "fr":
        if slug in fr_with_en:
            en = _en_slug(slug)
            fr = slug
            en_url = f"https://sebastienrousseau.com/{en}/"
            fr_url = f"https://sebastienrousseau.com/fr/{fr}/"
        else:
            # Static page under /fr/<fr-slug>/ — already wired by the
            # FR renderer in build_translations.py.
            return html
    else:
        if slug in en_with_fr:
            en = slug
            fr = _fr_slug(slug)
            en_url = f"https://sebastienrousseau.com/{en}/"
            fr_url = f"https://sebastienrousseau.com/fr/{fr}/"
        elif slug in _STATIC_EN_TO_FR:
            en_url = f"https://sebastienrousseau.com/{slug}/"
            fr_url = f"https://sebastienrousseau.com/fr/{_STATIC_EN_TO_FR[slug]}/"
        else:
            return html
    # Strip any existing hreflang link tags so we don't duplicate.
    html = _HREFLANG_RE.sub('', html)
    links = (
        f'<link rel="alternate" hreflang="en" href="{en_url}" />'
        f'<link rel="alternate" hreflang="fr" href="{fr_url}" />'
        f'<link rel="alternate" hreflang="x-default" href="{en_url}" />'
    )
    return _HEAD_END_RE.sub(links + '</head>', html, count=1)


def main() -> None:  # noqa: C901 — postbuild orchestrator; per-pass counters are sequential by design
    pages = list(PUBLIC.rglob("*.html"))
    # Pre-pass: build the chronological prev/next index over every dated
    # BlogPosting page. Indexed once per build, then read per page.
    nav_index = build_post_nav_index(pages)
    fr_titles = build_fr_title_index(pages)
    en_with_fr, fr_with_en = _translated_slugs()
    gh_stats = _gh_stats_index()
    sri_patched = 0
    csp_patched = 0
    itemlist_patched = 0
    social_patched = 0
    og_patched = 0
    img_dims_patched = 0
    howto_patched = 0
    link_hoisted = 0
    wc_patched = 0
    about_patched = 0
    furniture_patched = 0
    anchor_patched = 0
    citation_patched = 0
    sources_patched = 0
    mermaid_patched = 0
    nav_patched = 0
    hreflang_patched = 0
    for page in pages:
        original = page.read_text(encoding="utf-8", errors="ignore")
        patched = fix_sri(original)
        if patched != original:
            sri_patched += 1
        # ItemList must run BEFORE the JSON-LD CSP-hash pass so the new
        # block's hash gets included in the page's script-src.
        patched_il = inject_itemlist(page, patched)
        if patched_il != patched:
            itemlist_patched += 1
        patched_si = fix_social_image(patched_il)
        if patched_si != patched_il:
            social_patched += 1
        patched_og = inject_og_completeness(page, patched_si)
        if patched_og != patched_si:
            og_patched += 1
        patched_dim, n_dim = stamp_image_dimensions(patched_og)
        img_dims_patched += n_dim
        patched_howto = inject_howto(page, patched_dim)
        if patched_howto != patched_dim:
            howto_patched += 1
        patched_wc = inject_word_count(patched_howto)
        if patched_wc != patched_si:
            wc_patched += 1
        patched_about = inject_about(patched_wc)
        if patched_about != patched_wc:
            about_patched += 1
        # Article furniture (tag badges + meta bar + ToC + anchor links +
        # citation graph) MUST run after wordCount + about have populated
        # the BlogPosting JSON-LD, but BEFORE the JSON-LD CSP-hash pass so
        # the citation array is included in the hash.
        patched_fu = inject_article_furniture(patched_about)
        if patched_fu != patched_about:
            furniture_patched += 1
        patched_an = inject_anchor_links_and_toc(patched_fu)
        if patched_an != patched_fu:
            anchor_patched += 1
        # Convert article FAQ structure (`<p><strong>Q?</strong></p><p>A</p>`)
        # to the collapsible <details class="qa-item"> pattern for UX parity
        # with /projects/ and /papers/.
        patched_an = _convert_faq_to_qa(patched_an)
        patched_ci = inject_citations(patched_an)
        if patched_ci != patched_an:
            citation_patched += 1
        patched_src = inject_sources_list(patched_ci)
        if patched_src != patched_ci:
            sources_patched += 1
        patched_mermaid = inject_mermaid(patched_src)
        if patched_mermaid != patched_src:
            mermaid_patched += 1
            patched_src = patched_mermaid
        # Prev/next nav must run AFTER inject_sources_list because the
        # sources injector anchors against either the nav or the </main>;
        # placing nav first would push sources above the nav cleanly.
        page_is_fr = page.parent.parent.name == "fr"
        patched_nav = inject_prev_next_nav(
            patched_src, page.parent.name, nav_index, is_fr=page_is_fr,
            fr_titles=fr_titles,
        )
        if patched_nav != patched_src:
            nav_patched += 1
        # Reciprocal hreflang for paired English/French pages.
        rel_slug = page.parent.name
        is_fr = page.parent.parent.name == "fr"
        # Special case: the site root /index.html. Its parent dir is
        # "public" — we treat it as the home and emit hreflang to /fr/.
        if page.parent.name == "public" or (page.name == "index.html" and page.parent == PUBLIC):
            _head_re = re.compile(r'</head>', re.IGNORECASE)
            _hf_re = re.compile(r'<link rel="alternate"[^>]+hreflang="[^"]+"[^/]*/>', re.IGNORECASE)
            cleaned = _hf_re.sub('', patched_nav)
            home_links = (
                '<link rel="alternate" hreflang="en" href="https://sebastienrousseau.com/" />'
                '<link rel="alternate" hreflang="fr" href="https://sebastienrousseau.com/fr/" />'
                '<link rel="alternate" hreflang="x-default" href="https://sebastienrousseau.com/" />'
            )
            patched_hl = _head_re.sub(home_links + '</head>', cleaned, count=1)
        else:
            patched_hl = inject_hreflang(
                patched_nav,
                rel_slug,
                "fr" if is_fr else "en",
                en_with_fr,
                fr_with_en,
            )
        if patched_hl != patched_nav:
            hreflang_patched += 1
        # Speculation Rules — hover-prerender every internal link.
        patched_hl = inject_speculation_rules(patched_hl)
        # Live GitHub stats on project / home cards.
        patched_hl = inject_github_stats(patched_hl, gh_stats)
        # Hoist any <link rel=stylesheet> SSG injected inside <body> back
        # into <head> so pa11y AAA stops flagging "link in body".
        patched_hl, n_hoisted = hoist_body_link_stylesheets(patched_hl)
        link_hoisted += n_hoisted
        patched2 = inject_jsonld_hashes(patched_hl)
        if patched2 != patched_nav:
            csp_patched += 1
        if patched2 != original:
            page.write_text(patched2, encoding="utf-8")

    # Refresh sitemap lastmod from each post's frontmatter last_reviewed.
    lastmod_index = build_lastmod_index()
    sitemap_patched = refresh_sitemap_lastmod(PUBLIC / "sitemap.xml", lastmod_index)

    # Overwrite robots.txt + llms.txt with the curated versions.
    robots_written = write_robots(PUBLIC)
    llms_written = write_llms_txt(PUBLIC)
    llms_full_written = write_llms_full_txt(PUBLIC)

    # Repair Shokunin's RSS / Atom / news-sitemap URLs (.meta/ + localhost).
    # Must run BEFORE the ampersand-escape pass so the URL rewrite operates
    # on the original string and doesn't get derailed by escaped ampersands
    # in titles.
    feed_urls_patched = fix_xml_feed_urls(PUBLIC)
    # Repair Shokunin's RSS / news-sitemap output (bare & in titles).
    xml_patched = fix_xml_feeds(PUBLIC)

    print(
        f"postbuild: {len(pages)} HTML pages, "
        f"{sri_patched} got real SRI, "
        f"{itemlist_patched} got ItemList JSON-LD, "
        f"{social_patched} got og:image fixed, "
        f"{og_patched} got og:url/locale/site_name, "
        f"{img_dims_patched} img(s) stamped w/h, "
        f"{howto_patched} HowTo schema(s) injected, "
        f"{wc_patched} got wordCount, "
        f"{about_patched} got about/mentions entities, "
        f"{furniture_patched} got tag badges + meta bar, "
        f"{anchor_patched} got anchor links + ToC, "
        f"{citation_patched} got citation graphs, "
        f"{sources_patched} got visible sources list, "
        f"{mermaid_patched} got mermaid blocks, "
        f"{nav_patched} got prev/next nav, "
        f"{hreflang_patched} got hreflang pairs, "
        f"{csp_patched} got CSP JSON-LD hashes, "
        f"{sitemap_patched} sitemap entries refreshed, "
        f"{feed_urls_patched} feed(s) URL-repaired, "
        f"{xml_patched} XML feed(s) scrubbed, "
        f"robots.txt {'updated' if robots_written else 'unchanged'}, "
        f"llms.txt {'updated' if llms_written else 'unchanged'}, "
        f"llms-full.txt {'updated' if llms_full_written else 'unchanged'}"
    )


if __name__ == "__main__":
    main()
