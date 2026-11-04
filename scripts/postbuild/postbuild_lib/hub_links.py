# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Article-to-pillar-hub links, and links that land on redirect stubs.

Measured on the v0.0.31 build across the 11 indexed locales (1,320
articles), the internal-link graph already had no orphan article and at
least three same-locale related links on every article. Two gaps were left:

* No article linked to its editorial pillar hub (``/categories/<pillar>/``,
  localised under ``/<lang>/categories/`` in every locale). The tag chips
  link to per-tag landings, but nothing tied an article to the one hub
  that groups its whole pillar. :func:`inject_pillar_hub_link` adds that
  link to the end of the cluster block, in the page's own language.
* 39 article pages linked to a meta-refresh redirect stub (a retired
  article URL, ``/papers/``, a locale's old ``/publications/`` slug). On
  locale pages two of those were English article URLs, so the link also
  crossed locales. :func:`repair_stub_links` points each such link at the
  stub's final target, localised to the page's language when that locale
  has the article. It runs after the redirect pages exist, reading the
  same stub map ``build_worker_assets`` publishes to the edge.

Both passes are idempotent.
"""

from __future__ import annotations

import html as _html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from _lang_registry import LanguageError, load_listings
from build_worker_assets import collapse_chains, stub_redirects
from postbuild_lib._i18n import _detect_page_lang, _slug_maps
from postbuild_lib.article_furniture import _article_pillar, _fallback_post_tags

PUBLIC = Path("public")
BASE_URL = "https://sebastienrousseau.com"

_HUB_MARKER = 'class="cluster-links-hub"'
_CLUSTER_RE = re.compile(r'<nav class="cluster-links"[\s\S]*?(</nav>)', re.IGNORECASE)
_BODY_CLOSE_RE = re.compile(r"</article>|</main>", re.IGNORECASE)
# The label/name separator, where a locale's typography differs from ": ".
_SEPARATOR = {"fr": "&#160;: ", "zh-hans": "：", "zh-hant": "：", "ja": "："}

_DATED_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-[^/]+$")
_ANCHOR_RE = re.compile(r"<a\b[^>]*>", re.IGNORECASE)
_HREF_RE = re.compile(r'\bhref="([^"#?]*)([#?][^"]*)?"')


# ---------------------------------------------------------------------------
# Pillar hub link
# ---------------------------------------------------------------------------


def _hub_href(lang: str, pillar: str) -> str:
    prefix = "" if lang == "en" else f"/{lang}"
    return f"{prefix}/categories/{pillar}/"


def _pillar_copy(lang: str, pillar: str) -> tuple[str, str]:
    """``(category label, pillar name)`` in ``lang``, English per missing key."""
    english = load_listings("en")
    try:
        local = load_listings(lang)
    except LanguageError:
        local = english
    label = local.get("ui", {}).get("categoryLabel") or english["ui"]["categoryLabel"]
    name = local.get("pillars", {}).get(pillar) or english["pillars"][pillar]
    return label, name


def _hub_paragraph(lang: str, pillar: str, href: str) -> str:
    label, name = _pillar_copy(lang, pillar)
    sep = _SEPARATOR.get(lang, ": ")
    return (
        f'<p class="cluster-links-hub">{_html.escape(label, quote=False)}{sep}'
        f'<a href="{href}">{_html.escape(name, quote=False)}</a></p>'
    )


def _insertion_point(html: str) -> int | None:
    """Inside the cluster block when there is one, else the end of the body."""
    cluster = _CLUSTER_RE.search(html)
    if cluster:
        return cluster.start(1)
    close = _BODY_CLOSE_RE.search(html)
    return close.start() if close else None


def inject_pillar_hub_link(html: str, public: Path = PUBLIC) -> str:
    """Link a dated article to its pillar hub in the page's own locale.

    The pillar is the one the end-of-article CTA already uses (the first
    of the article's English ``tags:`` that resolves to a taxonomy pillar),
    so the two never disagree. Skipped when the article has no pillar or
    the locale has no hub page for it, so the link can never 404."""
    if '"@type":"BlogPosting"' not in html or _HUB_MARKER in html:
        return html
    lang = _detect_page_lang(html)
    pillar = _article_pillar(_fallback_post_tags(html, lang))
    if not pillar:
        return html
    href = _hub_href(lang, pillar)
    at = _insertion_point(html)
    if at is None or not (public / href.strip("/") / "index.html").is_file():
        return html
    return html[:at] + _hub_paragraph(lang, pillar, href) + html[at:]


# ---------------------------------------------------------------------------
# Links to redirect stubs
# ---------------------------------------------------------------------------


def _stub_key(url: str) -> str | None:
    """The redirect-map key a site link would hit, or None if off-site."""
    if url.startswith(BASE_URL):
        url = url[len(BASE_URL) :] or "/"
    if not url.startswith("/") or url.startswith("//"):
        return None
    url = url.removesuffix("index.html")
    return url if url.endswith("/") else url + "/"


def localise_target(target: str, lang: str) -> str:
    """An English article ``target`` as ``lang``'s translation, if it has one."""
    stem = target.strip("/")
    if lang == "en" or not _DATED_RE.match(stem):
        return target
    try:
        mapped = _slug_maps(lang)["articles_en_to_lang"].get(stem)
    except Exception:  # a missing slug map must never fail a build
        mapped = None
    return f"/{lang}/{mapped}/" if mapped else target


def rewrite_stub_links(html: str, lang: str, redirects: dict[str, str]) -> tuple[str, int]:
    """Point every ``<a href>`` that lands on a redirect stub at its target."""
    count = 0

    def _href(m: re.Match[str]) -> str:
        nonlocal count
        key = _stub_key(m.group(1))
        target = redirects.get(key) if key else None
        if target is None:
            return m.group(0)
        count += 1
        return f'href="{localise_target(target, lang)}{m.group(2) or ""}"'

    out = _ANCHOR_RE.sub(lambda tag: _HREF_RE.sub(_href, tag.group(0)), html)
    return out, count


def repair_stub_links(public: Path = PUBLIC) -> int:
    """Rewrite stub links on every page that is not itself a stub.

    Returns the number of pages changed."""
    redirects = collapse_chains(stub_redirects(public))
    if not redirects:
        return 0
    changed = 0
    for page in sorted(public.rglob("*.html")):
        rel = "/" + page.relative_to(public).as_posix().removesuffix("index.html")
        if rel in redirects:
            continue
        html = page.read_text(encoding="utf-8", errors="ignore")
        out, count = rewrite_stub_links(html, _detect_page_lang(html), redirects)
        if count:
            page.write_text(out, encoding="utf-8")
            changed += 1
    return changed
