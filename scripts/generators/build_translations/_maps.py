"""Locale text maps + EN→locale substitution passes.

Builds the per-language ``en_slug → title / description / excerpt /
eyebrow`` lookup tables from ``_posts/<lang>/*.md`` frontmatter, and
hosts every rewrite pass that substitutes EN strings/URLs with their
locale counterparts on forked pages.
"""

from __future__ import annotations

import html as _html
import re
from pathlib import Path

import _lang_registry

from . import _state as st
from ._fm import parse_frontmatter

# ---------------------------------------------------------------------------
# EN-URL → locale-URL rewriting
# ---------------------------------------------------------------------------

# The locale prefix is *absorbed* rather than merely tolerated. The origin
# group is optional and the pattern is unanchored, so on a URL that already
# carries one — "…com/ar/2026-05-26-slug" — the origin matched empty at the
# position after "/ar", the slug matched, and repl re-added "/ar/", emitting
# "/ar/ar/…". 103 links across the site 404'd because of it, invisible to the
# internal link audit because an absolute self-link is classified as external.
_EN_URL_PATTERN_TMPL = (
    r"(https?://sebastienrousseau\.com)?"
    r"(?:/(?:{locales}))?"
    r"/(?P<slug>{slugs})(/(?:index\.html)?)?"
)


def _build_en_url_rewriter() -> re.Pattern[str]:
    """Build a single anchored regex matching any internal EN slug
    that has a recorded FR counterpart. Used to rewrite EN URLs to
    /fr/<fr-slug>/ inside French page bodies."""
    slugs = "|".join(re.escape(s) for s in sorted(st.EN_TO_FR.keys(), key=len, reverse=True))
    if not slugs:
        return re.compile(r"(?!)")
    locales = "|".join(
        re.escape(lang.code)
        for lang in sorted(_lang_registry.LANGUAGES, key=lambda x: len(x.code), reverse=True)
    )
    return re.compile(_EN_URL_PATTERN_TMPL.format(slugs=slugs, locales=locales))


_EN_URL_RE_CACHE: dict[str, re.Pattern[str]] = {}


def _en_url_re() -> re.Pattern[str]:
    """Lang-aware cache of the EN-URL regex. Each call returns the
    regex built against the *current* EN_TO_FR map (rebound per lang
    by ``bind_lang``)."""
    key = st.LANG_CODE
    if key not in _EN_URL_RE_CACHE:
        _EN_URL_RE_CACHE[key] = _build_en_url_rewriter()
    return _EN_URL_RE_CACHE[key]


def rewrite_en_urls(html_fragment: str) -> str:
    """Rewrite every reference to an EN article URL to its
    current-language counterpart, keeping the same origin (absolute →
    absolute, root-relative → root-relative)."""

    def repl(m: re.Match[str]) -> str:
        origin = m.group(1) or ""
        en = m.group("slug")
        lang_slug = st.fr_slug(en)
        tail = m.group(3) or ""
        return f"{origin}/{st.LANG_CODE}/{lang_slug}{tail}"

    return _en_url_re().sub(repl, html_fragment)


# ---------------------------------------------------------------------------
# Locale frontmatter lookup tables (lazy, cleared per-language)
# ---------------------------------------------------------------------------


def _build_fr_title_map() -> dict[str, str]:
    """Walk every ``_posts/<lang>/*.md`` and return ``en_slug -> locale title``."""
    out: dict[str, str] = {}
    if not st.SRC.is_dir():
        return out
    for md in st.SRC.glob("*.md"):
        if not st._DATED_RE.match(md.stem):
            continue
        en = st.FR_TO_EN.get(md.stem, md.stem)
        fm, _ = parse_frontmatter(md.read_text(encoding="utf-8"))
        title = fm.get("title")
        if title:
            out[en] = title
    return out


def _ensure_fr_title_map() -> dict[str, str]:
    """Lazy-init the EN→FR title map."""
    if not st._FR_TITLE_MAP:
        st._FR_TITLE_MAP.update(_build_fr_title_map())
    return st._FR_TITLE_MAP


def _build_fr_description_map() -> dict[str, str]:
    """Walk every ``_posts/<lang>/*.md`` and return ``en_slug -> locale description``."""
    out: dict[str, str] = {}
    if not st.SRC.is_dir():
        return out
    for md in st.SRC.glob("*.md"):
        if not st._DATED_RE.match(md.stem):
            continue
        en = st.FR_TO_EN.get(md.stem, md.stem)
        fm, _ = parse_frontmatter(md.read_text(encoding="utf-8"))
        desc = fm.get("description")
        if desc:
            out[en] = desc
    return out


def _ensure_fr_description_map() -> dict[str, str]:
    if not st._FR_DESCRIPTION_MAP:
        st._FR_DESCRIPTION_MAP.update(_build_fr_description_map())
    return st._FR_DESCRIPTION_MAP


# ---------------------------------------------------------------------------
# Per-locale newsroom-card overrides
#
# The EN homepage and /articles/ listing render each article as a
# ``<article class="newsroom-card">`` block whose excerpt + eyebrow are
# baked-in EN strings. When we fork those pages for a locale, the
# default flow is:
#
#   * ``rewrite_newsroom_card_titles`` replaces the <h3> title with the
#     locale title (read from ``_posts/<lang>/<slug>.md`` frontmatter)
#   * ``rewrite_en_descs_in_text`` replaces any verbatim EN description
#     with its locale equivalent
#   * static-pattern token patches translate isolated EN nouns
#     ("April" → "avril", etc.)
#
# That left two leaks on every locale homepage card:
#
#   1. ``<p class="newsroom-excerpt">`` — comes from the EN article's
#      ``excerpt:`` frontmatter, which is a different field from
#      ``description:`` and so never gets swapped. Token patches half-
#      translate it (e.g. "The UK Payments Forward Plan and avril 2026
#      policy package set out a single framework…").
#   2. ``<span class="newsroom-eyebrow">`` — derived from the EN
#      ``tags:`` field and rendered as smart-cased English.
#
# These two maps + ``_smart_title_for_eyebrow`` close the gap by
# pulling the locale article's own ``excerpt:`` and ``tags:`` from
# ``_posts/<lang>/*.md`` and substituting them into the card markup at
# build time.
# ---------------------------------------------------------------------------


def _build_fr_excerpt_map() -> dict[str, str]:
    """Walk every ``_posts/<lang>/*.md`` and return ``en_slug -> locale
    excerpt`` so newsroom-card excerpts on the locale homepage and
    listing pages can be swapped to the locale's own frontmatter
    ``excerpt:`` field."""
    out: dict[str, str] = {}
    if not st.SRC.is_dir():
        return out
    for md in st.SRC.glob("*.md"):
        if not st._DATED_RE.match(md.stem):
            continue
        en = st.FR_TO_EN.get(md.stem, md.stem)
        fm, _ = parse_frontmatter(md.read_text(encoding="utf-8"))
        excerpt = fm.get("excerpt") or fm.get("subtitle") or fm.get("description")
        if excerpt:
            out[en] = excerpt
    return out


def _ensure_fr_excerpt_map() -> dict[str, str]:
    if not st._FR_EXCERPT_MAP:
        st._FR_EXCERPT_MAP.update(_build_fr_excerpt_map())
    return st._FR_EXCERPT_MAP


# Acronyms preserved in their canonical casing inside the eyebrow.
# Mirrors ``scripts/postbuild/regen_homepage.py`` so the EN homepage
# (rendered there) and locale homepage cards (rendered here) keep the
# same conventions for acronym handling.
_EYEBROW_ACRONYMS = {
    "AI",
    "AML",
    "API",
    "BIS",
    "BoE",
    "CBDC",
    "CBPR",
    "CSP",
    "CTO",
    "DLT",
    "DORA",
    "DSS",
    "ECB",
    "EU",
    "EUR",
    "FCA",
    "FedNow",
    "FX",
    "G20",
    "G7",
    "GDPR",
    "GENIUS",
    "GMT",
    "GBP",
    "HMRC",
    "HMT",
    "HM",
    "HSBC",
    "HSM",
    "ICT",
    "IETF",
    "ISO",
    "JP",
    "JPM",
    "KYC",
    "LLM",
    "ML",
    "MPP",
    "MT",
    "MTS",
    "MX",
    "NCSC",
    "NIS2",
    "NIST",
    "PIN",
    "PISP",
    "PoC",
    "PQC",
    "PSP",
    "PSR",
    "PSU",
    "QKD",
    "RTGS",
    "RTP",
    "SaaS",
    "SEPA",
    "SFTP",
    "SLA",
    "SWIFT",
    "SDX",
    "TIC",
    "TMS",
    "TLS",
    "UK",
    "UN",
    "US",
    "USD",
    "UX",
    "VC",
    "WCAG",
    "XML",
    "JSON-LD",
    "PII",
    "JSON",
    "YAML",
    "TOML",
    "HTML",
    "CSS",
    "PWA",
    "BST",
    "UTC",
    "USDC",
    "USDT",
    "BRSRV",
    "BSTBL",
    "MMF",
}


def _smart_title_for_eyebrow(token: str) -> str:
    """Title-case a single word but preserve known acronyms in their
    canonical casing. ``.title()`` would butcher ``UK`` into ``Uk``."""
    if token.upper() in _EYEBROW_ACRONYMS:
        return token.upper()
    if any(c.isupper() for c in token[1:]):
        # Mixed-case (e.g. "FedNow") — trust the source.
        return token
    return token.title()


def _eyebrow_from_locale_tags(tags: str) -> str:
    """First three comma-separated tags from the locale article's
    ``tags:`` frontmatter field, smart-cased per ``_EYEBROW_ACRONYMS``,
    joined with ' · '. Mirrors ``regen_homepage.py``'s eyebrow rule so
    EN and locale homepages stay visually consistent."""
    parts = [t.strip() for t in tags.split(",") if t.strip()][:3]
    return " · ".join(" ".join(_smart_title_for_eyebrow(w) for w in p.split()) for p in parts)


def _build_fr_eyebrow_map() -> dict[str, str]:
    """Walk every ``_posts/<lang>/*.md`` and return ``en_slug -> locale
    eyebrow string`` so newsroom-card eyebrows can be swapped to a
    locale-derived label instead of the smart-cased EN tags."""
    out: dict[str, str] = {}
    if not st.SRC.is_dir():
        return out
    for md in st.SRC.glob("*.md"):
        if not st._DATED_RE.match(md.stem):
            continue
        en = st.FR_TO_EN.get(md.stem, md.stem)
        fm, _ = parse_frontmatter(md.read_text(encoding="utf-8"))
        tags = fm.get("tags") or ""
        eyebrow = _eyebrow_from_locale_tags(tags)
        if eyebrow:
            out[en] = eyebrow
    return out


def _ensure_fr_eyebrow_map() -> dict[str, str]:
    if not st._FR_EYEBROW_MAP:
        st._FR_EYEBROW_MAP.update(_build_fr_eyebrow_map())
    return st._FR_EYEBROW_MAP


# ---------------------------------------------------------------------------
# Verbatim EN description / title substitution
# ---------------------------------------------------------------------------


def _en_descs_to_fr() -> tuple[re.Pattern[str], dict[str, str]]:
    """Build a regex + map matching every EN article description verbatim
    (and HTML-escaped variants) so we can substitute the FR description
    on listing pages (tags, topics, papers, project pages, …)."""
    if st._EN_DESC_TO_FR_RE_CACHE is not None and st._EN_DESC_TO_FR_MAP_CACHE is not None:
        return st._EN_DESC_TO_FR_RE_CACHE, st._EN_DESC_TO_FR_MAP_CACHE
    fr_descs = _ensure_fr_description_map()
    mapping: dict[str, str] = {}
    posts_dir = Path("_posts")
    for md in posts_dir.glob("2*.md"):
        text = md.read_text(encoding="utf-8")
        m = re.search(r'^description:\s*"((?:[^"\\]|\\.)*)"', text, re.MULTILINE)
        if not m:
            continue
        en_desc = m.group(1)
        en_slug = md.stem
        fr_desc = fr_descs.get(en_slug)
        if not fr_desc:
            continue
        mapping[en_desc] = fr_desc
        mapping[_html.escape(en_desc, quote=True)] = _html.escape(fr_desc, quote=True)
        mapping[_html.escape(en_desc, quote=False)] = _html.escape(fr_desc, quote=False)
    if not mapping:
        st._EN_DESC_TO_FR_RE_CACHE = re.compile(r"(?!)")
        st._EN_DESC_TO_FR_MAP_CACHE = {}
        return st._EN_DESC_TO_FR_RE_CACHE, st._EN_DESC_TO_FR_MAP_CACHE
    sorted_keys = sorted(mapping.keys(), key=len, reverse=True)
    st._EN_DESC_TO_FR_RE_CACHE = re.compile("|".join(re.escape(k) for k in sorted_keys if k))
    st._EN_DESC_TO_FR_MAP_CACHE = mapping
    return st._EN_DESC_TO_FR_RE_CACHE, st._EN_DESC_TO_FR_MAP_CACHE


def rewrite_en_descs_in_text(html: str) -> str:
    """Replace every verbatim EN article description with its FR
    counterpart. Affects card excerpts on /fr/tags/, /fr/topics/<sub>/,
    /fr/papers/ etc."""
    desc_re, desc_map = _en_descs_to_fr()
    if not desc_map:
        return html

    def repl(m: re.Match[str]) -> str:
        return desc_map.get(m.group(0), m.group(0))

    return desc_re.sub(repl, html)


def _en_titles_to_fr_re() -> re.Pattern[str]:
    """Compile a regex matching any known EN article title verbatim,
    capturing the matched EN title so we can substitute the FR one.
    Also matches HTML-entity-escaped variants so we catch titles inside
    rendered HTML attributes (& → &amp;, ' → &#x27;, " → &quot;)."""
    if st._EN_TITLES_TO_FR_RE_CACHE is not None:
        return st._EN_TITLES_TO_FR_RE_CACHE
    raw_titles: list[str] = []
    posts_dir = Path("_posts")
    for md in posts_dir.glob("2*.md"):
        text = md.read_text(encoding="utf-8")
        m = re.search(r'^title:\s*"((?:[^"\\]|\\.)*)"', text, re.MULTILINE)
        if m:
            raw_titles.append(m.group(1))
    if not raw_titles:
        st._EN_TITLES_TO_FR_RE_CACHE = re.compile(r"(?!)")
        return st._EN_TITLES_TO_FR_RE_CACHE
    variants: set[str] = set()
    for t in raw_titles:
        variants.add(t)
        variants.add(_html.escape(t, quote=True))
        variants.add(_html.escape(t, quote=False))
    sorted_variants = sorted(variants, key=len, reverse=True)
    pattern = "|".join(re.escape(v) for v in sorted_variants if v)
    st._EN_TITLES_TO_FR_RE_CACHE = re.compile(pattern)
    return st._EN_TITLES_TO_FR_RE_CACHE


def _en_title_to_fr_map() -> dict[str, str]:
    """Map every EN title variant (raw + HTML-entity escaped) to the
    FR title (and the same FR title encoded the same way)."""
    if st._EN_TITLE_TO_FR_MAP_CACHE is not None:
        return st._EN_TITLE_TO_FR_MAP_CACHE
    out: dict[str, str] = {}
    fr_titles = _ensure_fr_title_map()
    posts_dir = Path("_posts")
    for md in posts_dir.glob("2*.md"):
        text = md.read_text(encoding="utf-8")
        m = re.search(r'^title:\s*"((?:[^"\\]|\\.)*)"', text, re.MULTILINE)
        if not m:
            continue
        en_title = m.group(1)
        en_slug = md.stem
        fr_title = fr_titles.get(en_slug)
        if not fr_title:
            continue
        out[en_title] = fr_title
        out[_html.escape(en_title, quote=True)] = _html.escape(fr_title, quote=True)
        out[_html.escape(en_title, quote=False)] = _html.escape(fr_title, quote=False)
    st._EN_TITLE_TO_FR_MAP_CACHE = out
    return st._EN_TITLE_TO_FR_MAP_CACHE


def rewrite_en_titles_in_text(html: str) -> str:
    """Wherever a known EN article title appears verbatim in plain text
    (citation lists, headings inside cards, etc.), replace it with the
    matching FR title."""
    title_re = _en_titles_to_fr_re()
    title_map = _en_title_to_fr_map()
    if not title_map:
        return html

    def repl(m: re.Match[str]) -> str:
        return title_map.get(m.group(0), m.group(0))

    return title_re.sub(repl, html)


# ---------------------------------------------------------------------------
# Card / link rewriting
# ---------------------------------------------------------------------------

_RELATED_CARD_RE = re.compile(
    r'(<article class="related-card">)([\s\S]*?)(</article>)',
)
_HREF_FR_SLUG_RE = re.compile(
    r'href="(?:https?://sebastienrousseau\.com)?/fr/([a-z0-9-]+)/(?:index\.html)?"'
)


_FR_LINK_RE = re.compile(
    r'<a(\s[^>]*)href="(?:https?://sebastienrousseau\.com)?/fr/([a-z0-9-]+)/(?:index\.html)?"([^>]*)>',
    re.IGNORECASE,
)


def rewrite_fr_link_titles(html: str) -> str:
    """Walk every ``<a href="/fr/<slug>/…">`` and overwrite the
    ``title="…"`` and ``aria-label="…"`` attributes with the matching
    FR title from the slug map. Inner anchor text is left untouched
    (the author may have chosen it deliberately as a citation or
    contextual label)."""
    fr_titles = _ensure_fr_title_map()

    def repl(m: re.Match[str]) -> str:
        before, slug, after = m.group(1), m.group(2), m.group(3)
        en = st.FR_TO_EN.get(slug)
        if not en:
            return m.group(0)
        fr_title = fr_titles.get(en)
        if not fr_title:
            return m.group(0)
        esc = _html.escape(fr_title, quote=True)
        attrs = (before or "") + (after or "")
        # Replace title= and aria-label= if present, else inject title=.
        if re.search(r'\btitle="', attrs):
            attrs = re.sub(r'(\btitle=")[^"]*(")', rf"\g<1>{esc}\g<2>", attrs, count=1)
        else:
            attrs = attrs.rstrip() + f' title="{esc}"'
        if re.search(r'\baria-label="', attrs):
            attrs = re.sub(r'(\baria-label=")[^"]*(")', rf"\g<1>{esc}\g<2>", attrs, count=1)
        return f'<a{attrs} href="/{st.LANG_CODE}/{slug}/index.html">'

    return _FR_LINK_RE.sub(repl, html)


_NEWSROOM_CARD_RE = re.compile(
    # Tolerate both ``class="newsroom-card"`` and the minified
    # ``class=newsroom-card`` forms — the HTML minifier strips quotes
    # off attributes whose values lack whitespace/special chars.
    r'(<article\s[^>]*class\s*=\s*(?:"newsroom-card[^"]*"|newsroom-card[^\s>]*)[^>]*>)([\s\S]*?)(</article>)',
)


def rewrite_newsroom_card_titles(html: str) -> str:
    """On locale listing pages (papers, projects, tags, topics, homepage, …)
    the ``newsroom-card`` markup is forked from the EN shell. Each card
    carries EN content for the title, excerpt and eyebrow which would
    otherwise leak through token-level patches only — see the comment
    on ``_build_fr_excerpt_map`` for the leak this closes.

    For each card whose href identifies the article, look up:
      - locale title       (frontmatter ``title:``)        → <h3><a>
      - locale title       (escaped)                       → aria-label + title=
      - locale excerpt     (frontmatter ``excerpt:``)      → <p class="newsroom-excerpt">
      - locale eyebrow     (first 3 ``tags:`` smart-cased) → <span class="newsroom-eyebrow">

    A missing locale field leaves the corresponding EN value in place
    — partial localisation is still an improvement over none."""
    fr_titles = _ensure_fr_title_map()
    fr_excerpts = _ensure_fr_excerpt_map()
    fr_eyebrows = _ensure_fr_eyebrow_map()

    def patch(m: re.Match[str]) -> str:
        open_tag, inner, close_tag = m.group(1), m.group(2), m.group(3)
        # Match the article href in both quoted and unquoted-attribute
        # forms — the HTML minifier strips quotes off attribute values
        # that don't need them (no whitespace, no special chars).
        slug_m = re.search(
            r'href\s*=\s*(?:"(?:https?://sebastienrousseau\.com)?/'
            + re.escape(st.LANG_CODE)
            + r'/([a-z0-9-]+)/(?:index\.html)?"'
            + r"|(?:https?://sebastienrousseau\.com)?/"
            + re.escape(st.LANG_CODE)
            + r"/([a-z0-9-]+)/(?:index\.html)?(?=[\s>]))",
            inner,
        )
        if not slug_m:
            return m.group(0)
        slug = slug_m.group(1) or slug_m.group(2)
        en = st.FR_TO_EN.get(slug)
        if not en:
            return m.group(0)

        fr_title = fr_titles.get(en)
        fr_excerpt = fr_excerpts.get(en)
        fr_eyebrow = fr_eyebrows.get(en)

        if fr_title:
            esc = _html.escape(fr_title, quote=True)
            # <h3>…<a>TITLE</a>… inner text.
            inner = re.sub(
                r"(<h3[^>]*>\s*<a [^>]+>)[^<]+(</a>)",
                rf"\g<1>{_html.escape(fr_title)}\g<2>",
                inner,
                count=1,
            )
            # aria-label on media link.
            inner = re.sub(
                r'(<a [^>]*class="newsroom-card-media"[^>]*aria-label=")[^"]+(")',
                rf"\g<1>{esc}\g<2>",
                inner,
                count=1,
            )
            # title= on the same link.
            inner = re.sub(
                r'(<a [^>]*class="newsroom-card-media"[^>]*title=")[^"]+(")',
                rf"\g<1>{esc}\g<2>",
                inner,
                count=1,
            )

        if fr_excerpt:
            # <p class="newsroom-excerpt">…</p> — tolerate the minified
            # output's unquoted class attribute (``class=newsroom-excerpt``).
            inner = re.sub(
                r'(<p\s[^>]*class\s*=\s*(?:"newsroom-excerpt"|newsroom-excerpt)[^>]*>)[^<]*(</p>)',
                rf"\g<1>{_html.escape(fr_excerpt)}\g<2>",
                inner,
                count=1,
            )

        if fr_eyebrow:
            # <span class="newsroom-eyebrow">…</span> — same minifier
            # consideration as above.
            inner = re.sub(
                r'(<span\s[^>]*class\s*=\s*(?:"newsroom-eyebrow"|newsroom-eyebrow)[^>]*>)[^<]*(</span>)',
                rf"\g<1>{_html.escape(fr_eyebrow)}\g<2>",
                inner,
                count=1,
            )

        return open_tag + inner + close_tag

    return _NEWSROOM_CARD_RE.sub(patch, html)


def rewrite_related_card_titles(html_fragment: str) -> str:
    """Walk the related-posts grid; replace EN titles inside each card
    with the matching FR title looked up from the slug map."""
    fr_titles = _ensure_fr_title_map()

    def patch_card(m: re.Match[str]) -> str:
        open_tag, inner, close_tag = m.group(1), m.group(2), m.group(3)
        # Pull the FR slug from the first link in the card.
        slug_m = _HREF_FR_SLUG_RE.search(inner)
        if not slug_m:
            return m.group(0)
        fr_slug_str = slug_m.group(1)
        en = st.FR_TO_EN.get(fr_slug_str)
        if not en:
            return m.group(0)
        fr_title = fr_titles.get(en)
        if not fr_title:
            return m.group(0)
        esc = _html.escape(fr_title, quote=True)
        # Rewrite aria-label on media link.
        inner = re.sub(
            r'(<a [^>]*class="related-media"[^>]*aria-label=")[^"]+(")',
            rf"\g<1>{esc}\g<2>",
            inner,
            count=1,
        )
        # Rewrite the visible <h3>...<a>TITLE</a>... block.
        inner = re.sub(
            r"(<h3[^>]*>\s*<a [^>]+>)[^<]+(</a>)",
            rf"\g<1>{_html.escape(fr_title)}\g<2>",
            inner,
            count=1,
        )
        # Rewrite anchor-link aria-label "Link to TITLE".
        inner = re.sub(
            r'(<a class="heading-anchor"[^>]*aria-label="(?:Lien vers|Link to) )[^"]+(")',
            rf"\g<1>{esc}\g<2>",
            inner,
            count=1,
        )
        return open_tag + inner + close_tag

    return _RELATED_CARD_RE.sub(patch_card, html_fragment)
