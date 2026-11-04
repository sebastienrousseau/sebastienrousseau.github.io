# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Build-output gates for plan items 2.4 (author box + Person) and 2.5
(internal links), over the indexed locales only.

Each test reads the built ``public/`` (skipped when it is absent):

* every indexable article shows the author box with credentials;
* every Article-family JSON-LD node carries headline, both dates, image
  and an ``author`` that is exactly the site's one ``Person`` ``@id``, and
  that Person node, on the same page, has ``name``, ``url`` and ``sameAs``;
* no article is an orphan: another indexable page in its locale links it
  from the page content (site header, breadcrumb and footer excluded);
* every article links at least three indexable articles in its own
  locale, its pillar hub in its own locale, and nothing that is a
  redirect stub, a noindex-locale page or another locale's article;
* every hub (tag landing, pillar, topic) lists at least one article;
* the About page links the evidence it names: repositories, the
  published paper, and the speaking page.
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from functools import cache
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

import _lang_registry as _lr
import _locale_indexing as _li

pytestmark = pytest.mark.skipif(
    not (PUBLIC / "index.html").is_file(), reason="public/ not built: run ./build.sh first"
)

SITE = "https://sebastienrousseau.com"
PERSON_ID = f"{SITE}/#person"
CODES = frozenset(lang.code for lang in _lr.active())
ARTICLE_TYPES = {"BlogPosting", "Article", "NewsArticle", "TechArticle", "ScholarlyArticle"}
REQUIRED = ("headline", "datePublished", "dateModified", "image", "author")
HUBS = ("tag-hub", "pillar-hub", "topic-hub")

_DATED = re.compile(r"^\d{4}-\d{2}-\d{2}-")
_LD_RE = re.compile(r'<script type="application/ld\+json"[^>]*>([\s\S]*?)</script>', re.I)
_HREF_RE = re.compile(r'<a\b[^>]*\bhref="([^"]+)"', re.I)
_NOINDEX_RE = re.compile(r'<meta\s+name="robots"\s+content="[^"]*noindex', re.I)
_REFRESH_RE = re.compile(r'http-equiv=["\']?refresh', re.I)
_CRUMBS_RE = re.compile(r'<nav class="crumbs"[\s\S]*?</nav>', re.I)


def _tags_segment(lang: str) -> str:
    return "tags" if lang == "en" else _lr.load_slugs(lang).get("static", {}).get("tags", "tags")


def _kind(parts: tuple[str, ...], lang: str) -> str:
    rest = (parts if lang == "en" else parts[1:])[:-1]
    if len(rest) == 1 and _DATED.match(rest[0]):
        return "article"
    if len(rest) != 2:
        return "other"
    if rest[0] == _tags_segment(lang):
        return "tag-hub"
    return {"categories": "pillar-hub", "topics": "topic-hub"}.get(rest[0], "other")


def _content(html: str) -> str:
    """The page minus the site header, breadcrumb and footer."""
    start, end = html.find("</header>"), html.find('<footer class="ap-foot"')
    return _CRUMBS_RE.sub("", html[max(start, 0) : end if end >= 0 else len(html)])


def _norm(href: str) -> str | None:
    href = href.removeprefix(SITE) if href.startswith(SITE) else href
    if not href.startswith("/") or href.startswith("//"):
        return None
    href = href.split("#", 1)[0].split("?", 1)[0].removesuffix("index.html")
    if "." in href.rsplit("/", 1)[-1]:
        return None
    return href if href.endswith("/") else href + "/"


@cache
def _site() -> dict[str, dict]:
    """``{url: {lang, kind, indexable, stub, html}}``; html kept for indexed locales."""
    pages: dict[str, dict] = {}
    for page in PUBLIC.rglob("index.html"):
        parts = page.relative_to(PUBLIC).parts
        lang = parts[0] if len(parts) > 1 and parts[0] in CODES else "en"
        html = page.read_text(encoding="utf-8", errors="ignore")
        stub = bool(_REFRESH_RE.search(html[:16384]))
        kind = _kind(parts, lang)
        if kind == "article" and '"BlogPosting"' not in html:
            kind = "other"
        indexable = _li.is_indexed(lang) and not stub and not _NOINDEX_RE.search(html)
        url = "/" + "/".join(parts[:-1]) + ("/" if len(parts) > 1 else "")
        pages[url] = {
            "lang": lang,
            "kind": kind,
            "stub": stub,
            "indexable": indexable,
            "html": html if indexable else "",
        }
    return pages


@cache
def _links() -> dict[str, frozenset[str]]:
    """Content links of every indexable page, normalised to site paths."""
    return {
        url: frozenset(t for t in (_norm(h) for h in _HREF_RE.findall(_content(p["html"]))) if t)
        for url, p in _site().items()
        if p["indexable"]
    }


def _articles() -> list[tuple[str, dict]]:
    return [(u, p) for u, p in sorted(_site().items()) if p["indexable"] and p["kind"] == "article"]


def _fail(name: str, bad: list) -> None:
    assert not bad, f"{len(bad)} {name}, e.g. {bad[:5]}"


def test_indexed_locales_have_articles() -> None:
    per = defaultdict(int)
    for _url, p in _articles():
        per[p["lang"]] += 1
    assert set(per) == _li.indexed_codes(), sorted(_li.indexed_codes() - set(per))


# -- 2.4 Author box + Person ------------------------------------------------


def test_every_article_shows_the_author_box_with_credentials() -> None:
    bad = [
        u
        for u, p in _articles()
        if 'class="author-card"' not in p["html"] or 'class="author-credentials"' not in p["html"]
    ]
    _fail("article(s) without an author box with credentials", bad)


def _nodes(html: str) -> list[dict]:
    out: list[dict] = []
    stack: list[object] = [json.loads(raw) for raw in _LD_RE.findall(html)]
    while stack:
        item = stack.pop()
        if isinstance(item, list):
            stack.extend(item)
        elif isinstance(item, dict):
            out.append(item)
            stack.extend(v for v in item.values() if isinstance(v, (dict, list)))
    return out


def _types(node: dict) -> set[str]:
    raw = node.get("@type")
    return set(raw if isinstance(raw, list) else [raw])


def _article_problems(node: dict) -> list[str]:
    kind = sorted(_types(node) & ARTICLE_TYPES)[0]
    problems = [f"{kind} lacks {k}" for k in REQUIRED if not node.get(k)]
    if node.get("author") not in ({"@id": PERSON_ID}, [{"@id": PERSON_ID}]):
        problems.append(f"{kind} author is {node.get('author')!r}")
    return problems


def _jsonld_problems(html: str) -> list[str]:
    nodes = _nodes(html)
    person = next((n for n in nodes if n.get("@id") == PERSON_ID and "Person" in _types(n)), {})
    problems = [f"Person lacks {k}" for k in ("name", "url", "sameAs") if not person.get(k)]
    articles = [n for n in nodes if _types(n) & ARTICLE_TYPES]
    if not articles:
        problems.append("no Article node")
    for node in articles:
        problems += _article_problems(node)
    return problems


def test_article_jsonld_is_complete_and_author_resolves_to_the_person() -> None:
    bad = [(u, probs) for u, p in _articles() if (probs := _jsonld_problems(p["html"]))]
    _fail("article(s) with incomplete Article/Person JSON-LD", bad)


def test_person_same_as_lists_only_profiles_the_site_shows() -> None:
    """``sameAs`` must not drift from the profiles the identifiers list on
    the About page links (rel="me")."""
    about = _site()["/about/"]["html"]
    shown = set(re.findall(r'href="([^"]+)" rel="external me noopener"', about))
    person = next(n for n in _nodes(about) if n.get("@id") == PERSON_ID and "Person" in _types(n))
    assert shown and shown <= set(person["sameAs"]), sorted(shown - set(person["sameAs"]))


# -- 2.5 Internal links -----------------------------------------------------


def test_no_orphan_article() -> None:
    site, links = _site(), _links()
    inbound: dict[str, set[str]] = defaultdict(set)
    for src, targets in links.items():
        for t in targets:
            if t != src and t in site and site[t]["lang"] == site[src]["lang"]:
                inbound[t].add(src)
    _fail("orphan article(s)", [u for u, _p in _articles() if not inbound[u]])


def test_every_article_links_three_related_articles_in_its_locale() -> None:
    site, links = _site(), _links()
    bad = []
    for url, p in _articles():
        same = {
            t
            for t in links[url] - {url}
            if site.get(t, {}).get("kind") == "article"
            and site[t]["indexable"]
            and site[t]["lang"] == p["lang"]
        }
        if len(same) < 3:
            bad.append((url, len(same)))
    _fail("article(s) with fewer than 3 same-locale related links", bad)


def test_no_article_links_a_stub_noindex_locale_or_other_locale_article() -> None:
    site, links = _site(), _links()
    bad = []
    for url, p in _articles():
        for t in sorted(links[url]):
            target = site.get(t)
            if target is None:
                continue
            crossing = target["kind"] == "article" and target["lang"] != p["lang"]
            if target["stub"] or not _li.is_indexed(target["lang"]) or crossing:
                bad.append((url, t))
    _fail("article link(s) to a stub, a noindex locale or another locale", bad)


def test_every_article_links_its_pillar_hub_in_its_locale() -> None:
    site, links = _site(), _links()
    bad = [
        u
        for u, p in _articles()
        if not any(
            site.get(t, {}).get("kind") == "pillar-hub" and site[t]["lang"] == p["lang"]
            for t in links[u]
        )
    ]
    _fail("article(s) without a link to their pillar hub", bad)


def test_every_hub_lists_articles_in_its_locale() -> None:
    site, links = _site(), _links()
    hubs = [(u, p) for u, p in sorted(site.items()) if p["indexable"] and p["kind"] in HUBS]
    assert hubs, "no hub pages found"
    bad = [
        u
        for u, p in hubs
        if not any(
            site.get(t, {}).get("kind") == "article" and site[t]["lang"] == p["lang"]
            for t in links[u]
        )
    ]
    _fail("hub(s) listing no article", bad)


def test_about_links_its_evidence() -> None:
    about = _content(_site()["/about/"]["html"])
    for href in (
        "https://github.com/sebastienrousseau/kyberlib",
        "https://github.com/sebastienrousseau/pain001",
        "https://emergingpaymentsasia.org/wp-content/uploads/2025/09/",
        "/speaking/",
        "/projects/",
    ):
        assert f'href="{href}' in about, href
