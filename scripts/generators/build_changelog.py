#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Changelog + "what's new" + status generator — Phase 5 (freshness signals).

Runs after ``ssg`` (and after ``build_translations`` so the homepage
strip only lands on the *English* ``public/index.html`` — locale
homepages are forked earlier and must not carry untranslated English
entries) and before ``postbuild.py`` (so the emitted pages are picked
up by the sitemap-augment pass and their inline JSON-LD is hashed into
the per-page CSP by the postbuild contract).

Deliverables
------------
  - ``public/changelog/index.html`` — every dated post as a changelog
    entry, grouped by month, newest first, each linking to its article.
  - A "What's new" strip injected into ``public/index.html`` listing
    the latest N entries + a link to the changelog.
  - ``public/status/index.html`` — a lightweight build/deploy + uptime
    status page (no backend).
  - ``public/status.json`` — machine-readable status for badges/agents.
  - ``public/status/badge.svg`` — a self-hosted, same-origin build badge.

Determinism
-----------
The output is derived **only** from committed dated-post front matter
(the ISO date lives in the slug) and is sorted by ``(date, slug)``
descending with a stable key. No wall-clock time is embedded anywhere,
so two builds of the same commit are byte-identical. PR back-links are
an *optional* enrichment read from full git history; on a shallow CI
clone the enrichment is skipped, which keeps every CI build identical.

Template skeleton is the ssg-emitted ``public/articles/index.html``
shell (same approach as ``build_listings.py`` / ``build_topics.py``),
so the changelog and status pages inherit the site chrome, head meta,
CSP, and CSS with zero layout drift.
"""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

_LIB = Path(__file__).resolve().parents[1] / "lib"
sys.path.insert(0, str(_LIB))

from _core import DATED_SLUG_RE, display_date, read_frontmatter
from _lang_registry import load_strings

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
POSTS = ROOT / "_posts"
SHELL_SRC = PUBLIC / "articles" / "index.html"

BASE = "https://sebastienrousseau.com"
SSG_PIN = "0.0.44"  # ADR-0002 — the CI-pinned generator version.
WHATS_NEW_LIMIT = 5  # entries surfaced in the homepage strip.

_MONTHS = (
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)

# --- Shell-surgery regexes (mirrors build_listings.py) ----------------------
_MAIN_RE = re.compile(r"(<main\b[^>]*>)([\s\S]*?)(</main>)", re.IGNORECASE)
_AP_HERO_BLOCK_RE = re.compile(r'<section class="ap-hero">[\s\S]*?</section>', re.IGNORECASE)
_TITLE_RE = re.compile(r"<title>[^<]*</title>", re.IGNORECASE)
_DESC_RE = re.compile(r'<meta name="description" content="[^"]*"', re.IGNORECASE)
_CANONICAL_RE = re.compile(r'<link rel="canonical" href="[^"]*"', re.IGNORECASE)
_OG_TITLE_RE = re.compile(r'<meta property="og:title" content="[^"]*"', re.IGNORECASE)
_OG_DESC_RE = re.compile(r'<meta property="og:description" content="[^"]*"', re.IGNORECASE)
_OG_URL_RE = re.compile(r'<meta property="og:url" content="[^"]*"', re.IGNORECASE)
_LDJSON_BLOCKS_RE = re.compile(
    r'<script type="application/ld\+json">[\s\S]*?</script>', re.IGNORECASE
)
# Homepage injection anchor — the layout wraps markdown output in
# `<div class="home-content">`. Tolerant of ssg minifying the quotes away.
_HOME_ANCHOR_RE = re.compile(r'(<div\s+class=["\']?home-content["\']?\s*>)', re.IGNORECASE)


class Entry(NamedTuple):
    """One changelog row derived from a dated post's front matter."""

    iso: str  # YYYY-MM-DD (canonical, from the slug)
    slug: str  # full dated slug (URL is /<slug>/)
    title: str
    description: str


# ---------------------------------------------------------------------------
# Collection (pure, deterministic — the unit-tested core)
# ---------------------------------------------------------------------------
def collect_entries(posts_dir: Path = POSTS) -> list[Entry]:
    """Every dated ``_posts/`` article as an :class:`Entry`, newest first.

    Deterministic: the date is the slug's ISO prefix (committed), and the
    sort key is ``(iso, slug)`` descending — stable across environments
    regardless of filesystem iteration order.
    """
    entries: list[Entry] = []
    if not posts_dir.is_dir():
        return entries
    for path in posts_dir.glob("*.md"):
        m = DATED_SLUG_RE.match(path.stem)
        if not m:
            continue
        fm = read_frontmatter(path)
        title = (fm.get("title") or path.stem).strip()
        description = (fm.get("description") or fm.get("excerpt") or "").strip()
        entries.append(Entry(m.group(1), path.stem, title, description))
    entries.sort(key=lambda e: (e.iso, e.slug), reverse=True)
    return entries


def _month_key(iso: str) -> str:
    return iso[:7]  # YYYY-MM


def _month_label(iso: str) -> str:
    """``2026-07-03`` → ``July 2026``. Passes bad input straight through."""
    try:
        _, mm = iso[:7].split("-")
        return f"{_MONTHS[int(mm) - 1]} {iso[:4]}"
    except (ValueError, IndexError):
        return iso[:7]


def group_by_month(entries: list[Entry]) -> list[tuple[str, list[Entry]]]:
    """Group already-sorted entries into ``[(month-label, [Entry, …]), …]``
    preserving the newest-first ordering of both months and entries."""
    grouped: dict[str, list[Entry]] = {}
    order: list[str] = []
    for e in entries:
        key = _month_key(e.iso)
        if key not in grouped:
            grouped[key] = []
            order.append(key)
    for e in entries:
        grouped[_month_key(e.iso)].append(e)
    return [(_month_label(f"{k}-01"), grouped[k]) for k in order]


# ---------------------------------------------------------------------------
# Optional PR back-links (full-history only; skipped on shallow CI clones)
# ---------------------------------------------------------------------------
def pr_links(posts_dir: Path = POSTS) -> dict[str, int]:
    """Map ``slug -> PR number`` from git history, best-effort.

    Only runs when the working copy has full history — a shallow clone
    (the CI default) returns an empty map, keeping CI output byte-stable.
    Any git failure is swallowed: the changelog degrades to article-only
    links, never breaks the build.
    """
    try:
        shallow = subprocess.run(
            ["git", "rev-parse", "--is-shallow-repository"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        if shallow != "false":
            return {}
        out = subprocess.run(
            [
                "git",
                "log",
                "--diff-filter=A",
                "--name-only",
                "--format=%x1f%s",
                "--",
                "_posts/*.md",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except (subprocess.SubprocessError, OSError):
        return {}

    links: dict[str, int] = {}
    subject = ""
    pr_re = re.compile(r"\(#(\d+)\)")
    file_re = re.compile(r"^_posts/(\d{4}-\d{2}-\d{2}-[^/]+)\.md$")
    for line in out.splitlines():
        if line.startswith("\x1f"):
            subject = line[1:]
            continue
        fm = file_re.match(line.strip())
        if not fm:
            continue
        slug = fm.group(1)
        pr = pr_re.search(subject)
        # `git log` walks newest→oldest; keep the first (newest) PR seen.
        if pr and slug not in links:
            links[slug] = int(pr.group(1))
    return links


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------
def _esc(s: str) -> str:
    return html.escape(s, quote=True)


def render_changelog_body(
    entries: list[Entry],
    title: str,
    lede: str,
    prs: dict[str, int] | None = None,
) -> str:
    """The changelog page's ``<main>`` inner HTML — one section per month
    (``<h2>``), each a semantic list of entries. Reuses existing listing
    CSS classes so no new styles are required."""
    prs = prs or {}
    months = group_by_month(entries)
    sections: list[str] = []
    for label, month_entries in months:
        items: list[str] = []
        for e in month_entries:
            url = f"/{e.slug}/"
            desc = (
                f' <span class="changelog-note">{_esc(e.description)}</span>'
                if e.description
                else ""
            )
            pr = ""
            if e.slug in prs:
                n = prs[e.slug]
                pr = (
                    f' <a class="changelog-pr" '
                    f'href="https://github.com/sebastienrousseau/sebastienrousseau.github.io/pull/{n}" '
                    f'rel="noopener">#{n}</a>'
                )
            items.append(
                '<li class="changelog-entry">'
                f'<time datetime="{e.iso}" class="changelog-date">{_esc(display_date(e.iso))}</time> '
                f'<a class="changelog-link" href="{url}">{_esc(e.title)}</a>'
                f"{desc}{pr}"
                "</li>"
            )
        sections.append(
            f'<section class="changelog-month" aria-label="{_esc(label)}">'
            f"<h2>{_esc(label)}</h2>"
            f'<ul class="changelog-list">{"".join(items)}</ul>'
            "</section>"
        )
    return (
        '<div class="wrap report-wrap">'
        '<header class="tag-landing-hero">'
        '<p class="eyebrow">CHANGELOG</p>'
        f"<h1>{_esc(title)}</h1>"
        f'<p class="tag-landing-meta">{_esc(lede)} · '
        f'<span id="changelog-count">{len(entries)}</span> entries</p>'
        "</header>" + "".join(sections) + "</div>"
    )


def render_whats_new_section(entries: list[Entry], strings: dict[str, str]) -> str:
    """The homepage "what's new" strip — the latest N entries + a CTA.
    Reuses the homepage's ``.feat`` section chrome for visual parity."""
    label = strings.get("whatsNew.title") or "What's new"
    cta = strings.get("whatsNew.cta") or "View the changelog"
    shown = entries[:WHATS_NEW_LIMIT]
    items = "".join(
        '<li class="whats-new-item">'
        f'<a href="/{e.slug}/">'
        f'<time datetime="{e.iso}">{_esc(display_date(e.iso))}</time> '
        f"<span>{_esc(e.title)}</span></a></li>"
        for e in shown
    )
    # ItemList schema.org so search + LLM crawlers read the strip as a
    # machine-readable list of recent articles (each links to a page that
    # carries full Article JSON-LD). Inline JSON-LD is CSP-hashed downstream.
    ld = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": label,
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": f"{BASE}/{e.slug}/", "name": e.title}
            for i, e in enumerate(shown)
        ],
    }
    jsonld = (
        '<script type="application/ld+json">'
        + json.dumps(ld, separators=(",", ":"), ensure_ascii=False)
        + "</script>"
    )
    return (
        '<section class="feat reveal whats-new" aria-labelledby="whats-new-h">'
        + jsonld
        + '<div class="wrap">'
        f'<h2 id="whats-new-h" class="feat-headline center">{_esc(label)}</h2>'
        f'<ul class="whats-new-list">{items}</ul>'
        '<div class="feat-cta-row">'
        f'<a class="pill ghost" href="/changelog/">{_esc(cta)}</a>'
        "</div>"
        "</div>"
        "</section>"
    )


def inject_whats_new(home_html: str, section: str) -> tuple[str, bool]:
    """Insert the strip as the first child of ``home-content``. Returns
    ``(html, injected?)`` — fail-soft so a template change never breaks
    the build."""
    if "whats-new" in home_html and 'aria-labelledby="whats-new-h"' in home_html:
        return home_html, False  # idempotent — already injected
    new, n = _HOME_ANCHOR_RE.subn(lambda m: m.group(1) + section, home_html, count=1)
    return (new, True) if n else (home_html, False)


def _changelog_jsonld(entries: list[Entry], title: str, lede: str) -> str:
    items = [
        {
            "@type": "ListItem",
            "position": i + 1,
            "url": f"{BASE}/{e.slug}/",
            "name": e.title,
        }
        for i, e in enumerate(entries)
    ]
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "@id": f"{BASE}/changelog/",
                "url": f"{BASE}/changelog/",
                "name": title,
                "description": lede,
                "isPartOf": {"@id": f"{BASE}/#website"},
                "inLanguage": "en-GB",
                "mainEntity": {
                    "@type": "ItemList",
                    "numberOfItems": len(items),
                    "itemListElement": items,
                },
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": title,
                        "item": f"{BASE}/changelog/",
                    },
                ],
            },
        ],
    }
    return (
        '<script type="application/ld+json">'
        + json.dumps(graph, separators=(",", ":"), ensure_ascii=False)
        + "</script>"
    )


def _strip_itemlist_jsonld(shell: str) -> str:
    for block in _LDJSON_BLOCKS_RE.findall(shell):
        if '"ItemList"' in block or '"itemListElement"' in block:
            shell = shell.replace(block, "", 1)
    return shell


def _swap_head(out: str, title: str, desc: str, canonical: str) -> str:
    out = _TITLE_RE.sub(f"<title>{_esc(title)}</title>", out, count=1)
    out = _DESC_RE.sub(f'<meta name="description" content="{_esc(desc)}"', out, count=1)
    out = _CANONICAL_RE.sub(f'<link rel="canonical" href="{canonical}"', out, count=1)
    out = _OG_TITLE_RE.sub(f'<meta property="og:title" content="{_esc(title)}"', out, count=1)
    out = _OG_DESC_RE.sub(f'<meta property="og:description" content="{_esc(desc)}"', out, count=1)
    out = _OG_URL_RE.sub(f'<meta property="og:url" content="{canonical}"', out, count=1)
    return out


def render_page(
    shell: str, body: str, title: str, desc: str, canonical: str, jsonld: str = ""
) -> str:
    """Fork the articles shell into a standalone page: swap head meta,
    drop the ap-hero, replace ``<main>`` body, and inject scoped JSON-LD."""
    out = _strip_itemlist_jsonld(shell)
    out = _swap_head(out, title, desc, canonical)
    out = _AP_HERO_BLOCK_RE.sub("", out, count=1)
    out = _MAIN_RE.sub(lambda m: m.group(1) + body + m.group(3), out, count=1)
    if jsonld:
        out = re.sub(r"(</body>)", jsonld + r"\1", out, count=1)
    return out


# ---------------------------------------------------------------------------
# Status surfaces (deterministic — no wall-clock)
# ---------------------------------------------------------------------------
def render_status_json(entries: list[Entry]) -> str:
    """Machine-readable status. Intentionally carries no timestamp so the
    artifact is byte-reproducible; freshness is conveyed by ``latest``."""
    latest = entries[0] if entries else None
    payload = {
        "schemaVersion": 1,
        "site": "sebastienrousseau.com",
        "status": "operational",
        "build": {"pipeline": "github-actions", "ssg": SSG_PIN},
        "content": {
            "articles": len(entries),
            "latest": (
                {"date": latest.iso, "slug": latest.slug, "title": latest.title} if latest else None
            ),
        },
        "links": {"changelog": f"{BASE}/changelog/", "status": f"{BASE}/status/"},
    }
    return json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def render_status_badge() -> str:
    """A self-hosted, same-origin (img-src 'self') shields-style badge.
    Static text → deterministic."""
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="118" height="20" '
        'role="img" aria-label="build: passing">'
        "<title>build: passing</title>"
        '<linearGradient id="s" x2="0" y2="100%">'
        '<stop offset="0" stop-color="#bbb" stop-opacity=".1"/>'
        '<stop offset="1" stop-opacity=".1"/></linearGradient>'
        '<clipPath id="r"><rect width="118" height="20" rx="3" fill="#fff"/></clipPath>'
        '<g clip-path="url(#r)">'
        '<rect width="37" height="20" fill="#555"/>'
        '<rect x="37" width="81" height="20" fill="#2f7d31"/>'
        '<rect width="118" height="20" fill="url(#s)"/></g>'
        '<g fill="#fff" text-anchor="middle" '
        'font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="11">'
        '<text x="19" y="14">build</text>'
        '<text x="76" y="14">passing</text></g></svg>'
    )


def render_status_body(entries: list[Entry], strings: dict[str, str]) -> str:
    title = strings.get("status.title") or "Status"
    latest = entries[0] if entries else None
    latest_html = ""
    if latest:
        latest_html = (
            "<p>Most recent publication: "
            f'<a href="/{latest.slug}/">{_esc(latest.title)}</a> '
            f'(<time datetime="{latest.iso}">{_esc(display_date(latest.iso))}</time>).</p>'
        )
    repo = "https://github.com/sebastienrousseau/sebastienrousseau.github.io"
    return (
        '<div class="wrap report-wrap">'
        '<header class="tag-landing-hero">'
        '<p class="eyebrow">STATUS</p>'
        f"<h1>{_esc(title)}</h1>"
        '<p class="tag-landing-meta">'
        f'<img src="/status/badge.svg" width="118" height="20" '
        f'alt="Build status: passing" decoding="async"> All systems operational.</p>'
        "</header>"
        '<section aria-label="Build and deploy">'
        "<h2>Build &amp; deploy</h2>"
        "<p>Every deploy is gated in CI: reproducible build, hash-strict CSP + SRI, "
        "pa11y + axe accessibility, a Lighthouse performance budget, and 28-locale "
        "i18n parity. A red gate blocks the deploy.</p>"
        f'<p><a href="{repo}/actions" rel="noopener">Continuous-integration runs</a> · '
        '<a href="/status.json">status.json</a></p>'
        "</section>"
        '<section aria-label="Content freshness">'
        "<h2>Content</h2>"
        f"<p>{len(entries)} dated articles published. "
        f'See the <a href="/changelog/">changelog</a> for the full history.</p>'
        f"{latest_html}"
        "</section>"
        '<section aria-label="Uptime">'
        "<h2>Uptime</h2>"
        "<p>The site is a static artifact served from a global CDN with no origin "
        "server to fall over. Availability is monitored externally; incidents, if "
        f'any, are posted to the <a href="{repo}/issues" rel="noopener">issue tracker</a>.</p>'
        "</section>"
        "</div>"
    )


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------
def main() -> int:
    if not SHELL_SRC.is_file():
        raise SystemExit(f"shell template missing: {SHELL_SRC} — run ssg + build_listings first")
    shell = SHELL_SRC.read_text(encoding="utf-8")
    strings = load_strings("en")

    entries = collect_entries()
    prs = pr_links()

    cl_title = strings.get("changelog.title") or "Changelog"
    cl_lede = strings.get("changelog.lede") or "Recent publications, grouped by month."

    # 1. /changelog/
    body = render_changelog_body(entries, cl_title, cl_lede, prs)
    jsonld = _changelog_jsonld(entries, cl_title, cl_lede)
    page = render_page(
        shell,
        body,
        title=f"{cl_title} — Sebastien Rousseau",
        desc=cl_lede,
        canonical=f"{BASE}/changelog/",
        jsonld=jsonld,
    )
    (PUBLIC / "changelog").mkdir(parents=True, exist_ok=True)
    (PUBLIC / "changelog" / "index.html").write_text(page, encoding="utf-8")

    # 2. Homepage "what's new" strip (EN homepage only).
    home_path = PUBLIC / "index.html"
    injected = False
    if home_path.is_file():
        home = home_path.read_text(encoding="utf-8")
        section = render_whats_new_section(entries, strings)
        home, injected = inject_whats_new(home, section)
        if injected:
            home_path.write_text(home, encoding="utf-8")
        else:
            print(
                "build_changelog: warning — homepage anchor not found; strip skipped",
                file=sys.stderr,
            )

    # 3. /status/ + status.json + badge.
    st_title = strings.get("status.title") or "Status"
    st_body = render_status_body(entries, strings)
    st_page = render_page(
        shell,
        st_body,
        title=f"{st_title} — Sebastien Rousseau",
        desc="Build, deploy and uptime status for sebastienrousseau.com.",
        canonical=f"{BASE}/status/",
    )
    (PUBLIC / "status").mkdir(parents=True, exist_ok=True)
    (PUBLIC / "status" / "index.html").write_text(st_page, encoding="utf-8")
    (PUBLIC / "status" / "badge.svg").write_text(render_status_badge(), encoding="utf-8")
    (PUBLIC / "status.json").write_text(render_status_json(entries), encoding="utf-8")

    print(
        f"build_changelog: {len(entries)} entries, "
        f"{len(group_by_month(entries))} months, {len(prs)} PR link(s); "
        f"what's-new strip {'injected' if injected else 'skipped'}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
