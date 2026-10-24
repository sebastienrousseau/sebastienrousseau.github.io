#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Pick a banner image from the local CDN inventory and emit its
CloudCDN URL.

Reads the inventory at
the cloudcdn.pro checkout beside this one,
``../../JavaScript/cloudcdn.pro/stocks/images/`` (override with
``CDN_INVENTORY``), filters out images already used as banners
in any ``_posts/`` markdown frontmatter so a fresh article doesn't
re-use a banner, and returns one match.

Usage:
    python3 scripts/pick_banner.py                          # random unused
    python3 scripts/pick_banner.py --hint cloud,kubernetes  # keyword-biased
    python3 scripts/pick_banner.py --list 20                # just list 20 unused
    python3 scripts/pick_banner.py --check NAME             # verify NAME exists
                                                              and is unused

Output (success): a single line, the image's CDN URL — e.g.
    https://cloudcdn.pro/stocks/images/NAME.webp

The transform endpoint closed on 2026-06-23. Banners link the file itself;
postbuild adds the -320/-640/-1200/-1920 variants as a srcset.

Exit codes: 0 ok, 1 no candidate, 2 usage error.
"""

from __future__ import annotations

import sys as _sys  # path bootstrap — scripts reorg (scripts/lib/ on sys.path)
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "lib"))

import argparse
import os
import random
import re
import sys
from pathlib import Path

from _core import ROOT, load_banner_affinity

# Default inventory: the cloudcdn.pro checkout beside this one
# (Code/Public/JavaScript/ next to Code/Public/Web/). Override via the
# CDN_INVENTORY env var when running elsewhere (cloud routine, CI,
# contributor machines).
DEFAULT_INVENTORY = (
    Path(__file__).resolve().parents[2].parents[1] / "JavaScript/cloudcdn.pro/stocks/images"
)

# Responsive sizes the CDN serves beside each image (NAME-640.webp and so
# on). They are sizes of another image, never a banner in their own right.
_VARIANT_RE = re.compile(r"-(?:320|640|1200|1920)\.webp$", re.IGNORECASE)

_BANNER_LINE_RE = re.compile(
    r'banner:\s*"https://cloudcdn\.pro/[^"]*?/([^/"]+\.webp)"',
    re.IGNORECASE,
)

# Keyword → image-filename-substring affinity, loaded from
# _data/banner_tags.json so editorial tagging can be updated without
# touching script logic.
_AFFINITY: dict[str, tuple[str, ...]] = load_banner_affinity()


def collect_inventory(inv: Path) -> list[str]:
    if not inv.is_dir():
        return []
    return sorted(
        p.name
        for p in inv.iterdir()
        if p.suffix.lower() == ".webp" and not _VARIANT_RE.search(p.name)
    )


def collect_used_banners(posts_dir: Path) -> set[str]:
    used: set[str] = set()
    if not posts_dir.is_dir():
        return used
    for md in posts_dir.rglob("*.md"):
        try:
            text = md.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for m in _BANNER_LINE_RE.finditer(text):
            used.add(m.group(1))
    return used


def score_candidate(name: str, hints: list[str]) -> int:
    """Higher score = better match for the provided keyword hints."""
    if not hints:
        return 0
    lower = name.lower()
    score = 0
    for h in hints:
        wanted = _AFFINITY.get(h.lower(), (h.lower(),))
        score += sum(1 for w in wanted if w in lower)
    return score


def pick(
    inv: list[str],
    used: set[str],
    hints: list[str],
    exclude: set[str] | None = None,
    rng: random.Random | None = None,
) -> str | None:
    """Return one banner filename — keyword-biased if hints provided,
    otherwise random — that is in `inv`, not in `used`, not in `exclude`."""
    candidates = [n for n in inv if n not in used and (not exclude or n not in exclude)]
    if not candidates:
        return None
    rng = rng or random.Random()  # noqa: S311 — banner picker, not crypto
    return _hint_biased_pick(candidates, hints, rng) or rng.choice(candidates)


def _hint_biased_pick(candidates: list[str], hints: list[str], rng: random.Random) -> str | None:
    """One of the best-scoring candidates, or ``None`` when no hint matched.

    Ties are broken randomly rather than by name so repeat runs with the
    same hints don't keep handing back the same banner.
    """
    if not hints:
        return None
    scored = sorted(
        ((score_candidate(n, hints), n) for n in candidates),
        key=lambda t: (-t[0], t[1]),
    )
    top_score = scored[0][0]
    if top_score <= 0:
        return None
    return rng.choice([n for s, n in scored if s == top_score])


def banner_url(name: str) -> str:
    """The CloudCDN URL for a stock image, as a post's ``banner:`` holds it."""
    return f"https://cloudcdn.pro/stocks/images/{name}"


def _build_parser() -> argparse.ArgumentParser:
    """CLI surface — see the module docstring for the contract."""
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--hint",
        default="",
        help="comma-separated keyword hints "
        "(cloud,kubernetes,quantum,payments,ai,rust,blockchain,iso,agentic)",
    )
    p.add_argument(
        "--list", type=int, default=0, metavar="N", help="just list N unused candidates and exit"
    )
    p.add_argument(
        "--check", default="", help="verify the named .webp exists in inventory + unused"
    )
    p.add_argument(
        "--inventory",
        type=Path,
        default=Path(os.environ.get("CDN_INVENTORY", str(DEFAULT_INVENTORY))),
    )
    p.add_argument(
        "--seed", type=int, default=None, help="deterministic picker for reproducible tests"
    )
    return p


def _cmd_check(name: str, inv: list[str], used: set[str]) -> int:
    """``--check NAME``: confirm NAME is in inventory and not already a banner."""
    if name not in inv:
        print(f"pick_banner: {name} not in inventory", file=sys.stderr)
        return 1
    if name in used:
        print(f"pick_banner: {name} already used as a banner", file=sys.stderr)
        return 1
    print(banner_url(name))
    return 0


def _cmd_list(inv: list[str], used: set[str], limit: int) -> int:
    """``--list N``: print up to N unused inventory names, one per line."""
    for n in [n for n in inv if n not in used][:limit]:
        print(n)
    return 0


def _cmd_pick(inv: list[str], used: set[str], args: argparse.Namespace) -> int:
    """Default command: pick one unused banner and print its CDN URL."""
    rng = random.Random(args.seed) if args.seed is not None else None  # noqa: S311
    hints = [h.strip() for h in args.hint.split(",") if h.strip()]
    name = pick(inv, used, hints, rng=rng)
    if not name:
        print("pick_banner: no unused inventory image found", file=sys.stderr)
        return 1
    print(banner_url(name))
    return 0


def main() -> int:
    args = _build_parser().parse_args()
    inv = collect_inventory(args.inventory)
    if not inv:
        print(f"pick_banner: empty inventory at {args.inventory}", file=sys.stderr)
        return 1
    used = collect_used_banners(ROOT / "_posts")
    if args.check:
        return _cmd_check(args.check, inv, used)
    if args.list:
        return _cmd_list(inv, used, args.list)
    return _cmd_pick(inv, used, args)


if __name__ == "__main__":
    sys.exit(main())
