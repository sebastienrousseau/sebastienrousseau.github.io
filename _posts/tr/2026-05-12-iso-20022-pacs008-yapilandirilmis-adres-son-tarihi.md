---
title: "Kasım 2026 pacs.008 yapılandırılmış adres son tarihi: altı aylık bir görünüm"
subtitle: "Kasım 2026 ortasından itibaren SWIFT CBPR+, pacs.008 ve ilgili sınır ötesi ödeme mesajlarındaki yapılandırılmamış posta adreslerini reddedecek. Mesajların yaklaşık %65'i hâlâ uyumsuzken iyileştirme penceresi hızla kapanıyor."
description: "Kasım 2026'dan itibaren SWIFT CBPR+, sınır ötesi ödeme mesajlarında yapılandırılmış posta adresleri zorunlu kılıyor. Yapılandırılmamış adres satırları (yalnızca AdrLine), pacs.008'deki temel taraf alanları için artık kabul edilmeyecek. En az düzeyde TwnNm ve Ctry gerekir; StrtNm ile BldgNb ya da PstBx önerilir. Altı ay kala, ödeme mesajlarının %65'i hâlâ yapılandırılmamış adres taşıyor ve bankaların %44'ü programın gerisinde."
date: "May 12, 2026"
language: "tr"
locale: "tr_TR"
banner: "https://cloudcdn.pro/stocks/images/markus-winkler-IrRbSND5EUc-unsplash.webp"
banner_alt: "ISO 20022 pacs.008 yapılandırılmış adres şeması: TwnNm ve Ctry alanları vurgulanmış sınır ötesi ödeme mesaj alanları"
keywords: "ISO 20022, pacs.008, pacs.009, pacs.004, pacs.003, pain.001, CBPR+, SWIFT, SR2026, yapılandırılmış adres, TwnNm, Ctry, StrtNm, BldgNb, SEPA, EPC, sınır ötesi ödemeler, yaptırım taraması, pacs008"
---

Kasım 2026 ortasından itibaren SWIFT CBPR+, pacs.008 ve ilgili sınır ötesi ödeme mesajlarındaki yapılandırılmamış posta adreslerini reddedecek. Mesajların yaklaşık %65'i hâlâ uyumsuz ve bankaların %44'ü programın gerisindeyken, iyileştirme penceresi çoğu hazırlık programının başa çıkacak biçimde tasarlandığından daha hızlı kapanıyor.

---

> **Önemli Çıkarımlar**
>
> - **Kasım 2026**'dan itibaren SWIFT CBPR+, sınır ötesi ödeme mesajlarında yapılandırılmamış posta adreslerini artık kabul etmeyecek. Değişiklik **pacs.008** (müşteri kredi transferi), **pacs.009** (FI kredi transferi), **pacs.004** (iadeler) ve **pacs.003** (doğrudan borçlandırmalar) mesajlarının yanı sıra bunları besleyen yukarı akıştaki **pain.001** akışları için de geçerlidir.
> - En az düzeyde, **Şehir Adı (TwnNm)** ve **Ülke (Ctry)** kendilerine ayrılmış yapılandırılmış alanlarda bulunmalıdır. **Sokak Adı (StrtNm)** ile birlikte **Bina Numarası (BldgNb)** ya da **Posta Kutusu (PstBx)** güçlü biçimde önerilir. Yalnızca serbest metin adres satırları (AdrLine), temel taraf alanları için gereksinimi artık karşılamayacaktır.
> - Değişiklik yaptırım taraması doğruluğunu artırır, manuel düzeltme oranlarını azaltır ve straight-through processing'i korur; ancak bu yalnızca mesaj motorlarını değil, yukarı akıştaki müşteri verilerini de iyileştirmiş kurumlar için geçerlidir.
> - Sektörün hazırlığı dengesizdir. Mart 2026 itibarıyla **CBPR+ mesajlarının yaklaşık %65'i hâlâ yapılandırılmamış adres taşıyor**, **bankaların %44'ü** son tarih için yolunda değil ve **müşteri adres kayıtlarının ortalama %32'si** yapılandırılmamış olarak kalıyor.
> - Açık kaynak araçlar, aralarında pacs.008 mesaj akışlarını oluşturmak, doğrulamak ve düzenlemek için bir Python kütüphanesi ile FastAPI hizmeti olan **[pacs008](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API")** de bulunmak üzere, mesajlar SWIFT ağına ulaşmadan önce şema doğrulamasını, adres kalitesi kontrollerini ve CI düzeyinde uygulamayı otomatikleştirerek iyileştirme sürelerini kısaltabilir.

---

## Her Zaman Yaklaşmakta Olan Bir Son Tarih

Kasım 2026 yapılandırılmış adres gereksinimi ani bir düzenleyici hamle değildir. Özgün [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) göçü duyurulduğundan bu yana SWIFT CBPR+ yol haritasında yer alıyor ve Kasım 2025'teki MT/MX bir arada var olma döneminin sonunu izliyor. 2026'da değişen şey yakınlıktır. Yaklaşık altı ay kalmışken sektör artık çözülmemiş veri kalitesi sorunlarının operasyonel riske dönüştüğü pencerenin içinde çalışıyor.

Rakamlar hikâyeyi açıkça anlatıyor. SWIFT'in Mart 2026 topluluk güncellemesi [ödeme mesajlarının yaklaşık %65'inin hâlâ yapılandırılmamış adres içerdiğini ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed") ve benimsemenin coğrafyalar ile kurum türleri arasında dengesiz kaldığını belirtiyor. 308 kıdemli ödeme uzmanıyla yapılan Mart 2026 tarihli bir [RedCompass Labs anketi ⧉](https://financialit.net/news/banking/nearly-half-banks-are-behind-iso-20022 "Nearly Half of Banks Are Behind on ISO 20022"), bankaların %44'ünün yapılandırılmış adres son tarihini karşılama yolunda şu anda ilerlemediğini ortaya koydu; bunu, 2026 hazırlığına ortalama 20 milyon dolar (en büyük kurumlarda 30 milyon doların üzerinde) harcamalarına ve [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) programlarına ortalama 13 ek personel atamalarına rağmen yapıyorlar. Aynı anket, müşteri adres kayıtlarının ortalama %32'sinin yapılandırılmamış kaldığını ve bankaların %60'ının yapılandırılmış adres alanlarını desteklerken çekirdek bankacılık sistemlerinde boşluklar bildirdiğini de saptadı.

Başka bir deyişle bu, mesaj motoru üzerinde bir ay daha çalışarak çözülebilecek bir sorun değildir. Mesaj katmanından yukarıya, işe alım sistemlerine, KYC süreçlerine, kurumsal kanallara ve onlarca yılda birikmiş serbest metin müşteri ana verilerine uzanan bir veri kalitesi sorunudur.

## Kuralın Gerçekte Gerektirdiği

SWIFT CBPR+ Standards Release 2026 (SR2026) kapsamında temel gereksinim ilkede basit, ayrıntıda ise tavizsizdir. Kasım 2026 ortasından itibaren, CBPR+ ödeme mesajlarındaki tüm ajanlar ve taraflar için [Şehir Adı ile Ülke, kendilerine ayrılmış yapılandırılmış alanlarda sağlanmalıdır ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed"); yalnızca çok sınırlı istisnalar vardır (camt.052, camt.053, camt.054 içindeki ekstre ve bildirimler ile birkaç idari mesaj katı gereksinimin dışında kalır). Ajanlar için yalnızca BIC'nin sürekli kullanımı, ad ve adres bilgisine geçerli bir alternatif olmaya devam eder.

Geçiş sonrasında iki adres biçimine izin verilir:

- **Tam yapılandırılmış**: posta adresinin her bileşeni kendine ayrılmış [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) öğesine eşlenir: StrtNm (Sokak Adı), BldgNb (Bina Numarası) veya BldgNm (Bina Adı), PstCd (Posta Kodu), TwnNm (Şehir Adı), CtrySubDvsn (Ülke Alt Bölümü), Ctry (Ülke, ISO 3166-1 alpha-2 kodu olarak). Bu, SWIFT'in mümkün olan yerlerde açıkça daha tercih edilir seçenek olarak belirlediği biçimdir.
- **Hibrit**: Şehir Adı ve Ülke kendi yapılandırılmış alanlarında doldurulur, adresin geri kalanı ise en fazla iki yapılandırılmamış AdrLine öğesi kullanabilir. Önemlisi, [yapılandırılmış öğeler yapılandırılmamış satırların içinde yinelenmemelidir ⧉](https://www.statestreet.com/web/insights/articles/documents/state-street-client-guide-to-iso-20022-2025.pdf "State Street Client Guide to ISO 20022 2025"); herhangi bir bileşen için adres ya biri ya diğeridir.

Tam yapılandırılmamış adresler, yani adresin tamamının TwnNm veya Ctry olmaksızın AdrLine öğelerinde bulunduğu adresler, etkilenen taraf alanlarının hiçbiri için kabul edilmeyecektir. European Payments Council, SEPA kural kitabını aynı geçişe hizaladı; dolayısıyla [15 Kasım 2026'dan itibaren yapılandırılmamış biçim SCT, SDD ve SCT Inst genelinde de yasaklanmıştır ⧉](https://clearingpost.com/insights/iso-20022-structured-address-deadline-november-2026/ "The November 2026 Structured Address Deadline: What Every PSP Needs to Do Now"). Bu hizalama kasıtlıdır: SWIFT ve EPC, tek bir sektör çapında geçiş hafta sonu tasarladı.

Kuşkuya yer bırakmamak adına, [pacs008 dokümantasyonu etkilenen mesajları doğrudan sıralıyor ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008"): pacs.008 (müşteri kredi transferlerinde borçlu ve alacaklı), pacs.009 (FI kredi transferleri ve teminat ödemelerinde kurum adresleri), pacs.004 (iadelerde taraf adresleri) ve pacs.003 (doğrudan borçlandırmalar). Gereksinim yukarı akışa da yansır: yapılandırılmamış adres taşıyan kurumsal pain.001 dosyaları, alıcı bankada uyumlu pacs.008 üretimini engelleyecektir.

## Sektör Bunu Neden Öncelik Hâline Getirdi

Yapılandırılmış adreslerin gerekçesi estetik değildir. Operasyoneldir ve kendini üç yerde gösterir.

**Yaptırım taraması.** En büyük pratik yarar, yapılandırılmış adreslerin tarama sistemlerinin taraf adını konum verilerinden ayırmasına olanak tanımasıdır. Serbest metin adres blokları, bir şehir adı yaptırımlı bir kişi adının belirteciyle örtüştüğünde ya da serbest metne gömülü bir ülke tümüyle gözden kaçtığında düzenli olarak yanlış pozitiflere yol açar. Yapılandırılmış alanlar, tarama motorlarının ülkeye özgü risk kurallarını belirlenimci biçimde uygulamasına olanak tanır ve ayrıştırılmış bir dizeyi tahmin etmek yerine yaptırım listesi eşleştirmesinin ülke koduna karşı uygulanmasını mümkün kılar. Mart 2026'da yayımlanan CGI UK analizi bu noktayı açıkça vurguluyor: [yapılandırılmış adres verileri, salt bir uyum yükümlülüğü değil, operasyonel dayanıklılığın merkezine yerleşiyor ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement").

**Manuel düzeltme oranları.** Sınır ötesi ödemeler bugün manuel araştırmalar, istisna yönetimi ve düzeltme kuyrukları biçiminde önemli bir operasyonel maliyet taşıyor; bunun büyük bölümü, tarama veya yönlendirme sistemlerinin güvenle ayrıştıramadığı adreslerden kaynaklanıyor. Yapılandırılmış adreslere çoktan geçmiş bankalar, özellikle aracı ajanların daha önce kendilerinin üretmediği serbest metin verilerini yorumlamak zorunda kaldığı orta koridor akışlarında STP istisnalarında kayda değer azalmalar bildiriyor.

**Ağ düzeyinde uygulama.** SR2026, SWIFT ağ katmanında doğrulamayı sıkılaştırıyor. Yeni kontrollerin bazıları başlangıçta engellemesiz modda çalışacak, yani ödemeleri durdurmadan veri kalitesi sorunlarını işaretleyecek; ancak gidişat açıktır ve geçiş sonrasında [uyumlu olmayan mesajlar doğrudan reddedilecektir ⧉](https://www.redcompasslabs.com/insights/iso-20022-is-arriving-all-at-once-for-us-banks/ "ISO 20022 is arriving all at once for US banks"). Birkaç ABD ödeme rayı (Fedwire, CHIPS) ve SWIFT CBPR+ esasen aynı takvimde birleşiyor; bu da bazı kurumların önceki planlarında varsaydığı kademeli geçiş seçeneğini ortadan kaldırıyor.

## Alan Düzeyinde Görünüm: Mesajda Ne Değişiyor

pacs.008 mesajı, ilk CBPR+ kullanım kılavuzları Mart 2023'te yürürlüğe girdiğinden beri yapılandırılmış adres desteği taşıyor. Kasım 2026'da değişen şey şema değil, doğrulamadır. Şimdiye kadar bankaların AdrLine öğelerini serbest metinle doldurup bunu ağdan geçirmesine izin verildi. Son tarihten itibaren taraf bloklarının içerikleri, asgari yapılandırılmış alan gereksinimlerini karşılamalıdır.

### Zorunlu, Önerilen ve Kaldırılan

| Öğe | XPath (`PstlAdr` altında) | Kasım 2026 sonrası durum | Notlar |
|---|---|---|---|
| Şehir Adı | `<TwnNm>` | **Zorunlu** | Etkilenen taraf başına en az bir yapılandırılmış Şehir Adı |
| Ülke | `<Ctry>` | **Zorunlu** | ISO 3166-1 alpha-2 kodu |
| Sokak Adı | `<StrtNm>` | Güçlü biçimde önerilir | Tam yapılandırılmış biçim için gerekli |
| Bina Numarası | `<BldgNb>` | Önerilir | BldgNb ya da PstBx, ikisi birden değil |
| Posta Kutusu | `<PstBx>` | Önerilir | BldgNb'ye alternatif |
| Posta Kodu | `<PstCd>` | Önerilir | Bazı yerel şemalarda gerekli |
| Ülke Alt Bölümü | `<CtrySubDvsn>` | İsteğe bağlı | Eyalet, bölge, il |
| Adres Satırı (serbest metin) | `<AdrLine>` | **Kısıtlı** | Hibritte en fazla 2 satır; yapılandırılmış alanlardaki aynı bileşenle asla birlikte değil |
| Adres Türü | `<AdrTp>` | İsteğe bağlı | Posta adresleri için `ADDR` kullanımı önerilir |

*Kaynak: SR2026 için SWIFT CBPR+ kullanım kılavuzları ile [pacs008.com yapılandırılmış adres dokümantasyonunun ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008") sentezi.*

Pratik sonuç şudur: ister kendi mesaj üretiminde, ister kurumsal müşterilerden alınan pain.001 dosyalarında, ister akış hâlindeki ödemeleri zenginleştirmek için kullanılan ana veri kayıtlarında olsun, hâlâ yalnızca AdrLine'a dayanan her kurumun bu veriyi geçiş öncesinde yapılandırılmış alanlara taşıması gerekir. SWIFT'in akış içi çeviri hizmeti geçişte yardımcı olabilir, ancak [Ocak 2026'dan itibaren ek ücrete tabidir ⧉](https://www.pcbb.com/products/international-banking/international-payments/iso20022-faq "ISO 20022 FAQ — PCBB") ve her adres biçimini güvenilir biçimde ayrıştıramaz. SWIFT ayrıca, yapılandırılmamış eski verilerden Şehir ve Ülke bilgisini güven puanlarıyla çıkarmak üzere 200'den fazla ülkeden gelen verilerle eğitilmiş [açık kaynaklı bir yapay zekâ adres yapılandırma modeli yayımladı ⧉](https://www.swift.com/standards/iso-20022/iso-20022-faqs/swift-ai-address-structuring-model "ISO 20022: The Swift AI address structuring model"); ancak bu açıkça bir iyileştirme yardımıdır, yukarı akıştaki temiz verinin uzun vadeli yerine geçen bir çözüm değildir.

## pacs008.com Zaman Çizelgesini Kısaltmaya Nasıl Yardımcı Oluyor

Adres kalitesi ve mesaj doğrulama boru hatlarını hızla sanayileştirmesi gereken kurumlar için [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API"), özellikle FI'dan FI'a müşteri kredi transferi iş akışı için tasarlanmış, MIT lisanslı açık kaynak bir araç seti ve FastAPI hizmeti sunar. İyileştirme programlarının en sık takıldığı üç katmanı ele alır: veri doğrulama, XML üretimi ve boru hattı uygulaması.

Araç setinin yapılandırılmış adres yetenekleri SR2026 gereksinimlerine hizalıdır:

- **Yapılandırılmış ve hibrit posta adresi alanlarının üretim öncesi doğrulaması**, böylece uyumlu olmayan veriler herhangi bir XML üretilmeden veya gönderilmeden önce yakalanır.
- Kasım 2026 son tarihinden sonra başarısız olacak **yapılandırılmamış adres verilerinin işaretlenmesi**, hibrit olarak kabul edilebilir durumlar ile tam yapılandırılmamış durumlar arasında net bir ayrımla.
- Hem son tarih öncesi hibrit biçimler hem de son tarih sonrası tam yapılandırılmış düzenler için **çift biçim desteği**; böylece kurumlar, kendi geçişlerini henüz tamamlamamış karşı taraflarla birlikte çalışabilirliği bozmadan aşamalı olarak göç edebilir.
- Adres kalitesi kontrollerinin akış sonunda sonradan eklenen bir düşünce değil de yapı sürecinin bir parçası olması için **CI boru hattı entegrasyonu**: bu, [veri yönetişiminin bir uyum katmanı değil, temel bir tasarım ilkesi olması gerektiği yönündeki CGI gözlemine ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement") verilen pratik yanıttır.

Adreslerin ötesinde, araç seti SR2026 sürümünün sıkılaştırdığı daha geniş doğrulama yüzeyini kapsar: 20 mesaja özgü şemaya karşı JSON Schema doğrulaması, 75 ülke genelinde IBAN biçim ve sağlama doğrulaması, üretilen XML'in resmi [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) şemalarına karşı XSD doğrulaması ve desteklenen 13 pacs.008 revizyonunun tümü boyunca (pacs.008.001.01'den pacs.008.001.13'e kadar) sürüm duyarlı üretim. Operasyon ve uyum ekipleri için ayrıca GDPR ve PCI DSS gereksinimlerini karşılamak üzere defusedxml aracılığıyla XXE önleme, sıkı yol geçişi koruması ve yapılandırılmış JSON günlüklerinde PII maskeleme içerir; bunlar, üretim ödeme akışlarında pazarlık konusu edilemeyen ancak satıcı liderliğindeki göçlerde çoğu zaman geç aşamada eklenen türden kontrollerdir.

Kütüphane, `pip install pacs008` paketi olarak [PyPI'da ⧉](https://pypi.org/project/pacs008/ "pacs008 on PyPI") ve tam kaynak şeffaflığıyla [GitHub'da ⧉](https://github.com/sebastienrousseau/pacs008 "pacs008 on GitHub") mevcuttur. Seçeneklerini değerlendiren kurumlar için bunun önemi var: açık kaynak araçlar, iç ekiplerin doğrulama mantığını denetlemesine, lisans müzakereleri olmadan mevcut Python veya FastAPI ortamlarına entegre etmesine ve kendi sınır durumları ortaya çıktıkça düzeltmeleri geri katkılamasına olanak tanır.

Kapsam konusunda kesin olmakta yarar var. pacs008 bir mesaj katmanı araç setidir; bir ödeme motorunun, bir tarama sisteminin ya da bir kurumun kaynakta yapması gereken müşteri ana veri iyileştirmesinin yerini almaz. Yaptığı şey, o iyileştirme çalışmasını alıp uygulanabilir kılmaktır: yapılandırılmış adres uyumunu, uzun bir boru hattının sonundaki manuel bir incelemeden, üretim noktasındaki otomatik bir kapıya dönüştürür. Zamanı daralan programlar için o kapı, temiz bir geçiş ile geçiş sonrası bir ret dalgası arasındaki farktır.

## Araç Ekosistemi

pacs008, daha geniş bir [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) mesaj aracı ekosisteminin içinde yer alır ve yaklaşım seçimi kurumun teknoloji yığınına, ölçeğine ve göç felsefesine bağlıdır. Açık kaynak ve ticari ekosistem şunları içerir: [pyiso20022 ⧉](https://github.com/phoughton/pyiso20022 "pyiso20022 — an ISO 20022 message generator and parser") (beta doğrulamalı, geniş çok kategorili bir Python kütüphanesi), yukarı akış ödeme başlatması için ilgili [pain001 ⧉](https://pain001.com/ "Pain001 — Automate ISO 20022-compliant payment file creation") kütüphanesi, [Prowide ISO 20022 ⧉](https://www.prowidesoftware.com/development-tools/iso20022 "Prowide ISO 20022 — open source MX message parser for Java") (CBPR+ doğrulaması ve çevirileri için ticari katmanı olan kapsamlı bir Apache 2.0 Java kütüphanesi) ve [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) yeteneğini daha geniş hazine veya ödeme platformu tekliflerine paketleyen bir dizi ticari platform (Mambu, Kyriba, PaymentComponents ve diğerleri).

Bu ödünleşim tanıdıktır. Ticari platformlar şirket içi mühendislik yükünü azaltır, ancak kurumu kendi yol haritasıyla örtüşmeyebilecek bir satıcı yol haritasına bağlar. Kapsamlı çok kategorili kütüphaneler daha geniş bir yüzeyi kapsar, ancak herhangi bir tek mesaj türü için daha fazla entegrasyon çalışması gerektirir. Odaklı açık kaynak kütüphaneler, yani FI'dan FI'a müşteri kredi transferi için pacs008 ve ödeme başlatması için [pain001](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html), belirli darboğazları hızla ele alması gereken kurumlar için entegrasyon süresini en aza indirir ve kurumu kendi doğrulama kurallarının denetiminde bırakır. Özellikle yapılandırılmış adres sorunu için odaklı bir yaklaşımın avantajı, uygulanan kuralların dar, iyi tanımlı ve geçiş öncesinde değişmesi olası olmayan kurallar olmasıdır.

## Bunun Sektöre Göre Anlamı

Kasım 2026 son tarihi tüm kurumları eşit biçimde etkilemez. Doğru yanıt, sınır ötesi trafik hacmine, mevcut veri ortamının olgunluğuna ve kurumun ödeme zincirinde oynadığı role bağlıdır.

### Büyük Muhabir ve Sınır Ötesi Bankalar

Önemli CBPR+ trafiği yürüten birinci kademe bankalar için yapılandırılmış adres gereksinimi, istisnaları ve araştırmaları, BAH sıkılaştırmasını ve (ABD'de) Fedwire ile CHIPS'in eşzamanlı göçünü de kapsayan çok daha büyük bir SR2026 hazırlık programının yalnızca bir iş kolu olur. RedCompass Labs verileri, bu kurumların çoğunun 2026 hazırlığına 20 ila 30 milyon dolar harcadığını ve 10 ila 20 uzmandan oluşan teslim ekipleri kurduğunu gösteriyor. Bu grup için risk teknik yeterlilik değil, teslim kapasitesidir. Aynı sürüm pencereleri için yarışan birden çok paralel iş koluyla, adres kalitesi iyileştirmesi daha görünür iş kollarının gerisinde sessizce kayarak bir geçiş haftası sorununa dönüşebilir. Pratik önlem, adres doğrulamasını boru hattında öne almaktır; böylece hatalar, üretime ulaşacaklarından aylar önce geliştirme ve test ortamlarında ortaya çıkar.

### Orta Ölçekli Bankalar ve Ödeme Kuruluşları

Orta ölçekli bankalar ile EMI/PI kuruluşları için yapılandırılmış adres gereksinimi çoğu zaman karşılaştıkları en önemli 2026 yükümlülüğüdür, çünkü birinci kademe bankalarla aynı çevre iş kolu yükünü taşımazlar. Buradaki zorluk genellikle yukarı akış veri kalitesidir. Onlarca yıldır adresleri serbest metin olarak toplamış müşteri işe alım süreçleri, doğrudan ayrıştırılamayan ana veri ortamları üretir. Otomatik iyileştirme, yani SWIFT'in açık kaynak adres yapılandırma modelinin, ticari adres temizleme hizmetlerinin ya da bir kombinasyonun kullanımı, kayıtların önemli bir bölümünü ele alabilir; ancak karmaşık uluslararası adreslerden oluşan artık bir uzun kuyruk manuel inceleme gerektirecektir. Bu çalışma ne kadar erken başlarsa o kuyruk o kadar küçülür.

### Kurumsal Şirketler ve Ödeme Hizmeti Sağlayıcıları

pain.001 aracılığıyla ödeme başlatan kurumsal şirketler, bankanın pacs.008 üretiminin yukarı akışındadır ancak yapılandırılmış adres gereksiniminden muaf değildir. Bankalar, kurumsal müşteriler adına lehtar adreslerini geriye dönük olarak doldurmayacaktır; yapılandırılmış veri, kurumsal şirketin kendi sistemlerinden gelmelidir. Kurumsal hazine yöneticileri için bu, ERP ve hazine sistemlerinin lehtar adreslerini yapılandırılmış biçimde toplamasını, imza sahibi ve nihai borçlu bilgisinin de benzer biçimde yapılandırılmasını ve ödeme başlatma şablonlarının dosya üretimi sırasında alanları sessizce düşürmemesini sağlamak anlamına gelir. pain.001 dosyalarının uçuş öncesi doğrulaması, ister kurumsal şirketin kendi araçları ister bankanın açtığı hizmetler kullanılsın, pratik kontrol noktası hâline geliyor.

### Satıcılar, Fintech'ler ve Sistem Entegratörleri

Ödeme rayları üzerine inşa eden satıcılar için son tarih, daha sonraki aşamalara ertelenmiş olabilecek [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) yeteneği için zorlayıcı bir işlevdir. Sınır ötesi ödemeleri bankacılık ortakları üzerinden yönlendiren veya başlatan fintech'lerin, yapılandırılmış adres toplamayı kendi arayüzlerinde ve API'lerinde öne çıkarması ya da uyumlu pain.001 dosyalarının kendi verilerinden üretilemeyeceğini kabul etmesi gerekir. Hızlı hareket edebilen satıcılar için fırsat, iyileştirme yükünü kurumsal müşteriler adına üstlenmektir: bir uyum sorununu bir hizmete dönüştürmek.

## Sonuç

Kasım 2026 yapılandırılmış adres son tarihi, bir anlamda dar bir değişikliktir: iki zorunlu alan, birkaç önerilen alan ve yaptırımla ilgili veriler için baştan hiç kullanılmaması gereken bir serbest metin seçeneğinin kaldırılması. Başka bir anlamda, özgün CBPR+ göçünden bu yana operasyonel açıdan en önemli [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) dönüm noktasıdır, çünkü yapılandırılmış veriyi yalnızca mesaj katmanına değil, onu besleyen yukarı akış sistemlerine de zorlar.

Son tarihe altı ay kala sektör düzeyindeki hazırlık tablosu iç açıcı değil. CBPR+ mesajlarının üçte ikisi hâlâ yapılandırılmamış adres taşıyor. Bankaların neredeyse yarısı yolunda değil. Müşteri adres kayıtlarının yaklaşık üçte biri hâlâ ayrıştırılamıyor. Finansman yerinde; anketler tutarlı biçimde sekiz ve dokuz haneli yatırımları gösteriyor, ancak iş yerinde değil ve sorunun veri kalitesi boyutu son aylarda yalnızca harcamayla çözülemez.

Şimdi işe yarayan şey, doğrulama noktasında otomasyondur: kuralları, sorunları ağa ulaştıktan sonra değil ulaşmadan önce yakalayan boru hatlarına yerleştirmek. Python veya FastAPI ortamları işleten kurumlar için [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") gibi açık kaynak araçlar, bu geçişi bir satıcı seçim döngüsü olmadan yapmanın pratik bir yolunu sunar. Teknoloji yığını ne olursa olsun herkes için stratejik nokta aynıdır: değişimi şimdi sanayileştiren kurumlar, son dakika uyumuna güvenenlerden çok daha güçlü bir konumda olacaktır; 2026 tartışmasının büyük bölümünü çerçeveleyen RedCompass Labs araştırmasının ifadesini ödünç almak gerekirse.

Kasımdaki geçiş hafta sonu bir bölümü kapatacak. O hafta sonuna temiz verilerle, otomatik doğrulamayla ve yapılandırılmış adreslerin yaptırım taraması için gerçekte ne yaptığına dair çalışan bir kavrayışla ulaşan kurumlar, o hafta sonunu trafiği izleyerek geçirecek. Bunlar olmadan ulaşanlar ise telefon başında geçirecek.

## Sıkça Sorulan Sorular

**Kasım 2026 son tarihinde tam olarak ne değişiyor?**

Kasım 2026 ortasından itibaren SWIFT CBPR+, taraf alanları yalnızca yapılandırılmamış posta adresleri içeren pacs.008, pacs.009, pacs.004 ve pacs.003 mesajlarını reddedecek. Asgari yapılandırılmış gereksinim, TwnNm öğesindeki Şehir Adı ve Ctry öğesindeki Ülkedir (ISO 3166-1 alpha-2 kodu kullanılarak). Hibrit adreslere hâlâ izin verilir; yani Şehir ve Ülke yapılandırılmış alanlarda, kalan bileşenler için en fazla iki serbest metin AdrLine öğesi. Ancak aynı bileşen hem yapılandırılmış hem yapılandırılmamış alanlarda yer alamaz. Tam yapılandırılmış adresler tercih edilen biçimdir. European Payments Council, SEPA şemalarını (SCT, SDD, SCT Inst) aynı geçiş tarihine hizaladı.

**Hangi mesajlar ve hangi taraf alanları etkileniyor?**

pacs.008 için gereksinim borçlu ve alacaklı posta adreslerine uygulanır. pacs.009 için FI kredi transferleri ve teminat ödemelerindeki kurum adreslerine uygulanır. pacs.004 için ödeme iadelerindeki taraf adreslerine uygulanır. pacs.003 için müşteri doğrudan borçlandırmalarındaki alacaklı ve borçlu adreslerine uygulanır. Ekstre ve bildirim mesajları (camt.052, camt.053, camt.054) ile bazı idari mesajlar katı gereksinimin dışında kalır. Kurumsal müşterilerden gelen yukarı akıştaki pain.001 mesajları doğrudan CBPR+ ile yönetilmez, ancak pain.001 dosyalarındaki yapılandırılmamış adresler aşağı akışta uyumlu pacs.008 üretimini engelleyecek ve böylece fiilen kapsama girecektir.

**Yapılandırılmış, hibrit ve yapılandırılmamış adresler arasındaki fark nedir?**

Tam yapılandırılmış bir adres her bileşeni kendine ayrılmış [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) öğesine eşler: StrtNm, BldgNb veya PstBx, PstCd, TwnNm, CtrySubDvsn, Ctry. Hibrit bir adreste Şehir Adı ve Ülke yapılandırılmış alanlarda, adresin geri kalanı en fazla iki serbest metin AdrLine öğesinde bulunur; aynı bileşen her ikisinde birden yer almamalıdır. Yapılandırılmamış bir adreste tüm posta adresi, yapılandırılmış TwnNm veya Ctry olmaksızın AdrLine öğelerinde bulunur; bu, etkilenen taraf alanları için Kasım 2026'da kaldırılan biçimdir.

**pacs008.com bu geçişe nasıl yardımcı oluyor?**

[pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") kütüphanesi, XML üretiminden önce yapılandırılmış ve hibrit posta adresi alanlarını doğrular, son tarihten sonra başarısız olacak yapılandırılmamış verileri işaretler, hem son tarih öncesi hibrit hem de son tarih sonrası tam yapılandırılmış biçimleri destekler ve CI boru hatları ile toplu doğrulama iş akışlarına entegre olur. Desteklenen 13 pacs.008 sürümünün tümü için XML üretir, resmi [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) XSD şemalarına karşı doğrular ve otomatik düzenleme için bir FastAPI hizmeti açar. MIT türü bir lisans altında açık kaynaktır, PyPI'da mevcuttur ve özellikle FI'dan FI'a müşteri kredi transferi iş akışları için tasarlanmıştır; dolayısıyla doğrulama kuralları çok sayıda mesaj türü üzerinden soyutlanmak yerine SR2026 CBPR+ kullanım kılavuzlarına göre ayarlanmıştır.

**Kurumum Kasım 2026'ya kadar hazır olmazsa ne olur?**

Etkilenen taraf alanlarında yapılandırılmamış adres içeren mesajlar, geçişten sonra ağ düzeyinde reddedilecektir. Pratikte bu, ödeme başarısızlıkları, artan istisna hacimleri, manuel düzeltme dalgaları ve olası müşteri etkisi anlamına gelir. SWIFT'in akış içi çeviri hizmeti bazı geçiş durumları için mevcuttur, ancak Ocak 2026'dan itibaren ek ücrete tabidir ve her adres biçimini güvenilir biçimde ayrıştıramaz. SWIFT ayrıca, yapılandırılmamış eski verilerden Şehir ve Ülke bilgisini çıkaran açık kaynaklı bir yapay zekâ adres yapılandırma modeli yayımladı, ancak bu iyileştirme ve ön işleme için tasarlanmıştır, yukarı akıştaki temiz verinin kalıcı yerine geçen bir çözüm değildir. Son tarihe iyileştirilmiş bir müşteri ana veri ortamı ve otomatik bir doğrulama boru hattı olmadan ulaşan kurumlar, zorlu bir geçiş haftası ve izleyen aylarda kayda değer bir operasyonel artış beklemelidir.

## Kaynaklar

- Sebastien Rousseau, (2023). [Automating ISO 20022-Compliant Payment File Creation with Pain001](https://sebastienrousseau.com/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html "Automating ISO 20022-Compliant Payment File Creation with Pain001").
- pacs008, (2026). [November 2026 structured-address deadline ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008"). pacs008.com.
- pacs008, (2026). [pacs008 — ISO 20022 pacs.008 Toolkit and API ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API"). pacs008.com.
- SWIFT, (2026). [ISO 20022 milestone for November 2026: Unstructured addresses to be removed ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed"). SWIFT.
- SWIFT, (2026). [ISO 20022 for Financial Institutions ⧉](https://www.swift.com/standards/iso-20022/iso-20022-financial-institutions-focus-payments-instructions "ISO 20022 for Financial Institutions"). SWIFT.
- SWIFT, (2026). [The Swift AI address structuring model ⧉](https://www.swift.com/standards/iso-20022/iso-20022-faqs/swift-ai-address-structuring-model "ISO 20022: The Swift AI address structuring model"). SWIFT.
- RedCompass Labs, (2026). [Nearly Half of Banks Are Behind on ISO 20022 ⧉](https://financialit.net/news/banking/nearly-half-banks-are-behind-iso-20022 "Nearly Half of Banks Are Behind on ISO 20022"). Financial IT.
- RedCompass Labs, (2026). [ISO 20022 is arriving all at once for US banks ⧉](https://www.redcompasslabs.com/insights/iso-20022-is-arriving-all-at-once-for-us-banks/ "ISO 20022 is arriving all at once for US banks"). RedCompass Labs.
- ClearingPost, (2026). [The November 2026 Structured Address Deadline: What Every PSP Needs to Do Now ⧉](https://clearingpost.com/insights/iso-20022-structured-address-deadline-november-2026/ "The November 2026 Structured Address Deadline"). ClearingPost.
- CGI UK, (2026). [2026: A defining year for ISO 20022 and structured data enforcement ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement"). CGI UK.
- J.P. Morgan, (2026). [ISO 20022 Migration: Guidance, Messaging & More ⧉](https://www.jpmorgan.com/insights/payments/fx-cross-border/iso-20022-migration "ISO 20022 Migration: Guidance, Messaging & More"). J.P. Morgan.
- ING, (2026). [FAQ Swift ISO 20022 ⧉](https://www.ingwb.com/en/service/payments-and-collections/swift-iso20022/faq-swift-iso-20022 "FAQ Swift ISO 20022 — ING"). ING Wholesale Banking.
- Mambu, (2026). [CBPR+ is live: what ISO 20022 means in practice ⧉](https://mambu.com/en/insights/articles/cbpr-is-live-what-iso-20022-means-in-practice "CBPR+ is live: what ISO 20022 means in practice"). Mambu.
- Kyriba, (2026). [ISO 20022 migration: what every treasury team needs to know about what's next ⧉](https://www.kyriba.com/blog/iso-20022-corporate-treasury-2026/ "ISO 20022 migration: what every treasury team needs to know about what's next"). Kyriba.
- Standard Chartered, (2025). [ISO 20022 – Standard Chartered Address Guidelines (H2H and API) ⧉](https://www.sc.com/en/uploads/sites/66/content/docs/sc-cib-tb-ISO-20022%E2%80%93CBPR-Address-guidelines-H2H-and-API-sept-2025.pdf "Standard Chartered ISO 20022 Address Guidelines"). Standard Chartered.
- State Street, (2025). [Client Guide to ISO 20022 ⧉](https://www.statestreet.com/web/insights/articles/documents/state-street-client-guide-to-iso-20022-2025.pdf "State Street Client Guide to ISO 20022 2025"). State Street.
- ISO 20022, (2026). [Message Definitions Catalogue ⧉](https://www.iso20022.org/iso-20022-message-definitions "ISO 20022 Message Definitions"). ISO 20022.
