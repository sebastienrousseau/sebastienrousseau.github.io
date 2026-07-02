"""Unit coverage for check_taxonomy validators — Phase 1.3.

check_taxonomy.py validates _data/taxonomy.yml (required fields, allowed
pillars, alias-collision detection) and builds the alias→slug map. It was
untested. Cover the pure validation + alias-map logic.
"""

from __future__ import annotations

import check_taxonomy as ct

_GOOD = {"name": "AI", "plural": "AI", "description": "d", "category": "ai"}


# --- _validate_entry -------------------------------------------------------


def test_validate_entry_ok() -> None:
    assert ct._validate_entry("ai", _GOOD) == []


def test_validate_entry_non_mapping() -> None:
    assert ct._validate_entry("ai", ["not", "a", "dict"]) == ["ai: entry is not a mapping"]


def test_validate_entry_missing_fields_and_bad_category() -> None:
    problems = ct._validate_entry("x", {"name": "X", "category": "nope"})
    assert any("missing required field 'plural'" in p for p in problems)
    assert any("missing required field 'description'" in p for p in problems)
    assert any("not in allowed pillars" in p for p in problems)


# --- _check_alias_collisions -----------------------------------------------


def test_alias_collision_none() -> None:
    seen: dict[str, str] = {}
    assert ct._check_alias_collisions("ai", {"aliases": ["ml"]}, seen) == []
    assert seen == {"ai": "ai", "ml": "ai"}


def test_alias_collision_detected() -> None:
    seen = {"ml": "ai"}
    out = ct._check_alias_collisions("payments", {"aliases": ["ML"]}, seen)  # ML→ml collides
    assert out == ["payments: alias 'ML' already maps to 'ai'"]


# --- validate_taxonomy -----------------------------------------------------


def test_validate_taxonomy_clean() -> None:
    assert ct.validate_taxonomy({"ai": _GOOD}) == []


def test_validate_taxonomy_reports_problems() -> None:
    tax = {"ai": _GOOD, "bad": {"name": "B"}}
    problems = ct.validate_taxonomy(tax)
    assert any(p.startswith("bad:") for p in problems)


# --- alias_map -------------------------------------------------------------


def test_alias_map_lowercases_and_includes_aliases() -> None:
    amap = ct.alias_map({"AI": {"aliases": [" ML ", "Deep-Learning"]}})
    assert amap["ai"] == "AI"
    assert amap["ml"] == "AI"
    assert amap["deep-learning"] == "AI"
