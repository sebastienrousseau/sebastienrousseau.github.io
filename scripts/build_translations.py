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

import html as _html
import json as _json
import re
import sys
from pathlib import Path

from markdown_it import MarkdownIt

sys.path.insert(0, str(Path(__file__).parent))
from _fr_slugs import EN_TO_FR, FR_TO_EN, fr_slug

PUBLIC = Path("public")
SRC = Path("_posts/fr")
OUT = PUBLIC / "fr"
BASE = "https://sebastienrousseau.com"

_DATED_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-")

# French UI strings — used by the meta-bar swap pass below and by
# postbuild's furniture renderers when they detect <html lang="fr">.
I18N_FR: dict[str, str] = {
    "Published": "Publié le",
    "Updated": "Mis à jour le",
    "min read": "min de lecture",
    "Previous": "Précédent",
    "Next": "Suivant",
    "Sources & references": "Sources et références",
    "About the author": "À propos de l'auteur",
    "Topics": "Sujets",
    "Contents": "Sommaire",
    "Estimated read time": "Temps de lecture estimé",
    "Article pagination": "Pagination des articles",
    "Link to": "Lien vers",
}

_FM_KEY_RE = re.compile(r'^([a-zA-Z_]+):\s*"((?:[^"\\]|\\.)*)"\s*$')


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
            fm[m.group(1)] = m.group(2)
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
_TITLE_RE = re.compile(r'<title>[^<]*</title>', re.IGNORECASE)
_DESC_META_RE = re.compile(r'(<meta\s+name="description"\s+content=")[^"]*(")', re.IGNORECASE)
_KW_META_RE = re.compile(r'(<meta\s+name="keywords"\s+content=")[^"]*(")', re.IGNORECASE)
_HTML_LANG_RE = re.compile(r'(<html\b[^>]*\blang=")[^"]*(")', re.IGNORECASE)
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
CHROME_PATCHES: list[tuple[str, str]] = [
    # Skip link
    (r'>Skip to main content</a>', '>Aller au contenu principal</a>'),

    # Top nav — toggle, theme, search, CTA, brand
    (r'aria-label="Toggle navigation"', 'aria-label="Basculer la navigation"'),
    (r'title="Toggle navigation"', 'title="Basculer la navigation"'),
    (r'aria-label="Primary"', 'aria-label="Navigation principale"'),
    (r'aria-label="Switch to dark theme"', 'aria-label="Activer le thème sombre"'),
    (r'aria-label="Switch to light theme"', 'aria-label="Activer le thème clair"'),
    (r'title="Switch theme"', 'title="Changer de thème"'),
    (r'aria-label="Search \(Cmd or Ctrl \+ K\)"', 'aria-label="Rechercher (Cmd ou Ctrl + K)"'),
    (r'title="Search \(⌘K\)"', 'title="Rechercher (⌘K)"'),
    (r'aria-label="Get in touch"', 'aria-label="Me contacter"'),
    (r'>Get in touch ›</a>', '>Me contacter ›</a>'),
    (r'aria-label="Sebastien Rousseau home"', 'aria-label="Accueil de Sebastien Rousseau"'),

    # Nav menu items — keep visitors inside /fr/ by pointing every
    # nav link to the localised page under /fr/.
    (r'<li><a href="/about/index\.html">About</a></li>',
     '<li><a href="/fr/about/index.html">À propos</a></li>'),
    (r'<li><a href="/papers/index\.html">Papers</a></li>',
     '<li><a href="/fr/papers/index.html">Publications</a></li>'),
    (r'<li><a href="/topics/index\.html">Topics</a></li>',
     '<li><a href="/fr/topics/index.html">Sujets</a></li>'),
    (r'<li><a href="/projects/index\.html">Projects</a></li>',
     '<li><a href="/fr/projects/index.html">Projets</a></li>'),
    (r'<li><a href="/articles/index\.html">Articles</a></li>',
     '<li><a href="/fr/index.html">Articles</a></li>'),
    (r'<li><a href="/contact/index\.html">Contact</a></li>',
     '<li><a href="/fr/contact/index.html">Contact</a></li>'),
    (r'<li><a href="/playlists/index\.html">Playlists</a></li>',
     '<li><a href="/fr/playlists/index.html">Playlists</a></li>'),

    # Back-to-top
    (r'aria-label="Back to top"', 'aria-label="Retour en haut"'),

    # Footer column titles
    (r'<h2 class="ap-foot-title">Writing</h2>', '<h2 class="ap-foot-title">Écrits</h2>'),
    (r'<h2 class="ap-foot-title">Work</h2>', '<h2 class="ap-foot-title">Activité</h2>'),
    (r'<h2 class="ap-foot-title">Reach</h2>', '<h2 class="ap-foot-title">Réseaux</h2>'),

    # Footer links — surgical, scoped by href. Point at /fr/ siblings so
    # visitors stay in the French edition.
    (r'<a href="/about/index\.html">About</a>',
     '<a href="/fr/about/index.html">À propos</a>'),
    (r'<a href="/made-with-static-site-generator/index\.html">Made with Static Site Generator</a>',
     '<a href="/fr/made-with-static-site-generator/index.html">Conçu avec Static Site Generator</a>'),
    (r'<a href="/papers/index\.html">Papers</a>',
     '<a href="/fr/papers/index.html">Publications</a>'),
    (r'<a href="/tags/index\.html">Tags</a>',
     '<a href="/fr/tags/index.html">Étiquettes</a>'),
    (r'<a href="/projects/index\.html">Projects</a>',
     '<a href="/fr/projects/index.html">Projets</a>'),
    (r'<a href="/playlists/index\.html">Playlists</a>',
     '<a href="/fr/playlists/index.html">Playlists</a>'),
    (r'<a href="/contact/index\.html">Contact</a>',
     '<a href="/fr/contact/index.html">Contact</a>'),
    (r'<a href="/articles/index\.html">Articles</a>',
     '<a href="/fr/index.html">Articles</a>'),

    # Social section
    (r'aria-label="Social links"', 'aria-label="Liens sociaux"'),
    (r'aria-label="Sebastien Rousseau on ', 'aria-label="Sebastien Rousseau sur '),

    # Footer legal links — route to /fr/ siblings
    (r'<a href="/accessibility/index\.html">Accessibility</a>',
     '<a href="/fr/accessibility/index.html">Accessibilité</a>'),
    (r'<a href="/privacy/index\.html">Privacy</a>',
     '<a href="/fr/privacy/index.html">Confidentialité</a>'),
    (r'<a href="/terms/index\.html">Terms</a>',
     '<a href="/fr/terms/index.html">Conditions</a>'),

    # Search palette (Shokunin widget — rendered HTML)
    (r'placeholder="Search documentation\.\.\."', 'placeholder="Rechercher dans la documentation..."'),
    (r'aria-label="Search"(?!\s*\()', 'aria-label="Rechercher"'),
    (r'<kbd>Esc</kbd>\s*close', '<kbd>Esc</kbd> fermer'),
    (r'navigate</span>', 'naviguer</span>'),
    (r'<kbd>Enter</kbd>\s*open', '<kbd>Entrée</kbd> ouvrir'),
    # Visible "Search" label inside the in-nav button
    (r'<span>Search</span>', '<span>Rechercher</span>'),

    # Language selector
    (r'aria-label="Language"', 'aria-label="Langue"'),
    (r'aria-label="EN, Change language"', 'aria-label="FR, Changer de langue"'),
    (r'title="Change language"', 'title="Changer de langue"'),
    (r'title="Coming soon"', 'title="Prochainement"'),
    (r'<span class="ap-lang-current">EN</span>', '<span class="ap-lang-current">FR</span>'),

    # Feed link titles in <head>
    (r'title="Atom Feed"', 'title="Flux Atom"'),
    (r'title="RSS Feed"', 'title="Flux RSS"'),

    # Lead aside (TL;DR + Key takeaways + Related reading) — extracted
    # from the English shell so structure matches; localise the labels.
    (r'aria-label="Article summary"', 'aria-label="Résumé de l\'article"'),
    (r'<strong>Key takeaways</strong>', '<strong>Points clés</strong>'),
    (r'<strong>Related reading:</strong>', '<strong>Articles connexes :</strong>'),

    # Related-posts grid at the end of the body
    (r'<h2 id="related-heading" class="related-heading">Related reading</h2>',
     '<h2 id="related-heading" class="related-heading">Articles connexes</h2>'),

    # Post-reviewed label (in case the English block leaks through)
    (r'>Last reviewed <', '>Dernière révision <'),

    # Author card aria
    (r'aria-label="About the author"', 'aria-label="À propos de l\'auteur"'),
    (r'>Full profile</a>', '>Profil complet</a>'),
    (r'alt="Portrait of Sebastien Rousseau"', 'alt="Portrait de Sebastien Rousseau"'),

    # Bottom finale CTA aside (homepage only — defensive)
    (r'<p class="feat-eyebrow">Get in touch</p>', '<p class="feat-eyebrow">Me contacter</p>'),
    (r'>Start a conversation</a>', '>Démarrer une conversation</a>'),

    # Footer 2nd-block aside on listing pages
    (r'<a href="/articles/index\.html">Read latest research</a>',
     '<a href="/articles/index.html">Lire les recherches récentes</a>'),
    (r'<a href="/contact/index\.html">Get in touch</a>',
     '<a href="/contact/index.html">Me contacter</a>'),
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
    return html


# Internal static pages that have a FR mirror at /fr/<page>/. Any
# remaining anchor on a FR page pointing at the bare EN URL gets
# rewritten to the FR sibling here. Idempotent.
_STATIC_FR_PAGES = (
    "about", "papers", "projects", "topics", "tags", "contact",
    "accessibility", "privacy", "terms", "playlists",
    "made-with-static-site-generator", "made-with-shokunin",
    "404", "offline", "thanks",
)
_STATIC_LINK_RE = re.compile(
    r'(href=")(?:https?://sebastienrousseau\.com)?/('
    + "|".join(_STATIC_FR_PAGES)
    + r')(/(?:index\.html)?)?(")',
)
_TOPIC_SUBPAGE_RE = re.compile(
    r'(href=")(?:https?://sebastienrousseau\.com)?/topics/([a-z0-9-]+)(/(?:index\.html)?)(")',
)
_ARTICLES_LINK_RE = re.compile(
    r'(href=")(?:https?://sebastienrousseau\.com)?/articles(/(?:index\.html)?)?(")',
)


def rewrite_static_links(html: str) -> str:
    """Rewrite every internal anchor on a FR page that still points at a
    top-level EN static page (/about/, /papers/, …) so it lands on the
    FR mirror under /fr/. ``/articles/`` collapses to ``/fr/`` (the hub)."""
    html = _STATIC_LINK_RE.sub(r'\1/fr/\2/\4', html)
    html = _TOPIC_SUBPAGE_RE.sub(r'\1/fr/topics/\2\3\4', html)
    html = _ARTICLES_LINK_RE.sub(r'\1/fr/\3', html)
    return html


# French author-card content (static — replaces the English author-card
# that post_enrich.py baked into the rendered shell). Synced with the
# English version in scripts/post_enrich.py.
def _french_author_card() -> str:
    return (
        '<aside class="author-card" aria-label="À propos de l\'auteur">'
        '<img alt="Portrait de Sebastien Rousseau" '
        'src="https://cloudcdn.pro/stocks/images/sebastien-rousseau.png" '
        'width="64" height="64" loading="lazy" decoding="async" />'
        '<span class="author-card-body">'
        '<strong class="author-card-name">'
        '<a href="/about/index.html">Sebastien Rousseau</a></strong>'
        '<span class="author-card-bio">Technologue senior dans la banque, '
        'j\'écris sur l\'IA appliquée, la migration ISO 20022, la cryptographie '
        'post-quantique pour les services financiers, et la transformation '
        'structurelle des paiements wholesale.</span>'
        '<span class="author-credentials">'
        'Plus de 20 ans d\'expérience chez HSBC Commercial &amp; Investment Bank, '
        'PayPal, Barclays, Shazam, AKQA, Virgin Group. '
        '<a href="/about/index.html">Profil complet</a> &middot; '
        '<a href="https://www.linkedin.com/in/sebastienrousseau/" rel="external noopener">LinkedIn</a> &middot; '
        '<a href="https://github.com/sebastienrousseau" rel="external noopener">GitHub</a>'
        '</span></span></aside>'
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
TAKEAWAY_LABELS_EN_TO_FR: dict[str, str] = {
    "Idea": "Idée",
    "Impact": "Impact",
    "Incentives": "Incitations",
    "Incentive": "Incitation",
    "Insight": "Aperçu",
    "Issues": "Enjeux",
    "Issue": "Enjeu",
    "Innovations": "Innovations",
    "Innovation": "Innovation",
    "Use Cases": "Cas d'usage",
    "Use Case": "Cas d'usage",
    "Limitations": "Limites",
    "Outlook": "Perspectives",
    "Conclusion": "Conclusion",
    "Regulation": "Réglementation",
    "Fraud Risks": "Risques de fraude",
    "Sustainability": "Soutenabilité",
    "Privacy and Security": "Vie privée et sécurité",
    "Privacy": "Vie privée",
    "Security": "Sécurité",
    "Recommendations": "Recommandations",
    "Approach": "Approche",
    "Background": "Contexte",
    "Methodology": "Méthodologie",
    "Findings": "Résultats",
    "Challenges": "Défis",
    "Opportunities": "Opportunités",
    "Risks": "Risques",
    "Mitigations": "Mesures d'atténuation",
}

# Compile to a single regex matched against the inner text of
# ``<li><strong>LABEL.</strong>``. The trailing dot is preserved.
_TAKEAWAY_LABEL_RE = re.compile(
    r'(<li><strong>)('
    + "|".join(re.escape(k) for k in sorted(TAKEAWAY_LABELS_EN_TO_FR, key=len, reverse=True))
    + r')(\.</strong>)'
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
        '',
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
        '</aside>'
    )


_FR_GENERIC_H2 = frozenset({
    "aperçu", "introduction", "vue d'ensemble", "sommaire",
    "table des matières", "lectures complémentaires",
    "points clés", "références", "sources et références",
    "résumé", "à propos", "conclusion",
})


def _derive_fr_takeaways(body_md: str, max_items: int = 4) -> list[tuple[str, str]]:
    """Walk the FR markdown body; for each H2 (then H3) that isn't a
    generic heading, return (heading_text, first_sentence).
    """
    bullets: list[tuple[str, str]] = []
    lines = body_md.splitlines()
    n = len(lines)

    def first_sentence(start_idx: int) -> str:
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
            heading = ln[len(prefix):].strip().rstrip(".").rstrip(":")
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
                f'  <li><strong>{_html.escape(heading)}.</strong> '
                f'{_html.escape(sentence)}</li>'
            )
        parts.append('</ul>')
    parts.append('</aside>')
    return "".join(parts)


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
    review = (
        f'<p class="post-reviewed">Dernière révision '
        f'<time datetime="{today}">{today}</time>.</p>'
    )
    return lead + body_html + _french_author_card() + review + related_aside


def _swap_breadcrumb(html: str, slug: str, title: str) -> str:
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
                item["item"] = f"{BASE}/fr/"
            elif pos == 3:
                item["name"] = title
                item["item"] = f"{BASE}/fr/{slug}/"
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
                    if isinstance(node, dict) and node.get("@type") == "BreadcrumbList":
                        if patch_breadcrumb(node):
                            changed = True
        if not changed:
            return m.group(0)
        return (
            '<script type="application/ld+json">'
            + _json.dumps(data, separators=(",", ":"), ensure_ascii=False)
            + '</script>'
        )

    return re.sub(
        r'<script type="application/ld\+json">([\s\S]+?)</script>',
        fix,
        html,
    )


_EN_URL_PATTERN_TMPL = (
    r'(https?://sebastienrousseau\.com)?/(?P<slug>{slugs})(/(?:index\.html)?)?'
)


def _build_en_url_rewriter() -> re.Pattern[str]:
    """Build a single anchored regex matching any internal EN slug
    that has a recorded FR counterpart. Used to rewrite EN URLs to
    /fr/<fr-slug>/ inside French page bodies."""
    slugs = "|".join(re.escape(s) for s in sorted(EN_TO_FR.keys(), key=len, reverse=True))
    if not slugs:
        return re.compile(r"$^")
    return re.compile(_EN_URL_PATTERN_TMPL.format(slugs=slugs))


_EN_URL_RE = _build_en_url_rewriter()


def rewrite_en_urls(html_fragment: str) -> str:
    """Rewrite every reference to an EN article URL to its FR
    counterpart, keeping the same origin (absolute → absolute,
    root-relative → root-relative)."""

    def repl(m: re.Match[str]) -> str:
        origin = m.group(1) or ""
        en = m.group("slug")
        fr = fr_slug(en)
        tail = m.group(3) or ""
        return f"{origin}/fr/{fr}{tail}"

    return _EN_URL_RE.sub(repl, html_fragment)


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
            attrs = re.sub(r'(\btitle=")[^"]*(")', rf'\g<1>{esc}\g<2>', attrs, count=1)
        else:
            attrs = attrs.rstrip() + f' title="{esc}"'
        if re.search(r'\baria-label="', attrs):
            attrs = re.sub(r'(\baria-label=")[^"]*(")', rf'\g<1>{esc}\g<2>', attrs, count=1)
        return f'<a{attrs} href="/fr/{slug}/index.html">'

    return _FR_LINK_RE.sub(repl, html)


_NEWSROOM_CARD_RE = re.compile(
    r'(<article class="newsroom-card[^"]*">)([\s\S]*?)(</article>)',
)


def rewrite_newsroom_card_titles(html: str) -> str:
    """On FR listing pages (papers, projects, tags, topics, …) the
    ``newsroom-card`` markup carries EN titles inside ``<h3><a>…</a></h3>``.
    Look up the FR title from the slug and overwrite."""
    fr_titles = _ensure_fr_title_map()

    def patch(m: re.Match[str]) -> str:
        open_tag, inner, close_tag = m.group(1), m.group(2), m.group(3)
        slug_m = re.search(
            r'href="(?:https?://sebastienrousseau\.com)?/fr/([a-z0-9-]+)/(?:index\.html)?"',
            inner,
        )
        if not slug_m:
            return m.group(0)
        en = FR_TO_EN.get(slug_m.group(1))
        if not en:
            return m.group(0)
        fr_title = fr_titles.get(en)
        if not fr_title:
            return m.group(0)
        esc = _html.escape(fr_title, quote=True)
        # <h3>…<a>TITLE</a>… inner text.
        inner = re.sub(
            r'(<h3[^>]*>\s*<a [^>]+>)[^<]+(</a>)',
            rf'\1{_html.escape(fr_title)}\2',
            inner,
            count=1,
        )
        # aria-label on media link.
        inner = re.sub(
            r'(<a [^>]*class="newsroom-card-media"[^>]*aria-label=")[^"]+(")',
            rf'\1{esc}\2',
            inner,
            count=1,
        )
        # title= on the same link.
        inner = re.sub(
            r'(<a [^>]*class="newsroom-card-media"[^>]*title=")[^"]+(")',
            rf'\1{esc}\2',
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
            rf'\1{esc}\2',
            inner,
            count=1,
        )
        # Rewrite the visible <h3>...<a>TITLE</a>... block.
        inner = re.sub(
            r'(<h3[^>]*>\s*<a [^>]+>)[^<]+(</a>)',
            rf'\1{_html.escape(fr_title)}\2',
            inner,
            count=1,
        )
        # Rewrite anchor-link aria-label "Link to TITLE".
        inner = re.sub(
            r'(<a class="heading-anchor"[^>]*aria-label="(?:Lien vers|Link to) )[^"]+(")',
            rf'\1{esc}\2',
            inner,
            count=1,
        )
        return open_tag + inner + close_tag

    return _RELATED_CARD_RE.sub(patch_card, html_fragment)


def _patch_blogposting_jsonld(
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
        node["inLanguage"] = "fr"
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
            ipo["inLanguage"] = "fr"
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
            + '</script>'
        )

    return re.sub(
        r'<script type="application/ld\+json">([\s\S]+?)</script>',
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
    url_fr = f"{BASE}/fr/{slug_fr}/"

    # html lang
    shell = _HTML_LANG_RE.sub(r'\1fr-FR\2', shell, count=1)
    # head meta
    shell = _TITLE_RE.sub(f'<title>{_html.escape(page_title)}</title>', shell, count=1)
    shell = _DESC_META_RE.sub(rf'\1{_html.escape(description, quote=True)}\2', shell, count=1)
    if keywords:
        shell = _KW_META_RE.sub(rf'\1{_html.escape(keywords, quote=True)}\2', shell, count=1)
    shell = _OG_TITLE_RE.sub(rf'\1{_html.escape(page_title, quote=True)}\2', shell, count=1)
    shell = _OG_DESC_RE.sub(rf'\1{_html.escape(description, quote=True)}\2', shell, count=1)
    shell = _OG_URL_RE.sub(rf'\1{url_fr}\2', shell, count=1)
    shell = _OG_LOCALE_RE.sub(r'\1fr_FR\2', shell, count=1)
    shell = _TW_TITLE_RE.sub(rf'\1{_html.escape(page_title, quote=True)}\2', shell, count=1)
    shell = _TW_DESC_RE.sub(rf'\1{_html.escape(description, quote=True)}\2', shell, count=1)
    shell = _CANONICAL_RE.sub(rf'\1{url_fr}\2', shell, count=1)

    # hero H1 + subtitle
    shell = _HERO_RE.sub(
        rf'\1{_html.escape(title)}\2{_html.escape(subtitle)}\3',
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

    # Chrome translation — nav, footer, search palette, social labels, etc.
    shell = translate_chrome(shell)

    # Rewrite inline-link title="…" and aria-label="…" attributes on every
    # <a> pointing to a /fr/<slug>/ URL so hover-tooltips advertise the
    # French title (visible link text is left alone — author choice).
    shell = rewrite_fr_link_titles(shell)
    shell = rewrite_newsroom_card_titles(shell)
    shell = rewrite_en_titles_in_text(shell)
    shell = rewrite_en_descs_in_text(shell)

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

    # Breadcrumb final segment
    shell = _swap_breadcrumb(shell, slug_fr, title)

    # Localised feed links — point French pages at the FR feed shadows.
    # Covers absolute, root-relative, and any prod/preview host variants
    # Shokunin may have emitted into the shell.
    shell = re.sub(
        r'href="(?:https?://[^/"]+)?/atom\.xml"',
        'href="/fr/atom.xml"',
        shell,
    )
    shell = re.sub(
        r'href="(?:https?://[^/"]+)?/rss\.xml"',
        'href="/fr/rss.xml"',
        shell,
    )

    return shell


# ---------------------------------------------------------------------------
# Hub: /fr/index.html
# ---------------------------------------------------------------------------

_NEWSROOM_RE = re.compile(r'<section class="newsroom">[\s\S]*?</section>', re.IGNORECASE)
_LDJSON_RE = re.compile(r'<script type="application/ld\+json">[\s\S]*?</script>', re.IGNORECASE)


def render_hub(entries: list[dict[str, str]]) -> str | None:
    """Hub page listing every French translation. Forks the rendered
    /articles/ page as shell."""
    shell_src = PUBLIC / "articles" / "index.html"
    if not shell_src.is_file():
        return None
    shell = shell_src.read_text(encoding="utf-8")

    # Strip the English ItemList (we emit a French one scoped to /fr/).
    for block in _LDJSON_RE.findall(shell):
        if '"ItemList"' in block or '"itemListElement"' in block:
            shell = shell.replace(block, '', 1)

    # Mirror /articles/ structure exactly: FEATURED block (newest)
    # + ARCHIVE grid (the rest). Same markup classes so the CSS
    # styling carries across both languages identically.
    if not entries:
        return None

    featured = entries[0]
    archive = entries[1:]
    feat_url = f"/fr/{featured['slug']}/index.html"
    feat_block = (
        '<header class="newsroom-section-head"><p class="newsroom-kicker">À LA UNE</p>'
        '<h2>Article récent</h2></header>'
        '<article class="newsroom-featured">'
        f'<a class="newsroom-featured-media" href="{feat_url}" title="{_html.escape(featured["title"], quote=True)}">'
        f'<img alt="{_html.escape(featured["banner_alt"], quote=True)}" '
        f'src="{featured["banner"]}" loading="eager" fetchpriority="high" '
        'decoding="async" width="800" height="800" />'
        '</a>'
        '<div class="newsroom-featured-body">'
        f'<h3><a href="{feat_url}" title="{_html.escape(featured["title"], quote=True)}">{_html.escape(featured["title"])}</a></h3>'
        f'<p>{_html.escape(featured["description"])}</p>'
        f'<p><a class="pill ghost" href="{feat_url}" title="{_html.escape(featured["title"], quote=True)}">Lire l\'article complet</a></p>'
        '</div>'
        '</article>'
    )

    cards: list[str] = []
    for e in archive:
        url = f"/fr/{e['slug']}/index.html"
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
        '<header class="newsroom-section-head"><p class="newsroom-kicker">ARCHIVES</p>'
        '<h2>Tous les articles</h2></header>'
        '<div class="newsroom-grid">' + "".join(cards) + '</div>'
    ) if cards else ""

    body = (
        '<section class="newsroom">'
        + feat_block
        + archive_block
        + '</section>'
    )
    shell = _NEWSROOM_RE.sub(body, shell, count=1)
    shell = _HTML_LANG_RE.sub(r'\1fr-FR\2', shell, count=1)
    title = "Articles en français — Sebastien Rousseau"
    desc = "Sélection d'articles traduits manuellement en français."
    shell = _TITLE_RE.sub(f'<title>{_html.escape(title)}</title>', shell, count=1)
    shell = _DESC_META_RE.sub(rf'\1{_html.escape(desc, quote=True)}\2', shell, count=1)
    shell = _OG_TITLE_RE.sub(rf'\1{_html.escape(title, quote=True)}\2', shell, count=1)
    shell = _OG_DESC_RE.sub(rf'\1{_html.escape(desc, quote=True)}\2', shell, count=1)
    shell = _OG_URL_RE.sub(r'\1https://sebastienrousseau.com/fr/\2', shell, count=1)
    shell = _OG_LOCALE_RE.sub(r'\1fr_FR\2', shell, count=1)
    shell = _CANONICAL_RE.sub(r'\1https://sebastienrousseau.com/fr/\2', shell, count=1)
    shell = translate_chrome(shell)
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
STATIC_PAGES_FR: dict[str, dict[str, str]] = {
    "about": {
        "title": "À propos — Sebastien Rousseau",
        "description": "Sebastien Rousseau, technologue senior dans la banque : IA appliquée, migration ISO 20022, cryptographie post-quantique, transformation structurelle des paiements wholesale.",
        "keywords": "Sebastien Rousseau, biographie, banque, paiements, IA, ISO 20022, cryptographie post-quantique, HSBC, PayPal, Barclays",
    },
    "papers": {
        "title": "Publications — Sebastien Rousseau",
        "description": "Articles, rapports et publications de Sebastien Rousseau sur l'IA, les paiements ISO 20022 et la cryptographie post-quantique.",
        "keywords": "publications, articles, rapports, recherche, ISO 20022, IA, cryptographie post-quantique",
    },
    "projects": {
        "title": "Projets — Sebastien Rousseau",
        "description": "Portfolio de bibliothèques open source maintenues par Sebastien Rousseau pour les paiements, le règlement transfrontalier et la cryptographie résistante au quantique.",
        "keywords": "projets open source, Python, Rust, paiements, ISO 20022, cryptographie post-quantique",
    },
    "topics": {
        "title": "Sujets — Sebastien Rousseau",
        "description": "Explorez les analyses par thématique : IA appliquée, paiements ISO 20022, cryptographie post-quantique, et transformation des paiements wholesale.",
        "keywords": "sujets, thématiques, IA, paiements, ISO 20022, cryptographie post-quantique",
    },
    "tags": {
        "title": "Étiquettes — Sebastien Rousseau",
        "description": "Parcourez les articles par étiquette : IA, ISO 20022, blockchain, cryptographie post-quantique et bien plus.",
        "keywords": "étiquettes, tags, navigation par sujet",
    },
    "contact": {
        "title": "Me contacter — Sebastien Rousseau",
        "description": "Entrez en contact avec Sebastien Rousseau pour les conseils en transformation des paiements, la migration ISO 20022 ou la stratégie post-quantique.",
        "keywords": "contact, conseil, paiements, ISO 20022, cryptographie post-quantique",
    },
    "accessibility": {
        "title": "Accessibilité — Sebastien Rousseau",
        "description": "Déclaration d'accessibilité : conformité WCAG 2.2 AA, principes inclusifs, retour d'expérience et coordonnées de signalement.",
        "keywords": "accessibilité, WCAG, conformité, inclusion numérique, audit",
    },
    "privacy": {
        "title": "Politique de confidentialité — Sebastien Rousseau",
        "description": "Comment ce site collecte, utilise et protège vos données. Mesure d'audience anonyme, cookies, hébergement et droits RGPD.",
        "keywords": "vie privée, RGPD, cookies, données personnelles, analytics",
    },
    "terms": {
        "title": "Conditions d'utilisation — Sebastien Rousseau",
        "description": "Conditions générales d'utilisation du site sebastienrousseau.com : licence du contenu, restrictions, marques et juridiction.",
        "keywords": "conditions, mentions légales, licence, copyright",
    },
    "made-with-static-site-generator": {
        "title": "Conçu avec Static Site Generator — Sebastien Rousseau",
        "description": "Ce site est généré avec Shokunin, un générateur de sites statiques rapide écrit en Rust.",
        "keywords": "Shokunin, générateur de sites statiques, Rust, performance",
    },
    "made-with-shokunin": {
        "title": "Conçu avec Shokunin — Sebastien Rousseau",
        "description": "Ce site est conçu avec Shokunin, un générateur de sites statiques en Rust optimisé pour la performance et le SEO.",
        "keywords": "Shokunin, SSG, Rust, performance, SEO",
    },
    "playlists": {
        "title": "Playlists — Sebastien Rousseau",
        "description": "Sélection musicale et auditive de Sebastien Rousseau.",
        "keywords": "playlists, musique",
    },
    "404": {
        "title": "Page introuvable — Sebastien Rousseau",
        "description": "La page demandée est introuvable. Retournez à l'accueil ou utilisez la recherche.",
        "keywords": "404, page introuvable",
    },
    "offline": {
        "title": "Hors ligne — Sebastien Rousseau",
        "description": "Vous êtes hors ligne. Reconnectez-vous pour accéder au contenu.",
        "keywords": "hors ligne, PWA",
    },
    "thanks": {
        "title": "Merci — Sebastien Rousseau",
        "description": "Merci de votre message. Je reviendrai vers vous très bientôt.",
        "keywords": "merci",
    },
}

# Body-string patches applied to every FR static page. These are
# additional English phrases that appear in rendered page bodies and
# need localising. They're idempotent (no-op if the string is absent).
# Per-page French <main> body replacements. The EN body inside the
# outer ``<div class="wrap">…</div>`` is swapped wholesale on the FR
# mirror so the page reads as natively French. Pages not listed here
# fall back to the lighter STATIC_BODY_PATCHES regex pass.
STATIC_BODIES_FR: dict[str, str] = {
    "404": (
        '<p>Cette page renvoie une erreur 404 : vous avez cliqué sur un lien '
        "rompu ou demandé une page qui n'existe pas. Voici quelques liens "
        "utiles pour reprendre votre lecture.</p>"
        '<p>Quelques liens qui pourraient vous être utiles :</p>'
        '<ul>'
        '<li><a href="/fr/">accueil</a> — la page d\'accueil de ce site</li>'
        '<li><a href="/fr/contact/index.html">contact</a> — me contacter</li>'
        '</ul>'
    ),
    "offline": (
        '<p>Essayez :</p>'
        '<ul>'
        '<li>Vérifier les paramètres de sécurité qui pourraient bloquer la connexion.</li>'
        '<li>Vérifier les câbles et connexions.</li>'
        '<li>Vérifier la qualité du signal dans votre zone.</li>'
        '<li>Vider le cache et les cookies de votre navigateur.</li>'
        '<li>Réinitialiser votre modem ou routeur.</li>'
        '<li>Redémarrer votre routeur.</li>'
        '<li>Désactiver le mode avion.</li>'
        '</ul>'
    ),
    "thanks": (
        '<p>En attendant, voici quelques pistes :</p>'
        '<ul>'
        '<li><a href="/fr/"><strong>Explorez mon site</strong></a> : '
        "découvrez mes services, comment je peux vous aider et ce qui me "
        "distingue des autres professionnels du domaine.</li>"
        '<li><a href="/fr/index.html"><strong>Lisez mes articles</strong></a> : '
        "j'écris sur une variété de sujets — intelligence artificielle (IA), "
        "cryptographie post-quantique (PQC), blockchain, cryptomonnaies et plus.</li>"
        '<li><a href="/fr/playlists/index.html"><strong>Écoutez mes playlists</strong></a> : '
        "je suis passionné de musique et j'ai créé des playlists couvrant "
        "plusieurs genres. J'espère qu'elles vous plairont autant qu'à moi.</li>"
        '</ul>'
        '<p>Cordialement,</p>'
        '<p>Sebastien Rousseau</p>'
    ),
    "accessibility": (
        "<p>Nous nous engageons à fournir une accessibilité numérique aux "
        "personnes en situation de handicap et améliorons continuellement "
        "l'expérience utilisateur, en mettant en œuvre les mesures "
        "d'accessibilité appropriées.</p>"
        '<h2>Mesures de soutien à l\'accessibilité</h2>'
        "<p>Nous visons à rendre notre site aussi accessible que possible "
        "à tous les utilisateurs. Cela inclut la possibilité de :</p>"
        '<ul>'
        "<li>Accéder à la majeure partie du site avec un lecteur d'écran.</li>"
        '<li>Garantir une navigation cohérente entre les pages.</li>'
        "<li>Augmenter le niveau de zoom jusqu'à 400 % sans débordement du texte.</li>"
        '<li>Modifier couleurs, contraste et styles via des extensions de navigateur.</li>'
        '<li>Naviguer dans le site uniquement au clavier.</li>'
        '<li>Disposer d\'alternatives textuelles pour tout contenu non textuel.</li>'
        '<li>Utiliser un logiciel de reconnaissance vocale pour la navigation.</li>'
        '</ul>'
        '<p>Nous avons également simplifié le texte du site pour faciliter la compréhension.</p>'
        '<h2>Notre statut de conformité</h2>'
        "<p>Nous reconnaissons que certaines parties de notre site ne sont pas "
        "pleinement accessibles, mais nous travaillons activement à corriger "
        "cela. Notre objectif est la conformité aux Web Content Accessibility "
        "Guidelines (WCAG) version 2.1 niveau AA. Vous pourriez rencontrer "
        "les problèmes suivants :</p>"
        '<ul>'
        "<li>Images dépourvues d'alternative textuelle utile pour les technologies d'assistance.</li>"
        '<li>Ratios de contraste insuffisants pour les personnes daltoniennes.</li>'
        '<li>Liens cachés manquants pour la navigation au clavier.</li>'
        "<li>Liens non étiquetés s'ouvrant dans de nouveaux onglets sans avertissement.</li>"
        '</ul>'
        '<h2>Signaler un problème</h2>'
        "<p>Si vous rencontrez un obstacle d'accessibilité, merci de nous le "
        "signaler via la <a href=\"/fr/contact/index.html\">page de contact</a>. "
        "Nous nous engageons à répondre dans les meilleurs délais.</p>"
    ),
    "privacy": (
        '<h2>Collecte et utilisation des informations</h2>'
        "<p>Nous ne collectons pas directement de données personnelles lors "
        "de votre navigation sur notre site. Nous n'utilisons pas de cookies "
        "à des fins logiques et n'enregistrons aucune information personnelle "
        "d'utilisateur.</p>"
        '<h2>Utilisation d\'outils de suivi</h2>'
        "<p>Nous utilisons deux services tiers pour surveiller et analyser "
        "le trafic web : Google Analytics et Microsoft Clarity.</p>"
        '<h3>Google Analytics</h3>'
        "<p>Google Analytics est un service d'analyse web fourni par Google qui "
        "suit et analyse le trafic du site. Google utilise les données collectées "
        "pour suivre et surveiller l'utilisation de notre site. Ces données sont "
        "partagées avec d'autres services Google. Pour plus d'informations sur "
        "les pratiques de confidentialité de Google, consultez la page "
        '<a href="https://policies.google.com/privacy">Règles de confidentialité de Google ⧉</a>.</p>'
        '<h3>Microsoft Clarity</h3>'
        "<p>Microsoft Clarity est un outil d'analyse comportementale qui nous "
        "aide à comprendre comment les utilisateurs interagissent avec notre "
        "site. Les données collectées incluent les mouvements de souris, les "
        "clics et les défilements. Pour plus d'informations sur les pratiques "
        "de confidentialité de Microsoft, consultez la "
        '<a href="https://privacy.microsoft.com/fr-fr/privacystatement">Déclaration de confidentialité de Microsoft ⧉</a>.</p>'
        '<h2>Vos droits</h2>'
        "<p>Selon votre lieu de résidence, vous disposez de certains droits "
        "concernant vos données personnelles : droit d'accès, de rectification, "
        "d'effacement, ou d'opposition à leur utilisation. Pour exercer ces "
        "droits, contactez-nous via la "
        '<a href="/fr/contact/index.html">page de contact</a>.</p>'
        '<h2>Modifications de cette politique</h2>'
        "<p>Nous pouvons mettre à jour cette politique de confidentialité de "
        "temps à autre. Toute modification sera publiée sur cette page. Nous "
        "vous encourageons à consulter régulièrement cette politique pour "
        "rester informé.</p>"
    ),
    "terms": (
        '<h2>Acceptation des conditions d\'utilisation</h2>'
        "<p>Les présentes conditions générales d'utilisation (les « Conditions ») "
        "s'appliquent au site web situé à l'adresse "
        '<a href="https://sebastienrousseau.com/">https://sebastienrousseau.com/</a> '
        "(le « Site »).</p>"
        "<p>EN UTILISANT LE SITE, VOUS ACCEPTEZ CES CONDITIONS ; SI VOUS N'ÊTES "
        "PAS D'ACCORD, N'UTILISEZ PAS LE SITE.</p>"
        '<h3>Propriété intellectuelle</h3>'
        "<p>Le Site et son contenu original, ses fonctionnalités et sa "
        "fonctionnalité sont et resteront la propriété exclusive de Sebastien "
        "Rousseau. Ce Site est protégé par les lois de copyright, de marques "
        "déposées et autres lois applicables aux États-Unis et à l'international.</p>"
        '<h3>Liens vers d\'autres sites</h3>'
        "<p>Notre Site peut contenir des liens vers des sites web tiers (les "
        "« Sites liés ») ou des services qui ne sont ni détenus ni contrôlés "
        "par Sebastien Rousseau. Ces Sites liés sont fournis uniquement à des "
        "fins de commodité pour nos visiteurs.</p>"
        "<p>Sebastien Rousseau n'exerce aucun contrôle et n'assume aucune "
        "responsabilité concernant le contenu, les politiques de confidentialité "
        "ou les pratiques des Sites liés ou services.</p>"
        '<h3>Limitation de responsabilité</h3>'
        "<p>SEBASTIEN ROUSSEAU NE GARANTIT PAS QUE LE SITE OU TOUT CONTENU, "
        "SERVICE OU FONCTIONNALITÉ DU SITE SERA EXEMPT D'ERREURS OU "
        "ININTERROMPU, OU QUE LES ÉVENTUELS DÉFAUTS SERONT CORRIGÉS, OU "
        "ENCORE QUE VOTRE UTILISATION DU SITE PRODUIRA DES RÉSULTATS "
        "SPÉCIFIQUES. LE SITE ET SON CONTENU SONT FOURNIS « EN L'ÉTAT » ET "
        "« SELON DISPONIBILITÉ ».</p>"
        '<h3>Loi applicable</h3>'
        "<p>Ces Conditions sont régies par les lois en vigueur sans égard "
        "aux principes de conflits de lois. Tout litige sera soumis à la "
        "juridiction compétente.</p>"
        '<h3>Modifications</h3>'
        "<p>Nous nous réservons le droit, à notre seule discrétion, de "
        "modifier ou de remplacer ces Conditions à tout moment. Si une "
        "révision est significative, nous fournirons un préavis avant que "
        "les nouvelles conditions n'entrent en vigueur.</p>"
        '<h3>Nous contacter</h3>'
        "<p>Pour toute question concernant ces Conditions, contactez-moi "
        'via la <a href="/fr/contact/index.html">page de contact</a>.</p>'
    ),
    "contact": (
        '<p class="lede">Je n\'utiliserai vos informations personnelles que '
        "pour protéger votre vie privée. Les données collectées dans le "
        "formulaire ci-dessous servent exclusivement à répondre à votre "
        "demande.</p>"
        '<form class="ap-form" action="https://formspree.io/f/mjvqpwyo" method="POST">'
        '<div class="ap-form-row">'
        '<label for="sender">Nom</label>'
        '<input type="text" id="sender" name="name" autocomplete="name" required />'
        '</div>'
        '<div class="ap-form-row">'
        '<label for="email">E-mail</label>'
        '<input type="email" id="email" name="email" autocomplete="email" required />'
        '</div>'
        '<div class="ap-form-row">'
        '<label for="subject">Sujet</label>'
        '<select id="subject" name="subject" required aria-label="Choisir un sujet">'
        '<option value="">Choisir un sujet</option>'
        '<option value="press">Publicité / presse</option>'
        '<option value="business">Demande professionnelle</option>'
        '<option value="feedback">Retour / suggestion</option>'
        '<option value="general">Question générale</option>'
        '<option value="papers">Demande d\'accès immédiat</option>'
        '<option value="product">Question produit</option>'
        '<option value="support">Support produit</option>'
        '</select>'
        '</div>'
        '<div class="ap-form-row">'
        '<label for="message">Message</label>'
        '<textarea id="message" name="message" rows="6" required></textarea>'
        '</div>'
        '<p class="ap-form-recaptcha">Protégé par Google reCAPTCHA</p>'
        '<button type="submit" class="pill primary">Envoyer le message</button>'
        '</form>'
    ),
    "made-with-shokunin": (
        '<p><img src="https://cloudcdn.pro/clients/shokunin/v1/banners/banner-shokunin.svg" '
        'alt="Bannière du Static Site Generator" '
        'title="Conçu avec Static Site Generator, le SSG le plus rapide écrit en Rust" '
        'class="w-50 p-3 me-3 float-end" /></p>'
        '<h2>Adoptez Static Site Generator pour une création de site sans effort</h2>'
        "<p>Créer un site web ne doit pas être une entreprise complexe, "
        "coûteuse ou chronophage. Cela doit être rapide, sûr et fiable, "
        "adapté à vos besoins spécifiques. Static Site Generator répond à "
        "ces critères en offrant une solution gratuite et riche en "
        "fonctionnalités pour bâtir des sites statiques.</p>"
        "<h2>Libérez la puissance de Static Site Generator</h2>"
        "<p>L'interface intuitive de Static Site Generator donne du pouvoir "
        "aux débutants comme aux développeurs expérimentés. Avec lui, vous "
        "pouvez créer un site visuellement abouti et fonctionnellement "
        "solide en quelques minutes, sans écrire une seule ligne de code.</p>"
        '<p><a href="https://shokunin.com/" '
        'title="Static Site Generator : le SSG le plus rapide écrit en Rust">'
        "Lancez-vous dès aujourd'hui et découvrez la puissance transformatrice "
        "de Static Site Generator ! ❯</a></p>"
    ),
    "made-with-static-site-generator": (
        '<img alt="Bannière du Static Site Generator" '
        'src="https://cloudcdn.pro/clients/shokunin/v1/banners/banner-shokunin.svg" '
        'class="w-50 p-3 me-3 float-end" />'
        '<h2>Adoptez Static Site Generator pour une création de site sans effort</h2>'
        "<p>Créer un site web ne doit pas être une entreprise complexe, "
        "coûteuse ou chronophage. Cela doit être rapide, sûr et fiable, "
        "adapté à vos besoins spécifiques. Static Site Generator répond à "
        "ces critères en offrant une solution gratuite et riche en "
        "fonctionnalités pour bâtir des sites statiques.</p>"
        "<h2>Libérez la puissance de Static Site Generator</h2>"
        "<p>L'interface intuitive de Static Site Generator donne du pouvoir "
        "aux débutants comme aux développeurs expérimentés. Avec lui, vous "
        "pouvez créer un site visuellement abouti et fonctionnellement "
        "solide en quelques minutes, sans écrire une seule ligne de code.</p>"
        '<p><a href="https://github.com/sebastienrousseau/static-site-generator" '
        'title="Static Site Generator : le SSG le plus rapide écrit en Rust">'
        "Lancez-vous dès aujourd'hui et découvrez la puissance transformatrice "
        "de Static Site Generator ! ❯</a></p>"
    ),
    "about": (
        '<p><img src="https://cloudcdn.pro/stocks/images/sebastien-rousseau.png" '
        'alt="Portrait de Sebastien Rousseau" '
        'class="image-wrapper float-sm-start rounded-circle w-25 float-end" /></p>'
        '<h2>Biographie</h2>'
        "<p>Sebastien Rousseau est un cadre dirigeant senior, à la fois technique "
        "et business, fort de plus de 20 ans d'expérience dans la technologie "
        "des paiements et l'avenir de la finance numérique. Il est passionné "
        "par la conception de la prochaine génération de produits bancaires et "
        "de paiement, à travers l'intégration stratégique de l'intelligence "
        "artificielle (IA), de la cryptographie post-quantique (PQC) et de la "
        "technologie blockchain.</p>"
        "<p>En tant que Senior Product Manager chez HSBC, Sebastien a piloté "
        "avec succès le développement et le lancement de plusieurs produits "
        "et services innovants, dont les HSBC Treasury APIs et l'offre HSBC "
        "Banking-as-a-Service (BaaS). Ces solutions globales pour la clientèle "
        "entreprise visent à offrir une expérience numérique fluide aux clients "
        "d'HSBC.</p>"
        "<p>Avant HSBC, Sebastien a joué un rôle clé dans la conception et la "
        "livraison d'améliorations opérationnelles sur de nombreux projets "
        "mobiles complexes. Il a travaillé avec Barclays Bank PLC, Shazam "
        "Entertainment Limited et PayPal Inc. Il a commencé sa carrière chez "
        "AKQA, à Londres, où il a dirigé la division technologie mobile, "
        "accompagnant des comptes clients mondiaux clés (Nike, RBS, MTV, GAP, "
        "Nokia, Target) et menant des projets mobiles innovants.</p>"
        "<p>L'expérience diversifiée de Sebastien dans la banque, les services "
        "financiers et la technologie en fait un atout précieux pour toute "
        "organisation cherchant à innover et à conduire une transformation "
        "numérique. Sa double approche stratégique et technique lui permet "
        "de combler le fossé entre les exigences métier et leur mise en œuvre "
        "technique, garantissant des solutions à la fois efficaces et "
        "alignées sur les objectifs de l'entreprise.</p>"
        '<h2>Expertise</h2>'
        '<ul>'
        "<li><strong>Paiements & règlement</strong> — ISO 20022, paiements "
        "transfrontaliers, SEPA Instant, SWIFT gpi.</li>"
        "<li><strong>IA appliquée</strong> — IA générative, LLM, automatisation "
        "des opérations bancaires.</li>"
        "<li><strong>Cryptographie post-quantique</strong> — algorithmes NIST PQC, "
        "migration des protocoles, sécurité financière à long terme.</li>"
        "<li><strong>Open source</strong> — bibliothèques Python et Rust pour "
        "la finance (pain001, pacs008, dtt, hsh, kyberlib, shokunin).</li>"
        '</ul>'
        '<h2>Me contacter</h2>'
        "<p>Pour les demandes professionnelles, le conseil ou la prise de "
        "parole, contactez-moi via la "
        '<a href="/fr/contact/index.html">page de contact</a> ou sur '
        '<a href="https://www.linkedin.com/in/sebastienrousseau/" rel="external noopener">LinkedIn</a>.</p>'
    ),
}


STATIC_BODY_PATCHES: list[tuple[str, str]] = [
    # Topic hub breadcrumb + headings
    (r'<a href="/">Home</a> &middot; <span>Topics</span>',
     '<a href="/fr/">Accueil</a> &middot; <span>Sujets</span>'),
    (r'>Home<', '>Accueil<'),
    (r'>Topics</h1>', '>Sujets</h1>'),
    (r'>PILLARS</p>', '>PILIERS</p>'),
    (r'PILLAR · TOPIC', 'PILIER · SUJET'),
    (r'PILLAR · PROJECT', 'PILIER · PROJET'),
    (r'Curated topic clusters[^<]+',
     "Clusters de sujets — choisissez un fil et suivez-le à travers l'archive."),
    # /fr/papers/
    (r'INDUSTRY WHITE PAPER · EPAA', 'LIVRE BLANC INDUSTRIE · EPAA'),
    (r'INDUSTRY WHITE PAPER', 'LIVRE BLANC INDUSTRIE'),
    (r'WHITE PAPER', 'LIVRE BLANC'),
    (r' · Free download', " · Téléchargement gratuit"),
    (r'Free download<', 'Téléchargement gratuit<'),
    (r'>Download<', '>Télécharger<'),
    (r'>Request access<', "<>Demander l'accès<"),
    (r'>English · PDF', '>Français · PDF'),
    # /fr/papers/ paper titles and abstracts
    (r'>Quantum-Safe Payments: Why the Payments Industry Must Act Now<',
     ">Paiements résistants au quantique : pourquoi le secteur doit agir maintenant<"),
    (r'>Accelerating Real-Time Speech Recognition with OpenAI Whisper and Metal Performance Shaders on macOS<',
     ">Accélérer la reconnaissance vocale en temps réel avec OpenAI Whisper et Metal Performance Shaders sur macOS<"),
    (r'>Recent research and analysis<',
     ">Recherches et analyses récentes<"),
    # /fr/papers/ section heads + ledes
    (r'September 2025 &middot; Emerging Payments Association Asia \(EPAA\)',
     "Septembre 2025 &middot; Emerging Payments Association Asia (EPAA)"),
    (r'>Quantum computing threatens the cryptographic foundations[^<]+',
     ">L'informatique quantique menace les fondations cryptographiques des services financiers. Les paiements — du temps réel au règlement transfrontalier — reposent sur des protections que l'informatique quantique finira par rendre obsolètes. Ce livre blanc EPAA expose pourquoi le secteur doit agir dès maintenant."),
    (r'2024 &middot; Independent Research &middot;',
     "2024 &middot; Recherche indépendante &middot;"),
    (r'>This independent research paper presents[^<]+',
     ">Ce rapport de recherche indépendant présente une optimisation de la reconnaissance vocale en temps réel sur macOS à l'aide d'OpenAI Whisper et des Metal Performance Shaders, démontrant des gains de latence et d'efficacité énergétique mesurables."),
    (r'>License &amp; pricing<', '>Licence et tarification<'),
    (r'>One copy per buyer<', ">Un exemplaire par acheteur<"),
    # FAQ section
    (r'>Questions\? Answers\.<', '>Questions ? Réponses.<'),
    (r'>Are the white papers free to read\?<',
     ">Les livres blancs sont-ils en libre lecture ?<"),
    # FAQ Q1 answer (wrapped <p> contains <em>, so use full-block replace)
    (r'(<summary[^>]*>Les livres blancs sont-ils en libre lecture \?</summary>)\s*<section class="qa-a">[\s\S]*?</section>',
     r'\1<section class="qa-a"><p>Le livre blanc EPAA <em>Quantum-Safe Payments</em> est en téléchargement public gratuit sur '
     r'<a href="https://emergingpaymentsasia.org/wp-content/uploads/2025/09/Quantum-Safe-Payments-Why-the-Payments-Industry-Must-Act-Now.pdf" rel="external noopener">emergingpaymentsasia.org</a>. '
     r'Le rapport de recherche indépendant sur la reconnaissance vocale en temps réel avec OpenAI Whisper et Metal Performance Shaders est sous licence et disponible à l\'achat individuel à 49,00 $ '
     r'(anglais, PDF, ~95 Ko). Un exemplaire par acheteur ; téléchargements à usage personnel uniquement, non redistribuables.</p></section>'),
    # FAQ Q2 answer
    (r'(<summary[^>]*>Puis-je citer ces documents \?</summary>)\s*<section class="qa-a">[\s\S]*?</section>',
     r'\1<section class="qa-a"><p>Oui. Les courtes citations avec attribution sont bienvenues dans le cadre du fair use. '
     r'Pour les publications EPAA, citez l\'EPAA comme éditeur avec le groupe de travail, l\'année et l\'URL du PDF. '
     r'Pour les rapports de recherche indépendants, citez sous la forme : <em>Rousseau, S. (année). Titre. Auto-publié.</em> avec l\'URL canonique. '
     r'Pour reproduire une figure ou un passage étendu, merci de me contacter.</p></section>'),
    # FAQ Q3 answer
    (r'(<summary[^>]*>Où puis-je suivre les nouvelles publications \?</summary>)\s*<section class="qa-a">[\s\S]*?</section>',
     r'\1<section class="qa-a"><p>Abonnez-vous au flux <a href="/fr/rss.xml">RSS</a> ou suivez-moi sur '
     r'<a href="https://www.linkedin.com/in/sebastienrousseau/" rel="external noopener">LinkedIn</a> pour être informé des nouvelles publications, livres blancs et analyses.</p></section>'),
    (r'>May I cite or quote from these papers\?<',
     ">Puis-je citer ces documents ?<"),
    (r'>Yes\. Short quotations with attribution[^<]+',
     ">Oui. Les courtes citations avec attribution sont bienvenues dans le cadre du fair use. Pour les publications EPAA, citez l'EPAA comme éditeur avec le groupe de travail, l'année et l'URL du PDF. Pour les rapports de recherche indépendants, citez sous la forme : Rousseau, S. (année). Titre. Auto-publié. avec l'URL canonique. Pour reproduire une figure ou un passage étendu, merci de me contacter."),
    (r'>Where can I follow new releases\?<',
     ">Où puis-je suivre les nouvelles publications ?<"),
    (r'>Subscribe to the RSS feed or follow me on LinkedIn[^<]+',
     ">Abonnez-vous au flux RSS ou suivez-moi sur LinkedIn pour être informé des nouvelles publications, livres blancs et analyses."),
    # /fr/projects/
    (r'>Browse all projects<', '>Parcourir tous les projets<'),
    (r'>Three areas of practice\.\s*<span',
     '>Trois domaines de pratique. <span'),
    (r'>One philosophy\.</span>',
     '>Une philosophie.</span>'),
    (r'>WHAT IS INSIDE<', '>CONTENU<'),
    (r'>OPEN SOURCE FOR FINANCIAL SERVICES<',
     '>OPEN SOURCE POUR LES SERVICES FINANCIERS<'),
    (r'>Payments and settlement\.<', '>Paiements et règlement.<'),
    (r'>Post-quantum cryptography\.<', '>Cryptographie post-quantique.<'),
    (r'>Applied AI\.<', '>IA appliquée.<'),
    (r'>Explore payments tools<', '>Explorer les outils de paiement<'),
    (r'>Explore PQC tools<', '>Explorer les outils PQC<'),
    (r'>Explore AI tools<', '>Explorer les outils IA<'),
    (r'>Authored & maintained<', '>Écrits et maintenus<'),
    (r'>Authored &amp; maintained<', '>Écrits et maintenus<'),
    (r'>Open source for the future of finance\.<',
     ">Open source pour l'avenir de la finance.<"),
    # /fr/playlists/
    (r'<p class="newsroom-kicker">FEATURED</p>',
     '<p class="newsroom-kicker">À LA UNE</p>'),
    (r'>Latest Music</h2>', '>Musique récente</h2>'),
    (r'>Latest playlist</h2>', '>Playlist récente</h2>'),
    (r'>Soulful, jazz and downtempo</h2>',
     '>Soulful, jazz et downtempo</h2>'),
    (r'<p class="newsroom-kicker">MORNING & MOOD</p>',
     '<p class="newsroom-kicker">MATIN & AMBIANCE</p>'),
    (r'>Morning, mood and chill</h2>',
     '>Matin, ambiance et chill</h2>'),
    (r'<p class="newsroom-kicker">ELECTRONIC</p>',
     '<p class="newsroom-kicker">ÉLECTRONIQUE</p>'),
    (r'>Electronic, house and techno</h2>',
     '>Électro, house et techno</h2>'),
    (r'>Pop, rock and alternative</h2>',
     '>Pop, rock et alternatif</h2>'),
    (r'<p class="newsroom-kicker">FOCUS</p>',
     '<p class="newsroom-kicker">CONCENTRATION</p>'),
    (r'>Focus and productivity</h2>',
     '>Concentration et productivité</h2>'),
    # Section ledes
    (r'>Smooth Jazz, Neo Soul, and laid-back grooves[^<]+',
     '>Smooth Jazz, Neo Soul et grooves nonchalants. Des playlists pour quand la journée demande de ralentir.'),
    (r'>This page has a comprehensive list[^<]+',
     ">Cette page présente une sélection des playlists Spotify les plus "
     "populaires et acclamées par la critique, couvrant un large éventail "
     "de genres. Que vous soyez fan de jazz, de soul, de hip-hop ou de "
     "musique électronique, vous trouverez une playlist à votre goût."),
    # Playlist excerpts
    (r'>Step into the harmonious realm of TETRA\.[^<]+',
     ">Entrez dans le royaume harmonieux de TETRA. Une playlist euphorique conçue pour élever votre esprit et remplir votre âme de joie."),
    (r'>Unwind and embrace the essence of summer with this curated selection of Jazz, Soul, R(?:&amp;|&)B and Neo Soul beats\.',
     ">Détendez-vous et embrassez l'essence de l'été avec cette sélection de Jazz, Soul, R&amp;B et Neo Soul."),
    (r'>A deep dive into the quintessential collection of Jazz, Soul, R(?:&amp;|&)B and Neo Soul beats\.',
     ">Une plongée en profondeur dans la collection quintessentielle de Jazz, Soul, R&amp;B et Neo Soul."),
    (r'>Take a break from a busy day and relax with soothing nu jazz and downtempo beats\.',
     ">Faites une pause dans une journée chargée et détendez-vous avec du nu jazz et du downtempo apaisants."),
    (r'>Soulful tracks with a fashion-forward vibe\. Music to set the tone for a productive and stylish day\.',
     ">Des morceaux soul à la vibe avant-gardiste. La musique idéale pour donner le ton d'une journée productive et stylée."),
    (r'>Celebrate the joy of life and dive into a world of vivid emotions, vibrant hues and soulful rhythms\.',
     ">Célébrez la joie de vivre et plongez dans un monde d'émotions vives, de couleurs vibrantes et de rythmes soul."),
    (r'>Laid-back beats, house-influenced grooves and new deep house tracks\.',
     ">Beats nonchalants, grooves d'inspiration house et nouvelles pépites deep house."),
    (r'>Seamlessly blending funky disco, house, French touch and other genres into an ultra-cool and energetic musical experience\.',
     ">Un mélange fluide de disco funky, house, French touch et autres genres pour une expérience musicale ultra-cool et énergique."),
    (r'>A sonic voyage featuring Nu-Disco, French House, Electro and Disco House tunes from artists like Madeon and Fred Falke\.',
     ">Un voyage sonore mêlant Nu-Disco, French House, Electro et Disco House d'artistes comme Madeon et Fred Falke."),
    (r'>Laid-back beats, hip-hop-influenced grooves and new indie pop tracks\.',
     ">Beats nonchalants, grooves d'inspiration hip-hop et nouveaux titres indie pop."),
    (r'>Original Hip Hop, Rap and R(?:&amp;|&)B Flavor Sessions\.',
     ">Sessions originales aux saveurs Hip Hop, Rap et R&amp;B."),
    (r'>Brace yourself for hardcore rap and hip hop tracks\.',
     ">Préparez-vous à du rap et du hip hop hardcore."),
    (r'>A few of the favourite hip-hop gems\.',
     ">Quelques-unes des pépites hip-hop favorites."),
    (r'>Soulful beats and thoughtful lyrics\. A captivating look into the world of contemporary hip hop, R(?:&amp;|&)B and rap\.',
     ">Beats soul et paroles réfléchies. Un regard captivant sur le hip hop, le R&amp;B et le rap contemporains."),
    (r'>Laid-back vibes and mellow rhythms with this stunning playlist of Lo-Fi Hip Hop beats\.',
     ">Ambiances nonchalantes et rythmes doux dans cette superbe playlist Lo-Fi Hip Hop."),
    (r'>Celebrate the diverse heritage of African music\. From the soulful rhythms of Wassoulou to the lively beats of Londonko\.',
     ">Célébrez la riche diversité de la musique africaine. Des rythmes soul du Wassoulou aux beats vifs du Londonko."),
    # /fr/tags/
    (r'aria-label="Tag: ([^,]+), (\d+) Posts"', r'aria-label="Étiquette : \1, \2 articles"'),
    (r'(\(\d+) Posts\)', r'\1 articles)'),
    # Hero / shared section labels
    (r'>Latest research<', '>Recherches récentes<'),
    (r'>Read latest research<', '>Lire les recherches récentes<'),
    (r'>Featured articles<', '>Articles à la une<'),
    (r'>All articles<', '>Tous les articles<'),
    (r'>Read more<', '>Lire la suite<'),
    (r'>Read full article<', '>Lire l\'article complet<'),
    (r'>Newest first<', '>Plus récent d\'abord<'),
    (r'>Oldest first<', '>Plus ancien d\'abord<'),
    (r'>By topic<', '>Par sujet<'),
    (r'>All topics<', '>Tous les sujets<'),
    (r'>By tag<', '>Par étiquette<'),
    (r'>All tags<', '>Toutes les étiquettes<'),
    (r'>Published<', '>Publié<'),
    (r'>Updated<', '>Mis à jour<'),
    # /papers/ + /projects/ chrome
    (r'>Open source<', '>Open source<'),
    (r'>Authored & maintained<', '>Écrits et maintenus<'),
    (r'>Open source for the future of finance\.<', '>Open source pour l\'avenir de la finance.<'),
    (r'>A portfolio of', '>Un portfolio de'),
    # /contact/
    (r'>Start a conversation<', '>Démarrer une conversation<'),
    (r'>Drop me a line<', '>Écrivez-moi<'),
    # Generic CTAs that may appear on multiple pages
    (r'>Learn more<', '>En savoir plus<'),
    (r'>Subscribe<', '>S\'abonner<'),
    (r'>Follow<', '>Suivre<'),
    (r'>Latest<', '>Récent<'),
]

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


def render_static_translation(slug: str) -> str | None:
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
    keywords = cfg.get("keywords", "")
    url_fr = f"{BASE}/fr/{slug}/"

    shell = _HTML_LANG_RE.sub(r'\1fr-FR\2', shell, count=1)
    shell = _TITLE_RE.sub(f'<title>{_html.escape(title)}</title>', shell, count=1)
    shell = _DESC_META_RE.sub(rf'\1{_html.escape(description, quote=True)}\2', shell, count=1)
    if keywords:
        shell = _KW_META_RE.sub(rf'\1{_html.escape(keywords, quote=True)}\2', shell, count=1)
    shell = _OG_TITLE_RE.sub(rf'\1{_html.escape(title, quote=True)}\2', shell, count=1)
    shell = _OG_DESC_RE.sub(rf'\1{_html.escape(description, quote=True)}\2', shell, count=1)
    shell = _OG_URL_RE.sub(rf'\1{url_fr}\2', shell, count=1)
    shell = _OG_LOCALE_RE.sub(r'\1fr_FR\2', shell, count=1)
    shell = _TW_TITLE_RE.sub(rf'\1{_html.escape(title, quote=True)}\2', shell, count=1)
    shell = _TW_DESC_RE.sub(rf'\1{_html.escape(description, quote=True)}\2', shell, count=1)
    shell = _CANONICAL_RE.sub(rf'\1{url_fr}\2', shell, count=1)

    # Rewrite EN article URLs inside the body to FR counterparts.
    shell = rewrite_en_urls(shell)

    # Swap the EN <main> body for the curated FR body when one is
    # provided. Falls through to STATIC_BODY_PATCHES (light text-swap)
    # for pages without a curated translation.
    fr_body = STATIC_BODIES_FR.get(slug)
    if fr_body:
        shell = _replace_static_main_body(shell, fr_body)

    # Localise chrome (nav / footer / search / aria) + body text.
    shell = translate_chrome(shell)
    for pat, repl in _STATIC_BODY_COMPILED:
        shell = pat.sub(repl, shell)

    # Rewrite article-card titles + tooltips on listing pages
    # (papers, projects, tags, topic hub, …) to the FR title.
    shell = rewrite_fr_link_titles(shell)
    shell = rewrite_newsroom_card_titles(shell)
    shell = rewrite_en_titles_in_text(shell)
    shell = rewrite_en_descs_in_text(shell)

    # Localise feed links.
    shell = re.sub(
        r'href="(?:https?://[^/"]+)?/atom\.xml"',
        'href="/fr/atom.xml"',
        shell,
    )
    shell = re.sub(
        r'href="(?:https?://[^/"]+)?/rss\.xml"',
        'href="/fr/rss.xml"',
        shell,
    )

    # Patch the WebPage / WebSite JSON-LD's @id, url, name, description.
    def patch_jsonld(m: re.Match[str]) -> str:
        raw = m.group(1)
        try:
            data = _json.loads(raw)
        except _json.JSONDecodeError:
            return m.group(0)
        changed = False

        def patch_node(node: dict) -> bool:
            local = False
            t = node.get("@type")
            if t in ("WebPage", "AboutPage", "ContactPage", "CollectionPage"):
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
                    node["inLanguage"] = "fr"
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
            + '</script>'
        )

    shell = re.sub(
        r'<script type="application/ld\+json">([\s\S]+?)</script>',
        patch_jsonld,
        shell,
    )

    return shell


def write_static_translations() -> int:
    """Render and write every FR static page. Returns count written."""
    n = 0
    for slug in STATIC_PAGES_FR:
        page = render_static_translation(slug)
        if page is None:
            print(f"build_translations: skip static '{slug}' — EN shell missing")
            continue
        dst = OUT / slug / "index.html"
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(page, encoding="utf-8")
        n += 1

    # Topic sub-pages — clone each /topics/<topic>/ as /fr/topics/<topic>/.
    # build_topics.py emits the EN versions before us; we fork + translate.
    topics_dir = PUBLIC / "topics"
    if topics_dir.is_dir():
        for topic_dir in sorted(topics_dir.iterdir()):
            if not topic_dir.is_dir():
                continue
            src = topic_dir / "index.html"
            if not src.is_file():
                continue
            page = _render_topic_subpage_fr(topic_dir.name, src.read_text(encoding="utf-8"))
            dst = OUT / "topics" / topic_dir.name / "index.html"
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(page, encoding="utf-8")
            n += 1

    return n


# Per-topic French title + lede. Mirrors scripts/build_topics.py:TOPICS.
TOPIC_FR_LABELS: dict[str, dict[str, str]] = {
    "post-quantum-cryptography": {
        "title": "Cryptographie post-quantique",
        "lede": "Cryptographie sur réseaux euclidiens, normes NIST PQC, paiements résistants au quantique et menace « récolter maintenant, déchiffrer plus tard ». Notes de recherche, bibliothèques open source et playbooks de migration pour les équipes sécurité des services financiers.",
    },
    "iso-20022-payments": {
        "title": "ISO 20022 & Paiements",
        "lede": "Migration des messages transfrontaliers, conformité d'adresse structurée, SEPA Instant, SWIFT gpi et les rails de paiement wholesale qui portent l'ensemble. Outils, playbooks et calendrier réglementaire.",
    },
    "applied-ai-banking": {
        "title": "IA appliquée à la banque",
        "lede": "IA générative, LLM multimodaux, voix et modèles de parole — et comment ils redessinent les opérations bancaires, le service client et l'ingénierie produit dans les institutions de premier rang.",
    },
    "rust-open-source": {
        "title": "Rust & Open Source",
        "lede": "Bibliothèques Rust open source que j'écris et maintiens : journalisation, génération de code, date-heure, primitives cryptographiques, KEM basé sur Kyber, et un générateur de sites statiques Rust.",
    },
    "blockchain-digital-assets": {
        "title": "Blockchain & Actifs numériques",
        "lede": "Blockchain et actifs numériques : tokenisation, ERC-20, stablecoins, infrastructure cryptomonnaies, et le cadre réglementaire qui les façonne.",
    },
}


def _render_topic_subpage_fr(topic_slug: str, shell: str) -> str:
    """Fork an EN /topics/<slug>/ page into /fr/topics/<slug>/."""
    cfg = TOPIC_FR_LABELS.get(topic_slug, {
        "title": topic_slug.replace("-", " ").title(),
        "lede": "",
    })
    title = cfg["title"]
    lede = cfg["lede"]
    page_title = f"{title} — Sebastien Rousseau"
    url_fr = f"{BASE}/fr/topics/{topic_slug}/"

    shell = _HTML_LANG_RE.sub(r'\1fr-FR\2', shell, count=1)
    shell = _TITLE_RE.sub(f'<title>{_html.escape(page_title)}</title>', shell, count=1)
    if lede:
        shell = _DESC_META_RE.sub(rf'\1{_html.escape(lede, quote=True)}\2', shell, count=1)
        shell = _OG_DESC_RE.sub(rf'\1{_html.escape(lede, quote=True)}\2', shell, count=1)
    shell = _OG_TITLE_RE.sub(rf'\1{_html.escape(page_title, quote=True)}\2', shell, count=1)
    shell = _OG_URL_RE.sub(rf'\1{url_fr}\2', shell, count=1)
    shell = _OG_LOCALE_RE.sub(r'\1fr_FR\2', shell, count=1)
    shell = _CANONICAL_RE.sub(rf'\1{url_fr}\2', shell, count=1)
    shell = _TW_TITLE_RE.sub(rf'\1{_html.escape(page_title, quote=True)}\2', shell, count=1)
    if lede:
        shell = _TW_DESC_RE.sub(rf'\1{_html.escape(lede, quote=True)}\2', shell, count=1)

    # Rewrite article cards (EN slugs → FR slugs).
    shell = rewrite_en_urls(shell)

    # Translate the topic H1 + lede in the body if present.
    # Pattern from build_topics.py: <h1>{TITLE}</h1>...<p class="topic-lede">{LEDE}</p>
    shell = re.sub(
        r'<h1>[^<]+</h1>',
        f'<h1>{_html.escape(title)}</h1>',
        shell,
        count=1,
    )
    if lede:
        shell = re.sub(
            r'(<p class="topic-lede">)[^<]+(</p>)',
            rf'\1{_html.escape(lede)}\2',
            shell,
            count=1,
        )
    # Breadcrumb in body: "Home · Topics · Title" → "Accueil · Sujets · Titre"
    shell = re.sub(
        r'<nav aria-label="Breadcrumb" class="topic-breadcrumb">[\s\S]*?</nav>',
        f'<nav aria-label="Fil d\'Ariane" class="topic-breadcrumb">'
        f'<a href="/fr/">Accueil</a> &middot; '
        f'<a href="/fr/topics/index.html">Sujets</a> &middot; '
        f'<span>{_html.escape(title)}</span></nav>',
        shell,
        count=1,
    )
    # Topics-page lede on the hub
    shell = re.sub(
        r'Curated topic clusters[^<]+',
        "Clusters de sujets curated — choisissez un fil et suivez-le à travers l'archive.",
        shell,
    )
    shell = re.sub(
        r'PILLARS', 'PILIERS', shell,
    )
    shell = re.sub(
        r'>Topics</h1>', '>Sujets</h1>', shell,
    )
    shell = re.sub(
        r'PILLAR · TOPIC', 'PILIER · SUJET', shell,
    )
    shell = re.sub(
        r'(\d+) article\(s\)', r'\1 article(s)', shell,
    )

    # Patch JSON-LD breadcrumb + URLs to point to /fr/topics/.
    def patch_jsonld(m: re.Match[str]) -> str:
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
                    node["inLanguage"] = "fr"
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
                        item["item"] = f"{BASE}/fr/topics/"
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
            + '</script>'
        )

    shell = re.sub(
        r'<script type="application/ld\+json">([\s\S]+?)</script>',
        patch_jsonld,
        shell,
    )

    # Chrome localisation
    shell = translate_chrome(shell)
    shell = rewrite_fr_link_titles(shell)
    shell = rewrite_newsroom_card_titles(shell)
    shell = rewrite_en_titles_in_text(shell)
    shell = rewrite_en_descs_in_text(shell)
    # Feed links
    shell = re.sub(
        r'href="(?:https?://[^/"]+)?/atom\.xml"',
        'href="/fr/atom.xml"',
        shell,
    )
    shell = re.sub(
        r'href="(?:https?://[^/"]+)?/rss\.xml"',
        'href="/fr/rss.xml"',
        shell,
    )
    return shell


def main() -> None:
    if not SRC.is_dir():
        print("build_translations: _posts/fr not found — nothing to do")
        return
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
        entries.append({
            "slug": slug_fr,
            "en_slug": en,
            "title": fm.get("title", ""),
            "description": fm.get("description", ""),
            "date": fm.get("date", ""),
            "keywords": fm.get("keywords", ""),
            "banner": fm.get("banner", "https://cloudcdn.pro/stocks/images/sebastien-rousseau.png"),
            "banner_alt": fm.get("banner_alt", fm.get("title", "")),
        })
        written += 1

    if entries:
        # Sort newest first to mirror the English /articles/ ordering.
        entries.sort(key=lambda e: e["slug"], reverse=True)
        hub = render_hub(entries)
        if hub:
            (OUT / "index.html").write_text(hub, encoding="utf-8")
            written += 1

    # Static-page mirrors (about, papers, projects, topics, tags,
    # contact, accessibility, privacy, terms, …) — keep FR visitors
    # inside /fr/ when they click any nav or footer link.
    static_written = write_static_translations()
    written += static_written

    # FR search index — visible text of every FR page, loaded by the
    # Shokunin search palette when the visitor is in /fr/.
    search_entries = _build_fr_search_index()
    (OUT / "search-index.json").write_text(
        _json.dumps({"entries": search_entries}, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )

    print(
        f"build_translations: wrote {written} page(s) "
        f"({len(entries)} translation(s) + hub + {static_written} static page(s)) "
        f"+ FR search index ({len(search_entries)} entries)"
    )


# ---------------------------------------------------------------------------
# FR search index
# ---------------------------------------------------------------------------

_TAG_RE = re.compile(r'<[^>]+>')
_WHITESPACE_RE = re.compile(r'\s+')
_TITLE_TAG_RE = re.compile(r'<title>([^<]+)</title>', re.IGNORECASE)
_MAIN_TAG_RE = re.compile(r'<main\b[\s\S]*?</main>', re.IGNORECASE)


def _extract_visible_text(html: str) -> str:
    """Strip every tag inside <main>, collapse whitespace, return plain text."""
    m = _MAIN_TAG_RE.search(html)
    body = m.group(0) if m else html
    # Drop <script> and <style> blocks first.
    body = re.sub(r'<script[\s\S]*?</script>', ' ', body, flags=re.IGNORECASE)
    body = re.sub(r'<style[\s\S]*?</style>', ' ', body, flags=re.IGNORECASE)
    # Drop HTML comments.
    body = re.sub(r'<!--[\s\S]*?-->', ' ', body)
    text = _TAG_RE.sub(' ', body)
    text = _html.unescape(text)
    return _WHITESPACE_RE.sub(' ', text).strip()


def _build_fr_search_index() -> list[dict[str, str]]:
    """Walk public/fr/ for rendered HTML and build search entries."""
    entries: list[dict[str, str]] = []
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
        entries.append({"title": title, "url": url, "content": text})
    return entries


if __name__ == "__main__":
    main()
