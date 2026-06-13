#!/usr/bin/env python3
"""Paged article listing generator — `/articles/`, `/articles/page/N/`.

Runs after ssg, before build_translations + postbuild. Reads all
dated posts under ``_posts/`` (slug starts ``YYYY-MM-DD-``), sorts by
date descending, chunks into pages of 24, and writes:

  - ``public/articles/index.html``        — page 1 (rewritten from
                                            the ssg-produced cover)
  - ``public/articles/page/N/index.html`` — N >= 2

For each non-English locale, the same structure is replicated under
``public/<lang>/<localised-articles>/page/N/index.html``, using the
``static.articles`` slug from ``_data/i18n/<lang>/slugs.json``
(e.g. fr → articles, ja → kiji, ar → maqalat, …).

Each page renders:

  - Hero with title "Articles" + page-N-of-M label
  - Responsive card grid of 24 article cards
  - Pagination nav (Prev / numbered / Next)

Template skeleton comes from the ssg-emitted
``public/articles/index.html`` — the same approach
``build_tag_landings.py`` uses. The hero ``.ap-hero`` block is
stripped to keep exactly one ``<h1>`` per page (AAA).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
POSTS = ROOT / "_posts"
TEMPLATE_PATH = PUBLIC / "articles" / "index.html"

PAGE_SIZE = 24
_BASE_URL = "https://sebastienrousseau.com"

_TITLE_FM_RE = re.compile(r'^title:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)
_EXCERPT_FM_RE = re.compile(r'^excerpt:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)
_DATED_SLUG_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-(.+)$")
_MAIN_RE = re.compile(r'(<main\b[^>]*>)([\s\S]*?)(</main>)', re.IGNORECASE)
_AP_HERO_BLOCK_RE = re.compile(
    r'<section class="ap-hero">[\s\S]*?</section>', re.IGNORECASE
)
_HTML_LANG_RE = re.compile(r'<html lang="[^"]*"', re.IGNORECASE)
_TITLE_RE = re.compile(r"<title>[^<]*</title>", re.IGNORECASE)
_DESC_RE = re.compile(r'<meta name="description" content="[^"]*"', re.IGNORECASE)
_CANONICAL_RE = re.compile(r'<link rel="canonical" href="[^"]*"', re.IGNORECASE)
_OG_TITLE_RE = re.compile(r'<meta property="og:title" content="[^"]*"', re.IGNORECASE)
_OG_DESC_RE = re.compile(r'<meta property="og:description" content="[^"]*"', re.IGNORECASE)
_OG_URL_RE = re.compile(r'<meta property="og:url" content="[^"]*"', re.IGNORECASE)
_INLANG_RE = re.compile(r'"inLanguage":\s*"(?:en|en-GB|en-US)"')
_HREFLANG_ARTICLE_RE = re.compile(r'href="/(\d{4}-\d{2}-\d{2}-[^/"]+)/"')

LOCALES_NON_EN = (
    "ar", "bn", "cs", "de", "es", "fil", "fr", "ha", "he", "hi",
    "id", "it", "ja", "ko", "nl", "pl", "pt-br", "ro", "ru", "sv",
    "th", "tr", "uk", "vi", "yo", "zh-hans", "zh-hant",
)


def _esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#x27;")
    )


def _walk_posts() -> list[tuple[str, str, str, str]]:
    """Return [(title, iso-date, slug, excerpt), …] for every dated post,
    newest first."""
    out: list[tuple[str, str, str, str]] = []
    for path in sorted(POSTS.glob("*.md")):
        stem_m = _DATED_SLUG_RE.match(path.stem)
        if not stem_m:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        title_m = _TITLE_FM_RE.search(text)
        excerpt_m = _EXCERPT_FM_RE.search(text)
        out.append(
            (
                title_m.group(1) if title_m else path.stem,
                stem_m.group(1),
                path.stem,
                excerpt_m.group(1) if excerpt_m else "",
            )
        )
    out.sort(key=lambda p: p[1], reverse=True)
    return out


def _load_static_slug(lang: str, key: str, default: str) -> str:
    """Return ``static.<key>`` from a locale's slugs.json, with default."""
    path = ROOT / "_data" / "i18n" / lang / "slugs.json"
    if not path.is_file():
        return default
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default
    return (data.get("static") or {}).get(key) or default


def _load_locale_article_slugs(lang: str) -> dict[str, str]:
    path = ROOT / "_data" / "i18n" / lang / "slugs.json"
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    arts = data.get("articles") or {}
    return {k: v for k, v in arts.items() if isinstance(v, str) and v}


def _render_card(title: str, iso_date: str, slug: str, excerpt: str) -> str:
    excerpt_html = (
        f'<p class="card-excerpt">{_esc(excerpt)}</p>' if excerpt else ""
    )
    return (
        f'<article class="tag-landing-card">'
        f'<h2><a href="/{slug}/">{_esc(title)}</a></h2>'
        f'<time datetime="{iso_date}" class="card-date">{iso_date}</time>'
        f"{excerpt_html}"
        f"</article>"
    )


def _render_pagination(
    page: int, total_pages: int, base_path: str
) -> str:
    """Render a Prev/numbered/Next pagination nav. ``base_path`` is the
    URL prefix (no trailing slash) — e.g. ``/articles`` for EN or
    ``/fr/articles`` for FR locale. Page 1 lives at ``<base_path>/``;
    page N lives at ``<base_path>/page/N/``."""
    if total_pages <= 1:
        return ""

    def page_url(n: int) -> str:
        return f"{base_path}/" if n == 1 else f"{base_path}/page/{n}/"

    parts: list[str] = []
    if page > 1:
        parts.append(
            f'<a href="{page_url(page - 1)}" rel="prev" class="page-nav-prev">'
            "&larr; Previous"
            "</a>"
        )
    nums: list[str] = []
    for n in range(1, total_pages + 1):
        if n == page:
            nums.append(
                f'<span class="page-nav-num is-current" aria-current="page">{n}</span>'
            )
        else:
            nums.append(f'<a href="{page_url(n)}" class="page-nav-num">{n}</a>')
    parts.append(f'<span class="page-nav-pages">{"".join(nums)}</span>')
    if page < total_pages:
        parts.append(
            f'<a href="{page_url(page + 1)}" rel="next" class="page-nav-next">'
            "Next &rarr;"
            "</a>"
        )
    return (
        f'<nav class="page-nav" aria-label="Pagination">{"".join(parts)}</nav>'
    )


def _render_listing_body(
    page: int,
    total_pages: int,
    page_posts: list[tuple[str, str, str, str]],
    base_path: str,
    page_label: str,
    title: str,
) -> str:
    cards = "".join(_render_card(*p) for p in page_posts)
    pagination = _render_pagination(page, total_pages, base_path)
    return (
        f'<div class="wrap report-wrap">'
        f'<header class="tag-landing-hero">'
        f'<p class="eyebrow">ARCHIVE</p>'
        f"<h1>{_esc(title)}</h1>"
        f'<p class="tag-landing-meta">{page_label}</p>'
        f"</header>"
        f'<section class="tag-landing-list" aria-label="Article cards">'
        f"{cards}"
        f"</section>"
        f"{pagination}"
        f"</div>"
    )


def _swap_head(
    out: str,
    title: str,
    desc: str,
    canonical_url: str,
) -> str:
    out = _TITLE_RE.sub(f"<title>{_esc(title)}</title>", out, count=1)
    out = _DESC_RE.sub(
        f'<meta name="description" content="{_esc(desc)}"', out, count=1
    )
    out = _CANONICAL_RE.sub(
        f'<link rel="canonical" href="{canonical_url}"', out, count=1
    )
    out = _OG_TITLE_RE.sub(
        f'<meta property="og:title" content="{_esc(title)}"', out, count=1
    )
    out = _OG_DESC_RE.sub(
        f'<meta property="og:description" content="{_esc(desc)}"', out, count=1
    )
    out = _OG_URL_RE.sub(
        f'<meta property="og:url" content="{canonical_url}"', out, count=1
    )
    return out


def _render_page_html(
    template: str,
    page: int,
    total_pages: int,
    page_posts: list[tuple[str, str, str, str]],
    canonical_url: str,
    base_path: str,
    title: str,
) -> str:
    page_label = f"Page {page} of {total_pages}"
    desc = (
        f"Articles by Sebastien Rousseau on AI, payments, post-quantum "
        f"cryptography, and the technology of banking. {page_label}."
    )
    body = _render_listing_body(
        page, total_pages, page_posts, base_path, page_label, title
    )
    out = _swap_head(template, title, desc, canonical_url)
    out = _AP_HERO_BLOCK_RE.sub("", out, count=1)
    out = _MAIN_RE.sub(rf"\1{body}\3", out, count=1)
    return out


def _write_locale_page(
    en_html: str,
    lang: str,
    page: int,
    article_map: dict[str, str],
    locale_prefix: str,
    out_path: Path,
) -> None:
    """Rewrite an EN page into one locale variant: <html lang>,
    canonical, internal links, og:url, JSON-LD inLanguage."""
    out = en_html
    out = _HTML_LANG_RE.sub(f'<html lang="{lang}"', out, count=1)
    canonical = f"{_BASE_URL}/{lang}/{locale_prefix}/"
    if page > 1:
        canonical += f"page/{page}/"
    out = _CANONICAL_RE.sub(
        f'<link rel="canonical" href="{canonical}"', out, count=1
    )
    out = _OG_URL_RE.sub(
        f'<meta property="og:url" content="{canonical}"', out, count=1
    )

    def _swap_article(m: re.Match[str], _lang: str = lang, _amap: dict = article_map) -> str:
        en_slug = m.group(1)
        return f'href="/{_lang}/{_amap.get(en_slug, en_slug)}/"'

    out = _HREFLANG_ARTICLE_RE.sub(_swap_article, out)
    # The per-page pagination links (/articles/page/N/) → localised.
    out = out.replace('href="/articles/', f'href="/{lang}/{locale_prefix}/')
    out = _INLANG_RE.sub(f'"inLanguage":"{lang}"', out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(out, encoding="utf-8")


def _chunk(seq: list, size: int) -> list[list]:
    return [seq[i : i + size] for i in range(0, len(seq), size)]


def _write_listings() -> tuple[int, int]:
    if not TEMPLATE_PATH.is_file():
        print(
            f"build_listings: missing template {TEMPLATE_PATH}",
            file=sys.stderr,
        )
        return 0, 0
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    posts = _walk_posts()
    pages = _chunk(posts, PAGE_SIZE)
    total_pages = len(pages)
    en_pages: list[tuple[int, str]] = []
    for idx, page_posts in enumerate(pages, start=1):
        canonical = (
            f"{_BASE_URL}/articles/"
            if idx == 1
            else f"{_BASE_URL}/articles/page/{idx}/"
        )
        page_html = _render_page_html(
            template, idx, total_pages, page_posts, canonical, "/articles", "Articles"
        )
        out_path = (
            PUBLIC / "articles" / "index.html"
            if idx == 1
            else PUBLIC / "articles" / "page" / str(idx) / "index.html"
        )
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(page_html, encoding="utf-8")
        en_pages.append((idx, page_html))

    locale_written = 0
    article_maps = {lang: _load_locale_article_slugs(lang) for lang in LOCALES_NON_EN}
    locale_prefixes = {
        lang: _load_static_slug(lang, "articles", "articles") for lang in LOCALES_NON_EN
    }
    for idx, en_html in en_pages:
        for lang in LOCALES_NON_EN:
            prefix = locale_prefixes[lang]
            out_path = (
                PUBLIC / lang / prefix / "index.html"
                if idx == 1
                else PUBLIC / lang / prefix / "page" / str(idx) / "index.html"
            )
            _write_locale_page(en_html, lang, idx, article_maps[lang], prefix, out_path)
            locale_written += 1
    return len(en_pages), locale_written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    en_written, locale_written = _write_listings()
    print(
        f"build_listings: wrote {en_written} EN paged listing(s) + "
        f"{locale_written} locale fork(s) "
        f"across {len(LOCALES_NON_EN)} non-EN locales."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
