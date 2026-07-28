---
title: "Blockchain'in arkasındaki teknolojiyi anlamak"
subtitle: "Blockchain'in arkasındaki kriptografi ve uzlaşmaya yönelik pratik bir inceleme"
description: "Blockchain'in nasıl çalıştığına teknik bir giriş: kriptografik hash zincirleri, Merkle ağaçları, dağıtık uzlaşma ve Ethereum'un programlanabilir katmanının bir ödeme defterini akıllı sözleşmeler ve tokenleştirilmiş varlıklar için bir platforma nasıl dönüştürdüğü."
date: "January 9, 2018"
language: "tr-TR"
locale: "tr_TR"
banner: "https://cloudcdn.pro/stocks/images/adam-smigielski-K5mPtONmpHM.webp"
banner_alt: "Karanlık arka planda ışık izleriyle birbirine bağlanan soyut dijital defter blokları"
keywords: "blockchain teknolojisi, kriptografik hash, Merkle ağacı, dağıtık uzlaşma, proof of work, Ethereum, akıllı sözleşmeler, EVM, Solidity, ERC-20, dağıtık defter, merkeziyetsiz finans"
---


![Karanlık arka planda ışık izleriyle birbirine bağlanan soyut dijital defter blokları](https://cloudcdn.pro/stocks/images/adam-smigielski-K5mPtONmpHM.webp).class=\"img-fluid clearfix\"

> **Yönetici Özeti / Önemli Çıkarımlar**
>
> - **Sorun.** Dijital nakit, çifte harcama sorununu çözmeyi gerektirir: güvenilir bir takas kurumu olmadan aynı birimin iki kez harcanmasını önlemek. Bitcoin'in 2008 tarihli teknik raporu bu sorunu, güvenilen aracıları kriptografik kanıt ve dağıtık uzlaşma ile değiştirerek çözdü ([Nakamoto, 2008](https://bitcoin.org/bitcoin.pdf "Bitcoin: Eşten Eşe Elektronik Nakit Sistemi")).
> - **Veri yapısı.** Bir blockchain, her blok başlığının bir önceki başlığın SHA-256 hash'ini içerdiği, bloklardan oluşan bağlı bir listedir. Hash zinciri geçmişi yalnızca-ekleme (append-only) biçimine sokar: geçmişteki herhangi bir bloğun değiştirilmesi sonraki her hash'i geçersiz kılar ve saldırganı sonraki tüm proof-of-work'ü yeniden yapmaya zorlar.
> - **Merkle ağaçları.** Bir blok içindeki işlemler ikili bir Merkle ağacına hash'lenir. Blok başlığında saklanan kök hash, tüm bloğu indirmeden herhangi bir tekil işlemin verimli biçimde doğrulanmasına olanak tanır; hafif SPV istemcilerinin temeli budur.
> - **Ethereum'un uzantısı.** Ethereum'un Yellow Paper (2014) belgesi EVM'yi tanıttı: her tam düğümde çalışan deterministik bir yığın makinesi. Akıllı sözleşmeler, zincire dağıtılan bytecode'dur; tüm düğümlerde aynı şekilde çalışır ve atomik olarak sonuçlanır, güvenilen aracıların yerini kendi kendini uygulayan kodla alır ([Wood, 2014](https://ethereum.github.io/yellowpaper/paper.pdf "Ethereum Yellow Paper")).
> - **Pratik önem.** 2017'den bu yana dağıtılan her tokenleştirilmiş varlık, stablecoin ve DeFi protokolü bu temeller üzerinde çalışır. Hash zincirini, Merkle ağacını ve EVM yürütme modelini anlamak, Ethereum tabanlı herhangi bir sistemle çalışmanın ön koşuludur.

---

## Blockchain'in Çözdüğü Sorun

Bitcoin'den önce, dijital ödemeler çifte harcamayı önlemek için güvenilir bir aracı gerektiriyordu: bir banka, ödeme işlemcisi veya takas kurumu. Alice, 10 £ temsil eden dijital bir dosyayı Bob'a gönderdiğinde, dosyanın kendisinde onun aynı kopyayı Carol'a göndermesini engelleyen hiçbir şey yoktu. Mevcut her sistemdeki çözüm merkezî kayıt tutmaydı: bankanın defteri paranın harcandığını söylüyordu, dolayısıyla para tekrar harcanamıyordu.

Bitcoin'in katkısı, o güvenilir defteri, tüm işlemlerin kaydının binlerce bağımsız düğüm arasında çoğaltıldığı dağıtık bir defterle değiştirmekti. Düğümler arasındaki karşılıklı güvensizlik, iki mekanizma aracılığıyla güvenliğe dönüştürüldü:

1. **Kriptografik bağlama.** Her işlem bloğu, bir önceki bloğun hash'ini içerir. Hash fonksiyonu tek yönlü, deterministik bir eşlemedir: herhangi bir girdi verildiğinde fonksiyon sabit uzunlukta bir çıktı üretir ve girdinin tek bir bitinin bile değiştirilmesi tamamen farklı bir çıktı üretir. Bu, geçmişteki bir bloğa yapılan herhangi bir değişikliğin ondan sonraki her bloğu geçersiz kılması anlamına gelir.

2. **Proof-of-work uzlaşması.** Yeni bir blok eklemek, bloğun hash'inin bir hedef eşiğin altına düşmesini sağlayan bir nonce değeri bulmayı gerektirir; bulunması hesaplama açısından pahalı, doğrulanması ise önemsiz derecede ucuzdur. Bu, geçmişi yeniden yazmayı, değiştirilen bloğun derinliğiyle orantılı olarak pahalı hale getirir, çünkü bir saldırganın o bloktan zincirin ucuna kadar tüm proof-of-work'ü yeniden yapması gerekir.

Bu birleşim, en fazla kümülatif proof-of-work'e sahip en uzun zincirin, yapısı gereği, gerçek kaynaklar harcayan dürüst katılımcılar tarafından sürdürülen zincir olduğu anlamına gelir.

## Kriptografik Yapı Taşları

Blockchain teknolojisi, önceden var olan üç kriptografik ilkeyi yeni bir mimaride birleştirir:

### SHA-256 Hash Fonksiyonları

SHA-256 (256-bit Güvenli Hash Algoritması), NIST tarafından standartlaştırılan SHA-2 ailesinin bir üyesidir. Rastgele uzunlukta bir girdi alır ve 256-bit'lik bir çıktı üretir. Blockchain kullanımı için temel özellikler:

- **Deterministik.** Aynı girdi her zaman aynı çıktıyı üretir.
- **Ön görüntü direnci (pre-image resistance).** Bir hash çıktısı verildiğinde, girdiyi yeniden oluşturmak hesaplama açısından olanaksızdır.
- **Çığ etkisi (avalanche effect).** Girdinin bir bitinin değiştirilmesi çıktı bitlerinin kabaca yarısını değiştirir ve kaba kuvvet aramasını verimsiz kılar.
- **Çakışma direnci (collision resistance).** Aynı hash'i üreten iki farklı girdi bulmak hesaplama açısından olanaksızdır.

Bitcoin, uzunluk uzatma (length-extension) saldırılarına karşı ek güvenlik için SHA-256'yı iki kez uygular (SHA-256d). Ethereum, bir SHA-3 finalisti varyantı olan Keccak-256'yı kullanır.

### Merkle Ağaçları

Merkle ağacı, hash'lerden oluşan ikili bir ağaçtır. Her yaprak düğüm bir işlemin hash'idir. Her iç düğüm, iki alt düğümünün hash'idir. Kök, yani Merkle kökü, bloktaki tüm işlemleri blok başlığında saklanan tek bir 32 baytlık değerde özetler.

Pratik sonuç: belirli bir işlemin bir bloğa dahil edildiğini doğrulamak için tüm `n` işleme değil, yalnızca `log₂(n)` hash'e ihtiyaç duyarsınız. 2.000 işlemli bir blok için doğrulama, 2.000 yerine 11 hash gerektirir; hafif istemcilerdeki Basitleştirilmiş Ödeme Doğrulaması'nın (SPV) temeli budur.

### Dijital İmzalar (ECDSA)

Bitcoin ve Ethereum'da işlem yetkilendirmesi, secp256k1 eğrisi üzerinde Eliptik Eğri Dijital İmza Algoritması'nı (ECDSA) kullanır. Bir özel anahtar bir işlemi imzalar; herhangi bir düğüm, özel anahtarı bilmeden ilgili açık anahtarı kullanarak imzayı doğrulayabilir. Bu, bir adresten yapılacak harcamayı yalnızca özel anahtarın sahibinin yetkilendirebilmesini sağlar.

Ethereum adresleri, açık anahtarın Keccak-256 hash'inin son 20 baytıdır; bu türetme, adresleri anahtar çiftine kriptografik olarak bağlı kalırken kompakt ve taşınabilir kılar.

## Bitcoin Blockchain'i Nasıl Çalışır

Bir Bitcoin bloğu üç mantıksal bileşen içerir:

**Blok başlığı:** protokol sürümü, bir önceki blok başlığının hash'i, işlemlerin Merkle kökü, bir Unix zaman damgası, güncel zorluk hedefi ve nonce'den oluşan 80 bayt. Madenciler, başlığın çift SHA-256 hash'i zorluk hedefinin altına düşene kadar nonce'yi (ve bazen coinbase işlemindeki zaman damgasını veya extra-nonce'yi) yineler.

**İşlem listesi:** bloğa dahil edilen işlemlerin sıralı kümesi. Coinbase işlemi (ilki), blok ödülünü ve işlem ücretlerini madencinin adresine atar.

**Zincir:** başlıkların birbirine bağlanması. Zincirdeki kümülatif proof-of-work (her bloğu üretmek için yapılan tüm işin toplamı), hangi çatalın kanonik zincir olduğunu belirler. Düğümler her zaman en fazla kümülatif işe sahip zinciri izler.

Bitcoin için blok süresi 10 dakika olacak şekilde hedeflenir. Zorluk, toplam ağ hash oranı değiştikçe bu hedefi korumak için her 2.016 blokta bir (yaklaşık iki haftada bir) ayarlanır.

## Ethereum'un Programlanabilir Katmanı

Ethereum, Bitcoin'in işlem modelini "değer aktar"dan "kod çalıştır"a genelleştirdi. Temel eklemeler:

**Ethereum Sanal Makinesi (EVM):** tüm tam düğümlerde deterministik olarak çalışan, 256-bit kelimeli, yığın tabanlı bir sanal makine. Her opcode'un açık bir gas maliyeti vardır. Hesaplama, sonsuz döngülerin ağı durdurmasını önleyecek şekilde blok gas limitiyle sınırlandırılır. Aynı durum üzerinde aynı bytecode'u çalıştıran tüm düğümler aynı çıktıyı üretmelidir; yürütme üzerindeki bu uzlaşma, akıllı sözleşmeleri güvene ihtiyaç duymayan (trustless) hale getiren şeydir.

**Hesaplar.** Ethereum'un iki hesap türü vardır: özel anahtarlarla kontrol edilen Harici Sahipli Hesaplar (EOA) ve kodu zincir üzerinde saklanan Sözleşme Hesapları. Bir sözleşme adresine gönderilen bir işlem, sözleşmenin bytecode yürütmesini tetikler.

**Durum (State).** Ethereum'un küresel durumu, adreslerin hesap durumlarına (nonce, bakiye, depolama, kod hash'i) eşlenmesidir. Durum kökü, yani tüm hesap durumlarının bir Merkle Patricia trie'si, her blok başlığına dahil edilir ve herhangi bir hesabın herhangi bir blok yüksekliğindeki durumunun verimli biçimde kanıtlanmasına olanak tanır.

**Gas.** Kullanıcılar her EVM işlemi için gas (ETH cinsinden) öder. Gas iki işlev görür: madencileri/doğrulayıcıları hesaplama karşılığında ödüllendirir ve herhangi bir tek işlemin tüketebileceği kaynakları sınırlayarak pahalı işlemler yoluyla hizmet reddi (denial-of-service) saldırılarını önler.

## Solidity ile Akıllı Sözleşme Yazmak

Solidity, EVM bytecode'una derlenen, statik olarak tiplenmiş, sözleşme odaklı bir dildir. Minimal bir token sözleşmesi temel kavramları gösterir:

```solidity
pragma solidity ^0.8.0;

contract MyToken {
    string public name;
    string public symbol;
    uint8 public decimals;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;

    event Transfer(address indexed from, address indexed to, uint256 value);

    constructor(
        string memory _name,
        string memory _symbol,
        uint8 _decimals,
        uint256 _totalSupply
    ) {
        name = _name;
        symbol = _symbol;
        decimals = _decimals;
        totalSupply = _totalSupply;
        balanceOf[msg.sender] = _totalSupply;
    }

    function transfer(address _to, uint256 _value) external returns (bool) {
        require(balanceOf[msg.sender] >= _value, "Insufficient balance");
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }
}
```

Temel gözlemler: `mapping(address => uint256)`, bellek içi bir veri yapısı değil, bir EVM depolama düzenidir; okuma ve yazma işlemleri gas harcar. `require`, başarısızlık durumunda tüm işlemi geri alır ve kullanılmayan gas'i iade eder. `event Transfer`, zincir dışı indeksleyicilerin tüm durumu yeniden okumadan transferleri izlemek için kullandığı bir günlük yayar. `constructor` dağıtım sırasında bir kez çalışır; sonraki çağrılar adlandırılmış fonksiyonlara gider.

ERC-20 standardı, değiştirilebilir (fungible) tokenler için ortak bir arayüzü resmileştirdi: `transfer`, `transferFrom`, `approve`, `allowance`, `balanceOf`, `totalSupply`. Bu sayede ERC-20 uyumlu herhangi bir token, özel entegrasyon olmadan ERC-20 farkında herhangi bir borsa veya cüzdanla çalışabilir.

## Defterden Finansal Altyapıya

Burada açıklanan blockchain ilkeleri (hash zincirleri, Merkle ağaçları, EVM ve ERC-20), 2018 ile 2026 arasında daha geniş bir finansal uygulama kümesinin temeli haline geldi:

**Merkeziyetsiz Finans (DeFi).** Borç verme protokolleri (Compound, Aave), otomatik piyasa yapıcılar (Uniswap) ve getiri toplayıcılar (yield aggregator) tümü EVM akıllı sözleşmeleri olarak çalışır. Geleneksel finansal aracıların takas, saklama ve mutabakat işlevlerinin yerini kendi kendini yürüten kod ve zincir üzerindeki likidite havuzlarıyla alırlar.

**Tokenleştirilmiş Varlıklar.** Merkez bankaları ve ticari bankalar, EVM uyumlu zincirlerin izinli varyantları üzerinde tokenleştirilmiş mevduatları, tokenleştirilmiş tahvilleri ve tokenleştirilmiş para piyasası fonlarını pilot olarak deniyor. Altta yatan mekanikler (hash ile güvence altına alınmış durum geçişleri, atomik mutabakat, programlanabilir transfer kuralları) 2014 Ethereum mimarisinin doğrudan mirasçılarıdır.

**Merkez Bankası Dijital Paraları.** İngiltere Merkez Bankası'nın toptan CBDC araştırması, ECB'nin dijital euro programı ve Project Agorá'nın tümü, Bitcoin ve Ethereum'daki temel tasarımlardan türetilen veya bunlarla uyumlu DLT mimarilerini araştırıyor. Uzlaşma ve hash zinciri yapıları, izinlendirme ve yönetişim modeli kamuya açık blockchain'lerden tamamen farklı olduğunda bile geçerliliğini korur.

2008 Bitcoin teknik raporundan 2026 tokenleştirilmiş finansına uzanan yolculuk yirmi yılı kapsar, ancak tutarlı bir teknik soy hattı üzerinde ilerler. Bir SHA-256 hash zincirinin değişmezliği nasıl uyguladığını, bir Merkle ağacının verimli doğrulamayı nasıl mümkün kıldığını ve EVM'nin akıllı sözleşmeleri atomik olarak nasıl yürüttüğünü anlamak, düzenlemeye tabi finansal hizmetlerde blockchain'in ne yapıp ne yapamayacağına dair her iddiayı değerlendirmenin ön koşuludur.

## Sıkça Sorulan Sorular

**Bir blockchain ile dağıtık veritabanı arasındaki fark nedir?**

Geleneksel bir dağıtık veritabanı, erişilebilirlik ve performans için verileri düğümler arasında çoğaltır, ancak güven merkezîdir: bir yönetici kayıtları değiştirebilir. Bir blockchain, hash zincirleme ve uzlaşma yoluyla kurcalamayı hesaplama açısından pahalı hale getirir: geçmişteki herhangi bir kaydı değiştirmek, sonraki tüm proof-of-work veya proof-of-stake'i yeniden yapmayı ve ağı değiştirilmiş çatalı kabul etmeye ikna etmeyi gerektirir. Ayırt edici özellik, erişim denetimleriyle değil, kriptografi ve teşvik tasarımıyla uygulanan kurcalama kanıtıdır (tamper-evidence).

**Ethereum neden SHA-256 yerine Keccak-256 kullanır?**

Ethereum, Keccak-256'yı (NIST standartlaştırma düzenlemelerinden önceki SHA-3 finalisti) kısmen, tasarımcıları Bitcoin'in halihazırda bağımlı olduğu SHA-2 soyundan bağımsızlık istediği için benimsedi. Keccak ayrıca belirli EVM işlemleri için onu çekici kılan farklı cebirsel özelliklere sahiptir. Geliştiriciler için pratik etki, Ethereum adres türetme ve depolama yuvası hash'lemesinin, Bitcoin'deki gibi SHA-256d değil, Keccak-256 kullanmasıdır.

**EVM'de "gas" neyi önler?**

Gas iki tür saldırıyı önler. İlk olarak, hesaplama açısından pahalı işlemler yoluyla hizmet reddini önler: her opcode gas'e mal olur, dolayısıyla bir saldırgan ağı bedelsiz olarak sonsuz döngüler çalıştırmaya zorlayamaz. İkinci olarak, blok gas limiti blok başına toplam hesaplamayı sınırlayarak blok doğrulama süresinin tam düğümler için sınırlı ve öngörülebilir kalmasını sağlar. Gas olmasaydı, tek bir sözleşme çağrısı sınırsız hesaplama yürüterek ağı durdurabilirdi.

**Proof-of-stake, proof-of-work ile karşılaştırıldığında güvenlik modelini nasıl değiştirir?**

Proof-of-work'te güvenlik enerji harcamasıyla sağlanır: zincire saldırmak, ağın hash oranının %50'sinden fazlasını kontrol etmeyi, yani onun fiziksel donanım ve gücünün %50'sinden fazlasını kontrol etmeyi gerektirir. Proof-of-stake'te (2022'deki Merge'den bu yana Ethereum tarafından kullanılıyor) güvenlik ekonomik teminatla sağlanır: doğrulayıcılar teminat olarak ETH kilitler ve çelişkili blokları imzalarlarsa bu teminat kesilir (slashing). %51 saldırısı, kilitlenmiş tüm ETH'nin %50'sinden fazlasını edinmeyi ve riske atmayı gerektirir; bu, donanım ve enerji maliyeti değil, bir sermaye maliyetidir. Güvenlik modeli farklıdır, ancak rasyonel doğrulayıcıların sermaye imhasına ücret gelirini tercih ettiği varsayımı altında ekonomik açıdan matematiksel olarak karşılaştırılabilir.

## Kaynaklar

- Nakamoto, S., (2008). [Bitcoin: Eşten Eşe Elektronik Nakit Sistemi ⧉](https://bitcoin.org/bitcoin.pdf "Bitcoin Teknik Raporu").
- Buterin, V., (2014). [Ethereum: Yeni Nesil Bir Akıllı Sözleşme ve Merkeziyetsiz Uygulama Platformu ⧉](https://ethereum.org/whitepaper "Ethereum Teknik Raporu").
- Wood, G., (2014). [Ethereum: Güvenli, Merkeziyetsiz, Genelleştirilmiş Bir İşlem Defteri ⧉](https://ethereum.github.io/yellowpaper/paper.pdf "Ethereum Yellow Paper").
- NIST, (2015). [SHA-3 Standardı: Permütasyon Tabanlı Hash ve Genişletilebilir Çıktı Fonksiyonları ⧉](https://www.nist.gov/publications/sha-3-standard-permutation-based-hash-and-extendable-output-functions "NIST FIPS 202").
