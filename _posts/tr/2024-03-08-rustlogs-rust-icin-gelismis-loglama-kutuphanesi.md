---
title: "RustLogs: Rust uygulamaları için gelişmiş loglama kütüphanesi"
subtitle: "Üretim Rust uygulamaları için sağlam loglama"
description: "RustLogs, üretim Rust uygulamaları için yapılandırılmış, performanslı bir loglama kütüphanesidir."
date: "March 08, 2024"
language: "tr-TR"
locale: "tr_TR"
banner: "https://cloudcdn.pro/stocks/images/rustlogs.webp"
banner_alt: "Bir kod terminalinin görselleştirmesi"
keywords: "RustLogs, Rust, loglama, observability, açık kaynak, üretim"
---


---

> **TL;DR.** RustLogs (RLG), yapılandırılmış log formatları, eşzamansız loglama ve kapsamlı özelleştirme seçenekleri sunan esnek Rust loglama kütüphanesidir.
>
> **Önemli Çıkarımlar**
>
> - **1. Etkili Loglamaya Duyulan İhtiyacı Anlamak.** RustLogs (RLG) ayrıntılarına geçmeden önce, yazılım geliştirmede etkili loglamanın neden temel olduğunu anlamak için biraz duralım.
> - **2. RustLogs (RLG): Kapsamlı Bir Loglama Kütüphanesi.** RustLogs (RLG), Rust uygulamalarına loglama yeteneği eklemeyi basitleştirmeyi ve düzenlemeyi amaçlayan, özellik açısından zengin bir loglama kütüphanesidir.
> - **3. RustLogs (RLG) ile Başlangıç.** RustLogs (RLG)'yi Rust projenizde kullanmaya başlamak için onu Cargo.toml dosyanıza bağımlılık olarak eklemeniz gerekir.
> - **4. RustLogs (RLG) ile Eşzamansız Loglama.** RustLogs (RLG)'nin öne çıkan özelliklerinden biri, eşzamansız loglama desteğidir.

---

## Giriş

Yazılım geliştirme dünyasında loglama; bir uygulamanın davranışını anlamada, sorunları teşhis etmede ve sorunsuz çalışmayı sağlamada önemli bir rol oynar. Performansı ve güvenliğiyle bilinen bir sistem programlama dili olan Rust, geliştiricilere geniş bir loglama çözümleri yelpazesi sunar. Bu kütüphaneler arasında RustLogs (RLG) doğdu. Rust uygulamalarına sağlam loglama yetenekleri eklemeyi kolaylaştıran güçlü ve esnek bir loglama kütüphanesidir.

![divider][divider].class=\"m-10 w-100\"

### 1. Etkili Loglamaya Duyulan İhtiyacı Anlamak

RustLogs (RLG) ayrıntılarına geçmeden önce, yazılım geliştirmede etkili loglamanın neden temel olduğunu anlamak için biraz duralım. Loglama; bir uygulamanın davranışı, veri akışı ve olası sorunları hakkında çalışma zamanı bilgisini yakalamak için önemli bir tekniktir. Geliştiriciler, kod tabanı boyunca log ifadelerini stratejik olarak yerleştirerek uygulamanın iç işleyişine dair değerli bilgiler edinebilir ve her türlü anomaliyi veya hatayı tespit edebilir. Geliştiriciler, koda log ifadelerini stratejik olarak ekleyerek fonksiyon çalıştırmaları, değişken içerikleri ve hata bildirimleri gibi önemli verileri etkili biçimde toplayabilir. Bu bilgi; hataları giderirken, performansı iyileştirirken veya beklenmeyen davranışları incelerken paha biçilmez hale gelir.

Ancak loglama işlevini sıfırdan uygulamak zaman alan ve hataya açık bir görev olabilir. Log seviyelerinin, biçimlendirmenin, çıktı hedeflerinin ve performans maliyetinin dikkatle değerlendirilmesini gerektirir. RustLogs (RLG) tam da burada devreye girerek özellikle Rust geliştiricileri için tasarlanmış kapsamlı ve kullanıcı dostu bir loglama çözümü sunar.

![divider][divider].class=\"m-10 w-100\"

### 2. RustLogs (RLG): Kapsamlı Bir Loglama Kütüphanesi

RustLogs (RLG), Rust uygulamalarına loglama yeteneği ekleme sürecini basitleştirmeyi ve düzenlemeyi amaçlayan, özellik açısından zengin bir loglama kütüphanesidir. Temiz ve sezgisel bir API'nin yanı sıra güçlü bir makro kümesi sunarak loglamayı kod tabanınıza entegre etmeyi kolaylaştırır. RustLogs (RLG) geniş bir log seviyesi yelpazesi sunar. Bu, bilginin önem ve ciddiyetine göre loglarınızın ne kadar ayrıntılı olacağını denetlemenizi sağlar.

RustLogs (RLG)'nin temel güçlü yanlarından biri, log biçimlendirme ve çıktı hedefleri açısından esnekliğidir. Yapılandırılmış loglama desteklenir; bu sayede log verilerini JSON gibi yapılandırılmış bir biçimde yakalayabilirsiniz. Bu, ayrıştırmayı ve analizi kolaylaştırır. Ayrıca RustLogs (RLG); syslog, Apache Access Log ve Log4j XML gibi yaygın loglama çerçeveleri dahil olmak üzere çeşitli çıktı biçimleriyle uyumluluk sağlar. Bu çok yönlülük, RustLogs (RLG)'nin mevcut loglama altyapıları ve araçlarıyla sorunsuz biçimde entegre olmasını sağlar.

![divider][divider].class=\"m-10 w-100\"

### 3. RustLogs (RLG) ile Başlangıç

RustLogs (RLG)'yi Rust projenizde kullanmaya başlamak için onu `Cargo.toml` dosyanıza bağımlılık olarak eklemeniz gerekir. RustLogs (RLG)'nin istediğiniz sürümünü belirtin ve gerisini Cargo'ya bırakın:

```toml
[dependencies]
rlg = "0.0.3"
```

Bağımlılık eklendikten sonra RustLogs (RLG)'yi Rust kodunuzda kullanmaya başlayabilirsiniz. Kütüphane, log kayıtları oluşturmak için basit ve sezgisel bir API sunar. İşte temel bir örnek:

```rust
use rlg::log::Log;
use rlg::log_format::LogFormat;
use rlg::log_level::LogLevel;

let log_entry = Log::new(
    "session_id",
    "timestamp",
    &LogLevel::INFO,
    "component",
    "This is a log message",
    &LogFormat::JSON,
);
```

Yeni bir log kaydı oluşturmak için `Log::new()` fonksiyonunu kullanın. Oturum kimliğini, zaman damgasını, log seviyesini, bileşeni, log mesajını ve log biçimini (bu örnekte JSON) belirtin. RustLogs (RLG) önceden tanımlı log seviyeleri ve biçimleri sunar. `ALL`, `DEBUG`, `DISABLED`, `ERROR`, `FATAL`, `INFO`, `NONE`, `TRACE`, `VERBOSE` ve `WARNING` gibi log seviyeleri arasından seçim yapın. Log biçimleri için `CLF`, `JSON`, `CEF`, `ELF`, `W3C`, `GELF`, `ApacheAccessLog`, `Logstash`, `Log4jXML` ve `NDJSON` arasından seçin. Bu, loglama kurulumunuz üzerinde tam denetim sağlar.

![divider][divider].class=\"m-10 w-100\"

### 4. RustLogs (RLG) ile Eşzamansız Loglama

RustLogs (RLG)'nin öne çıkan özelliklerinden biri, eşzamansız loglama desteğidir. Modern yazılım geliştirmede performans son derece önemlidir ve loglama amacıyla ana yürütme iş parçacığını bloke etmek gereksiz gecikmeye yol açabilir. RustLogs (RLG), kutudan çıktığı haliyle eşzamansız loglama yetenekleri sunarak bu sorunu çözer.

RustLogs (RLG) ile bir log kaydındaki `log()` metodunu kullanarak mesajları eşzamansız olarak loglayabilirsiniz. Bu metot, uygulamanızın ana mantığı sırasında çalışan bir `Future` döndürür. Bu, uygulamanızın loglamanın bitmesini beklemeden devam etmesini sağlar. İşte RustLogs (RLG) ile eşzamansız loglamaya bir örnek:

```rust
use rlg::log::Log;
use rlg::log_format::LogFormat;
use rlg::log_level::LogLevel;

async fn log_async() {
    let log_entry = Log::new(
        "session_id",
        "timestamp",
        &LogLevel::INFO,
        "component",
        "This is an async log message",
        &LogFormat::JSON,
    );

    match log_entry.log().await {
        Ok(_) => println!("Log message written successfully"),
        Err(e) => eprintln!("Error writing log message: {}", e),
    }
}
```

Eşzamansız loglamadan yararlanan RustLogs (RLG), uygulamanızın performansının loglama işlemleri nedeniyle bozulmamasını sağlar. Bu, yüksek verimli senaryolarda veya büyük hacimli log verileriyle çalışırken özellikle yararlıdır.

![divider][divider].class=\"m-10 w-100\"

### 5. Esnek Yapılandırma ve Özelleştirme

RustLogs (RLG), farklı loglama gereksinimlerini karşılamak için yüksek düzeyde esneklik ve özelleştirme seçenekleri sunar. Log dosyası konumu, log seviyeleri ve çıktı biçimleri gibi farklı loglama seçeneklerini yapılandırabilirsiniz. Bu, loglamayı uygulamanızın ihtiyaçlarına göre kurmanızı sağlar.

RustLogs (RLG) varsayılan olarak mesajları geçerli dizindeki `RLG.log` adlı bir dosyaya loglar. Ancak `LOG_FILE_PATH` ortam değişkenini ayarlayarak log dosyası yolunu kolayca özelleştirebilirsiniz:

```rust
std::env::set_var("LOG_FILE_PATH", "/path/to/custom/log/file.log");
```

Bu esneklik, log çıktısını dağıtım ortamınıza veya loglama altyapınıza göre farklı dosyalara yönlendirmenizi sağlar.

Ayrıca RustLogs (RLG), yapılandırma ayarlarını ortam değişkenlerinden yüklemenize veya varsayılan değerlere geri dönmenize olanak tanıyan bir `Config` yapısı sunar. Bu, loglama yapılandırmanızı merkezileştirmenizi ve kodunuzu değiştirmeden kolayca düzenlemenizi sağlar:

```rust
use rlg::config::Config;

let config = Config::load();
```

`Config` yapısıyla, yüklenen yapılandırma ayarlarına uygulamanızın her yerinden erişebilir ve bunları kullanabilirsiniz. Bu, farklı çalıştırmalar veya dağıtımlar arasında tutarlı bir loglama davranışı sağlar.

![divider][divider].class=\"m-10 w-100\"

### 6. Loglamayı Basitleştiren Güçlü Makrolar

RustLogs (RLG), yaygın loglama görevlerini basitleştiren ve tekrarlayan (boilerplate) kodu azaltan güçlü bir makro kümesi sunar. Bu makrolar, en az kurulum ve yapılandırmayla mesaj loglamanın kullanışlı bir yolunu sağlar. İşte RustLogs (RLG)'de bulunan makrolardan birkaç örnek:

- `macro_log!`: Belirtilen parametrelerle yeni bir log kaydı oluşturur.

```rust
let log = macro_log!(session_id, time, level, component, description, format);
```

- `macro_info_log!`: Varsayılan oturum kimliği ve biçimle bir bilgi (info) logu oluşturur.

```rust
let log = macro_info_log!(time, component, description);
```

- `macro_warn_log!`: Bir uyarı logu oluşturur.

```rust
let log = macro_warn_log!(time, component, description);
```

- `macro_error_log!`: Varsayılan biçimle bir hata logu oluşturur.

```rust
let log = macro_error_log!(time, component, description);
```

Bu makrolar, log kayıtları oluşturmanın karmaşıklıklarını soyutlayarak loglamak istediğiniz temel bilgiye odaklanmanızı sağlar. Oturum kimlikleri, biçimler ve diğer parametreler için makul varsayılanlar sunarak yazmanız ve bakımını yapmanız gereken kod miktarını azaltır.

![divider][divider].class=\"m-10 w-100\"

### 7. Mevcut Loglama Altyapılarıyla Entegrasyon

RustLogs (RLG)'nin temel avantajlarından biri, çeşitli loglama altyapıları ve araçlarıyla uyumluluğudur. Kütüphane geniş bir çıktı biçimi yelpazesini destekleyerek mevcut loglama iş hatları ve analiz platformlarıyla entegrasyonu kolaylaştırır.

Örneğin, syslog gibi merkezi bir loglama sistemi kullanıyorsanız RustLogs (RLG), log mesajlarını syslog biçiminde sorunsuz biçimde yazabilir. Logstash veya Graylog gibi log toplama araçları kullanıyorsanız RustLogs, logları bu sistemlerle uyumlu biçimlerde, örneğin JSON veya GELF olarak çıktılayabilir.

Bu entegrasyon yeteneği, mevcut loglama kurulumunuzu bozmadan RustLogs (RLG)'nin gücünden yararlanabilmenizi sağlar. RustLogs (RLG)'nin sunduğu kullanım kolaylığı ve esneklikten yararlanırken tercih ettiğiniz loglama altyapısını kullanmaya devam edebilirsiniz.

![divider][divider].class=\"m-10 w-100\"

### 8. Hata Yönetimi ve Sağlamlık

Loglama işlemleri hatalara karşı bağışık değildir ve RustLogs (RLG), loglarınızın güvenilirliğini ve bütünlüğünü sağlamak için sağlam hata yönetimi mekanizmaları sunar. Kütüphane, `log()` metodundan bir `Result` türü döndürerek olası hataları düzgün biçimde ele almanıza olanak tanır.

Loglama sırasında oluşabilecek yaygın hatalar arasında dosya G/Ç hataları, biçimlendirme sorunları veya logları uzak hedeflere gönderirken ortaya çıkan ağ kaynaklı hatalar bulunur. RustLogs (RLG) bu hataları yakalar ve bilgilendirici hata mesajları sunarak bunları uygun biçimde teşhis etmenizi ve ele almanızı sağlar.

İşte RustLogs (RLG) ile hata yönetimine bir örnek:

```rust
use rlg::log::Log;
use rlg::log_format::LogFormat;
use rlg::log_level::LogLevel;

async fn log_with_error_handling() {
    let log_entry = Log::new(
        "session_id",
        "timestamp",
        &LogLevel::INFO,
        "component",
        "This is a log message",
        &LogFormat::JSON,
    );

    match log_entry.log().await {
        Ok(_) => println!("Log message written successfully"),
        Err(e) => eprintln!("Error writing log message: {}", e),
    }
}
```

RustLogs (RLG), loglama hatalarının fark edilmeden geçmemesini sağlar. Hataları etkili biçimde ele alarak düzeltici önlemler almak için ihtiyaç duyduğunuz bilgiyi size verir.

![divider][divider].class=\"m-10 w-100\"

### 9. Performans Değerlendirmeleri

Loglama söz konusu olduğunda performans dikkate alınması gereken kritik bir etkendir. Aşırı loglama veya verimsiz loglama mekanizmaları önemli bir ek yük getirebilir ve uygulamanızın genel performansını etkileyebilir. RustLogs (RLG), performans göz önünde bulundurularak tasarlanmıştır ve loglamanın sisteminiz üzerindeki etkisini en aza indirmek için çeşitli iyileştirmeler sunar.

İlk olarak, daha önce belirtildiği gibi RustLogs (RLG) eşzamansız loglamayı destekler. RustLogs (RLG) eşzamansız G/Ç işlemleri kullanır; bu sayede loglama ana iş parçacığını bloke etmez. Bu, loglama arka planda gerçekleşirken uygulamanızın işlemeye devam etmesini sağlar. Bu bloke etmeyen yaklaşım, loglama işlemlerinden kaynaklanan performans cezasını en aza indirir.

Ayrıca RustLogs (RLG) verimli biçimlendirme ve çıktı mekanizmaları kullanır. Kütüphane önceden ayrılmış arabellekler kullanır ve mümkün olduğunda gereksiz bellek ayırmalarından kaçınır. Bu iyileştirme, bellek ayak izini azaltır ve loglamanın genel verimliliğini artırır.

RustLogs (RLG), loglarınızdaki ayrıntı düzeyini denetlemenizi sağlar. Yalnızca en önemli bilgiyi loglamayı veya hata ayıklama amacıyla daha fazla ayrıntı eklemeyi seçebilirsiniz. Uygulamanızın farklı bileşenleri veya modülleri için uygun log seviyeleri yapılandırarak, üretim ortamlarında gereksiz loglamayı kaldırıp performansı iyileştirebilirsiniz.

![divider][divider].class=\"m-10 w-100\"

## Sonuç

RustLogs (RLG), loglamayı Rust uygulamalarına dahil etme sürecini basitleştiren güçlü, esnek ve kullanıcı dostu bir loglama kütüphanesidir. Yapılandırılmış loglama, eşzamansız işlemler ve yaygın loglama altyapılarıyla uyumluluk dahil olmak üzere kapsamlı özellik kümesi, onu çeşitli loglama ihtiyaçları için çok yönlü bir seçim haline getirir.

Kütüphanenin sezgisel API'si, güçlü makroları ve sağlam hata yönetimi mekanizmaları, geliştiricilerin değerli çalışma zamanı bilgisini verimli ve güvenilir biçimde yakalamasını sağlar. RustLogs'un performans iyileştirmeleri ve esnek yapılandırma seçenekleri, kullanılabilirliğini ve farklı proje gereksinimlerine uyarlanabilirliğini daha da artırır.

Kapsamlı bir belgelendirme ve Rust ekosistemiyle sorunsuz entegrasyon sayesinde RustLogs, Rust geliştiricileri için güvenilir ve etkili bir loglama çözümü olarak öne çıkar. RustLogs'un yeteneklerinden yararlanan geliştiriciler; uygulamalarının davranışına dair daha derin bilgiler edinebilir, hata ayıklama süreçlerini düzenleyebilir ve kod tabanlarının uzun vadeli sürdürülebilirliğini sağlayabilir.

Rust topluluğu büyümeye ve gelişmeye devam ederken RustLogs, geliştiricinin araç dağarcığında önemli bir araç haline gelmeyi ve onlara sağlam, iyi loglanmış ve sürdürülebilir uygulamaları kolaylıkla oluşturma imkânı vermeyi amaçlar.

[**Hemen Başlayın →**][00]

[00]: https://rustlogs.com/ "Rust Uygulamaları için Gelişmiş Bir Loglama Kütüphanesi"

[divider]: https://cloudcdn.pro/clients/common/images/elements/divider.svg "Ayırıcı"
