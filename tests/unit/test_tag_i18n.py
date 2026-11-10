# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Translated tag names and descriptions for the indexed locales.

Until v0.0.33 ``_data/taxonomy.yml`` was the only source of a tag's name
and description, so every locale's tag landing served the English deck,
meta description and ``og:description``: on ``/fr/etiquettes/dora/`` the
one paragraph that describes the page was English. The indexed locales
(``_data/seo/locale-indexing.json``) now carry ``_data/i18n/<lang>/tags.json``.

Two halves:

* the data, checked without a build: every tag with a landing page has a
  translated entry in every indexed locale, the description is never the
  English one, a name equal to the English name is listed in
  ``_intentionally_english`` (and only then), and standard, product and
  acronym names in the English description survive translation;
* the built pages (skipped when ``public/`` is absent): no indexed-locale
  tag landing serves the English description, and its H1 is English only
  for a tag listed as intentionally English.
"""

from __future__ import annotations

import html as _html
import json
import re
from functools import cache
from pathlib import Path

import build_tag_landings as btl
import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
I18N = ROOT / "_data" / "i18n"

# Standard, regulation, product, protocol and acronym names that stay as
# they are in every translation. Each one listed here that appears in an
# English description must appear verbatim in every translation of it.
PROTECTED = (
    "ISO 20022",
    "DORA",
    "Digital Operational Resilience Act",
    "SWIFT",
    "CBPR+",
    "Cross-Border Payments and Reporting Plus",
    "pacs.008",
    "pain.001",
    "camt",
    "MT101",
    "FIPS 203",
    "FIPS 204",
    "CRYSTALS-Kyber",
    "CRYSTALS-Dilithium",
    "NIST",
    "AI RMF",
    "SP 800/1800",
    "EU AI Act",
    "PSD2",
    "PSD3",
    "CMA9",
    "FDX",
    "RTP",
    "FedNow",
    "SEPA Instant",
    "Faster Payments",
    "GPI",
    "G20",
    "EBA",
    "HNDL",
    "RAG",
    "LLM",
    "Kubernetes",
    "DeFi",
    "CDN",
    "Model Context Protocol",
    "Rust",
)


def _kept_locales() -> list[str]:
    data = json.loads((ROOT / "_data" / "seo" / "locale-indexing.json").read_text("utf-8"))
    return [code for code in data["indexed"] if code != "en"]


KEPT = _kept_locales()


@cache
def _taxonomy() -> dict:
    return yaml.safe_load((ROOT / "_data" / "taxonomy.yml").read_text(encoding="utf-8"))


@cache
def _landing_slugs() -> tuple[str, ...]:
    taxonomy = _taxonomy()
    posts, _ = btl._walk(taxonomy)
    return tuple(s for s in taxonomy if len(posts.get(s, [])) >= btl._LANDING_THRESHOLD)


@cache
def _raw(lang: str) -> dict:
    return json.loads((I18N / lang / "tags.json").read_text(encoding="utf-8"))


def _entries(lang: str) -> dict[str, dict]:
    return {k: v for k, v in _raw(lang).items() if not k.startswith("_")}


def _en(slug: str) -> tuple[str, str]:
    entry = _taxonomy()[slug]
    return entry["name"], " ".join(entry["description"].split())


def test_there_are_ten_indexed_locales() -> None:
    assert len(KEPT) == 10


@pytest.mark.parametrize("lang", KEPT)
def test_every_landing_tag_has_a_translation(lang: str) -> None:
    entries = _entries(lang)
    missing = [s for s in _landing_slugs() if s not in entries]
    unknown = [s for s in entries if s not in _taxonomy()]
    assert missing == [] and unknown == []


@pytest.mark.parametrize("lang", KEPT)
def test_entries_are_well_formed(lang: str) -> None:
    for slug, entry in _entries(lang).items():
        assert set(entry) == {"name", "description", "reviewed"}, slug
        assert isinstance(entry["name"], str) and entry["name"].strip(), slug
        assert isinstance(entry["description"], str) and entry["description"].strip(), slug
        assert isinstance(entry["reviewed"], bool), slug


@pytest.mark.parametrize("lang", KEPT)
def test_no_description_is_the_english_one(lang: str) -> None:
    same = [s for s, e in _entries(lang).items() if e["description"].strip() == _en(s)[1]]
    assert same == []


@pytest.mark.parametrize("lang", KEPT)
def test_intentionally_english_lists_exactly_the_english_names(lang: str) -> None:
    listed = set(_raw(lang).get("_intentionally_english", []))
    english = {s for s, e in _entries(lang).items() if e["name"] == _en(s)[0]}
    assert listed == english


@pytest.mark.parametrize("lang", KEPT)
def test_protected_names_survive_translation(lang: str) -> None:
    lost = [
        (slug, term)
        for slug, entry in _entries(lang).items()
        for term in PROTECTED
        if re.search(rf"(?<![\w-]){re.escape(term)}(?![\w-])", _en(slug)[1])
        and term not in entry["description"]
    ]
    assert lost == []


# ---------------------------------------------------------------------------
# Built output
# ---------------------------------------------------------------------------

_H1_RE = re.compile(r'<header class="tag-landing-hero">.*?<h1[^>]*>(.*?)</h1>', re.S)
_DECK_RE = re.compile(r'<header class="tag-landing-hero">.*?<p class="deck"([^>]*)>(.*?)</p>', re.S)
_META_RE = re.compile(r'<meta (?:name|property)="(description|og:description)" content="([^"]*)"')

built = pytest.mark.skipif(
    not (PUBLIC / "tags" / "index.html").is_file(), reason="public/ not built: run ./build.sh"
)


def _page(lang: str, slug: str) -> str:
    path = PUBLIC / lang / btl.LOCALE_TAGS_PATH[lang] / slug / "index.html"
    assert path.is_file(), f"missing tag landing {path.relative_to(ROOT)}"
    return path.read_text(encoding="utf-8")


@built
@pytest.mark.parametrize("lang", KEPT)
def test_built_landings_never_serve_the_english_description(lang: str) -> None:
    leaks = []
    for slug in _landing_slugs():
        page = _page(lang, slug)
        deck = _DECK_RE.search(page)
        assert deck is not None, slug
        en_desc = _en(slug)[1]
        texts = [_html.unescape(deck.group(2))] + [
            _html.unescape(m.group(2)) for m in _META_RE.finditer(page)
        ]
        if any(_carries(t, en_desc) for t in texts) or 'lang="en"' in deck.group(1):
            leaks.append(slug)
    assert leaks == []


@built
@pytest.mark.parametrize("lang", KEPT)
def test_built_landings_carry_the_translated_strings(lang: str) -> None:
    wrong = []
    english_ok = set(_raw(lang).get("_intentionally_english", []))
    for slug in _landing_slugs():
        page = _page(lang, slug)
        entry = _entries(lang)[slug]
        h1 = _html.unescape(_H1_RE.search(page).group(1))  # type: ignore[union-attr]
        metas = dict(_META_RE.findall(page))
        if h1 != entry["name"] or (h1 == _en(slug)[0] and slug not in english_ok):
            wrong.append((slug, "h1", h1))
        wrong.extend(
            (slug, key, metas.get(key))
            for key in ("description", "og:description")
            if not _carries(_html.unescape(metas.get(key, "")), entry["description"])
        )
    assert wrong == []


def _carries(meta: str, desc: str) -> bool:
    """The meta holds the translated description, whole or as the opening
    that ``meta_length`` keeps when it fits the description to length."""
    if desc in meta:
        return True
    # The label before it can repeat the description's first words, so
    # try every place the description could start.
    starts = (m.start() for m in re.finditer(re.escape(desc[:12]), meta))
    return any(len(meta) > i + 12 and desc.startswith(meta[i:].rstrip("…")) for i in starts)
