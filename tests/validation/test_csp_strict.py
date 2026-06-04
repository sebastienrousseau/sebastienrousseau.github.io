#!/usr/bin/env python3
"""CSP regression test — keep the Content-Security-Policy tight.

The policy is shipped via `<meta http-equiv="Content-Security-Policy">`
in every layout. Past regressions: someone adds `'unsafe-inline'` to
script-src or widens `img-src` to a blanket `https:` because a single
image stops loading. This gate fails the build on those changes.

Properties enforced (across every rendered page):
1. `script-src` has no `'unsafe-inline'` or `'unsafe-eval'`.
2. `style-src` has no `'unsafe-inline'` or `'unsafe-eval'`.
3. `img-src` has no bare `https:` allow — origins must be enumerated.
4. `default-src 'self'` is the policy's default.
5. `object-src 'none'` is present (no embedded plugins).
6. `base-uri 'self'` is present (no <base> shenanigans).
7. Every page that has inline JSON-LD also has the matching
   `'sha256-…'` token in script-src (postbuild.py contract).

Run from repo root: ``python3 tests/validation/test_csp_strict.py``.
"""
from __future__ import annotations

import sys as _sys  # path bootstrap — scripts reorg (scripts/lib/ on sys.path)
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[2] / "scripts" / "lib"))

import base64
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"

# Two orderings of the meta tag's attributes — Shokunin's minifier emits
# `content` either before or after `http-equiv` depending on page kind.
_CSP_META_RE_HTTP_FIRST = re.compile(
    r'<meta\b[^>]*?http-equiv=["\']?Content-Security-Policy["\']?[^>]*?'
    r'content=(["\'])((?:(?!\1).)+)\1',
    re.IGNORECASE | re.DOTALL,
)
_CSP_META_RE_CONTENT_FIRST = re.compile(
    r'<meta\b[^>]*?content=(["\'])((?:(?!\1).)+)\1[^>]*?'
    r'http-equiv=["\']?Content-Security-Policy["\']?',
    re.IGNORECASE | re.DOTALL,
)


def _extract_csp(html: str) -> str | None:
    """Pull the CSP content string out of the meta tag, tolerating the
    fact that the value itself contains apostrophes (`'self'`, `'none'`,
    `'unsafe-…'`) and that Shokunin's minifier may swap the
    attribute order. We match the opening quote with a backreference so
    inner apostrophes aren't mistaken for the closing quote."""
    m = _CSP_META_RE_HTTP_FIRST.search(html) or _CSP_META_RE_CONTENT_FIRST.search(html)
    return m.group(2) if m else None
_JSONLD_RE = re.compile(
    r'<script[^>]*type=["\']?application/ld\+json["\']?[^>]*>([\s\S]*?)</script>',
    re.IGNORECASE,
)
_HTML_COMMENT_RE = re.compile(r"<!--[\s\S]*?-->")


def _b64_sha256(data: bytes) -> str:
    return base64.b64encode(hashlib.sha256(data).digest()).decode("ascii")


def _parse_directives(policy: str) -> dict[str, list[str]]:
    """Parse a CSP string into ``{directive: [tokens…]}``. Whitespace
    is tolerant — Cloudflare's minifier may strip multiple spaces."""
    out: dict[str, list[str]] = {}
    for clause in policy.split(";"):
        clause = clause.strip()
        if not clause:
            continue
        parts = clause.split()
        out[parts[0].lower()] = parts[1:]
    return out


def _has_bad_token(tokens: list[str], bad: str) -> bool:
    return any(t.strip("'\"") == bad for t in tokens)


def check_policy(directives: dict[str, list[str]], rel: str) -> list[str]:
    """Static-shape checks on the policy itself."""
    defects: list[str] = []
    script = directives.get("script-src", [])
    if _has_bad_token(script, "unsafe-inline"):
        defects.append(f"{rel}: script-src contains 'unsafe-inline'")
    if _has_bad_token(script, "unsafe-eval"):
        defects.append(f"{rel}: script-src contains 'unsafe-eval'")
    style = directives.get("style-src", [])
    if _has_bad_token(style, "unsafe-inline"):
        defects.append(f"{rel}: style-src contains 'unsafe-inline'")
    if _has_bad_token(style, "unsafe-eval"):
        defects.append(f"{rel}: style-src contains 'unsafe-eval'")
    img = directives.get("img-src", [])
    if any(t == "https:" for t in img):
        defects.append(f"{rel}: img-src has bare 'https:' — enumerate origins")
    if "default-src" not in directives:
        defects.append(f"{rel}: default-src missing — must be 'self'")
    elif "'self'" not in directives["default-src"]:
        defects.append(f"{rel}: default-src must include 'self'")
    if "object-src" not in directives or "'none'" not in directives["object-src"]:
        defects.append(f"{rel}: object-src must be 'none'")
    if "base-uri" not in directives or "'self'" not in directives["base-uri"]:
        defects.append(f"{rel}: base-uri must be 'self'")
    return defects


def check_jsonld_hashes(policy: str, html: str, rel: str) -> list[str]:
    """Every inline JSON-LD body must have its sha256 covered by
    script-src — otherwise the browser blocks the block and breaks
    structured data. HTML comments are stripped first since the
    parser ignores `<script>` literals inside comments, and we
    mirror that behaviour to avoid false positives on the on-page
    docstring that describes how CSP works."""
    defects: list[str] = []
    scannable = _HTML_COMMENT_RE.sub("", html)
    for m in _JSONLD_RE.finditer(scannable):
        body = m.group(1)
        digest = _b64_sha256(body.encode("utf-8"))
        token = f"'sha256-{digest}'"
        if token not in policy:
            defects.append(
                f"{rel}: inline JSON-LD missing sha256 token {token[:25]}…",
            )
    return defects


def main() -> int:
    if not PUBLIC.is_dir():
        print("error: public/ not built — run ./build.sh first", file=sys.stderr)
        return 1
    pages = sorted(PUBLIC.rglob("index.html"))
    if not pages:
        print("warn: no pages found — skipping CSP check", file=sys.stderr)
        return 0
    problems: list[str] = []
    for page in pages:
        html = page.read_text(encoding="utf-8", errors="ignore")
        rel = page.relative_to(PUBLIC).as_posix()
        policy = _extract_csp(html)
        if policy is None:
            problems.append(f"{rel}: no CSP <meta> tag found")
            continue
        directives = _parse_directives(policy)
        problems.extend(check_policy(directives, rel))
        problems.extend(check_jsonld_hashes(policy, html, rel))
    if problems:
        print(f"csp-strict: {len(problems)} defect(s):", file=sys.stderr)
        for line in problems[:30]:
            print(f"  - {line}", file=sys.stderr)
        if len(problems) > 30:
            print(f"  …and {len(problems) - 30} more", file=sys.stderr)
        return 1
    print(f"ok: CSP strict-shape passes on {len(pages)} page(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
