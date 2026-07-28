---
title: "Àkàndé: hlasový asistent poháněný GPT pro vedoucí pracovníky"
subtitle: "Architektura hlasového asistenta v jazyce Python s otevřeným zdrojovým kódem: Whisper, GPT-4, cache v SQLite a fpdf2"
description: "Àkàndé je hlasový asistent v jazyce Python s otevřeným zdrojovým kódem, který spojuje rozpoznávání řeči OpenAI Whisper, doplňování konverzace GPT-4 a lokální cache odpovědí v SQLite do hlasově řízeného pracovního postupu. Generuje shrnutí v PDF z historie konverzace a veškerá uložená data ponechává lokálně."
date: "Feb 12, 2024"
language: "cs-CZ"
locale: "cs_CZ"
banner: "https://cloudcdn.pro/stocks/images/akande-voice-assistant.webp"
banner_alt: "Bílé kulové moderní zařízení"
keywords: "Àkàndé, OpenAI GPT-4, Whisper STT, cache v SQLite, fpdf2, hlasový asistent v jazyce Python, chat completions API, generování shrnutí v PDF, cache SHA-256, převod textu na řeč, AI asistent pro vedoucí pracovníky, otevřený zdrojový kód"
---


> **Shrnutí pro vedení / Klíčové body**
>
> - **[Àkàndé ⧉][00]** je hlasový asistent v jazyce Python s otevřeným zdrojovým kódem, který spojuje převod řeči na text OpenAI Whisper, doplňování konverzace GPT-4, lokální cache odpovědí v SQLite a export do PDF pomocí fpdf2 do jediného hlasově řízeného pracovního postupu, jenž nevyžaduje žádné cloudové úložiště ani lokální váhy AI modelu.
> - **Cache v SQLite** ukládá hashe SHA-256 normalizovaných řetězců dotazů namapované na surový text odpovědi API; zásahy do cache stojí nula tokenů a vracejí se do 10 ms, takže opakované dotazy (například připomenutí rozhodnutí z dřívější části schůzky) jsou v podstatě zdarma.
> - **Vícekolová konverzace** se udržuje sestavováním seznamu `messages` v paměti a jeho předáváním při každém volání Chat Completions API. Model dostává celou historii relace, takže se může odkazovat na dřívější výměny, za cenu postupně rostoucí spotřeby tokenů na každé kolo.
> - **Generování shrnutí v PDF** serializuje seznam `messages` relace do formátovaného dokumentu fpdf2: kola uživatele a kola asistenta jsou označena, vkládají se časová razítka a automatické stránkování zvládne relace libovolné délky; soubor se zapisuje do lokálního souborového systému, nikoli nahrává.
> - **Hranice soukromí:** zařízení opouští pouze aktuální dotaz (a historie relace až do limitu kontextového okna). Žádné zvukové nahrávky, žádné přepisy ani žádné cachované odpovědi se neodesílají na žádnou vzdálenou službu kromě API OpenAI.

[**Àkàndé ⧉**][00] je hlasový asistent v jazyce Python s otevřeným zdrojovým kódem postavený kolem tří skladatelných komponent: OpenAI Whisper pro rozpoznávání řeči, GPT-4 Chat Completions API pro porozumění jazyku a jeho generování a lokální databáze SQLite pro cachování odpovědí a uchování relace. Výsledkem je hlasově řízený pracovní postup, který lze spustit na notebooku bez lokálních vah modelu, offline úložné infrastruktury nebo kontejnerového stacku.

Tento článek popisuje technickou architekturu každé komponenty, návrhová rozhodnutí kolem cachování a vícekolového kontextu a pipeline exportu do PDF.

## Přehled pipeline

Jedna interakce s Àkàndé probíhá v této posloupnosti:

1. **Zachycení zvuku.** Uživatel mluví; aplikace nahrává zvuk do dočasného souboru WAV pomocí `sounddevice` nebo kompatibilní zvukové knihovny.
2. **Převod řeči na text.** Soubor WAV se odešle do `openai.audio.transcriptions.create()` (Whisper API); přepis se vrátí jako prostý řetězec.
3. **Vyhledání v cache.** Přepis se normalizuje (převede na malá písmena, sjednotí mezery) a zahashuje pomocí SHA-256; hash se vyhledá v lokální tabulce SQLite `response_cache`.
4. **Volání API nebo zásah do cache.** Při minutí se přepis přidá do seznamu `messages` relace a odešle do `openai.chat.completions.create()`; text odpovědi se uloží do cache.
5. **Převod textu na řeč.** Text odpovědi se převede na zvuk pomocí endpointu `openai.audio.speech.create()` (TTS) nebo lokální knihovny TTS a přehraje se.
6. **Export do PDF** (na vyžádání). Celý seznam `messages` se serializuje do formátovaného dokumentu fpdf2 a zapíše na disk.

## Integrace s OpenAI: Chat Completions a Whisper

Àkàndé používá SDK `openai` pro jazyk Python jak pro rozpoznávání řeči, tak pro generování textu. Volání přepisu ve Whisperu:

```python
with open(audio_file_path, "rb") as f:
    transcript = openai.audio.transcriptions.create(
        model="whisper-1",
        file=f,
        language=None  # auto-detect
    )
user_text = transcript.text
```

Volání Chat Completions udržuje seznam `messages` v rozsahu relace:

```python
messages.append({"role": "user", "content": user_text})

response = openai.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=messages,
    temperature=0.2,
    max_tokens=1024
)

assistant_text = response.choices[0].message.content
messages.append({"role": "assistant", "content": assistant_text})
```

Systémový prompt se jednou vloží na začátku relace a řídí personu Àkàndé, formát výstupu a případná doménově specifická omezení:

```python
messages = [
    {
        "role": "system",
        "content": (
            "You are Àkàndé, a concise executive assistant. "
            "Respond in plain prose. Do not use markdown. "
            "If asked to summarise, produce three bullet points maximum."
        )
    }
]
```

Nastavení `temperature=0.2` vyměňuje kreativní variabilitu za determinismus, což je důležité u faktických dotazů, jako je připomenutí rozhodnutí z dřívější části relace.

## Cache odpovědí v SQLite

Schéma cache je minimální:

```sql
CREATE TABLE IF NOT EXISTS response_cache (
    query_hash  TEXT PRIMARY KEY,
    response    TEXT NOT NULL,
    created_at  INTEGER NOT NULL  -- Unix timestamp
);
```

Cesta pro vyhledání a zápis:

```python
import hashlib, sqlite3, time

def _normalise(text: str) -> str:
    return " ".join(text.lower().split())

def cache_get(conn: sqlite3.Connection, query: str) -> str | None:
    h = hashlib.sha256(_normalise(query).encode()).hexdigest()
    row = conn.execute(
        "SELECT response FROM response_cache WHERE query_hash = ?", (h,)
    ).fetchone()
    return row[0] if row else None

def cache_set(conn: sqlite3.Connection, query: str, response: str) -> None:
    h = hashlib.sha256(_normalise(query).encode()).hexdigest()
    conn.execute(
        "INSERT OR REPLACE INTO response_cache VALUES (?, ?, ?)",
        (h, response, int(time.time()))
    )
    conn.commit()
```

`INSERT OR REPLACE` zajišťuje, že se cachovaná odpověď aktualizuje, pokud se stejný dotaz odešle po upgradu modelu. Vyřazovací dotaz založený na TTL (`DELETE WHERE created_at < ?`) lze naplánovat při spuštění a omezit tak velikost cache.

Výkon při zásahu do cache: vyhledání v SQLite na lokálním SSD se vrátí do 1 ms u tabulek až do přibližně 100 000 řádků. Latence úplného cyklu u živého volání GPT-4 API je u krátkých odpovědí typicky 600–900 ms. U denního briefingu s několika opakovanými dotazy cache po první relaci eliminuje většinu volání API.

## Generování shrnutí v PDF

Export do PDF používá [fpdf2](https://py-pdf.github.io/fpdf2/), udržovanou knihovnu PDF pro jazyk Python bez binárních závislostí:

```python
from fpdf import FPDF
from datetime import datetime

def export_session_pdf(messages: list[dict], output_path: str) -> None:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)
    pdf.set_margins(20, 20, 20)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, f"Àkàndé Session — {datetime.now():%Y-%m-%d %H:%M}", ln=True)
    pdf.ln(4)

    for msg in messages:
        if msg["role"] == "system":
            continue
        label = "You" if msg["role"] == "user" else "Àkàndé"
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 6, label, ln=True)
        pdf.set_font("Helvetica", size=10)
        pdf.multi_cell(0, 5, msg["content"])
        pdf.ln(3)

    pdf.output(output_path)
```

`multi_cell()` zajišťuje zalamování řádků a automatické konce stránek, takže relace libovolné délky vytvoří dobře formátovaný dokument bez ruční logiky stránkování. Výstupem je soubor kompatibilní s PDF/A bez vložených písem nad rámec standardních metrik písma Helvetica.

## Model soukromí

Hranici soukromí v Àkàndé vymezují tři skutečnosti:

1. Zvuk se odesílá do Whisper API přes HTTPS a OpenAI jej neuchovává nad rámec volání API (podle zásad OpenAI pro využití dat API k únoru 2024).
2. Volání Chat Completions API přenášejí seznam `messages` relace, který u vícekolových relací může obsahovat celou historii konverzace.
3. Databáze SQLite a soubory PDF leží výhradně v lokálním souborovém systému; nedochází k žádné synchronizaci na pozadí s jakoukoli cloudovou službou.

U výkonných scénářů zahrnujících citlivá témata, jako jsou jednání o fúzích a akvizicích, personální záležitosti či regulatorní strategie, by měla být historie relace přenášená do API před nasazením prověřena vůči zásadám organizace pro využití AI. Limit `max_tokens` u systémového promptu lze využít k zamezení nechtěného přenosu kontextu, který přesahuje zamýšlený rozsah zpřístupnění.

## Často kladené otázky

**Uchovává Àkàndé historii konverzace po skončení relace?**
Seznam `messages` v paměti se při ukončení procesu zahodí. Historie konverzace se uchová pouze tehdy, když uživatel spustí export do PDF nebo když se přidá vlastní vrstva perzistence. Cache v SQLite ukládá hashe dotazů a text odpovědí, nikoli celý kontext konverzace.

**Jak cache zachází s dotazy, které jsou podobné, ale nikoli totožné?**
Cache používá hashování s přesnou shodou na normalizovaném řetězci dotazu. Dva dotazy, které se liší jediným slovem, vytvoří odlišné hashe a povedou k samostatným voláním API. Sémantické cachování (využívající podobnost embeddingů k porovnání téměř duplicitních dotazů) by vyžadovalo další krok vektorového vyhledání a není součástí základní implementace.

**Který model GPT používá Àkàndé ve výchozím nastavení?**
Výchozím je `gpt-4-turbo-preview` k únoru 2024. Název modelu je konfigurační parametr, takže lze nahradit libovolným modelem chat completion od OpenAI. Přechod na `gpt-3.5-turbo` snižuje náklady API přibližně 20× na token, ale zhoršuje kvalitu uvažování u složitých vícekrokových dotazů.

**Lze formát exportu do PDF přizpůsobit?**
Ano. Exportní funkce fpdf2 přijímá jako jediný povinný vstup seznam `messages`, takže úpravou exportní funkce lze změnit písmo, okraje, velikost stránky, obsah záhlaví i označování. fpdf2 rovněž podporuje přidávání obrázků, tabulek a písem Unicode, což umožňuje bohatší rozvržení dokumentů pro organizace se specifickými požadavky na branding.

## Zdroje

1. OpenAI. *Audio Transcriptions — Whisper API*. OpenAI Platform Documentation, 2024. https://platform.openai.com/docs/api-reference/audio/createTranscription
2. OpenAI. *Chat Completions API*. OpenAI Platform Documentation, 2024. https://platform.openai.com/docs/api-reference/chat/create
3. Voss, J. et al. *fpdf2: Modern PDF generation for Python*. GitHub, 2024. https://github.com/py-pdf/fpdf2
4. SQLite Consortium. *SQLite Documentation*. sqlite.org, 2024. https://www.sqlite.org/docs.html

[00]: https://akande.co "Àkàndé Voice Assistant"
