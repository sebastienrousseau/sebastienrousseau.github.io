#!/usr/bin/env python3
"""Enrich every dated blog post.

Two enrichment passes, both idempotent and bounded by HTML comment markers
so re-running mutates nothing on a clean tree:

  1. ``<!-- lead-start --> … <!-- lead-end -->`` at the **top** of the body.
     A people-first / GEO direct-answer block. Renders as a markdown
     blockquote so it surfaces above the fold:

       > **TL;DR.** 40–60 word direct answer to the page's implied query.
       >
       > **Key takeaways:**
       > - First non-structural H2 in the body, with its first sentence.
       > - Next H2, etc.
       >
       > **Related reading:** [Topic-cluster sibling 1](…), [sibling 2](…).

     If the body already contains a hand-written ``> **Key Takeaways``
     blockquote (as the 2026 articles do), the auto-injection is skipped
     and the existing block is preserved.

  2. ``<!-- enrich-start --> … <!-- enrich-end -->`` at the **bottom**.
     "Last reviewed" badge + a "Related articles" card grid computed
     by tag overlap, same as before.

Frontmatter is augmented in place when ``excerpt`` or ``last_reviewed``
are missing.
"""

from __future__ import annotations

import sys as _sys  # path bootstrap — scripts reorg (scripts/lib/ on sys.path)
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "lib"))

import re
from datetime import date
from pathlib import Path

POSTS = Path("_posts")
TODAY = date.today().isoformat()
DATED = re.compile(r"^\d{4}-\d{2}-\d{2}-.+\.md$")

# H2 titles that are structural rather than substantive; skipped when
# auto-deriving key takeaways. Lowercased for comparison.
GENERIC_H2 = {
    "insight",
    "introduction",
    "background",
    "overview",
    "summary",
    "conclusion",
    "references",
    "related articles",
    "related reading",
    "further reading",
    "key takeaways",
    "table of contents",
}

# Marker pairs.
LEAD_START = "<!-- lead-start -->"
LEAD_END = "<!-- lead-end -->"
LEAD_BLOCK_RE = re.compile(
    rf"{re.escape(LEAD_START)}[\s\S]*?{re.escape(LEAD_END)}\s*",
    re.MULTILINE,
)
# `<!-- lead-start: manual -->` opts a hand-curated lead aside out of
# regeneration. The auto-injector neither strips nor replaces it.
LEAD_MANUAL_MARKER = "<!-- lead-start: manual -->"
ENRICH_BLOCK_RE = re.compile(
    r"\n\n<!-- enrich-start -->[\s\S]*?<!-- enrich-end -->\s*",
)

# Hand-written ``> **Key Takeaways`` blockquote detector — used to opt-out
# of auto lead injection on posts that already curate their own intro.
HAS_HAND_LEAD = re.compile(r"^\s*>\s*\*\*Key Takeaways", re.MULTILINE)


# ---------------------------------------------------------------------------

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _frontmatter import fm_get, fm_set, split_frontmatter


def strip_md(s: str) -> str:
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"\*(.+?)\*", r"\1", s)
    # Inline links: [text](url) -> text
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    # Reference-style links: [text][ref] -> text. Without this, the new HTML
    # lead block ends up with literal "[Rust ⧉][06]" text because the markdown
    # processor doesn't see inside the raw <aside>.
    s = re.sub(r"\[([^\]]+)\]\[[^\]]+\]", r"\1", s)
    s = re.sub(r"`([^`]+)`", r"\1", s)
    return s


def derive_excerpt(body: str) -> str:
    """First non-frontmatter prose paragraph as a 160-char excerpt."""
    cleaned = re.sub(r"^<[^>]+>\s*$", "", body, flags=re.MULTILINE)
    for line in cleaned.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith(("#", "<", "!", "[", "*[")):
            continue
        s = strip_md(s)
        if len(s) > 200:
            s = s[:197].rsplit(" ", 1)[0] + "…"
        return s
    return ""


def derive_key_takeaways(body: str, max_items: int = 4) -> list[str]:  # noqa: C901 — Markdown body walker; the branching IS the spec
    """Auto-derive Key Takeaway bullets from the body.

    Walks the document looking for substantive headings — H2 first, then
    H3 — that aren't structural ("Insight", "Introduction", etc.). For
    each match, pulls the first non-image sentence that follows. Stops
    at ``max_items`` to keep the lead block tight.
    """
    bullets: list[str] = []
    lines = body.splitlines()
    n = len(lines)

    def emit_for_heading(heading: str, start_idx: int) -> bool:  # noqa: C901 — nested paragraph-finder; structural complexity
        if heading.lower() in GENERIC_H2:
            return False
        # Walk forward to the first paragraph (a run of one or more
        # non-blank, non-structural lines). Join wrapped lines together
        # before sentence-splitting, so we don't cut mid-clause.
        paragraph_lines: list[str] = []
        for j in range(start_idx, min(start_idx + 20, n)):
            raw = lines[j].rstrip()
            stripped = raw.strip()
            if not stripped:
                if paragraph_lines:
                    break  # end of the paragraph
                continue
            if stripped.startswith(("#", "<", "!", "*[", "```", "|", ">")):
                if paragraph_lines:
                    break
                continue
            if stripped.startswith(("- ", "* ")):
                if paragraph_lines:
                    break
                continue
            # Reference-style link lines like `[01]: https://…` — skip when
            # at the start of search; treat as paragraph end after content.
            if re.match(r"^\[\d+\]:\s", stripped):
                if paragraph_lines:
                    break
                continue
            paragraph_lines.append(stripped)
        if not paragraph_lines:
            return False
        paragraph = " ".join(paragraph_lines)
        paragraph = strip_md(paragraph)
        # Remove the trailing Shokunin attribute syntax `.class=\"…\"`.
        paragraph = re.sub(r"\s*\.class=\\.+$", "", paragraph)
        # First sentence boundary.
        m = re.search(r"[.!?](?=\s|$)", paragraph)
        sentence = paragraph[: m.end()] if m else paragraph
        if not sentence.endswith((".", "!", "?")):
            sentence += "."
        if len(sentence) > 220:
            sentence = sentence[:217].rsplit(" ", 1)[0] + "…"
        bullets.append(f"**{heading}.** {sentence}")
        return True

    # First pass: H2 headings.
    for i, ln in enumerate(lines):
        if not ln.startswith("## "):
            continue
        heading = strip_md(ln[3:].strip()).rstrip(".").rstrip(":")
        emit_for_heading(heading, i + 1)
        if len(bullets) >= max_items:
            return bullets

    # Fallback: H3 headings if H2s yielded too few.
    if len(bullets) < max_items:
        for i, ln in enumerate(lines):
            if not ln.startswith("### "):
                continue
            heading = strip_md(ln[4:].strip()).rstrip(".").rstrip(":")
            emit_for_heading(heading, i + 1)
            if len(bullets) >= max_items:
                return bullets
    return bullets


def remove_existing_lead(body: str) -> str:
    """Strip any prior auto-injected lead block so re-runs are idempotent."""
    return LEAD_BLOCK_RE.sub("", body, count=1)


def body_starts_with_lead(body: str) -> bool:
    """True if the post already opens with a hand-curated Key Takeaways
    blockquote. We then leave the post alone."""
    head = body[:2000]
    return bool(HAS_HAND_LEAD.search(head))


def first_h1(body: str) -> tuple[str, int] | None:
    """Return (heading_text, index_after_h1) for the body's first H1,
    or None if absent. Correctly ignores headings inside code blocks."""
    lines = body.splitlines()
    in_code_block = False
    current_index = 0
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
        elif not in_code_block and line.startswith("# "):
            heading = line[2:].strip()
            idx = current_index + len(line)
            return heading, idx
        current_index += len(line) + 1
    return None


def post_url(post: dict) -> str:
    return post["url"] or f"/{post['path'].stem}/index.html"


def build_lead(excerpt: str, takeaways: list[str], related: list[dict]) -> str:
    # Render the lead as an HTML <aside class="post-lead"> rather than a
    # markdown blockquote. The unique CSS class is the anchor for Schema.org
    # SpeakableSpecification (so voice assistants + AI Overviews know the
    # canonical block to quote) and gives us a stable styling hook.
    parts: list[str] = ["", LEAD_START, '<aside class="post-lead" aria-label="Article summary">']
    parts.append(
        f'<p class="post-lead-tldr"><strong>TL;DR.</strong> {md_inline_to_html(excerpt)}</p>'
    )
    if takeaways:
        parts.append('<p class="post-lead-heading"><strong>Key takeaways</strong></p>')
        parts.append('<ul class="post-lead-takeaways">')
        parts.extend(f"  <li>{md_inline_to_html(t)}</li>" for t in takeaways)
        parts.append("</ul>")
    if related:
        links = ", ".join(
            f'<a href="{post_url(r)}">{md_inline_to_html(strip_md(r["title"]))}</a>'
            for r in related
        )
        parts.append(f'<p class="post-lead-related"><strong>Related reading:</strong> {links}.</p>')
    parts.append("</aside>")
    parts.append(LEAD_END)
    # Emit two trailing newlines so the lead block ends with a blank line.
    # CommonMark requires a blank line between a raw HTML block and the next
    # markdown block — without it, a heading sitting right after the lead
    # (e.g. `## Introduction` on the very next line) gets parsed as literal
    # text instead of <h2>, which breaks heading-order accessibility.
    parts.append("")
    parts.append("")
    return "\n".join(parts)


def md_inline_to_html(text: str) -> str:
    """Convert the inline-markdown subset we use in lead content (bold, italic,
    inline-code, links) to HTML. Lead is rendered as raw HTML now, so the
    markdown processor won't see it.
    """
    # Links: [text](url) — do this first so the URL contents don't trip the
    # other patterns.
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    # Bold: **text**
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    # Italic: *text*  (avoid eating bold by requiring the prior ** to be gone)
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", text)
    # Inline code: `text`
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


# ---------------------------------------------------------------------------


def _load_post(md: Path) -> dict[str, object] | None:
    """Read one dated post into the internal ``post`` dict, or return
    None if the file isn't a dated post / has no frontmatter."""
    if not DATED.match(md.name):
        return None
    parts = split_frontmatter(md.read_text())
    if not parts:
        return None
    fm, body = parts
    body_text = "".join(body)
    return {
        "path": md,
        "fm": fm,
        "body": body_text,
        "title": fm_get(fm, "title") or md.stem,
        "url": fm_get(fm, "url") or "",
        "image": fm_get(fm, "banner") or fm_get(fm, "image") or "",
        "image_alt": fm_get(fm, "banner_alt") or fm_get(fm, "title") or "",
        "date_iso": md.name[:10],
        "tags": [t.strip() for t in (fm_get(fm, "tags") or "").split(",") if t.strip()],
    }


def _update_frontmatter(post: dict[str, object]) -> tuple[list[str], str]:
    """Stage 1: ensure ``excerpt`` + ``last_reviewed`` in frontmatter.
    Returns the patched frontmatter list and the resolved reviewed-date."""
    fm = list(post["fm"])
    if not fm_get(fm, "excerpt"):
        fm = fm_set(fm, "excerpt", derive_excerpt(post["body"]).replace('"', "'"))
    reviewed = max(TODAY, post["date_iso"])
    existing_reviewed = fm_get(fm, "last_reviewed") or ""
    if not existing_reviewed or existing_reviewed < post["date_iso"]:
        fm = fm_set(fm, "last_reviewed", reviewed)
    return fm, reviewed


def _build_tag_index(
    all_posts: list[dict[str, object]],
) -> dict[str, list[dict[str, object]]]:
    """Build a tag → list-of-posts inverted index. Built once per
    post_enrich.main() run and passed into every _related_posts call,
    collapsing the related-post lookup from O(N²) to O(N · tags_per_post).
    On a 50-post archive this is mildly faster; at the 2000-post horizon
    it's the difference between sub-second and many seconds."""
    idx: dict[str, list[dict[str, object]]] = {}
    for post in all_posts:
        for tag in post["tags"]:
            idx.setdefault(tag.lower(), []).append(post)
    return idx


def _related_posts(
    post: dict[str, object],
    all_posts: list[dict[str, object]],
    tag_index: dict[str, list[dict[str, object]]] | None = None,
) -> list[dict[str, object]]:
    """Stage 2: topic-cluster related posts via tag-overlap score.

    With ``tag_index`` provided (the inverted index built once in
    ``main()``), the lookup walks only posts that share at least one
    tag with ``post`` — no longer the full N. Without it, falls back
    to the O(N) scan so single-post callers (e.g. test fixtures) still
    work without setup.
    """
    own_tags = {t.lower() for t in post["tags"]}
    own_path = post["path"]
    candidates: list[tuple[int, str, dict[str, object]]] = []
    if tag_index is not None:
        # O(tags × posts-per-tag) walk via the inverted index. Score per
        # other-post = count of tags it shares with `post`.
        overlap: dict[int, tuple[int, dict[str, object]]] = {}
        for tag in own_tags:
            for other in tag_index.get(tag, ()):
                if other["path"] == own_path:
                    continue
                oid = id(other)
                if oid in overlap:
                    overlap[oid] = (overlap[oid][0] + 1, other)
                else:
                    overlap[oid] = (1, other)
        candidates = [(score, other["date_iso"], other) for score, other in overlap.values()]
    else:
        # Fallback: O(N) scan for single-post callers (test fixtures).
        for other in all_posts:
            if other["path"] == own_path:
                continue
            other_tags = {t.lower() for t in other["tags"]}
            score = len(own_tags & other_tags)
            if score:
                candidates.append((score, other["date_iso"], other))
    candidates.sort(key=lambda x: (-x[0], -int(x[1].replace("-", ""))))
    return [o for _, _, o in candidates[:3]]


def _insert_lead(body_text: str, tldr: str, related: list[dict[str, object]]) -> tuple[str, bool]:
    """Stage 3: insert the top-of-body lead block. Returns (new_body,
    inserted_flag). Idempotent — skip if a hand-curated lead opens
    the body already."""
    if LEAD_MANUAL_MARKER in body_text[:2000]:
        return body_text, False
    body_text = remove_existing_lead(body_text)
    if body_starts_with_lead(body_text):
        return body_text, False
    takeaways = derive_key_takeaways(body_text)
    lead = build_lead(tldr, takeaways, related)
    h1 = first_h1(body_text)
    if h1:
        _, end = h1
        while end < len(body_text) and body_text[end] in "\r\n":
            end += 1
        body_text = body_text[:end] + lead + body_text[end:]
    else:
        body_text = "\n" + lead + body_text.lstrip("\n")
    return body_text, True


_AUTHOR_CARD_HTML = (
    '<aside class="author-card" aria-label="About the author">'
    '<img alt="Portrait of Sebastien Rousseau" '
    'src="https://cloudcdn.pro/stocks/images/sebastien-rousseau.png" '
    'width="64" height="64" loading="lazy" decoding="async" />'
    '<span class="author-card-body">'
    '<strong class="author-card-name">'
    '<a href="/about/index.html">Sebastien Rousseau</a></strong>'
    '<span class="author-card-bio">Senior banking technologist writing on applied AI, ISO 20022 '
    "migration, post-quantum cryptography for financial services, and "
    "the structural transformation of wholesale payments.</span>"
    '<span class="author-credentials">'
    "20+ years across HSBC Commercial &amp; Investment Bank, PayPal, "
    "Barclays, Shazam, AKQA, Virgin Group. "
    '<a href="/about/index.html">Full profile</a> &middot; '
    '<a href="https://www.linkedin.com/in/sebastienrousseau/" rel="external noopener">LinkedIn</a> &middot; '
    '<a href="https://github.com/sebastienrousseau" rel="external noopener">GitHub</a>'
    "</span></span></aside>"
)


def _related_grid_html(related: list[dict[str, object]], post: dict[str, object]) -> list[str]:
    """Build the bottom Related-reading <aside> when there are matches."""
    if not related:
        return []
    out = [
        '<aside class="related-posts" aria-labelledby="related-heading">',
        '<h2 id="related-heading" class="related-heading">Related reading</h2>',
        '<div class="related-grid">',
    ]
    for r in related:
        title = r["title"].replace('"', "&quot;")
        url = post_url(r)
        img = r["image"] or ""
        alt = (r.get("image_alt") or r["title"]).replace('"', "&quot;")
        img_html = (
            f'<img alt="{alt}" src="{img}" loading="lazy" decoding="async" width="600" height="400" />'
            if img
            else ""
        )
        out.append(
            '<article class="related-card">'
            f'<a href="{url}" class="related-media" aria-label="{title}" tabindex="-1">{img_html}</a>'
            '<footer class="related-body">'
            f'<h3><a href="{url}">{r["title"]}</a></h3>'
            f'<p><time datetime="{r["date_iso"]}">{r["date_iso"]}</time></p>'
            '</footer></article>'
        )
    out.append("</div>")
    out.append("</aside>")
    return out


def _append_enrich_block(
    body_text: str, reviewed: str, related: list[dict[str, object]], post: dict[str, object]
) -> str:
    """Stage 4: append the bottom enrichment block (author card +
    last-reviewed line + related grid). Idempotent — strips any prior
    enrich-start/enrich-end block before re-appending."""
    body_text = body_text.rstrip()
    body_text = ENRICH_BLOCK_RE.sub("", body_text)
    block: list[str] = ["", "<!-- enrich-start -->", _AUTHOR_CARD_HTML]
    block.append(
        f'<p class="post-reviewed">Last reviewed '
        f'<time datetime="{reviewed}">{reviewed}</time>.</p>'
    )
    block.extend(_related_grid_html(related, post))
    block.append("<!-- enrich-end -->")
    return body_text + "\n" + "\n".join(block) + "\n"


def _enrich_one(
    post: dict[str, object],
    all_posts: list[dict[str, object]],
    tag_index: dict[str, list[dict[str, object]]] | None = None,
) -> tuple[bool, bool]:
    """Run all four stages on one post. Returns (was_modified, lead_inserted)."""
    fm, reviewed = _update_frontmatter(post)
    description = fm_get(fm, "description") or ""
    excerpt = fm_get(fm, "excerpt") or ""
    tldr = description if len(description) >= 80 else (excerpt or description)
    related = _related_posts(post, all_posts, tag_index=tag_index)
    body_text, led = _insert_lead(post["body"], tldr, related)
    new_body = _append_enrich_block(body_text, reviewed, related, post)
    out_text = "".join(fm) + new_body
    if out_text != post["path"].read_text():
        post["path"].write_text(out_text)
        return True, led
    return False, led


def main() -> None:
    """Walk every dated post under ``_posts/`` and run the 4-stage
    enrich pipeline on each. Stages: (1) frontmatter excerpt +
    last_reviewed, (2) topic-cluster related lookup, (3) top-of-body
    lead block, (4) bottom enrichment block.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Enrich dated blog posts.")
    parser.add_argument("--dir", default="_posts", help="Directory containing posts")
    args = parser.parse_args()

    posts_dir = Path(args.dir)
    posts: list[dict[str, object]] = []
    for md in sorted(posts_dir.glob("*.md")):
        post = _load_post(md)
        if post is not None:
            posts.append(post)

    # Build the inverted tag → posts index ONCE for the whole loop, then
    # share it across every per-post enrich call. Collapses the related-
    # post lookup from O(N²) to O(N · tags_per_post).
    tag_index = _build_tag_index(posts)

    enriched = 0
    led = 0
    for post in posts:
        was_modified, was_led = _enrich_one(post, posts, tag_index=tag_index)
        if was_modified:
            enriched += 1
        if was_led:
            led += 1

    print(f"enriched {enriched}/{len(posts)} dated posts ({led} got a new top-of-body lead block)")


if __name__ == "__main__":
    main()

