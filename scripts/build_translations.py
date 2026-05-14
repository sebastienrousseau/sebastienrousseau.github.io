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


def _french_body(body_html: str, description: str, lead_aside: str, related_aside: str) -> str:
    today = _date_today()
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
    body_html = rewrite_en_urls(body_html)
    # main body — built fresh in French (lead + body + author-card + reviewed + related)
    fr_body = _french_body(body_html, description, lead_aside, related_aside)

    def replace_main(m: re.Match[str]) -> str:
        return m.group(1) + fr_body + m.group(3)

    shell = _MAIN_BODY_RE.sub(replace_main, shell, count=1)

    # Chrome translation — nav, footer, search palette, social labels, etc.
    shell = translate_chrome(shell)

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
STATIC_BODY_PATCHES: list[tuple[str, str]] = [
    # Topic hub breadcrumb + headings
    (r'<a href="/">Home</a> &middot; <span>Topics</span>',
     '<a href="/fr/">Accueil</a> &middot; <span>Sujets</span>'),
    (r'>Home<', '>Accueil<'),
    (r'>Topics</h1>', '>Sujets</h1>'),
    (r'>PILLARS</p>', '>PILIERS</p>'),
    (r'PILLAR · TOPIC', 'PILIER · SUJET'),
    (r'Curated topic clusters[^<]+',
     "Clusters de sujets — choisissez un fil et suivez-le à travers l'archive."),
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
    shell = _CANONICAL_RE.sub(rf'\1{url_fr}\2', shell, count=1)

    # Rewrite EN article URLs inside the body to FR counterparts.
    shell = rewrite_en_urls(shell)

    # Localise chrome (nav / footer / search / aria) + body text.
    shell = translate_chrome(shell)
    for pat, repl in _STATIC_BODY_COMPILED:
        shell = pat.sub(repl, shell)

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
