# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""The privacy notice names every third party the site sends visitors to.

The notice once said the site used Google Analytics and Microsoft Clarity,
which it never loaded, and left out Formspree and reCAPTCHA, which the
contact form does load. This gate scans what the site's layouts, scripts
and data actually load (script sources, form actions, iframes) and fails
when the notice does not name the provider, or when it claims a tracker
the site does not load.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
NOTICE = ROOT / "_posts" / "privacy.md"

# What the site may load, and the name the notice must use for it.
PROVIDERS = {
    "formspree.io/f/": "Formspree",
    "www.google.com/recaptcha": "reCAPTCHA",
    "cdn.jsdelivr.net": "jsDelivr",
    "open.spotify.com/embed": "Spotify",
    "googletagmanager.com": "Google Analytics",
    "google-analytics.com": "Google Analytics",
    "clarity.ms": "Microsoft Clarity",
    "plausible.io": "Plausible",
}
TRACKERS = ("Google Analytics", "Microsoft Clarity", "Plausible")
SOURCES = ("_layouts/*.html", "_layouts/*.js", "scripts/**/*.py", "_data/**/*.json", "_posts/*.md")


def _site_text() -> str:
    files = {p for pattern in SOURCES for p in ROOT.glob(pattern) if p != NOTICE}
    return "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in sorted(files))


def _loaded(site: str) -> set[str]:
    return {name for host, name in PROVIDERS.items() if host in site}


def _body(notice: str) -> str:
    return notice.split("\n---\n", 1)[-1]


def missing_from_notice(site: str, notice: str) -> list[str]:
    body = _body(notice)
    return sorted(name for name in _loaded(site) if name not in body)


def claimed_but_not_loaded(site: str, notice: str) -> list[str]:
    """Trackers the notice says the site uses, though nothing loads them.
    A sentence that says the site does *not* load one is fine."""
    loaded = _loaded(site)
    out = []
    for name in TRACKERS:
        if name in loaded:
            continue
        for sentence in re.split(r"(?<=[.!?])\s+", _body(notice)):
            if name in sentence and not re.search(r"\bno\b|\bnot\b|\bnever\b", sentence, re.I):
                out.append(name)
                break
    return out


def test_notice_names_every_provider_the_site_loads() -> None:
    assert missing_from_notice(_site_text(), NOTICE.read_text(encoding="utf-8")) == []


def test_notice_claims_no_tracker_the_site_does_not_load() -> None:
    assert claimed_but_not_loaded(_site_text(), NOTICE.read_text(encoding="utf-8")) == []


@pytest.mark.parametrize(
    ("site", "notice", "missing", "claimed"),
    [
        ('action="https://formspree.io/f/x"', "---\nWe use Formspree.", [], []),
        ('action="https://formspree.io/f/x"', "---\nNothing here.", ["Formspree"], []),
        ("", "---\nWe use Google Analytics to track traffic.", [], ["Google Analytics"]),
        ("", "---\nThe site loads no Google Analytics.", [], []),
        ("https://clarity.ms/tag", "---\nWe use Microsoft Clarity.", [], []),
    ],
)
def test_checks(site: str, notice: str, missing: list[str], claimed: list[str]) -> None:
    assert missing_from_notice(site, notice) == missing
    assert claimed_but_not_loaded(site, notice) == claimed
