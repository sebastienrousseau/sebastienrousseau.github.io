#!/usr/bin/env python3
"""Post new blog articles to Medium as drafts via the Medium API.

Reads every BlogPosting page from the built `public/` tree, compares
against a state file, and drafts any article not yet sent.

Usage:
    # Normal run — only drafts articles not yet in state
    MEDIUM_TOKEN=<token> python3 scripts/rss_to_medium.py

    # Backfill — mark all existing articles as already-drafted WITHOUT
    # posting them (use once to avoid flooding Medium with old content)
    python3 scripts/rss_to_medium.py --backfill

    # Dry-run — show what would be posted, but do nothing
    DRY_RUN=1 python3 scripts/rss_to_medium.py

Required env var:
    MEDIUM_TOKEN   — Medium Integration Token (Settings → Integration Tokens)

Optional env vars:
    MEDIUM_STATE   — path to state JSON (default: .github/medium-state.json)
    PUBLIC_DIR     — path to built site (default: public)
    DRY_RUN        — set to "1" to log without posting
"""
from __future__ import annotations

import html as html_lib
import json
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
TOKEN = os.environ.get("MEDIUM_TOKEN", "")
STATE_PATH = Path(os.environ.get("MEDIUM_STATE", ".github/medium-state.json"))
PUBLIC_DIR = Path(os.environ.get("PUBLIC_DIR", "public"))
DRY_RUN = os.environ.get("DRY_RUN", "") == "1"

MEDIUM_API = "https://api.medium.com/v1"
BLOGPOSTING_MARKER = '"@type":"BlogPosting"'

# Regex patterns for extracting fields from built HTML
_JSONLD_RE = re.compile(
    r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>',
    re.DOTALL | re.IGNORECASE,
)
_CANONICAL_RE = re.compile(r'<link\s+rel="canonical"\s+href="([^"]+)"', re.IGNORECASE)
_LEAD_ASIDE_RE = re.compile(
    r'<!-- lead-start -->(.*?)<!-- lead-end -->', re.DOTALL | re.IGNORECASE
)
_TAKEAWAYS_RE = re.compile(
    r'<ul\s+class="post-lead-takeaways">(.*?)</ul>', re.DOTALL | re.IGNORECASE
)
_LI_RE = re.compile(r'<li>(.*?)</li>', re.DOTALL | re.IGNORECASE)
_TAGS_RE = re.compile(r'<[^>]+>')


def _api(method: str, path: str, body: dict | None = None) -> dict:
    url = f"{MEDIUM_API}{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        body_text = exc.read().decode(errors="replace")
        raise RuntimeError(f"Medium API {exc.code}: {body_text}") from exc


def _strip(text: str) -> str:
    return html_lib.unescape(_TAGS_RE.sub("", text)).strip()


def _load_state() -> dict:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return {"drafted": []}


def _save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n")


_LOCALE_DIRS = {
    "ar","bn","cs","de","es","fil","fr","ha","he","hi","id","it","ja",
    "ko","nl","pl","pt-br","ro","ru","sv","th","tr","uk","vi","yo",
    "zh-hans","zh-hant",
}


def _find_articles() -> list[Path]:
    """Return English BlogPosting index.html files from public/.

    Skips locale sub-trees (ar/, fr/, zh-hans/, …) so Medium only
    receives the canonical English version of each article.
    """
    results = []
    for p in sorted(PUBLIC_DIR.rglob("index.html")):
        # Skip locale sub-directories
        parts = p.relative_to(PUBLIC_DIR).parts
        if parts and parts[0] in _LOCALE_DIRS:
            continue
        content = p.read_text(encoding="utf-8", errors="replace")
        if BLOGPOSTING_MARKER in content:
            results.append(p)
    return results


def _parse_article(path: Path) -> dict | None:
    """Extract title, description, canonical URL, tags, and lead HTML."""
    content = path.read_text(encoding="utf-8", errors="replace")

    # canonical URL
    cm = _CANONICAL_RE.search(content)
    if not cm:
        return None
    url = cm.group(1).rstrip("/")

    # JSON-LD BlogPosting block — may be top-level or inside @graph
    blogposting: dict = {}
    for m in _JSONLD_RE.finditer(content):
        try:
            block = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        if isinstance(block, dict):
            if block.get("@type") == "BlogPosting":
                blogposting = block
                break
            # @graph wrapper
            for node in block.get("@graph", []):
                if isinstance(node, dict) and node.get("@type") == "BlogPosting":
                    blogposting = node
                    break
        if blogposting:
            break
    if not blogposting:
        return None

    title = blogposting.get("name") or blogposting.get("headline") or ""
    description = blogposting.get("description") or ""
    keywords_raw = blogposting.get("keywords") or ""
    tags = [k.strip() for k in keywords_raw.split(",") if k.strip()][:5]
    banner = blogposting.get("image") or ""
    if isinstance(banner, dict):
        banner = banner.get("url", "")
    banner_alt = ""
    date_published = blogposting.get("datePublished") or ""

    # Lead aside block
    lead_html = ""
    lm = _LEAD_ASIDE_RE.search(content)
    if lm:
        lead_html = lm.group(1).strip()

    # Extract bullet takeaways
    takeaways: list[str] = []
    tm = _TAKEAWAYS_RE.search(lead_html or content)
    if tm:
        for li in _LI_RE.finditer(tm.group(1)):
            text = _strip(li.group(1))
            if text:
                takeaways.append(text)

    return {
        "url": url,
        "title": title,
        "description": description,
        "tags": tags,
        "banner": banner,
        "banner_alt": banner_alt,
        "date_published": date_published,
        "takeaways": takeaways,
    }


def _build_medium_html(article: dict) -> str:
    """Build a Medium-friendly HTML draft body."""
    url = article["url"]
    title = article["title"]
    desc = article["description"]
    takeaways = article["takeaways"]
    banner = article["banner"]

    parts = []

    if banner:
        parts.append(f'<figure><img src="{html_lib.escape(banner)}" alt=""></figure>')

    parts.append(f"<p>{html_lib.escape(desc)}</p>")

    if takeaways:
        parts.append("<h3>Key takeaways</h3><ul>")
        for t in takeaways:
            parts.append(f"<li>{html_lib.escape(t)}</li>")
        parts.append("</ul>")

    parts.append(
        f'<p><strong>Read the full article:</strong> '
        f'<a href="{html_lib.escape(url)}">{html_lib.escape(title)}</a></p>'
    )
    parts.append(
        f'<hr><p><em>Originally published at '
        f'<a href="{html_lib.escape(url)}">{html_lib.escape(url)}</a>. '
        f'Licensed under CC-BY-4.0.</em></p>'
    )

    return "\n".join(parts)


def _backfill() -> int:
    """Mark every current article as already-drafted without posting.
    Run once after setting up the workflow to avoid flooding Medium with
    years of back-catalogue."""
    articles = _find_articles()
    state = _load_state()
    already: set[str] = set(state.get("drafted", []))
    new_urls = []
    for path in articles:
        article = _parse_article(path)
        if article and article["url"] not in already:
            new_urls.append(article["url"])
    state["drafted"] = sorted(already | set(new_urls))
    _save_state(state)
    print(f"Backfill complete — {len(new_urls)} URL(s) marked, {len(state['drafted'])} total in state.")
    return 0


def main() -> int:
    if "--backfill" in sys.argv:
        return _backfill()

    if not TOKEN and not DRY_RUN:
        print("ERROR: MEDIUM_TOKEN not set", file=sys.stderr)
        return 1

    state = _load_state()
    already_drafted: set[str] = set(state.get("drafted", []))

    # Get Medium user ID
    if DRY_RUN:
        user_id = "dry-run-user"
    else:
        try:
            me = _api("GET", "/me")
            user_id = me["data"]["id"]
            print(f"Authenticated as: {me['data'].get('username', user_id)}")
        except RuntimeError as exc:
            print(f"ERROR: could not authenticate with Medium: {exc}", file=sys.stderr)
            return 1

    articles = _find_articles()
    drafted_this_run: list[str] = []

    for path in articles:
        article = _parse_article(path)
        if article is None:
            continue

        url = article["url"]
        if url in already_drafted:
            continue

        title = article["title"]
        print(f"Drafting: {title}")
        print(f"  URL: {url}")

        medium_html = _build_medium_html(article)

        payload = {
            "title": title,
            "contentFormat": "html",
            "content": medium_html,
            "canonicalUrl": url,
            "publishStatus": "draft",
            "tags": article["tags"],
        }

        if DRY_RUN:
            print("  [DRY RUN] would POST to Medium")
        else:
            try:
                result = _api("POST", f"/users/{user_id}/posts", payload)
                post_url = result.get("data", {}).get("url", "")
                print(f"  Draft created: {post_url}")
            except RuntimeError as exc:
                print(f"  ERROR: {exc}", file=sys.stderr)
                continue

        drafted_this_run.append(url)

    if drafted_this_run:
        state["drafted"] = sorted(already_drafted | set(drafted_this_run))
        _save_state(state)
        print(f"\nDrafted {len(drafted_this_run)} article(s). State saved to {STATE_PATH}")
    else:
        print("No new articles to draft.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
