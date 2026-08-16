"""Unit tests for postbuild_assets.normalise_csp.

ssg generates its own listing pages (tag indexes) without going through our
_layouts/, and ships them a weaker default policy — `style-src` carrying
'unsafe-inline', and `base-uri 'none'` where the CSP gate requires 'self'.
postbuild only ever *patched* an existing policy (adding JSON-LD hashes), so
those pages sailed through with the generator's policy intact and failed the
gate on every one.

The subtle part is that the generated page computes a sha256 for its own
inline bootstrap. Overwriting the policy wholesale would strip that hash and
block the script at runtime — the page would pass the gate and break in the
browser, which is strictly worse than failing.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
_SPEC = importlib.util.spec_from_file_location(
    "postbuild_assets_under_test", ROOT / "scripts" / "postbuild" / "postbuild_assets.py"
)
pba = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = pba
_SPEC.loader.exec_module(pba)

CANONICAL = (
    "default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self'; style-src 'self'"
)
GENERATOR = (
    "default-src 'self'; base-uri 'none'; object-src 'none'; "
    "script-src 'sha256-ABC123=' 'none'; style-src 'self' 'unsafe-inline'"
)
GEN_HASH = "'sha256-ABC123='"


def _page(policy: str) -> str:
    return (
        "<html><head>"
        f'<meta http-equiv="Content-Security-Policy" content="{policy}" />'
        "</head><body>x</body></html>"
    )


def _stub_canonical(monkeypatch, policy: str = CANONICAL) -> None:
    monkeypatch.setattr(pba, "canonical_csp", lambda: policy)


# ---------------------------------------------------------------------------
# _needs_normalising
# ---------------------------------------------------------------------------


def test_flags_unsafe_inline_in_style_src():
    assert pba._needs_normalising("base-uri 'self'; style-src 'self' 'unsafe-inline'") is True


def test_flags_unsafe_inline_in_script_src():
    assert pba._needs_normalising("base-uri 'self'; script-src 'self' 'unsafe-inline'") is True


def test_flags_base_uri_that_is_not_self():
    assert pba._needs_normalising("base-uri 'none'; style-src 'self'") is True


def test_accepts_a_canonical_shaped_policy():
    assert pba._needs_normalising(CANONICAL) is False


# ---------------------------------------------------------------------------
# normalise_csp
# ---------------------------------------------------------------------------


def test_replaces_generator_policy(monkeypatch):
    _stub_canonical(monkeypatch)
    out, changed = pba.normalise_csp(_page(GENERATOR))
    assert changed is True
    assert "'unsafe-inline'" not in out
    assert "base-uri 'self'" in out


def test_preserves_generator_inline_script_hash(monkeypatch):
    """Dropping this hash blocks the page's own bootstrap at runtime."""
    _stub_canonical(monkeypatch)
    out, _ = pba.normalise_csp(_page(GENERATOR))
    assert GEN_HASH in out


def test_hash_is_merged_into_script_src_not_appended_loose(monkeypatch):
    _stub_canonical(monkeypatch)
    out, _ = pba.normalise_csp(_page(GENERATOR))
    script_src = next(d for d in out.split('content="')[1].split(";") if "script-src" in d)
    assert GEN_HASH in script_src


def test_leaves_a_compliant_policy_untouched(monkeypatch):
    _stub_canonical(monkeypatch)
    page = _page(CANONICAL)
    out, changed = pba.normalise_csp(page)
    assert changed is False
    assert out == page


def test_is_idempotent(monkeypatch):
    _stub_canonical(monkeypatch)
    once, first = pba.normalise_csp(_page(GENERATOR))
    twice, second = pba.normalise_csp(once)
    assert first is True
    assert second is False
    assert twice == once


def test_no_csp_meta_is_a_no_op(monkeypatch):
    _stub_canonical(monkeypatch)
    page = "<html><head><title>x</title></head></html>"
    assert pba.normalise_csp(page) == (page, False)


def test_meta_without_content_attribute_is_a_no_op(monkeypatch):
    _stub_canonical(monkeypatch)
    page = '<html><head><meta http-equiv="Content-Security-Policy" /></head></html>'
    assert pba.normalise_csp(page) == (page, False)


def test_handles_minified_attribute_order(monkeypatch):
    """ssg's minifier emits content=... before an unquoted http-equiv."""
    _stub_canonical(monkeypatch)
    page = (
        f'<html><head><meta content="{GENERATOR}" http-equiv=Content-Security-Policy></head></html>'
    )
    out, changed = pba.normalise_csp(page)
    assert changed is True
    assert "'unsafe-inline'" not in out
    assert GEN_HASH in out


# ---------------------------------------------------------------------------
# canonical_csp
# ---------------------------------------------------------------------------


def test_canonical_csp_is_read_from_the_layout():
    """The layout is the single source of truth; a hard-coded copy would drift."""
    policy = pba.canonical_csp()
    assert "default-src 'self'" in policy
    assert "base-uri 'self'" in policy
    assert pba._needs_normalising(policy) is False
