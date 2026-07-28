---
title: "Google Gemma AI: Açık Kaynak Yapay Zeka Geliştirmeyi Dönüştürüyor"
subtitle: "Yeteneklere, Açık Kaynak Katkılarına ve Gelecek Adımlara Yakından Bakış"
description: "Google'ın Gemma yapay zeka modeli: Hem bireysel hem de kurumsal kullanım için etik yapay zeka çözümleri sunan açık kaynaklı bir proje."
date: "February 26, 2024"
language: "tr-TR"
locale: "tr_TR"
hreflang: "tr"
banner: "https://cloudcdn.pro/stocks/images/ai-ship.webp"
banner_alt: "Neon ışıklı fütüristik mavi uzay gemisi"
keywords: "Google Gemma AI, açık kaynak yapay zeka modeli, Gemma teknik mimarisi, Gemma 2B 7B, etik yapay zeka, macOS yapay zeka entegrasyonu, kurumsal yapay zeka çözümleri, konuşma tabanlı yapay zeka, veri analizi yapay zekası, uç cihazlar için yapay zeka"
---


## Erişilebilir ve Etik ML Geliştirme için Google'ın Açık Kaynak Yapay Zeka Modeli

Google kısa süre önce, yapay zeka geliştirme için erişilebilir ve etik bir temel sunmak üzere tasarlanmış açık kaynaklı bir yapay zeka modeli olan [**Gemma ⧉**][00] modelini kullanıma sundu. Açık kaynaklı bir model olarak Gemma; tam mimarisini, eğitim metodolojisini, model ağırlıklarını ve parametrelerini izin veren lisanslar altında sunar. Böylece dış araştırmacılar ve geliştiriciler bunlara serbestçe erişebilir, bunlardan öğrenebilir, üzerine geliştirme yapabilir ve hatta kendi özel ihtiyaçlarına göre uyarlayabilir. Bu şeffaf yaklaşım, hesap verebilirliği korumak amacıyla Gemma'nın geliştirme uygulamalarının da incelenmesine olanak tanır.

`Gemma 2B` ve `7B` gibi yapılandırmalarıyla mobil cihazlardan bulut altyapılarına kadar geniş bir uygulama yelpazesine hitap eder. Gemma'nın açık kaynak topluluğuna sunulması, Google'ın etik yapay zekaya yönelik güçlü bağlılığını gösterir ve dünya genelindeki geliştiricilerle yeniliği ve iş birliğini teşvik eder.

Bu makale; Gemma'nın mimarisini, macOS ile entegrasyonunu ve kurumsal çözümleri ile daha geniş yapay zeka alanını dönüştürme potansiyelini inceler.

![Google Gemma Logosu - Kaynak: Google](https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/gemma.svg).class=\"fade-in w-25 p-5 float-end\"

## Gemma'yı Anlamak

### Gemma'nın Teknik Mimarisi

Google'ın Gemini mimarisi Gemma'ya ilham verir ve Gemma iki ana yapılandırmada sunulur:

- **Gemma 2B** modeli, daha düşük bellek kullanımı ve güç tüketimiyle cihaz üzerinde verimlilik için optimize edilmiştir. Bu da onu akıllı telefonlardaki konuşma botları veya akıllı ev cihazları gibi mobil ve gömülü uygulamalar için ideal kılar.

- **Gemma 7B** modeli, büyük veri kümelerini ve belgeleri çözümleme gibi daha karmaşık görevlere uygun, belirgin biçimde daha yüksek bir kapasiteye sahiptir. Bu modelin yeri, veritabanları üzerinde çıkarım çalıştıran veri merkezleri ve bulut altyapısıdır.

Her ikisi de kişisel projelerden kurumsal çözümlere kadar uzanan kullanımlar için çok yönlü yapay zeka yapı taşları sağlar.

### Gemma'nın Eğitimi ve Yetenekleri

[**Teknik rapor ⧉**][01] temel alındığında, Gemma modelleri (2B ve 7B); web içeriği, matematik ve programlamaya ağırlık veren devasa veri kümeleri üzerinde eğitilmiş gelişmiş modellerdir. Bu modeller, öncülleri Gemini'nin aksine çok dilli veya çok kipli özellikleri önceliklendirmez. Kapsamlı bir sözcük dağarcığı içerir ve farklı veri türlerinin işlenmesini iyileştiren yeni bir belirteçleme yaklaşımı kullanır. Denetimli öğrenmeyi ve insan geri bildiriminden pekiştirmeli öğrenmeyi birleştiren komut ayarlaması yalnızca İngilizceye odaklanır ve incelikli metin anlama ile üretimi için optimize edilir. Bu metodolojik yenilik, modellerin özel alanlardaki potansiyelini vurgular ve dil modeli eğitiminin gelişen alanını gösterir.

### Gemma ve Açık Kaynak Topluluğu

[**İzin veren lisanslar ⧉**][03] altında açık kaynaklı bir sürüm olarak Gemma, aynı zamanda Google'ın etik yapay zeka iş birliğini destekleme taahhüdünü temsil eder. Dış geliştiriciler artık erişimi yaygınlaştırmak ve hesap verebilirliği korumak için Gemma'yı şeffaf bir biçimde temel alabilir, inceleyebilir ve uyarlayabilir.

![divider][divider].class=\"m-10 w-100\"

![Ollama Logosu - Kaynak: Ollama](https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/ollama.svg).class=\"fade-in w-25 p-5 float-start\"

## Google Gemma'yı macOS'te Ollama ile Entegre Etmek

[**Ollama ⧉**][02], bir macOS sisteminde yapay zeka asistanlarını yerel olarak incelemeyi sağlayan bir arayüzdür. Gemma 2B ve 7B modellerini Apple'ın M serisi bilgisayarlarında kurmak için bunu kullanacağız. Bu kılavuz, Gemma'yı macOS'te Ollama ile entegre etme sürecinde size yol gösterecektir.

Bilgisayarın işlemci mimarisini yazdırmak için uname komutunu kullanabilirsiniz. Terminal'i açın ve şunu çalıştırın:

```bash
uname -m
```

Çıktı `arm64` ise M serisi bir Mac'iniz var demektir. `x86_64` ise Intel bir Mac'iniz vardır. Bu kılavuz M serisi Mac'ler içindir.

### Ortamı Hazırlamak

#### 1. Python 3.8+, pip ve venv'in kurulu olduğundan emin olun

Başlamadan önce, Mac'inizde [**Python 3.8 ⧉**][04] veya üstünün kurulu olduğundan ve `pip` ile `venv` araçlarına sahip olduğunuzdan emin olun. Python ve pip sürümlerinizi kontrol etmek ve pip'i güncellemek için Terminal'de şu komutları çalıştırabilirsiniz:

```bash
python3 --version
pip3 --version
pip3 install --upgrade pip
```

#### 2. Bağımlılıkları yalıtmak için bir sanal ortam oluşturun

Terminal'i açın ve sistem genelindeki paketlerle çakışmaları önlemek için bir sanal ortam oluşturun.

```bash
python3 -m venv gemma_env
source gemma_env/bin/activate
```

#### 3. macOS için en son Ollama sürümünü kurun

macOS için [**en son Ollama ⧉**][05] sürümünü resmi web sitesinden indirin. Ollama uygulamasını çıkarın ve Uygulamalar klasörünüze taşıyın. Uygulamayı açın ve kurulum talimatlarını izleyin.

#### 4. Ollama kurulumunun başarılı olduğunu doğrulayın

Ollama'nın doğru kurulduğunu şunu çalıştırarak kontrol edin:

```bash
ollama --version
```

Ollama'nın sürümünün yazdırıldığını görmelisiniz.

### Sistem Önerileri

En iyi Gemma 2B performansı için şunlara ihtiyacınız olacak:

- **İşlemci**: Çok çekirdekli Intel i5 veya üstü
- **Bellek**: 16 GB RAM (Gemma 7B için 32 GB)
- **Depolama**: 50 GB boş alanlı SSD
- **macOS**: Güncel (Monterey veya sonrası)

Ollama kurulduktan sonra, Gemma modellerini yerel olarak başlatmaya ve bunlarla etkileşime geçmeye hazırsınız.

![divider][divider].class=\"m-10 w-100\"

## Yerel Gemma Örneğini Başlatmak

### 1. Gemma modelini Ollama CLI ile başlatın

Çalıştırmak istediğiniz Gemma modelini seçin:

- Gemma 2B (daha küçük model): `ollama run gemma:2b`
- Gemma 7B (daha büyük model): `ollama run gemma:7b`

### 2. İlk çalıştırma model varlıklarını indirir (zaman alabilir)

İlk çalıştırma, seçtiğiniz Gemma modelini indirir; bu işlem biraz zaman alabilir. İşlem tamamlandığında Gemma kullanıma hazır hâle gelir.

#### Örnek Konuşma Sorgusu

```bash
>>> Hello Gemma. How are you today?
```

Gemma, doğal dilde bir yanıt verecektir.

```bash
>>> Hello Gemma. How are you today?
Hello! It's a lovely day to be alive. Thank you for asking. How are you doing today? 😊
```

### Sanal Ortamı Devre Dışı Bırakmak

```bash
deactivate
```

Bu, sisteminizin varsayılan Python ortamına geri döner.

Sorun giderme yardımı veya kuruluma ilişkin daha fazla ayrıntı için [Ollama Belgeleri ⧉](https://ollama.com/docs) ve [Gemma Belgeleri ⧉](https://github.com/google-deepmind/gemma) kaynaklarına bakın.

![divider][divider].class=\"m-10 w-100\"

## Gemma'nın Açık Kaynak Etkisi

Piyasaya sürülmesinden bu yana Gemma, erişilebilir ve iş birliğine dayalı açık kaynak yaklaşımı sayesinde yeniliği hızla artırdı.

İzin veren lisanslama, araştırma amacıyla Gemma'nın kendi mimarisinin incelenmesine ve çok ayrıntılı düzeyde değişiklik yapılmasına da olanak tanır. Geliştiriciler; ince ayarları, uyarlamaları ve tümüyle yeni yetenekleri kod iş birliği platformlarında paylaşıyor.

Bu ortak çaba, gelişen en iyi uygulamalarla uyumlu, etik ve hesap verebilir yapay zeka sistemleri kurmak için Gemma'nın yeteneklerini sürekli iyileştiriyor.

Zamanla, açık kaynaklı bir platform olma niteliği sayesinde Gemma için araçlardan, entegrasyonlardan ve hatta tümüyle yeni uygulamalardan oluşan bir ekosistem ortaya çıkabilir.

![divider][divider].class=\"m-10 w-100\"

## Kurumsal Çözümler için Gemma Kullanım Senaryoları

Google'ın yapay zeka modeli Gemma, teknik mimarisi ve açık kaynaklı yapısıyla belirli iş ihtiyaçlarını karşılamak üzere çeşitli kurumsal çözümler sunar.

### 1. Sohbet Botları ve Konuşma Ajanları

Gemma'nın daha küçük modeli olan Gemma 2B, cihaz üzerinde verimlilik için optimize edilmiştir; bu da onu **konuşma botları** ve **sanal asistanlar** geliştirmek için ideal kılar. Kuruluşlar, kapsamlı hesaplama kaynaklarına gerek duymadan müşteri hizmetlerini, desteği ve etkileşimi güçlendirmek için bu yapay zeka destekli ajanları mobil cihazlara veya gömülü sistemlere dağıtabilir.

Gemma yeni piyasaya sürülmüş olsa da yetenekleri, müşterilere yardımcı olan yapay zeka sohbet botları ve sanal ajanların mevcut uygulamalarıyla iyi biçimde örtüşür. Gemma olgunlaştıkça, yeni nesil konuşma arayüzlerini mümkün kılan doğrudan entegrasyonlar görmeyi bekliyoruz.

### 2. Veri Analizi ve İçgörüler

Karmaşık görevler için daha yüksek kapasiteye sahip olan daha büyük Gemma 7B modeli, büyük veri kümelerini ve belgeleri çözümlemeye uygundur. Kuruluşlar, karar verme süreçlerine ve stratejik planlamaya yardımcı olacak biçimde büyük miktardaki veriden içgörü, eğilim ve örüntü çıkarmak için bu modelden yararlanabilir.

### 3. İçerik Oluşturma ve Özetleme

Gemma modelleri; raporlar, makaleler ve pazarlama materyalleri gibi içeriklerin üretilmesine ve özetlenmesine yardımcı olabilir. Bu yetenek, yüksek kaliteli içerik üretmek için gereken zamanı ve emeği önemli ölçüde azaltabilir ve işletmelerin yaratıcılığa ve stratejiye odaklanmasını sağlayabilir.

### 4. Kişiselleştirilmiş E-posta Pazarlaması ve Reklam Hedefleme

Doğal dili anlayarak ve üreterek Gemma, kuruluşların daha kişiselleştirilmiş ve etkili e-posta pazarlama kampanyaları ile reklam hedefleme stratejileri oluşturmasına yardımcı olabilir. Bu kullanım senaryosu, müşteri etkileşiminin ve dönüşüm oranlarının iyileşmesini sağlayabilir.

### 5. Uç Cihazlar için Doğal Dil İşleme (NLP)

Gemma'nın optimizasyonları, NLP görevlerinin doğrudan uç cihazlarda çalıştırılmasına uygun hâle getirir. Bu yetenek; perakende, üretim ve IoT uygulamaları gibi alanlarda gerçek zamanlı iş kararlarının alınmasına ve daha kesintisiz gerçek dünya entegrasyonlarına olanak tanır.

### 6. Geliştiriciler için Kod Zekâsı

Gemma, kod düzenleme ve geliştirme görevleri için doğal dil arayüzleri sunarak geliştirici verimliliğini artırabilir. Örneğin geliştiriciler; kod önerileri, işlevlerin açıklamaları, hata ayıklama yardımı ve kod incelemeleri almak için konuşma sorgularını kullanabilir. Gemma, ilgili önerileri sunmak için bağlamı ve anlamı çözümler. Bu \"yapay zeka eşli programlayıcı\", iş akışlarını sadeleştirmeye, hataları azaltmaya ve yapay zeka destekli ürünlerin geliştirilmesini hızlandırmaya yardımcı olabilir.

### 7. Çok Kipli Uygulamalar

Metin, ses ve görüntü alanlarında bilgi işleyebilme yeteneğiyle Gemma, kipler arası kullanım senaryoları için çok yönlüdür. Bu özellik; sanal gerçeklik (VR) ve artırılmış gerçeklik (AR) deneyimleri gibi kullanıcılarla daha doğal ve sezgisel biçimde etkileşim gerektiren uygulamalar için özellikle yararlıdır.

Gemma'nın açık kaynaklı yapısı ve teknik çok yönlülüğü, yapay zekayı operasyonel ihtiyaçları genelinde kullanmak isteyen kuruluşlar için onu değerli bir araç hâline getirir. Gemma, müşteri deneyimini güçlendiren sanal asistanlar ve sohbet botları oluşturmada beceriklidir ve büyük miktarda veri analizini işleyebilir. Açık kaynaklı modeli aynı zamanda yeniliği ve iş birliğini teşvik eder ve kuruluşların Gemma'yı kendi ihtiyaçlarını karşılayacak biçimde uyarlamasına olanak tanır.

![divider][divider].class=\"m-10 w-100\"

## Gelecek Ne Getiriyor?

İleriye baktığımızda Gemma, daha fazla büyüme ve gelişme için hazır konumdadır. Çeşitli donanım ortamlarıyla uyumluluğunu artırmaya, ek diller için desteği iyileştirmeye ve uygulama yelpazesini genişletmeye yönelik çalışmalar sürüyor. Google ve Gemma; doğruluk, önyargı tespiti ve güvenli veri kullanımı konularındaki zorlukları ele almayı ve Gemma'yı etik yapay zeka geliştirmede öncü bir konuma yerleştirmeyi amaçlıyor.

![divider][divider].class=\"m-10 w-100\"

## Sonuç

Gemma'nın piyasaya sürülmesi, yapay zeka alanında bir dönüm noktasıdır ve daha erişilebilir, etik ve iş birliğine dayalı geliştirme uygulamalarına yönelik bir kaymayı öne çıkarır. Gelişmeye devam ettikçe Gemma, yapay zekanın geleceğini biçimlendirmede belirleyici bir rol üstlenecek ve açık kaynak projelerinin etik standartlara bağlı kalırken yeniliği nasıl ilerletebileceğine dair bir örnek sunacaktır.

[00]: https://ai.google.dev/gemma "Google Gemma AI"
[01]: https://storage.googleapis.com/deepmind-media/gemma/gemma-report.pdf "Gemma Technical Report"
[02]: https://ollama.com "Ollama"
[03]: https://ai.google.dev/gemma/terms "Gemma Licensing"
[04]: https://www.python.org/downloads/release/python-380/ "Python 3.8"
[05]: https://ollama.com/download "Ollama Download"

[divider]: https://cloudcdn.pro/clients/common/images/elements/divider.svg "Divider"
