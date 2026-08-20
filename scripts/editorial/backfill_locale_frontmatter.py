#!/usr/bin/env python3
"""Backfill ``title:``, ``excerpt:``, ``subtitle:`` and ``tags:`` in
``_posts/<lang>/<slug>.md`` from the article body when the frontmatter
is still English **and** the body is in the target locale.

Why this exists
---------------

A subset of locale articles shipped with translated body prose but
frontmatter still copied verbatim from the EN source. The publish-time
sub-agent translated the body but skipped the SEO frontmatter for
older articles, because the "translate frontmatter SEO fields too"
rule landed later in the routine.

That mismatch was invisible until ``rewrite_newsroom_card_titles``
started reading ``excerpt:`` and ``tags:`` from those frontmatter
fields (PR #123) — at which point the cards on every locale home
suddenly render in English for the affected articles even though the
*article page* opens in the correct language.

What this fixes
---------------

For each locale article whose frontmatter ``title:`` looks English,
extract from the already-translated body:

  - The first ``# H1`` heading                                → new ``title:``
  - The first ``<p class="post-lead-tldr">…</p>`` block
    (``<strong>`` boilerplate stripped)                        → new ``excerpt:``

Crucially, before writing, the script confirms the **extracted text is
in the target locale**, not English. Detection uses two passes:

  1. **Non-Latin scripts** (ZH, JA, KO, AR, HE, HI, BN, TH) — require
     at least one character from the locale's Unicode range. If the
     body H1 contains zero CJK / Arabic / Devanagari / Thai / etc.
     characters for those locales, it's still English in the body too
     and we leave the frontmatter alone.

  2. **Latin-script locales** (FR, ES, DE, IT, PT-BR, NL, PL, CS, UK,
     RO, TR, FIL, HA, YO, SV, VI, ID) — use a per-locale stop-word
     dictionary to flag text as belonging to that locale, and a richer
     English-word dictionary to flag text as English. Heuristic:
     locale score > 0 **and** locale score > english score → accept.

The script is idempotent — re-running on a previously-fixed file is a
no-op because the existing frontmatter no longer looks English.

Older locale files (pre-2026) often have ENGLISH body text too —
those articles were never actually translated, just had locale URLs
allocated. The language-detection guard catches that and leaves them
alone rather than baking English text into the frontmatter.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POSTS = ROOT / "_posts"

LOCALES = [
    "fr",
    "es",
    "de",
    "it",
    "pt-br",
    "nl",
    "ja",
    "zh-hans",
    "zh-hant",
    "ko",
    "ar",
    "ru",
    "pl",
    "cs",
    "uk",
    "ro",
    "tr",
    "he",
    "hi",
    "bn",
    "id",
    "vi",
    "th",
    "fil",
    "ha",
    "yo",
    "sv",
]

_DATED_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-.+\.md$")

# ---------------------------------------------------------------------------
# Language detection
# ---------------------------------------------------------------------------

# Per-locale character-range tests. Each pattern, if it matches at least
# once in the text, is strong evidence the text is in that locale. Use
# only for locales whose script is distinct from Latin EN.
_SCRIPT_RANGES: dict[str, re.Pattern[str]] = {
    "zh-hans": re.compile(r"[一-鿿]"),
    "zh-hant": re.compile(r"[一-鿿]"),
    "ja": re.compile(r"[぀-ゟ゠-ヿ]"),  # Hiragana + Katakana
    "ko": re.compile(r"[가-힯]"),  # Hangul
    "ar": re.compile(r"[؀-ۿ]"),
    "he": re.compile(r"[֐-׿]"),
    "hi": re.compile(r"[ऀ-ॿ]"),  # Devanagari
    "bn": re.compile(r"[ঀ-৿]"),  # Bengali
    "th": re.compile(r"[฀-๿]"),
    "ru": re.compile(r"[Ѐ-ӿ]"),  # Cyrillic
    "uk": re.compile(r"[Ѐ-ӿ]"),
}

# Locales whose Latin alphabet uses diacritics or special characters
# rarely seen in English. Presence is a positive signal for that locale.
_LATIN_DIACRITICS: dict[str, re.Pattern[str]] = {
    "fr": re.compile(r"[àâçéèêëîïôùûüœÀÂÇÉÈÊËÎÏÔÙÛÜŒ]"),
    "es": re.compile(r"[ñáéíóúüÑÁÉÍÓÚÜ¿¡]"),
    "de": re.compile(r"[äöüßÄÖÜ]"),
    "it": re.compile(r"[àèéìòùÀÈÉÌÒÙ]"),
    "pt-br": re.compile(r"[ãõáéíóúâêôçÃÕÁÉÍÓÚÂÊÔÇ]"),
    "nl": re.compile(r"[ëïóüáéàèíúÉËÏÓÜ]"),
    "pl": re.compile(r"[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]"),
    "cs": re.compile(r"[áčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ]"),
    "ro": re.compile(r"[ăâîșțĂÂÎȘȚ]"),
    "tr": re.compile(r"[çğıİöşüÇĞÖŞÜ]"),
    "vi": re.compile(
        r"[àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴĐ]"
    ),
    "sv": re.compile(r"[åäöÅÄÖ]"),
    "yo": re.compile(r"[àáèéẹ̀́ìíọùúṣṢẸỌ]"),  # tonal vowels
    "ha": re.compile(r"[ɓɗƙƴ]"),  # implosive consonants
}

# Stop-words per locale — short common words that English doesn't share.
# Used as a secondary signal for Latin-script locales where diacritics
# might not appear in a short title.
# Per-locale stop-word sets live in _data/i18n/locale-stopwords.json (extracted
# from a 500-line inline dict for data/code separation, Phase 4.1). Used as a
# secondary Latin-script locale signal by _is_in_target_locale.
_LOCALE_STOPWORDS: dict[str, frozenset[str]] = {
    lang: frozenset(words)
    for lang, words in json.loads(
        (ROOT / "_data" / "i18n" / "locale-stopwords.json").read_text(encoding="utf-8")
    ).items()
}

# Distinctly English stop-words / phrases — strong signal text is EN.
_EN_STOPWORDS: frozenset[str] = frozenset(
    [
        "the",
        "and",
        "of",
        "to",
        "a",
        "in",
        "is",
        "for",
        "on",
        "with",
        "by",
        "from",
        "at",
        "as",
        "an",
        "be",
        "this",
        "that",
        "are",
        "or",
        "but",
        "not",
        "have",
        "has",
        "will",
        "would",
        "could",
        "should",
        "which",
        "who",
        "whose",
        "where",
        "when",
        "how",
        "why",
        "their",
        "our",
        "your",
        "his",
        "her",
        "its",
        "also",
        "more",
        "most",
        "some",
        "any",
        "all",
        "both",
        "each",
        "every",
        "few",
        "many",
        "other",
        "such",
        "no",
        "nor",
        "only",
        "own",
        "same",
        "than",
        "too",
        "very",
        "into",
        "through",
        "during",
        "before",
        "after",
        "between",
        "during",
        "above",
        "below",
        "within",
        "without",
    ]
)


def _tokenize(text: str) -> list[str]:
    """Lower-case word tokens; only letter-runs, no punctuation."""
    return re.findall(
        r"[a-zA-ZàâäéèêëîïôöùûüçÀÂÄÉÈÊËÎÏÔÖÙÛÜÇñÑáíóúÁÍÓÚãõÃÕßąćęłńśźżĄĆĘŁŃŚŹŻčďěňřšťůýžČĎĚŇŘŠŤŮÝŽășțĂȘȚğıİşĞŞ]+",
        text.lower(),
    )


def _is_in_target_locale(text: str, locale: str) -> bool:
    """Best-effort test that ``text`` is in ``locale`` and not English.
    Returns True only when there's positive evidence for the locale and
    not overwhelming evidence it's English."""
    if not text or not text.strip():
        return False
    # Non-Latin script: require at least one in-script character.
    script_re = _SCRIPT_RANGES.get(locale)
    if script_re is not None:
        return script_re.search(text) is not None
    return _latin_locale_verdict(text, locale)


def _stopword_hits(tokens: list[str], stops: frozenset[str]) -> int:
    """How many of ``tokens`` are stop-words in ``stops``."""
    return sum(1 for t in tokens if t in stops)


def _latin_locale_verdict(text: str, locale: str) -> bool:
    """Latin-script decision: combine diacritic detection + stop-word signal.

    Latin locales share an alphabet with English, so no single character
    proves anything; the verdict needs both signals weighed together.
    """
    tokens = _tokenize(text)
    if not tokens:
        return False
    diacritic_re = _LATIN_DIACRITICS.get(locale)
    has_diacritic = bool(diacritic_re and diacritic_re.search(text))
    locale_score = _stopword_hits(tokens, _LOCALE_STOPWORDS.get(locale, frozenset()))
    en_score = _stopword_hits(tokens, _EN_STOPWORDS)
    # Decision rule:
    #   - diacritic + any locale stop-word: clearly the locale
    #   - locale stop-words > EN stop-words: locale
    #   - everything else: not confidently locale → leave alone
    if has_diacritic and locale_score >= 1:
        return True
    if locale_score >= 2 and locale_score > en_score:
        return True
    return locale_score >= 1 and en_score == 0


# ---------------------------------------------------------------------------
# Frontmatter rewriting
# ---------------------------------------------------------------------------

_EN_TITLE_MARKERS = (
    "The ",
    " and ",
    " of the ",
    " the ",
    " is ",
    " for ",
    " from ",
    "with the",
    " in 2026",
    " in 2025",
    "Banking",
    "Quantum",
    "Tokenised",
    "Tokenized",
    "Stablecoin",
    "Cloud Native",
)


def _looks_english_field(text: str | None) -> bool:
    """Lightweight EN heuristic for the *existing* frontmatter value —
    decides whether we *want* to overwrite. Different from
    ``_is_in_target_locale`` which checks whether the *replacement* is OK."""
    if not text:
        return False
    s = text[:240]
    if any(m in s for m in _EN_TITLE_MARKERS):
        return True
    tokens = _tokenize(s)
    if not tokens:
        return False
    en_score = sum(1 for t in tokens if t in _EN_STOPWORDS)
    return en_score >= 2


def _read_field(fm: str, name: str) -> str | None:
    m = re.search(rf'^{re.escape(name)}:\s*"((?:[^"\\]|\\.)*)"', fm, re.MULTILINE)
    return m.group(1) if m else None


def _replace_field(fm: str, name: str, new_value: str) -> str:
    escaped = new_value.replace("\\", "\\\\").replace('"', '\\"')
    return re.sub(
        rf'(^{re.escape(name)}:\s*)"(?:[^"\\]|\\.)*"',
        rf'\g<1>"{escaped}"',
        fm,
        count=1,
        flags=re.MULTILINE,
    )


def _insert_excerpt_after_title(fm: str, value: str) -> str:
    """Insert an ``excerpt:`` line right after ``title:``."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return re.sub(
        r"(^title:[^\n]*\n)",
        rf'\g<1>excerpt: "{escaped}"\n',
        fm,
        count=1,
        flags=re.MULTILINE,
    )


def _split_frontmatter(text: str) -> tuple[str, str] | None:
    lines = text.splitlines(keepends=True)
    delim_idx = [i for i, ln in enumerate(lines) if ln.strip() == "---"]
    if len(delim_idx) < 2:
        return None
    return "".join(lines[: delim_idx[1] + 1]), "".join(lines[delim_idx[1] + 1 :])


def _extract_h1(body: str) -> str | None:
    for line in body.splitlines():
        m = re.match(r"^#\s+(.+?)\s*$", line)
        if m:
            return m.group(1).strip()
    return None


def _extract_tldr(body: str) -> str | None:
    m = re.search(
        r'<p\s+class="post-lead-tldr"[^>]*>(.*?)</p>',
        body,
        re.DOTALL,
    )
    if not m:
        return None
    inner = m.group(1).strip()
    inner = re.sub(r"^<strong[^>]*>[^<]+</strong>\s*", "", inner, count=1)
    inner = re.sub(r"\s+", " ", inner).strip()
    return inner or None


def _fix_one(md: Path, locale: str) -> str | None:
    text = md.read_text(encoding="utf-8")
    split = _split_frontmatter(text)
    if not split:
        return None
    fm, body = split

    title, excerpt = _locale_candidates(fm, body, locale)
    if not title and not excerpt:
        return None

    new_fm, notes = _apply_candidates(fm, title, excerpt)
    if new_fm == fm:
        return None

    md.write_text(new_fm + body, encoding="utf-8")
    return ", ".join(notes)


def _locale_candidates(fm: str, body: str, locale: str) -> tuple[str | None, str | None]:
    """Body-derived title/excerpt worth writing back, or ``None`` per field.

    A field is a candidate only when the existing frontmatter looks English
    *and* the body's replacement is confidently in ``locale`` — otherwise
    we would be swapping English for English, which defeats the point.
    """
    existing_title = _read_field(fm, "title")
    existing_excerpt = _read_field(fm, "excerpt")

    title = _extract_h1(body) if _looks_english_field(existing_title) else None
    excerpt = (
        _extract_tldr(body)
        if existing_excerpt is None or _looks_english_field(existing_excerpt)
        else None
    )
    if title and not _is_in_target_locale(title, locale):
        title = None
    if excerpt and not _is_in_target_locale(excerpt, locale):
        excerpt = None
    return title, excerpt


def _apply_candidates(fm: str, title: str | None, excerpt: str | None) -> tuple[str, list[str]]:
    """Write the candidates into ``fm``, returning the new block and a log line."""
    new_fm = fm
    notes: list[str] = []
    if title:
        new_fm = _replace_field(new_fm, "title", title)
        notes.append(f"title→{_note_value(title)}")
    if excerpt:
        if _read_field(new_fm, "excerpt") is None:
            new_fm = _insert_excerpt_after_title(new_fm, excerpt)
        else:
            new_fm = _replace_field(new_fm, "excerpt", excerpt)
        notes.append(f"excerpt→{_note_value(excerpt)}")
    return new_fm, notes


def _note_value(value: str) -> str:
    """Quoted, ellipsised field value for the human-readable change log."""
    return f'"{value[:55]}{"…" if len(value) > 55 else ""}"'


def main() -> int:
    rewrites = 0
    files = 0
    for loc in LOCALES:
        d = POSTS / loc
        if not d.is_dir():
            continue
        for md in sorted(d.glob("*.md")):
            if not _DATED_RE.match(md.name):
                continue
            files += 1
            summary = _fix_one(md, loc)
            if summary:
                rewrites += 1
                print(f"{md.relative_to(ROOT)}: {summary}")
    print()
    print(f"backfill_locale_frontmatter: rewrote {rewrites} file(s) out of {files} scanned")
    return 0


if __name__ == "__main__":
    sys.exit(main())
