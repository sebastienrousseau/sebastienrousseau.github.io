---
title: "Audio Analyser: Azure beszéd-, NLP- és fordítási folyamat"
tags: "Azure, CherryPy, SpeechToText, NLP, SentimentAnalysis, BatchTranscription, AudioAnalyser, NeuralASR, TextAnalytics, Multilingual, ISO 20022, post-quantum cryptography, AI, open source, DORA, platform engineering, sovereign cloud, cloud native banking"
subtitle: "Egy Azure-alapú beszédelemző eszköz architektúrája és folyamata"
description: "Az Audio Analyser az Azure Cognitive Services beszéd-szöveg átírási neurális modelljeit, a Text Analytics NLP-jét és a CherryPy-t használja, hogy a hangfelvételeket kereshető átiratokká alakítsa hangulatpontszámokkal, kulcsszókinyeréssel és többnyelvű fordításokkal."
date: "Jan 29, 2024"
language: "hu"
locale: "hu_HU"
banner: "https://cloudcdn.pro/stocks/images/modern-corporate-office-with-technological-displays.webp"
banner_alt: "Minimalista, modern vállalati iroda"
keywords: "Azure Cognitive Services, beszéd-szöveg átírás, neurális akusztikai modell, Azure Text Analytics, természetes nyelvi feldolgozás, hangulatelemzés, CherryPy, kötegelt átírási API, többnyelvű ASR, Azure Translator, hangátírás, Python hangfeldolgozás"
---

> **Vezetői összefoglaló / Legfontosabb tanulságok**
>
> - Az **Azure Batch Transcription API** legfeljebb 2,5 órás hangfájlokat (WAV/MP3/OGG/FLAC) fogad el, aszinkron módon dolgozza fel őket, és egy `recognizedPhrases` JSON tömböt ad vissza, kifejezésenkénti `nBest` jelöltekkel, megbízhatósági pontszámokkal, fordított szövegnormalizált (ITN) kimenettel és opcionális beszélődiarizációval, streaming kapcsolat nélkül (Microsoft Azure, 2024).
> - A **Microsoft neurális akusztikai modelljei** a szóhibaarányt (WER) körülbelül 50%-kal csökkentették a korábbi rejtett Markov-modell (HMM) alapvonalakhoz képest a Switchboard társalgási teszten, elérve a professzionális emberi átírók szintjét ezen az adathalmazon, mintegy 5,1%-os WER mellett (Xiong et al., Microsoft Research, 2016/2021-es frissítés).
> - Az **Azure Text Analytics** (ma az Azure AI Language része) az átiratszöveget kulcskifejezés-kinyeréssel, névelem-felismeréssel (NER), véleménybányászattal kombinált hangulatelemzéssel és nyelvfelismeréssel dolgozza fel, mindezt egyetlen `analyze_sentiment` vagy `begin_analyze_actions` hívásban, a Python SDK segítségével.
> - A **CherryPy** biztosítja a webréteget: URL-útválasztást, multipart feltöltéskezelést, munkamenet-kezelést és Jinja2 sablonmegjelenítést egy minimális Python folyamatban, amely egyetlen olcsó virtuális gépen futtatható orkesztrációs többletköltség nélkül.
> - Az **Azure Translator NMT** automatikusan felismeri a forrásnyelvet, és az átiratokat 135 célnyelv bármelyikére lefordítja, lehetővé téve a downstream NLP-elemzést mind az eredeti, mind a lefordított szövegen ugyanazon a folyamatfutáson belül.

Az [**Audio Analyser ⧉**][00] egy nyílt forráskódú Python alkalmazás, amely három Azure Cognitive Services szolgáltatást kapcsol össze egyetlen munkafolyamatba: a Batch Transcriptiont a beszéd szöveggé alakításához, az Azure AI Language-et (Text Analytics) az NLP-hez, és az Azure Translatort a többnyelvű kimenethez. A webes felületet a CherryPy szolgálja ki, az eredmények pedig JSON, egyszerű szöveg vagy helyi SQLite adatbázis formátumban tárolhatók.

Ez a cikk az egyes folyamatszakaszok technikai architektúráját, az Azure API-szerződéseket és a CherryPy réteg tervezési döntéseit ismerteti.

## Hogyan működik az Audio Analyser: architektúra áttekintés

A folyamat öt különálló szakaszból áll:

1. **Feltöltés**: a felhasználó egy hangfájlt küld be a CherryPy webes felületén keresztül. A CherryPy egy ideiglenes könyvtárban tárolja a fájlt, és visszaad egy feladatazonosítót.
2. **Átírás**: az Audio Analyser beküldi a fájlt az Azure Batch Transcription REST API-nak. Mivel a kötegelt átírás aszinkron, az alkalmazás rendszeres időközönként lekérdezi a feladatállapot végpontot, és a folytatás előtt megvárja a `Succeeded` állapotot.
3. **NLP**: a nyers átirat szövege az Azure AI Language-be kerül kulcskifejezés-kinyerés, NER, hangulatelemzés és nyelvfelismerés céljából.
4. **Fordítás** (opcionális): ha meg van adva célnyelv, az átirat az Azure Translatorhoz kerül, és az NLP-elemzés újra lefut a lefordított szövegen.
5. **Kimenet**: az eredmények a kiválasztott kimeneti formátumba (JSON, TXT vagy SQLite) íródnak, és megjelennek a CherryPy webes felületén.

A Python szabványos könyvtárán kívüli egyetlen futásidejű függőség az `azure-cognitiveservices-speech`, az `azure-ai-textanalytics`, az `azure-ai-translation-text` és a `cherrypy`. Az összes Azure hitelesítő adat környezeti változókból kerül beolvasásra.

## Azure Cognitive Services: a kötegelt átírási motor

Az Azure Speech szolgáltatás kötegelt átírási API-ja (`/speechtotext/v3.0/transcriptions`) egy Azure Blob Storage-ban tárolt hangfájlra mutató hivatkozást és egy konfigurációs JSON törzset fogad el. Az Audio Analyser egy előre aláírt SAS URL segítségével feltölti a helyi fájlt a Blob Storage-ba, majd beküldi az átírási feladatot.

Egy minimális feladatbeküldési adatcsomag:

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

A válasz `recognizedPhrases` tömbje minden felismert megnyilatkozáshoz egy objektumot tartalmaz. Minden bejegyzés tartalmazza:

- `nBest[0].confidence`: lebegőpontos érték 0 és 1 között
- `nBest[0].lexical`: a nyers szavak úgy, ahogy elhangzottak
- `nBest[0].itn`: fordított szövegnormalizált forma (számok, dátumok, pénznemek kifejtve)
- `nBest[0].display`: olvasásra formázva, központozással
- `speaker`: egész számú beszélőazonosító, ha a diarizáció engedélyezve van

A **Custom Speech** finomhangolás elérhető a szakterület-specifikus szókincshez. Egy kiejtési lexikon vagy adaptációs korpusz (a szakterületre jellemző szöveges mondatok halmaza) feltöltése módosítja a nyelvi modellt, és jelentősen csökkentheti a WER-t a szakosított tartalmakon, például pénzügyi kifejezéseknél vagy orvosi szakzsargonnál.

## Természetes nyelvi feldolgozás az Azure AI Language segítségével

Az átírás után az Audio Analyser a megjelenítési formájú átiratot az `azure-ai-textanalytics` Python SDK-n keresztül küldi el az Azure AI Language-nek:

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

A `show_opinion_mining=True` bekapcsolja az aspektusszintű hangulatelemzést: az API nem csak a dokumentumszintű polaritást adja vissza, hanem konkrét cél-értékelés párokat is (például cél="hangminőség", értékelés="gyenge"). Ez az ügyfélszolgálati hívások elemzésében hasznossá teszi a kimenetet a konkrét problémák azonosításához.

A névelem-felismerés a szövegrészeket a következők egyikébe sorolja: `Person`, `Organization`, `Location`, `Event`, `Product`, `DateTime`, `Quantity`, `IP`, `URL`, `Email`, `PersonType`, `Skill`, `Address`, `PhoneNumber`.

## Többnyelvű támogatás az Azure Translator segítségével

Az Azure Translator a nyelvfelismerés után hívódik meg, amikor a felhasználó célnyelvet kér. A szolgáltatás 135 nyelvet és dialektust támogat neurális gépi fordítással (NMT). Az Audio Analyser a `/translate` REST végpontot használja `autodetect` értékkel a `from` paraméterben, így nincs szükség a forrásnyelv megadására:

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

A fordítás után az Audio Analyser opcionálisan újra lefuttatja a Text Analytics NLP-menetet a lefordított szövegen, így a kulcskifejezés- és hangulatkimenetek a forrás- és a célnyelven egyaránt elérhetők.

A kimeneti formátum kiválasztása (JSON, TXT, SQLite) indításkor történik. Az SQLite kimenet minden elemzési munkamenetet egy sorként tárol, amelynek oszlopai a feladatazonosító, az időbélyeg, a forrásnyelv, az átirat, a lefordított átirat, a hangulatpontszámok és a kulcskifejezések JSON blobként, ami lehetővé teszi a munkameneteken átívelő SQL lekérdezéseket.

## A CherryPy mint webréteg

A CherryPy osztályalapú vezérlők segítségével képezi le az URL-útvonalakat Python metódusokra. Az Audio Analyser három útvonalat használ:

| Útvonal | Metódus | Leírás |
|---|---|---|
| `GET /` | `index()` | Megjeleníti a feltöltési űrlapot |
| `POST /analyse` | `analyse()` | Fogadja a multipart feltöltést, elindítja a folyamatot, visszaadja a feladatazonosítót |
| `GET /results/<job_id>` | `results()` | Lekérdezi a feladat állapotát; befejezéskor megjeleníti az eredményoldalt |

A minimális konfiguráció kicsiben tartja a szerver erőforrásigényét:

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

A munkamenet-állapot tárolja az aktuális feladatazonosítót, a kiválasztott kimeneti formátumot és a célfordítási nyelvet. A CherryPy beépített munkamenet-tárolása alapértelmezés szerint fájlalapú, így nincs szükség külső gyorsítótárrétegre.

## Gyakran ismételt kérdések

**Milyen hangformátumokat és fájlméreteket fogad el az Audio Analyser?**
Az Azure Batch Transcription API a WAV, MP3, OGG és FLAC fájlokat támogatja legfeljebb 2,5 óra hosszúságig. Az ezt meghaladó fájlokat feltöltés előtt fel kell darabolni. A sztereó fájlok elfogadottak; monóvá alakításra nincs szükség.

**Hogyan működik a beszélődiarizáció?**
A `diarizationEnabled: true` beállítása a kötegelt átírási kérésben aktiválja az Azure beszélőelkülönítő modelljét. A válaszban minden `recognizedPhrase` tartalmaz egy `speaker` egész számú mezőt. A modell akusztikai jellemzők alapján azonosítja a beszélőket, és egy munkameneten belül konzisztens azonosítókat rendel hozzájuk, de külön hangprofil-regisztrációs lépés nélkül nem állapítja meg, hogy kik a beszélők.

**Megőrződnek a hangfájlok az átírás után?**
A hangfájlok egy rövid élettartamú SAS URL-lel töltődnek fel az Azure Blob Storage-ba, és a feltöltés befejeztével törlődnek az ideiglenes helyi könyvtárból. A blobok megőrzése az Azure Blob Storage-ban a tároló életciklus-házirendjétől függ; alapértelmezés szerint az Audio Analyser nem állít be explicit törlési házirendet, ezért éles környezetben ajánlott egy rövid TTL-szabály (például az 1 napnál régebbi blobok törlése) beállítása az Azure portálon.

**Futtatható az NLP-elemzés fordítás nélkül?**
Igen. A fordítás egy opcionális folyamatszakasz, amelyet a `--target-lang` CLI-kapcsoló vagy a webes felület célnyelv-legördülő menüje vezérel. Ha nincs kiválasztva célnyelv, a folyamat csak a beszéd szöveggé alakítását és a Text Analyticset futtatja.

## Hivatkozások

1. Microsoft. *Batch transcription overview: Azure AI services*. Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/speech-service/batch-transcription>
2. Xiong, W. et al. "Achieving Human Parity in Conversational Speech Recognition." *Microsoft Research Technical Report*, 2016; updated 2021. <https://arxiv.org/abs/1610.05256>
3. Microsoft. *What is Azure AI Language?* Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/language-service/overview>
4. Microsoft. *Azure AI Translator: Supported languages*. Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/translator/language-support>

[00]: https://audioanalyser.co/ "Audio Analyser: Azure-alapú beszédelemző eszköz"
