# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""scripts/seo_and_audit/target_queries.py (plan G-9)."""

from __future__ import annotations

from pathlib import Path

import target_queries as tq
import yaml


def test_thirty_queries_ten_per_hub() -> None:
    targets = yaml.safe_load(tq.TARGETS.read_text(encoding="utf-8"))
    assert sorted(targets) == ["applied-ai", "iso-20022", "post-quantum-cryptography"]
    assert all(len(q) == 10 for q in targets.values())


def test_report_from_an_export(tmp_path: Path) -> None:
    export = tmp_path / "Queries.csv"
    export.write_text(
        "Top queries,Clicks,Impressions,CTR,Position\npacs.008 explained,3,120,2.5%,8.4\n",
        encoding="utf-8",
    )
    data = tq.load_export(export)
    text = tq.render({"iso-20022": ["pacs.008 explained", "pain.001 explained"]}, data)
    assert "| pacs.008 explained | 3 | 120 | 8.4 |" in text
    assert "| pain.001 explained | 0 | 0 | not ranking |" in text
    out = tmp_path / "r.md"
    assert tq.main(["--export", str(export), "--out", str(out)]) == 0 and out.read_text(
        encoding="utf-8"
    ).startswith("# Target")
