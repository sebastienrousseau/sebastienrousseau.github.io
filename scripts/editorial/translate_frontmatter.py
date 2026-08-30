#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Translate English frontmatter SEO/metadata fields in all locale posts.

One Claude API call per English article → translates all 27 locales in batch.
Only overwrites fields whose value is still identical to the English source.
Idempotent — safe to re-run.

Fields translated:
  description, subtitle, seo_title, keywords, tags, banner_alt,
  item_description, item_title, twitter_description, twitter_title,
  apple-mobile-web-app-title, excerpt

Usage:
  python3 scripts/editorial/translate_frontmatter.py
  python3 scripts/editorial/translate_frontmatter.py --slug 2026-05-20-cloud-native-banking-financial-institutions-2026
  python3 scripts/editorial/translate_frontmatter.py --langs fr de ar
  python3 scripts/editorial/translate_frontmatter.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from collections.abc import Mapping
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POSTS = ROOT / "_posts"

sys.path.insert(0, str(ROOT / "scripts" / "lib"))
import _lang_registry

# Fields to translate if still matching English source
FIELDS = [
    "description",
    "subtitle",
    "seo_title",
    "keywords",
    "tags",
    "banner_alt",
    "item_description",
    "item_title",
    "twitter_description",
    "twitter_title",
    "apple-mobile-web-app-title",
    "excerpt",
]

LANG_NAMES: dict[str, str] = {
    "ar": "Arabic",
    "bn": "Bengali",
    "cs": "Czech",
    "de": "German",
    "el": "Greek",
    "es": "Spanish",
    "fa": "Persian",
    "fil": "Filipino (Tagalog)",
    "fr": "French",
    "ha": "Hausa",
    "he": "Hebrew",
    "hi": "Hindi",
    "hu": "Hungarian",
    "id": "Indonesian",
    "it": "Italian",
    "ja": "Japanese",
    "ko": "Korean",
    "mr": "Marathi",
    "ms": "Malay",
    "nl": "Dutch",
    "pl": "Polish",
    "pt-br": "Brazilian Portuguese",
    "ro": "Romanian",
    "ru": "Russian",
    "sv": "Swedish",
    "ta": "Tamil",
    "te": "Telugu",
    "th": "Thai",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "vi": "Vietnamese",
    "yo": "Yoruba",
    "zh-hans": "Simplified Chinese",
    "zh-hant": "Traditional Chinese",
}

# ---------------------------------------------------------------------------
# Frontmatter field read / write helpers
# ---------------------------------------------------------------------------


def _read_field(text: str, field: str) -> str | None:
    """Read a quoted frontmatter field value."""
    m = re.search(
        rf'^{re.escape(field)}:\s*"((?:[^"\\]|\\.)*)"',
        text,
        re.MULTILINE,
    )
    if m:
        return m.group(1).replace('\\"', '"').replace("\\\\", "\\")
    return None


def _replace_field(text: str, field: str, new_value: str) -> str:
    """Replace a quoted frontmatter field value."""
    escaped = new_value.replace("\\", "\\\\").replace('"', '\\"')
    return re.sub(
        rf'(^{re.escape(field)}:\s*)"(?:[^"\\]|\\.)*"',
        rf'\g<1>"{escaped}"',
        text,
        count=1,
        flags=re.MULTILINE,
    )


def _field_exists(text: str, field: str) -> bool:
    return bool(re.search(rf"^{re.escape(field)}:", text, re.MULTILINE))


# ---------------------------------------------------------------------------
# Slug map helpers
# ---------------------------------------------------------------------------

_slug_cache: dict[str, dict[str, str]] = {}


def _slug_map(lang: str) -> dict[str, str]:
    if lang not in _slug_cache:
        _slug_cache[lang] = _lang_registry.load_slugs(lang).get("articles", {})
    return _slug_cache[lang]


def _find_locale_file(en_slug: str, lang: str) -> Path | None:
    locale_slug = _slug_map(lang).get(en_slug, en_slug)
    p = POSTS / lang / f"{locale_slug}.md"
    return p if p.is_file() else None


# ---------------------------------------------------------------------------
# Translation via Claude API
# ---------------------------------------------------------------------------

_FIELD_GUIDANCE = {
    "description": "Full meta description (150–160 chars in target language). Keep technical terms.",
    "subtitle": "Concise subtitle summarising the article. Natural prose in target language.",
    "seo_title": "Short SEO title ≤60 chars in target language. Keep proper nouns.",
    "keywords": "Comma-separated SEO keywords in target language. Keep proper nouns / product names in English.",
    "tags": "Comma-separated tags in target language. Keep proper nouns / product names in English.",
    "banner_alt": "Descriptive alt text for the hero image in target language.",
    "item_description": "Short RSS description in target language (≤200 chars).",
    "item_title": "Article title for RSS feed in target language.",
    "twitter_description": "Twitter card description in target language (≤200 chars).",
    "twitter_title": "Short Twitter card title in target language (≤60 chars).",
    "apple-mobile-web-app-title": "Very short app title, 2–4 words in target language.",
    "excerpt": "1–2 sentence excerpt in target language.",
}


def _batch_prompt(en_fields: dict[str, str], locales_needing: dict[str, list[str]]) -> str:
    """The translation prompt for one batch of languages."""
    guidance_lines = "\n".join(f"  - {f}: {_FIELD_GUIDANCE[f]}" for f in FIELDS if f in en_fields)
    return f"""\
You are a professional translator and SEO specialist for financial technology content.
Translate blog post frontmatter fields precisely, preserving technical terms,
product names, and brand names in their original form while making the text
native-sounding in the target language.
Return ONLY a valid JSON object — no prose, no markdown code fences, no explanations.

English source frontmatter fields:
{json.dumps(en_fields, ensure_ascii=False, indent=2)}

Field-by-field guidance:
{guidance_lines}

Required translations per language (language_code → list of field names to translate):
{json.dumps(dict(locales_needing), ensure_ascii=False, indent=2)}

Language names:
{json.dumps({lang: LANG_NAMES[lang] for lang in locales_needing}, ensure_ascii=False, indent=2)}

Return a JSON object where each key is a language code and the value is an object
with ONLY the fields listed for that language translated into that language.
Example structure:
{{
  "fr": {{
    "description": "...",
    "seo_title": "..."
  }},
  "de": {{
    "description": "...",
    "seo_title": "..."
  }}
}}
"""


def _invoke_translator(prompt: str) -> dict[str, dict[str, str]]:
    """One ``claude -p`` call. Raises on empty output or unparseable JSON so
    the retry loop above can decide whether to try again."""
    result = subprocess.run(
        ["claude", "-p", prompt],
        capture_output=True,
        text=True,
        timeout=300,
    )
    content = result.stdout.strip()
    if not content:
        raise ValueError(f"Empty response (stderr: {result.stderr[:200]})")
    # Strip markdown code fences if present
    content = re.sub(r"^```(?:json)?\s*", "", content)
    content = re.sub(r"\s*```$", "", content)
    parsed: dict[str, dict[str, str]] = json.loads(content)
    return parsed


def _translate_batch(
    en_fields: dict[str, str],
    locales_needing: dict[str, list[str]],
) -> dict[str, dict[str, str]]:
    """
    One ``claude -p`` call: translate ``en_fields`` into every language in
    ``locales_needing`` (lang → list of fields needed).
    Returns {lang: {field: translated_value}}. Three attempts, then gives up
    and returns {} — a failed translation must not abort the run.
    """
    if not locales_needing:
        return {}
    prompt = _batch_prompt(en_fields, locales_needing)

    for attempt in range(3):
        try:
            return _invoke_translator(prompt)
        except json.JSONDecodeError as e:
            print(f"  [attempt {attempt + 1}] JSON parse error: {e}", file=sys.stderr)
            delay = 3
        except subprocess.TimeoutExpired:
            print("  Timeout — retrying", file=sys.stderr)
            delay = 5
        except (OSError, ValueError) as e:
            # OSError: claude binary missing/unrunnable; ValueError: the
            # empty-response raise above. Anything else should traceback.
            print(f"  Error: {e}", file=sys.stderr)
            delay = 5
        if attempt < 2:
            time.sleep(delay)

    return {}


# ---------------------------------------------------------------------------
# Per-article processor
# ---------------------------------------------------------------------------


def _en_fields(en_text: str) -> dict[str, str]:
    """The English front-matter values worth propagating."""
    return {f: v for f in FIELDS if (v := _read_field(en_text, f))}


def _locales_needing(
    en_slug: str, en_fields: dict[str, str], target_langs: list[str]
) -> tuple[dict[str, list[str]], dict[str, Path]]:
    """Per locale, which fields still hold the untranslated English value."""
    needing: dict[str, list[str]] = {}
    paths: dict[str, Path] = {}
    for lang in target_langs:
        path = _find_locale_file(en_slug, lang)
        if path is None:
            continue
        loc_text = path.read_text(encoding="utf-8")
        needs = [
            f
            for f in FIELDS
            if _field_exists(loc_text, f) and _read_field(loc_text, f) == en_fields.get(f)
        ]
        if needs:
            needing[lang] = needs
            paths[lang] = path
    return needing, paths


def _apply_translations(path: Path, fields_translated: Mapping[str, object]) -> list[str]:
    """Write the translated fields into one locale file. Returns the field
    names actually applied (empty when nothing changed)."""
    text = path.read_text(encoding="utf-8")
    new_text = text
    applied: list[str] = []
    for field, value in fields_translated.items():
        if not value or not isinstance(value, str):
            continue
        replaced = _replace_field(new_text, field, value)
        if replaced != new_text:
            new_text = replaced
            applied.append(field)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return applied
    return []


def _run_batches(
    en_fields: dict[str, str],
    needing: dict[str, list[str]],
    paths: dict[str, Path],
) -> int:
    """Translate in batches of 3 languages per call (~27s each, proven
    reliable). Returns the number of locale files updated."""
    batch_size = 3
    lang_list = list(needing.items())
    updated = 0
    for batch_start in range(0, len(lang_list), batch_size):
        batch = dict(lang_list[batch_start : batch_start + batch_size])
        for lang, fields_translated in _translate_batch(en_fields, batch).items():
            path = paths.get(lang)
            if path is None:
                continue
            applied = _apply_translations(path, fields_translated)
            if applied:
                updated += 1
                print(f"    [{lang}] updated: {', '.join(applied)}")
    return updated


def _process_article(
    en_slug: str,
    en_path: Path,
    *,
    langs_filter: list[str] | None,
    dry_run: bool,
) -> int:
    en_fields = _en_fields(en_path.read_text(encoding="utf-8"))
    if not en_fields:
        return 0

    all_langs = [lang.code for lang in _lang_registry.active() if lang.code != "en"]
    needing, paths = _locales_needing(en_slug, en_fields, langs_filter or all_langs)
    if not needing:
        return 0

    total_fields = sum(len(v) for v in needing.values())
    print(f"  {en_slug}: {len(needing)} locales, {total_fields} field-translations needed")

    if dry_run:
        for lang, fields in sorted(needing.items()):
            print(f"    [{lang}] would translate: {', '.join(fields)}")
        return 0

    return _run_batches(en_fields, needing, paths)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument(
        "--slug",
        help="Process only this English slug (no .md suffix).",
    )
    p.add_argument(
        "--langs",
        nargs="*",
        metavar="LANG",
        help="Restrict to these locale codes.",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Report what would change without writing files.",
    )
    args = p.parse_args()

    if args.slug:
        en_path = POSTS / f"{args.slug}.md"
        if not en_path.is_file():
            print(f"error: {en_path} not found", file=sys.stderr)
            return 1
        en_posts = [en_path]
    else:
        en_posts = sorted(POSTS.glob("[0-9][0-9][0-9][0-9]-*.md"))

    total_files = 0
    for en_path in en_posts:
        en_slug = en_path.stem
        n = _process_article(
            en_slug,
            en_path,
            langs_filter=args.langs,
            dry_run=args.dry_run,
        )
        total_files += n

    mode = "(dry-run)" if args.dry_run else ""
    print(f"\ntranslate_frontmatter {mode}: updated {total_files} locale files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
