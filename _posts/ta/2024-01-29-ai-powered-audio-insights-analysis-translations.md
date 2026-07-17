---
title: "Audio Analyser: Azure பேச்சு, NLP மற்றும் மொழிபெயர்ப்பு பைப்லைன்"
tags: "Azure, CherryPy, SpeechToText, NLP, SentimentAnalysis, BatchTranscription, AudioAnalyser, NeuralASR, TextAnalytics, Multilingual, ISO 20022, post-quantum cryptography, AI, open source, DORA, platform engineering, sovereign cloud, cloud native banking"
subtitle: "Azure-ஆல் இயக்கப்படும் பேச்சு பகுப்பாய்வுக் கருவியின் கட்டமைப்பும் பைப்லைனும்"
description: "Audio Analyser ஆனது Azure Cognitive Services பேச்சு-முதல்-உரை நரம்பியல் மாதிரிகள், Text Analytics NLP, மற்றும் CherryPy ஆகியவற்றைப் பயன்படுத்தி ஒலிப்பதிவுகளை உணர்வுநிலை மதிப்பெண்கள், முக்கிய சொல் பிரித்தெடுத்தல் மற்றும் பன்மொழி மொழிபெயர்ப்புகளுடன் கூடிய தேடக்கூடிய படியெடுப்புகளாக மாற்றுகிறது."
date: "Jan 29, 2024"
language: "ta"
locale: "ta_IN"
banner: "https://cloudcdn.pro/stocks/images/modern-corporate-office-with-technological-displays.webp"
banner_alt: "குறைந்தபட்ச, நவீன பெருநிறுவன அலுவலகம்"
keywords: "Azure Cognitive Services, பேச்சு-முதல்-உரை, நரம்பியல் ஒலியியல் மாதிரி, Azure Text Analytics, இயற்கை மொழி செயலாக்கம், உணர்வுநிலை பகுப்பாய்வு, CherryPy, தொகுப்பு படியெடுப்பு API, பன்மொழி ASR, Azure Translator, ஒலி படியெடுப்பு, Python ஒலி செயலாக்கம்"
---

> **நிர்வாகச் சுருக்கம் / முக்கிய குறிப்புகள்**
>
> - **Azure தொகுப்பு படியெடுப்பு API** 2.5 மணிநேரம் வரையிலான ஒலிக் கோப்புகளை (WAV/MP3/OGG/FLAC) ஏற்று, அவற்றை ஒத்திசைவற்ற முறையில் செயலாக்கி, ஒவ்வொரு சொற்றொடருக்குமான `nBest` வேட்பாளர்கள், நம்பிக்கை மதிப்பெண்கள், தலைகீழ்-உரை-இயல்பாக்கப்பட்ட (ITN) வெளியீடு மற்றும் விருப்பமான பேச்சாளர் வேறுபடுத்தல் ஆகியவற்றுடன் கூடிய `recognizedPhrases` JSON அணிவரிசையை வழங்குகிறது — எந்த ஸ்ட்ரீமிங் இணைப்பும் தேவையில்லை (Microsoft Azure, 2024).
> - **Microsoft-இன் நரம்பியல் ஒலியியல் மாதிரிகள்** Switchboard உரையாடல் அளவுகோலில் முந்தைய மறைந்த மார்கோவ் மாதிரி (HMM) அடிப்படைகளுடன் ஒப்பிடும்போது சொல் பிழை விகிதத்தை (WER) தோராயமாக 50% குறைத்தன, அந்தத் தரவுத்தொகுப்பில் ~5.1% WER-இல் தொழில்முறை மனித படியெடுப்பாளர்களுடன் சமநிலையை அடைந்தன (Xiong et al., Microsoft Research, 2016/2021 புதுப்பிப்பு).
> - **Azure Text Analytics** (இப்போது Azure AI Language-இன் ஒரு பகுதி) படியெடுப்பு உரையை முக்கிய சொற்றொடர் பிரித்தெடுத்தல், பெயரிடப்பட்ட உட்பொருள் அங்கீகாரம் (NER), கருத்துச் சுரங்கத்துடன் கூடிய உணர்வுநிலை பகுப்பாய்வு மற்றும் மொழி கண்டறிதல் ஆகியவற்றின் மூலம் செயலாக்குகிறது — அனைத்தும் Python SDK-ஐப் பயன்படுத்தி ஒற்றை `analyze_sentiment` அல்லது `begin_analyze_actions` அழைப்பில்.
> - **CherryPy** வலை அடுக்கை வழங்குகிறது: URL வழிநடத்தல், மல்டிபார்ட் பதிவேற்ற கையாளுதல், அமர்வு மேலாண்மை மற்றும் Jinja2 வார்ப்புரு வழங்கல் ஆகியவை ஒற்றைச் சிக்கலான குறைந்தபட்ச Python செயல்பாட்டில், ஆர்கெஸ்ட்ரேஷன் மேல்நிலைச் செலவின்றி ஒற்றை குறைந்த-செலவு VM-இல் இயங்கக்கூடியது.
> - **Azure Translator NMT** மூல மொழியைத் தானாகக் கண்டறிந்து படியெடுப்புகளை 135 இலக்கு மொழிகளில் எதிலும் மொழிபெயர்க்கிறது, அதே பைப்லைன் இயக்கத்திற்குள் மூல மற்றும் மொழிபெயர்க்கப்பட்ட உரை இரண்டிலும் பின்தொடர் NLP பகுப்பாய்வை செயல்படுத்துகிறது.

[**Audio Analyser ⧉**][00] என்பது மூன்று Azure Cognitive Services-ஐ ஒற்றை பணிப்பாய்வுக்குள் இணைக்கும் ஒரு திறந்த மூல Python பயன்பாடு ஆகும்: பேச்சு-முதல்-உரைக்கான தொகுப்பு படியெடுப்பு, NLP-க்கான Azure AI Language (Text Analytics), மற்றும் பன்மொழி வெளியீட்டிற்கான Azure Translator. வலை இடைமுகம் CherryPy மூலம் வழங்கப்படுகிறது, மேலும் முடிவுகளை JSON, எளிய உரை அல்லது உள்ளூர் SQLite தரவுத்தளத்தில் நிலைநிறுத்தலாம்.

இந்தக் கட்டுரை ஒவ்வொரு பைப்லைன் நிலையின் தொழில்நுட்பக் கட்டமைப்பையும், Azure API ஒப்பந்தங்களையும், CherryPy அடுக்கில் மேற்கொள்ளப்பட்ட வடிவமைப்புத் தேர்வுகளையும் விவரிக்கிறது.

## Audio Analyser எவ்வாறு செயல்படுகிறது: கட்டமைப்பு மேலோட்டம்

பைப்லைனில் ஐந்து தனித்தனி நிலைகள் உள்ளன:

1. **பதிவேற்றம்** — பயனர் CherryPy வலை இடைமுகம் வழியாக ஒரு ஒலிக் கோப்பைச் சமர்ப்பிக்கிறார். CherryPy கோப்பை ஒரு தற்காலிக அடைவில் சேமித்து ஒரு வேலை ID-ஐ வழங்குகிறது.
2. **படியெடுப்பு** — Audio Analyser கோப்பை Azure தொகுப்பு படியெடுப்பு REST API-க்குச் சமர்ப்பிக்கிறது. தொகுப்பு படியெடுப்பு ஒத்திசைவற்றது என்பதால், பயன்பாடு வேலை நிலை இறுதிப்புள்ளியை இடைவெளிகளில் வாக்கெடுத்து, தொடர்வதற்கு முன் `Succeeded` நிலைக்காகக் காத்திருக்கிறது.
3. **NLP** — மூலப் படியெடுப்பு உரை முக்கிய சொற்றொடர் பிரித்தெடுத்தல், NER, உணர்வுநிலை பகுப்பாய்வு மற்றும் மொழி கண்டறிதலுக்காக Azure AI Language-க்கு அனுப்பப்படுகிறது.
4. **மொழிபெயர்ப்பு** (விருப்பம்) — ஒரு இலக்கு மொழி குறிப்பிடப்பட்டால், படியெடுப்பு Azure Translator-க்கு அனுப்பப்பட்டு, மொழிபெயர்க்கப்பட்ட உரையில் NLP பகுப்பாய்வு மீண்டும் இயக்கப்படுகிறது.
5. **வெளியீடு** — முடிவுகள் தேர்ந்தெடுக்கப்பட்ட வெளியீட்டு வடிவமைப்பில் (JSON, TXT அல்லது SQLite) எழுதப்பட்டு CherryPy வலை UI-இல் வழங்கப்படுகின்றன.

Python நிலையான நூலகத்திற்கு வெளியே உள்ள ஒரே இயக்க-நேர சார்புகள் `azure-cognitiveservices-speech`, `azure-ai-textanalytics`, `azure-ai-translation-text` மற்றும் `cherrypy` ஆகியவை மட்டுமே. அனைத்து Azure சான்றுகளும் சூழல் மாறிகளிலிருந்து படிக்கப்படுகின்றன.

## Azure Cognitive Services: தொகுப்பு படியெடுப்பு இயந்திரம்

Azure Speech சேவையின் தொகுப்பு படியெடுப்பு API (`/speechtotext/v3.0/transcriptions`) ஆனது Azure Blob Storage-இல் உள்ள ஒரு ஒலிக் கோப்பிற்கான குறிப்பையும் ஒரு கட்டமைப்பு JSON உடலையும் ஏற்கிறது. Audio Analyser உள்ளூர் கோப்பை முன்-கையொப்பமிடப்பட்ட SAS URL-ஐப் பயன்படுத்தி Blob Storage-க்குப் பதிவேற்றி, பின்னர் படியெடுப்பு வேலையைச் சமர்ப்பிக்கிறது.

ஒரு குறைந்தபட்ச வேலைச் சமர்ப்பிப்பு பேலோடு:

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

பதில் `recognizedPhrases` அணிவரிசை அங்கீகரிக்கப்பட்ட ஒவ்வொரு உச்சரிப்புக்கும் ஒரு பொருளைக் கொண்டுள்ளது. ஒவ்வொரு உள்ளீடும் பின்வருவனவற்றை உள்ளடக்கியது:

- `nBest[0].confidence` — 0-க்கும் 1-க்கும் இடையிலான ஃப்ளோட்
- `nBest[0].lexical` — பேசப்பட்டபடி மூலச் சொற்கள்
- `nBest[0].itn` — தலைகீழ்-உரை-இயல்பாக்கப்பட்ட வடிவம் (எண்கள், தேதிகள், நாணயங்கள் விரிவாக்கப்பட்டவை)
- `nBest[0].display` — நிறுத்தற்குறிகளுடன், படிப்பதற்காக வடிவமைக்கப்பட்டது
- `speaker` — வேறுபடுத்தல் இயக்கப்பட்டிருக்கும்போது முழு எண் பேச்சாளர் ID

களம்-குறிப்பிட்ட சொற்களஞ்சியத்திற்காக **Custom Speech** நுண்ணிய-சரிப்படுத்தல் கிடைக்கிறது. ஒரு உச்சரிப்பு சொற்களஞ்சியம் அல்லது தழுவல் தொகுப்பை (களத்தைப் பிரதிநிதித்துவப்படுத்தும் உரை வாக்கியங்களின் தொகுப்பு) பதிவேற்றுவது மொழி மாதிரியைச் சரிசெய்து, நிதிச் சொற்கள் அல்லது மருத்துவ சொற்கள் போன்ற சிறப்பு உள்ளடக்கத்தில் WER-ஐ கணிசமாகக் குறைக்கலாம்.

## Azure AI Language உடன் இயற்கை மொழி செயலாக்கம்

படியெடுப்பிற்குப் பிறகு, Audio Analyser காட்சி-வடிவ படியெடுப்பை `azure-ai-textanalytics` Python SDK வழியாக Azure AI Language-க்கு அனுப்புகிறது:

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

`show_opinion_mining=True` என்பது அம்சம்-நிலை உணர்வுநிலையைச் செயல்படுத்துகிறது: API ஆனது ஆவண-நிலை துருவமுனைப்பை மட்டுமல்ல, குறிப்பிட்ட இலக்கு–மதிப்பீட்டு ஜோடிகளையும் (எ.கா., target="audio quality", assessment="poor") வழங்குகிறது. இது வாடிக்கையாளர் சேவை அழைப்பு பகுப்பாய்வில் உறுதியான சிக்கல்களை அடையாளம் காண்பதற்கு வெளியீட்டைப் பயனுள்ளதாக்குகிறது.

பெயரிடப்பட்ட உட்பொருள் அங்கீகாரம் ஸ்பான்களை பின்வருவனவற்றில் ஒன்றாக வகைப்படுத்துகிறது: `Person`, `Organization`, `Location`, `Event`, `Product`, `DateTime`, `Quantity`, `IP`, `URL`, `Email`, `PersonType`, `Skill`, `Address`, `PhoneNumber`.

## Azure Translator வழியாக பன்மொழி ஆதரவு

பயனர் ஒரு இலக்கு மொழியைக் கோரும்போது, மொழி கண்டறிதலுக்குப் பிறகு Azure Translator அழைக்கப்படுகிறது. இந்தச் சேவை நரம்பியல் இயந்திர மொழிபெயர்ப்பு (NMT) மூலம் 135 மொழிகளையும் கிளைமொழிகளையும் ஆதரிக்கிறது. Audio Analyser ஆனது `from` அளவுருவாக `autodetect`-ஐக் கொண்டு `/translate` REST இறுதிப்புள்ளியைப் பயன்படுத்துகிறது, எனவே எந்த மூல-மொழி விவரக்குறிப்பும் தேவையில்லை:

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

மொழிபெயர்ப்பிற்குப் பிறகு, முக்கிய சொற்றொடர் மற்றும் உணர்வுநிலை வெளியீடுகள் மூல மற்றும் இலக்கு மொழிகள் இரண்டிலும் கிடைக்கும்படி, Audio Analyser விருப்பமாக மொழிபெயர்க்கப்பட்ட உரையில் Text Analytics NLP நிறைவைச் செயல்முறையை மீண்டும் இயக்குகிறது.

வெளியீட்டு வடிவமைப்புத் தேர்வு (JSON, TXT, SQLite) தொடக்கத்தில் அமைக்கப்படுகிறது. SQLite வெளியீடு ஒவ்வொரு பகுப்பாய்வு அமர்வையும் வேலை ID, நேர முத்திரை, மூல மொழி, படியெடுப்பு, மொழிபெயர்க்கப்பட்ட படியெடுப்பு, உணர்வுநிலை மதிப்பெண்கள் மற்றும் முக்கிய சொற்றொடர்களுக்கான நெடுவரிசைகளுடன் JSON blob ஆக ஒரு வரிசையாகச் சேமிக்கிறது — இது அமர்வுகள் முழுவதும் SQL வினவல்களைச் செயல்படுத்துகிறது.

## வலை அடுக்காக CherryPy

CherryPy வகுப்பு-அடிப்படையிலான கட்டுப்படுத்திகளைப் பயன்படுத்தி URL வழிகளை Python முறைகளுக்கு வரைபடமாக்குகிறது. Audio Analyser மூன்று வழிகளைப் பயன்படுத்துகிறது:

| வழி | முறை | விளக்கம் |
|---|---|---|
| `GET /` | `index()` | பதிவேற்ற படிவத்தை வழங்குகிறது |
| `POST /analyse` | `analyse()` | மல்டிபார்ட் பதிவேற்றத்தை ஏற்று, பைப்லைனைத் தூண்டி, வேலை ID-ஐ வழங்குகிறது |
| `GET /results/<job_id>` | `results()` | வேலை நிலையை வாக்கெடுக்கிறது; முடிந்ததும் முடிவுப் பக்கத்தை வழங்குகிறது |

குறைந்தபட்ச கட்டமைப்பு சர்வர் தடத்தைச் சிறியதாக வைத்திருக்கிறது:

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

அமர்வு நிலை தற்போதைய வேலை ID, தேர்ந்தெடுக்கப்பட்ட வெளியீட்டு வடிவமைப்பு மற்றும் இலக்கு மொழிபெயர்ப்பு மொழியை வைத்திருக்கிறது. CherryPy-இன் உள்ளமைந்த அமர்வுச் சேமிப்பு இயல்பாகக் கோப்பு-ஆதரவுடையது, எந்த வெளிப்புற தற்காலிக சேமிப்பு அடுக்கும் தேவையில்லை.

## அடிக்கடி கேட்கப்படும் கேள்விகள்

**Audio Analyser என்ன ஒலி வடிவமைப்புகளையும் கோப்பு அளவுகளையும் ஏற்கிறது?**
Azure தொகுப்பு படியெடுப்பு API ஆனது 2.5 மணிநேர நீளம் வரையிலான WAV, MP3, OGG மற்றும் FLAC கோப்புகளை ஆதரிக்கிறது. இந்த வரம்பிற்கு வெளியே உள்ள கோப்புகள் பதிவேற்றுவதற்கு முன் பிரிக்கப்பட வேண்டும். ஸ்டீரியோ கோப்புகள் ஏற்கப்படுகின்றன; மோனோ மாற்றம் தேவையில்லை.

**பேச்சாளர் வேறுபடுத்தல் எவ்வாறு செயல்படுகிறது?**
தொகுப்பு படியெடுப்பு கோரிக்கையில் `diarizationEnabled: true` என அமைப்பது Azure-இன் பேச்சாளர் பிரிப்பு மாதிரியைச் செயல்படுத்துகிறது. பதிலில் உள்ள ஒவ்வொரு `recognizedPhrase`-இலும் ஒரு `speaker` முழு எண் புலம் இருக்கும். மாதிரி பேச்சாளர்களை ஒலியியல் பண்புகளால் அடையாளம் கண்டு ஒரு அமர்வுக்குள் நிலையான ID-களை ஒதுக்குகிறது, ஆனால் தனியான குரல் சுயவிவரப் பதிவுநிலைப்படி இல்லாமல் பேச்சாளர்கள் யார் என்பதை அடையாளம் காணாது.

**படியெடுப்பிற்குப் பிறகு ஒலிக் கோப்புகள் தக்கவைக்கப்படுகின்றனவா?**
ஒலிக் கோப்புகள் ஒரு குறுகிய-ஆயுள் SAS URL உடன் Azure Blob Storage-க்குப் பதிவேற்றப்பட்டு, பதிவேற்றம் முடிந்த பிறகு தற்காலிக உள்ளூர் அடைவிலிருந்து நீக்கப்படுகின்றன. Azure Blob Storage-இல் blob-களின் தக்கவைப்பு கொள்கலனின் வாழ்க்கைச்சுழற்சிக் கொள்கையைப் பொறுத்தது; இயல்பாக, Audio Analyser ஒரு வெளிப்படையான நீக்கல் கொள்கையை அமைக்காது, எனவே உற்பத்தி வரிசைப்படுத்தல்களுக்கு Azure போர்ட்டலில் ஒரு குறுகிய TTL விதியை (எ.கா., 1 நாளைவிடப் பழைய blob-களை நீக்கு) கட்டமைப்பது பரிந்துரைக்கப்படுகிறது.

**மொழிபெயர்ப்பு இல்லாமல் NLP பகுப்பாய்வை இயக்க முடியுமா?**
ஆம். மொழிபெயர்ப்பு என்பது `--target-lang` CLI கொடியால் அல்லது வலை UI-இல் உள்ள இலக்கு மொழி கீழ்-தோன்றியால் கட்டுப்படுத்தப்படும் ஒரு விருப்பமான பைப்லைன் நிலையாகும். எந்த இலக்கு மொழியும் தேர்ந்தெடுக்கப்படாதபோது, பைப்லைன் பேச்சு-முதல்-உரை மற்றும் Text Analytics-ஐ மட்டுமே இயக்குகிறது.

## குறிப்புகள்

1. Microsoft. *Batch transcription overview — Azure AI services*. Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/speech-service/batch-transcription>
2. Xiong, W. et al. "Achieving Human Parity in Conversational Speech Recognition." *Microsoft Research Technical Report*, 2016; updated 2021. <https://arxiv.org/abs/1610.05256>
3. Microsoft. *What is Azure AI Language?* Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/language-service/overview>
4. Microsoft. *Azure AI Translator — Supported languages*. Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/translator/language-support>

[00]: https://audioanalyser.co/ "Audio Analyser — Azure-backed speech analytics tool"
