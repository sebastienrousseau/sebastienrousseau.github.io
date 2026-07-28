---
title: "Yeni bir kripto para ve daha hızlı ödeme çözümünün tanıtımı"
subtitle: "Yeni nesil finans için yeni bir kripto para ve daha hızlı ödeme çözümü."
description: "2018'in başında EXTC platformu, Ethereum ERC-223 akıllı sözleşmeleri aracılığıyla daha hızlı sınır ötesi ödemeleri araştırdı; merkeziyetsiz finansın daha sonra inşa edeceği yapının erken bir taslağı."
date: "February 4, 2018"
language: "tr-TR"
locale: "tr_TR"
banner: "https://cloudcdn.pro/stocks/images/laureen-missaire-DBbuhMbAIsQ.webp"
banner_alt: "Kahverengi ahşap masanın üzerinde kapalı bir dizüstü bilgisayar"
keywords: "EXTC, ERC-223, Ethereum akıllı sözleşmeleri, daha hızlı ödemeler, kripto para, blockchain ödemeleri, ödeme tokenı, merkeziyetsiz finans, ERC-20, sınır ötesi ödemeler"
---


![Üzerinde çok sayıda delik bulunan çok yüksek bir bina](https://cloudcdn.pro/stocks/images/laureen-missaire-DBbuhMbAIsQ.webp).class=\"img-fluid clearfix\"

> **Yönetici Özeti / Önemli Çıkarımlar**
>
> - **Temel hipotez.** Ethereum akıllı sözleşmeleri, sınır ötesi ödemelerde muhabir bankacılığın aktarma yarışının yerini alabilir; ödemeler günler yerine saniyeler içinde sonuçlanır ve yüzde 3-7'lik komisyon katmanı ortadan kalkar ([Dünya Bankası, 2018](https://www.worldbank.org/en/topic/migrationremittancesdiasporaissues/brief/migration-remittances-data "Dünya Bankası Havale Fiyatları")).
> - **ERC-223'ün özel katkısı.** Standart, akıllı sözleşmelerin bir `tokenFallback` fonksiyonu sunmasını zorunlu kılarak ERC-20'deki sessiz token kaybı kusurunu giderdi; başarısız transferler, tokenları geri döndürülemez biçimde yakmak yerine geri alınır ([Ethereum EIP'leri](https://eips.ethereum.org/EIPS/eip-20 "EIP-20: Token Standardı")).
> - **EXTC'nin ödeme ilkelleri.** Token tasarımı; tekil atomik transferleri, zaman tetiklemeli düzenli ödeme talimatlarını, çok imzalı kurumsal ödemeleri ve teminata dayalı anlık mikro kredileri destekliyordu ve bunların tümü bir takas kurumu olmadan gerçekleşiyordu.
> - **Deneyin ortaya koyduğu şey.** Teknik tasarım tutarlıydı ancak 2018'de Ethereum ana ağı saniyede yaklaşık 15 işlem gerçekleştiriyordu. Ölçekli ödeme hacmi, henüz üretime hazır olmayan Layer-2 çözümleri gerektiriyordu.
> - **Miras.** EXTC'deki mimari fikirler, yani programlanabilir para, atomik mutabakat ve uyumun gömülü olduğu token mantığı, sonraki DeFi protokollerinde, CBDC tasarımlarında ve tokenlaştırılmış mevduat çerçevelerinde yeniden ortaya çıktı.

---

## Sorun: 2018'de Sınır Ötesi Ödemeler

2018'in başında uluslararası ödemeler tasarımı gereği yavaş, pahalı ve şeffaflıktan uzaktı. Birleşik Krallık'tan Güneydoğu Asya'ya yapılan bireysel bir transfer genellikle iki ila dört muhabir bankayı içeriyordu; her biri bir komisyon alıyor ve mutabakat zincirine bir gün ekliyordu. Dünya Bankası'nın Remittance Prices Worldwide veri tabanı, 2018'in ilk çeyreğinde 200 USD tutarındaki bir havale için yüzde 6,9'luk küresel bir ortalama maliyet kaydetti.

Kripto para, eşler arası dijital nakdin teknik olarak uygulanabilir olduğunu zaten göstermişti. Bitcoin, işlemleri dünya genelinde yaklaşık on dakikada sonuçlandırıyordu ve Ethereum'un programlanabilir katmanı akıllı sözleşmeleri, yani ödeme kurallarını doğrudan transferin içine kodlayabilen kendi kendine yürütülen kodu ekledi. Zincir üzerinde teknik olarak mümkün olan ile eski muhabir bankacılığın sunduğu arasındaki boşluk, EXTC'nin girdiği tasarım alanıydı.

## Teknik Temel: ERC-20 ve Kusuru

Ethereum Improvement Proposal 20 ile resmileştirilen ERC-20 standardı, ikame edilebilir tokenlar için standart arayüzü tanımladı: `balanceOf`, `transfer`, `transferFrom`, `approve` ve `allowance`. 2018'in başına gelindiğinde ERC-20, ana ağda dağıtılmış yüzlerce tokenla birlikte baskın token standardıydı.

Ancak ERC-20'nin yapısal bir sorunu vardı. Tokenlar standart `transfer` fonksiyonu kullanılarak doğrudan bir akıllı sözleşme adresine gönderildiğinde, sözleşmenin gelen transferi algılamasının veya buna göre işlem yapmasının bir yolu yoktu. Bu şekilde gönderilen tokenlar kalıcı olarak sıkışıp kalıyordu. Ethereum topluluğu, 2018'in ortasına kadar bu yolla milyonlarca dolarlık ERC-20 tokenının kaybedildiğini tahmin etti.

Dexaran tarafından Ethereum GitHub sorun takipçisinde önerilen ERC-223, alıcı sözleşmelere bir `tokenFallback(address _from, uint _value, bytes _data)` fonksiyon zorunluluğu ekleyerek bunu çözdü. Alıcı sözleşme `tokenFallback` fonksiyonunu uygulamıyorsa transfer geri alınıyor ve tokenlar gönderene iade ediliyordu. Bu, ERC-223 transferlerini atomik hâle getirdi: sözleşme ya tokenları kabul edip mantığını yürütüyor ya da işlem temiz biçimde başarısız oluyordu.

## EXTC Token Tasarımı

Express Transaction Credits tokenı beş temel özellik etrafında tasarlandı:

- **Ad, sembol ve ondalıklar.** Standart ERC-223 kimlik alanları; sent altı hassasiyet için 18 ondalık basamak.
- **Toplam arz.** Basım anında sabitlenir; kaybolan veya talep edilmeyen tokenlar yeniden çıkarılamadığı için EXTC deflasyonist bir varlık hâline gelir.
- **Bakiye ve transfer.** ERC-223'ün `tokenFallback` zorunluluğuyla genişletilmiş standart okuma ve yazma fonksiyonları.
- **Çok imzalı destek.** Kurumsal ödemeler, yürütülmeden önce birden fazla yetkili adresten ortak imza gerektiriyor ve merkezî bir takas kurumu olmadan denetim izleri sağlıyordu.
- **Zaman kilitli transferler.** Düzenli ödeme talimatı ilkeli, EXTC'nin gelecekteki ödemeleri planlamasına olanak tanıyordu; bu, geleneksel banka transferlerinin ancak dışarıdan bir talimatla elde edebildiği bir yetenekti.

## Platformun Hedeflediği Ödeme İlkelleri

EXTC'nin mimarisi, eski sistemlerin verimsiz biçimde ele aldığı dört belirli ödeme iş akışının yerini alacak şekilde tasarlandı:

**Tekil atomik ödemeler:** tek bir Ethereum işleminde sonuçlanan, 2018 ana ağında genellikle 15-30 saniye içinde tamamlanan tek seferlik bir transfer.

**Zaman esaslı düzenli ödeme talimatları:** zaman kilitli akıllı sözleşme çağrıları olarak kodlanan yinelenen transferler; bir bankanın periyodik talimatları almasına ve yeniden yürütmesine gerek bırakmaz.

**Kurumsal toplu ödemeler:** tek bir işlemde birden fazla alıcıya yapılan toplu ödemeler; her bir transfer çok imzalı yetkilendirme gerektirir, böylece maliyet ve karşı taraf riski azalır.

**Teminata dayalı anlık krediler:** borç alanlar EXTC tokenlarını bir akıllı sözleşmede teminat olarak kilitliyordu; sözleşme, teminatı aldığında kredi tutarını bir kredi komitesi veya değerlendirme gecikmesi olmadan otomatik olarak serbest bırakıyordu.

## Deneyin Ortaya Koyduğu Şey

EXTC tasarımı teknik olarak tutarlıydı. ERC-223 temeli, baskın token standardının en önemli güvenlik kusurunu giderdi ve ödeme ilkelleri, muhabir bankacılığın verimsiz biçimde ele aldığı gerçek iş akışlarına doğrudan karşılık geliyordu.

Pratik kısıt Ethereum'un işlem kapasitesiydi. 2018'in ilk çeyreğinde ana ağ, blok başına yaklaşık 8 milyonluk gas limitiyle saniyede ortalama 15 işlem yapıyordu. Küresel havale hacminin küçük bir kısmını bile işleyen bir ödeme ağı, ana ağı dakikalar içinde doyuma ulaştırırdı; Dünya Bankası 2017'de 270 milyon göçmenin ülkelerine para gönderdiğini tahmin ediyordu.

Layer-2 ölçekleme çözümleri, özellikle durum kanalları ve daha sonra rollup teknolojisine dönüşen erken sürümler, 2018'de etkin biçimde araştırılıyordu ancak üretime hazır değildi. Lightning Network, Ocak 2018'de önemli çekincelerle Bitcoin ana ağında yeni devreye alınmıştı. Blockchain tabanlı bir ödeme ağının muhabir banka ölçeğinde çalışması için gereken teknik ön koşullar henüz mevcut değildi.

## Ayakta Kalan Fikirler

EXTC'den ve aynı dönemdeki ödeme tokenı projelerinden birkaç mimari kavram, sonraki gelişmelerle doğrulandı:

**Programlanabilir para**, yani ödeme kurallarının doğrudan transfer mantığına kodlanması, sırasıyla 2018 ve 2020'de kullanıma sunulan Compound ve Aave gibi DeFi kredi protokollerinin temel bir özelliği hâline geldi.

**Takas kurumları olmadan atomik mutabakat**, yani bir transferin ya tümüyle başarılı olması ya da geri alınması özelliği, artık tokenlaştırılmış mevduat çerçevelerinde ve İngiltere Merkez Bankası ile Avrupa Merkez Bankası dâhil merkez bankalarının incelediği toptan CBDC mimarilerinde bir tasarım gereksinimidir.

**Uyumun gömülü olduğu tokenlar**, yani token sözleşmesinin kendisinde kodlanan transfer kısıtlamaları ve raporlama yükümlülükleri, ERC-1400 (menkul kıymet tokenları) gibi düzenlemeye tabi token standartlarında ve Project Agorá ile benzeri çok merkez bankalı tokenlaştırma deneylerinin uyum katmanı tasarımlarında görülür.

EXTC deneyi üretim ölçeğine ulaşmadı ancak sorduğu sorular, yani programlanabilir mutabakat, atomik transferler ve kendi kendini uygulayan ödeme kuralları hakkındaki sorular, 2018 için doğru sorulardı. Bunları yanıtlamak için gereken altyapının olgunlaşması beş yıl daha aldı.

## Sıkça Sorulan Sorular

**ERC-223 neydi ve EXTC neden ERC-20 yerine onu kullandı?**

Akıllı sözleşme adreslerine doğrudan gönderilen ERC-20 tokenları, sözleşmelerin gelen transferi algılamasının bir yolu olmadığı için sessizce kayboluyordu. ERC-223, alıcı sözleşmelerin bir `tokenFallback` fonksiyonu uygulamasını zorunlu kılarak bunu düzeltti; fonksiyon yoksa transfer, tokenları yakmak yerine geri alınıyordu. EXTC, zincir üzerindeki tüm transferleri atomik ve güvenli hâle getirmek için ERC-223'ü benimsedi.

**Erken ödeme tokenı projeleri neden muhabir bankacılığın yerini alacak ölçeğe ulaşamadı?**

2018'de Ethereum ana ağı saniyede yaklaşık 15 işlem gerçekleştiriyordu. Ticaret finansmanı veya kurumsal ödemeler hariç yalnızca küresel havale hacimleri bile saniyede on binlerce işlem gerektirirdi. Bu işlem kapasitesine ulaşmak için gereken Layer-2 ölçekleme altyapısı 2021-2023'e kadar üretime hazır değildi.

**EXTC'nin ardındaki fikirlere ne oldu?**

Temel kavramlar, yani programlanabilir ödeme kuralları, atomik mutabakat ve uyumun gömülü olduğu token mantığı, DeFi protokolleri, düzenlemeye tabi menkul kıymet token standartları (ERC-1400) ve merkez bankası dijital para birimi araştırmaları tarafından benimsendi. Ticari bankaların şimdi pilot uygulamasını yürüttüğü tokenlaştırılmış mevduat çerçeveleri, doğrudan EXTC gibi erken ödeme tokenı deneylerinin ilk sorduğu tasarım sorularına dayanır.

**2018 EXTC tasarımı, 2026 tokenlaştırılmış mevduat önerileriyle nasıl karşılaştırılır?**

Mutabakat modeli benzerdir: parasal alacakları temsil eden ve bir dağıtık defter üzerinde atomik olarak transfer edilen tokenlar. Temel farklar şunlardır: (1) 2026 tokenlaştırılmış mevduatları, hamiline tokenlar yerine ticari banka yükümlülükleridir; (2) kamuya açık ana ağ yerine düzenleyici gözetimin bulunduğu izinli veya hibrit defterlerde çalışırlar; (3) uyum ve kimlik doğrulama, katılımcılara bırakılmak yerine protokol katmanında uygulanır.

## Kaynaklar

- Ethereum Foundation, (2018). [EIP-20: Token Standardı ⧉](https://eips.ethereum.org/EIPS/eip-20 "EIP-20 Token Standardı").
- Dexaran, Ethereum GitHub, (2017). [ERC-223 Token Standardı Önerisi ⧉](https://github.com/ethereum/EIPs/issues/223 "ERC-223 tartışması").
- Dünya Bankası, (2018). [Remittance Prices Worldwide, 2018 İlk Çeyrek ⧉](https://www.worldbank.org/en/topic/migrationremittancesdiasporaissues/brief/migration-remittances-data "Dünya Bankası Havale Fiyatları").
- Buterin, V., (2014). [Ethereum: Yeni Nesil Bir Akıllı Sözleşme ve Merkeziyetsiz Uygulama Platformu ⧉](https://ethereum.org/whitepaper "Ethereum Teknik Belgesi").
