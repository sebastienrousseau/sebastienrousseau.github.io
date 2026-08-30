# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Unit tests for the dark-mode pa11y sweep config.

Covers the ``build_dark_config`` generation in ``pa11y_cache.py`` and
the ``#dark`` marker round-trip in ``pa11y_retry_flakes.py`` — the two
pieces that keep the dark shard sound: Chrome must launch with the
prefers-color-scheme:dark flags, the theme assertion action must be
attached to every dark URL, and a flake retry must never silently
re-audit a dark URL in light mode.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts" / "seo_and_audit"))
import pa11y_cache as pc
import pa11y_retry_flakes as prf

BASE = "http://127.0.0.1:8000"
HIDE = "#x"


def _public_with(tmp_path: Path, relpaths: list[str]) -> Path:
    public = tmp_path / "public"
    for rel in relpaths:
        page = public / rel
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text("<html></html>", encoding="utf-8")
    return public


def test_dark_config_carries_flags_actions_and_marker(tmp_path: Path) -> None:
    public = _public_with(tmp_path, list(pc.DARK_SWEEP_RELPATHS))
    cfg = pc.build_dark_config(public, BASE + "/", HIDE)

    args = cfg["defaults"]["chromeLaunchConfig"]["args"]
    assert "--blink-settings=preferredColorScheme=0" in args
    assert "--force-dark-mode" in args
    assert cfg["defaults"]["standard"] == "WCAG2AAA"
    assert cfg["defaults"]["hideElements"] == HIDE

    assert len(cfg["urls"]) == len(pc.DARK_SWEEP_RELPATHS)
    for entry in cfg["urls"]:
        assert entry["url"].startswith(BASE + "/")
        assert entry["url"].endswith("#dark")
        assert entry["actions"] == pc.DARK_THEME_ACTIONS
        # entries must be independent copies, not shared references
        assert entry["actions"] is not pc.DARK_THEME_ACTIONS


def test_dark_config_drops_missing_pages(tmp_path: Path) -> None:
    """A renamed/removed representative page is dropped, not swept to a
    404."""
    present = list(pc.DARK_SWEEP_RELPATHS)[:3]
    public = _public_with(tmp_path, present)
    cfg = pc.build_dark_config(public, BASE, HIDE)
    swept = {e["url"].removeprefix(BASE + "/").removesuffix("#dark") for e in cfg["urls"]}
    assert swept == set(present)


def test_dark_config_does_not_disturb_light_fingerprint(tmp_path: Path) -> None:
    """Adding the dark sweep must not move the light config hash — a
    moved hash would force a full ~2,000-page re-sweep for nothing."""
    light = pc.build_pa11yci_config([], HIDE)
    assert pc.compute_config_hash(light) == pc.compute_config_hash(
        pc.build_pa11yci_config(["u1", "u2"], HIDE)
    )
    # and build_dark_config must not mutate the shared defaults
    public = _public_with(tmp_path, ["index.html"])
    pc.build_dark_config(public, BASE, HIDE)
    assert pc.build_pa11yci_config([], HIDE) == light


def test_cmd_pre_writes_dark_config(tmp_path: Path) -> None:
    public = _public_with(tmp_path, ["index.html", "trust/index.html"])
    dark_out = tmp_path / ".pa11yci.dark"
    rc = pc.main(
        [
            "pre",
            "--public-dir",
            str(public),
            "--cache",
            str(tmp_path / "cache.json"),
            "--pa11yci-out",
            str(tmp_path / ".pa11yci"),
            "--manifest-out",
            str(tmp_path / "manifest.json"),
            "--dark-out",
            str(dark_out),
            "--base-url",
            BASE,
            "--pa11y-version",
            "test",
            "--chromium-version",
            "test",
        ]
    )
    assert rc == 0
    cfg = json.loads(dark_out.read_text(encoding="utf-8"))
    urls = [e["url"] for e in cfg["urls"]]
    assert f"{BASE}/index.html#dark" in urls
    assert f"{BASE}/trust/index.html#dark" in urls


def test_retry_translates_dark_marker() -> None:
    entry = prf._retry_entry(f"{BASE}/trust/index.html#dark")
    assert isinstance(entry, dict)
    assert entry["actions"] == pc.DARK_THEME_ACTIONS
    assert entry["chromeLaunchConfig"]["args"] == pc.DARK_CHROME_ARGS


def test_retry_leaves_light_urls_untouched() -> None:
    url = f"{BASE}/index.html"
    assert prf._retry_entry(url) == url
