---
title: "Audio Analyser: Azure Speech, NLP మరియు అనువాద పైప్‌లైన్"
tags: "Azure, CherryPy, SpeechToText, NLP, SentimentAnalysis, BatchTranscription, AudioAnalyser, NeuralASR, TextAnalytics, Multilingual, ISO 20022, post-quantum cryptography, AI, open source, DORA, platform engineering, sovereign cloud, cloud native banking"
subtitle: "Azure ఆధారిత స్పీచ్ అనలిటిక్స్ సాధనం యొక్క నిర్మాణం మరియు పైప్‌లైన్"
description: "Audio Analyser అనేది Azure Cognitive Services యొక్క స్పీచ్-టు-టెక్స్ట్ న్యూరల్ మోడల్స్, Text Analytics NLP మరియు CherryPyను ఉపయోగించి ఆడియో రికార్డింగ్‌లను సెంటిమెంట్ స్కోర్లు, కీవర్డ్ సంగ్రహణ మరియు బహుభాషా అనువాదాలతో కూడిన శోధించదగిన ట్రాన్స్‌క్రిప్ట్‌లుగా మారుస్తుంది."
date: "Jan 29, 2024"
language: "te"
locale: "te_IN"
banner: "https://cloudcdn.pro/stocks/images/modern-corporate-office-with-technological-displays.webp"
banner_alt: "కనిష్ఠవాద, ఆధునిక కార్పొరేట్ కార్యాలయం"
keywords: "Azure Cognitive Services, స్పీచ్-టు-టెక్స్ట్, న్యూరల్ ఎకౌస్టిక్ మోడల్, Azure Text Analytics, సహజ భాషా ప్రాసెసింగ్, సెంటిమెంట్ విశ్లేషణ, CherryPy, బ్యాచ్ ట్రాన్స్‌క్రిప్షన్ API, బహుభాషా ASR, Azure Translator, ఆడియో ట్రాన్స్‌క్రిప్షన్, Python ఆడియో ప్రాసెసింగ్"
---

> **కార్యనిర్వాహక సారాంశం / ముఖ్యాంశాలు**
>
> - **Azure Batch Transcription API** 2.5 గంటల వరకు (WAV/MP3/OGG/FLAC) ఆడియో ఫైల్‌లను స్వీకరిస్తుంది, వాటిని అసమకాలికంగా ప్రాసెస్ చేస్తుంది, మరియు ప్రతి-పదబంధ `nBest` అభ్యర్థులు, విశ్వాస స్కోర్లు, విలోమ-పాఠ్య-సాధారణీకృత (ITN) అవుట్‌పుట్ మరియు ఐచ్ఛిక వక్త డయరైజేషన్‌తో ఒక `recognizedPhrases` JSON శ్రేణిని తిరిగి ఇస్తుంది — స్ట్రీమింగ్ కనెక్షన్ అవసరం లేదు (Microsoft Azure, 2024).
> - **Microsoft యొక్క న్యూరల్ ఎకౌస్టిక్ మోడల్స్** Switchboard సంభాషణా బెంచ్‌మార్క్‌పై పూర్వపు హిడెన్ మార్కోవ్ మోడల్ (HMM) బేస్‌లైన్‌లతో పోలిస్తే పద దోష రేటును సుమారు 50% తగ్గించాయి, ఆ డేటాసెట్‌పై ~5.1% WER వద్ద వృత్తిపరమైన మానవ ట్రాన్స్‌క్రైబర్‌లతో సమానత్వాన్ని చేరుకున్నాయి (Xiong et al., Microsoft Research, 2016/2021 నవీకరణ).
> - **Azure Text Analytics** (ఇప్పుడు Azure AI Language లో భాగం) ట్రాన్స్‌క్రిప్ట్ పాఠ్యాన్ని కీ పదబంధ సంగ్రహణ, నామిత అస్తిత్వ గుర్తింపు (NER), అభిప్రాయ మైనింగ్‌తో సెంటిమెంట్ విశ్లేషణ మరియు భాషా గుర్తింపు ద్వారా ప్రాసెస్ చేస్తుంది — అన్నీ Python SDK ఉపయోగించి ఒకే `analyze_sentiment` లేదా `begin_analyze_actions` కాల్‌లో.
> - **CherryPy** వెబ్ లేయర్‌ను అందిస్తుంది: URL రూటింగ్, మల్టీపార్ట్ అప్‌లోడ్ నిర్వహణ, సెషన్ నిర్వహణ మరియు Jinja2 టెంప్లేట్ రెండరింగ్ — ఆర్కెస్ట్రేషన్ ఓవర్‌హెడ్ లేకుండా ఒకే తక్కువ-ఖర్చు VM పై నడవగల కనిష్ఠ Python ప్రాసెస్‌లో.
> - **Azure Translator NMT** మూల భాషను స్వయంచాలకంగా గుర్తించి, ట్రాన్స్‌క్రిప్ట్‌లను 135 లక్ష్య భాషలలో ఏదైనా దానికి అనువదిస్తుంది, ఒకే పైప్‌లైన్ రన్‌లో మూల మరియు అనువదించిన పాఠ్యం రెండింటిపైనా దిగువ NLP విశ్లేషణను సాధ్యం చేస్తుంది.

[**Audio Analyser ⧉**][00] అనేది మూడు Azure Cognitive Services లను ఒకే వర్క్‌ఫ్లోలో కలిపే ఒక ఓపెన్-సోర్స్ Python అప్లికేషన్: స్పీచ్-టు-టెక్స్ట్ కోసం Batch Transcription, NLP కోసం Azure AI Language (Text Analytics), మరియు బహుభాషా అవుట్‌పుట్ కోసం Azure Translator. వెబ్ ఇంటర్‌ఫేస్‌ను CherryPy అందిస్తుంది, మరియు ఫలితాలను JSON, సాదా పాఠ్యం లేదా స్థానిక SQLite డేటాబేస్‌కు నిలిపి ఉంచవచ్చు.

ఈ వ్యాసం ప్రతి పైప్‌లైన్ దశ యొక్క సాంకేతిక నిర్మాణం, Azure API కాంట్రాక్ట్‌లు, మరియు CherryPy లేయర్‌లో చేసిన డిజైన్ ఎంపికలను వివరిస్తుంది.

## Audio Analyser ఎలా పనిచేస్తుంది: నిర్మాణ అవలోకనం

పైప్‌లైన్‌లో ఐదు విభిన్న దశలు ఉన్నాయి:

1. **అప్‌లోడ్** — వినియోగదారు CherryPy వెబ్ ఇంటర్‌ఫేస్ ద్వారా ఒక ఆడియో ఫైల్‌ను సమర్పిస్తారు. CherryPy ఫైల్‌ను తాత్కాలిక డైరెక్టరీలో నిల్వ చేసి ఒక జాబ్ IDని తిరిగి ఇస్తుంది.
2. **ట్రాన్స్‌క్రిప్షన్** — Audio Analyser ఫైల్‌ను Azure Batch Transcription REST API కు సమర్పిస్తుంది. బ్యాచ్ ట్రాన్స్‌క్రిప్షన్ అసమకాలికం కావడంతో, అప్లికేషన్ నిర్దిష్ట వ్యవధులలో జాబ్ స్టేటస్ ఎండ్‌పాయింట్‌ను పోల్ చేస్తుంది మరియు కొనసాగడానికి ముందు `Succeeded` స్థితి కోసం వేచి ఉంటుంది.
3. **NLP** — ముడి ట్రాన్స్‌క్రిప్ట్ పాఠ్యం కీ పదబంధ సంగ్రహణ, NER, సెంటిమెంట్ విశ్లేషణ మరియు భాషా గుర్తింపు కోసం Azure AI Language కు అందించబడుతుంది.
4. **అనువాదం** (ఐచ్ఛికం) — ఒక లక్ష్య భాష పేర్కొనబడితే, ట్రాన్స్‌క్రిప్ట్ Azure Translator కు పంపబడుతుంది, మరియు NLP విశ్లేషణ అనువదించిన పాఠ్యంపై తిరిగి అమలు చేయబడుతుంది.
5. **అవుట్‌పుట్** — ఫలితాలు ఎంచుకున్న అవుట్‌పుట్ ఫార్మాట్‌కు (JSON, TXT లేదా SQLite) వ్రాయబడతాయి మరియు CherryPy వెబ్ UIలో రెండర్ చేయబడతాయి.

Python స్టాండర్డ్ లైబ్రరీ వెలుపల ఏకైక రన్‌టైమ్ డిపెండెన్సీలు `azure-cognitiveservices-speech`, `azure-ai-textanalytics`, `azure-ai-translation-text`, మరియు `cherrypy`. అన్ని Azure క్రెడెన్షియల్స్ ఎన్విరాన్‌మెంట్ వేరియబుల్స్ నుండి చదవబడతాయి.

## Azure Cognitive Services: బ్యాచ్ ట్రాన్స్‌క్రిప్షన్ ఇంజన్

Azure Speech సర్వీస్ బ్యాచ్ ట్రాన్స్‌క్రిప్షన్ API (`/speechtotext/v3.0/transcriptions`) Azure Blob Storage లోని ఆడియో ఫైల్‌కు ఒక సూచన మరియు ఒక కాన్ఫిగరేషన్ JSON బాడీని స్వీకరిస్తుంది. Audio Analyser ప్రీ-సైన్డ్ SAS URL ఉపయోగించి స్థానిక ఫైల్‌ను Blob Storage కు అప్‌లోడ్ చేసి, ఆపై ట్రాన్స్‌క్రిప్షన్ జాబ్‌ను సమర్పిస్తుంది.

కనిష్ఠ జాబ్ సమర్పణ పేలోడ్:

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

ప్రతిస్పందన `recognizedPhrases` శ్రేణి గుర్తించబడిన ప్రతి ఉచ్చారణకు ఒక వస్తువును కలిగి ఉంటుంది. ప్రతి ఎంట్రీ వీటిని కలిగి ఉంటుంది:

- `nBest[0].confidence` — 0 మరియు 1 మధ్య ఫ్లోట్
- `nBest[0].lexical` — మాట్లాడిన విధంగా ముడి పదాలు
- `nBest[0].itn` — విలోమ-పాఠ్య-సాధారణీకృత రూపం (సంఖ్యలు, తేదీలు, కరెన్సీలు విస్తరించబడతాయి)
- `nBest[0].display` — విరామ చిహ్నాలతో చదవడానికి ఫార్మాట్ చేయబడింది
- `speaker` — డయరైజేషన్ ప్రారంభించబడినప్పుడు పూర్ణాంక వక్త ID

**Custom Speech** ఫైన్-ట్యూనింగ్ డొమైన్-నిర్దిష్ట పదజాలం కోసం అందుబాటులో ఉంది. ఒక ఉచ్చారణ లెక్సికాన్ లేదా అనుసరణ కార్పస్ (డొమైన్‌ను ప్రతిబింబించే పాఠ్య వాక్యాల సమితి) అప్‌లోడ్ చేయడం భాషా మోడల్‌ను సర్దుబాటు చేస్తుంది మరియు ఆర్థిక పదాలు లేదా వైద్య పరిభాష వంటి ప్రత్యేక కంటెంట్‌పై WERను గణనీయంగా తగ్గించగలదు.

## Azure AI Language తో సహజ భాషా ప్రాసెసింగ్

ట్రాన్స్‌క్రిప్షన్ తర్వాత, Audio Analyser డిస్‌ప్లే-ఫారమ్ ట్రాన్స్‌క్రిప్ట్‌ను `azure-ai-textanalytics` Python SDK ద్వారా Azure AI Language కు పంపుతుంది:

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

`show_opinion_mining=True` అంశ-స్థాయి సెంటిమెంట్‌ను ప్రారంభిస్తుంది: API కేవలం పత్ర-స్థాయి ధ్రువీకరణను మాత్రమే కాకుండా నిర్దిష్ట లక్ష్యం–అంచనా జతలను తిరిగి ఇస్తుంది (ఉదా., target="audio quality", assessment="poor"). ఇది కస్టమర్ సర్వీస్ కాల్ విశ్లేషణలో నిర్దిష్ట సమస్యలను గుర్తించడానికి అవుట్‌పుట్‌ను ఉపయోగకరంగా చేస్తుంది.

నామిత అస్తిత్వ గుర్తింపు స్పాన్‌లను వీటిలో ఒకటిగా వర్గీకరిస్తుంది: `Person`, `Organization`, `Location`, `Event`, `Product`, `DateTime`, `Quantity`, `IP`, `URL`, `Email`, `PersonType`, `Skill`, `Address`, `PhoneNumber`.

## Azure Translator ద్వారా బహుభాషా మద్దతు

వినియోగదారు లక్ష్య భాషను అభ్యర్థించినప్పుడు, భాషా గుర్తింపు తర్వాత Azure Translator ప్రారంభించబడుతుంది. ఈ సర్వీస్ న్యూరల్ మెషిన్ ట్రాన్స్‌లేషన్ (NMT)తో 135 భాషలు మరియు మాండలికాలకు మద్దతు ఇస్తుంది. Audio Analyser `/translate` REST ఎండ్‌పాయింట్‌ను `from` పరామితిగా `autodetect` తో ఉపయోగిస్తుంది, కాబట్టి మూల-భాషా స్పెసిఫికేషన్ అవసరం లేదు:

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

అనువాదం తర్వాత, Audio Analyser ఐచ్ఛికంగా అనువదించిన పాఠ్యంపై Text Analytics NLP పాస్‌ను తిరిగి అమలు చేస్తుంది, తద్వారా కీ పదబంధం మరియు సెంటిమెంట్ అవుట్‌పుట్‌లు మూల మరియు లక్ష్య భాషలు రెండింటిలోనూ అందుబాటులో ఉంటాయి.

అవుట్‌పుట్ ఫార్మాట్ ఎంపిక (JSON, TXT, SQLite) ప్రారంభంలో సెట్ చేయబడుతుంది. SQLite అవుట్‌పుట్ ప్రతి విశ్లేషణ సెషన్‌ను జాబ్ ID, టైమ్‌స్టాంప్, మూల భాష, ట్రాన్స్‌క్రిప్ట్, అనువదించిన ట్రాన్స్‌క్రిప్ట్, సెంటిమెంట్ స్కోర్లు మరియు కీ పదబంధాల కోసం నిలువు వరుసలతో ఒక వరుసగా నిల్వ చేస్తుంది (కీ పదబంధాలు JSON బ్లాబ్‌గా) — సెషన్‌ల అంతటా SQL ప్రశ్నలను సాధ్యం చేస్తుంది.

## వెబ్ లేయర్‌గా CherryPy

CherryPy క్లాస్-ఆధారిత కంట్రోలర్‌లను ఉపయోగించి URL రూట్‌లను Python పద్ధతులకు మ్యాప్ చేస్తుంది. Audio Analyser మూడు రూట్‌లను ఉపయోగిస్తుంది:

| రూట్ | పద్ధతి | వివరణ |
|---|---|---|
| `GET /` | `index()` | అప్‌లోడ్ ఫారమ్‌ను రెండర్ చేస్తుంది |
| `POST /analyse` | `analyse()` | మల్టీపార్ట్ అప్‌లోడ్‌ను స్వీకరిస్తుంది, పైప్‌లైన్‌ను ప్రేరేపిస్తుంది, జాబ్ IDను తిరిగి ఇస్తుంది |
| `GET /results/<job_id>` | `results()` | జాబ్ స్థితిని పోల్ చేస్తుంది; పూర్తయినప్పుడు ఫలిత పేజీని రెండర్ చేస్తుంది |

కనిష్ఠ కాన్ఫిగరేషన్ సర్వర్ ఫుట్‌ప్రింట్‌ను చిన్నగా ఉంచుతుంది:

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

సెషన్ స్థితి ప్రస్తుత జాబ్ ID, ఎంచుకున్న అవుట్‌పుట్ ఫార్మాట్ మరియు లక్ష్య అనువాద భాషను కలిగి ఉంటుంది. CherryPy యొక్క అంతర్నిర్మిత సెషన్ నిల్వ డిఫాల్ట్‌గా ఫైల్-బ్యాక్డ్, ఇది ఏ బాహ్య కాష్ లేయర్ అవసరం లేదు.

## తరచుగా అడిగే ప్రశ్నలు

**Audio Analyser ఏ ఆడియో ఫార్మాట్‌లు మరియు ఫైల్ పరిమాణాలను స్వీకరిస్తుంది?**
Azure Batch Transcription API 2.5 గంటల నిడివి వరకు WAV, MP3, OGG మరియు FLAC ఫైల్‌లకు మద్దతు ఇస్తుంది. ఈ పరిధి వెలుపల ఉన్న ఫైల్‌లను అప్‌లోడ్‌కు ముందు విభజించాలి. స్టీరియో ఫైల్‌లు స్వీకరించబడతాయి; మోనో మార్పిడి అవసరం లేదు.

**వక్త డయరైజేషన్ ఎలా పనిచేస్తుంది?**
బ్యాచ్ ట్రాన్స్‌క్రిప్షన్ అభ్యర్థనలో `diarizationEnabled: true` సెట్ చేయడం Azure యొక్క వక్త వేరుచేసే మోడల్‌ను క్రియాశీలం చేస్తుంది. ప్రతిస్పందనలోని ప్రతి `recognizedPhrase` ఒక `speaker` పూర్ణాంక ఫీల్డ్‌ను కలిగి ఉంటుంది. మోడల్ ఎకౌస్టిక్ లక్షణాల ద్వారా వక్తలను గుర్తించి, ఒక సెషన్‌లో స్థిరమైన IDలను కేటాయిస్తుంది, కానీ ప్రత్యేక వాయిస్ ప్రొఫైల్ నమోదు దశ లేకుండా వక్తలు ఎవరో గుర్తించదు.

**ట్రాన్స్‌క్రిప్షన్ తర్వాత ఆడియో ఫైల్‌లు నిలుపబడతాయా?**
ఆడియో ఫైల్‌లు స్వల్పకాలిక SAS URLతో Azure Blob Storage కు అప్‌లోడ్ చేయబడతాయి మరియు అప్‌లోడ్ పూర్తయిన తర్వాత తాత్కాలిక స్థానిక డైరెక్టరీ నుండి తొలగించబడతాయి. Azure Blob Storage లో బ్లాబ్‌ల నిలుపుదల కంటైనర్ యొక్క లైఫ్‌సైకిల్ విధానంపై ఆధారపడి ఉంటుంది; డిఫాల్ట్‌గా, Audio Analyser స్పష్టమైన తొలగింపు విధానాన్ని సెట్ చేయదు, కాబట్టి ఉత్పత్తి విస్తరణల కోసం Azure పోర్టల్‌లో ఒక చిన్న TTL నియమాన్ని (ఉదా., 1 రోజు కంటే పాత బ్లాబ్‌లను తొలగించడం) కాన్ఫిగర్ చేయడం సిఫార్సు చేయబడింది.

**అనువాదం లేకుండా NLP విశ్లేషణను అమలు చేయవచ్చా?**
అవును. అనువాదం అనేది `--target-lang` CLI ఫ్లాగ్ లేదా వెబ్ UIలోని లక్ష్య భాష డ్రాప్‌డౌన్ ద్వారా నియంత్రించబడే ఒక ఐచ్ఛిక పైప్‌లైన్ దశ. ఏ లక్ష్య భాష ఎంచుకోబడనప్పుడు, పైప్‌లైన్ కేవలం స్పీచ్-టు-టెక్స్ట్ మరియు Text Analytics మాత్రమే అమలు చేస్తుంది.

## సూచనలు

1. Microsoft. *Batch transcription overview — Azure AI services*. Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/speech-service/batch-transcription>
2. Xiong, W. et al. "Achieving Human Parity in Conversational Speech Recognition." *Microsoft Research Technical Report*, 2016; updated 2021. <https://arxiv.org/abs/1610.05256>
3. Microsoft. *What is Azure AI Language?* Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/language-service/overview>
4. Microsoft. *Azure AI Translator — Supported languages*. Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/translator/language-support>

[00]: https://audioanalyser.co/ "Audio Analyser — Azure-backed speech analytics tool"
