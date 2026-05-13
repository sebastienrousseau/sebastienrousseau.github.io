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

    # Nav menu items
    (r'<li><a href="/about/index\.html">About</a></li>',
     '<li><a href="/about/index.html">À propos</a></li>'),
    (r'<li><a href="/papers/index\.html">Papers</a></li>',
     '<li><a href="/papers/index.html">Publications</a></li>'),
    (r'<li><a href="/topics/index\.html">Topics</a></li>',
     '<li><a href="/topics/index.html">Sujets</a></li>'),
    (r'<li><a href="/projects/index\.html">Projects</a></li>',
     '<li><a href="/projects/index.html">Projets</a></li>'),
    (r'<li><a href="/articles/index\.html">Articles</a></li>',
     '<li><a href="/fr/index.html">Articles</a></li>'),
    (r'<li><a href="/contact/index\.html">Contact</a></li>',
     '<li><a href="/contact/index.html">Contact</a></li>'),

    # Back-to-top
    (r'aria-label="Back to top"', 'aria-label="Retour en haut"'),

    # Footer column titles
    (r'<h2 class="ap-foot-title">Writing</h2>', '<h2 class="ap-foot-title">Écrits</h2>'),
    (r'<h2 class="ap-foot-title">Work</h2>', '<h2 class="ap-foot-title">Activité</h2>'),
    (r'<h2 class="ap-foot-title">Reach</h2>', '<h2 class="ap-foot-title">Réseaux</h2>'),

    # Footer links — surgical, scoped by href
    (r'<a href="/about/index\.html">About</a>', '<a href="/about/index.html">À propos</a>'),
    (r'<a href="/made-with-static-site-generator/index\.html">Made with Static Site Generator</a>',
     '<a href="/made-with-static-site-generator/index.html">Conçu avec Static Site Generator</a>'),
    (r'<a href="/papers/index\.html">Papers</a>', '<a href="/papers/index.html">Publications</a>'),
    (r'<a href="/tags/index\.html">Tags</a>', '<a href="/tags/index.html">Étiquettes</a>'),
    (r'<a href="/projects/index\.html">Projects</a>', '<a href="/projects/index.html">Projets</a>'),

    # Social section
    (r'aria-label="Social links"', 'aria-label="Liens sociaux"'),
    (r'aria-label="Sebastien Rousseau on ', 'aria-label="Sebastien Rousseau sur '),

    # Footer legal links
    (r'<a href="/accessibility/index\.html">Accessibility</a>',
     '<a href="/accessibility/index.html">Accessibilité</a>'),
    (r'<a href="/privacy/index\.html">Privacy</a>',
     '<a href="/privacy/index.html">Confidentialité</a>'),
    (r'<a href="/terms/index\.html">Terms</a>',
     '<a href="/terms/index.html">Conditions</a>'),

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

    # JSON-LD BlogPosting tweaks
    shell = _BLOGPOSTING_HEADLINE_RE.sub(rf'\1{_html.escape(title, quote=True)}\2', shell, count=1)
    shell = _BLOGPOSTING_DESC_RE.sub(rf'\1{_html.escape(description, quote=True)}\2', shell, count=1)
    shell = _BLOGPOSTING_LANG_RE.sub(r'\1fr\2', shell, count=1)
    shell = _BLOGPOSTING_URL_RE.sub(rf'\1{url_fr}\2', shell, count=1)

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
    print(f"build_translations: wrote {written} page(s) ({len(entries)} translation(s) + hub if any)")


if __name__ == "__main__":
    main()
