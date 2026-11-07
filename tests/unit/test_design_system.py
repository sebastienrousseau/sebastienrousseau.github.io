# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Design system v2 gate.

1. Parity: every ``_layouts/*.html`` shell carries ``assets/css/
   design-system.css`` verbatim, after the legacy block wrapped in
   ``@layer legacy``. A hand edit to one layout, or a generator run that
   skipped ``design_system.apply``, fails here.
2. Mechanics: ``apply`` is idempotent and ``strip`` undoes it exactly.
3. Invariants on the stylesheet itself, so the scale cannot drift again:
   three column widths only, every font size from a ``--fs-*`` token, every
   fluid token carrying a ``rem`` term (WCAG 1.4.4 text resize), no
   ``!important``, no raw colours.
"""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
LAYOUTS = ROOT / "_layouts"
CSS_PATH = ROOT / "assets" / "css" / "design-system.css"

_SPEC = importlib.util.spec_from_file_location(
    "design_system", ROOT / "scripts" / "generators" / "design_system.py"
)
assert _SPEC is not None and _SPEC.loader is not None
ds = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(ds)

LAYOUT_FILES = sorted(LAYOUTS.glob("*.html"))
CSS = CSS_PATH.read_text(encoding="utf-8")
CSS_NO_COMMENTS = re.sub(r"/\*.*?\*/", "", CSS, flags=re.S)


@pytest.mark.parametrize("path", LAYOUT_FILES, ids=lambda p: p.name)
def test_layout_carries_current_design_system(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    assert ds.LAYER_OPEN in html, f"{path.name}: legacy block not wrapped in @layer legacy"
    assert ds.applied_css(html) == ds.design_system_css(), (
        f"{path.name}: design-system block differs from assets/css/design-system.css; "
        "run python3 scripts/generators/gen_layouts.py"
    )


@pytest.mark.parametrize("path", LAYOUT_FILES, ids=lambda p: p.name)
def test_apply_is_idempotent(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    assert ds.apply(html) == html


def test_strip_round_trips() -> None:
    shell = "<head>\n    <style>\n      .a{color:red}\n    </style>\n</head>"
    applied = ds.apply(shell, css=".b{}")
    assert "@layer legacy" in applied and ".b{}" in applied
    assert ds.strip(applied).replace("\n\n", "\n") == shell.replace("\n\n", "\n")


def test_page_css_appended_after_apply_lands_in_legacy_layer() -> None:
    shell = ds.apply("    <style>\n      .a{}\n    </style>", css=".ds{}")
    # What gen_layouts does for page-scoped CSS: append before </style>.
    injected = shell.replace("    </style>", "      .page{}\n    </style>")
    out = ds.apply(injected, css=".ds{}")
    legacy = out[out.index(ds.LAYER_OPEN) : out.index(ds.LAYER_CLOSE)]
    assert ".page{}" in legacy, "page CSS must sit inside @layer legacy, before the design system"
    assert out.index(".page{}") < out.index(".ds{}")


def test_only_three_column_widths() -> None:
    widths = set(re.findall(r"max-width:\s*([^;]+);", CSS_NO_COMMENTS))
    allowed = {"var(--max)", "var(--measure)", "calc(var(--max) + 2 * var(--pad-x))"}
    assert widths <= allowed, f"unexpected column widths: {widths - allowed}"


def test_every_font_size_uses_a_token() -> None:
    sizes = re.findall(r"(?<!-)font-size:\s*([^;]+);", CSS_NO_COMMENTS)
    assert sizes, "no font-size declarations found"
    bad = [s for s in sizes if not re.fullmatch(r"var\(--fs-[a-z0-9-]+\)", s.strip())]
    assert not bad, f"font sizes must come from --fs-* tokens: {bad}"


def test_fluid_tokens_respect_text_resize() -> None:
    tokens = re.findall(r"--fs-[a-z0-9-]+:\s*(clamp\([^;]+\));", CSS_NO_COMMENTS)
    assert len(tokens) >= 12
    for t in tokens:
        lo, mid, hi = (p.strip() for p in t[len("clamp(") : -1].split(",", 2))
        assert lo.endswith("rem") and hi.endswith("rem"), f"bounds must be rem: {t}"
        assert "rem" in mid and "vw" in mid, f"preferred value needs rem + vw: {t}"


def test_no_important_and_no_raw_colours() -> None:
    assert "!important" not in CSS_NO_COMMENTS
    assert not re.search(r"#[0-9a-fA-F]{3,8}\b", CSS_NO_COMMENTS)
