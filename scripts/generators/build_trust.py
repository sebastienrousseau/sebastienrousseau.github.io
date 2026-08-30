#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Generate the ``/trust/`` enterprise-governance page.

Assembles the provenance evidence the platform already produces (SBOM,
SLSA build-provenance attestation, Sigstore-signed articles, OpenSSF
Scorecard), the open licensing of the payments/PQC libraries, an honest
single-maintainer governance statement with its mitigations and a stated
intent to pursue foundation stewardship, and the externally verifiable
recognition items from ``recognition.yml``. This is the page a vendor-risk
or compliance reader reaches for when evaluating single-maintainer open
source for regulated use.

No ROI numbers are invented and no foundation donation is asserted —
governance is described as intent, provenance as fact.

Runs from ``build.sh`` AFTER ``build_translations`` (English tree only,
like ``build_changelog``) and BEFORE ``postbuild``.

Output: ``public/trust/index.html``
Input:  ``_data/proof/recognition.yml``
        ``public/articles/index.html`` (shell template)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml  # type: ignore[import-untyped]
except ImportError:  # pragma: no cover
    print("build_trust: pyyaml not installed", file=sys.stderr)
    raise

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
from build_case_studies import _swap_into_shell
from case_studies_components import _esc

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
RECOGNITION_YML = ROOT / "_data" / "proof" / "recognition.yml"
SHELL_SRC = PUBLIC / "articles" / "index.html"
BASE_URL = "https://sebastienrousseau.com"
URL = f"{BASE_URL}/trust/"

DESC = (
    "Provenance, licensing, and governance for Sebastien Rousseau's open-source "
    "payments and post-quantum libraries: SBOM, SLSA attestation, Sigstore signing, "
    "OpenSSF Scorecard, and Apache-2.0 / MIT licensing."
)

# Flagship libraries positioned for regulated use — license is a fact
# (Apache-2.0 / MIT) verifiable from each repository.
_LICENSING = [
    (
        "pain001",
        "ISO 20022 pain.001 generation",
        "Apache-2.0 / MIT",
        "https://github.com/sebastienrousseau/pain001",
    ),
    (
        "pacs008",
        "ISO 20022 pacs.008 FI-to-FI transfer",
        "Apache-2.0 / MIT",
        "https://github.com/sebastienrousseau/pacs008",
    ),
    (
        "KyberLib",
        "ML-KEM (CRYSTALS-Kyber, NIST FIPS 203)",
        "Apache-2.0 / MIT",
        "https://github.com/sebastienrousseau/kyberlib",
    ),
    (
        "BankStatementParser",
        "Structured statement parsing",
        "Apache-2.0 / MIT",
        "https://github.com/sebastienrousseau/bankstatementparser",
    ),
]


def _icon(name: str) -> str:
    """Apple-style line icon (24 viewBox, currentColor stroke, CSP-safe)."""
    return (
        '<span class="tr-card-icon" aria-hidden="true">'
        '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" '
        'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
        f'stroke-linejoin="round">{_ICONS[name]}</svg></span>'
    )


_ICONS = {
    # file-text: the SBOM inventory document
    "sbom": (
        '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 '
        '2-2V8z"/><path d="M14 2v6h6"/><path d="M8 13h8M8 17h8"/>'
    ),
    # shield-check: the signed attestation
    "slsa": ('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>'),
    # pen: the signature on every article
    "sign": ('<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>'),
    # gauge: the weekly score
    "score": (
        '<circle cx="12" cy="12" r="10"/><path d="m16 8-4.5 4.5"/>'
        '<path d="M12 6v.01M6 12h.01M18 12h.01M8 8l.01.01M16 16l.01.01"/>'
    ),
}


def _provenance_section() -> str:
    verify = "gh attestation verify sbom.cdx.json \\\n  --owner sebastienrousseau"
    cards = (
        f'<article class="tr-card">{_icon("sbom")}'
        "<h3>Software bill of materials</h3>"
        "<p>A CycloneDX SBOM is generated and validated in CI on every build.</p>"
        '<p class="tr-card-act"><a href="/sbom.cdx.json">Download sbom.cdx.json</a></p>'
        "</article>"
        f'<article class="tr-card">{_icon("slsa")}'
        "<h3>Build provenance (SLSA)</h3>"
        "<p>The deployed SBOM carries a signed build-provenance attestation. "
        "Verify it yourself:</p>"
        f'<pre id="slsa-verify">{_esc(verify)}</pre>'
        '<p class="tr-card-act"><button type="button" class="ap-cta-mini tr-copy" '
        'data-copy="#slsa-verify" '
        'aria-label="SLSA verify command — Copy">Copy</button></p></article>'
        f'<article class="tr-card">{_icon("sign")}'
        "<h3>Signed publications</h3>"
        "<p>Every article is Sigstore-signed and dated, so a reader can prove "
        "authorship and integrity independently.</p></article>"
        f'<article class="tr-card">{_icon("score")}'
        "<h3>OpenSSF Scorecard</h3>"
        "<p>Supply-chain posture is scored weekly.</p>"
        '<p class="tr-card-act">'
        '<a href="https://scorecard.dev/viewer/?uri=github.com/sebastienrousseau/sebastienrousseau.github.io" '
        'rel="noopener">View the live Scorecard</a></p></article>'
    )
    return (
        '<section aria-labelledby="trust-provenance">'
        '<div class="tr-wrap"><header class="tr-head">'
        '<p class="tr-kicker">Provenance</p>'
        '<h2 id="trust-provenance">Evidence, not assurances.</h2></header>'
        f'<div class="tr-cards">{cards}</div></div></section>'
    )


# Preview panel, the Economist-style content sampler. Both cards preview
# real, already-published content; titles and excerpts are quoted from the
# target pages (the case-study hub card and the article's own h1 + meta
# description), so the panel adds layout, not claims.
_PREV_CASE_IMG = (
    '<img alt="Aerial cityscape at dusk — symbolising structured payment '
    'file automation under ISO 20022 across global clearing networks" '
    'src="https://cloudcdn.pro/stocks/images/tyler-prahm-lmV3gJSAgbo-1200.webp" '
    'loading="lazy" decoding="async" width="800" height="500" '
    'srcset="https://cloudcdn.pro/stocks/images/tyler-prahm-lmV3gJSAgbo-640.webp 640w, '
    "https://cloudcdn.pro/stocks/images/tyler-prahm-lmV3gJSAgbo-1200.webp 1200w, "
    'https://cloudcdn.pro/stocks/images/tyler-prahm-lmV3gJSAgbo-1920.webp 1920w" '
    'sizes="(max-width:900px) 100vw, 570px">'
)
# Portrait source (640x1035 intrinsic at 640w); the card crops it to 16/10
# anchored to the faceted facade at the frame's foot (.tr-prev-img-b).
_PREV_PAPER_IMG = (
    '<img alt="Faceted triangular glass panels at the top of a modern '
    'building against a pale sky" '
    'src="https://cloudcdn.pro/stocks/images/adrien-olichon-3137055-1200.webp" '
    'loading="lazy" decoding="async" width="800" height="500" '
    'class="tr-prev-img-b" '
    'srcset="https://cloudcdn.pro/stocks/images/adrien-olichon-3137055-640.webp 640w, '
    "https://cloudcdn.pro/stocks/images/adrien-olichon-3137055-1200.webp 1200w, "
    'https://cloudcdn.pro/stocks/images/adrien-olichon-3137055-1920.webp 1920w" '
    'sizes="(max-width:900px) 100vw, 570px">'
)


def _preview_section() -> str:
    return (
        '<section class="tr-tint" aria-labelledby="trust-preview">'
        '<div class="tr-wrap"><header class="tr-head">'
        '<p class="tr-kicker">Preview</p>'
        '<h2 id="trust-preview">The evidence, applied.</h2></header>'
        '<div class="tr-preview">'
        f'<article class="tr-prev-card">{_PREV_CASE_IMG}'
        '<div class="tr-prev-body"><p class="tr-kicker">Case study</p>'
        '<h3><a href="/case-studies/pain001/">pain001: automating ISO 20022 '
        "payment files</a></h3>"
        "<p>The global MT &rarr; MX migration forces every bank and corporate "
        "treasury to produce structured pain.001 messages.</p>"
        '<p class="tr-prev-more"><a href="/case-studies/pain001/">Read the '
        'case study <span aria-hidden="true">&rsaquo;</span></a></p>'
        "</div></article>"
        f'<article class="tr-prev-card">{_PREV_PAPER_IMG}'
        '<div class="tr-prev-body"><p class="tr-kicker">Signed article</p>'
        '<h3><a href="/2026-04-11-quantum-thresholds-are-moving-again/">'
        "Quantum Thresholds Are Moving: 10,000-Qubit Shor Risk</a></h3>"
        "<p>Shor&rsquo;s algorithm may now run on as few as 10,000 qubits. RSA, ECC "
        "and the timeline for post-quantum migration are all moving up.</p>"
        '<p class="tr-prev-more">'
        '<a href="/2026-04-11-quantum-thresholds-are-moving-again/">Read the '
        'article <span aria-hidden="true">&rsaquo;</span></a></p>'
        "</div></article></div></div></section>"
    )


def _licensing_section() -> str:
    rows = "".join(
        f'<tr><th scope="row"><a href="{_esc(repo)}" rel="noopener">'
        f"{_esc(name)}</a></th><td>{_esc(what)}</td><td>{_esc(lic)}</td></tr>"
        for name, what, lic, repo in _LICENSING
    )
    return (
        '<section aria-labelledby="trust-licensing">'
        '<div class="tr-wrap tr-cols">'
        '<header class="tr-col-head"><p class="tr-kicker">Licensing</p>'
        '<h2 id="trust-licensing">Free to use, fork, and audit.</h2></header>'
        '<div class="tr-col-body">'
        '<div class="tr-table-wrap">'
        '<table class="tr-table"><thead><tr><th scope="col">Library</th>'
        '<th scope="col">Scope</th><th scope="col">License</th></tr></thead>'
        f"<tbody>{rows}</tbody></table></div>"
        '<p class="tr-note">Every library is permissively licensed and runs on '
        "your own infrastructure — no proprietary translator between your "
        "systems and the clearing network, no vendor lock-in.</p>"
        "</div></div></section>"
    )


def _governance_section() -> str:
    return (
        '<section class="tr-tint" aria-labelledby="trust-governance">'
        '<div class="tr-wrap tr-cols">'
        '<header class="tr-col-head"><p class="tr-kicker">Governance</p>'
        '<h2 id="trust-governance">'
        "The single-maintainer question, answered honestly.</h2>"
        '<p class="tr-lede">These libraries are authored and maintained by one '
        "person. For regulated adoption that raises a fair bus-factor "
        "question, so here is the mitigation, stated plainly rather than "
        "hidden:</p></header>"
        '<ul class="tr-gov-list">'
        "<li><strong>Open source, permissively licensed.</strong> Apache-2.0 / "
        "MIT means your organisation can fork, vendor, and continue maintaining "
        "the code independently of the original author.</li>"
        "<li><strong>Reproducible, signed releases.</strong> SBOM, SLSA "
        "provenance, and Sigstore signing let you verify exactly what you run.</li>"
        "<li><strong>Inspectable, not a black box.</strong> Every library ships "
        "as a reference implementation with tests and documentation.</li>"
        "<li><strong>Foundation stewardship is the stated direction.</strong> "
        "The intent for the payments libraries is to pursue neutral stewardship "
        "(for example FINOS or the Linux Foundation) to add multi-maintainer "
        "redundancy. This is a roadmap intent, not a completed donation.</li>"
        "</ul></div></section>"
    )


def _recognition_section(items: list[dict]) -> str:
    if not items:
        return ""
    rows = []
    for it in items:
        title = it.get("title", "")
        org = it.get("org", "")
        date = it.get("date", "")
        url = it.get("url", "")
        role = it.get("role", "")
        name_html = (
            f'<a href="{_esc(url)}" rel="noopener">{_esc(title)}</a>' if url else _esc(title)
        )
        rows.append(
            f'<li><span class="tr-rec-title">{name_html}</span>'
            f'<span class="tr-rec-org">{_esc(org)}</span>'
            f'<span class="tr-rec-date">{_esc(date)}</span>'
            f'<span class="tr-rec-role">{_esc(role)}</span></li>'
        )
    return (
        '<section aria-labelledby="trust-recognition">'
        '<div class="tr-wrap tr-cols">'
        '<header class="tr-col-head"><p class="tr-kicker">Recognition</p>'
        '<h2 id="trust-recognition">Conferred, not claimed.</h2>'
        '<p class="tr-lede">Every item below links to a dated, externally '
        "verifiable artefact.</p></header>"
        f'<ul class="tr-rec">{"".join(rows)}</ul>'
        "</div></section>"
    )


def _final_section() -> str:
    return (
        '<section class="tr-tint tr-final" aria-labelledby="trust-cta">'
        '<div class="tr-wrap"><p class="tr-kicker">Next step</p>'
        '<h2 id="trust-cta">Bring the evidence to your review.</h2>'
        '<div class="tr-cta">'
        '<a class="pill" href="/contact/index.html">Get in touch</a>'
        '<a class="pill ghost" href="/sbom.cdx.json">Download sbom.cdx.json</a>'
        "</div></div></section>"
    )


def _render_body(items: list[dict]) -> str:
    hero = (
        '<section class="tr-hero tr-tint" aria-labelledby="trust-h1">'
        '<div class="tr-wrap">'
        '<p class="tr-kicker">Enterprise governance &amp; trust</p>'
        '<h1 id="trust-h1">Built to be audited.</h1>'
        '<p class="tr-lede">Provenance, licensing, and governance for the '
        "open-source payments and post-quantum libraries — the evidence a "
        "vendor-risk or compliance review needs, in one place.</p>"
        '<div class="tr-cta">'
        '<a class="pill" href="/case-studies/">See the case studies</a></div>'
        "</div></section>"
    )
    return (
        '<div class="trust-page">'
        + hero
        + _provenance_section()
        + _preview_section()
        + _licensing_section()
        + _governance_section()
        + _recognition_section(items)
        + _final_section()
        + "</div>"
    )


def main() -> int:
    if not SHELL_SRC.is_file():
        print(f"build_trust: shell missing at {SHELL_SRC}", file=sys.stderr)
        return 1
    items: list[dict] = []
    if RECOGNITION_YML.is_file():
        data = yaml.safe_load(RECOGNITION_YML.read_text(encoding="utf-8")) or {}
        items = data.get("items", []) or []

    shell = SHELL_SRC.read_text(encoding="utf-8")
    body = _render_body(items)
    out = _swap_into_shell(shell, body, "Trust & governance — Sebastien Rousseau", DESC, URL)
    # EN-only page: the copied /articles hreflang alternates are wrong here
    # and a page with no alternates is valid (test_hreflang_reciprocity),
    # same policy as build_iso20022_mcp. Conditional: the raw ssg shell
    # carries no hreflang links (postbuild injects them), so a fresh build
    # has nothing to strip and that is normal, not an error.
    out, _ = re.subn(
        r'[ \t]*<link\s+rel="alternate"\s+hreflang="[^"]*"\s+href="[^"]*"\s*/?>\n?',
        "",
        out,
    )
    target = PUBLIC / "trust" / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(out, encoding="utf-8")
    print(f"build_trust: wrote {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
