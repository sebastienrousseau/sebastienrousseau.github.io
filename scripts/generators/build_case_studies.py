#!/usr/bin/env python3
"""Generate outcome-led case-study pages under ``public/case-studies/``.

Phase 1 of the Authority Playbook (see plan §1). Each case study is a
data file in ``_data/proof/case-studies/<slug>.yml`` rendered into a
standalone HTML document sharing the FT-tier ``/articles/`` shell — so
the typography, accessibility, and CSP profile stay identical to the
rest of the site.

The page structure follows the plan's exact order:
    Problem → Role → What I built → Outcomes / Engineering rigour →
    External validation → Standards → Links → Related articles

Outputs:
    public/case-studies/index.html            hub listing every study
    public/case-studies/<slug>/index.html    one per data file

Inputs:
    _data/proof/case-studies/*.yml           case-study data (source of truth)
    _data/proof/metrics.json                 build-time metrics (optional)
    public/articles/index.html               FT-tier shell template

Runs in ``build.sh`` after ``ssg`` has emitted the articles shell, and
before ``build_translations`` so the locale-fork pass can pick the
case-study pages up.
"""

from __future__ import annotations

import argparse
import html as _html
import json
import re
import sys
from pathlib import Path

try:
    import yaml  # type: ignore[import-untyped]
except ImportError:
    print("error: PyYAML not installed (see requirements.txt)", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
DATA_DIR = ROOT / "_data" / "proof" / "case-studies"
METRICS_PATH = ROOT / "_data" / "proof" / "metrics.json"
SHELL_SRC = PUBLIC / "articles" / "index.html"
OUT_DIR = PUBLIC / "case-studies"

_BASE_URL = "https://sebastienrousseau.com"
_TITLE_RE = re.compile(r"<title>[^<]*</title>", re.IGNORECASE)
_DESC_RE = re.compile(
    r'<meta name="description" content="[^"]*"', re.IGNORECASE
)
_CANONICAL_RE = re.compile(
    r'<link rel="canonical" href="[^"]*"', re.IGNORECASE
)
_OG_TITLE_RE = re.compile(
    r'(<meta property="og:title" content=")[^"]*(")', re.IGNORECASE
)
_OG_DESC_RE = re.compile(
    r'(<meta property="og:description" content=")[^"]*(")', re.IGNORECASE
)
_OG_URL_RE = re.compile(
    r'(<meta property="og:url" content=")[^"]*(")', re.IGNORECASE
)
_MAIN_WRAP_RE = re.compile(
    r'(<main\b[^>]*>\s*)<div class="wrap[^"]*">[\s\S]*?</div>(\s*</main>)',
    re.IGNORECASE,
)
_AP_HERO_BLOCK_RE = re.compile(
    r'<section class="ap-hero">[\s\S]*?</section>', re.IGNORECASE
)


def _esc(s: str) -> str:
    return _html.escape(str(s or ""), quote=True)


def _load_studies() -> list[dict]:
    """Load every YAML file under ``_data/proof/case-studies/`` and
    return them as dicts. Empty list if the directory is missing."""
    if not DATA_DIR.is_dir():
        return []
    studies = []
    for path in sorted(DATA_DIR.glob("*.yml")):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            print(f"build_case_studies: skip {path.name} — {exc}", file=sys.stderr)
            continue
        if not data.get("slug"):
            print(f"build_case_studies: skip {path.name} — missing slug", file=sys.stderr)
            continue
        studies.append(data)
    return studies


def _load_metrics() -> dict:
    if not METRICS_PATH.is_file():
        return {}
    try:
        return json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _render_rigour_table(rigour: list[dict]) -> str:
    if not rigour:
        return ""
    rows = "".join(
        f'<tr><th scope="row">{_esc(r.get("metric",""))}</th>'
        f'<td>{_esc(r.get("value",""))}</td></tr>'
        for r in rigour
    )
    return (
        '<table class="case-study-rigour">'
        '<caption>Engineering rigour</caption>'
        '<thead><tr><th scope="col">Signal</th><th scope="col">Evidence</th></tr></thead>'
        f"<tbody>{rows}</tbody></table>"
    )


def _render_list(heading: str, items: list[str], css_class: str) -> str:
    if not items:
        return ""
    lis = "".join(f"<li>{_esc(item)}</li>" for item in items)
    return f'<section class="{css_class}"><h2>{_esc(heading)}</h2><ul>{lis}</ul></section>'


def _render_links(links: dict[str, str]) -> str:
    if not links:
        return ""
    order = (
        "repo", "site", "pypi", "crates", "docs", "stats",
        "qtonic_evaluation", "bank", "linkedin",
    )
    label_map = {
        "repo": "GitHub repository",
        "site": "Project site",
        "pypi": "PyPI",
        "crates": "crates.io",
        "docs": "Docs.rs",
        "stats": "PyPI download stats",
        "qtonic_evaluation": "Qtonic Quantum Lab independent evaluation",
        "bank": "HSBC",
        "linkedin": "LinkedIn",
    }
    rows = []
    seen = set()
    for key in order:
        if key in links and key not in seen:
            seen.add(key)
            rows.append(
                f'<li><a href="{_esc(links[key])}" rel="noopener noreferrer">'
                f"{_esc(label_map.get(key, key))}</a></li>"
            )
    for key, val in links.items():
        if key not in seen:
            rows.append(
                f'<li><a href="{_esc(val)}" rel="noopener noreferrer">{_esc(key)}</a></li>'
            )
    return f'<section class="case-study-links"><h2>Links</h2><ul>{"".join(rows)}</ul></section>'


def _render_related_articles(slugs: list[str]) -> str:
    if not slugs:
        return ""
    items = "".join(
        f'<li><a href="/{slug}/">{_esc(slug.replace("-", " "))}</a></li>'
        for slug in slugs
    )
    return (
        '<section class="case-study-related"><h2>Related articles</h2>'
        f"<ul>{items}</ul></section>"
    )


def _render_body(study: dict) -> str:
    title = study.get("title", study.get("slug", ""))
    role = study.get("role", "")
    period = study.get("period", "")
    status = study.get("status", "")
    problem = study.get("problem", "")
    what_i_built = study.get("what_i_built", "")

    meta_lines = []
    if role:
        meta_lines.append(f'<p class="case-study-meta"><strong>Role:</strong> {_esc(role)}</p>')
    if period:
        meta_lines.append(f'<p class="case-study-meta"><strong>Period:</strong> {_esc(period)}</p>')
    if status:
        meta_lines.append(f'<p class="case-study-meta"><strong>Status:</strong> {_esc(status)}</p>')

    rigour_table = _render_rigour_table(study.get("rigour", []) or [])
    validation_block = _render_list(
        "External validation", study.get("validation", []) or [], "case-study-validation"
    )
    standards_block = _render_list(
        "Standards", study.get("standards", []) or [], "case-study-standards"
    )
    links_block = _render_links(study.get("links", {}) or {})
    related_block = _render_related_articles(study.get("related_articles", []) or [])

    return (
        '<div class="wrap report-wrap case-study-wrap">'
        '<header class="tag-landing-hero case-study-hero">'
        '<p class="eyebrow">CASE STUDY</p>'
        f"<h1>{_esc(title)}</h1>"
        f"{''.join(meta_lines)}"
        "</header>"
        '<section class="case-study-problem">'
        "<h2>Problem</h2>"
        f"<p>{_esc(problem)}</p>"
        "</section>"
        '<section class="case-study-built">'
        "<h2>What I built</h2>"
        f"<p>{_esc(what_i_built)}</p>"
        "</section>"
        f"{rigour_table}"
        f"{validation_block}"
        f"{standards_block}"
        f"{links_block}"
        f"{related_block}"
        "</div>"
    )


def _render_index_body(studies: list[dict]) -> str:
    if not studies:
        return (
            '<div class="wrap report-wrap">'
            '<header class="tag-landing-hero">'
            '<p class="eyebrow">CASE STUDIES</p>'
            "<h1>Case studies</h1>"
            '<p class="deck">No case studies yet — check back soon.</p>'
            "</header></div>"
        )
    cards = []
    for study in studies:
        slug = study["slug"]
        title = study.get("title", slug)
        problem = study.get("problem", "")
        cards.append(
            '<article class="tag-landing-card tag-landing-card--ft">'
            f'<div class="card-body">'
            '<p class="eyebrow card-eyebrow">CASE STUDY</p>'
            f'<h2><a href="/case-studies/{_esc(slug)}/">{_esc(title)}</a></h2>'
            f'<p class="card-excerpt">{_esc(problem[:220])}…</p>'
            "</div></article>"
        )
    return (
        '<div class="wrap report-wrap">'
        '<header class="tag-landing-hero">'
        '<p class="eyebrow">CASE STUDIES</p>'
        "<h1>Case studies</h1>"
        '<p class="deck">Outcome-led case studies for the open-source libraries and product programmes that show up in the article archive. Each entry leads with externally verifiable rigour signals — never adopter counts I can\'t back up.</p>'
        f'<p class="tag-landing-meta">{len(studies)} case studies</p>'
        "</header>"
        '<section class="tag-landing-list" aria-label="Case studies">'
        + "".join(cards)
        + "</section>"
        "</div>"
    )


def _swap_into_shell(shell: str, body: str, title: str, desc: str, url: str) -> str:
    out = _TITLE_RE.sub(f"<title>{_esc(title)}</title>", shell, count=1)
    out = _DESC_RE.sub(
        f'<meta name="description" content="{_esc(desc)}"', out, count=1
    )
    out = _CANONICAL_RE.sub(
        f'<link rel="canonical" href="{_esc(url)}"', out, count=1
    )
    out = _OG_TITLE_RE.sub(rf'\1{_esc(title)}\2', out, count=1)
    out = _OG_DESC_RE.sub(rf'\1{_esc(desc)}\2', out, count=1)
    out = _OG_URL_RE.sub(rf'\1{_esc(url)}\2', out, count=1)
    out = _AP_HERO_BLOCK_RE.sub("", out, count=1)
    out = _MAIN_WRAP_RE.sub(rf'\1{body}\2', out, count=1)
    return out


def _write_study(shell: str, study: dict) -> Path:
    slug = study["slug"]
    title = study.get("title", slug)
    desc = (study.get("problem", "") or "")[:155]
    url = f"{_BASE_URL}/case-studies/{slug}/"
    body = _render_body(study)
    out = _swap_into_shell(shell, body, title, desc, url)
    target = OUT_DIR / slug / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(out, encoding="utf-8")
    return target


def _write_index(shell: str, studies: list[dict]) -> Path:
    body = _render_index_body(studies)
    out = _swap_into_shell(
        shell,
        body,
        "Case studies — Sebastien Rousseau",
        "Outcome-led case studies for the open-source libraries and product programmes shipped at sebastienrousseau.com — each entry leads with externally verifiable rigour signals.",
        f"{_BASE_URL}/case-studies/",
    )
    target = OUT_DIR / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(out, encoding="utf-8")
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    if not SHELL_SRC.is_file():
        print(f"build_case_studies: missing shell {SHELL_SRC}", file=sys.stderr)
        return 0
    studies = _load_studies()
    shell = SHELL_SRC.read_text(encoding="utf-8")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    paths = [_write_study(shell, study).as_posix() for study in studies]
    paths.append(_write_index(shell, studies).as_posix())
    print(f"build_case_studies: wrote {len(studies)} case studies + 1 index ({len(paths)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
