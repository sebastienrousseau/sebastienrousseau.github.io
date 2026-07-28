---
title: "Express Transaction Credits platformunun yapımı"
subtitle: "Express Transaction Credits platformunu ERC-223 akıllı sözleşmeleriyle tasarlamak"
description: "Express Transaction Credits platformunun (EXTC) 2018'de Ethereum ERC-223 üzerine nasıl inşa edildiğine dair teknik bir inceleme: token mimarisi, çok imzalı ödemeler, zaman kilitli transferler ve teminatlı anlık krediler."
date: "February 15, 2018"
language: "tr-TR"
locale: "tr_TR"
hreflang: "tr"
banner: "https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp"
banner_alt: "Devasa beyaz sütunlar"
keywords: "EXTC platformu, ERC-223, Ethereum akıllı sözleşmeleri, token mimarisi, çok imzalı, zaman kilitli transfer, blockchain ödemeleri, teminatlı krediler, merkeziyetsiz finans, 2018 kripto"
---


![Devasa beyaz sütunlar](https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp).class=\"img-fluid clearfix\"

> **Yönetici Özeti / Önemli Çıkarımlar**
>
> - **Temel sorun.** 2018'de Ethereum'un baskın token standardı olan ERC-20'nin yapısal bir kusuru vardı: bir akıllı sözleşme adresine doğrudan aktarılan token'lar, sözleşmede bir işleyici yoksa sessizce yok ediliyordu. ERC-20 üzerine kurulan her ödeme platformu bu riski devralıyordu ([Ethereum EIPs](https://eips.ethereum.org/EIPS/eip-20 "EIP-20: Token Standardı")).
> - **Çözüm olarak ERC-223.** ERC-223, alıcı sözleşmelerin bir `tokenFallback(address, uint, bytes)` işlevi uygulamasını zorunlu kılıyordu. Bu işlev yoksa aktarım atomik olarak geri alınıyordu. Hiçbir token sessizce kaybedilemezdi ([Ethereum EIPs GitHub](https://github.com/ethereum/EIPs/issues/223 "ERC-223 Token Standardı Önerisi")).
> - **EXTC'nin beş sözleşme temel bileşeni.** Token kimliği (ad, sembol, 18 ondalık hassasiyet), sabit arz, ERC-223 uyumlu aktarım, çok imzalı kurumsal ödeme ve blok yüksekliğine göre zaman kilitli düzenli ödeme talimatları.
> - **Teminatlı kredi mekanizması.** Borç alanlar EXTC token'larını bir sözleşme emanetine kilitliyordu; sözleşme, teminatın alınmasıyla birlikte kredi tutarını, teminat değerlendirme gecikmesi ya da kredi komitesi onayı olmadan atomik olarak serbest bırakıyordu.
> - **Deneyin Ethereum sınırları hakkında ortaya koyduğu.** ~15 TPS'lik ana ağ verimi ve Ocak 2018 zirvesinde işlem başına 0,10-1,00 dolarlık gaz maliyetleriyle, havale ölçeğinde bir hacmi işleyen bir ödeme ağı bile, Layer-2 altyapısı olmadan halka açık Ethereum üzerinde ekonomik ve teknik olarak uygulanabilir değildi.

---

## Tasarım Sorunu: ERC-20 Neden Yetersizdi

2015'te önerilen ve Ethereum Improvement Proposal 20 ile resmileştirilen ERC-20 standardı, 2017-2018 ICO patlamasına güç veren standart değiştirilebilir token arayüzünü tanımladı. Altı temel işlevi (`totalSupply`, `balanceOf`, `transfer`, `transferFrom`, `approve` ve `allowance`) basit token ihracı ve değişimi için yeterliydi.

Ancak bir ödeme platformu için ERC-20'nin üretim açısından kritik bir kusuru vardı. `transfer(address _to, uint256 _value)` işlevi, token'ları alıcı sözleşmede herhangi bir kod tetiklemeden, sözleşme adresleri de dâhil olmak üzere herhangi bir adrese aktarıyordu. Gelen ERC-20 aktarımlarını izlemek için özel olarak programlanmamış bir sözleşmenin bunları algılamasının hiçbir yolu yoktu. Bu şekilde gönderilen token'lar, kurtarma mekanizması olmadan kalıcı olarak hapsoluyordu.

Ethereum topluluğu, 2018'in ortalarına kadar bu mekanizma yoluyla onlarca milyon dolar değerinde ERC-20 token'ının kalıcı olarak kaybedildiğini tahmin ediyordu. Aktarımların sessizce başarısız olabildiği ve kullanıcı fonlarını yok edebildiği bir ödeme platformu inşa etmek kabul edilebilir değildi.

## ERC-223 Çözümü: Bildirimli Atomik Aktarım

Ethereum EIPs GitHub hata takip sisteminde önerilen ERC-223, bir token aktarımının yapması gerekenleri değiştirerek sessiz kayıp sorununu ele aldı. ERC-223 kapsamında `transfer(address _to, uint256 _value, bytes _data)`, alıcı adresin sözleşme kodu içerip içermediğini denetliyordu. İçeriyorsa aktarım `_to.tokenFallback(address _from, uint256 _value, bytes _data)` çağrısını yapıyordu.

Kritik özellik şuydu: alıcı sözleşme `tokenFallback` işlevini uygulamıyorsa, aktarım işleminin tamamı geri alınıyordu. Gönderenin bakiyesinden hiçbir token çıkmıyordu. Hiçbir token hapsolmuyordu. Aktarım atomikti: ya alıcının kodu çalışarak tamamlanıyor ya da durum hiç değişmeden tümüyle başarısız oluyordu.

EXTC için bu şu anlama geliyordu:

- **Akıllı sözleşmelere ödeme, tasarım gereği güvenliydi.** Emanet sözleşmeleri, çok imzalı cüzdanlar ve kredi sözleşmeleri, fonların geri döndürülemez biçimde kaybedilmesi riski olmadan EXTC token'ları alabiliyordu.
- **`_data` alanı zengin ödeme meta verilerini mümkün kıldı.** Bayt yükü, basit bir ERC-20 aktarımının iletemeyeceği bilgileri, yani fatura referanslarını, yönlendirme kodlarını veya uyum beyanlarını taşıyabiliyordu.
- **Gaz maliyetleri az da olsa daha yüksekti.** `tokenFallback` çağrısı, aktarım başına yaklaşık 2.000-5.000 gaz ekliyordu; 2018 gaz fiyatlarında küçük bir ek yük.

## EXTC Sözleşme Mimarisi

EXTC token sözleşmesi, beş modül etrafında yapılandırılmış bir Solidity uygulamasıydı:

### 1. Token Kimliği

```
string public name = "Express Transaction Credits";
string public symbol = "EXTC";
uint8 public decimals = 18;
```

On sekiz ondalık basamak, EXTC'ye cent altı hassasiyet kazandırarak mikro ödeme ve mikro kredi kullanım senaryolarının gerektirdiği ayrıntı düzeyiyle eşleşiyordu. `EXTC` sembolü, token sözleşmesine kaydedilen zincir üstü tanımlayıcıydı.

### 2. Sabit Toplam Arz

Toplam arz sözleşme dağıtımı sırasında belirleniyor ve sonraki basımlarla şişirilemiyordu. Bu tasarım tercihi EXTC'yi deflasyonist kılıyordu: geri döndürülemez yakma işlemleriyle dolaşımdan kalıcı olarak çıkarılan token'lar, yerine yenisi konmadan arzı azaltıyordu. Sabit arz modeli, 2018 ödeme token'ı tasarımlarında standarttı ve deflasyonist baskının bir değişim aracı için bir özellik olduğu yönündeki Bitcoin etkili varsayımı yansıtıyordu.

### 3. ERC-223 Uyumlu Bakiye ve Aktarım

Temel aktarım işlevi, ERC-223 arayüzünün tamamını uyguluyordu. Dâhili bakiye eşlemeleri, her adresin varlıklarını izliyordu. `isContract(address)` yardımcı işlevi, `tokenFallback` çağrısının gerekip gerekmediğini belirlemek için EOA (harici sahipli hesap) adreslerini sözleşme adreslerinden ayırıyordu.

### 4. Çok İmzalı Kurumsal Ödemeler

Kurumsal ödeme iş akışları ortak yetkilendirme gerektiriyordu: hiçbir tek imza sahibi, tanımlı bir eşiğin üzerindeki bir ödemeyi tek taraflı olarak başlatamıyordu. EXTC sözleşmesi, N'de iki imza gerektiren bir çok imza şeması uyguluyordu:

1. Belirlenmiş bir başlatıcı, alıcıyı, tutarı ve bir nonce değerini belirterek bir aktarım öneriyordu.
2. Bir ortak imza sahibi nonce değerini onaylıyordu.
3. Aktarım yalnızca her iki imza da zincir üstüne kaydedildikten sonra gerçekleşiyordu.

Bu, kurumsal hesaplar için tek nokta arıza riskini ortadan kaldırırken, tüm yetkilendirme akışını bir takas kurumu aracısı olmadan zincir üstünde ve denetlenebilir tutuyordu.

### 5. Blok Yüksekliğine Göre Zaman Kilitli Düzenli Ödeme Talimatları

Yinelenen ödemeler (maaşlar, abonelikler, planlanmış kredi geri ödemeleri) bir düzenli ödeme talimatı bileşeni gerektiriyordu. EXTC bunu bir zaman kilidi olarak uyguladı: bir aktarım kaydı, sözleşmede bir `releaseBlock` parametresiyle saklanıyordu. Aktarım, Ethereum blok yüksekliği `releaseBlock` değerine ulaşana kadar gerçekleşemiyordu.

Zaman göstergesi olarak blok yüksekliği, 2018'de pragmatik bir tercihti. Ethereum 15 saniyelik bir blok aralığını hedefliyordu; bu da blok yüksekliğini dakikalar mertebesinde gerçek zamana makul ölçüde güvenilir bir gösterge kılıyordu. Mutlak zaman damgaları (`block.timestamp`) mevcuttu ancak ±900 saniyelik bir pencere içinde madenci manipülasyonuna açıktı; bu nedenle blok yüksekliği finansal sözleşmeler için daha güvenli referanstı.

## Teminatlı Anlık Kredi Mekanizması

EXTC kredi bileşeni en karmaşık bileşendi. Tasarım şöyleydi:

1. **Borç alan teminatı kilitler.** Borç alan `lockCollateral(uint256 _collateralAmount)` çağrısını yaparak, bir ERC-223 `tokenFallback` aracılığıyla EXTC token'larını kredi sözleşmesi emanetine aktarıyordu.
2. **Kredi-değer oranı denetimi.** Sözleşme, önceden yapılandırılmış bir LTV oranını (örneğin %50) okuyor ve kilitlenen teminata karşılık azami kredi tutarını hesaplıyordu.
3. **Atomik kredi ödemesi.** Teminat asgari eşiği karşılıyorsa, sözleşme kredi tutarını borç alanın adresine anında aktarıyordu. Teminat değerlendirme kuyruğu, kredi komitesi ya da mutabakat gecikmesi yoktu.
4. **Geri ödeme ve serbest bırakma.** Geri ödemede (anapara artı sabit bir faiz oranı) sözleşme teminatı borç alana geri veriyordu. `releaseBlock` değerine kadar geri ödemenin yapılmaması otomatik tasfiyeyi tetikliyordu: sözleşme teminatı borç verenin belirlediği adrese aktarıyordu.

Akışın tamamı sözleşme koduyla uygulanıyordu. İki taraftan hiçbirinin diğerine güvenmesi ya da şartların uygulanması için bir aracıya dayanması gerekmiyordu.

## Deneyin Ortaya Koyduğu

EXTC sözleşme mimarisi teknik olarak tutarlıydı. ERC-223, ERC-20'nin en ciddi güvenlik kusurunu çözdü. Çok imza ve zaman kilidi bileşenleri, gerçek kurumsal ödeme iş akışlarıyla doğrudan eşleşiyordu. Teminatlı kredi mekanizması, teminatlı kredilendirmenin tam otomatik ve zincir üstünde kendi kendini uygulayan bir yapıya kavuşturulabileceğini gösterdi.

Uygulamada iki kısıt ortaya çıktı:

**Gaz maliyetleri.** Ocak 2018 zirvesinde Ethereum gaz fiyatları 50-100 gwei'ye ulaştı ve tek bir ERC-223 token aktarımının maliyetini 0,50-2,00 dolara çıkardı. 10-50 dolarlık mikro ödemeler ya da havaleler için bu ücretler aşırı yüksekti.

**Verim.** 2018 başında Ethereum ana ağının blok gaz limiti yaklaşık 8 milyon gazdı. Bir ERC-223 aktarımı kabaca 50.000-80.000 gaz tüketiyordu. Dolayısıyla ağ, blok başına yaklaşık 100-160 EXTC token aktarımı, yani 15 saniyelik blok aralığında saniyede kabaca 7-11 aktarım işleyebiliyordu. Ödeme ağı ölçeği, yani saniyede yüzlerce veya binlerce işlem, o dönemde henüz üretim biçiminde var olmayan Layer-2 altyapısı olmadan halka açık Ethereum üzerinde ulaşılabilir değildi.

Bunlar EXTC'deki tasarım kusurları değil, altyapı kısıtlarıydı. Sözleşme mantığı doğruydu. Altta yatan blok zinciri, finans sektörü ölçeğinde ödeme hacmini henüz destekleyemiyordu.

## Üretime Ulaşan Fikirler

EXTC'den birkaç tasarım deseni, sonraki geliştirmelerle doğrulandı:

**Alıcı bildirimli atomik token aktarımı**, yani temel ERC-223 özelliği, bildirim modelini genişleten ve daha sonra DeFi kredi protokollerine dâhil edilen ERC-777'nin (2019) temeli oldu. `tokenFallback` deseni modern DeFi mimarisinin her yerinde görülür.

**Kurumsal ödemeler için çok imzalı yetkilendirme**, yani yürütmeden önce zincir üstünde birden çok imza gerektirme deseni, DAO hazine yönetimi ve kurumsal saklama çözümleri için standart model hâline geldi. 2018'de piyasaya çıkan Gnosis Safe, bu deseni büyük ölçekte yaygınlaştırdı.

**Aracısız teminatlı anlık krediler**, yani teminatı emanete kilitleme ve kredi tutarını atomik olarak serbest bırakma mekanizması, Compound (2018) ve Aave (2020) gibi DeFi kredi protokollerinin temel tasarımıdır.

**Planlanmış ödemeler için blok yüksekliği zaman kilitleri**, yani gelecekteki yürütme zamanlamasını sözleşmeye kodlama deseni, DeFi ekosistemi genelinde token hakediş sözleşmelerinde, gecikmeli yönetişim önerilerinde ve zaman ağırlıklı ortalama fiyat (TWAP) oracle tasarımlarında görülür.

EXTC deneyi üretim ölçeğine ulaşmadı. Tasarımı uygulanabilir kılmak için gereken altyapının olgunlaşması üç ila beş yıl daha aldı. Sorduğu tasarım soruları, 2018 için doğru sorulardı.

## Sıkça Sorulan Sorular

**ERC-223, ERC-20'nin kusurunu gidermesine rağmen neden hiçbir zaman baskın token standardı olarak benimsenmedi?**

ERC-223, alıcı sözleşmelerin `tokenFallback` uygulamasını zorunlu kılıyor ve ERC-20 token'ları için hâlihazırda dağıtılmış binlerce sözleşmeyle geriye dönük uyumluluğu bozuyordu. Mevcut ERC-20 ekosistemi taşınamayacak kadar büyüktü. Sonraki öneriler, özellikle ERC-777 ve ERC-1363, aynı sorunu farklı uyumluluk ödünleşimleriyle ele aldı; ancak ERC-20, ağ etkileri ile sessiz kayıp senaryosunu önleyen sarmalanmış token desenlerinin devreye girmesinin birleşimiyle baskın kalmayı sürdürdü.

**EXTC token'ına ve platformuna ne oldu?**

EXTC, 2018'den bir kavram kanıtı ve erken dönem araştırma projesiydi. Ethereum'un ölçeklenebilirlik sınırları ve düzenleyici belirsizlik netleştikçe, daha geniş ICO ve ödeme token'ı piyasası 2018-2019 boyunca keskin biçimde daraldı. EXTC tasarımına gömülü fikirler, Layer-2 altyapısına, daha iyi araçlara ve daha net düzenleyici çerçevelere erişimi olan sonraki protokollerde yeniden ortaya çıktı.

**EXTC'nin teminatlı kredi modeli, Aave gibi modern DeFi protokolleriyle nasıl karşılaştırılır?**

Temel mekanizma aynıdır: teminat kilitle, bir LTV oranına göre boyutlandırılmış bir kredi al, geri öde ya da tasfiyeyle karşılaş. Farklar şunlardır: (1) modern DeFi protokolleri sabit oranlar yerine dinamik LTV için oracle fiyat akışları kullanır; (2) havuz kullanımına yanıt veren algoritmik faiz oranları kullanır; (3) 2018 ana ağından 10-100 kat daha düşük gaz maliyetleriyle Layer-2 ağları üzerinde çalışır; (4) Aave ve Compound resmi güvenlik denetimlerinden geçmiş ve milyarlarca dolarlık likidite tutmuştur; bu da temel modelin sağlam olduğuna dair ampirik doğrulama sağlar.

**2018 başında Solidity sürüm kısıtları nelerdi?**

EXTC sözleşmesi, 2018 başında baskın sürüm olan Solidity 0.4.x için yazıldı. Solidity 0.4, sonraki sürümlerde getirilen birçok güvenlik özelliğinden yoksundu: tam sayı taşması denetimi (0.8.0'da otomatik olarak eklendi), hata mesajlı `require`/`revert` (0.4'te sınırlıydı) ve açık işlev görünürlüğü (0.4'te varsayılan public'ti). Sözleşme, taşmaya karşı korunmak için OpenZeppelin'in SafeMath kütüphanesine dayanıyordu; bu, derleyici bunu yerel olarak zorunlu kılmadan önce yaygın bir desendi.

## Kaynakça

- Ethereum Foundation, (2015). [EIP-20: Token Standardı ⧉](https://eips.ethereum.org/EIPS/eip-20 "EIP-20 Token Standardı").
- Dexaran, Ethereum GitHub, (2017). [ERC-223 Token Standardı Önerisi ⧉](https://github.com/ethereum/EIPs/issues/223 "ERC-223 tartışması").
- OpenZeppelin, (2018). [OpenZeppelin Contracts: SafeMath ⧉](https://github.com/OpenZeppelin/openzeppelin-contracts "OpenZeppelin Contracts").
- Ethereum Foundation, (2014). [Ethereum Teknik İncelemesi ⧉](https://ethereum.org/whitepaper "Ethereum Teknik İncelemesi").
