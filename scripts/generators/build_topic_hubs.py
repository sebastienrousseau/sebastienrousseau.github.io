#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Generate the topic hubs from ``_data/hubs.yml`` (plan G-1).

One front door per topic: ``/iso-20022/``, ``/post-quantum-cryptography/``
and ``/applied-ai/``. Each hub has the same blocks, in order: the H1 and a
quotable answer paragraph; "At a glance" facts, each with its official
source and verification date; three reading paths (boards, engineers, risk
and regulators); a dated roadmap where the topic has one; the free tools;
the latest six articles in the hub's tags and the full list after them;
the FAQ (with FAQPage JSON-LD built from it); and the expert block.

JSON-LD: CollectionPage (``about`` a DefinedTerm, ``hasPart`` the
articles), FAQPage and BreadcrumbList. ``check`` is the gate the plan asks
for: at least 20 linked articles, every fact and milestone sourced and
verified within 120 days (90 is a warning). English only, same shell and
slot as ``build_trust.py``.
"""

from __future__ import annotations

import datetime as dt
import html
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parent / "lib"))
import _expert_block
import _profile
from build_case_studies import _swap_into_shell
from build_speaking import _metrics

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
DATA = ROOT / "_data" / "hubs.yml"
SHELL_SRC = PUBLIC / "articles" / "index.html"
BASE = "https://sebastienrousseau.com"
MIN_ARTICLES = 20
MAX_AGE, WARN_AGE = 120, 90
_DATED_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-")
_ALT_RE = re.compile(r'[ \t]*<link\s+rel="alternate"\s+hreflang="[^"]*"\s+href="[^"]*"\s*/?>\n?')
TOOL_LINKS = {
    "iso-20022": [("Structured-address checker", "/tools/#tool-address-h"), ("ISO 20022 message identifier", "/tools/#tool-message-h")],
    "post-quantum-cryptography": [("PQC sizing calculator", "/tools/#tool-pqc-h")],
    "applied-ai": [("ISO 20022 MCP suite", "/iso20022-mcp/index.html")],
}  # fmt: skip


def _e(text: object) -> str:
    return html.escape(" ".join(str(text).split()), quote=False)


def tag_slugs(taxonomy: dict[str, Any]) -> dict[str, str]:
    """Lower-case tag name or alias -> taxonomy slug."""
    out: dict[str, str] = {}
    for slug, entry in taxonomy.items():
        if isinstance(entry, dict):
            for name in [slug, entry.get("name", ""), *entry.get("aliases", [])]:
                out[str(name).strip().lower()] = slug
    return out


def articles(posts: Path, index: dict[str, str]) -> list[dict[str, Any]]:
    """Every dated English article, newest first: slug, title, tag slugs."""
    out = []
    for path in sorted(posts.glob("*.md"), reverse=True):
        if not _DATED_RE.match(path.name):
            continue
        fm = yaml.safe_load(path.read_text(encoding="utf-8").split("---", 2)[1]) or {}
        tags = fm.get("tags", "")
        names = tags.split(",") if isinstance(tags, str) else tags
        out.append(
            {
                "slug": path.stem,
                "title": str(fm.get("title", path.stem)),
                "tags": {index.get(str(n).strip().lower()) for n in names} - {None},
            }
        )
    return out


def hub_articles(hub: dict[str, Any], all_articles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    wanted = set(hub.get("tags", []))
    return [a for a in all_articles if a["tags"] & wanted]


def _link(slug: str, title: str) -> str:
    return f'<a href="/{slug}/index.html">{_e(title)}</a>'


def _section(sid: str, eyebrow: str, heading: str, inner: str, alt: bool = False) -> str:
    cls = "narrative-section alt" if alt else "narrative-section"
    return (
        f'<section class="{cls}" aria-labelledby="{sid}"><div class="narrative-wrap"><div>'
        f'<p class="narrative-eyebrow">{_e(eyebrow)}</p><h2 id="{sid}" class="narrative-head">{_e(heading)}</h2>'
        f"{inner}</div></div></section>"
    )


def _facts(items: list[dict[str, str]]) -> str:
    rows = "".join(
        f'<li>{_e(f["text"])} <a href="{_e(f["source"])}" rel="external noopener">Source</a> '
        f'<span class="fact-verified">(checked {_e(f["last_verified"])})</span></li>'
        for f in items
    )
    return f'<ul class="hub-facts">{rows}</ul>'


def _paths(paths: list[dict[str, Any]], titles: dict[str, str]) -> str:
    cards = "".join(
        f'<li class="story-card"><h3 class="story-card-title">{_e(p["audience"])}</h3><ol>'
        + "".join(f"<li>{_link(s, titles.get(s, s))}</li>" for s in p["slugs"])
        + "</ol></li>"
        for p in paths
    )
    return f'<ul class="story-grid" role="list">{cards}</ul>'


def _roadmap(items: list[dict[str, str]]) -> str:
    rows = "".join(
        f'<li><time datetime="{_e(m["date"])}">{_e(m["date"])}</time> {_e(m["text"])} '
        f'<a href="{_e(m["source"])}" rel="external noopener">Source</a></li>'
        for m in items
    )
    return f'<ol class="hub-roadmap">{rows}</ol>'


def _faq(faq: list[dict[str, str]]) -> str:
    return (
        '<div class="qa-list">'
        + "".join(
            f'<details class="qa-item"><summary class="qa-q">{_e(i["q"])}</summary>'
            f'<div class="qa-a"><p>{_e(i["a"])}</p></div></details>'
            for i in faq
        )
        + "</div>"
    )


def render_hub(key: str, hub: dict[str, Any], arts: list[dict[str, Any]], expert: str) -> str:
    titles = {a["slug"]: a["title"] for a in arts}
    latest = "".join(f"<li>{_link(a['slug'], a['title'])}</li>" for a in arts[:6])
    rest = "".join(f"<li>{_link(a['slug'], a['title'])}</li>" for a in arts[6:])
    tools = "".join(
        f'<li><a href="{href}">{_e(name)}</a></li>' for name, href in TOOL_LINKS.get(key, [])
    )
    parts = [
        '<section class="story-cta" aria-labelledby="hub-h1"><header class="story-head">'
        f'<p class="story-eyebrow">Topic hub</p><h1 id="hub-h1" class="story-title">{_e(hub["h1"])}</h1>'
        f'<p class="hub-answer">{_e(hub["answer"])}</p></header></section>',
        _section("hub-glance", "At a glance", "The facts that matter", _facts(hub["at_a_glance"])),
        _section(
            "hub-paths", "Start here", "Three ways in", _paths(hub["paths"], titles), alt=True
        ),
    ]
    if hub.get("roadmap"):
        parts.append(
            _section("hub-roadmap", "Roadmap", "Dates to plan around", _roadmap(hub["roadmap"]))
        )
    if tools:
        parts.append(_section("hub-tools", "Tools", "Free tools", f"<ul>{tools}</ul>"))
    parts.append(
        _section(
            "hub-latest", "Latest thinking", "Latest articles",
            f"<ul>{latest}</ul>" + (f"<details><summary>All {len(arts)} articles</summary><ul>{rest}</ul></details>" if rest else ""),
            alt=True,
        )
    )  # fmt: skip
    parts.append(_section("hub-faq", "FAQ", "Questions and answers", _faq(hub["faq"])))
    parts.append(expert)
    return '<div class="hub-page">' + "".join(parts) + jsonld(key, hub, arts) + "</div>"


def jsonld(key: str, hub: dict[str, Any], arts: list[dict[str, Any]]) -> str:
    url = BASE + hub["path"]
    graph = [
        {
            "@type": "CollectionPage",
            "@id": f"{url}#page",
            "name": hub["h1"],
            "url": url,
            "about": {"@type": "DefinedTerm", "name": hub["h1"], "termCode": key},
            "hasPart": [
                {"@type": "Article", "headline": a["title"], "url": f"{BASE}/{a['slug']}/"}
                for a in arts
            ],
            "author": {"@id": f"{BASE}/#person"},
        },
        {
            "@type": "FAQPage",
            "@id": f"{url}#faq",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": i["q"],
                    "acceptedAnswer": {"@type": "Answer", "text": " ".join(i["a"].split())},
                }
                for i in hub["faq"]
            ],
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                {"@type": "ListItem", "position": 2, "name": hub["h1"], "item": url},
            ],
        },
    ]
    payload = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    return f'<script type="application/ld+json">{payload}</script>'


def check(
    key: str, hub: dict[str, Any], arts: list[dict[str, Any]], today: dt.date
) -> tuple[list[str], list[str]]:
    """(errors, warnings) for one hub."""
    errors, warnings = [], []
    if len(arts) < MIN_ARTICLES:
        errors.append(f"{key}: {len(arts)} linked articles (need {MIN_ARTICLES})")
    for item in [*hub.get("at_a_glance", []), *hub.get("roadmap", [])]:
        if not item.get("source") or not item.get("last_verified"):
            errors.append(
                f"{key}: fact without source or last_verified: {item.get('text', '')[:60]}"
            )
            continue
        age = (today - dt.date.fromisoformat(str(item["last_verified"]))).days
        if age > MAX_AGE:
            errors.append(f"{key}: fact last verified {age} days ago: {item['text'][:60]}")
        elif age > WARN_AGE:
            warnings.append(
                f"{key}: fact due for re-verification ({age} days): {item['text'][:60]}"
            )
    return errors, warnings


def main() -> int:
    if not (SHELL_SRC.is_file() and DATA.is_file()):
        print("build_topic_hubs: shell or _data/hubs.yml missing", file=sys.stderr)
        return 1
    hubs = yaml.safe_load(DATA.read_text(encoding="utf-8"))
    taxonomy = yaml.safe_load((ROOT / "_data" / "taxonomy.yml").read_text(encoding="utf-8"))
    all_arts = articles(ROOT / "_posts", tag_slugs(taxonomy))
    expert = _expert_block.render(_profile.load(), _metrics().get("downloads_total"))
    shell = SHELL_SRC.read_text(encoding="utf-8")
    failed = False
    for key, hub in hubs.items():
        arts = hub_articles(hub, all_arts)
        errors, warnings = check(key, hub, arts, dt.date.today())
        for line in warnings:
            print(f"build_topic_hubs: warning: {line}", file=sys.stderr)
        for line in errors:
            print(f"build_topic_hubs: {line}", file=sys.stderr)
        failed |= bool(errors)
        out = _swap_into_shell(
            shell,
            render_hub(key, hub, arts, expert),
            hub["title"],
            " ".join(hub["description"].split()),
            BASE + hub["path"],
        )
        target = PUBLIC / hub["path"].strip("/") / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(_ALT_RE.sub("", out), encoding="utf-8")
        print(f"build_topic_hubs: wrote {target.relative_to(ROOT)} ({len(arts)} articles)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
