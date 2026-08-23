#!/usr/bin/env python3
"""Generate the curated /tags/ cover page that replaces the monolith.

Reads ``_data/taxonomy.yml`` + ``_posts/*.md`` frontmatter, resolves
each tag string through the taxonomy alias map, and writes a curated
cover page to ``_posts_build/tags.md``. The cover renders:

1. **6 pillar category cards** — one per editorial pillar (ai /
   payments / infra / policy / open-source / leadership), with the
   total article count under each.
2. **Featured tags** — top 12 canonicals by article count, rendered
   as cards with article count.
3. **All canonicals A–Z** — every landing-eligible canonical (≥ 3
   posts) as an alphabet jump list. Future commits add per-tag
   landing pages at ``/tags/<slug>/``; for now anchors point at the
   in-page section.

The original ``_posts/tags.md`` frontmatter stays untouched (banner,
SEO meta, hreflang, etc.); only the ``[[content]]`` placeholder is
swapped for the curated body.

Runs **before ssg** in ``build.sh`` so the generator output flows
through the full pipeline (build_translations forks locale variants,
postbuild fingerprints CSS + injects breadcrumbs/etc.).

Exit code 0 on success. No-op when ``_data/taxonomy.yml`` is missing.

Run from repo root::

    python3 scripts/generators/build_tags.py --dir _posts_build
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
SOURCE = ROOT / "_posts" / "tags.md"
PILLAR_ORDER = ("ai", "payments", "infra", "policy", "open-source", "leadership")
PILLAR_LABELS: dict[str, str] = {
    "ai": "Applied AI",
    "payments": "Payments & money",
    "infra": "Infrastructure & cryptography",
    "policy": "Policy & resilience",
    "open-source": "Open source",
    "leadership": "Banking leadership",
}
PILLAR_DECKS: dict[str, str] = {
    "ai": "Generative AI, agentic systems, governance, and the LLM tooling that lands in banking workflows.",
    "payments": "Rails, settlement, tokenisation, treasury programmability, and the economics of moving money.",
    "infra": "Post-quantum cryptography, cloud-native banking, platform engineering, and the engineering stack that runs the rail.",
    "policy": "DORA, EU AI Act, NIST standards, third-party risk — the supervisory pressure shaping technology decisions.",
    "open-source": "OSS in regulated banking — supply-chain trust, Rust, MCP, the projects banks rely on and ship.",
    "leadership": "CTO / CIO concerns — strategic technology decisions, organisational design, original analysis.",
}
_FEATURED_TOP_N = 12
_LANDING_THRESHOLD = 3
_TAG_FM_RE = re.compile(r'^tags:\s*"?([^"\n]+)"?', re.MULTILINE)
_TITLE_FM_RE = re.compile(r'^title:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
from _core import DATED_SLUG_RE as _DATED_SLUG_RE  # canonical dated-slug matcher


def _alias_map(taxonomy: dict) -> dict[str, str]:
    out: dict[str, str] = {}
    for slug, entry in taxonomy.items():
        out[slug.strip().lower()] = slug
        for alias in entry.get("aliases", []) or []:
            out[alias.strip().lower()] = slug
    return out


def _post_meta(path: Path) -> tuple[str | None, str, str, str] | None:
    """Extract (title, iso-date, slug, raw-tags-line) from a post.
    Returns None for posts that don't have a dated filename or don't
    carry a tags frontmatter line."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    tags_m = _TAG_FM_RE.search(text)
    if not tags_m:
        return None
    title_m = _TITLE_FM_RE.search(text)
    title = title_m.group(1) if title_m else path.stem
    stem_m = _DATED_SLUG_RE.match(path.stem)
    if not stem_m:
        return title, "", path.stem, tags_m.group(1)
    return title, stem_m.group(1), path.stem, tags_m.group(1)


def _walk_posts(
    taxonomy: dict,
) -> tuple[
    collections.Counter[str],
    dict[str, list[tuple[str, str, str]]],
]:
    """Return (per-canonical post counts, per-canonical [(title, iso-date,
    slug), …] sorted newest-first)."""
    amap = _alias_map(taxonomy)
    counts: collections.Counter[str] = collections.Counter()
    posts: dict[str, list[tuple[str, str, str]]] = collections.defaultdict(list)
    for path in sorted((ROOT / "_posts").glob("*.md")):
        # Skip non-article markdown: hub pages, the homepage (index.md),
        # and anything else without a YYYY-MM-DD date prefix.
        if not _DATED_SLUG_RE.match(path.stem):
            continue
        meta = _post_meta(path)
        if not meta:
            continue
        title, iso_date, slug, tags_line = meta
        seen: set[str] = set()
        for raw in tags_line.split(","):
            tag = raw.strip().strip('"').strip("'").strip()
            canon = amap.get(tag.lower())
            if canon and canon not in seen:
                counts[canon] += 1
                posts[canon].append((title, iso_date, slug))
                seen.add(canon)
    for canon in posts:
        posts[canon].sort(key=lambda p: p[1] or "0000", reverse=True)
    return counts, posts


def _resolved_tag_counts(taxonomy: dict) -> collections.Counter[str]:
    counts, _ = _walk_posts(taxonomy)
    return counts


def _group_by_pillar(taxonomy: dict, counts: collections.Counter[str]) -> dict[str, list[str]]:
    """Return {pillar: [canonical-slug, ...]} sorted by article count desc."""
    groups: dict[str, list[tuple[str, int]]] = {p: [] for p in PILLAR_ORDER}
    for slug, entry in taxonomy.items():
        pillar = entry.get("category", "leadership")
        groups.setdefault(pillar, []).append((slug, counts.get(slug, 0)))
    return {
        pillar: [s for s, _ in sorted(tags, key=lambda x: (-x[1], x[0]))]
        for pillar, tags in groups.items()
    }


def _render_pillar_cards(
    counts: collections.Counter[str],
    by_pillar: dict[str, list[str]],
) -> str:
    """Pillar cards are NAVIGATION (anchors that jump to the matching
    pillar section below) — not section headings themselves. Using
    <h3> in here would skip from the page <h1> to <h3> with no
    intervening <h2>, which is a WCAG hierarchy violation. The
    accessible name comes from the <a>'s aria-label."""
    cards: list[str] = []
    for pillar in PILLAR_ORDER:
        slugs = by_pillar.get(pillar, [])
        article_count = sum(counts.get(s, 0) for s in slugs)
        label = f"{PILLAR_LABELS[pillar]} — {len(slugs)} tags, {article_count} articles"
        cards.append(
            f'<a href="#pillar-{pillar}" class="tag-pillar-card" '
            f'aria-label="{label}">'
            f'<p class="eyebrow">{PILLAR_LABELS[pillar]}</p>'
            f'<p class="tag-pillar-count"><strong>{len(slugs)} tags</strong> · '
            f"{article_count} articles</p>"
            f"<p>{PILLAR_DECKS[pillar]}</p>"
            f"</a>"
        )
    return (
        '<nav aria-label="Editorial pillars" class="tag-pillar-grid">' + "".join(cards) + "</nav>"
    )


def _render_featured_tags(taxonomy: dict, counts: collections.Counter[str]) -> str:
    """Featured cards mirror the pillar cards — anchors, not headings.
    Card text reads as the link label; aria-label provides the SR
    announcement when the visible text doesn't say "articles"."""
    top = sorted(
        ((slug, n) for slug, n in counts.items() if n >= _LANDING_THRESHOLD),
        key=lambda x: -x[1],
    )[:_FEATURED_TOP_N]
    cards = []
    for slug, n in top:
        entry = taxonomy[slug]
        label = f"{entry['name']} — {n} articles"
        cards.append(
            f'<a href="#tag-{slug}" class="tag-featured-card" '
            f'aria-label="{label}">'
            f"<strong>{entry['name']}</strong>"
            f'<span class="meta">{n} articles</span>'
            f"</a>"
        )
    return (
        '<section aria-labelledby="featured-heading" class="tag-featured">'
        '<h2 id="featured-heading">Featured topics</h2>'
        '<nav class="tag-featured-grid" aria-label="Featured topics list">'
        + "".join(cards)
        + "</nav></section>"
    )


def _render_tag_post_list(posts_for_tag: list[tuple[str, str, str]]) -> str:
    """Render a <details> block of articles under this tag, newest first.
    Title text deliberately keeps the post's own title — search will
    surface them and that's the editorial deep-link readers click.

    ``<time datetime="YYYY-MM-DD">`` carries the machine-readable date
    so screen readers announce "12 June 2026", not the literal slug
    string. AAA requirement (WCAG 1.3.1)."""
    if not posts_for_tag:
        return ""
    items = []
    for title, iso_date, slug in posts_for_tag:
        date_label = f'<time datetime="{iso_date}">{iso_date}</time>' if iso_date else ""
        items.append(f'<li><a href="/{slug}/">{title}</a> {date_label}</li>')
    n = len(posts_for_tag)
    return (
        f'<details class="tag-posts"><summary>'
        f"View {n} article{'s' if n != 1 else ''}"
        f"</summary><ul>" + "".join(items) + "</ul></details>"
    )


def _render_pillar_section(
    pillar: str,
    taxonomy: dict,
    counts: collections.Counter[str],
    posts: dict[str, list[tuple[str, str, str]]],
    by_pillar: dict[str, list[str]],
) -> str:
    items = []
    for slug in by_pillar.get(pillar, []):
        n = counts.get(slug, 0)
        if n < 1:
            continue
        entry = taxonomy[slug]
        items.append(
            f'<li id="tag-{slug}"><strong>{entry["name"]}</strong>'
            f' <span class="meta">— {n} article{"s" if n != 1 else ""}</span>'
            f"<p>{entry['description'].strip()}</p>"
            f"{_render_tag_post_list(posts.get(slug, []))}"
            f"</li>"
        )
    return (
        f'<section id="pillar-{pillar}" class="tag-pillar-section">'
        f"<h2>{PILLAR_LABELS[pillar]}</h2>"
        f'<p class="deck">{PILLAR_DECKS[pillar]}</p>'
        f'<ul class="tag-list">' + "".join(items) + "</ul></section>"
    )


def _render_body(
    taxonomy: dict,
    counts: collections.Counter[str],
    posts: dict[str, list[tuple[str, str, str]]],
) -> str:
    by_pillar = _group_by_pillar(taxonomy, counts)
    parts: list[str] = [
        '<p class="deck">Browse the editorial corpus by pillar, by featured topic, or by canonical tag. Each tag expands to show the articles it covers.</p>',
        _render_pillar_cards(counts, by_pillar),
        _render_featured_tags(taxonomy, counts),
    ]
    parts.extend(
        _render_pillar_section(pillar, taxonomy, counts, posts, by_pillar)
        for pillar in PILLAR_ORDER
    )
    return "\n\n".join(parts)


def _write_cover(
    out_dir: Path,
    taxonomy: dict,
    counts: collections.Counter[str],
    posts: dict[str, list[tuple[str, str, str]]],
) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    if not SOURCE.is_file():
        raise FileNotFoundError(f"missing source {SOURCE}")
    template = SOURCE.read_text(encoding="utf-8")
    body = _render_body(taxonomy, counts, posts)
    # Swap the [[content]] placeholder for the curated body. If the
    # placeholder isn't present, append to the end so we never lose
    # frontmatter or the banner line.
    if "[[content]]" in template:
        out_text = template.replace("[[content]]", body, 1)
    else:
        out_text = template + "\n\n" + body
    dest = out_dir / "tags.md"
    dest.write_text(out_text, encoding="utf-8")
    return dest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dir", default="_posts_build", help="Output dir (default _posts_build)")
    args = parser.parse_args()
    if not TAXONOMY.is_file():
        print(f"build_tags: no taxonomy at {TAXONOMY}, skipping", file=sys.stderr)
        return 0
    taxonomy = yaml.safe_load(TAXONOMY.read_text(encoding="utf-8")) or {}
    counts, posts = _walk_posts(taxonomy)
    out_dir = (ROOT / args.dir).resolve()
    dest = _write_cover(out_dir, taxonomy, counts, posts)
    landing = sum(1 for n in counts.values() if n >= _LANDING_THRESHOLD)
    print(
        f"build_tags: wrote {dest.relative_to(ROOT)} — "
        f"{len(taxonomy)} canonical tags, {sum(counts.values())} tagged-post links resolved, "
        f"{landing} landing-eligible."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
