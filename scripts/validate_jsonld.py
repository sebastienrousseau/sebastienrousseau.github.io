#!/usr/bin/env python3
"""Lightweight Schema.org JSON-LD validator for built HTML.

This is not a full Schema.org spec validator — Google's Rich Results
Test does that, and there's no offline equivalent that's worth pulling
in as a dependency. Instead, this catches the specific failure modes
we've actually hit on this site:

- malformed JSON inside <script type="application/ld+json">
- missing required fields on the @types we use
- broken URLs (empty href="" / src="" leaking back in)
- duplicate @id collisions across the graph
- unresolved {{template}} placeholders that escaped the SSG pass

Run:
    python3 scripts/validate_jsonld.py [--base-dir public|docs]

Exits non-zero if any page has a hard error; warnings are reported but
don't fail the build.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

JSONLD_RE = re.compile(
    r'<script[^>]*type=["\']?application/ld\+json["\']?[^>]*>([\s\S]*?)</script>',
    re.IGNORECASE,
)
COMMENT_RE = re.compile(r'<!--[\s\S]*?-->')

# Required-property table per @type. Keep narrow — false positives are
# more expensive than missing a real issue, and the Rich Results Test
# covers the wider spec.
REQUIRED: dict[str, set[str]] = {
    "BlogPosting":      {"headline", "author", "datePublished"},
    "Article":          {"headline", "author", "datePublished"},
    "NewsArticle":      {"headline", "author", "datePublished"},
    "Person":           {"name"},
    "Organization":     {"name"},
    "WebSite":          {"name", "url"},
    "WebPage":          {"name"} ,
    "ImageObject":      {"url"},
    "BreadcrumbList":   {"itemListElement"},
    "ListItem":         {"position", "name"},
    "ItemList":         {"itemListElement"},
    "FAQPage":          {"mainEntity"},
    "Question":         {"name", "acceptedAnswer"},
    "Answer":           {"text"},
    "ProfilePage":      {"mainEntity"},
    "SpeakableSpecification": {"cssSelector"},
}


def iter_typed_nodes(obj, parent_key=None):
    """Yield (type_str, node) tuples for every Schema.org node we can find,
    recursing into @graph arrays and child objects."""
    if isinstance(obj, dict):
        t = obj.get("@type")
        if isinstance(t, str):
            yield t, obj
        elif isinstance(t, list):
            for s in t:
                if isinstance(s, str):
                    yield s, obj
        for k, v in obj.items():
            yield from iter_typed_nodes(v, parent_key=k)
    elif isinstance(obj, list):
        for item in obj:
            yield from iter_typed_nodes(item, parent_key=parent_key)


def validate_page(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    html = path.read_text(encoding="utf-8", errors="ignore")
    # Strip HTML comments first — they can contain literal
    # <script type="application/ld+json"> text (documentation) that we
    # don't want the regex to match as a real script block.
    html = COMMENT_RE.sub('', html)
    blocks = JSONLD_RE.findall(html)
    if not blocks:
        return errors, warnings

    ids_seen: set[str] = set()
    for i, raw in enumerate(blocks):
        body = raw.strip()
        # Unresolved templating leaking through.
        if "{{" in body or "}}" in body and not body.count("}") == body.count("{"):
            errors.append(f"block#{i}: unresolved template token ({'{{' if '{{' in body else '}}'} found)")
        try:
            data = json.loads(body)
        except json.JSONDecodeError as e:
            errors.append(f"block#{i}: invalid JSON ({e.msg} at line {e.lineno} col {e.colno})")
            continue

        for type_str, node in iter_typed_nodes(data):
            # Skip pure @id references — these are pointers to a node
            # defined elsewhere (in the same graph or another page), not
            # full node definitions.
            keys_no_at = {k.lstrip("@") for k in node.keys()}
            if keys_no_at <= {"type", "id"}:
                continue
            required = REQUIRED.get(type_str)
            if required:
                present = set(node.keys()) | keys_no_at
                missing = required - present
                if missing:
                    errors.append(f"{type_str}: missing required {sorted(missing)}")
            # @id uniqueness within the page.
            nid = node.get("@id")
            if isinstance(nid, str):
                if nid in ids_seen:
                    warnings.append(f"{type_str}: duplicate @id {nid!r}")
                ids_seen.add(nid)
            # Empty url/href detection.
            for key in ("url", "href", "image", "sameAs"):
                val = node.get(key)
                if isinstance(val, str) and val.strip() == "":
                    errors.append(f"{type_str}.{key} is empty string")
                elif isinstance(val, list):
                    if any(isinstance(x, str) and x.strip() == "" for x in val):
                        errors.append(f"{type_str}.{key}[] contains empty string")

    return errors, warnings


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--base-dir", default="public",
                   help="HTML tree to validate (default: public)")
    args = p.parse_args()
    base = Path(args.base_dir)
    if not base.is_dir():
        print(f"ERROR: {base} not found", file=sys.stderr)
        return 2

    pages = sorted(base.rglob("*.html"))
    total_errors = 0
    total_warnings = 0
    failed_pages = 0
    for page in pages:
        errs, warns = validate_page(page)
        if errs or warns:
            rel = page.relative_to(base).as_posix()
            for e in errs:
                print(f"ERROR  {rel}: {e}")
            for w in warns:
                print(f"WARN   {rel}: {w}")
            total_errors += len(errs)
            total_warnings += len(warns)
            if errs:
                failed_pages += 1

    print()
    print(
        f"validate_jsonld: {len(pages)} HTML pages scanned, "
        f"{failed_pages} with errors, "
        f"{total_errors} error(s), {total_warnings} warning(s)"
    )
    return 1 if total_errors else 0


if __name__ == "__main__":
    sys.exit(main())
