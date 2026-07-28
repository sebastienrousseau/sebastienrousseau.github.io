---
title: "LibMake: Rust Kütüphane İskeleti Üreticisi"
subtitle: "LibMake: en iyi uygulamaları ilk günden zorunlu kılan bir Rust kod üreticisi"
description: "LibMake, tek bir komuttan ya da sürümlenmiş bir TOML/YAML yapılandırma dosyasından eksiksiz bir kütüphane iskeleti üreten bir Rust CLI aracıdır. Ürettikleri arasında doküman şablonlu Cargo.toml ve src/lib.rs, test ve benchmark koşumları ile GitHub Actions CI yer alır."
date: "October 26, 2023"
language: "tr-TR"
locale: "tr_TR"
hreflang: "tr"
banner: "https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp"
banner_alt: "Devasa beyaz sütunlar"
keywords: "LibMake, Rust kod üretici, cargo iskeleti, Rust kütüphane şablonu, Tera şablonlama, GitHub Actions Rust, cargo-audit, Rust API Kılavuzu, boilerplate üretici, Rust CI iş akışı"
---


![Devasa beyaz sütunlar](https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp).class=\"img-fluid clearfix\"

---

> **TL;DR.** LibMake, tek bir komuttan ya da sürümlenmiş bir TOML/YAML yapılandırma dosyasından eksiksiz bir kütüphane iskeleti üreten bir Rust CLI aracıdır: doküman şablonlu Cargo.toml ve src/lib.rs, test ve benchmark koşumları ile GitHub Actions CI.
>
> **Önemli Çıkarımlar**
>
> - **Kurulum ve Temel Kullanım.** LibMake, crates.io üzerinde yayımlanır ve Cargo ile kurulur.
> - **Yapılandırma Dosyası Modu.** Ekip kullanımı için tüm CLI bayrakları bir TOML yapılandırma dosyasında ifade edilebilir.
> - **Üretilen Proje Yapısı.** Bir LibMake çağrısı belirli bir dizin düzeni oluşturur.
> - **GitHub Actions CI İş Akışı.** Üretilen `.github/workflows/release.yml`, her push ve pull request'te beş iş çalıştırır.

---

[**LibMake ⧉**][00], tek bir çağrıyla eksiksiz bir kütüphane projesi iskeleti üreten açık kaynaklı bir Rust CLI aracı ve kütüphanesidir. Yalnızca asgari bir Cargo.toml ve src/lib.rs oluşturan `cargo new --lib` ile üretime hazır bir kütüphane kurulumu arasındaki boşluğu hedefler; bu kurulum, doküman yorumlarının, CI'nin, test koşumlarının, benchmark yapısının, CONTRIBUTING.md ve lisans dosyalarının elle eklenmesini gerektirir.

Bu makale, LibMake'in neler ürettiğini, yapılandırma dosyası ve CLI modlarının nasıl çalıştığını, üretilen CI yapısını ve şablonlama sistemini açıklar.

## Kurulum ve Temel Kullanım

LibMake, [crates.io](https://crates.io/crates/libmake) üzerinde yayımlanır ve Cargo ile kurulur:

```bash
cargo install libmake
```

Asgari CLI çağrısı, geçerli dizinde adlandırılmış bir kütüphane üretir:

```bash
libmake \
  --author "Jane Smith" \
  --email "jane@example.com" \
  --name "my_library" \
  --description "A Rust library for doing useful things" \
  --version "0.1.0" \
  --licence "MIT OR Apache-2.0" \
  --repository "https://github.com/example/my_library" \
  --rustversion "1.70.0" \
  --edition "2021" \
  --output "my_library"
```

Ek isteğe bağlı bayraklar arasında `--categories`, `--keywords`, `--homepage`, `--documentation`, `--readme` ve `--build` bulunur.

## Yapılandırma Dosyası Modu

Ekip kullanımı için tüm CLI bayrakları bir TOML yapılandırma dosyasında ifade edilebilir:

```toml
# libmake.toml


author      = "Jane Smith"
email       = "jane@example.com"
name        = "my_library"
description = "A Rust library for doing useful things"
version     = "0.1.0"
licence     = "MIT OR Apache-2.0"
repository  = "https://github.com/example/my_library"
rustversion = "1.70.0"
edition     = "2021"
output      = "my_library"
categories  = ["algorithms", "data-structures"]
keywords    = ["rust", "library"]
```

Şu şekilde çağrılır:

```bash
libmake --config libmake.toml
```

LibMake ayrıca `--config-json`, `--config-yaml` ve `--config-csv` bayrakları aracılığıyla sırasıyla JSON, YAML ve CSV yapılandırma biçimlerini de kabul eder. `libmake.toml` dosyasını depo köküne işlemek, her katkıda bulunana yeniden üretilebilir bir iskelet temeli sağlar ve şablon yapılandırmasındaki değişiklikler Git farklarında görünür.

## Üretilen Proje Yapısı

Bir LibMake çağrısı şu düzeni oluşturur:

```
my_library/
├── .github/
│   └── workflows/
│       └── release.yml     # full CI matrix
├── benches/
│   └── lib_benchmarks.rs   # Criterion benchmark stub
├── src/
│   └── lib.rs              # doc-commented, deny(missing_docs)
├── tests/
│   └── lib_tests.rs        # integration test stub
├── CONTRIBUTING.md
├── Cargo.toml              # complete metadata
├── LICENSE-APACHE
├── LICENSE-MIT
└── README.md
```

Üretilen `src/lib.rs`, sandık düzeyinde bir doküman yorumu, `#![deny(missing_docs)]`, README'yi rustdoc'a çekmek için `#![doc = include_str!("../README.md")]` ve ilişkili bir doküman yorumuna sahip bir taslak genel tür içerir. Bu seçimler, tüm genel öğelerin belgelenmesi gerektiğini belirten Rust API Kılavuzu gereksinimini izler.

Üretilen `benches/lib_benchmarks.rs`, [Criterion.rs](https://github.com/bheisler/criterion.rs) kullanır ve `criterion` öğesinin bir geliştirme bağımlılığı olarak eklenmesini gerektirir; LibMake bunu `Cargo.toml` dosyasına otomatik olarak ekler.

## GitHub Actions CI İş Akışı

Üretilen `.github/workflows/release.yml`, her push ve pull request'te beş iş çalıştırır:

| İş | Araç Zinciri | Neyi denetler |
|---|---|---|
| `test` | stable, beta, nightly (matris) | `cargo test --all-features` |
| `clippy` | stable | `cargo clippy -- -D warnings` |
| `fmt` | stable | `cargo fmt --check` |
| `audit` | stable | `cargo audit` (cargo-audit işte kurulur) |
| `doc` | stable | `cargo doc --no-deps` (eksik dokümanlarda başarısız olur) |

nightly işinde `continue-on-error: true` ayarı bulunur; böylece bir nightly regresyonu birleştirmeleri engellemez, ancak yine de hatayı iş akışı çalışmasında görünür kılar.

## Tera ile Şablonlama

LibMake, tüm üretilen dosyaları oluşturmak için [Tera](https://keats.github.io/tera/) şablon motorunu kullanır; bu, Rust için Jinja2 benzeri bir söz dizimidir. Her şablon, bağlam olarak tam yapılandırma yapısını alır:

```
{{ name }}            → my_library
{{ author }}          → Jane Smith
{{ edition }}         → 2021
{{ description }}     → A Rust library for doing useful things
```

Özel şablon dizinleri `--template` bayrağı aracılığıyla desteklenir:

```bash
libmake --config libmake.toml --template ./my_templates/
```

Özel dizin, varsayılan şablon yapısını (aynı dosya adları) yansıtmalıdır. Özel dizinde bulunan herhangi bir dosya, karşılık gelen yerleşik şablonu geçersiz kılar; özel dizinde bulunmayan dosyalar yerleşik sürüme geri döner. Bu, kısmi geçersiz kılmalara olanak tanır; örneğin, varsayılan src/lib.rs ve Cargo.toml şablonlarını korurken yalnızca CI iş akışı şablonunu değiştirmek gibi.

## Sıkça Sorulan Sorular

**LibMake, `cargo new --lib`'den nasıl farklıdır?**
`cargo new --lib`, yalnızca `Cargo.toml` ve `src/lib.rs` (tek bir `#[cfg(test)]` bloğu içeren) ile asgari bir proje oluşturur. LibMake ise tam yapıyı üretir: entegrasyon testleri, benchmark'lar, CI, CONTRIBUTING.md, ikili lisans dosyaları ve düzgün belgelenmiş bir src/lib.rs; bunlar yer tutucular yerine projenin gerçek meta verileriyle yapılandırılır.

**LibMake mevcut bir Cargo çalışma alanıyla kullanılabilir mi?**
LibMake bağımsız bir sandık dizini üretir. Üretilen sandığı mevcut bir çalışma alanına eklemek için, çıktı yolunu kök `Cargo.toml` dosyasındaki çalışma alanı `members` dizisine ekleyin. LibMake mevcut çalışma alanı dosyalarını değiştirmez.

**İlk üretimden sonra iskelet şablonlarını güncelleyebilir miyim?**
LibMake dosyaları bir kez üretir; önceden üretilmiş projeleri izlemez veya güncellemez. Güncellenmiş şablonları benimsemek için önerilen yaklaşım, LibMake'i geçici bir dizine yeniden çalıştırmak ve sonucu mevcut sandıkla karşılaştırarak istenen değişiklikleri seçmeli olarak uygulamaktır.

**LibMake hangi Rust sürümlerini ve MSRV değerlerini destekler?**
LibMake, `--edition` ve `--rustversion` için herhangi bir dizeyi kabul eder ve değerleri doğrudan `Cargo.toml` dosyasına yazar. Belirtilen sürümün veya MSRV'nin gerçek bir Rust sürümü olup olmadığını doğrulamaz; bu nedenle doğru değerlerin sağlanmasından çağıranlar sorumludur.

## Kaynaklar

1. Rousseau, S. *LibMake — A code generator to reduce repetitive tasks and build high-quality Rust libraries*. GitHub, 2023. https://github.com/sebastienrousseau/libmake
2. The Rust Programming Language. *Rust API Guidelines*. GitHub, 2023. https://rust-lang.github.io/api-guidelines/
3. The Cargo Book. *Package Layout*. The Rust Programming Language, 2023. https://doc.rust-lang.org/cargo/guide/project-layout.html
4. Keats, V. et al. *Tera — A template engine inspired by Jinja2 and Django templates*. GitHub, 2023. https://keats.github.io/tera/

[00]: https://github.com/sebastienrousseau/libmake "LibMake: Rust kütüphane iskeleti üreticisi"
