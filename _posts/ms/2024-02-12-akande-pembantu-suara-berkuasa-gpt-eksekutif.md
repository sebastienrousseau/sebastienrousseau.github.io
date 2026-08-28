---
title: "Àkàndé: Pembantu Suara Berkuasa GPT untuk Eksekutif"
tags: "Àkàndé, GPT4, WhisperSTT, SQLiteCache, fpdf2, PythonVoiceAssistant, ChatCompletionsAPI, PDFSummary, open source, ExecutiveAI, ISO 20022, post-quantum cryptography, AI, DORA, platform engineering, sovereign cloud, cloud native banking"
subtitle: "Seni bina pembantu suara Python sumber terbuka: Whisper, GPT-4, cache SQLite, dan fpdf2"
description: "Àkàndé ialah pembantu suara Python sumber terbuka yang merangkai pengecaman pertuturan OpenAI Whisper, penyiapan sembang GPT-4, dan cache respons SQLite tempatan menjadi aliran kerja dipacu suara. Ia menjana ringkasan PDF daripada sejarah perbualan dan menyimpan semua data secara tempatan."
date: "Feb 12, 2024"
language: "ms"
locale: "ms_MY"
banner: "https://cloudcdn.pro/stocks/images/akande-voice-assistant.webp"
banner_alt: "Peranti moden berbentuk sfera berwarna putih"
keywords: "Àkàndé, OpenAI GPT-4, Whisper STT, caching SQLite, fpdf2, pembantu suara Python, API chat completions, penjanaan ringkasan PDF, cache SHA-256, teks-ke-pertuturan, AI pembantu eksekutif, sumber terbuka"
---

> **Ringkasan Eksekutif / Intipati Utama**
>
> - **[Àkàndé ⧉][00]** ialah pembantu suara Python sumber terbuka yang merangkai pertuturan-ke-teks OpenAI Whisper, penyiapan sembang GPT-4, cache respons SQLite tempatan, dan eksport PDF fpdf2 menjadi satu aliran kerja dipacu suara yang tidak memerlukan storan awan mahupun pemberat model AI tempatan.
> - **Cache SQLite** menyimpan cincangan SHA-256 bagi rentetan pertanyaan yang dinormalkan yang dipetakan kepada teks respons API mentah; hit cache tidak mengenakan sebarang token dan kembali dalam masa kurang 10 ms, menjadikan pertanyaan berulang (seperti menyemak semula sesuatu keputusan dari awal mesyuarat) pada dasarnya percuma.
> - **Perbualan berbilang pusingan** dikekalkan dengan membina senarai `messages` dalam ingatan dan menghantarnya pada setiap panggilan API Chat Completions: model menerima sejarah sesi penuh supaya ia boleh merujuk pertukaran terdahulu, dengan kos peningkatan penggunaan token secara berperingkat setiap pusingan.
> - **Penjanaan ringkasan PDF** menyirikan senarai `messages` sesi kepada dokumen fpdf2 yang berformat: pusingan pengguna dan pusingan pembantu dilabelkan, cap masa dimasukkan, dan penomboran halaman automatik mengendalikan sesi sepanjang mana-mana; fail ditulis ke sistem fail tempatan, bukan dimuat naik.
> - **Sempadan privasi:** hanya pertanyaan langsung (dan sejarah sesi sehingga had tetingkap konteks) meninggalkan peranti. Tiada rakaman audio, tiada transkrip, dan tiada respons cache dihantar ke mana-mana perkhidmatan jauh selain daripada API OpenAI.

[**Àkàndé ⧉**][00] ialah pembantu suara Python sumber terbuka yang dibina di sekitar tiga komponen yang boleh digabungkan: OpenAI Whisper untuk pengecaman pertuturan, API GPT-4 Chat Completions untuk pemahaman dan penjanaan bahasa, dan pangkalan data SQLite tempatan untuk caching respons dan kegigihan sesi. Hasilnya ialah aliran kerja dipacu suara yang boleh dijalankan pada komputer riba tanpa pemberat model tempatan, infrastruktur storan luar talian, mahupun timbunan kontena.

Artikel ini menerangkan seni bina teknikal setiap komponen, keputusan reka bentuk berkenaan caching dan konteks berbilang pusingan, serta saluran paip eksport PDF.

## Gambaran Keseluruhan Saluran Paip

Satu interaksi Àkàndé mengikut urutan ini:

1. **Tangkapan audio** — pengguna bercakap; aplikasi merakam audio ke fail WAV sementara menggunakan `sounddevice` atau pustaka audio yang serasi.
2. **Pertuturan-ke-teks** — fail WAV dihantar ke `openai.audio.transcriptions.create()` (API Whisper); transkrip dikembalikan sebagai rentetan biasa.
3. **Carian cache** — transkrip dinormalkan (dijadikan huruf kecil, ruang putih diringkaskan) dan dicincang SHA-256; cincangan itu dicari dalam jadual `response_cache` SQLite tempatan.
4. **Panggilan API atau hit cache** — apabila tiada padanan, transkrip dilampirkan pada senarai `messages` sesi dan dihantar ke `openai.chat.completions.create()`; teks respons disimpan dalam cache.
5. **Teks-ke-pertuturan** — teks respons ditukar kepada audio menggunakan titik akhir `openai.audio.speech.create()` (TTS) atau pustaka TTS tempatan, dan dimainkan semula.
6. **Eksport PDF** (atas permintaan) — keseluruhan senarai `messages` disirikan kepada dokumen fpdf2 berformat dan ditulis ke cakera.

## Penyepaduan OpenAI: Chat Completions dan Whisper

Àkàndé menggunakan SDK Python `openai` untuk kedua-dua pengecaman pertuturan dan penjanaan teks. Panggilan transkripsi Whisper:

```python
with open(audio_file_path, "rb") as f:
    transcript = openai.audio.transcriptions.create(
        model="whisper-1",
        file=f,
        language=None  # auto-detect
    )
user_text = transcript.text
```

Panggilan Chat Completions mengekalkan senarai `messages` berskop sesi:

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

Gesaan sistem diletakkan sekali di awal sesi dan mengawal persona Àkàndé, format keluaran, serta sebarang kekangan khusus domain:

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

Menetapkan `temperature=0.2` menukar variasi kreatif dengan ketentuan, yang penting untuk pertanyaan berfakta seperti mengingati semula sesuatu keputusan dari awal sesi.

## Cache Respons SQLite

Skema cache adalah minimum:

```sql
CREATE TABLE IF NOT EXISTS response_cache (
    query_hash  TEXT PRIMARY KEY,
    response    TEXT NOT NULL,
    created_at  INTEGER NOT NULL  -- Unix timestamp
);
```

Laluan carian dan tulisan:

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

`INSERT OR REPLACE` memastikan respons yang dicache dikemas kini jika pertanyaan yang sama dihantar selepas naik taraf model. Pertanyaan pengusiran berasaskan TTL (`DELETE WHERE created_at < ?`) boleh dijadualkan semasa permulaan untuk mengehadkan saiz cache.

Prestasi hit cache: carian SQLite pada SSD tempatan kembali dalam masa kurang 1 ms untuk jadual sehingga ~100,000 baris. Kependaman ulang-alik bagi panggilan API GPT-4 langsung biasanya 600–900 ms untuk respons pendek. Untuk taklimat harian dengan beberapa pertanyaan berulang, cache menghapuskan kebanyakan panggilan API selepas sesi pertama.

## Penjanaan Ringkasan PDF

Eksport PDF menggunakan [fpdf2](https://py-pdf.github.io/fpdf2/), sebuah pustaka PDF Python yang diselenggara tanpa kebergantungan binari:

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

`multi_cell()` mengendalikan pembalut baris dan pemisah halaman automatik, jadi sesi sepanjang mana-mana menghasilkan dokumen yang berformat baik tanpa logik penomboran halaman manual. Keluarannya ialah fail yang serasi PDF/A tanpa fon terbenam melebihi metrik Helvetica standard.

## Model Privasi

Sempadan privasi dalam Àkàndé ditakrifkan oleh tiga fakta:

1. Audio dihantar ke API Whisper melalui HTTPS dan tidak disimpan oleh OpenAI melebihi panggilan API tersebut (menurut dasar penggunaan data API OpenAI setakat Februari 2024).
2. Panggilan API Chat Completions menghantar senarai `messages` sesi, yang mungkin mengandungi keseluruhan sejarah perbualan untuk sesi berbilang pusingan.
3. Pangkalan data SQLite dan fail PDF berada sepenuhnya pada sistem fail tempatan; tiada penyegerakan latar belakang ke mana-mana perkhidmatan awan berlaku.

Untuk kes penggunaan eksekutif yang melibatkan topik sensitif, seperti perbincangan M&A, hal ehwal kakitangan, dan strategi kawal selia, sejarah sesi yang dihantar ke API perlu disemak terhadap dasar penggunaan AI organisasi sebelum penggunaan. Had `max_tokens` pada gesaan sistem boleh digunakan untuk mengelakkan penghantaran konteks yang tidak sengaja yang melebihi skop pendedahan yang dimaksudkan.

## Soalan Lazim

**Adakah Àkàndé menyimpan sejarah perbualan selepas sesi berakhir?**
Senarai `messages` dalam ingatan dibuang apabila proses tamat. Sejarah perbualan hanya disimpan jika pengguna mencetuskan eksport PDF atau jika lapisan kegigihan tersuai ditambah. Cache SQLite menyimpan cincangan pertanyaan dan teks respons, bukan keseluruhan konteks perbualan.

**Bagaimanakah cache mengendalikan pertanyaan yang serupa tetapi tidak sama?**
Cache menggunakan pencincangan padanan tepat pada rentetan pertanyaan yang dinormalkan. Dua pertanyaan yang berbeza sebanyak satu perkataan akan menghasilkan cincangan yang berbeza dan mengakibatkan panggilan API yang berasingan. Caching semantik (menggunakan keserupaan embedding untuk memadankan pertanyaan hampir-pendua) memerlukan langkah carian vektor tambahan dan bukan sebahagian daripada pelaksanaan asas.

**Model GPT manakah yang digunakan Àkàndé secara lalai?**
Lalai ialah `gpt-4-turbo-preview` setakat Februari 2024. Nama model ialah parameter konfigurasi, jadi mana-mana model chat completion OpenAI boleh digantikan. Bertukar kepada `gpt-3.5-turbo` mengurangkan kos API sebanyak kira-kira 20× setiap token tetapi mengurangkan kualiti penaakulan untuk pertanyaan berbilang langkah yang kompleks.

**Bolehkah format eksport PDF disesuaikan?**
Ya. Fungsi eksport fpdf2 menerima senarai `messages` sebagai satu-satunya input yang diperlukan, jadi fon, margin, saiz halaman, kandungan pengepala, dan pelabelan semuanya boleh diubah dengan menyunting fungsi eksport. fpdf2 juga menyokong penambahan imej, jadual, dan fon Unicode, membolehkan susun atur dokumen yang lebih kaya untuk organisasi yang mempunyai keperluan penjenamaan tertentu.

## Rujukan

1. OpenAI. *Audio Transcriptions — Whisper API*. OpenAI Platform Documentation, 2024. https://platform.openai.com/docs/api-reference/audio/createTranscription
2. OpenAI. *Chat Completions API*. OpenAI Platform Documentation, 2024. https://platform.openai.com/docs/api-reference/chat/create
3. Voss, J. et al. *fpdf2: Modern PDF generation for Python*. GitHub, 2024. https://github.com/py-pdf/fpdf2
4. SQLite Consortium. *SQLite Documentation*. sqlite.org, 2024. https://www.sqlite.org/docs.html

[00]: https://akande.co "Pembantu Suara Àkàndé"
