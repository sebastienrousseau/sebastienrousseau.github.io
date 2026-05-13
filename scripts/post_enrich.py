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

import re
from datetime import date
from pathlib import Path

POSTS = Path("_posts")
TODAY = date.today().isoformat()
DATED = re.compile(r"^\d{4}-\d{2}-\d{2}-.+\.md$")

# H2 titles that are structural rather than substantive; skipped when
# auto-deriving key takeaways. Lowercased for comparison.
GENERIC_H2 = {
    "insight", "introduction", "background", "overview", "summary",
    "conclusion", "references", "related articles", "related reading",
    "further reading", "key takeaways", "table of contents",
}

# Marker pairs.
LEAD_START = "<!-- lead-start -->"
LEAD_END   = "<!-- lead-end -->"
LEAD_BLOCK_RE = re.compile(
    rf"{re.escape(LEAD_START)}[\s\S]*?{re.escape(LEAD_END)}\s*",
    re.MULTILINE,
)
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
    or None if absent."""
    for m in re.finditer(r"^# (.+)$", body, re.MULTILINE):
        return m.group(1).strip(), m.end()
    return None


def post_url(post: dict) -> str:
    return post["url"] or f"/{post['path'].stem}/index.html"


def build_lead(excerpt: str, takeaways: list[str], related: list[dict]) -> str:
    # Render the lead as an HTML <aside class="post-lead"> rather than a
    # markdown blockquote. The unique CSS class is the anchor for Schema.org
    # SpeakableSpecification (so voice assistants + AI Overviews know the
    # canonical block to quote) and gives us a stable styling hook.
    parts: list[str] = ["", LEAD_START, '<aside class="post-lead" aria-label="Article summary">']
    parts.append(f'<p class="post-lead-tldr"><strong>TL;DR.</strong> {md_inline_to_html(excerpt)}</p>')
    if takeaways:
        parts.append('<p class="post-lead-heading"><strong>Key takeaways</strong></p>')
        parts.append('<ul class="post-lead-takeaways">')
        parts.extend(f"  <li>{md_inline_to_html(t)}</li>" for t in takeaways)
        parts.append('</ul>')
    if related:
        links = ", ".join(
            f'<a href="{post_url(r)}">{md_inline_to_html(strip_md(r["title"]))}</a>'
            for r in related
        )
        parts.append(f'<p class="post-lead-related"><strong>Related reading:</strong> {links}.</p>')
    parts.append('</aside>')
    parts.append(LEAD_END)
    parts.append("")
    return "\n".join(parts)


def md_inline_to_html(text: str) -> str:
    """Convert the inline-markdown subset we use in lead content (bold, italic,
    inline-code, links) to HTML. Lead is rendered as raw HTML now, so the
    markdown processor won't see it.
    """
    # Links: [text](url) — do this first so the URL contents don't trip the
    # other patterns.
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    # Bold: **text**
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    # Italic: *text*  (avoid eating bold by requiring the prior ** to be gone)
    text = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', text)
    # Inline code: `text`
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    return text


# ---------------------------------------------------------------------------

def main() -> None:  # noqa: C901 — multi-stage enrich pipeline; sequential by design
    posts: list[dict[str, object]] = []
    for md in sorted(POSTS.glob("*.md")):
        if not DATED.match(md.name):
            continue
        parts = split_frontmatter(md.read_text())
        if not parts:
            continue
        fm, body = parts
        body_text = "".join(body)
        post = {
            "path": md,
            "fm": fm,
            "body": body_text,
            "title": fm_get(fm, "title") or md.stem,
            "url": fm_get(fm, "url") or "",
            "image": fm_get(fm, "image") or "",
            "date_iso": md.name[:10],
            "tags": [t.strip() for t in (fm_get(fm, "tags") or "").split(",") if t.strip()],
        }
        posts.append(post)

    enriched = 0
    led = 0
    for post in posts:
        fm = list(post["fm"])

        # 1. Ensure excerpt + last_reviewed in frontmatter.
        if not fm_get(fm, "excerpt"):
            fm = fm_set(fm, "excerpt", derive_excerpt(post["body"]).replace('"', "'"))
        if not fm_get(fm, "last_reviewed"):
            fm = fm_set(fm, "last_reviewed", TODAY)

        # TL;DR sentence prefers the hand-written `description` (curated for
        # SEO and AI Overviews) and falls back to the auto-derived excerpt
        # only when description is missing or trivially short.
        description = fm_get(fm, "description") or ""
        excerpt = fm_get(fm, "excerpt") or ""
        tldr = description if len(description) >= 80 else (excerpt or description)

        # 2. Topic-cluster related posts (tag overlap, up to 3).
        own_tags = set(t.lower() for t in post["tags"])
        scored = []
        for other in posts:
            if other["path"] == post["path"]:
                continue
            other_tags = set(t.lower() for t in other["tags"])
            score = len(own_tags & other_tags)
            if score:
                scored.append((score, other["date_iso"], other))
        scored.sort(key=lambda x: (-x[0], -int(x[1].replace("-", ""))))
        related = [o for _, _, o in scored[:3]]

        # 3. Top-of-body lead block (idempotent + opt-out if hand-curated).
        body_text = post["body"]
        body_text = remove_existing_lead(body_text)

        if body_starts_with_lead(body_text):
            # The post already opens with a hand-written Key Takeaways block;
            # leave it alone for the lead, but still update bottom enrichment.
            pass
        else:
            takeaways = derive_key_takeaways(body_text)
            lead = build_lead(tldr, takeaways, related)

            # Insert the lead AFTER the body's H1 if one exists, otherwise
            # at the very top of the body content (immediately after the
            # trailing "---\n" of frontmatter, which the body string carries).
            h1 = first_h1(body_text)
            if h1:
                _, end = h1
                # Skip past any trailing newline characters.
                while end < len(body_text) and body_text[end] in "\r\n":
                    end += 1
                body_text = body_text[:end] + lead + body_text[end:]
            else:
                # Find first non-blank content position; body usually starts
                # with one or more leading newlines from the frontmatter
                # delimiter — preserve them.
                body_text = "\n" + lead + body_text.lstrip("\n")
            led += 1

        # 4. Bottom-of-body enrichment block (Last reviewed + Related grid).
        body_text = body_text.rstrip()
        body_text = ENRICH_BLOCK_RE.sub("", body_text)
        block = ["", "<!-- enrich-start -->"]
        block.append(
            f'<p class="post-reviewed">Last reviewed '
            f'<time datetime="{TODAY}">{TODAY}</time>.</p>'
        )
        if related:
            block.append('<aside class="related-posts" aria-labelledby="related-heading">')
            block.append('<h2 id="related-heading" class="related-heading">Related reading</h2>')
            block.append('<div class="related-grid">')
            for r in related:
                title = r["title"].replace('"', "&quot;")
                url = post_url(r)
                img = r["image"] or ""
                img_html = (
                    f'<img alt="{title}" src="{img}" loading="lazy" decoding="async" width="600" height="400" />'
                    if img else ""
                )
                block.append(
                    '<article class="related-card">'
                    f'<a href="{url}" class="related-media" aria-label="{title}" tabindex="-1">{img_html}</a>'
                    '<footer class="related-body">'
                    f'<h3><a href="{url}">{r["title"]}</a></h3>'
                    f'<p><time datetime="{r["date_iso"]}">{r["date_iso"]}</time></p>'
                    '</footer></article>'
                )
            block.append('</div>')
            block.append('</aside>')
        block.append("<!-- enrich-end -->")
        new_body = body_text + "\n" + "\n".join(block) + "\n"

        out_text = "".join(fm) + new_body
        if out_text != post["path"].read_text():
            post["path"].write_text(out_text)
            enriched += 1

    print(f"enriched {enriched}/{len(posts)} dated posts ({led} got a new top-of-body lead block)")


if __name__ == "__main__":
    main()
