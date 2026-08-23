#!/usr/bin/env python3
"""Internal topic-cluster linker.

Scans the body of each dated post in ``_posts/`` and, for the first
occurrence of any curated technical entity, replaces the bare phrase with
a markdown link to the canonical post for that entity. Strengthens topical
authority and gives AI engines a cleaner entity graph to follow.

Safety:
- Only the first occurrence per entity per post is linked.
- Skipped if the post is itself the canonical for that entity.
- Skipped if the match falls inside YAML frontmatter, a Markdown heading,
  inline code, fenced code, an existing Markdown link, or the enrichment
  block (TL;DR + Related reading + Last reviewed).
- Idempotent: re-runs are no-ops once every applicable post has gained
  its links.
"""

from __future__ import annotations

import sys as _sys  # path bootstrap — scripts reorg (scripts/lib/ on sys.path)
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "lib"))

import re
from pathlib import Path

POSTS = Path("_posts")

# Curated entity -> canonical post stem. Anchor text uses the first variant;
# the regex matches any variant. Each canonical stem maps to the post that
# defines or owns the entity — we never self-link a post to itself.
ENTITY_MAP: list[tuple[list[str], str]] = [
    (["pain001"], "2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001"),
    (["ISO 20022"], "2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001"),
    (["KyberLib"], "2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats"),
    (["CRYSTALS-Kyber"], "2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age"),
    (
        ["Hash (HSH)", "HSH library"],
        "2023-10-16-protecting-data-in-the-quantum-age-the-hash-library-hsh",
    ),
    (
        ["libmake"],
        "2023-10-26-libmake-a-code-generator-to-reduce-repetitive-tasks-and-build-high-quality-rust-libraries",
    ),
    (
        ["DateTime (DTT)", "DTT library"],
        "2023-12-04-mastering-date-and-time-in-rust-with-the-dtt-library",
    ),
    (["Static Site Generator"], "2023-10-09-the-fastest-rust-based-static-site-generator"),
    (["OpenVoice"], "2024-04-01-openvoice-leading-innovation-in-voice-cloning-technology"),
    (
        ["Akande"],
        "2024-02-12-akande-voice-assistant-revolutionising-personal-and-executive-assistance",
    ),
    (
        ["Quantum Key Distribution", "QKD"],
        "2023-12-11-quantum-key-distribution-revolutionising-security-in-banking",
    ),
    (["Quantum-Safe Payments"], "2025-09-01-quantum-safe-payments-epaa"),
]

DATED_NAME = re.compile(r"^\d{4}-\d{2}-\d{2}-")


def split_segments(body: str) -> list[tuple[str, bool]]:
    """Split body into (segment, is_protected) chunks. Protected segments are
    fenced code, inline code, existing markdown links, ATX headings, and
    raw HTML blocks — we don't touch those."""
    PROTECT_RE = re.compile(
        r"(?ms)"
        r"(```[\s\S]*?```)"  # fenced code blocks
        r"|(`[^`\n]+`)"  # inline code
        r"|(\[[^\]\n]*\]\([^)\n]+\))"  # existing markdown link
        r"|(^\#{1,6}\s.*?$)"  # ATX heading
        r"|(<[a-zA-Z][^>]*>[\s\S]*?</[a-zA-Z][^>]*>)"  # raw HTML block
        r"|(^\s*\[[^\]]+\]:\s.*?$)"  # reference-style link def line
    )
    segments: list[tuple[str, bool]] = []
    last = 0
    for m in PROTECT_RE.finditer(body):
        if m.start() > last:
            segments.append((body[last : m.start()], False))
        segments.append((m.group(0), True))
        last = m.end()
    if last < len(body):
        segments.append((body[last:], False))
    return segments


def link_segment(segment: str, entities: list[tuple[list[str], str]]) -> tuple[str, set[int]]:
    """Replace the first match of each remaining entity in `segment` with a
    Markdown link. Match is case-insensitive but the anchor text is taken
    from the source (preserves authorial casing). Returns
    (new_segment, indexes_of_entities_consumed)."""
    consumed: set[int] = set()
    out = segment
    for idx, (variants, stem) in enumerate(entities):
        pattern_parts = [re.escape(v) for v in variants]
        pat = re.compile(r"\b(" + "|".join(pattern_parts) + r")\b", re.IGNORECASE)
        m = pat.search(out)
        if not m:
            continue
        anchor = m.group(0)  # preserve source casing
        url = f"/{stem}/index.html"
        replacement = f"[{anchor}]({url})"
        out = out[: m.start()] + replacement + out[m.end() :]
        consumed.add(idx)
    return out, consumed


FRONTMATTER_RE = re.compile(r"^(---\s*\n.*?\n---\s*\n)(.*)$", re.DOTALL)
LEAD_BLOCK_RE = re.compile(r"<!-- lead-start -->[\s\S]*?<!-- lead-end -->")
ENRICH_BLOCK_RE = re.compile(r"<!-- enrich-start -->[\s\S]*?<!-- enrich-end -->")


def _body_regions(body: str) -> list[tuple[str, bool]]:
    """Split *body* into ``(text, is_protected)`` pieces covering it exactly.

    The lead and enrich blocks are auto-regenerated and any links inside them
    belong to post_enrich.py, so they are carved out as protected holes.
    """
    holes: list[tuple[int, int, str]] = []
    for pattern in (LEAD_BLOCK_RE, ENRICH_BLOCK_RE):
        hm = pattern.search(body)
        if hm:
            holes.append((hm.start(), hm.end(), hm.group(0)))
    holes.sort()

    pieces: list[tuple[str, bool]] = []
    cursor = 0
    for start, end, text in holes:
        if start > cursor:
            pieces.append((body[cursor:start], False))
        pieces.append((text, True))
        cursor = end
    if cursor < len(body):
        pieces.append((body[cursor:], False))
    return pieces


def _applicable_entities(body: str, stem: str) -> list[tuple[list[str], str]]:
    """Entities this post may link.

    Drops the entity whose canonical post IS this file (no self-link), and any
    entity whose canonical URL is already present — the across-runs
    idempotency guard, since a previous pass placed exactly one link for it.
    """
    out: list[tuple[list[str], str]] = []
    for variants, canonical_stem in ENTITY_MAP:
        if canonical_stem == stem or f"/{canonical_stem}/index.html" in body:
            continue
        out.append((variants, canonical_stem))
    return out


def _link_region(
    region_text: str, applicable: list[tuple[list[str], str]], remaining_idx: list[int]
) -> tuple[str, list[int]]:
    """Link one unprotected region, returning its text and the still-unused
    entity indices. Segments that are themselves protected (code, headings,
    existing links) are passed through untouched."""
    new_sub: list[str] = []
    for seg, seg_protected in split_segments(region_text):
        if seg_protected or not remaining_idx:
            new_sub.append(seg)
            continue
        active = [applicable[i] for i in remaining_idx]
        new_seg, consumed_local = link_segment(seg, active)
        if consumed_local:
            consumed_global = {remaining_idx[i] for i in consumed_local}
            remaining_idx = [i for i in remaining_idx if i not in consumed_global]
        new_sub.append(new_seg)
    return "".join(new_sub), remaining_idx


def process_post(path: Path) -> int:
    """Return number of new internal links added to this post."""
    src = path.read_text()
    m = FRONTMATTER_RE.match(src)
    if not m:
        return 0
    fm_block, body = m.group(1), m.group(2)

    applicable = _applicable_entities(body, path.stem)
    remaining_idx = list(range(len(applicable)))

    out_pieces: list[str] = []
    for region_text, protected in _body_regions(body):
        if protected or not remaining_idx:
            out_pieces.append(region_text)
            continue
        linked, remaining_idx = _link_region(region_text, applicable, remaining_idx)
        out_pieces.append(linked)

    new_body = "".join(out_pieces)
    if new_body == body:
        return 0

    path.write_text(fm_block + new_body)
    return len(applicable) - len(remaining_idx)


def main() -> None:
    # `--dir` is REQUIRED, with no default — see ADR-0003. This linker rewrites
    # post bodies in place; defaulting to `_posts` meant a bare run silently
    # mutated committed source. Callers pass `--dir _posts` (intentional source
    # write) or `--dir _posts_build` (build copy).
    import argparse

    parser = argparse.ArgumentParser(
        description="Inject topic-cluster cross-links into dated posts."
    )
    parser.add_argument(
        "--dir",
        required=True,
        help="Directory of posts to link (e.g. _posts). Required: this rewrites "
        "files in place, so the target must be explicit (ADR-0003).",
    )
    args = parser.parse_args()
    posts_dir = Path(args.dir)

    posts = sorted(p for p in posts_dir.glob("*.md") if DATED_NAME.match(p.name))
    total_links = 0
    touched = 0
    for p in posts:
        before = p.read_text()
        added = process_post(p)
        if p.read_text() != before:
            touched += 1
            total_links += added
    print(f"topic_link: {touched}/{len(posts)} posts touched, ~{total_links} links added")


if __name__ == "__main__":
    main()
