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
    if new_xml != xml:
        sitemap_path.write_text(new_xml, encoding="utf-8")
    return patched


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
}


def _labels(html: str) -> dict[str, str]:
    return LABELS_FR if _is_french(html) else LABELS_EN


def slugify(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s).strip().lower()
    s = re.sub(r"&[a-z0-9#]+;", " ", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:80]


def _fmt_date(iso_or_rfc: str) -> str:
    """Render a date string as 'D Mon YYYY'. Accepts ISO 8601 ('2026-05-11'
    or '2026-05-11T06:06:06+00:00') or RFC 822 ('Mon, 11 May 2026 …').
    Returns the input unchanged if neither format matches."""
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
            return _dt.strptime(iso_or_rfc, fmt).strftime("%-d %b %Y")
        except ValueError:
            continue
    return iso_or_rfc


def _render_tag_badges(keywords: list[str]) -> str:
    if not keywords:
        return ""
    badges = "".join(
        f'<a href="/tags/index.html#h3-{slugify(k)}" class="article-tag" rel="tag">{k}</a>'
        for k in keywords
    )
    return f'<nav class="article-tags" aria-label="Topics">{badges}</nav>'


def _render_meta_bar(date_pub: str, date_mod: str, word_count: int | None, labels: dict[str, str]) -> str:
    parts: list[str] = []
    parts.append(
        f'<a href="{AUTHOR_URL}" class="article-author" rel="author">'
        f'<img alt="Portrait of {AUTHOR_NAME}" src="{AUTHOR_AVATAR}" '
        f'width="36" height="36" loading="lazy" decoding="async" />'
        f'<span>{AUTHOR_NAME}</span></a>'
    )
    if date_pub:
        parts.append(
            f'<time datetime="{date_pub}" class="meta-pub">'
            f'{labels["Published"]} {_fmt_date(date_pub)}</time>'
        )
    # Suppress "Updated" when the modification date is the same as or
    # earlier than the publication date — otherwise a post scheduled into
    # the future shows a nonsensical "Updated before Published" stamp.
    if date_mod and date_mod[:10] > date_pub[:10]:
        parts.append(
            f'<time datetime="{date_mod}" class="meta-rev">'
            f'{labels["Updated"]} {_fmt_date(date_mod)}</time>'
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
    badges = _render_tag_badges(keywords)
    meta = _render_meta_bar(date_pub, date_mod, word_count, _labels(html))
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


def inject_prev_next_nav(html: str, slug: str, nav_index: dict[str, tuple[tuple[str, str] | None, tuple[str, str] | None]]) -> str:
    """Inject a <nav class="post-pagination"> with prev/next links just
    before the closing ``</div></main>`` of any dated BlogPosting page.
    Localized via _labels(html); French pages get French labels."""
    if '"@type":"BlogPosting"' not in html:
        return html
    if slug not in nav_index:
        return html
    if 'class="post-pagination"' in html:
        return html
    prev_e, next_e = nav_index[slug]
    if not prev_e and not next_e:
        return html
    labels = _labels(html)

    def render(entry: tuple[str, str] | None, direction: str, label: str) -> str:
        if not entry:
            return '<span class="post-pagination-stub" aria-hidden="true"></span>'
        s, t = entry
        return (
            f'<a class="post-pagination-{direction}" href="/{s}/">'
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


def _translated_slugs() -> set[str]:
    """Walk public/fr/ for slugs that have a French translation."""
    fr_dir = PUBLIC / "fr"
    if not fr_dir.is_dir():
        return set()
    return {p.parent.name for p in fr_dir.glob("*/index.html")}


def inject_hreflang(html: str, slug: str, lang: str, translated: set[str]) -> str:
    """Inject reciprocal hreflang links so Google + crawlers pair the two
    language versions. Only applies to slugs that actually have a French
    translation; English-only posts are untouched.
    """
    if slug not in translated:
        return html
    en_url = f"https://sebastienrousseau.com/{slug}/"
    fr_url = f"https://sebastienrousseau.com/fr/{slug}/"
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
    translated = _translated_slugs()
    sri_patched = 0
    csp_patched = 0
    itemlist_patched = 0
    social_patched = 0
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
        patched_wc = inject_word_count(patched_si)
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
        patched_nav = inject_prev_next_nav(patched_src, page.parent.name, nav_index)
        if patched_nav != patched_src:
            nav_patched += 1
        # Reciprocal hreflang for paired English/French pages. Slug is the
        # parent dir name for English (/foo/) and grandparent for French
        # (/fr/foo/) — strip the "fr/" prefix when matching.
        rel_slug = page.parent.name
        is_fr = page.parent.parent.name == "fr"
        patched_hl = inject_hreflang(patched_nav, rel_slug, "fr" if is_fr else "en", translated)
        if patched_hl != patched_nav:
            hreflang_patched += 1
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
        f"llms.txt {'updated' if llms_written else 'unchanged'}"
    )


if __name__ == "__main__":
    main()
