# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""One fluid type scale across every layout.

The shared stylesheet in ``_layouts/index.html`` defines one size token
per typographic role (``--fs-micro`` to ``--fs-display``), and the page
CSS that ``gen_layouts.py`` appends for /speaking/, /iso20022-mcp/,
/trust/, /contact/ and /playlists/ uses the same tokens. Before the
scale, the H1 on eleven key pages took eight different sizes at 1440 px.
These checks keep it to one scale:

1. Every role selector below sets its ``font-size`` to its token, in
   every layout that carries it.
2. No rule sets a raw ``font-size`` at all, outside the chrome (nav,
   footer, code, pseudo-elements, print) and relative ``em``/``%`` sizes.
3. Inside ``clamp()``, ``calc()``, ``min()`` and ``max()`` an operator has
   exactly one space either side: ssg's ``minify_css`` drops the space
   after a run of spaces, which leaves ``1rem+ 1vw`` and voids the value.
4. Every ``--fs-*`` token has ``rem`` bounds, so it follows the reader's
   default font size.

The runtime half of the check, which renders the pages and measures
every heading, paragraph and eyebrow, is
``.github/ci-tools/visual/type-scale.mjs``.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
LAYOUTS = sorted((ROOT / "_layouts").glob("*.html"))

# Role selectors as written in the stylesheet, by token.
ROLES: dict[str, tuple[str, ...]] = {
    "display": (
        ".ap-hero h1",
        ".cs-hero h1",
        ".trust-page h1",
        ".story-hero-inner h1",
        ".pl-topper h1",
    ),
    "h1": (
        ".feat-hero .feat-headline.center",
        ".speaking-page h1",
        ".iso20022-mcp-page .spk-hero h1",
        "header.tag-landing-hero h1",
        "body:has(.report-article) .ap-hero h1",
        ".newsroom-section-head h1",
    ),
    "h2": (
        ".feat-headline",
        ".feat-card-title",
        ".offer-headline",
        ".narrative-section .narrative-head",
        ".story-cta .story-title",
        ".speaking-page h2",
        ".iso20022-mcp-page .spk-head h2",
        ".trust-page h2",
        ".newsroom-section-head h2",
        ".topic-pillar-head h2",
        ".cs-stage h2:not(:where(.cs-card-title))",
        ".qa-headline",
    ),
    "h2-prose": (".report-article h2", "main.content > .wrap > h2", ".related-heading"),
    "h3": (
        ".speaking-page h3",
        ".trust-page h3",
        ".trust-page .tr-prev-body h3",
        ".cs-card-title",
        ".book-title",
    ),
    "h4": (
        ".offer-card h3",
        ".newsroom-card-body h3",
        ".iso20022-mcp-page .mcp-sec-cell h3",
        ".iso20022-mcp-page .mcp-step h3",
        ".iso20022-mcp-page .mcp-client h3",
        ".iso20022-mcp-page .mcp-prompt h3",
        ".story-cta .story-card-title",
        ".qa-item > summary",
        ".report-article h3",
        "article.tag-landing-card h2",
        ".speaking-page .spk-path h3",
        ".article-toc h2",
    ),
    "lead": (
        ".ap-hero .sub",
        ".feat-sub",
        ".speaking-page .spk-lede",
        ".trust-page .tr-lede",
        ".trust-page .tr-col-head .tr-lede",
        ".cs-hero .cs-deck",
        ".topic-pillar-lede",
        ".newsroom-section-head .newsroom-lede",
        ".topic-lede",
    ),
    "prose": (
        ".report-article p",
        ".report-article li",
        "main.content > .wrap > p",
        "main.content > .wrap > :is(ul, ol) > li",
        ".narrative-section .narrative-body",
    ),
    "body": (
        ".cs-card-excerpt",
        ".book-excerpt",
        ".feat-card p:not(:where(.feat-eyebrow))",
        ".cs-stage p:not(:where(.cs-card-kicker,.cs-stage-no))",
    ),
    "small": (
        ".offer-card p",
        ".newsroom-card-body .newsroom-excerpt",
        ".speaking-page .spk-path p",
        ".speaking-page .spk-desc",
        ".trust-page .tr-card p",
        ".trust-page .tr-note",
        ".iso20022-mcp-page .mcp-step p",
        ".iso20022-mcp-page .mcp-note",
        ".author-card-body",
    ),
    "ui": (
        ".pill",
        ".offer-card .offer-link",
        ".speaking-page .spk-btn",
        ".article-cta-actions .btn-primary",
        ".article-cta-actions .btn-ghost",
    ),
    "meta": (
        ".newsroom-meta",
        ".book-meta",
        ".proof-note",
        ".read-as-summary",
        ".hero-clock-caption",
        ".artefact-foot",
    ),
    "micro": (
        ".eyebrow",
        ".feat-eyebrow",
        ".offer-eyebrow",
        ".newsroom-eyebrow",
        ".newsroom-kicker",
        ".narrative-section .narrative-eyebrow",
        ".book-eyebrow",
        ".cs-hero .cs-kicker",
        ".cs-card-kicker",
        ".cs-stage-no",
        ".speaking-page .spk-eyebrow",
        ".speaking-page .spk-lbl",
        ".trust-page .tr-kicker",
        ".newsroom-tldr-label",
        ".artefact-badge",
        ".finale-ai-kicker",
        ".contact-aside-title",
    ),
    "stat": (".speaking-page .spk-num", ".proof-rail .kpi-cell-value"),
}

# Raw sizes are allowed only in the chrome and for relative units.
_EXEMPT_SELECTOR = re.compile(
    r"\.ap-(nav|menu|brand|burger|lang|cta-mini|search|foot|newsletter)|#mode-toggle|\.theme-icon"
    r"|(^|\s)pre\b|\bcode\b|\.mcp-term|::?(before|after)|^html$|^small,sub,sup$|-media$|\.error-eyebrow"
)
_EXEMPT_VALUE = re.compile(r"^(0|inherit)$|\d(em|%)$|^var\(--(fs|gr)-")
_STYLE = re.compile(r"<style>\n(.*?)\n\s*</style>", re.DOTALL)
_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)
_FONT_SIZE = re.compile(r"(?<![-\w])font-size\s*:\s*([^;}]*)")
_MATH = re.compile(r"\b(?:clamp|calc|min|max)\((?:[^()]|\([^()]*\))*\)")


def _shared_css(path: Path) -> str:
    match = _STYLE.search(path.read_text(encoding="utf-8"))
    assert match, f"{path.name}: no shared <style> block"
    return _COMMENT.sub("", match.group(1))


def _rules(css: str, context: str = ""):
    """Yield (context, selector, body) for every style rule, at any depth."""
    pos = 0
    while (open_at := css.find("{", pos)) != -1:
        prelude = css[pos:open_at].split(";")[-1].strip()
        depth, end = 1, open_at + 1
        while depth:
            depth += {"{": 1, "}": -1}.get(css[end], 0)
            end += 1
        inner = css[open_at + 1 : end - 1]
        if prelude.startswith("@"):
            if "{" in inner:
                yield from _rules(inner, prelude)
        else:
            yield context, re.sub(r"\s+", " ", prelude), inner
        pos = end


def _selectors(prelude: str) -> list[str]:
    parts, depth, current = [], 0, ""
    for char in prelude:
        depth += {"(": 1, ")": -1, "[": 1, "]": -1}.get(char, 0)
        if char == "," and depth == 0:
            parts.append(current.strip())
            current = ""
        else:
            current += char
    return [*parts, current.strip()]


def _sizes(css: str):
    """Yield (context, selector, font-size value) per selector."""
    for context, prelude, body in _rules(css):
        for value in _FONT_SIZE.findall(body):
            for selector in _selectors(prelude):
                yield context, selector, value.replace("!important", "").strip()


@pytest.mark.parametrize("layout", LAYOUTS, ids=lambda p: p.name)
def test_role_selectors_use_their_token(layout: Path) -> None:
    sizes = [(s, v) for c, s, v in _sizes(_shared_css(layout)) if "print" not in c]
    wrong = [
        f"{selector} {{font-size:{value}}} (want var(--fs-{token}))"
        for token, selectors in ROLES.items()
        for selector, value in sizes
        if selector in selectors and value != f"var(--fs-{token})"
    ]
    assert not wrong, f"{layout.name}:\n  " + "\n  ".join(wrong)


def test_every_role_selector_exists() -> None:
    present = {s for layout in LAYOUTS for _c, s, _v in _sizes(_shared_css(layout))}
    missing = [s for selectors in ROLES.values() for s in selectors if s not in present]
    assert not missing, f"role selectors no layout sets a font-size on: {missing}"


# Context rules (main.content is also .ap-section) that outranked every role class inside
# <main> while they set a size: card titles, ledes and eyebrows all took the
# prose size. Prose sizes live on the prose selectors in ROLES instead.
_BROAD_PROSE = (
    "main.content h2",
    "main.content h3",
    "main.content p",
    "main.content li",
    "main.content :is(h2)",
    "main.content :is(h3)",
    "main.content :is(p,li)",
    ".ap-section h2",
)


def test_broad_main_rules_set_no_size() -> None:
    css = _shared_css(ROOT / "_layouts" / "index.html")
    sized = sorted({s for _c, s, _v in _sizes(css) if s in _BROAD_PROSE})
    assert not sized, f"these outrank the role selectors inside <main>: {sized}"


@pytest.mark.parametrize("layout", LAYOUTS, ids=lambda p: p.name)
def test_no_raw_font_size(layout: Path) -> None:
    raw = [
        f"{selector} {{font-size:{value}}}"
        for context, selector, value in _sizes(_shared_css(layout))
        if "print" not in context
        and "layer" not in context
        and not _EXEMPT_SELECTOR.search(selector)
        and not _EXEMPT_VALUE.search(value)
    ]
    assert not raw, f"{layout.name}: font-size off the type scale:\n  " + "\n  ".join(raw)


def _bad_math(css: str) -> list[str]:
    """Math expressions with a run of spaces, or a glued operator, around +-*/."""
    spacing = re.compile(r"\s{2,}[-+*/]\s|\s[-+*/]\s{2,}|[\w%)][+-] [\d.(]")
    return [expr for expr in _MATH.findall(css) if spacing.search(expr)]


@pytest.mark.parametrize("layout", LAYOUTS, ids=lambda p: p.name)
def test_css_math_has_single_spaces(layout: Path) -> None:
    bad = _bad_math(_shared_css(layout))
    assert not bad, f"{layout.name}: operator spacing ssg's minify_css breaks: {bad}"


def test_math_spacing_check_catches_runs_and_glue() -> None:
    assert _bad_math("a{b:clamp(1rem, 1rem  + 1vw, 2rem)}")
    assert _bad_math("a{b:clamp(1rem, 1rem+ 1vw, 2rem)}")
    assert _bad_math("a{b:calc(100% -  2px)}")
    assert not _bad_math("a{b:clamp(1rem, 1rem + 1vw, 2rem);c:calc(var(--x) * 2)}")


def test_tokens_have_rem_bounds() -> None:
    css = _shared_css(ROOT / "_layouts" / "index.html")
    tokens = re.findall(r"--fs-([\w-]+):\s*clamp\(([^,]+),[^,]+,([^)]+)\)", css)
    names = {name for name, _lo, _hi in tokens}
    assert {"micro", "body", "h1", "display", "stat"} <= names
    bad = [
        name
        for name, lo, hi in tokens
        if not (lo.strip().endswith("rem") and hi.strip().endswith("rem"))
    ]
    assert not bad, f"--fs-* tokens with non-rem bounds: {bad}"


def test_rule_parser_sees_nested_rules() -> None:
    css = ".a{font-size:var(--fs-h1)}@media (min-width:1px){.b,.c{font-size:2px}}"
    assert list(_sizes(css)) == [
        ("", ".a", "var(--fs-h1)"),
        ("@media (min-width:1px)", ".b", "2px"),
        ("@media (min-width:1px)", ".c", "2px"),
    ]
