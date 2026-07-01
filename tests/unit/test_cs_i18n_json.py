"""Guard for the case-study i18n data extraction — Phase 4.1.

The per-locale case-study UI labels were moved out of build_case_studies.py
into _data/proof/case-studies-i18n.json (data/code separation). This pins the
data contract so the loader + _lbl merge can't silently break: the file must
exist, carry v1/v2/v3, cover every active locale plus EN, and _lbl must layer
v3 over v2 over v1 with EN fallback.
"""

from __future__ import annotations

import json
from pathlib import Path

import build_case_studies as cs

I18N_PATH = Path(__file__).resolve().parents[2] / "_data" / "proof" / "case-studies-i18n.json"


def test_i18n_json_exists_and_has_three_layers() -> None:
    data = json.loads(I18N_PATH.read_text(encoding="utf-8"))
    assert set(data) >= {"v1", "v2", "v3"}
    assert data["v1"]["en"]["Role"] == "Role"


def test_loaded_dicts_match_json() -> None:
    data = json.loads(I18N_PATH.read_text(encoding="utf-8"))
    assert data["v1"] == cs._CS_LABELS
    assert data["v2"] == cs._CS_LABELS_V2
    assert data["v3"] == cs._CS_LABELS_V3


def test_every_layer_covers_en() -> None:
    for layer in (cs._CS_LABELS, cs._CS_LABELS_V2, cs._CS_LABELS_V3):
        assert "en" in layer


def test_lbl_layers_v3_over_v2_over_v1_with_en_fallback() -> None:
    en = cs._lbl("en")
    # V1 key
    assert en["Role"] == "Role"
    # V2 key present in merged set
    assert en["Home"] == "Home"
    # V3 key present in merged set
    assert en["Next"] == "Next"
    # A locale falls back to EN for any key missing in its layers.
    fr = cs._lbl("fr")
    assert fr["Role"] == "Rôle"  # translated V1
    assert set(en) == set(fr)  # same key universe (EN fallback fills gaps)


def test_lbl_unknown_locale_is_pure_en() -> None:
    assert cs._lbl("xx") == cs._lbl("en")
