---
title: "ERC-20 token standardı"
subtitle: "Ethereum ekosisteminin ortak token arayüzü"
description: "ERC-20, Ethereum ağındaki değiştirilebilir token'lar için referans standarttır. ICO'ları ve DeFi'yi mümkün kılan teknik temelleri inceliyoruz."
date: "January 24, 2018"
language: "tr-TR"
locale: "tr_TR"
banner: "https://cloudcdn.pro/stocks/images/m-ZzOa5G8hSPI.webp"
banner_alt: "Ethereum ve token sembollerinin görselleştirmesi"
keywords: "ERC-20, Ethereum, token, akıllı sözleşmeler, ICO, DeFi, Solidity"
---


![Ethereum ve token sembollerinin görselleştirmesi](https://cloudcdn.pro/stocks/images/m-ZzOa5G8hSPI.webp).class=\"img-fluid clearfix\"

---

> **TL;DR.** ERC-20, Ethereum blok zincirinde en yaygın kullanılan token türüdür ve genellikle akıllı sözleşme tabanlı bir dijital sözleşme olarak anılır.
>
> **Önemli Çıkarımlar**
>
> - **Fikir.** ERC-20 standardı, ERC-20 uyumlu tüm token'ların uygulaması gereken altı temel işlevden oluşan bir küme tanımlar.
> - **Etki.** ERC-20 standardı Ethereum ekosistemi üzerinde önemli bir etki bırakmıştır.
> - **Teşvik.** ERC-20 protokolünün getirdiği standartlaşmanın doğrudan ekonomik bir etkisi de olmuştur.
> - **Standartlaştırılmış bir token arayüzüne duyulan ihtiyaç.** ERC-20 (Ethereum Request for Comments 20) standardı ortaya çıkmadan önce, Ethereum blok zinciri token mimarileri açısından bir Vahşi Batı'yı andırıyordu.

---

## Bakış

### Standartlaştırılmış bir token arayüzüne duyulan ihtiyaç

ERC-20 (Ethereum Request for Comments 20) standardı ortaya çıkmadan önce, Ethereum blok zinciri token mimarileri açısından bir Vahşi Batı'yı andırıyordu. Yeni oluşturulan her token'ın kendine özgü kuralları, işlevleri ve arayüzleri vardı. Bu durum geliştiricilere hem zorlu bir öğrenme eğrisi dayatıyor hem de token'ların birlikte çalışabilirliğini engelliyordu. Özünde her yeni token, öğrenilmesi, anlaşılması ve uygulanması gereken yeni bir dil gibiydi. Bu parçalı yapı, Ethereum platformunda token'ların ölçeklenebilirliğini ve geniş çapta benimsenmesini yavaşlatıyordu.

ERC-20 standardının getirilmesi, birleştirici bir dil işlevi gördü ve tüm Ethereum token'larının uyması gereken ortak bir kural ve işlev kümesi ortaya koydu. Artık geliştiriciler, söz konusu token ne olursa olsun tutarlı bir arayüzle çalışabiliyor. Bu standartlaşma, token etkileşim süreçlerini sadeleştirerek çeşitli uygulama ve hizmetlere daha sorunsuz entegrasyonu mümkün kıldı. Sonuç olarak geliştiriciler token'larla daha anlamlı biçimde etkileşime girebiliyor; bu da Ethereum ekosisteminde yeniliği ve büyümeyi destekleyen bir ortam yaratıyor.

#### Token mimarilerinin Vahşi Batısı

Ethereum blok zinciri başlangıçta tek bir token türünü, ETH'yi desteklemek üzere tasarlanmıştı. Ancak platform popülerlik kazandıkça geliştiriciler, çeşitli varlıkları ve kavramları temsil etmek için kendi token'larını oluşturmaya başladı. Bu durum, her biri kendine özgü kural ve işlev kümesine sahip farklı token mimarilerinin çoğalmasına yol açtı.

Bu parçalı yapı, geliştiricilerin birden fazla token'la etkileşime girebilen uygulamalar geliştirmesini zorlaştırdı. Ayrıca kullanıcıların token varlıklarını farklı platformlar arasında yönetmesini de güçleştirdi.

#### ERC-20 standardı

ERC-20 standardı, token mimarilerinin Vahşi Batısının doğurduğu sorunları gidermek için 2015 yılında tanıtıldı. Standart, tüm Ethereum token'larının uyması gereken ortak bir kural ve işlev kümesi tanımlar. Bu standartlaşma, geliştiricilerin herhangi bir ERC-20 token'ıyla etkileşime girebilen uygulamalar geliştirmesini kolaylaştırdığı gibi kullanıcıların token varlıklarını yönetmesini de kolaylaştırır.

ERC-20 standardı Ethereum topluluğu tarafından geniş çapta benimsenmiştir. Bugün 200.000'den fazla ERC-20 token'ı bulunmakta ve standart; merkeziyetsiz borsalar, borç verme platformları ve oyun tabanlı dapp'ler dahil çok çeşitli uygulamalar tarafından kullanılmaktadır.

## Fikir

### Tüm token'lar için ortak işlev ve özellik kümesi

ERC-20 standardı, ERC-20 uyumlu tüm token'ların uygulaması gereken altı temel işlevden oluşan bir küme tanımlar. Bu işlevler şunlardır:

- `transfer(address to, uint256 amount)`: Çağıranın adresinden belirtilen adrese belirli miktarda token aktarır.
- `approve(address spender, uint256 amount)`: Belirtilen adresin, çağıran adına belirli miktarda token harcamasına yetki verir.
- `allowance(address owner, address spender)`: Belirtilen harcayıcının (spender), belirtilen sahip (owner) adına harcamasına izin verilen token miktarını döndürür.
- `totalSupply()`: Dolaşımdaki toplam token sayısını döndürür.
- `balanceOf(address owner)`: Belirtilen adresin sahip olduğu token sayısını döndürür.
- `name()`: Token'ın adını döndürür.
- `symbol()`: Token'ın sembolünü döndürür.

ERC-20 standardı ayrıca, ilgili işlevlerin başarıyla yürütülmesi üzerine yayımlanması gereken iki olay tanımlar. Bu olaylar şunlardır:

- `Transfer(address from, address to, uint256 amount)`: Bir adresten diğerine belirli miktarda token aktarıldığında yayımlanır.
- `Approval(address owner, address spender, uint256 amount)`: Belirtilen adrese, belirtilen sahip (owner) adına belirli miktarda token harcama yetkisi verildiğinde yayımlanır.

## Etki

### DeFi'nin büyümesi ve Ethereum'un benimsenmesi

ERC-20 standardı Ethereum ekosistemi üzerinde önemli bir etki bırakmıştır. DeFi (Merkeziyetsiz Finans) hareketinin başlıca itici güçlerinden biri olmuş ve Ethereum'un benimsenmesini artırmaya da katkı sağlamıştır.

Borç vermeden varlık yönetimine kadar bir dizi finansal hizmet sunan DeFi platformları, işlemleri kolaylaştırmak için büyük ölçüde token'lara dayanır. ERC-20'nin evrensel bir adaptör işlevi görmesiyle, DeFi uygulamalarının kodlarını her token için ayrı ayrı uyarlamak zorunda kalmadan geniş bir token yelpazesini bünyesine katması çok daha kolay hale gelmiştir.

ERC-20 standardı kullanıcıların token varlıklarını yönetmesini de kolaylaştırmıştır. Token'lar aynı temel kurallara uyduğu için kullanıcılar, token varlıklarını birden fazla platform arasında aktarmayı, harcamayı ve yönetmeyi daha kolay buluyor. Gelişen bu kullanıcı deneyimi, Ethereum'un artan benimsenme oranlarının itici bir etkeni olmuştur.

## Teşvikler

### Düşük geliştirme maliyetleri ve gelişmiş güvenlik

ERC-20 protokolünün getirdiği standartlaşmanın doğrudan ekonomik bir etkisi de olmuştur. Token oluşturmak için test edilmiş ve toplulukça onaylanmış bir şablon sunarak geliştiriciler için giriş engellerini önemli ölçüde azaltmıştır. Geliştiriciler artık tekerleği yeniden icat etmek zorunda olmadıkları için yeni bir token'ı daha düşük geliştirme maliyetiyle ve daha kısa sürede piyasaya sunabiliyor. Standart ayrıca, herhangi bir ERC-20 token'ıyla evrensel biçimde etkileşime girebilen DApp'lerin (Merkeziyetsiz Uygulamalar) ve hizmetlerin oluşturulmasını dolaylı olarak teşvik ederek daha canlı bir ekosistemi besler.

Bir diğer önemli fayda, güvenliğin güçlenmesidir. ERC-20 standardı Ethereum topluluğu tarafından titiz bir incelemeden geçmiş ve bu sayede token uygulaması için sağlam ve güvenli bir model haline gelmiştir. Bu standarda uyulması, token'ın akıllı sözleşmesinin temel unsurlarının toplulukça kabul görmüş en iyi uygulamalarla örtüştüğü anlamına gelir. Bu da hatalı tasarlanmış bir token modelinden kaynaklanabilecek güvenlik açıklarının riskini en aza indirir. Her tür açığa karşı bir garanti olmasa da, token'ların ve dolayısıyla onları kullanan projelerin genel güvenliğini sağlama yolunda önemli bir adımdır.

![divider](https://cloudcdn.pro/clients/common/images/elements/divider.svg).class=\"m-10 w-100\"

**Birlikte geçirdiğimiz zaman burada sona eriyor. Ayırdığınız vakit için teşekkür ederim!**

Herhangi bir sorunuz olursa, [LinkedIn ⧉][11] üzerinden veya [İletişim sayfası][10] aracılığıyla benimle iletişime geçmekten çekinmeyin. Ayırdığınız vakit için tekrar teşekkür eder, sizden haber almayı dört gözle beklerim.

[**❬ Makalelere Dön**][09]

[09]: /articles/index.html "Makalelere Dön"
[10]: /contact/index.html "Sebastien Rousseau ile İletişime Geçin"
[11]: https://www.linkedin.com/in/sebastienrousseau/ "Sebastien Rousseau LinkedIn'de"
