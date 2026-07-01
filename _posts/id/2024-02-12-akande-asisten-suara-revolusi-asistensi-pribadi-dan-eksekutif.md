---
title: "Àkàndé: Asisten Suara Bertenaga GPT untuk Eksekutif"
subtitle: "Arsitektur asisten suara Python open source: Whisper, GPT-4, cache SQLite, dan fpdf2"
description: "Àkàndé adalah asisten suara Python open source yang merangkai pengenalan ucapan OpenAI Whisper, chat completions GPT-4, dan cache respons SQLite lokal ke dalam workflow berbasis suara, menghasilkan ringkasan PDF dari riwayat percakapan dan menjaga semua data tersimpan secara lokal."
date: "Feb 12, 2024"
language: "id-ID"
locale: "id_ID"
banner: "https://cloudcdn.pro/stocks/images/akande-voice-assistant.webp"
banner_alt: "Perangkat modern berbentuk bulat berwarna putih"
keywords: "Àkàndé, OpenAI GPT-4, Whisper STT, SQLite caching, fpdf2, asisten suara Python, chat completions API, pembuatan ringkasan PDF, cache SHA-256, text-to-speech, AI asisten eksekutif, open source"
---

![Perangkat modern berbentuk bulat berwarna putih](https://cloudcdn.pro/stocks/images/akande-voice-assistant.webp).class=\"img-fluid clearfix\"

> **TL;DR.** Àkàndé adalah asisten suara Python open source yang merangkai pengenalan ucapan OpenAI Whisper, chat completions GPT-4, dan cache respons SQLite lokal ke dalam workflow berbasis suara, menghasilkan ringkasan PDF dari riwayat percakapan dan menjaga semua data tersimpan secara lokal.
>
> **Kesimpulan utama**
>
> - **Ikhtisar Pipeline.** Satu interaksi Àkàndé mengikuti urutan audio capture, speech-to-text, cache lookup, API call atau cache hit, text-to-speech, dan ekspor PDF.
> - **Integrasi OpenAI: Chat Completions dan Whisper.** Àkàndé menggunakan Python SDK `openai` untuk pengenalan ucapan dan pembuatan teks.
> - **Cache Respons SQLite.** Cache menyimpan hash SHA-256 dari query yang dinormalisasi dan memetakannya ke teks respons API mentah.
> - **Pembuatan Ringkasan PDF.** Ekspor PDF memakai fpdf2, library PDF Python terawat tanpa dependensi biner.

> **Ringkasan Eksekutif / Kesimpulan Utama**
>
> - **[Àkàndé ⧉][00]** adalah asisten suara Python open source yang merangkai OpenAI Whisper speech-to-text, GPT-4 chat completions, cache respons SQLite lokal, dan ekspor PDF fpdf2 ke dalam satu workflow berbasis suara tanpa memerlukan cloud storage atau bobot model AI lokal.
> - **Cache SQLite** menyimpan hash SHA-256 dari string query yang dinormalisasi dan memetakannya ke teks respons API mentah; cache hit tidak memakai token dan kembali dalam kurang dari 10 ms, sehingga query berulang, misalnya meninjau keputusan dari awal rapat, praktis gratis.
> - **Percakapan multi-turn** dipertahankan dengan membangun daftar `messages` di memori dan mengirimkannya pada setiap panggilan Chat Completions API. Model menerima riwayat sesi penuh sehingga dapat merujuk pertukaran sebelumnya, dengan konsekuensi penggunaan token meningkat bertahap per giliran.
> - **Pembuatan ringkasan PDF** menserialisasi daftar `messages` sesi menjadi dokumen fpdf2 terformat: giliran pengguna dan assistant diberi label, timestamp dimasukkan, dan pagination otomatis menangani sesi sepanjang apa pun; file ditulis ke filesystem lokal, bukan diunggah.
> - **Batas privasi:** hanya query langsung dan riwayat sesi sampai batas context window yang keluar dari perangkat. Rekaman audio, transkrip, dan respons cache tidak dikirim ke layanan jarak jauh selain OpenAI API.

[**Àkàndé ⧉**][00] adalah asisten suara Python open source yang dibangun dari tiga komponen yang dapat dikomposisi: OpenAI Whisper untuk pengenalan ucapan, GPT-4 Chat Completions API untuk pemahaman dan pembuatan bahasa, serta basis data SQLite lokal untuk cache respons dan persistensi sesi. Hasilnya adalah workflow berbasis suara yang dapat dijalankan di laptop tanpa bobot model lokal, infrastruktur penyimpanan offline, atau stack container.

Artikel ini menjelaskan arsitektur teknis tiap komponen, keputusan desain seputar caching dan konteks multi-turn, serta pipeline ekspor PDF.

## Ikhtisar Pipeline

Satu interaksi Àkàndé mengikuti urutan ini:

1. **Audio capture** — pengguna berbicara; aplikasi merekam audio ke file WAV sementara menggunakan `sounddevice` atau library audio yang kompatibel.
2. **Speech-to-text** — file WAV dikirim ke `openai.audio.transcriptions.create()` (Whisper API); transkrip dikembalikan sebagai string biasa.
3. **Cache lookup** — transkrip dinormalisasi (huruf kecil, whitespace dirapikan) dan di-hash dengan SHA-256; hash dicari di tabel SQLite lokal `response_cache`.
4. **API call atau cache hit** — jika miss, transkrip ditambahkan ke daftar `messages` sesi dan dikirim ke `openai.chat.completions.create()`; teks respons disimpan dalam cache.
5. **Text-to-speech** — teks respons dikonversi ke audio memakai endpoint `openai.audio.speech.create()` (TTS) atau library TTS lokal, lalu diputar.
6. **Ekspor PDF** (sesuai permintaan) — daftar `messages` lengkap diserialisasi ke dokumen fpdf2 terformat dan ditulis ke disk.

## Integrasi OpenAI: Chat Completions dan Whisper

Àkàndé menggunakan Python SDK `openai` untuk pengenalan ucapan dan pembuatan teks. Panggilan transkripsi Whisper:

```python
with open(audio_file_path, "rb") as f:
    transcript = openai.audio.transcriptions.create(
        model="whisper-1",
        file=f,
        language=None  # auto-detect
    )
user_text = transcript.text
```

Panggilan Chat Completions mempertahankan daftar `messages` yang scoped ke sesi:

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

System prompt ditambahkan sekali di awal sesi dan mengendalikan persona Àkàndé, format output, serta batasan khusus domain:

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

Mengatur `temperature=0.2` menukar variasi kreatif dengan determinisme, yang penting untuk query faktual seperti mengingat keputusan dari awal sesi.

## Cache Respons SQLite

Skema cache minimal:

```sql
CREATE TABLE IF NOT EXISTS response_cache (
    query_hash  TEXT PRIMARY KEY,
    response    TEXT NOT NULL,
    created_at  INTEGER NOT NULL  -- Unix timestamp
);
```

Jalur lookup dan write:

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

`INSERT OR REPLACE` memastikan respons cache diperbarui jika query yang sama dikirim setelah upgrade model. Query eviction berbasis TTL (`DELETE WHERE created_at < ?`) dapat dijadwalkan saat startup untuk membatasi ukuran cache.

Performa cache hit: lookup SQLite pada SSD lokal kembali dalam kurang dari 1 ms untuk tabel hingga sekitar 100.000 baris. Latensi round-trip untuk panggilan GPT-4 API langsung biasanya 600-900 ms untuk respons pendek. Untuk briefing harian dengan beberapa query berulang, cache menghilangkan sebagian besar panggilan API setelah sesi pertama.

## Pembuatan Ringkasan PDF

Ekspor PDF menggunakan [fpdf2](https://py-pdf.github.io/fpdf2/), library PDF Python terawat tanpa dependensi biner:

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

`multi_cell()` menangani line wrapping dan page break otomatis, sehingga sesi sepanjang apa pun menghasilkan dokumen terformat baik tanpa logika pagination manual. Outputnya adalah file yang kompatibel dengan PDF/A tanpa font tertanam selain metrik Helvetica standar.

## Model Privasi

Batas privasi Àkàndé didefinisikan oleh tiga fakta:

1. Audio dikirim ke Whisper API melalui HTTPS dan tidak disimpan oleh OpenAI di luar panggilan API, sesuai kebijakan penggunaan data API OpenAI per Februari 2024.
2. Panggilan Chat Completions API mengirim daftar `messages` sesi, yang dapat berisi seluruh riwayat percakapan untuk sesi multi-turn.
3. Basis data SQLite dan file PDF sepenuhnya berada di filesystem lokal; tidak ada sinkronisasi latar belakang ke layanan cloud apa pun.

Untuk kasus penggunaan eksekutif yang melibatkan topik sensitif, seperti diskusi M&A, urusan personel, atau strategi regulasi, riwayat sesi yang dikirim ke API harus ditinjau terhadap kebijakan penggunaan AI organisasi sebelum deployment. Batas `max_tokens` pada system prompt dapat digunakan untuk mencegah pengiriman konteks yang tidak sengaja melebihi cakupan pengungkapan yang dimaksud.

## Pertanyaan yang Sering Diajukan

**Apakah Àkàndé menyimpan riwayat percakapan setelah sesi berakhir?**
Daftar `messages` di memori dibuang ketika proses keluar. Riwayat percakapan hanya disimpan jika pengguna memicu ekspor PDF atau jika lapisan persistensi khusus ditambahkan. Cache SQLite menyimpan hash query dan teks respons, bukan konteks percakapan lengkap.

**Bagaimana cache menangani query yang mirip tetapi tidak identik?**
Cache memakai exact-match hashing pada string query yang dinormalisasi. Dua query yang berbeda satu kata akan menghasilkan hash berbeda dan memicu panggilan API terpisah. Semantic caching, yaitu memakai similarity embedding untuk mencocokkan query yang hampir sama, membutuhkan langkah vector lookup tambahan dan bukan bagian dari implementasi dasar.

**Model GPT apa yang digunakan Àkàndé secara default?**
Default-nya adalah `gpt-4-turbo-preview` per Februari 2024. Nama model adalah parameter konfigurasi, sehingga model OpenAI chat completion apa pun dapat diganti. Beralih ke `gpt-3.5-turbo` mengurangi biaya API sekitar 20x per token, tetapi menurunkan kualitas penalaran untuk query multi-langkah yang kompleks.

**Bisakah format ekspor PDF disesuaikan?**
Ya. Fungsi ekspor fpdf2 menerima daftar `messages` sebagai satu-satunya input wajib, sehingga font, margin, ukuran halaman, konten header, dan pelabelan semuanya dapat diubah dengan mengedit fungsi ekspor. fpdf2 juga mendukung gambar, tabel, dan font Unicode, sehingga layout dokumen yang lebih kaya dapat dibuat untuk organisasi dengan kebutuhan branding tertentu.

## Referensi

1. OpenAI. *Audio Transcriptions — Whisper API*. OpenAI Platform Documentation, 2024. https://platform.openai.com/docs/api-reference/audio/createTranscription
2. OpenAI. *Chat Completions API*. OpenAI Platform Documentation, 2024. https://platform.openai.com/docs/api-reference/chat/create
3. Voss, J. et al. *fpdf2: Modern PDF generation for Python*. GitHub, 2024. https://github.com/py-pdf/fpdf2
4. SQLite Consortium. *SQLite Documentation*. sqlite.org, 2024. https://www.sqlite.org/docs.html

[00]: https://akande.co "Asisten Suara Àkàndé"
