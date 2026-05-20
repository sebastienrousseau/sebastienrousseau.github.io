#!/usr/bin/env python3
"""Pick a banner image from the local CDN inventory and emit the
CloudCDN transform URL.

Reads the inventory at
``/Users/seb/Code/Public/CDN/cloudcdn.pro/stocks/images/`` (override
with ``CDN_INVENTORY``), filters out images already used as banners
in any ``_posts/`` markdown frontmatter so a fresh article doesn't
re-use a banner, and returns one match.

Usage:
    python3 scripts/pick_banner.py                          # random unused
    python3 scripts/pick_banner.py --hint cloud,kubernetes  # keyword-biased
    python3 scripts/pick_banner.py --list 20                # just list 20 unused
    python3 scripts/pick_banner.py --check NAME             # verify NAME exists
                                                              and is unused

Output (success): a single line, the CDN transform URL — e.g.
    https://cloudcdn.pro/api/transform?url=/stocks/images/NAME.webp&w=1200&format=webp&q=80

Exit codes: 0 ok, 1 no candidate, 2 usage error.
"""
from __future__ import annotations

import argparse
import os
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INVENTORY = Path("/Users/seb/Code/Public/CDN/cloudcdn.pro/stocks/images")

_BANNER_LINE_RE = re.compile(
    r'banner:\s*"https://cloudcdn\.pro/[^"]*?/([^/"]+\.webp)"',
    re.IGNORECASE,
)

# Light keyword → image-token affinity so the picker can pre-bias toward
# topic-relevant candidates. Each tuple is (keyword, list-of-substrings
# preferred when present in the filename).
_AFFINITY: dict[str, tuple[str, ...]] = {
    "cloud":       ("cloud", "data-center", "server", "infrastructure"),
    "kubernetes":  ("kubernetes", "k8s", "container"),
    "quantum":     ("quantum", "cryptography", "lattice", "kyber"),
    "payments":    ("payment", "money", "bank", "card", "coin", "fintech"),
    "ai":          ("ai", "robot", "neural", "intelligence", "gpt", "llm", "gemini"),
    "rust":        ("rust", "code", "logo"),
    "blockchain":  ("blockchain", "crypto", "bitcoin", "token"),
    "governance":  ("regulation", "law", "compliance", "court"),
    "iso":         ("payment", "money", "swift", "rtgs"),
    "agentic":     ("ai", "robot", "agent"),
    "office":      ("office", "desk", "meeting"),
}


def collect_inventory(inv: Path) -> list[str]:
    if not inv.is_dir():
        return []
    return sorted(p.name for p in inv.iterdir() if p.suffix.lower() == ".webp")


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


def pick(inv: list[str], used: set[str], hints: list[str],
         exclude: set[str] | None = None,
         rng: random.Random | None = None) -> str | None:
    """Return one banner filename — keyword-biased if hints provided,
    otherwise random — that is in `inv`, not in `used`, not in `exclude`."""
    candidates = [
        n for n in inv if n not in used and (not exclude or n not in exclude)
    ]
    if not candidates:
        return None
    rng = rng or random.Random()  # noqa: S311 — banner picker, not crypto
    if hints:
        scored = sorted(
            ((score_candidate(n, hints), n) for n in candidates),
            key=lambda t: (-t[0], t[1]),
        )
        top_score = scored[0][0]
        if top_score > 0:
            tier = [n for s, n in scored if s == top_score]
            return rng.choice(tier)
    return rng.choice(candidates)


def transform_url(name: str, *, width: int = 1200, q: int = 80) -> str:
    """Emit the CloudCDN transform URL for a stock image."""
    return (
        "https://cloudcdn.pro/api/transform"
        f"?url=/stocks/images/{name}&w={width}&format=webp&q={q}"
    )


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--hint", default="",
                   help="comma-separated keyword hints "
                        "(cloud,kubernetes,quantum,payments,ai,rust,blockchain,iso,agentic)")
    p.add_argument("--list", type=int, default=0, metavar="N",
                   help="just list N unused candidates and exit")
    p.add_argument("--check", default="",
                   help="verify the named .webp exists in inventory + unused")
    p.add_argument("--width", type=int, default=1200)
    p.add_argument("--quality", type=int, default=80)
    p.add_argument("--inventory", type=Path,
                   default=Path(os.environ.get("CDN_INVENTORY", str(DEFAULT_INVENTORY))))
    p.add_argument("--seed", type=int, default=None,
                   help="deterministic picker for reproducible tests")
    args = p.parse_args()

    inv = collect_inventory(args.inventory)
    if not inv:
        print(f"pick_banner: empty inventory at {args.inventory}", file=sys.stderr)
        return 1
    used = collect_used_banners(ROOT / "_posts")
    rng = random.Random(args.seed) if args.seed is not None else None  # noqa: S311

    if args.check:
        name = args.check
        if name not in inv:
            print(f"pick_banner: {name} not in inventory", file=sys.stderr)
            return 1
        if name in used:
            print(f"pick_banner: {name} already used as a banner", file=sys.stderr)
            return 1
        print(transform_url(name, width=args.width, q=args.quality))
        return 0

    if args.list:
        candidates = [n for n in inv if n not in used]
        for n in candidates[: args.list]:
            print(n)
        return 0

    hints = [h.strip() for h in args.hint.split(",") if h.strip()]
    pick_name = pick(inv, used, hints, rng=rng)
    if not pick_name:
        print("pick_banner: no unused inventory image found", file=sys.stderr)
        return 1
    print(transform_url(pick_name, width=args.width, q=args.quality))
    return 0


if __name__ == "__main__":
    sys.exit(main())
