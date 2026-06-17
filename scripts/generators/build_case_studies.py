#!/usr/bin/env python3
"""Generate outcome-led case-study pages under ``public/case-studies/``.

Phase 1 of the Authority Playbook (see plan §1). Each case study is a
data file in ``_data/proof/case-studies/<slug>.yml`` rendered into a
standalone HTML document sharing the FT-tier ``/articles/`` shell — so
the typography, accessibility, and CSP profile stay identical to the
rest of the site.

The page structure follows the plan's exact order:
    Problem → Role → What I built → Outcomes / Engineering rigour →
    External validation → Standards → Links → Related articles

Outputs:
    public/case-studies/index.html            hub listing every study
    public/case-studies/<slug>/index.html    one per data file

Inputs:
    _data/proof/case-studies/*.yml           case-study data (source of truth)
    _data/proof/metrics.json                 build-time metrics (optional)
    public/articles/index.html               FT-tier shell template

Runs in ``build.sh`` after ``ssg`` has emitted the articles shell, and
before ``build_translations`` so the locale-fork pass can pick the
case-study pages up.
"""

from __future__ import annotations

import argparse
import html as _html
import json
import re
import sys
from pathlib import Path

try:
    import yaml  # type: ignore[import-untyped]
except ImportError:
    print("error: PyYAML not installed (see requirements.txt)", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
DATA_DIR = ROOT / "_data" / "proof" / "case-studies"
METRICS_PATH = ROOT / "_data" / "proof" / "metrics.json"
SHELL_SRC = PUBLIC / "articles" / "index.html"
OUT_DIR = PUBLIC / "case-studies"

# Per-locale section headings + meta-row labels. The case-study YAML
# body content (Problem prose, What-I-built prose, validation bullets)
# stays in EN — those are signed statements of fact that need a careful
# human translation pass. Section frames and labels translate now so
# every locale fork at /<lang>/<localised>/ is properly chrome-localised.
_CS_LABELS: dict[str, dict[str, str]] = {
    "en":      {"eyebrow":"CASE STUDY","eyebrow_plural":"CASE STUDIES","Case studies":"Case studies","Role":"Role","Period":"Period","Status":"Status","Problem":"Problem","What I built":"What I built","Engineering rigour":"Engineering rigour","Signal":"Signal","Evidence":"Evidence","External validation":"External validation","Standards":"Standards","Links":"Links","Related articles":"Related articles","deck":"Outcome-led case studies for the open-source libraries and product programmes shipped at sebastienrousseau.com — each entry leads with externally verifiable rigour signals.","count":"{n} case studies"},
    "ar":      {"eyebrow":"دراسة حالة","eyebrow_plural":"دراسات الحالة","Case studies":"دراسات الحالة","Role":"الدور","Period":"الفترة","Status":"الحالة","Problem":"المشكلة","What I built":"ما الذي بنيته","Engineering rigour":"الصرامة الهندسية","Signal":"إشارة","Evidence":"دليل","External validation":"التحقق الخارجي","Standards":"المعايير","Links":"الروابط","Related articles":"مقالات ذات صلة","deck":"دراسات حالة موجَّهة بالنتائج لمكتبات المصدر المفتوح وبرامج المنتجات التي تُشحن على sebastienrousseau.com — يُقدِّم كل مدخل إشارات صرامة قابلة للتحقق خارجياً.","count":"{n} دراسات حالة"},
    "bn":      {"eyebrow":"কেস স্টাডি","eyebrow_plural":"কেস স্টাডিজ","Case studies":"কেস স্টাডিজ","Role":"ভূমিকা","Period":"সময়কাল","Status":"অবস্থা","Problem":"সমস্যা","What I built":"আমি যা তৈরি করেছি","Engineering rigour":"প্রকৌশল কঠোরতা","Signal":"সংকেত","Evidence":"প্রমাণ","External validation":"বাহ্যিক যাচাইকরণ","Standards":"মান","Links":"লিঙ্ক","Related articles":"সম্পর্কিত নিবন্ধ","deck":"sebastienrousseau.com-এ প্রকাশিত ওপেন-সোর্স লাইব্রেরি এবং পণ্য প্রোগ্রামগুলির জন্য ফলাফল-নেতৃত্বাধীন কেস স্টাডি — প্রতিটি এন্ট্রি বাহ্যিকভাবে যাচাইযোগ্য কঠোরতা সংকেতের সাথে নেতৃত্ব দেয়।","count":"{n} কেস স্টাডিজ"},
    "cs":      {"eyebrow":"PŘÍPADOVÁ STUDIE","eyebrow_plural":"PŘÍPADOVÉ STUDIE","Case studies":"Případové studie","Role":"Role","Period":"Období","Status":"Stav","Problem":"Problém","What I built":"Co jsem postavil","Engineering rigour":"Inženýrská přísnost","Signal":"Signál","Evidence":"Důkaz","External validation":"Externí validace","Standards":"Standardy","Links":"Odkazy","Related articles":"Související články","deck":"Případové studie zaměřené na výsledky pro open-source knihovny a produktové programy dodávané na sebastienrousseau.com — každá položka vede s externě ověřitelnými signály přísnosti.","count":"{n} případových studií"},
    "de":      {"eyebrow":"FALLSTUDIE","eyebrow_plural":"FALLSTUDIEN","Case studies":"Fallstudien","Role":"Rolle","Period":"Zeitraum","Status":"Status","Problem":"Problem","What I built":"Was ich gebaut habe","Engineering rigour":"Engineering-Strenge","Signal":"Signal","Evidence":"Nachweis","External validation":"Externe Validierung","Standards":"Standards","Links":"Links","Related articles":"Verwandte Artikel","deck":"Ergebnisorientierte Fallstudien zu den auf sebastienrousseau.com veröffentlichten Open-Source-Bibliotheken und Produktprogrammen — jeder Eintrag beginnt mit extern verifizierbaren Strenge-Signalen.","count":"{n} Fallstudien"},
    "es":      {"eyebrow":"CASO DE ESTUDIO","eyebrow_plural":"CASOS DE ESTUDIO","Case studies":"Casos de estudio","Role":"Rol","Period":"Periodo","Status":"Estado","Problem":"Problema","What I built":"Lo que construí","Engineering rigour":"Rigor de ingeniería","Signal":"Señal","Evidence":"Evidencia","External validation":"Validación externa","Standards":"Normas","Links":"Enlaces","Related articles":"Artículos relacionados","deck":"Casos de estudio orientados a resultados para las bibliotecas de código abierto y programas de producto publicados en sebastienrousseau.com — cada entrada se abre con señales de rigor verificables externamente.","count":"{n} casos de estudio"},
    "fil":     {"eyebrow":"CASE STUDY","eyebrow_plural":"MGA CASE STUDY","Case studies":"Mga case study","Role":"Tungkulin","Period":"Panahon","Status":"Katayuan","Problem":"Suliranin","What I built":"Ang ginawa ko","Engineering rigour":"Mahigpit na inhinyeriya","Signal":"Senyas","Evidence":"Patunay","External validation":"Panlabas na pagpapatunay","Standards":"Mga pamantayan","Links":"Mga link","Related articles":"Mga kaugnay na artikulo","deck":"Mga case study na nakabatay sa resulta para sa mga open-source na library at programa ng produktong inilalabas sa sebastienrousseau.com — bawat entry ay pinangungunahan ng panlabas na napapatunayang mga senyas ng higpit.","count":"{n} mga case study"},
    "fr":      {"eyebrow":"ÉTUDE DE CAS","eyebrow_plural":"ÉTUDES DE CAS","Case studies":"Études de cas","Role":"Rôle","Period":"Période","Status":"Statut","Problem":"Problème","What I built":"Ce que j'ai construit","Engineering rigour":"Rigueur d'ingénierie","Signal":"Signal","Evidence":"Preuve","External validation":"Validation externe","Standards":"Normes","Links":"Liens","Related articles":"Articles connexes","deck":"Études de cas axées sur les résultats pour les bibliothèques open-source et les programmes produits livrés sur sebastienrousseau.com — chaque entrée s'ouvre sur des signaux de rigueur vérifiables par des tiers.","count":"{n} études de cas"},
    "ha":      {"eyebrow":"NAZARI","eyebrow_plural":"NAZARIN SHARI'A","Case studies":"Nazarin shari'a","Role":"Matsayi","Period":"Lokaci","Status":"Hali","Problem":"Matsala","What I built":"Abin da na gina","Engineering rigour":"Tsananin injiniya","Signal":"Sigina","Evidence":"Hujja","External validation":"Tabbatarwa daga waje","Standards":"Ka'idoji","Links":"Hanyoyi","Related articles":"Labarai masu alaƙa","deck":"Nazarin shari'a da aka mai da hankali kan sakamako don dakunan karatu masu buɗaɗɗen tushe da shirye-shiryen samfuri da aka kawo a sebastienrousseau.com — kowane shigarwa yana farawa da sigina na tsanani waɗanda za a iya tabbatarwa daga waje.","count":"nazarin shari'a {n}"},
    "he":      {"eyebrow":"מקרה בוחן","eyebrow_plural":"מקרי בוחן","Case studies":"מקרי בוחן","Role":"תפקיד","Period":"תקופה","Status":"מצב","Problem":"בעיה","What I built":"מה שבניתי","Engineering rigour":"קפדנות הנדסית","Signal":"אות","Evidence":"ראיה","External validation":"אימות חיצוני","Standards":"תקנים","Links":"קישורים","Related articles":"מאמרים קשורים","deck":"מקרי בוחן ממוקדי-תוצאה לספריות הקוד הפתוח ולתוכניות המוצר המתפרסמות ב-sebastienrousseau.com — כל ערך נפתח באותות קפדנות הניתנים לאימות חיצוני.","count":"{n} מקרי בוחן"},
    "hi":      {"eyebrow":"केस स्टडी","eyebrow_plural":"केस स्टडीज़","Case studies":"केस स्टडीज़","Role":"भूमिका","Period":"अवधि","Status":"स्थिति","Problem":"समस्या","What I built":"मैंने जो बनाया","Engineering rigour":"इंजीनियरिंग की कठोरता","Signal":"संकेत","Evidence":"प्रमाण","External validation":"बाहरी सत्यापन","Standards":"मानक","Links":"लिंक","Related articles":"संबंधित लेख","deck":"sebastienrousseau.com पर शिप किए गए ओपन-सोर्स लाइब्रेरीज़ और प्रोडक्ट प्रोग्राम्स के लिए परिणाम-केंद्रित केस स्टडीज़ — हर एंट्री बाहरी रूप से सत्यापन-योग्य कठोरता संकेतों के साथ शुरू होती है।","count":"{n} केस स्टडीज़"},
    "id":      {"eyebrow":"STUDI KASUS","eyebrow_plural":"STUDI KASUS","Case studies":"Studi kasus","Role":"Peran","Period":"Periode","Status":"Status","Problem":"Masalah","What I built":"Apa yang saya bangun","Engineering rigour":"Ketelitian rekayasa","Signal":"Sinyal","Evidence":"Bukti","External validation":"Validasi eksternal","Standards":"Standar","Links":"Tautan","Related articles":"Artikel terkait","deck":"Studi kasus yang berfokus pada hasil untuk pustaka sumber terbuka dan program produk yang dirilis di sebastienrousseau.com — setiap entri dibuka dengan sinyal ketelitian yang dapat diverifikasi secara eksternal.","count":"{n} studi kasus"},
    "it":      {"eyebrow":"CASO DI STUDIO","eyebrow_plural":"CASI DI STUDIO","Case studies":"Casi di studio","Role":"Ruolo","Period":"Periodo","Status":"Stato","Problem":"Problema","What I built":"Cosa ho costruito","Engineering rigour":"Rigore ingegneristico","Signal":"Segnale","Evidence":"Prova","External validation":"Validazione esterna","Standards":"Standard","Links":"Link","Related articles":"Articoli correlati","deck":"Casi di studio orientati ai risultati per le librerie open-source e i programmi di prodotto pubblicati su sebastienrousseau.com — ogni voce si apre con segnali di rigore verificabili dall'esterno.","count":"{n} casi di studio"},
    "ja":      {"eyebrow":"事例研究","eyebrow_plural":"事例研究","Case studies":"事例研究","Role":"役割","Period":"期間","Status":"状態","Problem":"課題","What I built":"構築したもの","Engineering rigour":"エンジニアリングの厳密性","Signal":"指標","Evidence":"証拠","External validation":"第三者検証","Standards":"規格","Links":"リンク","Related articles":"関連記事","deck":"sebastienrousseau.com で公開されているオープンソースライブラリと製品プログラムに関する成果主導の事例研究 — 各エントリは外部で検証可能な厳密性の指標から始まります。","count":"{n} 件の事例研究"},
    "ko":      {"eyebrow":"사례 연구","eyebrow_plural":"사례 연구","Case studies":"사례 연구","Role":"역할","Period":"기간","Status":"상태","Problem":"문제","What I built":"구축한 것","Engineering rigour":"엔지니어링 엄격성","Signal":"지표","Evidence":"증거","External validation":"외부 검증","Standards":"표준","Links":"링크","Related articles":"관련 글","deck":"sebastienrousseau.com에서 발행되는 오픈소스 라이브러리와 제품 프로그램에 대한 성과 중심의 사례 연구 — 각 항목은 외부에서 검증 가능한 엄격성 지표로 시작합니다.","count":"사례 연구 {n}건"},
    "nl":      {"eyebrow":"CASESTUDY","eyebrow_plural":"CASESTUDY'S","Case studies":"Casestudy's","Role":"Rol","Period":"Periode","Status":"Status","Problem":"Probleem","What I built":"Wat ik heb gebouwd","Engineering rigour":"Engineering-precisie","Signal":"Signaal","Evidence":"Bewijs","External validation":"Externe validatie","Standards":"Standaarden","Links":"Links","Related articles":"Verwante artikelen","deck":"Resultaatgerichte casestudy's voor de open-source bibliotheken en productprogramma's die op sebastienrousseau.com worden gepubliceerd — elke vermelding opent met extern verifieerbare precisie-signalen.","count":"{n} casestudy's"},
    "pl":      {"eyebrow":"STUDIUM PRZYPADKU","eyebrow_plural":"STUDIA PRZYPADKÓW","Case studies":"Studia przypadków","Role":"Rola","Period":"Okres","Status":"Status","Problem":"Problem","What I built":"Co zbudowałem","Engineering rigour":"Rygor inżynierski","Signal":"Sygnał","Evidence":"Dowód","External validation":"Walidacja zewnętrzna","Standards":"Standardy","Links":"Linki","Related articles":"Powiązane artykuły","deck":"Studia przypadków skoncentrowane na wynikach dla bibliotek open-source i programów produktowych dostarczanych na sebastienrousseau.com — każdy wpis otwiera sygnałami rygoru weryfikowalnymi zewnętrznie.","count":"{n} studiów przypadków"},
    "pt-br":   {"eyebrow":"ESTUDO DE CASO","eyebrow_plural":"ESTUDOS DE CASO","Case studies":"Estudos de caso","Role":"Função","Period":"Período","Status":"Status","Problem":"Problema","What I built":"O que construí","Engineering rigour":"Rigor de engenharia","Signal":"Sinal","Evidence":"Evidência","External validation":"Validação externa","Standards":"Normas","Links":"Links","Related articles":"Artigos relacionados","deck":"Estudos de caso orientados a resultados para as bibliotecas de código aberto e programas de produto entregues em sebastienrousseau.com — cada entrada abre com sinais de rigor verificáveis externamente.","count":"{n} estudos de caso"},
    "ro":      {"eyebrow":"STUDIU DE CAZ","eyebrow_plural":"STUDII DE CAZ","Case studies":"Studii de caz","Role":"Rol","Period":"Perioadă","Status":"Stare","Problem":"Problemă","What I built":"Ce am construit","Engineering rigour":"Rigoare inginerească","Signal":"Semnal","Evidence":"Dovadă","External validation":"Validare externă","Standards":"Standarde","Links":"Linkuri","Related articles":"Articole conexe","deck":"Studii de caz axate pe rezultate pentru bibliotecile open-source și programele de produs livrate pe sebastienrousseau.com — fiecare intrare se deschide cu semnale de rigoare verificabile extern.","count":"{n} studii de caz"},
    "ru":      {"eyebrow":"КЕЙС","eyebrow_plural":"КЕЙС-СТАДИ","Case studies":"Кейс-стади","Role":"Роль","Period":"Период","Status":"Статус","Problem":"Проблема","What I built":"Что я построил","Engineering rigour":"Инженерная строгость","Signal":"Сигнал","Evidence":"Доказательство","External validation":"Внешняя валидация","Standards":"Стандарты","Links":"Ссылки","Related articles":"Связанные статьи","deck":"Кейс-стади, ориентированные на результат, для библиотек с открытым исходным кодом и продуктовых программ, выпущенных на sebastienrousseau.com — каждая запись начинается с внешне проверяемых сигналов строгости.","count":"{n} кейс-стади"},
    "sv":      {"eyebrow":"FALLSTUDIE","eyebrow_plural":"FALLSTUDIER","Case studies":"Fallstudier","Role":"Roll","Period":"Period","Status":"Status","Problem":"Problem","What I built":"Vad jag byggde","Engineering rigour":"Ingenjörsmässig stringens","Signal":"Signal","Evidence":"Bevis","External validation":"Extern validering","Standards":"Standarder","Links":"Länkar","Related articles":"Relaterade artiklar","deck":"Resultatdrivna fallstudier för de öppna källkods-biblioteken och produktprogrammen som publiceras på sebastienrousseau.com — varje post öppnas med externt verifierbara stringens-signaler.","count":"{n} fallstudier"},
    "th":      {"eyebrow":"กรณีศึกษา","eyebrow_plural":"กรณีศึกษา","Case studies":"กรณีศึกษา","Role":"บทบาท","Period":"ช่วงเวลา","Status":"สถานะ","Problem":"ปัญหา","What I built":"สิ่งที่ฉันสร้าง","Engineering rigour":"ความเข้มงวดทางวิศวกรรม","Signal":"สัญญาณ","Evidence":"หลักฐาน","External validation":"การตรวจสอบจากภายนอก","Standards":"มาตรฐาน","Links":"ลิงก์","Related articles":"บทความที่เกี่ยวข้อง","deck":"กรณีศึกษาที่มุ่งเน้นผลลัพธ์สำหรับไลบรารีโอเพนซอร์สและโปรแกรมผลิตภัณฑ์ที่ส่งมอบบน sebastienrousseau.com — แต่ละรายการเปิดด้วยสัญญาณความเข้มงวดที่ตรวจสอบได้จากภายนอก","count":"กรณีศึกษา {n} รายการ"},
    "tr":      {"eyebrow":"VAKA ÇALIŞMASI","eyebrow_plural":"VAKA ÇALIŞMALARI","Case studies":"Vaka çalışmaları","Role":"Rol","Period":"Dönem","Status":"Durum","Problem":"Problem","What I built":"Ne inşa ettim","Engineering rigour":"Mühendislik titizliği","Signal":"Sinyal","Evidence":"Kanıt","External validation":"Harici doğrulama","Standards":"Standartlar","Links":"Bağlantılar","Related articles":"İlgili makaleler","deck":"sebastienrousseau.com'da yayınlanan açık kaynak kütüphaneler ve ürün programları için sonuç odaklı vaka çalışmaları — her giriş dışarıdan doğrulanabilir titizlik sinyalleriyle başlar.","count":"{n} vaka çalışması"},
    "uk":      {"eyebrow":"КЕЙС","eyebrow_plural":"КЕЙС-СТАДІ","Case studies":"Кейс-стаді","Role":"Роль","Period":"Період","Status":"Статус","Problem":"Проблема","What I built":"Що я побудував","Engineering rigour":"Інженерна строгість","Signal":"Сигнал","Evidence":"Доказ","External validation":"Зовнішня валідація","Standards":"Стандарти","Links":"Посилання","Related articles":"Пов'язані статті","deck":"Кейс-стаді, орієнтовані на результат, для бібліотек з відкритим вихідним кодом і продуктових програм, опублікованих на sebastienrousseau.com — кожен запис починається із зовнішньо перевірюваних сигналів строгості.","count":"{n} кейс-стаді"},
    "vi":      {"eyebrow":"NGHIÊN CỨU TÌNH HUỐNG","eyebrow_plural":"NGHIÊN CỨU TÌNH HUỐNG","Case studies":"Nghiên cứu tình huống","Role":"Vai trò","Period":"Giai đoạn","Status":"Trạng thái","Problem":"Vấn đề","What I built":"Những gì tôi đã xây dựng","Engineering rigour":"Sự nghiêm ngặt kỹ thuật","Signal":"Tín hiệu","Evidence":"Bằng chứng","External validation":"Xác minh bên ngoài","Standards":"Tiêu chuẩn","Links":"Liên kết","Related articles":"Bài viết liên quan","deck":"Các nghiên cứu tình huống dựa trên kết quả cho các thư viện mã nguồn mở và chương trình sản phẩm được phát hành tại sebastienrousseau.com — mỗi mục mở đầu bằng các tín hiệu nghiêm ngặt có thể kiểm chứng từ bên ngoài.","count":"{n} nghiên cứu tình huống"},
    "yo":      {"eyebrow":"ÌWADÌ-ÀPẸẸRẸ","eyebrow_plural":"ÀWỌN ÌWADÌ-ÀPẸẸRẸ","Case studies":"Iwadi àpẹẹrẹ","Role":"Ipa","Period":"Àkókò","Status":"Ipo","Problem":"Ìṣòro","What I built":"Ohun tí mo kọ́","Engineering rigour":"Ìmùúrasílẹ̀ ìmọ̀-ẹ̀rọ","Signal":"Àmì","Evidence":"Ẹ̀rí","External validation":"Ìfọwọ́sí ìta","Standards":"Ìlànà","Links":"Awọn ìjápọ̀","Related articles":"Àwọn àpilẹ̀kọ tó jọmọ́","deck":"Àwọn ìwadì-àpẹẹrẹ tí ó dá lórí àbájáde fún àwọn ilé-ìkàwé orísun ṣíṣí àti àwọn ètò ọjà tí a fi ránṣẹ́ ní sebastienrousseau.com — ẹ̀kọ́ kọ̀ọ̀kan máa ń bẹ̀rẹ̀ pẹ̀lú àmì ìmùúrasílẹ̀ tí a lè jẹ́ kí ẹnikẹ́ni jẹ́rìí sí láti ìta.","count":"{n} ìwadì-àpẹẹrẹ"},
    "zh-hans": {"eyebrow":"案例研究","eyebrow_plural":"案例研究","Case studies":"案例研究","Role":"角色","Period":"周期","Status":"状态","Problem":"问题","What I built":"我构建了什么","Engineering rigour":"工程严谨性","Signal":"信号","Evidence":"证据","External validation":"外部验证","Standards":"标准","Links":"链接","Related articles":"相关文章","deck":"针对在 sebastienrousseau.com 发布的开源库与产品计划的成果导向案例研究——每一条目均以可外部验证的严谨性信号开篇。","count":"{n} 个案例研究"},
    "zh-hant": {"eyebrow":"案例研究","eyebrow_plural":"案例研究","Case studies":"案例研究","Role":"角色","Period":"週期","Status":"狀態","Problem":"問題","What I built":"我建構了什麼","Engineering rigour":"工程嚴謹性","Signal":"信號","Evidence":"證據","External validation":"外部驗證","Standards":"標準","Links":"連結","Related articles":"相關文章","deck":"針對在 sebastienrousseau.com 發布的開源函式庫與產品計劃的成果導向案例研究——每一條目均以可外部驗證的嚴謹性信號開篇。","count":"{n} 個案例研究"},
}

# Extra labels introduced for the Bloomberg-tier elevation. Kept as a
# second dict so the diff stays small + the original 28-row table above
# remains a single line per locale. Merged into the active locale's
# label set at render time. Missing keys fall back to EN.
_CS_LABELS_V2: dict[str, dict[str, str]] = {
    "en":      {"Home":"Home","Sector":"Sector","Read case study":"Read case study","By the numbers":"By the numbers","Independently verified":"Independently verified","Aligned standards":"Aligned standards","Verifiable links":"Verifiable links","More case studies":"More case studies","Trusted by":"Trusted by","Filter by category":"Filter by category","All categories":"All categories","Share on X":"Share on X","Share on LinkedIn":"Share on LinkedIn","Copy link":"Copy link","Share":"Share","Featured":"Featured","Categories":"Categories","Case study":"Case study","Verified":"Verified"},
    "ar":      {"Home":"الرئيسية","Sector":"القطاع","Read case study":"اقرأ دراسة الحالة","By the numbers":"بالأرقام","Independently verified":"تم التحقق منه بشكل مستقل","Aligned standards":"المعايير المتوافقة","Verifiable links":"روابط قابلة للتحقق","More case studies":"المزيد من دراسات الحالة","Trusted by":"موثوق من قبل","Filter by category":"تصفية حسب الفئة","All categories":"كل الفئات","Share on X":"مشاركة على X","Share on LinkedIn":"مشاركة على LinkedIn","Copy link":"نسخ الرابط","Share":"مشاركة","Featured":"مميز","Categories":"الفئات","Case study":"دراسة حالة","Verified":"تم التحقق"},
    "bn":      {"Home":"হোম","Sector":"সেক্টর","Read case study":"কেস স্টাডি পড়ুন","By the numbers":"সংখ্যার মাধ্যমে","Independently verified":"স্বাধীনভাবে যাচাইকৃত","Aligned standards":"সংযুক্ত মান","Verifiable links":"যাচাইযোগ্য লিঙ্ক","More case studies":"আরও কেস স্টাডি","Trusted by":"বিশ্বাস করেন","Filter by category":"বিভাগ অনুসারে ফিল্টার করুন","All categories":"সব বিভাগ","Share on X":"X-এ শেয়ার করুন","Share on LinkedIn":"LinkedIn-এ শেয়ার করুন","Copy link":"লিঙ্ক কপি করুন","Share":"শেয়ার করুন","Featured":"বৈশিষ্ট্যযুক্ত","Categories":"বিভাগ","Case study":"কেস স্টাডি","Verified":"যাচাইকৃত"},
    "cs":      {"Home":"Domů","Sector":"Sektor","Read case study":"Přečíst případovou studii","By the numbers":"V číslech","Independently verified":"Nezávisle ověřeno","Aligned standards":"Sladěné standardy","Verifiable links":"Ověřitelné odkazy","More case studies":"Další případové studie","Trusted by":"Důvěřují","Filter by category":"Filtrovat podle kategorie","All categories":"Všechny kategorie","Share on X":"Sdílet na X","Share on LinkedIn":"Sdílet na LinkedIn","Copy link":"Kopírovat odkaz","Share":"Sdílet","Featured":"Doporučeno","Categories":"Kategorie","Case study":"Případová studie","Verified":"Ověřeno"},
    "de":      {"Home":"Start","Sector":"Sektor","Read case study":"Fallstudie lesen","By the numbers":"In Zahlen","Independently verified":"Unabhängig verifiziert","Aligned standards":"Angepasste Standards","Verifiable links":"Verifizierbare Links","More case studies":"Weitere Fallstudien","Trusted by":"Vertraut von","Filter by category":"Nach Kategorie filtern","All categories":"Alle Kategorien","Share on X":"Auf X teilen","Share on LinkedIn":"Auf LinkedIn teilen","Copy link":"Link kopieren","Share":"Teilen","Featured":"Vorgestellt","Categories":"Kategorien","Case study":"Fallstudie","Verified":"Verifiziert"},
    "es":      {"Home":"Inicio","Sector":"Sector","Read case study":"Leer caso de estudio","By the numbers":"En cifras","Independently verified":"Verificado independientemente","Aligned standards":"Normas alineadas","Verifiable links":"Enlaces verificables","More case studies":"Más casos de estudio","Trusted by":"De confianza para","Filter by category":"Filtrar por categoría","All categories":"Todas las categorías","Share on X":"Compartir en X","Share on LinkedIn":"Compartir en LinkedIn","Copy link":"Copiar enlace","Share":"Compartir","Featured":"Destacado","Categories":"Categorías","Case study":"Caso de estudio","Verified":"Verificado"},
    "fil":     {"Home":"Tahanan","Sector":"Sektor","Read case study":"Basahin ang case study","By the numbers":"Sa mga numero","Independently verified":"Naberipikang malaya","Aligned standards":"Naaayon na pamantayan","Verifiable links":"Mga link na nababerypika","More case studies":"Higit pang case study","Trusted by":"Pinagkakatiwalaan ng","Filter by category":"Salain ayon sa kategorya","All categories":"Lahat ng kategorya","Share on X":"Ibahagi sa X","Share on LinkedIn":"Ibahagi sa LinkedIn","Copy link":"Kopyahin ang link","Share":"Ibahagi","Featured":"Tampok","Categories":"Mga kategorya","Case study":"Case study","Verified":"Naberipika"},
    "fr":      {"Home":"Accueil","Sector":"Secteur","Read case study":"Lire l'étude de cas","By the numbers":"En chiffres","Independently verified":"Vérifié indépendamment","Aligned standards":"Normes alignées","Verifiable links":"Liens vérifiables","More case studies":"Autres études de cas","Trusted by":"Approuvé par","Filter by category":"Filtrer par catégorie","All categories":"Toutes les catégories","Share on X":"Partager sur X","Share on LinkedIn":"Partager sur LinkedIn","Copy link":"Copier le lien","Share":"Partager","Featured":"À la une","Categories":"Catégories","Case study":"Étude de cas","Verified":"Vérifié"},
    "ha":      {"Home":"Gida","Sector":"Sashe","Read case study":"Karanta nazarin shari'a","By the numbers":"Da lambobi","Independently verified":"An tabbatar da kansa","Aligned standards":"Ka'idoji da suka dace","Verifiable links":"Hanyoyi masu tabbatuwa","More case studies":"Karin nazarin shari'a","Trusted by":"Amintacce ta","Filter by category":"Tace ta nau'i","All categories":"Dukkan nau'i","Share on X":"Raba a X","Share on LinkedIn":"Raba a LinkedIn","Copy link":"Kwafi hanyar haɗi","Share":"Raba","Featured":"Wanda aka zaba","Categories":"Nau'i","Case study":"Nazari","Verified":"An tabbatar"},
    "he":      {"Home":"דף הבית","Sector":"מגזר","Read case study":"קרא מקרה בוחן","By the numbers":"במספרים","Independently verified":"אומת באופן עצמאי","Aligned standards":"תקנים מיושרים","Verifiable links":"קישורים ניתנים לאימות","More case studies":"מקרי בוחן נוספים","Trusted by":"זוכה לאמון","Filter by category":"סנן לפי קטגוריה","All categories":"כל הקטגוריות","Share on X":"שתף ב-X","Share on LinkedIn":"שתף ב-LinkedIn","Copy link":"העתק קישור","Share":"שתף","Featured":"מומלץ","Categories":"קטגוריות","Case study":"מקרה בוחן","Verified":"מאומת"},
    "hi":      {"Home":"होम","Sector":"क्षेत्र","Read case study":"केस स्टडी पढ़ें","By the numbers":"संख्या में","Independently verified":"स्वतंत्र रूप से सत्यापित","Aligned standards":"संरेखित मानक","Verifiable links":"सत्यापन योग्य लिंक","More case studies":"अधिक केस स्टडीज़","Trusted by":"विश्वसनीय","Filter by category":"श्रेणी से फ़िल्टर करें","All categories":"सभी श्रेणियां","Share on X":"X पर साझा करें","Share on LinkedIn":"LinkedIn पर साझा करें","Copy link":"लिंक कॉपी करें","Share":"साझा करें","Featured":"विशेष","Categories":"श्रेणियाँ","Case study":"केस स्टडी","Verified":"सत्यापित"},
    "id":      {"Home":"Beranda","Sector":"Sektor","Read case study":"Baca studi kasus","By the numbers":"Dalam angka","Independently verified":"Diverifikasi secara independen","Aligned standards":"Standar yang selaras","Verifiable links":"Tautan yang dapat diverifikasi","More case studies":"Studi kasus lainnya","Trusted by":"Dipercaya oleh","Filter by category":"Filter berdasarkan kategori","All categories":"Semua kategori","Share on X":"Bagikan di X","Share on LinkedIn":"Bagikan di LinkedIn","Copy link":"Salin tautan","Share":"Bagikan","Featured":"Pilihan","Categories":"Kategori","Case study":"Studi kasus","Verified":"Terverifikasi"},
    "it":      {"Home":"Home","Sector":"Settore","Read case study":"Leggi il caso di studio","By the numbers":"In cifre","Independently verified":"Verificato in modo indipendente","Aligned standards":"Standard allineati","Verifiable links":"Link verificabili","More case studies":"Altri casi di studio","Trusted by":"Scelto da","Filter by category":"Filtra per categoria","All categories":"Tutte le categorie","Share on X":"Condividi su X","Share on LinkedIn":"Condividi su LinkedIn","Copy link":"Copia link","Share":"Condividi","Featured":"In evidenza","Categories":"Categorie","Case study":"Caso di studio","Verified":"Verificato"},
    "ja":      {"Home":"ホーム","Sector":"セクター","Read case study":"事例研究を読む","By the numbers":"数字で見る","Independently verified":"独立検証済み","Aligned standards":"準拠する規格","Verifiable links":"検証可能なリンク","More case studies":"他の事例研究","Trusted by":"信頼を寄せる","Filter by category":"カテゴリで絞り込み","All categories":"すべてのカテゴリ","Share on X":"X で共有","Share on LinkedIn":"LinkedIn で共有","Copy link":"リンクをコピー","Share":"共有","Featured":"注目","Categories":"カテゴリ","Case study":"事例研究","Verified":"検証済み"},
    "ko":      {"Home":"홈","Sector":"분야","Read case study":"사례 연구 읽기","By the numbers":"숫자로 보기","Independently verified":"독립적으로 검증됨","Aligned standards":"준수 표준","Verifiable links":"검증 가능한 링크","More case studies":"더 많은 사례 연구","Trusted by":"신뢰","Filter by category":"카테고리로 필터링","All categories":"모든 카테고리","Share on X":"X에 공유","Share on LinkedIn":"LinkedIn에 공유","Copy link":"링크 복사","Share":"공유","Featured":"추천","Categories":"카테고리","Case study":"사례 연구","Verified":"검증됨"},
    "nl":      {"Home":"Home","Sector":"Sector","Read case study":"Lees casestudy","By the numbers":"In cijfers","Independently verified":"Onafhankelijk geverifieerd","Aligned standards":"Afgestemde standaarden","Verifiable links":"Verifieerbare links","More case studies":"Meer casestudy's","Trusted by":"Vertrouwd door","Filter by category":"Filteren op categorie","All categories":"Alle categorieën","Share on X":"Delen op X","Share on LinkedIn":"Delen op LinkedIn","Copy link":"Link kopiëren","Share":"Delen","Featured":"Uitgelicht","Categories":"Categorieën","Case study":"Casestudy","Verified":"Geverifieerd"},
    "pl":      {"Home":"Strona główna","Sector":"Sektor","Read case study":"Przeczytaj studium przypadku","By the numbers":"W liczbach","Independently verified":"Zweryfikowane niezależnie","Aligned standards":"Dopasowane standardy","Verifiable links":"Weryfikowalne linki","More case studies":"Więcej studiów przypadków","Trusted by":"Zaufali","Filter by category":"Filtruj według kategorii","All categories":"Wszystkie kategorie","Share on X":"Udostępnij na X","Share on LinkedIn":"Udostępnij na LinkedIn","Copy link":"Kopiuj link","Share":"Udostępnij","Featured":"Wyróżnione","Categories":"Kategorie","Case study":"Studium przypadku","Verified":"Zweryfikowane"},
    "pt-br":   {"Home":"Início","Sector":"Setor","Read case study":"Ler estudo de caso","By the numbers":"Em números","Independently verified":"Verificado independentemente","Aligned standards":"Normas alinhadas","Verifiable links":"Links verificáveis","More case studies":"Mais estudos de caso","Trusted by":"Confiável para","Filter by category":"Filtrar por categoria","All categories":"Todas as categorias","Share on X":"Compartilhar no X","Share on LinkedIn":"Compartilhar no LinkedIn","Copy link":"Copiar link","Share":"Compartilhar","Featured":"Destaque","Categories":"Categorias","Case study":"Estudo de caso","Verified":"Verificado"},
    "ro":      {"Home":"Acasă","Sector":"Sector","Read case study":"Citește studiul de caz","By the numbers":"În cifre","Independently verified":"Verificat independent","Aligned standards":"Standarde aliniate","Verifiable links":"Linkuri verificabile","More case studies":"Mai multe studii de caz","Trusted by":"De încredere pentru","Filter by category":"Filtrează după categorie","All categories":"Toate categoriile","Share on X":"Distribuie pe X","Share on LinkedIn":"Distribuie pe LinkedIn","Copy link":"Copiază link","Share":"Distribuie","Featured":"Recomandat","Categories":"Categorii","Case study":"Studiu de caz","Verified":"Verificat"},
    "ru":      {"Home":"Главная","Sector":"Сектор","Read case study":"Читать кейс","By the numbers":"В цифрах","Independently verified":"Независимо подтверждено","Aligned standards":"Согласованные стандарты","Verifiable links":"Проверяемые ссылки","More case studies":"Больше кейсов","Trusted by":"Доверяют","Filter by category":"Фильтр по категории","All categories":"Все категории","Share on X":"Поделиться в X","Share on LinkedIn":"Поделиться в LinkedIn","Copy link":"Копировать ссылку","Share":"Поделиться","Featured":"Рекомендуем","Categories":"Категории","Case study":"Кейс","Verified":"Проверено"},
    "sv":      {"Home":"Hem","Sector":"Sektor","Read case study":"Läs fallstudie","By the numbers":"I siffror","Independently verified":"Oberoende verifierad","Aligned standards":"Anpassade standarder","Verifiable links":"Verifierbara länkar","More case studies":"Fler fallstudier","Trusted by":"Anlitas av","Filter by category":"Filtrera efter kategori","All categories":"Alla kategorier","Share on X":"Dela på X","Share on LinkedIn":"Dela på LinkedIn","Copy link":"Kopiera länk","Share":"Dela","Featured":"Utvald","Categories":"Kategorier","Case study":"Fallstudie","Verified":"Verifierad"},
    "th":      {"Home":"หน้าแรก","Sector":"ภาคส่วน","Read case study":"อ่านกรณีศึกษา","By the numbers":"ในตัวเลข","Independently verified":"ผ่านการตรวจสอบโดยอิสระ","Aligned standards":"มาตรฐานที่สอดคล้อง","Verifiable links":"ลิงก์ที่ตรวจสอบได้","More case studies":"กรณีศึกษาเพิ่มเติม","Trusted by":"ได้รับความไว้วางใจจาก","Filter by category":"กรองตามหมวดหมู่","All categories":"ทุกหมวดหมู่","Share on X":"แชร์บน X","Share on LinkedIn":"แชร์บน LinkedIn","Copy link":"คัดลอกลิงก์","Share":"แชร์","Featured":"แนะนำ","Categories":"หมวดหมู่","Case study":"กรณีศึกษา","Verified":"ตรวจสอบแล้ว"},
    "tr":      {"Home":"Ana sayfa","Sector":"Sektör","Read case study":"Vaka çalışmasını oku","By the numbers":"Rakamlarla","Independently verified":"Bağımsız doğrulandı","Aligned standards":"Uyumlu standartlar","Verifiable links":"Doğrulanabilir bağlantılar","More case studies":"Daha fazla vaka çalışması","Trusted by":"Güvenilen","Filter by category":"Kategoriye göre filtrele","All categories":"Tüm kategoriler","Share on X":"X'te paylaş","Share on LinkedIn":"LinkedIn'de paylaş","Copy link":"Bağlantıyı kopyala","Share":"Paylaş","Featured":"Öne çıkan","Categories":"Kategoriler","Case study":"Vaka çalışması","Verified":"Doğrulandı"},
    "uk":      {"Home":"Головна","Sector":"Сектор","Read case study":"Читати кейс","By the numbers":"У цифрах","Independently verified":"Незалежно підтверджено","Aligned standards":"Узгоджені стандарти","Verifiable links":"Перевіряні посилання","More case studies":"Більше кейсів","Trusted by":"Довіряють","Filter by category":"Фільтр за категорією","All categories":"Усі категорії","Share on X":"Поділитися на X","Share on LinkedIn":"Поділитися на LinkedIn","Copy link":"Копіювати посилання","Share":"Поділитися","Featured":"Рекомендуємо","Categories":"Категорії","Case study":"Кейс","Verified":"Перевірено"},
    "vi":      {"Home":"Trang chủ","Sector":"Lĩnh vực","Read case study":"Đọc nghiên cứu tình huống","By the numbers":"Bằng những con số","Independently verified":"Được xác minh độc lập","Aligned standards":"Tiêu chuẩn tương thích","Verifiable links":"Liên kết có thể xác minh","More case studies":"Thêm nghiên cứu tình huống","Trusted by":"Được tin dùng bởi","Filter by category":"Lọc theo danh mục","All categories":"Tất cả danh mục","Share on X":"Chia sẻ trên X","Share on LinkedIn":"Chia sẻ trên LinkedIn","Copy link":"Sao chép liên kết","Share":"Chia sẻ","Featured":"Nổi bật","Categories":"Danh mục","Case study":"Nghiên cứu tình huống","Verified":"Đã xác minh"},
    "yo":      {"Home":"Ilé","Sector":"Apá","Read case study":"Ka iwadi àpẹẹrẹ","By the numbers":"Ní àwọn nọ́ńbà","Independently verified":"Ti a fọwọ́sí lọ́tọ̀ọ̀tọ̀","Aligned standards":"Àwọn ìlànà tó bá ara mu","Verifiable links":"Àwọn ìjápọ̀ tó lè jẹ́rìí","More case studies":"Àwọn iwadi àpẹẹrẹ míì","Trusted by":"Èyí tí àwọn yìí gbẹ́kẹ̀lé","Filter by category":"Yan láti inú àwọn kíláàsì","All categories":"Gbogbo àwọn kíláàsì","Share on X":"Pín lórí X","Share on LinkedIn":"Pín lórí LinkedIn","Copy link":"Daako ìjápọ̀","Share":"Pín","Featured":"Tó wà lójú","Categories":"Àwọn kíláàsì","Case study":"Iwadi àpẹẹrẹ","Verified":"Ti a fọwọ́sí"},
    "zh-hans": {"Home":"首页","Sector":"行业","Read case study":"阅读案例研究","By the numbers":"用数字说话","Independently verified":"独立验证","Aligned standards":"对标标准","Verifiable links":"可验证链接","More case studies":"更多案例研究","Trusted by":"获得信任","Filter by category":"按类别筛选","All categories":"全部类别","Share on X":"在 X 上分享","Share on LinkedIn":"在 LinkedIn 上分享","Copy link":"复制链接","Share":"分享","Featured":"精选","Categories":"类别","Case study":"案例研究","Verified":"已验证"},
    "zh-hant": {"Home":"首頁","Sector":"行業","Read case study":"閱讀案例研究","By the numbers":"用數字說話","Independently verified":"獨立驗證","Aligned standards":"對標標準","Verifiable links":"可驗證連結","More case studies":"更多案例研究","Trusted by":"獲得信任","Filter by category":"按類別篩選","All categories":"全部類別","Share on X":"在 X 上分享","Share on LinkedIn":"在 LinkedIn 上分享","Copy link":"複製連結","Share":"分享","Featured":"精選","Categories":"類別","Case study":"案例研究","Verified":"已驗證"},
}

# Stage-composition labels — added when the per-study renderer moved to
# the AKQA-tier staged layout. Kept as a 3rd dict so V1+V2 stay frozen.
_CS_LABELS_V3: dict[str, dict[str, str]] = {
    "en":      {"Next":"Next","Get in touch":"Get in touch","CTA headline":"Want this kind of evidence in your bank?","CTA body":"Architecture reviews, post-quantum migration plans, treasury-API programmes — all signed, all verifiable.","Years banking":"Banking + payments","No fabrication":"Verifiable — no fabrication"},
    "ar":      {"Next":"التالي","Get in touch":"تواصل معنا","CTA headline":"هل تريد هذا النوع من الأدلة في بنكك؟","CTA body":"مراجعات معمارية، خطط هجرة ما بعد الكم، وبرامج واجهات الخزينة — كل ذلك موقّع وقابل للتحقق.","Years banking":"خبرة في الخدمات المصرفية والمدفوعات","No fabrication":"قابل للتحقق — لا اختلاق"},
    "bn":      {"Next":"পরবর্তী","Get in touch":"যোগাযোগ করুন","CTA headline":"আপনার ব্যাংকে এই ধরনের প্রমাণ চান?","CTA body":"স্থাপত্য পর্যালোচনা, কোয়ান্টাম-পরবর্তী মাইগ্রেশন পরিকল্পনা, ট্রেজারি-API প্রোগ্রাম — সব স্বাক্ষরিত, সব যাচাইযোগ্য।","Years banking":"ব্যাংকিং + পেমেন্ট অভিজ্ঞতা","No fabrication":"যাচাইযোগ্য — কোনো বানানো নয়"},
    "cs":      {"Next":"Další","Get in touch":"Kontaktovat","CTA headline":"Chcete tento druh důkazů ve své bance?","CTA body":"Architektonické přehledy, plány migrace na post-kvantovou kryptografii, programy treasury API — vše podepsané, vše ověřitelné.","Years banking":"Bankovnictví a platby","No fabrication":"Ověřitelné — bez fabrikace"},
    "de":      {"Next":"Weiter","Get in touch":"Kontakt aufnehmen","CTA headline":"Möchten Sie diese Art von Nachweisen in Ihrer Bank?","CTA body":"Architektur-Reviews, Post-Quanten-Migrationspläne, Treasury-API-Programme — alle signiert, alle verifizierbar.","Years banking":"Banking + Zahlungsverkehr","No fabrication":"Verifizierbar — keine Erfindung"},
    "es":      {"Next":"Siguiente","Get in touch":"Contactar","CTA headline":"¿Quieres este tipo de evidencia en tu banco?","CTA body":"Revisiones de arquitectura, planes de migración post-cuántica, programas de Treasury API — todo firmado, todo verificable.","Years banking":"Banca + pagos","No fabrication":"Verificable — sin fabricación"},
    "fil":     {"Next":"Susunod","Get in touch":"Makipag-ugnayan","CTA headline":"Gusto mo ng ganitong klaseng ebidensya sa iyong bangko?","CTA body":"Mga pagrepaso sa arkitektura, plano ng post-quantum migration, mga programa ng Treasury API — lahat pinirmahan, lahat napapatunayan.","Years banking":"Banking at pagbabayad","No fabrication":"Napapatunayan — walang gawa-gawa"},
    "fr":      {"Next":"Suivant","Get in touch":"Me contacter","CTA headline":"Vous voulez ce type de preuves dans votre banque ?","CTA body":"Revues d'architecture, plans de migration post-quantique, programmes d'API de trésorerie — tout est signé, tout est vérifiable.","Years banking":"Banque + paiements","No fabrication":"Vérifiable — sans fabrication"},
    "ha":      {"Next":"Na gaba","Get in touch":"Tuntube ni","CTA headline":"Kuna so wannan irin shaida a bankin ku?","CTA body":"Bita na gine-gine, tsare-tsare na ƙaura bayan kima, shirye-shiryen API na ma'aji — duk an sa hannu, duk za a iya tabbatarwa.","Years banking":"Banki da biyan kuɗi","No fabrication":"Za a iya tabbatarwa — babu ƙirƙira"},
    "he":      {"Next":"הבא","Get in touch":"צור קשר","CTA headline":"רוצה ראיות מסוג זה בבנק שלך?","CTA body":"סקירות אדריכלות, תוכניות הגירה פוסט-קוונטית, תוכניות Treasury API — הכל חתום, הכל ניתן לאימות.","Years banking":"בנקאות + תשלומים","No fabrication":"ניתן לאימות — ללא בדיה"},
    "hi":      {"Next":"अगला","Get in touch":"संपर्क करें","CTA headline":"क्या आप अपने बैंक में इस तरह के प्रमाण चाहते हैं?","CTA body":"आर्किटेक्चर समीक्षाएं, पोस्ट-क्वांटम माइग्रेशन योजनाएं, ट्रेजरी-API कार्यक्रम — सभी हस्ताक्षरित, सभी सत्यापन योग्य।","Years banking":"बैंकिंग + भुगतान","No fabrication":"सत्यापन योग्य — कोई गढ़ंत नहीं"},
    "id":      {"Next":"Berikutnya","Get in touch":"Hubungi","CTA headline":"Ingin bukti seperti ini di bank Anda?","CTA body":"Tinjauan arsitektur, rencana migrasi pasca-kuantum, program API Treasury — semua ditandatangani, semua dapat diverifikasi.","Years banking":"Perbankan + pembayaran","No fabrication":"Dapat diverifikasi — tanpa rekayasa"},
    "it":      {"Next":"Avanti","Get in touch":"Contattami","CTA headline":"Vuoi questo tipo di evidenze nella tua banca?","CTA body":"Revisioni di architettura, piani di migrazione post-quantistica, programmi di Treasury API — tutto firmato, tutto verificabile.","Years banking":"Banking + pagamenti","No fabrication":"Verificabile — senza invenzioni"},
    "ja":      {"Next":"次へ","Get in touch":"お問い合わせ","CTA headline":"このような証拠を貴行で実現しませんか？","CTA body":"アーキテクチャレビュー、ポスト量子移行計画、Treasury API プログラム — すべて署名済み、すべて検証可能。","Years banking":"銀行 + 決済","No fabrication":"検証可能 — 捏造なし"},
    "ko":      {"Next":"다음","Get in touch":"문의하기","CTA headline":"귀행에 이런 종류의 증거를 원하십니까?","CTA body":"아키텍처 리뷰, 포스트 양자 마이그레이션 계획, Treasury API 프로그램 — 모두 서명되고 검증 가능합니다.","Years banking":"은행 + 결제","No fabrication":"검증 가능 — 조작 없음"},
    "nl":      {"Next":"Volgende","Get in touch":"Neem contact op","CTA headline":"Wilt u dit soort bewijs in uw bank?","CTA body":"Architectuurbeoordelingen, post-kwantum migratieplannen, Treasury-API-programma's — allemaal ondertekend, allemaal verifieerbaar.","Years banking":"Bankieren + betalingen","No fabrication":"Verifieerbaar — geen verzinsels"},
    "pl":      {"Next":"Dalej","Get in touch":"Skontaktuj się","CTA headline":"Chcesz takiego rodzaju dowodów w swoim banku?","CTA body":"Przeglądy architektury, plany migracji post-kwantowej, programy Treasury API — wszystko podpisane, wszystko weryfikowalne.","Years banking":"Bankowość + płatności","No fabrication":"Weryfikowalne — bez fabrykacji"},
    "pt-br":   {"Next":"Próximo","Get in touch":"Entre em contato","CTA headline":"Quer esse tipo de evidência no seu banco?","CTA body":"Revisões de arquitetura, planos de migração pós-quântica, programas de Treasury API — todos assinados, todos verificáveis.","Years banking":"Bancos + pagamentos","No fabrication":"Verificável — sem fabricação"},
    "ro":      {"Next":"Următorul","Get in touch":"Contactează-mă","CTA headline":"Vrei acest tip de dovezi în banca ta?","CTA body":"Revizuiri de arhitectură, planuri de migrare post-cuantică, programe Treasury API — toate semnate, toate verificabile.","Years banking":"Banking + plăți","No fabrication":"Verificabil — fără fabricație"},
    "ru":      {"Next":"Далее","Get in touch":"Связаться","CTA headline":"Хотите такие же доказательства в вашем банке?","CTA body":"Архитектурные обзоры, планы пост-квантовой миграции, программы Treasury API — всё подписано, всё проверяемо.","Years banking":"Банкинг + платежи","No fabrication":"Проверяемо — без фабрикации"},
    "sv":      {"Next":"Nästa","Get in touch":"Kontakta mig","CTA headline":"Vill du ha den här typen av bevis i din bank?","CTA body":"Arkitekturgranskningar, planer för post-kvantmigrering, Treasury-API-program — allt signerat, allt verifierbart.","Years banking":"Bank + betalningar","No fabrication":"Verifierbar — utan påhittade siffror"},
    "th":      {"Next":"ถัดไป","Get in touch":"ติดต่อ","CTA headline":"ต้องการหลักฐานแบบนี้ในธนาคารของคุณหรือไม่?","CTA body":"การตรวจสอบสถาปัตยกรรม แผนการย้ายระบบหลังควอนตัม โปรแกรม Treasury API — ทั้งหมดได้รับการลงนามและตรวจสอบได้","Years banking":"ธนาคารและการชำระเงิน","No fabrication":"ตรวจสอบได้ — ไม่มีการกุข้อมูล"},
    "tr":      {"Next":"Sonraki","Get in touch":"İletişime geç","CTA headline":"Bu tür kanıtlar bankanızda olsun ister misiniz?","CTA body":"Mimari incelemeler, kuantum sonrası göç planları, Treasury API programları — hepsi imzalı, hepsi doğrulanabilir.","Years banking":"Bankacılık + ödemeler","No fabrication":"Doğrulanabilir — uydurma yok"},
    "uk":      {"Next":"Далі","Get in touch":"Зв'язатися","CTA headline":"Хочете такі ж докази у вашому банку?","CTA body":"Архітектурні огляди, плани постквантової міграції, програми Treasury API — все підписано, все можна перевірити.","Years banking":"Банкінг + платежі","No fabrication":"Перевіряється — без фабрикацій"},
    "vi":      {"Next":"Tiếp theo","Get in touch":"Liên hệ","CTA headline":"Bạn muốn loại bằng chứng này trong ngân hàng của mình?","CTA body":"Đánh giá kiến trúc, kế hoạch di chuyển hậu lượng tử, chương trình Treasury API — tất cả đều được ký, tất cả đều có thể xác minh.","Years banking":"Ngân hàng + thanh toán","No fabrication":"Có thể xác minh — không bịa đặt"},
    "yo":      {"Next":"Tókàn","Get in touch":"Kàn si","CTA headline":"Ṣe o fẹ́ irú ẹ̀rí yìí ní ilé-ìfowópamọ́ rẹ?","CTA body":"Àyẹ̀wò àkànṣe, ètò ìṣílọ́ lẹ́yìn-kuontomu, àwọn ètò Treasury API — gbogbo wọn fọwọ́sí, gbogbo wọn lè jẹ́rìí.","Years banking":"Ìfowópamọ́ àti àwọn ìsanwó","No fabrication":"Lè jẹ́rìí — kò sí ètè"},
    "zh-hans": {"Next":"下一步","Get in touch":"联系我们","CTA headline":"想在贵行实现这种证据吗？","CTA body":"架构评审、后量子迁移规划、Treasury API 项目——全部签名，全部可验证。","Years banking":"银行 + 支付","No fabrication":"可验证——无虚构"},
    "zh-hant": {"Next":"下一步","Get in touch":"聯絡我們","CTA headline":"想在貴行實現這種證據嗎？","CTA body":"架構評審、後量子遷移規劃、Treasury API 專案——全部簽名，全部可驗證。","Years banking":"銀行 + 支付","No fabrication":"可驗證——無虛構"},
}


def _lbl(lang: str) -> dict[str, str]:
    """Merged label set for ``lang`` — V3 keys layered on V2 on V1, with
    EN as the fallback for any missing key across all dicts."""
    base = {**_CS_LABELS["en"], **_CS_LABELS_V2["en"], **_CS_LABELS_V3["en"]}
    v1 = _CS_LABELS.get(lang, _CS_LABELS["en"])
    v2 = _CS_LABELS_V2.get(lang, _CS_LABELS_V2["en"])
    v3 = _CS_LABELS_V3.get(lang, _CS_LABELS_V3["en"])
    return {**base, **v1, **v2, **v3}

_BASE_URL = "https://sebastienrousseau.com"
_TITLE_RE = re.compile(r"<title>[^<]*</title>", re.IGNORECASE)
_DESC_RE = re.compile(
    r'<meta name="description" content="[^"]*"', re.IGNORECASE
)
_CANONICAL_RE = re.compile(
    r'<link rel="canonical" href="[^"]*"', re.IGNORECASE
)
_OG_TITLE_RE = re.compile(
    r'(<meta property="og:title" content=")[^"]*(")', re.IGNORECASE
)
_OG_DESC_RE = re.compile(
    r'(<meta property="og:description" content=")[^"]*(")', re.IGNORECASE
)
_OG_URL_RE = re.compile(
    r'(<meta property="og:url" content=")[^"]*(")', re.IGNORECASE
)
_MAIN_WRAP_RE = re.compile(
    r'(<main\b[^>]*>\s*)<div class="wrap[^"]*">[\s\S]*?</div>(\s*</main>)',
    re.IGNORECASE,
)
_AP_HERO_BLOCK_RE = re.compile(
    r'<section class="ap-hero">[\s\S]*?</section>', re.IGNORECASE
)


def _esc(s: str) -> str:
    return _html.escape(str(s or ""), quote=True)


def _load_studies() -> list[dict]:
    """Load every YAML file under ``_data/proof/case-studies/`` and
    return them as dicts. Empty list if the directory is missing.
    Per-locale overlays under ``i18n/<lang>/<slug>.yml`` are loaded
    separately and merged at render time via ``_localised_study``."""
    if not DATA_DIR.is_dir():
        return []
    studies = []
    for path in sorted(DATA_DIR.glob("*.yml")):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            print(f"build_case_studies: skip {path.name} — {exc}", file=sys.stderr)
            continue
        if not data.get("slug"):
            print(f"build_case_studies: skip {path.name} — missing slug", file=sys.stderr)
            continue
        studies.append(data)
    return studies


def _load_overlay(lang: str, slug: str) -> dict:
    """Load a per-locale overlay YAML if it exists. Returns {} if missing
    or unreadable — caller falls back to EN content."""
    if lang == "en":
        return {}
    path = DATA_DIR / "i18n" / lang / f"{slug}.yml"
    if not path.is_file():
        return {}
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        print(f"build_case_studies: overlay parse failed {path} — {exc}", file=sys.stderr)
        return {}


_OVERLAY_KEEP_EN = frozenset({
    "slug", "banner", "category_slug", "links",
    "related_articles", "signed", "period",
    "outcome_highlights_keep_values", "standards",
})
_OVERLAY_LIST_FIELDS = frozenset({"outcome_highlights", "rigour"})


def _merge_list_of_dicts(base: list, overlay_rows: list) -> list[dict]:
    """Zip overlay rows over base rows so a translator can override
    just the prose ``label`` / ``metric`` keys without restating
    ``value``."""
    merged: list[dict] = []
    for i, base_row in enumerate(list(base) or []):
        row = dict(base_row) if isinstance(base_row, dict) else {}
        if i < len(overlay_rows) and isinstance(overlay_rows[i], dict):
            row.update(overlay_rows[i])
        merged.append(row)
    return merged


def _merge_overlay(study: dict, overlay: dict) -> dict:
    """Return a copy of ``study`` with fields from ``overlay`` substituted.
    List-of-dicts fields (outcome_highlights, rigour) are zipped index-by-
    index so partial overlays still work. Scalar / list-of-string fields
    are simple replacements. URLs, slugs, banner image, signed flag, and
    related_articles stay EN-canonical."""
    if not overlay:
        return study
    out = dict(study)
    for key, val in overlay.items():
        if key in _OVERLAY_KEEP_EN:
            continue
        if key in _OVERLAY_LIST_FIELDS and isinstance(val, list):
            out[key] = _merge_list_of_dicts(study.get(key) or [], val)
        else:
            out[key] = val
    return out


def _localised_study(study: dict, lang: str) -> dict:
    """Return ``study`` merged with its per-locale overlay (if any)."""
    return _merge_overlay(study, _load_overlay(lang, study["slug"]))


def _load_metrics() -> dict:
    if not METRICS_PATH.is_file():
        return {}
    try:
        return json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _hub_url(lang: str, url_segment: str) -> str:
    return "/case-studies/" if lang == "en" else f"/{lang}/{url_segment}/"


def _study_url(lang: str, url_segment: str, slug: str) -> str:
    return (
        f"/case-studies/{slug}/"
        if lang == "en"
        else f"/{lang}/{url_segment}/{slug}/"
    )


def _related_article_href(slug: str, lang: str, article_slug_map: dict[str, str]) -> str:
    target_slug = article_slug_map.get(slug, slug) if lang != "en" else slug
    return f"/{slug}/" if lang == "en" else f"/{lang}/{target_slug}/"


def _render_breadcrumb(
    lbl: dict[str, str], lang: str, url_segment: str, current: str | None = None
) -> str:
    sep = '<span aria-hidden="true"> › </span>'
    home_href = "/" if lang == "en" else f"/{lang}/"
    hub_href = _hub_url(lang, url_segment)
    parts = [
        f'<a href="{home_href}">{_esc(lbl["Home"])}</a>{sep}',
        f'<a href="{hub_href}">{_esc(lbl["Case studies"])}</a>',
    ]
    if current:
        parts.append(f'{sep}<span aria-current="page">{_esc(current)}</span>')
    return (
        f'<nav class="cs-breadcrumb" aria-label="{_esc(lbl["Home"])}">'
        + "".join(parts) + "</nav>"
    )


def _render_outcomes(outcomes: list[dict], lbl: dict[str, str]) -> str:
    if not outcomes:
        return ""
    items = "".join(
        '<div class="cs-outcomes-item">'
        f'<dt>{_esc(o.get("value",""))}</dt>'
        f'<dd>{_esc(o.get("label",""))}</dd>'
        "</div>"
        for o in outcomes
    )
    return (
        f'<section class="cs-outcomes" aria-label="{_esc(lbl["By the numbers"])}">'
        f'<h2>{_esc(lbl["By the numbers"])}</h2>'
        f'<dl>{items}</dl></section>'
    )


def _render_pullquote(quote: str) -> str:
    if not quote or not quote.strip():
        return ""
    return f'<aside class="cs-pullquote"><p>{_esc(quote.strip().strip(chr(34)))}</p></aside>'


def _render_meta_strip(study: dict, lbl: dict[str, str]) -> str:
    pieces: list[str] = []
    fields = [
        ("Role", study.get("role", "")),
        ("Period", study.get("period", "")),
        ("Status", study.get("status", "")),
        ("Sector", study.get("sector", "")),
    ]
    for key, val in fields:
        if val:
            pieces.append(
                f'<li><strong>{_esc(lbl[key])}</strong> {_esc(val)}</li>'
            )
    if not pieces:
        return ""
    return f'<ul class="cs-meta-strip" role="list">{"".join(pieces)}</ul>'


def _render_rigour_table(rigour: list[dict], lbl: dict[str, str]) -> str:
    if not rigour:
        return ""
    rows = "".join(
        f'<tr><th scope="row">{_esc(r.get("metric",""))}</th>'
        f'<td>{_esc(r.get("value",""))}</td></tr>'
        for r in rigour
    )
    return (
        '<section class="cs-rigour"><h2>'
        f'{_esc(lbl["Engineering rigour"])}</h2>'
        '<table class="case-study-rigour">'
        f'<caption>{_esc(lbl["Engineering rigour"])}</caption>'
        f'<thead><tr><th scope="col">{_esc(lbl["Signal"])}</th>'
        f'<th scope="col">{_esc(lbl["Evidence"])}</th></tr></thead>'
        f"<tbody>{rows}</tbody></table></section>"
    )


def _render_list_section(heading: str, items: list[str], css_class: str) -> str:
    if not items:
        return ""
    lis = "".join(f"<li>{_esc(item)}</li>" for item in items)
    return f'<section class="{css_class}"><h2>{_esc(heading)}</h2><ul>{lis}</ul></section>'


_LINK_LABELS = {
    "repo": "GitHub repository",
    "site": "Project site",
    "pypi": "PyPI",
    "crates": "crates.io",
    "docs": "Docs.rs",
    "stats": "PyPI download stats",
    "qtonic_evaluation": "Qtonic Quantum Lab — independent evaluation",
    "qgram_adopter": "QGram (Quantum2pi) — KyberLib adopter",
    "bank": "HSBC",
    "linkedin": "LinkedIn",
}
_LINK_ORDER = (
    "repo", "site", "pypi", "crates", "docs", "stats",
    "qtonic_evaluation", "qgram_adopter", "bank", "linkedin",
)


def _render_rail_links(links: dict[str, str], lbl: dict[str, str]) -> str:
    if not links:
        return ""
    rows: list[str] = []
    seen: set[str] = set()
    for key in _LINK_ORDER:
        if key in links and key not in seen:
            seen.add(key)
            rows.append(
                f'<li><a href="{_esc(links[key])}" rel="noopener noreferrer">'
                f'{_esc(_LINK_LABELS.get(key, key))}</a></li>'
            )
    for key, val in links.items():
        if key not in seen:
            rows.append(
                f'<li><a href="{_esc(val)}" rel="noopener noreferrer">{_esc(key)}</a></li>'
            )
    return (
        '<div class="cs-rail-links">'
        f'<h3>{_esc(lbl["Verifiable links"])}</h3>'
        f'<ul>{"".join(rows)}</ul></div>'
    )


def _render_share_rail(url: str, title: str, lbl: dict[str, str]) -> str:
    import urllib.parse as _up

    full_url = url if url.startswith("http") else f"{_BASE_URL}{url}"
    enc_url = _up.quote(full_url, safe="")
    enc_title = _up.quote(title, safe="")
    x_href = f"https://twitter.com/intent/tweet?url={enc_url}&text={enc_title}"
    li_href = f"https://www.linkedin.com/sharing/share-offsite/?url={enc_url}"
    return (
        '<div class="cs-rail-share-block">'
        f'<h3>{_esc(lbl["Share"])}</h3>'
        '<div class="cs-rail-share">'
        f'<a href="{x_href}" rel="noopener noreferrer" target="_blank" '
        f'aria-label="{_esc(lbl["Share on X"])}" title="{_esc(lbl["Share on X"])}">X</a>'
        f'<a href="{li_href}" rel="noopener noreferrer" target="_blank" '
        f'aria-label="{_esc(lbl["Share on LinkedIn"])}" title="{_esc(lbl["Share on LinkedIn"])}">in</a>'
        '</div>'
        '</div>'
    )


def _render_related_articles_section(
    slugs: list[str], lbl: dict[str, str], lang: str, article_slug_map: dict[str, str]
) -> str:
    if not slugs:
        return ""
    items = []
    for slug in slugs:
        href = _related_article_href(slug, lang, article_slug_map)
        # Strip date prefix for display; keep underscores → spaces fallback.
        display = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", slug).replace("-", " ").capitalize()
        items.append(f'<li><a href="{href}">{_esc(display)}</a></li>')
    return (
        '<section class="cs-related-articles">'
        f'<h2>{_esc(lbl["Related articles"])}</h2>'
        f'<ul>{"".join(items)}</ul></section>'
    )


def _render_more_case_studies(
    current: dict, all_studies: list[dict], lbl: dict[str, str],
    lang: str, url_segment: str,
) -> str:
    others = [s for s in all_studies if s["slug"] != current["slug"]][:4]
    if not others:
        return ""
    cards = []
    for s in others:
        slug = s["slug"]
        title = s.get("title", slug)
        kicker = s.get("kicker", lbl["eyebrow"])
        banner = s.get("banner", "")
        banner_alt = s.get("banner_alt", title)
        href = _study_url(lang, url_segment, slug)
        media = ""
        if banner:
            media = (
                f'<a href="{href}" class="cs-card-media">'
                f'<img alt="{_esc(banner_alt)}" src="{_esc(banner)}" '
                'loading="lazy" decoding="async" width="600" height="338">'
                f'<span class="cs-card-kicker">{_esc(kicker)}</span></a>'
            )
        cards.append(
            f'<article data-category="{_esc(s.get("category_slug",""))}">'
            f'{media}'
            '<div class="cs-card-body">'
            f'<h3><a href="{href}">{_esc(title)}</a></h3>'
            '</div></article>'
        )
    return (
        '<section class="cs-related">'
        f'<h2>{_esc(lbl["More case studies"])}</h2>'
        '<div class="cs-related-grid" role="list">'
        + "".join(cards) +
        '</div></section>'
    )


def _json_ld_block(payload: dict) -> str:
    return (
        '<script type="application/ld+json">'
        + json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
        + '</script>'
    )


def _build_breadcrumb_jsonld(
    lbl: dict[str, str], lang: str, url_segment: str,
    study: dict | None = None,
) -> dict:
    bcp47 = {
        "en": "en-GB", "fr": "fr-FR", "de": "de-DE", "es": "es-ES",
        "it": "it-IT", "ja": "ja-JP", "ko": "ko-KR", "ru": "ru-RU",
    }.get(lang, lang)
    home_url = _BASE_URL + ("/" if lang == "en" else f"/{lang}/")
    hub_url = _BASE_URL + _hub_url(lang, url_segment)
    items = [
        {"@type": "ListItem", "position": 1, "name": lbl["Home"], "item": home_url},
        {"@type": "ListItem", "position": 2, "name": lbl["Case studies"], "item": hub_url},
    ]
    if study is not None:
        items.append({
            "@type": "ListItem", "position": 3,
            "name": study.get("title", study["slug"]),
            "item": _BASE_URL + _study_url(lang, url_segment, study["slug"]),
        })
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items,
        "inLanguage": bcp47,
    }


_BCP47_OVERRIDES = {
    "en": "en-GB", "fr": "fr-FR", "de": "de-DE", "es": "es-ES",
    "it": "it-IT", "ja": "ja-JP", "ko": "ko-KR", "ru": "ru-RU",
}


def _source_code_entity(study: dict, links: dict, person_id: str) -> dict | None:
    """Schema.org SoftwareSourceCode node for a repo-linked study."""
    if not (links.get("repo") or links.get("crates") or links.get("pypi")):
        return None
    language = "Rust" if links.get("crates") else ("Python" if links.get("pypi") else None)
    entity = {
        "@type": "SoftwareSourceCode",
        "name": study.get("title", study["slug"]),
        "codeRepository": links.get("repo"),
        "programmingLanguage": language,
        "license": "https://www.apache.org/licenses/LICENSE-2.0",
        "author": {"@type": "Person", "@id": person_id},
    }
    return {k: v for k, v in entity.items() if v is not None}


def _build_article_jsonld(
    study: dict, lbl: dict[str, str], lang: str, url_segment: str,
) -> dict:
    bcp47 = _BCP47_OVERRIDES.get(lang, lang)
    url = _BASE_URL + _study_url(lang, url_segment, study["slug"])
    person_id = f"{_BASE_URL}/#person"
    links = study.get("links", {}) or {}
    main_entity = _source_code_entity(study, links, person_id)
    about = [{
        "@type": "Organization",
        "name": "HSBC Holdings plc",
        "url": links["bank"],
    }] if "bank" in links else []
    # Collapse YAML folded-scalar newlines so JSON-LD stays a single
    # logical line. Postbuild HTML transforms apply unescape passes that
    # turn json.dumps's \n back into a literal newline, which breaks
    # test_page_inline_jsonld_is_valid_json.
    description = " ".join((study.get("problem", "") or "").split())[:200]
    article: dict = {
        "@context": "https://schema.org",
        "@type": "Article",
        "@id": url + "#article",
        "headline": study.get("title", study["slug"]),
        "description": description,
        "url": url,
        "articleSection": lbl["Case study"],
        "inLanguage": bcp47,
        "isPartOf": {
            "@type": "CollectionPage",
            "@id": _BASE_URL + _hub_url(lang, url_segment) + "#collection",
        },
        "author": {"@type": "Person", "@id": person_id},
        "creator": {"@type": "Person", "@id": person_id},
        "publisher": {"@type": "Person", "@id": person_id},
        "license": "https://creativecommons.org/licenses/by/4.0/",
    }
    if study.get("banner"):
        article["image"] = study["banner"]
    if main_entity:
        article["mainEntity"] = main_entity
    if about:
        article["about"] = about
    return article


def _build_collection_jsonld(
    studies: list[dict], lbl: dict[str, str], lang: str, url_segment: str,
) -> dict:
    bcp47 = {
        "en": "en-GB", "fr": "fr-FR", "de": "de-DE", "es": "es-ES",
        "it": "it-IT", "ja": "ja-JP", "ko": "ko-KR", "ru": "ru-RU",
    }.get(lang, lang)
    hub_url = _BASE_URL + _hub_url(lang, url_segment)
    items = []
    for i, study in enumerate(studies, start=1):
        items.append({
            "@type": "ListItem",
            "position": i,
            "url": _BASE_URL + _study_url(lang, url_segment, study["slug"]),
            "name": study.get("title", study["slug"]),
        })
    return {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "@id": hub_url + "#collection",
        "name": lbl["Case studies"],
        "description": lbl["deck"],
        "url": hub_url,
        "inLanguage": bcp47,
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(studies),
            "itemListElement": items,
        },
    }


def _hero_variant(slug: str) -> str:
    """Rotate hero composition across 5 studies so each feels distinct.
    Stable per slug — same slug always gets the same variant."""
    return ("centre", "left", "split")[sum(ord(c) for c in slug) % 3]


def _stage_no(n: int, label: str) -> str:
    """Numbered stage eyebrow — '01 — THE PROBLEM' style."""
    return (
        f'<p class="cs-stage-no">'
        f'<span aria-hidden="true">{n:02d} — </span>'
        f'{_esc(label.upper())}</p>'
    )


def _render_hero_stage(
    study: dict, lbl: dict[str, str], lang: str, url_segment: str,
) -> str:
    """FT customer-stories hero — full-bleed photo with overlay text + CTA."""
    title = study.get("title", study.get("slug", ""))
    kicker = study.get("kicker", lbl["eyebrow"])
    deck = study.get("pull_quote", "").strip()
    if deck.startswith('"') and deck.endswith('"'):
        deck = deck[1:-1]
    banner = study.get("banner", "")
    breadcrumb = _render_breadcrumb(lbl, lang, url_segment, title)

    media_html = ""
    if banner:
        media_html = (
            '<figure class="cs-hero-media" aria-hidden="true">'
            f'<img alt="" src="{_esc(banner)}" '
            'loading="eager" fetchpriority="high" decoding="async" '
            'width="1600" height="900">'
            '</figure>'
        )

    return (
        '<section class="cs-stage cs-hero" data-stage>'
        + media_html
        + '<div class="cs-stage-row">'
        + '<div class="cs-hero-text">'
        + breadcrumb
        + f'<p class="cs-kicker">{_esc(kicker)}</p>'
        + f'<h1>{_esc(title)}</h1>'
        + (f'<p class="cs-deck">{_esc(deck)}</p>' if deck else '')
        + f'<a class="cs-hero-cta" href="#story">{_esc(lbl.get("Read case study", "Read more"))}</a>'
        + '</div>'
        + '</div>'
        + '</section>'
    )


def _render_meta_bar(study: dict, lbl: dict[str, str]) -> str:
    """Compact meta strip below hero — role / period / status / sector."""
    pieces: list[str] = []
    fields = [
        ("Role", study.get("role", "")),
        ("Period", study.get("period", "")),
        ("Status", study.get("status", "")),
        ("Sector", study.get("sector", "")),
    ]
    for key, val in fields:
        if val:
            pieces.append(
                f'<li><strong>{_esc(lbl[key])}</strong> {_esc(val)}</li>'
            )
    if not pieces:
        return ""
    return (
        '<section class="cs-stage cs-meta-bar" data-stage>'
        '<div class="cs-stage-row">'
        f'<ul role="list">{"".join(pieces)}</ul>'
        '</div></section>'
    )


def _render_outcomes_stage(outcomes: list[dict], lbl: dict[str, str]) -> str:
    if not outcomes:
        return ""
    items = "".join(
        '<div class="cs-outcome">'
        f'<dt>{_esc(o.get("value",""))}</dt>'
        f'<dd>{_esc(o.get("label",""))}</dd>'
        "</div>"
        for o in outcomes
    )
    return (
        '<section class="cs-stage cs-outcomes" data-stage '
        f'aria-label="{_esc(lbl["By the numbers"])}">'
        '<div class="cs-stage-row">'
        + _stage_no(0, lbl["By the numbers"]).replace(
            '<span aria-hidden="true">00 — </span>', ''
        )
        + f'<dl>{items}</dl>'
        '</div></section>'
    )


def _render_quote_stage(quote: str) -> str:
    """Full-bleed italic serif pull quote."""
    q = (quote or "").strip().strip('"').strip("“").strip("”")
    if not q:
        return ""
    return (
        '<section class="cs-stage cs-quote" data-stage>'
        '<div class="cs-stage-row">'
        f'<blockquote><p>{_esc(q)}</p>'
        '<cite>— from the case-study brief</cite></blockquote>'
        '</div></section>'
    )


def _render_story_stage(n: int, label: str, body_text: str, anchor: str = "") -> str:
    if not body_text:
        return ""
    anchor_attr = f' id="{anchor}"' if anchor else ""
    return (
        f'<section class="cs-stage cs-story" data-stage{anchor_attr}>'
        '<div class="cs-stage-row">'
        f'<div class="cs-stage-head">{_stage_no(n, label)}'
        f'<h2>{_esc(label)}</h2></div>'
        '<div class="cs-stage-body">'
        f'<p>{_esc(body_text)}</p>'
        '</div></div></section>'
    )


def _render_rigour_stage(rigour: list[dict], lbl: dict[str, str], n: int) -> str:
    if not rigour:
        return ""
    cards = "".join(
        '<li class="cs-rigour-card">'
        f'<p class="cs-rigour-card-signal">{_esc(r.get("metric",""))}</p>'
        f'<p class="cs-rigour-card-value">{_esc(r.get("value",""))}</p>'
        '</li>'
        for r in rigour
    )
    return (
        '<section class="cs-stage cs-rigour" data-stage>'
        '<div class="cs-stage-row">'
        + _stage_no(n, lbl["Engineering rigour"])
        + f'<h2>{_esc(lbl["Engineering rigour"])}</h2>'
        + f'<ul class="cs-rigour-grid" role="list">{cards}</ul>'
        '</div></section>'
    )


def _render_validation_stage(items: list[str], lbl: dict[str, str], n: int) -> str:
    if not items:
        return ""
    lis = "".join(f'<li>{_esc(i)}</li>' for i in items)
    return (
        '<section class="cs-stage cs-validation" data-stage>'
        '<div class="cs-stage-row">'
        + _stage_no(n, lbl["Independently verified"])
        + f'<h2>{_esc(lbl["Independently verified"])}</h2>'
        + f'<ul>{lis}</ul>'
        '</div></section>'
    )


def _render_standards_stage(items: list[str], lbl: dict[str, str], n: int) -> str:
    if not items:
        return ""
    pills = "".join(f'<li>{_esc(i)}</li>' for i in items)
    return (
        '<section class="cs-stage cs-standards" data-stage>'
        '<div class="cs-stage-row">'
        + _stage_no(n, lbl["Aligned standards"])
        + f'<h2>{_esc(lbl["Aligned standards"])}</h2>'
        + f'<ul class="cs-standards-pills" role="list">{pills}</ul>'
        '</div></section>'
    )


def _render_links_stage(links: dict[str, str], lbl: dict[str, str], n: int) -> str:
    if not links:
        return ""
    rows: list[str] = []
    seen: set[str] = set()
    for key in _LINK_ORDER:
        if key in links and key not in seen:
            seen.add(key)
            rows.append(
                f'<li><a href="{_esc(links[key])}" rel="noopener noreferrer">'
                f'{_esc(_LINK_LABELS.get(key, key))}</a></li>'
            )
    for key, val in links.items():
        if key not in seen:
            rows.append(
                f'<li><a href="{_esc(val)}" rel="noopener noreferrer">{_esc(key)}</a></li>'
            )
    return (
        '<section class="cs-stage cs-stage--wash cs-links" data-stage>'
        '<div class="cs-stage-row">'
        + _stage_no(n, lbl["Verifiable links"])
        + f'<h2>{_esc(lbl["Verifiable links"])}</h2>'
        + f'<ul class="cs-links-grid" role="list">{"".join(rows)}</ul>'
        '</div></section>'
    )


def _render_related_articles_stage(
    slugs: list[str], lbl: dict[str, str], lang: str, article_slug_map: dict[str, str]
) -> str:
    if not slugs:
        return ""
    items = []
    for slug in slugs:
        href = _related_article_href(slug, lang, article_slug_map)
        display = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", slug).replace("-", " ").capitalize()
        items.append(f'<li><a href="{href}">{_esc(display)}</a></li>')
    return (
        '<section class="cs-stage cs-related" data-stage>'
        '<div class="cs-stage-row cs-stage-row--mid">'
        f'<p class="cs-stage-no">{_esc(lbl["Related articles"]).upper()}</p>'
        f'<h2>{_esc(lbl["Related articles"])}</h2>'
        f'<ul class="cs-links-grid" role="list">{"".join(items)}</ul>'
        '</div></section>'
    )


def _render_cta_stage(lbl: dict[str, str], lang: str) -> str:
    home = "/" if lang == "en" else f"/{lang}/"
    contact = f"{home}contact/"
    return (
        '<section class="cs-stage cs-cta" data-stage>'
        '<div class="cs-stage-row">'
        f'<p class="cs-stage-no">{_esc(lbl.get("Next", "Next")).upper()}</p>'
        f'<h2>{_esc(lbl.get("CTA headline", "Want this kind of evidence in your bank?"))}</h2>'
        f'<p>{_esc(lbl.get("CTA body", "Architecture reviews, post-quantum migration plans, treasury-API programmes — all signed, all verifiable."))}</p>'
        f'<a class="cs-cta-btn" href="{contact}">'
        f'{_esc(lbl.get("Get in touch", "Get in touch"))}'
        '</a>'
        '</div></section>'
    )


def _render_more_studies_stage(
    current: dict, all_studies: list[dict], lbl: dict[str, str],
    lang: str, url_segment: str,
) -> str:
    others = [s for s in all_studies if s["slug"] != current["slug"]][:4]
    if not others:
        return ""
    cards = []
    for s in others:
        slug = s["slug"]
        title = s.get("title", slug)
        kicker = s.get("kicker", lbl["eyebrow"])
        banner = s.get("banner", "")
        href = _study_url(lang, url_segment, slug)
        media_html = ""
        if banner:
            media_html = (
                '<span class="cs-more-card-media" aria-hidden="true">'
                f'<img class="cs-more-card-bg" alt="" src="{_esc(banner)}" '
                'loading="lazy" decoding="async" width="600" height="375">'
                '</span>'
            )
        cards.append(
            '<article class="cs-more-card">'
            + media_html
            + '<div class="cs-more-card-body">'
            + f'<p class="cs-more-card-kicker">{_esc(kicker)}</p>'
            + f'<h3 class="cs-more-card-title"><a href="{href}">{_esc(title)}</a></h3>'
            + '</div></article>'
        )
    return (
        '<section class="cs-stage cs-more" data-stage>'
        '<div class="cs-stage-row">'
        f'<p class="cs-stage-no">{_esc(lbl["More case studies"]).upper()}</p>'
        f'<h2>{_esc(lbl["More case studies"])}</h2>'
        f'<div class="cs-more-grid" role="list">{"".join(cards)}</div>'
        '</div></section>'
    )


_SHARE_SVG = {
    "x": (
        '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false">'
        '<path d="M9.52 6.88L14.86 1h-1.42L8.83 6.07 4.94 1H.78l5.6 7.7L.78 15h1.42l4.78-5.27L11.07 15h4.16L9.52 6.88zM2.71 2.07h1.83l7.61 10.51h-1.83L2.71 2.07z"/>'
        '</svg>'
    ),
    "li": (
        '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false">'
        '<path d="M13.6 13.6h-2.37V9.93c0-.87-.02-2-1.22-2-1.22 0-1.4.95-1.4 1.93v3.74H6.24V6.04h2.27v1.04h.03c.32-.6 1.09-1.22 2.25-1.22 2.4 0 2.85 1.58 2.85 3.64v4.1zM3.56 5C2.81 5 2.2 4.39 2.2 3.64S2.81 2.28 3.56 2.28s1.36.61 1.36 1.36S4.31 5 3.56 5zm1.18 8.6H2.39V6.04h2.36V13.6z"/>'
        '</svg>'
    ),
    "fb": (
        '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false">'
        '<path d="M9 14H6.5V8.5H5V6h1.5V4.5C6.5 3.07 7.07 2 9.07 2H10.5v2.5H9.43c-.38 0-.43.14-.43.43V6h1.5L10 8.5H9V14z"/>'
        '</svg>'
    ),
    "mail": (
        '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false">'
        '<path d="M2 3h12c.55 0 1 .45 1 1v8c0 .55-.45 1-1 1H2c-.55 0-1-.45-1-1V4c0-.55.45-1 1-1zm6 5.18L13.18 4H2.82L8 8.18zM2 5.46V12h12V5.46L8 9.5 2 5.46z"/>'
        '</svg>'
    ),
}


def _render_side_meta(study: dict, lbl: dict[str, str]) -> str:
    """Role / Period / Status / Sector dt-dd rows for the sidebar."""
    rows = []
    for field, label_key in (("role", "Role"), ("period", "Period"),
                              ("status", "Status"), ("sector", "Sector")):
        value = study.get(field, "")
        if value:
            rows.append(
                '<div class="cs-side-section">'
                f'<dt>{_esc(lbl[label_key])}</dt>'
                f'<dd>{_esc(value)}</dd></div>'
            )
    return f'<dl class="cs-side-meta">{"".join(rows)}</dl>' if rows else ""


def _render_side_links(links: dict, lbl: dict[str, str]) -> str:
    """Verifiable-links block — _LINK_ORDER first, remainder appended."""
    if not links:
        return ""
    link_rows: list[str] = []
    seen: set[str] = set()
    for key in _LINK_ORDER:
        if key in links and key not in seen:
            seen.add(key)
            link_rows.append(
                f'<li><a href="{_esc(links[key])}" rel="noopener noreferrer">'
                f'{_esc(_LINK_LABELS.get(key, key))}</a></li>'
            )
    for key, val in links.items():
        if key not in seen:
            link_rows.append(
                f'<li><a href="{_esc(val)}" rel="noopener noreferrer">{_esc(key)}</a></li>'
            )
    return (
        '<div class="cs-side-section cs-side-links">'
        f'<h3>{_esc(lbl["Verifiable links"])}</h3>'
        f'<ul>{"".join(link_rows)}</ul></div>'
    )


def _render_share_block(study: dict, lbl: dict[str, str], lang: str) -> str:
    """Article-style share rail (44×44 circular SVG icons)."""
    import urllib.parse as _up

    full_url = f"{_BASE_URL}{_study_url(lang, '', study['slug'])}"
    enc_url = _up.quote(full_url, safe="")
    enc_title = _up.quote(study.get("title", study["slug"]), safe="")
    enc_mail_body = _up.quote(f"Read more: {full_url}", safe="")
    return (
        '<div class="cs-side-section cs-side-share-block">'
        f'<h3>{_esc(lbl["Share"])}</h3>'
        '<nav class="share-rail" aria-label="Share">'
        '<ul>'
        f'<li><a href="https://twitter.com/intent/tweet?url={enc_url}&amp;text={enc_title}" '
        f'rel="noopener noreferrer" target="_blank" '
        f'aria-label="{_esc(lbl["Share on X"])}">{_SHARE_SVG["x"]}</a></li>'
        f'<li><a href="https://www.linkedin.com/sharing/share-offsite/?url={enc_url}" '
        f'rel="noopener noreferrer" target="_blank" '
        f'aria-label="{_esc(lbl["Share on LinkedIn"])}">{_SHARE_SVG["li"]}</a></li>'
        f'<li><a href="https://www.facebook.com/sharer/sharer.php?u={enc_url}" '
        f'rel="noopener noreferrer" target="_blank" '
        f'aria-label="Share on Facebook">{_SHARE_SVG["fb"]}</a></li>'
        f'<li><a href="mailto:?subject={enc_title}&amp;body={enc_mail_body}" '
        f'rel="noopener noreferrer" '
        f'aria-label="Share by email">{_SHARE_SVG["mail"]}</a></li>'
        '</ul></nav>'
        '</div>'
    )


def _render_side_panel(study: dict, lbl: dict[str, str], lang: str) -> str:
    """FT-style left rail: meta dl + standards + verifiable links + share."""
    standards = study.get("standards", []) or []
    standards_block = ""
    if standards:
        pills = "".join(f"<li>{_esc(s)}</li>" for s in standards)
        standards_block = (
            '<div class="cs-side-section cs-side-standards">'
            f'<h3>{_esc(lbl["Aligned standards"])}</h3>'
            f'<ul>{pills}</ul></div>'
        )
    return (
        '<aside class="cs-side" aria-label="Story details">'
        + _render_side_meta(study, lbl)
        + standards_block
        + _render_side_links(study.get("links", {}) or {}, lbl)
        + _render_share_block(study, lbl, lang)
        + '</aside>'
    )


def _render_inline_outcomes(outcomes: list[dict]) -> str:
    if not outcomes:
        return ""
    items = "".join(
        '<div>'
        f'<dt>{_esc(o.get("value",""))}</dt>'
        f'<dd>{_esc(o.get("label",""))}</dd>'
        '</div>'
        for o in outcomes
    )
    return f'<dl class="cs-outcomes-inline">{items}</dl>'


def _render_inline_pull_quote(quote: str) -> str:
    q = (quote or "").strip().strip('"').strip("“").strip("”")
    if not q:
        return ""
    return (
        '<aside class="cs-pull-inline">'
        f'<p>{_esc(q)}</p>'
        f'<cite>— from the case-study brief</cite>'
        '</aside>'
    )


def _render_inline_rigour(rigour: list[dict], lbl: dict[str, str]) -> str:
    if not rigour:
        return ""
    items = "".join(
        '<li>'
        f'<p class="cs-rigour-signal">{_esc(r.get("metric",""))}</p>'
        f'<p class="cs-rigour-value">{_esc(r.get("value",""))}</p>'
        '</li>'
        for r in rigour
    )
    return f'<ul class="cs-rigour-rows" role="list">{items}</ul>'


def _render_inline_validation(items: list[str]) -> str:
    if not items:
        return ""
    lis = "".join(f"<li>{_esc(i)}</li>" for i in items)
    return f'<ul class="cs-validation-inline" role="list">{lis}</ul>'


def _render_inline_related_articles(
    slugs: list[str], lbl: dict[str, str], lang: str, article_slug_map: dict[str, str]
) -> str:
    if not slugs:
        return ""
    items: list[str] = []
    for slug in slugs:
        href = _related_article_href(slug, lang, article_slug_map)
        display = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", slug).replace("-", " ").capitalize()
        items.append(f'<li><a href="{href}">{_esc(display)}</a></li>')
    return f'<ul class="cs-side-links cs-related-rows" role="list">{"".join(items)}</ul>'


def _prose_section(headline_html: str, body_html: str, anchor: str = "") -> str:
    """Emit one <section> with a stage-headline + body HTML."""
    open_tag = f'<section id="{anchor}">' if anchor else "<section>"
    return f'{open_tag}<h2 class="cs-stage-headline">{headline_html}</h2>{body_html}</section>'


def _deck_html(study: dict) -> str:
    """Pull-quote deck used as standfirst above the numbered sections."""
    deck = (study.get("pull_quote", "") or "").strip().strip('"').strip("“").strip("”")
    return f'<p class="cs-deck-intro">{_esc(deck)}</p>' if deck else ""


def _prose_body_for(study: dict, lbl: dict[str, str], lang: str,
                    article_slug_map: dict[str, str], field: str) -> str:
    """Render the body HTML for one of the named sections.

    The keys mirror the YAML field names so the section table below can
    drive the whole render with one lookup per row."""
    value = study.get(field)
    if not value:
        return ""
    if field in ("problem", "what_i_built"):
        return f'<p>{_esc(value)}</p>'
    if field == "outcome_highlights":
        return _render_inline_outcomes(value)
    if field == "rigour":
        return _render_inline_rigour(value, lbl)
    if field == "validation":
        return _render_inline_validation(value)
    if field == "related_articles":
        return _render_inline_related_articles(value, lbl, lang, article_slug_map)
    return ""


# Ordered (field, label-key, stage-number-or-zero, anchor) tuples driving
# the right-column section render. Stage number 0 means "no NN — prefix".
_MAIN_SECTIONS: tuple[tuple[str, str, int, str], ...] = (
    ("problem", "Problem", 1, "story"),
    ("what_i_built", "What I built", 2, ""),
    ("outcome_highlights", "By the numbers", 0, ""),
    ("rigour", "Engineering rigour", 3, ""),
    ("validation", "Independently verified", 4, ""),
    ("related_articles", "Related articles", 0, ""),
)


def _render_main_body_parts(
    study: dict, lbl: dict[str, str], lang: str, article_slug_map: dict[str, str],
) -> list[str]:
    """Build the ordered narrative sections for the right column."""
    parts: list[str] = []
    deck = _deck_html(study)
    if deck:
        parts.append(deck)
    for field, label_key, stage, anchor in _MAIN_SECTIONS:
        body = _prose_body_for(study, lbl, lang, article_slug_map, field)
        if not body:
            continue
        prefix = _stage_n(stage) if stage else ""
        parts.append(_prose_section(f'{prefix}{_esc(lbl[label_key])}', body, anchor=anchor))
    return parts


def _render_body_two_col(
    study: dict, lbl: dict[str, str], lang: str, url_segment: str,
    article_slug_map: dict[str, str],
) -> str:
    """FT customer-story two-column body: sticky left rail + right prose column."""
    side = _render_side_panel(study, lbl, lang)
    main_parts = _render_main_body_parts(study, lbl, lang, article_slug_map)
    main_body = f'<div class="cs-body-main">{"".join(main_parts)}</div>'
    return (
        '<section class="cs-stage cs-body-stage" data-stage>'
        '<div class="cs-stage-row cs-body-grid">'
        + side + main_body
        + '</div></section>'
    )


def _stage_n(n: int) -> str:
    return f'<span aria-hidden="true">{n:02d} — </span>'


def _render_body(
    study: dict, lbl: dict[str, str], lang: str, url_segment: str,
    article_slug_map: dict[str, str], all_studies: list[dict],
) -> str:
    """Per-study page — FT customer-stories pattern:
       hero (full-bleed photo) → 2-col body (sticky meta rail + prose) →
       CTA closer → more case studies → JSON-LD."""

    article_jsonld = _json_ld_block(_build_article_jsonld(study, lbl, lang, url_segment))
    breadcrumb_jsonld = _json_ld_block(_build_breadcrumb_jsonld(lbl, lang, url_segment, study))

    return (
        '<div class="case-study-wrap">'
        + _render_hero_stage(study, lbl, lang, url_segment)
        + _render_body_two_col(study, lbl, lang, url_segment, article_slug_map)
        + _render_cta_stage(lbl, lang)
        + _render_more_studies_stage(study, all_studies, lbl, lang, url_segment)
        + breadcrumb_jsonld
        + article_jsonld
        + '</div>'
    )


def _collect_categories(studies: list[dict]) -> list[tuple[str, str]]:
    """Unique (slug, display-name) pairs over the studies, preserving order."""
    categories: list[tuple[str, str]] = []
    seen: set[str] = set()
    for s in studies:
        slug = s.get("category_slug", "")
        if slug and slug not in seen:
            seen.add(slug)
            categories.append((slug, s.get("category", "") or slug))
    return categories


def _filter_dropdown_html(
    categories: list[tuple[str, str]], lbl: dict[str, str],
) -> tuple[str, str]:
    """Return (summary_swap_spans, radio_input_block) for the CSS-only
    category filter."""
    summary_swaps = (
        f'<span class="cs-dd-label cs-dd-label--all">{_esc(lbl["All categories"])}</span>'
        + "".join(
            f'<span class="cs-dd-label cs-dd-label--{_esc(slug)}">{_esc(name)}</span>'
            for slug, name in categories
        )
    )
    radio_options = (
        '<input type="radio" id="csf-all" name="csfilter" value="" checked>'
        f'<label for="csf-all">{_esc(lbl["All categories"])}</label>'
        + "".join(
            f'<input type="radio" id="csf-{_esc(slug)}" name="csfilter" value="{_esc(slug)}">'
            f'<label for="csf-{_esc(slug)}">{_esc(name)}</label>'
            for slug, name in categories
        )
    )
    return summary_swaps, radio_options


def _render_index_body(
    studies: list[dict], lbl: dict[str, str], lang: str, url_segment: str,
) -> str:
    """Hub page — full-bleed hero (uses first study's banner as bg),
    metrics-bar stage, filter-bar stage, banner-card grid stage, CTA."""
    breadcrumb = _render_breadcrumb(lbl, lang, url_segment)

    if not studies:
        return (
            '<div class="case-study-wrap">'
            '<section class="cs-stage cs-hero cs-hub-hero" data-stage>'
            '<div class="cs-stage-row">'
            + breadcrumb
            + f'<p class="cs-kicker">{_esc(lbl["eyebrow_plural"])}</p>'
            + f'<h1>{_esc(lbl["Case studies"])}</h1>'
            + f'<p class="cs-deck">{_esc(lbl["deck"])}</p>'
            + '</div></section></div>'
        )

    # Pick a hero banner from the first study so the hub feels editorial.
    hero_banner = studies[0].get("banner", "")

    categories = _collect_categories(studies)
    summary_swaps, radio_options = _filter_dropdown_html(categories, lbl)

    metric_items = "".join(
        '<div class="cs-hub-metric">'
        f'<dt>{_esc(label)}</dt>'
        f'<dd>{_esc(value)}</dd>'
        '</div>'
        for value, label in (
            (str(len(studies)), lbl["Case studies"]),
            (str(len(categories)), lbl["Categories"]),
            ("19 yrs", lbl.get("Years banking", "Banking + payments")),
            ("100%", lbl.get("No fabrication", "Verifiable — no fabrication")),
        )
    )

    hero_media = ""
    if hero_banner:
        hero_media = (
            '<figure class="cs-hero-media" aria-hidden="true">'
            f'<img alt="" src="{_esc(hero_banner)}" '
            'loading="eager" fetchpriority="high" decoding="async" '
            'width="1600" height="900">'
            '</figure>'
        )
    hero_stage = (
        '<section class="cs-stage cs-hero cs-hub-hero" data-stage>'
        + hero_media
        + '<div class="cs-stage-row">'
        '<div class="cs-hero-text">'
        + breadcrumb
        + f'<p class="cs-kicker">{_esc(lbl["eyebrow_plural"])}</p>'
        + f'<h1>{_esc(lbl["Case studies"])}</h1>'
        + f'<p class="cs-deck">{_esc(lbl["deck"])}</p>'
        + f'<a class="cs-hero-cta" href="#hub-grid">{_esc(lbl.get("Read case study", "Browse"))}</a>'
        + '</div></div>'
        + '</section>'
    )

    metrics_stage = (
        '<section class="cs-stage cs-hub-metrics-bar" data-stage '
        f'aria-label="{_esc(lbl["By the numbers"])}">'
        '<div class="cs-stage-row">'
        f'<dl class="cs-hub-metrics">{metric_items}</dl>'
        '</div></section>'
    )

    filter_bar = (
        '<section class="cs-stage cs-hub-filter" data-stage id="hub-grid">'
        '<div class="cs-stage-row">'
        '<form class="cs-filter-bar" role="search">'
        '<details class="cs-dropdown">'
        '<summary class="cs-dropdown-summary" '
        f'aria-label="{_esc(lbl["Filter by category"])}">'
        '<span class="cs-dd-prefix">' + _esc(lbl["Filter by category"]) + ':</span> '
        + summary_swaps
        + '</summary>'
        '<fieldset class="cs-dropdown-menu" role="radiogroup" '
        f'aria-label="{_esc(lbl["Filter by category"])}">'
        '<legend class="visually-hidden">'
        + _esc(lbl["Filter by category"]) +
        '</legend>'
        + radio_options
        + '</fieldset>'
        '</details>'
        + f'<span class="cs-filter-meta">{_esc(lbl["count"].format(n=len(studies)))}</span>'
        '</form>'
    )

    cards: list[str] = []
    for s in studies:
        slug = s["slug"]
        title = s.get("title", slug)
        kicker = s.get("kicker", lbl["eyebrow"])
        cat_slug = s.get("category_slug", "")
        problem = s.get("problem", "")
        excerpt = (problem.strip()[:200].rstrip() + "…") if problem else ""
        banner = s.get("banner", "")
        banner_alt = s.get("banner_alt", title)
        href = _study_url(lang, url_segment, slug)

        media_html = ""
        if banner:
            media_html = (
                f'<a class="cs-card-media" href="{href}" tabindex="-1" aria-hidden="true">'
                f'<img alt="{_esc(banner_alt)}" src="{_esc(banner)}" '
                'loading="lazy" decoding="async" width="800" height="500">'
                '</a>'
            )

        cards.append(
            f'<article data-category="{_esc(cat_slug)}">'
            + media_html
            + '<div class="cs-card-body">'
            + f'<p class="cs-card-kicker">{_esc(kicker)}</p>'
            + f'<h2 class="cs-card-title"><a href="{href}">{_esc(title)}</a></h2>'
            + f'<p class="cs-card-excerpt">{_esc(excerpt)}</p>'
            + '</div></article>'
        )

    # Close the filter section, then open a sibling grid stage so the
    # CSS :has() ~ filter selector can reach it without inline JS.
    grid = (
        '</div></section>'
        '<section class="cs-stage cs-grid-stage" data-stage>'
        '<div class="cs-stage-row">'
        f'<section class="cs-grid" aria-label="{_esc(lbl["Case studies"])}">'
        + "".join(cards) + '</section>'
        '</div></section>'
    )

    cta_stage = _render_cta_stage(lbl, lang)

    collection_jsonld = _json_ld_block(_build_collection_jsonld(studies, lbl, lang, url_segment))
    breadcrumb_jsonld = _json_ld_block(_build_breadcrumb_jsonld(lbl, lang, url_segment, None))

    return (
        '<div class="case-study-wrap">'
        + hero_stage
        + metrics_stage
        + filter_bar + grid
        + cta_stage
        + breadcrumb_jsonld
        + collection_jsonld
        + '</div>'
    )


def _swap_into_shell(shell: str, body: str, title: str, desc: str, url: str) -> str:
    out = _TITLE_RE.sub(f"<title>{_esc(title)}</title>", shell, count=1)
    out = _DESC_RE.sub(
        f'<meta name="description" content="{_esc(desc)}"', out, count=1
    )
    out = _CANONICAL_RE.sub(
        f'<link rel="canonical" href="{_esc(url)}"', out, count=1
    )
    out = _OG_TITLE_RE.sub(rf'\1{_esc(title)}\2', out, count=1)
    out = _OG_DESC_RE.sub(rf'\1{_esc(desc)}\2', out, count=1)
    out = _OG_URL_RE.sub(rf'\1{_esc(url)}\2', out, count=1)
    out = _AP_HERO_BLOCK_RE.sub("", out, count=1)
    out = _MAIN_WRAP_RE.sub(rf'\1{body}\2', out, count=1)
    return out


def _write_study(
    shell: str, study: dict, lang: str, url_segment: str,
    lbl: dict[str, str], out_dir: Path, article_slug_map: dict[str, str],
    all_studies: list[dict],
) -> Path:
    slug = study["slug"]
    title = study.get("title", slug)
    desc = (study.get("problem", "") or "")[:155]
    url = (
        f"{_BASE_URL}/case-studies/{slug}/"
        if lang == "en"
        else f"{_BASE_URL}/{lang}/{url_segment}/{slug}/"
    )
    body = _render_body(study, lbl, lang, url_segment, article_slug_map, all_studies)
    out = _swap_into_shell(shell, body, title, desc, url)
    target = out_dir / slug / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(out, encoding="utf-8")
    return target


def _write_index(
    shell: str, studies: list[dict], lang: str, url_segment: str,
    lbl: dict[str, str], out_dir: Path,
) -> Path:
    body = _render_index_body(studies, lbl, lang, url_segment)
    url = (
        f"{_BASE_URL}/case-studies/"
        if lang == "en"
        else f"{_BASE_URL}/{lang}/{url_segment}/"
    )
    out = _swap_into_shell(
        shell, body,
        f"{lbl['Case studies']} — Sebastien Rousseau",
        lbl["deck"],
        url,
    )
    target = out_dir / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(out, encoding="utf-8")
    return target


def _emit_one_locale(
    shell: str, studies: list[dict], lang: str, url_segment: str,
    lbl: dict[str, str], article_slug_map: dict[str, str],
) -> int:
    out_dir = OUT_DIR if lang == "en" else (PUBLIC / lang / url_segment)
    out_dir.mkdir(parents=True, exist_ok=True)
    # Apply per-locale overlay to each study before rendering. EN passes
    # through unchanged (overlay loader returns {} for lang == 'en').
    localised_studies = [_localised_study(s, lang) for s in studies]
    for study in localised_studies:
        _write_study(shell, study, lang, url_segment, lbl, out_dir, article_slug_map, localised_studies)
    _write_index(shell, localised_studies, lang, url_segment, lbl, out_dir)
    return len(localised_studies) + 1


def _emit_locale_forks(studies: list[dict]) -> int:
    """For each active non-EN locale, fork the EN locale shell + run
    translate_chrome to localise nav / footer / search aria / lang switch
    on the case-study pages. Body text is rendered from the per-locale
    label table; YAML body content (Problem prose etc.) stays in EN."""
    sys.path.insert(0, str(ROOT / "scripts" / "lib"))
    sys.path.insert(0, str(ROOT / "scripts" / "generators"))
    try:
        import _lang_registry  # type: ignore[import-not-found]
        from build_translations import _chrome as _ch  # type: ignore[import-not-found]
        from build_translations import _state as _st  # type: ignore[import-not-found]
    except ImportError as exc:
        print(f"build_case_studies: skip locale forks — {exc}", file=sys.stderr)
        return 0

    en_shell = SHELL_SRC.read_text(encoding="utf-8")
    total = 0
    for lang in _lang_registry.active():
        if lang.code == "en":
            continue
        lbl = _lbl(lang.code)
        slugs_map = _lang_registry.load_slugs(lang.code)
        url_segment = slugs_map.get("static", {}).get("case-studies", "case-studies")
        article_slug_map = slugs_map.get("articles", {})
        _st.bind_lang(lang.code)
        # Render the case-study body in this locale (uses per-locale labels)
        # then run the same chrome translator the rest of the locale forks
        # use — nav, footer, search aria, lang switcher all localise.
        localised_shell = _ch._set_html_lang(en_shell)
        localised_shell = _ch.translate_chrome(localised_shell)
        # Rewrite every JSON-LD inLanguage="en"/"en-GB" → this locale's
        # BCP-47 tag so test_jsonld_localized.py passes for the locale forks.
        localised_shell = _ch._localize_inlanguage_globally(localised_shell, lang.code)
        total += _emit_one_locale(
            localised_shell, studies, lang.code, url_segment, lbl, article_slug_map
        )
    return total


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    if not SHELL_SRC.is_file():
        print(f"build_case_studies: missing shell {SHELL_SRC}", file=sys.stderr)
        return 0
    studies = _load_studies()
    shell = SHELL_SRC.read_text(encoding="utf-8")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    en_lbl = _lbl("en")
    en_count = _emit_one_locale(shell, studies, "en", "case-studies", en_lbl, {})
    locale_count = _emit_locale_forks(studies)
    print(
        f"build_case_studies: wrote {len(studies)} case studies + 1 index in EN "
        f"({en_count} files); {locale_count} files across 27 locale forks"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
