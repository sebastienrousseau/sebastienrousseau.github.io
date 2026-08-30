# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""The language registry's malformed-data guards.

Every generator in the tree reads its per-locale data through these fourteen
loaders. The happy path is exercised constantly by the rest of the suite; the
guards were not exercised at all.

They are the reason a corrupt or half-written data file stops the build
instead of flowing onward. Without them a `labels.json` that parsed as a list
would return a list, and the first generator to call `.get()` on it would
fail somewhere unrelated — or worse, a loader returning an empty mapping
would render 34 locales with silently missing chrome and no error anywhere.

These tests are cheap: write a bad file to a tmp directory, assert the loader
refuses it and names the path.
"""

from __future__ import annotations

import json
from pathlib import Path

import _lang_registry as reg
import pytest

# (loader name, filename, a payload that parses as JSON but is the wrong shape)
_LOADERS: list[tuple[str, str, object]] = [
    ("load_author", "author.json", ["not", "a", "mapping"]),
    ("load_labels", "labels.json", ["not", "a", "mapping"]),
    ("load_listings", "listings.json", ["not", "a", "mapping"]),
    ("load_playlists", "playlists.json", ["not", "a", "mapping"]),
    ("load_projects", "projects.json", ["not", "a", "mapping"]),
    ("load_static_pages", "static_pages.json", ["not", "a", "mapping"]),
    ("load_strings", "strings.json", ["not", "a", "mapping"]),
    ("load_takeaway_labels", "takeaway_labels.json", ["not", "a", "mapping"]),
    ("load_topics", "topics.json", ["not", "a", "mapping"]),
    ("load_chrome_patches_inline", "chrome_patches.json", {"wrong_key": []}),
    ("load_home_patches", "home_patches.json", {"wrong_key": []}),
    ("load_static_patches", "static_patches.json", {"wrong_key": []}),
    ("load_static_bodies", "static_bodies.json", {"wrong_key": {}}),
]


@pytest.fixture
def locale_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    d = tmp_path / "xx"
    d.mkdir()
    monkeypatch.setattr(reg, "I18N_DIR", tmp_path)
    reg.load_slugs.cache_clear() if hasattr(reg.load_slugs, "cache_clear") else None
    return d


@pytest.mark.parametrize(("loader", "filename", "bad"), _LOADERS)
def test_loader_rejects_a_wrongly_shaped_file(
    locale_dir: Path, loader: str, filename: str, bad: object
) -> None:
    """Parses as JSON, wrong shape — the case a schema-less load lets through."""
    (locale_dir / filename).write_text(json.dumps(bad), encoding="utf-8")
    fn = getattr(reg, loader)
    if hasattr(fn, "cache_clear"):
        fn.cache_clear()
    with pytest.raises(reg.LanguageError) as exc:
        fn("xx")
    assert filename in str(exc.value), "the error must name the offending file"


@pytest.mark.parametrize(("loader", "filename", "_bad"), _LOADERS)
def test_loader_reports_a_missing_file(
    locale_dir: Path, loader: str, filename: str, _bad: object
) -> None:
    """A locale added to the registry but not yet populated must fail loudly,
    not return an empty mapping that renders as missing chrome."""
    fn = getattr(reg, loader)
    if hasattr(fn, "cache_clear"):
        fn.cache_clear()
    with pytest.raises(reg.LanguageError) as exc:
        fn("xx")
    assert filename in str(exc.value)


def test_load_slugs_requires_both_static_and_articles(locale_dir: Path) -> None:
    """Either key missing means every URL for that locale would fall back to
    English silently — the loader refuses rather than let that ship."""
    for payload in ({"static": {}}, {"articles": {}}, {"static": {}, "articles": []}):
        (locale_dir / "slugs.json").write_text(json.dumps(payload), encoding="utf-8")
        if hasattr(reg.load_slugs, "cache_clear"):
            reg.load_slugs.cache_clear()
        with pytest.raises(reg.LanguageError, match="required key"):
            reg.load_slugs("xx")


def test_load_slugs_accepts_a_well_formed_map(locale_dir: Path) -> None:
    (locale_dir / "slugs.json").write_text(
        json.dumps({"static": {"about": "a-propos"}, "articles": {}}), encoding="utf-8"
    )
    if hasattr(reg.load_slugs, "cache_clear"):
        reg.load_slugs.cache_clear()
    assert reg.load_slugs("xx")["static"]["about"] == "a-propos"


# ---------------------------------------------------------------------------
# Registry lookups
# ---------------------------------------------------------------------------


def test_get_returns_a_known_language() -> None:
    assert reg.get("fr").code == "fr"


def test_get_raises_on_an_unknown_code() -> None:
    """A typo'd locale code must not silently resolve to a default."""
    with pytest.raises(reg.LanguageError, match="unknown language code"):
        reg.get("not-a-locale")


def test_active_and_inactive_partition_the_registry() -> None:
    active = {lang.code for lang in reg.active()}
    everything = {lang.code for lang in reg.LANGUAGES}
    assert active <= everything
    assert all(lang.active for lang in reg.active())


def test_every_active_language_has_a_unique_code() -> None:
    codes = [lang.code for lang in reg.LANGUAGES]
    assert len(codes) == len(set(codes))
