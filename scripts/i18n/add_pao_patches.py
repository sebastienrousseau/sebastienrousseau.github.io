#!/usr/bin/env python3
"""Append the six homepage Problem-Approach-Outcome patches to a locale's
``home_patches.json``.

Reads a translation seed JSON from stdin with this shape::

    {
      "labels": {"problem": "...", "approach": "...", "outcome": "...", "impact": "..."},
      "cards": {
        "pain001":   {"problem": "...", "approach": "...", "outcome": "...", "metric": "..."},
        "pacs008":   {...},
        "bsp":       {...},
        "hsh":       {...},
        "kyberlib":  {...},
        "noyalib":   {...}
      }
    }

The script builds six ``[regex_source, replacement]`` pairs using the EN
rendered HTML as the regex source and the localised strings as the
replacement, then appends them to the patches array. Existing patches
are left intact.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Each entry: card key -> (regex_source_template, replacement_template)
# Placeholders in the replacement: {problem}, {approach}, {outcome}, {labels.problem}, etc.
CARDS = {
    "pain001": {
        "regex": r"<dl class=pao><div><dt>Problem</dt><dd>Hand-authoring <strong>ISO 20022 pain\.001</strong> is fragile under SEPA and SWIFT cutovers\.</dd></div><div><dt>Approach</dt><dd>Schema-driven Python that maps CSV or SQLite into validated payment XML\.</dd></div><div><dt>Outcome</dt><dd>Ops ship pain\.001 in minutes; the audit trail survives the migration\.</dd></div></dl><p class=proj-metric><span class=proj-metric-label>Impact</span> ISO 20022 · SEPA \+ SWIFT</p>",
        "metric_en": "ISO 20022 · SEPA + SWIFT",
    },
    "pacs008": {
        "regex": r"<dl class=pao><div><dt>Problem</dt><dd>FI-to-FI credit transfers fail audit when XSD, IBAN and PII rules diverge\.</dd></div><div><dt>Approach</dt><dd>One library: JSON Schema, XSD, IBAN across 75 countries, GDPR-grade masking\.</dd></div><div><dt>Outcome</dt><dd>Cross-border credit transfers that pass first-time at the regulator\.</dd></div></dl><p class=proj-metric><span class=proj-metric-label>Impact</span> 75 countries · IBAN</p>",
        "metric_en": "75 countries · IBAN",
    },
    "bsp": {
        "regex": r"<dl class=pao><div><dt>Problem</dt><dd>Statement formats trap reconciliation teams in manual rekeying\.</dd></div><div><dt>Approach</dt><dd>One Python toolkit that normalises multi-format statements with audit-grade lineage\.</dd></div><div><dt>Outcome</dt><dd>Reconciliation runs without bespoke per-bank glue code\.</dd></div></dl><p class=proj-metric><span class=proj-metric-label>Impact</span> Multi-format · Audit-grade</p>",
        "metric_en": "Multi-format · Audit-grade",
    },
    "hsh": {
        "regex": r"<dl class=pao><div><dt>Problem</dt><dd>Pre-PQC hashing libraries leave credential stores quantum-exposed\.</dd></div><div><dt>Approach</dt><dd>Memory-safe Rust hash and digest library with a post-quantum posture\.</dd></div><div><dt>Outcome</dt><dd>Drop-in secure hashing for services planning PQC migration\.</dd></div></dl><p class=proj-metric><span class=proj-metric-label>Impact</span> Memory-safe · Rust</p>",
        "metric_en": "Memory-safe · Rust",
    },
    "kyberlib": {
        "regex": r"<dl class=pao><div><dt>Problem</dt><dd>Tier-1 banks carry harvest-now-decrypt-later exposure on every TLS session\.</dd></div><div><dt>Approach</dt><dd>Pure-Rust <strong>CRYSTALS-Kyber</strong> \(NIST FIPS 203\) that plugs into existing auth flows\.</dd></div><div><dt>Outcome</dt><dd>Post-quantum key exchange in production-grade Rust, independently validated\.</dd></div></dl><p class=proj-metric><span class=proj-metric-label>Impact</span> NIST FIPS 203</p>",
        "metric_en": "NIST FIPS 203",
    },
    "noyalib": {
        "regex": r"<dl class=pao><div><dt>Problem</dt><dd>AI, MCP and config pipelines run on YAML parsers with C-backed UB and silent spec drift\.</dd></div><div><dt>Approach</dt><dd>Pure-Rust YAML 1\.2 across library, CLI, LSP, MCP and WASM — zero unsafe, full spec\.</dd></div><div><dt>Outcome</dt><dd>YAML pipelines that stop being the supply-chain weak link\.</dd></div></dl><p class=proj-metric><span class=proj-metric-label>Impact</span> 406 \/ 406 spec · 0 unsafe</p>",
        "metric_en": "406 / 406 spec · 0 unsafe",
    },
}


def _build_replacement(card_key: str, card_strings: dict, labels: dict) -> str:
    metric = card_strings.get("metric", CARDS[card_key]["metric_en"])
    return (
        f"<dl class=pao><div><dt>{labels['problem']}</dt><dd>{card_strings['problem']}</dd></div>"
        f"<div><dt>{labels['approach']}</dt><dd>{card_strings['approach']}</dd></div>"
        f"<div><dt>{labels['outcome']}</dt><dd>{card_strings['outcome']}</dd></div></dl>"
        f"<p class=proj-metric><span class=proj-metric-label>{labels['impact']}</span> {metric}</p>"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("locale", help="locale code, e.g. fr")
    parser.add_argument("--seed", type=Path, help="path to translation seed JSON (default: stdin)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    seed_text = args.seed.read_text(encoding="utf-8") if args.seed else sys.stdin.read()
    seed = json.loads(seed_text)
    labels = seed["labels"]
    cards = seed["cards"]

    home_patches_path = ROOT / "_data" / "i18n" / args.locale / "home_patches.json"
    if not home_patches_path.exists():
        print(f"ERROR: {home_patches_path} does not exist", file=sys.stderr)
        return 1

    with home_patches_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    existing_regexes = {p[0] for p in data["patches"]}
    appended = 0
    for card_key, defs in CARDS.items():
        if card_key not in cards:
            print(f"WARN: missing card '{card_key}' in seed; skipping", file=sys.stderr)
            continue
        regex = defs["regex"]
        if regex in existing_regexes:
            continue
        replacement = _build_replacement(card_key, cards[card_key], labels)
        data["patches"].append([regex, replacement])
        appended += 1

    if args.dry_run:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0

    with home_patches_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"OK {args.locale} — appended {appended} PAO patches")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
