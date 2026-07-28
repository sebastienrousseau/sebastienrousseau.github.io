---
title: "Audio Analyser: Azure Speech, NLP a pipeline pro překlad"
subtitle: "Architektura a pipeline nástroje pro řečovou analytiku postaveného na Azure"
description: "Audio Analyser využívá neuronové modely speech-to-text z Azure Cognitive Services, NLP z Text Analytics a CherryPy k převodu zvukových nahrávek na prohledávatelné přepisy se skóre sentimentu, extrakcí klíčových slov a vícejazyčnými překlady."
date: "January 29, 2024"
language: "cs-CZ"
locale: "cs_CZ"
banner: "https://cloudcdn.pro/stocks/images/modern-corporate-office-with-technological-displays.webp"
banner_alt: "Minimalistická, moderní firemní kancelář"
keywords: "Azure Cognitive Services, speech-to-text, neuronový akustický model, Azure Text Analytics, zpracování přirozeného jazyka, analýza sentimentu, CherryPy, batch transcription API, vícejazyčné ASR, Azure Translator, přepis zvuku, zpracování zvuku v Pythonu"
---


> **Shrnutí pro vedení / Klíčové body**
>
> - **Azure Batch Transcription API** přijímá zvukové soubory do délky 2,5 hodiny (WAV/MP3/OGG/FLAC), zpracovává je asynchronně a vrací pole JSON `recognizedPhrases` s kandidáty `nBest` pro každou frázi, se skóre spolehlivosti, s výstupem po inverzní textové normalizaci (ITN) a s volitelnou diarizací mluvčích. Streamovací spojení není potřeba (Microsoft Azure, 2024).
> - **Neuronové akustické modely společnosti Microsoft** snížily chybovost slov (WER) přibližně o 50 % oproti dřívějším základním modelům se skrytými Markovovými řetězci (HMM) na konverzačním benchmarku Switchboard a na této datové sadě dosáhly úrovně profesionálních lidských přepisovatelů při WER přibližně 5,1 % (Xiong et al., Microsoft Research, aktualizace 2016/2021).
> - **Azure Text Analytics** (nyní součást Azure AI Language) zpracovává text přepisu pomocí extrakce klíčových frází, rozpoznávání pojmenovaných entit (NER), analýzy sentimentu s dolováním názorů a detekce jazyka, a to v jediném volání `analyze_sentiment` nebo `begin_analyze_actions` prostřednictvím Python SDK.
> - **CherryPy** poskytuje webovou vrstvu: směrování URL, zpracování vícedílného nahrávání, správu relací a vykreslování šablon Jinja2 v minimálním procesu Pythonu, který lze provozovat na jediném levném virtuálním stroji bez režie orchestrace.
> - **Azure Translator NMT** automaticky rozpozná zdrojový jazyk a přeloží přepisy do kteréhokoli ze 135 cílových jazyků, což umožňuje navazující NLP analýzu původního i přeloženého textu v rámci jednoho běhu pipeline.

[**Audio Analyser ⧉**][00] je open-source aplikace v jazyce Python, která propojuje tři služby Azure Cognitive Services do jednoho pracovního postupu: Batch Transcription pro speech-to-text, Azure AI Language (Text Analytics) pro NLP a Azure Translator pro vícejazyčný výstup. Webové rozhraní obsluhuje CherryPy a výsledky lze uložit do JSON, prostého textu nebo lokální databáze SQLite.

Tento článek popisuje technickou architekturu jednotlivých fází pipeline, kontrakty API služeb Azure a návrhová rozhodnutí učiněná ve vrstvě CherryPy.

## Jak Audio Analyser funguje: přehled architektury

Pipeline má pět samostatných fází:

1. **Nahrání.** Uživatel odešle zvukový soubor přes webové rozhraní CherryPy. CherryPy uloží soubor do dočasného adresáře a vrátí ID úlohy.
2. **Přepis.** Audio Analyser odešle soubor do REST API Azure Batch Transcription. Protože dávkový přepis probíhá asynchronně, aplikace v intervalech dotazuje koncový bod se stavem úlohy a před pokračováním čeká na stav `Succeeded`.
3. **NLP.** Nezpracovaný text přepisu se předá do Azure AI Language pro extrakci klíčových frází, NER, analýzu sentimentu a detekci jazyka.
4. **Překlad** (volitelně). Je-li zadán cílový jazyk, přepis se odešle do Azure Translator a NLP analýza se znovu spustí nad přeloženým textem.
5. **Výstup.** Výsledky se zapíší do zvoleného výstupního formátu (JSON, TXT nebo SQLite) a vykreslí se ve webovém uživatelském rozhraní CherryPy.

Jediné běhové závislosti mimo standardní knihovnu Pythonu jsou `azure-cognitiveservices-speech`, `azure-ai-textanalytics`, `azure-ai-translation-text` a `cherrypy`. Veškeré přihlašovací údaje Azure se čtou z proměnných prostředí.

## Azure Cognitive Services: engine pro dávkový přepis

API pro dávkový přepis služby Azure Speech (`/speechtotext/v3.0/transcriptions`) přijímá odkaz na zvukový soubor v Azure Blob Storage a konfigurační tělo JSON. Audio Analyser nahraje lokální soubor do Blob Storage pomocí předem podepsané SAS URL a poté odešle úlohu přepisu.

Minimální payload pro odeslání úlohy:

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

Pole `recognizedPhrases` v odpovědi obsahuje jeden objekt na každou rozpoznanou výpověď. Každý záznam obsahuje:

- `nBest[0].confidence`: desetinné číslo mezi 0 a 1
- `nBest[0].lexical`: nezpracovaná slova tak, jak byla vyřčena
- `nBest[0].itn`: forma po inverzní textové normalizaci (čísla, data a měny v rozepsané podobě)
- `nBest[0].display`: naformátováno pro čtení, s interpunkcí
- `speaker`: celočíselné ID mluvčího, je-li povolena diarizace

Pro doménově specifickou slovní zásobu je k dispozici doladění **Custom Speech**. Nahrání výslovnostního lexikonu nebo adaptačního korpusu (sady textových vět reprezentativních pro danou doménu) upraví jazykový model a může výrazně snížit WER u specializovaného obsahu, jako jsou finanční termíny nebo lékařský žargon.

## Zpracování přirozeného jazyka pomocí Azure AI Language

Po přepisu odešle Audio Analyser přepis ve formě pro zobrazení do Azure AI Language prostřednictvím Python SDK `azure-ai-textanalytics`:

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

`show_opinion_mining=True` zapíná sentiment na úrovni aspektů: API nevrací pouze polaritu na úrovni dokumentu, ale konkrétní dvojice cíl–hodnocení (např. target="audio quality", assessment="poor"). Díky tomu je výstup užitečný pro identifikaci konkrétních problémů při analýze hovorů zákaznického servisu.

Rozpoznávání pojmenovaných entit klasifikuje úseky textu jako jednu z hodnot: `Person`, `Organization`, `Location`, `Event`, `Product`, `DateTime`, `Quantity`, `IP`, `URL`, `Email`, `PersonType`, `Skill`, `Address`, `PhoneNumber`.

## Vícejazyčná podpora pomocí Azure Translator

Azure Translator se volá po detekci jazyka, když uživatel požádá o cílový jazyk. Služba podporuje 135 jazyků a dialektů s neuronovým strojovým překladem (NMT). Audio Analyser používá REST koncový bod `/translate` s parametrem `from` nastaveným na `autodetect`, takže není nutné zadávat zdrojový jazyk:

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

Po překladu Audio Analyser volitelně znovu provede NLP průchod Text Analytics nad přeloženým textem, takže výstupy klíčových frází a sentimentu jsou dostupné ve zdrojovém i cílovém jazyce.

Volba výstupního formátu (JSON, TXT, SQLite) se nastavuje při spuštění. Výstup SQLite ukládá každou analytickou relaci jako řádek se sloupci pro ID úlohy, časové razítko, zdrojový jazyk, přepis, přeložený přepis, skóre sentimentu a klíčové fráze ve formě JSON blobu, což umožňuje dotazy SQL napříč relacemi.

## CherryPy jako webová vrstva

CherryPy mapuje cesty URL na metody Pythonu pomocí controllerů založených na třídách. Audio Analyser používá tři cesty:

| Cesta | Metoda | Popis |
|---|---|---|
| `GET /` | `index()` | Vykreslí formulář pro nahrání |
| `POST /analyse` | `analyse()` | Přijme vícedílné nahrání, spustí pipeline, vrátí ID úlohy |
| `GET /results/<job_id>` | `results()` | Dotazuje stav úlohy; po dokončení vykreslí stránku s výsledky |

Minimální konfigurace udržuje stopu serveru malou:

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

Stav relace uchovává aktuální ID úlohy, zvolený výstupní formát a cílový jazyk překladu. Vestavěné úložiště relací CherryPy je ve výchozím nastavení souborové a nevyžaduje žádnou externí vrstvu cache.

## Často kladené otázky

**Jaké formáty a velikosti zvukových souborů Audio Analyser přijímá?**
Azure Batch Transcription API podporuje soubory WAV, MP3, OGG a FLAC do délky 2,5 hodiny. Soubory mimo tento rozsah je před nahráním třeba rozdělit. Stereo soubory jsou přijímány; převod na mono není nutný.

**Jak funguje diarizace mluvčích?**
Nastavení `diarizationEnabled: true` v požadavku na dávkový přepis aktivuje model Azure pro oddělení mluvčích. Každá `recognizedPhrase` v odpovědi obsahuje celočíselné pole `speaker`. Model rozlišuje mluvčí podle akustických charakteristik a přiděluje jim v rámci relace konzistentní ID, ale bez samostatného kroku registrace hlasového profilu neurčuje, kdo mluvčí jsou.

**Uchovávají se zvukové soubory po přepisu?**
Zvukové soubory se nahrávají do Azure Blob Storage pomocí krátkodobě platné SAS URL a po dokončení nahrání se odstraní z dočasného lokálního adresáře. Uchovávání blobů v Azure Blob Storage závisí na zásadě životního cyklu kontejneru; ve výchozím nastavení Audio Analyser nenastavuje explicitní zásadu mazání, proto se pro produkční nasazení doporučuje v Azure portálu nakonfigurovat pravidlo s krátkým TTL (např. mazat bloby starší než 1 den).

**Lze NLP analýzu spustit bez překladu?**
Ano. Překlad je volitelná fáze pipeline řízená přepínačem CLI `--target-lang` nebo rozbalovací nabídkou cílového jazyka ve webovém rozhraní. Není-li zvolen žádný cílový jazyk, pipeline provede pouze speech-to-text a Text Analytics.

## Reference

1. Microsoft. *Batch transcription overview — Azure AI services*. Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/speech-service/batch-transcription>
2. Xiong, W. et al. "Achieving Human Parity in Conversational Speech Recognition." *Microsoft Research Technical Report*, 2016; updated 2021. <https://arxiv.org/abs/1610.05256>
3. Microsoft. *What is Azure AI Language?* Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/language-service/overview>
4. Microsoft. *Azure AI Translator — Supported languages*. Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/translator/language-support>

[00]: https://audioanalyser.co/ "Audio Analyser: nástroj pro řečovou analytiku postavený na Azure"
