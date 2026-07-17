---
title: "Audio Analyser: خط لوله‌ی گفتار، پردازش زبان طبیعی و ترجمه‌ی Azure"
tags: "Azure, CherryPy, SpeechToText, NLP, SentimentAnalysis, BatchTranscription, AudioAnalyser, NeuralASR, TextAnalytics, Multilingual, ISO 20022, post-quantum cryptography, AI, open source, DORA, platform engineering, sovereign cloud, cloud native banking"
subtitle: "معماری و خط لوله‌ی یک ابزار تحلیل گفتار مبتنی بر Azure"
description: "Audio Analyser با استفاده از مدل‌های عصبی گفتار به متنِ Azure Cognitive Services، پردازش زبان طبیعیِ Text Analytics و CherryPy، ضبط‌های صوتی را به رونوشت‌های قابل‌جستجو همراه با امتیازهای احساسات، استخراج کلیدواژه و ترجمه‌های چندزبانه تبدیل می‌کند."
date: "Jan 29, 2024"
language: "fa"
locale: "fa_IR"
banner: "https://cloudcdn.pro/stocks/images/modern-corporate-office-with-technological-displays.webp"
banner_alt: "یک دفتر کار شرکتی مدرن و مینیمالیستی"
keywords: "Azure Cognitive Services، گفتار به متن، مدل صوتی عصبی، Azure Text Analytics، پردازش زبان طبیعی، تحلیل احساسات، CherryPy، API رونویسی دسته‌ای، ASR چندزبانه، Azure Translator، رونویسی صوتی، پردازش صوت با Python"
---

> **خلاصه‌ی اجرایی / نکات کلیدی**
>
> - **API رونویسی دسته‌ای Azure** فایل‌های صوتی تا ۲٫۵ ساعت (WAV/MP3/OGG/FLAC) را می‌پذیرد، آن‌ها را به‌صورت ناهمگام پردازش می‌کند و یک آرایه‌ی JSON با نام `recognizedPhrases` بازمی‌گرداند که شامل نامزدهای `nBest` برای هر عبارت، امتیازهای اطمینان، خروجی نرمال‌سازی‌شده‌ی معکوسِ متن (ITN) و تفکیک گوینده‌ی اختیاری است — بدون نیاز به اتصال جریانی (Microsoft Azure، ۲۰۲۴).
> - **مدل‌های صوتی عصبی مایکروسافت** نرخ خطای واژه را روی معیار مکالمه‌ای Switchboard تقریباً ۵۰٪ نسبت به خط‌مبناهای پیشینِ مدل پنهان مارکوف (HMM) کاهش دادند و روی آن مجموعه‌داده با نرخ خطای واژه‌ی حدود ۵٫۱٪ به برابری با رونویس‌نویسان حرفه‌ای انسانی رسیدند (Xiong و همکاران، Microsoft Research، ۲۰۱۶/به‌روزرسانی ۲۰۲۱).
> - **Azure Text Analytics** (اکنون بخشی از Azure AI Language) متن رونوشت را از طریق استخراج عبارت کلیدی، شناسایی موجودیت نام‌دار (NER)، تحلیل احساسات همراه با کاوش نظر، و تشخیص زبان پردازش می‌کند — همه در یک فراخوانی واحد `analyze_sentiment` یا `begin_analyze_actions` با استفاده از SDK پایتون.
> - **CherryPy** لایه‌ی وب را فراهم می‌کند: مسیریابی URL، مدیریت آپلود چندبخشی، مدیریت نشست و رندر قالب Jinja2 در یک فرآیند حداقلی پایتون که می‌تواند روی یک ماشین مجازی کم‌هزینه‌ی واحد و بدون سربارِ ارکستراسیون اجرا شود.
> - **NMT مترجم Azure** زبان مبدأ را به‌طور خودکار تشخیص می‌دهد و رونوشت‌ها را به هر یک از ۱۳۵ زبان مقصد ترجمه می‌کند و امکان تحلیل پردازش زبان طبیعیِ پایین‌دستی را روی هر دو متن اصلی و ترجمه‌شده در همان اجرای خط لوله فراهم می‌سازد.

[**Audio Analyser ⧉**][00] یک برنامه‌ی متن‌بازِ Python است که سه سرویس Azure Cognitive Services را در یک گردش‌کار واحد به هم متصل می‌کند: رونویسی دسته‌ای برای گفتار به متن، Azure AI Language (Text Analytics) برای پردازش زبان طبیعی، و Azure Translator برای خروجی چندزبانه. رابط وب توسط CherryPy ارائه می‌شود و نتایج را می‌توان در JSON، متن ساده یا یک پایگاه‌داده‌ی محلی SQLite ذخیره کرد.

این مقاله معماری فنی هر مرحله از خط لوله، قراردادهای API آژور، و انتخاب‌های طراحی انجام‌شده در لایه‌ی CherryPy را شرح می‌دهد.

## Audio Analyser چگونه کار می‌کند: نمای کلی معماری

این خط لوله پنج مرحله‌ی مجزا دارد:

1. **آپلود** — کاربر یک فایل صوتی را از طریق رابط وب CherryPy ارسال می‌کند. CherryPy فایل را در یک پوشه‌ی موقت ذخیره می‌کند و یک شناسه‌ی کار (job ID) بازمی‌گرداند.
2. **رونویسی** — Audio Analyser فایل را به REST API رونویسی دسته‌ای Azure ارسال می‌کند. از آنجا که رونویسی دسته‌ای ناهمگام است، برنامه در فواصل زمانی نقطه‌ی پایانیِ وضعیت کار را نظرسنجی (poll) می‌کند و پیش از ادامه، منتظر وضعیت `Succeeded` می‌ماند.
3. **پردازش زبان طبیعی** — متن خام رونوشت برای استخراج عبارت کلیدی، NER، تحلیل احساسات و تشخیص زبان به Azure AI Language سپرده می‌شود.
4. **ترجمه** (اختیاری) — اگر زبان مقصدی مشخص شده باشد، رونوشت به Azure Translator ارسال می‌شود و تحلیل پردازش زبان طبیعی دوباره روی متن ترجمه‌شده اجرا می‌شود.
5. **خروجی** — نتایج در قالب خروجی انتخاب‌شده (JSON، TXT یا SQLite) نوشته و در رابط وب CherryPy رندر می‌شوند.

تنها وابستگی‌های زمان اجرا خارج از کتابخانه‌ی استاندارد پایتون عبارت‌اند از `azure-cognitiveservices-speech`، `azure-ai-textanalytics`، `azure-ai-translation-text` و `cherrypy`. همه‌ی اعتبارنامه‌های Azure از متغیرهای محیطی خوانده می‌شوند.

## Azure Cognitive Services: موتور رونویسی دسته‌ای

API رونویسی دسته‌ای سرویس گفتار Azure (`/speechtotext/v3.0/transcriptions`) یک ارجاع به فایل صوتی در Azure Blob Storage و یک بدنه‌ی پیکربندی JSON را می‌پذیرد. Audio Analyser فایل محلی را با استفاده از یک URL پیش‌امضاشده‌ی SAS به Blob Storage آپلود می‌کند و سپس کار رونویسی را ارسال می‌کند.

یک بار داده‌ی حداقلی برای ارسال کار:

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

آرایه‌ی پاسخِ `recognizedPhrases` برای هر گفتارِ شناسایی‌شده یک شیء دربردارد. هر ورودی شامل موارد زیر است:

- `nBest[0].confidence` — عدد اعشاری بین ۰ و ۱
- `nBest[0].lexical` — واژه‌های خام همان‌گونه که بیان شده‌اند
- `nBest[0].itn` — شکل نرمال‌سازی‌شده‌ی معکوسِ متن (اعداد، تاریخ‌ها و واحدهای پول بسط‌یافته)
- `nBest[0].display` — قالب‌بندی‌شده برای خواندن، همراه با نشانه‌گذاری
- `speaker` — شناسه‌ی عددی گوینده هنگام فعال بودن تفکیک گوینده

تنظیم دقیق **Custom Speech** برای واژگان خاصِ حوزه در دسترس است. آپلود یک واژه‌نامه‌ی تلفظ یا پیکره‌ی سازگارسازی (مجموعه‌ای از جملات متنیِ نماینده‌ی آن حوزه) مدل زبانی را تنظیم می‌کند و می‌تواند نرخ خطای واژه را روی محتوای تخصصی مانند اصطلاحات مالی یا اصطلاحات تخصصی پزشکی به‌طور چشمگیری کاهش دهد.

## پردازش زبان طبیعی با Azure AI Language

پس از رونویسی، Audio Analyser رونوشت به‌شکل نمایشی را از طریق SDK پایتونِ `azure-ai-textanalytics` به Azure AI Language ارسال می‌کند:

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

`show_opinion_mining=True` احساساتِ سطح-جنبه را فعال می‌کند: این API نه‌تنها قطبیت در سطح سند، بلکه جفت‌های مشخصِ هدف–ارزیابی را بازمی‌گرداند (برای مثال، هدف="کیفیت صدا"، ارزیابی="ضعیف"). این امر خروجی را برای شناسایی مسائل مشخص در تحلیل تماس‌های خدمات مشتری سودمند می‌سازد.

شناسایی موجودیت نام‌دار، بازه‌ها را به‌عنوان یکی از این موارد دسته‌بندی می‌کند: `Person`، `Organization`، `Location`، `Event`، `Product`، `DateTime`، `Quantity`، `IP`، `URL`، `Email`، `PersonType`، `Skill`، `Address`، `PhoneNumber`.

## پشتیبانی چندزبانه از طریق Azure Translator

پس از تشخیص زبان و هنگامی که کاربر زبان مقصدی درخواست کند، Azure Translator فراخوانی می‌شود. این سرویس از ۱۳۵ زبان و گویش با ترجمه‌ی ماشینی عصبی (NMT) پشتیبانی می‌کند. Audio Analyser از نقطه‌ی پایانی REST به‌نام `/translate` با مقدار `autodetect` برای پارامتر `from` استفاده می‌کند، بنابراین نیازی به تعیین زبان مبدأ نیست:

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

پس از ترجمه، Audio Analyser به‌صورت اختیاری پردازش زبان طبیعیِ Text Analytics را دوباره روی متن ترجمه‌شده اجرا می‌کند تا خروجی‌های عبارت کلیدی و احساسات هم به زبان مبدأ و هم به زبان مقصد در دسترس باشند.

انتخاب قالب خروجی (JSON، TXT، SQLite) هنگام راه‌اندازی تنظیم می‌شود. خروجی SQLite هر نشست تحلیل را به‌عنوان یک ردیف با ستون‌هایی برای شناسه‌ی کار، برچسب زمانی، زبان مبدأ، رونوشت، رونوشت ترجمه‌شده، امتیازهای احساسات و عبارت‌های کلیدی به‌صورت یک BLOB از نوع JSON ذخیره می‌کند — و امکان پرس‌وجوهای SQL در میان نشست‌ها را فراهم می‌سازد.

## CherryPy به‌عنوان لایه‌ی وب

CherryPy با استفاده از کنترلرهای مبتنی بر کلاس، مسیرهای URL را به متدهای پایتون نگاشت می‌کند. Audio Analyser از سه مسیر استفاده می‌کند:

| مسیر | متد | توضیح |
|---|---|---|
| `GET /` | `index()` | فرم آپلود را رندر می‌کند |
| `POST /analyse` | `analyse()` | آپلود چندبخشی را می‌پذیرد، خط لوله را راه می‌اندازد، شناسه‌ی کار را بازمی‌گرداند |
| `GET /results/<job_id>` | `results()` | وضعیت کار را نظرسنجی می‌کند؛ در صورت تکمیل، صفحه‌ی نتیجه را رندر می‌کند |

پیکربندی حداقلی، ردپای سرور را کوچک نگه می‌دارد:

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

وضعیت نشست، شناسه‌ی کار جاری، قالب خروجی انتخاب‌شده و زبان مقصد ترجمه را نگه می‌دارد. ذخیره‌سازی نشستِ داخلی CherryPy به‌طور پیش‌فرض فایل‌پایه است و به هیچ لایه‌ی حافظه‌ی نهانِ بیرونی نیاز ندارد.

## پرسش‌های پرتکرار

**Audio Analyser چه قالب‌ها و اندازه‌های فایل صوتی را می‌پذیرد؟**
API رونویسی دسته‌ای Azure از فایل‌های WAV، MP3، OGG و FLAC تا طول ۲٫۵ ساعت پشتیبانی می‌کند. فایل‌های خارج از این بازه باید پیش از آپلود تقسیم شوند. فایل‌های استریو پذیرفته می‌شوند؛ تبدیل به مونو لازم نیست.

**تفکیک گوینده چگونه کار می‌کند؟**
تنظیم `diarizationEnabled: true` در درخواست رونویسی دسته‌ای، مدل جداسازی گوینده‌ی Azure را فعال می‌کند. هر `recognizedPhrase` در پاسخ شامل یک فیلد عددی `speaker` است. این مدل گویندگان را با ویژگی‌های صوتی شناسایی می‌کند و در طول یک نشست شناسه‌های سازگاری به آن‌ها اختصاص می‌دهد، اما بدون یک مرحله‌ی جداگانه‌ی ثبتِ پروفایل صوتی، هویت گویندگان را مشخص نمی‌کند.

**آیا فایل‌های صوتی پس از رونویسی نگهداری می‌شوند؟**
فایل‌های صوتی با یک URL از نوع SAS با عمر کوتاه به Azure Blob Storage آپلود و پس از تکمیل آپلود، از پوشه‌ی موقت محلی حذف می‌شوند. نگهداری بلاب‌ها در Azure Blob Storage به سیاست چرخه‌ی عمرِ کانتینر بستگی دارد؛ به‌طور پیش‌فرض، Audio Analyser هیچ سیاست حذف صریحی تعیین نمی‌کند، بنابراین برای استقرارهای تولیدی توصیه می‌شود که یک قاعده‌ی TTL کوتاه (برای مثال، حذف بلاب‌های قدیمی‌تر از ۱ روز) در پورتال Azure پیکربندی شود.

**آیا می‌توان تحلیل پردازش زبان طبیعی را بدون ترجمه اجرا کرد؟**
بله. ترجمه یک مرحله‌ی اختیاری از خط لوله است که با پرچمِ CLI به‌نام `--target-lang` یا فهرست کشویی زبان مقصد در رابط وب کنترل می‌شود. هنگامی که هیچ زبان مقصدی انتخاب نشده باشد، خط لوله تنها گفتار به متن و Text Analytics را اجرا می‌کند.

## منابع

1. Microsoft. *Batch transcription overview — Azure AI services*. Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/speech-service/batch-transcription>
2. Xiong, W. et al. "Achieving Human Parity in Conversational Speech Recognition." *Microsoft Research Technical Report*, 2016; updated 2021. <https://arxiv.org/abs/1610.05256>
3. Microsoft. *What is Azure AI Language?* Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/language-service/overview>
4. Microsoft. *Azure AI Translator — Supported languages*. Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/translator/language-support>

[00]: https://audioanalyser.co/ "Audio Analyser — Azure-backed speech analytics tool"
