# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Apply the content decisions in ``_data/seo/content-decisions.yml`` (plan B-3).

The content audit (``scripts/seo_and_audit/content_audit.py``) suggests an
action per English article; the maintainer records the decision:

    /2026-10-05-some-article/: noindex
    /2026-10-06-other-article/: merge:/2026-05-12-stronger-article/
    /2026-10-07-third-article/: keep        # keep, refresh, review: no-ops

* ``noindex`` merges ``noindex, follow`` into the page's robots meta and
  into each of its translations (found through the locale slug maps), so
  ``prune_sitemaps`` drops them all.
* ``merge:<target>`` turns the page into a redirect page to ``<target>``
  (meta refresh, canonical and og:url to the target, hreflang removed) and
  each translation into a redirect to the target's translation in that
  locale, or to the target itself when there is none.

``validate`` lists decisions whose path or merge target does not exist, or
whose merge target is itself merged or noindexed; ``finalize_seo`` fails the
build on any. Runs after the locale pass and before the sitemaps are pruned.
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml
from postbuild_lib.locale_indexing import merge_noindex
from postbuild_lib.redirects import _convert_page

ROOT = Path(__file__).resolve().parents[3]
DECISIONS = ROOT / "_data" / "seo" / "content-decisions.yml"
SITE = "https://sebastienrousseau.com"
NO_OPS = {"keep", "refresh", "review"}


def load(path: Path = DECISIONS) -> dict[str, str]:
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return {str(k): str(v).strip() for k, v in data.items()}


def _slug(path: str) -> str:
    return path.strip("/")


def translations(slug: str, i18n: Path) -> dict[str, str]:
    """``{lang: native slug}`` for an English article slug."""
    out = {}
    for maps in sorted(i18n.glob("*/slugs.json")):
        native = json.loads(maps.read_text(encoding="utf-8")).get("articles", {}).get(slug)
        if native:
            out[maps.parent.name] = native
    return out


def validate(decisions: dict[str, str], public: Path) -> list[str]:
    problems = []
    for path, action in decisions.items():
        if action in NO_OPS:
            continue
        if not (public / _slug(path) / "index.html").is_file():
            problems.append(f"{path}: no such page")
        if action.startswith("merge:"):
            target = action.split(":", 1)[1]
            if not (public / _slug(target) / "index.html").is_file():
                problems.append(f"{path}: merge target {target} does not exist")
            elif decisions.get(target, "keep") not in NO_OPS:
                problems.append(f"{path}: merge target {target} is itself {decisions[target]}")
        elif action != "noindex":
            problems.append(f"{path}: unknown action {action!r}")
    return problems


def _noindex(page: Path) -> bool:
    html = page.read_text(encoding="utf-8")
    out = merge_noindex(html)
    if out != html:
        page.write_text(out, encoding="utf-8")
    return out != html


def apply_content_decisions(public: Path, decisions: dict[str, str], i18n: Path) -> tuple[int, int]:
    """Apply every decision. Returns (pages noindexed, pages redirected)."""
    noindexed = merged = 0
    for path, action in decisions.items():
        slug = _slug(path)
        langs = translations(slug, i18n)
        pages = [(None, public / slug / "index.html")] + [
            (lang, public / lang / native / "index.html") for lang, native in langs.items()
        ]
        for lang, page in pages:
            if not page.is_file():
                continue
            if action == "noindex":
                noindexed += _noindex(page)
            elif action.startswith("merge:"):
                target = _slug(action.split(":", 1)[1])
                native = translations(target, i18n).get(lang or "")
                href = f"{SITE}/{lang}/{native}/" if lang and native else f"{SITE}/{target}/"
                merged += _convert_page(page, href)
    return noindexed, merged
