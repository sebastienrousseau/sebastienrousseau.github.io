"""Per-page citation furniture: citation graph JSON-LD, cite popovers, and the
visible sources list. Split from article_furniture (Phase 4.1). Imports the
shared article-metadata helper + a few regexes from article_furniture
(one-directional — article_furniture does not import this module).
"""

from __future__ import annotations

import json as _json
import re
from datetime import datetime as _datetime
from html import escape as _esc
from html import unescape as _unesc

from postbuild_lib._i18n import _labels
from postbuild_lib.article_furniture import (
    _AUTHOR_FIRST,
    _AUTHOR_LAST,
    _CANONICAL_RE,
    _DESCRIPTION_RE,
    _MAIN_RE,
    _OG_TITLE_RE,
    _WRAP_CLOSE_RE,
    _extract_article_metadata,
)

CITATION_AUTHORITIES = (
    "iso20022.org",
    "swift.com",
    "iso.org",
    "ietf.org",
    "w3.org",
    "nist.gov",
    "csrc.nist.gov",
    "bis.org",
    "ecb.europa.eu",
    "imf.org",
    "wikipedia.org",
    "wikidata.org",
    "arxiv.org",
    "ieee.org",
    "acm.org",
    "doi.org",
    "blackrock.com",
    "sec.gov",
    "treasury.gov",
    "ofac.treasury.gov",
    "hsbc.com",
    "jpmorgan.com",
    "santander.com",
    "bmo.com",
    "google.com",
    "openai.com",
    "anthropic.com",
    "deepmind.com",
    "github.com",
    "emergingpaymentsasia.org",
)
_OUTBOUND_LINK_RE = re.compile(r'<a\b[^>]*\bhref="(https?://[^"]+)"', re.IGNORECASE)
_AUTHOR_INITIAL = "S."


def _parse_iso_date(date_str: str) -> _datetime | None:
    if not date_str:
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%d"):
        try:
            return _datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def _first_word(title: str) -> str:
    m = re.search(r"\w+", title)
    return m.group(0).lower() if m else "post"


def _citation_blocks(title: str, url: str, date_str: str) -> dict[str, str]:
    """Render the 5 academic citation formats from article metadata."""
    dt = _parse_iso_date(date_str)
    year = str(dt.year) if dt else "n.d."
    month_short = dt.strftime("%b") if dt else ""
    month_long = dt.strftime("%B") if dt else ""
    day = str(dt.day) if dt else ""
    author_lastfirst = f"{_AUTHOR_LAST}, {_AUTHOR_FIRST}"
    author_vancouver = f"{_AUTHOR_LAST} {_AUTHOR_INITIAL[0]}"
    author_apa = f"{_AUTHOR_LAST}, {_AUTHOR_INITIAL}"
    bib_key = f"{_AUTHOR_LAST.lower()}{year}{_first_word(title)}"
    bibtex = (
        f"@online{{{bib_key},\n"
        f"  author  = {{{author_lastfirst}}},\n"
        f"  title   = {{{{{title}}}}},\n"
        f"  year    = {{{year}}},\n"
        f"  url     = {{{url}}},\n"
        f"  urldate = {{{year}}}\n"
        f"}}"
    )
    ris = f"TY  - GEN\nAU  - {author_lastfirst}\nTI  - {title}\nPY  - {year}\nUR  - {url}\nER  -"
    vancouver = (
        f"{author_vancouver}. {title}. sebastienrousseau.com. "
        f"{year} {month_short} {day}. Available from: {url}"
    )
    chicago = (
        f'{author_lastfirst}. "{title}." sebastienrousseau.com. {month_long} {day}, {year}. {url}.'
    )
    apa = f"{author_apa} ({year}, {month_long} {day}). {title}. sebastienrousseau.com. {url}"
    return {
        "BibTeX": bibtex,
        "RIS": ris,
        "Vancouver": vancouver,
        "Chicago": chicago,
        "APA": apa,
    }


def inject_cite_popover(html: str) -> str:
    """Append a zero-JS ``<details class="cite-popover" id="cite-popover">``
    block at the wrap-div close, with one ``<pre>`` per citation format
    (BibTeX / RIS / Vancouver / Chicago / APA). The action-rail's
    "Cite" button jumps here. WS5 will wire copy-to-clipboard
    buttons + main.js handlers; for now readers select-all + copy
    from the <pre>. BlogPosting pages only; idempotent.

    Idempotency gates on the ``id="cite-popover"`` anchor rather than
    the class — `inject_syndication_panel` runs first and also uses
    ``class="cite-popover"`` for shared FT styling (with
    ``id="syndicate-popover"``). Without the ID-based gate, the
    syndicate-popover's class match short-circuits this injector and
    the action-rail's ``href="#cite-popover"`` resolves to no target
    (pa11y WCAG2AAA NoSuchID)."""
    if '"@type":"BlogPosting"' not in html:
        return html
    if 'id="cite-popover"' in html:
        return html
    url_m = _CANONICAL_RE.search(html)
    title_m = _OG_TITLE_RE.search(html)
    if not (url_m and title_m):
        return html
    url = url_m.group(1)
    title = _unesc(title_m.group(1))
    _kw, date_pub, _dm, _wc = _extract_article_metadata(html)
    formats = _citation_blocks(title, url, date_pub)
    labels = _labels(html)
    copy_label = _esc(labels.get("Cite.copy", "Copy"))
    # Meta header — title + description give the reader context before
    # they commit to a citation format. Description comes from the
    # canonical <meta name="description"> the article already carries.
    desc_m = _DESCRIPTION_RE.search(html)
    desc = _unesc(desc_m.group(1)) if desc_m else ""
    # Heading-skip-safe: the cite popover is a <details> disclosure
    # widget whose <summary> already serves as the accessible name.
    # An <h3> here under the article's body <h2>s would still parse,
    # but inside a closed <details> the screen-reader heading tree
    # gets confusing. Use a <p class="cite-title"> with strong text
    # — same visual weight, no heading-skip claim.
    meta_block = (
        f'<header class="cite-meta">'
        f'<p class="cite-title"><strong>{_esc(title)}</strong></p>'
        + (f"<p>{_esc(desc)}</p>" if desc else "")
        + "</header>"
    )
    blocks = []
    for name, body in formats.items():
        target_id = f"cite-{name.lower()}"
        blocks.append(
            f'<div class="cite-format"><p class="cite-format-label">{_esc(name)}</p>'
            f'<pre id="{target_id}">{_esc(body)}</pre>'
            f'<button type="button" class="copy-btn" data-copy="#{target_id}" '
            f'aria-label="{_esc(name, quote=True)} — {copy_label}">{copy_label}</button>'
            f"</div>"
        )
    popover = (
        f'<details class="cite-popover" id="cite-popover">'
        f"<summary>{_esc(labels.get('Cite.heading', 'Cite this article'))}</summary>"
        + meta_block
        + "".join(blocks)
        + "</details>"
    )
    return _WRAP_CLOSE_RE.sub(popover + r"\1", html, count=1)


_NON_BODY_ASIDE_RE = re.compile(
    r'<aside\s+class="(?:author-card|related-posts|post-lead|article-sources|article-toc)\b[^"]*"[\s\S]*?</aside>',
    re.IGNORECASE,
)


def _extract_citations(html: str) -> list[dict[str, str]]:
    """Return at most 12 distinct authoritative outbound links from the
    article body. Strips author-card / related-posts / post-lead / ToC /
    article-sources asides first so the author's own profile links and
    nav chrome don't pollute the citation graph."""
    main_m = _MAIN_RE.search(html)
    if not main_m:
        return []
    body = _NON_BODY_ASIDE_RE.sub("", main_m.group(2))
    seen: set[str] = set()
    out: list[dict[str, str]] = []
    for lm in _OUTBOUND_LINK_RE.finditer(body):
        url = lm.group(1)
        if url in seen:
            continue
        seen.add(url)
        host = url.split("/", 3)[2].lower() if url.count("/") >= 2 else ""
        if not any(host == d or host.endswith("." + d) for d in CITATION_AUTHORITIES):
            continue
        out.append({"@type": "CreativeWork", "url": url})
        if len(out) >= 12:
            break
    return out


def inject_citations(html: str) -> str:
    """Append a "citation" array to the BlogPosting JSON-LD listing the
    authoritative outbound URLs the post references. AI engines extract
    citation graphs from this property to build provenance chains."""
    if '"@type":"BlogPosting"' not in html:
        return html
    cites = _extract_citations(html)
    if not cites:
        return html
    fragment = ',"citation":' + _json.dumps(cites, separators=(",", ":"))
    # Insert just before the "speakable" key in the BlogPosting object.
    return re.sub(
        r'(,"speakable":)',
        fragment + r"\1",
        html,
        count=1,
    )


def inject_sources_list(html: str) -> str:
    """Mirror the JSON-LD citation array as a human-visible <aside> so the
    primary-source references are visible to readers, not just AI crawlers.
    Inserted just before the prev/next nav so it sits at the foot of every
    dated post. Idempotent."""
    if '"@type":"BlogPosting"' not in html:
        return html
    if 'class="article-sources"' in html:
        return html
    cites = _extract_citations(html)
    if not cites:
        return html
    items: list[str] = []
    for c in cites:
        url = c["url"]
        parts = url.split("/", 3)
        host = parts[2] if len(parts) > 2 else url
        path = "/" + parts[3] if len(parts) > 3 else ""
        display = path if len(path) <= 80 else path[:77] + "…"
        items.append(
            f'<li><a href="{url}" rel="external noopener nofollow">'
            f'<span class="source-host">{host}</span>'
            f'<span class="source-path">{display}</span>'
            f"</a></li>"
        )
    heading = _labels(html)["Sources & references"]
    fragment = (
        '<aside class="article-sources" aria-labelledby="sources-heading">'
        f'<h2 id="sources-heading" class="article-sources-heading">{heading}</h2>'
        f'<ol class="article-sources-list">{"".join(items)}</ol>'
        "</aside>"
    )
    # Insert before the prev/next nav if it's already there, else before
    # the closing </div></main>.
    if 'class="post-pagination"' in html:
        return re.sub(r'(<nav class="post-pagination")', fragment + r"\1", html, count=1)
    return re.sub(r"(</div>\s*</main>)", fragment + r"\1", html, count=1)
