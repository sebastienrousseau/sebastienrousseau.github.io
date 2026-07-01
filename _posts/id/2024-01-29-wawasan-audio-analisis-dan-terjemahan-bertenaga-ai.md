---
title: "Audio Analyser: Pipeline Azure Speech, NLP, dan Terjemahan"
subtitle: "Arsitektur dan pipeline alat analitik ucapan berbasis Azure"
description: "Audio Analyser menggunakan model neural speech-to-text Azure Cognitive Services, NLP Text Analytics, dan CherryPy untuk mengubah rekaman audio menjadi transkrip yang dapat dicari, skor sentimen, ekstraksi kata kunci, dan terjemahan multibahasa."
date: "Jan 29, 2024"
language: "id-ID"
locale: "id_ID"
banner: "https://cloudcdn.pro/stocks/images/modern-corporate-office-with-technological-displays.webp"
banner_alt: "Kantor perusahaan modern yang minimalis"
keywords: "Azure Cognitive Services, speech-to-text, neural acoustic model, Azure Text Analytics, natural language processing, analisis sentimen, CherryPy, batch transcription API, multilingual ASR, Azure Translator, transkripsi audio, pemrosesan audio Python"
---

![Kantor perusahaan modern yang minimalis](https://cloudcdn.pro/stocks/images/modern-corporate-office-with-technological-displays.webp).class=\"img-fluid clearfix\"

> **TL;DR.** Audio Analyser menggunakan model neural speech-to-text Azure Cognitive Services, NLP Text Analytics, dan CherryPy untuk mengubah rekaman audio menjadi transkrip yang dapat dicari, skor sentimen, ekstraksi kata kunci, dan terjemahan multibahasa.
>
> **Kesimpulan utama**
>
> - **Cara Kerja Audio Analyser: Ikhtisar Arsitektur.** Pipeline memiliki lima tahap terpisah: upload, transkripsi, NLP, terjemahan opsional, dan output.
> - **Azure Cognitive Services: Mesin Batch Transcription.** API batch transcription Azure Speech menerima referensi file audio di Azure Blob Storage dan body konfigurasi JSON.
> - **Natural Language Processing dengan Azure AI Language.** Setelah transkripsi, Audio Analyser mengirim transkrip display-form ke Azure AI Language melalui Python SDK.
> - **Dukungan Multibahasa melalui Azure Translator.** Azure Translator dipanggil setelah deteksi bahasa ketika pengguna meminta bahasa target.

> **Ringkasan Eksekutif / Kesimpulan Utama**
>
> - **Azure Batch Transcription API** menerima file audio hingga 2,5 jam (WAV/MP3/OGG/FLAC), memprosesnya secara asinkron, dan mengembalikan array JSON `recognizedPhrases` dengan kandidat `nBest` per frasa, skor confidence, output inverse-text-normalised (ITN), dan diarization pembicara opsional, tanpa koneksi streaming.
> - **Model akustik neural Microsoft** menurunkan word error rate sekitar 50% dibanding baseline hidden Markov model (HMM) sebelumnya pada benchmark percakapan Switchboard, mencapai paritas dengan transkriber manusia profesional pada dataset tersebut di kisaran 5,1% WER.
> - **Azure Text Analytics**, kini bagian dari Azure AI Language, memproses teks transkrip melalui ekstraksi key phrase, named entity recognition (NER), analisis sentimen dengan opinion mining, dan deteksi bahasa dalam satu panggilan `analyze_sentiment` atau `begin_analyze_actions` memakai Python SDK.
> - **CherryPy** menyediakan lapisan web: URL routing, penanganan multipart upload, manajemen sesi, dan rendering template Jinja2 dalam proses Python minimal yang dapat berjalan di VM murah tanpa overhead orkestrasi.
> - **Azure Translator NMT** otomatis mendeteksi bahasa sumber dan menerjemahkan transkrip ke 135 bahasa target, memungkinkan analisis NLP downstream pada teks asli dan terjemahan dalam run pipeline yang sama.

[**Audio Analyser ⧉**][00] adalah aplikasi Python open source yang menghubungkan tiga Azure Cognitive Services dalam satu workflow: Batch Transcription untuk speech-to-text, Azure AI Language (Text Analytics) untuk NLP, dan Azure Translator untuk output multibahasa. Antarmuka web disajikan oleh CherryPy, dan hasil dapat disimpan ke JSON, teks biasa, atau basis data SQLite lokal.

Artikel ini menjelaskan arsitektur teknis tiap tahap pipeline, kontrak API Azure, dan pilihan desain pada lapisan CherryPy.

## Cara Kerja Audio Analyser: Ikhtisar Arsitektur

Pipeline memiliki lima tahap terpisah:

1. **Upload** — pengguna mengirim file audio melalui antarmuka web CherryPy. CherryPy menyimpan file di direktori sementara dan mengembalikan job ID.
2. **Transkripsi** — Audio Analyser mengirim file ke Azure Batch Transcription REST API. Karena batch transcription bersifat asinkron, aplikasi melakukan polling endpoint status job pada interval tertentu dan menunggu state `Succeeded` sebelum melanjutkan.
3. **NLP** — teks transkrip mentah diteruskan ke Azure AI Language untuk ekstraksi key phrase, NER, analisis sentimen, dan deteksi bahasa.
4. **Terjemahan** (opsional) — jika bahasa target ditentukan, transkrip dikirim ke Azure Translator, lalu analisis NLP dijalankan ulang pada teks terjemahan.
5. **Output** — hasil ditulis ke format output yang dipilih (JSON, TXT, atau SQLite) dan ditampilkan di UI web CherryPy.

Satu-satunya dependensi runtime di luar Python standard library adalah `azure-cognitiveservices-speech`, `azure-ai-textanalytics`, `azure-ai-translation-text`, dan `cherrypy`. Semua kredensial Azure dibaca dari environment variables.

## Azure Cognitive Services: Mesin Batch Transcription

API batch transcription layanan Azure Speech (`/speechtotext/v3.0/transcriptions`) menerima referensi file audio di Azure Blob Storage dan body konfigurasi JSON. Audio Analyser mengunggah file lokal ke Blob Storage menggunakan SAS URL yang sudah ditandatangani, lalu mengirim job transkripsi.

Payload minimal untuk pengiriman job:

```json
{
  "contentUrls": ["https://<account>.blob.core.windows.net/<container>/<file>.wav?<sas>"],
  "locale": "en-US",
  "displayName": "audio-analyser-job-001",
  "properties": {
    "diarizationEnabled": true,
    "wordLevelTimestampsEnabled": true,
    "punctuationMode": "DictatedAndAutomatic",
    "profanityFilterMode": "Masked"
  }
}
```

Array respons `recognizedPhrases` berisi satu objek untuk tiap ujaran yang dikenali. Setiap entri mencakup:

- `nBest[0].confidence` — float antara 0 dan 1
- `nBest[0].lexical` — kata mentah sebagaimana diucapkan
- `nBest[0].itn` — bentuk inverse-text-normalised, dengan angka, tanggal, dan mata uang diperluas
- `nBest[0].display` — format untuk dibaca, dengan tanda baca
- `speaker` — ID pembicara berupa integer ketika diarization diaktifkan

Fine-tuning **Custom Speech** tersedia untuk kosakata khusus domain. Mengunggah pronunciation lexicon atau adaptation corpus, yaitu kumpulan kalimat teks yang mewakili domain, menyesuaikan model bahasa dan dapat secara substansial mengurangi WER pada konten khusus seperti istilah finansial atau jargon medis.

## Natural Language Processing dengan Azure AI Language

Setelah transkripsi, Audio Analyser mengirim transkrip display-form ke Azure AI Language melalui Python SDK `azure-ai-textanalytics`:

```python
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

client = TextAnalyticsClient(
    endpoint=os.environ["AZURE_LANGUAGE_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["AZURE_LANGUAGE_KEY"])
)

documents = [{"id": "1", "language": detected_lang, "text": transcript}]

sentiment_result = client.analyze_sentiment(documents, show_opinion_mining=True)
for doc in sentiment_result:
    print(f"Sentiment: {doc.sentiment}")
    print(f"Scores: pos={doc.confidence_scores.positive:.2f} "
          f"neg={doc.confidence_scores.negative:.2f} "
          f"neu={doc.confidence_scores.neutral:.2f}")
    for sentence in doc.sentences:
        for opinion in sentence.mined_opinions:
            print(f"  Target: {opinion.target.text}, "
                  f"Assessment: {[a.text for a in opinion.assessments]}")

keyphrases_result = client.extract_key_phrases(documents)
entities_result  = client.recognize_entities(documents)
```

`show_opinion_mining=True` mengaktifkan sentimen level aspek: API tidak hanya mengembalikan polaritas tingkat dokumen, tetapi juga pasangan target-assessment spesifik, misalnya target="audio quality" dan assessment="poor". Ini membuat output berguna untuk mengidentifikasi masalah konkret dalam analisis panggilan layanan pelanggan.

Named entity recognition mengklasifikasikan span sebagai salah satu dari: `Person`, `Organization`, `Location`, `Event`, `Product`, `DateTime`, `Quantity`, `IP`, `URL`, `Email`, `PersonType`, `Skill`, `Address`, `PhoneNumber`.

## Dukungan Multibahasa melalui Azure Translator

Azure Translator dipanggil setelah deteksi bahasa ketika pengguna meminta bahasa target. Layanan ini mendukung 135 bahasa dan dialek dengan neural machine translation (NMT). Audio Analyser menggunakan endpoint REST `/translate` dengan `autodetect` sebagai parameter `from`, sehingga spesifikasi bahasa sumber tidak diperlukan:

```python
import requests, uuid

url = "https://api.cognitive.microsofttranslator.com/translate"
params = {"api-version": "3.0", "to": target_lang}
headers = {
    "Ocp-Apim-Subscription-Key": os.environ["AZURE_TRANSLATOR_KEY"],
    "Ocp-Apim-Subscription-Region": os.environ["AZURE_TRANSLATOR_REGION"],
    "Content-type": "application/json",
    "X-ClientTraceId": str(uuid.uuid4())
}
body = [{"text": transcript}]
response = requests.post(url, params=params, headers=headers, json=body)
translated_text = response.json()[0]["translations"][0]["text"]
detected_language = response.json()[0]["detectedLanguage"]["language"]
```

Setelah terjemahan, Audio Analyser secara opsional menjalankan ulang tahap NLP Text Analytics pada teks terjemahan agar output key phrase dan sentimen tersedia dalam bahasa sumber maupun bahasa target.

Pilihan format output (JSON, TXT, SQLite) ditetapkan saat startup. Output SQLite menyimpan setiap sesi analisis sebagai baris dengan kolom untuk job ID, timestamp, bahasa sumber, transkrip, transkrip terjemahan, skor sentimen, dan key phrase sebagai blob JSON, sehingga query SQL lintas sesi dapat dilakukan.

## CherryPy sebagai Lapisan Web

CherryPy memetakan route URL ke metode Python menggunakan controller berbasis kelas. Audio Analyser memakai tiga route:

| Route | Metode | Deskripsi |
|---|---|---|
| `GET /` | `index()` | Merender form upload |
| `POST /analyse` | `analyse()` | Menerima multipart upload, memicu pipeline, mengembalikan job ID |
| `GET /results/<job_id>` | `results()` | Melakukan polling status job; merender halaman hasil ketika selesai |

Konfigurasi minimal menjaga footprint server tetap kecil:

```python
import cherrypy

cherrypy.config.update({
    "server.socket_host": "0.0.0.0",
    "server.socket_port": 8080,
    "tools.sessions.on": True,
    "tools.sessions.timeout": 60
})
cherrypy.quickstart(AudioAnalyserApp(), "/", conf)
```

State sesi menyimpan job ID saat ini, format output yang dipilih, dan bahasa target terjemahan. Penyimpanan sesi bawaan CherryPy secara default berbasis file, sehingga tidak membutuhkan lapisan cache eksternal.

## Pertanyaan yang Sering Diajukan

**Format audio dan ukuran file apa yang diterima Audio Analyser?**
Azure Batch Transcription API mendukung file WAV, MP3, OGG, dan FLAC hingga 2,5 jam. File di luar rentang ini sebaiknya dipotong sebelum upload. File stereo diterima; konversi mono tidak diperlukan.

**Bagaimana cara kerja speaker diarisation?**
Mengatur `diarizationEnabled: true` dalam request batch transcription mengaktifkan model pemisahan pembicara Azure. Setiap `recognizedPhrase` dalam respons menyertakan field integer `speaker`. Model mengidentifikasi pembicara berdasarkan karakteristik akustik dan menetapkan ID konsisten dalam satu sesi, tetapi tidak mengidentifikasi siapa pembicara tersebut tanpa langkah pendaftaran voice profile terpisah.

**Apakah file audio disimpan setelah transkripsi?**
File audio diunggah ke Azure Blob Storage dengan SAS URL berumur pendek dan dihapus dari direktori lokal sementara setelah upload selesai. Retensi blob di Azure Blob Storage bergantung pada lifecycle policy container; secara default, Audio Analyser tidak menetapkan kebijakan penghapusan eksplisit, sehingga konfigurasi aturan TTL pendek, misalnya menghapus blob yang lebih lama dari 1 hari, direkomendasikan untuk deployment produksi.

**Bisakah analisis NLP dijalankan tanpa terjemahan?**
Ya. Terjemahan adalah tahap pipeline opsional yang dikendalikan oleh flag CLI `--target-lang` atau dropdown bahasa target di UI web. Ketika tidak ada bahasa target yang dipilih, pipeline hanya menjalankan speech-to-text dan Text Analytics.

## Referensi

1. Microsoft. *Batch transcription overview — Azure AI services*. Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/speech-service/batch-transcription>
2. Xiong, W. et al. "Achieving Human Parity in Conversational Speech Recognition." *Microsoft Research Technical Report*, 2016; updated 2021. <https://arxiv.org/abs/1610.05256>
3. Microsoft. *What is Azure AI Language?* Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/language-service/overview>
4. Microsoft. *Azure AI Translator — Supported languages*. Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/translator/language-support>

[00]: https://audioanalyser.co/ "Audio Analyser — alat analitik ucapan berbasis Azure"
