"""Article renderer — one French page from English shell + French
frontmatter + body, plus the lead-aside / takeaway / author-card
furniture that goes with it."""

from __future__ import annotations

import html as _html
import re

import _lang_registry

from . import _state as st
from ._chrome import (
    _CANONICAL_RE,
    _DESC_META_RE,
    _HERO_RE,
    _KW_META_RE,
    _MAIN_BODY_RE,
    _OG_DESC_RE,
    _OG_LOCALE_RE,
    _OG_TITLE_RE,
    _OG_URL_RE,
    _TITLE_RE,
    _TW_DESC_RE,
    _TW_TITLE_RE,
    _date_today,
    _localize_inlanguage_globally,
    _patch_blogposting_jsonld,
    _set_html_lang,
    _swap_breadcrumb,
    localize_feed_links,
    translate_chrome,
)
from ._fm import render_markdown
from ._maps import (
    rewrite_en_descs_in_text,
    rewrite_en_titles_in_text,
    rewrite_en_urls,
    rewrite_fr_link_titles,
    rewrite_newsroom_card_titles,
    rewrite_related_card_titles,
)


# French author-card content (static — replaces the English author-card
# that post_enrich.py baked into the rendered shell). Synced with the
# English version in scripts/post_enrich.py.
def _french_author_card() -> str:
    """Author-card aside for the current language. All localised text
    (aria-label, portrait alt, bio, credentials prefix, full-profile
    link) reads from the registry; the URL resolves via STATIC_SLUG_FR.
    """
    about_slug = st.STATIC_SLUG_FR.get("about", "about")
    strings = _lang_registry.load_strings(st.LANG_CODE)
    author = _lang_registry.load_author(st.LANG_CODE)
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
        f'<a href="/{st.LANG_CODE}/{about_slug}/index.html">Sebastien Rousseau</a></strong>'
        f'<span class="author-card-bio">{bio}</span>'
        '<span class="author-credentials">'
        f"{credentials_prefix} "
        f'<a href="/{st.LANG_CODE}/{about_slug}/index.html">{full_profile}</a> &middot; '
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

# Compile to a single regex matched against the inner text of
# ``<li><strong>LABEL.</strong>``. The trailing dot is preserved.
# Built from the FR label keys at import — the EN key set is identical
# across languages; only the replacement values differ per language.
_TAKEAWAY_LABEL_RE = re.compile(
    r"(<li><strong>)("
    + "|".join(re.escape(k) for k in sorted(st.TAKEAWAY_LABELS_EN_TO_FR, key=len, reverse=True))
    + r")(\.</strong>)"
)


def _localise_takeaway_labels(html_fragment: str) -> str:
    """Translate the English takeaway labels in the FR lead aside."""

    def repl(m: re.Match[str]) -> str:
        return m.group(1) + st.TAKEAWAY_LABELS_EN_TO_FR[m.group(2)] + m.group(3)

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


def _collect_paragraph(lines: list[str], start_idx: int) -> list[str]:
    """Gather the first plain-text paragraph after ``start_idx``,
    skipping headings, HTML, images, lists, tables and link
    definitions."""
    n = len(lines)
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
    return paragraph_lines


def _clean_first_sentence(paragraph_lines: list[str]) -> str:
    """Strip markdown emphasis + links from the collected paragraph and
    return its first sentence (ellipsised past 220 chars)."""
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


def _takeaways_for_level(
    lines: list[str],
    prefix: str,
    bullets: list[tuple[str, str]],
    max_items: int,
) -> None:
    """Append (heading, first-sentence) bullets for every non-generic
    heading at ``prefix`` level until ``max_items`` is reached."""
    for i, ln in enumerate(lines):
        if not ln.startswith(prefix):
            continue
        heading = ln[len(prefix) :].strip().rstrip(".").rstrip(":")
        heading_clean = re.sub(r"[*_`]", "", heading)
        if heading_clean.lower() in _FR_GENERIC_H2:
            continue
        sent = _clean_first_sentence(_collect_paragraph(lines, i + 1))
        if sent:
            bullets.append((heading_clean, sent))
            if len(bullets) >= max_items:
                return


def _derive_fr_takeaways(body_md: str, max_items: int = 4) -> list[tuple[str, str]]:
    """Walk the FR markdown body; for each H2 (then H3) that isn't a
    generic heading, return (heading_text, first_sentence).
    """
    bullets: list[tuple[str, str]] = []
    lines = body_md.splitlines()
    _takeaways_for_level(lines, "## ", bullets, max_items)
    if len(bullets) < max_items:
        _takeaways_for_level(lines, "### ", bullets, max_items)
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

_CRUMBS_NAV_RE = re.compile(r'<nav class="crumbs"[\s\S]*?</nav>')


def _strip_postbuild_crumbs(shell: str) -> str:
    """Drop the visible breadcrumb nav that postbuild injects above the
    hero. The CI smoke re-renders locale pages from already-postbuilt EN
    shells; the EN trail must not leak — postbuild re-runs afterwards
    and re-injects a localized trail from each page's own JSON-LD."""
    return _CRUMBS_NAV_RE.sub("", shell)


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
    _strings = _lang_registry.load_strings(st.LANG_CODE)
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


def render_translation(slug: str, fm: dict[str, str], body_md: str) -> str | None:
    """Render one French page from English shell + French frontmatter + body.

    Returns the patched HTML, or None if the English shell is missing.
    """
    shell_src = st.PUBLIC / slug / "index.html"
    if not shell_src.is_file():
        print(f"build_translations: skip {slug} — English shell missing at {shell_src}")
        return None
    shell = _strip_postbuild_crumbs(shell_src.read_text(encoding="utf-8"))
    body_html = render_markdown(body_md)

    title = fm.get("title", slug)
    description = fm.get("description", "")
    keywords = fm.get("keywords", "")
    subtitle = fm.get("subtitle", description)
    page_title = f"{title} — Sebastien Rousseau"
    slug_fr = st.fr_slug(slug)
    url_fr = f"{st.BASE}/{st.LANG_CODE}/{slug_fr}/"

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
    shell = _OG_LOCALE_RE.sub(rf"\g<1>{st.LANG_LOCALE}\g<2>", shell, count=1)
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
    shell = _localize_inlanguage_globally(shell, st.LANG_CODE)

    # Breadcrumb final segment
    shell = _swap_breadcrumb(shell, slug_fr, title)

    # Localised feed links — point French pages at the FR feed shadows.
    shell = localize_feed_links(shell)

    return shell
