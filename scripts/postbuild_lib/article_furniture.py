"""Article UI furniture + nav + hreflang lookups.

Owns every per-page transform applied AFTER the SEO + JSON-LD passes:

* tag badges + meta bar (author / dates / read time) after the H1
* anchor links on every H2/H3 inside <main>
* table-of-contents sidebar for posts with >= 5 H2 sections
* FAQ <p><strong>Q?</strong></p><p>A</p> → collapsible <details qa-item>
* citation graph as visible <ol> at the bottom of dated posts
* sources list extracted from outbound links
* mermaid block rendering
* prev/next nav with active-link marker
* speculation rules
* hoist body-level <link rel=stylesheet> into <head>

Plus the lang/slug helpers used by the hreflang pass:
* _all_active_non_en_langs / _slug_maps / _translated_slugs* /
  _resolve_en_slug / _alternates_for_en_slug.

Pure functions over HTML strings; module-level state is regex
constants + author identity constants only.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import _lang_registry as _lr  # type: ignore[import-not-found]
from _fr_slugs import en_slug as _en_slug  # type: ignore[import-not-found]

from postbuild_lib.seo import _keywords_re  # type: ignore[unused-import]

PUBLIC = Path("public")


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


_LABEL_CACHE: dict[str, dict[str, str]] = {}


def _labels_for_lang(code: str) -> dict[str, str]:
    """Per-language label cache. Loads from ``labels.json`` and overlays
    a handful of extra keys ``LABELS_EN`` has but the JSON glossary
    intentionally doesn't (Table of contents, Article pagination, etc.)
    so older call sites stay valid."""
    if code in _LABEL_CACHE:
        return _LABEL_CACHE[code]
    if code == "en":
        out = dict(LABELS_EN)
    else:
        try:
            base = _lr.load_labels(code)
        except _lr.LanguageError:
            base = {}
        out = dict(LABELS_EN)
        out.update(base)
    _LABEL_CACHE[code] = out
    return out


def _detect_page_lang(html: str) -> str:
    m = _HTML_LANG_DETECT_RE.search(html)
    if not m:
        return "en"
    return m.group(1).lower().split("-", 1)[0]


def _labels(html: str) -> dict[str, str]:
    return _labels_for_lang(_detect_page_lang(html))


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
    alt_text = (
        f"Portrait de {AUTHOR_NAME}" if lang == "fr"
        else f"Portrait of {AUTHOR_NAME}"
    )
    parts.append(
        f'<a href="{author_url}" class="article-author" rel="author">'
        f'<img alt="{alt_text}" src="{AUTHOR_AVATAR}" '
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


# ---------------------------------------------------------------------------
# Sigstore attestation footer (gated on _data/sigstore/config.json)
# ---------------------------------------------------------------------------
#
# When ``scripts/sigstore_sign.py`` runs (which only happens if
# ``_data/sigstore/config.json`` exists), it writes a Sigstore bundle
# per article under ``public/sigstore/<slug>.bundle``. This injector
# adds a small footer attestation badge to articles that have a
# matching bundle. The badge links to the bundle + the public-key
# verify command so any reader can confirm the page bytes match what
# the author signed.

_SIGSTORE_CONFIG_PRESENT: bool = (Path("_data/sigstore/config.json").is_file())


def inject_sigstore_attestation(html: str, slug: str) -> str:
    """Insert a 'Signed · cosign' badge near the article footer when a
    Sigstore bundle exists for this slug. No-op otherwise."""
    if not _SIGSTORE_CONFIG_PRESENT:
        return html
    if '"@type":"BlogPosting"' not in html:
        return html
    bundle = PUBLIC / "sigstore" / f"{slug}.bundle"
    if not bundle.is_file():
        return html
    if 'class="article-sigstore"' in html:
        return html  # idempotent
    is_fr = _is_french(html)
    label = (
        "Signature Sigstore · vérifiable avec cosign"
        if is_fr else "Sigstore signature · verifiable with cosign"
    )
    badge = (
        f'<aside class="article-sigstore" aria-label="{label}">'
        f'<a href="/sigstore/{slug}.bundle" rel="external" '
        f'type="application/vnd.dev.sigstore.bundle+json">'
        f'🔏 {label}</a></aside>'
    )
    # Insert just before the existing article furniture's end-of-main.
    return re.sub(r'(</main>)', badge + r'\1', html, count=1)


def _extract_article_metadata(html: str) -> tuple[list[str], str, str, int | None]:
    """Pull the inputs ``inject_article_furniture`` needs out of the page:
    keyword list, datePublished, dateModified, wordCount."""
    keywords: list[str] = []
    m = _keywords_re.search(html)
    if m and m.group(1):
        keywords = [k.strip() for k in m.group(1).split(",") if k.strip()]
    dm = _BLOGPOSTING_DATES_RE.search(html)
    date_pub, date_mod = (dm.group(1), dm.group(2)) if dm else ("", "")
    wm = _WORDCOUNT_RE.search(html)
    word_count = int(wm.group(1)) if wm else None
    return keywords, date_pub, date_mod, word_count


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
    keywords, date_pub, date_mod, word_count = _extract_article_metadata(html)
    labels = _labels(html)
    lang = "fr" if _is_french(html) else "en"
    fragment = (
        _render_tag_badges(keywords, labels, lang)
        + _render_meta_bar(date_pub, date_mod, word_count, labels, lang)
    )
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
    # Track slugs already emitted on this page; append -2, -3… on
    # collision. Non-ASCII scripts (Arabic, Cyrillic, CJK) often
    # slugify to the same Latin fragment (e.g. "FHE", "2026") for
    # multiple headings — without dedup, pa11y fails on duplicate ids.
    seen: dict[str, int] = {}

    def _unique(slug: str, idx: int) -> str:
        if not slug:
            slug = f"section-{idx}"
        n = seen.get(slug, 0) + 1
        seen[slug] = n
        return slug if n == 1 else f"{slug}-{n}"

    heading_idx = 0

    def patch_heading(hm: re.Match[str]) -> str:
        nonlocal heading_idx
        heading_idx += 1
        level = hm.group(1).lower()
        inner = hm.group(2)
        text = re.sub(r'<[^>]+>', '', inner).strip()
        if not text:
            return hm.group(0)
        slug = _unique(slugify(text), heading_idx)
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
        # Skip non-EN translations — they share the (EN-)slug with the English
        # original at the data level, but live under /<lang>/<lang-slug>/.
        # Including them would double-count and yield wrong nav.
        if p.parent.parent.name in _all_active_non_en_langs():
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


_NAV_LINK_RE = re.compile(
    r'(<nav\s+aria-label=["\']?Primary["\']?(?:[\s\S]*?</nav>)|<nav\s+aria-label=["\']?[^"\'>]+["\']?(?:[\s\S]*?</nav>))',
    re.IGNORECASE,
)


def _nav_target_for_en_page(top: str) -> str:
    """Map an EN top-level page slug to its nav-link href."""
    if _DATED_SLUG_RE.match(top):
        return "/articles/index.html"
    return f"/{top}/index.html"


def _nav_target_for_lang_page(lang: str, top: str) -> str:
    """Map a localised top-level page slug to its nav-link href."""
    articles_slug = _slug_maps(lang)["statics_en_to_lang"].get("articles", "articles")
    if _DATED_SLUG_RE.match(top):
        return f"/{lang}/{articles_slug}/index.html"
    return f"/{lang}/{top}/index.html"


def _nav_active_target(page: Path) -> str | None:
    """Return the nav-link href that should be marked active for this
    page, or ``None`` if there's no obvious match.

    Greedy by depth: ``/about/`` → ``/about/index.html``;
    ``/2026-05-12-…/`` → ``/articles/index.html``;
    ``/<lang>/<x>/`` → ``/<lang>/<x>/index.html``.
    """
    rel = page.relative_to(PUBLIC).as_posix()
    if rel == "index.html":
        return "/index.html"  # home
    parts = rel.split("/")
    if len(parts) == 2 and parts[1] == "index.html":
        return _nav_target_for_en_page(parts[0])
    if len(parts) == 3 and parts[2] == "index.html":
        lang, top = parts[0], parts[1]
        if lang not in _all_active_non_en_langs():
            return None
        return _nav_target_for_lang_page(lang, top)
    return None


def inject_nav_active(html: str, page: Path) -> str:
    """Add ``aria-current="page"`` + ``class="active"`` to the nav link
    matching this page. For home pages (/, /<lang>/), the brand link
    sitting outside the nav menu is the home indicator, so we mark it
    there. Idempotent — re-running doesn't double-mark."""
    target = _nav_active_target(page)
    if not target:
        return html

    # Always clear any pre-existing active markers in the header first.
    header_m = re.search(r'<header\b[^>]*>([\s\S]*?)</header>', html, re.IGNORECASE)
    if not header_m:
        return html
    header_body = header_m.group(1)
    header_clean = re.sub(r'\s+aria-current=["\']?[^"\'>]+["\']?', '', header_body)
    header_clean = re.sub(r'(<a\b[^>]*?)\s+class=["\']?active["\']?', r'\1', header_clean)

    pat = re.compile(
        r'(<a\s+(?:[^>]*?)href=["\']?)('
        + re.escape(target)
        + r')(["\']?)([^>]*>)',
        re.IGNORECASE,
    )

    def repl(m: re.Match[str]) -> str:
        return f'{m.group(1)}{m.group(2)}{m.group(3)} aria-current="page" class="active"{m.group(4)}'

    new_body = pat.sub(repl, header_clean, count=1)
    open_tag = header_m.group(0)[: header_m.group(0).index(">") + 1]
    return html.replace(header_m.group(0), open_tag + new_body + "</header>", 1)


def inject_prev_next_nav(
    html: str,
    slug: str,
    nav_index: dict[str, tuple[tuple[str, str] | None, tuple[str, str] | None]],
    is_fr: bool = False,
    fr_titles: dict[str, str] | None = None,
    *,
    page_lang: str = "en",
) -> str:
    """Inject a ``<nav class="post-pagination">`` with prev/next links
    just before the closing ``</div></main>`` of any dated BlogPosting
    page. Localised via ``_labels(html)``; non-EN pages get translated
    labels and links pointing to the matching translation under
    ``/<lang>/<lang-slug>/``.
    """
    if '"@type":"BlogPosting"' not in html:
        return html
    # Resolve the EN slug regardless of which lang we're patching.
    if page_lang != "en":
        maps = _slug_maps(page_lang)
        lookup_slug = maps["articles_lang_to_en"].get(slug, slug)
    else:
        lookup_slug = slug
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
        if page_lang != "en":
            articles_map = _slug_maps(page_lang)["articles_en_to_lang"]
            if s in articles_map:
                href = f"/{page_lang}/{articles_map[s]}/"
                if page_lang == "fr":
                    t = fr_titles.get(s, t)
            else:
                href = f"/{s}/"
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

# Local copies of the CSP-meta regexes (kept in postbuild.py too — both
# modules patch the same tag from different injection passes).
_csp_tag_re = re.compile(
    r'<meta\b[^>]*?http-equiv=["\']?Content-Security-Policy["\']?[^>]*?>',
    re.IGNORECASE,
)
_content_attr_re = re.compile(
    r'(content=)(["\'])(.+?)(\2)',
    re.IGNORECASE | re.DOTALL,
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

        return _content_attr_re.sub(patch_content, tag, count=1)

    return _csp_tag_re.sub(patch_csp, new_html, count=1)


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


def _sanitize_link_tag(tag: str) -> str:
    """Strip the stray trailing double-quote SSG emits on the search-widget
    stylesheet (``crossorigin="anonymous""``). Browsers treat that as an
    attribute-value error and bail out of ``<head>`` parsing, which then
    cascades into pa11y flagging the legitimate ``<link rel=icon>`` etc.
    as "link in body"."""
    # Collapse any duplicate `crossorigin="anonymous"` runs into one.
    tag = re.sub(
        r'(crossorigin="anonymous")(\s+crossorigin="anonymous")+',
        r'\1', tag,
    )
    # Remove a trailing `"` immediately before the closing `>`.
    tag = re.sub(r'""(\s*/?>)', r'"\1', tag)
    return tag


def hoist_body_link_stylesheets(html: str) -> tuple[str, int]:
    """Hoist every in-body ``<link rel=stylesheet>`` into ``<head>`` and
    sanitize the tag (SSG ships one with a malformed double-quote attribute
    that breaks Chrome's head-parser). HTML5 forbids ``<link>`` in body, so
    pa11y AAA flags this on every page shipping the SSG search widget."""
    head_end_m = _BODY_END_RE.search(html)
    if not head_end_m:
        return html, 0
    head_end = head_end_m.start()
    head, body = html[:head_end], html[head_end:]

    # Also sanitize any in-head stylesheet tags that already have the malformed
    # attribute — a previous hoist pass may have moved them up without fixing.
    head = _BODY_LINK_STYLESHEET_RE.sub(lambda m: _sanitize_link_tag(m.group(0)), head)

    matches = list(_BODY_LINK_STYLESHEET_RE.finditer(body))
    if not matches:
        return head + body, 0
    extracted: list[str] = []
    new_body = body
    for m in reversed(matches):
        extracted.insert(0, _sanitize_link_tag(m.group(0)))
        new_body = new_body[:m.start()] + new_body[m.end():]
    return head + "".join(extracted) + new_body, len(extracted)


def inject_speculation_rules(html: str) -> str:
    """Inject the Speculation Rules API block before </head>. Idempotent."""
    if 'type="speculationrules"' in html:
        return html
    return _HEAD_END_RE.sub(SPECULATION_RULES_BLOCK + '</head>', html, count=1)




# ---------------------------------------------------------------------------
# 8. Lang / slug helpers — used by the hreflang pass + various injectors
# ---------------------------------------------------------------------------


def _all_active_non_en_langs() -> list[str]:
    """Return the code for every active non-EN language."""
    return [lg.code for lg in _lr.LANGUAGES if lg.active and lg.code != "en"]


def _slug_maps_for(code: str) -> dict[str, dict[str, str]]:
    """Return the article + static slug maps (both directions) for ``code``."""
    s = _lr.load_slugs(code)
    articles = s.get("articles", {})
    statics = s.get("static", {})
    return {
        "articles_en_to_lang": articles,
        "articles_lang_to_en": {v: k for k, v in articles.items()},
        "statics_en_to_lang": statics,
        "statics_lang_to_en": {v: k for k, v in statics.items()},
    }


_SLUG_MAPS_CACHE: dict[str, dict[str, dict[str, str]]] = {}


def _slug_maps(code: str) -> dict[str, dict[str, str]]:
    if code not in _SLUG_MAPS_CACHE:
        _SLUG_MAPS_CACHE[code] = _slug_maps_for(code)
    return _SLUG_MAPS_CACHE[code]


_STATIC_EN_TO_FR: dict[str, str] = _lr.load_slugs("fr")["static"]


def _translated_slugs_per_lang() -> dict[str, set[str]]:
    """Return ``{code: set_of_rendered_slugs}`` for every active non-EN
    language whose output dir exists under ``public/``."""
    out: dict[str, set[str]] = {}
    for code in _all_active_non_en_langs():
        d = PUBLIC / code
        if not d.is_dir():
            continue
        out[code] = {p.parent.name for p in d.glob("*/index.html")}
    return out


def _translated_slugs() -> tuple[set[str], set[str]]:
    """Legacy FR-only helper. Returns ``(en_slugs_with_fr,
    fr_slugs_with_en)`` for the call sites that haven't yet moved to
    the lang-keyed API."""
    fr_dir = PUBLIC / "fr"
    if not fr_dir.is_dir():
        return set(), set()
    rendered_fr = {p.parent.name for p in fr_dir.glob("*/index.html")}
    fr_articles_map = _lr.load_slugs("fr").get("articles", {})
    en_with_fr = {en for en, fr in fr_articles_map.items() if fr in rendered_fr}
    fr_to_en = {v: k for k, v in fr_articles_map.items()}
    fr_with_en = rendered_fr & set(fr_to_en.keys())
    return en_with_fr, fr_with_en


def _resolve_en_slug(slug: str, lang: str) -> str | None:
    """Reverse-map any language's slug to its EN counterpart."""
    if lang == "en":
        return slug
    maps = _slug_maps(lang)
    return (
        maps["articles_lang_to_en"].get(slug)
        or maps["statics_lang_to_en"].get(slug)
    )


def _alternates_for_en_slug(
    en_slug: str,
    translated_per_lang: dict[str, set[str]],
) -> list[tuple[str, str]]:
    """Build the full ``[(lang_code, absolute_url), …]`` alternate list
    for an EN slug."""
    alts: list[tuple[str, str]] = [
        ("en", f"https://sebastienrousseau.com/{en_slug}/"),
    ]
    for code in _all_active_non_en_langs():
        maps = _slug_maps(code)
        lang_slug = (
            maps["articles_en_to_lang"].get(en_slug)
            or maps["statics_en_to_lang"].get(en_slug)
        )
        if not lang_slug:
            continue
        if lang_slug not in translated_per_lang.get(code, set()):
            continue
        alts.append((code, f"https://sebastienrousseau.com/{code}/{lang_slug}/"))
    return alts


def inject_hreflang(
    html: str,
    slug: str,
    lang: str,
    translated_per_lang: dict[str, set[str]] | None = None,
    *,
    en_with_fr: set[str] | None = None,
    fr_with_en: set[str] | None = None,
) -> str:
    """Inject reciprocal hreflang links so search crawlers + the
    language-selector JS pair every translated version of a page."""
    if translated_per_lang is None:
        translated_per_lang = {}
        if fr_with_en:
            translated_per_lang["fr"] = fr_with_en
    en_slug = _resolve_en_slug(slug, lang)
    if en_slug is None:
        return html
    alts = _alternates_for_en_slug(en_slug, translated_per_lang)
    if len(alts) < 2:
        return html
    en_url = alts[0][1]
    html = _HREFLANG_RE.sub('', html)
    links = ''.join(
        f'<link rel="alternate" hreflang="{code}" href="{url}" />'
        for code, url in alts
    )
    links += f'<link rel="alternate" hreflang="x-default" href="{en_url}" />'
    return _HEAD_END_RE.sub(links + '</head>', html, count=1)
