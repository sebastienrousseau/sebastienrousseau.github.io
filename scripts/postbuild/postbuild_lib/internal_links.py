"""Contextual in-prose internal linking across the article corpus.

The site had 105 dated articles on six coherent pillars and almost nothing
wiring them together: a median of 2 unique internal links per article inside
``<main>``, 65 % of articles below three, and — on the pages sampled — zero
contextual links in the prose itself. Meanwhile each article carried a median
of 8 outbound links, so the corpus passed more authority out than it
circulated. Topical clusters, which are how a focused corpus outranks a larger
generalist one, cannot form without internal links; and retrieval systems use
link structure to decide which page on a site is the canonical treatment of a
concept.

``topic_link.py`` already does this from a hand-curated map of ~12 entities
pointing at 2023–2024 posts, which is why the 2026 regulatory corpus (DORA,
the AI Act, the Data Act, EUDI, the CRA) gained almost nothing from it. This
module derives the link graph instead, from two things the repo already
maintains: ``_data/taxonomy.yml`` (53 canonical tags, each with aliases and a
pillar) and the ``tags:`` front matter on every post.

For a given article: find sibling articles sharing canonical tags, rank them
by shared-tag count then recency, and link the first in-prose occurrence of a
tag's alias to the best sibling carrying that tag.

Safety — a link is only ever placed inside a ``<p>`` that:
  * lives in the article body (after ``<main>``),
  * contains no existing ``<a``, ``<code`` or ``<pre`` (never re-links, never
    touches code),
  * is not inside the lead/summary aside or the related-reading strip.
At most one link per paragraph, one link per target article, and never a
self-link. Idempotent: a second pass finds the paragraphs already carry ``<a``
and does nothing.
"""

from __future__ import annotations

import html as _html
import re
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - yaml ships in requirements.txt
    yaml = None  # type: ignore[assignment]

from _frontmatter import parse_frontmatter as _parse_frontmatter
from postbuild_lib._i18n import _detect_page_lang, _slug_maps

POSTS = Path("_posts")
TAXONOMY = Path("_data") / "taxonomy.yml"
BASE_URL = "https://sebastienrousseau.com"

# How many contextual links one article may gain. Six is enough to seat an
# article in its cluster without the prose reading like a link farm; the gate
# in tests/validation/test_internal_links.py requires at least four total
# internal links per article, counting the related-reading strip.
MAX_LINKS_PER_PAGE = 6

_DATED_STEM_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-")

_MAIN_OPEN_RE = re.compile(r"<main\b[^>]*>", re.IGNORECASE)
_PARA_RE = re.compile(r"<p\b[^>]*>(?P<body>[\s\S]*?)</p>", re.IGNORECASE)
# Paragraphs we never touch: anything already carrying a link or code, and the
# lead/summary strip (which has its own curated related-reading list).
_SKIP_IN_PARA_RE = re.compile(r"<a\b|<code\b|<pre\b|post-lead|heading-anchor", re.IGNORECASE)
# Anchors this pass placed on a previous run, identified by their marker
# attribute so re-running is a no-op rather than a second round of links.
_EXISTING_LINK_RE = re.compile(
    r'<a href="/(?:[a-z-]+/)?(?P<stem>\d{4}-\d{2}-\d{2}-[^"/]+)/"[^>]*\bdata-topic-link\b',
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Corpus + taxonomy
# ---------------------------------------------------------------------------


def load_taxonomy(path: Path = TAXONOMY) -> dict:
    if yaml is None or not path.is_file():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def alias_to_canonical(taxonomy: dict) -> dict[str, str]:
    """Lowercased alias (and slug) -> canonical tag slug."""
    out: dict[str, str] = {}
    for slug, entry in taxonomy.items():
        out[slug.strip().lower()] = slug
        for alias in (entry or {}).get("aliases", []) or []:
            out[str(alias).strip().lower()] = slug
    return out


def _canonical_tags(raw: str, aliases: dict[str, str]) -> set[str]:
    tags: set[str] = set()
    for part in raw.split(","):
        key = part.strip().lower()
        if key in aliases:
            tags.add(aliases[key])
    return tags


def load_corpus(posts: Path = POSTS, taxonomy: dict | None = None) -> list[dict]:
    """Every dated English post as ``{stem, title, tags}``, newest first."""
    taxonomy = load_taxonomy() if taxonomy is None else taxonomy
    aliases = alias_to_canonical(taxonomy)
    corpus: list[dict] = []
    if not posts.is_dir():
        return corpus
    for path in sorted(posts.glob("*.md")):
        stem = path.stem
        if not _DATED_STEM_RE.match(stem):
            continue
        fm, _body = _parse_frontmatter(path.read_text(encoding="utf-8"))
        title, tags = fm.get("title"), fm.get("tags")
        if not title or not tags:
            continue
        corpus.append(
            {
                "stem": stem,
                "title": title.strip(),
                "tags": _canonical_tags(tags, aliases),
            }
        )
    corpus.sort(key=lambda a: a["stem"], reverse=True)
    return corpus


# ---------------------------------------------------------------------------
# Alias matching
# ---------------------------------------------------------------------------


def _alias_patterns(taxonomy: dict) -> list[tuple[str, re.Pattern[str]]]:
    """``(canonical_tag, pattern)`` per alias, longest alias first so
    "ISO 20022 payments" wins over "ISO 20022"."""
    entries: list[tuple[str, str]] = []
    for slug, entry in taxonomy.items():
        for alias in (entry or {}).get("aliases", []) or []:
            text = str(alias).strip()
            # Slug-shaped aliases ("iso-20022") never appear in prose.
            if len(text) < 3 or ("-" in text and " " not in text):
                continue
            entries.append((slug, text))
    entries.sort(key=lambda pair: len(pair[1]), reverse=True)
    return [
        (slug, re.compile(rf"(?<![\w-]){re.escape(text)}(?![\w-])", re.IGNORECASE))
        for slug, text in entries
    ]


# ---------------------------------------------------------------------------
# Target selection
# ---------------------------------------------------------------------------


def _page_stem(page: Path, public: Path) -> str | None:
    try:
        parts = page.relative_to(public).parts
    except ValueError:
        return None
    if not parts or parts[-1] != "index.html":
        return None
    stem = parts[-2] if len(parts) >= 2 else ""
    return stem if _DATED_STEM_RE.match(stem) else None


def _localised_url(en_stem: str, lang: str) -> str:
    """Canonical, trailing-slash URL for *en_stem* in *lang*."""
    if lang == "en":
        return f"/{en_stem}/"
    try:
        mapped = _slug_maps(lang)["articles_en_to_lang"].get(en_stem, en_stem)
    except Exception:  # a missing slug map must never fail a build
        mapped = en_stem
    return f"/{lang}/{mapped}/"


def rank_targets(self_tags: set[str], corpus: list[dict], self_stem: str) -> list[dict]:
    """Siblings sharing at least one canonical tag, best first.

    Ordered by shared-tag count, then by recency — the stem carries a
    ``YYYY-MM-DD`` prefix, so a descending lexical sort is a descending date
    sort. Recency is the tiebreak that matters: a 2026 regulatory piece
    should link the current treatment of a topic, not a 2023 post that
    happens to carry the same tag.

    Every other article is returned, not only tag-siblings. A topic named in
    the prose deserves a link to whichever article is its canonical treatment
    even when the current article is not itself tagged with it; ordering by
    shared-tag count keeps same-cluster articles ahead of the rest.
    """
    scored = [
        (len(self_tags & article["tags"]), article["stem"], article)
        for article in corpus
        if article["stem"] != self_stem
    ]
    scored.sort(key=lambda t: (t[0], t[1]), reverse=True)
    return [article for _, _, article in scored]


# ---------------------------------------------------------------------------
# The pass
# ---------------------------------------------------------------------------


class _Placer:
    """Places at most one link per paragraph, one per tag, one per target."""

    def __init__(
        self,
        self_tags: set[str],
        targets: list[dict],
        patterns: list[tuple[str, re.Pattern[str]]],
        lang: str,
    ) -> None:
        self.self_tags = self_tags
        self.patterns = patterns
        self.lang = lang
        self.by_tag: dict[str, list[dict]] = {}
        for article in targets:
            for tag in article["tags"]:
                self.by_tag.setdefault(tag, []).append(article)
        self.used_stems: set[str] = set()
        self.used_tags: set[str] = set()
        self.placed = 0

    def seed_from(self, body: str) -> None:
        """Re-establish state from anchors a previous pass already placed, so
        a re-run is a true no-op instead of adding a second set of links."""
        for m in _EXISTING_LINK_RE.finditer(body):
            stem = m.group("stem")
            self.used_stems.add(stem)
            self.placed += 1
            for tag, articles in self.by_tag.items():
                if any(a["stem"] == stem for a in articles):
                    self.used_tags.add(tag)

    def _candidate(self, tag: str) -> dict | None:
        if tag in self.used_tags:
            return None
        return next((a for a in self.by_tag.get(tag, []) if a["stem"] not in self.used_stems), None)

    def _anchor(self, article: dict, text: str) -> str:
        url = _localised_url(article["stem"], self.lang)
        title = _html.escape(article["title"], quote=True)
        return f'<a href="{url}" title="{title}" data-topic-link>{text}</a>'

    def paragraph(self, m: re.Match[str]) -> str:
        whole = m.group(0)
        if self.placed >= MAX_LINKS_PER_PAGE or _SKIP_IN_PARA_RE.search(whole):
            return whole
        for tag, pattern in self.patterns:
            article = self._candidate(tag)
            if article is None:
                continue
            hit = pattern.search(whole)
            if not hit:
                continue
            self.used_stems.add(article["stem"])
            self.used_tags.add(tag)
            self.placed += 1
            return whole[: hit.start()] + self._anchor(article, hit.group(0)) + whole[hit.end() :]
        return whole


def inject_contextual_links(
    page: Path,
    html: str,
    corpus: list[dict],
    taxonomy: dict,
    public: Path = Path("public"),
    patterns: list[tuple[str, re.Pattern[str]]] | None = None,
) -> str:
    """Link the first in-prose mention of a shared topic to a sibling article."""
    en_stem = _page_stem(page, public)
    if not en_stem:
        return html
    # Locale pages are forked from the English shell before this pass, and a
    # locale's prose is a translation — the English alias strings do not
    # appear in it. Linking there needs per-locale alias tables the taxonomy
    # does not carry.
    lang = _detect_page_lang(html)
    if lang != "en":
        return html
    self_article = next((a for a in corpus if a["stem"] == en_stem), None)
    if not self_article or not self_article["tags"]:
        return html
    targets = rank_targets(self_article["tags"], corpus, en_stem)
    if not targets:
        return html
    # Only the article body — never the head, nav, or lead aside.
    main_m = _MAIN_OPEN_RE.search(html)
    if not main_m:
        return html
    placer = _Placer(
        self_article["tags"],
        targets,
        _alias_patterns(taxonomy) if patterns is None else patterns,
        lang,
    )
    head, body = html[: main_m.end()], html[main_m.end() :]
    placer.seed_from(body)
    return head + _PARA_RE.sub(placer.paragraph, body)


def canonicalise_absolute_self_links(html: str, base: str = BASE_URL) -> str:
    """Give same-origin absolute article links their canonical trailing slash.

    The related-reading strip emitted ``https://sebastienrousseau.com/2026-08-03-slug``
    with no trailing slash, while the canonical, the sitemap and every other
    internal link use ``…/slug/``. Every one of those links therefore pointed
    at a non-canonical URL. Idempotent."""
    pattern = re.compile(rf'href="{re.escape(base)}/(\d{{4}}-\d{{2}}-\d{{2}}-[^"/?#]+)"')
    return pattern.sub(lambda m: f'href="{base}/{m.group(1)}/"', html)


# ---------------------------------------------------------------------------
# Cluster floor — guarantee every article is reachable from its siblings
# ---------------------------------------------------------------------------
#
# Contextual linking is precise but its density is bounded by how much of the
# taxonomy's alias vocabulary happens to appear in a given article's prose. On
# the 2026 regulatory corpus that is often two or three phrases, and articles
# whose lead is hand-curated (`<!-- lead-start: manual -->`) skip post_enrich's
# related-reading strip entirely, so some articles ended up with a single
# internal link. This block is the floor: the highest-overlap siblings not
# already linked on the page, rendered at the end of the article body.
#
# Postbuild-only — it never touches `_posts/` source, so it applies equally to
# manual and generated leads.

CLUSTER_LINK_TARGET = 5

_CLUSTER_MARKER = 'class="cluster-links"'
_ARTICLE_CLOSE_RE = re.compile(r"</article>", re.IGNORECASE)
_MAIN_CLOSE_RE = re.compile(r"</main>", re.IGNORECASE)
_ANY_ARTICLE_HREF_RE = re.compile(
    r'href="(?:' + re.escape(BASE_URL) + r')?/(?:[a-z-]+/)?(\d{4}-\d{2}-\d{2}-[^"/?#]+)/?"'
)

_CLUSTER_HEADING = {
    "en": "Continue reading in this cluster",
}


def _already_linked_stems(html: str) -> set[str]:
    return set(_ANY_ARTICLE_HREF_RE.findall(html))


def _cluster_picks(
    page: Path, html: str, corpus: list[dict], public: Path, target: int
) -> tuple[list[dict], str] | None:
    """The siblings to link, plus the page language — or None if not eligible."""
    en_stem = _page_stem(page, public)
    if not en_stem:
        return None
    lang = _detect_page_lang(html)
    if lang != "en":
        return None
    self_article = next((a for a in corpus if a["stem"] == en_stem), None)
    if not self_article:
        return None
    linked = _already_linked_stems(html)
    picks = [
        a for a in rank_targets(self_article["tags"], corpus, en_stem) if a["stem"] not in linked
    ][:target]
    return (picks, lang) if picks else None


def _cluster_block(picks: list[dict], lang: str) -> str:
    items = "".join(
        f'<li><a href="{_localised_url(a["stem"], lang)}">'
        f"{_html.escape(a['title'], quote=False)}</a></li>"
        for a in picks
    )
    return (
        f'<nav class="cluster-links" aria-labelledby="cluster-links-heading">'
        f'<h2 id="cluster-links-heading" class="cluster-links-heading">'
        f'{_CLUSTER_HEADING["en"]}</h2>'
        f'<ul class="cluster-links-list">{items}</ul></nav>'
    )


def inject_related_cluster(
    page: Path,
    html: str,
    corpus: list[dict],
    public: Path = Path("public"),
    target: int = CLUSTER_LINK_TARGET,
) -> str:
    """Append the article's nearest unlinked siblings as a navigation block."""
    if _CLUSTER_MARKER in html:
        return html
    resolved = _cluster_picks(page, html, corpus, public, target)
    if resolved is None:
        return html
    close = _ARTICLE_CLOSE_RE.search(html) or _MAIN_CLOSE_RE.search(html)
    if not close:
        return html
    block = _cluster_block(*resolved)
    return html[: close.start()] + block + html[close.start() :]
