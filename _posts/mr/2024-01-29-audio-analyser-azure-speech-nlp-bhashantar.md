---
title: "Audio Analyser: Azure Speech, NLP आणि भाषांतर पाइपलाइन"
tags: "Azure, CherryPy, SpeechToText, NLP, SentimentAnalysis, BatchTranscription, AudioAnalyser, NeuralASR, TextAnalytics, Multilingual, ISO 20022, post-quantum cryptography, AI, open source, DORA, platform engineering, sovereign cloud, cloud native banking"
subtitle: "Azure-आधारित स्पीच अॅनालिटिक्स साधनाची आर्किटेक्चर आणि पाइपलाइन"
description: "Audio Analyser हे Azure Cognitive Services चे speech-to-text न्यूरल मॉडेल्स, Text Analytics NLP आणि CherryPy वापरून ऑडिओ रेकॉर्डिंग्जना भावना-गुणांक, कीवर्ड निष्कर्षण आणि बहुभाषिक भाषांतरांसह शोधता येण्याजोग्या ट्रान्सक्रिप्ट्समध्ये रूपांतरित करते."
date: "Jan 29, 2024"
language: "mr"
locale: "mr_IN"
banner: "https://cloudcdn.pro/stocks/images/modern-corporate-office-with-technological-displays.webp"
banner_alt: "एक साधेपणाचे, आधुनिक कॉर्पोरेट कार्यालय"
keywords: "Azure Cognitive Services, speech-to-text, न्यूरल अकॉस्टिक मॉडेल, Azure Text Analytics, नैसर्गिक भाषा प्रक्रिया, भावना विश्लेषण, CherryPy, batch transcription API, बहुभाषिक ASR, Azure Translator, ऑडिओ ट्रान्सक्रिप्शन, Python ऑडिओ प्रक्रिया"
---

> **कार्यकारी सारांश / मुख्य मुद्दे**
>
> - **Azure Batch Transcription API** हे 2.5 तासांपर्यंतच्या ऑडिओ फाइल्स (WAV/MP3/OGG/FLAC) स्वीकारते, त्या अ‍ॅसिंक्रोनसपणे प्रक्रिया करते आणि प्रत्येक वाक्यासाठी `nBest` उमेदवार, आत्मविश्वास-गुणांक, inverse-text-normalised (ITN) आउटपुट आणि पर्यायी स्पीकर डायरायझेशनसह एक `recognizedPhrases` JSON अ‍ॅरे परत करते — कोणत्याही स्ट्रीमिंग कनेक्शनची गरज नाही (Microsoft Azure, 2024).
> - **Microsoft चे न्यूरल अकॉस्टिक मॉडेल्स** यांनी Switchboard संभाषण-आधारित बेंचमार्कवर पूर्वीच्या hidden Markov model (HMM) आधाररेषांच्या तुलनेत शब्द-त्रुटी-दर (word error rate) सुमारे 50% ने कमी केला, त्या डेटासेटवर ~5.1% WER गाठत व्यावसायिक मानवी ट्रान्सक्रायबर्सशी बरोबरी साधली (Xiong et al., Microsoft Research, 2016/2021 अद्यतन).
> - **Azure Text Analytics** (आता Azure AI Language चा भाग) हे Python SDK वापरून एकाच `analyze_sentiment` किंवा `begin_analyze_actions` कॉलमध्ये key phrase निष्कर्षण, named entity recognition (NER), opinion mining सह भावना विश्लेषण, आणि भाषा-ओळख यांद्वारे ट्रान्सक्रिप्ट मजकुरावर प्रक्रिया करते.
> - **CherryPy** वेब स्तर पुरवते: URL राउटिंग, multipart अपलोड हाताळणी, सत्र व्यवस्थापन, आणि Jinja2 टेम्पलेट रेंडरिंग — हे सर्व एका किमान Python प्रक्रियेत, जी ऑर्केस्ट्रेशनच्या अतिरिक्त भारशिवाय एकाच कमी किंमतीच्या VM वर चालू शकते.
> - **Azure Translator NMT** हे स्रोत भाषा आपोआप ओळखते आणि ट्रान्सक्रिप्ट्सचे 135 लक्ष्य भाषांपैकी कोणत्याहीमध्ये भाषांतर करते, ज्यामुळे एकाच पाइपलाइन रनमध्ये मूळ आणि भाषांतरित अशा दोन्ही मजकुरांवर पुढील NLP विश्लेषण करता येते.

[**Audio Analyser ⧉**][00] हे एक ओपन-सोर्स Python अ‍ॅप्लिकेशन आहे जे तीन Azure Cognitive Services ना एकाच वर्कफ्लोमध्ये जोडते: speech-to-text साठी Batch Transcription, NLP साठी Azure AI Language (Text Analytics), आणि बहुभाषिक आउटपुटसाठी Azure Translator. वेब इंटरफेस CherryPy द्वारे सर्व्ह केला जातो, आणि निकाल JSON, साध्या मजकुरात, किंवा स्थानिक SQLite डेटाबेसमध्ये जतन केले जाऊ शकतात.

हा लेख प्रत्येक पाइपलाइन टप्प्याचे तांत्रिक आर्किटेक्चर, Azure API करार, आणि CherryPy स्तरात घेतलेल्या रचना-निर्णयांचे वर्णन करतो.

## Audio Analyser कसे कार्य करते: आर्किटेक्चरचा आढावा

पाइपलाइनमध्ये पाच स्वतंत्र टप्पे आहेत:

1. **अपलोड** — वापरकर्ता CherryPy वेब इंटरफेसद्वारे एक ऑडिओ फाइल सादर करतो. CherryPy ती फाइल एका तात्पुरत्या डिरेक्टरीत साठवते आणि एक job ID परत करते.
2. **ट्रान्सक्रिप्शन** — Audio Analyser ती फाइल Azure Batch Transcription REST API कडे सादर करते. batch transcription अ‍ॅसिंक्रोनस असल्याने, अ‍ॅप्लिकेशन ठराविक अंतराने job स्थिती एंडपॉइंटची तपासणी करते आणि पुढे जाण्यापूर्वी `Succeeded` स्थितीची वाट पाहते.
3. **NLP** — कच्चा ट्रान्सक्रिप्ट मजकूर key phrase निष्कर्षण, NER, भावना विश्लेषण, आणि भाषा-ओळखीसाठी Azure AI Language कडे पाठवला जातो.
4. **भाषांतर** (पर्यायी) — जर एखादी लक्ष्य भाषा निर्दिष्ट केली असेल, तर ट्रान्सक्रिप्ट Azure Translator कडे पाठवला जातो, आणि भाषांतरित मजकुरावर NLP विश्लेषण पुन्हा चालवले जाते.
5. **आउटपुट** — निकाल निवडलेल्या आउटपुट स्वरूपात (JSON, TXT, किंवा SQLite) लिहिले जातात आणि CherryPy वेब UI मध्ये रेंडर केले जातात.

Python स्टँडर्ड लायब्ररी बाहेरील एकमेव रनटाइम अवलंबित्वे म्हणजे `azure-cognitiveservices-speech`, `azure-ai-textanalytics`, `azure-ai-translation-text`, आणि `cherrypy`. सर्व Azure क्रेडेन्शियल्स environment variables मधून वाचले जातात.

## Azure Cognitive Services: Batch Transcription इंजिन

Azure Speech सेवेचे batch transcription API (`/speechtotext/v3.0/transcriptions`) हे Azure Blob Storage मधील एका ऑडिओ फाइलचा संदर्भ आणि एक कॉन्फिगरेशन JSON बॉडी स्वीकारते. Audio Analyser स्थानिक फाइल एका pre-signed SAS URL वापरून Blob Storage वर अपलोड करते, आणि नंतर ट्रान्सक्रिप्शन job सादर करते.

एक किमान job सादरीकरण पेलोड:

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

प्रतिसादातील `recognizedPhrases` अ‍ॅरेमध्ये प्रत्येक ओळखल्या गेलेल्या उच्चारासाठी एक ऑब्जेक्ट असतो. प्रत्येक नोंदीमध्ये हे समाविष्ट असते:

- `nBest[0].confidence` — 0 आणि 1 दरम्यानचा float
- `nBest[0].lexical` — बोलल्याप्रमाणे कच्चे शब्द
- `nBest[0].itn` — inverse-text-normalised स्वरूप (आकडे, तारखा, चलन विस्तारित)
- `nBest[0].display` — विरामचिन्हांसह, वाचनासाठी स्वरूपित
- `speaker` — डायरायझेशन सक्षम असताना integer स्पीकर ID

**Custom Speech** फाइन-ट्यूनिंग हे डोमेन-विशिष्ट शब्दसंग्रहासाठी उपलब्ध आहे. एक pronunciation lexicon किंवा adaptation corpus (डोमेनचे प्रतिनिधित्व करणाऱ्या मजकूर वाक्यांचा संच) अपलोड केल्याने भाषा मॉडेल समायोजित होते आणि आर्थिक संज्ञा किंवा वैद्यकीय परिभाषा यांसारख्या विशेष सामग्रीवरील WER लक्षणीयरीत्या कमी करू शकते.

## Azure AI Language सह नैसर्गिक भाषा प्रक्रिया

ट्रान्सक्रिप्शननंतर, Audio Analyser `azure-ai-textanalytics` Python SDK द्वारे display-form ट्रान्सक्रिप्ट Azure AI Language कडे पाठवते:

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

`show_opinion_mining=True` हे aspect-स्तरीय भावना सक्षम करते: API फक्त दस्तऐवज-स्तरीय ध्रुवीयताच नव्हे तर विशिष्ट target–assessment जोड्या परत करते (उदा., target="audio quality", assessment="poor"). यामुळे ग्राहक-सेवा कॉल विश्लेषणातील ठोस समस्या ओळखण्यासाठी आउटपुट उपयुक्त ठरते.

Named entity recognition हे स्पॅन्सचे यापैकी एका वर्गात वर्गीकरण करते: `Person`, `Organization`, `Location`, `Event`, `Product`, `DateTime`, `Quantity`, `IP`, `URL`, `Email`, `PersonType`, `Skill`, `Address`, `PhoneNumber`.

## Azure Translator द्वारे बहुभाषिक समर्थन

वापरकर्त्याने लक्ष्य भाषेची विनंती केल्यावर भाषा-ओळखीनंतर Azure Translator कार्यान्वित केले जाते. ही सेवा neural machine translation (NMT) सह 135 भाषा आणि बोलींना समर्थन देते. Audio Analyser `/translate` REST एंडपॉइंट वापरते, ज्यात `from` पॅरामीटर म्हणून `autodetect` दिलेले असते, त्यामुळे स्रोत-भाषेचे कोणतेही विनिर्देशन आवश्यक नसते:

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

भाषांतरानंतर, Audio Analyser पर्यायाने भाषांतरित मजकुरावर Text Analytics NLP पास पुन्हा चालवते, जेणेकरून key phrase आणि भावना आउटपुट स्रोत आणि लक्ष्य अशा दोन्ही भाषांमध्ये उपलब्ध होतात.

आउटपुट स्वरूप निवड (JSON, TXT, SQLite) सुरुवातीलाच सेट केली जाते. SQLite आउटपुट प्रत्येक विश्लेषण सत्र एक पंक्ती (row) म्हणून साठवते, ज्यामध्ये job ID, टाइमस्टॅम्प, स्रोत भाषा, ट्रान्सक्रिप्ट, भाषांतरित ट्रान्सक्रिप्ट, भावना-गुणांक, आणि key phrases यांसाठी JSON blob अशा स्तंभांचा समावेश असतो — यामुळे सत्रांमध्ये SQL क्वेरीज करता येतात.

## वेब स्तर म्हणून CherryPy

CherryPy हे class-आधारित कंट्रोलर्स वापरून URL राउट्सना Python पद्धतींशी जोडते. Audio Analyser तीन राउट्स वापरते:

| राउट | पद्धत | वर्णन |
|---|---|---|
| `GET /` | `index()` | अपलोड फॉर्म रेंडर करते |
| `POST /analyse` | `analyse()` | multipart अपलोड स्वीकारते, पाइपलाइन सुरू करते, job ID परत करते |
| `GET /results/<job_id>` | `results()` | job स्थिती तपासते; पूर्ण झाल्यावर निकाल पृष्ठ रेंडर करते |

किमान कॉन्फिगरेशन सर्व्हरचा आकार लहान ठेवते:

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

सत्र-स्थिती (session state) सध्याचा job ID, निवडलेले आउटपुट स्वरूप, आणि लक्ष्य भाषांतर भाषा धारण करते. CherryPy चे अंगभूत सत्र-साठवण पूर्वनिर्धारितपणे फाइल-आधारित आहे, त्यामुळे कोणत्याही बाह्य कॅशे स्तराची आवश्यकता नाही.

## वारंवार विचारले जाणारे प्रश्न

**Audio Analyser कोणती ऑडिओ स्वरूपे आणि फाइल आकार स्वीकारते?**
Azure Batch Transcription API हे 2.5 तासांपर्यंतच्या लांबीच्या WAV, MP3, OGG, आणि FLAC फाइल्सना समर्थन देते. या मर्यादेबाहेरील फाइल्स अपलोडपूर्वी विभागल्या जाव्यात. स्टिरिओ फाइल्स स्वीकारल्या जातात; मोनो रूपांतरण आवश्यक नाही.

**स्पीकर डायरायझेशन कसे कार्य करते?**
batch transcription विनंतीत `diarizationEnabled: true` सेट केल्याने Azure चे स्पीकर-वेगळे-करण्याचे मॉडेल सक्रिय होते. प्रतिसादातील प्रत्येक `recognizedPhrase` मध्ये एक `speaker` integer फील्ड असते. मॉडेल स्पीकर्सना अकॉस्टिक वैशिष्ट्यांवरून ओळखते आणि एका सत्रात सुसंगत ID नियुक्त करते, परंतु स्वतंत्र voice profile नोंदणी टप्प्याशिवाय स्पीकर्स कोण आहेत हे ओळखत नाही.

**ट्रान्सक्रिप्शननंतर ऑडिओ फाइल्स राखून ठेवल्या जातात का?**
ऑडिओ फाइल्स अल्पायुषी SAS URL सह Azure Blob Storage वर अपलोड केल्या जातात आणि अपलोड पूर्ण झाल्यावर तात्पुरत्या स्थानिक डिरेक्टरीतून हटवल्या जातात. Azure Blob Storage मधील blobs चे राखून ठेवणे कंटेनरच्या lifecycle policy वर अवलंबून असते; पूर्वनिर्धारितपणे, Audio Analyser कोणतेही स्पष्ट हटवण्याचे धोरण सेट करत नाही, त्यामुळे उत्पादन तैनातींसाठी Azure portal मध्ये एक अल्प TTL नियम (उदा., 1 दिवसाहून जुने blobs हटवा) कॉन्फिगर करण्याची शिफारस केली जाते.

**NLP विश्लेषण भाषांतराशिवाय चालवता येते का?**
होय. भाषांतर हा एक पर्यायी पाइपलाइन टप्पा आहे, जो `--target-lang` CLI फ्लॅग किंवा वेब UI मधील लक्ष्य-भाषा ड्रॉपडाउनद्वारे नियंत्रित होतो. जेव्हा कोणतीही लक्ष्य भाषा निवडली जात नाही, तेव्हा पाइपलाइन फक्त speech-to-text आणि Text Analytics चालवते.

## संदर्भ

1. Microsoft. *Batch transcription overview — Azure AI services*. Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/speech-service/batch-transcription>
2. Xiong, W. et al. "Achieving Human Parity in Conversational Speech Recognition." *Microsoft Research Technical Report*, 2016; updated 2021. <https://arxiv.org/abs/1610.05256>
3. Microsoft. *What is Azure AI Language?* Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/language-service/overview>
4. Microsoft. *Azure AI Translator — Supported languages*. Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/translator/language-support>

[00]: https://audioanalyser.co/ "Audio Analyser — Azure-backed speech analytics tool"
