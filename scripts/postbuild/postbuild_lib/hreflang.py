# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Per-page i18n injection: hreflang alternates + language switcher.

Split from article_furniture (Phase 4.1, step 2) atop the _i18n base. Imports
the i18n foundation from postbuild_lib._i18n and three shared HTML constants
from article_furniture (one-directional — article_furniture does not import
this module).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import _lang_registry as _lr

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from _core import DATED_SLUG_RE as _DATED_SLUG_RE
from postbuild_lib._i18n import _all_active_non_en_langs, _slug_maps
from postbuild_lib.article_furniture import (
    _H1_RE,
    _HEAD_END_RE,
    PUBLIC,
)


def build_fr_title_index(pages: list[Path]) -> dict[str, str]:
    """Walk rendered FR pages, return ``en_slug -> FR H1 title`` so the
    prev/next nav on a FR page can advertise the FR title for the
    neighbouring article instead of the English H1.
    """
    out: dict[str, str] = {}
    fr_articles_map = _lr.load_slugs("fr").get("articles", {})
    fr_to_en = {v: k for k, v in fr_articles_map.items()}
    for p in pages:
        if p.parent.parent.name != "fr":
            continue
        slug = p.parent.name  # FR slug
        if not _DATED_SLUG_RE.match(slug):
            continue
        en = fr_to_en.get(slug, slug)
        if en == slug:  # not in slug map
            continue
        html = p.read_text(encoding="utf-8", errors="ignore")
        m = _H1_RE.search(html)
        if m:
            out[en] = m.group(1).strip()
    return out


# Match a <link rel="alternate" hreflang=…> tag with any attribute order and
# either HTML5 (``>``) or XHTML (``/>``) self-close.
#
# Public because three passes strip hreflang before re-emitting it and each
# had grown its own copy. Two of those copies used ``[^/]*/>``, which can
# never match a real tag — every ``https://`` href contains a slash — so the
# strip silently did nothing and the cluster was appended again on every
# run. One copy was fixed in place; postbuild_transforms kept the broken
# form, which is how topic and locale-home pages reached 435 hreflang links
# (twelve duplicate clusters, ~3.8 KB a run).
HREFLANG_LINK_RE = re.compile(
    r'<link\b(?=[^>]*\brel=["\']?alternate["\']?)(?=[^>]*\bhreflang=)[^>]*/?>',
    re.IGNORECASE,
)
_HREFLANG_RE = HREFLANG_LINK_RE


def _translated_slugs_per_lang() -> dict[str, set[str]]:
    """Return ``{code: set_of_rendered_slugs}`` for every active non-EN
    language whose output dir exists under ``public/``."""
    out: dict[str, set[str]] = {}
    for code in _all_active_non_en_langs():
        d = PUBLIC / code
        if not d.is_dir():
            continue
        out[code] = {p.parent.name for p in d.glob("*/index.html")}
    return out


def _translated_slugs() -> tuple[set[str], set[str]]:
    """Legacy FR-only helper. Returns ``(en_slugs_with_fr,
    fr_slugs_with_en)`` for the call sites that haven't yet moved to
    the lang-keyed API."""
    fr_dir = PUBLIC / "fr"
    if not fr_dir.is_dir():
        return set(), set()
    rendered_fr = {p.parent.name for p in fr_dir.glob("*/index.html")}
    fr_articles_map = _lr.load_slugs("fr").get("articles", {})
    en_with_fr = {en for en, fr in fr_articles_map.items() if fr in rendered_fr}
    fr_to_en = {v: k for k, v in fr_articles_map.items()}
    fr_with_en = rendered_fr & set(fr_to_en.keys())
    return en_with_fr, fr_with_en


def _resolve_en_slug(slug: str, lang: str) -> str | None:
    """Reverse-map any language's slug to its EN counterpart."""
    if lang == "en":
        return slug
    maps = _slug_maps(lang)
    return maps["articles_lang_to_en"].get(slug) or maps["statics_lang_to_en"].get(slug)


def _alternates_for_en_slug(
    en_slug: str,
    translated_per_lang: dict[str, set[str]],
) -> list[tuple[str, str]]:
    """Build the full ``[(lang_code, absolute_url), …]`` alternate list
    for an EN slug."""
    alts: list[tuple[str, str]] = [
        ("en", f"https://sebastienrousseau.com/{en_slug}/"),
    ]
    for code in _all_active_non_en_langs():
        maps = _slug_maps(code)
        lang_slug = maps["articles_en_to_lang"].get(en_slug) or maps["statics_en_to_lang"].get(
            en_slug
        )
        if not lang_slug:
            continue
        if lang_slug not in translated_per_lang.get(code, set()):
            continue
        alts.append((code, f"https://sebastienrousseau.com/{code}/{lang_slug}/"))
    return alts


_LANG_SWITCH_STRINGS: dict[str, tuple[str, str]] = {
    "en": ("This post is also available in", "Available languages"),
    "fr": ("Cet article est aussi disponible en", "Langues disponibles"),
    "es": ("Este artículo también está disponible en", "Idiomas disponibles"),
    "de": ("Dieser Artikel ist auch verfügbar auf", "Verfügbare Sprachen"),
    "it": ("Questo articolo è disponibile anche in", "Lingue disponibili"),
    "pt-br": ("Este artigo também está disponível em", "Idiomas disponíveis"),
    "nl": ("Dit artikel is ook beschikbaar in", "Beschikbare talen"),
    "ja": ("この記事は次の言語でもご覧いただけます", "対応言語"),
    "zh-hans": ("本文亦提供以下语言版本", "可用语言"),
    "zh-hant": ("本文亦提供以下語言版本", "可用語言"),
    "ko": ("이 글은 다음 언어로도 제공됩니다", "지원 언어"),
    "ar": ("هذه المقالة متوفرة أيضًا باللغات", "اللغات المتوفرة"),
    "ru": ("Эта статья также доступна на", "Доступные языки"),
    "pl": ("Ten artykuł jest również dostępny w", "Dostępne języki"),
    "cs": ("Tento článek je k dispozici také v", "Dostupné jazyky"),
    "uk": ("Ця стаття також доступна", "Доступні мови"),
    "ro": ("Acest articol este disponibil și în", "Limbi disponibile"),
    "tr": ("Bu makale şu dillerde de mevcuttur", "Mevcut diller"),
    "he": ("מאמר זה זמין גם בשפות", "שפות זמינות"),
    "hi": ("यह लेख इन भाषाओं में भी उपलब्ध है", "उपलब्ध भाषाएँ"),
    "bn": ("এই নিবন্ধটি এই ভাষাগুলিতেও উপলব্ধ", "উপলব্ধ ভাষাসমূহ"),
    "id": ("Artikel ini juga tersedia dalam", "Bahasa yang tersedia"),
    "vi": ("Bài viết này cũng có sẵn bằng", "Ngôn ngữ có sẵn"),
    "th": ("บทความนี้มีให้ในภาษาต่อไปนี้ด้วย", "ภาษาที่ใช้ได้"),
    "fil": ("Available rin ang artikulong ito sa", "Mga available na wika"),
    "ha": ("Wannan labarin yana samuwa kuma a cikin", "Harsunan da ake samu"),
    "yo": ("Àpilẹ̀kọ yìí tún wà ní", "Àwọn èdè tó wà"),
    "sv": ("Den här artikeln finns även på", "Tillgängliga språk"),
    # Planned locales (issue #360). Present so the article-level switcher
    # renders correctly the moment each locale's content backfill lands;
    # inert while the locale is active=False (data-driven — only appears
    # for articles that actually have a translation).
    "fa": ("این مقاله به زبان‌های زیر نیز در دسترس است", "زبان‌های موجود"),
    "mr": ("हा लेख या भाषांमध्येही उपलब्ध आहे", "उपलब्ध भाषा"),
    "ta": ("இந்தக் கட்டுரை பின்வரும் மொழிகளிலும் கிடைக்கிறது", "கிடைக்கும் மொழிகள்"),
    "te": ("ఈ కథనం ఈ భాషల్లో కూడా అందుబాటులో ఉంది", "అందుబాటులో ఉన్న భాషలు"),
    "ms": ("Artikel ini juga tersedia dalam", "Bahasa yang tersedia"),
    "el": ("Αυτό το άρθρο είναι επίσης διαθέσιμο στα", "Διαθέσιμες γλώσσες"),
    "hu": ("Ez a cikk a következő nyelveken is elérhető", "Elérhető nyelvek"),
}
_LANG_SWITCH_ORDER: tuple[str, ...] = (
    "fr",
    "es",
    "de",
    "it",
    "pt-br",
    "nl",
    "ja",
    "zh-hans",
    "zh-hant",
    "ko",
    "ar",
    "ru",
    "pl",
    "cs",
    "uk",
    "ro",
    "tr",
    "he",
    "hi",
    "bn",
    "id",
    "vi",
    "th",
    "fil",
    "ha",
    "yo",
    "sv",
    "fa",
    "mr",
    "ta",
    "te",
    "ms",
    "el",
    "hu",
    "en",
)
_LANG_SWITCH_INSERT_RE = re.compile(
    r"(</section>)(\s*<main\b)",
    re.IGNORECASE,
)


def _render_lang_switch_item(
    code: str,
    href: str,
) -> str:
    """One <li><a> for the lang rail. Sets lang + hreflang + dir=rtl when
    appropriate so screen readers pronounce the native label correctly."""
    lang_obj = _lr.get(code)
    rtl_attr = ' dir="rtl"' if lang_obj.rtl else ""
    return (
        f'<li><a href="{href}" lang="{lang_obj.bcp47}" hreflang="{lang_obj.bcp47}"'
        f' rel="alternate"{rtl_attr}>{lang_obj.long_label}</a></li>'
    )


def _lang_switch_others(
    en_slug: str,
    lang: str,
    translated_per_lang: dict[str, set[str]],
) -> list[tuple[str, str]]:
    """Return ``[(code, relative_href), …]`` for every locale this article
    is available in, excluding the current page's lang, in the
    :data:`_LANG_SWITCH_ORDER` priority order."""
    alts = _alternates_for_en_slug(en_slug, translated_per_lang)
    by_code = {code: url.replace("https://sebastienrousseau.com", "", 1) for code, url in alts}
    return [
        (code, by_code[code]) for code in _LANG_SWITCH_ORDER if code in by_code and code != lang
    ]


def inject_lang_switcher(
    html: str,
    slug: str,
    lang: str,
    translated_per_lang: dict[str, set[str]],
) -> str:
    """Insert an inline per-article language switcher between the hero
    and the article body.

    Surfaces the 28-locale advantage to readers as content, not chrome.
    Different from the site-wide ``.ap-lang-item`` dropdown — that's nav
    furniture; this is editorial. Both can coexist on the same page.

    Idempotent. Skips:
      - pages without the BlogPosting JSON-LD anchor (listing / static)
      - pages already carrying a ``.article-langswitch`` block
      - articles available in fewer than two locales (no rail needed)
    """
    if '"@type":"BlogPosting"' not in html:
        return html
    if 'class="article-langswitch"' in html:
        return html
    en_slug = _resolve_en_slug(slug, lang)
    if en_slug is None:
        return html
    others = _lang_switch_others(en_slug, lang, translated_per_lang)
    if not others:
        return html

    lead_text, aria_label = _LANG_SWITCH_STRINGS.get(
        lang,
        _LANG_SWITCH_STRINGS["en"],
    )
    items = "".join(_render_lang_switch_item(c, h) for c, h in others)
    aside = (
        f'<aside class="article-langswitch" aria-label="{aria_label}">'
        f'<span class="article-langswitch-lead">{lead_text}</span> '
        f'<ul class="article-langswitch-list">{items}</ul>'
        f"</aside>"
    )

    new_html, n = _LANG_SWITCH_INSERT_RE.subn(
        lambda m: f"{m.group(1)}{aside}{m.group(2)}",
        html,
        count=1,
    )
    return new_html if n else html


def inject_hreflang(
    html: str,
    slug: str,
    lang: str,
    translated_per_lang: dict[str, set[str]] | None = None,
    *,
    en_with_fr: set[str] | None = None,
    fr_with_en: set[str] | None = None,
) -> str:
    """Inject reciprocal hreflang links so search crawlers + the
    language-selector JS pair every translated version of a page."""
    if translated_per_lang is None:
        translated_per_lang = {}
        if fr_with_en:
            translated_per_lang["fr"] = fr_with_en
    en_slug = _resolve_en_slug(slug, lang)
    if en_slug is None:
        return html
    alts = _alternates_for_en_slug(en_slug, translated_per_lang)
    if len(alts) < 2:
        return html
    en_url = alts[0][1]
    html = _HREFLANG_RE.sub("", html)
    links = "".join(
        f'<link rel="alternate" hreflang="{code}" href="{url}" />' for code, url in alts
    )
    links += f'<link rel="alternate" hreflang="x-default" href="{en_url}" />'
    return _HEAD_END_RE.sub(links + "</head>", html, count=1)
