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
TAXONOMY = ROOT / "_data" / "taxonomy.yml"
PUBLIC = ROOT / "public"
TEMPLATE_PATH = PUBLIC / "tags" / "index.html"

_LANDING_THRESHOLD = 3
_BASE_URL = "https://sebastienrousseau.com"
_TAG_FM_RE = re.compile(r'^tags:\s*"?([^"\n]+)"?', re.MULTILINE)
_TITLE_FM_RE = re.compile(r'^title:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)
_EXCERPT_FM_RE = re.compile(r'^excerpt:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)
_DATED_SLUG_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-(.+)$")
_MAIN_RE = re.compile(
    r'(<main\b[^>]*>)([\s\S]*?)(</main>)',
    re.IGNORECASE,
)
_TITLE_RE = re.compile(r"<title>[^<]*</title>", re.IGNORECASE)
_DESC_RE = re.compile(
    r'<meta name="description" content="[^"]*"', re.IGNORECASE
)
_CANONICAL_RE = re.compile(
    r'<link rel="canonical" href="[^"]*"', re.IGNORECASE
)
_OG_TITLE_RE = re.compile(
    r'<meta property="og:title" content="[^"]*"', re.IGNORECASE
)
_OG_DESC_RE = re.compile(
    r'<meta property="og:description" content="[^"]*"', re.IGNORECASE
)
_OG_URL_RE = re.compile(
    r'<meta property="og:url" content="[^"]*"', re.IGNORECASE
)
_HTML_LANG_RE = re.compile(r'<html lang="[^"]*"', re.IGNORECASE)


def _esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#x27;")
    )


def _alias_map(taxonomy: dict) -> dict[str, str]:
    out: dict[str, str] = {}
    for slug, entry in taxonomy.items():
        out[slug.strip().lower()] = slug
        for alias in entry.get("aliases", []) or []:
            out[alias.strip().lower()] = slug
    return out


def _post_meta(path: Path) -> tuple[str, str, str, str, list[str]] | None:
    """Return (title, iso-date, slug, excerpt, [raw tag strings]) or None."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    tags_m = _TAG_FM_RE.search(text)
    if not tags_m:
        return None
    title_m = _TITLE_FM_RE.search(text)
    title = title_m.group(1) if title_m else path.stem
    excerpt_m = _EXCERPT_FM_RE.search(text)
    excerpt = excerpt_m.group(1) if excerpt_m else ""
    stem_m = _DATED_SLUG_RE.match(path.stem)
    iso_date = stem_m.group(1) if stem_m else ""
    raw_tags = [t.strip().strip('"').strip("'").strip() for t in tags_m.group(1).split(",")]
    return title, iso_date, path.stem, excerpt, [t for t in raw_tags if t]


def _canonical_set(raw_tags: list[str], amap: dict[str, str]) -> set[str]:
    """Resolve a post's raw tag strings to a deduplicated set of
    canonical slugs via the alias map."""
    return {amap[r.lower()] for r in raw_tags if r.lower() in amap}


def _ingest_post(
    path: Path,
    amap: dict[str, str],
    posts: dict[str, list[tuple[str, str, str, str]]],
    cooccur: dict[str, collections.Counter[str]],
) -> None:
    meta = _post_meta(path)
    if not meta:
        return
    title, iso_date, slug, excerpt, raw_tags = meta
    canons = _canonical_set(raw_tags, amap)
    for c in canons:
        posts[c].append((title, iso_date, slug, excerpt))
        for other in canons - {c}:
            cooccur[c][other] += 1


def _walk(taxonomy: dict) -> tuple[
    dict[str, list[tuple[str, str, str, str]]],
    dict[str, collections.Counter[str]],
]:
    """Return:
    * per-canonical [(title, iso-date, slug, excerpt), ...] newest first
    * per-canonical Counter of OTHER canonicals that co-occur on the
      same posts — drives the "related tags" sidebar.
    """
    amap = _alias_map(taxonomy)
    posts: dict[str, list[tuple[str, str, str, str]]] = collections.defaultdict(list)
    cooccur: dict[str, collections.Counter[str]] = collections.defaultdict(
        collections.Counter
    )
    for path in sorted((ROOT / "_posts").glob("*.md")):
        if path.name in {"tags.md", "categories.md"}:
            continue
        _ingest_post(path, amap, posts, cooccur)
    for c in posts:
        posts[c].sort(key=lambda p: p[1] or "0000", reverse=True)
    return posts, cooccur


def _render_article_cards(posts_for_tag: list[tuple[str, str, str, str]]) -> str:
    cards = []
    for title, iso_date, slug, excerpt in posts_for_tag:
        date_html = (
            f'<time datetime="{iso_date}" class="card-date">{iso_date}</time>'
            if iso_date
            else ""
        )
        excerpt_html = (
            f'<p class="card-excerpt">{_esc(excerpt)}</p>' if excerpt else ""
        )
        cards.append(
            f'<article class="tag-landing-card">'
            f'<h2><a href="/{slug}/">{_esc(title)}</a></h2>'
            f"{date_html}"
            f"{excerpt_html}"
            f"</article>"
        )
    return "".join(cards)


def _render_related_tags(
    cooccur: collections.Counter[str], taxonomy: dict, slug: str, n: int = 6
) -> str:
    """Render the top-N co-occurring canonical tags as chip links."""
    top = cooccur.most_common(n)
    if not top:
        return ""
    chips = "".join(
        f'<a href="/tags/{other}/" class="related-tag-chip">'
        f'{_esc(taxonomy[other]["name"])} '
        f'<span class="meta">{cnt}</span></a>'
        for other, cnt in top
    )
    return (
        f'<nav aria-labelledby="related-tags-h2-{slug}" class="related-tags">'
        f'<h2 id="related-tags-h2-{slug}">Related tags</h2>'
        f'<p>Topics this tag most often appears with.</p>'
        f"<div class=\"related-tags-grid\">{chips}</div>"
        f"</nav>"
    )


def _render_jsonld(
    slug: str,
    entry: dict,
    posts_for_tag: list[tuple[str, str, str, str]],
) -> str:
    """CollectionPage + ItemList. Both Schema.org types Google indexes
    for topic pages and AI summarisers consume."""
    import json

    url = f"{_BASE_URL}/tags/{slug}/"
    items = [
        {
            "@type": "ListItem",
            "position": i + 1,
            "url": f"{_BASE_URL}/{post_slug}/",
            "name": title,
        }
        for i, (title, _iso, post_slug, _ex) in enumerate(posts_for_tag)
    ]
    payload = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "@id": url,
                "url": url,
                "name": f'{entry["name"]} — Articles',
                "description": entry["description"].strip(),
                "isPartOf": {
                    "@type": "WebSite",
                    "@id": f"{_BASE_URL}/#website",
                },
            },
            {
                "@type": "ItemList",
                "@id": f"{url}#itemlist",
                "numberOfItems": len(items),
                "itemListElement": items,
            },
        ],
    }
    body = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return f'<script type="application/ld+json">{body}</script>'


def _render_landing_body(
    slug: str,
    entry: dict,
    posts_for_tag: list[tuple[str, str, str, str]],
    cooccur: collections.Counter[str],
    taxonomy: dict,
) -> str:
    n = len(posts_for_tag)
    pillar = entry.get("category", "leadership").upper()
    return (
        f'<div class="wrap report-wrap">'
        f'<header class="tag-landing-hero">'
        f'<p class="eyebrow">{_esc(pillar)}</p>'
        f"<h1>{_esc(entry['name'])}</h1>"
        f'<p class="deck">{_esc(entry["description"].strip())}</p>'
        f'<p class="tag-landing-meta">{n} article{"s" if n != 1 else ""}</p>'
        f"</header>"
        f'<section class="tag-landing-list" aria-label="Articles tagged {_esc(entry["name"])}">'
        f"{_render_article_cards(posts_for_tag)}"
        f"</section>"
        + _render_related_tags(cooccur, taxonomy, slug)
        + "</div>"
    )


def _render_landing_html(
    template: str,
    slug: str,
    entry: dict,
    posts_for_tag: list[tuple[str, str, str, str]],
    cooccur: collections.Counter[str],
    taxonomy: dict,
) -> str:
    """Take the /tags/index.html cover as the shell skeleton, swap the
    <main> body, title, description, canonical, og:* meta, and inject
    the per-tag JSON-LD before </head>."""
    url = f"{_BASE_URL}/tags/{slug}/"
    title = f'{entry["name"]} — Articles by topic'
    desc = entry["description"].strip()
    body = _render_landing_body(slug, entry, posts_for_tag, cooccur, taxonomy)
    out = template
    out = _TITLE_RE.sub(f"<title>{_esc(title)}</title>", out, count=1)
    out = _DESC_RE.sub(
        f'<meta name="description" content="{_esc(desc)}"', out, count=1
    )
    out = _CANONICAL_RE.sub(
        f'<link rel="canonical" href="{url}"', out, count=1
    )
    out = _OG_TITLE_RE.sub(
        f'<meta property="og:title" content="{_esc(title)}"', out, count=1
    )
    out = _OG_DESC_RE.sub(
        f'<meta property="og:description" content="{_esc(desc)}"', out, count=1
    )
    out = _OG_URL_RE.sub(
        f'<meta property="og:url" content="{url}"', out, count=1
    )
    out = _MAIN_RE.sub(rf"\1{body}\3", out, count=1)
    jsonld = _render_jsonld(slug, entry, posts_for_tag)
    out = out.replace("</head>", f"{jsonld}</head>", 1)
    return out


def _write_landings(
    taxonomy: dict,
    posts: dict[str, list[tuple[str, str, str, str]]],
    cooccur: dict[str, collections.Counter[str]],
) -> int:
    if not TEMPLATE_PATH.is_file():
        print(
            f"build_tag_landings: missing template {TEMPLATE_PATH}",
            file=sys.stderr,
        )
        return 2
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    written = 0
    for slug, entry in taxonomy.items():
        ps = posts.get(slug, [])
        if len(ps) < _LANDING_THRESHOLD:
            continue
        page_html = _render_landing_html(
            template, slug, entry, ps, cooccur.get(slug, collections.Counter()), taxonomy
        )
        out_path = PUBLIC / "tags" / slug / "index.html"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(page_html, encoding="utf-8")
        written += 1
    return written


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
    written = _write_landings(taxonomy, posts, cooccur)
    print(
        f"build_tag_landings: wrote {written} per-tag landing page(s) "
        f"under public/tags/<slug>/index.html"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
