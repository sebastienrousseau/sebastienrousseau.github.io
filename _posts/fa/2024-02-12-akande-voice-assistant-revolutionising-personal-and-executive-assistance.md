---
title: "Àkàndé: دستیار صوتی مبتنی بر GPT برای مدیران اجرایی"
tags: "Àkàndé, GPT4, WhisperSTT, SQLiteCache, fpdf2, PythonVoiceAssistant, ChatCompletionsAPI, PDFSummary, open source, ExecutiveAI, ISO 20022, post-quantum cryptography, AI, DORA, platform engineering, sovereign cloud, cloud native banking"
subtitle: "معماری یک دستیار صوتی متن‌باز پایتون: Whisper، GPT-4، حافظهٔ نهان SQLite و fpdf2"
description: "Àkàndé یک دستیار صوتی متن‌باز پایتون است که تشخیص گفتار OpenAI Whisper، تکمیل گفت‌وگوی GPT-4 و یک حافظهٔ نهان پاسخ محلی SQLite را در یک گردش‌کار صوتی‌محور به هم زنجیر می‌کند - خلاصه‌های PDF را از تاریخچهٔ مکالمه تولید می‌کند و همهٔ داده‌های ذخیره‌شده را به‌صورت محلی نگه می‌دارد."
date: "Feb 12, 2024"
language: "fa"
locale: "fa_IR"
banner: "https://cloudcdn.pro/stocks/images/akande-voice-assistant.webp"
banner_alt: "یک دستگاه مدرن کروی و سفید"
keywords: "Àkàndé, OpenAI GPT-4, Whisper STT, حافظهٔ نهان SQLite, fpdf2, دستیار صوتی پایتون, chat completions API, تولید خلاصهٔ PDF, حافظهٔ نهان SHA-256, تبدیل متن به گفتار, هوش مصنوعی دستیار اجرایی, متن‌باز"
---

> **خلاصهٔ اجرایی / نکات کلیدی**
>
> - **[Àkàndé ⧉][00]** یک دستیار صوتی متن‌باز پایتون است که تبدیل گفتار به متن OpenAI Whisper، تکمیل گفت‌وگوی GPT-4، یک حافظهٔ نهان پاسخ محلی SQLite و خروجی PDF با fpdf2 را در یک گردش‌کار صوتی‌محور واحد به هم زنجیر می‌کند که به هیچ ذخیره‌سازی ابری و هیچ وزن مدل هوش مصنوعی محلی نیاز ندارد.
> - **حافظهٔ نهان SQLite** درهم‌سازی‌های SHA-256 از رشته‌های پرس‌وجوی نرمال‌شده را ذخیره می‌کند که به متن پاسخ خام API نگاشت می‌شوند؛ برخوردهای حافظهٔ نهان صفر توکن هزینه دارند و در کمتر از ۱۰ میلی‌ثانیه بازمی‌گردند، و این پرس‌وجوهای تکراری (مانند مرور یک تصمیم از اوایل یک جلسه) را عملاً رایگان می‌کند.
> - **مکالمهٔ چندنوبتی** با ساختن فهرست `messages` در حافظه و ارسال آن در هر فراخوانی API تکمیل گفت‌وگو حفظ می‌شود — مدل تاریخچهٔ کامل نشست را دریافت می‌کند تا بتواند به تبادل‌های پیشین ارجاع دهد، به قیمت افزایش تدریجی مصرف توکن در هر نوبت.
> - **تولید خلاصهٔ PDF** فهرست `messages` نشست را به یک سند قالب‌بندی‌شدهٔ fpdf2 سریال‌سازی می‌کند: نوبت‌های کاربر و نوبت‌های دستیار برچسب‌گذاری می‌شوند، مُهرهای زمانی درج می‌شوند و صفحه‌بندی خودکار نشست‌هایی با هر طولی را مدیریت می‌کند؛ فایل روی سیستم فایل محلی نوشته می‌شود، نه بارگذاری در جایی دیگر.
> - **مرز حریم خصوصی:** تنها پرس‌وجوی زنده (و تاریخچهٔ نشست تا حد پنجرهٔ زمینه) دستگاه را ترک می‌کند — هیچ ضبط صوتی، هیچ رونوشتی و هیچ پاسخ ذخیره‌شده‌ای به هیچ سرویس راه دوری جز API خودِ OpenAI ارسال نمی‌شود.

[**Àkàndé ⧉**][00] یک دستیار صوتی متن‌باز پایتون است که حول سه مؤلفهٔ قابل ترکیب ساخته شده است: OpenAI Whisper برای تشخیص گفتار، API تکمیل گفت‌وگوی GPT-4 برای درک و تولید زبان، و یک پایگاه دادهٔ محلی SQLite برای ذخیرهٔ نهان پاسخ‌ها و ماندگاری نشست. حاصل، یک گردش‌کار صوتی‌محور است که می‌توان آن را روی یک لپ‌تاپ و بدون وزن‌های مدل محلی، زیرساخت ذخیره‌سازی برون‌خط یا یک پشتهٔ کانتینر اجرا کرد.

این مقاله معماری فنی هر مؤلفه، تصمیم‌های طراحی پیرامون ذخیرهٔ نهان و زمینهٔ چندنوبتی، و خط لولهٔ خروجی PDF را شرح می‌دهد.

## نمای کلی خط لوله

یک تعامل واحد در Àkàndé این توالی را دنبال می‌کند:

1. **ضبط صدا** — کاربر صحبت می‌کند؛ برنامه با استفاده از `sounddevice` یا یک کتابخانهٔ صوتی سازگار، صدا را در یک فایل WAV موقت ضبط می‌کند.
2. **تبدیل گفتار به متن** — فایل WAV به `openai.audio.transcriptions.create()` (API Whisper) سپرده می‌شود؛ رونوشت به‌صورت یک رشتهٔ ساده بازگردانده می‌شود.
3. **جست‌وجوی حافظهٔ نهان** — رونوشت نرمال‌سازی می‌شود (کوچک‌کردن حروف، فشرده‌سازی فاصله‌ها) و با SHA-256 درهم‌سازی می‌شود؛ درهم‌سازی در جدول محلی `response_cache` در SQLite جست‌وجو می‌شود.
4. **فراخوانی API یا برخورد با حافظهٔ نهان** — در صورت عدم برخورد، رونوشت به فهرست `messages` نشست افزوده و به `openai.chat.completions.create()` ارسال می‌شود؛ متن پاسخ در حافظهٔ نهان ذخیره می‌شود.
5. **تبدیل متن به گفتار** — متن پاسخ با استفاده از نقطهٔ پایانی `openai.audio.speech.create()` (TTS) یا یک کتابخانهٔ محلی TTS به صدا تبدیل و پخش می‌شود.
6. **خروجی PDF** (بنا به درخواست) — فهرست کامل `messages` به یک سند قالب‌بندی‌شدهٔ fpdf2 سریال‌سازی و روی دیسک نوشته می‌شود.

## یکپارچه‌سازی OpenAI: تکمیل گفت‌وگو و Whisper

Àkàndé از SDK پایتون `openai` هم برای تشخیص گفتار و هم برای تولید متن استفاده می‌کند. فراخوانی رونوشت‌برداری Whisper:

```python
with open(audio_file_path, "rb") as f:
    transcript = openai.audio.transcriptions.create(
        model="whisper-1",
        file=f,
        language=None  # auto-detect
    )
user_text = transcript.text
```

فراخوانی تکمیل گفت‌وگو یک فهرست `messages` با دامنهٔ نشست را نگه می‌دارد:

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

پرامپت سیستمی یک‌بار در آغاز نشست پیش‌درج می‌شود و شخصیت Àkàndé، قالب خروجی و هرگونه محدودیت خاص حوزه را کنترل می‌کند:

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

تنظیم `temperature=0.2` تنوع خلاقانه را با قطعیت مبادله می‌کند — امری مهم برای پرس‌وجوهای واقعیت‌محور مانند فراخوانی یک تصمیم از اوایل نشست.

## حافظهٔ نهان پاسخ SQLite

شمای حافظهٔ نهان کمینه است:

```sql
CREATE TABLE IF NOT EXISTS response_cache (
    query_hash  TEXT PRIMARY KEY,
    response    TEXT NOT NULL,
    created_at  INTEGER NOT NULL  -- Unix timestamp
);
```

مسیر جست‌وجو و نوشتن:

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

دستور `INSERT OR REPLACE` تضمین می‌کند که اگر همان پرس‌وجو پس از ارتقای مدل ارسال شود، پاسخ نهان‌شده به‌روزرسانی گردد. یک پرس‌وجوی تخلیهٔ مبتنی بر TTL (`DELETE WHERE created_at < ?`) را می‌توان هنگام راه‌اندازی زمان‌بندی کرد تا اندازهٔ حافظهٔ نهان محدود بماند.

کارایی برخورد با حافظهٔ نهان: یک جست‌وجوی SQLite روی یک SSD محلی برای جدول‌هایی تا حدود ۱۰۰٬۰۰۰ ردیف در کمتر از ۱ میلی‌ثانیه بازمی‌گردد. تأخیر رفت‌وبرگشت برای یک فراخوانی زندهٔ API در GPT-4 معمولاً برای پاسخ‌های کوتاه ۶۰۰ تا ۹۰۰ میلی‌ثانیه است. برای یک بریفینگ روزانه با تعداد اندکی پرس‌وجوی تکراری، حافظهٔ نهان پس از نخستین نشست بیشتر فراخوانی‌های API را حذف می‌کند.

## تولید خلاصهٔ PDF

خروجی PDF از [fpdf2](https://py-pdf.github.io/fpdf2/) استفاده می‌کند، یک کتابخانهٔ PDF پایتون که به‌طور فعال نگهداری می‌شود و هیچ وابستگی باینری ندارد:

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

`multi_cell()` شکستن خطوط و شکست صفحهٔ خودکار را مدیریت می‌کند، بنابراین نشست‌هایی با هر طولی بدون منطق صفحه‌بندی دستی یک سند خوش‌قالب تولید می‌کنند. خروجی یک فایل سازگار با PDF/A است که هیچ فونت جاسازی‌شده‌ای فراتر از معیارهای استاندارد Helvetica ندارد.

## مدل حریم خصوصی

مرز حریم خصوصی در Àkàndé با سه واقعیت تعریف می‌شود:

1. صدا از طریق HTTPS به API Whisper سپرده می‌شود و فراتر از خودِ فراخوانی API توسط OpenAI نگهداری نمی‌شود (بر پایهٔ سیاست استفاده از دادهٔ API خودِ OpenAI تا فوریهٔ ۲۰۲۴).
2. فراخوانی‌های API تکمیل گفت‌وگو فهرست `messages` نشست را ارسال می‌کنند — که ممکن است برای نشست‌های چندنوبتی حاوی تاریخچهٔ کامل مکالمه باشد.
3. پایگاه دادهٔ SQLite و فایل‌های PDF به‌طور کامل روی سیستم فایل محلی قرار دارند؛ هیچ همگام‌سازی پس‌زمینه‌ای با هیچ سرویس ابری رخ نمی‌دهد.

برای موارد کاربرد اجرایی که موضوعات حساسی را در بر می‌گیرند — گفت‌وگوهای ادغام و تملک، مسائل پرسنلی، راهبرد مقرراتی — تاریخچهٔ نشست منتقل‌شده به API باید پیش از استقرار در برابر سیاست استفاده از هوش مصنوعی سازمان بازبینی شود. از محدودیت `max_tokens` روی پرامپت سیستمی می‌توان برای جلوگیری از انتقال ناخواستهٔ زمینه‌ای که فراتر از دامنهٔ افشای موردنظر است بهره برد.

## پرسش‌های پرتکرار

**آیا Àkàndé تاریخچهٔ مکالمه را پس از پایان نشست نگه می‌دارد؟**
فهرست `messages` درون‌حافظه‌ای هنگام خروج فرایند دور ریخته می‌شود. تاریخچهٔ مکالمه تنها در صورتی نگهداری می‌شود که کاربر یک خروجی PDF را راه بیندازد یا یک لایهٔ ماندگاری سفارشی افزوده شود. حافظهٔ نهان SQLite درهم‌سازی‌های پرس‌وجو و متن پاسخ را ذخیره می‌کند، نه زمینهٔ کامل مکالمه را.

**حافظهٔ نهان چگونه با پرس‌وجوهایی که مشابه‌اند اما یکسان نیستند برخورد می‌کند؟**
حافظهٔ نهان از درهم‌سازی تطبیق دقیق روی رشتهٔ پرس‌وجوی نرمال‌شده استفاده می‌کند. دو پرس‌وجو که تنها در یک واژه تفاوت دارند درهم‌سازی‌های متفاوتی تولید می‌کنند و به فراخوانی‌های جداگانهٔ API می‌انجامند. ذخیرهٔ نهان معنایی (استفاده از شباهت بردار جای‌گذاری برای تطبیق پرس‌وجوهای نزدیک به هم) به یک گام جست‌وجوی برداری اضافی نیاز دارد و بخشی از پیاده‌سازی پایه نیست.

**Àkàndé به‌طور پیش‌فرض از کدام مدل GPT استفاده می‌کند؟**
مقدار پیش‌فرض تا فوریهٔ ۲۰۲۴، `gpt-4-turbo-preview` است. نام مدل یک پارامتر پیکربندی است، بنابراین می‌توان هر مدل تکمیل گفت‌وگوی OpenAI را جایگزین کرد. تغییر به `gpt-3.5-turbo` هزینهٔ API را در هر توکن حدود ۲۰ برابر کاهش می‌دهد اما کیفیت استدلال را برای پرس‌وجوهای پیچیدهٔ چندمرحله‌ای کم می‌کند.

**آیا قالب خروجی PDF قابل سفارشی‌سازی است؟**
بله. تابع خروجی fpdf2 فهرست `messages` را به‌عنوان تنها ورودی الزامی خود می‌پذیرد، بنابراین فونت، حاشیه‌ها، اندازهٔ صفحه، محتوای سرصفحه و برچسب‌گذاری همگی با ویرایش تابع خروجی قابل تغییرند. fpdf2 همچنین از افزودن تصاویر، جدول‌ها و فونت‌های یونیکد پشتیبانی می‌کند و طرح‌بندی‌های سند غنی‌تری را برای سازمان‌هایی با الزامات برندسازی خاص ممکن می‌سازد.

## منابع

1. OpenAI. *Audio Transcriptions — Whisper API*. OpenAI Platform Documentation, 2024. https://platform.openai.com/docs/api-reference/audio/createTranscription
2. OpenAI. *Chat Completions API*. OpenAI Platform Documentation, 2024. https://platform.openai.com/docs/api-reference/chat/create
3. Voss, J. et al. *fpdf2: Modern PDF generation for Python*. GitHub, 2024. https://github.com/py-pdf/fpdf2
4. SQLite Consortium. *SQLite Documentation*. sqlite.org, 2024. https://www.sqlite.org/docs.html

[00]: https://akande.co "Àkàndé Voice Assistant"
