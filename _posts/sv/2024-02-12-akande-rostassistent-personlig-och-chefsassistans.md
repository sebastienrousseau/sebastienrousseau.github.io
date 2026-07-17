---
title: "Àkàndé: GPT-driven röstassistent för chefer"
subtitle: "Arkitekturen i en Python-röstassistent med öppen källkod: Whisper, GPT-4, SQLite-cache och fpdf2"
description: "Àkàndé är en Python-röstassistent med öppen källkod som kedjar samman OpenAI Whisper-taligenkänning, GPT-4-chattkompletteringar och en lokal SQLite-svarscache till ett röststyrt arbetsflöde, genererar PDF-sammanfattningar från konversationshistoriken och håller all lagrad data lokal."
date: "February 12, 2024"
language: "sv-SE"
locale: "sv_SE"
banner: "https://cloudcdn.pro/stocks/images/akande-voice-assistant.webp"
banner_alt: "En vit, sfärisk modern enhet"
keywords: "Àkàndé, OpenAI GPT-4, Whisper STT, SQLite-cachning, fpdf2, Python-röstassistent, chat completions API, PDF-sammanfattningar, SHA-256-cache, text till tal, AI-assistent för chefer, öppen källkod"
---

> **Sammanfattning / Viktiga slutsatser**
>
> - **[Àkàndé ⧉][00]** är en Python-röstassistent med öppen källkod som kedjar samman OpenAI Whisper tal-till-text, GPT-4-chattkompletteringar, en lokal SQLite-svarscache och PDF-export via fpdf2 till ett enda röststyrt arbetsflöde som varken kräver molnlagring eller lokala AI-modellvikter.
> - **SQLite-cachen** lagrar SHA-256-hashar av normaliserade frågesträngar mappade till rå API-svarstext; cacheträffar kostar noll token och returneras på under 10 ms, vilket gör upprepade frågor (som att gå tillbaka till ett beslut från tidigare under ett möte) i praktiken gratis.
> - **Flervändig konversation** upprätthålls genom att `messages`-listan byggs i minnet och skickas med vid varje anrop till Chat Completions-API:t; modellen tar emot hela sessionshistoriken så att den kan referera till tidigare utbyten, till priset av stegvis ökande tokenanvändning per tur.
> - **Genereringen av PDF-sammanfattningar** serialiserar sessionens `messages`-lista till ett formaterat fpdf2-dokument: användarturer och assistentturer etiketteras, tidsstämplar infogas och automatisk paginering hanterar sessioner av valfri längd; filen skrivs till det lokala filsystemet och laddas inte upp.
> - **Integritetsgräns:** endast den aktiva frågan (och sessionshistoriken upp till kontextfönstrets gräns) lämnar enheten; inga ljudinspelningar, inga transkriptioner och inga cachade svar skickas till någon annan fjärrtjänst än OpenAI:s API.

[**Àkàndé ⧉**][00] är en Python-röstassistent med öppen källkod byggd kring tre sammansättningsbara komponenter: OpenAI Whisper för taligenkänning, GPT-4 Chat Completions-API:t för språkförståelse och textgenerering, samt en lokal SQLite-databas för svarscachning och sessionspersistens. Resultatet är ett röststyrt arbetsflöde som kan köras på en bärbar dator utan lokala modellvikter, infrastruktur för offlinelagring eller en containerstack.

Denna artikel beskriver den tekniska arkitekturen för varje komponent, designbesluten kring cachning och flervändig kontext samt pipelinen för PDF-export.

## Översikt över pipelinen

En enskild Àkàndé-interaktion följer denna sekvens:

1. **Ljudupptagning**: användaren talar; applikationen spelar in ljud till en temporär WAV-fil med `sounddevice` eller ett kompatibelt ljudbibliotek.
2. **Tal till text**: WAV-filen skickas till `openai.audio.transcriptions.create()` (Whisper-API:t); transkriptionen returneras som en vanlig sträng.
3. **Cacheuppslag**: transkriptionen normaliseras (gemener, sammanslagna blanksteg) och SHA-256-hashas; hashen slås upp i den lokala SQLite-tabellen `response_cache`.
4. **API-anrop eller cacheträff**: vid en miss läggs transkriptionen till sessionens `messages`-lista och skickas till `openai.chat.completions.create()`; svarstexten lagras i cachen.
5. **Text till tal**: svarstexten konverteras till ljud med endpointen `openai.audio.speech.create()` (TTS) eller ett lokalt TTS-bibliotek, och spelas upp.
6. **PDF-export** (på begäran): hela `messages`-listan serialiseras till ett formaterat fpdf2-dokument och skrivs till disk.

## OpenAI-integration: Chat Completions och Whisper

Àkàndé använder Python-SDK:t `openai` för både taligenkänning och textgenerering. Whisper-transkriptionsanropet:

```python
with open(audio_file_path, "rb") as f:
    transcript = openai.audio.transcriptions.create(
        model="whisper-1",
        file=f,
        language=None  # auto-detect
    )
user_text = transcript.text
```

Chat Completions-anropet upprätthåller en sessionsbunden `messages`-lista:

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

Systemprompten läggs till en gång vid sessionsstart och styr Àkàndés persona, utdataformat och eventuella domänspecifika begränsningar:

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

Att sätta `temperature=0.2` byter kreativ variation mot determinism, vilket är viktigt för faktafrågor som att återkalla ett beslut från tidigare i sessionen.

## SQLite-svarscache

Cacheschemat är minimalt:

```sql
CREATE TABLE IF NOT EXISTS response_cache (
    query_hash  TEXT PRIMARY KEY,
    response    TEXT NOT NULL,
    created_at  INTEGER NOT NULL  -- Unix timestamp
);
```

Uppslags- och skrivvägen:

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

`INSERT OR REPLACE` säkerställer att ett cachat svar uppdateras om samma fråga skickas in på nytt efter en modelluppgradering. En TTL-baserad utrensningsfråga (`DELETE WHERE created_at < ?`) kan schemaläggas vid uppstart för att begränsa cachens storlek.

Prestanda vid cacheträff: ett SQLite-uppslag på en lokal SSD returnerar på under 1 ms för tabeller upp till ~100 000 rader. Tur-och-retur-latensen för ett live-anrop till GPT-4-API:t är typiskt 600–900 ms för korta svar. För en daglig genomgång med en handfull upprepade frågor eliminerar cachen de flesta API-anrop efter den första sessionen.

## Generering av PDF-sammanfattningar

PDF-exporten använder [fpdf2](https://py-pdf.github.io/fpdf2/), ett underhållet Python-bibliotek för PDF-generering utan binära beroenden:

```python
from fpdf import FPDF
from datetime import datetime

def export_session_pdf(messages: list[dict], output_path: str) -> None:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)
    pdf.set_margins(20, 20, 20)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, f"Àkàndé Session - {datetime.now():%Y-%m-%d %H:%M}", ln=True)
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

`multi_cell()` hanterar radbrytning och automatiska sidbrytningar, så sessioner av valfri längd ger ett välformaterat dokument utan manuell pagineringslogik. Utdata är en PDF/A-kompatibel fil utan andra inbäddade typsnitt än standardmåtten för Helvetica.

## Integritetsmodell

Integritetsgränsen i Àkàndé definieras av tre fakta:

1. Ljud skickas till Whisper-API:t över HTTPS och behålls inte av OpenAI efter API-anropet (enligt OpenAI:s policy för API-dataanvändning per februari 2024).
2. Anrop till Chat Completions-API:t överför sessionens `messages`-lista, som kan innehålla hela konversationshistoriken i flervändiga sessioner.
3. SQLite-databasen och PDF-filerna finns helt och hållet i det lokala filsystemet; ingen bakgrundssynkronisering till någon molntjänst förekommer.

För chefsanvändning som rör känsliga ämnen (M&A-diskussioner, personalärenden, regulatorisk strategi) bör den sessionshistorik som överförs till API:t granskas mot organisationens policy för AI-användning före driftsättning. Gränsen `max_tokens` för systemprompten kan användas för att förhindra oavsiktlig överföring av kontext som går utöver den avsedda utlämningsramen.

## Vanliga frågor

**Behåller Àkàndé konversationshistoriken efter att sessionen avslutats?**
Den minnesbaserade `messages`-listan kastas när processen avslutas. Konversationshistorik behålls endast om användaren utlöser en PDF-export eller om ett anpassat persistenslager läggs till. SQLite-cachen lagrar frågehashar och svarstext, inte den fullständiga konversationskontexten.

**Hur hanterar cachen frågor som är snarlika men inte identiska?**
Cachen använder exakt matchande hashning av den normaliserade frågesträngen. Två frågor som skiljer sig åt med ett enda ord ger olika hashar och resulterar i separata API-anrop. Semantisk cachning (att använda inbäddningslikhet för att matcha nästan identiska frågor) skulle kräva ett ytterligare vektoruppslagssteg och ingår inte i basimplementationen.

**Vilken GPT-modell använder Àkàndé som standard?**
Standardmodellen är `gpt-4-turbo-preview` per februari 2024. Modellnamnet är en konfigurationsparameter, så vilken chattkompletteringsmodell som helst från OpenAI kan användas i stället. Ett byte till `gpt-3.5-turbo` sänker API-kostnaden med ungefär 20× per token men försämrar resonemangskvaliteten för komplexa flerstegsfrågor.

**Kan PDF-exportformatet anpassas?**
Ja. Exportfunktionen i fpdf2 tar `messages`-listan som sin enda obligatoriska indata, så typsnitt, marginaler, sidstorlek, sidhuvudsinnehåll och etikettering kan alla ändras genom att redigera exportfunktionen. fpdf2 stöder även bilder, tabeller och Unicode-typsnitt, vilket möjliggör rikare dokumentlayouter för organisationer med särskilda varumärkeskrav.

## Referenser

1. OpenAI. *Audio Transcriptions – Whisper API*. OpenAI Platform Documentation, 2024. https://platform.openai.com/docs/api-reference/audio/createTranscription
2. OpenAI. *Chat Completions API*. OpenAI Platform Documentation, 2024. https://platform.openai.com/docs/api-reference/chat/create
3. Voss, J. et al. *fpdf2: Modern PDF generation for Python*. GitHub, 2024. https://github.com/py-pdf/fpdf2
4. SQLite Consortium. *SQLite Documentation*. sqlite.org, 2024. https://www.sqlite.org/docs.html

[00]: https://akande.co "Àkàndé Voice Assistant"
