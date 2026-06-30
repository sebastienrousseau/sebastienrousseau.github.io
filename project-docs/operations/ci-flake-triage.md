# Runbook — CI flake triage

**When:** a PR or `main` check fails but you suspect the failure is
infrastructure, not your change. Goal: distinguish a real defect from a
flake fast, and clear flakes without masking real failures.

**Rule:** never blanket-retry to get green. Read the failure first. Retry
only the specific patterns below, which are known-non-deterministic.

---

## Known flake patterns

### 1. pa11y shard hits the 50-minute timeout (`cancelled`)

**Symptom:** `pa11y shard N/4` shows `fail`/`cancelled` at ~50 min while the
other shards pass. The job log shows a wedged headless-Chrome process, not a
WCAG violation. The workflow caps each shard at `timeout-minutes: 50` for
exactly this (a hung Chrome can otherwise stall for hours).

**Triage:** open the failed shard's log and grep for real violations:

```bash
gh run view --job <job-id> --log-failed | grep -E 'WCAG2AAA|contrast|Error:'
```

- **No `WCAG2AAA…` lines** → it's the hang. Re-run just the failed jobs:
  ```bash
  gh run rerun <run-id> --failed
  ```
- **Real `WCAG2AAA…` lines** → it's a genuine a11y regression. Fix it (see
  the contrast / hidden-element patterns already used for `.story-hero` in
  `scripts/seo_and_audit/pa11y_cache.py`'s `hideElements`).

A re-run of a true flake passes in the normal ~34 min.

### 2. `NaN:1` contrast on an image-overlay hero

**Symptom:** `contrast ratio of NaN:1` on a page with white text over a
full-bleed background image. pa11y cannot read an image/gradient background.

**Fix (not a retry):** hide the decorative element from the contrast sweep
via `hideElements` in `scripts/seo_and_audit/pa11y_cache.py` (e.g.
`.story-hero`), and give it a solid dark `background-color` so the overlay
text is genuinely legible. This is a config change, not a flake.

### 3. Transient `gh`/network error

**Symptom:** `error connecting to api.github.com` from a `gh` command.

**Triage:** wait a few seconds and re-issue the exact command. This is a
client-side blip, not a CI failure.

### 4. Local build "lang-leakage" that CI does not show

**Symptom:** a **local** `./build.sh` prints
`lang-leakage: N EN-string leak(s)` (often on the `2024-03-18-…mm1` pages,
matching the word "Language" inside "Large Language Models") and exits 1,
but the same commit's CI `build-audit` is green.

**Cause:** the locally-installed `ssg` (0.0.45) escapes/over-scans in a way
the pinned CI toolchain (0.0.44, ADR-0002) does not. This is a **local-only
artifact** — trust CI, not the local 0.0.45 build, for this gate. Do not
"fix" content for it.

---

## Distinguishing real failures (do NOT retry)

| Job | Real failure looks like |
|---|---|
| Build + smoke tests | a named `pytest` assertion (e.g. `test_schemas` label mismatch), a validation-gate `FAIL:` line, a coverage drop |
| Static analysis | ruff/mypy/naming/jscpd error with a file:line |
| pa11y | `WCAG2AAA…` lines with a real contrast ratio / missing alt |
| diff / schema-diff | an actual structural diff the gate rejects |

For these, fix the root cause and push a new commit. A retry will just fail
again and waste a ~50-min cycle.

## Re-run commands

```bash
gh run rerun <run-id> --failed      # only the failed jobs in a run
gh run rerun <run-id>               # the whole run
gh run watch <run-id>               # follow to completion
```

## Acceptance

Either the re-run is green (confirmed flake) or you have a specific
root-cause fix pushed. Never merge on an unexplained red.
