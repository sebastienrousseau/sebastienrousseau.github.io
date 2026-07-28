---
title: "Àkàndé: ผู้ช่วยเสียงที่ขับเคลื่อนด้วย GPT สำหรับผู้บริหาร"
subtitle: "สถาปัตยกรรมของผู้ช่วยเสียงโอเพนซอร์สบน Python: Whisper, GPT-4, แคช SQLite และ fpdf2"
description: "Àkàndé คือผู้ช่วยเสียงโอเพนซอร์สบน Python ที่เชื่อมการรู้จำเสียงพูดด้วย OpenAI Whisper การสร้างบทสนทนาด้วย GPT-4 และแคชคำตอบ SQLite ในเครื่องเข้าเป็นเวิร์กโฟลว์ที่ขับเคลื่อนด้วยเสียง สร้างสรุปแบบ PDF จากประวัติการสนทนาและเก็บข้อมูลทั้งหมดไว้ในเครื่อง"
date: "February 12, 2024"
language: "th-TH"
locale: "th_TH"
banner: "https://cloudcdn.pro/stocks/images/akande-voice-assistant.webp"
banner_alt: "อุปกรณ์ทรงกลมสีขาวสไตล์โมเดิร์น"
keywords: "Àkàndé, OpenAI GPT-4, Whisper STT, การแคช SQLite, fpdf2, ผู้ช่วยเสียง Python, chat completions API, การสร้างสรุป PDF, แคช SHA-256, การแปลงข้อความเป็นเสียง, AI ผู้ช่วยผู้บริหาร, โอเพนซอร์ส"
---


> **บทสรุปผู้บริหาร / ประเด็นสำคัญ**
>
> - **[Àkàndé ⧉][00]** คือผู้ช่วยเสียงโอเพนซอร์สบน Python ที่เชื่อมการแปลงเสียงพูดเป็นข้อความด้วย OpenAI Whisper, การสร้างบทสนทนาด้วย GPT-4, แคชคำตอบ SQLite ในเครื่อง และการส่งออก PDF ด้วย fpdf2 เข้าเป็นเวิร์กโฟลว์เดียวที่ขับเคลื่อนด้วยเสียง โดยไม่ต้องใช้พื้นที่จัดเก็บบนคลาวด์และไม่ต้องใช้น้ำหนักโมเดล AI ในเครื่อง
> - **แคช SQLite** จัดเก็บค่าแฮช SHA-256 ของสตริงคำค้นที่ผ่านการปรับให้เป็นมาตรฐาน โดยจับคู่กับข้อความคำตอบดิบจาก API การพบข้อมูลในแคช (cache hit) ใช้โทเคนเป็นศูนย์และตอบกลับภายในเวลาไม่ถึง 10 มิลลิวินาที ทำให้คำค้นซ้ำ (เช่น การทบทวนการตัดสินใจก่อนหน้านี้ในการประชุม) แทบไม่มีต้นทุน
> - **การสนทนาแบบหลายรอบ** คงไว้ด้วยการสร้างรายการ `messages` ในหน่วยความจำและส่งไปในทุกการเรียก Chat Completions API โมเดลจะได้รับประวัติเซสชันทั้งหมดจึงสามารถอ้างถึงบทสนทนาก่อนหน้าได้ โดยแลกกับการใช้โทเคนต่อรอบที่เพิ่มขึ้นทีละน้อย
> - **การสร้างสรุป PDF** แปลงรายการ `messages` ของเซสชันเป็นเอกสาร fpdf2 ที่จัดรูปแบบแล้ว โดยกำกับรอบของผู้ใช้และรอบของผู้ช่วย แทรกเวลาประทับ และแบ่งหน้าอัตโนมัติเพื่อรองรับเซสชันทุกความยาว ไฟล์จะถูกเขียนลงระบบไฟล์ในเครื่อง ไม่ได้อัปโหลด
> - **ขอบเขตความเป็นส่วนตัว:** มีเพียงคำค้นปัจจุบัน (และประวัติเซสชันภายในขีดจำกัดของหน้าต่างบริบท) เท่านั้นที่ออกจากอุปกรณ์ ไม่มีการส่งไฟล์บันทึกเสียง ข้อความถอดเสียง หรือคำตอบในแคชไปยังบริการภายนอกใด นอกเหนือจาก API ของ OpenAI

[**Àkàndé ⧉**][00] คือผู้ช่วยเสียงโอเพนซอร์สบน Python ที่สร้างขึ้นรอบองค์ประกอบที่ประกอบเข้าด้วยกันได้สามส่วน ได้แก่ OpenAI Whisper สำหรับการรู้จำเสียงพูด, GPT-4 Chat Completions API สำหรับการเข้าใจและสร้างภาษา และฐานข้อมูล SQLite ในเครื่องสำหรับการแคชคำตอบและการคงสถานะของเซสชัน ผลลัพธ์คือเวิร์กโฟลว์ที่ขับเคลื่อนด้วยเสียงซึ่งสามารถทำงานบนแล็ปท็อปได้ โดยไม่ต้องใช้น้ำหนักโมเดลในเครื่อง โครงสร้างพื้นฐานการจัดเก็บแบบออฟไลน์ หรือชุดคอนเทนเนอร์

บทความนี้อธิบายสถาปัตยกรรมทางเทคนิคของแต่ละองค์ประกอบ การตัดสินใจด้านการออกแบบเกี่ยวกับการแคชและบริบทแบบหลายรอบ และไปป์ไลน์การส่งออก PDF

## ภาพรวมของไปป์ไลน์

การโต้ตอบกับ Àkàndé หนึ่งครั้งดำเนินตามลำดับต่อไปนี้:

1. **การบันทึกเสียง:** ผู้ใช้พูด แอปพลิเคชันบันทึกเสียงลงในไฟล์ WAV ชั่วคราวโดยใช้ `sounddevice` หรือไลบรารีเสียงที่เข้ากันได้
2. **การแปลงเสียงเป็นข้อความ:** ไฟล์ WAV ถูกส่งไปยัง `openai.audio.transcriptions.create()` (Whisper API) และได้รับข้อความถอดเสียงกลับมาเป็นสตริงธรรมดา
3. **การค้นหาในแคช:** ข้อความถอดเสียงถูกปรับให้เป็นมาตรฐาน (แปลงเป็นตัวพิมพ์เล็ก ยุบช่องว่าง) และแฮชด้วย SHA-256 จากนั้นค้นหาค่าแฮชในตาราง `response_cache` ของ SQLite ในเครื่อง
4. **การเรียก API หรือการพบในแคช:** เมื่อไม่พบในแคช ข้อความถอดเสียงจะถูกเพิ่มต่อท้ายรายการ `messages` ของเซสชันและส่งไปยัง `openai.chat.completions.create()` จากนั้นข้อความคำตอบจะถูกจัดเก็บในแคช
5. **การแปลงข้อความเป็นเสียง:** ข้อความคำตอบถูกแปลงเป็นเสียงโดยใช้เอนด์พอยต์ `openai.audio.speech.create()` (TTS) หรือไลบรารี TTS ในเครื่อง แล้วเล่นกลับ
6. **การส่งออก PDF** (ตามคำขอ): รายการ `messages` ทั้งหมดถูกแปลงเป็นเอกสาร fpdf2 ที่จัดรูปแบบแล้วและเขียนลงดิสก์

## การผสานรวม OpenAI: Chat Completions และ Whisper

Àkàndé ใช้ `openai` Python SDK ทั้งสำหรับการรู้จำเสียงพูดและการสร้างข้อความ การเรียกถอดเสียงด้วย Whisper:

```python
with open(audio_file_path, "rb") as f:
    transcript = openai.audio.transcriptions.create(
        model="whisper-1",
        file=f,
        language=None  # auto-detect
    )
user_text = transcript.text
```

การเรียก Chat Completions คงรายการ `messages` ที่กำหนดขอบเขตตามเซสชัน:

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

พรอมต์ระบบถูกใส่ไว้ด้านหน้าเพียงครั้งเดียวตอนเริ่มเซสชัน และควบคุมบุคลิกของ Àkàndé รูปแบบผลลัพธ์ และข้อจำกัดเฉพาะโดเมนใด ๆ:

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

การตั้งค่า `temperature=0.2` แลกความหลากหลายเชิงสร้างสรรค์กับความแน่นอนของผลลัพธ์ ซึ่งสำคัญสำหรับคำค้นเชิงข้อเท็จจริง เช่น การเรียกคืนการตัดสินใจก่อนหน้านี้ในเซสชัน

## แคชคำตอบ SQLite

สคีมาของแคชมีขนาดเล็กที่สุด:

```sql
CREATE TABLE IF NOT EXISTS response_cache (
    query_hash  TEXT PRIMARY KEY,
    response    TEXT NOT NULL,
    created_at  INTEGER NOT NULL  -- Unix timestamp
);
```

เส้นทางการค้นหาและการเขียน:

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

`INSERT OR REPLACE` รับประกันว่าคำตอบในแคชจะถูกอัปเดตหากมีการส่งคำค้นเดิมหลังการอัปเกรดโมเดล คำสั่งลบตาม TTL (`DELETE WHERE created_at < ?`) สามารถตั้งเวลาให้ทำงานตอนเริ่มระบบเพื่อจำกัดขนาดของแคชได้

ประสิทธิภาพของการพบในแคช: การค้นหาใน SQLite บน SSD ในเครื่องตอบกลับภายในเวลาไม่ถึง 1 มิลลิวินาทีสำหรับตารางที่มีแถวไม่เกินราว 100,000 แถว ส่วนเวลาไป-กลับของการเรียก GPT-4 API แบบสดโดยทั่วไปอยู่ที่ 600 ถึง 900 มิลลิวินาทีสำหรับคำตอบสั้น ๆ สำหรับการบรีฟประจำวันที่มีคำค้นซ้ำอยู่ไม่กี่รายการ แคชจะช่วยตัดการเรียก API ส่วนใหญ่ออกหลังจากเซสชันแรก

## การสร้างสรุป PDF

การส่งออก PDF ใช้ [fpdf2](https://py-pdf.github.io/fpdf2/) ไลบรารี PDF บน Python ที่มีการดูแลอย่างต่อเนื่องและไม่มีการพึ่งพาไบนารี:

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

`multi_cell()` จัดการการตัดบรรทัดและการขึ้นหน้าใหม่อัตโนมัติ ดังนั้นเซสชันทุกความยาวจึงให้เอกสารที่จัดรูปแบบเรียบร้อยโดยไม่ต้องเขียนตรรกะแบ่งหน้าเอง ผลลัพธ์เป็นไฟล์ที่รองรับ PDF/A โดยไม่มีการฝังฟอนต์นอกเหนือจากมาตรวัดฟอนต์ Helvetica มาตรฐาน

## แบบจำลองความเป็นส่วนตัว

ขอบเขตความเป็นส่วนตัวใน Àkàndé กำหนดด้วยข้อเท็จจริงสามประการ:

1. เสียงถูกส่งไปยัง Whisper API ผ่าน HTTPS และ OpenAI ไม่เก็บรักษาไว้เกินกว่าการเรียก API นั้น (ตามนโยบายการใช้ข้อมูลของ API ของ OpenAI ณ เดือนกุมภาพันธ์ 2024)
2. การเรียก Chat Completions API ส่งรายการ `messages` ของเซสชัน ซึ่งอาจมีประวัติการสนทนาทั้งหมดสำหรับเซสชันแบบหลายรอบ
3. ฐานข้อมูล SQLite และไฟล์ PDF อยู่บนระบบไฟล์ในเครื่องทั้งหมด ไม่มีการซิงก์เบื้องหลังไปยังบริการคลาวด์ใด ๆ

สำหรับกรณีใช้งานระดับผู้บริหารที่เกี่ยวข้องกับหัวข้ออ่อนไหว เช่น การเจรจาควบรวมกิจการ เรื่องบุคลากร และกลยุทธ์ด้านกฎระเบียบ ควรตรวจทานประวัติเซสชันที่ส่งไปยัง API เทียบกับนโยบายการใช้ AI ขององค์กรก่อนนำไปใช้งานจริง ขีดจำกัด `max_tokens` บนพรอมต์ระบบสามารถใช้เพื่อป้องกันการส่งบริบทเกินขอบเขตการเปิดเผยที่ตั้งใจไว้โดยไม่ได้ตั้งใจ

## คำถามที่พบบ่อย

**Àkàndé เก็บประวัติการสนทนาไว้หลังจากเซสชันสิ้นสุดหรือไม่?**
รายการ `messages` ในหน่วยความจำจะถูกทิ้งเมื่อกระบวนการสิ้นสุด ประวัติการสนทนาจะถูกเก็บไว้ก็ต่อเมื่อผู้ใช้สั่งการส่งออก PDF หรือมีการเพิ่มชั้นการคงข้อมูลแบบกำหนดเอง แคช SQLite จัดเก็บค่าแฮชของคำค้นและข้อความคำตอบ ไม่ใช่บริบทการสนทนาทั้งหมด

**แคชจัดการคำค้นที่คล้ายกันแต่ไม่เหมือนกันอย่างไร?**
แคชใช้การแฮชแบบตรงกันทุกตัวอักษรบนสตริงคำค้นที่ปรับให้เป็นมาตรฐานแล้ว คำค้นสองรายการที่ต่างกันเพียงคำเดียวจะให้ค่าแฮชต่างกันและนำไปสู่การเรียก API แยกกัน การแคชเชิงความหมาย (ใช้ความคล้ายของเวกเตอร์ฝังเพื่อจับคู่คำค้นที่เกือบซ้ำกัน) จะต้องมีขั้นตอนการค้นหาเวกเตอร์เพิ่มเติมและไม่ได้เป็นส่วนหนึ่งของการพัฒนาพื้นฐาน

**Àkàndé ใช้โมเดล GPT ใดเป็นค่าเริ่มต้น?**
ค่าเริ่มต้นคือ `gpt-4-turbo-preview` ณ เดือนกุมภาพันธ์ 2024 ชื่อโมเดลเป็นพารามิเตอร์การตั้งค่า จึงสามารถแทนที่ด้วยโมเดล chat completion ของ OpenAI รุ่นใดก็ได้ การเปลี่ยนไปใช้ `gpt-3.5-turbo` ลดต้นทุน API ลงราว 20 เท่าต่อโทเคน แต่ลดคุณภาพการให้เหตุผลสำหรับคำค้นหลายขั้นตอนที่ซับซ้อน

**สามารถปรับแต่งรูปแบบการส่งออก PDF ได้หรือไม่?**
ได้ ฟังก์ชันส่งออกของ fpdf2 รับรายการ `messages` เป็นอินพุตที่จำเป็นเพียงอย่างเดียว ดังนั้นฟอนต์ ระยะขอบ ขนาดหน้า เนื้อหาส่วนหัว และการกำกับป้ายจึงสามารถเปลี่ยนได้ทั้งหมดด้วยการแก้ไขฟังก์ชันส่งออก fpdf2 ยังรองรับการเพิ่มรูปภาพ ตาราง และฟอนต์ Unicode ทำให้จัดวางเอกสารได้หลากหลายยิ่งขึ้นสำหรับองค์กรที่มีข้อกำหนดด้านแบรนด์เฉพาะ

## เอกสารอ้างอิง

1. OpenAI. *Audio Transcriptions — Whisper API*. OpenAI Platform Documentation, 2024. https://platform.openai.com/docs/api-reference/audio/createTranscription
2. OpenAI. *Chat Completions API*. OpenAI Platform Documentation, 2024. https://platform.openai.com/docs/api-reference/chat/create
3. Voss, J. et al. *fpdf2: Modern PDF generation for Python*. GitHub, 2024. https://github.com/py-pdf/fpdf2
4. SQLite Consortium. *SQLite Documentation*. sqlite.org, 2024. https://www.sqlite.org/docs.html

[00]: https://akande.co "Àkàndé Voice Assistant"
