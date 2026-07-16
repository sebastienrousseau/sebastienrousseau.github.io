"""Redirect-page conversion: /papers -> /research (EN + every locale fork).

The publications hub moved to /research in the 5-item nav re-architecture
(Suite / Research / Case studies / Resources / About). /research is the
canonical hub; the legacy /papers URLs stay rendered so old inbound links,
bookmarks and the URL inventory keep resolving, but each is converted into
a true redirect page:

* ``<meta http-equiv="refresh" content="0; url=<target>">`` injected into
  ``<head>`` -- Google treats an instant meta refresh as a permanent
  redirect signal.
* ``<link rel="canonical">`` and ``og:url`` swapped to the redirect target
  (the canonical consolidation signal).
* The hreflang alternate cluster is stripped: redirect pages are not
  content, and the /research cluster owns the hreflang pairing.
* The URL is dropped from every sitemap: non-canonical URLs do not belong
  in a sitemap.

Locale forks get equivalent treatment via the per-locale slug maps:
``/<lang>/<papers-slug>/`` redirects to ``/<lang>/<research-slug>/`` (for
example ``/fr/publications/`` -> ``/fr/recherche/``).

Must run AFTER the per-page pipeline (normalize_canonical would otherwise
rewrite the canonical back to self) and AFTER the sitemap augment pass in
``_finalize_build`` (which would otherwise re-add the purged entries).
Idempotent: re-running on already-converted pages is a no-op.

The redirect-page semantics are codified by two validation gates:
``test_canonical_consistency`` (redirect pages must canonicalise to their
refresh target, everything else to itself) and
``test_sitemap_completeness`` (redirect pages are exempt from the
every-page-in-sitemap rule).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import _lang_registry as _lr
from postbuild_lib._i18n import _all_active_non_en_langs
from postbuild_lib.article_furniture import _BASE_URL, PUBLIC

# EN slug pairs: source page -> canonical target. Locale forks are derived
# from the per-locale slug maps at run time.
REDIRECTS: dict[str, str] = {"papers": "research"}

_META_REFRESH_RE = re.compile(r'<meta\s+http-equiv="refresh"[^>]*>', re.IGNORECASE)
_CANONICAL_RE = re.compile(
    r'(<link\b[^>]*\brel=["\']?canonical["\']?[^>]*\bhref=["\']?)([^"\'\s>]+)(["\']?[^>]*>)',
    re.IGNORECASE,
)
_OG_URL_RE = re.compile(
    r'(<meta\b[^>]*\bproperty=["\']?og:url["\']?[^>]*\bcontent=["\']?)([^"\'\s>]+)(["\']?[^>]*>)',
    re.IGNORECASE,
)
_HREFLANG_LINK_RE = re.compile(
    r'\s*<link\b(?=[^>]*\brel=["\']?alternate["\']?)(?=[^>]*\bhreflang=)[^>]*/?>',
    re.IGNORECASE,
)
_HEAD_OPEN_RE = re.compile(r"<head\b[^>]*>", re.IGNORECASE)
_URL_BLOCK_RE = re.compile(r"<url>[\s\S]*?</url>")
_LOC_RE = re.compile(r"<loc>([^<]+)</loc>")


def _redirect_pairs(public: Path) -> list[tuple[Path, str]]:
    """Return ``[(source index.html, absolute target URL), ...]`` for EN +
    every active non-EN locale fork that exists on disk."""
    pairs: list[tuple[Path, str]] = []
    for en_src, en_dst in REDIRECTS.items():
        pairs.append((public / en_src / "index.html", f"{_BASE_URL}/{en_dst}/"))
        for code in _all_active_non_en_langs():
            statics = _lr.load_slugs(code).get("static", {})
            src_slug = statics.get(en_src, en_src)
            dst_slug = statics.get(en_dst, en_dst)
            pairs.append(
                (
                    public / code / src_slug / "index.html",
                    f"{_BASE_URL}/{code}/{dst_slug}/",
                )
            )
    return [(p, t) for p, t in pairs if p.is_file()]


def _convert_page(page: Path, target: str) -> bool:
    """Rewrite one rendered page into a redirect page. Returns True when
    the file changed."""
    html = page.read_text(encoding="utf-8")
    out = html
    # 1. Meta refresh in <head> (idempotent).
    tag = f'<meta http-equiv="refresh" content="0; url={target}" />'
    if _META_REFRESH_RE.search(out):
        out = _META_REFRESH_RE.sub(tag, out, count=1)
    else:
        m = _HEAD_OPEN_RE.search(out)
        if not m:  # defensive: malformed page, leave untouched
            return False
        out = out[: m.end()] + tag + out[m.end() :]
    # 2. Canonical + og:url -> target.
    out = _CANONICAL_RE.sub(lambda m: m.group(1) + target + m.group(3), out, count=1)
    out = _OG_URL_RE.sub(lambda m: m.group(1) + target + m.group(3), out, count=1)
    # 3. Strip the hreflang cluster.
    out = _HREFLANG_LINK_RE.sub("", out)
    if out != html:
        page.write_text(out, encoding="utf-8")
        return True
    return False


def _purge_from_sitemaps(public: Path, redirect_urls: set[str]) -> int:
    """Remove ``<url>`` blocks whose ``<loc>`` is a redirect source from
    every sitemap under ``public/``. Returns the number of entries
    removed."""

    def _norm(u: str) -> str:
        u = u.strip()
        if u.endswith("/index.html"):
            u = u[: -len("index.html")]
        return u.rstrip("/")

    wanted_gone = {_norm(u) for u in redirect_urls}
    removed = 0
    for sm in public.glob("sitemap*.xml"):
        text = sm.read_text(encoding="utf-8")

        def repl(m: re.Match[str]) -> str:
            nonlocal removed
            loc = _LOC_RE.search(m.group(0))
            if loc and _norm(loc.group(1)) in wanted_gone:
                removed += 1
                return ""
            return m.group(0)

        new = _URL_BLOCK_RE.sub(repl, text)
        if new != text:
            sm.write_text(new, encoding="utf-8")
    return removed


def apply_redirect_pages(public: Path = PUBLIC) -> tuple[int, int]:
    """Convert every configured legacy URL (EN + locale forks) into a
    redirect page and purge them from the sitemaps. Returns
    ``(pages_converted, sitemap_entries_removed)``."""
    pairs = _redirect_pairs(public)
    converted = sum(1 for page, target in pairs if _convert_page(page, target))
    sources: set[str] = set()
    for page, _target in pairs:
        rel = page.relative_to(public).as_posix()
        sources.add(f"{_BASE_URL}/{rel}")
    purged = _purge_from_sitemaps(public, sources)
    return converted, purged
