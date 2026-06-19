"""Per-language render driver + ``main()`` entry point."""

from __future__ import annotations

import json as _json

import _lang_registry

from . import _state as st
from ._article import render_translation
from ._fm import parse_frontmatter
from ._pages import render_articles_hub, render_home, write_static_translations
from ._search import _build_fr_search_index
from ._state import fr_slug


def _render_one_lang(code: str) -> int:
    """Render every page for one language. Returns total page count."""
    st.bind_lang(code)
    if not st.SRC.is_dir():
        print(f"build_translations: _posts/{code} not found — nothing to do for {code}")
        return 0
    entries: list[dict[str, str]] = []
    written = 0
    for md in sorted(st.SRC.glob("*.md")):
        if not st._DATED_RE.match(md.stem):
            continue
        text = md.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        if not fm.get("title"):
            print(f"build_translations: skip {md.stem} — no title in frontmatter")
            continue
        # File stem may be either the EN slug (legacy) or the FR slug.
        # Resolve both directions so we can find the matching English shell.
        if md.stem in st.FR_TO_EN:
            en = st.FR_TO_EN[md.stem]
            slug_fr = md.stem
        else:
            en = md.stem
            slug_fr = fr_slug(md.stem)
        page = render_translation(en, fm, body)
        if page is None:
            continue
        dst = st.OUT / slug_fr / "index.html"
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(page, encoding="utf-8")
        entries.append(
            {
                "slug": slug_fr,
                "en_slug": en,
                "title": fm.get("title", ""),
                "description": fm.get("description", ""),
                "date": fm.get("date", ""),
                "keywords": fm.get("keywords", ""),
                "banner": fm.get(
                    "banner", "https://cloudcdn.pro/stocks/images/sebastien-rousseau.png"
                ),
                "banner_alt": fm.get("banner_alt", fm.get("title", "")),
            }
        )
        written += 1

    if entries:
        # Sort newest first to mirror the English /articles/ ordering.
        entries.sort(key=lambda e: e["slug"], reverse=True)
        # /fr/articles/ — the French articles listing (was /fr/index.html).
        articles_hub = render_articles_hub(entries)
        if articles_hub:
            articles_path = st.OUT / st.STATIC_SLUG_FR.get("articles", "articles") / "index.html"
            articles_path.parent.mkdir(parents=True, exist_ok=True)
            articles_path.write_text(articles_hub, encoding="utf-8")
            written += 1

    # /fr/index.html — the French home page, forked from the EN /index.html
    # so the structure (hero + projects + quote + paper + latest + experience)
    # is identical to / for visual parity.
    home = render_home()
    if home:
        (st.OUT / "index.html").write_text(home, encoding="utf-8")
        written += 1

    # Static-page mirrors (about, papers, projects, topics, tags,
    # contact, accessibility, privacy, terms, …) — keep FR visitors
    # inside /fr/ when they click any nav or footer link.
    static_written = write_static_translations()
    written += static_written

    # Per-language search index — visible text of every rendered page,
    # loaded by the Static Site Generator search palette when the visitor is in
    # /<code>/.
    search_entries = _build_fr_search_index()
    (st.OUT / "search-index.json").write_text(
        _json.dumps({"entries": search_entries}, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )

    print(
        f"build_translations[{code}]: wrote {written} page(s) "
        f"({len(entries)} translation(s) + hub + {static_written} static page(s)) "
        f"+ search index ({len(search_entries)} entries)"
    )
    return written


def main() -> None:
    """Render every active non-EN language. Each language is independent;
    a failure in one shouldn't block the others, but a structural error
    (missing data file) should still surface — we don't swallow
    exceptions, so the build fails fast.
    """
    targets = [lg.code for lg in _lang_registry.LANGUAGES if lg.active and lg.code != "en"]
    if not targets:
        print("build_translations: no active non-EN languages")
        return
    total = 0
    for code in targets:
        total += _render_one_lang(code)
    print(f"build_translations: {len(targets)} language(s) rendered, {total} page(s) total")
