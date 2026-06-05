#!/usr/bin/env python3
"""Render manual French translations under ``public/fr/{slug}/``.

Translation sources live in ``_posts/fr/*.md``. For each translation,
this script:

  1. Parses YAML frontmatter (title, description, banner, dates, …).
  2. Renders the markdown body to HTML via markdown-it-py.
  3. Loads the rendered English page at ``public/{slug}/index.html`` and
     uses it as a shell — same nav, footer, head meta, CSS — so the
     French version inherits every layout fix automatically.
  4. Swaps the English body for the French body and patches every
     language-bearing attribute (html lang, meta description, og:*,
     canonical, JSON-LD inLanguage / headline / description).
  5. Writes ``public/fr/{slug}/index.html``.

Also emits ``public/fr/index.html`` — the French articles hub.

Hreflang reciprocity (English ↔ French) is wired in postbuild.py so
the link tags survive subsequent rebuilds.

Must run AFTER ``ssg`` and ``build_topics.py``, BEFORE
``build_agent_api.py`` and ``postbuild.py`` (so the French pages enter
the same SRI / CSP / sitemap pipeline as the English originals).
"""

from __future__ import annotations

import sys as _sys  # path bootstrap — scripts reorg (scripts/lib/ on sys.path)
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "lib"))

import html as _html
import json as _json
import re
import sys
from pathlib import Path

from markdown_it import MarkdownIt

sys.path.insert(0, str(Path(__file__).parent))
import _lang_registry  # script-mode sibling import

PUBLIC = Path("public")
BASE = "https://sebastienrousseau.com"

# Lang-parametric globals — rebound per-language by ``main()`` before
# calling the render functions. Default values target FR so module-load
# stays backward-compatible while the loop drives each active non-EN
# language end-to-end.
LANG_CODE = "fr"
LANG_BCP47 = "fr-FR"
LANG_LOCALE = "fr_FR"
SRC = Path(f"_posts/{LANG_CODE}")
OUT = PUBLIC / LANG_CODE

# Slug maps used by the render functions and by helpers throughout.
# EN_TO_FR / FR_TO_EN / fr_slug names preserved for diff minimality;
# rebound per-language in ``main()``.
_articles_map = _lang_registry.load_slugs(LANG_CODE)["articles"]
EN_TO_FR: dict[str, str] = dict(_articles_map)
FR_TO_EN: dict[str, str] = {v: k for k, v in _articles_map.items()}


def fr_slug(en_slug: str) -> str:
    return EN_TO_FR.get(en_slug, en_slug)


_DATED_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-")

# French UI strings — used by the meta-bar swap pass below and by
# postbuild's furniture renderers when they detect <html lang="fr">.
# Body-text labels for inline article chrome — now sourced from
# _data/i18n/<lang>/labels.json via _lang_registry.load_labels(). The
# old inline dict is kept as a frozen alias so any external code that
# imported I18N_FR keeps working through Phase 6a; Phase 6b will move
# the consumers to read by lang_code directly.
I18N_FR: dict[str, str] = _lang_registry.load_labels("fr")

_FM_KEY_RE = re.compile(r'^([a-zA-Z_]+):\s*(?:"((?:[^"\\]|\\.)*)"|\'((?:[^\'\\]|\\.)*)\')\s*$')


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Return (frontmatter_dict, body_markdown). Frontmatter is the
    block between the first pair of ``---`` lines."""
    lines = text.splitlines(keepends=True)
    fm: dict[str, str] = {}
    body_start = 0
    sep_count = 0
    inside = False
    for i, line in enumerate(lines):
        if line.strip() == "---":
            sep_count += 1
            inside = sep_count == 1
            if sep_count == 2:
                body_start = i + 1
                break
            continue
        if not inside:
            continue
        m = _FM_KEY_RE.match(line.strip())
        if m:
            fm[m.group(1)] = m.group(2) if m.group(2) is not None else m.group(3)
    body = "".join(lines[body_start:])
    return fm, body


def render_markdown(body: str) -> str:
    md = MarkdownIt("commonmark", {"html": True, "linkify": True})
    md.enable(["table", "strikethrough"])
    return md.render(body)


# ---------------------------------------------------------------------------
# Page-level transforms
# ---------------------------------------------------------------------------

_MAIN_BODY_RE = re.compile(
    r'(<main\b[^>]*>\s*<div class="wrap[^"]*">)([\s\S]*?)(</div>\s*</main>)',
    re.IGNORECASE,
)
_HERO_RE = re.compile(
    r'(<section class="ap-hero">\s*<h1>)[^<]*(</h1>\s*<p class="sub">)[^<]*(</p>)',
    re.IGNORECASE,
)
_TITLE_RE = re.compile(r"<title>[^<]*</title>", re.IGNORECASE)
_DESC_META_RE = re.compile(r'(<meta\s+name="description"\s+content=")[^"]*(")', re.IGNORECASE)
_KW_META_RE = re.compile(r'(<meta\s+name="keywords"\s+content=")[^"]*(")', re.IGNORECASE)
_HTML_LANG_RE = re.compile(r'(<html\b[^>]*\blang=)"?[^"\s>]*"?', re.IGNORECASE)
_HTML_DIR_RE = re.compile(r'(<html\b[^>]*?)\s+dir="[^"]*"', re.IGNORECASE)
_HTML_OPEN_RE = re.compile(r"(<html\b[^>]*?)(>)", re.IGNORECASE)


def _is_current_rtl() -> bool:
    """Return True if the current ``LANG_CODE`` is an RTL language
    (per ``_lang_registry.LANGUAGES``)."""
    return any(lg.code == LANG_CODE and lg.rtl for lg in _lang_registry.LANGUAGES)


def _set_html_lang(shell: str) -> str:
    """Patch the ``<html>`` element: set the lang attribute to the
    current BCP-47 tag, and add/strip ``dir="rtl"`` based on the
    language's RTL flag. Drops any existing dir before re-adding the
    right one — idempotent across re-runs."""
    shell = _HTML_LANG_RE.sub(rf'\g<1>"{LANG_BCP47}"', shell, count=1)
    shell = _HTML_DIR_RE.sub(r"\g<1>", shell, count=1)
    if _is_current_rtl():
        shell = _HTML_OPEN_RE.sub(r'\g<1> dir="rtl"\g<2>', shell, count=1)
    return shell


_OG_TITLE_RE = re.compile(r'(<meta\s+property="og:title"\s+content=")[^"]*(")', re.IGNORECASE)
_OG_DESC_RE = re.compile(r'(<meta\s+property="og:description"\s+content=")[^"]*(")', re.IGNORECASE)
_OG_URL_RE = re.compile(r'(<meta\s+property="og:url"\s+content=")[^"]*(")', re.IGNORECASE)
_OG_LOCALE_RE = re.compile(r'(<meta\s+property="og:locale"\s+content=")[^"]*(")', re.IGNORECASE)
_TW_TITLE_RE = re.compile(r'(<meta\s+name="twitter:title"\s+content=")[^"]*(")', re.IGNORECASE)
_TW_DESC_RE = re.compile(r'(<meta\s+name="twitter:description"\s+content=")[^"]*(")', re.IGNORECASE)
_CANONICAL_RE = re.compile(r'(<link\s+rel="canonical"\s+href=")[^"]*(")', re.IGNORECASE)
_BLOGPOSTING_HEADLINE_RE = re.compile(r'("@type":"BlogPosting"[^}]*?"headline":")[^"]*(")')
_BLOGPOSTING_DESC_RE = re.compile(r'("@type":"BlogPosting"[^}]*?"description":")[^"]*(")')
_BLOGPOSTING_LANG_RE = re.compile(r'("@type":"BlogPosting"[^}]*?"inLanguage":")[^"]*(")')
_BLOGPOSTING_URL_RE = re.compile(r'("@type":"BlogPosting"[^}]*?"url":")[^"]*(")')


def _date_today() -> str:
    from datetime import datetime as _dt

    return _dt.now().strftime("%Y-%m-%d")


# Comprehensive chrome-string translations. Applied to every French page
# after the rendered English shell is forked. Each entry is a (regex,
# replacement) pair — anchored to its HTML context so it can't match
# the same English word inside article body content.
#
# Phase 0c refactor: the first chunk of CHROME_PATCHES is auto-built
# from ``_data/i18n/fr/strings.json`` via
# ``_lang_registry.build_chrome_patches("fr")``. Adding the same key to
# ``_data/i18n/<lang>/strings.json`` for a new language produces the
# right patches automatically — no Python edit required for mechanical
# attribute/text cases. The manual list below covers regex-quirky cases
# the auto-gen can't express cleanly (entity tolerance, dynamic
# prefixes, negative lookaheads, multi-string composites).
CHROME_PATCHES: list[tuple[str, str]] = [
    *_lang_registry.build_chrome_patches("fr"),
    *_lang_registry.load_chrome_patches_inline("fr"),
]

_CHROME_PATCHES_COMPILED: list[tuple[re.Pattern[str], str]] = [
    (re.compile(p), r) for p, r in CHROME_PATCHES
]


def translate_chrome(html: str) -> str:
    """Apply all CHROME_PATCHES to localize nav / footer / search / social
    strings on a French page. Anchored regexes — no false positives in
    article body."""
    for pat, repl in _CHROME_PATCHES_COMPILED:
        html = pat.sub(repl, html)
    html = rewrite_static_links(html)
    html = localize_en_dates(html)
    return html


# English month names → per-language equivalents. Rebound by
# _bind_lang() so date-localisation uses the current language's names.
_LANG_MONTHS: dict[str, dict[str, str]] = {
    "fr": {
        "January": "janvier",
        "February": "février",
        "March": "mars",
        "April": "avril",
        "May": "mai",
        "June": "juin",
        "July": "juillet",
        "August": "août",
        "September": "septembre",
        "October": "octobre",
        "November": "novembre",
        "December": "décembre",
        "Jan": "janv.",
        "Feb": "févr.",
        "Mar": "mars",
        "Apr": "avr.",
        "Jun": "juin",
        "Jul": "juill.",
        "Aug": "août",
        "Sep": "sept.",
        "Sept": "sept.",
        "Oct": "oct.",
        "Nov": "nov.",
        "Dec": "déc.",
    },
    "de": {
        "January": "Januar",
        "February": "Februar",
        "March": "März",
        "April": "April",
        "May": "Mai",
        "June": "Juni",
        "July": "Juli",
        "August": "August",
        "September": "September",
        "October": "Oktober",
        "November": "November",
        "December": "Dezember",
        "Jan": "Jan.",
        "Feb": "Feb.",
        "Mar": "März",
        "Apr": "Apr.",
        "Jun": "Juni",
        "Jul": "Juli",
        "Aug": "Aug.",
        "Sep": "Sept.",
        "Sept": "Sept.",
        "Oct": "Okt.",
        "Nov": "Nov.",
        "Dec": "Dez.",
    },
}
_EN_MONTH_TO_FR: dict[str, str] = dict(_LANG_MONTHS["fr"])  # rebound per-lang

_DATE_FULL_RE = re.compile(
    r"\b(" + "|".join(m for m in _EN_MONTH_TO_FR if len(m) > 4) + r")\s+(\d{1,2}),\s+(\d{4})\b"
)
_DATE_SHORT_RE = re.compile(
    r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\s+(\d{1,2}),\s+(\d{4})\b"
)
_DATE_YEAR_MONTH_RE = re.compile(
    r"\b(" + "|".join(m for m in _EN_MONTH_TO_FR if len(m) > 4) + r")\s+(\d{4})\b"
)


def localize_en_dates(html: str) -> str:
    """Rewrite English `Month DD, YYYY` and `Mon DD, YYYY` to the French
    equivalent. Skips inside <time datetime="…"> attribute values."""

    # Replace only inside visible text — protect <time datetime="…"> values.
    # Cheap approach: split on `<time` tags, only patch the *visible* segment
    # ("…">DATE</time>"); leave the attribute value alone.
    # Simpler: apply substitutions, but inside attribute values the same
    # substitutions are safe because we only swap the visible-month words —
    # ISO datetime attributes use numbers (YYYY-MM-DD), not month names.
    def full_repl(m: re.Match[str]) -> str:
        return f"{int(m.group(2))} {_EN_MONTH_TO_FR[m.group(1)]} {m.group(3)}"

    def short_repl(m: re.Match[str]) -> str:
        month = _EN_MONTH_TO_FR.get(m.group(1), m.group(1))
        return f"{int(m.group(2))} {month} {m.group(3)}"

    def ym_repl(m: re.Match[str]) -> str:
        return f"{_EN_MONTH_TO_FR[m.group(1)]} {m.group(2)}"

    html = _DATE_FULL_RE.sub(full_repl, html)
    html = _DATE_SHORT_RE.sub(short_repl, html)
    html = _DATE_YEAR_MONTH_RE.sub(ym_repl, html)
    return html


# Canonical EN → FR slug map for the static pages mirrored under /fr/.
# Visible URLs are localised (e.g. /fr/privacy/ → /fr/confidentialite/).
# Slugs without a translation (contact, playlists, 404, articles) keep
# their English form because the word is identical or universal.
STATIC_SLUG_FR: dict[str, str] = _lang_registry.load_slugs("fr")["static"]
STATIC_SLUG_EN: dict[str, str] = {v: k for k, v in STATIC_SLUG_FR.items()}

# Static pages we mirror under /fr/. Keys are the EN slugs.
_STATIC_FR_PAGES = tuple(STATIC_SLUG_FR.keys())
_STATIC_LINK_RE = re.compile(
    r'(href=)(["\']?)(?:https?://sebastienrousseau\.com)?/('
    + "|".join(re.escape(s) for s in _STATIC_FR_PAGES)
    + r")(/(?:index\.html)?)?\2(?=[\s>])",
)
# Also catch links to ALREADY-FR slugs like /fr/privacy/ that should be /fr/confidentialite/
_LEGACY_FR_LINK_RE = re.compile(
    r'(href=)(["\']?)(?:https?://sebastienrousseau\.com)?/fr/('
    + "|".join(re.escape(s) for s in _STATIC_FR_PAGES)
    + r")(/(?:index\.html)?)?\2(?=[\s>])",
)
_TOPIC_SUBPAGE_RE = re.compile(
    r'(href=)(["\']?)(?:https?://sebastienrousseau\.com)?/(?:fr/)?topics/([a-z0-9-]+)(/(?:index\.html)?)\2(?=[\s>])',
)


def rewrite_static_links(html: str) -> str:
    """Rewrite every internal anchor on a FR page that still points at a
    top-level EN (or EN-slug FR) static page so it lands on the
    correctly-localised FR slug under /fr/. Handles both quoted and
    unquoted href attributes."""

    def repl_top_level(m: re.Match[str]) -> str:
        en_slug = m.group(3)
        fr_slug_str = STATIC_SLUG_FR.get(en_slug, en_slug)
        tail = m.group(4) or "/"
        if not tail.startswith("/"):
            tail = "/" + tail
        return f'{m.group(1)}"/{LANG_CODE}/{fr_slug_str}{tail}"'

    def repl_legacy_fr(m: re.Match[str]) -> str:
        en_slug = m.group(3)
        fr_slug_str = STATIC_SLUG_FR.get(en_slug, en_slug)
        if fr_slug_str == en_slug:
            return m.group(0)  # nothing to change
        tail = m.group(4) or "/"
        if not tail.startswith("/"):
            tail = "/" + tail
        return f'{m.group(1)}"/{LANG_CODE}/{fr_slug_str}{tail}"'

    def repl_topic_sub(m: re.Match[str]) -> str:
        topics_slug_lang = STATIC_SLUG_FR.get("topics", "topics")
        return f'{m.group(1)}"/{LANG_CODE}/{topics_slug_lang}/{m.group(3)}{m.group(4)}"'

    html = _STATIC_LINK_RE.sub(repl_top_level, html)
    html = _LEGACY_FR_LINK_RE.sub(repl_legacy_fr, html)
    html = _TOPIC_SUBPAGE_RE.sub(repl_topic_sub, html)
    return html


# French author-card content (static — replaces the English author-card
# that post_enrich.py baked into the rendered shell). Synced with the
# English version in scripts/post_enrich.py.
def _french_author_card() -> str:
    """Author-card aside for the current language. All localised text
    (aria-label, portrait alt, bio, credentials prefix, full-profile
    link) reads from the registry; the URL resolves via STATIC_SLUG_FR.
    """
    about_slug = STATIC_SLUG_FR.get("about", "about")
    strings = _lang_registry.load_strings(LANG_CODE)
    author = _lang_registry.load_author(LANG_CODE)
    aria = strings.get("author.aria.aboutAuthor", "About the author")
    portrait_alt = strings.get("author.alt.portrait", "Portrait of Sebastien Rousseau")
    full_profile = strings.get("author.fullProfile", "Full profile")
    bio = author.get("bio", "")
    credentials_prefix = author.get("credentialsPrefix", "")
    return (
        f'<aside class="author-card" aria-label="{aria}">'
        f'<img alt="{portrait_alt}" '
        'src="https://cloudcdn.pro/stocks/images/sebastien-rousseau.png" '
        'width="64" height="64" loading="lazy" decoding="async" />'
        '<span class="author-card-body">'
        '<strong class="author-card-name">'
        f'<a href="/{LANG_CODE}/{about_slug}/index.html">Sebastien Rousseau</a></strong>'
        f'<span class="author-card-bio">{bio}</span>'
        '<span class="author-credentials">'
        f"{credentials_prefix} "
        f'<a href="/{LANG_CODE}/{about_slug}/index.html">{full_profile}</a> &middot; '
        '<a href="https://www.linkedin.com/in/sebastienrousseau/" rel="external noopener">LinkedIn</a> &middot; '
        '<a href="https://github.com/sebastienrousseau" rel="external noopener">GitHub</a>'
        "</span></span></aside>"
    )


_LEAD_ASIDE_RE = re.compile(
    r'<aside\s+class="post-lead"[\s\S]*?</aside>',
    re.IGNORECASE,
)
_RELATED_POSTS_ASIDE_RE = re.compile(
    r'<aside\s+class="related-posts"[\s\S]*?</aside>',
    re.IGNORECASE,
)

# English takeaway-section labels that appear inside <li><strong>…</strong>
# in the post-lead aside. These come from the EN article's H2s and need
# translating on every FR page.
# Takeaway-aside labels — now sourced from _data/i18n/<lang>/takeaway_labels.json
# via _lang_registry.load_takeaway_labels(). Kept as a frozen alias here so
# legacy consumers keep working through Phase 6b; Phase 6c will move call
# sites to read by lang_code directly.
TAKEAWAY_LABELS_EN_TO_FR: dict[str, str] = _lang_registry.load_takeaway_labels("fr")

# Compile to a single regex matched against the inner text of
# ``<li><strong>LABEL.</strong>``. The trailing dot is preserved.
_TAKEAWAY_LABEL_RE = re.compile(
    r"(<li><strong>)("
    + "|".join(re.escape(k) for k in sorted(TAKEAWAY_LABELS_EN_TO_FR, key=len, reverse=True))
    + r")(\.</strong>)"
)


def _localise_takeaway_labels(html_fragment: str) -> str:
    """Translate the English takeaway labels in the FR lead aside."""

    def repl(m: re.Match[str]) -> str:
        return m.group(1) + TAKEAWAY_LABELS_EN_TO_FR[m.group(2)] + m.group(3)

    return _TAKEAWAY_LABEL_RE.sub(repl, html_fragment)


_POST_LEAD_TLDR_RE = re.compile(
    r'(<p class="post-lead-tldr"><strong>TL;DR\.</strong>\s*)([^<]+)(</p>)',
)


def _localise_post_lead(lead_html: str, description: str) -> str:
    """Patch the lead aside extracted from the EN shell:
    1. Replace the EN TL;DR with the FR description.
    2. Translate takeaway section labels (Idea / Impact / …).
    3. Drop the EN ``Related reading:`` paragraph — the page has its own
       at the bottom in French already.
    """
    if not lead_html:
        return lead_html
    if description:
        lead_html = _POST_LEAD_TLDR_RE.sub(
            lambda m: m.group(1) + _html.escape(description) + m.group(3),
            lead_html,
            count=1,
        )
    lead_html = _localise_takeaway_labels(lead_html)
    # Strip the EN "Related reading:" line — it's English titles, and the
    # related-posts grid at the bottom already covers it in French.
    lead_html = re.sub(
        r'<p class="post-lead-related">[\s\S]*?</p>',
        "",
        lead_html,
        count=1,
    )
    return lead_html


def _extract_shell_blocks(shell_html: str) -> tuple[str, str]:
    """Pull the post-lead aside (TL;DR + Key takeaways + Related reading)
    and the related-posts aside (3-card grid) out of the rendered English
    shell so we can reuse them on the French page for UX parity. Labels
    inside get translated later by translate_chrome()."""
    lead_m = _LEAD_ASIDE_RE.search(shell_html)
    related_m = _RELATED_POSTS_ASIDE_RE.search(shell_html)
    return (lead_m.group(0) if lead_m else "", related_m.group(0) if related_m else "")


def _french_lead_fallback(description: str) -> str:
    """Minimal lead aside used when the English shell doesn't ship one
    (very short posts) — keeps the TL;DR row visually consistent."""
    if not description:
        return ""
    return (
        '<aside class="post-lead" aria-label="Résumé de l\'article">'
        f'<p class="post-lead-tldr"><strong>TL;DR.</strong> {_html.escape(description)}</p>'
        "</aside>"
    )


_FR_GENERIC_H2 = frozenset(
    {
        "aperçu",
        "introduction",
        "vue d'ensemble",
        "sommaire",
        "table des matières",
        "lectures complémentaires",
        "points clés",
        "références",
        "sources et références",
        "résumé",
        "à propos",
        "conclusion",
    }
)


def _derive_fr_takeaways(body_md: str, max_items: int = 4) -> list[tuple[str, str]]:  # noqa: C901 — sequential heuristics; splitting hurts readability
    """Walk the FR markdown body; for each H2 (then H3) that isn't a
    generic heading, return (heading_text, first_sentence).
    """
    bullets: list[tuple[str, str]] = []
    lines = body_md.splitlines()
    n = len(lines)

    def first_sentence(start_idx: int) -> str:  # noqa: C901
        paragraph_lines: list[str] = []
        for j in range(start_idx, min(start_idx + 20, n)):
            stripped = lines[j].strip()
            if not stripped:
                if paragraph_lines:
                    break
                continue
            if stripped.startswith(("#", "<", "!", "*[", "```", "|", ">")):
                if paragraph_lines:
                    break
                continue
            if stripped.startswith(("- ", "* ")):
                if paragraph_lines:
                    break
                continue
            if re.match(r"^\[\d+\]:\s", stripped):
                if paragraph_lines:
                    break
                continue
            paragraph_lines.append(stripped)
        if not paragraph_lines:
            return ""
        paragraph = " ".join(paragraph_lines)
        # Strip markdown emphasis + links.
        paragraph = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", paragraph)
        paragraph = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", paragraph)
        paragraph = re.sub(r"\*\*([^*]+)\*\*", r"\1", paragraph)
        paragraph = re.sub(r"\*([^*]+)\*", r"\1", paragraph)
        paragraph = re.sub(r"`([^`]+)`", r"\1", paragraph)
        paragraph = re.sub(r"\s*\.class=\\.+$", "", paragraph)
        # First sentence.
        m = re.search(r"[.!?](?=\s|$)", paragraph)
        sentence = paragraph[: m.end()] if m else paragraph
        if not sentence.endswith((".", "!", "?")):
            sentence += "."
        if len(sentence) > 220:
            sentence = sentence[:217].rsplit(" ", 1)[0] + "…"
        return sentence

    def add_for_level(prefix: str) -> None:
        for i, ln in enumerate(lines):
            if not ln.startswith(prefix):
                continue
            heading = ln[len(prefix) :].strip().rstrip(".").rstrip(":")
            heading_clean = re.sub(r"[*_`]", "", heading)
            if heading_clean.lower() in _FR_GENERIC_H2:
                continue
            sent = first_sentence(i + 1)
            if sent:
                bullets.append((heading_clean, sent))
                if len(bullets) >= max_items:
                    return

    add_for_level("## ")
    if len(bullets) < max_items:
        add_for_level("### ")
    return bullets


def _build_fr_lead(description: str, takeaways: list[tuple[str, str]]) -> str:
    """Build the post-lead aside fresh, in French, from the FR body."""
    parts: list[str] = [
        '<aside class="post-lead" aria-label="Résumé de l\'article">',
        f'<p class="post-lead-tldr"><strong>TL;DR.</strong> {_html.escape(description)}</p>',
    ]
    if takeaways:
        parts.append('<p class="post-lead-heading"><strong>Points clés</strong></p>')
        parts.append('<ul class="post-lead-takeaways">')
        for heading, sentence in takeaways:
            parts.append(
                f"  <li><strong>{_html.escape(heading)}.</strong> " f"{_html.escape(sentence)}</li>"
            )
        parts.append("</ul>")
    parts.append("</aside>")
    return "".join(parts)


_BODY_FURNITURE_RE = re.compile(
    r'<aside\s+class="(?:author-card|related-posts|post-lead)\b[^"]*"[\s\S]*?</aside>'
    r'|<p\s+class="post-reviewed"\b[^>]*>[\s\S]*?</p>',
    re.IGNORECASE,
)


def _french_body(
    body_html: str,
    description: str,
    lead_aside: str,
    related_aside: str,
    body_md: str = "",
) -> str:
    today = _date_today()
    # Prefer a freshly-derived FR lead (using the FR body's H2 sentences)
    # over the extracted-from-EN-shell lead aside, since the EN takeaways
    # are still English even after label localisation.
    fr_takeaways = _derive_fr_takeaways(body_md) if body_md else []
    if fr_takeaways:
        lead = _build_fr_lead(description, fr_takeaways)
    else:
        lead = lead_aside or _french_lead_fallback(description)
    _strings = _lang_registry.load_strings(LANG_CODE)
    review_label = _strings.get("article.lastReviewedLabel", "Last reviewed ")
    review = (
        f'<p class="post-reviewed">{review_label}' f'<time datetime="{today}">{today}</time>.</p>'
    )
    # The translated source markdown may already contain post_enrich-injected
    # author-card / post-reviewed / lead-aside / related-posts blocks copied
    # from the EN scaffold; strip them so the localised versions emitted by
    # this function are the only ones on the page (otherwise WCAG2AAA fails
    # on duplicate `id="related-heading"`).
    body_html = _BODY_FURNITURE_RE.sub("", body_html)
    return lead + body_html + _french_author_card() + review + related_aside


def _swap_breadcrumb(html: str, slug: str, title: str) -> str:  # noqa: C901 — JSON-LD patch ladder
    """Patch the BreadcrumbList JSON-LD on the page to point at /fr/{slug}/
    and localize the labels (Home → Accueil, Articles → Articles).

    Walks every ``<script type="application/ld+json">`` block, parses the
    JSON content, and rewrites the one whose ``@type`` is ``BreadcrumbList``.
    Avoids brittle non-greedy regex over nested ``}`` characters.
    """

    def patch_breadcrumb(node: dict[str, object]) -> bool:
        items = node.get("itemListElement")
        if not isinstance(items, list):
            return False
        for item in items:
            if not isinstance(item, dict):
                continue
            pos = item.get("position")
            if pos == 1:
                item["name"] = "Accueil"
                item["item"] = f"{BASE}/"
            elif pos == 2:
                item["name"] = "Articles"
                item["item"] = f"{BASE}/{LANG_CODE}/"
            elif pos == 3:
                item["name"] = title
                item["item"] = f"{BASE}/{LANG_CODE}/{slug}/"
        return True

    def fix(m: re.Match[str]) -> str:
        raw = m.group(1)
        if '"BreadcrumbList"' not in raw:
            return m.group(0)
        try:
            data = _json.loads(raw)
        except _json.JSONDecodeError:
            return m.group(0)
        # Top-level may be a BreadcrumbList directly or an @graph wrapper.
        changed = False
        if isinstance(data, dict):
            if data.get("@type") == "BreadcrumbList":
                changed = patch_breadcrumb(data)
            graph = data.get("@graph")
            if isinstance(graph, list):
                for node in graph:
                    if (
                        isinstance(node, dict)
                        and node.get("@type") == "BreadcrumbList"
                        and patch_breadcrumb(node)
                    ):
                        changed = True
        if not changed:
            return m.group(0)
        return (
            '<script type="application/ld+json">'
            + _json.dumps(data, separators=(",", ":"), ensure_ascii=False)
            + "</script>"
        )

    return re.sub(
        r'<script type="application/ld\+json">([\s\S]+?)</script>',
        fix,
        html,
    )


_EN_URL_PATTERN_TMPL = r"(https?://sebastienrousseau\.com)?/(?P<slug>{slugs})(/(?:index\.html)?)?"


def _build_en_url_rewriter() -> re.Pattern[str]:
    """Build a single anchored regex matching any internal EN slug
    that has a recorded FR counterpart. Used to rewrite EN URLs to
    /fr/<fr-slug>/ inside French page bodies."""
    slugs = "|".join(re.escape(s) for s in sorted(EN_TO_FR.keys(), key=len, reverse=True))
    if not slugs:
        return re.compile(r"$^")
    return re.compile(_EN_URL_PATTERN_TMPL.format(slugs=slugs))


_EN_URL_RE_CACHE: dict[str, re.Pattern[str]] = {}


def _en_url_re() -> re.Pattern[str]:
    """Lang-aware cache of the EN-URL regex. Each call returns the
    regex built against the *current* EN_TO_FR map (rebound per lang
    by ``_bind_lang``)."""
    key = LANG_CODE
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
        lang_slug = fr_slug(en)
        tail = m.group(3) or ""
        return f"{origin}/{LANG_CODE}/{lang_slug}{tail}"

    return _en_url_re().sub(repl, html_fragment)


def _build_fr_title_map() -> dict[str, str]:
    """Walk every ``_posts/fr/*.md`` and return ``en_slug -> FR title``."""
    out: dict[str, str] = {}
    if not SRC.is_dir():
        return out
    for md in SRC.glob("*.md"):
        if not _DATED_RE.match(md.stem):
            continue
        en = FR_TO_EN.get(md.stem, md.stem)
        fm, _ = parse_frontmatter(md.read_text(encoding="utf-8"))
        title = fm.get("title")
        if title:
            out[en] = title
    return out


_FR_TITLE_MAP: dict[str, str] = {}


def _ensure_fr_title_map() -> dict[str, str]:
    """Lazy-init the EN→FR title map."""
    if not _FR_TITLE_MAP:
        _FR_TITLE_MAP.update(_build_fr_title_map())
    return _FR_TITLE_MAP


def _build_fr_description_map() -> dict[str, str]:
    """Walk every ``_posts/fr/*.md`` and return ``en_slug -> FR description``."""
    out: dict[str, str] = {}
    if not SRC.is_dir():
        return out
    for md in SRC.glob("*.md"):
        if not _DATED_RE.match(md.stem):
            continue
        en = FR_TO_EN.get(md.stem, md.stem)
        fm, _ = parse_frontmatter(md.read_text(encoding="utf-8"))
        desc = fm.get("description")
        if desc:
            out[en] = desc
    return out


_FR_DESCRIPTION_MAP: dict[str, str] = {}


def _ensure_fr_description_map() -> dict[str, str]:
    if not _FR_DESCRIPTION_MAP:
        _FR_DESCRIPTION_MAP.update(_build_fr_description_map())
    return _FR_DESCRIPTION_MAP


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
    if not SRC.is_dir():
        return out
    for md in SRC.glob("*.md"):
        if not _DATED_RE.match(md.stem):
            continue
        en = FR_TO_EN.get(md.stem, md.stem)
        fm, _ = parse_frontmatter(md.read_text(encoding="utf-8"))
        excerpt = fm.get("excerpt") or fm.get("subtitle") or fm.get("description")
        if excerpt:
            out[en] = excerpt
    return out


_FR_EXCERPT_MAP: dict[str, str] = {}


def _ensure_fr_excerpt_map() -> dict[str, str]:
    if not _FR_EXCERPT_MAP:
        _FR_EXCERPT_MAP.update(_build_fr_excerpt_map())
    return _FR_EXCERPT_MAP


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
    if not SRC.is_dir():
        return out
    for md in SRC.glob("*.md"):
        if not _DATED_RE.match(md.stem):
            continue
        en = FR_TO_EN.get(md.stem, md.stem)
        fm, _ = parse_frontmatter(md.read_text(encoding="utf-8"))
        tags = fm.get("tags") or ""
        eyebrow = _eyebrow_from_locale_tags(tags)
        if eyebrow:
            out[en] = eyebrow
    return out


_FR_EYEBROW_MAP: dict[str, str] = {}


def _ensure_fr_eyebrow_map() -> dict[str, str]:
    if not _FR_EYEBROW_MAP:
        _FR_EYEBROW_MAP.update(_build_fr_eyebrow_map())
    return _FR_EYEBROW_MAP


_EN_DESC_TO_FR_RE_CACHE: re.Pattern[str] | None = None
_EN_DESC_TO_FR_MAP_CACHE: dict[str, str] | None = None


def _en_descs_to_fr() -> tuple[re.Pattern[str], dict[str, str]]:
    """Build a regex + map matching every EN article description verbatim
    (and HTML-escaped variants) so we can substitute the FR description
    on listing pages (tags, topics, papers, project pages, …)."""
    global _EN_DESC_TO_FR_RE_CACHE, _EN_DESC_TO_FR_MAP_CACHE
    if _EN_DESC_TO_FR_RE_CACHE is not None and _EN_DESC_TO_FR_MAP_CACHE is not None:
        return _EN_DESC_TO_FR_RE_CACHE, _EN_DESC_TO_FR_MAP_CACHE
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
        _EN_DESC_TO_FR_RE_CACHE = re.compile(r"$^")
        _EN_DESC_TO_FR_MAP_CACHE = {}
        return _EN_DESC_TO_FR_RE_CACHE, _EN_DESC_TO_FR_MAP_CACHE
    sorted_keys = sorted(mapping.keys(), key=len, reverse=True)
    _EN_DESC_TO_FR_RE_CACHE = re.compile("|".join(re.escape(k) for k in sorted_keys if k))
    _EN_DESC_TO_FR_MAP_CACHE = mapping
    return _EN_DESC_TO_FR_RE_CACHE, _EN_DESC_TO_FR_MAP_CACHE


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


_EN_TITLES_TO_FR_RE_CACHE: re.Pattern[str] | None = None


def _en_titles_to_fr_re() -> re.Pattern[str]:
    """Compile a regex matching any known EN article title verbatim,
    capturing the matched EN title so we can substitute the FR one.
    Also matches HTML-entity-escaped variants so we catch titles inside
    rendered HTML attributes (& → &amp;, ' → &#x27;, " → &quot;)."""
    global _EN_TITLES_TO_FR_RE_CACHE
    if _EN_TITLES_TO_FR_RE_CACHE is not None:
        return _EN_TITLES_TO_FR_RE_CACHE
    raw_titles: list[str] = []
    posts_dir = Path("_posts")
    for md in posts_dir.glob("2*.md"):
        text = md.read_text(encoding="utf-8")
        m = re.search(r'^title:\s*"((?:[^"\\]|\\.)*)"', text, re.MULTILINE)
        if m:
            raw_titles.append(m.group(1))
    if not raw_titles:
        _EN_TITLES_TO_FR_RE_CACHE = re.compile(r"$^")
        return _EN_TITLES_TO_FR_RE_CACHE
    variants: set[str] = set()
    for t in raw_titles:
        variants.add(t)
        variants.add(_html.escape(t, quote=True))
        variants.add(_html.escape(t, quote=False))
    sorted_variants = sorted(variants, key=len, reverse=True)
    pattern = "|".join(re.escape(v) for v in sorted_variants if v)
    _EN_TITLES_TO_FR_RE_CACHE = re.compile(pattern)
    return _EN_TITLES_TO_FR_RE_CACHE


_EN_TITLE_TO_FR_MAP_CACHE: dict[str, str] | None = None


def _en_title_to_fr_map() -> dict[str, str]:
    """Map every EN title variant (raw + HTML-entity escaped) to the
    FR title (and the same FR title encoded the same way)."""
    global _EN_TITLE_TO_FR_MAP_CACHE
    if _EN_TITLE_TO_FR_MAP_CACHE is not None:
        return _EN_TITLE_TO_FR_MAP_CACHE
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
    _EN_TITLE_TO_FR_MAP_CACHE = out
    return _EN_TITLE_TO_FR_MAP_CACHE


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


def rewrite_fr_link_titles(html: str) -> str:
    """Walk every ``<a href="/fr/<slug>/…">`` and overwrite the
    ``title="…"`` and ``aria-label="…"`` attributes with the matching
    FR title from the slug map. Inner anchor text is left untouched
    (the author may have chosen it deliberately as a citation or
    contextual label)."""
    fr_titles = _ensure_fr_title_map()

    def repl(m: re.Match[str]) -> str:
        before, slug, after = m.group(1), m.group(2), m.group(3)
        en = FR_TO_EN.get(slug)
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
        return f'<a{attrs} href="/{LANG_CODE}/{slug}/index.html">'

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
            + re.escape(LANG_CODE)
            + r'/([a-z0-9-]+)/(?:index\.html)?"'
            + r"|(?:https?://sebastienrousseau\.com)?/"
            + re.escape(LANG_CODE)
            + r"/([a-z0-9-]+)/(?:index\.html)?(?=[\s>]))",
            inner,
        )
        if not slug_m:
            return m.group(0)
        slug = slug_m.group(1) or slug_m.group(2)
        en = FR_TO_EN.get(slug)
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
        en = FR_TO_EN.get(fr_slug_str)
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


def _patch_blogposting_jsonld(  # noqa: C901 — schema patch passes
    html: str,
    *,
    title: str,
    description: str,
    keywords: str,
    url_fr: str,
    banner: str,
    banner_alt: str,
) -> str:
    """Walk every JSON-LD script block; for each BlogPosting node,
    rewrite headline / description / inLanguage / url / mainEntityOfPage /
    image / keywords / isPartOf so the FR page advertises itself as a
    French resource."""

    def patch_node(node: dict) -> bool:
        t = node.get("@type")
        if t != "BlogPosting":
            return False
        node["headline"] = title
        node["description"] = description
        node["inLanguage"] = LANG_CODE
        node["url"] = url_fr
        if keywords:
            node["keywords"] = keywords
        if banner:
            node["image"] = {
                "@type": "ImageObject",
                "url": banner,
                "width": "100vw",
                "height": "100vh",
                "caption": banner_alt or title,
            }
        mep = node.get("mainEntityOfPage")
        if isinstance(mep, dict):
            mep["@id"] = url_fr
        elif isinstance(mep, str):
            node["mainEntityOfPage"] = url_fr
        # isPartOf — point at the FR articles hub.
        ipo = node.get("isPartOf")
        if isinstance(ipo, dict):
            ipo["@id"] = "https://sebastienrousseau.com/fr/#blog"
            ipo["name"] = "Sebastien Rousseau — Articles (français)"
            ipo["url"] = "https://sebastienrousseau.com/fr/"
            ipo["inLanguage"] = LANG_CODE
        return True

    def fix(m: re.Match[str]) -> str:
        raw = m.group(1)
        if '"BlogPosting"' not in raw:
            return m.group(0)
        try:
            data = _json.loads(raw)
        except _json.JSONDecodeError:
            return m.group(0)
        changed = False
        if isinstance(data, dict):
            if patch_node(data):
                changed = True
            graph = data.get("@graph")
            if isinstance(graph, list):
                for node in graph:
                    if isinstance(node, dict) and patch_node(node):
                        changed = True
        if not changed:
            return m.group(0)
        return (
            '<script type="application/ld+json">'
            + _json.dumps(data, separators=(",", ":"), ensure_ascii=False)
            + "</script>"
        )

    return re.sub(
        r'<script type="application/ld\+json">([\s\S]+?)</script>',
        fix,
        html,
    )


def _localize_inlanguage_globally(html: str, lang: str = "fr") -> str:
    """Walk EVERY JSON-LD block on the page and set ``inLanguage`` to
    ``lang`` on every node that has the field.

    The targeted patchers (BlogPosting, AboutPage, ContactPage, …) only
    touch nodes they recognise — the secondary blocks that ship
    ``WebSite`` and ``ProfilePage`` graphs from the EN layout get left
    behind, so the FR page ends up advertising ``inLanguage="en-GB"``
    on its WebSite node even though everything else is French. This
    is what ``scripts/test_jsonld_localized.py`` was built to catch.
    """

    def walk(node: object) -> None:
        if isinstance(node, dict):
            if "inLanguage" in node and isinstance(node["inLanguage"], str):
                node["inLanguage"] = lang
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    def fix(m: re.Match[str]) -> str:
        raw = m.group(1)
        if "inLanguage" not in raw:
            return m.group(0)
        try:
            data = _json.loads(raw)
        except _json.JSONDecodeError:
            return m.group(0)
        walk(data)
        return (
            '<script type="application/ld+json">'
            + _json.dumps(data, separators=(",", ":"), ensure_ascii=False)
            + "</script>"
        )

    # Quote-tolerant match — the minifier sometimes strips the quotes
    # around the type attribute (`<script type=application/ld+json>`).
    return re.sub(
        r'<script\b[^>]*type=["\']?application/ld\+json["\']?[^>]*>([\s\S]+?)</script>',
        fix,
        html,
    )


def render_translation(slug: str, fm: dict[str, str], body_md: str) -> str | None:
    """Render one French page from English shell + French frontmatter + body.

    Returns the patched HTML, or None if the English shell is missing.
    """
    shell_src = PUBLIC / slug / "index.html"
    if not shell_src.is_file():
        print(f"build_translations: skip {slug} — English shell missing at {shell_src}")
        return None
    shell = shell_src.read_text(encoding="utf-8")
    body_html = render_markdown(body_md)

    title = fm.get("title", slug)
    description = fm.get("description", "")
    keywords = fm.get("keywords", "")
    subtitle = fm.get("subtitle", description)
    page_title = f"{title} — Sebastien Rousseau"
    slug_fr = fr_slug(slug)
    url_fr = f"{BASE}/{LANG_CODE}/{slug_fr}/"

    # html lang
    shell = _set_html_lang(shell)
    # head meta
    shell = _TITLE_RE.sub(f"<title>{_html.escape(page_title)}</title>", shell, count=1)
    shell = _DESC_META_RE.sub(rf"\g<1>{_html.escape(description, quote=True)}\g<2>", shell, count=1)
    if keywords:
        shell = _KW_META_RE.sub(rf"\g<1>{_html.escape(keywords, quote=True)}\g<2>", shell, count=1)
    shell = _OG_TITLE_RE.sub(rf"\g<1>{_html.escape(page_title, quote=True)}\g<2>", shell, count=1)
    shell = _OG_DESC_RE.sub(rf"\g<1>{_html.escape(description, quote=True)}\g<2>", shell, count=1)
    shell = _OG_URL_RE.sub(rf"\g<1>{url_fr}\g<2>", shell, count=1)
    shell = _OG_LOCALE_RE.sub(rf"\g<1>{LANG_LOCALE}\g<2>", shell, count=1)
    shell = _TW_TITLE_RE.sub(rf"\g<1>{_html.escape(page_title, quote=True)}\g<2>", shell, count=1)
    shell = _TW_DESC_RE.sub(rf"\g<1>{_html.escape(description, quote=True)}\g<2>", shell, count=1)
    shell = _CANONICAL_RE.sub(rf"\g<1>{url_fr}\g<2>", shell, count=1)

    # hero H1 + subtitle
    shell = _HERO_RE.sub(
        rf"\g<1>{_html.escape(title)}\g<2>{_html.escape(subtitle)}\g<3>",
        shell,
        count=1,
    )

    # Extract reusable structural blocks from the English shell so the
    # French page mirrors the same layout (lead aside + related-posts grid).
    # Rewrite any EN cross-links to their FR counterparts so the page stays
    # inside /fr/ when readers click related-reading links.
    lead_aside, related_aside = _extract_shell_blocks(shell)
    lead_aside = _localise_post_lead(lead_aside, description)
    lead_aside = rewrite_en_urls(lead_aside)
    related_aside = rewrite_en_urls(related_aside)
    related_aside = rewrite_related_card_titles(related_aside)
    body_html = rewrite_en_urls(body_html)
    # main body — built fresh in French (lead + body + author-card + reviewed + related).
    # body_md is passed so we can re-derive the takeaways from the FR H2s.
    fr_body = _french_body(body_html, description, lead_aside, related_aside, body_md=body_md)

    def replace_main(m: re.Match[str]) -> str:
        return m.group(1) + fr_body + m.group(3)

    shell = _MAIN_BODY_RE.sub(replace_main, shell, count=1)

    # EN title/description substitutions FIRST — before chrome runs
    # localize_en_dates() which would otherwise break verbatim matches.
    shell = rewrite_en_titles_in_text(shell)
    shell = rewrite_en_descs_in_text(shell)

    # Chrome translation — nav, footer, search palette, social labels, etc.
    shell = translate_chrome(shell)

    # Rewrite inline-link title="…" and aria-label="…" attributes on every
    # <a> pointing to a /fr/<slug>/ URL so hover-tooltips advertise the
    # French title (visible link text is left alone — author choice).
    shell = rewrite_fr_link_titles(shell)
    shell = rewrite_newsroom_card_titles(shell)

    # JSON-LD BlogPosting tweaks — parse + mutate + serialise so we can
    # cross nested objects (regex can't see past `}` inside the graph).
    banner = fm.get("banner", "")
    banner_alt = fm.get("banner_alt", "")
    shell = _patch_blogposting_jsonld(
        shell,
        title=title,
        description=description,
        keywords=keywords,
        url_fr=url_fr,
        banner=banner,
        banner_alt=banner_alt,
    )

    # Localise every remaining inLanguage in JSON-LD blocks (WebSite,
    # ProfilePage, and any other secondary graph that the targeted
    # patchers above don't touch). Phase 2 SEO gate enforces this.
    shell = _localize_inlanguage_globally(shell, LANG_CODE)

    # Breadcrumb final segment
    shell = _swap_breadcrumb(shell, slug_fr, title)

    # Localised feed links — point French pages at the FR feed shadows.
    # Covers absolute, root-relative, and any prod/preview host variants
    # Shokunin may have emitted into the shell.
    shell = re.sub(
        r'href="(?:https?://[^/"]+)?/atom\.xml"',
        f'href="/{LANG_CODE}/atom.xml"',
        shell,
    )
    shell = re.sub(
        r'href="(?:https?://[^/"]+)?/rss\.xml"',
        f'href="/{LANG_CODE}/rss.xml"',
        shell,
    )

    return shell


# ---------------------------------------------------------------------------
# Hub: /fr/index.html
# ---------------------------------------------------------------------------

_NEWSROOM_RE = re.compile(r'<section class="newsroom">[\s\S]*?</section>', re.IGNORECASE)
_LDJSON_RE = re.compile(r'<script type="application/ld\+json">[\s\S]*?</script>', re.IGNORECASE)


def render_articles_hub(entries: list[dict[str, str]]) -> str | None:
    """Articles listing — French equivalent of /articles/. Forks the
    rendered /articles/ page as shell and writes to /fr/articles/."""
    shell_src = PUBLIC / "articles" / "index.html"
    if not shell_src.is_file():
        return None
    shell = shell_src.read_text(encoding="utf-8")

    # Strip the English ItemList (we emit a French one scoped to /fr/).
    for block in _LDJSON_RE.findall(shell):
        if '"ItemList"' in block or '"itemListElement"' in block:
            shell = shell.replace(block, "", 1)

    # Mirror /articles/ structure exactly: FEATURED block (newest)
    # + ARCHIVE grid (the rest). Same markup classes so the CSS
    # styling carries across both languages identically.
    if not entries:
        return None

    featured = entries[0]
    archive = entries[1:]
    feat_url = f"/{LANG_CODE}/{featured['slug']}/index.html"
    _hub_strings: dict[str, dict[str, str]] = {
        "fr": {
            "featuredKicker": "À LA UNE",
            "featuredHeading": "Article récent",
            "archiveKicker": "ARCHIVES",
            "archiveHeading": "Tous les articles",
            "readFull": "Lire l'article complet",
            "desc": "Sélection d'articles traduits manuellement en français.",
            "heroH1": "Articles",
            "heroSub": "Articles sur l'IA, la cryptographie post-quantique, ISO 20022 et l'avenir des paiements.",
        },
        "de": {
            "featuredKicker": "AKTUELL",
            "featuredHeading": "Neuester Artikel",
            "archiveKicker": "ARCHIV",
            "archiveHeading": "Alle Artikel",
            "readFull": "Vollständigen Artikel lesen",
            "desc": "Eine Auswahl manuell ins Deutsche übersetzter Artikel.",
            "heroH1": "Artikel",
            "heroSub": "Artikel über KI, Post-Quanten-Kryptografie, ISO 20022 und die Zukunft des Zahlungsverkehrs.",
        },
    }
    _h = _hub_strings.get(LANG_CODE, _hub_strings["fr"])
    feat_block = (
        f'<header class="newsroom-section-head"><p class="newsroom-kicker">{_h["featuredKicker"]}</p>'
        f'<h2>{_h["featuredHeading"]}</h2></header>'
        '<article class="newsroom-featured">'
        f'<a class="newsroom-featured-media" href="{feat_url}" title="{_html.escape(featured["title"], quote=True)}">'
        f'<img alt="{_html.escape(featured["banner_alt"], quote=True)}" '
        f'src="{featured["banner"]}" loading="eager" fetchpriority="high" '
        'decoding="async" width="800" height="800" />'
        '</a>'
        '<div class="newsroom-featured-body">'
        f'<h3><a href="{feat_url}" title="{_html.escape(featured["title"], quote=True)}">{_html.escape(featured["title"])}</a></h3>'
        f'<p>{_html.escape(featured["description"])}</p>'
        f'<p><a class="pill ghost" href="{feat_url}" title="{_html.escape(featured["title"], quote=True)}">{_h["readFull"]}</a></p>'
        '</div>'
        '</article>'
    )

    cards: list[str] = []
    for e in archive:
        url = f"/{LANG_CODE}/{e['slug']}/index.html"
        cards.append(
            '<article class="newsroom-card">'
            f'<a class="newsroom-card-media" href="{url}" title="{_html.escape(e["title"], quote=True)}">'
            f'<img alt="{_html.escape(e["banner_alt"], quote=True)}" src="{e["banner"]}" loading="lazy" decoding="async" width="600" height="600" />'
            '</a>'
            '<div class="newsroom-card-body">'
            f'<h3><a href="{url}" title="{_html.escape(e["title"], quote=True)}">{_html.escape(e["title"])}</a></h3>'
            f'<p class="newsroom-meta"><time datetime="{e["slug"][:10]}">{e["slug"][:10]}</time> · Sebastien Rousseau</p>'
            f'<p class="newsroom-excerpt">{_html.escape(e["description"])}</p>'
            '</div>'
            '</article>'
        )

    archive_block = (
        (
            f'<header class="newsroom-section-head"><p class="newsroom-kicker">{_h["archiveKicker"]}</p>'
            f'<h2>{_h["archiveHeading"]}</h2></header>'
            '<div class="newsroom-grid">' + "".join(cards) + "</div>"
        )
        if cards
        else ""
    )

    body = '<section class="newsroom">' + feat_block + archive_block + "</section>"
    shell = _NEWSROOM_RE.sub(body, shell, count=1)
    # Localise hero H1 + subtitle on the articles hub.
    shell = _HERO_RE.sub(
        rf'\g<1>{_html.escape(_h["heroH1"])}\g<2>{_html.escape(_h["heroSub"])}\g<3>',
        shell,
        count=1,
    )
    shell = _set_html_lang(shell)
    _articles_hub_titles = {
        "fr": "Articles en français — Sebastien Rousseau",
        "de": "Artikel auf Deutsch — Sebastien Rousseau",
    }
    title = _articles_hub_titles.get(LANG_CODE, _articles_hub_titles["fr"])
    desc = _h["desc"]
    shell = _TITLE_RE.sub(f"<title>{_html.escape(title)}</title>", shell, count=1)
    shell = _DESC_META_RE.sub(rf"\g<1>{_html.escape(desc, quote=True)}\g<2>", shell, count=1)
    shell = _OG_TITLE_RE.sub(rf"\g<1>{_html.escape(title, quote=True)}\g<2>", shell, count=1)
    shell = _OG_DESC_RE.sub(rf"\g<1>{_html.escape(desc, quote=True)}\g<2>", shell, count=1)
    _articles_slug_lang = STATIC_SLUG_FR.get("articles", "articles")
    _hub_url = f"https://sebastienrousseau.com/{LANG_CODE}/{_articles_slug_lang}/"
    shell = _OG_URL_RE.sub(rf"\g<1>{_hub_url}\g<2>", shell, count=1)
    shell = _OG_LOCALE_RE.sub(rf"\g<1>{LANG_LOCALE}\g<2>", shell, count=1)
    shell = _CANONICAL_RE.sub(rf"\g<1>{_hub_url}\g<2>", shell, count=1)
    shell = translate_chrome(shell)
    # Reciprocal hreflang for the language selector.
    shell = re.sub(
        r'<link rel="alternate"[^>]+hreflang="[^"]+"[^>]*/>',
        "",
        shell,
    )
    hreflang_block = (
        f'<link rel="alternate" hreflang="en" href="{BASE}/articles/" />'
        f'<link rel="alternate" hreflang="{LANG_CODE}" href="{BASE}/{LANG_CODE}/{_articles_slug_lang}/" />'
        f'<link rel="alternate" hreflang="x-default" href="{BASE}/articles/" />'
    )
    shell = shell.replace("</head>", hreflang_block + "</head>", 1)
    shell = _localize_inlanguage_globally(shell, LANG_CODE)
    return shell


# ---------------------------------------------------------------------------
# Home: /fr/index.html — forks the EN /index.html shell so the FR home
# carries the same hero / projects / quote / latest / experience sections.
# ---------------------------------------------------------------------------

# Per-section EN→FR substitutions for the home page body. Anchored to
# unique strings so they only fire on /fr/index.html. The regex pairs
# are applied AFTER chrome translation, so chrome strings + nav are
# already French by the time these run.
HOME_FR_PATCHES: list[tuple[str, str]] = list(_lang_registry.load_home_patches("fr"))

_HOME_FR_COMPILED: list[tuple[re.Pattern[str], str]] = [
    (re.compile(p), r) for p, r in HOME_FR_PATCHES
]


def render_home() -> str | None:  # noqa: C901 — orchestrates the FR home fork end-to-end
    """Fork ``public/index.html`` (the EN home) to produce
    ``public/fr/index.html`` so the FR landing page mirrors the EN
    structure (hero + projects + quote + paper + latest + experience).
    """
    shell_src = PUBLIC / "index.html"
    if not shell_src.is_file():
        return None
    shell = shell_src.read_text(encoding="utf-8")

    _home_titles = {
        "fr": "Sebastien Rousseau — IA, paiements et cryptographie quantique",
        "de": "Sebastien Rousseau — KI, Zahlungen und Quantenkryptografie",
    }
    _home_descs = {
        "fr": (
            "L'avenir de la banque par l'IA appliquée, les paiements et la sécurité "
            "résistante au quantique. Recherche, bibliothèques open source et "
            "conseil produit pour les services financiers."
        ),
        "de": (
            "Die Zukunft des Bankwesens durch angewandte KI, Zahlungen und "
            "quantensichere Sicherheit. Forschung, Open-Source-Bibliotheken und "
            "Produktberatung für Finanzdienstleistungen."
        ),
    }
    title = _home_titles.get(LANG_CODE, _home_titles["fr"])
    desc = _home_descs.get(LANG_CODE, _home_descs["fr"])
    url_fr = f"{BASE}/{LANG_CODE}/"

    shell = _set_html_lang(shell)
    shell = _TITLE_RE.sub(f"<title>{_html.escape(title)}</title>", shell, count=1)
    shell = _DESC_META_RE.sub(rf"\g<1>{_html.escape(desc, quote=True)}\g<2>", shell, count=1)
    shell = _OG_TITLE_RE.sub(rf"\g<1>{_html.escape(title, quote=True)}\g<2>", shell, count=1)
    shell = _OG_DESC_RE.sub(rf"\g<1>{_html.escape(desc, quote=True)}\g<2>", shell, count=1)
    shell = _OG_URL_RE.sub(rf"\g<1>{url_fr}\g<2>", shell, count=1)
    shell = _OG_LOCALE_RE.sub(rf"\g<1>{LANG_LOCALE}\g<2>", shell, count=1)
    shell = _TW_TITLE_RE.sub(rf"\g<1>{_html.escape(title, quote=True)}\g<2>", shell, count=1)
    shell = _TW_DESC_RE.sub(rf"\g<1>{_html.escape(desc, quote=True)}\g<2>", shell, count=1)
    shell = _CANONICAL_RE.sub(rf"\g<1>{url_fr}\g<2>", shell, count=1)

    # Rewrite article URLs (EN → FR) + ensure all internal links keep visitor in /fr/.
    shell = rewrite_en_urls(shell)
    shell = rewrite_en_titles_in_text(shell)
    shell = rewrite_en_descs_in_text(shell)

    # Apply chrome (nav, footer, search, aria, language selector, dates).
    shell = translate_chrome(shell)

    # Per-section body patches.
    for pat, repl in _HOME_FR_COMPILED:
        shell = pat.sub(repl, shell)

    # Card titles + tooltips for any article link.
    shell = rewrite_fr_link_titles(shell)
    shell = rewrite_newsroom_card_titles(shell)

    # Localise feed links.
    shell = re.sub(
        r'href="(?:https?://[^/"]+)?/atom\.xml"',
        f'href="/{LANG_CODE}/atom.xml"',
        shell,
    )
    shell = re.sub(
        r'href="(?:https?://[^/"]+)?/rss\.xml"',
        f'href="/{LANG_CODE}/rss.xml"',
        shell,
    )

    # Patch JSON-LD WebSite / Person / breadcrumb on the home page.
    def patch_jsonld(m: re.Match[str]) -> str:  # noqa: C901
        raw = m.group(1)
        try:
            data = _json.loads(raw)
        except _json.JSONDecodeError:
            return m.group(0)
        changed = False

        def patch_node(node: dict) -> bool:
            t = node.get("@type")
            local = False
            if t == "WebSite":
                if "url" in node:
                    node["url"] = url_fr
                    local = True
                if "name" in node:
                    node["name"] = title
                    local = True
                if "description" in node:
                    node["description"] = desc
                    local = True
                if "inLanguage" in node:
                    node["inLanguage"] = LANG_CODE
                    local = True
            if t == "WebPage":
                if "url" in node:
                    node["url"] = url_fr
                    local = True
                if "name" in node:
                    node["name"] = title
                    local = True
                if "description" in node:
                    node["description"] = desc
                    local = True
                if "inLanguage" in node:
                    node["inLanguage"] = LANG_CODE
                    local = True
            return local

        if isinstance(data, dict):
            if patch_node(data):
                changed = True
            graph = data.get("@graph")
            if isinstance(graph, list):
                for node in graph:
                    if isinstance(node, dict) and patch_node(node):
                        changed = True
        if not changed:
            return m.group(0)
        return (
            '<script type="application/ld+json">'
            + _json.dumps(data, separators=(",", ":"), ensure_ascii=False)
            + "</script>"
        )

    shell = re.sub(
        r'<script type="application/ld\+json">([\s\S]+?)</script>',
        patch_jsonld,
        shell,
    )

    # Reciprocal hreflang so the language selector finds the EN home.
    shell = re.sub(
        r'<link rel="alternate"[^>]+hreflang="[^"]+"[^>]*/>',
        "",
        shell,
    )
    hreflang_block = (
        f'<link rel="alternate" hreflang="en" href="{BASE}/" />'
        f'<link rel="alternate" hreflang="{LANG_CODE}" href="{url_fr}" />'
        f'<link rel="alternate" hreflang="x-default" href="{BASE}/" />'
    )
    shell = shell.replace("</head>", hreflang_block + "</head>", 1)
    shell = _localize_inlanguage_globally(shell, LANG_CODE)

    return shell


# ---------------------------------------------------------------------------
# Static-page translations (about, papers, projects, topics, tags, …)
# ---------------------------------------------------------------------------

# Static pages we mirror under /fr/. Each EN slug maps to its FR title +
# meta-description override. The body of these pages is mostly chrome
# (cards, lists generated by SSG from frontmatter); CHROME_PATCHES carries
# every nav / footer / aria-label translation. For pages with prose
# content (about, contact, privacy, terms, …) we additionally swap
# specific English strings via STATIC_BODY_PATCHES below.
STATIC_PAGES_FR: dict[str, dict[str, str]] = _lang_registry.load_static_pages("fr")

# Body-string patches applied to every FR static page. These are
# additional English phrases that appear in rendered page bodies and
# need localising. They're idempotent (no-op if the string is absent).
# Per-page French <main> body replacements. The EN body inside the
# outer ``<div class="wrap">…</div>`` is swapped wholesale on the FR
# mirror so the page reads as natively French. Pages not listed here
# fall back to the lighter STATIC_BODY_PATCHES regex pass.
STATIC_BODIES_FR: dict[str, str] = dict(_lang_registry.load_static_bodies("fr"))


STATIC_BODY_PATCHES: list[tuple[str, str]] = list(_lang_registry.load_static_patches("fr"))

_STATIC_BODY_COMPILED: list[tuple[re.Pattern[str], str]] = [
    (re.compile(p), r) for p, r in STATIC_BODY_PATCHES
]


_STATIC_WRAP_RE = re.compile(
    r'(<main\b[^>]*>\s*<div class="wrap[^"]*"[^>]*>)([\s\S]*?)(</div>\s*</main>)',
    re.IGNORECASE,
)


def _replace_static_main_body(html: str, fr_body: str) -> str:
    """Swap the inner content of ``<main><div class="wrap">…</div></main>``
    for a curated FR body. Falls back unchanged if the structure doesn't
    match (e.g. layouts that use a different wrapper)."""

    def repl(m: re.Match[str]) -> str:
        return m.group(1) + fr_body + m.group(3)

    return _STATIC_WRAP_RE.sub(repl, html, count=1)


def render_static_translation(slug: str) -> str | None:  # noqa: C901 — per-page pipeline
    """Fork the rendered EN page at ``public/{slug}/index.html``,
    translate chrome + body text, patch meta tags, swap canonical/og to
    point at ``/fr/{slug}/``, then return the HTML.
    """
    cfg = STATIC_PAGES_FR.get(slug)
    if cfg is None:
        return None
    shell_src = PUBLIC / slug / "index.html"
    if not shell_src.is_file():
        return None
    shell = shell_src.read_text(encoding="utf-8")

    title = cfg["title"]
    description = cfg["description"]
    subtitle = cfg.get("subtitle", description)
    keywords = cfg.get("keywords", "")
    fr_slug_str = STATIC_SLUG_FR.get(slug, slug)
    url_fr = f"{BASE}/{LANG_CODE}/{fr_slug_str}/"

    shell = _set_html_lang(shell)
    shell = _TITLE_RE.sub(f"<title>{_html.escape(title)}</title>", shell, count=1)
    shell = _DESC_META_RE.sub(rf"\g<1>{_html.escape(description, quote=True)}\g<2>", shell, count=1)
    if keywords:
        shell = _KW_META_RE.sub(rf"\g<1>{_html.escape(keywords, quote=True)}\g<2>", shell, count=1)
    shell = _OG_TITLE_RE.sub(rf"\g<1>{_html.escape(title, quote=True)}\g<2>", shell, count=1)
    shell = _OG_DESC_RE.sub(rf"\g<1>{_html.escape(description, quote=True)}\g<2>", shell, count=1)
    shell = _OG_URL_RE.sub(rf"\g<1>{url_fr}\g<2>", shell, count=1)
    shell = _OG_LOCALE_RE.sub(rf"\g<1>{LANG_LOCALE}\g<2>", shell, count=1)
    shell = _TW_TITLE_RE.sub(rf"\g<1>{_html.escape(title, quote=True)}\g<2>", shell, count=1)
    shell = _TW_DESC_RE.sub(rf"\g<1>{_html.escape(description, quote=True)}\g<2>", shell, count=1)
    shell = _CANONICAL_RE.sub(rf"\g<1>{url_fr}\g<2>", shell, count=1)
    # Hero subtitle (<p class="sub">…</p>) is per-page — replace it.
    shell = re.sub(
        r'<p class="sub">[^<]*</p>',
        f'<p class="sub">{_html.escape(subtitle)}</p>',
        shell,
        count=1,
    )

    # Rewrite EN article URLs inside the body to FR counterparts.
    shell = rewrite_en_urls(shell)

    # Swap the EN <main> body for the curated FR body when one is
    # provided. Falls through to STATIC_BODY_PATCHES (light text-swap)
    # for pages without a curated translation.
    fr_body = STATIC_BODIES_FR.get(slug)
    if fr_body:
        shell = _replace_static_main_body(shell, fr_body)

    # EN title + description substitutions FIRST — before chrome runs
    # localize_en_dates() (which would otherwise rewrite "August 2026" →
    # "août 2026" inside an EN description and break the verbatim match).
    shell = rewrite_en_titles_in_text(shell)
    shell = rewrite_en_descs_in_text(shell)

    # Localise chrome (nav / footer / search / aria) + body text.
    shell = translate_chrome(shell)
    for pat, repl in _STATIC_BODY_COMPILED:
        shell = pat.sub(repl, shell)

    # Rewrite article-card titles + tooltips on listing pages
    # (papers, projects, tags, topic hub, …) to the FR title.
    shell = rewrite_fr_link_titles(shell)
    shell = rewrite_newsroom_card_titles(shell)

    # Localise feed links.
    shell = re.sub(
        r'href="(?:https?://[^/"]+)?/atom\.xml"',
        f'href="/{LANG_CODE}/atom.xml"',
        shell,
    )
    shell = re.sub(
        r'href="(?:https?://[^/"]+)?/rss\.xml"',
        f'href="/{LANG_CODE}/rss.xml"',
        shell,
    )

    # Patch the WebPage / WebSite JSON-LD's @id, url, name, description.
    def patch_jsonld(m: re.Match[str]) -> str:  # noqa: C901
        raw = m.group(1)
        try:
            data = _json.loads(raw)
        except _json.JSONDecodeError:
            return m.group(0)
        changed = False

        def patch_node(node: dict) -> bool:
            local = False
            t = node.get("@type")
            if t in ("WebPage", "AboutPage", "ProfilePage", "ContactPage", "CollectionPage"):
                if "name" in node:
                    node["name"] = title
                    local = True
                if "description" in node:
                    node["description"] = description
                    local = True
                if "url" in node:
                    node["url"] = url_fr
                    local = True
                if "inLanguage" in node:
                    node["inLanguage"] = LANG_CODE
                    local = True
            if t == "BreadcrumbList":
                items = node.get("itemListElement", [])
                for item in items:
                    if not isinstance(item, dict):
                        continue
                    pos = item.get("position")
                    if pos == 1:
                        item["name"] = "Accueil"
                        item["item"] = f"{BASE}/"
                        local = True
                    elif pos == 2:
                        item["name"] = title.split(" — ")[0]
                        item["item"] = url_fr
                        local = True
            return local

        if isinstance(data, dict):
            if patch_node(data):
                changed = True
            graph = data.get("@graph")
            if isinstance(graph, list):
                for node in graph:
                    if isinstance(node, dict) and patch_node(node):
                        changed = True
        if not changed:
            return m.group(0)
        return (
            '<script type="application/ld+json">'
            + _json.dumps(data, separators=(",", ":"), ensure_ascii=False)
            + "</script>"
        )

    shell = re.sub(
        r'<script type="application/ld\+json">([\s\S]+?)</script>',
        patch_jsonld,
        shell,
    )

    # Reciprocal hreflang — strip stale links and emit fresh ones so the
    # language selector's JS resolves 🇬🇧 English to the EN counterpart.
    # Must run AFTER translate_chrome (which calls rewrite_static_links
    # and would rewrite an EN absolute URL → /fr/<slug>/).
    shell = re.sub(
        r'<link rel="alternate"[^>]+hreflang="[^"]+"[^>]*/>',
        "",
        shell,
    )
    en_url = f"{BASE}/{slug}/"
    hreflang_block = (
        f'<link rel="alternate" hreflang="en" href="{en_url}" />'
        f'<link rel="alternate" hreflang="{LANG_CODE}" href="{url_fr}" />'
        f'<link rel="alternate" hreflang="x-default" href="{en_url}" />'
    )
    shell = shell.replace("</head>", hreflang_block + "</head>", 1)
    shell = _localize_inlanguage_globally(shell, LANG_CODE)

    return shell


def write_static_translations() -> int:
    """Render and write every FR static page. Returns count written."""
    n = 0
    for slug in STATIC_PAGES_FR:
        page = render_static_translation(slug)
        if page is None:
            print(f"build_translations: skip static '{slug}' — EN shell missing")
            continue
        fr_slug_str = STATIC_SLUG_FR.get(slug, slug)
        dst = OUT / fr_slug_str / "index.html"
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(page, encoding="utf-8")
        n += 1

    # Topic sub-pages — clone each /topics/<topic>/ as /<lang>/<topics_slug>/<topic>/.
    # build_topics.py emits the EN versions before us; we fork + translate.
    topics_dir = PUBLIC / "topics"
    if topics_dir.is_dir():
        topics_slug_lang = STATIC_SLUG_FR.get("topics", "topics")
        for topic_dir in sorted(topics_dir.iterdir()):
            if not topic_dir.is_dir():
                continue
            src = topic_dir / "index.html"
            if not src.is_file():
                continue
            page = _render_topic_subpage_fr(topic_dir.name, src.read_text(encoding="utf-8"))
            dst = OUT / topics_slug_lang / topic_dir.name / "index.html"
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(page, encoding="utf-8")
            n += 1

    return n


# Per-topic French title + lede. Mirrors scripts/build_topics.py:TOPICS.
TOPIC_FR_LABELS: dict[str, dict[str, str]] = _lang_registry.load_topics("fr")


def _render_topic_subpage_fr(topic_slug: str, shell: str) -> str:  # noqa: C901 — topic-page chrome patches
    """Fork an EN /topics/<slug>/ page into /fr/sujets/<slug>/."""
    cfg = TOPIC_FR_LABELS.get(
        topic_slug,
        {
            "title": topic_slug.replace("-", " ").title(),
            "lede": "",
        },
    )
    title = cfg["title"]
    lede = cfg["lede"]
    page_title = f"{title} — Sebastien Rousseau"
    topics_slug_lang = STATIC_SLUG_FR.get("topics", "topics")
    url_fr = f"{BASE}/{LANG_CODE}/{topics_slug_lang}/{topic_slug}/"

    shell = _set_html_lang(shell)
    shell = _TITLE_RE.sub(f"<title>{_html.escape(page_title)}</title>", shell, count=1)
    if lede:
        shell = _DESC_META_RE.sub(rf"\g<1>{_html.escape(lede, quote=True)}\g<2>", shell, count=1)
        shell = _OG_DESC_RE.sub(rf"\g<1>{_html.escape(lede, quote=True)}\g<2>", shell, count=1)
    shell = _OG_TITLE_RE.sub(rf"\g<1>{_html.escape(page_title, quote=True)}\g<2>", shell, count=1)
    shell = _OG_URL_RE.sub(rf"\g<1>{url_fr}\g<2>", shell, count=1)
    shell = _OG_LOCALE_RE.sub(rf"\g<1>{LANG_LOCALE}\g<2>", shell, count=1)
    shell = _CANONICAL_RE.sub(rf"\g<1>{url_fr}\g<2>", shell, count=1)
    shell = _TW_TITLE_RE.sub(rf"\g<1>{_html.escape(page_title, quote=True)}\g<2>", shell, count=1)
    if lede:
        shell = _TW_DESC_RE.sub(rf"\g<1>{_html.escape(lede, quote=True)}\g<2>", shell, count=1)

    # Rewrite article cards (EN slugs → FR slugs).
    shell = rewrite_en_urls(shell)

    # Translate the topic H1 + lede in the body if present.
    # Pattern from build_topics.py: <h1>{TITLE}</h1>...<p class="topic-lede">{LEDE}</p>
    shell = re.sub(
        r"<h1>[^<]+</h1>",
        f"<h1>{_html.escape(title)}</h1>",
        shell,
        count=1,
    )
    if lede:
        shell = re.sub(
            r'(<p class="topic-lede">)[^<]+(</p>)',
            rf"\g<1>{_html.escape(lede)}\g<2>",
            shell,
            count=1,
        )
    # Breadcrumb in body: "Home · Topics · Title" → "Accueil · Sujets · Titre"
    shell = re.sub(
        r'<nav aria-label="Breadcrumb" class="topic-breadcrumb">[\s\S]*?</nav>',
        f'<nav aria-label="Fil d\'Ariane" class="topic-breadcrumb">'
        f'<a href="/{LANG_CODE}/">Accueil</a> &middot; '
        f'<a href="/{LANG_CODE}/{STATIC_SLUG_FR.get("topics", "topics")}/index.html">Sujets</a> &middot; '
        f'<span>{_html.escape(title)}</span></nav>',
        shell,
        count=1,
    )
    # Topics-page lede on the hub
    shell = re.sub(
        r"Curated topic clusters[^<]+",
        "Clusters de sujets curated — choisissez un fil et suivez-le à travers l'archive.",
        shell,
    )
    shell = re.sub(
        r"PILLARS",
        "PILIERS",
        shell,
    )
    shell = re.sub(
        r">Topics</h1>",
        ">Sujets</h1>",
        shell,
    )
    shell = re.sub(
        r"PILLAR · TOPIC",
        "PILIER · SUJET",
        shell,
    )
    shell = re.sub(
        r"(\d+) article\(s\)",
        r"\1 article(s)",
        shell,
    )

    # Patch JSON-LD breadcrumb + URLs to point to /fr/topics/.
    def patch_jsonld(m: re.Match[str]) -> str:  # noqa: C901
        raw = m.group(1)
        try:
            data = _json.loads(raw)
        except _json.JSONDecodeError:
            return m.group(0)
        changed = False

        def patch_node(node: dict) -> bool:
            local = False
            t = node.get("@type")
            if t == "CollectionPage":
                if "name" in node:
                    node["name"] = title
                    local = True
                if "description" in node and lede:
                    node["description"] = lede
                    local = True
                if "url" in node:
                    node["url"] = url_fr
                    local = True
                if "inLanguage" in node:
                    node["inLanguage"] = LANG_CODE
                    local = True
            if t == "BreadcrumbList":
                for item in node.get("itemListElement", []):
                    if not isinstance(item, dict):
                        continue
                    pos = item.get("position")
                    if pos == 1:
                        item["name"] = "Accueil"
                        item["item"] = f"{BASE}/"
                        local = True
                    elif pos == 2:
                        item["name"] = "Sujets"
                        item["item"] = (
                            f"{BASE}/{LANG_CODE}/{STATIC_SLUG_FR.get('topics', 'topics')}/"
                        )
                        local = True
                    elif pos == 3:
                        item["name"] = title
                        item["item"] = url_fr
                        local = True
            return local

        if isinstance(data, dict):
            if patch_node(data):
                changed = True
            graph = data.get("@graph")
            if isinstance(graph, list):
                for node in graph:
                    if isinstance(node, dict) and patch_node(node):
                        changed = True
        if not changed:
            return m.group(0)
        return (
            '<script type="application/ld+json">'
            + _json.dumps(data, separators=(",", ":"), ensure_ascii=False)
            + "</script>"
        )

    shell = re.sub(
        r'<script type="application/ld\+json">([\s\S]+?)</script>',
        patch_jsonld,
        shell,
    )

    # EN title/description substitutions FIRST — before chrome runs
    # localize_en_dates() which would otherwise break verbatim matches.
    shell = rewrite_en_titles_in_text(shell)
    shell = rewrite_en_descs_in_text(shell)
    # Chrome localisation (includes localize_en_dates)
    shell = translate_chrome(shell)
    shell = rewrite_fr_link_titles(shell)
    shell = rewrite_newsroom_card_titles(shell)
    # Reciprocal hreflang
    shell = re.sub(
        r'<link rel="alternate"[^>]+hreflang="[^"]+"[^>]*/>',
        "",
        shell,
    )
    en_url = f"{BASE}/topics/{topic_slug}/"
    hreflang_block = (
        f'<link rel="alternate" hreflang="en" href="{en_url}" />'
        f'<link rel="alternate" hreflang="{LANG_CODE}" href="{url_fr}" />'
        f'<link rel="alternate" hreflang="x-default" href="{en_url}" />'
    )
    shell = shell.replace("</head>", hreflang_block + "</head>", 1)
    # Feed links
    shell = re.sub(
        r'href="(?:https?://[^/"]+)?/atom\.xml"',
        f'href="/{LANG_CODE}/atom.xml"',
        shell,
    )
    shell = re.sub(
        r'href="(?:https?://[^/"]+)?/rss\.xml"',
        f'href="/{LANG_CODE}/rss.xml"',
        shell,
    )
    shell = _localize_inlanguage_globally(shell, LANG_CODE)
    return shell


def _bind_lang(code: str) -> None:
    """Rebind every per-language module-level global to ``code``'s
    values. Called by ``main()`` before each render pass.

    Globals reassigned: LANG_CODE / LANG_BCP47 / LANG_LOCALE / SRC / OUT /
    EN_TO_FR / FR_TO_EN / I18N_FR / TAKEAWAY_LABELS_EN_TO_FR /
    STATIC_SLUG_FR / STATIC_PAGES_FR / TOPIC_FR_LABELS / HOME_FR_PATCHES /
    STATIC_BODIES_FR / STATIC_BODY_PATCHES / CHROME_PATCHES /
    _CHROME_PATCHES_COMPILED / _HOME_FR_COMPILED. (Names carry the
    legacy ``_FR`` suffix for diff minimality; semantically they hold
    the current ``code``'s data.)
    """
    global LANG_CODE, LANG_BCP47, LANG_LOCALE, SRC, OUT
    global EN_TO_FR, FR_TO_EN
    global I18N_FR, TAKEAWAY_LABELS_EN_TO_FR
    global STATIC_SLUG_FR, STATIC_PAGES_FR, TOPIC_FR_LABELS
    global HOME_FR_PATCHES, STATIC_BODIES_FR, STATIC_BODY_PATCHES
    global CHROME_PATCHES, _CHROME_PATCHES_COMPILED, _HOME_FR_COMPILED, _STATIC_BODY_COMPILED
    lang = next(lg for lg in _lang_registry.LANGUAGES if lg.code == code)
    LANG_CODE = code
    LANG_BCP47 = lang.bcp47
    LANG_LOCALE = lang.og_locale
    SRC = Path(f"_posts/{code}")
    OUT = PUBLIC / code
    slugs = _lang_registry.load_slugs(code)
    articles = slugs.get("articles", {})
    EN_TO_FR = dict(articles)
    FR_TO_EN = {v: k for k, v in articles.items()}
    I18N_FR = _lang_registry.load_labels(code)
    TAKEAWAY_LABELS_EN_TO_FR = _lang_registry.load_takeaway_labels(code)
    STATIC_SLUG_FR = slugs.get("static", {})
    STATIC_PAGES_FR = _lang_registry.load_static_pages(code)
    TOPIC_FR_LABELS = _lang_registry.load_topics(code)
    HOME_FR_PATCHES = list(_lang_registry.load_home_patches(code))
    STATIC_BODIES_FR = dict(_lang_registry.load_static_bodies(code))
    STATIC_BODY_PATCHES = list(_lang_registry.load_static_patches(code))
    CHROME_PATCHES = [
        *_lang_registry.build_chrome_patches(code),
        *_lang_registry.load_chrome_patches_inline(code),
    ]
    _CHROME_PATCHES_COMPILED = [(re.compile(p), r) for p, r in CHROME_PATCHES]
    _HOME_FR_COMPILED = [(re.compile(p), r) for p, r in HOME_FR_PATCHES]
    _STATIC_BODY_COMPILED = [(re.compile(p), r) for p, r in STATIC_BODY_PATCHES]
    # Clear every per-language lazy cache so the second pass doesn't
    # inherit the first language's title / description / excerpt /
    # eyebrow / regex tables.
    global _FR_TITLE_MAP, _FR_DESCRIPTION_MAP, _FR_EXCERPT_MAP, _FR_EYEBROW_MAP
    global _EN_DESC_TO_FR_RE_CACHE, _EN_DESC_TO_FR_MAP_CACHE
    global _EN_TITLES_TO_FR_RE_CACHE, _EN_TITLE_TO_FR_MAP_CACHE
    _FR_TITLE_MAP.clear()
    _FR_DESCRIPTION_MAP.clear()
    _FR_EXCERPT_MAP.clear()
    _FR_EYEBROW_MAP.clear()
    _EN_DESC_TO_FR_RE_CACHE = None
    _EN_DESC_TO_FR_MAP_CACHE = None
    _EN_TITLES_TO_FR_RE_CACHE = None
    _EN_TITLE_TO_FR_MAP_CACHE = None
    # Swap month-name map to the current language so localize_en_dates
    # emits the right month form (FR "novembre", DE "November", …).
    global _EN_MONTH_TO_FR
    _EN_MONTH_TO_FR = dict(_LANG_MONTHS.get(code, _LANG_MONTHS["fr"]))


def _render_one_lang(code: str) -> int:
    """Render every page for one language. Returns total page count."""
    _bind_lang(code)
    if not SRC.is_dir():
        print(f"build_translations: _posts/{code} not found — nothing to do for {code}")
        return 0
    entries: list[dict[str, str]] = []
    written = 0
    for md in sorted(SRC.glob("*.md")):
        if not _DATED_RE.match(md.stem):
            continue
        text = md.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        if not fm.get("title"):
            print(f"build_translations: skip {md.stem} — no title in frontmatter")
            continue
        # File stem may be either the EN slug (legacy) or the FR slug.
        # Resolve both directions so we can find the matching English shell.
        if md.stem in FR_TO_EN:
            en = FR_TO_EN[md.stem]
            slug_fr = md.stem
        else:
            en = md.stem
            slug_fr = fr_slug(md.stem)
        page = render_translation(en, fm, body)
        if page is None:
            continue
        dst = OUT / slug_fr / "index.html"
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(page, encoding="utf-8")
        entries.append(
            {
                "slug": slug_fr,
                "en_slug": en,
                "title": fm.get("title", ""),
                "description": fm.get("description", ""),
                "date": fm.get("date", ""),
                "keywords": fm.get("keywords", ""),
                "banner": fm.get(
                    "banner", "https://cloudcdn.pro/stocks/images/sebastien-rousseau.png"
                ),
                "banner_alt": fm.get("banner_alt", fm.get("title", "")),
            }
        )
        written += 1

    if entries:
        # Sort newest first to mirror the English /articles/ ordering.
        entries.sort(key=lambda e: e["slug"], reverse=True)
        # /fr/articles/ — the French articles listing (was /fr/index.html).
        articles_hub = render_articles_hub(entries)
        if articles_hub:
            articles_path = OUT / STATIC_SLUG_FR.get("articles", "articles") / "index.html"
            articles_path.parent.mkdir(parents=True, exist_ok=True)
            articles_path.write_text(articles_hub, encoding="utf-8")
            written += 1

    # /fr/index.html — the French home page, forked from the EN /index.html
    # so the structure (hero + projects + quote + paper + latest + experience)
    # is identical to / for visual parity.
    home = render_home()
    if home:
        (OUT / "index.html").write_text(home, encoding="utf-8")
        written += 1

    # Static-page mirrors (about, papers, projects, topics, tags,
    # contact, accessibility, privacy, terms, …) — keep FR visitors
    # inside /fr/ when they click any nav or footer link.
    static_written = write_static_translations()
    written += static_written

    # Per-language search index — visible text of every rendered page,
    # loaded by the Shokunin search palette when the visitor is in
    # /<code>/.
    search_entries = _build_fr_search_index()
    (OUT / "search-index.json").write_text(
        _json.dumps({"entries": search_entries}, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )

    print(
        f"build_translations[{code}]: wrote {written} page(s) "
        f"({len(entries)} translation(s) + hub + {static_written} static page(s)) "
        f"+ search index ({len(search_entries)} entries)"
    )
    return written


def main() -> None:
    """Render every active non-EN language. Each language is independent;
    a failure in one shouldn't block the others, but a structural error
    (missing data file) should still surface — we don't swallow
    exceptions, so the build fails fast.
    """
    targets = [lg.code for lg in _lang_registry.LANGUAGES if lg.active and lg.code != "en"]
    if not targets:
        print("build_translations: no active non-EN languages")
        return
    total = 0
    for code in targets:
        total += _render_one_lang(code)
    print(f"build_translations: {len(targets)} language(s) rendered, {total} page(s) total")


# ---------------------------------------------------------------------------
# Search index (per-language)
# ---------------------------------------------------------------------------

_TAG_RE = re.compile(r"<[^>]+>")
_WHITESPACE_RE = re.compile(r"\s+")
_TITLE_TAG_RE = re.compile(r"<title>([^<]+)</title>", re.IGNORECASE)
_MAIN_TAG_RE = re.compile(r"<main\b[\s\S]*?</main>", re.IGNORECASE)
_HEADING_RE = re.compile(r"<h[1-6]\b[^>]*>([\s\S]*?)</h[1-6]>", re.IGNORECASE)


def _extract_visible_text(html: str) -> str:
    """Strip every tag inside <main>, collapse whitespace, return plain text."""
    m = _MAIN_TAG_RE.search(html)
    body = m.group(0) if m else html
    # Drop <script> and <style> blocks first.
    body = re.sub(r"<script[\s\S]*?</script>", " ", body, flags=re.IGNORECASE)
    body = re.sub(r"<style[\s\S]*?</style>", " ", body, flags=re.IGNORECASE)
    # Drop HTML comments.
    body = re.sub(r"<!--[\s\S]*?-->", " ", body)
    text = _TAG_RE.sub(" ", body)
    text = _html.unescape(text)
    return _WHITESPACE_RE.sub(" ", text).strip()


def _extract_headings(html: str) -> list[str]:
    """Pull h1-h6 text from <main>. Required by the search widget — every
    entry must have a `headings` array or the runtime trips a TypeError."""
    m = _MAIN_TAG_RE.search(html)
    body = m.group(0) if m else html
    out: list[str] = []
    for hm in _HEADING_RE.finditer(body):
        inner = _TAG_RE.sub(" ", hm.group(1))
        inner = _WHITESPACE_RE.sub(" ", _html.unescape(inner)).strip()
        if inner:
            out.append(inner)
    return out


def _build_fr_search_index() -> list[dict[str, object]]:
    """Walk public/fr/ for rendered HTML and build search entries."""
    entries: list[dict[str, object]] = []
    if not OUT.is_dir():
        return entries
    for path in sorted(OUT.rglob("index.html")):
        rel = path.relative_to(PUBLIC).as_posix()  # e.g. "fr/about/index.html"
        url = "/" + rel
        html = path.read_text(encoding="utf-8")
        title_m = _TITLE_TAG_RE.search(html)
        title = _html.unescape(title_m.group(1).strip()) if title_m else url
        text = _extract_visible_text(html)
        # Trim — the EN index keeps ~2KB per entry. Match that.
        if len(text) > 2200:
            text = text[:2200]
        entries.append(
            {
                "title": title,
                "url": url,
                "content": text,
                "headings": _extract_headings(html),
            }
        )
    return entries


if __name__ == "__main__":
    main()
