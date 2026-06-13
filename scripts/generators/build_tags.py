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
_DATE_FM_RE = re.compile(r'^date:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)


def _alias_map(taxonomy: dict) -> dict[str, str]:
    out: dict[str, str] = {}
    for slug, entry in taxonomy.items():
        out[slug.strip().lower()] = slug
        for alias in entry.get("aliases", []) or []:
            out[alias.strip().lower()] = slug
    return out


def _resolved_tag_counts(taxonomy: dict) -> collections.Counter[str]:
    amap = _alias_map(taxonomy)
    counts: collections.Counter[str] = collections.Counter()
    for path in sorted((ROOT / "_posts").glob("*.md")):
        if path.name in {"tags.md", "categories.md"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        m = _TAG_FM_RE.search(text)
        if not m:
            continue
        for raw in m.group(1).split(","):
            tag = raw.strip().strip('"').strip("'").strip()
            canon = amap.get(tag.lower())
            if canon:
                counts[canon] += 1
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
    cards: list[str] = []
    for pillar in PILLAR_ORDER:
        slugs = by_pillar.get(pillar, [])
        article_count = sum(counts.get(s, 0) for s in slugs)
        cards.append(
            f'<a href="#pillar-{pillar}" class="tag-pillar-card">'
            f'<p class="eyebrow">{PILLAR_LABELS[pillar]}</p>'
            f'<h3>{len(slugs)} tags · {article_count} articles</h3>'
            f'<p>{PILLAR_DECKS[pillar]}</p>'
            f"</a>"
        )
    return (
        '<section aria-label="Editorial pillars" class="tag-pillar-grid">'
        + "".join(cards)
        + "</section>"
    )


def _render_featured_tags(taxonomy: dict, counts: collections.Counter[str]) -> str:
    top = sorted(
        ((slug, n) for slug, n in counts.items() if n >= _LANDING_THRESHOLD),
        key=lambda x: -x[1],
    )[:_FEATURED_TOP_N]
    cards = []
    for slug, n in top:
        entry = taxonomy[slug]
        cards.append(
            f'<a href="#tag-{slug}" class="tag-featured-card">'
            f'<h3>{entry["name"]}</h3>'
            f'<p class="meta">{n} articles</p>'
            f"</a>"
        )
    return (
        '<section aria-labelledby="featured-heading" class="tag-featured">'
        '<h2 id="featured-heading">Featured topics</h2>'
        '<section class="tag-featured-grid" aria-label="Featured topics list">'
        + "".join(cards)
        + "</section></section>"
    )


def _render_pillar_section(
    pillar: str,
    taxonomy: dict,
    counts: collections.Counter[str],
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
            f"<p>{entry['description'].strip()}</p></li>"
        )
    return (
        f'<section id="pillar-{pillar}" class="tag-pillar-section">'
        f'<h2>{PILLAR_LABELS[pillar]}</h2>'
        f'<p class="deck">{PILLAR_DECKS[pillar]}</p>'
        f'<ul class="tag-list">'
        + "".join(items)
        + "</ul></section>"
    )


def _render_body(taxonomy: dict, counts: collections.Counter[str]) -> str:
    by_pillar = _group_by_pillar(taxonomy, counts)
    parts: list[str] = [
        '<p class="deck">Browse the editorial corpus by pillar, by featured topic, or by canonical tag. Tags with fewer than 3 articles are shown but currently have no dedicated landing page.</p>',
        _render_pillar_cards(counts, by_pillar),
        _render_featured_tags(taxonomy, counts),
    ]
    parts.extend(
        _render_pillar_section(pillar, taxonomy, counts, by_pillar) for pillar in PILLAR_ORDER
    )
    return "\n\n".join(parts)


def _write_cover(out_dir: Path, taxonomy: dict, counts: collections.Counter[str]) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    if not SOURCE.is_file():
        raise FileNotFoundError(f"missing source {SOURCE}")
    template = SOURCE.read_text(encoding="utf-8")
    body = _render_body(taxonomy, counts)
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
    counts = _resolved_tag_counts(taxonomy)
    out_dir = (ROOT / args.dir).resolve()
    dest = _write_cover(out_dir, taxonomy, counts)
    landing = sum(1 for n in counts.values() if n >= _LANDING_THRESHOLD)
    print(
        f"build_tags: wrote {dest.relative_to(ROOT)} — "
        f"{len(taxonomy)} canonical tags, {sum(counts.values())} tagged-post links resolved, "
        f"{landing} landing-eligible."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
