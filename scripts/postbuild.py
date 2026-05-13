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
from pathlib import Path

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
#   (authoritative_external_url, optional_own_canonical_post_stem)
# We use Wikipedia or the issuing body's canonical page rather than Wikidata
# Q-numbers — same grounding power for AI overviews, no memorised-ID
# hallucination risk, and easy to verify. When the entity has a canonical
# post in *this* repo, the post URL is added as a second sameAs anchor so
# search + AI engines learn that this site is an authority on the topic.
# A page never self-anchors: if the current post IS the canonical for an
# entity, the canonical URL is suppressed.
ENTITY_AUTHORITY: dict[str, tuple[str, str | None]] = {
    # Cryptography
    "CRYSTALS-Kyber":               ("https://en.wikipedia.org/wiki/Kyber",
                                     "2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age"),
    "post-quantum cryptography":    ("https://en.wikipedia.org/wiki/Post-quantum_cryptography",
                                     "2025-09-01-quantum-safe-payments-epaa"),
    "lattice-based cryptography":   ("https://en.wikipedia.org/wiki/Lattice-based_cryptography",
                                     "2024-04-15-quantum-algorithm-challenges-lattice-based-cryptography"),
    "Quantum key distribution":     ("https://en.wikipedia.org/wiki/Quantum_key_distribution",
                                     "2023-12-11-quantum-key-distribution-revolutionising-security-in-banking"),
    "Shor's algorithm":             ("https://en.wikipedia.org/wiki/Shor%27s_algorithm",
                                     "2026-04-11-quantum-thresholds-are-moving-again"),
    "homomorphic encryption":       ("https://en.wikipedia.org/wiki/Homomorphic_encryption",
                                     "2024-03-25-fully-homomorphic-encryption-in-a-banking-quantum-era"),
    "Quantum computing":            ("https://en.wikipedia.org/wiki/Quantum_computing", None),
    "NIST PQC":                     ("https://csrc.nist.gov/projects/post-quantum-cryptography", None),
    # Payments
    "ISO 20022":                    ("https://www.iso20022.org/",
                                     "2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001"),
    "SWIFT gpi":                    ("https://www.swift.com/our-solutions/swift-gpi", None),
    "SEPA":                         ("https://en.wikipedia.org/wiki/Single_Euro_Payments_Area", None),
    # AI
    "Large language model":         ("https://en.wikipedia.org/wiki/Large_language_model",
                                     "2026-05-11-lucy-besson-knowledge-transfer-ai-quantum"),
    "Generative AI":                ("https://en.wikipedia.org/wiki/Generative_artificial_intelligence",
                                     "2023-11-12-exploring-generative-ai"),
    "Artificial intelligence":      ("https://en.wikipedia.org/wiki/Artificial_intelligence", None),
    "Multimodal learning":          ("https://en.wikipedia.org/wiki/Multimodal_learning",
                                     "2024-03-18-advancing-ai-with-multimodal-llms-insights-from-mm1"),
    # Programming
    "Rust":                         ("https://en.wikipedia.org/wiki/Rust_(programming_language)", None),
    "Python":                       ("https://en.wikipedia.org/wiki/Python_(programming_language)", None),
    # Crypto / Web3
    "Blockchain":                   ("https://en.wikipedia.org/wiki/Blockchain",
                                     "2018-01-02-blockchain-the-technology-that-matters-in-2018"),
    "Bitcoin":                      ("https://en.wikipedia.org/wiki/Bitcoin",
                                     "2018-01-01-bitcoin-the-year-in-review"),
    "Ethereum":                     ("https://en.wikipedia.org/wiki/Ethereum",
                                     "2018-01-24-the-erc-20-token-standard"),
    "ERC-20":                       ("https://en.wikipedia.org/wiki/Ethereum#Tokens",
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
        for entity, (ext_url, canonical_stem) in ENTITY_AUTHORITY.items():
            ent_l = entity.lower()
            if (kwl == ent_l or ent_l in kwl or kwl in ent_l) and entity not in seen:
                seen.add(entity)
                same_as: list[str] = [ext_url]
                # Add the user's own canonical post as a second sameAs anchor —
                # tells crawlers this site is also an authority on the entity.
                # Skip when the current page IS the canonical post (no self-link).
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

_FM_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
_FM_FIELD_RE = re.compile(r'^([a-zA-Z_-]+):\s*"?([^"\n]*)"?', re.MULTILINE)


def _read_fm(path: Path) -> dict[str, str]:
    src = path.read_text(encoding="utf-8", errors="ignore")
    m = _FM_RE.match(src)
    if not m:
        return {}
    fm_text = m.group(1)
    out: dict[str, str] = {}
    for fm in _FM_FIELD_RE.finditer(fm_text):
        out.setdefault(fm.group(1), fm.group(2).strip())
    return out


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
    if new_xml != xml:
        sitemap_path.write_text(new_xml, encoding="utf-8")
    return patched


def main() -> None:
    pages = list(PUBLIC.rglob("*.html"))
    sri_patched = 0
    csp_patched = 0
    itemlist_patched = 0
    social_patched = 0
    wc_patched = 0
    about_patched = 0
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
        patched_wc = inject_word_count(patched_si)
        if patched_wc != patched_si:
            wc_patched += 1
        patched_about = inject_about(patched_wc)
        if patched_about != patched_wc:
            about_patched += 1
        patched2 = inject_jsonld_hashes(patched_about)
        if patched2 != patched_about:
            csp_patched += 1
        if patched2 != original:
            page.write_text(patched2, encoding="utf-8")

    # Refresh sitemap lastmod from each post's frontmatter last_reviewed.
    lastmod_index = build_lastmod_index()
    sitemap_patched = refresh_sitemap_lastmod(PUBLIC / "sitemap.xml", lastmod_index)

    # Overwrite robots.txt + llms.txt with the curated versions.
    robots_written = write_robots(PUBLIC)
    llms_written = write_llms_txt(PUBLIC)

    print(
        f"postbuild: {len(pages)} HTML pages, "
        f"{sri_patched} got real SRI, "
        f"{itemlist_patched} got ItemList JSON-LD, "
        f"{social_patched} got og:image fixed, "
        f"{wc_patched} got wordCount, "
        f"{about_patched} got about/mentions entities, "
        f"{csp_patched} got CSP JSON-LD hashes, "
        f"{sitemap_patched} sitemap entries refreshed, "
        f"robots.txt {'updated' if robots_written else 'unchanged'}, "
        f"llms.txt {'updated' if llms_written else 'unchanged'}"
    )


if __name__ == "__main__":
    main()
