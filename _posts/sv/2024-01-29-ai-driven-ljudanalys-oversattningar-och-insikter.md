---
title: "Audio Analyser: pipeline för Azure Speech, NLP och översättning"
subtitle: "Arkitektur och pipeline för ett Azure-baserat talanalysverktyg"
description: "Audio Analyser använder neurala tal-till-text-modeller från Azure Cognitive Services, NLP via Text Analytics och CherryPy för att omvandla ljudinspelningar till sökbara transkript med sentimentpoäng, nyckelordsextraktion och flerspråkiga översättningar."
date: "January 29, 2024"
language: "sv-SE"
locale: "sv_SE"
banner: "https://cloudcdn.pro/stocks/images/modern-corporate-office-with-technological-displays.webp"
banner_alt: "Ett minimalistiskt, modernt företagskontor"
keywords: "Azure Cognitive Services, tal-till-text, neural akustisk modell, Azure Text Analytics, naturlig språkbehandling, sentimentanalys, CherryPy, batchtranskriberings-API, flerspråkig ASR, Azure Translator, ljudtranskribering, ljudbehandling i Python"
---

> **Sammanfattning / Viktigaste slutsatser**
>
> - **Azure Batch Transcription API** tar emot ljudfiler på upp till 2,5 timmar (WAV/MP3/OGG/FLAC), bearbetar dem asynkront och returnerar en JSON-array `recognizedPhrases` med `nBest`-kandidater per fras, konfidenspoäng, invers textnormaliserad (ITN) utdata och valfri talardiarisering; ingen strömmande anslutning krävs (Microsoft Azure, 2024).
> - **Microsofts neurala akustiska modeller** minskade ordfelfrekvensen med cirka 50 % relativt tidigare baslinjer med dolda Markovmodeller (HMM) på det konversationella riktmärket Switchboard, och nådde paritet med professionella mänskliga transkriberare på den datamängden vid cirka 5,1 % WER (Xiong m.fl., Microsoft Research, 2016, uppdaterad 2021).
> - **Azure Text Analytics** (numera en del av Azure AI Language) bearbetar transkripttext genom nyckelfrasextraktion, igenkänning av namngivna entiteter (NER), sentimentanalys med åsiktsutvinning och språkdetektering; allt i ett enda anrop till `analyze_sentiment` eller `begin_analyze_actions` via Python-SDK:n.
> - **CherryPy** utgör webblagret: URL-dirigering, hantering av multipart-uppladdningar, sessionshantering och rendering av Jinja2-mallar i en minimal Python-process som kan köras på en enda billig VM utan orkestreringskostnader.
> - **Azure Translator NMT** detekterar källspråket automatiskt och översätter transkript till valfritt av 135 målspråk, vilket möjliggör efterföljande NLP-analys på både original- och översatt text inom samma pipelinekörning.

[**Audio Analyser ⧉**][00] är en Python-applikation med öppen källkod som kopplar samman tre Azure Cognitive Services i ett enda arbetsflöde: Batch Transcription för tal-till-text, Azure AI Language (Text Analytics) för NLP och Azure Translator för flerspråkig utdata. Webbgränssnittet serveras av CherryPy, och resultaten kan sparas som JSON, ren text eller i en lokal SQLite-databas.

Denna artikel beskriver den tekniska arkitekturen för varje pipelinesteg, Azure-API:ernas kontrakt och designvalen i CherryPy-lagret.

## Så fungerar Audio Analyser: arkitekturöversikt

Pipelinen består av fem separata steg:

1. **Uppladdning**: användaren skickar in en ljudfil via CherryPy-webbgränssnittet. CherryPy lagrar filen i en temporär katalog och returnerar ett jobb-ID.
2. **Transkribering**: Audio Analyser skickar filen till Azure Batch Transcription REST API. Eftersom batchtranskribering är asynkron pollar applikationen jobbstatusändpunkten med jämna mellanrum och väntar på tillståndet `Succeeded` innan den går vidare.
3. **NLP**: den råa transkripttexten skickas till Azure AI Language för nyckelfrasextraktion, NER, sentimentanalys och språkdetektering.
4. **Översättning** (valfritt): om ett målspråk anges skickas transkriptet till Azure Translator, och NLP-analysen körs på nytt på den översatta texten.
5. **Utdata**: resultaten skrivs till det valda utdataformatet (JSON, TXT eller SQLite) och renderas i CherryPy-webbgränssnittet.

De enda körtidsberoendena utanför Pythons standardbibliotek är `azure-cognitiveservices-speech`, `azure-ai-textanalytics`, `azure-ai-translation-text` och `cherrypy`. Alla Azure-autentiseringsuppgifter läses från miljövariabler.

## Azure Cognitive Services: motorn för batchtranskribering

Azure Speech-tjänstens API för batchtranskribering (`/speechtotext/v3.0/transcriptions`) tar emot en referens till en ljudfil i Azure Blob Storage samt en JSON-kropp med konfiguration. Audio Analyser laddar upp den lokala filen till Blob Storage med en försignerad SAS-URL och skickar därefter in transkriberingsjobbet.

En minimal nyttolast för jobbinlämning:

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

Svarsarrayen `recognizedPhrases` innehåller ett objekt per igenkänd yttrande. Varje post innehåller:

- `nBest[0].confidence`: flyttal mellan 0 och 1
- `nBest[0].lexical`: råa ord som de uttalades
- `nBest[0].itn`: invers textnormaliserad form (tal, datum och valutor expanderade)
- `nBest[0].display`: formaterad för läsning, med interpunktion
- `speaker`: heltals-ID för talare när diarisering är aktiverad

**Custom Speech**-finjustering finns tillgänglig för domänspecifikt ordförråd. Genom att ladda upp ett uttalslexikon eller en anpassningskorpus (en uppsättning textmeningar som är representativa för domänen) justeras språkmodellen, vilket kan minska WER väsentligt på specialiserat innehåll som finansiella termer eller medicinsk fackjargong.

## Naturlig språkbehandling med Azure AI Language

Efter transkriberingen skickar Audio Analyser transkriptet i display-form till Azure AI Language via Python-SDK:n `azure-ai-textanalytics`:

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

`show_opinion_mining=True` aktiverar sentiment på aspektnivå: API:et returnerar inte bara polaritet på dokumentnivå utan specifika par av mål och bedömning (till exempel mål="ljudkvalitet", bedömning="dålig"). Detta gör utdata användbar för att identifiera konkreta problem vid analys av kundtjänstsamtal.

Igenkänning av namngivna entiteter klassificerar textavsnitt som en av: `Person`, `Organization`, `Location`, `Event`, `Product`, `DateTime`, `Quantity`, `IP`, `URL`, `Email`, `PersonType`, `Skill`, `Address`, `PhoneNumber`.

## Flerspråkigt stöd via Azure Translator

Azure Translator anropas efter språkdetekteringen när användaren begär ett målspråk. Tjänsten stöder 135 språk och dialekter med neural maskinöversättning (NMT). Audio Analyser använder REST-ändpunkten `/translate` med `autodetect` som `from`-parameter, så ingen specifikation av källspråk krävs:

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

Efter översättningen kan Audio Analyser valfritt köra Text Analytics-NLP-passet på nytt på den översatta texten, så att nyckelfraser och sentimentutdata finns tillgängliga på både käll- och målspråket.

Valet av utdataformat (JSON, TXT, SQLite) görs vid uppstart. SQLite-utdata lagrar varje analyssession som en rad med kolumner för jobb-ID, tidsstämpel, källspråk, transkript, översatt transkript, sentimentpoäng och nyckelfraser som en JSON-blob, vilket möjliggör SQL-frågor över sessioner.

## CherryPy som webblager

CherryPy mappar URL-rutter till Python-metoder med klassbaserade kontroller. Audio Analyser använder tre rutter:

| Rutt | Metod | Beskrivning |
|---|---|---|
| `GET /` | `index()` | Renderar uppladdningsformuläret |
| `POST /analyse` | `analyse()` | Tar emot multipart-uppladdning, startar pipelinen, returnerar jobb-ID |
| `GET /results/<job_id>` | `results()` | Pollar jobbstatus; renderar resultatsidan när jobbet är klart |

Den minimala konfigurationen håller serverns fotavtryck litet:

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

Sessionstillståndet håller aktuellt jobb-ID, valt utdataformat och målspråk för översättning. CherryPys inbyggda sessionslagring är filbaserad som standard och kräver inget externt cachelager.

## Vanliga frågor

**Vilka ljudformat och filstorlekar accepterar Audio Analyser?**
Azure Batch Transcription API stöder WAV-, MP3-, OGG- och FLAC-filer på upp till 2,5 timmar. Filer utanför detta intervall bör delas upp före uppladdning. Stereofiler accepteras; konvertering till mono krävs inte.

**Hur fungerar talardiarisering?**
Att sätta `diarizationEnabled: true` i batchtranskriberingsbegäran aktiverar Azures modell för talarseparation. Varje `recognizedPhrase` i svaret innehåller ett heltalsfält `speaker`. Modellen identifierar talare utifrån akustiska egenskaper och tilldelar konsekventa ID:n inom en session, men identifierar inte vilka talarna är utan ett separat registreringssteg med röstprofil.

**Behålls ljudfiler efter transkriberingen?**
Ljudfiler laddas upp till Azure Blob Storage med en kortlivad SAS-URL och raderas från den temporära lokala katalogen när uppladdningen är klar. Kvarhållning av blobbar i Azure Blob Storage beror på containerns livscykelpolicy; som standard sätter Audio Analyser ingen uttrycklig raderingspolicy, så att konfigurera en kort TTL-regel (till exempel radera blobbar äldre än 1 dag) i Azure-portalen rekommenderas för produktionsdriftsättningar.

**Kan NLP-analysen köras utan översättning?**
Ja. Översättning är ett valfritt pipelinesteg som styrs av CLI-flaggan `--target-lang` eller rullgardinsmenyn för målspråk i webbgränssnittet. När inget målspråk är valt kör pipelinen endast tal-till-text och Text Analytics.

## Referenser

1. Microsoft. *Batch transcription overview: Azure AI services*. Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/speech-service/batch-transcription>
2. Xiong, W. m.fl. "Achieving Human Parity in Conversational Speech Recognition." *Microsoft Research Technical Report*, 2016; uppdaterad 2021. <https://arxiv.org/abs/1610.05256>
3. Microsoft. *What is Azure AI Language?* Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/language-service/overview>
4. Microsoft. *Azure AI Translator: Supported languages*. Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/translator/language-support>

[00]: https://audioanalyser.co/ "Audio Analyser: Azure-baserat verktyg för talanalys"
