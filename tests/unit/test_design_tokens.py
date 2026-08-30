# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Design-token drift gate.

Two invariants, both aimed at stopping visual-system drift at review
time instead of after deploy:

1. **Hex-literal freeze** — ``_layouts/*.html`` ``<style>`` blocks may
   not gain NEW raw hex colour literals. Colours belong in the token
   definition blocks (custom-property declarations such as
   ``--link-color: light-dark(#004caf, #8cc0ff)``); rule bodies must
   consume ``var(--…)``. Hex literals inside a ``--token:`` declaration
   are always allowed. Every hex literal that exists OUTSIDE a token
   declaration today is snapshotted in the committed baseline
   (``tests/unit/golden/design_tokens_hex_baseline.json``) as frozen
   legacy debt: the gate fails only when a file gains a hex value it
   did not have, or more occurrences of one it did (i.e. new drift),
   listing the offenders. Removing literals never fails the gate.

2. **``<details>`` accordion contract** — every ``<details>`` element
   in the built site (``public/``, the generator-emitted pages) must
   carry ``class="qa-item"`` so it inherits the accordion styling and
   JS behaviour, except the known legit non-accordion uses:
   ``cite-popover``, ``tag-posts``, ``cs-dropdown``,
   ``about-identifiers``. Pages under ``/labs/`` are standalone WASM
   demo shells outside the design system and are excluded (same
   convention as ``test_build_output.py``). This check is
   SKIP_IF_NO_BUILD-guarded, so it runs in CI's post-build
   ``pytest tests/unit/`` pass.

Baseline regeneration
---------------------

When a hex literal is added or moved DELIBERATELY (e.g. a new token
block, an approved one-off), regenerate the frozen baseline and commit
it together with the layout change:

    python3 tests/unit/test_design_tokens.py --regen

This rewrites ``tests/unit/golden/design_tokens_hex_baseline.json``
from the current ``_layouts/`` state. Review the diff: every added
entry is a colour literal you are choosing to freeze outside the token
system.

The committed JSON is an envelope ``{"_jscpd", "layouts", "_jscpd_end"}``
whose marker strings carry jscpd's inline ignore comments: layouts that
share a style block legitimately repeat identical hex histograms, so the
snapshot is frozen golden data, not refactorable duplication.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
LAYOUTS = ROOT / "_layouts"
PUBLIC = ROOT / "public"
BASELINE_PATH = Path(__file__).parent / "golden" / "design_tokens_hex_baseline.json"

SKIP_IF_NO_BUILD = pytest.mark.skipif(
    not PUBLIC.is_dir() or not (PUBLIC / "index.html").is_file(),
    reason="public/ not built — run ./build.sh first",
)

# ---------------------------------------------------------------------------
# Part 1 — hex literals in _layouts/*.html <style> blocks
# ---------------------------------------------------------------------------

_STYLE_BLOCK_RE = re.compile(r"<style\b[^>]*>(.*?)</style>", re.IGNORECASE | re.DOTALL)

# 3/4/6/8-digit CSS hex colours. The negative lookahead rejects longer
# ident tails so id selectors like ``#fade-in`` or ``#cafe-menu`` never
# false-positive.
_HEX_RE = re.compile(r"#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})(?![0-9a-zA-Z_-])")

# A hex literal is a *token definition* when its declaration starts
# with a custom property name: ``--foo: … #hex …;``.
_TOKEN_DECL_RE = re.compile(r"^\s*--[\w-]+\s*:")


def _is_token_definition(css: str, match_start: int) -> bool:
    """True when the hex at ``match_start`` sits inside a custom-property
    declaration. Scan back to the nearest declaration boundary (``{`` or
    ``;``) and test whether the declaration starts with ``--name:``."""
    boundary = max(css.rfind("{", 0, match_start), css.rfind(";", 0, match_start))
    return bool(_TOKEN_DECL_RE.match(css[boundary + 1 : match_start]))


def collect_hex_literals(layout: Path) -> dict[str, int]:
    """Hex colour literals (lowercased) outside token definitions in the
    file's ``<style>`` blocks, mapped to occurrence counts."""
    counts: dict[str, int] = {}
    text = layout.read_text(encoding="utf-8")
    for block in _STYLE_BLOCK_RE.finditer(text):
        css = block.group(1)
        for m in _HEX_RE.finditer(css):
            if _is_token_definition(css, m.start()):
                continue
            key = m.group(0).lower()
            counts[key] = counts.get(key, 0) + 1
    return counts


def snapshot_layouts() -> dict[str, dict[str, int]]:
    """Current { layout-filename: { hex: count } } state, sorted for a
    stable committed JSON diff."""
    snap: dict[str, dict[str, int]] = {}
    for layout in sorted(LAYOUTS.glob("*.html")):
        counts = collect_hex_literals(layout)
        if counts:
            snap[layout.name] = dict(sorted(counts.items()))
    return snap


# The committed baseline is a golden snapshot: layouts that share a
# style block repeat identical hex histograms by construction, so the
# file wraps the data in an envelope whose marker strings tell jscpd to
# skip it (see module docstring, "Baseline regeneration").
_BASELINE_MARKER_START = "jscpd:ignore-start"
_BASELINE_MARKER_END = "jscpd:ignore-end"


def _load_baseline() -> dict[str, dict[str, int]]:
    return json.loads(BASELINE_PATH.read_text(encoding="utf-8"))["layouts"]


def test_no_new_hex_literals_in_layout_styles() -> None:
    """Fail when any _layouts/*.html <style> block gains a hex colour
    literal (value or extra occurrence) not in the frozen baseline."""
    assert BASELINE_PATH.is_file(), (
        f"missing baseline {BASELINE_PATH}; regenerate with "
        f"`python3 {Path(__file__).relative_to(ROOT)} --regen` and commit it"
    )
    baseline = _load_baseline()
    offenders: list[str] = []
    for name, counts in snapshot_layouts().items():
        frozen = baseline.get(name, {})
        for hexval, n in counts.items():
            allowed = frozen.get(hexval, 0)
            if n > allowed:
                offenders.append(
                    f"_layouts/{name}: {hexval} x{n} (baseline allows {allowed}) — "
                    "define it as a --token or consume an existing var(--…)"
                )
    assert not offenders, (
        "NEW hex colour literal(s) in _layouts <style> blocks (outside token "
        "definitions):\n  " + "\n  ".join(offenders) + "\nIf deliberate, regenerate the "
        "baseline (see module docstring) and commit the diff."
    )


def test_hex_baseline_is_current_format() -> None:
    """Guard the committed baseline shape so a hand-edit can't silently
    disable the gate (or drop the jscpd ignore envelope around the
    golden data)."""
    raw = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    assert set(raw) == {"_jscpd", "layouts", "_jscpd_end"}, (
        "baseline must be the {_jscpd, layouts, _jscpd_end} envelope"
    )
    assert _BASELINE_MARKER_START in raw["_jscpd"], "lost the jscpd ignore-start marker"
    assert _BASELINE_MARKER_END in raw["_jscpd_end"], "lost the jscpd ignore-end marker"
    baseline = raw["layouts"]
    assert isinstance(baseline, dict) and baseline, "baseline must be a non-empty object"
    for name, counts in baseline.items():
        assert (LAYOUTS / name).is_file(), f"baseline references missing layout {name}"
        for hexval, n in counts.items():
            assert _HEX_RE.fullmatch(hexval), f"bad hex key {hexval!r} in baseline[{name}]"
            assert isinstance(n, int) and n > 0, f"bad count for {name}:{hexval}"


# ---------------------------------------------------------------------------
# Part 2 — <details> accordion contract on generator-emitted pages
# ---------------------------------------------------------------------------

_DETAILS_TAG_RE = re.compile(r"<details\b[^>]*>", re.IGNORECASE)
_CLASS_ATTR_RE = re.compile(r'class\s*=\s*["\']([^"\']*)["\']', re.IGNORECASE)

# Legit non-accordion <details> uses. Anything else must be a qa-item.
ALLOWED_DETAILS_CLASSES = frozenset(
    {"qa-item", "cite-popover", "tag-posts", "cs-dropdown", "about-identifiers"}
)


def _details_offenders(page: Path) -> list[str]:
    html = page.read_text(encoding="utf-8", errors="ignore")
    out = []
    for m in _DETAILS_TAG_RE.finditer(html):
        cm = _CLASS_ATTR_RE.search(m.group(0))
        classes = set(cm.group(1).split()) if cm else set()
        if not classes & ALLOWED_DETAILS_CLASSES:
            out.append(m.group(0))
    return out


@SKIP_IF_NO_BUILD
def test_details_elements_carry_qa_item_class() -> None:
    """Every <details> in built pages must be class=qa-item or one of the
    allowlisted non-accordion variants. /labs/ WASM shells excluded."""
    offenders: list[str] = []
    for page in sorted(PUBLIC.rglob("*.html")):
        rel = page.relative_to(PUBLIC).as_posix()
        if rel.startswith("labs/"):
            continue
        offenders.extend(f"{rel}: {tag}" for tag in _details_offenders(page))
    assert not offenders, (
        "<details> without class=qa-item (or an allowlisted variant "
        f"{sorted(ALLOWED_DETAILS_CLASSES)}) in generator-emitted pages:\n  "
        + "\n  ".join(offenders[:40])
        + (f"\n  … and {len(offenders) - 40} more" if len(offenders) > 40 else "")
    )


# ---------------------------------------------------------------------------
# Baseline regeneration entry point (see module docstring)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if "--regen" not in sys.argv:
        print(__doc__)
        raise SystemExit(2)
    BASELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
    snap = snapshot_layouts()
    payload = {
        "_jscpd": (
            f"{_BASELINE_MARKER_START} -- golden baseline: layouts sharing a "
            "style block repeat identical hex histograms by construction; "
            "this is frozen snapshot data, not refactorable duplication"
        ),
        "layouts": dict(sorted(snap.items())),
        "_jscpd_end": _BASELINE_MARKER_END,
    }
    BASELINE_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    total = sum(sum(c.values()) for c in snap.values())
    print(f"wrote {BASELINE_PATH} — {len(snap)} layout file(s), {total} frozen hex literal(s)")
