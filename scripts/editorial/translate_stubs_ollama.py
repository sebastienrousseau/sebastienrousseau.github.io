#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Translate incomplete locale posts with a local Ollama model.

The script targets files reported by ``audit_translations.py``. It maps each
locale file back to the English source through ``_data/i18n/<lang>/slugs.json``,
asks Ollama for a complete Markdown replacement, and refuses to write output
that still contains hard placeholder markers.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POSTS = ROOT / "_posts"
I18N = ROOT / "_data" / "i18n"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_translations

PROTECTED_FRONTMATTER = {
    "id",
    "permalink",
    "url",
    "cdn",
    "cname",
    "author",
    "name",
    "image",
    "icon",
    "logo",
    "twitter_creator",
    "twitter_site",
    "measurementID",
    "theme-color",
    "date",
    "pub_date",
    "item_pub_date",
    "last_build_date",
    "last_reviewed",
    "atom_link",
    "twitter_url",
    "item_link",
    "item_guid",
}

LOCALE_NAMES = {
    "ar": "Arabic",
    "bn": "Bengali",
    "el": "Greek",
    "fa": "Persian",
    "fil": "Filipino",
    "fr": "French",
    "ha": "Hausa",
    "he": "Hebrew",
    "hu": "Hungarian",
    "id": "Indonesian",
    "mr": "Marathi",
    "ms": "Malay",
    "ro": "Romanian",
    "ta": "Tamil",
    "te": "Telugu",
    "uk": "Ukrainian",
    "yo": "Yoruba",
}

GLOSSARY = {
    "ar": "agent -> وكيل; tool-call -> استدعاء أداة; guardrails -> حواجز حماية; audit log -> سجل التدقيق; keep ISO 20022, DORA, SR 11-7, FIPS, ML-KEM canonical.",
    "bn": "agent -> এজেন্ট; tool-call -> টুল কল; guardrails -> সুরক্ষা বেড়া; audit log -> অডিট লগ; keep ISO 20022, DORA, SR 11-7, FIPS, ML-KEM canonical.",
    "el": "agent -> πράκτορας; tool-call -> κλήση εργαλείου; guardrails -> μηχανισμοί προστασίας; audit log -> αρχείο ελέγχου; keep ISO 20022, DORA, SR 11-7, FIPS, ML-KEM canonical.",
    "fa": "agent -> عامل; tool-call -> فراخوانی ابزار; guardrails -> حفاظ‌ها; audit log -> سیاههٔ حسابرسی; Western digits; keep ISO 20022, DORA, SR 11-7, FIPS, ML-KEM canonical.",
    "fil": "Keep canonical English technical terms such as tool-call, guardrails, audit log, kill switch, OAuth, OPA; translate surrounding prose into Filipino.",
    "fr": "cloud-native -> cloud-natif; guardrails -> garde-fous; audit log -> journal d'audit; kill switch -> coupure d'urgence; resilience -> résilience.",
    "ha": "Keep canonical English technical terms such as tool-call, guardrails, audit log, kill switch, OAuth, OPA; translate surrounding prose into Hausa.",
    "he": "agent -> סוכן; tool-call -> קריאה לכלי; guardrails -> מעקות בטיחות; audit log -> יומן ביקורת; Western digits.",
    "hu": "agent -> ügynök; tool-call -> eszközhívás; guardrails -> védőkorlátok; audit log -> auditnapló; kill switch -> vészleállító kapcsoló.",
    "id": "agent -> agen; tool-call -> panggilan alat; guardrails -> batas pengaman; audit log -> log audit; kill switch -> sakelar darurat.",
    "mr": "agent -> एजंट; tool-call -> साधन कॉल; guardrails -> सुरक्षा कठडे; audit log -> लेखापरीक्षण नोंद; keep ISO 20022, DORA, SR 11-7, FIPS, ML-KEM canonical.",
    "ms": "agent -> ejen; tool-call -> panggilan alat; guardrails -> pagar keselamatan; audit log -> log audit; kill switch -> suis mati kecemasan.",
    "ro": "agent -> agent; tool-call -> apel de instrument; guardrails -> bariere de siguranță; audit log -> jurnal de audit; kill switch -> întrerupător de urgență.",
    "ta": "agent -> முகவர்; tool-call -> கருவி அழைப்பு; guardrails -> பாதுகாப்பு வேலிகள்; audit log -> தணிக்கைப் பதிவு; keep ISO 20022, DORA, SR 11-7, FIPS, ML-KEM canonical.",
    "te": "agent -> ఏజెంట్; tool-call -> సాధన కాల్; guardrails -> భద్రతా కంచెలు; audit log -> ఆడిట్ లాగ్; keep ISO 20022, DORA, SR 11-7, FIPS, ML-KEM canonical.",
    "uk": "agent -> агент; tool-call -> виклик інструмента; guardrails -> запобіжники; audit log -> журнал аудиту; kill switch -> аварійний вимикач.",
    "yo": "Keep canonical English technical terms such as tool-call, guardrails, audit log, kill switch, OAuth, OPA; translate surrounding prose into Yoruba.",
}


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter")
    end = text.find("\n---", 4)
    if end < 0:
        raise ValueError("unterminated frontmatter")
    return text[: end + 4], text[end + 4 :].lstrip()


def frontmatter_map(text: str) -> dict[str, str]:
    fm, _ = split_frontmatter(text)
    out: dict[str, str] = {}
    for raw in fm.splitlines()[1:-1]:
        if ":" not in raw:
            continue
        key, _, value = raw.partition(":")
        out[key.strip()] = value.strip().strip('"').strip("'")
    return out


def reverse_slug_map(lang: str) -> dict[str, str]:
    path = I18N / lang / "slugs.json"
    if not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    articles = data.get("articles", {})
    return {localized: en for en, localized in articles.items()}


def english_source_for(path: Path) -> Path:
    lang = path.parent.name
    localized_slug = path.stem
    en_slug = reverse_slug_map(lang).get(localized_slug, localized_slug)
    source = POSTS / f"{en_slug}.md"
    if source.is_file():
        return source

    fm = frontmatter_map(path.read_text(encoding="utf-8"))
    for key in ("atom_link", "item_guid", "item_link", "twitter_url", "news_loc", "author_website"):
        value = fm.get(key, "")
        match = re.search(r"sebastienrousseau\.com/([^/]+)/?(?:index\.html|rss\.xml)?$", value)
        if not match:
            continue
        candidate = POSTS / f"{match.group(1)}.md"
        if candidate.is_file():
            return candidate

    raise FileNotFoundError(f"cannot map {path.relative_to(ROOT)} to English source")


def extract_translation(output: str) -> str:
    start = output.find("BEGIN_TRANSLATION")
    end = output.rfind("END_TRANSLATION")
    if start >= 0 and end > start:
        output = output[start + len("BEGIN_TRANSLATION") : end]
    output = output.strip()
    fence = re.fullmatch(r"```(?:markdown|md)?\s*\n(?P<body>.*)\n```", output, re.S)
    if fence:
        output = fence.group("body").strip()
    return output


def prompt_for(lang: str, source_text: str, current_text: str) -> str:
    source_fm, source_body = split_frontmatter(source_text)
    current_fm, _ = split_frontmatter(current_text)
    protected = ", ".join(sorted(PROTECTED_FRONTMATTER))
    locale_name = LOCALE_NAMES.get(lang, lang)
    glossary = GLOSSARY.get(
        lang, "Translate technical prose naturally; preserve canonical acronyms."
    )
    return f"""You are localising a technical banking article for sebastienrousseau.com.

Target locale: {lang} ({locale_name})
Glossary: {glossary}

Return one complete Markdown file only, between BEGIN_TRANSLATION and END_TRANSLATION.

Requirements:
- Translate the English article body fully into native {locale_name}; do not summarise.
- Remove any translation-stub, Translation pending, DRAFT translation, canonical-fallback, native-review, or editorial-note language.
- Preserve Markdown structure exactly: headings, list nesting, tables, links, code spans, HTML tags, and comments such as <!-- lead-start --> and <!-- enrich-end -->.
- Preserve URLs exactly. Translate visible link text and title attributes only.
- Localise SEO frontmatter fields such as title, seo_title, subtitle, description, excerpt, keywords, tags, item_title, item_description, twitter_title, twitter_description, banner_alt, image_alt, logo_alt, twitter_image_alt, thanks.
- Do not change these frontmatter fields: {protected}.
- Keep language/hreflang as {lang}; keep locale consistent with the existing target frontmatter.
- Do not invent claims, statistics, sources, or links.

Existing target frontmatter to preserve where protected:
{current_fm}

English source frontmatter:
{source_fm}

English source body:
{source_body}

BEGIN_TRANSLATION
"""


def ollama_translate(model: str, prompt: str, timeout: int) -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "think": False,
    }
    request = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
    except urllib.error.URLError as exc:
        raise RuntimeError(f"ollama API request failed: {exc}") from exc
    data = json.loads(body)
    if error := data.get("error"):
        raise RuntimeError(str(error))
    return extract_translation(str(data.get("response", "")))


def validate(path: Path, text: str) -> None:
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: model output missing frontmatter")
    split_frontmatter(text)
    defects = [name for name, pattern in audit_translations.HARD_PATTERNS if pattern.search(text)]
    if defects:
        raise ValueError(f"{path}: model output still contains {', '.join(defects)}")


def defect_paths(langs: set[str] | None) -> list[Path]:
    paths = []
    for path in audit_translations.iter_locale_posts():
        if langs and path.parent.name not in langs:
            continue
        if audit_translations.scan(path):
            paths.append(path)
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, help="Ollama model name, for example llama3.1:8b")
    parser.add_argument("--langs", nargs="*", help="optional locale codes to process")
    parser.add_argument("--limit", type=int, help="maximum number of files to translate")
    parser.add_argument(
        "--timeout", type=int, default=900, help="per-file Ollama timeout in seconds"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="list target files without translating"
    )
    args = parser.parse_args()

    langs = set(args.langs) if args.langs else None
    paths = defect_paths(langs)
    if args.limit is not None:
        paths = paths[: args.limit]

    if not paths:
        print("No incomplete locale posts matched.")
        return 0

    for path in paths:
        rel = path.relative_to(ROOT)
        source = english_source_for(path)
        print(f"{rel} <- {source.relative_to(ROOT)}")
        if args.dry_run:
            continue
        translated = ollama_translate(
            args.model,
            prompt_for(
                path.parent.name,
                source.read_text(encoding="utf-8"),
                path.read_text(encoding="utf-8"),
            ),
            args.timeout,
        )
        validate(path, translated)
        path.write_text(translated.rstrip() + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
