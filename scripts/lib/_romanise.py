"""Romanisation and slug derivation for locale article slugs — ADR-0012.

Every locale localises its article slug, following the translated title
(``tests/validation/test_slug_policy.py``). Deriving that slug from a
non-Latin title needs romanisation, and the scripts differ in how much of
that a character table can do:

* Greek, Cyrillic and the Indic abugidas map character-by-character. The
  Indic path applies the inherent vowel on the *source* text, because after
  mapping, "th" for a single aspirate is indistinguishable from t + h.
* Korean hangul decomposes arithmetically from the syllable block.
* Arabic and Hebrew are abjads: the short vowels are not written, so a
  table can only produce a consonant skeleton — ``altqnya`` where the house
  style is ``altiqniya``.
* Thai writes no word boundaries, so a table returns one unsegmented token.
* Japanese and Chinese need readings a table cannot hold at all.

The gap is closed by a lexicon rather than by hand-written slugs. Entries in
``_data/i18n/romanisation-lexicon.json`` map a source word or phrase to its
romanised form; lookup is longest-match at each position, which supplies the
missing vowels for ar/he and the missing word boundaries for th/ja/zh in one
mechanism. Anything absent from the lexicon still falls through to the
tables, so adding a locale costs nothing until its output is wrong.

Slugs stay reproducible: ``tests/validation/test_slug_derivable.py`` asserts
that every localised slug equals ``slugify(title, locale)``.
"""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

_LEXICON_PATH = Path(__file__).resolve().parents[2] / "_data" / "i18n" / "romanisation-lexicon.json"

# --- Greek (ISO 843 / common transliteration) ------------------------------
EL = {
    "α": "a",
    "β": "v",
    "γ": "g",
    "δ": "d",
    "ε": "e",
    "ζ": "z",
    "η": "i",
    "θ": "th",
    "ι": "i",
    "κ": "k",
    "λ": "l",
    "μ": "m",
    "ν": "n",
    "ξ": "x",
    "ο": "o",
    "π": "p",
    "ρ": "r",
    "σ": "s",
    "ς": "s",
    "τ": "t",
    "υ": "y",
    "φ": "f",
    "χ": "ch",
    "ψ": "ps",
    "ω": "o",
    "ά": "a",
    "έ": "e",
    "ή": "i",
    "ί": "i",
    "ό": "o",
    "ύ": "y",
    "ώ": "o",
    "ϊ": "i",
    "ϋ": "y",
    "ΐ": "i",
    "ΰ": "y",
}
# digraphs first
EL_DI = [
    ("ου", "ou"),
    ("αι", "ai"),
    ("ει", "ei"),
    ("οι", "oi"),
    ("ευ", "ef"),
    ("αυ", "af"),
    ("ντ", "nt"),
    ("μπ", "b"),
    ("γκ", "gk"),
    ("τσ", "ts"),
    ("τζ", "tz"),
]

# --- Cyrillic-free scripts -------------------------------------------------
# Bengali
BN = {
    "অ": "a",
    "আ": "a",
    "ই": "i",
    "ঈ": "i",
    "উ": "u",
    "ঊ": "u",
    "ঋ": "ri",
    "এ": "e",
    "ঐ": "oi",
    "ও": "o",
    "ঔ": "ou",
    "ক": "k",
    "খ": "kh",
    "গ": "g",
    "ঘ": "gh",
    "ঙ": "ng",
    "চ": "ch",
    "ছ": "chh",
    "জ": "j",
    "ঝ": "jh",
    "ঞ": "n",
    "ট": "t",
    "ঠ": "th",
    "ড": "d",
    "ঢ": "dh",
    "ণ": "n",
    "ত": "t",
    "থ": "th",
    "দ": "d",
    "ধ": "dh",
    "ন": "n",
    "প": "p",
    "ফ": "ph",
    "ব": "b",
    "ভ": "bh",
    "ম": "m",
    "য": "j",
    "র": "r",
    "ল": "l",
    "শ": "sh",
    "ষ": "sh",
    "স": "s",
    "হ": "h",
    "ড়": "r",
    "ঢ়": "rh",
    "য়": "y",
    "ৎ": "t",
    "ং": "ng",
    "ঃ": "h",
    "ঁ": "n",
    "া": "a",
    "ি": "i",
    "ী": "i",
    "ু": "u",
    "ূ": "u",
    "ৃ": "ri",
    "ে": "e",
    "ৈ": "oi",
    "ো": "o",
    "ৌ": "ou",
    "্": "",
    "০": "0",
    "১": "1",
    "২": "2",
    "৩": "3",
    "৪": "4",
    "৫": "5",
    "৬": "6",
    "৭": "7",
    "৮": "8",
    "৯": "9",
}
# Devanagari (Marathi)
MR = {
    "अ": "a",
    "आ": "a",
    "इ": "i",
    "ई": "i",
    "उ": "u",
    "ऊ": "u",
    "ऋ": "ri",
    "ए": "e",
    "ऐ": "ai",
    "ओ": "o",
    "औ": "au",
    "क": "k",
    "ख": "kh",
    "ग": "g",
    "घ": "gh",
    "ङ": "ng",
    "च": "ch",
    "छ": "chh",
    "ज": "j",
    "झ": "jh",
    "ञ": "n",
    "ट": "t",
    "ठ": "th",
    "ड": "d",
    "ढ": "dh",
    "ण": "n",
    "त": "t",
    "थ": "th",
    "द": "d",
    "ध": "dh",
    "न": "n",
    "प": "p",
    "फ": "ph",
    "ब": "b",
    "भ": "bh",
    "म": "m",
    "य": "y",
    "र": "r",
    "ल": "l",
    "व": "v",
    "श": "sh",
    "ष": "sh",
    "स": "s",
    "ह": "h",
    "ळ": "l",
    "ऱ": "r",
    "ऴ": "l",
    "क्ष": "ksh",
    "ज्ञ": "dny",
    "ा": "a",
    "ॉ": "o",
    "ॅ": "e",
    "ॊ": "o",
    "ि": "i",
    "ी": "i",
    "ु": "u",
    "ू": "u",
    "ृ": "ri",
    "े": "e",
    "ै": "ai",
    "ो": "o",
    "ौ": "au",
    "्": "",
    "ं": "n",
    "ः": "h",
    "ँ": "n",
    "़": "",
    "०": "0",
    "१": "1",
    "२": "2",
    "३": "3",
    "४": "4",
    "५": "5",
    "६": "6",
    "७": "7",
    "८": "8",
    "९": "9",
}
# Tamil
TA = {
    "அ": "a",
    "ஆ": "aa",
    "இ": "i",
    "ஈ": "ii",
    "உ": "u",
    "ஊ": "uu",
    "எ": "e",
    "ஏ": "ee",
    "ஐ": "ai",
    "ஒ": "o",
    "ஓ": "oo",
    "ஔ": "au",
    "க": "k",
    "ங": "ng",
    "ச": "ch",
    "ஞ": "nj",
    "ட": "t",
    "ண": "n",
    "த": "th",
    "ந": "n",
    "ப": "p",
    "ம": "m",
    "ய": "y",
    "ர": "r",
    "ல": "l",
    "வ": "v",
    "ழ": "zh",
    "ள": "l",
    "ற": "r",
    "ன": "n",
    "ஜ": "j",
    "ஷ": "sh",
    "ஸ": "s",
    "ஹ": "h",
    "ா": "a",
    "ி": "i",
    "ீ": "i",
    "ு": "u",
    "ூ": "u",
    "ெ": "e",
    "ே": "e",
    "ை": "ai",
    "ொ": "o",
    "ோ": "o",
    "ௌ": "au",
    "்": "",
    "ஃ": "h",
}
# Telugu
TE = {
    "అ": "a",
    "ఆ": "aa",
    "ఇ": "i",
    "ఈ": "ii",
    "ఉ": "u",
    "ఊ": "uu",
    "ఋ": "ru",
    "ఎ": "e",
    "ఏ": "ee",
    "ఐ": "ai",
    "ఒ": "o",
    "ఓ": "oo",
    "ఔ": "au",
    "క": "k",
    "ఖ": "kh",
    "గ": "g",
    "ఘ": "gh",
    "ఙ": "ng",
    "చ": "ch",
    "ఛ": "chh",
    "జ": "j",
    "ఝ": "jh",
    "ఞ": "n",
    "ట": "t",
    "ఠ": "th",
    "డ": "d",
    "ఢ": "dh",
    "ణ": "n",
    "త": "t",
    "థ": "th",
    "ద": "d",
    "ధ": "dh",
    "న": "n",
    "ప": "p",
    "ఫ": "ph",
    "బ": "b",
    "భ": "bh",
    "మ": "m",
    "య": "y",
    "ర": "r",
    "ల": "l",
    "వ": "v",
    "శ": "sh",
    "ష": "sh",
    "స": "s",
    "హ": "h",
    "ళ": "l",
    "ా": "a",
    "ి": "i",
    "ీ": "i",
    "ు": "u",
    "ూ": "u",
    "ృ": "ru",
    "ె": "e",
    "ే": "e",
    "ై": "ai",
    "ొ": "o",
    "ో": "o",
    "ౌ": "au",
    "్": "",
    "ం": "m",
    "ః": "h",
}
# Arabic / Persian
AR = {
    "ا": "a",
    "أ": "a",
    "إ": "i",
    "آ": "aa",
    "ب": "b",
    "ت": "t",
    "ث": "th",
    "ج": "j",
    "ح": "h",
    "خ": "kh",
    "د": "d",
    "ذ": "dh",
    "ر": "r",
    "ز": "z",
    "س": "s",
    "ش": "sh",
    "ص": "s",
    "ض": "d",
    "ط": "t",
    "ظ": "z",
    "ع": "a",
    "غ": "gh",
    "ف": "f",
    "ق": "q",
    "ك": "k",
    "ل": "l",
    "م": "m",
    "ن": "n",
    "ه": "h",
    "و": "w",
    "ي": "y",
    "ى": "a",
    "ة": "a",
    "ء": "",
    "ؤ": "u",
    "ئ": "i",
    "لا": "la",
    "پ": "p",
    "چ": "ch",
    "ژ": "zh",
    "گ": "g",
    "ک": "k",
    "ی": "y",
    "ً": "",
    "ٌ": "",
    "ٍ": "",
    "َ": "a",
    "ُ": "u",
    "ِ": "i",
    "ّ": "",
    "ْ": "",
    "ـ": "",
    "٠": "0",
    "١": "1",
    "٢": "2",
    "٣": "3",
    "٤": "4",
    "٥": "5",
    "٦": "6",
    "٧": "7",
    "٨": "8",
    "٩": "9",
    "۰": "0",
    "۱": "1",
    "۲": "2",
    "۳": "3",
    "۴": "4",
    "۵": "5",
    "۶": "6",
    "۷": "7",
    "۸": "8",
    "۹": "9",
}
# Hebrew
HE = {
    "א": "a",
    "ב": "b",
    "ג": "g",
    "ד": "d",
    "ה": "h",
    "ו": "v",
    "ז": "z",
    "ח": "ch",
    "ט": "t",
    "י": "y",
    "כ": "k",
    "ך": "k",
    "ל": "l",
    "מ": "m",
    "ם": "m",
    "נ": "n",
    "ן": "n",
    "ס": "s",
    "ע": "a",
    "פ": "p",
    "ף": "f",
    "צ": "ts",
    "ץ": "ts",
    "ק": "k",
    "ר": "r",
    "ש": "sh",
    "ת": "t",
    "׳": "",
    "״": "",
}
# --- Cyrillic (ru / uk), matching the existing house slugs -----------------
# ru: "itogi-goda", "samyi-bystryi-staticheskii-generator-na-rust"
# uk: "pidsumky-roku", "naishvydshyi-rust-statychnyy-henerator"
RU = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "e",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "kh",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "shch",
    "ъ": "",
    "ы": "y",
    "ь": "",
    "э": "e",
    "ю": "yu",
    "я": "ya",
}
UK = dict(RU)
UK.update({"г": "h", "ґ": "g", "и": "y", "і": "i", "ї": "yi", "є": "ye", "\u0027": ""})

TABLES = {
    "el": EL,
    "ru": RU,
    "uk": UK,
    "hi": MR,
    "bn": BN,
    "mr": MR,
    "ta": TA,
    "te": TE,
    "ar": AR,
    "fa": AR,
    "he": HE,
}
DIGRAPHS = {"el": EL_DI}

# Stopwords per locale (romanised), dropped when shortening.
STOP = {
    "th": {"nai", "khong", "lae", "thi", "kap", "pen", "mi", "kan", "dai", "cha", "rue", "tho"},
    "ko": {"eul", "reul", "eun", "neun", "i", "ga", "e", "eseo", "wa", "gwa", "ui", "do", "man"},
    "ru": {
        "i",
        "v",
        "na",
        "s",
        "po",
        "dlya",
        "ot",
        "do",
        "za",
        "kak",
        "chto",
        "eto",
        "ne",
        "pri",
        "iz",
    },
    "uk": {
        "i",
        "v",
        "na",
        "z",
        "po",
        "dlya",
        "vid",
        "do",
        "za",
        "yak",
        "shcho",
        "tse",
        "ne",
        "pry",
        "iz",
    },
    "hi": {"ke", "ki", "ka", "mein", "se", "aur", "par", "hai", "ko", "ek", "ye", "is"},
    "el": {
        "kai",
        "to",
        "tis",
        "tou",
        "ton",
        "ti",
        "sto",
        "stin",
        "gia",
        "me",
        "apo",
        "o",
        "i",
        "ta",
        "tha",
        "einai",
        "pos",
    },
    "bn": {"o", "ebong", "er", "e", "theke", "jonno", "ki", "ta", "a", "ar", "na", "hoy", "sale"},
    "mr": {"ani", "cha", "chi", "che", "la", "madhye", "var", "ahe", "ka", "ha", "he", "ya", "na"},
    "ta": {"matrum", "oru", "indha", "antha", "en", "athu", "mel", "il", "ai", "ku"},
    "te": {"mariyu", "oka", "ee", "aa", "lo", "ki", "ku", "tho", "nundi", "ela"},
    "ar": {
        "al",
        "wa",
        "fi",
        "min",
        "ila",
        "ala",
        "an",
        "ma",
        "hadha",
        "allati",
        "allathi",
        "li",
        "bi",
        "la",
    },
    "fa": {"va", "dar", "az", "be", "ba", "ke", "in", "an", "ra", "bar", "ast", "mi"},
    "he": {"ve", "ha", "be", "le", "shel", "al", "im", "et", "me", "ki"},
    "hu": {
        "a",
        "az",
        "es",
        "egy",
        "hogy",
        "nem",
        "is",
        "mint",
        "vagy",
        "ez",
        "ezt",
        "ami",
        "meg",
        "fel",
        "ki",
        "be",
    },
    "ms": {
        "dan",
        "yang",
        "di",
        "ke",
        "dari",
        "untuk",
        "pada",
        "ini",
        "itu",
        "adalah",
        "dengan",
        "akan",
        "atau",
    },
    "ro": {
        "si",
        "in",
        "la",
        "de",
        "pe",
        "cu",
        "un",
        "o",
        "este",
        "pentru",
        "care",
        "din",
        "ce",
        "ale",
        "al",
    },
    "ha": {"da", "na", "a", "ta", "ya", "ga", "ba", "wanda", "don", "ne", "ce", "ko", "sai"},
    "yo": {"ati", "ni", "ti", "si", "fun", "lati", "pe", "ki", "awon", "ba", "lo", "wa", "je"},
    "vi": {"cua", "va", "cho", "tu", "den", "trong", "nam", "la", "cac", "nhung", "voi", "ve"},
    "tr": {"da", "de", "ve", "ile", "icin", "bir", "bu", "ki", "ya", "mi"},
    "cs": {
        "a",
        "v",
        "na",
        "pro",
        "se",
        "je",
        "od",
        "do",
        "po",
        "za",
        "ke",
        "ku",
        "o",
        "u",
        "s",
        "z",
    },
    "de": {
        "der",
        "die",
        "das",
        "und",
        "fur",
        "von",
        "mit",
        "im",
        "in",
        "den",
        "dem",
        "des",
        "zu",
        "auf",
        "ein",
        "eine",
    },
    "es": {
        "el",
        "la",
        "los",
        "las",
        "de",
        "del",
        "y",
        "en",
        "para",
        "con",
        "un",
        "una",
        "al",
        "por",
        "que",
    },
    "fr": {
        "le",
        "la",
        "les",
        "des",
        "du",
        "de",
        "et",
        "en",
        "pour",
        "avec",
        "un",
        "une",
        "au",
        "aux",
        "dans",
        "qui",
    },
    "fil": {"ang", "ng", "mga", "sa", "at", "na", "ay", "para", "ito", "isang", "nang"},
    "id": {
        "dan",
        "yang",
        "di",
        "ke",
        "dari",
        "untuk",
        "pada",
        "ini",
        "itu",
        "adalah",
        "dengan",
        "akan",
        "atau",
    },
    "it": {
        "il",
        "lo",
        "la",
        "i",
        "gli",
        "le",
        "di",
        "del",
        "della",
        "e",
        "in",
        "per",
        "con",
        "un",
        "una",
        "al",
        "che",
    },
    "nl": {"de", "het", "een", "en", "van", "voor", "met", "in", "op", "bij", "aan", "die", "dat"},
    "pl": {"i", "w", "na", "dla", "z", "do", "po", "za", "o", "u", "od", "the", "jest", "ktore"},
    "pt-br": {
        "o",
        "a",
        "os",
        "as",
        "de",
        "do",
        "da",
        "dos",
        "das",
        "e",
        "em",
        "para",
        "com",
        "um",
        "uma",
        "ao",
        "que",
    },
    "sv": {"och", "i", "pa", "for", "med", "av", "till", "den", "det", "en", "ett", "som", "att"},
}
# Latin-script diacritic folding beyond NFKD (Hausa hooked letters, Yoruba dots).
EXTRA = {
    "ɓ": "b",
    "ɗ": "d",
    "ƙ": "k",
    "ƴ": "y",
    "Ɓ": "b",
    "Ɗ": "d",
    "Ƙ": "k",
    "Ƴ": "y",
    "ẹ": "e",
    "ọ": "o",
    "ṣ": "s",
    "Ẹ": "e",
    "Ọ": "o",
    "Ṣ": "s",
    "ŋ": "n",
    "đ": "d",
    "Đ": "d",
    "ı": "i",
    "İ": "i",
}


_LEXICON_CACHE: dict[str, dict[str, str]] | None = None


def lexicon() -> dict[str, dict[str, str]]:
    """The reviewed source-word → romanisation map, keyed by locale."""
    global _LEXICON_CACHE
    if _LEXICON_CACHE is None:
        raw = json.loads(_LEXICON_PATH.read_text(encoding="utf-8"))
        _LEXICON_CACHE = {k: v for k, v in raw.items() if not k.startswith("$")}
    return _LEXICON_CACHE


def _apply_lexicon(text: str, code: str) -> str:
    """Replace the longest lexicon match at each position.

    Longest-match is what makes this work for the unsegmented scripts: a
    Thai or Chinese title has no spaces, so the entry boundaries *are* the
    word boundaries. Each hit is emitted space-padded, which is why the
    caller can then split on non-alphanumerics and get real words.
    """
    entries = lexicon().get(code)
    if not entries:
        return text
    lengths = sorted({len(k) for k in entries}, reverse=True)
    out: list[str] = []
    i, n = 0, len(text)
    while i < n:
        for size in lengths:
            if size > n - i:
                continue
            hit = entries.get(text[i : i + size])
            if hit is not None:
                out.append(f" {hit} ")
                i += size
                break
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def _script_pass(text: str, code: str) -> str:
    """Apply whichever romanisation the locale's script needs."""
    if code == "th":
        return th_romanise(text)
    if code == "ko":
        return ko_romanise(text)
    if code in _CONS_RANGES:
        return indic_romanise(text, code)
    tbl = TABLES.get(code)
    return "".join(tbl.get(ch, ch) for ch in text) if tbl else text


def romanise(text: str, code: str) -> str:
    text = text.replace("‌", "").replace("‍", "")
    text = _apply_lexicon(text, code)
    if code in TABLES:
        # Tables are keyed on lowercase. Without folding, capitals fall
        # through the map and the ASCII filter eats them — silently, and
        # only on words that happen to start a sentence or a proper noun.
        # Greek lost "Μια" -> "ia"; Cyrillic lost "Від" -> "id" and
        # dropped "От" entirely. Scripts without case are unaffected.
        text = text.lower()
    for src, dst in DIGRAPHS.get(code, []):
        text = text.replace(src, dst)
    text = _script_pass(text, code)
    text = "".join(EXTRA.get(ch, ch) for ch in text)
    text = unicodedata.normalize("NFKD", text)
    return "".join(c for c in text if not unicodedata.combining(c))


def _trim_tail(kept: list[str], stop: set[str], min_words: int) -> None:
    """Drop a dangling stopword or two-letter fragment off the end.

    The word cap cuts mid-phrase, which used to leave slugs ending "...-janj",
    "...-post", "...-se".
    """
    while len(kept) > min_words and (
        kept[-1] in stop or (len(kept[-1]) <= 2 and not kept[-1].isdigit())
    ):
        kept.pop()


def _shorten(kept: list[str], stop: set[str], min_words: int) -> str:
    """Trim the tail, then drop words until the slug fits the length bound."""
    _trim_tail(kept, stop, min_words)
    out = "-".join(kept)
    while len(out) > 76 and len(kept) > min_words:  # 76 + 11-char date prefix < 90
        kept.pop()
        _trim_tail(kept, stop, min_words)
        out = "-".join(kept)
    return out


def _keeps(
    word: str,
    kept: list[str],
    seen: set[str],
    skip: frozenset[str],
    stop: set[str],
    min_words: int,
) -> bool:
    """Whether ``word`` earns a slot in the slug."""
    if word in seen or word in skip:
        return False  # no repeated tokens, and never the post's own year
    if word in stop and (not kept or len(kept) >= min_words):
        return False  # a slug should neither open nor trail on a stopword
    if len(word) == 1 and not word.isdigit():
        return False
    # A leading two-letter fragment is never the topic ("da-bankalar…").
    return not (not kept and len(word) <= 2 and not word.isdigit())


def _backfill(kept: list[str], seen: set[str], words: list[str], min_words: int) -> None:
    """A title that is almost all stopwords still needs a usable slug."""
    for w in words:
        if w not in seen and len(w) > 1:
            kept.append(w)
            seen.add(w)
        if len(kept) >= min_words:
            return


def slugify(
    title: str,
    code: str,
    max_words: int = 6,
    min_words: int = 2,
    skip: frozenset[str] = frozenset(),
) -> str:
    """Derive the slug body (no date prefix) from a translated title."""
    r = romanise(title, code).lower().replace("&", " and ")
    words = [w for w in re.split(r"[^a-z0-9]+", r) if w]
    stop = STOP.get(code, set())
    kept: list[str] = []
    seen: set[str] = set()
    for w in words:
        if len(kept) >= max_words:
            break
        if _keeps(w, kept, seen, skip, stop, min_words):
            kept.append(w)
            seen.add(w)
    if len(kept) < min_words:
        _backfill(kept, seen, words, min_words)
    return _shorten(kept, stop, min_words)


# zh-hant slugs all carry a "-tw" suffix; it is the only locale that marks the
# script variant in the URL, and all 105 of its posts follow the convention.
_SUFFIX = {"zh-hant": "-tw"}


def derive_slug(title: str, code: str, year: str | None = None) -> str:
    """Full slug body for a post: ``slugify`` plus the locale conventions.

    ``year`` is the post's own year. A title that opens with it ("2026 में
    बैंकों…", "2026'da bankalar…") would otherwise repeat the date already in
    the filename prefix, giving ``2026-07-03-2026-...``.
    """
    body = slugify(title, code, skip=frozenset({year}) if year else frozenset())
    suffix = _SUFFIX.get(code, "")
    if suffix and not body.endswith(suffix):
        body += suffix
    return body


# --- Indic inherent vowel --------------------------------------------------
# A consonant carries an implicit 'a' unless a vowel sign (matra) or the
# virama follows. Applying that on the SOURCE text is the only place the
# distinction survives: after mapping, "th" for a single aspirate is
# indistinguishable from t+h, which is what broke the first attempt
# (prthm -> partahm instead of pratham).
_VIRAMA = {"hi": "\u094d", "bn": "\u09cd", "mr": "\u094d", "te": "\u0c4d", "ta": "\u0bcd"}
_MATRA = {
    "hi": set("\u093e\u093f\u0940\u0941\u0942\u0943\u0947\u0948\u094b\u094c\u0949\u0945\u094a"),
    "bn": set("\u09be\u09bf\u09c0\u09c1\u09c2\u09c3\u09c7\u09c8\u09cb\u09cc\u09d7"),
    "mr": set("\u093e\u093f\u0940\u0941\u0942\u0943\u0947\u0948\u094b\u094c\u0949\u0945\u094a"),
    "te": set("\u0c3e\u0c3f\u0c40\u0c41\u0c42\u0c43\u0c46\u0c47\u0c48\u0c4a\u0c4b\u0c4c"),
    "ta": set("\u0bbe\u0bbf\u0bc0\u0bc1\u0bc2\u0bc6\u0bc7\u0bc8\u0bca\u0bcb\u0bcc"),
}
_CONS_RANGES = {
    "hi": ("\u0915", "\u0939"),
    "bn": ("\u0995", "\u09b9"),
    "mr": ("\u0915", "\u0939"),
    "te": ("\u0c15", "\u0c39"),
    "ta": ("\u0b95", "\u0bb9"),
}


def _is_cons(ch: str, code: str) -> bool:
    lo, hi = _CONS_RANGES[code]
    return lo <= ch <= hi


_FINAL_SCHWA_DROP = {"hi", "bn", "mr"}


def _has_inherent_vowel(nxt: str, code: str, vir: str, matra: set[str]) -> bool:
    """Whether a consonant carries its implicit 'a'.

    It does unless a vowel sign or the virama follows — except word-finally in
    the languages that drop the final schwa (hi/bn/mr say "pratham", not
    "prathama").
    """
    if nxt == vir or nxt in matra:
        return False
    # nxt is neither the virama nor a matra by now, so a non-consonant here
    # (or the end of the string) means the syllable ends the word.
    word_end = nxt == "" or not _is_cons(nxt, code)
    return not (word_end and code in _FINAL_SCHWA_DROP)


def indic_romanise(text: str, code: str) -> str:
    tbl, out = TABLES[code], []
    vir, matra = _VIRAMA[code], _MATRA[code]
    for i, ch in enumerate(text):
        if ch == vir:
            continue
        out.append(tbl.get(ch, ch))
        if _is_cons(ch, code):
            nxt = text[i + 1] if i + 1 < len(text) else ""
            if _has_inherent_vowel(nxt, code, vir, matra):
                out.append("a")
    return "".join(out)


# --- Korean (Revised Romanization) -----------------------------------------
# Hangul syllables are algorithmic, not a lookup: U+AC00 + initial*588 +
# medial*28 + final. So this is exact rather than approximate, unlike the
# Semitic tables. Matches the house style already in ko slugs
# ("yeongan-chongjeong", "beulrokchein").
_KO_INITIAL = [
    "g",
    "kk",
    "n",
    "d",
    "tt",
    "r",
    "m",
    "b",
    "pp",
    "s",
    "ss",
    "",
    "j",
    "jj",
    "ch",
    "k",
    "t",
    "p",
    "h",
]
_KO_MEDIAL = [
    "a",
    "ae",
    "ya",
    "yae",
    "eo",
    "e",
    "yeo",
    "ye",
    "o",
    "wa",
    "wae",
    "oe",
    "yo",
    "u",
    "wo",
    "we",
    "wi",
    "yu",
    "eu",
    "ui",
    "i",
]
_KO_FINAL = [
    "",
    "k",
    "k",
    "ks",
    "n",
    "nj",
    "nh",
    "t",
    "l",
    "lk",
    "lm",
    "lb",
    "ls",
    "lt",
    "lp",
    "lh",
    "m",
    "p",
    "ps",
    "t",
    "t",
    "ng",
    "t",
    "t",
    "k",
    "t",
    "p",
    "t",
]


def ko_romanise(text: str) -> str:
    out = []
    for ch in text:
        code = ord(ch) - 0xAC00
        if 0 <= code < 11172:
            out.append(_KO_INITIAL[code // 588])
            out.append(_KO_MEDIAL[(code % 588) // 28])
            out.append(_KO_FINAL[code % 28])
        else:
            out.append(ch)
    return "".join(out)


# --- Thai (RTGS-flavoured) -------------------------------------------------
# Thai is an alphabet, not a syllabary: 61 distinct characters across all the
# titles, so a table covers it the way it covers Greek and Cyrillic. Vowels
# that are written before their consonant are reordered by _TH_PRE below;
# tone marks carry no romanisation and are dropped. Matches the house style
# already in th slugs ("thopthuan-pi", "theknoloyi").
TH = {
    "ก": "k",
    "ข": "kh",
    "ฃ": "kh",
    "ค": "kh",
    "ฅ": "kh",
    "ฆ": "kh",
    "ง": "ng",
    "จ": "ch",
    "ฉ": "ch",
    "ช": "ch",
    "ซ": "s",
    "ฌ": "ch",
    "ญ": "y",
    "ฎ": "d",
    "ฏ": "t",
    "ฐ": "th",
    "ฑ": "th",
    "ฒ": "th",
    "ณ": "n",
    "ด": "d",
    "ต": "t",
    "ถ": "th",
    "ท": "th",
    "ธ": "th",
    "น": "n",
    "บ": "b",
    "ป": "p",
    "ผ": "ph",
    "ฝ": "f",
    "พ": "ph",
    "ฟ": "f",
    "ภ": "ph",
    "ม": "m",
    "ย": "y",
    "ร": "r",
    "ฤ": "rue",
    "ล": "l",
    "ฦ": "lue",
    "ว": "w",
    "ศ": "s",
    "ษ": "s",
    "ส": "s",
    "ห": "h",
    "ฬ": "l",
    "อ": "o",
    "ฮ": "h",
    "ะ": "a",
    "ั": "a",
    "า": "a",
    "ำ": "am",
    "ิ": "i",
    "ี": "i",
    "ึ": "ue",
    "ื": "ue",
    "ุ": "u",
    "ู": "u",
    "ๅ": "a",
    "ๆ": "",
    "็": "",
    "์": "",
    "ฺ": "",
    "่": "",
    "้": "",
    "๊": "",
    "๋": "",
    "ํ": "",
    "๎": "",
    "๐": "0",
    "๑": "1",
    "๒": "2",
    "๓": "3",
    "๔": "4",
    "๕": "5",
    "๖": "6",
    "๗": "7",
    "๘": "8",
    "๙": "9",
}
# Vowels written to the LEFT of the consonant they follow in speech.
_TH_PRE = {"เ": "e", "แ": "ae", "โ": "o", "ใ": "ai", "ไ": "ai"}


def th_romanise(text: str) -> str:
    out, i = [], 0
    while i < len(text):
        ch = text[i]
        if ch in _TH_PRE:
            # Reorder: the glyph precedes its consonant on the page but
            # follows it when spoken, so emit the consonant first.
            j = i + 1
            cons = []
            while j < len(text) and text[j] in TH and TH[text[j]] and text[j] not in _TH_PRE:
                cons.append(TH[text[j]])
                if len(cons) >= 2:
                    break
                j += 1
            out.append("".join(cons[:1]) or "")
            out.append(_TH_PRE[ch])
            out.extend(cons[1:])
            i = j + 1 if cons else i + 1
            continue
        out.append(TH.get(ch, ch))
        i += 1
    return "".join(out)
