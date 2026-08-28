#!/usr/bin/env python3
"""No translation-pipeline artefacts may reach a post.

Articles are drafted and translated through tooling, and four of its
artefacts have leaked into ``_posts`` and been published:

* ``BEGIN_TRANSLATION`` separating a truncated first copy of a document from
  a complete second one — 8 posts, which rendered the second copy's YAML
  comments as H1s and served the body twice.
* A trailing ``END_TRANSLATION`` — 15 posts, rendered as literal text.
* ``</content>`` and ``</invoke>`` tool-call tags, on their own line or
  appended to the last reference — 8 posts.
* Anything after ``<!-- enrich-end -->``, the marker that terminates the
  article furniture — 144 posts, carrying stray ``---``, ``` ``` ``` fences
  and one English translator's note.

118 rendered pages were serving one of these. None is ever legitimate, so
this gate fails the build rather than recording a backlog: the fix is always
to delete the artefact.

Usage:  python3 tests/validation/test_no_pipeline_artefacts.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POSTS = ROOT / "_posts"

END_MARKER = "<!-- enrich-end -->"
_MARKERS = ("BEGIN_TRANSLATION", "END_TRANSLATION")
_TOOL_TAG = re.compile(r"</?(?:invoke|content|antml:[a-z]+)\b[^>]*>")
_FRONTMATTER_COMMENT = "# RSS - The RSS feed front matter (YAML)."


def offences(text: str) -> list[str]:
    """Every artefact found in one post's source."""
    found = [f"contains {m}" for m in _MARKERS if m in text]
    tags = sorted(set(_TOOL_TAG.findall(text)))
    if tags:
        found.append(f"tool-call tags {tags}")
    if text.count(_FRONTMATTER_COMMENT) > 1:
        found.append("duplicated frontmatter block")
    if END_MARKER in text and text.split(END_MARKER)[-1].strip():
        trailing = text.split(END_MARKER)[-1].strip()[:60]
        found.append(f"content after {END_MARKER}: {trailing!r}")
    return found


def main() -> int:
    failures: list[str] = []
    scanned = 0
    for post in sorted(POSTS.rglob("*.md")):
        scanned += 1
        failures.extend(
            f"{post.relative_to(ROOT)}: {offence}"
            for offence in offences(post.read_text(encoding="utf-8"))
        )

    if failures:
        for line in failures:
            print(f"FAIL {line}", file=sys.stderr)
        print(
            f"\npipeline-artefacts: {len(failures)} offence(s) in {scanned} posts. "
            f"Delete the artefact — none of these is ever content.",
            file=sys.stderr,
        )
        return 1
    print(f"ok: no translation-pipeline artefacts in {scanned} posts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
