#!/usr/bin/env python3
"""Generate the ``/speaking/`` authority hub from ``speaking.yml``.

The speaking kit — bios, outcome-framed talk topics, and an invite CTA —
already lives in ``_data/proof/speaking.yml`` but nothing rendered it.
This generator forks the FT-tier ``/articles/index.html`` shell (so the
typography, CSP, SRI, and accessibility profile stay identical to the
rest of the site) and swaps in a body composed only of existing utility
classes, then relies on the postbuild passes for SEO / CSP / JSON-LD
hashing.

Runs from ``build.sh`` AFTER ``build_translations`` (so it lands only on
the English tree, like ``build_changelog``) and BEFORE ``postbuild`` (so
the sitemap-augment pass adds it and its inline JSON-LD is CSP-hashed).

Output: ``public/speaking/index.html``
Input:  ``_data/proof/speaking.yml``   (single source of truth)
        ``public/articles/index.html`` (shell template)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml  # type: ignore[import-untyped]
except ImportError:  # pragma: no cover
    print("build_speaking: pyyaml not installed", file=sys.stderr)
    raise

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
from build_case_studies import _swap_into_shell
from case_studies_components import _esc

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
SPEAKING_YML = ROOT / "_data" / "proof" / "speaking.yml"
SHELL_SRC = PUBLIC / "articles" / "index.html"
BASE_URL = "https://sebastienrousseau.com"
URL = f"{BASE_URL}/speaking/"


def _bio_block(key: str, label: str, value: str) -> str:
    bid = f"bio-{key}"
    return (
        '<div class="cite-format">'
        f'<p class="cite-format-label">{_esc(label)}</p>'
        f'<pre id="{bid}">{_esc(value.strip())}</pre>'
        f'<button type="button" class="copy-btn" data-copy="#{bid}" '
        f'aria-label="{_esc(label)} — Copy">Copy</button>'
        "</div>"
    )


def _topics_jsonld(topics: list[dict]) -> str:
    items = [
        {
            "@type": "ListItem",
            "position": i + 1,
            "name": t.get("title", ""),
            "description": t.get("summary", "").strip(),
        }
        for i, t in enumerate(topics)
        if t.get("title")
    ]
    payload = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Speaking topics — Sebastien Rousseau",
        "itemListElement": items,
    }
    return (
        '<script type="application/ld+json">'
        + json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        + "</script>"
    )


def _render_body(data: dict) -> str:
    bio = data.get("bio", {}) or {}
    topics = data.get("topics", []) or []
    short = bio.get("short", "").strip()

    parts: list[str] = []
    parts.append(
        '<section class="feat" aria-labelledby="speaking-h1"><div class="wrap">'
        '<p class="feat-eyebrow">Speaking &amp; advisory</p>'
        '<h1 id="speaking-h1" class="feat-headline">Speaking &amp; advisory.</h1>'
        f"<p>{_esc(short)}</p>"
        '<p><a class="pill" href="/contact/">Invite me to speak</a></p>'
        "</div></section>"
    )

    if topics:
        cards = "".join(
            '<article class="offer-card">'
            f"<h3>{_esc(t.get('title', ''))}</h3>"
            f"<p>{_esc(t.get('summary', '').strip())}</p>"
            "</article>"
            for t in topics
            if t.get("title")
        )
        parts.append(
            '<section class="feat alt" aria-labelledby="speaking-topics">'
            '<div class="wrap">'
            '<p class="feat-eyebrow">Topics</p>'
            '<h2 id="speaking-topics" class="feat-headline">'
            "Talks, framed as outcomes.</h2>"
            f'<div class="offer-cards">{cards}</div>'
            "</div></section>"
        )

    bio_blocks = [
        _bio_block(k, label, bio[k])
        for k, label in (
            ("short", "Short bio"),
            ("medium", "Medium bio"),
            ("long", "Long bio"),
        )
        if bio.get(k)
    ]
    if bio_blocks:
        parts.append(
            '<section class="feat" aria-labelledby="speaking-bio"><div class="wrap">'
            '<p class="feat-eyebrow">Press &amp; media</p>'
            '<h2 id="speaking-bio" class="feat-headline">Ready-to-use bio.</h2>'
            + "".join(bio_blocks)
            + "</div></section>"
        )

    parts.append(_topics_jsonld(topics))
    return "".join(parts)


def main() -> int:
    if not SHELL_SRC.is_file():
        print(f"build_speaking: shell missing at {SHELL_SRC}", file=sys.stderr)
        return 1
    if not SPEAKING_YML.is_file():
        print(f"build_speaking: {SPEAKING_YML} missing", file=sys.stderr)
        return 1

    data = yaml.safe_load(SPEAKING_YML.read_text(encoding="utf-8")) or {}
    shell = SHELL_SRC.read_text(encoding="utf-8")
    body = _render_body(data)
    title = "Speaking & advisory — Sebastien Rousseau"
    desc = (data.get("bio", {}).get("short", "") or "").strip()[:155]
    out = _swap_into_shell(shell, body, title, desc, URL)

    target = PUBLIC / "speaking" / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(out, encoding="utf-8")
    print(f"build_speaking: wrote {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
