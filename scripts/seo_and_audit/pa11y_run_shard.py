#!/usr/bin/env python3
"""Run one pa11y shard in bounded chunks so a wedged Chrome costs minutes.

A headless-Chrome process that stops responding hangs pa11y-ci on the URL it
is holding. pa11y's own ``timeout`` is a page-load timeout inside the
browser, so it never fires when the browser itself is the thing that wedged.

The shard step used to bound the whole shard — 35 minutes, retried once. That
turned one stuck URL into 70 minutes of CI, no results at all for the other
URLs in the shard, and no clue which URL was responsible. It happened in 3 of
the 15 CI runs before this change, and one such hang on 2026-07-30 kept three
merges off production.

This runs the shard in chunks instead. Each chunk is bounded, so a wedge
costs one chunk rather than the whole shard, the URLs in it are named, and
every other chunk still reports. A wedged chunk is retried once with Chrome
killed first, because the hang is transient; if it wedges again its URLs are
reported as unchecked and the shard fails — visibly, and in minutes.

Output is pa11y-ci's own JSON shape, so pa11y_retry_flakes.py and the
finalise merge consume it unchanged:
``{"total": N, "passes": N, "errors": N, "results": {url: [issue, ...]}}``

Usage:
  python3 scripts/seo_and_audit/pa11y_run_shard.py \
      --config .pa11yci.shard --out pa11y.shard.json [--chunk-size 8] \
      [--timeout 360]
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

WEDGED = -9  # our own marker for "the chunk had to be killed"
TIMED_OUT = (WEDGED, 124, 137)  # ours, plus timeout(1)'s codes for compatibility


def _load_urls(config: Path) -> tuple[dict, list]:
    data = json.loads(config.read_text(encoding="utf-8"))
    return data, list(data.get("urls", []))


def _run_chunk(config: Path, timeout_s: int) -> tuple[int, dict]:
    """Run pa11y-ci over one chunk config. Returns (returncode, report).

    The timeout is Python's rather than ``timeout(1)``: that is GNU coreutils,
    present on the CI runner but not on macOS, so shelling out to it left the
    real subprocess path untestable anywhere but CI. The child gets its own
    process group so the kill reaches the Chrome processes pa11y spawned —
    terminating only pa11y-ci would leave the wedged browser behind, which is
    the thing that poisons the retry.
    """
    proc = subprocess.Popen(
        ["pa11y-ci", "-c", str(config), "--reporter", "json"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    try:
        stdout, stderr = proc.communicate(timeout=timeout_s)
    except subprocess.TimeoutExpired:
        _kill_group(proc)
        proc.communicate()
        return WEDGED, {}
    try:
        return proc.returncode, json.loads(stdout or "{}")
    except json.JSONDecodeError:
        # pa11y-ci exits non-zero with a usable report on real errors; only a
        # crash leaves unparseable output, and that must not look like a pass.
        print(stdout[-2000:], file=sys.stderr)
        print(stderr[-2000:], file=sys.stderr)
        return proc.returncode or 1, {}


def _kill_group(proc: subprocess.Popen) -> None:
    """SIGKILL the child's whole process group, Chrome included."""
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        proc.kill()


def _kill_chrome() -> None:
    subprocess.run(["pkill", "-f", "chrome|chromium"], capture_output=True)


def _url_names(chunk: list) -> list[str]:
    """pa11y config entries are either a URL string or {"url": ...}."""
    return [u if isinstance(u, str) else u.get("url", "?") for u in chunk]


def _attempt_chunk(cfg: Path, chunk: list, timeout_s: int) -> tuple[dict, list[str], bool]:
    """Run one chunk, retrying once if it wedges.

    Returns (results, unchecked_urls, crashed).
    """
    rc, report = _run_chunk(cfg, timeout_s)
    if rc in TIMED_OUT:
        print(f"pa11y: chunk wedged (exit {rc}); killing Chrome and retrying once")
        _kill_chrome()
        rc, report = _run_chunk(cfg, timeout_s)
        if rc in TIMED_OUT:
            names = _url_names(chunk)
            print(f"pa11y: chunk wedged again — unchecked: {', '.join(names)}")
            _kill_chrome()
            return {}, names, False
    # pa11y-ci exits 2 when a page has issues; only an unparseable report with
    # an unexpected code means it crashed, and that must not read as a pass.
    crashed = not report and rc not in (0, 1, 2)
    return report.get("results", {}), [], crashed


def run(config: Path, out: Path, chunk_size: int, timeout_s: int, budget_s: int = 3300) -> int:
    """Check the shard in bounded chunks.

    ``budget_s`` caps the whole shard so the pathological case — every chunk
    wedging twice — still lands inside the job's own timeout-minutes rather
    than being killed by it, which would lose the results already gathered.
    """
    base, urls = _load_urls(config)
    if not urls:
        out.write_text(
            json.dumps({"total": 0, "passes": 0, "errors": 0, "results": {}}), encoding="utf-8"
        )
        print("empty shard")
        return 0

    results: dict[str, list] = {}
    wedged: list[str] = []
    crashed = False
    tmp = Path(tempfile.mkdtemp(prefix="pa11y-chunk-"))
    began = time.monotonic()
    try:
        for start in range(0, len(urls), chunk_size):
            chunk = urls[start : start + chunk_size]
            if time.monotonic() - began > budget_s:
                remaining = _url_names(urls[start:])
                print(
                    f"pa11y: shard budget of {budget_s}s spent; {len(remaining)} URL(s) unchecked"
                )
                wedged.extend(remaining)
                break
            cfg = tmp / f"chunk-{start}.json"
            cfg.write_text(json.dumps({**base, "urls": chunk}), encoding="utf-8")
            report, stuck, broke = _attempt_chunk(cfg, chunk, timeout_s)
            wedged.extend(stuck)
            crashed = crashed or broke
            results.update(report)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    errors = sum(1 for issues in results.values() if issues)
    out.write_text(
        json.dumps(
            {
                "total": len(results),
                "passes": len(results) - errors,
                "errors": errors,
                "results": results,
            }
        ),
        encoding="utf-8",
    )
    print(f"pa11y: {len(results)}/{len(urls)} URL(s) checked, {errors} with errors")
    if wedged:
        print(f"::error::pa11y left {len(wedged)} URL(s) unchecked after a retry")
        return 1
    return 1 if crashed else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--chunk-size", type=int, default=8)
    ap.add_argument("--timeout", type=int, default=360, help="seconds per chunk attempt")
    ap.add_argument(
        "--budget",
        type=int,
        default=3300,
        help="seconds for the whole shard; must stay under the job timeout",
    )
    args = ap.parse_args(argv)
    return run(args.config, args.out, args.chunk_size, args.timeout, args.budget)


if __name__ == "__main__":
    raise SystemExit(main())
