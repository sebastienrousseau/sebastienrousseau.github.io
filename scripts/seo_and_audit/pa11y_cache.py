"""Hash-cache layer in front of pa11y-ci.

The full WCAG2AAA sweep of 1990 built pages takes ~37 min on a GitHub-
hosted runner. Almost every daily PR touches <30 pages, so re-sweeping
the other 1960 every run is pure waste.

This module gives the accessibility CI job a content-addressed cache:

  * ``pre``  — read ``public/`` + the existing cache, decide which URLs
    actually need a pa11y run, and write the ``.pa11yci`` config for
    just those URLs.
  * ``post`` — given a record of which delta URLs passed, update the
    cache with their hashes so the next run can skip them.

The cache JSON shape:

    {
      "fingerprint": {
        "pa11y_version":     "3.1.0",
        "chromium_version":  "130.0.6723.69",
        "config_hash":       "<sha256 of the .pa11yci JSON sans urls list>",
        "wcag_standard":     "WCAG2AAA"
      },
      "pages": {
        "<relpath/index.html>": {
          "hash":      "<sha256 of rendered HTML>",
          "status":    "pass",
          "checked":   "2026-05-21T11:00:00Z"
        },
        ...
      }
    }

A page is cache-hit only when ALL of:

  * the page's content hash matches the stored hash, AND
  * the stored fingerprint matches the *current* fingerprint
    (pa11y version, Chromium version, config hash, standard).

Any fingerprint change forces a full re-sweep, which is the right
behaviour: a Chromium upgrade can surface new violations on previously-
passing pages, and a ``.pa11yci`` config change (e.g. a different
``hideElements`` selector) means we're checking a different surface.

Pure functions over filesystem paths + JSON dicts; no global state.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

CACHE_VERSION = 3


# Patterns matching the transient build artefacts that change every
# build but are functionally identical from pa11y's perspective:
# pa11y evaluates the rendered DOM for WCAG violations, so swapping
# one SRI hash for another or rotating a fingerprinted asset URL has
# no effect on accessibility. Stripping these before SHA-256 means a
# pure layout / CSS / minifier change (which churns every page's
# <head>) no longer busts the cache for unchanged-semantic pages.
#
# Each entry is (compiled_pattern, replacement_bytes). Patterns are
# byte-level so we can stream-normalise without UTF-8 decoding the
# whole page.
_NORMALISERS: list[tuple[re.Pattern[bytes], bytes]] = [
    # Fingerprinted asset URLs: ``main.799e2fd8.js`` → ``main.js``.
    # The fingerprint encodes file content; same content = same hash
    # in spec but the build path embeds a fresh 8-hex slug each run.
    (re.compile(rb"([A-Za-z0-9_-]+)\.[0-9a-f]{8}\.(js|css|mjs)"), rb"\1.\2"),
    # CSP-bundled stylesheets/scripts where the hash IS the filename
    # (no name prefix), e.g. ``_csp/97f63c950cabc48b.css``. The SSG's
    # CSP plugin emits these per-build; identical bundled content
    # still produces a stable hash, but a layout-touching PR rotates
    # which bundle is referenced from every page's <head>. Without
    # this rule, the cache would miss across the whole site for any
    # CSS-only edit.
    (re.compile(rb"_csp/[0-9a-f]{16,}\.(css|js|mjs)"), rb"_csp/X.\1"),
    # SRI integrity attributes — same hash, same SRI. Stripping the
    # value entirely is safe because we already gate on the asset URL
    # above; if the JS content actually changed, the URL hash above
    # will diverge.
    (re.compile(rb'integrity="[^"]*"'), b'integrity=""'),
    (re.compile(rb"integrity='[^']*'"), b"integrity=''"),
    # CSP ``'sha256-<base64>'`` script/style hashes embedded in the
    # Content-Security-Policy meta. Same rationale as SRI.
    (re.compile(rb"'sha256-[A-Za-z0-9+/=]{20,}'"), b"'sha256-X'"),
    # RSS/Atom feed link timestamps + sitemap lastmod fields, if they
    # ever leak into <link>s. Keep this conservative; only strip the
    # common ``?v=YYYYMMDD`` / ``?v=<timestamp>`` cache-busters.
    (re.compile(rb"\?v=[0-9]{8,14}"), b"?v=X"),
]


def _normalise_html(blob: bytes) -> bytes:
    """Strip the transient build artefacts from a page's bytes before
    fingerprinting. See ``_NORMALISERS`` for the patterns + rationale."""
    for pattern, replacement in _NORMALISERS:
        blob = pattern.sub(replacement, blob)
    return blob


def compute_page_hash(path: Path) -> str:
    """SHA-256 of the rendered HTML *after* normalising transient build
    artefacts (fingerprinted asset URLs, SRI integrity values, CSP
    sha256 hashes, ``?v=`` cache busters). Semantic / a11y-relevant
    content drives the hash; the SSG's per-build asset churn does not."""
    blob = path.read_bytes()
    blob = _normalise_html(blob)
    return hashlib.sha256(blob).hexdigest()


def compute_config_hash(config: dict[str, Any]) -> str:
    """Hash the pa11y config sans the URL list. The URL list changes
    every run (different cache state), but the *settings* — standard,
    timeout, hideElements, chromeLaunchConfig — are what actually
    determine whether the cached pass is still valid."""
    sans_urls = {k: v for k, v in config.items() if k != "urls"}
    payload = json.dumps(sans_urls, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def detect_pa11y_version(pa11y_ci_bin: str = "pa11y-ci") -> str:
    """Read pa11y-ci's own ``--version`` output. CI installs a pinned
    major (^3) but we want the exact patch version in the fingerprint."""
    try:
        out = subprocess.run(
            [pa11y_ci_bin, "--version"],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        ).stdout.strip()
        return out or "unknown"
    except (FileNotFoundError, subprocess.SubprocessError):
        return "unknown"


_CHROMIUM_VERSION_RE = re.compile(r"(\d+\.\d+\.\d+\.\d+)")


def detect_chromium_version() -> str:
    """Probe the Chromium binary that Puppeteer ships with pa11y. The
    CI runner has /usr/bin/chromium or /usr/bin/chromium-browser; locally
    macOS users typically hit a Puppeteer-bundled copy. Returns
    "unknown" if no candidate responds — degrading to a full re-sweep
    on the next run rather than a stale-cache hit."""
    candidates = [
        "/usr/bin/chromium-browser",
        "/usr/bin/chromium",
        "/usr/bin/google-chrome",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ]
    for bin_path in candidates:
        if not Path(bin_path).is_file():
            continue
        try:
            out = subprocess.run(
                [bin_path, "--version"],
                check=True,
                capture_output=True,
                text=True,
                timeout=10,
            ).stdout.strip()
            m = _CHROMIUM_VERSION_RE.search(out)
            if m:
                return m.group(1)
        except (FileNotFoundError, subprocess.SubprocessError):
            continue
    return "unknown"


def load_cache(cache_path: Path) -> dict[str, Any]:
    """Read an existing cache JSON, or return an empty skeleton."""
    if not cache_path.is_file():
        return {"version": CACHE_VERSION, "fingerprint": {}, "pages": {}}
    try:
        with cache_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if data.get("version") != CACHE_VERSION:
            # Schema bump — discard and start fresh.
            return {"version": CACHE_VERSION, "fingerprint": {}, "pages": {}}
        data.setdefault("fingerprint", {})
        data.setdefault("pages", {})
        return data
    except (OSError, json.JSONDecodeError):
        return {"version": CACHE_VERSION, "fingerprint": {}, "pages": {}}


def save_cache(cache_path: Path, cache: dict[str, Any]) -> None:
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(cache, sort_keys=True, indent=2)
    cache_path.write_text(payload, encoding="utf-8")


def fingerprint_matches(cache: dict[str, Any], current: dict[str, Any]) -> bool:
    """Cache-hits are only honoured when every fingerprint key matches.
    A single delta (Chromium upgrade, config change, pa11y bump) forces
    a full re-sweep."""
    stored = cache.get("fingerprint", {})
    keys = ("pa11y_version", "chromium_version", "config_hash", "wcag_standard")
    return all(stored.get(k) == current.get(k) for k in keys)


def page_is_spotify_iframe(html: str) -> bool:
    """The accessibility sweep already skips Spotify-iframe pages because
    Puppeteer races the iframe load. Replicated here so the cache layer
    skips the same set, keeping the URL count identical to the legacy
    behaviour for the first cache fill."""
    if "<iframe" not in html:
        return False
    # NOTE: this is page-content detection (does the page embed Spotify?),
    # not a security boundary — a bare-domain substring is exactly right and
    # must stay broad to keep the pa11y URL count identical to legacy. The
    # py/incomplete-url-substring-sanitization alert here is a false positive
    # (dismissed in code-scanning).
    return "open.spotify.com" in html or "scdn.co" in html


# Relative paths (POSIX) of pages whose content is generated boilerplate
# with no original editorial signal — running pa11y on them only
# duplicates checks already performed against the layout templates that
# generate them. Skipping them costs nothing and trims the sweep.
_ZERO_VALUE_RELPATHS: frozenset[str] = frozenset(
    {
        # Credit page for the Static Site Generator — single short
        # paragraph plus the standard site chrome. Whatever a11y
        # signal it carries is already exercised on every other page
        # in the site, so pa11y can skip it.
        "made-with-static-site-generator/index.html",
    }
)


# Instant client-side redirect stubs (<meta http-equiv="refresh"
# content="0; url=...">). Puppeteer follows the refresh immediately, so
# pa11y never evaluates the stub itself: it evaluates whatever the
# *target* serves at sweep time. For the /papers/ -> /research/ moves
# (29 pages incl. locales) the target is an absolute production URL, so
# a CI sweep of the freshly built tree ends up scoring the production
# 404 page ("Execution context was destroyed" / NaN-contrast failures
# across whichever shards drew a redirect stub). The stubs carry no
# editorial signal; the redirect targets are swept as their own pages.
_META_REFRESH_RE = re.compile(r'<meta\s+http-equiv="refresh"', re.IGNORECASE)


def page_is_redirect_stub(html: str) -> bool:
    """True when the page is a client-side redirect stub. Only the head
    slice is scanned so prose about meta refresh can never match."""
    end = html.find("</head>")
    head = html if end < 0 else html[:end]
    return bool(_META_REFRESH_RE.search(head))


def page_should_skip(html: str, rel: str) -> bool:
    """True when ``rel`` (the public/-relative path of an index.html)
    is on the explicit zero-value list, OR when the page embeds a
    Spotify iframe (Puppeteer races the load), OR when the page is an
    instant meta-refresh redirect stub (Puppeteer navigates away before
    pa11y can evaluate it). The cache layer treats all reasons
    identically: mark as ``skipped``, don't fingerprint, don't sweep."""
    if rel in _ZERO_VALUE_RELPATHS:
        return True
    if page_is_redirect_stub(html):
        return True
    return page_is_spotify_iframe(html)


def partition_pages(
    public_dir: Path,
    cache: dict[str, Any],
    current_fingerprint: dict[str, Any],
) -> tuple[list[tuple[Path, str]], list[tuple[Path, str]], list[str]]:
    """Walk public/ and partition pages into:

      * ``to_sweep`` — (path, current_hash) for pages that need a pa11y
        run. Either they aren't in the cache, the stored hash differs,
        or the fingerprint changed (forces full re-sweep).
      * ``cache_hits`` — (path, current_hash) for pages whose stored
        hash matches AND fingerprint matches. These get marked
        ``status="pass"`` without running pa11y.
      * ``skipped`` - relpaths the cache layer ignored: they embed a
        Spotify iframe (pa11y can't check them reliably), they are
        instant meta-refresh redirect stubs (Puppeteer navigates away
        and pa11y ends up scoring the redirect target), or they live on
        the explicit zero-value list (boilerplate credit pages whose
        a11y signal is already exercised by the layout).

    The function is pure-ish: it reads disk and the cache dict but
    mutates neither. The caller decides what to do with each list.
    """
    fp_match = fingerprint_matches(cache, current_fingerprint)
    pages_cache = cache.get("pages", {}) if fp_match else {}

    to_sweep: list[tuple[Path, str]] = []
    cache_hits: list[tuple[Path, str]] = []
    skipped: list[str] = []

    for path in sorted(public_dir.rglob("index.html")):
        rel = path.relative_to(public_dir).as_posix()
        try:
            html = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if page_should_skip(html, rel):
            skipped.append(rel)
            continue
        h = compute_page_hash(path)
        cached_entry = pages_cache.get(rel)
        if (
            fp_match
            and cached_entry
            and cached_entry.get("hash") == h
            and cached_entry.get("status") == "pass"
        ):
            cache_hits.append((path, h))
        else:
            to_sweep.append((path, h))

    return to_sweep, cache_hits, skipped


def build_pa11yci_config(urls: list[str], hide_elements: str) -> dict[str, Any]:
    """Mirror the inline config the accessibility job has used since
    2024. Kept here so a single source of truth feeds both the pa11yci
    JSON written to disk AND the config-hash used to detect config
    drift."""
    return {
        # Top-level pa11y-ci option (not a pa11y option), so it sits
        # outside ``defaults``. Default is 2; GitHub-hosted ubuntu-latest
        # has 4 vCPUs, so 4 parallel Chromium tabs roughly halves the
        # wall-clock on full cache misses without OOMing the runner.
        "concurrency": 4,
        "defaults": {
            "standard": "WCAG2AAA",
            "timeout": 20000,
            # Wait for the page to settle before pa11y starts evaluating.
            # Without this, late-firing navigation triggers (related-posts
            # prefetch, lazy-loaded enrich block, hreflang script) can race
            # the Puppeteer evaluate call and produce
            # "Execution context was destroyed, most likely because of a
            # navigation." See 2026-05-31 build-audit run 26711760568 for
            # the symptom — a single /he/2024-04-01-openvoice/ page failed
            # while the other 2,296 URLs passed.
            "wait": 500,
            "chromeLaunchConfig": {
                "args": ["--no-sandbox", "--disable-setuid-sandbox"],
            },
            "hideElements": hide_elements,
        },
        "urls": urls,
    }


# ---------------------------------------------------------------------------
# Dark-mode sweep
# ---------------------------------------------------------------------------
#
# The main sweep audits pages in their default (light) rendering, which
# is how a 2.31:1 dark-mode contrast failure shipped in July 2026: every
# colour pair was AAA in light mode and never evaluated in dark. Rather
# than double the ~40-minute wall time by re-sweeping all ~2,000 pages,
# a fixed representative subset — one page per layout/surface family —
# is re-audited with the site's dark theme forced.
#
# Mechanism: theme-init.js (inline in <head>) sets ``data-theme`` on
# <html> before paint from localStorage OR ``prefers-color-scheme``. A
# fresh headless profile has no saved preference, so forcing the media
# feature to dark at Chrome launch deterministically boots every page
# dark. Two reinforcing flags (verified locally on Chrome 150 against a
# host in BOTH light and dark system themes):
#
#   * ``--blink-settings=preferredColorScheme=0`` — Blink's
#     PreferredColorScheme enum is kDark=0 / kLight=1; this overrides
#     the host/system theme in both directions.
#   * ``--force-dark-mode`` — forces the browser-side dark theme, which
#     also reports prefers-color-scheme: dark on current Chromium.
#
# NOTE deliberately NOT click-based: clicking ``.theme-toggle`` merely
# flips whatever theme the host booted, so on a dark-mode host it would
# land on LIGHT. The single ``wait for element html[data-theme="dark"]``
# action below is an assertion, not a mutation — if a future Chromium
# drops either flag the wait times out and the shard fails loudly
# instead of silently auditing light mode. The ``#dark`` URL fragment is
# a human-readable marker in reports/logs only — it does not affect
# navigation.
#
# Cache interaction: none, by design. The dark subset is small enough
# (~7 URLs, ~1-2 min) to sweep on every run that sweeps anything, and
# keeping it out of the hash cache avoids polluting light-mode "pass"
# entries with dark results. When the partition step reports a full
# cache hit (pa11y-needed=false) nothing on the site changed, so the
# dark rendering cannot have changed either and skipping is sound. The
# light .pa11yci defaults are untouched, so the cache config-hash
# fingerprint does not move and no full re-sweep is triggered.

DARK_CHROME_ARGS: list[str] = [
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--blink-settings=preferredColorScheme=0",
    "--force-dark-mode",
]

DARK_THEME_ACTIONS: list[str] = [
    'wait for element html[data-theme="dark"] to be visible',
]

# Representative subset: home, ISO 20022 MCP hub, MCP docs, speaking,
# trust, one article (report layout + cite/QA furniture), one locale
# home (RTL/i18n chrome). One page per surface family — the dark-mode
# CSS is defined centrally in the layout <style> blocks, so one page
# per layout exercises every dark token pair without re-sweeping the
# whole tree.
DARK_SWEEP_RELPATHS: tuple[str, ...] = (
    "index.html",
    "iso20022-mcp/index.html",
    "iso20022-mcp-docs/index.html",
    "speaking/index.html",
    "trust/index.html",
    "2026-05-11-lucy-besson-knowledge-transfer-ai-quantum/index.html",
    "fr/index.html",
)


def build_dark_config(
    public_dir: Path, base_url: str, hide_elements: str
) -> dict[str, Any]:
    """Pa11y-ci config for the dark-mode representative subset. Same
    defaults as the light sweep except Chrome launches with the
    prefers-color-scheme:dark flags; each URL entry is an object
    carrying the dark-theme assertion ``actions`` and a ``#dark`` marker
    fragment. Pages missing from public/ are dropped (a renamed page
    must not fail the sweep with a 404)."""
    base = base_url.rstrip("/")
    urls: list[dict[str, Any]] = [
        {"url": f"{base}/{rel}#dark", "actions": list(DARK_THEME_ACTIONS)}
        for rel in DARK_SWEEP_RELPATHS
        if (public_dir / rel).is_file()
    ]
    config = build_pa11yci_config([], hide_elements)
    config["defaults"]["chromeLaunchConfig"] = {"args": list(DARK_CHROME_ARGS)}
    config["urls"] = urls
    return config


_DEFAULT_HIDE_ELEMENTS = (
    "#ssg-search-widget, #ssg-search-btn, "
    "iframe[src*='recaptcha'], iframe[src*='google.com/recaptcha'], "
    "form iframe, "
    # /projects-*/ story heroes overlay white text on a full-bleed image
    # behind a dark scrim. pa11y cannot read an image/gradient background and
    # returns NaN contrast (flaky even with the image hidden). The overlay is
    # genuinely legible (white on a dark scrim, manually verified), so hide the
    # whole decorative hero from the contrast sweep — it carries no links and
    # htmlcs does not require an h1.
    ".story-hero"
)


def cmd_pre(args: argparse.Namespace) -> int:
    """Pre-pass: read public/, partition against cache, write .pa11yci
    config for the to-sweep set + emit a manifest of cache-hit relpaths
    so the post-pass can mark them as still-passing without re-checking.
    """
    public_dir = Path(args.public_dir)
    cache_path = Path(args.cache)
    cache = load_cache(cache_path)

    pa11y_version = args.pa11y_version or detect_pa11y_version()
    chromium_version = args.chromium_version or detect_chromium_version()
    hide_elements = args.hide_elements or _DEFAULT_HIDE_ELEMENTS

    # First compute the config hash on a *URL-less* config so it stays
    # stable across cache fills.
    bare_config = build_pa11yci_config([], hide_elements)
    config_hash = compute_config_hash(bare_config)
    current_fp = {
        "pa11y_version": pa11y_version,
        "chromium_version": chromium_version,
        "config_hash": config_hash,
        "wcag_standard": "WCAG2AAA",
    }

    to_sweep, cache_hits, skipped = partition_pages(public_dir, cache, current_fp)

    # Build the real .pa11yci with just the to-sweep URLs.
    base_url = args.base_url.rstrip("/")
    sweep_urls = [f"{base_url}/{p.relative_to(public_dir).as_posix()}" for p, _ in to_sweep]
    config = build_pa11yci_config(sweep_urls, hide_elements)
    Path(args.pa11yci_out).write_text(
        json.dumps(config, indent=2),
        encoding="utf-8",
    )

    # Dark-mode config: fixed representative subset, cache-independent
    # (see the Dark-mode sweep comment block above). getattr keeps
    # programmatic callers that build a bare Namespace working; an empty
    # value skips the dark config entirely.
    dark_out = getattr(args, "dark_out", "")
    dark_config: dict[str, Any] = {"urls": []}
    if dark_out:
        dark_config = build_dark_config(public_dir, base_url, hide_elements)
        Path(dark_out).write_text(
            json.dumps(dark_config, indent=2),
            encoding="utf-8",
        )

    # Manifest the post-pass needs.
    manifest = {
        "fingerprint": current_fp,
        "to_sweep_hashes": {p.relative_to(public_dir).as_posix(): h for p, h in to_sweep},
        "cache_hit_hashes": {p.relative_to(public_dir).as_posix(): h for p, h in cache_hits},
        "skipped": skipped,
    }
    Path(args.manifest_out).write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )

    total = len(to_sweep) + len(cache_hits) + len(skipped)
    print(
        f"pa11y-cache pre: {total} pages — "
        f"{len(cache_hits)} cached pass, "
        f"{len(to_sweep)} to sweep, "
        f"{len(skipped)} Spotify-iframe skips."
    )
    if dark_out:
        print(
            f"pa11y-cache pre: dark-mode subset — "
            f"{len(dark_config['urls'])} URLs written to {dark_out}"
        )
    print(
        f"  fingerprint: pa11y={pa11y_version} "
        f"chromium={chromium_version} "
        f"config={config_hash[:12]} standard=WCAG2AAA"
    )
    return 0


def _audited_clean_relpaths(args: argparse.Namespace) -> set[str] | None:
    """Relpaths some shard audited and found clean, or None if not asked.

    Reads the pa11y-ci JSON reports the shards uploaded. Their shape is
    ``{"results": {url: [issue, ...]}}`` and a *passing* URL is present
    with an empty issue list, so "audited clean" is exactly
    ``url in results and not results[url]``. A URL absent from every
    report was never audited — a hung shard never wrote one — and must
    not be cached.
    """
    reports_dir = getattr(args, "audited_reports", "") or ""
    if not reports_dir:
        return None
    base = (getattr(args, "base_url", "") or "").rstrip("/")
    clean: set[str] = set()
    for report in sorted(Path(reports_dir).rglob("*.json")):
        try:
            results = json.loads(report.read_text(encoding="utf-8")).get("results", {})
        except (json.JSONDecodeError, OSError):
            # A shard that died mid-write leaves a truncated report.
            # Treat it as "audited nothing" rather than failing the save.
            continue
        for url, issues in results.items():
            if issues:
                continue
            rel = url[len(base) :] if base and url.startswith(base) else url
            clean.add(rel.split("?", 1)[0].split("#", 1)[0].lstrip("/"))
    return clean


def cmd_post(args: argparse.Namespace) -> int:
    """Post-pass: given a successful pa11y run on the delta URLs (which
    is what `pa11y-ci -c .pa11yci` exited 0 for), update the cache so
    next run can skip them."""
    cache_path = Path(args.cache)
    manifest_path = Path(args.manifest)
    if not manifest_path.is_file():
        print(f"pa11y-cache post: manifest {manifest_path} missing — nothing to update")
        return 1
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    cache = load_cache(cache_path)
    current_fp = manifest["fingerprint"]

    # If the fingerprint moved relative to the stored cache, replace it
    # wholesale — old entries shouldn't survive a config/version change.
    if not fingerprint_matches(cache, current_fp):
        cache["fingerprint"] = current_fp
        cache["pages"] = {}

    now = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    pages = cache["pages"]

    # Cache-hit set: re-affirm with current timestamp. Their hash didn't
    # change, so the entry just gets touched.
    for rel, h in manifest.get("cache_hit_hashes", {}).items():
        pages[rel] = {"hash": h, "status": "pass", "checked": now}

    # Newly-passed sweep set: record the current hash as the new
    # checkpoint.
    #
    # Without --audited-reports this is a whole-delta update, which is
    # only sound on a green run: pa11y exited 0, so every swept URL
    # passed.
    #
    # With --audited-reports the run was NOT fully green — one shard
    # hung or failed — and we may only checkpoint the URLs some shard
    # actually audited and found clean. That keeps a transient hang in
    # one shard from throwing away the other shards' work, which is what
    # turns a single bad run into a compounding backlog: an unsaved
    # cache means the next run re-sweeps everything, runs longer, and is
    # likelier to hang again. Pages that were never audited simply stay
    # out of the cache and get swept next time.
    audited = _audited_clean_relpaths(args)
    swept = manifest.get("to_sweep_hashes", {})
    if audited is not None:
        skipped = [rel for rel in swept if rel not in audited]
        swept = {rel: h for rel, h in swept.items() if rel in audited}
        print(
            f"pa11y-cache post: partial update — {len(swept)} of "
            f"{len(swept) + len(skipped)} swept pages were audited clean; "
            f"{len(skipped)} left uncached for the next run.",
        )
    for rel, h in swept.items():
        pages[rel] = {"hash": h, "status": "pass", "checked": now}

    # Drop entries for files that no longer exist in public/. They'd
    # otherwise accumulate as the site changes.
    public_dir = Path(args.public_dir)
    live_relpaths = {p.relative_to(public_dir).as_posix() for p in public_dir.rglob("index.html")}
    stale = [rel for rel in pages if rel not in live_relpaths]
    for rel in stale:
        pages.pop(rel, None)

    save_cache(cache_path, cache)
    print(
        f"pa11y-cache post: {len(pages)} pages now cached as pass "
        f"(+{len(manifest.get('to_sweep_hashes', {}))} swept, "
        f"-{len(stale)} stale)."
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Pa11y-ci hash cache helper.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_pre = sub.add_parser("pre", help="Decide which pages to sweep.")
    p_pre.add_argument("--public-dir", default="public")
    p_pre.add_argument("--cache", default="_data/pa11y-cache.json")
    p_pre.add_argument("--pa11yci-out", default=".pa11yci")
    p_pre.add_argument("--dark-out", default=".pa11yci.dark")
    p_pre.add_argument("--manifest-out", default=".pa11y-cache-manifest.json")
    p_pre.add_argument("--base-url", default="http://127.0.0.1:8000")
    p_pre.add_argument("--pa11y-version", default="")
    p_pre.add_argument("--chromium-version", default="")
    p_pre.add_argument("--hide-elements", default="")
    p_pre.set_defaults(func=cmd_pre)

    p_post = sub.add_parser("post", help="Update cache after green sweep.")
    p_post.add_argument("--public-dir", default="public")
    p_post.add_argument("--cache", default="_data/pa11y-cache.json")
    p_post.add_argument("--manifest", default=".pa11y-cache-manifest.json")
    p_post.add_argument(
        "--audited-reports",
        default="",
        help=(
            "Directory of pa11y-ci shard JSON reports. When given, only "
            "URLs a shard actually audited and found clean are cached — "
            "use this to checkpoint a partially-green run."
        ),
    )
    p_post.add_argument("--base-url", default="http://127.0.0.1:8000")
    p_post.set_defaults(func=cmd_post)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
