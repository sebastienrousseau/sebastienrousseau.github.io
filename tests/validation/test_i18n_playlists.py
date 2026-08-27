#!/usr/bin/env python3
"""Gate: every active language ships a complete /playlists/ catalogue.

The /playlists/ page is generated from ``scripts/lib/_playlist_copy.py``
— 39 cards, a featured band, five lane heads, a seven-question FAQ and a
device aside. Because all of that lives inside ``<main>``, the EN-leakage
gate (``test_lang_no_leakage.py``, which deliberately scopes to chrome)
could not see it, and the whole body shipped in English on all 34
localized trees while the page's ``<title>`` claimed otherwise.

This gate closes that hole. For every active non-EN language it checks
``_data/i18n/<code>/playlists.json`` against the English reference:

  * same key set — every UI string, lane, card id, FAQ row and device;
  * ``{title}`` placeholder preserved in the three strings that
    interpolate a playlist name;
  * values safe to splice into HTML (no raw ``<`` or ``"``);
  * prose actually translated — a paragraph, blurb, FAQ answer or
    heading that is byte-identical to the English is a gap, not a
    choice.

Genre eyebrows and lane titles are exempt from the last check: "Deep
house · Melodic house" is the genre's name in most languages, and
forcing a translation there would be worse copy, not better.

Run from repo root: ``python3 tests/validation/test_i18n_playlists.py``.
"""

from __future__ import annotations

import sys as _sys  # path bootstrap — scripts reorg (scripts/lib/ on sys.path)
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[2] / "scripts" / "lib"))

import sys

import _lang_registry  # type: ignore[import-not-found]

# Strings interpolating a playlist name must keep the placeholder or the
# rendered alt/aria text loses the name entirely.
_PLACEHOLDER_KEYS = ("coverAlt", "openAria", "frameTitle")


def _prose_problems(code: str, cat: dict, ref: dict) -> list[str]:
    """Report prose fields left byte-identical to the English source."""
    out: list[str] = []

    def same(label: str, got: str, want: str) -> None:
        if got == want:
            out.append(f"[{code}/playlists] untranslated: {label}")

    for i, (got, want) in enumerate(zip(cat["intro"], ref["intro"], strict=True)):
        same(f"intro[{i}]", got, want)
    same("featured.kicker", cat["featured"]["kicker"], ref["featured"]["kicker"])
    same("featured.desc", cat["featured"]["desc"], ref["featured"]["desc"])
    for key in ref["lanes"]:
        same(f"lanes.{key}.sub", cat["lanes"][key]["sub"], ref["lanes"][key]["sub"])
    for pid in ref["cards"]:
        same(f"cards.{pid}.desc", cat["cards"][pid]["desc"], ref["cards"][pid]["desc"])
    same("faq.heading", cat["faq"]["heading"], ref["faq"]["heading"])
    same("faq.sub", cat["faq"]["sub"], ref["faq"]["sub"])
    for i, (got, want) in enumerate(zip(cat["faq"]["items"], ref["faq"]["items"], strict=True)):
        same(f"faq.items[{i}].q", got["q"], want["q"])
        same(f"faq.items[{i}].a", got["a"], want["a"])
    same("everywhere.heading", cat["everywhere"]["heading"], ref["everywhere"]["heading"])
    same("everywhere.body", cat["everywhere"]["body"], ref["everywhere"]["body"])
    return out


def _walk_values(node: object, path: str = ""):
    """Yield ``(path, str)`` for every string leaf in the catalogue."""
    if isinstance(node, str):
        yield path, node
    elif isinstance(node, dict):
        for k, v in node.items():
            yield from _walk_values(v, f"{path}.{k}" if path else str(k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from _walk_values(v, f"{path}[{i}]")


def _shape_problems(code: str, cat: dict, ref: dict) -> list[str]:
    """Key-set and cardinality checks against the English reference."""
    problems: list[str] = [
        f"[{code}/playlists] missing section: {section!r}"
        for section in ("ui", "lanes", "cards", "featured", "faq", "everywhere")
        if section not in cat
    ]
    if problems:
        return problems

    for section, want in (
        ("ui", set(ref["ui"])),
        ("lanes", set(ref["lanes"])),
        ("cards", set(ref["cards"])),
        ("featured", set(ref["featured"])),
    ):
        got = set(cat[section])
        problems.extend(
            f"[{code}/playlists] {section}: missing key {k!r}" for k in sorted(want - got)
        )
        problems.extend(
            f"[{code}/playlists] {section}: extra key {k!r}" for k in sorted(got - want)
        )

    problems.extend(
        f"[{code}/playlists] lanes.{key}: expected keys title + sub"
        for key in ref["lanes"]
        if key in cat["lanes"] and set(cat["lanes"][key]) != {"title", "sub"}
    )
    problems.extend(
        f"[{code}/playlists] cards.{pid}: expected keys eyebrow + desc"
        for pid in ref["cards"]
        if pid in cat["cards"] and set(cat["cards"][pid]) != {"eyebrow", "desc"}
    )
    problems.extend(
        f"[{code}/playlists] {name}: {got_len} entries, expected {want_len}"
        for name, got_len, want_len in (
            ("intro", len(cat.get("intro", [])), len(ref["intro"])),
            ("faq.items", len(cat["faq"].get("items", [])), len(ref["faq"]["items"])),
            (
                "everywhere.devices",
                len(cat["everywhere"].get("devices", [])),
                len(ref["everywhere"]["devices"]),
            ),
        )
        if got_len != want_len
    )
    return problems


def _markup_problems(code: str, cat: dict) -> list[str]:
    """Placeholder preservation + HTML-safety of every string leaf."""
    problems = [
        f"[{code}/playlists] ui.{key}: lost the {{title}} placeholder"
        for key in _PLACEHOLDER_KEYS
        if "{title}" not in cat["ui"][key]
    ]
    problems.extend(
        f'[{code}/playlists] {path}: raw < or " would break the markup'
        for path, value in _walk_values(cat)
        if not path.startswith("_") and ("<" in value or '"' in value)
    )
    return problems


def check(code: str, ref: dict) -> list[str]:
    try:
        cat = _lang_registry.load_playlists(code)
    except _lang_registry.LanguageError as e:
        return [str(e)]

    # Shape first: the later passes index into the catalogue and would
    # raise, not report, on a malformed one.
    problems = _shape_problems(code, cat, ref)
    if problems:
        return problems

    return _markup_problems(code, cat) + _prose_problems(code, cat, ref)


def main() -> int:
    ref = _lang_registry.playlist_reference()
    codes = [lg.code for lg in _lang_registry.active() if lg.code != "en"]
    if not codes:
        print("warn: no active non-EN languages", file=sys.stderr)
        return 0

    all_problems: list[str] = []
    for code in codes:
        all_problems.extend(check(code, ref))

    if all_problems:
        print("playlists catalogue defects:", file=sys.stderr)
        for line in all_problems[:60]:
            print(f"  - {line}", file=sys.stderr)
        if len(all_problems) > 60:
            print(f"  …and {len(all_problems) - 60} more", file=sys.stderr)
        return 1

    print(
        f"ok: /playlists/ catalogue complete for {len(codes)} language(s) "
        f"({len(ref['cards'])} cards, {len(ref['faq']['items'])} FAQ rows each)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
