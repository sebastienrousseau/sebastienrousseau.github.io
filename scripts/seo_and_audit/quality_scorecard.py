#!/usr/bin/env python3
"""Measure the repository against a fixed rubric and emit a scorecard.

A rating is only worth having if it is *measured*. The failure this repo
already lived through — `assert_eq!(default, "My SSG Site")` passing green
while that placeholder shipped on 7,189 live pages — is the same shape as an
asserted score: confident, checkable, and never checked.

So every metric here names the command that produces it, and any metric this
script cannot measure is reported as ``unmeasured`` rather than guessed. An
honest gap scores nothing and says so; it never quietly becomes a 10.

Usage:
    python3 scripts/seo_and_audit/quality_scorecard.py            # human table
    python3 scripts/seo_and_audit/quality_scorecard.py --json     # raw data
    python3 scripts/seo_and_audit/quality_scorecard.py --fail-under 8.0
"""

from __future__ import annotations

import argparse
import contextlib
import json
import re
import statistics
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
POSTS = ROOT / "_posts"

UNMEASURED = "unmeasured"


@dataclass
class Metric:
    """One measurable property, and how a measurement becomes a 0–10 score."""

    key: str
    label: str
    how: str
    """The command or method a reader can run to reproduce the value."""
    score_fn: Callable[[object], float | None]
    value: object = UNMEASURED
    detail: str = ""

    @property
    def score(self) -> float | None:
        if self.value is UNMEASURED or self.value is None:
            return None
        try:
            return self.score_fn(self.value)
        except Exception:  # a broken scorer must not fake a number
            return None


@dataclass
class Category:
    key: str
    label: str
    weight: float
    metrics: list[Metric] = field(default_factory=list)

    @property
    def score(self) -> float | None:
        scored = [m.score for m in self.metrics if m.score is not None]
        return round(statistics.mean(scored), 2) if scored else None

    @property
    def coverage(self) -> str:
        n = sum(1 for m in self.metrics if m.score is not None)
        return f"{n}/{len(self.metrics)}"


# ---------------------------------------------------------------------------
# Scoring helpers — all monotonic and explicit, so a score can be argued with
# ---------------------------------------------------------------------------


def band(thresholds: list[tuple[float, float]], *, higher_is_better: bool = True):
    """Piecewise scorer: first threshold whose bound is met wins."""

    def score(v: object) -> float:
        x = float(v)  # type: ignore[arg-type]
        for bound, points in thresholds:
            if (higher_is_better and x >= bound) or (not higher_is_better and x <= bound):
                return points
        return 0.0

    return score


def boolean(points_true: float = 10.0, points_false: float = 0.0):
    return lambda v: points_true if v else points_false


def run(cmd: list[str], cwd: Path = ROOT) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=900)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except (OSError, subprocess.SubprocessError):
        return -1, ""


def pages() -> list[Path]:
    return sorted(PUBLIC.rglob("index.html")) if PUBLIC.is_dir() else []


# ---------------------------------------------------------------------------
# Measurements
# ---------------------------------------------------------------------------


def _duplicate_asset_count() -> int | str:
    """Byte-identical files still shipped under distinct /_csp/ URLs."""
    csp = PUBLIC / "_csp"
    if not csp.is_dir():
        return UNMEASURED
    import hashlib

    seen: dict[str, int] = {}
    for f in csp.iterdir():
        if f.is_file() and f.suffix in {".css", ".js"}:
            h = hashlib.sha256(f.read_bytes()).hexdigest()
            seen[h] = seen.get(h, 0) + 1
    return sum(c - 1 for c in seen.values() if c > 1)


def _allowlisted_complexity() -> int | str:
    allow = ROOT / "scripts" / "dev" / "complexity-allowlist.txt"
    if not allow.is_file():
        return UNMEASURED
    return sum(
        1
        for line in allow.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    )


def measure_code(cat: Category) -> None:
    rc, _ = run(["ruff", "check", "scripts/", "tests/"])
    cat.metrics[0].value = rc == 0

    rc, _ = run(["bash", "scripts/typecheck.sh"])
    cat.metrics[1].value = rc == 0

    n = _allowlisted_complexity()
    cat.metrics[2].value = n
    if n is not UNMEASURED:
        cat.metrics[2].detail = f"{n} functions above C complexity, enumerated"

    _rc, out = run(["python3", "-m", "pytest", "tests/unit/", "--collect-only", "-q"])
    m = re.search(r"(\d+) tests collected", out)
    if m:
        cat.metrics[3].value = int(m.group(1))

    cat.metrics[4].value = _duplicate_asset_count()


def _meta_coverage(ps: list[Path]) -> tuple[float, float, float, int]:
    """(% with description, % canonical, % og:title, placeholder pages)."""
    desc = canon = og = placeholder = 0
    for p in ps:
        h = p.read_text(encoding="utf-8", errors="ignore")
        if re.search(r'<meta\b[^>]*name="description"[^>]*content="[^"]{20,}"', h):
            desc += 1
        if 'rel="canonical"' in h:
            canon += 1
        if "og:title" in h:
            og += 1
        if "My SSG Site" in h:
            placeholder += 1
    n = len(ps)
    return (
        round(100 * desc / n, 1),
        round(100 * canon / n, 1),
        round(100 * og / n, 1),
        placeholder,
    )


# An internal article link, in any locale. The locale prefix is the point:
# a pattern anchored on `^/20\d\d-` matches an English article and silently
# misses `/fr/2026-…`, which reported locale pages as having zero internal
# links when they had eight. Every dated page carries a cluster block; the
# measurement said 2.9 % of them did.
_ARTICLE_HREF = re.compile(
    r"^(?:https://sebastienrousseau\.com)?/(?:[a-z]{2}(?:-[a-z]+)?/)?\d{4}-\d{2}-\d{2}-"
)


def _internal_link_counts(ps: list[Path]) -> tuple[list[int], list[int]]:
    """Unique internal article links inside <main>, split (english, locale).

    Reported separately on purpose. A single median over all dated pages hides
    the shape completely: English articles sit at 16, locale copies at 0, and
    the combined median is 0 — which reads as "no internal linking anywhere"
    when the truth is "internal linking on 2.9% of them".
    """
    english: list[int] = []
    locale: list[int] = []
    for p in ps:
        if not re.match(r"^\d{4}-\d{2}-\d{2}-", p.parent.name):
            continue
        is_en = len(p.relative_to(PUBLIC).parts) == 2
        h = p.read_text(encoding="utf-8", errors="ignore")
        mm = re.search(r"<main\b[^>]*>([\s\S]*?)</main>", h)
        seg = mm.group(1) if mm else ""
        links = {href for href in re.findall(r'href="([^"]+)"', seg) if _ARTICLE_HREF.match(href)}
        (english if is_en else locale).append(len(links))
    return english, locale


def measure_seo(cat: Category, ps: list[Path]) -> None:
    if not ps:
        return
    desc, canon, og, placeholder = _meta_coverage(ps)
    cat.metrics[0].value = desc
    cat.metrics[1].value = canon
    cat.metrics[2].value = og
    cat.metrics[3].value = placeholder

    _rc, out = run(
        ["python3", "scripts/seo_and_audit/validate_jsonld.py", "--base-dir", "public"]
    )
    m = re.search(r"(\d+) with structured-data errors", out)
    if m:
        cat.metrics[4].value = int(m.group(1))

    english, locale = _internal_link_counts(ps)
    if english:
        cat.metrics[5].value = statistics.median(english)
        cat.metrics[5].detail = f"n={len(english)} EN articles, mean {statistics.mean(english):.1f}"
    if english or locale:
        total = len(english) + len(locale)
        reached = sum(1 for c in english + locale if c >= 4)
        cat.metrics[7].value = round(100 * reached / total, 1)
        cat.metrics[7].detail = (
            f"{reached}/{total} dated pages; locale median "
            f"{statistics.median(locale) if locale else 0:.0f}"
        )

    _rc, out = run(
        ["python3", "scripts/seo_and_audit/audit_links.py", "--base-dir", "public", "--strict-internal"]
    )
    m = re.search(r"(\d+) checked, (\d+) broken", out)
    if m:
        cat.metrics[6].value = int(m.group(2))


def measure_ux(cat: Category, ps: list[Path]) -> None:
    if not ps:
        return
    # TRANSFERRED bytes, not bytes on disk.
    #
    # This measured `stat().st_size` — raw HTML — which is not a quantity any
    # reader experiences. Production serves `content-encoding: gzip` (verified
    # against the live origin), and the corpus compresses 5x: p50 86 KB on disk
    # is 20 KB over the wire.
    #
    # Scoring raw bytes is not merely imprecise, it is inverted: a site serving
    # 60 KB uncompressed would have out-scored this one serving 20 KB
    # compressed, while being three times slower for every visitor. Compressing
    # a 400-page sample costs about a second and measures the real thing.
    import gzip
    import random

    # Fixed seed: sampling must be deterministic so two runs on the same
    # tree give the same score. Not a security context.
    rng = random.Random(11)  # noqa: S311
    sample = rng.sample(ps, min(len(ps), 400))
    sizes = sorted(len(gzip.compress(p.read_bytes(), 6)) for p in sample)
    cat.metrics[0].value = round(sizes[len(sizes) // 2] / 1024, 1)
    cat.metrics[0].detail = f"gzip, n={len(sample)} sampled pages"
    cat.metrics[1].value = round(sizes[int(len(sizes) * 0.9)] / 1024, 1)

    # Share of pages served by the single most-used stylesheet: the higher,
    # the more often a reader's cache already holds it.
    refs: dict[str, int] = {}
    for p in ps:
        h = p.read_text(encoding="utf-8", errors="ignore")
        for m in re.findall(r"/_csp/([a-f0-9]+\.css)", h):
            refs[m] = refs.get(m, 0) + 1
    if refs:
        cat.metrics[2].value = round(100 * max(refs.values()) / len(ps), 1)

    fonts = ROOT / "fonts" / "fonts.css"
    if fonts.is_file():
        css = fonts.read_text(encoding="utf-8")
        cat.metrics[3].value = "font-display:swap" in css.replace(" ", "") and "size-adjust" in css


def _read_json(path: Path) -> dict | None:
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except ValueError:
        return None
    return data if isinstance(data, dict) else None


def _unverified_wcag_criteria(crit: list[dict]) -> tuple[int, str]:
    """Criteria with NO verification route anywhere.

    Not criteria ssg's static analyser happens to be unable to check — that is
    a property of the analyser, not of the site. `runtime` criteria (contrast,
    reflow, text spacing, focus-not-obscured, status messages) ARE verified,
    by the Pa11y sweep: a real browser with axe-core across 3,697 pages in
    light and forced-dark. `not-applicable` ones have nothing to apply to. The
    two genuinely manual criteria are decided by
    tests/validation/test_wcag_manual_criteria.py, which is a build gate — if
    it fails they revert to unverified and this count rises.
    """
    runtime_ok = (PUBLIC / "accessibility-report.json").is_file()
    manual_ok = run(["python3", "tests/validation/test_wcag_manual_criteria.py"])[0] == 0
    unverified = 0
    if not runtime_ok:
        unverified += sum(1 for c in crit if c.get("status") == "runtime")
    if not manual_ok:
        unverified += sum(1 for c in crit if c.get("status") == "manual")
    detail = (
        f"runtime via Pa11y: {'yes' if runtime_ok else 'NO'}; "
        f"manual gate: {'pass' if manual_ok else 'FAIL'}"
    )
    return unverified, detail


def measure_a11y(cat: Category) -> None:
    report = _read_json(PUBLIC / "accessibility-report.json")
    if report is not None:
        cat.metrics[0].value = report.get("total_issues", UNMEASURED)
        cat.metrics[1].value = report.get("pages_scanned", UNMEASURED)

    wcag = _read_json(PUBLIC / "wcag-compliance.json")
    if wcag is None:
        return
    crit = wcag.get("criteria", [])
    auto = [c for c in crit if c.get("status") == "automated"]
    if auto:
        passing = [c for c in auto if c.get("all_pages_pass")]
        cat.metrics[2].value = round(100 * len(passing) / len(auto), 1)
        cat.metrics[2].detail = f"{len(passing)}/{len(auto)} automated criteria"
    cat.metrics[3].value, cat.metrics[3].detail = _unverified_wcag_criteria(crit)


def measure_security(cat: Category, ps: list[Path]) -> None:
    if not ps:
        return
    sample = ps[: min(len(ps), 400)]
    unsafe = sum(1 for p in sample if "'unsafe-inline'" in p.read_text(encoding="utf-8", errors="ignore"))
    cat.metrics[0].value = unsafe

    with_sri = sum(
        1 for p in sample if re.search(r'<link[^>]+integrity="sha', p.read_text(encoding="utf-8", errors="ignore"))
    )
    cat.metrics[1].value = round(100 * with_sri / len(sample), 1)

    dupe_integrity = sum(
        1
        for p in sample
        if re.search(r'integrity="[^"]*"\s+integrity="', p.read_text(encoding="utf-8", errors="ignore"))
    )
    cat.metrics[2].value = dupe_integrity

    cat.metrics[3].value = (PUBLIC / "sbom.cdx.json").is_file()

    total = 0
    for tool in ("visual", "pa11y", "lighthouse"):
        rc, _out = run(
            ["npm", "audit", "--audit-level=high", "--prefix", f".github/ci-tools/{tool}"]
        )
        if rc != 0:
            total += 1
    cat.metrics[4].value = total
    cat.metrics[4].detail = "ci-tools lockfiles failing `npm audit --audit-level=high`"


def measure_i18n(cat: Category) -> None:
    rc, _ = run(["python3", "tests/validation/test_hreflang_reciprocity.py"])
    cat.metrics[0].value = rc == 0
    rc, _ = run(["python3", "tests/validation/test_i18n_parity.py"])
    cat.metrics[1].value = rc == 0
    rc, _ = run(["python3", "tests/validation/test_slug_policy.py"])
    cat.metrics[2].value = rc == 0
    if POSTS.is_dir():
        locales = [d for d in POSTS.iterdir() if d.is_dir() and len(d.name) <= 7]
        cat.metrics[3].value = len(locales)


def measure_ops(cat: Category) -> None:
    ci = ROOT / ".github" / "workflows" / "ci.yml"
    if ci.is_file():
        text = ci.read_text(encoding="utf-8")
        cat.metrics[0].value = "Reproducible build" in text
        cat.metrics[1].value = "verify_deploy.py" in text
        cat.metrics[2].value = "include-hidden-files: true" in text
        # Coverage, not a count. This used to be `text.count("timeout-minutes:")`
        # scored against a threshold of 8 — with 7 jobs in the workflow, all
        # 7 of them bounded, a perfect result could never reach full marks.
        # That is a defect in the measurement, not in the repo: the property
        # worth having is "no job can hang indefinitely", which is a ratio.
        with contextlib.suppress(Exception):  # unparseable workflow -> unmeasured
            import yaml

            jobs = (yaml.safe_load(text) or {}).get("jobs", {}) or {}
            if jobs:
                bounded = sum(1 for j in jobs.values() if j.get("timeout-minutes"))
                cat.metrics[3].value = round(100 * bounded / len(jobs), 1)
                cat.metrics[3].detail = f"{bounded}/{len(jobs)} CI jobs bounded"
    adr = ROOT / "project-docs" / "adr"
    if adr.is_dir():
        cat.metrics[4].value = len(list(adr.glob("*.md")))


# ---------------------------------------------------------------------------
# The rubric
#
# Weights reflect what this site is *for*: research that gets found, read and
# cited. Content reach outranks build ergonomics, and an accessibility failure
# outranks a slow build. Thresholds are deliberately explicit so a score can be
# argued with rather than merely accepted.
# ---------------------------------------------------------------------------


def rubric() -> list[Category]:
    return [
        Category("code", "Code quality", 0.18, [
            Metric("lint", "ruff clean", "ruff check scripts/ tests/", boolean()),
            Metric("types", "mypy strict tier clean", "bash scripts/typecheck.sh", boolean()),
            Metric("complexity", "C-or-worse functions", "radon cc scripts/ -n C",
                   band([(0, 10), (10, 8), (25, 6), (40, 4), (60, 2)], higher_is_better=False)),
            Metric("tests", "unit tests collected", "pytest --collect-only -q",
                   band([(50_000, 10), (10_000, 9), (2_000, 8), (500, 6), (100, 4)])),
            Metric("dupe_assets", "byte-identical assets shipped twice", "sha256 over public/_csp/",
                   band([(0, 10), (1, 8), (3, 5), (6, 2)], higher_is_better=False)),
        ]),
        Category("seo", "SEO / discoverability", 0.22, [
            Metric("desc", "pages with a real meta description (%)", "regex over public/**/index.html",
                   band([(99, 10), (95, 9), (90, 7), (75, 5), (50, 3)])),
            Metric("canonical", "pages with rel=canonical (%)", "regex over public/",
                   band([(99, 10), (95, 9), (90, 7), (75, 4)])),
            Metric("og", "pages with og:title (%)", "regex over public/",
                   band([(99, 10), (95, 9), (90, 7), (75, 4)])),
            Metric("placeholder", "pages carrying a generator placeholder", "grep 'My SSG Site'",
                   band([(0, 10), (1, 3)], higher_is_better=False)),
            Metric("jsonld", "pages with structured-data errors", "validate_jsonld.py",
                   band([(0, 10), (1, 7), (10, 4), (50, 1)], higher_is_better=False)),
            Metric("links", "median internal links per article", "regex inside <main>",
                   band([(12, 10), (8, 9), (5, 7), (3, 5), (1, 2)])),
            Metric("broken", "broken internal links", "audit_links.py --strict-internal",
                   band([(0, 10), (1, 5)], higher_is_better=False)),
            Metric("links_reach", "dated pages with >=4 internal links (%)", "regex inside <main>, all locales",
                   band([(90, 10), (70, 8), (50, 6), (25, 4), (5, 2)])),
        ]),
        Category("ux", "UX / performance", 0.16, [
            Metric("p50", "median transferred page weight (KB, gzip)", "gzip over a 400-page sample",
                   band([(25, 10), (40, 9), (60, 7), (100, 5), (160, 3)], higher_is_better=False)),
            Metric("p90", "p90 transferred page weight (KB, gzip)", "gzip over the sample",
                   band([(40, 10), (60, 9), (90, 7), (140, 5)], higher_is_better=False)),
            Metric("css_share", "pages sharing one stylesheet (%)", "regex over /_csp/ refs",
                   band([(90, 10), (80, 9), (65, 7), (50, 5), (30, 3)])),
            Metric("fonts", "self-hosted fonts with swap + metric-matched fallbacks", "fonts/fonts.css",
                   boolean()),
        ]),
        Category("a11y", "Accessibility", 0.16, [
            Metric("issues", "Pa11y issues in the last sweep", "public/accessibility-report.json",
                   band([(0, 10), (1, 6), (10, 3)], higher_is_better=False)),
            Metric("scanned", "pages covered by the sweep", "public/accessibility-report.json",
                   band([(3000, 10), (1000, 9), (250, 7), (50, 5)])),
            Metric("wcag_auto", "automated WCAG 2.2 criteria passing (%)", "public/wcag-compliance.json",
                   band([(100, 10), (95, 9), (85, 7), (70, 5)])),
            Metric("wcag_manual", "WCAG criteria with no verification route", "pa11y sweep + manual-criteria gate",
                   band([(0, 10), (1, 6), (3, 3)], higher_is_better=False)),
        ]),
        Category("security", "Security / supply chain", 0.14, [
            Metric("unsafe_inline", "sampled pages allowing 'unsafe-inline'", "grep over a 400-page sample",
                   band([(0, 10), (1, 2)], higher_is_better=False)),
            Metric("sri", "sampled pages with SRI on stylesheets (%)", "regex over a 400-page sample",
                   band([(99, 10), (95, 9), (85, 7), (60, 4)])),
            Metric("dupe_integrity", "pages with duplicate integrity attributes", "regex over the sample",
                   band([(0, 10), (1, 3)], higher_is_better=False)),
            Metric("sbom", "CycloneDX SBOM emitted", "public/sbom.cdx.json", boolean()),
            Metric("npm_audit", "ci-tools lockfiles with high/critical advisories", "npm audit --audit-level=high",
                   band([(0, 10), (1, 4)], higher_is_better=False)),
        ]),
        Category("i18n", "Internationalisation", 0.08, [
            Metric("hreflang", "hreflang reciprocity gate", "tests/validation/test_hreflang_reciprocity.py", boolean()),
            Metric("parity", "locale parity gate", "tests/validation/test_i18n_parity.py", boolean()),
            Metric("slug_policy", "slug policy gate (ADR-0012)", "tests/validation/test_slug_policy.py", boolean()),
            Metric("locales", "active locales", "count of _posts/<lang>/",
                   band([(20, 10), (10, 9), (5, 7), (2, 5)])),
        ]),
        Category("ops", "Operability", 0.06, [
            Metric("reproducible", "byte-identical rebuild gate", ".github/workflows/ci.yml", boolean()),
            Metric("deploy_probe", "post-deploy origin verification", ".github/workflows/ci.yml", boolean()),
            Metric("hidden_files", "deploy ships dotfiles (.well-known)", ".github/workflows/ci.yml", boolean()),
            Metric("timeouts", "CI jobs bounded by a timeout (%)", "parse ci.yml jobs",
                   band([(100, 10), (90, 8), (75, 6), (50, 3)])),
            Metric("adrs", "architecture decision records", "project-docs/adr/",
                   band([(12, 10), (8, 9), (5, 7), (2, 5)])),
        ]),
    ]


def collect() -> list[Category]:
    cats = rubric()
    by = {c.key: c for c in cats}
    ps = pages()
    measure_code(by["code"])
    measure_seo(by["seo"], ps)
    measure_ux(by["ux"], ps)
    measure_a11y(by["a11y"])
    measure_security(by["security"], ps)
    measure_i18n(by["i18n"])
    measure_ops(by["ops"])
    return cats


def overall(cats: list[Category]) -> float | None:
    scored = [(c.score, c.weight) for c in cats if c.score is not None]
    if not scored:
        return None
    total_w = sum(w for _, w in scored)
    return round(sum(s * w for s, w in scored) / total_w, 2)


def _render_category(c: Category) -> list[str]:
    s = f"{c.score:.2f}" if c.score is not None else "n/a"
    lines = [f"  {c.label:<26}{s:>7}{c.coverage:>8}  weight {c.weight:.0%}"]
    for m in c.metrics:
        val = m.value if m.value is not UNMEASURED else UNMEASURED
        sc = f"{m.score:>4.1f}" if m.score is not None else "   —"
        extra = f"  ({m.detail})" if m.detail else ""
        lines.append(f"      {sc}  {m.label:<46} {val}{extra}")
    lines.append("")
    return lines


def render(cats: list[Category]) -> str:
    lines = [
        "",
        "  Quality scorecard — every figure below is measured, not asserted.",
        "  'unmeasured' means exactly that; it never scores.",
        "",
        f"  {'CATEGORY':<26}{'SCORE':>7}{'COVER':>8}  METRICS",
        f"  {'-' * 74}",
    ]
    for c in cats:
        lines.extend(_render_category(c))
    o = overall(cats)
    unmeasured = sum(1 for c in cats for m in c.metrics if m.score is None)
    total = sum(len(c.metrics) for c in cats)
    lines.append(f"  {'-' * 74}")
    lines.append(f"  {'WEIGHTED OVERALL':<26}{o if o is not None else 'n/a':>7}")
    lines.append(
        f"  {total - unmeasured}/{total} metrics measured"
        + (f"; {unmeasured} unmeasured and excluded" if unmeasured else "")
    )
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true", help="emit raw measurements")
    ap.add_argument("--fail-under", type=float, help="exit 1 below this overall score")
    args = ap.parse_args(argv)

    cats = collect()
    if args.json:
        print(json.dumps({
            "overall": overall(cats),
            "categories": [
                {
                    "key": c.key, "label": c.label, "weight": c.weight,
                    "score": c.score, "coverage": c.coverage,
                    "metrics": [
                        {"key": m.key, "label": m.label, "how": m.how,
                         "value": m.value if m.value is not UNMEASURED else None,
                         "score": m.score, "detail": m.detail}
                        for m in c.metrics
                    ],
                }
                for c in cats
            ],
        }, indent=2, default=str))
    else:
        print(render(cats))

    o = overall(cats)
    if args.fail_under is not None and (o is None or o < args.fail_under):
        print(f"scorecard: {o} is below the {args.fail_under} floor", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
