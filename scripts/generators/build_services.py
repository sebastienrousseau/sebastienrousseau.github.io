#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Generate the "Work with me" pages from ``_data/services.yml`` (plan F-4).

``/work-with-me/`` is the hub: one answer paragraph and three cards
(Speaking, which keeps its own page, plus the two pages below).
``/work-with-me/research/`` and ``/work-with-me/open-source/`` share one
structure, the pattern AI search quotes: an H1, a one-paragraph answer,
who it is for, what you get, how it works, proof, an FAQ and one call to
action that opens the contact form on the matching subject.

Each detail page carries ``Service`` JSON-LD (provider: the ``#person``
node; no offers or prices) and ``FAQPage`` JSON-LD built from the visible
questions and answers, word for word (F-3). Proof comes only from
``profile.yml`` and ``_data/proof/metrics.json``.

English only, indexable, no hreflang (like ``/trust/``). Runs from
``build.sh`` after ``build_translations`` and before ``postbuild``, so the
sitemap pass adds the pages and the CSP pass hashes their JSON-LD.
"""

from __future__ import annotations

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
from case_studies_components import _esc

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
DATA = ROOT / "_data" / "services.yml"
SHELL_SRC = PUBLIC / "articles" / "index.html"
BASE = "https://sebastienrousseau.com"
PERSON = {"@id": f"{BASE}/#person"}
AREAS = ("United Kingdom", "European Union", "Asia-Pacific")
AUDIENCE = "Banks, payment service providers, fintechs, regulators and industry bodies"
_ALT_RE = re.compile(r'[ \t]*<link\s+rel="alternate"\s+hreflang="[^"]*"\s+href="[^"]*"\s*/?>\n?')


def load() -> dict[str, Any]:
    data: dict[str, Any] = yaml.safe_load(DATA.read_text(encoding="utf-8"))
    return data


def _text(value: str) -> str:
    return " ".join(value.split())


def proof_items(keys: list[str], metrics: dict[str, str], profile: dict[str, Any]) -> list[str]:
    """The proof lines for ``keys``, from the profile and metrics only."""
    lines = {
        "epaa": profile["epaa"]["wording"] + ".",
        "fiap": "Fellow of the Institution of Analysts and Programmers (FIAP).",
        "trust": "SBOMs, build-provenance attestations, Sigstore signatures and licences "
        "for every flagship library, on the Trust page.",
    }
    if metrics.get("downloads_total"):
        lines["downloads"] = (
            f"{metrics['downloads_total']} all-time downloads of the open-source packages "
            "(crates.io, PyPI and npm)."
        )
    return [lines[k] for k in keys if k in lines]


def _section(eyebrow: str, heading_id: str, heading: str, inner: str) -> str:
    return (
        f'<section class="narrative-section" aria-labelledby="{heading_id}">'
        '<div class="narrative-wrap"><div>'
        f'<p class="narrative-eyebrow">{_esc(eyebrow)}</p>'
        f'<h2 id="{heading_id}" class="narrative-head">{_esc(heading)}</h2>'
        f"{inner}</div></div></section>"
    )


def _hero(eyebrow: str, h1: str, answer: str, disclosure: str) -> str:
    return (
        '<section class="story-cta" aria-labelledby="svc-h1">'
        f'<header class="story-head"><p class="story-eyebrow">{_esc(eyebrow)}</p>'
        f'<h1 id="svc-h1" class="story-title">{_esc(h1)}</h1>'
        f'<p class="svc-answer">{_esc(_text(answer))}</p>'
        f'<p class="svc-disclosure">{_esc(_text(disclosure))}</p></header></section>'
    )


def _cta(subject: str) -> str:
    return (
        '<p class="tr-cta"><a class="pill" href="/contact/index.html?subject='
        f'{_esc(subject)}">Get in touch</a></p>'
    )


def render_faq(faq: list[dict[str, str]]) -> str:
    items = "".join(
        '<details class="qa-item">'
        f'<summary class="qa-q">{_esc(item["q"])}</summary>'
        f'<div class="qa-a"><p>{_esc(_text(item["a"]))}</p></div></details>'
        for item in faq
    )
    return _section(
        "FAQ", "svc-faq", "Questions and answers", f'<div class="qa-list">{items}</div>'
    )


def render_page(page: dict[str, Any], disclosure: str, proof: list[str], expert: str = "") -> str:
    audiences = "".join(
        f"<h3>{_esc(a['heading'])}</h3><p>{_esc(_text(a['body']))}</p>" for a in page["audiences"]
    )
    gets = "".join(
        f"<p><strong>{_esc(d['lead'])}</strong> {_esc(_text(d['body']))}</p>"
        for d in page["deliverables"]
    )
    steps = "".join(f"<li>{_esc(_text(s))}</li>" for s in page["steps"])
    proof_html = "".join(f"<li>{_esc(p)}</li>" for p in proof)
    return (
        '<div class="services-page">'
        + _hero(page["eyebrow"], page["h1"], page["answer"], disclosure)
        + _section("Who it's for", "svc-who", "Who it's for", audiences)
        + _section("What you get", "svc-what", "What you get", gets)
        + _section("How it works", "svc-how", "How it works", f"<ol>{steps}</ol>")
        + _section("Proof", "svc-proof", "On the record", f"<ul>{proof_html}</ul>")
        + render_faq(page["faq"])
        + (expert or _cta(page["subject"]))
        + "</div>"
    )


def render_hub(hub: dict[str, Any], disclosure: str, expert: str = "") -> str:
    cards = "".join(
        f'<li class="story-card"><h2 class="story-card-title">{_esc(c["title"])}</h2>'
        f'<p class="story-card-body">{_esc(_text(c["body"]))}</p>'
        f'<p class="story-card-body"><a class="offer-link" href="{_esc(c["href"])}">'
        f"{_esc(c['link'])}</a></p></li>"
        for c in hub["cards"]
    )
    return (
        '<div class="services-page">'
        + _hero(hub["eyebrow"], hub["h1"], hub["answer"], disclosure)
        + f'<section class="story-cta" aria-label="Services"><ul class="story-grid" role="list">{cards}</ul></section>'
        + (expert or _cta("general"))
        + "</div>"
    )


def jsonld(page: dict[str, Any]) -> str:
    """Service and FAQPage JSON-LD for one detail page."""
    url = BASE + page["path"]
    graph = [
        {
            "@type": "Service",
            "@id": f"{url}#service",
            "name": page["service_name"],
            "serviceType": page["service_type"],
            "provider": PERSON,
            "areaServed": [{"@type": "Place", "name": a} for a in AREAS],
            "availableLanguage": ["en", "fr"],
            "audience": {"@type": "BusinessAudience", "audienceType": AUDIENCE},
            "url": url,
        },
        {
            "@type": "FAQPage",
            "@id": f"{url}#faq",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": item["q"],
                    "acceptedAnswer": {"@type": "Answer", "text": _text(item["a"])},
                }
                for item in page["faq"]
            ],
        },
    ]
    payload = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    return f'<script type="application/ld+json">{payload}</script>'


def _write(path: str, title: str, desc: str, body: str, shell: str) -> None:
    out = _swap_into_shell(shell, body, title, _text(desc), BASE + path)
    out = _ALT_RE.sub("", out)
    target = PUBLIC / path.strip("/") / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(out, encoding="utf-8")


def main() -> int:
    if not SHELL_SRC.is_file():
        print(f"build_services: shell missing at {SHELL_SRC}", file=sys.stderr)
        return 1
    data, profile, metrics = load(), _profile.load(), _metrics()
    shell = SHELL_SRC.read_text(encoding="utf-8")
    hub = data["hub"]
    _write(
        hub["path"],
        hub["title"],
        hub["description"],
        render_hub(
            hub, data["disclosure"], _expert_block.render(profile, metrics.get("downloads_total"))
        ),
        shell,
    )
    for page in data["pages"]:
        expert = _expert_block.render(profile, metrics.get("downloads_total"), page["subject"])
        body = render_page(
            page, data["disclosure"], proof_items(page["proof"], metrics, profile), expert
        )
        _write(page["path"], page["title"], page["description"], body + jsonld(page), shell)
    print(f"build_services: wrote {1 + len(data['pages'])} Work with me page(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
