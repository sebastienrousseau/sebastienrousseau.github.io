#!/usr/bin/env python3
"""Enrich every dated blog post with:
   - ``excerpt`` and ``last_reviewed`` frontmatter fields (preserved if already set).
   - A small "Last reviewed" badge appended to the article body.
   - A "Related articles" block at the bottom, computed by tag overlap with the
     other dated posts.

   The script only touches files whose filename matches ``YYYY-MM-DD-*.md`` so
   listing pages, about, contact, etc. are left alone.
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

POSTS = Path("_posts")
TODAY = date.today().isoformat()
DATED = re.compile(r"^\d{4}-\d{2}-\d{2}-.+\.md$")

# ---------------------------------------------------------------------------

def split_frontmatter(text: str) -> tuple[list[str], list[str]] | None:
    # Keep line endings so we can round-trip the file exactly. Lines without "\n"
    # only at end-of-file are tolerated by every join we do.
    lines = text.splitlines(keepends=True)
    bounds = [i for i, ln in enumerate(lines) if ln.strip() == "---"]
    if len(bounds) < 2:
        return None
    return lines[: bounds[1] + 1], lines[bounds[1] + 1 :]


def fm_get(fm_lines: list[str], key: str) -> str | None:
    pat = re.compile(rf'^{re.escape(key)}:\s*"?(.+?)"?\s*$')
    for ln in fm_lines:
        m = pat.match(ln)
        if m:
            return m.group(1)
    return None


def fm_set(fm_lines: list[str], key: str, value: str) -> list[str]:
    pat = re.compile(rf'^{re.escape(key)}:')
    # Lines from splitlines(keepends=True) already include "\n", so the new
    # line we synthesise must too — otherwise it runs straight into the next.
    formatted = f'{key}: "{value}"\n'
    for i, ln in enumerate(fm_lines):
        if pat.match(ln):
            fm_lines[i] = formatted
            return fm_lines
    out = list(fm_lines)
    closing = next(i for i in range(len(out) - 1, -1, -1) if out[i].strip() == "---")
    out.insert(closing, formatted)
    return out


def derive_excerpt(body: str) -> str:
    """Take the first non-frontmatter prose paragraph as a 160-char excerpt."""
    cleaned = re.sub(r"^<[^>]+>\s*$", "", body, flags=re.MULTILINE)
    for line in cleaned.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith(("#", "<", "!", "[", "*[")):
            continue
        # Strip markdown markup
        s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
        s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
        s = re.sub(r"`([^`]+)`", r"\1", s)
        if len(s) > 200:
            s = s[:197].rsplit(" ", 1)[0] + "…"
        return s
    return ""


# ---------------------------------------------------------------------------

def main() -> None:
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

    # Index posts by lowercase tag for relevance scoring.
    enriched = 0
    for post in posts:
        fm = list(post["fm"])
        # 1. Ensure excerpt + last_reviewed.
        if not fm_get(fm, "excerpt"):
            fm = fm_set(fm, "excerpt", derive_excerpt(post["body"]).replace('"', "'"))
        if not fm_get(fm, "last_reviewed"):
            fm = fm_set(fm, "last_reviewed", TODAY)

        # 2. Compute up to 3 related posts by tag overlap.
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

        # 3. Compose body: original + "Last reviewed" + Related block.
        body_text = post["body"].rstrip()
        # Strip any previous markers so re-running is idempotent.
        body_text = re.sub(
            r"\n\n<!-- enrich-start -->[\s\S]*?<!-- enrich-end -->\s*",
            "",
            body_text,
        )
        block = ["", "<!-- enrich-start -->"]
        block.append(f'<p class="post-reviewed">Last reviewed <time datetime="{TODAY}">{TODAY}</time>.</p>')
        if related:
            block.append('<aside class="related-posts" aria-labelledby="related-heading">')
            block.append('<h2 id="related-heading" class="related-heading">Related reading</h2>')
            block.append('<div class="related-grid">')
            for r in related:
                title = r["title"].replace('"', "&quot;")
                url = r["url"] or f"/{r['path'].stem}/index.html"
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

        # fm lines come from splitlines(keepends=True) so they already include
        # their "\n" terminator. Use "" join so we don't double-up the breaks.
        out_text = "".join(fm) + new_body
        if out_text != post["path"].read_text():
            post["path"].write_text(out_text)
            enriched += 1
    print(f"enriched {enriched}/{len(posts)} dated posts")


if __name__ == "__main__":
    main()
