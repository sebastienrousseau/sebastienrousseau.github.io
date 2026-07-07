#!/usr/bin/env python3
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


def _provenance_section() -> str:
    verify = "gh attestation verify sbom.cdx.json \\\n  --owner sebastienrousseau"
    cards = (
        '<article class="offer-card"><h3>Software bill of materials</h3>'
        "<p>A CycloneDX SBOM is generated and validated in CI on every build. "
        '<a href="/sbom.cdx.json">Download sbom.cdx.json</a>.</p></article>'
        '<article class="offer-card"><h3>Build provenance (SLSA)</h3>'
        "<p>The deployed SBOM carries a signed build-provenance attestation. "
        "Verify it yourself:</p>"
        f'<pre id="slsa-verify">{_esc(verify)}</pre>'
        '<button type="button" class="copy-btn" data-copy="#slsa-verify" '
        'aria-label="SLSA verify command — Copy">Copy</button></article>'
        '<article class="offer-card"><h3>Signed publications</h3>'
        "<p>Every article is Sigstore-signed and dated, so a reader can prove "
        "authorship and integrity independently.</p></article>"
        '<article class="offer-card"><h3>OpenSSF Scorecard</h3>'
        "<p>Supply-chain posture is scored weekly. "
        '<a href="https://scorecard.dev/viewer/?uri=github.com/sebastienrousseau/sebastienrousseau.github.io" '
        'rel="noopener">View the live Scorecard</a>.</p></article>'
    )
    return (
        '<section class="feat alt" aria-labelledby="trust-provenance">'
        '<div class="wrap"><p class="feat-eyebrow">Provenance</p>'
        '<h2 id="trust-provenance" class="feat-headline">Evidence, not assurances.</h2>'
        f'<div class="offer-cards">{cards}</div></div></section>'
    )


def _licensing_section() -> str:
    rows = "".join(
        f'<tr><th scope="row"><a href="{_esc(repo)}" rel="noopener">'
        f"{_esc(name)}</a></th><td>{_esc(what)}</td><td>{_esc(lic)}</td></tr>"
        for name, what, lic, repo in _LICENSING
    )
    return (
        '<section class="feat" aria-labelledby="trust-licensing"><div class="wrap">'
        '<p class="feat-eyebrow">Licensing</p>'
        '<h2 id="trust-licensing" class="feat-headline">Free to use, fork, and audit.</h2>'
        '<table><thead><tr><th scope="col">Library</th>'
        '<th scope="col">Scope</th><th scope="col">License</th></tr></thead>'
        f"<tbody>{rows}</tbody></table>"
        "<p>Every library is permissively licensed and runs on your own "
        "infrastructure — no proprietary translator between your systems and "
        "the clearing network, no vendor lock-in.</p>"
        "</div></section>"
    )


def _governance_section() -> str:
    return (
        '<section class="feat alt" aria-labelledby="trust-governance">'
        '<div class="wrap"><p class="feat-eyebrow">Governance</p>'
        '<h2 id="trust-governance" class="feat-headline">'
        "The single-maintainer question, answered honestly.</h2>"
        "<p>These libraries are authored and maintained by one person. For "
        "regulated adoption that raises a fair bus-factor question, so here is "
        "the mitigation, stated plainly rather than hidden:</p>"
        "<ul>"
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
        meta = " · ".join(x for x in (_esc(org), _esc(date), _esc(role)) if x)
        rows.append(f"<li><strong>{name_html}</strong><br>{meta}</li>")
    return (
        '<section class="feat" aria-labelledby="trust-recognition"><div class="wrap">'
        '<p class="feat-eyebrow">Recognition</p>'
        '<h2 id="trust-recognition" class="feat-headline">'
        "Conferred, not claimed.</h2>"
        "<p>Every item below links to a dated, externally verifiable artefact.</p>"
        f'<ul class="trust-recognition-list">{"".join(rows)}</ul>'
        "</div></section>"
    )


def _render_body(items: list[dict]) -> str:
    hero = (
        '<section class="feat" aria-labelledby="trust-h1"><div class="wrap">'
        '<p class="feat-eyebrow">Enterprise governance &amp; trust</p>'
        '<h1 id="trust-h1" class="feat-headline">Built to be audited.</h1>'
        "<p>Provenance, licensing, and governance for the open-source payments "
        "and post-quantum libraries — the evidence a vendor-risk or compliance "
        "review needs, in one place.</p>"
        '<p><a class="pill" href="/case-studies/">See the case studies</a></p>'
        "</div></section>"
    )
    return (
        hero
        + _provenance_section()
        + _licensing_section()
        + _governance_section()
        + _recognition_section(items)
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
    target = PUBLIC / "trust" / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(out, encoding="utf-8")
    print(f"build_trust: wrote {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
