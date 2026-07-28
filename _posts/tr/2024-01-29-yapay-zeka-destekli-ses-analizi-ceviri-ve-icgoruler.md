---
title: "Audio Analyser: Azure Konuşma, NLP ve Çeviri Hattı"
subtitle: "Azure tabanlı bir konuşma analizi aracının mimarisi ve hattı"
description: "Audio Analyser; ses kayıtlarını duygu puanları, anahtar sözcük çıkarımı ve çok dilli çevirilerle aranabilir dökümlere dönüştürmek için Azure Cognitive Services konuşmadan metne sinir modellerini, Text Analytics NLP'yi ve CherryPy'yi kullanır."
date: "Jan 29, 2024"
language: "tr-TR"
locale: "tr_TR"
banner: "https://cloudcdn.pro/stocks/images/modern-corporate-office-with-technological-displays.webp"
banner_alt: "Sade, modern bir kurumsal ofis"
keywords: "Azure Cognitive Services, konuşmadan metne, sinirsel akustik model, Azure Text Analytics, doğal dil işleme, duygu analizi, CherryPy, toplu döküm API'si, çok dilli ASR, Azure Translator, ses dökümü, Python ses işleme"
---


> **Yönetici Özeti / Önemli Çıkarımlar**
>
> - **Azure Batch Transcription API**, 2,5 saate kadar ses dosyalarını (WAV/MP3/OGG/FLAC) kabul eder, bunları eşzamansız olarak işler ve akış bağlantısı gerektirmeden ifade başına `nBest` adaylarını, güven puanlarını, ters metin normalleştirmeli (ITN) çıktıyı ve isteğe bağlı konuşmacı ayrımını içeren bir `recognizedPhrases` JSON dizisi döndürür (Microsoft Azure, 2024).
> - **Microsoft'un sinirsel akustik modelleri**, Switchboard konuşma karşılaştırma kümesinde önceki gizli Markov modeli (HMM) temellerine kıyasla sözcük hata oranını yaklaşık %50 azaltmış ve o veri kümesinde ~%5,1 WER ile profesyonel insan yazıcılarla eşitliğe ulaşmıştır (Xiong ve diğerleri, Microsoft Research, 2016/2021 güncellemesi).
> - **Azure Text Analytics** (artık Azure AI Language'in parçası), döküm metnini anahtar ifade çıkarımı, adlandırılmış varlık tanıma (NER), görüş madenciliğiyle duygu analizi ve dil algılama aşamalarından geçirir; tümü Python SDK ile tek bir `analyze_sentiment` veya `begin_analyze_actions` çağrısında gerçekleşir.
> - **CherryPy**, web katmanını sağlar: URL yönlendirmesi, çok parçalı yükleme işleme, oturum yönetimi ve düzenleme yükü olmadan tek bir düşük maliyetli VM üzerinde çalışabilen minimal bir Python sürecinde Jinja2 şablon işleme.
> - **Azure Translator NMT**, kaynak dili otomatik algılar ve dökümleri 135 hedef dilden herhangi birine çevirir; böylece aynı hat çalıştırması içinde hem özgün hem de çevrilmiş metin üzerinde alt aşama NLP analizine olanak tanır.

[**Audio Analyser ⧉**][00], üç Azure Cognitive Services hizmetini tek bir iş akışında birleştiren açık kaynaklı bir Python uygulamasıdır: konuşmadan metne için Batch Transcription, NLP için Azure AI Language (Text Analytics) ve çok dilli çıktı için Azure Translator. Web arayüzü CherryPy tarafından sunulur ve sonuçlar JSON, düz metin veya yerel bir SQLite veritabanında saklanabilir.

Bu makale, her hat aşamasının teknik mimarisini, Azure API sözleşmelerini ve CherryPy katmanında yapılan tasarım seçimlerini açıklar.

## Audio Analyser Nasıl Çalışır: Mimariye Genel Bakış

Hattın beş ayrı aşaması vardır:

1. **Yükleme** — kullanıcı, CherryPy web arayüzü üzerinden bir ses dosyası gönderir. CherryPy dosyayı geçici bir dizinde saklar ve bir iş kimliği döndürür.
2. **Döküm** — Audio Analyser dosyayı Azure Batch Transcription REST API'sine gönderir. Toplu döküm eşzamansız olduğundan, uygulama iş durumu uç noktasını belirli aralıklarla yoklar ve devam etmeden önce `Succeeded` durumunu bekler.
3. **NLP** — ham döküm metni, anahtar ifade çıkarımı, NER, duygu analizi ve dil algılama için Azure AI Language'e iletilir.
4. **Çeviri** (isteğe bağlı) — bir hedef dil belirtilmişse döküm Azure Translator'a gönderilir ve NLP analizi çevrilmiş metin üzerinde yeniden çalıştırılır.
5. **Çıktı** — sonuçlar seçilen çıktı biçimine (JSON, TXT veya SQLite) yazılır ve CherryPy web kullanıcı arayüzünde işlenir.

Python standart kütüphanesi dışındaki tek çalışma zamanı bağımlılıkları `azure-cognitiveservices-speech`, `azure-ai-textanalytics`, `azure-ai-translation-text` ve `cherrypy`'dir. Tüm Azure kimlik bilgileri ortam değişkenlerinden okunur.

## Azure Cognitive Services: Toplu Döküm Motoru

Azure Konuşma hizmeti toplu döküm API'si (`/speechtotext/v3.0/transcriptions`), Azure Blob Storage'daki bir ses dosyasına yapılan bir başvuruyu ve bir yapılandırma JSON gövdesini kabul eder. Audio Analyser, yerel dosyayı önceden imzalanmış bir SAS URL'si kullanarak Blob Storage'a yükler, ardından döküm işini gönderir.

Minimal bir iş gönderim yükü:

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

`recognizedPhrases` yanıt dizisi, tanınan her söylem için bir nesne içerir. Her giriş şunları içerir:

- `nBest[0].confidence`: 0 ile 1 arasında ondalık değer
- `nBest[0].lexical`: söylendiği haliyle ham sözcükler
- `nBest[0].itn`: ters metin normalleştirmeli biçim (sayılar, tarihler, para birimleri açılmış)
- `nBest[0].display`: noktalama işaretleriyle, okumaya uygun biçimlendirilmiş
- `speaker`: konuşmacı ayrımı etkinleştirildiğinde tam sayı konuşmacı kimliği

**Custom Speech** ince ayarı, alana özgü sözcük dağarcığı için kullanılabilir. Bir telaffuz sözlüğünün veya uyarlama derleminin (alanı temsil eden bir dizi metin cümlesi) yüklenmesi, dil modelini ayarlar ve finansal terimler ya da tıbbi jargon gibi özel içeriklerde WER'i önemli ölçüde azaltabilir.

## Azure AI Language ile Doğal Dil İşleme

Dökümden sonra Audio Analyser, görüntüleme biçimindeki dökümü `azure-ai-textanalytics` Python SDK'sı aracılığıyla Azure AI Language'e gönderir:

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

`show_opinion_mining=True`, yön düzeyinde duygu analizini etkinleştirir: API yalnızca belge düzeyindeki kutupluluğu değil, belirli hedef ve değerlendirme çiftlerini de döndürür (ör. hedef="ses kalitesi", değerlendirme="kötü"). Bu, müşteri hizmetleri çağrı analizinde somut sorunları belirlemek için çıktıyı yararlı kılar.

Adlandırılmış varlık tanıma, aralıkları şunlardan biri olarak sınıflandırır: `Person`, `Organization`, `Location`, `Event`, `Product`, `DateTime`, `Quantity`, `IP`, `URL`, `Email`, `PersonType`, `Skill`, `Address`, `PhoneNumber`.

## Azure Translator ile Çok Dilli Destek

Azure Translator, kullanıcı bir hedef dil istediğinde dil algılamasından sonra çağrılır. Hizmet, sinirsel makine çevirisi (NMT) ile 135 dili ve lehçeyi destekler. Audio Analyser, `from` parametresi olarak `autodetect` ile `/translate` REST uç noktasını kullanır; böylece kaynak dil belirtmeye gerek kalmaz:

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

Çeviriden sonra Audio Analyser, isteğe bağlı olarak Text Analytics NLP geçişini çevrilmiş metin üzerinde yeniden çalıştırır; böylece anahtar ifade ve duygu çıktıları hem kaynak hem de hedef dilde kullanılabilir olur.

Çıktı biçimi seçimi (JSON, TXT, SQLite) başlangıçta ayarlanır. SQLite çıktısı, her analiz oturumunu; iş kimliği, zaman damgası, kaynak dil, döküm, çevrilmiş döküm, duygu puanları ve JSON blobu olarak anahtar ifadeler için sütunlar içeren bir satır olarak saklar; böylece oturumlar arası SQL sorgularına olanak tanır.

## Web Katmanı Olarak CherryPy

CherryPy, sınıf tabanlı denetleyiciler kullanarak URL yollarını Python yöntemlerine eşler. Audio Analyser üç yol kullanır:

| Yol | Yöntem | Açıklama |
|---|---|---|
| `GET /` | `index()` | Yükleme formunu işler |
| `POST /analyse` | `analyse()` | Çok parçalı yüklemeyi kabul eder, hattı tetikler, iş kimliği döndürür |
| `GET /results/<job_id>` | `results()` | İş durumunu yoklar; tamamlandığında sonuç sayfasını işler |

Minimal yapılandırma, sunucu ayak izini küçük tutar:

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

Oturum durumu; geçerli iş kimliğini, seçilen çıktı biçimini ve hedef çeviri dilini tutar. CherryPy'nin yerleşik oturum deposu varsayılan olarak dosya tabanlıdır ve harici bir önbellek katmanı gerektirmez.

## Sık Sorulan Sorular

**Audio Analyser hangi ses biçimlerini ve dosya boyutlarını kabul eder?**
Azure Batch Transcription API; WAV, MP3, OGG ve FLAC dosyalarını 2,5 saat uzunluğa kadar destekler. Bu aralığın dışındaki dosyalar yüklemeden önce bölünmelidir. Stereo dosyalar kabul edilir; mono dönüşümü gerekmez.

**Konuşmacı ayrımı nasıl çalışır?**
Toplu döküm isteğinde `diarizationEnabled: true` ayarlamak, Azure'un konuşmacı ayrımı modelini etkinleştirir. Yanıttaki her `recognizedPhrase`, bir `speaker` tam sayı alanı içerir. Model, konuşmacıları akustik özelliklerine göre tanımlar ve bir oturum içinde tutarlı kimlikler atar; ancak ayrı bir ses profili kaydı adımı olmadan konuşmacıların kim olduğunu belirlemez.

**Ses dosyaları dökümden sonra saklanır mı?**
Ses dosyaları, kısa ömürlü bir SAS URL'siyle Azure Blob Storage'a yüklenir ve yükleme tamamlandıktan sonra geçici yerel dizinden silinir. Azure Blob Storage'daki blobların saklanması, konteynerin yaşam döngüsü ilkesine bağlıdır; varsayılan olarak Audio Analyser açık bir silme ilkesi belirlemez; bu nedenle üretim dağıtımları için Azure portalında kısa bir TTL kuralı (ör. 1 günden eski blobları sil) yapılandırılması önerilir.

**NLP analizi çeviri olmadan çalıştırılabilir mi?**
Evet. Çeviri, `--target-lang` CLI bayrağı veya web kullanıcı arayüzündeki hedef dil açılır menüsüyle denetlenen isteğe bağlı bir hat aşamasıdır. Hiçbir hedef dil seçilmediğinde hat yalnızca konuşmadan metne ve Text Analytics çalıştırır.

## Kaynakça

1. Microsoft. *Batch transcription overview — Azure AI services*. Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/speech-service/batch-transcription>
2. Xiong, W. ve diğerleri. "Achieving Human Parity in Conversational Speech Recognition." *Microsoft Research Technical Report*, 2016; 2021'de güncellendi. <https://arxiv.org/abs/1610.05256>
3. Microsoft. *What is Azure AI Language?* Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/language-service/overview>
4. Microsoft. *Azure AI Translator — Supported languages*. Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/translator/language-support>

[00]: https://audioanalyser.co/ "Audio Analyser: Azure destekli konuşma analizi aracı"
