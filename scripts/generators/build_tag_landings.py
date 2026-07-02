#!/usr/bin/env python3
"""Generate per-tag landing pages at ``public/tags/<slug>/index.html``.

Runs AFTER ssg, BEFORE build_translations + postbuild. For each
canonical tag with ≥ 3 posts (per ``_data/taxonomy.yml`` resolved
against the corpus), emits a focused landing page:

  - hero        : eyebrow (pillar) + h1 (tag name) + deck (description)
                  + article-count meta
  - main body   : article-card list (newest first) of every post
                  tagged with this canonical, related-tag chips
  - JSON-LD     : CollectionPage + ItemList (Schema.org)

The page reuses the just-emitted ``public/tags/index.html`` cover as
a TEMPLATE skeleton — head/nav/footer/CSS link/CSP placeholders are
all in place, so we just swap the content area. The follow-up
postbuild pass fingerprints CSS, stamps hreflang (we leave a
placeholder), and re-stamps the CSP hashes; locale forks come from
build_translations in a subsequent WS3 commit.

Run from repo root::

    python3 scripts/generators/build_tag_landings.py
"""

from __future__ import annotations

import argparse
import collections
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("error: PyYAML not installed", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[2]
from listing_common import (
    _BANNER_FM_RE,
    _DEFAULT_BANNER,
    _DESC_FM_RE,
    _EXCERPT_FM_RE,
    _TAG_FM_RE,
    _TITLE_FM_RE,
    PILLAR_ORDER,
    _alias_map,
)
from tag_landing_render import (
    _BASE_URL,
    _CANONICAL_RE,
    _LANDING_THRESHOLD,
    _OG_URL_RE,
    LOCALE_TAGS_PATH,
    _category_recent_posts,
    _locale_post_card_fields,
    _render_category_html,
    _render_landing_html,
    _swap_landing_cards,
)

TAXONOMY = ROOT / "_data" / "taxonomy.yml"
PUBLIC = ROOT / "public"
TEMPLATE_PATH = PUBLIC / "tags" / "index.html"
# Six editorial pillars from taxonomy.yml's category field. Order
# matches the cover-page pillar grid; same order is used to render
# /categories/index.html.
# Per-locale tags-path segment. Matches the hreflang chain already
# emitted on /tags/index.html. The canonical tag slug stays English
# (post-quantum-cryptography, iso-20022, …) — localising the slug
# itself is a future polish; for now we get URL parity at /<lang>/
# <localised-tags-segment>/<canonical>/index.html.
LOCALES_NON_EN = [code for code in LOCALE_TAGS_PATH if code != "en"]

_BANNER_ALT_FM_RE = re.compile(r'^banner_alt:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
from _core import DATED_SLUG_RE as _DATED_SLUG_RE  # canonical dated-slug matcher

_HTML_LANG_RE = re.compile(r'<html lang="[^"]*"', re.IGNORECASE)
# The /tags/index.html cover template carries a leftover hero section
# from its own markdown frontmatter — `<section class="ap-hero"><h1>
# Sebastien Rousseau</h1>…</section>`. Each landing supplies its own
# `<h1>` inside the wrap-div, so we strip the cover's hero to keep
# the page at exactly one h1 (WCAG 2.4.6 + 1.3.1 AAA).






# Tiny per-card share rail — 6 monochrome SVG glyphs (X, LinkedIn, Facebook,
# WhatsApp, email, copy-link). Mirrors build_listings._card_share_rail; copied
# here so build_tag_landings stays import-self-contained.




def _extract_excerpt(text: str) -> str:
    """Return the post's excerpt or fall back to description."""
    excerpt_m = _EXCERPT_FM_RE.search(text)
    if excerpt_m:
        return excerpt_m.group(1)
    desc_m = _DESC_FM_RE.search(text)
    return desc_m.group(1) if desc_m else ""


def _extract_banner(text: str, title: str) -> tuple[str, str]:
    """Return (banner_url, banner_alt) — banner_alt falls back to title."""
    banner_m = _BANNER_FM_RE.search(text)
    banner_alt_m = _BANNER_ALT_FM_RE.search(text)
    banner = banner_m.group(1) if banner_m else _DEFAULT_BANNER
    banner_alt = banner_alt_m.group(1) if banner_alt_m else title
    return banner, banner_alt


def _parse_raw_tags(tags_line: str) -> list[str]:
    """Split a `tags:` frontmatter line into stripped, non-empty tag
    strings."""
    return [
        t for t in (
            raw.strip().strip('"').strip("'").strip()
            for raw in tags_line.split(",")
        )
        if t
    ]


def _post_meta(path: Path) -> tuple[str, str, str, str, list[str], str, str] | None:
    """Return (title, iso-date, slug, excerpt, [raw tag strings],
    banner, banner_alt) or None."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    tags_m = _TAG_FM_RE.search(text)
    if not tags_m:
        return None
    title_m = _TITLE_FM_RE.search(text)
    title = title_m.group(1) if title_m else path.stem
    excerpt = _extract_excerpt(text)
    banner, banner_alt = _extract_banner(text, title)
    stem_m = _DATED_SLUG_RE.match(path.stem)
    iso_date = stem_m.group(1) if stem_m else ""
    raw_tags = _parse_raw_tags(tags_m.group(1))
    return title, iso_date, path.stem, excerpt, raw_tags, banner, banner_alt


def _canonical_set(raw_tags: list[str], amap: dict[str, str]) -> set[str]:
    """Resolve a post's raw tag strings to a deduplicated set of
    canonical slugs via the alias map."""
    return {amap[r.lower()] for r in raw_tags if r.lower() in amap}


def _post_pillars(raw_tags: list[str], taxonomy: dict, amap: dict[str, str]) -> list[str]:
    """Return ordered list of pillar slugs (categories) this post
    belongs to, derived from its raw tag strings."""
    pillars: set[str] = set()
    for r in raw_tags:
        canon = amap.get(r.lower())
        if not canon:
            continue
        cat = taxonomy.get(canon, {}).get("category")
        if cat:
            pillars.add(cat)
    return [p for p in PILLAR_ORDER if p in pillars]


def _ingest_post(
    path: Path,
    taxonomy: dict,
    amap: dict[str, str],
    posts: dict[str, list[tuple[str, str, str, str, list[str], str, str]]],
    cooccur: dict[str, collections.Counter[str]],
) -> None:
    meta = _post_meta(path)
    if not meta:
        return
    title, iso_date, slug, excerpt, raw_tags, banner, banner_alt = meta
    canons = _canonical_set(raw_tags, amap)
    pillars = _post_pillars(raw_tags, taxonomy, amap)
    for c in canons:
        posts[c].append((title, iso_date, slug, excerpt, pillars, banner, banner_alt))
        for other in canons - {c}:
            cooccur[c][other] += 1


def _walk(taxonomy: dict) -> tuple[
    dict[str, list[tuple[str, str, str, str, list[str], str, str]]],
    dict[str, collections.Counter[str]],
]:
    """Return:
    * per-canonical [(title, iso-date, slug, excerpt, pillars, banner,
      banner_alt), ...] newest first
    * per-canonical Counter of OTHER canonicals that co-occur on the
      same posts — drives the "related tags" sidebar.
    """
    amap = _alias_map(taxonomy)
    posts: dict[str, list[tuple[str, str, str, str, list[str], str, str]]] = collections.defaultdict(list)
    cooccur: dict[str, collections.Counter[str]] = collections.defaultdict(
        collections.Counter
    )
    for path in sorted((ROOT / "_posts").glob("*.md")):
        # Skip non-article markdown: hub pages (tags.md / categories.md),
        # the homepage (index.md), and anything else without a YYYY-MM-DD
        # date prefix. Without the prefix we'd otherwise emit cards
        # pointing at `/index/` etc. (an obvious broken-link smell).
        if not _DATED_SLUG_RE.match(path.stem):
            continue
        _ingest_post(path, taxonomy, amap, posts, cooccur)
    for c in posts:
        posts[c].sort(key=lambda p: p[1] or "0000", reverse=True)
    return posts, cooccur
















def _load_locale_article_slugs(lang: str) -> dict[str, str]:
    """Return {en-slug: locale-slug} from ``_data/i18n/<lang>/slugs.json``.
    Returns {} when the file is missing — locale forks then keep the
    EN article links rather than 404 silently."""
    import json

    path = ROOT / "_data" / "i18n" / lang / "slugs.json"
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    arts = data.get("articles") or {}
    return {k: v for k, v in arts.items() if isinstance(v, str) and v}


def _load_fr_to_en_slug_map(lang: str) -> dict[str, str]:
    """Return ``{locale_slug: en_slug}`` from
    ``_data/i18n/<lang>/slugs.json``. Returns {} on missing/malformed
    file."""
    import json

    slugs_path = ROOT / "_data" / "i18n" / lang / "slugs.json"
    if not slugs_path.is_file():
        return {}
    try:
        data = json.loads(slugs_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return {
        locale_slug: en_slug
        for en_slug, locale_slug in (data.get("articles") or {}).items()
        if isinstance(locale_slug, str) and locale_slug
    }




def _load_locale_post_index(lang: str) -> dict[str, tuple[str, str, str, str]]:
    """Return ``{en_slug: (locale_slug, locale_title, locale_excerpt,
    locale_banner)}`` for every dated post in ``_posts/<lang>/``. Same
    contract as build_listings._load_locale_post_index — duplicated
    here to keep build_tag_landings importable without forcing a
    cross-module import. Posts present only in EN fall back to the
    EN card content at render time."""
    src = ROOT / "_posts" / lang
    if not src.is_dir():
        return {}
    fr_to_en = _load_fr_to_en_slug_map(lang)
    out: dict[str, tuple[str, str, str, str]] = {}
    for path in sorted(src.glob("*.md")):
        fields = _locale_post_card_fields(path)
        if fields is None:
            continue
        stem, title, excerpt, banner = fields
        en_slug = fr_to_en.get(stem, stem)
        out[en_slug] = (stem, title, excerpt, banner)
    return out








_HREFLANG_ARTICLE_RE = re.compile(r'href="/(\d{4}-\d{2}-\d{2}-[^/"]+)/"')
# JSON-LD "inLanguage":"en" / "en-GB" strings sprinkled across the EN
# template. validate_jsonld.py flags them when the <html lang> base
# doesn't match — see the build's JSON-LD validation step. Update in
# place for each locale fork.
_INLANG_RE = re.compile(r'"inLanguage":\s*"(?:en|en-GB|en-US)"')


def _localise_html_links(
    en_html: str,
    lang: str,
    slug: str,
    article_map: dict[str, str],
) -> str:
    """Rewrite the EN landing HTML into one locale variant: <html lang>,
    canonical, og:url, internal article links, related-tag chip hrefs."""
    locale_tags = LOCALE_TAGS_PATH[lang]
    locale_root = f"/{lang}"
    out = en_html
    out = _HTML_LANG_RE.sub(f'<html lang="{lang}"', out, count=1)
    canonical = f"{_BASE_URL}{locale_root}/{locale_tags}/{slug}/"
    out = _CANONICAL_RE.sub(
        f'<link rel="canonical" href="{canonical}"', out, count=1
    )
    out = _OG_URL_RE.sub(
        f'<meta property="og:url" content="{canonical}"', out, count=1
    )
    # Article slug remap — strict {en-slug} matches only so we don't
    # silently rewrite unrelated hrefs.
    def _swap_article(m: re.Match[str]) -> str:
        en_slug = m.group(1)
        locale_slug = article_map.get(en_slug, en_slug)
        return f'href="{locale_root}/{locale_slug}/"'

    out = _HREFLANG_ARTICLE_RE.sub(_swap_article, out)
    # Related-tag chips: /tags/<canonical>/ → /<lang>/<locale-tags>/<canonical>/
    out = out.replace('href="/tags/', f'href="{locale_root}/{locale_tags}/')
    # Update JSON-LD inLanguage so validate_jsonld doesn't warn.
    out = _INLANG_RE.sub(f'"inLanguage":"{lang}"', out)
    return out


def _translate_chrome_for(lang: str, html: str) -> str:
    """Run the EN shell through ``build_translations.translate_chrome``
    bound to ``lang`` — translates nav, footer, search labels, aria
    attributes, language menu, dates. Keeps the body content (which
    is generator-emitted EN text) untouched. Raises ``RuntimeError`` if
    the package isn't importable so silent EN-chrome leaks don't ship."""
    # Ensure repo root is on sys.path even when this module is invoked
    # as a script (`python3 scripts/generators/build_tag_landings.py`) —
    # otherwise the `scripts.generators...` package path won't resolve
    # and the import would have to fall back to untranslated chrome.
    import sys as _sys
    if str(ROOT) not in _sys.path:
        _sys.path.insert(0, str(ROOT))
    from scripts.generators.build_translations import _state as _bt_state
    from scripts.generators.build_translations._chrome import translate_chrome
    _bt_state.bind_lang(lang)
    return translate_chrome(html)


def _write_locale_landings(
    taxonomy: dict,
    posts: dict[str, list[tuple[str, str, str, str, list[str], str, str]]],
    en_pages: dict[str, str],
) -> int:
    written = 0
    article_maps = {lang: _load_locale_article_slugs(lang) for lang in LOCALES_NON_EN}
    locale_indexes = {lang: _load_locale_post_index(lang) for lang in LOCALES_NON_EN}
    for slug in en_pages:
        if len(posts.get(slug, [])) < _LANDING_THRESHOLD:
            continue
        en_html = en_pages[slug]
        posts_for_tag = posts.get(slug, [])
        for lang in LOCALES_NON_EN:
            locale_html = _localise_html_links(en_html, lang, slug, article_maps[lang])
            locale_html = _swap_landing_cards(
                locale_html, posts_for_tag, locale_indexes[lang],
                article_maps[lang], lang,
            )
            locale_html = _translate_chrome_for(lang, locale_html)
            out_path = (
                PUBLIC / lang / LOCALE_TAGS_PATH[lang] / slug / "index.html"
            )
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(locale_html, encoding="utf-8")
            written += 1
    return written












def _write_category_pages(
    taxonomy: dict,
    posts: dict[str, list[tuple[str, str, str, str, list[str], str, str]]],
) -> tuple[int, int]:
    """Generate /categories/<pillar>/index.html for each of the 6
    pillars + locale forks. Reuses the /tags/index.html cover as a
    template skeleton."""
    if not TEMPLATE_PATH.is_file():
        return 0, 0
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    en_pages: dict[str, tuple[str, list[tuple[str, str, str, str, list[str], str, str]]]] = {}
    for pillar in PILLAR_ORDER:
        page_html = _render_category_html(template, pillar, taxonomy, posts)
        out_path = PUBLIC / "categories" / pillar / "index.html"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(page_html, encoding="utf-8")
        pillar_slugs = [
            slug for slug, e in taxonomy.items() if e.get("category") == pillar
        ]
        pillar_slugs.sort(key=lambda s: -len(posts.get(s, [])))
        recent = _category_recent_posts(pillar_slugs, posts)
        en_pages[pillar] = (page_html, recent)
    locale_written = _write_category_locale_forks(en_pages)
    return len(en_pages), locale_written


def _write_category_locale_forks(
    en_pages: dict[str, tuple[str, list[tuple[str, str, str, str, list[str], str, str]]]],
) -> int:
    """Same lang/canonical/links rewrite as tag-landing locales. The
    /categories/ path stays English across all locales (no localised
    segment for this round — a future polish can add per-locale
    "catégories" / "categorías" / etc.).

    Cards inside the "Recent articles" rail get re-rendered with
    locale-translated title/excerpt/banner + URL via the per-locale
    post index (frontmatter from ``_posts/<lang>/``)."""
    written = 0
    article_maps = {lang: _load_locale_article_slugs(lang) for lang in LOCALES_NON_EN}
    locale_indexes = {lang: _load_locale_post_index(lang) for lang in LOCALES_NON_EN}
    for pillar, (en_html, recent) in en_pages.items():
        for lang in LOCALES_NON_EN:
            locale_tags = LOCALE_TAGS_PATH[lang]
            out = en_html
            out = _HTML_LANG_RE.sub(f'<html lang="{lang}"', out, count=1)
            canonical = f"{_BASE_URL}/{lang}/categories/{pillar}/"
            out = _CANONICAL_RE.sub(
                f'<link rel="canonical" href="{canonical}"', out, count=1
            )
            out = _OG_URL_RE.sub(
                f'<meta property="og:url" content="{canonical}"', out, count=1
            )
            amap = article_maps[lang]

            def _swap_article(m: re.Match[str], _lang: str = lang, _amap: dict = amap) -> str:
                en_slug = m.group(1)
                return f'href="/{_lang}/{_amap.get(en_slug, en_slug)}/"'

            out = _HREFLANG_ARTICLE_RE.sub(_swap_article, out)
            out = out.replace('href="/tags/', f'href="/{lang}/{locale_tags}/')
            out = _INLANG_RE.sub(f'"inLanguage":"{lang}"', out)
            out = _swap_landing_cards(out, recent, locale_indexes[lang], amap, lang)
            out = _translate_chrome_for(lang, out)
            out_path = (
                PUBLIC / lang / "categories" / pillar / "index.html"
            )
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(out, encoding="utf-8")
            written += 1
    return written


def _write_landings(
    taxonomy: dict,
    posts: dict[str, list[tuple[str, str, str, str, list[str], str, str]]],
    cooccur: dict[str, collections.Counter[str]],
) -> tuple[int, int]:
    if not TEMPLATE_PATH.is_file():
        print(
            f"build_tag_landings: missing template {TEMPLATE_PATH}",
            file=sys.stderr,
        )
        return 0, 0
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    en_pages: dict[str, str] = {}
    for slug, entry in taxonomy.items():
        ps = posts.get(slug, [])
        if len(ps) < _LANDING_THRESHOLD:
            continue
        page_html = _render_landing_html(
            template, slug, entry, ps,
            cooccur.get(slug, collections.Counter()), taxonomy, posts,
        )
        out_path = PUBLIC / "tags" / slug / "index.html"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(page_html, encoding="utf-8")
        en_pages[slug] = page_html
    locale_written = _write_locale_landings(taxonomy, posts, en_pages)
    return len(en_pages), locale_written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    if not TAXONOMY.is_file():
        print(
            f"build_tag_landings: no taxonomy at {TAXONOMY}, skipping",
            file=sys.stderr,
        )
        return 0
    taxonomy = yaml.safe_load(TAXONOMY.read_text(encoding="utf-8")) or {}
    posts, cooccur = _walk(taxonomy)
    en_written, locale_written = _write_landings(taxonomy, posts, cooccur)
    cat_en, cat_locale = _write_category_pages(taxonomy, posts)
    print(
        f"build_tag_landings: wrote {en_written} EN tag landing(s) + "
        f"{locale_written} locale fork(s); {cat_en} EN category landing(s) + "
        f"{cat_locale} locale fork(s) "
        f"across {len(LOCALES_NON_EN)} non-EN locales."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
