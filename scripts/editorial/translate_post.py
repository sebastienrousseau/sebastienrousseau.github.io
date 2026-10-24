#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Scaffold per-locale stubs + slug-map entries for a newly-promoted
EN post. *Body translation is intentionally NOT done here* — that step
runs inside Claude Code on your laptop, using your Claude subscription,
so no Anthropic API key ever lives in this repo.

Workflow:

  1. ``scripts/editorial/publish-daily.sh`` (or ``make publish-today``) runs THIS
     script first. For each active non-EN locale it writes:
        - ``_posts/<lang>/<localized-slug>.md`` with localised
          frontmatter and a placeholder body (the EN body with a
          ``translation pending`` callout at the top).
        - An entry in ``_data/i18n/<lang>/slugs.json``'s ``articles``
          map so the i18n-parity + hreflang-reciprocity gates pass.

  2. Then in Claude Code on your laptop you say "translate today's
     article" — Claude reads each ``_posts/<lang>/<slug>.md``, rewrites
     the placeholder body into a real native-language translation
     (using the tone-of-voice + markdown-preservation rules in
     ``.claude/commands/publish-today.md``), and writes it back. The
     subscription you already pay for covers all 27 calls.

  3. Build + commit + push as normal.

Usage::

    python3 scripts/editorial/translate_post.py 2026-05-19-global-wholesale-payments-economics-2026
    python3 scripts/editorial/translate_post.py <slug> --langs fr es de ja   # subset
    python3 scripts/editorial/translate_post.py <slug> --dry-run             # plan only

Idempotent — re-running on an already-translated post leaves real
translations alone (only files whose body still starts with the
``<!-- translation-stub -->`` marker get overwritten).
"""

from __future__ import annotations

import sys as _sys  # path bootstrap — scripts reorg (scripts/lib/ on sys.path)
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "lib"))

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POSTS = ROOT / "_posts"
I18N = ROOT / "_data" / "i18n"

# Marker the scaffolder leaves at the top of every stub body. Used by
# Claude Code to detect which files still need a translation pass, and
# by re-runs of this script to know which stubs are safe to overwrite.
STUB_MARKER = "<!-- translation-stub: replace this body in Claude Code -->"

sys.path.insert(0, str(ROOT / "scripts"))
import _lang_registry
from _frontmatter import parse_frontmatter  # canonical shared parser (lib/_frontmatter)
from _romanise import derive_slug


def active_non_en_locales() -> list[str]:
    return [lang.code for lang in _lang_registry.active() if lang.code != "en"]


# ---------------------------------------------------------------------------
# Locale-slug substitution. Each locale has a small dictionary of canonical
# domain terms; tokens that aren't in the dict pass through unchanged.
# ---------------------------------------------------------------------------

_SLUG_DICT: dict[str, dict[str, str]] = {
    "fr": {
        "global": "mondiaux",
        "wholesale": "de-gros",
        "payments": "paiements",
        "economics": "economie",
        "agentic": "agentique",
        "engineering": "ingenierie",
        "banks": "banques",
        "blueprint": "feuille-de-route",
        "quantum": "quantique",
        "cryptography": "cryptographie",
        "standards": "normes",
        "developments": "evolutions",
        "best": "meilleure",
        "cloud": "cloud",
        "infrastructure": "infrastructure",
        "architecture": "architecture",
        "blackrock": "blackrock",
        "stablecoin": "stablecoin",
        "tokenised": "tokenise",
        "mmf": "fcp-monetaire",
        "securing": "securiser",
        "ledger": "registre",
        "post-quantum": "post-quantique",
        "migration": "migration",
        "corporate": "entreprise",
        "finance": "finance",
    },
    "de": {
        "global": "globale",
        "payments": "zahlungsverkehr",
        "economics": "okonomie",
    },
    "es": {
        "global": "global",
        "wholesale": "mayorista",
        "payments": "pagos",
        "economics": "economia",
    },
    "it": {
        "global": "globali",
        "payments": "pagamenti",
        "economics": "economia",
    },
    "pt-br": {
        "global": "globais",
        "wholesale": "atacado",
        "payments": "pagamentos",
        "economics": "economia",
    },
    # Other 22 locales fall through to the EN slug — slug shape is
    # acceptable per test_i18n_parity, hreflang uses the slug-map for
    # routing regardless.
}


def localized_slug(en_slug: str, lang: str) -> str:
    if lang not in _SLUG_DICT:
        return en_slug
    out_parts = [_SLUG_DICT[lang].get(token.lower(), token) for token in en_slug.split("-")]
    return "-".join(out_parts)


# ---------------------------------------------------------------------------
# Locale metadata.
# ---------------------------------------------------------------------------

_LOCALE_CODES: dict[str, str] = {
    "ar": "ar_AR",
    "bn": "bn_BD",
    "cs": "cs_CZ",
    "de": "de_DE",
    "el": "el_GR",
    "es": "es_ES",
    "fa": "fa_IR",
    "fil": "fil_PH",
    "fr": "fr_FR",
    "ha": "ha_NG",
    "he": "he_IL",
    "hi": "hi_IN",
    "hu": "hu_HU",
    "id": "id_ID",
    "it": "it_IT",
    "ja": "ja_JP",
    "ko": "ko_KR",
    "mr": "mr_IN",
    "ms": "ms_MY",
    "nl": "nl_NL",
    "pl": "pl_PL",
    "pt-br": "pt_BR",
    "ro": "ro_RO",
    "ru": "ru_RU",
    "sv": "sv_SE",
    "ta": "ta_IN",
    "te": "te_IN",
    "th": "th_TH",
    "tr": "tr_TR",
    "uk": "uk_UA",
    "vi": "vi_VN",
    "yo": "yo_NG",
    "zh-hans": "zh_CN",
    "zh-hant": "zh_TW",
}


# ---------------------------------------------------------------------------
# Frontmatter emit. Parsing uses the canonical lib/_frontmatter.parse_frontmatter
# (imported above); emit stays local because it writes this repo's specific
# single-line ``key: "value"`` scaffold shape.
# ---------------------------------------------------------------------------


def emit_frontmatter(fm: dict[str, str]) -> str:
    lines = ["---"]
    lines.extend(f'{k}: "{v}"' for k, v in fm.items())
    lines.append("---")
    return "\n".join(lines) + "\n\n"


# Article furniture inside <main> whose accessible name is a labels.json key.
# test_i18n_labels.py fails any locale post that keeps the English name, so
# the stub carries the locale's value from the start, not after translation.
_FURNITURE_LABEL_RE = re.compile(
    r'(<aside class="(?:post-lead|author-card)" aria-label=")'
    r'(Article summary|About the author)(")'
)


def localise_furniture_labels(body: str, lang_code: str) -> str:
    """Swap the English furniture aria-labels for ``lang_code``'s."""
    try:
        labels = _lang_registry.load_labels(lang_code)
    except _lang_registry.LanguageError:
        return body
    return _FURNITURE_LABEL_RE.sub(
        lambda m: m.group(1) + labels.get(m.group(2), m.group(2)) + m.group(3), body
    )


# ---------------------------------------------------------------------------
# Per-locale scaffold writer.
# ---------------------------------------------------------------------------


def scaffold_one(
    en_slug: str,
    en_text: str,
    lang_code: str,
    *,
    dry_run: bool,
) -> str:
    """Write the stub MD for ``lang_code``. Returns a short status
    string the CLI prints."""
    fm, body = parse_frontmatter(en_text)
    if not fm:
        raise SystemExit(f"could not parse frontmatter of {en_slug}")

    date = en_slug[:10]
    target_slug = f"{date}-{derive_slug(fm.get('title', ''), lang_code, date[:4])}"
    out_path = POSTS / lang_code / f"{target_slug}.md"
    slugs_json = I18N / lang_code / "slugs.json"

    rel_out = out_path.relative_to(ROOT)
    # Skip when a real translation already exists (re-runs should be safe).
    if out_path.is_file():
        existing = out_path.read_text(encoding="utf-8")
        if STUB_MARKER not in existing:
            return f"  [{lang_code}] keep — already translated: {rel_out}"

    if dry_run:
        return f"  [{lang_code}] would scaffold: {rel_out}"

    new_fm = dict(fm)
    new_fm["language"] = lang_code
    new_fm["locale"] = _LOCALE_CODES.get(lang_code, f"{lang_code}_{lang_code.upper()}")
    new_fm["hreflang"] = lang_code
    new_fm["url"] = f"https://sebastienrousseau.com/{lang_code}/{target_slug}"
    new_fm["permalink"] = new_fm["url"]
    new_fm["id"] = new_fm["url"]

    placeholder = (
        f"{STUB_MARKER}\n\n"
        f"> _Translation pending — read the "
        f"[English original](/{en_slug}/) while we localise._\n\n"
        + localise_furniture_labels(body, lang_code)
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(emit_frontmatter(new_fm) + placeholder, encoding="utf-8")

    if slugs_json.is_file():
        data = json.loads(slugs_json.read_text(encoding="utf-8"))
        data.setdefault("articles", {})[en_slug] = target_slug
        slugs_json.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    return f"  [{lang_code}] scaffolded: {rel_out}"


def _slug_map(lang_code: str) -> tuple[Path, dict]:
    path = I18N / lang_code / "slugs.json"
    if not path.is_file():
        return path, {}
    return path, json.loads(path.read_text(encoding="utf-8"))


def rederive_slug(en_slug: str, lang_code: str, *, dry_run: bool) -> str:
    """Rename a locale post so its slug follows its *translated* title.

    ``scaffold_one`` names the stub from the English title; translating
    the title afterwards leaves a slug that no longer derives from it,
    which ``tests/validation/test_slug_derivable.py`` rejects. This moves
    the file, rewrites its own URL fields and updates ``slugs.json``.
    """
    map_path, data = _slug_map(lang_code)
    current = data.get("articles", {}).get(en_slug)
    path = POSTS / lang_code / f"{current}.md"
    if not current or not path.is_file():
        return f"  [{lang_code}] skip: no locale post mapped for {en_slug}"
    text = path.read_text(encoding="utf-8")
    date = en_slug[:10]
    body = derive_slug(parse_frontmatter(text)[0].get("title", ""), lang_code, date[:4])
    if not body:
        return f"  [{lang_code}] error: title derives no slug; extend the romanisation lexicon"
    target = f"{date}-{body}"
    if target == current:
        return f"  [{lang_code}] keep: {current}"
    if dry_run:
        return f"  [{lang_code}] would rename: {current} -> {target}"
    base = f"https://sebastienrousseau.com/{lang_code}/"
    path.with_name(f"{target}.md").write_text(
        text.replace(base + current, base + target), encoding="utf-8"
    )
    path.unlink()
    data["articles"][en_slug] = target
    map_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return f"  [{lang_code}] renamed: {current} -> {target}"


def find_stub_locales(en_slug: str) -> list[tuple[str, Path]]:
    """List ``(lang_code, path)`` for every locale where the file still
    carries the stub marker. Used by Claude-Code-driven translation
    passes to know what's still pending."""
    pending: list[tuple[str, Path]] = []
    en_path = POSTS / f"{en_slug}.md"
    title = ""
    if en_path.is_file():
        fm, _ = parse_frontmatter(en_path.read_text(encoding="utf-8"))
        title = fm.get("title", "")
    date = en_slug[:10]

    for lang in active_non_en_locales():
        target_slug = None
        slugs_json = I18N / lang / "slugs.json"
        if slugs_json.is_file():
            try:
                data = json.loads(slugs_json.read_text(encoding="utf-8"))
                target_slug = data.get("articles", {}).get(en_slug)
            except (json.JSONDecodeError, OSError) as exc:
                print(
                    f"warning: failed to read slug map {slugs_json}: {exc}",
                    file=sys.stderr,
                )
        if not target_slug:
            if title:
                target_slug = f"{date}-{derive_slug(title, lang, date[:4])}"
            else:
                target_slug = localized_slug(en_slug, lang)
        p = POSTS / lang / f"{target_slug}.md"
        if p.is_file() and STUB_MARKER in p.read_text(encoding="utf-8"):
            pending.append((lang, p))
    return pending


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _cmd_list_stubs(en_slug: str) -> int:
    pending = find_stub_locales(en_slug)
    if not pending:
        print(f"all {len(active_non_en_locales())} locales translated for {en_slug}.")
        return 0
    print(f"{len(pending)} locale(s) still pending translation:")
    for lang, path in pending:
        print(f"  [{lang}] {path.relative_to(ROOT)}")
    return 0


def _cmd_rederive(en_slug: str, targets: list[str], *, dry_run: bool) -> int:
    results = [rederive_slug(en_slug, lang, dry_run=dry_run) for lang in targets]
    print("\n".join(results))
    return 1 if any("] error:" in r for r in results) else 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("slug", help="EN article slug under _posts/ (no .md suffix)")
    p.add_argument(
        "--langs",
        nargs="*",
        help="Restrict to these locale codes. Default: all active non-EN.",
    )
    p.add_argument("--dry-run", action="store_true", help="No writes.")
    p.add_argument(
        "--rederive-slugs",
        action="store_true",
        help="After translation: rename each locale post to the slug its translated title derives.",
    )
    p.add_argument(
        "--list-stubs",
        action="store_true",
        help="Print every locale still carrying the stub marker for this slug.",
    )
    args = p.parse_args()

    en_path = POSTS / f"{args.slug}.md"
    if not en_path.is_file():
        print(f"error: {en_path} not found", file=sys.stderr)
        return 1

    if args.list_stubs:
        return _cmd_list_stubs(args.slug)

    targets = args.langs or active_non_en_locales()
    if args.rederive_slugs:
        return _cmd_rederive(args.slug, targets, dry_run=args.dry_run)

    en_text = en_path.read_text(encoding="utf-8")
    print(f"scaffolding {args.slug} → {len(targets)} locale(s)")
    for lang in targets:
        print(scaffold_one(args.slug, en_text, lang, dry_run=args.dry_run))
    if not args.dry_run:
        print(
            "\nNext step: run Claude Code locally and ask it to translate "
            "the stub bodies (it'll find them with "
            f"`python3 scripts/editorial/translate_post.py {args.slug} --list-stubs`)."
        )
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())


# Quiet ruff/mypy on the intentional sys-path-then-import dance above.
_ = re
