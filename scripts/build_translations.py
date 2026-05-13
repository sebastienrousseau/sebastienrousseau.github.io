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
from pathlib import Path

from markdown_it import MarkdownIt

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


def _french_lead(description: str) -> str:
    if not description:
        return ""
    return (
        '<aside class="post-lead" aria-label="Résumé de l\'article">'
        f'<p class="post-lead-tldr"><strong>TL;DR.</strong> {_html.escape(description)}</p>'
        '</aside>'
    )


def _french_body(body_html: str, description: str) -> str:
    today = _date_today()
    lead = _french_lead(description)
    review = (
        f'<p class="post-reviewed">Dernière révision '
        f'<time datetime="{today}">{today}</time>.</p>'
    )
    return lead + body_html + _french_author_card() + review


def _swap_breadcrumb(html: str, slug: str, title: str) -> str:
    """Patch the BreadcrumbList JSON-LD on the page to point at /fr/{slug}/."""
    def fix(m: re.Match[str]) -> str:
        try:
            data = _json.loads(m.group(1))
        except _json.JSONDecodeError:
            return m.group(0)
        if isinstance(data, dict) and data.get("@type") == "BreadcrumbList":
            for item in data.get("itemListElement", []):
                if isinstance(item, dict) and item.get("position") == 3:
                    item["name"] = title
                    item["item"] = f"{BASE}/fr/{slug}/"
            return '<script type="application/ld+json">' + _json.dumps(data, separators=(",", ":"), ensure_ascii=False) + '</script>'
        return m.group(0)
    return re.sub(
        r'<script type="application/ld\+json">(\{[\s\S]*?"BreadcrumbList"[\s\S]*?\})</script>',
        fix,
        html,
        count=1,
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
    url_fr = f"{BASE}/fr/{slug}/"

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

    # main body — built fresh in French (TL;DR + body + author-card + reviewed)
    fr_body = _french_body(body_html, description)

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
    shell = _swap_breadcrumb(shell, slug, title)

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

    cards: list[str] = []
    for e in entries:
        url = f"/fr/{e['slug']}/index.html"
        cards.append(
            '<article class="newsroom-card">'
            f'<a class="newsroom-card-media" href="{url}" title="{_html.escape(e["title"], quote=True)}">'
            f'<img alt="{_html.escape(e["banner_alt"], quote=True)}" src="{e["banner"]}" loading="lazy" decoding="async" width="600" height="600" />'
            '</a>'
            '<div class="newsroom-card-body">'
            f'<h3><a href="{url}">{_html.escape(e["title"])}</a></h3>'
            f'<p class="newsroom-excerpt">{_html.escape(e["description"])}</p>'
            '</div>'
            '</article>'
        )
    body = (
        '<section class="newsroom">'
        '<nav aria-label="Fil d\'Ariane" class="topic-breadcrumb">'
        '<a href="/">Accueil</a> &middot; <span>Articles (FR)</span></nav>'
        '<header class="newsroom-section-head">'
        '<p class="newsroom-kicker">VERSION FRANÇAISE</p>'
        '<h1>Articles en français</h1>'
        '<p class="topic-lede">Traductions manuelles d\'une sélection d\'articles. '
        f'{len(entries)} article(s) disponible(s).</p>'
        '</header>'
        '<div class="newsroom-grid">' + "".join(cards) + '</div>'
        '</section>'
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
        page = render_translation(md.stem, fm, body)
        if page is None:
            continue
        dst = OUT / md.stem / "index.html"
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(page, encoding="utf-8")
        entries.append({
            "slug": md.stem,
            "title": fm.get("title", ""),
            "description": fm.get("description", ""),
            "banner": fm.get("banner", "https://cloudcdn.pro/stocks/images/sebastien-rousseau.png"),
            "banner_alt": fm.get("banner_alt", fm.get("title", "")),
        })
        written += 1

    if entries:
        hub = render_hub(entries)
        if hub:
            (OUT / "index.html").write_text(hub, encoding="utf-8")
            written += 1
    print(f"build_translations: wrote {written} page(s) ({len(entries)} translation(s) + hub if any)")


if __name__ == "__main__":
    main()
