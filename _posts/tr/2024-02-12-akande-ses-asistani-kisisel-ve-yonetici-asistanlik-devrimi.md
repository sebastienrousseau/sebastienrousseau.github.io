---
title: "Àkàndé: Yöneticiler için GPT tabanlı Ses Asistanı"
subtitle: "Açık kaynaklı bir Python ses asistanının mimarisi: Whisper, GPT-4, SQLite önbelleği ve fpdf2"
description: "Àkàndé, OpenAI Whisper konuşma tanıma, GPT-4 sohbet tamamlamaları ve yerel bir SQLite yanıt önbelleğini sesle yönetilen bir iş akışında birleştiren açık kaynaklı bir Python ses asistanıdır. Konuşma geçmişinden PDF özetleri üretir ve saklanan tüm verileri yerelde tutar."
date: "Feb 12, 2024"
language: "tr-TR"
locale: "tr_TR"
banner: "https://cloudcdn.pro/stocks/images/akande-voice-assistant.webp"
banner_alt: "Beyaz, küresel modern bir cihaz"
keywords: "Àkàndé, OpenAI GPT-4, Whisper STT, SQLite önbellekleme, fpdf2, Python ses asistanı, chat completions API, PDF özet üretimi, SHA-256 önbellek, metinden sese, yönetici asistanı yapay zekâ, açık kaynak"
---


> **Yönetici Özeti / Önemli Çıkarımlar**
>
> - **[Àkàndé ⧉][00]**, OpenAI Whisper konuşmadan metne, GPT-4 sohbet tamamlamaları, yerel bir SQLite yanıt önbelleği ve fpdf2 PDF dışa aktarımını tek bir sesle yönetilen iş akışında birleştiren açık kaynaklı bir Python ses asistanıdır; bulut depolama ve yerel yapay zekâ model ağırlıkları gerektirmez.
> - **SQLite önbelleği**, normalleştirilmiş sorgu dizelerinin SHA-256 karmalarını ham API yanıt metnine eşleyerek saklar; önbellek isabetleri sıfır token maliyeti taşır ve 10 ms'nin altında döner; bu da tekrarlanan sorguları (örneğin toplantının başında alınan bir kararı yeniden gözden geçirmek gibi) fiilen ücretsiz kılar.
> - **Çok turlu konuşma**, `messages` listesi bellekte oluşturularak ve her Chat Completions API çağrısında iletilerek sürdürülür; model tam oturum geçmişini alır ve önceki alışverişlere atıfta bulunabilir, bunun karşılığında tur başına token kullanımı kademeli olarak artar.
> - **PDF özet üretimi**, oturumun `messages` listesini biçimlendirilmiş bir fpdf2 belgesine seri hale getirir: kullanıcı turları ve asistan turları etiketlenir, zaman damgaları eklenir ve otomatik sayfalama her uzunluktaki oturumu ele alır; dosya karşıya yüklenmez, yerel dosya sistemine yazılır.
> - **Gizlilik sınırı:** yalnızca canlı sorgu (ve bağlam penceresi sınırına kadar olan oturum geçmişi) cihazdan ayrılır; hiçbir ses kaydı, dökümü veya önbelleğe alınmış yanıt, OpenAI'nin API'si dışında herhangi bir uzak hizmete gönderilmez.

[**Àkàndé ⧉**][00], üç birleştirilebilir bileşen etrafında kurulmuş açık kaynaklı bir Python ses asistanıdır: konuşma tanıma için OpenAI Whisper, dil anlama ve üretme için GPT-4 Chat Completions API'si ve yanıt önbellekleme ile oturum kalıcılığı için yerel bir SQLite veritabanı. Sonuç, yerel model ağırlıkları, çevrimdışı depolama altyapısı veya bir konteyner yığını olmadan bir dizüstü bilgisayarda çalıştırılabilen, sesle yönetilen bir iş akışıdır.

Bu makale, her bileşenin teknik mimarisini, önbellekleme ve çok turlu bağlam etrafındaki tasarım kararlarını ve PDF dışa aktarım hattını açıklar.

## İşlem Hattına Genel Bakış

Tek bir Àkàndé etkileşimi şu sırayı izler:

1. **Ses yakalama:** kullanıcı konuşur; uygulama, sesi `sounddevice` veya uyumlu bir ses kütüphanesi kullanarak geçici bir WAV dosyasına kaydeder.
2. **Konuşmadan metne:** WAV dosyası `openai.audio.transcriptions.create()` (Whisper API) çağrısına gönderilir; dökümü düz bir dize olarak döner.
3. **Önbellek araması:** döküm normalleştirilir (küçük harfe çevrilir, boşluklar sıkıştırılır) ve SHA-256 ile karmalanır; karma, yerel SQLite `response_cache` tablosunda aranır.
4. **API çağrısı veya önbellek isabeti:** bir ıskalama durumunda döküm oturumun `messages` listesine eklenir ve `openai.chat.completions.create()` çağrısına gönderilir; yanıt metni önbelleğe kaydedilir.
5. **Metinden sese:** yanıt metni `openai.audio.speech.create()` uç noktası (TTS) veya yerel bir TTS kütüphanesi kullanılarak sese dönüştürülür ve oynatılır.
6. **PDF dışa aktarımı** (talep üzerine): tam `messages` listesi biçimlendirilmiş bir fpdf2 belgesine seri hale getirilir ve diske yazılır.

## OpenAI Entegrasyonu: Chat Completions ve Whisper

Àkàndé, hem konuşma tanıma hem de metin üretimi için `openai` Python SDK'sını kullanır. Whisper döküm çağrısı:

```python
with open(audio_file_path, "rb") as f:
    transcript = openai.audio.transcriptions.create(
        model="whisper-1",
        file=f,
        language=None  # auto-detect
    )
user_text = transcript.text
```

Chat Completions çağrısı, oturum kapsamlı bir `messages` listesini sürdürür:

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

Sistem istemi, oturum başında bir kez başa eklenir ve Àkàndé'nin kişiliğini, çıktı biçimini ve alana özgü her türlü kısıtlamayı denetler:

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

`temperature=0.2` ayarı, yaratıcı çeşitliliği belirlilik lehine takas eder; bu, oturumun başında alınan bir kararı hatırlamak gibi olgusal sorgular için önemlidir.

## SQLite Yanıt Önbelleği

Önbellek şeması en aza indirilmiştir:

```sql
CREATE TABLE IF NOT EXISTS response_cache (
    query_hash  TEXT PRIMARY KEY,
    response    TEXT NOT NULL,
    created_at  INTEGER NOT NULL  -- Unix timestamp
);
```

Arama ve yazma yolu:

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

`INSERT OR REPLACE`, bir model yükseltmesinden sonra aynı sorgu gönderilirse önbelleğe alınmış bir yanıtın güncellenmesini sağlar. Önbellek boyutunu sınırlamak için başlangıçta TTL tabanlı bir tahliye sorgusu (`DELETE WHERE created_at < ?`) zamanlanabilir.

Önbellek isabet performansı: yerel bir SSD üzerindeki bir SQLite araması, ~100.000 satıra kadar olan tablolar için 1 ms'nin altında döner. Canlı bir GPT-4 API çağrısının gidiş dönüş gecikmesi, kısa yanıtlar için tipik olarak 600-900 ms'dir. Birkaç tekrarlanan sorgu içeren günlük bir brifing için önbellek, ilk oturumdan sonra API çağrılarının çoğunu ortadan kaldırır.

## PDF Özet Üretimi

PDF dışa aktarımı, ikili bağımlılığı olmayan, bakımı sürdürülen bir Python PDF kütüphanesi olan [fpdf2](https://py-pdf.github.io/fpdf2/) kullanır:

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

`multi_cell()`, satır kaydırmayı ve otomatik sayfa sonlarını ele alır; böylece her uzunluktaki oturum, elle sayfalama mantığı olmadan iyi biçimlendirilmiş bir belge üretir. Çıktı, standart Helvetica ölçümleri dışında gömülü yazı tipi içermeyen, PDF/A uyumlu bir dosyadır.

## Gizlilik Modeli

Àkàndé'deki gizlilik sınırı üç olguyla tanımlanır:

1. Ses, HTTPS üzerinden Whisper API'sine gönderilir ve API çağrısının ötesinde OpenAI tarafından saklanmaz (Şubat 2024 itibarıyla OpenAI'nin API veri kullanım politikasına göre).
2. Chat Completions API çağrıları, çok turlu oturumlar için tüm konuşma geçmişini içerebilen oturum `messages` listesini iletir.
3. SQLite veritabanı ve PDF dosyaları tamamen yerel dosya sisteminde bulunur; herhangi bir bulut hizmetine arka planda eşitleme gerçekleşmez.

Hassas konuları içeren yönetici kullanım durumları için (birleşme ve satın alma görüşmeleri, personel meseleleri, düzenleyici strateji) API'ye iletilen oturum geçmişi, dağıtımdan önce kuruluşun yapay zekâ kullanım politikasına göre gözden geçirilmelidir. Sistem istemindeki `max_tokens` sınırı, amaçlanan ifşa kapsamını aşan bağlamın istemeden iletilmesini önlemek için kullanılabilir.

## Sıkça Sorulan Sorular

**Àkàndé, oturum sona erdikten sonra konuşma geçmişini saklar mı?**
Bellekteki `messages` listesi, işlem sona erdiğinde atılır. Konuşma geçmişi yalnızca kullanıcı bir PDF dışa aktarımı tetiklerse veya özel bir kalıcılık katmanı eklenirse saklanır. SQLite önbelleği, tam konuşma bağlamını değil, sorgu karmalarını ve yanıt metnini saklar.

**Önbellek, benzer ancak aynı olmayan sorguları nasıl ele alır?**
Önbellek, normalleştirilmiş sorgu dizesi üzerinde tam eşleşme karması kullanır. Tek bir kelimeyle farklılık gösteren iki sorgu farklı karmalar üretir ve ayrı API çağrılarıyla sonuçlanır. Anlamsal önbellekleme (neredeyse yinelenen sorguları eşleştirmek için gömme benzerliği kullanarak) ek bir vektör arama adımı gerektirir ve temel uygulamanın parçası değildir.

**Àkàndé varsayılan olarak hangi GPT modelini kullanır?**
Varsayılan, Şubat 2024 itibarıyla `gpt-4-turbo-preview`'dur. Model adı bir yapılandırma parametresidir, bu nedenle herhangi bir OpenAI sohbet tamamlama modeli değiştirilebilir. `gpt-3.5-turbo`'ya geçmek, token başına API maliyetini yaklaşık 20 kat azaltır ancak karmaşık çok adımlı sorgular için akıl yürütme kalitesini düşürür.

**PDF dışa aktarım biçimi özelleştirilebilir mi?**
Evet. fpdf2 dışa aktarım fonksiyonu, tek gerekli girdisi olarak `messages` listesini kabul eder; bu nedenle yazı tipi, kenar boşlukları, sayfa boyutu, üstbilgi içeriği ve etiketleme, dışa aktarım fonksiyonu düzenlenerek değiştirilebilir. fpdf2 ayrıca görüntü, tablo ve Unicode yazı tipleri eklemeyi destekler; bu da belirli markalama gereksinimleri olan kuruluşlar için daha zengin belge düzenlerine olanak tanır.

## Kaynaklar

1. OpenAI. *Audio Transcriptions — Whisper API*. OpenAI Platform Documentation, 2024. https://platform.openai.com/docs/api-reference/audio/createTranscription
2. OpenAI. *Chat Completions API*. OpenAI Platform Documentation, 2024. https://platform.openai.com/docs/api-reference/chat/create
3. Voss, J. et al. *fpdf2: Modern PDF generation for Python*. GitHub, 2024. https://github.com/py-pdf/fpdf2
4. SQLite Consortium. *SQLite Documentation*. sqlite.org, 2024. https://www.sqlite.org/docs.html

[00]: https://akande.co "Àkàndé Voice Assistant"
