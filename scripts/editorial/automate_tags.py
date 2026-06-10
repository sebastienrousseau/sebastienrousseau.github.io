#!/usr/bin/env python3
"""Automate and optimize tags across all articles in `_posts/` and `_drafts/` (all locales).

This script:
  1. Standardizes all tags in English articles to their canonical forms (correct casing, spelling, acronyms).
  2. Automatically infers missing tags based on content analysis (keywords in title, description, content).
  3. Propagates the optimized tags to all 27 translated locales by mapping them to their correct localized versions.
  4. Keeps tag indices clean, sorted, deduplicated, and in sync.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POSTS_DIR = ROOT / "_posts"
DRAFTS_DIR = ROOT / "_drafts"
TRANSLATIONS_FILE = ROOT / "_data" / "tag_translations.json"

# Canonical English mapping (lowercased key -> canonical case)
CANONICAL_MAP = {
    "ai": "AI",
    "artificial intelligence": "AI",
    "artificialintelligence": "AI",
    "generative ai": "generative AI",
    "generative": "generative AI",
    "agentic ai": "agentic AI",
    "agentic commerce": "agentic AI",
    "agentic engineering": "agentic AI",
    "autonomous agents": "agentic AI",
    "agentic payments": "agentic payments",
    "paymentautomation": "payment automation",
    "payment automation": "payment automation",
    "payments": "payments",
    "payment": "payments",
    "payment initiation": "payments",
    "payment orchestration": "payments",
    "payment processing": "payments",
    "payments compliance": "payments",
    "payments security": "payments",
    "payments technology": "payments",
    "cross-border payments": "cross-border payments",
    "cross-border": "cross-border payments",
    "wholesale payments": "wholesale payments",
    "iso 20022": "ISO 20022",
    "iso20022": "ISO 20022",
    "iso 20022 pacs.008": "ISO 20022",
    "pacs.008": "pacs.008",
    "pacs008": "pacs.008",
    "pacs008.com": "pacs.008",
    "pain message": "pain message",
    "pain message standards": "pain message",
    "pain message validation": "pain message",
    "pain001": "pain001",
    "pain001001009": "pain001",
    "post-quantum": "post-quantum cryptography",
    "post-quantum cryptography": "post-quantum cryptography",
    "pqc": "post-quantum cryptography",
    "pqc standardisation": "post-quantum cryptography",
    "quantum-resistant cryptography": "post-quantum cryptography",
    "quantum-resistant": "post-quantum cryptography",
    "quantum-safe payments": "quantum-safe payments",
    "cryptography": "cryptography",
    "cryptographic hash": "cryptography",
    "cryptographic library": "cryptography",
    "cybersecurity": "cybersecurity",
    "security": "cybersecurity",
    "banking security": "cybersecurity",
    "quantum computing": "quantum computing",
    "quantum algorithms": "quantum algorithms",
    "quantum algorithm": "quantum algorithms",
    "blockchain": "blockchain",
    "blockchain payments": "blockchain",
    "blockchain technology": "blockchain",
    "distributed ledger": "blockchain",
    "stablecoin": "stablecoins",
    "stablecoins": "stablecoins",
    "tokenised deposits": "tokenised deposits",
    "tokenized deposits": "tokenised deposits",
    "deposit tokens": "tokenised deposits",
    "deposit token": "tokenised deposits",
    "great british tokenised deposits": "tokenised deposits",
    "rust": "Rust",
    "open-source": "open source",
    "opensource": "open source",
    "open source": "open source",
    "platform engineering": "platform engineering",
    "platform-engineering": "platform engineering",
    "sovereign cloud": "sovereign cloud",
    "cloud sovereignty": "sovereign cloud",
    "cloud native banking": "cloud native banking",
    "cloud native": "cloud native banking",
    "cloud-native": "cloud native banking",
    "operational resilience": "operational resilience",
    "resilience": "operational resilience",
    "cloud resilience": "cloud resilience",
    "cloud concentration risk": "cloud concentration risk",
    "nist": "NIST",
    "nist pqc": "NIST",
    "swift": "SWIFT",
    "fednow": "FedNow",
    "sepa": "SEPA",
    "usdc": "USDC",
    "cbdc": "CBDC",
    "llm": "LLM",
    "llms": "LLM",
    "large language model": "LLM",
    "large language models": "LLM",
    "prompt engineering": "prompt engineering",
    "promptengineering": "prompt engineering",
}

# Regex rules to automatically infer/add tags if present in the post
INFERENCE_RULES = {
    "ISO 20022": [
        r"\biso\s*20022\b",
        r"\bpain\.001\b",
        r"\bpacs\.008\b",
        r"\bcbpr\+\b",
        r"\bswift\b",
    ],
    "DORA": [
        r"\bdora\b",
        r"\bresilience\b",
        r"\bthird-party\s*risk\b",
        r"\bconcentration\s*risk\b",
    ],
    "post-quantum cryptography": [
        r"\bpost-quantum\b",
        r"\bpqc\b",
        r"\bquantum-safe\b",
        r"\bquantum-resistant\b",
        r"\bkyber\b",
        r"\bml-kem\b",
        r"\bml-dsa\b",
    ],
    "quantum computing": [
        r"\bquantum\s*computing\b",
        r"\bquantum\s*algorithm\b",
        r"\bqubit\b",
        r"\bshor's\b",
    ],
    "AI": [
        r"\bai\b",
        r"\bartificial\s*intelligence\b",
        r"\bgenerative\s*ai\b",
        r"\bllm\b",
        r"\bprompt\s*engineering\b",
        r"\bagentic\b",
    ],
    "stablecoins": [r"\bstablecoin\b", r"\bstablecoins\b", r"\busdc\b", r"\busdt\b"],
    "tokenised deposits": [
        r"\btokenised\s*deposit\b",
        r"\btokenised\s*deposits\b",
        r"\btokenized\s*deposits\b",
        r"\bdeposit\s*tokens\b",
    ],
    "Rust": [r"\brust\b", r"\bcargo\b", r"\bshokunin\b", r"\blibmake\b", r"\brustlogs\b"],
    "open source": [r"\bopen\s*source\b", r"\bopen-source\b", r"\boss\b"],
    "platform engineering": [
        r"\bplatform\s*engineering\b",
        r"\bkubernetes\b",
        r"\bargocd\b",
        r"\bgitops\b",
    ],
    "sovereign cloud": [r"\bsovereign\s*cloud\b", r"\bcloud\s*sovereignty\b"],
    "cloud native banking": [r"\bcloud\s*native\b", r"\bcloud-native\b"],
    "cross-border payments": [r"\bcross-border\b", r"\bcross-border\s*payments\b"],
}


def load_translations() -> dict[str, dict[str, str]]:
    if not TRANSLATIONS_FILE.is_file():
        return {}
    try:
        return json.loads(TRANSLATIONS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError, UnicodeDecodeError) as e:
        print(f"Error loading tag translations: {e}")
        return {}


def extract_frontmatter_and_content(file_path: Path) -> tuple[dict[str, str], str, str]:
    """Parse a post file and return (frontmatter_dict, yaml_string, body_content)."""
    content = file_path.read_text(encoding="utf-8")
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not fm_match:
        return {}, "", content

    fm_text = fm_match.group(1)
    body = fm_match.group(2)

    fm_dict = {}
    for line in fm_text.splitlines():
        if ":" in line:
            parts = line.split(":", 1)
            key = parts[0].strip()
            val = parts[1].strip()
            # strip quotes
            if (val.startswith('"') and val.endswith('"')) or (
                val.startswith("'") and val.endswith("'")
            ):
                val = val[1:-1]
            fm_dict[key] = val

    return fm_dict, fm_text, body


def clean_tags(tags: list[str]) -> list[str]:
    """Apply canonical mapping and deduplicate."""
    cleaned = []
    seen = set()
    for tag in tags:
        tag_stripped = tag.strip()
        if not tag_stripped:
            continue
        # Check canonical map
        canonical = CANONICAL_MAP.get(tag_stripped.lower(), tag_stripped)
        if canonical.lower() not in seen:
            seen.add(canonical.lower())
            cleaned.append(canonical)
    return cleaned


def infer_tags(content: str, current_tags: list[str]) -> list[str]:
    """Scan content for keywords and add relevant tags if missing."""
    inferred = list(current_tags)
    for tag, patterns in INFERENCE_RULES.items():
        if tag in inferred:
            continue
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                inferred.append(tag)
                break
    return inferred


def update_tags_in_file(file_path: Path, new_tags: list[str]) -> bool:
    """Safely replace the tags line in frontmatter, preserving other lines."""
    content = file_path.read_text(encoding="utf-8")
    tags_str = ", ".join(new_tags)

    # Match tags: "..." or tags: '...' or tags: ...
    pattern = re.compile(r'^tags:\s*("[^"]*"|\'[^\']*\'|[^\n]+)\s*$', re.MULTILINE)
    if pattern.search(content):
        new_content = pattern.sub(f'tags: "{tags_str}"', content, count=1)
        if new_content != content:
            file_path.write_text(new_content, encoding="utf-8")
            return True
    else:
        # If it doesn't have a tags line, we inject it right after title
        title_pat = re.compile(r"^(title:\s*.*)$", re.MULTILINE)
        if title_pat.search(content):
            new_content = title_pat.sub(f'\\1\ntags: "{tags_str}"', content, count=1)
            file_path.write_text(new_content, encoding="utf-8")
            return True
    return False


def translate_tag(tag: str, lang: str, translations: dict[str, dict[str, str]]) -> str:
    """Find translated tag name or fallback to canonical English."""
    tag_lower = tag.lower()
    if tag_lower in translations and lang in translations[tag_lower]:
        return translations[tag_lower][lang]
    # Fallback: check if the tag is in canonical map
    return CANONICAL_MAP.get(tag_lower, tag)


def get_english_posts() -> list[str]:
    """Fetch all English post filenames."""
    ignored = {
        "index",
        "tags",
        "articles",
        "projects",
        "papers",
        "playlists",
        "made-with",
        "terms",
        "privacy",
    }
    return [
        file
        for file in os.listdir(POSTS_DIR)
        if file.endswith(".md") and not any(file.startswith(prefix) for prefix in ignored)
    ]


def get_english_drafts() -> list[str]:
    """Fetch all English draft filenames."""
    if not DRAFTS_DIR.is_dir():
        return []
    return [
        file
        for file in os.listdir(DRAFTS_DIR)
        if file.endswith(".md") and not file.startswith("index")
    ]


def process_single_post(
    post: str, langs: list[str], translations: dict[str, dict[str, str]]
) -> int:
    """Process a single post (English + all translations) and return updated count."""
    path = POSTS_DIR / post
    fm_dict, _, body = extract_frontmatter_and_content(path)
    current_tags = [t.strip() for t in fm_dict.get("tags", "").split(",") if t.strip()]

    cleaned = clean_tags(current_tags)
    search_text = f"{fm_dict.get('title', '')} {fm_dict.get('description', '')} {body}"
    final_tags = infer_tags(search_text, cleaned)

    updated_count = 0
    if final_tags != current_tags and update_tags_in_file(path, final_tags):
        print(f"Optimized EN post: {post} -> tags: {final_tags}")
        updated_count += 1

    for lang in langs:
        lang_post_path = POSTS_DIR / lang / post
        if lang_post_path.is_file():
            lang_fm, _, _ = extract_frontmatter_and_content(lang_post_path)
            lang_tags = [t.strip() for t in lang_fm.get("tags", "").split(",") if t.strip()]
            expected_lang_tags = clean_tags(
                [translate_tag(t, lang, translations) for t in final_tags]
            )

            if expected_lang_tags != lang_tags and update_tags_in_file(
                lang_post_path, expected_lang_tags
            ):
                print(f"Propagated tags to {lang}: {post} -> {expected_lang_tags}")
                updated_count += 1
    return updated_count


def main():
    translations = load_translations()
    print(f"Loaded {len(translations)} tag translations.")

    english_posts = get_english_posts()
    english_drafts = get_english_drafts()
    langs = [d for d in os.listdir(POSTS_DIR) if (POSTS_DIR / d).is_dir() and d != "__pycache__"]

    updated_count = sum(process_single_post(post, langs, translations) for post in english_posts)

    # Process English drafts
    for draft in english_drafts:
        path = DRAFTS_DIR / draft
        fm_dict, _, body = extract_frontmatter_and_content(path)
        current_tags = [t.strip() for t in fm_dict.get("tags", "").split(",") if t.strip()]

        cleaned = clean_tags(current_tags)
        search_text = f"{fm_dict.get('title', '')} {fm_dict.get('description', '')} {body}"
        final_tags = infer_tags(search_text, cleaned)

        if final_tags != current_tags and update_tags_in_file(path, final_tags):
            print(f"Optimized EN draft: {draft} -> tags: {final_tags}")
            updated_count += 1

    # Finally, optimize the main tags page: _posts/tags.md
    tags_md_path = POSTS_DIR / "tags.md"
    if tags_md_path.is_file():
        tags_md_content = tags_md_path.read_text(encoding="utf-8")
        new_title = "Tags Index: AI, Payments & Rust OSS - Sebastien Rousseau"
        title_pattern = re.compile(r'^title:\s*"[^"]*"\s*$', re.MULTILINE)
        if title_pattern.search(tags_md_content):
            tags_md_content = title_pattern.sub(f'title: "{new_title}"', tags_md_content, count=1)
        tags_md_path.write_text(tags_md_content, encoding="utf-8")
        print("Optimized tags.md title.")

    print(f"Successfully processed all posts. Total tag fields updated: {updated_count}")
    sys.exit(0)


if __name__ == "__main__":
    main()
