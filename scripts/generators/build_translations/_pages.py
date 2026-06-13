"""Listing / static-page renderers: articles hub, home page, static-page
mirrors and topic sub-pages."""

from __future__ import annotations

import html as _html
import re

from . import _state as st
from ._chrome import (
    _CANONICAL_RE,
    _DESC_META_RE,
    _HERO_RE,
    _KW_META_RE,
    _OG_DESC_RE,
    _OG_LOCALE_RE,
    _OG_TITLE_RE,
    _OG_URL_RE,
    _TITLE_RE,
    _TW_DESC_RE,
    _TW_TITLE_RE,
    _localize_inlanguage_globally,
    _patch_jsonld_scripts,
    _set_html_lang,
    localize_feed_links,
    translate_chrome,
)
from ._maps import (
    rewrite_en_descs_in_text,
    rewrite_en_titles_in_text,
    rewrite_en_urls,
    rewrite_fr_link_titles,
    rewrite_newsroom_card_titles,
)

# ---------------------------------------------------------------------------
# Hub: /fr/articles/
# ---------------------------------------------------------------------------

_NEWSROOM_RE = re.compile(r'<section class="newsroom">[\s\S]*?</section>', re.IGNORECASE)
_LDJSON_RE = re.compile(r'<script type="application/ld\+json">[\s\S]*?</script>', re.IGNORECASE)


def render_articles_hub(entries: list[dict[str, str]]) -> str | None:
    """Articles listing — French equivalent of /articles/. Forks the
    rendered /articles/ page as shell and writes to /fr/articles/."""
    shell_src = st.PUBLIC / "articles" / "index.html"
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
    feat_url = f"/{st.LANG_CODE}/{featured['slug']}/index.html"
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
    _h = _hub_strings.get(st.LANG_CODE, _hub_strings["fr"])
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
        url = f"/{st.LANG_CODE}/{e['slug']}/index.html"
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
    title = _articles_hub_titles.get(st.LANG_CODE, _articles_hub_titles["fr"])
    desc = _h["desc"]
    shell = _TITLE_RE.sub(f"<title>{_html.escape(title)}</title>", shell, count=1)
    shell = _DESC_META_RE.sub(rf"\g<1>{_html.escape(desc, quote=True)}\g<2>", shell, count=1)
    shell = _OG_TITLE_RE.sub(rf"\g<1>{_html.escape(title, quote=True)}\g<2>", shell, count=1)
    shell = _OG_DESC_RE.sub(rf"\g<1>{_html.escape(desc, quote=True)}\g<2>", shell, count=1)
    _articles_slug_lang = st.STATIC_SLUG_FR.get("articles", "articles")
    _hub_url = f"https://sebastienrousseau.com/{st.LANG_CODE}/{_articles_slug_lang}/"
    shell = _OG_URL_RE.sub(rf"\g<1>{_hub_url}\g<2>", shell, count=1)
    shell = _OG_LOCALE_RE.sub(rf"\g<1>{st.LANG_LOCALE}\g<2>", shell, count=1)
    shell = _CANONICAL_RE.sub(rf"\g<1>{_hub_url}\g<2>", shell, count=1)
    shell = translate_chrome(shell)
    # Reciprocal hreflang for the language selector.
    shell = re.sub(
        r'<link rel="alternate"[^>]+hreflang="[^"]+"[^>]*/>',
        "",
        shell,
    )
    hreflang_block = (
        f'<link rel="alternate" hreflang="en" href="{st.BASE}/articles/" />'
        f'<link rel="alternate" hreflang="{st.LANG_CODE}" href="{st.BASE}/{st.LANG_CODE}/{_articles_slug_lang}/" />'
        f'<link rel="alternate" hreflang="x-default" href="{st.BASE}/articles/" />'
    )
    shell = shell.replace("</head>", hreflang_block + "</head>", 1)
    shell = _localize_inlanguage_globally(shell, st.LANG_CODE)
    return shell


# ---------------------------------------------------------------------------
# Home: /fr/index.html — forks the EN /index.html shell so the FR home
# carries the same hero / projects / quote / latest / experience sections.
# ---------------------------------------------------------------------------


def render_home() -> str | None:  # noqa: C901 — orchestrates the FR home fork end-to-end
    """Fork ``public/index.html`` (the EN home) to produce
    ``public/fr/index.html`` so the FR landing page mirrors the EN
    structure (hero + projects + quote + paper + latest + experience).
    """
    shell_src = st.PUBLIC / "index.html"
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
    title = _home_titles.get(st.LANG_CODE, _home_titles["fr"])
    desc = _home_descs.get(st.LANG_CODE, _home_descs["fr"])
    url_fr = f"{st.BASE}/{st.LANG_CODE}/"

    shell = _set_html_lang(shell)
    shell = _TITLE_RE.sub(f"<title>{_html.escape(title)}</title>", shell, count=1)
    shell = _DESC_META_RE.sub(rf"\g<1>{_html.escape(desc, quote=True)}\g<2>", shell, count=1)
    shell = _OG_TITLE_RE.sub(rf"\g<1>{_html.escape(title, quote=True)}\g<2>", shell, count=1)
    shell = _OG_DESC_RE.sub(rf"\g<1>{_html.escape(desc, quote=True)}\g<2>", shell, count=1)
    shell = _OG_URL_RE.sub(rf"\g<1>{url_fr}\g<2>", shell, count=1)
    shell = _OG_LOCALE_RE.sub(rf"\g<1>{st.LANG_LOCALE}\g<2>", shell, count=1)
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
    for pat, repl in st._HOME_FR_COMPILED:
        shell = pat.sub(repl, shell)

    # Card titles + tooltips for any article link.
    shell = rewrite_fr_link_titles(shell)
    shell = rewrite_newsroom_card_titles(shell)

    # Localise feed links.
    shell = localize_feed_links(shell)

    # Patch JSON-LD WebSite / Person / breadcrumb on the home page.
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
                node["inLanguage"] = st.LANG_CODE
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
                node["inLanguage"] = st.LANG_CODE
                local = True
        return local

    shell = _patch_jsonld_scripts(shell, patch_node)

    # Reciprocal hreflang so the language selector finds the EN home.
    shell = re.sub(
        r'<link rel="alternate"[^>]+hreflang="[^"]+"[^>]*/>',
        "",
        shell,
    )
    hreflang_block = (
        f'<link rel="alternate" hreflang="en" href="{st.BASE}/" />'
        f'<link rel="alternate" hreflang="{st.LANG_CODE}" href="{url_fr}" />'
        f'<link rel="alternate" hreflang="x-default" href="{st.BASE}/" />'
    )
    shell = shell.replace("</head>", hreflang_block + "</head>", 1)
    shell = _localize_inlanguage_globally(shell, st.LANG_CODE)

    return shell


# ---------------------------------------------------------------------------
# Static-page translations (about, papers, projects, topics, tags, …)
# ---------------------------------------------------------------------------

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
    cfg = st.STATIC_PAGES_FR.get(slug)
    if cfg is None:
        return None
    shell_src = st.PUBLIC / slug / "index.html"
    if not shell_src.is_file():
        return None
    shell = shell_src.read_text(encoding="utf-8")

    title = cfg["title"]
    description = cfg["description"]
    subtitle = cfg.get("subtitle", description)
    keywords = cfg.get("keywords", "")
    fr_slug_str = st.STATIC_SLUG_FR.get(slug, slug)
    url_fr = f"{st.BASE}/{st.LANG_CODE}/{fr_slug_str}/"

    shell = _set_html_lang(shell)
    shell = _TITLE_RE.sub(f"<title>{_html.escape(title)}</title>", shell, count=1)
    shell = _DESC_META_RE.sub(rf"\g<1>{_html.escape(description, quote=True)}\g<2>", shell, count=1)
    if keywords:
        shell = _KW_META_RE.sub(rf"\g<1>{_html.escape(keywords, quote=True)}\g<2>", shell, count=1)
    shell = _OG_TITLE_RE.sub(rf"\g<1>{_html.escape(title, quote=True)}\g<2>", shell, count=1)
    shell = _OG_DESC_RE.sub(rf"\g<1>{_html.escape(description, quote=True)}\g<2>", shell, count=1)
    shell = _OG_URL_RE.sub(rf"\g<1>{url_fr}\g<2>", shell, count=1)
    shell = _OG_LOCALE_RE.sub(rf"\g<1>{st.LANG_LOCALE}\g<2>", shell, count=1)
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
    fr_body = st.STATIC_BODIES_FR.get(slug)
    if fr_body:
        shell = _replace_static_main_body(shell, fr_body)

    # EN title + description substitutions FIRST — before chrome runs
    # localize_en_dates() (which would otherwise rewrite "August 2026" →
    # "août 2026" inside an EN description and break the verbatim match).
    shell = rewrite_en_titles_in_text(shell)
    shell = rewrite_en_descs_in_text(shell)

    # Localise chrome (nav / footer / search / aria) + body text.
    shell = translate_chrome(shell)
    for pat, repl in st._STATIC_BODY_COMPILED:
        shell = pat.sub(repl, shell)

    # Rewrite article-card titles + tooltips on listing pages
    # (papers, projects, tags, topic hub, …) to the FR title.
    shell = rewrite_fr_link_titles(shell)
    shell = rewrite_newsroom_card_titles(shell)

    # Localise feed links.
    shell = localize_feed_links(shell)

    # Patch the WebPage / WebSite JSON-LD's @id, url, name, description.
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
                node["inLanguage"] = st.LANG_CODE
                local = True
        if t == "BreadcrumbList":
            items = node.get("itemListElement", [])
            for item in items:
                if not isinstance(item, dict):
                    continue
                pos = item.get("position")
                if pos == 1:
                    item["name"] = st.I18N_FR.get("Home", "Home")
                    item["item"] = f"{st.BASE}/"
                    local = True
                elif pos == 2:
                    item["name"] = title.split(" — ")[0]
                    item["item"] = url_fr
                    local = True
        return local

    shell = _patch_jsonld_scripts(shell, patch_node)

    # Reciprocal hreflang — strip stale links and emit fresh ones so the
    # language selector's JS resolves 🇬🇧 English to the EN counterpart.
    # Must run AFTER translate_chrome (which calls rewrite_static_links
    # and would rewrite an EN absolute URL → /fr/<slug>/).
    shell = re.sub(
        r'<link rel="alternate"[^>]+hreflang="[^"]+"[^>]*/>',
        "",
        shell,
    )
    en_url = f"{st.BASE}/{slug}/"
    hreflang_block = (
        f'<link rel="alternate" hreflang="en" href="{en_url}" />'
        f'<link rel="alternate" hreflang="{st.LANG_CODE}" href="{url_fr}" />'
        f'<link rel="alternate" hreflang="x-default" href="{en_url}" />'
    )
    shell = shell.replace("</head>", hreflang_block + "</head>", 1)
    shell = _localize_inlanguage_globally(shell, st.LANG_CODE)

    return shell


def write_static_translations() -> int:
    """Render and write every FR static page. Returns count written."""
    n = 0
    for slug in st.STATIC_PAGES_FR:
        page = render_static_translation(slug)
        if page is None:
            print(f"build_translations: skip static '{slug}' — EN shell missing")
            continue
        fr_slug_str = st.STATIC_SLUG_FR.get(slug, slug)
        dst = st.OUT / fr_slug_str / "index.html"
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(page, encoding="utf-8")
        n += 1

    # Topic sub-pages — clone each /topics/<topic>/ as /<lang>/<topics_slug>/<topic>/.
    # build_topics.py emits the EN versions before us; we fork + translate.
    topics_dir = st.PUBLIC / "topics"
    if topics_dir.is_dir():
        topics_slug_lang = st.STATIC_SLUG_FR.get("topics", "topics")
        for topic_dir in sorted(topics_dir.iterdir()):
            if not topic_dir.is_dir():
                continue
            src = topic_dir / "index.html"
            if not src.is_file():
                continue
            page = _render_topic_subpage_fr(topic_dir.name, src.read_text(encoding="utf-8"))
            dst = st.OUT / topics_slug_lang / topic_dir.name / "index.html"
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(page, encoding="utf-8")
            n += 1

    return n


def _render_topic_subpage_fr(topic_slug: str, shell: str) -> str:  # noqa: C901 — topic-page chrome patches
    """Fork an EN /topics/<slug>/ page into /fr/sujets/<slug>/."""
    cfg = st.TOPIC_FR_LABELS.get(
        topic_slug,
        {
            "title": topic_slug.replace("-", " ").title(),
            "lede": "",
        },
    )
    title = cfg["title"]
    lede = cfg["lede"]
    page_title = f"{title} — Sebastien Rousseau"
    topics_slug_lang = st.STATIC_SLUG_FR.get("topics", "topics")
    url_fr = f"{st.BASE}/{st.LANG_CODE}/{topics_slug_lang}/{topic_slug}/"

    shell = _set_html_lang(shell)
    shell = _TITLE_RE.sub(f"<title>{_html.escape(page_title)}</title>", shell, count=1)
    if lede:
        shell = _DESC_META_RE.sub(rf"\g<1>{_html.escape(lede, quote=True)}\g<2>", shell, count=1)
        shell = _OG_DESC_RE.sub(rf"\g<1>{_html.escape(lede, quote=True)}\g<2>", shell, count=1)
    shell = _OG_TITLE_RE.sub(rf"\g<1>{_html.escape(page_title, quote=True)}\g<2>", shell, count=1)
    shell = _OG_URL_RE.sub(rf"\g<1>{url_fr}\g<2>", shell, count=1)
    shell = _OG_LOCALE_RE.sub(rf"\g<1>{st.LANG_LOCALE}\g<2>", shell, count=1)
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
        f'<a href="/{st.LANG_CODE}/">Accueil</a> &middot; '
        f'<a href="/{st.LANG_CODE}/{st.STATIC_SLUG_FR.get("topics", "topics")}/index.html">Sujets</a> &middot; '
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
                node["inLanguage"] = st.LANG_CODE
                local = True
        if t == "BreadcrumbList":
            for item in node.get("itemListElement", []):
                if not isinstance(item, dict):
                    continue
                pos = item.get("position")
                if pos == 1:
                    item["name"] = st.I18N_FR.get("Home", "Home")
                    item["item"] = f"{st.BASE}/"
                    local = True
                elif pos == 2:
                    item["name"] = "Sujets"
                    item["item"] = (
                        f"{st.BASE}/{st.LANG_CODE}/{st.STATIC_SLUG_FR.get('topics', 'topics')}/"
                    )
                    local = True
                elif pos == 3:
                    item["name"] = title
                    item["item"] = url_fr
                    local = True
        return local

    shell = _patch_jsonld_scripts(shell, patch_node)

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
    en_url = f"{st.BASE}/topics/{topic_slug}/"
    hreflang_block = (
        f'<link rel="alternate" hreflang="en" href="{en_url}" />'
        f'<link rel="alternate" hreflang="{st.LANG_CODE}" href="{url_fr}" />'
        f'<link rel="alternate" hreflang="x-default" href="{en_url}" />'
    )
    shell = shell.replace("</head>", hreflang_block + "</head>", 1)
    # Feed links
    shell = localize_feed_links(shell)
    shell = _localize_inlanguage_globally(shell, st.LANG_CODE)
    return shell
