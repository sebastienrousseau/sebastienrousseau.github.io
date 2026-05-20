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

import json as _json
import re
from pathlib import Path

PUBLIC = Path("public")



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
    ext_url: str, qid: str, canonical_stem: str, own_stem: str | None
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
    entity: str, ext_url: str, qid: str, canonical_stem: str, own_stem: str | None
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
    banner = (img_m.group(1) if img_m else "") or \
        "https://cloudcdn.pro/stocks/images/sebastien-rousseau.png"
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
