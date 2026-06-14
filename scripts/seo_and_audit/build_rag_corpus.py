#!/usr/bin/env python3
"""Emit `/feed.jsonl` + `/tags/<slug>/feed.jsonl` — RAG-ready corpus.

JSONL (newline-delimited JSON, one object per article) is the
de-facto exchange format for retrieval-augmented-generation pipelines
— Claude, Anthropic Workbench, LlamaIndex, LangChain, Pinecone, FAISS
all consume it natively. Per the editorial-overhaul plan §4 WS6, we
expose the full editorial corpus this way so AI clients can index +
cite our work with the canonical URL preserved.

Each record fields:

  url             — canonical article URL
  title           — frontmatter title
  summary         — frontmatter excerpt (1–2 sentences)
  body_markdown   — raw markdown source (lossy: shortcodes / Tera
                    blocks left as-is for the reader's tokeniser)
  body_text       — HTML-stripped plaintext from the built article
                    (post-postbuild, so the table-card data-labels +
                    breadcrumb visible chrome are removed)
  tags            — frontmatter `tags:` list (raw author strings —
                    canonical resolution happens client-side via
                    `_data/taxonomy.yml`)
  pillars         — list of editorial pillars the post belongs to
                    (resolved here for caller convenience)
  lang            — IETF tag (always en at root; locale variants
                    follow in a future commit)
  license         — frontmatter override or "CC-BY-4.0" default
  published_at    — ISO 8601 from the slug date prefix
  updated_at      — frontmatter `last_reviewed:` or published_at

Outputs:
  /feed.jsonl                — all dated articles, newest first
  /tags/<slug>/feed.jsonl    — per-canonical-tag subset

Runs in build.sh after postbuild has finalised every article. Static
files served by GitHub Pages — zero Worker invocations.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore[assignment]

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
POSTS = ROOT / "_posts"
TAXONOMY = ROOT / "_data" / "taxonomy.yml"

_BASE_URL = "https://sebastienrousseau.com"
_DEFAULT_LICENSE = "CC-BY-4.0"

_DATED_SLUG_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-(.+)$")
_FRONTMATTER_RE = re.compile(r"^---\n([\s\S]*?)\n---\n", re.MULTILINE)
_TITLE_FM_RE = re.compile(r'^title:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)
_EXCERPT_FM_RE = re.compile(r'^excerpt:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)
_TAG_FM_RE = re.compile(r'^tags:\s*"?([^"\n]+)"?', re.MULTILINE)
_LICENSE_FM_RE = re.compile(r'^license:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)
_LASTREV_FM_RE = re.compile(r'^last_reviewed:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)
_MAIN_RE = re.compile(r'<main\b[^>]*>([\s\S]*?)</main>', re.IGNORECASE)
_TAG_STRIP_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")


def _alias_map(taxonomy: dict) -> dict[str, str]:
    out: dict[str, str] = {}
    for slug, entry in taxonomy.items():
        out[slug.strip().lower()] = slug
        for alias in entry.get("aliases", []) or []:
            out[alias.strip().lower()] = slug
    return out


def _load_taxonomy() -> tuple[dict, dict[str, str]]:
    if yaml is None or not TAXONOMY.is_file():
        return {}, {}
    taxonomy = yaml.safe_load(TAXONOMY.read_text(encoding="utf-8")) or {}
    return taxonomy, _alias_map(taxonomy)


def _strip_frontmatter(text: str) -> str:
    """Drop the YAML frontmatter block so body_markdown is post-frontmatter."""
    m = _FRONTMATTER_RE.match(text)
    return text[m.end() :] if m else text


def _html_to_plaintext(path: Path) -> str:
    """Read the built article HTML, extract <main>'s text, strip tags
    + collapse whitespace. Returns "" if the file is missing."""
    if not path.is_file():
        return ""
    src = path.read_text(encoding="utf-8", errors="ignore")
    m = _MAIN_RE.search(src)
    body = m.group(1) if m else src
    text = _TAG_STRIP_RE.sub(" ", body)
    return _WS_RE.sub(" ", text).strip()


def _parse_tags_line(
    tags_line: str | None,
    taxonomy: dict,
    amap: dict[str, str],
) -> tuple[list[str], list[str]]:
    """Return (raw tag strings, sorted unique pillar slugs) for one
    post's frontmatter ``tags:`` line."""
    if not tags_line:
        return [], []
    raw_tags: list[str] = []
    pillars: set[str] = set()
    for raw in tags_line.split(","):
        tag = raw.strip().strip('"').strip("'").strip()
        if not tag:
            continue
        raw_tags.append(tag)
        canon = amap.get(tag.lower())
        if not canon:
            continue
        cat = taxonomy.get(canon, {}).get("category")
        if cat:
            pillars.add(cat)
    return raw_tags, sorted(pillars)


def _post_record(
    path: Path,
    taxonomy: dict,
    amap: dict[str, str],
) -> dict | None:
    text = path.read_text(encoding="utf-8", errors="ignore")
    stem_m = _DATED_SLUG_RE.match(path.stem)
    if not stem_m:
        return None
    title_m = _TITLE_FM_RE.search(text)
    if not title_m:
        return None
    excerpt_m = _EXCERPT_FM_RE.search(text)
    license_m = _LICENSE_FM_RE.search(text)
    lastrev_m = _LASTREV_FM_RE.search(text)
    tags_m = _TAG_FM_RE.search(text)
    raw_tags, pillars = _parse_tags_line(
        tags_m.group(1) if tags_m else None, taxonomy, amap
    )
    slug = path.stem
    iso_date = stem_m.group(1)
    return {
        "url": f"{_BASE_URL}/{slug}/",
        "title": title_m.group(1),
        "summary": excerpt_m.group(1) if excerpt_m else "",
        "body_markdown": _strip_frontmatter(text),
        "body_text": _html_to_plaintext(PUBLIC / slug / "index.html"),
        "tags": raw_tags,
        "pillars": pillars,
        "lang": "en",
        "license": license_m.group(1) if license_m else _DEFAULT_LICENSE,
        "published_at": iso_date,
        "updated_at": lastrev_m.group(1) if lastrev_m else iso_date,
    }


def _write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False))
            f.write("\n")


def _write_global_and_per_tag(records: list[dict], amap: dict[str, str]) -> tuple[int, int]:
    """Write `/feed.jsonl` and `/tags/<slug>/feed.jsonl`. Returns
    (global-record-count, per-tag-file-count)."""
    records.sort(key=lambda r: r["published_at"], reverse=True)
    _write_jsonl(PUBLIC / "feed.jsonl", records)
    # Group by canonical tag (alias-resolved) → subset
    by_canonical: dict[str, list[dict]] = {}
    for rec in records:
        seen: set[str] = set()
        for raw in rec["tags"]:
            canon = amap.get(raw.lower())
            if canon and canon not in seen:
                seen.add(canon)
                by_canonical.setdefault(canon, []).append(rec)
    for canon, recs in by_canonical.items():
        _write_jsonl(PUBLIC / "tags" / canon / "feed.jsonl", recs)
    return len(records), len(by_canonical)


def main() -> int:
    taxonomy, amap = _load_taxonomy()
    records: list[dict] = []
    for path in sorted(POSTS.glob("*.md")):
        rec = _post_record(path, taxonomy, amap)
        if rec is not None:
            records.append(rec)
    n, t = _write_global_and_per_tag(records, amap)
    print(
        f"build_rag_corpus: wrote {n} records to public/feed.jsonl + "
        f"{t} per-tag JSONL files under public/tags/<slug>/feed.jsonl."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
