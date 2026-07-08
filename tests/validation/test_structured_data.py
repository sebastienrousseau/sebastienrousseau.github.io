#!/usr/bin/env python3
"""Gate: every page ships valid, complete article structured data.

The SSG + postbuild emit rich JSON-LD (``BlogPosting`` / ``NewsArticle`` /
``TechArticle`` / ``FAQPage`` / ``BreadcrumbList``). ``test_jsonld_localized``
already checks the ``inLanguage`` localisation; this gate is the complementary
*validity + completeness* check that Google's Rich Results test would apply:

  1. Every ``application/ld+json`` block parses as JSON (no malformed graph).
  2. Every article-type node carries the fields search + AI crawlers need:
     ``headline``, ``author``, ``publisher``, ``inLanguage``, and a URL anchor.
  3. Every page that publishes an article node exposes at least one with
     ``datePublished`` **and** ``image`` (the primary article schema).
  4. Every ``FAQPage`` node carries a non-empty ``mainEntity`` of ``Question``
     nodes, each with an answer — so the FAQ rich result can render.

HTML comments are stripped before extraction: the CSP explainer comment
mentions "JSON-LD blocks" and would otherwise be mis-parsed as a block.

Run from repo root: ``python3 tests/validation/test_structured_data.py``.
Exits non-zero on the first page with a structured-data defect.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"

_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
_LD_RE = re.compile(
    r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script\s*>',
    re.IGNORECASE | re.DOTALL,
)

ARTICLE_TYPES = frozenset(
    {"Article", "BlogPosting", "NewsArticle", "TechArticle", "ScholarlyArticle", "Report"}
)
# Fields every article-type node must carry.
_ARTICLE_REQUIRED = ("headline", "author", "publisher", "inLanguage")
_URL_ANCHORS = ("url", "mainEntityOfPage", "@id")


def _iter_nodes(data: object):
    """Yield every dict node in a JSON-LD document, flattening @graph/lists."""
    stack = [data]
    while stack:
        cur = stack.pop()
        if isinstance(cur, list):
            stack.extend(cur)
        elif isinstance(cur, dict):
            yield cur
            if isinstance(cur.get("@graph"), list):
                stack.extend(cur["@graph"])


def _types(node: dict) -> set[str]:
    t = node.get("@type")
    if isinstance(t, str):
        return {t}
    if isinstance(t, list):
        return {x for x in t if isinstance(x, str)}
    return set()


def _nonempty(node: dict, key: str) -> bool:
    v = node.get(key)
    return v not in (None, "", [], {})


def _faq_ok(node: dict) -> bool:
    me = node.get("mainEntity")
    items = me if isinstance(me, list) else [me] if isinstance(me, dict) else []
    questions = [q for q in items if isinstance(q, dict) and "Question" in _types(q)]
    if not questions:
        return False
    return all(_nonempty(q, "name") and _nonempty(q, "acceptedAnswer") for q in questions)


def _page_defects(html: str) -> list[str]:
    defects: list[str] = []
    stripped = _COMMENT_RE.sub("", html)
    blocks = _LD_RE.findall(stripped)
    has_article = False
    has_primary = False  # an article node with datePublished + image
    for raw in blocks:
        try:
            data = json.loads(raw.strip())
        except json.JSONDecodeError as exc:
            defects.append(f"malformed JSON-LD block: {exc}")
            continue
        for node in _iter_nodes(data):
            types = _types(node)
            if types & ARTICLE_TYPES:
                has_article = True
                missing = [k for k in _ARTICLE_REQUIRED if not _nonempty(node, k)]
                if not any(_nonempty(node, a) for a in _URL_ANCHORS):
                    missing.append("url|mainEntityOfPage")
                if missing:
                    defects.append(
                        f"{'/'.join(sorted(types & ARTICLE_TYPES))} missing {', '.join(missing)}"
                    )
                if _nonempty(node, "datePublished") and _nonempty(node, "image"):
                    has_primary = True
            if "FAQPage" in types and not _faq_ok(node):
                defects.append("FAQPage without a valid Question/answer mainEntity")
    if has_article and not has_primary:
        defects.append("article page has no node with both datePublished and image")
    return defects


def main() -> int:
    if not PUBLIC.is_dir():
        print("error: public/ not built — run ./build.sh first", file=sys.stderr)
        return 1
    bad: dict[str, list[str]] = {}
    scanned = 0
    for page in PUBLIC.rglob("index.html"):
        html = page.read_text(encoding="utf-8", errors="ignore")
        if "application/ld+json" not in html:
            continue
        scanned += 1
        defects = _page_defects(html)
        if defects:
            bad[str(page.relative_to(PUBLIC))] = defects
    if bad:
        print("structured-data defects:", file=sys.stderr)
        for rel, defects in sorted(bad.items())[:30]:
            print(f"  {rel}", file=sys.stderr)
            for d in defects:
                print(f"      {d}", file=sys.stderr)
        if len(bad) > 30:
            print(f"  …and {len(bad) - 30} more pages", file=sys.stderr)
        return 1
    print(f"ok: structured data valid + complete — {scanned} pages scanned")
    return 0


if __name__ == "__main__":
    sys.exit(main())
