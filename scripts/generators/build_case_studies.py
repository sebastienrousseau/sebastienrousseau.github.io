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

sys.path.insert(0, str(Path(__file__).resolve().parent))
from case_studies_components import _esc
from case_studies_render import _render_body, _render_index_body
from case_studies_schema import _BASE_URL

try:
    import yaml  # type: ignore[import-untyped]
except ImportError:
    sys.stderr.write("error: PyYAML not installed (see requirements.txt)\n")
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
DATA_DIR = ROOT / "_data" / "proof" / "case-studies"
METRICS_PATH = ROOT / "_data" / "proof" / "metrics.json"
SHELL_SRC = PUBLIC / "articles" / "index.html"
OUT_DIR = PUBLIC / "case-studies"

# Per-locale case-study UI labels live in _data/proof/case-studies-i18n.json,
# extracted from three inline dicts for data/code separation (Phase 4.1).
# v1 = base section labels, v2 = Bloomberg-tier elevation, v3 = staged layout;
# _lbl() merges v3 over v2 over v1 with EN fallback.
_CS_I18N = json.loads(
    (ROOT / "_data" / "proof" / "case-studies-i18n.json").read_text(encoding="utf-8")
)
_CS_LABELS: dict[str, dict[str, str]] = _CS_I18N["v1"]
_CS_LABELS_V2: dict[str, dict[str, str]] = _CS_I18N["v2"]
_CS_LABELS_V3: dict[str, dict[str, str]] = _CS_I18N["v3"]


def _lbl(lang: str) -> dict[str, str]:
    """Merged label set for ``lang`` — V3 keys layered on V2 on V1, with
    EN as the fallback for any missing key across all dicts."""
    base = {**_CS_LABELS["en"], **_CS_LABELS_V2["en"], **_CS_LABELS_V3["en"]}
    v1 = _CS_LABELS.get(lang, _CS_LABELS["en"])
    v2 = _CS_LABELS_V2.get(lang, _CS_LABELS_V2["en"])
    v3 = _CS_LABELS_V3.get(lang, _CS_LABELS_V3["en"])
    return {**base, **v1, **v2, **v3}

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




def _load_studies() -> list[dict]:
    """Load every YAML file under ``_data/proof/case-studies/`` and
    return them as dicts. Empty list if the directory is missing.
    Per-locale overlays under ``i18n/<lang>/<slug>.yml`` are loaded
    separately and merged at render time via ``_localised_study``."""
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


def _load_overlay(lang: str, slug: str) -> dict:
    """Load a per-locale overlay YAML if it exists. Returns {} if missing
    or unreadable — caller falls back to EN content."""
    if lang == "en":
        return {}
    path = DATA_DIR / "i18n" / lang / f"{slug}.yml"
    if not path.is_file():
        return {}
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        print(f"build_case_studies: overlay parse failed {path} — {exc}", file=sys.stderr)
        return {}


_OVERLAY_KEEP_EN = frozenset({
    "slug", "banner", "category_slug", "links",
    "related_articles", "signed", "period",
    "outcome_highlights_keep_values", "standards",
})
_OVERLAY_LIST_FIELDS = frozenset({"outcome_highlights", "rigour"})


def _merge_list_of_dicts(base: list, overlay_rows: list) -> list[dict]:
    """Zip overlay rows over base rows so a translator can override
    just the prose ``label`` / ``metric`` keys without restating
    ``value``."""
    merged: list[dict] = []
    for i, base_row in enumerate(list(base) or []):
        row = dict(base_row) if isinstance(base_row, dict) else {}
        if i < len(overlay_rows) and isinstance(overlay_rows[i], dict):
            row.update(overlay_rows[i])
        merged.append(row)
    return merged


def _merge_overlay(study: dict, overlay: dict) -> dict:
    """Return a copy of ``study`` with fields from ``overlay`` substituted.
    List-of-dicts fields (outcome_highlights, rigour) are zipped index-by-
    index so partial overlays still work. Scalar / list-of-string fields
    are simple replacements. URLs, slugs, banner image, signed flag, and
    related_articles stay EN-canonical."""
    if not overlay:
        return study
    out = dict(study)
    for key, val in overlay.items():
        if key in _OVERLAY_KEEP_EN:
            continue
        if key in _OVERLAY_LIST_FIELDS and isinstance(val, list):
            out[key] = _merge_list_of_dicts(study.get(key) or [], val)
        else:
            out[key] = val
    return out


def _localised_study(study: dict, lang: str) -> dict:
    """Return ``study`` merged with its per-locale overlay (if any)."""
    return _merge_overlay(study, _load_overlay(lang, study["slug"]))


def _load_metrics() -> dict:
    if not METRICS_PATH.is_file():
        return {}
    try:
        return json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}










































def _hero_variant(slug: str) -> str:
    """Rotate hero composition across 5 studies so each feels distinct.
    Stable per slug — same slug always gets the same variant."""
    return ("centre", "left", "split")[sum(ord(c) for c in slug) % 3]
































sys.path.insert(0, str(ROOT / "scripts" / "lib"))



























# Ordered (field, label-key, stage-number-or-zero, anchor) tuples driving
# the right-column section render. Stage number 0 means "no NN — prefix".
















def _unescape_head_metas(html_text: str) -> str:
    """Repair entity-escaped ``<meta>`` / ``<link>`` tags some local SSG builds
    emit in the shell's <head>. Bounded to the ``<head>…</head>`` slice so
    escaped markup quoted in body prose is never turned into live tags.
    No-op on CI (tags are already real there).

    Shared helper — build_speaking.py and build_iso20022_mcp.py import this.
    """
    end = html_text.find("</head>")
    if end < 0:
        return html_text
    head = re.sub(
        r"&lt;(?:meta|link)\b.*?&gt;",
        lambda m: _html.unescape(m.group(0)),
        html_text[:end],
        flags=re.DOTALL,
    )
    return head + html_text[end:]


def _sub_verified(pattern: re.Pattern, repl, html: str, anchor: str) -> str:
    """``pattern.subn(..., count=1)`` that fails the build when the anchor is
    missing. A silent no-op here would ship a page wearing the shell's own
    title / description / canonical — worse than failing loudly."""
    out, n = pattern.subn(repl, html, count=1)
    if n == 0:
        raise SystemExit(f"_swap_into_shell: shell anchor not found: {anchor}")
    return out


def _swap_into_shell(shell: str, body: str, title: str, desc: str, url: str) -> str:
    # Callable replacements throughout: the swapped-in content is arbitrary
    # text/HTML, and str.sub replacement *templates* would interpret \g<0> /
    # lone backslashes in it (silent duplication or re.error).
    esc_title, esc_desc, esc_url = _esc(title), _esc(desc), _esc(url)
    out = _sub_verified(
        _TITLE_RE, lambda m: f"<title>{esc_title}</title>", shell, "<title>"
    )
    out = _sub_verified(
        _DESC_RE,
        lambda m: f'<meta name="description" content="{esc_desc}"',
        out,
        "meta description",
    )
    out = _sub_verified(
        _CANONICAL_RE,
        lambda m: f'<link rel="canonical" href="{esc_url}"',
        out,
        "canonical link",
    )
    out = _sub_verified(
        _OG_TITLE_RE, lambda m: m.group(1) + esc_title + m.group(2), out, "og:title"
    )
    out = _sub_verified(
        _OG_DESC_RE, lambda m: m.group(1) + esc_desc + m.group(2), out, "og:description"
    )
    out = _sub_verified(
        _OG_URL_RE, lambda m: m.group(1) + esc_url + m.group(2), out, "og:url"
    )
    # The ap-hero block is a conditional strip, not an anchor: only some
    # homepage-style shells carry it (the articles shell does not), so its
    # absence is expected and must not fail the build.
    out = _AP_HERO_BLOCK_RE.sub("", out, count=1)
    out = _sub_verified(
        _MAIN_WRAP_RE,
        lambda m: m.group(1) + body + m.group(2),
        out,
        '<main> content wrap (<div class="wrap…">)',
    )
    return out


def _write_study(
    shell: str, study: dict, lang: str, url_segment: str,
    lbl: dict[str, str], out_dir: Path, article_slug_map: dict[str, str],
    all_studies: list[dict],
) -> Path:
    slug = study["slug"]
    title = study.get("title", slug)
    desc = (study.get("problem", "") or "")[:155]
    url = (
        f"{_BASE_URL}/case-studies/{slug}/"
        if lang == "en"
        else f"{_BASE_URL}/{lang}/{url_segment}/{slug}/"
    )
    body = _render_body(study, lbl, lang, url_segment, article_slug_map, all_studies)
    out = _swap_into_shell(shell, body, title, desc, url)
    target = out_dir / slug / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(out, encoding="utf-8")
    return target


def _write_index(
    shell: str, studies: list[dict], lang: str, url_segment: str,
    lbl: dict[str, str], out_dir: Path,
) -> Path:
    body = _render_index_body(studies, lbl, lang, url_segment)
    url = (
        f"{_BASE_URL}/case-studies/"
        if lang == "en"
        else f"{_BASE_URL}/{lang}/{url_segment}/"
    )
    out = _swap_into_shell(
        shell, body,
        f"{lbl['Case studies']} — Sebastien Rousseau",
        lbl["deck"],
        url,
    )
    target = out_dir / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(out, encoding="utf-8")
    return target


def _emit_one_locale(
    shell: str, studies: list[dict], lang: str, url_segment: str,
    lbl: dict[str, str], article_slug_map: dict[str, str],
) -> int:
    out_dir = OUT_DIR if lang == "en" else (PUBLIC / lang / url_segment)
    out_dir.mkdir(parents=True, exist_ok=True)
    # Apply per-locale overlay to each study before rendering. EN passes
    # through unchanged (overlay loader returns {} for lang == 'en').
    localised_studies = [_localised_study(s, lang) for s in studies]
    for study in localised_studies:
        _write_study(shell, study, lang, url_segment, lbl, out_dir, article_slug_map, localised_studies)
    _write_index(shell, localised_studies, lang, url_segment, lbl, out_dir)
    return len(localised_studies) + 1


def _emit_locale_forks(studies: list[dict]) -> int:
    """For each active non-EN locale, fork the EN locale shell + run
    translate_chrome to localise nav / footer / search aria / lang switch
    on the case-study pages. Body text is rendered from the per-locale
    label table; YAML body content (Problem prose etc.) stays in EN."""
    sys.path.insert(0, str(ROOT / "scripts" / "lib"))
    sys.path.insert(0, str(ROOT / "scripts" / "generators"))
    try:
        import _lang_registry  # type: ignore[import-not-found]
        from build_translations import _chrome as _ch  # type: ignore[import-not-found]
        from build_translations import _state as _st  # type: ignore[import-not-found]
    except ImportError as exc:
        print(f"build_case_studies: skip locale forks — {exc}", file=sys.stderr)
        return 0

    en_shell = SHELL_SRC.read_text(encoding="utf-8")
    total = 0
    for lang in _lang_registry.active():
        if lang.code == "en":
            continue
        lbl = _lbl(lang.code)
        slugs_map = _lang_registry.load_slugs(lang.code)
        url_segment = slugs_map.get("static", {}).get("case-studies", "case-studies")
        article_slug_map = slugs_map.get("articles", {})
        _st.bind_lang(lang.code)
        # Render the case-study body in this locale (uses per-locale labels)
        # then run the same chrome translator the rest of the locale forks
        # use — nav, footer, search aria, lang switcher all localise.
        localised_shell = _ch._set_html_lang(en_shell)
        localised_shell = _ch.translate_chrome(localised_shell)
        # Rewrite every JSON-LD inLanguage="en"/"en-GB" → this locale's
        # BCP-47 tag so test_jsonld_localized.py passes for the locale forks.
        localised_shell = _ch._localize_inlanguage_globally(localised_shell, lang.code)
        total += _emit_one_locale(
            localised_shell, studies, lang.code, url_segment, lbl, article_slug_map
        )
    return total


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    if not SHELL_SRC.is_file():
        print(f"build_case_studies: missing shell {SHELL_SRC}", file=sys.stderr)
        return 0
    studies = _load_studies()
    shell = SHELL_SRC.read_text(encoding="utf-8")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    en_lbl = _lbl("en")
    en_count = _emit_one_locale(shell, studies, "en", "case-studies", en_lbl, {})
    locale_count = _emit_locale_forks(studies)
    print(
        f"build_case_studies: wrote {len(studies)} case studies + 1 index in EN "
        f"({en_count} files); {locale_count} files across 27 locale forks"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
