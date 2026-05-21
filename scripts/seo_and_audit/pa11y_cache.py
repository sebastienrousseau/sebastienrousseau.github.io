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

CACHE_VERSION = 1


def compute_page_hash(path: Path) -> str:
    """SHA-256 of the raw HTML bytes. Streamed so it works on the
    larger rendered pages without loading them fully into a string."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


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
            check=True, capture_output=True, text=True, timeout=10,
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
                check=True, capture_output=True, text=True, timeout=10,
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
    return "open.spotify.com" in html or "scdn.co" in html


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
      * ``skipped`` — relpaths that embed a Spotify iframe; pa11y can't
        check them reliably.

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
        if page_is_spotify_iframe(html):
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
        "defaults": {
            "standard": "WCAG2AAA",
            "timeout": 20000,
            "chromeLaunchConfig": {
                "args": ["--no-sandbox", "--disable-setuid-sandbox"],
            },
            "hideElements": hide_elements,
        },
        "urls": urls,
    }


_DEFAULT_HIDE_ELEMENTS = (
    "#ssg-search-widget, #ssg-search-btn, "
    "iframe[src*='recaptcha'], iframe[src*='google.com/recaptcha'], "
    "form iframe"
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
    sweep_urls = [
        f"{base_url}/{p.relative_to(public_dir).as_posix()}" for p, _ in to_sweep
    ]
    config = build_pa11yci_config(sweep_urls, hide_elements)
    Path(args.pa11yci_out).write_text(
        json.dumps(config, indent=2), encoding="utf-8",
    )

    # Manifest the post-pass needs.
    manifest = {
        "fingerprint": current_fp,
        "to_sweep_hashes": {
            p.relative_to(public_dir).as_posix(): h for p, h in to_sweep
        },
        "cache_hit_hashes": {
            p.relative_to(public_dir).as_posix(): h for p, h in cache_hits
        },
        "skipped": skipped,
    }
    Path(args.manifest_out).write_text(
        json.dumps(manifest, indent=2), encoding="utf-8",
    )

    total = len(to_sweep) + len(cache_hits) + len(skipped)
    print(
        f"pa11y-cache pre: {total} pages — "
        f"{len(cache_hits)} cached pass, "
        f"{len(to_sweep)} to sweep, "
        f"{len(skipped)} Spotify-iframe skips."
    )
    print(
        f"  fingerprint: pa11y={pa11y_version} "
        f"chromium={chromium_version} "
        f"config={config_hash[:12]} standard=WCAG2AAA"
    )
    return 0


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
    # checkpoint. The status comes from the caller — if pa11y exited 0
    # we trust the full delta passed; if it exited non-zero we never
    # reach this script (CI fails before we get here), so this branch
    # only fires on a green run.
    for rel, h in manifest.get("to_sweep_hashes", {}).items():
        pages[rel] = {"hash": h, "status": "pass", "checked": now}

    # Drop entries for files that no longer exist in public/. They'd
    # otherwise accumulate as the site changes.
    public_dir = Path(args.public_dir)
    live_relpaths = {
        p.relative_to(public_dir).as_posix()
        for p in public_dir.rglob("index.html")
    }
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
    p_post.set_defaults(func=cmd_post)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
