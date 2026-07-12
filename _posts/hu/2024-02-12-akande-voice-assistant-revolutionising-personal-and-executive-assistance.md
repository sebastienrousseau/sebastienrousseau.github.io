---
title: "Àkàndé: GPT-alapú hangasszisztens vezetőknek"
tags: "Àkàndé, GPT4, WhisperSTT, SQLiteCache, fpdf2, PythonVoiceAssistant, ChatCompletionsAPI, PDFSummary, open source, ExecutiveAI, ISO 20022, post-quantum cryptography, AI, DORA, platform engineering, sovereign cloud, cloud native banking"
subtitle: "Egy nyílt forráskódú Python hangasszisztens architektúrája: Whisper, GPT-4, SQLite gyorsítótár és fpdf2"
description: "Az Àkàndé egy nyílt forráskódú Python hangasszisztens, amely az OpenAI Whisper beszédfelismerést, a GPT-4 chat completions szolgáltatást és egy helyi SQLite válasz-gyorsítótárat fűz össze egyetlen hangvezérelt munkafolyamattá: PDF-összefoglalókat készít a beszélgetési előzményekből, és minden tárolt adatot helyben tart."
date: "Feb 12, 2024"
language: "hu"
locale: "hu_HU"
banner: "https://cloudcdn.pro/stocks/images/akande-voice-assistant.webp"
banner_alt: "Fehér, gömb alakú modern eszköz"
keywords: "Àkàndé, OpenAI GPT-4, Whisper STT, SQLite gyorsítótárazás, fpdf2, Python hangasszisztens, chat completions API, PDF-összefoglaló generálása, SHA-256 gyorsítótár, szövegfelolvasás, vezetői asszisztens MI, nyílt forráskód"
---

> **Vezetői összefoglaló / Legfontosabb tanulságok**
>
> - Az **[Àkàndé ⧉][00]** egy nyílt forráskódú Python hangasszisztens, amely az OpenAI Whisper beszéd-szöveg átalakítást, a GPT-4 chat completions szolgáltatást, egy helyi SQLite válasz-gyorsítótárat és az fpdf2 PDF-exportot egyetlen hangvezérelt munkafolyamattá fűzi össze, amelyhez nincs szükség felhőalapú tárolásra és helyi MI-modellsúlyokra.
> - **Az SQLite gyorsítótár** a normalizált lekérdezési karakterláncok SHA-256 hasheit tárolja, nyers API-válaszszöveghez rendelve; a gyorsítótár-találatok nulla tokenbe kerülnek, és 10 ms-nál rövidebb idő alatt térnek vissza, így az ismételt lekérdezések (például egy megbeszélés korábbi döntésének áttekintése) lényegében ingyenesek.
> - **A többfordulós beszélgetést** a `messages` lista memóriában való felépítése és minden Chat Completions API-hívásnál való átadása tartja fenn: a modell megkapja a teljes munkamenet-előzményt, így hivatkozhat a korábbi váltásokra, cserébe fordulónként fokozatosan növekvő tokenhasználatért.
> - **A PDF-összefoglaló generálása** a munkamenet `messages` listáját formázott fpdf2 dokumentummá szerializálja: a felhasználói és az asszisztensi fordulók címkézve vannak, időbélyegek kerülnek beszúrásra, az automatikus lapozás pedig bármilyen hosszúságú munkamenetet kezel; a fájl a helyi fájlrendszerbe íródik, nem töltődik fel.
> - **Adatvédelmi határ:** csak az élő lekérdezés (és a munkamenet-előzmény a kontextusablak határáig) hagyja el az eszközt; semmilyen hangfelvétel, átirat vagy gyorsítótárazott válasz nem kerül elküldésre az OpenAI API-ján kívül más távoli szolgáltatásnak.

Az [**Àkàndé ⧉**][00] egy nyílt forráskódú Python hangasszisztens, amely három egymással kombinálható komponensre épül: az OpenAI Whisperre a beszédfelismeréshez, a GPT-4 Chat Completions API-ra a nyelvi megértéshez és -generáláshoz, valamint egy helyi SQLite adatbázisra a válaszok gyorsítótárazásához és a munkamenet megőrzéséhez. Az eredmény egy hangvezérelt munkafolyamat, amely laptopon futtatható helyi modellsúlyok, offline tárolási infrastruktúra vagy konténer-verem nélkül.

Ez a cikk bemutatja az egyes komponensek műszaki architektúráját, a gyorsítótárazással és a többfordulós kontextussal kapcsolatos tervezési döntéseket, valamint a PDF-export folyamatát.

## A folyamat áttekintése

Egyetlen Àkàndé-interakció a következő sorrendet követi:

1. **Hangrögzítés**: a felhasználó beszél; az alkalmazás a `sounddevice` vagy egy kompatibilis hangkönyvtár segítségével egy ideiglenes WAV-fájlba rögzíti a hangot.
2. **Beszéd-szöveg átalakítás**: a WAV-fájl az `openai.audio.transcriptions.create()` hívásnak (Whisper API) kerül átadásra; az átirat egyszerű karakterláncként tér vissza.
3. **Gyorsítótár-keresés**: az átirat normalizálásra kerül (kisbetűssé alakítva, a szóközök összevonásával) és SHA-256 hasht kap; a hasht a program a helyi SQLite `response_cache` táblájában keresi meg.
4. **API-hívás vagy gyorsítótár-találat**: hiány esetén az átirat hozzáfűződik a munkamenet `messages` listájához, és elküldésre kerül az `openai.chat.completions.create()` hívásnak; a válaszszöveg a gyorsítótárba kerül.
5. **Szövegfelolvasás**: a válaszszöveg az `openai.audio.speech.create()` végpont (TTS) vagy egy helyi TTS-könyvtár segítségével hanggá alakul, és lejátszásra kerül.
6. **PDF-export** (igény szerint): a teljes `messages` lista formázott fpdf2 dokumentummá szerializálódik, és lemezre íródik.

## OpenAI-integráció: Chat Completions és Whisper

Az Àkàndé mind a beszédfelismeréshez, mind a szöveggeneráláshoz az `openai` Python SDK-t használja. A Whisper átírási hívás:

```python
with open(audio_file_path, "rb") as f:
    transcript = openai.audio.transcriptions.create(
        model="whisper-1",
        file=f,
        language=None  # automatikus felismerés
    )
user_text = transcript.text
```

A Chat Completions hívás egy munkamenet-hatókörű `messages` listát tart fenn:

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

A rendszerpromptot a munkamenet indításakor egyszer fűzi az elejére, és ez vezérli az Àkàndé perszónáját, a kimeneti formátumot és minden tartományspecifikus megkötést:

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

A `temperature=0.2` beállítás a kreatív változatosságot a determinizmusra cseréli, ami fontos az olyan tényszerű lekérdezéseknél, mint egy korábbi munkamenet-döntés felidézése.

## SQLite válasz-gyorsítótár

A gyorsítótár sémája minimális:

```sql
CREATE TABLE IF NOT EXISTS response_cache (
    query_hash  TEXT PRIMARY KEY,
    response    TEXT NOT NULL,
    created_at  INTEGER NOT NULL  -- Unix időbélyeg
);
```

A keresési és írási útvonal:

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

Az `INSERT OR REPLACE` biztosítja, hogy egy gyorsítótárazott válasz frissüljön, ha ugyanaz a lekérdezés egy modellfrissítés után újra beérkezik. Egy TTL-alapú eltávolítási lekérdezés (`DELETE WHERE created_at < ?`) indításkor ütemezhető a gyorsítótár méretének korlátozására.

Gyorsítótár-találati teljesítmény: egy helyi SSD-n futó SQLite-keresés 1 ms-nál rövidebb idő alatt tér vissza akár ~100 000 sort tartalmazó tábláknál is. Egy élő GPT-4 API-hívás oda-vissza késleltetése rövid válaszok esetén jellemzően 600–900 ms. Egy napi eligazításnál, amely néhány ismételt lekérdezést tartalmaz, a gyorsítótár az első munkamenet után az API-hívások többségét kiküszöböli.

## PDF-összefoglaló generálása

A PDF-export az [fpdf2](https://py-pdf.github.io/fpdf2/) könyvtárat használja, egy karbantartott, bináris függőségek nélküli Python PDF-könyvtárat:

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

A `multi_cell()` kezeli a sortörést és az automatikus oldaltöréseket, így bármilyen hosszúságú munkamenet jól formázott dokumentumot eredményez manuális lapozási logika nélkül. A kimenet egy PDF/A-kompatibilis fájl, amely a szabványos Helvetica-metrikákon túl nem tartalmaz beágyazott betűtípusokat.

## Adatvédelmi modell

Az Àkàndé adatvédelmi határát három tény határozza meg:

1. A hang HTTPS-en keresztül kerül a Whisper API-hoz, és az OpenAI az API-híváson túl nem őrzi meg (az OpenAI 2024. februári API-adathasználati szabályzata szerint).
2. A Chat Completions API-hívások továbbítják a munkamenet `messages` listáját, amely többfordulós munkameneteknél a teljes beszélgetési előzményt tartalmazhatja.
3. Az SQLite adatbázis és a PDF-fájlok teljes egészében a helyi fájlrendszerben találhatók; semmilyen háttérszinkronizáció nem történik felhőszolgáltatással.

Az érzékeny témákat érintő vezetői felhasználási esetekben, mint az M&A-tárgyalások, személyzeti ügyek vagy szabályozási stratégia, az API-nak továbbított munkamenet-előzményt a bevezetés előtt felül kell vizsgálni a szervezet MI-használati szabályzatával szemben. A rendszerpromptra vonatkozó `max_tokens` korlát felhasználható arra, hogy megakadályozza a szándékolt nyilvánosságra hozatali körön túlmutató kontextus véletlen továbbítását.

## Gyakran ismételt kérdések

**Megőrzi az Àkàndé a beszélgetési előzményeket a munkamenet befejezése után?**
A memóriában tárolt `messages` lista a folyamat kilépésekor törlődik. A beszélgetési előzmény csak akkor marad meg, ha a felhasználó PDF-exportot indít, vagy ha egyéni megőrzési réteget adnak hozzá. Az SQLite gyorsítótár a lekérdezési hasheket és a válaszszöveget tárolja, nem a teljes beszélgetési kontextust.

**Hogyan kezeli a gyorsítótár a hasonló, de nem azonos lekérdezéseket?**
A gyorsítótár pontos egyezésű hashelést használ a normalizált lekérdezési karakterláncon. Két lekérdezés, amely egyetlen szóban tér el, eltérő hasheket eredményez, és külön API-hívásokat von maga után. A szemantikus gyorsítótárazás (beágyazási hasonlóság használata a közel duplikált lekérdezések egyeztetésére) egy további vektorkeresési lépést igényelne, és nem része az alap implementációnak.

**Milyen GPT-modellt használ az Àkàndé alapértelmezés szerint?**
Az alapértelmezett a `gpt-4-turbo-preview` 2024 februárjában. A modell neve konfigurációs paraméter, így bármely OpenAI chat completion modell behelyettesíthető. A `gpt-3.5-turbo`-ra váltás tokenenként körülbelül 20-szorosára csökkenti az API-költséget, de rontja az érvelési minőséget összetett, többlépéses lekérdezéseknél.

**Testreszabható a PDF-export formátuma?**
Igen. Az fpdf2 exportfüggvény egyetlen kötelező bemenetként a `messages` listát fogadja, így a betűtípus, a margók, az oldalméret, a fejléc tartalma és a címkézés mind módosítható az exportfüggvény szerkesztésével. Az fpdf2 támogatja képek, táblázatok és Unicode-betűtípusok hozzáadását is, ami gazdagabb dokumentumelrendezéseket tesz lehetővé az egyedi arculati követelményekkel rendelkező szervezetek számára.

## Hivatkozások

1. OpenAI. *Audio Transcriptions — Whisper API*. OpenAI Platform Documentation, 2024. https://platform.openai.com/docs/api-reference/audio/createTranscription
2. OpenAI. *Chat Completions API*. OpenAI Platform Documentation, 2024. https://platform.openai.com/docs/api-reference/chat/create
3. Voss, J. et al. *fpdf2: Modern PDF generation for Python*. GitHub, 2024. https://github.com/py-pdf/fpdf2
4. SQLite Consortium. *SQLite Documentation*. sqlite.org, 2024. https://www.sqlite.org/docs.html

[00]: https://akande.co "Àkàndé Voice Assistant"
