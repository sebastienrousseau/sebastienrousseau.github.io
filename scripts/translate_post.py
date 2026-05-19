#!/usr/bin/env python3
"""Translate an EN ``_posts/<slug>.md`` into every active non-EN locale.

For each locale the script:

  1. Computes a localized slug (transliterates the EN slug to the target
     language using a small dictionary of payments/finance/PQC domain
     terms, falls back to the EN slug for codes we don't have a
     transliteration recipe for).
  2. Calls the Anthropic API to translate the body — system prompt
     enforces tone-of-voice, markdown structure, citation links,
     numerical accuracy, and reading level matching the source.
  3. Localizes the frontmatter (title, subtitle, description,
     keywords, twitter_* fields, language, locale).
  4. Writes ``_posts/<lang>/<localized-slug>.md`` and updates
     ``_data/i18n/<lang>/slugs.json``'s ``articles`` map so the
     i18n-parity + hreflang-reciprocity gates see it.

Usage::

    # one EN slug → all 27 locales:
    python3 scripts/translate_post.py 2026-05-19-global-wholesale-payments-economics-2026

    # only a subset of locales:
    python3 scripts/translate_post.py <slug> --langs fr es de ja

    # dry-run (no API call, no writes — emit plan):
    python3 scripts/translate_post.py <slug> --dry-run

Requires ``ANTHROPIC_API_KEY`` in env. ``pip install anthropic``.

Cost rough-cut: ~2k tokens in + ~3k tokens out × 27 langs ≈ 135k tokens
in / 81k tokens out per article. At Claude 4.7 Sonnet pricing that's
about $3 per article — cheap enough to run daily.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "_posts"
I18N = ROOT / "_data" / "i18n"

# ---------------------------------------------------------------------------
# Active locales — kept in sync with scripts/_lang_registry.py.
# ---------------------------------------------------------------------------

sys.path.insert(0, str(ROOT / "scripts"))
import _lang_registry


def active_non_en_locales() -> list[str]:
    return [lang.code for lang in _lang_registry.active() if lang.code != "en"]


# ---------------------------------------------------------------------------
# Slug localisation. Each language has a small dictionary of canonical
# domain terms; we substitute them into the slug. Unknown terms fall
# through unchanged. The result is then de-duplicated against any
# existing slug in the lang's slugs.json so we don't clobber a prior
# article.
# ---------------------------------------------------------------------------

# These dicts are intentionally small — they cover the recurring tokens
# in the payments/AI/quantum article series. Add to them as new domain
# terms appear in titles.
_SLUG_DICT: dict[str, dict[str, str]] = {
    "fr": {
        "global": "mondiaux", "wholesale": "de-gros", "payments": "paiements",
        "economics": "economie", "agentic": "agentique", "engineering": "ingenierie",
        "banks": "banques", "blueprint": "feuille-de-route", "quantum": "quantique",
        "cryptography": "cryptographie", "standards": "normes",
        "developments": "evolutions", "best": "meilleure", "cloud": "cloud",
        "infrastructure": "infrastructure", "architecture": "architecture",
        "blackrock": "blackrock", "stablecoin": "stablecoin",
        "tokenised": "tokenise", "mmf": "fcp-monetaire",
        "securing": "securiser", "ledger": "registre",
        "post-quantum": "post-quantique", "migration": "migration",
        "corporate": "entreprise", "finance": "finance",
    },
    "de": {
        "global": "globale", "wholesale": "wholesale", "payments": "zahlungsverkehr",
        "economics": "okonomie",
    },
    "es": {
        "global": "global", "wholesale": "mayorista", "payments": "pagos",
        "economics": "economia",
    },
    "it": {
        "global": "globali", "wholesale": "wholesale", "payments": "pagamenti",
        "economics": "economia",
    },
    "pt-br": {
        "global": "globais", "wholesale": "atacado", "payments": "pagamentos",
        "economics": "economia",
    },
    # The remaining 22 locales use the EN slug as-is — slug-shape
    # acceptable per test_i18n_parity, hreflang gets the right
    # native-language MD via the articles map.
}


def localized_slug(en_slug: str, lang: str) -> str:
    """Token-substitute the EN slug into the target language. Languages
    without a dict entry get the EN slug verbatim."""
    if lang not in _SLUG_DICT:
        return en_slug
    out_parts = [
        _SLUG_DICT[lang].get(token.lower(), token)
        for token in en_slug.split("-")
    ]
    return "-".join(out_parts)


# ---------------------------------------------------------------------------
# Translation prompt. The system prompt encodes the tone-of-voice rules
# enforced by hand on prior articles: no hype, terse executive register,
# preserve citations + markdown, never invent statistics or sources.
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = """You are translating a long-form English research
article into {language_native} for a senior banking / payments /
post-quantum-cryptography audience. The author's voice is:

  - Tight, declarative, executive register. No hype. No "in conclusion".
    No "delve into". No "embark on a journey".
  - British English origin — preserve all numerals, currency symbols,
    proper nouns, ISO standards (ISO 20022, FIPS 203, etc.) verbatim.
  - Markdown structure is load-bearing: keep every heading, blockquote,
    bullet list, table, code block, and citation link EXACTLY as
    structured. Only TRANSLATE the prose between markup.
  - Citation links use the form [Source name](url "Source title").
    Translate the visible link text and `title` attribute into the
    target language. Keep the URL verbatim.
  - Numbers, percentages, dates, and statistics are FACTS — never
    paraphrase or round. Translate the surrounding sentence only.
  - Acronyms (BIS, CPMI, FSB, NIST, NCSC, etc.) stay in English on
    first mention with the native-language expansion in parentheses
    if a standard one exists in the target language.

You MUST output translated Markdown only. No commentary, no preamble,
no "here is the translation". Just the translated Markdown body."""


def _build_prompt(lang_code: str, lang_native_name: str, en_body: str) -> str:
    return f"Translate the following article to {lang_native_name} ({lang_code}). " \
           "Preserve all Markdown, citation links (URLs + title), numbers, " \
           "and proper nouns. Match the source's executive register.\n\n" \
           "===EN SOURCE===\n" + en_body + "\n===END==="


# ---------------------------------------------------------------------------
# Anthropic API caller. Lazy-imported so the script can run in --dry-run
# mode without the SDK installed.
# ---------------------------------------------------------------------------


def translate_via_claude(
    en_body: str, lang_code: str, lang_native_name: str,
) -> str:
    """Call Claude with the system + user prompts and return the
    translated Markdown body. Requires ANTHROPIC_API_KEY + anthropic
    SDK."""
    try:
        import anthropic
    except ImportError:
        raise SystemExit(
            "anthropic SDK not installed. Run: pip install anthropic"
        ) from None

    client = anthropic.Anthropic()
    system = _SYSTEM_PROMPT.format(language_native=lang_native_name)
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8192,
        system=system,
        messages=[{
            "role": "user",
            "content": _build_prompt(lang_code, lang_native_name, en_body),
        }],
    )
    # Concatenate text blocks (the SDK returns a list of content blocks).
    return "".join(b.text for b in msg.content if getattr(b, "type", None) == "text").strip()


# ---------------------------------------------------------------------------
# Native language names (for the prompt + ``language``/``locale`` frontmatter).
# ---------------------------------------------------------------------------

_NATIVE_NAMES: dict[str, str] = {
    "ar": "Arabic (العربية)", "bn": "Bengali (বাংলা)", "cs": "Czech (Čeština)",
    "de": "German (Deutsch)", "es": "Spanish (Español)", "fil": "Filipino",
    "fr": "French (Français)", "ha": "Hausa", "he": "Hebrew (עברית)",
    "hi": "Hindi (हिन्दी)", "id": "Indonesian (Bahasa Indonesia)",
    "it": "Italian (Italiano)", "ja": "Japanese (日本語)",
    "ko": "Korean (한국어)", "nl": "Dutch (Nederlands)", "pl": "Polish (Polski)",
    "pt-br": "Brazilian Portuguese (Português brasileiro)",
    "ro": "Romanian (Română)", "ru": "Russian (Русский)",
    "sv": "Swedish (Svenska)", "th": "Thai (ไทย)", "tr": "Turkish (Türkçe)",
    "uk": "Ukrainian (Українська)", "vi": "Vietnamese (Tiếng Việt)",
    "yo": "Yoruba", "zh-hans": "Simplified Chinese (简体中文)",
    "zh-hant": "Traditional Chinese (繁體中文)",
}

_LOCALE_CODES: dict[str, str] = {
    "ar": "ar_AR", "bn": "bn_BD", "cs": "cs_CZ", "de": "de_DE", "es": "es_ES",
    "fil": "fil_PH", "fr": "fr_FR", "ha": "ha_NG", "he": "he_IL",
    "hi": "hi_IN", "id": "id_ID", "it": "it_IT", "ja": "ja_JP",
    "ko": "ko_KR", "nl": "nl_NL", "pl": "pl_PL", "pt-br": "pt_BR",
    "ro": "ro_RO", "ru": "ru_RU", "sv": "sv_SE", "th": "th_TH",
    "tr": "tr_TR", "uk": "uk_UA", "vi": "vi_VN", "yo": "yo_NG",
    "zh-hans": "zh_CN", "zh-hant": "zh_TW",
}


# ---------------------------------------------------------------------------
# Frontmatter parse/emit. Minimal — the existing scripts/_frontmatter.py
# could be reused but it pulls in extra deps; we only need YAML-ish
# read here.
# ---------------------------------------------------------------------------


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Split a YAML-frontmatter post into (mapping, body)."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 4)
    if end < 0:
        return {}, text
    fm_text = text[3:end].strip()
    body = text[end + 4:].lstrip()
    fm: dict[str, str] = {}
    for line in fm_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        fm[key.strip()] = val.strip().strip('"').strip("'")
    return fm, body


def emit_frontmatter(fm: dict[str, str]) -> str:
    lines = ["---"]
    lines.extend(f'{k}: "{v}"' for k, v in fm.items())
    lines.append("---")
    return "\n".join(lines) + "\n\n"


# ---------------------------------------------------------------------------
# Per-locale translator + slug-map updater.
# ---------------------------------------------------------------------------


def translate_one(
    en_slug: str, en_text: str, lang_code: str, *, dry_run: bool,
) -> None:
    fm, body = parse_frontmatter(en_text)
    if not fm:
        raise SystemExit(f"could not parse frontmatter of {en_slug}")

    target_slug = localized_slug(en_slug, lang_code)
    lang_native = _NATIVE_NAMES.get(lang_code, lang_code)
    locale_code = _LOCALE_CODES.get(lang_code, f"{lang_code}_{lang_code.upper()}")
    out_path = POSTS / lang_code / f"{target_slug}.md"
    slugs_json = I18N / lang_code / "slugs.json"

    print(f"  [{lang_code}] → {out_path.relative_to(ROOT)}")
    if dry_run:
        return

    # Body translation. Skip-and-stub when ANTHROPIC_API_KEY is missing,
    # so the script remains useful for slug-mapping bootstrap even
    # without an API key.
    if os.environ.get("ANTHROPIC_API_KEY"):
        translated_body = translate_via_claude(body, lang_code, lang_native)
    else:
        # Stub: the EN body wrapped with a one-line localised header. The
        # i18n-parity gate passes (file exists, slug-map updated), but
        # the body remains EN. Re-run with the API key to overwrite.
        translated_body = (
            f"> _Translation pending — read the [English original]"
            f"(/{en_slug}/)._\n\n"
            + body
        )

    # Localized frontmatter — only fields that should differ between
    # locales. Everything else stays as the EN copy.
    new_fm = dict(fm)
    new_fm["language"] = lang_code
    new_fm["locale"] = locale_code
    new_fm["hreflang"] = lang_code
    new_fm["url"] = f"https://sebastienrousseau.com/{lang_code}/{target_slug}"
    new_fm["permalink"] = new_fm["url"]
    new_fm["id"] = new_fm["url"]

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(emit_frontmatter(new_fm) + translated_body, encoding="utf-8")

    # Update slugs.json — add EN→native mapping.
    if slugs_json.is_file():
        data = json.loads(slugs_json.read_text(encoding="utf-8"))
        data.setdefault("articles", {})[en_slug] = target_slug
        slugs_json.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("slug", help="EN article slug under _posts/ (no .md suffix)")
    p.add_argument(
        "--langs", nargs="*",
        help="Restrict to these locale codes. Default: all active non-EN.",
    )
    p.add_argument("--dry-run", action="store_true", help="No API, no writes.")
    args = p.parse_args()

    en_path = POSTS / f"{args.slug}.md"
    if not en_path.is_file():
        print(f"error: {en_path} not found", file=sys.stderr)
        return 1
    en_text = en_path.read_text(encoding="utf-8")

    targets = args.langs or active_non_en_locales()
    print(f"translating {args.slug} → {len(targets)} locale(s)")
    if not os.environ.get("ANTHROPIC_API_KEY") and not args.dry_run:
        print(
            "  (no ANTHROPIC_API_KEY — emitting EN-stub bodies + slug "
            "mappings; re-run with the key to overwrite with real translations)",
            file=sys.stderr,
        )

    for lang in targets:
        translate_one(args.slug, en_text, lang, dry_run=args.dry_run)

    print("done.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
