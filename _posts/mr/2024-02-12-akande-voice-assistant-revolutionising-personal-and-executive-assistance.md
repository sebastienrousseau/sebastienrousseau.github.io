---
title: "Àkàndé: कार्यकारी अधिकाऱ्यांसाठी GPT-आधारित व्हॉइस असिस्टंट"
tags: "Àkàndé, GPT4, WhisperSTT, SQLiteCache, fpdf2, PythonVoiceAssistant, ChatCompletionsAPI, PDFSummary, open source, ExecutiveAI, ISO 20022, post-quantum cryptography, AI, DORA, platform engineering, sovereign cloud, cloud native banking"
subtitle: "ओपन-सोर्स Python व्हॉइस असिस्टंटची रचना: Whisper, GPT-4, SQLite कॅशे, आणि fpdf2"
description: "Àkàndé हे एक ओपन-सोर्स Python व्हॉइस असिस्टंट आहे जे OpenAI Whisper स्पीच रिकग्निशन, GPT-4 चॅट कम्प्लीशन्स, आणि स्थानिक SQLite रिस्पॉन्स कॅशे यांना एका व्हॉइस-चलित वर्कफ्लोमध्ये जोडते; ते संभाषण इतिहासातून PDF सारांश तयार करते आणि सर्व साठवलेला डेटा स्थानिकच ठेवते."
date: "Feb 12, 2024"
language: "mr"
locale: "mr_IN"
banner: "https://cloudcdn.pro/stocks/images/akande-voice-assistant.webp"
banner_alt: "एक पांढरे, गोलाकार आधुनिक उपकरण"
keywords: "Àkàndé, OpenAI GPT-4, Whisper STT, SQLite कॅशिंग, fpdf2, Python व्हॉइस असिस्टंट, चॅट कम्प्लीशन्स API, PDF सारांश निर्मिती, SHA-256 कॅशे, टेक्स्ट-टू-स्पीच, कार्यकारी असिस्टंट AI, ओपन-सोर्स"
---

> **कार्यकारी सारांश / मुख्य मुद्दे**
>
> - **[Àkàndé ⧉][00]** हे एक ओपन-सोर्स Python व्हॉइस असिस्टंट आहे जे OpenAI Whisper स्पीच-टू-टेक्स्ट, GPT-4 चॅट कम्प्लीशन्स, स्थानिक SQLite रिस्पॉन्स कॅशे, आणि fpdf2 PDF एक्सपोर्ट यांना एका व्हॉइस-चलित वर्कफ्लोमध्ये जोडते; यासाठी कोणतीही क्लाउड साठवण किंवा स्थानिक AI मॉडेल वेट्सची गरज नाही.
> - **SQLite कॅशे** सामान्यीकृत क्वेरी स्ट्रिंग्जचे SHA-256 हॅश साठवते आणि ते कच्च्या API रिस्पॉन्स टेक्स्टशी जोडते; कॅशे हिट्ससाठी शून्य टोकन खर्च होतो आणि ते 10  ms च्या आत परत येतात, त्यामुळे पुनरावृत्त क्वेऱ्या (जसे की मीटिंगच्या आधी घेतलेल्या निर्णयाचा पुनरावलोकन) मूलतः विनामूल्य होतात.
> - **बहु-वळणी संभाषण** हे मेमरीमध्ये `messages` यादी तयार करून आणि प्रत्येक चॅट कम्प्लीशन्स API कॉलवर ती पाठवून राखले जाते; मॉडेलला संपूर्ण सत्राचा इतिहास मिळतो त्यामुळे ते आधीच्या देवाणघेवाणीचा संदर्भ देऊ शकते, याची किंमत म्हणजे प्रत्येक वळणागणिक टोकन वापर हळूहळू वाढतो.
> - **PDF सारांश निर्मिती** सत्राची `messages` यादी एका स्वरूपित fpdf2 दस्तऐवजात रूपांतरित करते: वापरकर्त्याची वळणे आणि असिस्टंटची वळणे यांना लेबल दिली जातात, टाइमस्टॅम्प घातले जातात, आणि स्वयंचलित पॅजिनेशन कोणत्याही लांबीच्या सत्रांना हाताळते; फाईल स्थानिक फाइलसिस्टमवर लिहिली जाते, अपलोड केली जात नाही.
> - **गोपनीयता सीमा:** फक्त लाइव्ह क्वेरी (आणि संदर्भ विंडोच्या मर्यादेपर्यंतचा सत्र इतिहास) उपकरण सोडते; कोणतेही ऑडिओ रेकॉर्डिंग, कोणतेही ट्रान्सक्रिप्ट, आणि कोणतेही कॅश्ड रिस्पॉन्स OpenAI च्या API व्यतिरिक्त इतर कोणत्याही दूरस्थ सेवेला पाठवले जात नाहीत.

[**Àkàndé ⧉**][00] हे एक ओपन-सोर्स Python व्हॉइस असिस्टंट आहे जे तीन जोडणी करता येण्याजोग्या घटकांभोवती बांधले आहे: स्पीच रिकग्निशनसाठी OpenAI Whisper, भाषा समजून घेण्यासाठी आणि निर्मितीसाठी GPT-4 चॅट कम्प्लीशन्स API, आणि रिस्पॉन्स कॅशिंग व सत्र टिकवण्यासाठी स्थानिक SQLite डेटाबेस. याचा परिणाम असा एक व्हॉइस-चलित वर्कफ्लो आहे जो स्थानिक मॉडेल वेट्स, ऑफलाइन साठवण पायाभूत सुविधा, किंवा कंटेनर स्टॅकशिवाय लॅपटॉपवर चालवता येतो.

हा लेख प्रत्येक घटकाची तांत्रिक रचना, कॅशिंग व बहु-वळणी संदर्भाभोवतीचे रचना निर्णय, आणि PDF एक्सपोर्ट पाइपलाइन यांचे वर्णन करतो.

## पाइपलाइनचा आढावा

एकच Àkàndé संवाद या क्रमाने घडतो:

1. **ऑडिओ कॅप्चर** — वापरकर्ता बोलतो; अनुप्रयोग `sounddevice` किंवा सुसंगत ऑडिओ लायब्ररी वापरून ऑडिओ एका तात्पुरत्या WAV फाईलमध्ये रेकॉर्ड करतो.
2. **स्पीच-टू-टेक्स्ट** — WAV फाईल `openai.audio.transcriptions.create()` (Whisper API) ला सादर केली जाते; ट्रान्सक्रिप्ट एक साध्या स्ट्रिंगच्या स्वरूपात परत मिळतो.
3. **कॅशे लुकअप** — ट्रान्सक्रिप्ट सामान्यीकृत केला जातो (लोअरकेस केला जातो, व्हाईटस्पेस संकुचित केली जाते) आणि SHA-256 हॅश केला जातो; हा हॅश स्थानिक SQLite `response_cache` टेबलमध्ये शोधला जातो.
4. **API कॉल किंवा कॅशे हिट** — मिस झाल्यास, ट्रान्सक्रिप्ट सत्राच्या `messages` यादीत जोडला जातो आणि `openai.chat.completions.create()` ला पाठवला जातो; रिस्पॉन्स टेक्स्ट कॅशेमध्ये साठवला जातो.
5. **टेक्स्ट-टू-स्पीच** — रिस्पॉन्स टेक्स्ट `openai.audio.speech.create()` एंडपॉइंट (TTS) किंवा स्थानिक TTS लायब्ररी वापरून ऑडिओमध्ये रूपांतरित केला जातो, आणि परत वाजवला जातो.
6. **PDF एक्सपोर्ट** (मागणीनुसार) — संपूर्ण `messages` यादी एका स्वरूपित fpdf2 दस्तऐवजात रूपांतरित केली जाते आणि डिस्कवर लिहिली जाते.

## OpenAI एकात्मता: चॅट कम्प्लीशन्स आणि Whisper

Àkàndé स्पीच रिकग्निशन आणि टेक्स्ट निर्मिती या दोन्हीसाठी `openai` Python SDK वापरते. Whisper ट्रान्सक्रिप्शन कॉल:

```python
with open(audio_file_path, "rb") as f:
    transcript = openai.audio.transcriptions.create(
        model="whisper-1",
        file=f,
        language=None  # auto-detect
    )
user_text = transcript.text
```

चॅट कम्प्लीशन्स कॉल एक सत्र-मर्यादित `messages` यादी राखते:

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

सिस्टम प्रॉम्प्ट सत्राच्या सुरुवातीला एकदाच जोडला जातो आणि तो Àkàndé चे व्यक्तिमत्त्व, आउटपुट स्वरूप, आणि कोणतीही डोमेन-विशिष्ट मर्यादा नियंत्रित करतो:

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

`temperature=0.2` सेट केल्याने सर्जनशील विविधतेच्या बदल्यात निश्चितता मिळते; सत्रात आधी घेतलेला निर्णय आठवण्यासारख्या तथ्यात्मक क्वेऱ्यांसाठी हे महत्त्वाचे आहे.

## SQLite रिस्पॉन्स कॅशे

कॅशे स्कीमा किमान आहे:

```sql
CREATE TABLE IF NOT EXISTS response_cache (
    query_hash  TEXT PRIMARY KEY,
    response    TEXT NOT NULL,
    created_at  INTEGER NOT NULL  -- Unix timestamp
);
```

लुकअप आणि राईट पथ:

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

`INSERT OR REPLACE` याची खात्री करते की मॉडेल अपग्रेडनंतर तीच क्वेरी सादर केल्यास कॅश्ड रिस्पॉन्स अद्ययावत होतो. कॅशेचा आकार मर्यादित ठेवण्यासाठी सुरुवातीला एक TTL-आधारित एव्हिक्शन क्वेरी (`DELETE WHERE created_at < ?`) शेड्यूल केली जाऊ शकते.

कॅशे हिट कार्यक्षमता: स्थानिक SSD वर SQLite लुकअप ~1,00,000 पंक्तींपर्यंतच्या टेबलांसाठी 1 ms च्या आत परत येतो. लहान प्रतिसादांसाठी लाइव्ह GPT-4 API कॉलची राउंड-ट्रिप विलंब सामान्यतः 600–900 ms असते. काही पुनरावृत्त क्वेऱ्या असलेल्या दैनंदिन ब्रीफिंगसाठी, पहिल्या सत्रानंतर कॅशे बहुतांश API कॉल्स काढून टाकते.

## PDF सारांश निर्मिती

PDF एक्सपोर्टसाठी [fpdf2](https://py-pdf.github.io/fpdf2/) वापरले जाते, जे कोणत्याही बायनरी अवलंबनांशिवाय देखभाल केलेले Python PDF लायब्ररी आहे:

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

`multi_cell()` ओळ-गुंडाळणी आणि स्वयंचलित पृष्ठ-खंड हाताळते, त्यामुळे कोणत्याही लांबीची सत्रे मॅन्युअल पॅजिनेशन तर्कशास्त्राशिवाय एक सुव्यवस्थित दस्तऐवज तयार करतात. आउटपुट हे मानक Helvetica मेट्रिक्सव्यतिरिक्त कोणत्याही एम्बेडेड फॉन्टशिवाय एक PDF/A-सुसंगत फाईल असते.

## गोपनीयता मॉडेल

Àkàndé मधील गोपनीयता सीमा तीन तथ्यांनी परिभाषित केली आहे:

1. ऑडिओ HTTPS वरून Whisper API ला सादर केला जातो आणि तो API कॉलनंतर OpenAI कडून ठेवला जात नाही (फेब्रुवारी 2024 पर्यंतच्या OpenAI च्या API डेटा वापर धोरणानुसार).
2. चॅट कम्प्लीशन्स API कॉल्स सत्राची `messages` यादी प्रसारित करतात; बहु-वळणी सत्रांसाठी त्यात संपूर्ण संभाषण इतिहास असू शकतो.
3. SQLite डेटाबेस आणि PDF फाईल्स पूर्णपणे स्थानिक फाइलसिस्टमवर राहतात; कोणत्याही क्लाउड सेवेशी पार्श्वभूमी सिंक होत नाही.

संवेदनशील विषयांशी संबंधित कार्यकारी वापर प्रकरणांसाठी, जसे की विलीनीकरण व अधिग्रहण चर्चा, कर्मचारीविषयक बाबी, किंवा नियामक धोरण, API ला प्रसारित होणारा सत्र इतिहास तैनातीपूर्वी संस्थेच्या AI वापर धोरणाशी तपासून पाहिला पाहिजे. सिस्टम प्रॉम्प्टवरील `max_tokens` मर्यादेचा वापर इच्छित प्रकटीकरण व्याप्तीच्या पलीकडे जाणाऱ्या संदर्भाचे अनवधानाने प्रसारण रोखण्यासाठी केला जाऊ शकतो.

## वारंवार विचारले जाणारे प्रश्न

**सत्र संपल्यानंतर Àkàndé संभाषण इतिहास ठेवते का?**
प्रक्रिया बाहेर पडल्यावर मेमरीतील `messages` यादी टाकून दिली जाते. संभाषण इतिहास तेव्हाच ठेवला जातो जेव्हा वापरकर्ता PDF एक्सपोर्ट सुरू करतो किंवा एखादा सानुकूल टिकवणी स्तर जोडला जातो. SQLite कॅशे क्वेरी हॅश आणि रिस्पॉन्स टेक्स्ट साठवते, संपूर्ण संभाषण संदर्भ नाही.

**समान पण एकसारख्या नसलेल्या क्वेऱ्या कॅशे कशी हाताळते?**
कॅशे सामान्यीकृत क्वेरी स्ट्रिंगवर अचूक-जुळणी हॅशिंग वापरते. एका शब्दाने भिन्न असलेल्या दोन क्वेऱ्या वेगवेगळे हॅश तयार करतील आणि त्यामुळे स्वतंत्र API कॉल्स होतील. सिमँटिक कॅशिंग (जवळपास-डुप्लिकेट क्वेऱ्या जुळवण्यासाठी एम्बेडिंग साम्य वापरणे) यासाठी अतिरिक्त व्हेक्टर लुकअप पायरी आवश्यक असेल आणि ती मूळ अंमलबजावणीचा भाग नाही.

**Àkàndé डीफॉल्टनुसार कोणते GPT मॉडेल वापरते?**
फेब्रुवारी 2024 पर्यंत डीफॉल्ट `gpt-4-turbo-preview` आहे. मॉडेलचे नाव हे एक कॉन्फिगरेशन पॅरामीटर आहे, त्यामुळे कोणतेही OpenAI चॅट कम्प्लीशन मॉडेल बदलून वापरता येते. `gpt-3.5-turbo` वर स्विच केल्याने प्रति टोकन API खर्च सुमारे 20 पटीने कमी होतो परंतु जटिल बहु-पायरी क्वेऱ्यांसाठी तर्कक्षमतेची गुणवत्ता कमी होते.

**PDF एक्सपोर्ट स्वरूप सानुकूलित करता येते का?**
होय. fpdf2 एक्सपोर्ट फंक्शन `messages` यादी हेच त्याचे एकमेव आवश्यक इनपुट म्हणून स्वीकारते, त्यामुळे फॉन्ट, मार्जिन, पृष्ठ आकार, हेडर सामग्री, आणि लेबलिंग हे सर्व एक्सपोर्ट फंक्शन संपादित करून बदलता येते. fpdf2 प्रतिमा, टेबल्स, आणि Unicode फॉन्ट जोडण्यासही समर्थन देते, ज्यामुळे विशिष्ट ब्रँडिंग आवश्यकता असलेल्या संस्थांसाठी अधिक समृद्ध दस्तऐवज मांडणी शक्य होते.

## संदर्भ

1. OpenAI. *Audio Transcriptions — Whisper API*. OpenAI Platform Documentation, 2024. https://platform.openai.com/docs/api-reference/audio/createTranscription
2. OpenAI. *Chat Completions API*. OpenAI Platform Documentation, 2024. https://platform.openai.com/docs/api-reference/chat/create
3. Voss, J. et al. *fpdf2: Modern PDF generation for Python*. GitHub, 2024. https://github.com/py-pdf/fpdf2
4. SQLite Consortium. *SQLite Documentation*. sqlite.org, 2024. https://www.sqlite.org/docs.html

[00]: https://akande.co "Àkàndé Voice Assistant"
