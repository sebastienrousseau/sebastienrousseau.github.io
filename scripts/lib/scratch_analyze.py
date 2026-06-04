#!/usr/bin/env python3
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from refine_all import DRAFTS
from readability import count_syllables, analyze_text

def analyze_draft(name):
    text = DRAFTS[name]
    fre, fkgl, s, w, syl = analyze_text(text)
    print(f"Draft: {name}")
    print(f"FRE: {fre:.2f}, FKGL: {fkgl:.2f}, Sentences: {s}, Words: {w}, Syllables: {syl}")
    
    # Strip blocks like analyze_text does to see raw words
    t = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    t = re.sub(r"<[^>]*>", "", t)
    t = re.sub(r"`[^`]*`", "", t)
    t = re.sub(r"!\[.*?\]\(.*?\)", "", t)
    t = re.sub(r"\[(.*?)]\(.*?\)", r"\1", t)
    
    words = re.findall(r"\b[a-zA-Z']+\b", t)
    # Count syllables for each word
    word_syls = [(w, count_syllables(w)) for w in words]
    # Sort by syllable count descending
    sorted_words = sorted(word_syls, key=lambda x: x[1], reverse=True)
    
    print("\nTop 30 longest words by syllable count:")
    seen = set()
    count = 0
    for word, syl_cnt in sorted_words:
        wl = word.lower()
        if wl not in seen:
            seen.add(wl)
            print(f"  {word}: {syl_cnt}")
            count += 1
            if count >= 30:
                break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        analyze_draft(sys.argv[1])
    else:
        print("Provide a draft name, e.g. project-docs/SECURITY.md")
