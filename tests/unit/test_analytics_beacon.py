"""Traffic beacon: inert unless configured, and correct when it is (F-07).

The site carried no analytics at all — the only occurrence of
``cloudflareinsights`` anywhere was in the CSP allowlist, permitting a script
that was never included. These tests pin both halves of the contract: nothing
ships without a token, and what ships with one is right.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "postbuild"))

from postbuild_lib.analytics import BEACON_SRC, beacon_token, inject_analytics_beacon

# Not a credential — a Cloudflare Web Analytics beacon token is public,
# it ships in the page markup. Shape-valid dummy for the format check.
TOKEN = "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"  # noqa: S105
PAGE = "<html><body><p>Body.</p></body></html>"


@pytest.fixture(autouse=True)
def _no_ambient_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CF_BEACON_TOKEN", raising=False)


# --------------------------------------------------------------- token source


def test_no_config_means_no_token(tmp_path: Path) -> None:
    assert beacon_token(tmp_path / "absent.json") is None


def test_environment_supplies_the_token(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("CF_BEACON_TOKEN", TOKEN)
    assert beacon_token(tmp_path / "absent.json") == TOKEN


def test_config_file_supplies_the_token(tmp_path: Path) -> None:
    cfg = tmp_path / "analytics.json"
    cfg.write_text(json.dumps({"cloudflare_beacon_token": TOKEN}), encoding="utf-8")
    assert beacon_token(cfg) == TOKEN


def test_environment_wins_over_the_file(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """CI must be able to inject a token without a working-tree change."""
    cfg = tmp_path / "analytics.json"
    other = "f" * 32
    cfg.write_text(json.dumps({"cloudflare_beacon_token": other}), encoding="utf-8")
    monkeypatch.setenv("CF_BEACON_TOKEN", TOKEN)
    assert beacon_token(cfg) == TOKEN


@pytest.mark.parametrize("bad", ["", "not-hex", "abc", "A" * 32, "a" * 31, "a" * 33])
def test_malformed_tokens_are_rejected(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, bad: str
) -> None:
    """A malformed value must not reach the markup as a broken script tag."""
    monkeypatch.setenv("CF_BEACON_TOKEN", bad)
    assert beacon_token(tmp_path / "absent.json") is None


def test_unreadable_config_is_not_fatal(tmp_path: Path) -> None:
    cfg = tmp_path / "analytics.json"
    cfg.write_text("{ this is not json", encoding="utf-8")
    assert beacon_token(cfg) is None


def test_config_without_the_key_yields_no_token(tmp_path: Path) -> None:
    cfg = tmp_path / "analytics.json"
    cfg.write_text(json.dumps({"something_else": TOKEN}), encoding="utf-8")
    assert beacon_token(cfg) is None


# ------------------------------------------------------------------ injection


def test_no_token_injects_nothing() -> None:
    """A fork or an unconfigured local build stays beacon-free."""
    assert inject_analytics_beacon(PAGE, None) == PAGE


def test_beacon_is_injected_before_body_close() -> None:
    out = inject_analytics_beacon(PAGE, TOKEN)
    assert out.index(BEACON_SRC) < out.index("</body>")


def test_beacon_carries_the_token() -> None:
    out = inject_analytics_beacon(PAGE, TOKEN)
    assert f'data-cf-beacon=\'{{"token": "{TOKEN}"}}\'' in out


def test_beacon_is_deferred() -> None:
    """Measurement must never sit on the LCP path."""
    assert "<script defer" in inject_analytics_beacon(PAGE, TOKEN)


def test_injection_is_idempotent() -> None:
    once = inject_analytics_beacon(PAGE, TOKEN)
    assert inject_analytics_beacon(once, TOKEN) == once


def test_page_without_body_close_is_unchanged() -> None:
    fragment = "<div>no body element</div>"
    assert inject_analytics_beacon(fragment, TOKEN) == fragment
