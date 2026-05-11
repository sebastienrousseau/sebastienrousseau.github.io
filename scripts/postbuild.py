#!/usr/bin/env python3
"""Post-build pass on Shokunin's ``public/`` output.

Tasks performed:
1. **Real SRI** — replace every ``integrity="sha256-<short-hex>"`` placeholder
   that Shokunin emits on its ``/_csp/*`` assets with a real base64-encoded
   SHA-256 of the asset's actual byte content. Browsers will now enforce SRI.

2. **CSP for inline JSON-LD** — compute the SHA-256 of every
   ``<script type="application/ld+json">`` block inside each HTML page and
   inject those hashes into that page's ``script-src`` directive. The previous
   ``'unsafe-inline'`` carve-out is removed.
"""
from __future__ import annotations

import base64
import hashlib
import re
from pathlib import Path

PUBLIC = Path("public")


def b64_sha256(data: bytes) -> str:
    return base64.b64encode(hashlib.sha256(data).digest()).decode("ascii")


# ---------------------------------------------------------------------------
# 1. /_csp/* SRI fix
# ---------------------------------------------------------------------------

_csp_dir = PUBLIC / "_csp"
asset_hashes: dict[str, str] = {}
if _csp_dir.is_dir():
    for asset in _csp_dir.iterdir():
        if asset.is_file() and asset.suffix in (".js", ".css"):
            asset_hashes[asset.name] = b64_sha256(asset.read_bytes())

bogus_re = re.compile(r' integrity="sha256-[a-f0-9]+"')
asset_path_re = re.compile(r'(?:src|href)=["\']?/_csp/([^"\' ]+)')


def fix_sri(html: str) -> str:
    out: list[str] = []
    last = 0
    # Walk every <script>/<link> opening tag, look at its asset path + integrity.
    for m in re.finditer(r'<(?:script|link)[^>]+>', html):
        chunk = m.group(0)
        ap = asset_path_re.search(chunk)
        if not ap:
            continue
        digest = asset_hashes.get(ap.group(1))
        if not digest:
            continue
        # Strip any existing (bogus) integrity, then inject the real one.
        stripped = bogus_re.sub('', chunk)
        if 'integrity=' not in stripped:
            replaced = stripped.rstrip(' />') + f' integrity="sha256-{digest}" crossorigin="anonymous"' + stripped[-2:]
        else:
            replaced = stripped
        out.append(html[last:m.start()])
        out.append(replaced)
        last = m.end()
    out.append(html[last:])
    return "".join(out)


# ---------------------------------------------------------------------------
# 2. CSP hash for inline JSON-LD
# ---------------------------------------------------------------------------

# Capture the literal inline body of every <script type="application/ld+json"> tag.
# (Shokunin may emit either single- or double-quoted type attribute and may have
# attribute order vary, so the regex is intentionally loose.)
jsonld_re = re.compile(
    r'<script[^>]*type=["\']?application/ld\+json["\']?[^>]*>([\s\S]*?)</script>',
    re.IGNORECASE,
)
# Match the CSP meta tag whether attributes are quoted or not, in either order
# (Shokunin's minifier emits `<meta content="..." http-equiv=Content-Security-Policy>`).
csp_tag_re = re.compile(
    r'<meta\b[^>]*?http-equiv=["\']?Content-Security-Policy["\']?[^>]*?>',
    re.IGNORECASE,
)
content_attr_re = re.compile(
    r'(content=)(["\'])(.+?)(\2)',
    re.IGNORECASE | re.DOTALL,
)


def inject_jsonld_hashes(html: str) -> str:
    bodies = [m.group(1) for m in jsonld_re.finditer(html)]
    if not bodies:
        return html
    hashes = sorted({b64_sha256(b.encode("utf-8")) for b in bodies})
    hash_tokens = " ".join(f"'sha256-{h}'" for h in hashes)

    def patch_csp(tag_match: re.Match[str]) -> str:
        tag = tag_match.group(0)

        def patch_content(c: re.Match[str]) -> str:
            policy = c.group(3)
            new_policy = re.sub(r"(script-src[^;]*?)\s*'unsafe-inline'", r"\1", policy)
            new_policy = re.sub(
                r"(script-src)(\s+)",
                r"\1 " + hash_tokens + r"\2",
                new_policy,
                count=1,
            )
            return c.group(1) + c.group(2) + new_policy + c.group(4)

        return content_attr_re.sub(patch_content, tag, count=1)

    return csp_tag_re.sub(patch_csp, html, count=1)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main() -> None:
    pages = list(PUBLIC.rglob("*.html"))
    sri_patched = 0
    csp_patched = 0
    for page in pages:
        original = page.read_text(encoding="utf-8", errors="ignore")
        patched = fix_sri(original)
        if patched != original:
            sri_patched += 1
        patched2 = inject_jsonld_hashes(patched)
        if patched2 != patched:
            csp_patched += 1
        if patched2 != original:
            page.write_text(patched2, encoding="utf-8")
    print(
        f"postbuild: {len(pages)} HTML pages, "
        f"{sri_patched} got real SRI, {csp_patched} got CSP JSON-LD hashes"
    )


if __name__ == "__main__":
    main()
