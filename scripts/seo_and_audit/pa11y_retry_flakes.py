"""Re-run pa11y-ci against URLs that hit the Puppeteer
"Execution context was destroyed" navigation race.

When pa11y-ci sweeps the site, occasional URLs fail with::

    Protocol error (Runtime.callFunctionOn): Execution context was destroyed.
    Execution context was destroyed, most likely because of a navigation.

That is not a WCAG violation. It is a race between Puppeteer's evaluate
call and a late-firing client-side navigation (related-posts prefetch,
hreflang switching, lazy enrich hydration). pa11y-ci has no built-in
retry for this, so the whole run fails on a single flaky URL even though
the other 2,000+ pages passed.

This script reads pa11y-ci's JSON output, partitions failures into
"flake" (Execution context was destroyed only) versus "real" (any other
error), and:

* If any URL has a real failure, exits 1 — pa11y-ci's original output
  has already been printed by the workflow, so the violation context is
  available.
* Otherwise, re-runs pa11y-ci against only the flaky URLs once with a
  larger wait. If the retry passes, exits 0. If any retry still fails,
  exits 1 and prints the still-flaking URL list.

Used by ``.github/workflows/ci.yml`` accessibility job.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FLAKE_NEEDLES = ("Execution context was destroyed",)

RETRY_WAIT_MS = 1500


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: pa11y_retry_flakes.py <pa11y.json>", file=sys.stderr)
        return 2

    report = _load_report(Path(argv[1]))
    if report is None:
        return 2

    flaky, real_failures = _partition_failures(report.get("results", {}))

    if real_failures:
        _print_real_failures(real_failures)
        return 1

    if not flaky:
        # pa11y-ci returned nonzero but the JSON report shows no
        # failures. That can happen if the pa11y-ci process itself
        # exited early. Treat as a real failure.
        print("pa11y: nonzero exit with no recorded failures — bailing.")
        return 1

    print(f"pa11y: {len(flaky)} URL(s) hit the navigation flake; retrying:")
    for u in flaky:
        print(f"  {u}")

    rc = _retry_urls(flaky)
    if rc == 0:
        print(
            f"pa11y: all {len(flaky)} flaky URL(s) passed on retry — "
            "treating overall run as passing.",
        )
        # Clear the recovered flakes from the on-disk report. The retry
        # re-runs pa11y against a temp config and never rewrote this file,
        # so without this the uploaded shard artifact still carries the
        # flake errors and the finalise merge step fails with
        # "pa11y errors remain". real_failures was empty above, so once
        # the flaky URLs are dropped no failing URLs remain.
        results = report.get("results", {})
        for url in flaky:
            results.pop(url, None)
        report["results"] = results
        report["errors"] = sum(1 for issues in results.values() if issues)
        if "total" in report:
            report["passes"] = report["total"] - report["errors"]
        Path(argv[1]).write_text(json.dumps(report), encoding="utf-8")
    return rc


def _load_report(path: Path) -> dict | None:
    if not path.exists():
        print(f"missing pa11y-ci JSON report at {path}", file=sys.stderr)
        return None
    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # pa11y-ci sometimes flushes trailing stdout after its JSON
        # object ("Extra data"); decode the first complete object and
        # ignore the rest.
        try:
            obj, _ = json.JSONDecoder().raw_decode(text.lstrip())
            return obj
        except json.JSONDecodeError as exc:
            print(f"pa11y-ci JSON not parseable: {exc}", file=sys.stderr)
            return None


def _partition_failures(
    results: dict[str, list[dict]],
) -> tuple[list[str], list[tuple[str, list[str]]]]:
    """Split URL → issues into (flaky_urls, real_failures).

    pa11y-ci v3 JSON shape: ``{"results": {url: [issue, ...], ...}}``.
    A URL is flaky iff every issue against it matches FLAKE_NEEDLES.
    """
    flaky: list[str] = []
    real_failures: list[tuple[str, list[str]]] = []
    for url, issues in results.items():
        if not issues:
            continue
        if all(_is_flake(i) for i in issues):
            flaky.append(url)
        else:
            real_failures.append((url, [_describe(i) for i in issues]))
    return flaky, real_failures


def _print_real_failures(
    real_failures: list[tuple[str, list[str]]],
) -> None:
    print("pa11y: real WCAG failures detected, not retrying:")
    for url, descs in real_failures:
        print(f"  {url}")
        for d in descs:
            print(f"    - {d}")


def _is_flake(issue: dict) -> bool:
    msg = str(issue.get("message", ""))
    return any(needle in msg for needle in FLAKE_NEEDLES)


def _describe(issue: dict) -> str:
    code = issue.get("code", "?")
    msg = issue.get("message", "?")
    return f"[{code}] {msg}"


def _retry_urls(urls: list[str]) -> int:
    """Re-run pa11y-ci against just the supplied URLs with a generous
    wait. Returns the pa11y-ci exit code."""
    if not shutil.which("pa11y-ci"):
        print("pa11y-ci binary not on PATH for retry", file=sys.stderr)
        return 1

    config = {
        "defaults": {
            "standard": "WCAG2AAA",
            "timeout": 30000,
            "wait": RETRY_WAIT_MS,
            "chromeLaunchConfig": {
                "args": ["--no-sandbox", "--disable-setuid-sandbox"],
            },
        },
        "urls": urls,
    }

    with tempfile.NamedTemporaryFile(
        "w",
        suffix=".json",
        delete=False,
        encoding="utf-8",
    ) as tmp:
        json.dump(config, tmp)
        tmp_path = tmp.name

    try:
        result = subprocess.run(
            ["pa11y-ci", "-c", tmp_path],
            check=False,
        )
        return result.returncode
    finally:
        Path(tmp_path).unlink(missing_ok=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
