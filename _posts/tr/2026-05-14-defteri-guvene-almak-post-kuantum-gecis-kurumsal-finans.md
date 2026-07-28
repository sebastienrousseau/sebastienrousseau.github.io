---
title: "Defteri güvence altına almak: kurumsal finans için post-kuantum geçişine yönetim kurulu rehberi"
subtitle: "Kuantum riski araştırma merakı olmaktan çıkıp etkin bir düzenleyici zorunluluğa dönüştü. Ocak 2026'da yayımlanan G7 yol haritası ve canlı ödeme sistemlerinde uygulanabilirliği kanıtlayan BIS Project Leap ile birlikte, yönetim kurulu düzeyindeki soru artık geçişin yapılıp yapılmayacağı değil; bugünün verilerinin raf ömrü dolmadan geçişin tamamlanıp tamamlanamayacağıdır."
description: "Kuantum riski araştırma merakı olmaktan çıkıp etkin bir düzenleyici zorunluluğa dönüştü. Ocak 2026'da yayımlanan G7 yol haritası, netleşen AB, Birleşik Krallık ve ASD takvimleri ve BIS Project Leap'in merkez bankası düzeyinde uygulanabilirliği kanıtlamasıyla, yönetim kurulları için soru artık geçişin yapılıp yapılmayacağı değil; geçişin bugünün verilerinin kriptografik raf ömrü dolmadan tamamlanıp tamamlanamayacağıdır."
date: "May 14, 2026"
language: "tr-TR"
locale: "tr_TR"
banner: "https://cloudcdn.pro/stocks/images/getty-images-LaU3HadwEeE-unsplash.webp"
banner_alt: "Post-kuantum kriptografi geçiş yol haritası diyagramı: kurumsal bankacılık altyapısının RSA'dan ML-KEM ve ML-DSA'ya geçişi"
keywords: "post-kuantum kriptografi, PQC geçişi, kurumsal bankacılık, finansal hizmetler, G7 CEG yol haritası, BIS Project Leap, ML-KEM, ML-DSA, FIPS 203, FIPS 204"
---


Kuantum riski, araştırma merakı olmaktan çıkıp etkin bir düzenleyici zorunluluğa dönüştü. Ocak 2026'da yayımlanan G7 yol haritası, netleşen AB, Birleşik Krallık ve Avustralya takvimleri ve canlı ödeme sistemlerinde uygulanabilirliği kanıtlayan BIS Project Leap ile birlikte, yönetim kurulları için soru artık geçişin yapılıp yapılmayacağı değil; bugünün verilerinin kriptografik raf ömrü dolmadan geçişin tamamlanıp tamamlanamayacağıdır.

---

> **Önemli Çıkarımlar**
>
> - **2026, düzenleyici duruşun sertleştiği yıldır.** G7 Siber Uzman Grubu'nun Ocak yol haritası, AB NIS İşbirliği Grubu'nun eşgüdümlü takvimi ve Birleşik Krallık NCSC'nin üç aşamalı planı, tartışmayı farkındalıktan uygulamaya taşıdı. Avustralya Sinyal Direktörlüğü daha da ileri giderek klasik asimetrik kriptografi için kesin bir 2030 bitiş tarihi belirledi.
> - **Maruziyet asimetriktir.** RSA, ECC ve Diffie–Hellman acil sorundur; SWIFT el sıkışmalarının, TLS'nin, PKI'nin, kod imzalamanın ve takas ağı kimlik doğrulamasının dayandığı asimetrik algoritmalardır. Simetrik şifreleme (AES-256), anahtar uzunlukları korunduğu sürece istikrarlı kalır. Yönetim kurulu düzeyindeki odak, asimetrik yüzeyde olmalıdır.
> - **Harvest-now-decrypt-later gelecekteki bir senaryo değildir.** Rakipler bugün, şifrelenmiş finansal kayıtları, mutabakat kayıtlarını, birleşme ve satın alma materyallerini ve sınır ötesi havale verilerini, kriptografik olarak ilgili bir kuantum bilgisayarı (CRQC) var olduğunda çözme niyetiyle ele geçirip saklıyor. 10–20 yıllık gizlilik gereksinimi olan veriler için bu risk zaten gerçekleşmiştir.
> - **Sektör artık işleyen bir referans noktasına sahip.** Aralık 2025'te yayımlanan [BIS Project Leap Faz 2 ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), TARGET2 genelinde canlı likidite transferlerinde geleneksel dijital imzaları post-kuantum kriptografiyle başarıyla değiştirdi ve her geçiş programının karşılaşacağı belirli mühendislik maliyetlerini (doğrulama gecikmesi, paket boyutu) ortaya çıkardı.
> - **NIST paketi küresel çıpadır.** [FIPS 203 (ML-KEM) ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard") ve FIPS 204 (ML-DSA), ulusal duruşlar parametre kümeleri ve hibrit gereksinimler konusunda ayrışsa bile her büyük yargı bölgesi tarafından referans alınır. Yönetim kurulları ML-KEM-768/ML-DSA-65'i taban, ML-KEM-1024/ML-DSA-87'yi ise uzun ömürlü veriler için ihtiyatlı temel olarak değerlendirmelidir.
> - **Hibrit tek güvenilir yoldur.** Doğrudan geçişler hiçbir büyük otorite tarafından önerilmez. Klasik ve kuantuma dayanıklı algoritmaları paralel çalıştırmak, NCSC, ANSSI, BSI tarafından onaylanan ve Project Leap'te kanıtlanan dağıtım kalıbıdır. Her iki alternatiften de ağırdır, ancak hem bugünün uyumluluğunu hem de yarının tehdidini karşılayan tek yoldur.

---

## Düzenleyici Duruşun Sertleştiği Yıl

Geçtiğimiz on yılın büyük bölümünde, post-kuantum kriptografi uzun vadeli yol haritasının rahat bir köşesinde yaşadı. Kuantum bilgisayarları etkileyici ama uzaktı; RSA ve eliptik eğrilerin dayandığı kriptografik matematik istikrarlı bir zemin olarak görülüyordu; ve geçiş tartışması büyük ölçüde uzman çalışma gruplarıyla sınırlıydı. Bu konum artık savunulabilir değil.

Ocak 2026'da, ABD Hazinesi ve İngiltere Merkez Bankası eş başkanlığındaki [G7 Siber Uzman Grubu bugüne kadarki en önemli bildirisini yayımladı ⧉](https://www.gov.uk/government/publications/advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector/g7-cyber-expert-group-statement-on-advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector-january-20 "G7 CEG Statement on Advancing a Coordinated Roadmap for the Transition to Post-Quantum Cryptography in the Financial Sector"). Belge bir düzenleme değildir, ancak tipik bir rehberden daha fazla ağırlık taşır: kriptografik geçişin artık sistemik bir risk yönetimi meselesi olduğu yönünde, G7 yargı bölgelerindeki maliye bakanlıklarının, merkez bankalarının ve denetim otoritelerinin ortak görüşünü temsil eder. Yol haritası planlama ufkunu 2030'ların ortasına göre hizalar ve kritik finansal sistemlerin daha erken geçiş yapması teşvik edilir; merkez bankacılarının ihtiyatlı dilinde bu ifade, bir öneriden çok bir beklentiye işaret eder.

İki ay önce, BIS Innovation Hub ve Eurosistem, geleneksel dijital imzaları İtalya Merkez Bankası, Banque de France, Deutsche Bundesbank, Nexi-Colt ve Swift arasındaki canlı likidite transferlerinde post-kuantum kriptografiyle değiştiren teknik bir deney olan [Project Leap Faz 2 ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems") sonuçlarını yayımladı. Başlıktaki bulgu bir başarıydı: kuantuma dayanıklı imzalı transferler, işletimsel bir ödeme sistemi boyunca uçtan uca geçti. Başlığın altındaki ayrıntı daha öğreticidir ve bu makalenin ilerleyen bölümlerinde incelenir.

Bu iki olayın birleşimi, yani eşgüdümlü bir G7 politika çerçevesi ve gerçek bir ödeme sisteminde işleyen bir kanıt noktası, teknik topluluğun on yıldır beklediği şeyi üretti: "bu gerçek mi?" sorusuna kesin bir yanıt. Mayıs 2026'da yanıt evet. Geriye kalan soru hız sorusudur.

## Yönetim Kurulunu İlgilendirmesi Gereken Üç Tehdit Vektörü

Geçiş mekaniğini tartışmadan önce, tam olarak neyin risk altında olduğunu net bir şekilde belirtmekte fayda var. Kurumsal bankacılıkta kuantum riski, kriptografik varlık genelinde tekdüze değildir ve yönetim kurulunun dikkati en iyi, maruziyetin en keskin olduğu üç vektöre yönlendirilir.

### 1. Şimdi Topla, Sonra Çöz (HNDL)

En acil endişe gelecek değil. Şimdidir. Devlet düzeyindeki ve gelişmiş suç örgütü rakipler, şifrelenmiş finansal trafiği (havaleler, SWIFT mesaj akışları, birleşme ve satın alma iletişimleri, sınır ötesi mutabakat kayıtları, swap sözleşmeleri ve KYC dosyaları) şu anda okuyamadan sistematik olarak ele geçiriyor ve saklıyor. Amaçları basittir: şimdi sakla, bir CRQC var olduğunda sonra çöz. [Uluslararası Ödemeler Bankası'nın açıkça belirttiği gibi ⧉](https://www.bis.org/about/bisih/topics/cyber_security/leap.htm "Project Leap: quantum-proofing the financial system"), bu toplama zaten sürüyor.

Yönetim kurulları için sonuç rahatsız edici ama nettir: bugün klasik asimetrik şifreleme altında iletilen, gizlilik gereksinimi bir CRQC'nin gelişinin ötesine uzanan her türlü hassas veri, halihazırda ifşa olmuş sayılmalıdır. HNDL gerçekleştiğinde bir ihlal bildirimi olmaz. SIEM'de bir alarm çalmaz. Şifreleme şimdilik dayanır, ancak veriler çevreyi çoktan terk etmiştir.

### 2. Uzun Vadeli Hassasiyet Riski

Kurumsal bankacılık verileri, alışılmadık derecede uzun kurumsal raf ömürlerine sahiptir. Stratejik birleşme ve satın alma belgeleri on yıl boyunca piyasaya duyarlı kalabilir. Ticari sır iletişimleri ve fikri mülkiyet değerlemeleri on beş ila yirmi yıl gizli kalabilir. Sınır ötesi mutabakat kayıtları, merkezi karşı taraf maruziyetleri ve karşı taraf kredi değerlendirmeleri, doğrudan işlemsel ömürlerinin çok ötesinde ticari hassasiyetlerini korur.

Michele Mosca tarafından ilk kez dile getirilen ve artık her ciddi geçiş çerçevesine gömülü olan [Mosca denklemi ⧉](https://www.cryptomathic.com/a-bankers-guide-to-quantum-safe-cryptography-part-3-roadmap-to-pqc-migration-for-financial-institutions-cryptomathic "A Banker's Guide to Quantum Safe Cryptography — Part 3"), sorunu resmileştirir. Eğer **S** verinin raf ömrü, **M** onu koruyan sistemleri geçirmek için gereken süre ve **Q** bir CRQC'nin mevcut olmasına kadar geçen süre ise, o zaman:

```
S + M > Q ise, veriler zaten ifşa olmuştur.
```

Yirmi yıllık gizlilik ufkuna sahip veriler ve gerçekçi olarak tamamlanması beş ila yedi yıl gerektiren bir geçiş programı için, yönetim kurulunun üzerine bahis oynadığı örtük Q değeri en az 25 yıl sonrasıdır. Giderek büyüyen bir uzman değerlendirmesi külliyatı, yani [Forrester'ın 2026 APAC öngörüleri ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC Predictions"), Global Risk Institute'un yıllık anketleri ve QLDPC kodları kullanarak yaklaşık 100.000 fiziksel kübitte CRQC öneren Şubat 2026 tarihli bir mimari makale, bu bahsin güvenli olmadığını öne sürüyor.

### 3. Temel El Sıkışmaların Güvenlik Açığı

Üçüncü vektör mimari açıdan en önemlisidir. Simetrik şifreler (AES-256) görece istikrarlı kalır; Grover algoritması etkin güvenlik düzeyini yarıya indirir, ancak anahtar uzunluğunu iki katına çıkarmak marjı geri kazandırır. Felaket boyutundaki maruziyet asimetrik algoritmalaradır ve bunlar tam olarak kurumsal finanstaki her kimlik doğrulamalı el sıkışmanın dayandığı algoritmalardır: SWIFT açık anahtar altyapısında RSA, TLS istemci/sunucu kimlik doğrulamasında ECDSA, oturum anahtarı oluşturmada ECDH ve istemci mobil kimlik doğrulaması, API imzaları ve kod imzalama hatları boyunca ECC türevleri.

Shor algoritmasını çalıştıran işlevsel bir CRQC, bu sistemleri aşamalı olarak zayıflatmaz. Onları kırar. Bir CRQC işletime girdiğinde, RSA korumalı her el sıkışma, her ECDSA imzası ve her eliptik eğri anahtar değişimi, aylarca süren bir çabayla değil, saatler içinde geri kazanılabilir hale gelir. "Güvenli"den "ele geçirilmiş"e geçiş ikilidir ve etkilenen algoritmayı kullanan her sistemde eşzamanlı olarak yayılır. Düzenleyici aciliyetin dayandığı temel budur.

## Düzenleyici Sıkılaşma: Yargı Bölgesi Bazında Görünüm

Mayıs 2026'daki küresel düzenleyici tablo artık öneriler yamalı bohçası değil. Katılık düzeyi değişen ama aynı hedefte birleşen eşgüdümlü bir takvimler kümesidir. Başlıca finans merkezlerinde faaliyet gösteren çok uluslu bir banka, artık en hoşgörülü değil, en katı geçerli yargı bölgesine tabidir.

### Amerika Birleşik Devletleri

ABD, federal sistemlere dokunan her kurum için en kuralcı duruşa sahiptir. NSA'nın [Commercial National Security Algorithm Suite 2.0 ⧉](https://informedclearly.com/en/technology/46563/quantum-encryption-race-post-quantum-security-standards-2026 "Quantum-Encryption Race 2026") belgesi, ulusal güvenlik sistemleri için ML-KEM-1024 ve ML-DSA-87'yi zorunlu kılar; yeni sistemlerin Ocak 2027'den itibaren PQC dağıtması ve altyapı geçişinin 2035'e kadar tamamlanması gerekir. OMB Memorandumu M-23-02, federal kurumları aynı gidişata bağlar. Ticari bankalar için acil maruziyet, federal tedarik zincirleri, NSS'ye bitişik sözleşmeler ve NSA rehberliğinin daha geniş piyasaya uyguladığı dolaylı baskı yoluyladır.

### Avrupa Birliği

AB üç katmanda çalışıyor. NIS İşbirliği Grubu tarafından Haziran 2025'te ayrıntılandırılan [Avrupa Komisyonu'nun Eşgüdümlü Uygulama Yol Haritası ⧉](https://pqshield.com/pqc-transition-roadmaps-and-guidance/ "PQC Roadmaps and Transition Guidance"), 2026 (ulusal stratejiler), 2030 (yüksek riskli sistemlerin geçişi) ve 2035 (tam geçiş) için aşamalı kilometre taşları belirler. Siber Dayanıklılık Yasası (Cyber Resilience Act), 2027 sonundan itibaren dijital ürünler için en son teknoloji güvenlik yükseltmelerini zorunlu kılacaktır. NIS2, hiçbir direktif açık bir PQC gereksinimi içermese de BİT risk yönetimini güçlendirir. Ancak ulusal düzenleyiciler Komisyon'un önüne geçti. Almanya'nın BSI'si hibrit anahtar değişimini zorunlu kılar ve ML-KEM, FrodoKEM ve Classic McEliece'ten oluşan ihtiyatlı bir sepeti onaylar. Fransa'nın ANSSI'si hem anahtar kapsülleme hem de imzalar için hibrit gerektirir. Hollanda NLNCSA'sı ve Norveç otoriteleri, uzun ömürlü veriler için ihtiyatlı temel olarak ML-KEM-1024 etrafında hizalandı.

### Birleşik Krallık

Birleşik Krallık NCSC'si kesin rehberliğini Mart 2025'te yayımladı ve 2025 Yıllık İnceleme boyunca yeniden teyit etti. Üç aşamalı takvim açıktır:

- **2028'e kadar:** Yükseltme gerektiren kriptografik hizmetleri belirleyin, geçiş planını oluşturun ve eksiksiz bir kriptografik envanter üretin.
- **2028'den 2031'e:** Yüksek öncelikli yükseltmeleri, özellikle kritik sistemlerde ve dışa dönük internet protokollerinde yürütün.
- **2031'den 2035'e:** Tüm sistemler, hizmetler ve ürünler genelinde geçişi tamamlayın.

Birleşik Krallık finans kurumları için, [CMORG (Cross-Market Operational Resilience Group) PQC Rehberliği ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography"), NCSC çerçevesinin yanında yer alır; bankaları kritik ulusal altyapı olarak ele alır ve satıcı hazırlığı ile tedarik zinciri uyumunu vurgular.

### Asya-Pasifik

APAC duruşu daha parçalı ama hızla ilerliyor. Avustralya'nın ASD'si küresel olarak en katı konuma sahip: klasik açık anahtar kriptografisi 2030 sonundan sonra kullanılmamalı, hibrit önerisi yok ve ML-KEM-1024 gerekli (ML-KEM-768 yalnızca 2030'a kadar kabul edilebilir). Kuruluşların 2026 sonuna kadar rafine bir geçiş planına sahip olması gerekir. Singapur Para Otoritesi resmi kuantum-güvenli hazırlık rehberliği yayımladı. Japonya ve Güney Kore önemli yatırımlar yapıyor, ancak her ikisinin de ulusal algoritma hatları var (Kore KEM olarak NTRU+ ve SMAUG-T'yi, imza olarak ALMer ve HAETAE'yi seçti). Hindistan'ın 6.003,65 crore rupilik hükümet harcamasıyla desteklenen Ulusal Kuantum Misyonu, bankacılık ve finansal sistemleri açıkça stratejik öncelik olarak tanımlar. [Forrester'ın 2026 APAC öngörüleri ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC predictions"), bu yıl post-kuantum teknolojilerine yatırım yapması beklenen bölgesel kuruluşların sayısını yüzde 90'ın üzerine koyuyor.

### Net Konum

Bir yönetim kurulu için, bu yargısal konumların pratik sentezi nettir. Çok uluslu bir banka tek bir düzenleyicinin takvimine göre yönetilemez; en katı geçerli takvime göre yönetilmelidir. Çoğu büyük kurum için bu, yüksek riskli sistemler için 2030 sonu ve uzun kuyruk için 2035 sonu planlama ufku anlamına gelir; ASD'ye maruz kalan kuruluşlar 2030'a kadar saf PQC'yi hedeflerken, CNSA'ya maruz kalan kuruluşlar aynı zaman aralığını özellikle ML-KEM-1024 ve ML-DSA-87 ile hedefler.

## BIS Project Leap: Sektörün Gerçekte Kanıtladığı Şey

Project Leap bir yönetim kurulunun dikkatine değer, çünkü bir pazarlama kilometre taşı olduğu için değil, bugüne kadar canlı bir finansal ödeme sisteminde post-kuantum kriptografinin en güvenilir uçtan uca gösterimi olduğu için. Başlıktaki sonuç nettir: işe yarıyor. Altındaki ayrıntı, operasyonel çıkarımların bulunduğu yerdir.

2023'te tamamlanan Faz 1, Fransa Merkez Bankası ile Deutsche Bundesbank'ın BT sistemleri arasında kuantuma dayanıklı bir VPN kurdu; ödeme mesajları Paris ile Frankfurt arasında hibrit bir şifreleme şeması altında iletildi. 2025 sonunda tamamlanan ve [Aralık ayında raporlanan ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems") Faz 2 ise çok daha ileri gitti. Konsorsiyum, geleneksel RSA tabanlı dijital imzaları, Eurosistem'in Gerçek Zamanlı Brüt Mutabakat sistemi olan TARGET2 genelindeki likidite transferlerinin yürütülmesinde post-kuantum imzalarla değiştirdi. Katılımcılar (BIS Innovation Hub Eurosystem Centre, İtalya Merkez Bankası, Banque de France, Deutsche Bundesbank, TARGET2 bağlantısını sağlayan Nexi-Colt ve Swift), altyapısının nihayetinde geçiş yapması gereken kurumları tam olarak temsil ediyor.

Rapor, her geçiş programının içselleştirmesi gereken üç bulguya işaret etti:

- **Doğrulama gecikmesi anlamlı ölçüde daha yüksektir.** Post-kuantum imza doğrulaması, aynı donanımda RSA tabanlı doğrulamadan belirgin ölçüde daha uzun sürdü. Saniyeden kısa mesaj işlemeye göre tasarlanmış bir RTGS sistemi için bu marjinal bir gözlem değildir; bir kapasite planlama girdisidir.
- **Paket boyutları sistemin yeniden geliştirilmesini gerektirir.** PQC imzaları, ECDSA eşdeğerlerinden bir büyüklük mertebesi daha büyüktür (bununla ilgili daha fazla ayrıntı aşağıda). İç kuyrukları, izleme araçları ve veritabanı şemaları eski mesaj boyutlarına göre boyutlandırılmış ödeme sistemleri, yeniden tasarım olmadan yeni yükü barındıramaz. Project Leap, TARGET2'nin hibrit modeli önemli bir yeniden geliştirme olmadan "kolayca barındıramayacağını" açıkça tespit etti.
- **Hibrit doğru yanıttır, ancak daha ağırdır.** Klasik ve post-kuantum algoritmaları paralel çalıştırmak geriye dönük uyumluluğu korudu ve derinlemesine savunma sağladı, ancak kriptografik işlem yükünü iki katına çıkardı. Bu, geçiş sırasında PQC'yi doğru şekilde yapmanın operasyonel maliyetidir; yalnızca akıllıca mühendislikle kaçınılabilir değildir.

Bir PQC iş gerekçesini inceleyen bir CFO için, Project Leap bulguları tam da kesin oldukları için yararlıdır. Post-kuantum geçişinin maliyeti tek bir sermaye kalemi değildir. SLA sözleşmelerine yansıyan doğrulama gecikmesi, depolama ve bant genişliği bütçelerine dokunan mesaj boyutu genişlemesi ve hesaplama kapasitesi planlamasını etkileyen, kopyalanmış kriptografik işlemlerden oluşan bir geçiş dönemidir. Bunların hiçbiri spekülatif değildir. Canlı bir merkez bankası sisteminde ölçülmüşlerdir.

## NIST Araç Seti: ML-KEM ve ML-DSA Karşılaştırması

Her güvenilir ulusal çerçevenin teknik merkezi, Ağustos 2024'te yayımlanan NIST post-kuantum standartları paketidir. Bu standartlardan ikisi kurumsal bankacılık için acil odaktır: anahtar kapsülleme için ML-KEM (FIPS 203) ve dijital imzalar için ML-DSA (FIPS 204). Ortak bir matematiksel temel paylaşırlar; her ikisi de yapılandırılmış kafesler üzerindeki Module Learning With Errors (ML-LWE) ve Module Short Integer Solution problemlerinin zorluğuna dayanır. Ancak kriptografik varlıkta çok farklı roller üstlenirler ve performans ile boyut profilleri önemli ölçüde farklılık gösterir.

### ML-KEM (FIPS 203): Anahtar Kapsülleme

[CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) türetilen ML-KEM, iki tarafın güvensiz bir kanal üzerinden ortak bir simetrik anahtar oluşturması gereken protokollerde ECDH ve RSA-KEM'in yerine geçer. Pratik anlamda, RSA ve ECDH emekliye ayrıldıktan sonra TLS el sıkışmalarının gittiği yerdir. NIST, artan güvenlik gücü ve azalan performansla üç parametre kümesi tanımlar: ML-KEM-512 (NIST Kategori 1), ML-KEM-768 (Kategori 3) ve ML-KEM-1024 (Kategori 5).

### ML-DSA (FIPS 204): Dijital İmzalar

CRYSTALS-Dilithium'dan türetilen ML-DSA, RSA ve ECDSA imzalarının yerine geçer. Sertifika imzalama, kod imzalama, belge imzalama ve kimlik doğrulamayı yönetir. Üç parametre kümesi ML-DSA-44, ML-DSA-65 ve ML-DSA-87 olup, genel hatlarıyla NIST Kategori 2, 3 ve 5'e karşılık gelir.

### Boyut ve Performans Profili

Geçiş kapasitesini boyutlandıran bir CIO için en önemli rakamlar yapıntı (artefakt) boyutlarıdır. Bunlar ağ kapasitesi planlaması, depolama projeksiyonları ve protokol düzeyinde test için girdilerdir.

| Algoritma | Açık Anahtar | Şifreli Metin / İmza | En Yakın Klasik Eşdeğer | Klasik Boyuta Göre |
|---|---|---|---|---|
| ML-KEM-512 | 800 bayt | 768 bayt (şifreli metin) | ECDH P-256 (~32 baytlık açık anahtar) | ~25× daha büyük |
| ML-KEM-768 | 1.184 bayt | 1.088 bayt (şifreli metin) | ECDH P-384 | ~25× daha büyük |
| ML-KEM-1024 | 1.568 bayt | 1.568 bayt (şifreli metin) | ECDH P-521 | ~25× daha büyük |
| ML-DSA-44 | 1.312 bayt | ~2.420 bayt (imza) | ECDSA P-256 (64 baytlık imza) | ~38× daha büyük |
| ML-DSA-65 | 1.952 bayt | ~3.293 bayt (imza) | ECDSA P-384 | ~50× daha büyük |
| ML-DSA-87 | 2.592 bayt | ~4.595 bayt (imza) | ECDSA P-521 | ~70× daha büyük |

*Kaynak: [NIST FIPS 203 ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard") ve FIPS 204 spesifikasyonlarının sentezi; bağımsız kıyaslama literatüründen karşılaştırmalı verilerle.*

Doğrudan üç operasyonel çıkarım ortaya çıkar. **İlk olarak**, imza boyutu çoğu kurumsal dağıtım için bağlayıcı kısıttır. Bir ML-DSA-65 imzası, bir ECDSA P-256 imzasının yaklaşık elli katıdır ve ara CA'lar taşıyan TLS sertifika zincirleri orantılı olarak büyür. Bu yüzeydeki kapasite çalışması isteğe bağlı değildir; yük taşıyıcıdır. **İkinci olarak**, ML-KEM hesaplama açısından ECDH ile rekabetçidir ve bazı uygulamalarda, özellikle temel kafes aritmetiği için vektörleştirilmiş desteğe sahip donanımda, anlamlı ölçüde daha hızlıdır. **Üçüncü olarak**, ML-DSA doğrulaması tutarlı biçimde hızlıdır (çoğu zaman ECDSA doğrulamasından daha hızlı), ancak ML-DSA imzalama, kısıtlı donanımda birden fazla deneme gerektirebilen bir reddetme örneklemesi (rejection sampling) döngüsü içerir. Yüksek hacimli imzalama hizmetleri için bu, varsayılacak değil doğrulanacak bir kıyaslamadır.

### Parametre Kümelerini Seçmek

Parametre seçimine ilişkin yargısal konumlar birebir aynı değildir, ancak yakınsama nettir. ML-KEM-768 ve ML-DSA-65 kurumsal tabandır; Birleşik Krallık NCSC tarafından Birleşik Krallık kuruluşları için temel olarak onaylanır ve çoğu Avrupa çerçevesi altında kabul edilebilir. ML-KEM-1024 ve ML-DSA-87 ihtiyatlı tavandır; ABD ulusal güvenlik sistemleri için NSA CNSA 2.0 tarafından zorunlu kılınır ve 2030'a kadar Avustralya düzenlemesine tabi kuruluşlar için ASD tarafından gerekli görülür. Aşırı uzun vadeli hassasiyete sahip veriler için (egemen mutabakat kayıtları, on yıldan uzun fikri mülkiyet, uzun vadeli enstrümanların saklama kayıtları) daha yüksek parametre kümeleri savunulabilir varsayılan seçenektir.

### Ortak Bir Matematiksel Temel, Ortak Bir Risk

Yönetim kurulu düzeyinde dikkate değer bir nokta: hem ML-KEM hem de ML-DSA güvenliklerini aynı kafes problemleri ailesinden alır. Module-LWE'ye karşı gelecekteki bir kriptanalitik atılım, her iki standardı da eşzamanlı olarak etkilerdi. Birkaç ulusal otoritenin, özellikle Almanya'nın BSI'si ve Fransa'nın ANSSI'si, uzun vadeli imzalama ve kod imzalama kullanım durumları için kafes tabanlı yığını karma tabanlı imzalarla (SLH-DSA, FIPS 205) tamamlamayı önermesinin nedeni tam olarak budur. Bu anlamda kripto-çeviklik, yalnızca RSA'yı ML-KEM ile değiştirebilmekle ilgili değildir. Kriptanalitik ortam değiştiğinde bir PQC algoritmasını bir diğeriyle değiştirebilmekle ilgilidir.

## Mantıksal Bir Geçiş Yolu: Keşif → Triyaj → Hibrit Dağıtım

Çok yıllı bir PQC programını onaylayan bir yönetim kurulu için operasyonel soru, kabul edilemez hizmet erişilebilirliği riski almadan işin nasıl aşamalandırılacağıdır. G7 yol haritası, NCSC çerçevesi, BIS Project Leap ve büyük ulusal rehberlik belgeleri genelinde ortaya çıkan kalıp üç aşamada birleşir.

```
┌──────────────────────┐   ┌──────────────────────┐   ┌──────────────────────┐
│  1. KEŞİF & CBOM     │ → │  2. TRİYAJ (MOSCA)   │ → │  3. HİBRİT DAĞITIM   │
│  Tüm sistemlerde     │   │  Veri raf ömrüne     │   │  Çift zarf:          │
│  kriptografik        │   │  göre risk temelli   │   │  klasik + PQC,       │
│  envanter            │   │  önceliklendirme     │   │  kripto-çevik        │
└──────────────────────┘   └──────────────────────┘   └──────────────────────┘
```

### Faz 1: Keşif ve Kriptografik Malzeme Listesi (CBOM)

Haritası çıkarılmamış bir kriptografik varlık için geçiş planlanamaz ve çoğu kurum doğru bir haritaya sahip değildir. Bu nedenle ilk aşama, bir Kriptografik Malzeme Listesi (Cryptographic Bill of Materials) üretmektir; kuruluş genelindeki her asimetrik kriptografi örneğinin, algoritma, anahtar uzunluğu, protokol bağlamı, veri hassasiyeti ve sistem sahibi için etiketlendiği yapılandırılmış bir envanter. Kod tabanları, web uygulamaları, konteyner imgeleri, veritabanı yapılandırmaları, sertifika depoları, donanım güvenlik modülleri ve satıcı arayüzleri genelinde otomatik tarama pratik mekanizmadır; eski sistemlerin ve tescilli protokollerin manuel envanteri ise kaçınılmaz tamamlayıcıdır.

Faz 1'in çıktısı gösterişli değildir, ancak Faz 2 ve 3'ün üzerine oturabileceği tek temeldir. Ayrıca, PQC uyumluluk beyanları istenmeye başlandığında çoğu iç denetim işlevinin ve dış düzenleyicinin ilk arayacağı teslimattır.

### Faz 2: Mosca Denklemiyle Risk Triyajı

CBOM elde edildiğinde, kurum Mosca'nın çerçevesini varlık varlık uygulayabilir. Her kriptografik bağımlılık için soru, **S + M > Q** olup olmadığıdır; verinin raf ömrü artı geçiş süresinin, bir CRQC'ye kadar tahmini süreyi aşıp aşmadığıdır. Eşitsizliğin en keskin olduğu varlıklar (geçmesi yıllar süren altyapıdaki uzun ömürlü hassas veriler) kuyruğun başına geçer. Kısa veri ömürlerine veya halihazırda modernize edilmiş altyapıya sahip varlıklar programda daha sonra sıralanabilir.

Bu, yönetim kurulunun risk iştahının en görünür olduğu aşamadır. Kurumun karşısına planlamayı seçtiği Q değeri, aslında kuantum donanımı ilerlemesinin hızına ilişkin stratejik bir bahistir. İhtiyatlı bir Q (2030'ların ortası) daha agresif bir geçiş planı ve daha yüksek bir kısa vadeli sermaye kalemi üretir. İyimser bir Q (2040 sonrası) daha rahat bir plan ve halihazırda toplanmakta olan verilere daha yüksek bir kalıntı maruziyet üretir. Hiçbiri yanlış değildir; her ikisi de teknoloji işlevinin örtük varsayılanları değil, yönetim kurulunun açık kararları olmalıdır.

### Faz 3: Hibrit Dağıtım

Öncelikli varlıklar belirlendikten sonra dağıtım, Project Leap'te kanıtlanan ve NCSC, ANSSI, BSI ile G7 yol haritası tarafından onaylanan hibrit kalıbı izlemelidir. Hibrit bir dağıtım, klasik bir algoritma ile bir post-kuantum algoritmasını paralel çalıştırır ve çıktılarını tek bir zarfta birleştirir. Bileşik yapı, hem klasik saldırılara (klasik algoritma bugün dayanır) hem de kuantum saldırılarına (PQC algoritması yarın dayanır) karşı güvenlidir. Özellikle, yaygın kalıp anahtar kapsülleme için ML-KEM-768 veya ML-KEM-1024 ile birleştirilmiş X25519 ve çift imzanın operasyonel olarak uygulanabilir olduğu yerlerde imzalar için ML-DSA ile birleştirilmiş ECDSA'dır.

Project Leap'in hibridin herhangi bir saf yaklaşımdan "çok, çok daha ağır" olduğu bulgusu, bu öneriye dürüst bir karşı ağırlıktır. Yönetim kurulları geçiş sırasında hesaplama ve depolama kapasitesi artışı, daha uzun el sıkışmalar ve ek sertifika zinciri karmaşıklığı beklemelidir. Ödün şudur: hibrit, geçişin en büyük tek risk kaynağını ortadan kaldırır; üretim ortamında bir kriptografik temelden diğerine uçurum kenarındaki ani geçiş.

## Bunun Maliyeti ve Hiçbir Şey Yapmamanın Neden Daha Pahalı Olduğu

Mastercard'ın [2026 başında raporlanan ⧉](https://www.qnulabs.com/blog/bank-2030-expiry-date-q-day-fatal-strategy "Your Bank's 2030 Expiry — QNu Labs") analizi, küresel finans sektörü PQC geçiş maliyetini 28–42 milyar dolar olarak koydu. Bu toplam içinde, gerçek kurumsal harcamaları izleyen [RedCompass Labs ve CMORG araştırması ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography"), birinci kademe bankaların hazırlık programlarına yıllık 20–30 milyon dolar ayırdığını ve uygulama takvimlerinin birden fazla liderlik dönemine yayıldığını gösteriyor. Bunlar önemli rakamlardır. Ancak ilgili karşılaştırma bu değildir.

İlgili karşılaştırma, tek bir geriye dönük şifre çözme olayının maliyetidir. Toplanan havale trafiği, birleşme ve satın alma yazışmaları veya karşı taraf maruziyet verileri 2032'de bir rakip için okunabilir hale gelen bir kurum için, operasyonel ve itibari maliyet geçiş sermaye harcaması kalemiyle sınırlı değildir. Altta yatan on yıllık stratejik bilginin değeriyle sınırlıdır ve bu, sistemik açıdan önemli herhangi bir kurum için, akla yatkın herhangi bir geçiş bütçesinden önemli ölçüde büyüktür. G7'nin kriptografik geçişi bir teknoloji yükseltmesi yerine sistemik bir risk yönetimi meselesi olarak çerçevelemesi doğrudur ve yönetim kurulları buna bu temelde yaklaşmalıdır.

Ayrılması gereken ikinci bir maliyet kalemi var. PQC'ye geçiş, kripto-çeviklik için bir zorlayıcı işlevdir; kriptografik algoritmaları, onlara bağımlı sistemleri yeniden inşa etmeden değiştirebilme mimari kabiliyeti. Çoğu kurum şu anda kripto-çevikliğe sahip değildir; RSA ve ECC bağımlılıkları, onlarca yıl boyunca birikmiş PKI'lere, kod imzalama zincirlerine, satıcı entegrasyonlarına ve özel protokollere derinlemesine gömülüdür. PQC geçişinin baskısı altında yapılan çeviklik yatırımı kalıcıdır. Bir sonraki kriptografik geçiş geldiğinde yeniden kullanılacaktır; bu ister kafes tabanlı PQC'nin bir ardılı, ister bir kuantum anahtar dağıtımı katmanı, ister henüz standart yol haritasında olmayan bir şey olsun. Doğru ele alındığında, PQC geçiş sermaye harcaması, yinelenen opsiyonellik sağlayan tek seferlik bir yatırımdır.

## Sonuç

Post-kuantum geçişini 2026'da yönetim kurulu düzeyinde bir öncelik olarak ele almanın gerekçesi, bir CRQC'nin yakınlığı üzerine kurulu değildir. Buna ilişkin tahminler gerçekten belirsiz kalır; güvenilir akademik görüş, 2028'e kadar bir CRQC olasılığını yüzde birin oldukça altına, 2037–2040'a kadar ise yaklaşık yüzde elliye koyar. Gerekçe, belirsiz olmayan üç başka gözlem üzerine kuruludur.

İlk olarak, harvest-now-decrypt-later bugün gerçekleşiyor ve on yıldan uzun gizlilik gereksinimi olan veriler, CRQC'nin ne zaman geleceğinden bağımsız olarak ifşa durumundadır. İkinci olarak, büyük bir finans kurumunun kriptografik varlığının geçişi, yeterli finansman ve liderlik odağıyla bile beş ila yedi yıl sürer; yani 2026'da başlayan program 2031 civarında biter ki bu, CRQC olasılık dağılımının ihtiyatlı ucunun oldukça içindedir. Üçüncü olarak, düzenleyici beklentiler son on iki ayda önemli ölçüde sertleşti ve 2026 yönetim kurulu tutanaklarında net bir PQC programı kaydeden kurumlar, tutanaklarında yalnızca bir izleme tutumu kaydedenlere göre anlamlı ölçüde daha güçlü bir konumda olacaktır.

Şimdi başlayan kurumlar seçim avantajına sahiptir. İşi liderlik dönemleri boyunca sıralayabilir, daha geniş dayanıklılık girişimleriyle bütünleştirebilir ve hibrit dağıtımın operasyonel maliyetlerini normal sermaye planlaması içinde soğurabilirler. Bekleyen kurumlar aynı işle daha sıkı son tarihler altında, daha az sıralama imkânıyla ve PQC yeteneğine sahip donanım, uzmanlık ve satıcı kapasitesi üzerindeki tedarik kısıtları arka planında karşılaşacaktır. Erken hareket etmenin maliyeti bilinir; geç hareket etmenin maliyeti, tam da risk yönetiminin önlemek için tasarlandığı biçimde asimetriktir.

Bu sitedeki önceki bağlam için, [kuantum eşiği sıkışması üzerine Nisan 2026 yazısı](https://sebastienrousseau.com/2026-04-11-quantum-thresholds-are-moving-again/index.html "Quantum Thresholds Are Moving Again") temel donanım gidişatını inceledi; [CRYSTALS-Kyber üzerine Kasım 2023 analizi](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age") artık ML-KEM olarak standartlaştırılan matematiksel temelleri ele aldı; [Kuantum Anahtar Dağıtımı üzerine Aralık 2023 makalesi](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution Revolutionising Security in Banking") tamamlayıcı [QKD](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html) katmanını ele aldı; ve [KyberLib açık kaynak referans uygulaması](https://sebastienrousseau.com/2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats/index.html "KyberLib: A Rust-Powered Shield Against Quantum Threats"), kriptografik yüzeyi doğrudan incelemek isteyen kurumlar için temel ilkellerin işleyen bir Rust uygulamasını sunar. Yönetim kurullarının güvenilir geçiş programlarını uyumluluk tiyatrosundan ayırması, yalnızca düzenleyici başlıklarla değil, pratik ve teknik ayrıntıyla ilgilenmesiyle olur.

## Sıkça Sorulan Sorular

**Kriptografik olarak ilgili bir kuantum bilgisayarı gerçekte ne zaman var olacak?**

Güvenilir tahminler geniş ölçüde farklılık gösterir. 2026 başı itibarıyla, kamuya açık kuantum gösterimleri kabaca 24 ila 28 mantıksal kübite ulaştı; bir CRQC'nin ise hata düzeltme yaklaşımına bağlı olarak, 100.000 ile birkaç milyon fiziksel kübit arasında bir şeyle desteklenen yaklaşık 6.000 mantıksal kübit gerektirdiği tahmin ediliyor. Uzman uzlaşması, CRQC olasılığını 2028'e kadar yüzde birin altına, 2037–2040 aralığında yaklaşık yüzde elliye koyar; tahminler arasında önemli değişkenlik vardır. Teorik kaynak tahminlerindeki son azalmalar (birkaç yıl önce 20 milyon kübitten Gidney'in 2025 çalışmasında bir milyonun altına ve Şubat 2026 QLDPC mimari makalesinde yaklaşık 100.000'e) planlama ufkunu sıkıştırdı. Yönetim kurulu amaçları için uygun planlama varsayımı, yüksek riskli sistemler için 2030'ların ortası, ihtiyatlı orta nokta olarak 2030'ların sonu ve bağlayıcı endişe HNDL maruziyetiyse daha erkendir.

**Neden saf post-kuantum yerine hibrit dağıtım?**

Üç neden. İlk olarak, ML-KEM ve ML-DSA, iyi incelenmiş olsalar da, RSA ve ECC'den daha kısa kriptanalitik geçmişlere sahiptir. Hibrit bir şema, bileşenlerden biri dayandığı sürece güvenli kalır; saf bir PQC şeması, kafes problemi beklenmedik şekilde zayıflatılırsa ifşa olur. İkinci olarak, hibrit, henüz geçiş yapmamış karşı taraflarla geriye dönük uyumluluğu korur; bu, çok yıllı bir sektör geçişinde kritiktir. Üçüncü olarak, Avustralya Sinyal Direktörlüğü dışındaki her büyük otorite geçiş dönemi için açıkça hibrit önerir: NCSC, ANSSI, BSI, NLNCSA ve G7 çerçevesinin tümü çift zarf yaklaşımını onaylar. Project Leap'in ölçtüğü gibi ödün, anlamlı ölçüde daha yüksek hesaplama ve depolama yüküdür. Bu, opsiyonelliğin bedelidir.

**Hem ML-KEM hem de ML-DSA'ya ihtiyacımız var mı, yoksa birini seçebilir miyiz?**

Her ikisi de. ML-KEM ve ML-DSA farklı kriptografik roller üstlenir. ML-KEM, iki tarafın ortak bir simetrik anahtar üzerinde anlaşması gereken TLS, VPN'ler, mobil kimlik doğrulama ve benzeri protokollerdeki anahtar oluşturma ilkellerinin yerine geçer. ML-DSA, PKI sertifikalarındaki dijital imza ilkellerinin, kod imzalamanın, belge imzalamanın, SWIFT tarzı kimlik doğrulamalı mesajlaşmanın ve kimlik iddialarının yerine geçer. Bir kurumun kriptografik varlığı, her iki tür ilkeli de farklı yerlerde kullanır; geçiş her ikisini de ele almalıdır. ML-DSA'nın önemli ölçüde daha büyük imza boyutu (ECDSA'nın 50–70 katı) genellikle ikisinden operasyonel açıdan daha zorlayıcı olanıdır; ML-DSA için ağ ve depolama planlama çalışması çoğu geçiş kapasitesi değerlendirmesine egemendir.

**Bu kadar büyük bir programda ilerlemeyi nasıl ölçeriz?**

Üç metrik pratiktir ve başlıca düzenleyici çerçevelerle hizalanır. **CBOM kapsamı**: kurumun asimetrik kriptografik örneklerinin yüzde kaçının envanterlendiği, sınıflandırıldığı ve geçiş önceliği için etiketlendiği. **Yüksek riskli varlıkların geçiş kapsamı**: Mosca'nın S + M > Q koşulunun geçerli olduğu varlıkların yüzde kaçının hibrit PQC'ye taşındığı. **Kripto-çeviklik kapsamı**: kriptografik bağımlılığa sahip sistemlerin yüzde kaçının kod değişikliği olmadan, yalnızca yapılandırmayla algoritma değiştirebildiği. G7 CEG yol haritası, NCSC üç aşamalı çerçevesi ve AB eşgüdümlü yol haritası, farklı terminoloji kullanmalarına rağmen kabaca bu üç ölçüye karşılık gelir.

**Bir yıl daha beklemenin maliyeti nedir?**

Sıfır değildir ve simetrik değildir. Bir yıl beklemek, uzun ömürlü veriler üzerinde bir yıllık HNDL korumasından feragat eder; gizlilik gereksinimi 2040'a uzanan veriler gerekenden bir yıl daha uzun süre ifşa durumundadır. Sabit düzenleyici son tarihlere (ASD 2030, NSA CNSA 2.0 kilometre taşları, AB 2030 kritik sistemler hedefi) karşı geçiş penceresini sıkıştırır ki bu, daha yüksek teslimat riski ve azalmış sıralama esnekliği anlamına gelir. Kurumu, piyasada halihazırda görünür olan ve sektörün en büyük oyuncuları planlamadan uygulamaya geçtikçe kötüleşecek satıcı ve yetenek tedarik kısıtlarına maruz bırakır. Maliyet herhangi bir tek yılda felaket boyutunda değildir, ancak birikir ve düzenleyici ortam, yönetim kurullarının harcamayı değil gecikmeyi açıklamasının beklendiği bir konuma yakınsıyor.

## Kaynaklar

- Sebastien Rousseau, (2026). [Quantum Thresholds Are Moving Again](https://sebastienrousseau.com/2026-04-11-quantum-thresholds-are-moving-again/index.html "Quantum Thresholds Are Moving Again").
- Sebastien Rousseau, (2023). [CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age").
- Sebastien Rousseau, (2023). [Quantum Key Distribution Revolutionising Security in Banking](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution Revolutionising Security in Banking").
- Sebastien Rousseau, (2023). [KyberLib: A Rust-Powered Shield Against Quantum Threats](https://sebastienrousseau.com/2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats/index.html "KyberLib: A Rust-Powered Shield Against Quantum Threats").
- G7 Cyber Expert Group, (2026). [Advancing a Coordinated Roadmap for the Transition to Post-Quantum Cryptography in the Financial Sector ⧉](https://www.gov.uk/government/publications/advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector/g7-cyber-expert-group-statement-on-advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector-january-20 "G7 CEG Statement, January 2026"). GOV.UK.
- Bank for International Settlements, (2025). [Project Leap Phase 2: Quantum-Proofing Payment Systems ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"). BIS.
- Bank for International Settlements, (2025). [Project Leap: Quantum-Proofing the Financial System ⧉](https://www.bis.org/about/bisih/topics/cyber_security/leap.htm "Project Leap: quantum-proofing the financial system"). BIS.
- NIST, (2024). [FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism Standard ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard"). NIST.
- UK NCSC, (2025). [Timelines for Migration to Post-Quantum Cryptography ⧉](https://www.ncsc.gov.uk/guidance/pqc-migration-timelines "Timelines for migration to post-quantum cryptography — NCSC"). UK National Cyber Security Centre.
- CMORG, (2025). [Guidance for Post-Quantum Cryptography ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography"). Cross-Market Operational Resilience Group.
- Post-Quantum Cryptography Coalition, (2025). [International PQC Requirements ⧉](https://pqcc.org/international-pqc-requirements/ "International PQC Requirements — Post-Quantum Cryptography Coalition"). PQCC.
- PQShield, (2025). [PQC Roadmaps and Transition Guidance ⧉](https://pqshield.com/pqc-transition-roadmaps-and-guidance/ "PQC Roadmaps and Transition Guidance"). PQShield.
- Banking.Vision, (2026). [The Year of Quantum Computing: 2026 ⧉](https://banking.vision/en/the-year-of-quantum-computing/ "The Year of Quantum Computing 2026"). Banking.Vision / msg for banking.
- The Quantum Insider, (2026). [How to Prep For Post-Quantum Cryptography: G7 Releases Roadmap ⧉](https://thequantuminsider.com/2026/01/15/how-to-prep-for-post-quantum-crytography-g7-releases-roadmap-to-help-financial-sector-navigate-transition-to-quantum-era/ "How to Prep For Post-Quantum Cryptography — The Quantum Insider"). The Quantum Insider.
- Quantum Computing Report, (2026). [Shor, QLDPC Codes, and the Compression of RSA-2048 Resource Estimates ⧉](https://quantumcomputingreport.com/shor-qldpc-codes-and-the-compression-of-rsa-2048-resource-estimates-part-i/ "Shor, QLDPC Codes, and the Compression of RSA-2048 Resource Estimates"). Quantum Computing Report.
- Cryptomathic, (2025). [A Banker's Guide to Quantum Safe Cryptography — Roadmap to PQC Migration for Financial Institutions ⧉](https://www.cryptomathic.com/a-bankers-guide-to-quantum-safe-cryptography-part-3-roadmap-to-pqc-migration-for-financial-institutions-cryptomathic "A Banker's Guide to Quantum Safe Cryptography"). Cryptomathic.
- Forrester, (2025). [2026 Asia Pacific Predictions: Quantum Security ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC Predictions"). Forrester Research.
- The Asian Banker, (2025). [Building Resilience for a Quantum-Ready Financial System ⧉](https://www.theasianbanker.com/updates-and-articles/building-resilience-for-a-quantum-ready-financial-system "Building resilience for a quantum-ready financial system"). The Asian Banker.
