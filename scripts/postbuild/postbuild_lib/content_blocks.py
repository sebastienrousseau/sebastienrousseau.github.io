"""Per-page content-block furniture: hero banner, mermaid diagrams,
footnotes, pull-quotes, section rules, speculation rules, and FAQ→Q&A.

Split from article_furniture (Phase 4.1). Imports shared constants + _is_french
from article_furniture and _labels from _i18n (one-directional — article_furniture
does not import this module).
"""

from __future__ import annotations

import re
from html import escape as _esc
from html import unescape as _unesc

from postbuild_lib._i18n import _labels
from postbuild_lib.article_furniture import (
    _BANNER_ALT_FRONTMATTER_RE,
    _BANNER_FALLBACK_HEIGHT,
    _BANNER_FALLBACK_WIDTH,
    _FOOTNOTE_DEF_RE,
    _H1_RE,
    _HEAD_END_RE,
    _HERO_BANNER_INSERT_RE,
    _MIN_H2_FOR_RULES,
    _OG_IMAGE_ALT_RE,
    _WRAP_CLOSE_RE,
    _csp_tag_re,
    _is_french,
)

_PULL_BLOCKQUOTE_RE = re.compile(
    r'<blockquote\b[^>]*\bclass="[^"]*\bpull\b[^"]*"[^>]*>([\s\S]*?)</blockquote>',
    re.IGNORECASE,
)
_H2_WITH_ID_RE = re.compile(r'<h2\s+id="[^"]*"[^>]*>', re.IGNORECASE)
_FOOTNOTE_MARKER_RE = re.compile(r"\[\^(\d+)\]")


def inject_pullquotes(html: str) -> str:
    """Promote ``<blockquote class="pull">…</blockquote>`` blocks to
    ``<aside class="pull-quote">…</aside>`` so the FT-style serif italic
    + oversized opening-quote CSS (WS1 commit 2) applies. The marker
    class is opt-in — authors who don't want a pull-quote keep the
    plain blockquote. BlogPosting pages only; idempotent."""
    if '"@type":"BlogPosting"' not in html:
        return html
    if 'class="pull-quote"' in html:
        return html
    return _PULL_BLOCKQUOTE_RE.sub(
        lambda m: f'<aside class="pull-quote">{m.group(1)}</aside>',
        html,
    )


def inject_section_rules(html: str) -> str:
    """Insert ``<hr class="section-rule" aria-hidden="true">`` BEFORE
    every prose ``<h2 id="...">`` after the first, on long-read
    articles with at least 6 such headings. Targets the anchored body
    headings stamped by ``inject_anchor_links_and_toc`` — so the
    aside-only headings (Contents, Lead, Sources) are skipped, and
    short pieces don't get visually overloaded with rules. Skipping
    the first H2 preserves the natural break from the hero section.
    BlogPosting pages only; idempotent."""
    if '"@type":"BlogPosting"' not in html:
        return html
    if 'class="section-rule"' in html:
        return html
    headings = list(_H2_WITH_ID_RE.finditer(html))
    if len(headings) < _MIN_H2_FOR_RULES:
        return html
    rule = '<hr class="section-rule" aria-hidden="true">'
    out = html
    # Walk back-to-front so earlier offsets stay valid as we splice.
    for match in reversed(headings[1:]):
        start = match.start()
        out = out[:start] + rule + out[start:]
    return out


def _footnote_list_items(definitions: list[tuple[str, str]], labels: dict[str, str]) -> str:
    backref_label = labels.get("Footnotes.return", "Return to text")
    items = []
    for n, body in definitions:
        items.append(
            f'<li id="fn-{n}">{body} '
            f'<a class="footnote-back" href="#fnref-{n}" '
            f'aria-label="{_esc(backref_label, quote=True)}">↩</a></li>'
        )
    return "".join(items)


def inject_footnotes(html: str) -> str:
    """Convert literal markdown footnote markers (``[^n]`` in text and
    ``[^n]: …`` at the article foot) into HTML: each in-text marker
    becomes a numbered ``<sup><a>`` link, and the collected definitions
    surface as a ``<section class="footnotes">`` block immediately
    inside the wrap-div close. Static Site Generator (SSG) doesn't expand footnotes,
    so we do it at postbuild. BlogPosting pages only; idempotent."""
    if '"@type":"BlogPosting"' not in html:
        return html
    if 'class="footnotes"' in html:
        return html
    if "[^" not in html:
        return html
    definitions = _FOOTNOTE_DEF_RE.findall(html)
    if not definitions:
        return html
    # Strip the literal "[^n]: definition" lines from the body — they're
    # about to be moved into the <section class="footnotes"> block.
    body_no_defs = _FOOTNOTE_DEF_RE.sub("", html)

    # Wrap remaining "[^n]" markers in <sup><a> superscript links.
    def _sup(m: re.Match[str]) -> str:
        n = m.group(1)
        return f'<sup class="footnote-ref"><a href="#fn-{n}" id="fnref-{n}">{n}</a></sup>'

    body_marked = _FOOTNOTE_MARKER_RE.sub(_sup, body_no_defs)
    labels = _labels(html)
    heading = _esc(labels.get("Footnotes.heading", "Footnotes"), quote=True)
    items = _footnote_list_items(definitions, labels)
    section = (
        f'<section class="footnotes" aria-labelledby="footnotes-heading">'
        f'<h2 id="footnotes-heading">{heading}</h2>'
        f"<ol>{items}</ol></section>"
    )
    return _WRAP_CLOSE_RE.sub(section + r"\1", body_marked, count=1)


_OG_IMAGE_RE = re.compile(
    r'<meta\s+property="og:image"\s+content="([^"]+)"',
    re.IGNORECASE,
)
_OG_IMAGE_WIDTH_RE = re.compile(
    r'<meta\s+property="og:image:width"\s+content="(\d+)"',
    re.IGNORECASE,
)
_OG_IMAGE_HEIGHT_RE = re.compile(
    r'<meta\s+property="og:image:height"\s+content="(\d+)"',
    re.IGNORECASE,
)


def _banner_dimensions(html: str) -> tuple[int, int]:
    """Read og:image:width / og:image:height from the rendered HTML and
    return ``(width, height)`` as integers. Falls back to the canonical
    16:9 hero dims when either tag is absent or malformed.

    This is what fixes the lighthouse CLS regression: an article whose
    banner has a 2.5:1 natural ratio (e.g. 1425×571) needs a 2.5:1 box
    reservation. Hardcoding 16:9 attributes meant the browser reserved a
    16:9 box while CSS set ``aspect-ratio: 16/9``; when the natural image
    actually arrived, ``object-fit: cover`` cropped the strip but the box
    surrounding text still shifted by ~0.04 above the 0.1 CLS threshold.
    Reading the real og:image dimensions makes the reservation exact.
    """
    w_m = _OG_IMAGE_WIDTH_RE.search(html)
    h_m = _OG_IMAGE_HEIGHT_RE.search(html)
    # The og:image:width/height regexes only match \d+, so the int() cast
    # cannot fail — validation is the regex shape, not a runtime check.
    if w_m and h_m:
        w = int(w_m.group(1))
        h = int(h_m.group(1))
        if w > 0 and h > 0:
            return w, h
    return _BANNER_FALLBACK_WIDTH, _BANNER_FALLBACK_HEIGHT


def _banner_path(banner_url: str) -> str | None:
    """Return the on-CDN path component (e.g. ``/stocks/images/foo.webp``)
    of a banner URL, or ``None`` if the URL has no extractable path."""
    m = re.match(r"https?://[^/]+(/[^?#]+)", banner_url)
    return m.group(1) if m else None


def strip_legacy_inline_banner(html: str, banner_url: str) -> str:
    """Remove the legacy ``<p><img></p>`` wrapper that pre-2026 articles
    used to place the banner inline as the first body element.

    Pre-2026 articles routinely placed the banner as the first paragraph
    in the markdown source (``![alt](url)`` → ``<p><img></p>``). The
    article-banner figure injected by ``inject_hero_banner`` now carries
    that role at the top of every page, so the inline copy is a visible
    duplicate of the same image.

    Detection: find the first ``<p><img></p>`` after the article-banner
    figure (skipping ``langswitch`` aside + ``lead-start`` aside in
    between); if the img's src contains the og:image path as a substring,
    drop the entire ``<p>…</p>`` wrapper. The wrap_cdn_images postbuild
    pass may have rewritten the body img to a ``/api/transform?url=…``
    form, so substring match is used instead of URL equality.

    No-op if the page has no article-banner figure (e.g. listings,
    static pages) or the first body ``<p><img></p>`` doesn't match the
    banner.
    """
    og_path = _banner_path(banner_url)
    if og_path is None:
        return html
    # Anchor: the close of the auto-injected article-banner figure.
    anchor = re.search(r"</figure>", html, re.IGNORECASE)
    if not anchor:
        return html
    # Look at the first ~4 KB after </figure> for a `<p><img …></p>`
    # whose src contains the banner path. The langswitch + lead-start
    # asides come in between but are easy to skip — they're `<aside>`
    # tags that the regex skips over.
    start = anchor.end()
    window = html[start : start + 4000]
    m = re.search(
        r'<p>\s*<img\b[^>]*\bsrc="([^"]+)"[^>]*>\s*</p>',
        window,
        re.IGNORECASE,
    )
    if not m or og_path not in m.group(1):
        return html
    # Drop the matched <p>…</p>.
    abs_start = start + m.start()
    abs_end = start + m.end()
    return html[:abs_start] + html[abs_end:]


def inject_hero_banner(html: str) -> str:
    """Insert a hero ``<figure class="article-banner">`` right after the
    H1/byline ``<section class="ap-hero">`` on every BlogPosting page.

    Source: ``<meta property="og:image">`` (set by the SSG from the
    article's frontmatter ``banner:`` field).
    Alt:    ``<meta name="twitter:image:alt">`` (set by the SSG from
            ``banner_alt:``), falling back to the article's H1 title.

    Idempotent. Skips:
      - non-BlogPosting pages (listings / static pages)
      - pages already carrying ``class="article-banner"`` (re-runs)
      - legacy articles whose first body image already matches the
        og:image URL (``_body_starts_with_banner_image``); without this
        check we'd inject a duplicate, producing the banner-then-banner
        stack at the top of the article that the 2018 / 2023 series
        currently shows.
    """
    if '"@type":"BlogPosting"' not in html:
        return html
    if 'class="article-banner"' in html:
        return html
    og = _OG_IMAGE_RE.search(html)
    if not og:
        return html
    banner_url = og.group(1)
    banner_width, banner_height = _banner_dimensions(html)

    alt_m = _BANNER_ALT_FRONTMATTER_RE.search(html) or _OG_IMAGE_ALT_RE.search(html)
    if alt_m:
        alt_text = alt_m.group(1)
    else:
        # Fallback: derive from the H1 — better than nothing, screen-reader-safe.
        h1 = _H1_RE.search(html)
        alt_text = f"Banner for: {h1.group(1).strip()}" if h1 else ""

    figure = (
        f'<figure class="article-banner">'
        f'<img src="{banner_url}" alt="{alt_text}" '
        f'width="{banner_width}" height="{banner_height}" '
        f'fetchpriority="high" decoding="async" />'
        f"</figure>"
    )
    # Insert immediately after the closing </section> of the ap-hero block.
    # Same anchor _LANG_SWITCH_INSERT_RE uses, but we run BEFORE the lang
    # switcher so its insertion sees the banner already in place and slots
    # the langswitch aside after the banner.
    new_html, n = _HERO_BANNER_INSERT_RE.subn(
        lambda m: f"{m.group(1)}{figure}{m.group(2)}",
        html,
        count=1,
    )
    if not n:
        return html
    # Legacy authoring pattern: pre-2026 articles placed the banner image
    # inline as the first body element. The auto-injected figure above
    # now carries that role, so the inline copy is a visible duplicate.
    return strip_legacy_inline_banner(new_html, banner_url)


_FAQ_H2_RE = re.compile(
    r'<h2 id="(frequently-asked-questions|foire-aux-questions)"[^>]*>'
    r"([\s\S]+?)</h2>"
    r"([\s\S]+?)"
    r"(?=<h2|<aside|</main>|<hr|<footer)",
)


def _convert_faq_to_qa(html: str) -> str:
    """Convert the plain ``<p><strong>Q?</strong></p><p>A</p>…`` FAQ
    structure inside articles into the collapsible ``<details class="qa-item">``
    pattern used by ``/projects/`` and ``/papers/`` for UX/UI consistency.
    """
    is_fr = _is_french(html)
    headline = "Questions ?" if is_fr else "Questions?"
    soft = "Réponses." if is_fr else "Answers."

    def patch(m: re.Match[str]) -> str:
        faq_id = m.group(1)  # preserve original anchor so TOC links stay valid
        body = m.group(3)
        # Strip the trailing "<a class='heading-anchor'>#</a>" inside H2.
        # Walk for Q/A pairs: <p><strong>Q?</strong></p><p>A</p>
        qa_pairs: list[tuple[str, str]] = []
        # Capture Q + multiple following <p>…</p> until next <p><strong>...?</strong></p>.
        # Build a list of P-segments first, then pair Q with the answer chunk.
        segments: list[str] = [
            sm.group(1).strip() for sm in re.finditer(r"<p>([\s\S]*?)</p>", body)
        ]
        i = 0
        while i < len(segments):
            seg = segments[i]
            # Q heuristic: starts with <strong> and ends with ? (or French ?)
            qm = re.match(r"^<strong>([\s\S]+?)</strong>\s*$", seg)
            if qm:
                question = qm.group(1).strip()
                # Collect answer paragraphs until next strong-only paragraph
                ans_parts: list[str] = []
                j = i + 1
                while j < len(segments):
                    nxt = segments[j]
                    if re.match(r"^<strong>[\s\S]+?</strong>\s*$", nxt):
                        break
                    ans_parts.append(nxt)
                    j += 1
                qa_pairs.append((question, "</p><p>".join(ans_parts)))
                i = j
            else:
                i += 1

        if not qa_pairs:
            return m.group(0)

        new_h2 = (
            f'<h2 id="{faq_id}" class="qa-headline">{headline} '
            f'<span class="qa-headline-soft">{soft}</span></h2>'
        )
        out_parts: list[str] = [new_h2, f'<section class="qa-list" aria-labelledby="{faq_id}">']
        for q, a in qa_pairs:
            out_parts.append(
                f'<details class="qa-item"><summary class="qa-q">{q}</summary>'
                f'<div class="qa-a"><p>{a}</p></div></details>'
            )
        out_parts.append("</section>")
        return "".join(out_parts)

    return _FAQ_H2_RE.sub(patch, html)


_MERMAID_BLOCK_RE = re.compile(
    r'<pre[^>]*>\s*<code\s+class="language-mermaid"[^>]*>([\s\S]*?)</code>\s*</pre>',
    re.IGNORECASE,
)
_content_attr_re = re.compile(
    r'(content=)(["\'])(.+?)(\2)',
    re.IGNORECASE | re.DOTALL,
)


def inject_mermaid(html: str) -> str:
    """Convert ```mermaid fenced blocks into <pre class="mermaid"> containers
    so main.js can lazy-load the Mermaid library and render them. Also
    widens the meta-CSP script-src to allow the cdn.jsdelivr.net import,
    but only on pages that actually contain a Mermaid block."""
    if "language-mermaid" not in html:
        return html

    def replace(m: re.Match[str]) -> str:
        # Strip <span> wrappers a syntax highlighter may have added,
        # then unescape entities — Mermaid wants the raw source.
        # Mermaid v10's run() reads via innerHTML, so emit `>` as a raw
        # char (not `&gt;`) — otherwise `->>` arrows fail to parse.
        # Still escape `<` and `&` to keep the surrounding HTML valid.
        inner = re.sub(r"<[^>]+>", "", m.group(1))
        raw = _unesc(inner)
        safe = raw.replace("&", "&amp;").replace("<", "&lt;")
        return f'<pre class="mermaid">{safe}</pre>'

    new_html = _MERMAID_BLOCK_RE.sub(replace, html)
    if new_html == html:
        return html

    # Widen the meta-CSP for this page so the dynamic import resolves.
    def patch_csp(tag_match: re.Match[str]) -> str:
        tag = tag_match.group(0)

        def patch_content(c: re.Match[str]) -> str:
            policy = c.group(3)
            new_policy = policy
            # Widen script-src so the Mermaid lib can be imported from jsDelivr.
            if "cdn.jsdelivr.net" not in new_policy:
                new_policy = re.sub(
                    r"(script-src)(\s+)",
                    r"\1 https://cdn.jsdelivr.net\2",
                    new_policy,
                    count=1,
                )
            # Widen style-src so Mermaid can set inline styles on the SVG it
            # generates (arrowhead fills, sequence-number colors, message-line
            # strokes are all set via element.style.X). Without 'unsafe-inline'
            # in style-src for these pages, those assignments are silently
            # blocked by CSP and the diagram renders with browser default fill
            # (black filled paths = teardrop blobs).
            #
            # CSP3 spec gotcha: 'unsafe-inline' is IGNORED if any hash or nonce
            # is also present in the same source list. So we strip the existing
            # 'sha256-…' tokens from the style-src clause when we add
            # 'unsafe-inline', otherwise the browser silently drops it.
            if "'unsafe-inline'" not in new_policy:
                # Match the whole style-src clause (up to the next ; or end of value)
                def widen_style_src(m: re.Match[str]) -> str:
                    clause = m.group(0)
                    # Drop any 'sha256-…' or 'sha384-…' / 'sha512-…' hashes
                    clause = re.sub(r"\s*'sha(?:256|384|512)-[A-Za-z0-9+/=]+'", "", clause)
                    # Insert 'unsafe-inline' right after the directive name
                    clause = re.sub(
                        r"^(style-src)(\s+)",
                        r"\1 'unsafe-inline'\2",
                        clause,
                        count=1,
                    )
                    return clause

                new_policy = re.sub(
                    r"style-src[^;]*",
                    widen_style_src,
                    new_policy,
                    count=1,
                )
            if new_policy == policy:
                return c.group(0)
            return c.group(1) + c.group(2) + new_policy + c.group(4)

        return _content_attr_re.sub(patch_content, tag, count=1)

    return _csp_tag_re.sub(patch_csp, new_html, count=1)


SPECULATION_RULES_BLOCK = (
    '<script type="speculationrules">'
    '{"prerender":[{'
    '"where":{"and":['
    '{"href_matches":"/*"},'
    '{"not":{"href_matches":"/_csp/*"}},'
    '{"not":{"href_matches":"/*.xml"}},'
    '{"not":{"href_matches":"/*.json"}},'
    '{"not":{"href_matches":"/*.txt"}},'
    '{"not":{"href_matches":"/*.pdf"}},'
    '{"not":{"href_matches":"/manifest.json"}},'
    '{"not":{"href_matches":"/sw.js"}},'
    '{"not":{"href_matches":"/contact/*"}},'
    '{"not":{"href_matches":"/fr/contact/*"}}'
    "]},"
    '"eagerness":"moderate"'
    "}]}"
    "</script>"
)


def inject_speculation_rules(html: str) -> str:
    """Inject the Speculation Rules API block before </head>. Idempotent."""
    if 'type="speculationrules"' in html:
        return html
    return _HEAD_END_RE.sub(SPECULATION_RULES_BLOCK + "</head>", html, count=1)
