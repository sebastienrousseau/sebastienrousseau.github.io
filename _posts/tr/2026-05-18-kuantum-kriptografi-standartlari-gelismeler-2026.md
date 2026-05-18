---
title: "2026'da Kuantum Kriptografi Sıfırlaması: PQC Standartları, QKD Güvencesi ve Bankaların Erteleyemeyeceği Geçiş Çalışması"
subtitle: "Kuantum kriptografi ufuk taramasından uygulama disiplinine geçti: NIST PQC standartları hazır, Birleşik Krallık NCSC algoritma seçimlerini daralttı, IETF protokol çalışması hâlâ olgunlaşıyor ve QKD güvencesi laboratuvar güveninden sertifikasyon diline geçiyor."
description: "2026'da kuantum kriptografi artık kuantum bilgisayarların yakın olup olmadığı tartışması değil. Postkuantum kriptografi, kripto çevikliği, kuantum anahtar dağıtımı güvencesi, protokol standartları, tedarikçi hazırlığı ve şimdiden harvest-now-decrypt-later riskine maruz kalan uzun ömürlü finansal veriler arasında uzanan bir geçiş programıdır."
date: "May 18, 2026"
language: "tr-TR"
locale: "tr_TR"
banner: "https://cloudcdn.pro/stock/images/quantum-cryptography-2026-banner.webp"
banner_alt: "2026 için kuantum güvenli kriptografi geçiş haritası: NIST PQC standartları, hibrit protokol çalışmaları, QKD güvencesi, kripto çevikliği ve banka veri risk kademeleri"
keywords: "kuantum kriptografi 2026, postkuantum kriptografi, NIST FIPS 203, FIPS 204, FIPS 205, ML-KEM, ML-DSA, SLH-DSA, NCSC PQC, IETF TLS, IPsec, RFC 9794, hibrit anahtar değişimi, QKD, ETSI QKD, ISO IEC 23837, kripto çevikliği, harvest now decrypt later, HNDL, finansal hizmetler kriptografisi, banka güvenliği"
---

# 2026'da Kuantum Kriptografi Sıfırlaması: PQC Standartları, QKD Güvencesi ve Bankaların Erteleyemeyeceği Geçiş Çalışması

2026'da kuantum kriptografi iki pratik yola ayrıldı. Postkuantum kriptografi artık bir uygulama programıdır, çünkü NIST üç postkuantum standardının kullanıma hazır olduğunu ve federal sistemlerin bunlara FIPS standartları gibi davranması gerektiğini söylüyor ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")); kuantum anahtar dağıtımı bir güvence ve sertifikasyon meselesi hâline geliyor, çünkü QKD dağıtımları yalnızca laboratuvar gösterimleri yerine değerlendirme dili, koruma profilleri ve operasyonel standartlara ihtiyaç duyuyor ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI QKD Koruma Profilini yayımladı")).

---

> **Yönetici Özeti / Önemli Çıkarımlar**
>
> - **NIST, PQC'yi uygulama aşamasına taşıdı.** Mevcut standartlar: ML-KEM anahtar tesisi için FIPS 203, ML-DSA imzaları için FIPS 204 ve SLH-DSA imzaları için FIPS 205. NIST, kuruluşları savunmasız kriptografiyi belirlemeye ve geçişe şimdi başlamaya çağırıyor ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")).
> - **Birleşik Krallık NCSC pratik seçimleri daralttı.** Çoğu kullanım senaryosu için ML-KEM-768 ve ML-DSA-65'i öneriyor; sistemlerin taslak uyumlu deneyler yerine nihai standartların sağlam uygulamalarına dayanması gerektiği uyarısında bulunuyor ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC – PQC'ye hazırlıkta sonraki adımlar")).
> - **Protokol hazırlığı eşit değil.** IETF, TLS ve IPsec'i PQC ve hibrit anahtar değişimi için güncelliyor, ancak NCSC operasyonel sistemlerin değişen Internet Drafts yerine yayımlanmış RFC'leri tercih etmesi gerektiği uyarısında bulunuyor ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC – PQC'ye hazırlıkta sonraki adımlar")).
> - **Hibrit, bir geçiş mekanizmasıdır; bir bitiş durumu değil.** Hibrit açık anahtar artı postkuantum şemaları geçişi evrelemeye ve uygulama riskini hedge etmeye yardımcı olur; ancak karmaşıklık ekler ve sonradan yalnızca PQC'ye geçiş için ikinci bir migrasyon gerekebilir ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC – PQC'ye hazırlıkta sonraki adımlar")).
> - **QKD, PQC'nin yerini almaz.** QKD özel yüksek güvenceli hatlara hizmet edebilir, ancak bankacılıkla ilgisi yalnızca fiziğine değil; sertifikasyona, birlikte çalışabilirliğe, operasyonel maliyete ve mevcut anahtar yönetim sistemleriyle entegrasyona bağlıdır ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI QKD Koruma Profilini yayımladı")).
> - **Banka düzeyindeki soru envanterdir.** RSA, ECDH, ECDSA, EdDSA, tescilli VPN kriptografisi, HSM şablonları, sertifika ömürleri ve tedarikçi yönetimli kriptografiyi tespit edemeyen bir finans kuruluşu, hangi standartlar mevcut olursa olsun geçiş yapamaz.
> - **Risk şimdiden aktif.** Harvest-now-decrypt-later saldırıları, kriptografik olarak ilgili kuantum bilgisayarlar henüz mevcut olmasa bile uzun ömürlü finansal verileri savunmasız kılar; çünkü saldırganın bugün tek yapması gereken şifreli metni toplamaktır.
> - **Kripto çevikliği kalıcı kontroldür.** Kazanan mimari, RSA'dan ML-KEM'e tek seferlik bir geçiş değildir; algoritmaları, parametreleri, kütüphaneleri, sertifikaları, donanım politikalarını ve protokol modlarını bankayı yeniden inşa etmeden döndürebilen bir platform yeteneğidir.
>
---

## Bu Hafta Neden Önemli

Standart tartışması soyutlama noktasını geçti. NIST'in kamuya açık rehberi, kuruluşların yeni standartları şimdi uygulamaya başlaması, savunmasız algoritmaların kullanıldığı yerleri belirlemesi ve ürün, hizmet ve protokol güncellemelerini planlaması gerektiğini söylüyor ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")). Bu dil önemlidir çünkü PQC'yi bir araştırma konusundan teknoloji yenileme bağımlılığına dönüştürür.

Zamanlama da önemlidir, çünkü finansal verilerin uzun bir gizlilik yarı ömrü vardır. M&A materyalleri, hazine akışları, yaptırım soruşturmaları, müşteri kimlik belgeleri, ödeme yönlendirme metaverileri ve toptan mutabakat kayıtları yıllarca hassas kalabilir. Klasik açık anahtar kriptografisini kıran kuantum bilgisayarın bugün var olması gerekmiyor; maruziyetin bugün rasyonel olması için yeterli.

## 2026 Kriptografi Temel Çizgisi: Dört İş Akışı

### 1. PQC Standartları Plan Yapmaya Yetecek Kadar Hazır

İlk temel algoritmiktir. NIST'in PQC programı teknoloji liderlerine artık adlandırılmış hedefler veriyor: anahtar tesisi için ML-KEM, genel dijital imzalar için ML-DSA ve hash tabanlı imzalar için SLH-DSA ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC – PQC'ye hazırlıkta sonraki adımlar")). Pratik etkisi, satın alma, mimari ve tedarikçi yönetimi ekiplerinin "PQC standartları olacak mı?" sorusunu sormayı bırakıp, "her sistem bunları ne zaman destekleyecek?" diye sormaya başlayabilmesidir.

Daha çetin nokta uyumluluktur. NCSC, taslak standartlara dayanan uygulamaların nihai standartlarla uyumsuz olabileceği, ki bu da büyük banka geçişlerini, göz ardı edildiğinde tam olarak çökerten ayrıntı türü olduğu uyarısında bulunuyor ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC – PQC'ye hazırlıkta sonraki adımlar")). Bu nedenle bankalar deneysel pilotları üretim geçiş yollarından ayırmalıdır.

### 2. Darboğaz Protokollerdir

Algoritmalar tek başına banka trafiğini güvenli kılmaz. TLS, IPsec, SSH, S/MIME, ödeme API'leri, HSM entegrasyonları ve sertifika yönetim yığınları – hepsi protokol düzeyinde destek gerektirir. NCSC, IETF'nin TLS ve IPsec gibi yaygın kullanılan protokolleri PQC algoritmalarının anahtar değişimi ve imza mekanizmalarına dahil edilebileceği şekilde güncellediğini belirtiyor ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC – PQC'ye hazırlıkta sonraki adımlar")).

Bu, aşamalı bir uygulama sorunu yaratır. Bir banka kriptografiyi hemen envantere alabilir, hemen tedarikçi yol haritaları talep edebilir ve hemen kripto çevikliği tasarlayabilir; ancak yüksek kritikliğe sahip üretim kanallarını taşımadan önce yine de istikrarlı protokol uygulamalarını beklemesi gerekebilir.

### 3. QKD Bir Güvence Disiplini Hâline Geliyor

Kuantum anahtar dağıtımı, özellikle kurumun uç noktaları ve ağ rotalarını kontrol ettiği son derece özelleştirilmiş hatlar için geçerli olmaya devam ediyor. 2026'nın önemli gelişmesi tek bir yeni QKD kutusu değil; QKD ürün değerlendirmesi için bir koruma profili kilometre taşı olarak tanımlanan ETSI GS QKD 016 ile birlikte sertifikasyon dilinin ortaya çıkmasıdır ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI QKD Koruma Profilini yayımladı")).

Bankalar için bu, satın alma konuşmasını değiştirir. Doğru soru artık QKD'nin prensipte kuantum güvenli olup olmadığı değildir. Doğru soru, cihazın, entegrasyonun, anahtar yönetim sürecinin, operasyonel ortamın ve sertifikasyon kanıtlarının bankanın tehdit modelini karşılayıp karşılamadığıdır.

### 4. Kripto Çevikliği Mimari Yaklaşımdır

Kripto çevikliği, tüm sistemi değiştirmeden algoritmaları değiştirebilme yeteneğidir. Yazılım kütüphanelerini, protokol müzakeresini, HSM politikalarını, sertifika profillerini, anahtar ömürlerini, imzalama hizmetlerini, denetim kanıtlarını ve geri alma yollarını kapsar. Bu olmadan her kriptografik geçiş özel bir projeye dönüşür.

Bu temel mimari derstir. Postkuantum geçiş, finansal sistemin karşılaşacağı son kriptografik geçiş olmayacak. Şimdi kripto çevikliği inşa eden bankalar, algoritma güncellemeleri, tedarikçi riski, acil iptal ve düzenleyici kanıt için yeniden kullanılabilir bir kontrol düzlemi kazanır.

## Bankaların Şimdi Yapması Gerekenler

### Kriptografik Varlık Envanterini Oluşturun

İlk teslimat kriptografik bir malzeme listesidir. Açık anahtar algoritmalarını, anahtar uzunluklarını, sertifika otoritelerini, HSM şablonlarını, TLS sürümlerini, VPN ürünlerini, ödeme ağ geçitlerini, üçüncü taraf API'leri, mobil SDK'ları, durağan verilerin şifreleme sarmalayıcılarını, imzalama anahtarlarını, ürün yazılımı imzalama süreçlerini ve tedarikçi yönetimli kriptografiyi içermelidir.

Envanter gizlilik ile özgünlüğü ayırt etmelidir. Uzun ömürlü şifreli veriler harvest-now-decrypt-later riskine maruz kalırken, uzun ömürlü imzalama anahtarları savunmasız açık anahtar algoritmalarında köklenmiş kaldıkları sürece gelecekteki sahtecilik riski yaratır.

### Veri Yarı Ömrüne Göre Segmentleyin

Tüm veriler aynı geçiş sırasına ihtiyaç duymaz. Gerçek zamanlı bir kart yetkilendirme mesajının gizlilik yarı ömrü, bir yaptırım soruşturması, kurumsal satın alma dosyası, özel bankacılık kimlik paketi veya egemen borç ihracı belgesinden farklı olabilir. Bu nedenle kuantum geçişi yalnızca ağ güvenliğine değil, veri sınıflandırmasına aittir.

Öncelik, savunmasız anahtar tesisi ile uzun ömürlü verileri koruyan sistemler olmalıdır. Bunlar, bugün toplamanın yarın maruziyet yarattığı sistemlerdir.

### Tedarikçi Yol Haritalarını Sözleşmelere Dahil Edin

NIST, geçiş için ürünlerin, hizmetlerin ve protokollerin güncellemelere ihtiyacı olduğunu söylüyor ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")). Bu, satın alma dilinin değişmesi gerektiği anlamına gelir. Tedarikçiler PQC destek takvimlerini, nihai standart uyumluluğunu, hibrit mod davranışını, donanım modülü kısıtlamalarını, performans etkilerini, sertifika profili desteğini ve geri çekilme kontrollerini açıklamalıdır.

Yalnızca "kuantum güvenli yol haritası" diyen bir tedarikçi soruyu yanıtlamamıştır. Bankaya tarihler, algoritmalar, entegrasyon sınırları ve kanıt gerekir.

## PQC, QKD ve Hibrit: Pratik Bir Karar Tablosu

| Kontrol | En İyi Kullanım | 2026 Durumu | Bankacılık Çekincesi |
|---|---|---|---|
| **ML-KEM / FIPS 203** | Geleceğe dayanıklı gizlilik için anahtar tesisi | Standartlaştırıldı ve uygulama planlaması için hazır ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")) | Kritik üretim dağıtımı öncesinde protokol ve kütüphane desteği gerekir |
| **ML-DSA / FIPS 204** | Genel dijital imzalar | NCSC tarafından çoğu genel imza kullanımı için önerilir ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC – PQC'ye hazırlıkta sonraki adımlar")) | Sertifika zincirleri ve PKI geçişi operasyonel olarak zordur |
| **SLH-DSA / FIPS 205** | Donanım ve yazılım imzalama için hash tabanlı imzalar | NCSC tarafından referans verilen nihai NIST standardı ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC – PQC'ye hazırlıkta sonraki adımlar")) | Daha büyük imzalar kısıtlı ortamları etkileyebilir |
| **Hibrit PQ/T şemaları** | Geçiş döneminde migrasyon ve birlikte çalışabilirlik | Geçiş önlemi olarak yararlı ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC – PQC'ye hazırlıkta sonraki adımlar")) | Karmaşıklık ekler ve ikinci bir migrasyon gerektirebilir |
| **QKD** | Özel yüksek güvenceli hatlar | Güvence çalışması ETSI koruma profili aktivitesi yoluyla olgunlaşıyor ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI QKD Koruma Profilini yayımladı")) | İnternet ölçeğinde genel kimlik doğrulamayı veya kurumsal kripto envanterini çözmez |

## Kurum Tipine Göre Bunun Anlamı

### Birinci Kademe Evrensel Bankalar

Birinci kademe bankalar bir kavram kanıtı değil, bir program ofisine ihtiyaç duyar. Hedef işletim modeli kriptografik envanter, tedarikçi zorlaması, HSM yol haritası yönetimi, hibrit TLS/IPsec için test ortamları ve düzenleyiciye hazır kanıtları birleştirmelidir. En değerli erken çalışma her şifreyi hemen değiştirmek değil; değişimi güvenli kılan kontrol düzlemini inşa etmektir.

### Orta Düzey ve Bölgesel Bankalar

Orta düzey bankalar PQC'yi bir tedarikçi yönetimi ve platform standardizasyon çalışması olarak ele almalıdır. Sistemleri desteklenen kütüphaneler, standart TLS yığınları, yönetilen sertifika hizmetleri ve net tedarikçi son tarihleri etrafında yoğunlaştırarak pahalı özel iş yapımından kaçınabilirler. Temel risk; cihazların, ödeme ağ geçitlerinin ve eski middleware'in içindeki gizli kriptografidir.

### Fintech'ler, PSP'ler ve Kripto Yakını Kurumlar

Fintech'ler genellikle daha az eski güven çapasına sahip oldukları için daha hızlı hareket edebilir. Risk; üçüncü taraf API'lerde, bulut KMS varsayılanlarında, cüzdan altyapısında ve emanet entegrasyonlarında rahatlıktır. Kripto yakını firmalar, blockchain-yerel güvenlik anlatılarını postkuantum hazırlığıyla karıştırmamaya özellikle dikkat etmelidir.

### Mühendisler ve Güvenlik Mimarları

Mühendislik disiplini somuttur: hizmet envanterlerine algoritma metaverisi ekleyin, müzakere edilen protokol modlarını günlüğe kaydedin, hibrit testler için güvenli özellik bayrakları oluşturun, mümkün olduğunda sertifika ömürlerini kısaltın, sabit kodlanmış algoritma varsayımlarını kaldırın ve kripto politikasını kod fork'ları yerine yapılandırma yoluyla dağıtılabilir hâle getirin.

## Sonuç

Kuantum kriptografi sıfırlaması tek bir teknoloji satın alımı değildir. Bu bir kriptografik işletim modelidir. NIST sektöre bir standart temeli verdi, NCSC pratik rehberliği daralttı, protokol kuruluşları hâlâ hareket halinde ve QKD güvencesi daha resmi hâle geliyor. Bu geçişi kazanan bankacılık kurumları en büyük pilotu ilan edenler olmayacak. Kriptografilerinin nerede yaşadığını bilen, hangi verilerin önce korunması gerektiğini bilen ve bankayı yeniden inşa etmeden kriptografik ilkel öğeleri değiştirebilen kurumlar olacak.

## Sıkça Sorulan Sorular

**Postkuantum kriptografi bankaların kullanımına hazır mı?**

Planlama, tedarikçi etkileşimi, pilotlar ve seçilmiş uygulama çalışmaları için hazır. NIST üç standardın uygulamaya hazır olduğunu söylüyor; NCSC ise operasyonel kullanımın nihai standartların sağlam uygulamalarına ve istikrarlı protokollere dayanması gerektiği uyarısında bulunuyor ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography"), [NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC – PQC'ye hazırlıkta sonraki adımlar")).

**QKD, PQC ihtiyacını ortadan kaldırır mı?**

Hayır. QKD özel kontrollü hatlar için yararlı olabilir, ancak PQC genel yazılım, internet protokolleri, API'ler, sertifikalar ve kurumsal sistemler için ölçeklenebilir geçiş yoludur. QKD ayrıca banka sınıfı altyapı olarak ele alınmadan önce güvence ve sertifikasyon çerçevelerine bağlıdır ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI QKD Koruma Profilini yayımladı")).

**İlk olarak ne taşınmalı?**

Uzun ömürlü hassas verileri koruyan sistemler önceliklendirilmelidir. Bu; arşiv şifrelemesi, ödeme soruşturmaları, hazine ve sermaye piyasası belgeleri, özel bankacılık kimlik kayıtları, stratejik anlaşma dosyaları, kök sertifika otoriteleri, ürün yazılımı imzalama ve bankalar arası kanalları içerir.

**En büyük uygulama tuzağı nedir?**

En büyük tuzak PQC'yi bir algoritma takası olarak ele almaktır. Geçiş protokollere, sertifikalara, HSM'lere, tedarikçilere, performans testine, olay müdahalesine, izlemeye ve yönetişime dokunur. Kripto çevikliği olmadan, kurum aynı geçiş sorununu sonraki algoritma değişikliği için yeniden yaratır.

## Kaynaklar

- NIST, (2025). [Postkuantum kriptografi ⧉](https://www.nist.gov/pqc "Postkuantum kriptografi").
- NCSC, (2024). [Postkuantum kriptografiye hazırlıkta sonraki adımlar ⧉](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC PQC rehberi").
- NIST CSRC, (2026). [NIST Postkuantum Kriptografi Projesi ⧉](https://csrc.nist.gov/presentations/2026/mpts2026-3b1 "NIST PQC Projesi").
- ID Quantique, (2024). [ETSI, QKD için dünyanın ilk Koruma Profilini yayımlıyor ⧉](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI QKD 016").
<!-- enrich-start -->
<aside class="author-card" aria-label="About the author"><img alt="Portrait of Sebastien Rousseau" src="https://cloudcdn.pro/stocks/images/sebastien-rousseau.png" width="64" height="64" loading="lazy" decoding="async" /><span class="author-card-body"><strong class="author-card-name"><a href="/about/index.html">Sebastien Rousseau</a></strong><span class="author-card-bio">Senior banking technologist writing on applied AI, ISO 20022 migration, post-quantum cryptography for financial services, and the structural transformation of wholesale payments.</span><span class="author-credentials">20+ years across HSBC Commercial &amp; Investment Bank, PayPal, Barclays, Shazam, AKQA, Virgin Group. <a href="/about/index.html">Full profile</a> &middot; <a href="https://www.linkedin.com/in/sebastienrousseau/" rel="external noopener">LinkedIn</a> &middot; <a href="https://github.com/sebastienrousseau" rel="external noopener">GitHub</a></span></span></aside>
<p class="post-reviewed">Last reviewed <time datetime="2026-05-18">2026-05-18</time>.</p>
<!-- enrich-end -->
