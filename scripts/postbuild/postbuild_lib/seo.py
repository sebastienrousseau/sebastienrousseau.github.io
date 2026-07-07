"""SEO + Schema.org injection passes.

This module owns the section-4-through-6 helpers that postbuild
applies to every rendered HTML page:

* fix_social_image — rebuild og:image / twitter:image from the
  BlogPosting JSON-LD's image[0] when SSG picked a body inline.
* build_about_graph + inject_about — link articles to canonical
  entities so AI engines can ground them in Wikidata / their KGs.
* compute_word_count + inject_word_count — set wordCount inside
  every BlogPosting block.
* _build_howto_jsonld + inject_howto — emit HowTo schema for
  step-by-step posts.
* stamp_image_dimensions — width + height attributes for every img.
* _lang_to_og_locale + inject_og_completeness — fill og:url /
  og:locale / og:site_name when SSG omits them.
* _current_stem — small helper used by inject_about + inject_howto.

Each entry point is a pure function over HTML text; module-level
state is regex constants only.
"""

from __future__ import annotations

import html as _html
import json as _json
import re
from pathlib import Path

PUBLIC = Path("public")
POSTS = Path("_posts")


# ---------------------------------------------------------------------------
# 4. og:image / twitter:image rewrite
# ---------------------------------------------------------------------------

# Static Site Generator's auto-generated og:image scans the body and picks up the first
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
    "CRYSTALS-Kyber": (
        "https://en.wikipedia.org/wiki/Kyber",
        "Q116727584",
        "2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age",
    ),
    "post-quantum cryptography": (
        "https://en.wikipedia.org/wiki/Post-quantum_cryptography",
        "Q1364608",
        "2025-09-01-quantum-safe-payments-epaa",
    ),
    "lattice-based cryptography": (
        "https://en.wikipedia.org/wiki/Lattice-based_cryptography",
        "Q6499614",
        "2024-04-15-quantum-algorithm-challenges-lattice-based-cryptography",
    ),
    "Quantum key distribution": (
        "https://en.wikipedia.org/wiki/Quantum_key_distribution",
        "Q768051",
        "2023-12-11-quantum-key-distribution-revolutionising-security-in-banking",
    ),
    "Shor's algorithm": (
        "https://en.wikipedia.org/wiki/Shor%27s_algorithm",
        "Q717409",
        "2026-04-11-quantum-thresholds-are-moving-again",
    ),
    "homomorphic encryption": (
        "https://en.wikipedia.org/wiki/Homomorphic_encryption",
        "Q2154943",
        "2024-03-25-fully-homomorphic-encryption-in-a-banking-quantum-era",
    ),
    "Quantum computing": ("https://en.wikipedia.org/wiki/Quantum_computing", "Q484641", None),
    "NIST PQC": ("https://csrc.nist.gov/projects/post-quantum-cryptography", None, None),
    "ISO 20022": (
        "https://www.iso20022.org/",
        "Q15727611",
        "2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001",
    ),
    "SWIFT gpi": ("https://www.swift.com/our-solutions/swift-gpi", None, None),
    "SEPA": ("https://en.wikipedia.org/wiki/Single_Euro_Payments_Area", "Q286094", None),
    "Large language model": (
        "https://en.wikipedia.org/wiki/Large_language_model",
        "Q115305900",
        "2026-05-11-lucy-besson-knowledge-transfer-ai-quantum",
    ),
    "Generative AI": (
        "https://en.wikipedia.org/wiki/Generative_artificial_intelligence",
        "Q108766533",
        "2023-11-12-exploring-generative-ai",
    ),
    "Artificial intelligence": (
        "https://en.wikipedia.org/wiki/Artificial_intelligence",
        "Q11660",
        None,
    ),
    "Multimodal learning": (
        "https://en.wikipedia.org/wiki/Multimodal_learning",
        "Q117259025",
        "2024-03-18-advancing-ai-with-multimodal-llms-insights-from-mm1",
    ),
    "Rust": ("https://en.wikipedia.org/wiki/Rust_(programming_language)", "Q575650", None),
    "Python": ("https://en.wikipedia.org/wiki/Python_(programming_language)", "Q28865", None),
    "Blockchain": (
        "https://en.wikipedia.org/wiki/Blockchain",
        "Q20514253",
        "2018-01-02-blockchain-the-technology-that-matters-in-2018",
    ),
    "Bitcoin": (
        "https://en.wikipedia.org/wiki/Bitcoin",
        "Q131723",
        "2018-01-01-bitcoin-the-year-in-review",
    ),
    "Ethereum": (
        "https://en.wikipedia.org/wiki/Ethereum",
        "Q21825854",
        "2018-01-24-the-erc-20-token-standard",
    ),
    "ERC-20": (
        "https://en.wikipedia.org/wiki/Ethereum#Tokens",
        None,
        "2018-01-24-the-erc-20-token-standard",
    ),
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


def _keywords_from_html(html: str) -> list[str]:
    """Pull and clean the comma-separated keywords meta tag."""
    m = _keywords_re.search(html)
    if not m or not m.group(1):
        return []
    return [k.strip() for k in m.group(1).split(",") if k.strip()]


def _keyword_matches_entity(kw_lower: str, entity_lower: str) -> bool:
    """True if the keyword overlaps the entity name in either direction."""
    return kw_lower == entity_lower or entity_lower in kw_lower or kw_lower in entity_lower


def _same_as_anchors(
    ext_url: str, qid: str | None, canonical_stem: str | None, own_stem: str | None
) -> list[str]:
    """Build the ``sameAs`` list for an entity: authoritative external URL,
    plus Wikidata Q-number anchor, plus the user's canonical post (skipped
    when the current page IS the canonical post)."""
    out: list[str] = [ext_url]
    if qid:
        out.append(f"https://www.wikidata.org/wiki/{qid}")
    if canonical_stem and canonical_stem != own_stem:
        out.append(f"{SITE_ROOT}/{canonical_stem}/index.html")
    return out


def _build_entity_node(
    entity: str, ext_url: str, qid: str | None, canonical_stem: str | None, own_stem: str | None
) -> dict[str, object]:
    same_as = _same_as_anchors(ext_url, qid, canonical_stem, own_stem)
    return {
        "@type": "Thing",
        "name": entity,
        "sameAs": same_as if len(same_as) > 1 else same_as[0],
    }


def _match_entities_for_keywords(
    keywords: list[str], own_stem: str | None
) -> list[dict[str, object]]:
    """Walk the keyword list once and emit one entity node per first match."""
    seen: set[str] = set()
    matches: list[dict[str, object]] = []
    for kw in keywords:
        kw_l = kw.lower()
        for entity, (ext_url, qid, canonical_stem) in ENTITY_AUTHORITY.items():
            if entity in seen:
                continue
            if _keyword_matches_entity(kw_l, entity.lower()):
                seen.add(entity)
                matches.append(_build_entity_node(entity, ext_url, qid, canonical_stem, own_stem))
                break
    return matches


def build_about_graph(html: str) -> str | None:
    """Build the BlogPosting ``about`` + ``mentions`` JSON-LD fragment.
    First entity match becomes the primary subject; up to five more land
    in ``mentions``. Returns None when no keyword resolves to an entity."""
    keywords = _keywords_from_html(html)
    if not keywords:
        return None
    matches = _match_entities_for_keywords(keywords, _current_stem(html))
    if not matches:
        return None
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
        rf"\1{fragment},\2",
        html,
        count=1,
    )


# ---------------------------------------------------------------------------
# 5. wordCount injection into BlogPosting
# ---------------------------------------------------------------------------

_main_re = re.compile(r"<main\b[^>]*>([\s\S]*?)</main>", re.IGNORECASE)
_aside_re = re.compile(r"<aside\b[^>]*>([\s\S]*?)</aside>", re.IGNORECASE)
_html_tag_re = re.compile(r"<[^>]+>")
_whitespace_re = re.compile(r"\s+")


def compute_word_count(html: str) -> int | None:
    main_m = _main_re.search(html)
    if not main_m:
        return None
    content = main_m.group(1)
    # Drop asides (lead block, related-cards, etc.) — they're already
    # represented by speakable + isPartOf and aren't the article body.
    content = _aside_re.sub("", content)
    text = _html_tag_re.sub(" ", content)
    text = _whitespace_re.sub(" ", text).strip()
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
    # Force summary_large_image on real BlogPosting pages. Static Site Generator emits
    # `summary` for some posts despite the frontmatter saying otherwise,
    # losing the large banner preview on every share.
    html = sub_attr(
        r'(<meta\s+name="twitter:card"\s+content=)"summary"',
        "summary_large_image",
        html,
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
        "supply": [
            "Python 3.9+",
            "pain001 PyPI package",
            "ISO 20022 XML template",
            "Input CSV of payment instructions",
        ],
        "tool": ["pip", "Terminal", "lxml validator"],
        "steps": [
            ("Install pain001", "Install the package from PyPI with `pip install pain001`."),
            (
                "Prepare your inputs",
                "Place your payment-instruction CSV and your ISO 20022 XML template "
                "in the same directory; both must follow the column layout documented "
                "in the README.",
            ),
            ("Run pain001", "Invoke `pain001 -t template.xml -i instructions.csv -o pain001.xml`."),
            (
                "Validate the output",
                "Open the generated XML in lxml or your bank's validator; the file "
                "should parse against the pain.001.001.09 schema with zero errors.",
            ),
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
        "supply": [
            "pacs.008 sample messages",
            "Current address-quality metrics",
            "Mapping rules to ISO 20022 PostalAddress components",
        ],
        "tool": ["pacs008 parser", "ISO 20022 XML validator"],
        "steps": [
            (
                "Inventory unstructured addresses",
                "Audit your outbound pacs.008 traffic. Any address still in a single "
                "free-text field is in scope.",
            ),
            (
                "Map fields to structured components",
                "Decompose the address into Town, PostCode, Country, BuildingNumber, "
                "Street and other ISO 20022 PostalAddress slots.",
            ),
            (
                "Update your message generator",
                "Patch the pacs.008 templating layer so every new message emits "
                "structured fields by default; keep a fallback for receivers that "
                "haven't migrated.",
            ),
            (
                "Test against the deadline",
                "Run end-to-end tests against your scheme's test harness before the "
                "November 2026 enforcement date.",
            ),
        ],
    },
}


def _build_howto_jsonld(spec: dict) -> str:
    steps_json = []
    for i, (name, text) in enumerate(spec["steps"], 1):
        steps_json.append(
            {
                "@type": "HowToStep",
                "position": i,
                "name": name,
                "text": text,
            }
        )
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
    return (
        f'<script type="application/ld+json">{_json.dumps(payload, separators=(",", ":"))}</script>'
    )


def inject_howto(page: Path, html: str) -> str:
    """Append a curated HowTo JSON-LD block to opt-in articles."""
    slug = page.parent.name
    spec = HOWTO_SCHEMAS.get(slug)
    if not spec:
        return html
    if '"@type":"HowTo"' in html or '"@type": "HowTo"' in html:
        return html  # Already injected — idempotent.
    block = _build_howto_jsonld(spec)
    return re.sub(r"</body>", block + "</body>", html, count=1)


# ---------------------------------------------------------------------------
# 4c. Image width/height — eliminate CLS
# ---------------------------------------------------------------------------
#
# Browser allocates a placeholder of size width×height before the
# bytes arrive; without those attrs the layout reflows once the
# image lands → cumulative layout shift. Static Site Generator's Markdown
# pipeline doesn't probe remote dimensions, so every Markdown img
# ships unsized. Stamp them at postbuild time.
#
# We don't need exact dimensions — the browser uses the ratio. A
# manifest pins the common assets to their real size; everything
# else gets a 16:9 (1200×675) default which matches the dominant
# banner shape used across the site.

_IMG_TAG_RE = re.compile(r"<img\b([^>]*?)/?>", re.IGNORECASE)
_IMG_SRC_RE = re.compile(r"""\bsrc=["']?([^"'\s>]+)""", re.IGNORECASE)

# Known dimensions for high-frequency assets. Keep this short — the
# default below catches everything else.
_IMG_DIMS: dict[str, tuple[int, int]] = {
    "https://cloudcdn.pro/clients/common/images/elements/divider.svg": (40, 6),
    "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg": (160, 40),
    "https://cloudcdn.pro/clients/static-site-generator/v1/banners/banner-static-site-generator.svg": (
        1200,
        675,
    ),
    # Personal portrait — 162×162 native, used at small sizes everywhere.
    "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp": (162, 162),
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
        has_w = bool(re.search(r"\bwidth=", attrs, re.IGNORECASE))
        has_h = bool(re.search(r"\bheight=", attrs, re.IGNORECASE))
        has_loading = bool(re.search(r"\bloading=", attrs, re.IGNORECASE))
        has_decoding = bool(re.search(r"\bdecoding=", attrs, re.IGNORECASE))
        has_fetchpri = bool(re.search(r"\bfetchpriority=", attrs, re.IGNORECASE))

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
        return f"<img{attrs} {' '.join(extras)}>"

    return _IMG_TAG_RE.sub(patch, html), n


# ---------------------------------------------------------------------------
# 4b. Open Graph completeness
# ---------------------------------------------------------------------------
#
# Static Site Generator emits `og:title`, `og:description`, `og:type` but skips
# `og:image`, `og:url`, `og:locale`, `og:site_name` — every social
# share renders without a preview image and without locale routing.
# Back-fill them from data the page already carries: the BlogPosting
# image (where present), the page's own URL, and the <html lang>.

BASE_URL = "https://sebastienrousseau.com"
SITE_NAME = "Sebastien Rousseau"

_HTML_LANG_RE = re.compile(r'<html\b[^>]*\blang=["\']?([a-zA-Z-]+)', re.IGNORECASE)
_HEAD_END_RE = re.compile(r"</head>", re.IGNORECASE)
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


def _page_canonical_url(page: Path) -> str:
    """Canonical URL for a built page, with the home page collapsing
    ``/index.html`` to ``/``."""
    rel = page.relative_to(PUBLIC).as_posix()
    return f"{BASE_URL}/" if rel == "index.html" else f"{BASE_URL}/{rel}"


def _resolve_og_banner(html: str, present: set[str]) -> list[str]:
    """If ``og:image`` is missing, return the meta-tag additions (image +
    matching twitter:image) needed to populate it."""
    if "og:image" in present:
        return []
    img_m = _blogposting_image_re.search(html)
    banner = (
        img_m.group(1) if img_m else ""
    ) or "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp"
    out = [f'<meta property="og:image" content="{banner}">']
    if "twitter:image" not in present:
        out.append(f'<meta name="twitter:image" content="{banner}">')
    return out


def inject_og_completeness(page: Path, html: str) -> str:
    """Ensure og:image / og:url / og:locale / og:site_name are present."""
    lm = _HTML_LANG_RE.search(html)
    locale = _lang_to_og_locale(lm.group(1) if lm else "en-GB")
    present = {m.group(1).lower() for m in _OG_TAG_RE.finditer(html)}

    additions: list[str] = []
    if "og:url" not in present:
        additions.append(f'<meta property="og:url" content="{_page_canonical_url(page)}">')
    if "og:locale" not in present:
        additions.append(f'<meta property="og:locale" content="{locale}">')
    if "og:site_name" not in present:
        additions.append(f'<meta property="og:site_name" content="{SITE_NAME}">')
    additions.extend(_resolve_og_banner(html, present))

    if not additions:
        return html
    block = "\n".join(additions) + "\n"
    return _HEAD_END_RE.sub(block + "</head>", html, count=1)


# ---------------------------------------------------------------------------
# 4e. Clean meta / og / twitter description
# ---------------------------------------------------------------------------
#
# The SSG derives <meta name="description">, og:description and
# twitter:description by scraping the rendered <body>, which leaves
# double-escaped markup ("&amp;lt;div lang=&quot;en&quot; …") in the social
# preview card — the string that renders when someone shares the URL. The
# clean summary already exists on the page: the Article-family JSON-LD
# `description` (authored from front matter). Reuse it. For the EN home page,
# whose graph carries only the identity block (no description), fall back to
# the _posts/index.md front-matter description; then to a sanitised scrape so
# no page is ever left with corrupted markup in its description meta.

_JSONLD_BLOCK_RE = re.compile(
    r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',
    re.IGNORECASE | re.DOTALL,
)
_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")
_FM_DESC_RE = re.compile(r'^description:\s*["\']?(.+?)["\']?\s*$', re.MULTILINE)
_DESC_META_RE = re.compile(
    r"<meta\b[^>]*\b(?:name|property)="
    r'"(?:description|og:description|twitter:description)"[^>]*>',
    re.IGNORECASE,
)
_CONTENT_ATTR_RE = re.compile(r'(content=")[^"]*(")', re.IGNORECASE)


def _iter_jsonld_nodes(data: object) -> list[dict]:
    """Flatten every dict node in a parsed JSON-LD payload (handles
    ``@graph`` arrays and nested objects)."""
    out: list[dict] = []
    if isinstance(data, dict):
        out.append(data)
        for v in data.values():
            out.extend(_iter_jsonld_nodes(v))
    elif isinstance(data, list):
        for item in data:
            out.extend(_iter_jsonld_nodes(item))
    return out


# Markers of leaked markup — literal tags, single-escaped, and the
# double-escaped form the SSG body-scrape produces (``&amp;lt;div``, whose
# substring is NOT ``&lt;``). A legitimate ampersand (``R&amp;D``) is fine;
# only the escaped tag-open/close/quote sequences signal corruption.
_CORRUPT_MARKERS = ("<", "&lt;", "&gt;", "&amp;lt;", "&amp;gt;", "&amp;quot;")


def _is_clean_desc(text: str) -> bool:
    return bool(text) and len(text) >= 20 and not any(marker in text for marker in _CORRUPT_MARKERS)


def _node_is_article(node: dict) -> bool:
    t = node.get("@type", "")
    types = t if isinstance(t, list) else [t]
    return any("Article" in str(x) or "Posting" in str(x) for x in types)


def _clean_descriptions(html_text: str) -> list[tuple[bool, str]]:
    """Every clean JSON-LD description as ``(is_article_node, text)``."""
    out: list[tuple[bool, str]] = []
    for block in _JSONLD_BLOCK_RE.findall(html_text):
        try:
            data = _json.loads(block)
        except ValueError:
            continue
        for node in _iter_jsonld_nodes(data):
            desc = node.get("description")
            if isinstance(desc, str) and _is_clean_desc(desc):
                out.append((_node_is_article(node), desc))
    return out


def _desc_from_jsonld(html_text: str) -> str | None:
    """Cleanest description from the page JSON-LD, preferring Article-family
    nodes over the identity graph."""
    generic: str | None = None
    for is_article, desc in _clean_descriptions(html_text):
        if is_article:
            return desc
        if generic is None:
            generic = desc
    return generic


def _desc_from_source(page: Path) -> str | None:
    """Front-matter description for the EN home page — the only page whose
    JSON-LD carries no description."""
    try:
        rel = page.relative_to(PUBLIC).as_posix()
    except ValueError:
        return None
    if rel != "index.html":
        return None
    src = POSTS / "index.md"
    if not src.is_file():
        return None
    m = _FM_DESC_RE.search(src.read_text(encoding="utf-8")[:4000])
    return m.group(1).strip() if m else None


def _sanitised_scrape(html_text: str) -> str | None:
    """Last resort: recover readable text from the corrupted meta by
    unescaping until stable, stripping tags, and truncating."""
    m = re.search(
        r'<meta\b[^>]*\bname="description"[^>]*\bcontent="([^"]*)"',
        html_text,
        re.IGNORECASE,
    )
    if not m:
        return None
    text = m.group(1)
    for _ in range(3):
        nxt = _html.unescape(text)
        if nxt == text:
            break
        text = nxt
    text = _WS_RE.sub(" ", _TAG_RE.sub(" ", text)).strip()
    if len(text) < 20:
        return None
    if len(text) > 157:
        text = text[:157].rsplit(" ", 1)[0] + "…"
    return text


# ---------------------------------------------------------------------------
# 4g. Single-source KPI numbers from metrics.json
# ---------------------------------------------------------------------------
#
# The home / projects / about pages hard-coded their own KPI figures, which
# drifted (37.1M vs 37.3M downloads; 663 vs 664 stars; 73/84/88 articles).
# metrics.json is the fetched source of truth; fill any
# `<span class="kpi-cell-value" data-kpi="KEY">` from it at build time so one
# number appears everywhere.

_METRICS_JSON = POSTS.parent / "_data" / "proof" / "metrics.json"
_KPI_SPAN_RE = re.compile(
    r'(<span[^>]*\bclass="kpi-cell-value"[^>]*\bdata-kpi="([a-z_]+)"[^>]*>)'
    r"([^<]*)(</span>)",
    re.IGNORECASE,
)
_kpi_cache: dict[str, str] | None = None


def _format_metric(value: object, fmt: str) -> str:
    if not isinstance(value, (int, float)):
        return str(value)
    if fmt == "compact":
        if value >= 1_000_000:
            return f"{value / 1_000_000:.1f}M"
        if value >= 1_000:
            return f"{value / 1_000:.1f}K"
    return str(int(value))


def _kpi_metrics() -> dict[str, str]:
    global _kpi_cache
    if _kpi_cache is not None:
        return _kpi_cache
    out: dict[str, str] = {}
    try:
        data = _json.loads(_METRICS_JSON.read_text(encoding="utf-8"))
        for stat in data.get("stats", []):
            key = stat.get("key")
            if key:
                out[key] = _format_metric(stat.get("value"), stat.get("format", "plain"))
    except (OSError, ValueError):
        out = {}
    _kpi_cache = out
    return out


def inject_kpi_metrics(html_text: str) -> str:
    """Fill every ``data-kpi``-tagged KPI cell from metrics.json. Pages
    without such cells are untouched. Idempotent."""
    metrics = _kpi_metrics()
    if not metrics or 'data-kpi="' not in html_text:
        return html_text

    def _fill(m: re.Match[str]) -> str:
        val = metrics.get(m.group(2))
        return f"{m.group(1)}{val}{m.group(4)}" if val else m.group(0)

    return _KPI_SPAN_RE.sub(_fill, html_text)


_ARTICLE_TYPE_RE = re.compile(
    r'"@type"\s*:\s*"(?:BlogPosting|NewsArticle|TechArticle|ScholarlyArticle|Article)"'
)
_OGTYPE_WEBSITE_RE = re.compile(
    r'(<meta\b[^>]*\bproperty="og:type"[^>]*\bcontent=")website(")', re.IGNORECASE
)


_LDJSON_FULL_RE = re.compile(
    r'<script\b[^>]*type=["\']?application/ld\+json["\']?[^>]*>[\s\S]+?</script>',
    re.IGNORECASE,
)
_INLANG_VALUE_RE = re.compile(r'("inLanguage"\s*:\s*")([^"]*)(")')


def align_jsonld_inlanguage(html_text: str) -> str:
    """Align every JSON-LD ``inLanguage`` whose base language differs from the
    page's ``<html lang>`` base.

    The translation-time localiser walks each page's JSON-LD, but a handful of
    content items (a non-dated whitepaper, some late-added articles) slip
    through with the EN identity graph's ``inLanguage="en-GB"`` on their
    WebSite / ProfilePage nodes while ``<html lang>`` is the locale — which
    ``test_jsonld_localized`` flags. This postbuild belt-and-suspenders pass
    runs on every page and only touches mismatched values, so correctly
    localised pages (and all EN pages) are left byte-for-byte unchanged.
    Idempotent."""
    lm = _HTML_LANG_RE.search(html_text)
    if not lm:
        return html_text
    page_lang = lm.group(1)
    page_base = page_lang.split("-")[0].lower()

    def _fix_value(mm: re.Match[str]) -> str:
        if mm.group(2).split("-")[0].lower() == page_base:
            return mm.group(0)
        return f"{mm.group(1)}{page_lang}{mm.group(3)}"

    def _fix_block(m: re.Match[str]) -> str:
        return _INLANG_VALUE_RE.sub(_fix_value, m.group(0))

    return _LDJSON_FULL_RE.sub(_fix_block, html_text)


def fix_article_og_type(html_text: str) -> str:
    """Dated posts carry an Article-family JSON-LD block but the SSG sets
    ``og:type=website``. Promote it to ``article`` so social + news
    crawlers classify the page correctly. Non-article pages are untouched.
    Idempotent."""
    if not _ARTICLE_TYPE_RE.search(html_text):
        return html_text
    return _OGTYPE_WEBSITE_RE.sub(r"\1article\2", html_text, count=1)


def _current_meta_description(html_text: str) -> str | None:
    m = re.search(
        r'<meta\b[^>]*\bname="description"[^>]*\bcontent="([^"]*)"',
        html_text,
        re.IGNORECASE,
    )
    return m.group(1) if m else None


_CONTENT_CAPTURE_RE = re.compile(r'content="([^"]*)"', re.IGNORECASE)


def _tag_is_corrupt(tag: str) -> bool:
    cm = _CONTENT_CAPTURE_RE.search(tag)
    return cm is not None and any(mk in cm.group(1) for mk in _CORRUPT_MARKERS)


def clean_meta_description(page: Path, html_text: str) -> str:
    """Rewrite only the corrupted ``description`` / ``og:description`` /
    ``twitter:description`` tags with one clean, attribute-escaped summary.

    Source of truth, in order: the page's own clean ``<meta name=description>``
    (so a topic/category page keeps its real description rather than the
    generic identity-graph one), else the Article-family JSON-LD description,
    else the front-matter description (home page), else a sanitised scrape.
    Each tag is checked independently — clean tags (including generator-set
    ones) are left byte-for-byte unchanged, and any single corrupted tag
    (e.g. only ``twitter:description``) is repaired. Idempotent."""
    current = _current_meta_description(html_text)
    raw: str | None
    if current is not None and _is_clean_desc(current):
        raw = current
    else:
        raw = (
            _desc_from_jsonld(html_text) or _desc_from_source(page) or _sanitised_scrape(html_text)
        )
    if not raw:
        return html_text
    esc = _html.escape(_html.unescape(raw), quote=True)

    def _fix_tag(m: re.Match[str]) -> str:
        tag = m.group(0)
        if not _tag_is_corrupt(tag):
            return tag
        return _CONTENT_ATTR_RE.sub(lambda mm: f"{mm.group(1)}{esc}{mm.group(2)}", tag, count=1)

    return _DESC_META_RE.sub(_fix_tag, html_text)


# ---------------------------------------------------------------------------
# 4f. Canonical / og:url consistency
# ---------------------------------------------------------------------------
#
# The same page shipped three different URL forms: <link rel="canonical">
# = ".../slug/index.html", og:url = ".../slug" (no slash), and the sitemap
# <loc> = ".../slug/" (trailing slash). Search engines treat all three as
# canonicalisation signals, so the disagreement is a real defect. Collapse
# canonical + og:url onto the pretty trailing-slash form the sitemap already
# uses. A stray self-referencing hreflang alternate (bare domain, no slash)
# on the home page is normalised to the same form so the duplicate resolves.

_CANONICAL_LINK_RE = re.compile(r'<link\b[^>]*\brel=["\']?canonical["\']?[^>]*>', re.IGNORECASE)
_OGURL_META_RE = re.compile(r'<meta\b[^>]*\bproperty=["\']?og:url["\']?[^>]*>', re.IGNORECASE)
_HREF_ATTR_RE = re.compile(r'(href=")[^"]*(")', re.IGNORECASE)
_SELF_ALTERNATE_RE = re.compile(
    r'<link\b(?=[^>]*\brel=["\']?alternate["\']?)(?=[^>]*\bhreflang=)'
    rf'[^>]*\bhref=["\']?{re.escape(BASE_URL)}["\'\s>][^>]*>',
    re.IGNORECASE,
)


def _pretty_canonical_url(page: Path) -> str:
    """Trailing-slash canonical form matching the sitemap: home → ``/``,
    ``about/index.html`` → ``/about/``, ``slug/index.html`` → ``/slug/``."""
    rel = page.relative_to(PUBLIC)
    if rel.name != "index.html":
        return f"{BASE_URL}/{rel.as_posix()}"
    parent = rel.parent.as_posix()
    return f"{BASE_URL}/" if parent in ("", ".") else f"{BASE_URL}/{parent}/"


def normalize_canonical(page: Path, html_text: str) -> str:
    """Force <link rel=canonical> and og:url onto one trailing-slash form,
    and normalise a stray bare-domain self-alternate on the home page.
    Idempotent."""
    url = _pretty_canonical_url(page)

    def _set_href(m: re.Match[str]) -> str:
        return _HREF_ATTR_RE.sub(lambda mm: f"{mm.group(1)}{url}{mm.group(2)}", m.group(0), count=1)

    def _set_content(m: re.Match[str]) -> str:
        return _CONTENT_ATTR_RE.sub(
            lambda mm: f"{mm.group(1)}{url}{mm.group(2)}", m.group(0), count=1
        )

    out = _CANONICAL_LINK_RE.sub(_set_href, html_text, count=1)
    out = _OGURL_META_RE.sub(_set_content, out, count=1)
    # Repair the home-page self-alternate whose href is the bare domain
    # (no trailing slash) so it collapses onto the injected en alternate.
    if _pretty_canonical_url(page) == f"{BASE_URL}/":
        out = _SELF_ALTERNATE_RE.sub(
            lambda m: (
                m.group(0)
                .replace(f'href="{BASE_URL}"', f'href="{BASE_URL}/"')
                .replace(f"href={BASE_URL}>", f'href="{BASE_URL}/">')
                .replace(f"href={BASE_URL} ", f'href="{BASE_URL}/" ')
            ),
            out,
        )
    return out


# ---------------------------------------------------------------------------
