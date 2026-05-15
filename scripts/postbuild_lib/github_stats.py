"""GitHub repo-stats badge injection.

Reads ``_data/gh-stats.json`` (refreshed nightly by the
``refresh-gh-stats`` workflow) and injects star / fork / licence /
last-commit pill badges into every project + newsroom card that
resolves to a tracked repo. Build-time injection — zero JS, zero
CLS, no rate-limit risk.

Lookup heuristics (in order):
    1. Any github.com/sebastienrousseau/<slug> href in the card.
    2. The homepage URL recorded in the stats payload.
    3. The card's <h3> text matching the repo name.

Badge labels + relative-time strings are localised per page via
``_HTML_LANG_DETECT_RE``.
"""
from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path

_GH_STATS_PATH = Path("_data/gh-stats.json")

_HTML_LANG_DETECT_RE = re.compile(r'<html\b[^>]*\blang="([^"]+)"', re.IGNORECASE)

_GH_CARD_RE = re.compile(
    r'(<article class=(?:"(?:newsroom-card|proj-card)[^"]*"|(?:newsroom-card|proj-card))[^>]*>)'
    r'([\s\S]+?)(</article>)',
)
_GH_REPO_HREF_RE = re.compile(
    r'href=["\']?https?://github\.com/(sebastienrousseau/[a-zA-Z0-9._-]+)/?["\']?',
)
_GH_HREF_RE = re.compile(r'href=(?:"([^"]+)"|([^\s>]+))')

_RELTIME: dict[str, dict[str, str]] = {
    # Format strings keyed by lang. ``%d`` is the count; ``%s`` for the
    # "an" plural in FR is appended manually because Python's f-strings
    # don't allow conditional plurals inline.
    "en": {"s": "{n}s ago", "m": "{n}m ago", "h": "{n}h ago", "d": "{n}d ago", "w": "{n}w ago", "mo": "{n}mo ago", "y": "{n}y ago"},
    "fr": {"s": "il y a {n} s", "m": "il y a {n} min", "h": "il y a {n} h", "d": "il y a {n} j", "w": "il y a {n} sem.", "mo": "il y a {n} mois", "y": "il y a {n} an"},
    "de": {"s": "vor {n} s", "m": "vor {n} min", "h": "vor {n} Std.", "d": "vor {n} T.", "w": "vor {n} Wo.", "mo": "vor {n} Mon.", "y": "vor {n} J."},
}

_GH_BADGE_STRINGS: dict[str, dict[str, str]] = {
    "en": {"last": "last commit", "stars": "stars", "forks": "forks", "repoStats": "Repository stats"},
    "fr": {"last": "dernier commit", "stars": "étoiles", "forks": "forks", "repoStats": "Statistiques du dépôt"},
    "de": {"last": "letzter Commit", "stars": "Sterne", "forks": "Forks", "repoStats": "Repository-Statistiken"},
}


def _detect_page_lang(html: str) -> str:
    """``<html lang="xx-YY">`` → ``xx``. Defaults to ``en`` if absent."""
    m = _HTML_LANG_DETECT_RE.search(html)
    if not m:
        return "en"
    return m.group(1).lower().split("-", 1)[0]


def gh_stats_index() -> dict[str, dict]:
    """Load ``_data/gh-stats.json`` into a slug-keyed dict. Returns
    empty dict if the file is missing or invalid JSON."""
    if not _GH_STATS_PATH.is_file():
        return {}
    try:
        data = json.loads(_GH_STATS_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return {entry["slug"]: entry for entry in data.get("repos", []) if "slug" in entry}


def _relative_time(iso_ts: str, fr: bool = False, lang: str | None = None) -> str:
    """Render an ISO-8601 timestamp as a localised 'N units ago' label."""
    if not iso_ts:
        return ""
    try:
        ts = datetime.fromisoformat(iso_ts.replace("Z", "+00:00"))
    except ValueError:
        return ""
    code = lang if lang else ("fr" if fr else "en")
    t = _RELTIME.get(code, _RELTIME["en"])
    delta = (datetime.now(tz=UTC) - ts).total_seconds()
    if delta < 0:
        delta = 0
    if delta < 60:
        n, key = int(delta), "s"
    elif delta < 3600:
        n, key = int(delta // 60), "m"
    elif delta < 86400:
        n, key = int(delta // 3600), "h"
    elif delta < 604800:
        n, key = int(delta // 86400), "d"
    elif delta < 2629800:
        n, key = int(delta // 604800), "w"
    elif delta < 31557600:
        n, key = int(delta // 2629800), "mo"
    else:
        n, key = int(delta // 31557600), "y"
    out = t[key].format(n=n)
    if code == "fr" and key == "y" and n > 1:
        out += "s"
    return out


def _format_count(n: int) -> str:
    """1234 -> 1.2k, 1234567 -> 1.2M."""
    if n >= 1000000:
        return f"{n / 1000000:.1f}M".replace(".0M", "M")
    if n >= 1000:
        return f"{n / 1000:.1f}k".replace(".0k", "k")
    return str(n)


def _render_gh_badges(info: dict, lang: str = "en") -> str:
    stars = info.get("stars", 0)
    forks = info.get("forks", 0)
    license_id = info.get("license", "")
    pushed = info.get("pushed_at", "")
    pushed_rel = _relative_time(pushed, lang=lang)
    s = _GH_BADGE_STRINGS.get(lang, _GH_BADGE_STRINGS["en"])
    label_last = s["last"]
    aria_stars = f"{stars} {s['stars']}" if stars else ""
    aria_forks = f"{forks} {s['forks']}" if forks else ""
    parts: list[str] = []
    if stars:
        parts.append(
            f'<span class="gh-stat gh-stars" aria-label="{aria_stars}">'
            f'<span class="gh-ico" aria-hidden="true">★</span>'
            f'<span class="gh-num">{_format_count(stars)}</span></span>'
        )
    if forks:
        parts.append(
            f'<span class="gh-stat gh-forks" aria-label="{aria_forks}">'
            f'<span class="gh-ico" aria-hidden="true">⑂</span>'
            f'<span class="gh-num">{_format_count(forks)}</span></span>'
        )
    if license_id and license_id not in ("NOASSERTION", "", "OTHER"):
        parts.append(
            f'<span class="gh-stat gh-license">'
            f'<span class="gh-ico" aria-hidden="true">⚖</span>'
            f'<span class="gh-txt">{license_id}</span></span>'
        )
    if pushed_rel:
        parts.append(
            f'<span class="gh-stat gh-pushed" title="{pushed[:10]}">'
            f'<span class="gh-ico" aria-hidden="true">⏱</span>'
            f'<span class="gh-txt">{label_last} {pushed_rel}</span></span>'
        )
    if not parts:
        return ""
    aria = s["repoStats"]
    return f'<p class="gh-stats-row" aria-label="{aria}">{"".join(parts)}</p>'


def _normalise_url(u: str) -> str:
    """Normalise a URL for equality: drop scheme, www., trailing slash, lower-case."""
    u = u.strip().lower()
    u = re.sub(r'^https?://', '', u)
    u = re.sub(r'^www\.', '', u)
    return u.rstrip('/')


def _gh_lookup(inner: str, stats_index: dict[str, dict]) -> dict | None:
    """Resolve a card to its repo entry. Lookup precedence:

    1. Any ``github.com/sebastienrousseau/<slug>`` href in the card.
    2. The homepage URL recorded in the stats payload (scheme / www /
       trailing-slash insensitive).
    3. The card's <h3> text matching the repo name (case-insensitive).
    """
    if not stats_index:
        return None
    m = _GH_REPO_HREF_RE.search(inner)
    if m and m.group(1) in stats_index:
        return stats_index[m.group(1)]
    homepage_idx = {
        _normalise_url(e.get("homepage") or ""): e
        for e in stats_index.values()
        if e.get("homepage")
    }
    name_idx = {(e.get("name") or "").lower(): e for e in stats_index.values()}
    for hm in _GH_HREF_RE.finditer(inner):
        href = (hm.group(1) or hm.group(2) or "").strip()
        if not href.startswith(("http://", "https://")):
            continue
        key = _normalise_url(href)
        if key in homepage_idx:
            return homepage_idx[key]
    h3 = re.search(r'<h3[^>]*>\s*<a[^>]*>([^<]+)</a>', inner)
    if h3:
        title = h3.group(1).strip().lower()
        if title in name_idx:
            return name_idx[title]
    return None


def inject_github_stats(html: str, stats_index: dict[str, dict]) -> str:
    """Inject star / fork / last-commit badges into every newsroom-card
    on the page whose first GitHub anchor or project homepage URL
    matches a tracked repo."""
    if not stats_index or 'newsroom-card' not in html:
        return html
    page_lang = _detect_page_lang(html)

    def patch(m: re.Match[str]) -> str:
        open_tag, inner, close_tag = m.group(1), m.group(2), m.group(3)
        if 'class="gh-stats-row"' in inner:
            return m.group(0)
        info = _gh_lookup(inner, stats_index)
        if not info:
            return m.group(0)
        badges = _render_gh_badges(info, lang=page_lang)
        if not badges:
            return m.group(0)
        inner_new = re.sub(
            r'(</div>\s*)$',
            badges + r'\1',
            inner,
            count=1,
        )
        if inner_new == inner:
            inner_new = inner + badges
        return open_tag + inner_new + close_tag

    return _GH_CARD_RE.sub(patch, html)
