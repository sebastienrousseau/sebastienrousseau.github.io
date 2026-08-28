---
title: "Audio Analyser: Saluran Paip Pertuturan Azure, NLP, dan Terjemahan"
tags: "Azure, CherryPy, SpeechToText, NLP, SentimentAnalysis, BatchTranscription, AudioAnalyser, NeuralASR, TextAnalytics, Multilingual, ISO 20022, post-quantum cryptography, AI, open source, DORA, platform engineering, sovereign cloud, cloud native banking"
subtitle: "Seni bina dan saluran paip alat analitik pertuturan yang disokong Azure"
description: "Audio Analyser menggunakan model neural pertuturan-ke-teks Azure Cognitive Services, NLP Text Analytics, dan CherryPy untuk menukar rakaman audio menjadi transkrip boleh cari dengan skor sentimen, pengekstrakan kata kunci, dan terjemahan berbilang bahasa."
date: "Jan 29, 2024"
language: "ms"
locale: "ms_MY"
banner: "https://cloudcdn.pro/stocks/images/modern-corporate-office-with-technological-displays.webp"
banner_alt: "Pejabat korporat moden yang minimalis"
keywords: "Azure Cognitive Services, pertuturan-ke-teks, model akustik neural, Azure Text Analytics, pemprosesan bahasa tabii, analisis sentimen, CherryPy, API transkripsi kelompok, ASR berbilang bahasa, Azure Translator, transkripsi audio, pemprosesan audio Python"
---

> **Ringkasan Eksekutif / Intipati Utama**
>
> - **API Transkripsi Kelompok Azure** menerima fail audio sehingga 2.5 jam (WAV/MP3/OGG/FLAC), memprosesnya secara tak segerak, dan mengembalikan tatasusunan JSON `recognizedPhrases` dengan calon `nBest` setiap frasa, skor keyakinan, output ternormal-teks-songsang (ITN), dan diarisasi penutur pilihan — tanpa memerlukan sambungan penstriman (Microsoft Azure, 2024).
> - **Model akustik neural Microsoft** mengurangkan kadar ralat perkataan sebanyak kira-kira 50% berbanding garis dasar model Markov tersembunyi (HMM) terdahulu pada penanda aras perbualan Switchboard, mencapai kesetaraan dengan penyalin manusia profesional pada set data itu pada ~5.1% WER (Xiong et al., Microsoft Research, kemas kini 2016/2021).
> - **Azure Text Analytics** (kini sebahagian daripada Azure AI Language) memproses teks transkrip melalui pengekstrakan frasa utama, pengecaman entiti bernama (NER), analisis sentimen dengan perlombongan pendapat, dan pengesanan bahasa — kesemuanya dalam satu panggilan `analyze_sentiment` atau `begin_analyze_actions` menggunakan SDK Python.
> - **CherryPy** menyediakan lapisan web: penghalaan URL, pengendalian muat naik berbilang bahagian, pengurusan sesi, dan pemaparan templat Jinja2 dalam proses Python yang minimal yang boleh dijalankan pada satu VM kos rendah tanpa overhed orkestrasi.
> - **Azure Translator NMT** mengesan bahasa sumber secara automatik dan menterjemah transkrip ke dalam mana-mana daripada 135 bahasa sasaran, membolehkan analisis NLP hiliran ke atas kedua-dua teks asal dan terjemahan dalam larian saluran paip yang sama.

[**Audio Analyser ⧉**][00] ialah aplikasi Python sumber terbuka yang menyambungkan tiga Azure Cognitive Services ke dalam satu aliran kerja tunggal: Batch Transcription untuk pertuturan-ke-teks, Azure AI Language (Text Analytics) untuk NLP, dan Azure Translator untuk output berbilang bahasa. Antara muka web disajikan oleh CherryPy, dan hasil boleh dikekalkan ke JSON, teks biasa, atau pangkalan data SQLite tempatan.

Artikel ini menerangkan seni bina teknikal setiap peringkat saluran paip, kontrak API Azure, dan pilihan reka bentuk yang dibuat dalam lapisan CherryPy.

## Bagaimana Audio Analyser Berfungsi: Gambaran Seni Bina

Saluran paip ini mempunyai lima peringkat berasingan:

1. **Muat naik** — pengguna menyerahkan fail audio melalui antara muka web CherryPy. CherryPy menyimpan fail dalam direktori sementara dan mengembalikan ID kerja.
2. **Transkripsi** — Audio Analyser menyerahkan fail kepada REST API Azure Batch Transcription. Oleh sebab transkripsi kelompok bersifat tak segerak, aplikasi menyaring titik akhir status kerja pada selang waktu dan menunggu keadaan `Succeeded` sebelum meneruskan.
3. **NLP** — teks transkrip mentah dihantar kepada Azure AI Language untuk pengekstrakan frasa utama, NER, analisis sentimen, dan pengesanan bahasa.
4. **Terjemahan** (pilihan) — jika bahasa sasaran ditentukan, transkrip dihantar kepada Azure Translator, dan analisis NLP dijalankan semula ke atas teks yang diterjemah.
5. **Output** — hasil ditulis ke format output terpilih (JSON, TXT, atau SQLite) dan dipaparkan dalam UI web CherryPy.

Satu-satunya kebergantungan masa jalan di luar pustaka standard Python ialah `azure-cognitiveservices-speech`, `azure-ai-textanalytics`, `azure-ai-translation-text`, dan `cherrypy`. Semua kelayakan Azure dibaca daripada pemboleh ubah persekitaran.

## Azure Cognitive Services: Enjin Transkripsi Kelompok

API transkripsi kelompok perkhidmatan Azure Speech (`/speechtotext/v3.0/transcriptions`) menerima rujukan kepada fail audio dalam Azure Blob Storage dan badan JSON konfigurasi. Audio Analyser memuat naik fail tempatan ke Blob Storage menggunakan URL SAS pra-tandatangan, kemudian menyerahkan kerja transkripsi.

Muatan penyerahan kerja yang minimal:

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

Tatasusunan `recognizedPhrases` dalam respons mengandungi satu objek bagi setiap ujaran yang dikenali. Setiap entri termasuk:

- `nBest[0].confidence` — nilai apungan antara 0 dan 1
- `nBest[0].lexical` — perkataan mentah seperti yang dituturkan
- `nBest[0].itn` — bentuk ternormal-teks-songsang (nombor, tarikh, mata wang dikembangkan)
- `nBest[0].display` — diformat untuk dibaca, dengan tanda baca
- `speaker` — ID penutur integer apabila diarisasi didayakan

Penalaan halus **Custom Speech** tersedia untuk perbendaharaan kata khusus domain. Memuat naik leksikon sebutan atau korpus penyesuaian (satu set ayat teks yang mewakili domain) melaraskan model bahasa dan boleh mengurangkan WER dengan ketara pada kandungan khusus seperti istilah kewangan atau jargon perubatan.

## Pemprosesan Bahasa Tabii dengan Azure AI Language

Selepas transkripsi, Audio Analyser menghantar transkrip bentuk paparan kepada Azure AI Language melalui SDK Python `azure-ai-textanalytics`:

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

`show_opinion_mining=True` mendayakan sentimen peringkat aspek: API mengembalikan bukan sekadar polariti peringkat dokumen tetapi pasangan sasaran–penilaian tertentu (cth., target="audio quality", assessment="poor"). Ini menjadikan output berguna untuk mengenal pasti isu konkrit dalam analisis panggilan khidmat pelanggan.

Pengecaman entiti bernama mengelaskan julat sebagai salah satu daripada: `Person`, `Organization`, `Location`, `Event`, `Product`, `DateTime`, `Quantity`, `IP`, `URL`, `Email`, `PersonType`, `Skill`, `Address`, `PhoneNumber`.

## Sokongan Berbilang Bahasa melalui Azure Translator

Azure Translator dipanggil selepas pengesanan bahasa apabila pengguna meminta bahasa sasaran. Perkhidmatan ini menyokong 135 bahasa dan dialek dengan terjemahan mesin neural (NMT). Audio Analyser menggunakan titik akhir REST `/translate` dengan `autodetect` sebagai parameter `from`, jadi tiada penentuan bahasa sumber diperlukan:

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

Selepas terjemahan, Audio Analyser secara pilihan menjalankan semula laluan NLP Text Analytics ke atas teks yang diterjemah supaya output frasa utama dan sentimen tersedia dalam kedua-dua bahasa sumber dan sasaran.

Pemilihan format output (JSON, TXT, SQLite) ditetapkan semasa permulaan. Output SQLite menyimpan setiap sesi analisis sebagai satu baris dengan lajur bagi ID kerja, cap masa, bahasa sumber, transkrip, transkrip terjemah, skor sentimen, dan frasa utama sebagai blob JSON — membolehkan pertanyaan SQL merentas sesi.

## CherryPy sebagai Lapisan Web

CherryPy memetakan laluan URL kepada kaedah Python menggunakan pengawal berasaskan kelas. Audio Analyser menggunakan tiga laluan:

| Laluan | Kaedah | Penerangan |
|---|---|---|
| `GET /` | `index()` | Memaparkan borang muat naik |
| `POST /analyse` | `analyse()` | Menerima muat naik berbilang bahagian, mencetuskan saluran paip, mengembalikan ID kerja |
| `GET /results/<job_id>` | `results()` | Menyaring status kerja; memaparkan halaman hasil apabila selesai |

Konfigurasi minimal mengekalkan jejak pelayan kecil:

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

Keadaan sesi memegang ID kerja semasa, format output terpilih, dan bahasa terjemahan sasaran. Storan sesi terbina dalam CherryPy disokong fail secara lalai, tanpa memerlukan lapisan cache luaran.

## Soalan Lazim

**Apakah format audio dan saiz fail yang diterima oleh Audio Analyser?**
API Azure Batch Transcription menyokong fail WAV, MP3, OGG, dan FLAC sehingga 2.5 jam panjangnya. Fail di luar julat ini harus dibahagikan sebelum dimuat naik. Fail stereo diterima; penukaran mono tidak diperlukan.

**Bagaimanakah diarisasi penutur berfungsi?**
Menetapkan `diarizationEnabled: true` dalam permintaan transkripsi kelompok mengaktifkan model pengasingan penutur Azure. Setiap `recognizedPhrase` dalam respons termasuk medan integer `speaker`. Model mengenal pasti penutur mengikut ciri akustik dan memberikan ID yang konsisten dalam satu sesi, tetapi tidak mengenal pasti siapa penutur tanpa langkah pendaftaran profil suara yang berasingan.

**Adakah fail audio disimpan selepas transkripsi?**
Fail audio dimuat naik ke Azure Blob Storage dengan URL SAS berjangka pendek dan dipadamkan daripada direktori tempatan sementara selepas muat naik selesai. Pengekalan blob dalam Azure Blob Storage bergantung pada dasar kitaran hayat bekas; secara lalai, Audio Analyser tidak menetapkan dasar pemadaman eksplisit, jadi mengkonfigurasi peraturan TTL pendek (cth., padam blob yang lebih lama daripada 1 hari) dalam portal Azure disyorkan untuk penggunaan pengeluaran.

**Bolehkah analisis NLP dijalankan tanpa terjemahan?**
Ya. Terjemahan ialah peringkat saluran paip pilihan yang dikawal oleh bendera CLI `--target-lang` atau menu juntai bawah bahasa sasaran dalam UI web. Apabila tiada bahasa sasaran dipilih, saluran paip hanya menjalankan pertuturan-ke-teks dan Text Analytics sahaja.

## Rujukan

1. Microsoft. *Batch transcription overview — Azure AI services*. Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/speech-service/batch-transcription>
2. Xiong, W. et al. "Achieving Human Parity in Conversational Speech Recognition." *Microsoft Research Technical Report*, 2016; dikemas kini 2021. <https://arxiv.org/abs/1610.05256>
3. Microsoft. *What is Azure AI Language?* Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/language-service/overview>
4. Microsoft. *Azure AI Translator — Supported languages*. Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/translator/language-support>

[00]: https://audioanalyser.co/ "Audio Analyser — alat analitik pertuturan yang disokong Azure"

END_TRANSLATION
