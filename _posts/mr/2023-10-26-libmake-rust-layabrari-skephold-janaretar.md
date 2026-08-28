---
title: "LibMake: Rust लायब्ररी स्कॅफोल्ड जनरेटर"
tags: "LibMake, RustCodeGenerator, CargoScaffold, RustLibraryTemplate, TeraTemplating, GitHubActionsRust, CargoAudit, RustAPIGuidelines, BoilerplateGenerator, RustCI, ISO 20022, post-quantum cryptography, AI, Rust, open source"
subtitle: "LibMake: पहिल्या दिवसापासून सर्वोत्तम पद्धती लागू करणारा Rust कोड जनरेटर."
description: "LibMake हे एक Rust CLI साधन आहे जे एका आज्ञेतून किंवा आवृत्तीबद्ध TOML/YAML कॉन्फिग फाइलमधून संपूर्ण लायब्ररी स्कॅफोल्ड तयार करते - Cargo.toml, doc टेम्पलेटसह src/lib.rs, चाचणी व बेंचमार्क हार्नेस आणि GitHub Actions CI."
date: "Oct 26, 2023"
language: "mr"
locale: "mr_IN"
banner: "https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp"
banner_alt: "विशाल पांढरे स्तंभ"
keywords: "LibMake, Rust कोड जनरेटर, cargo स्कॅफोल्ड, Rust लायब्ररी टेम्पलेट, Tera टेम्पलेटिंग, GitHub Actions Rust, cargo-audit, Rust API मार्गदर्शक तत्त्वे, बॉयलरप्लेट जनरेटर, Rust CI वर्कफ्लो"
---

[**LibMake ⧉**][00] हे एक ओपन-सोर्स Rust CLI आणि लायब्ररी आहे जे एका आज्ञेतून संपूर्ण लायब्ररी प्रकल्प स्कॅफोल्ड तयार करते. हे `cargo new --lib` (जे केवळ किमान Cargo.toml आणि src/lib.rs तयार करते) आणि उत्पादन-सज्ज लायब्ररी मांडणी (ज्यासाठी doc टिप्पण्या, CI, चाचणी हार्नेस, बेंचमार्क रचना, CONTRIBUTING.md आणि परवाना फाइल्स स्वहस्ते जोडाव्या लागतात) यांतील दरी भरून काढते.

हा लेख LibMake काय तयार करते, कॉन्फिग-फाइल व CLI पद्धती कशा काम करतात, तयार होणारी CI रचना आणि टेम्पलेटिंग प्रणाली यांचे वर्णन करतो.

## स्थापना आणि मूलभूत वापर

LibMake [crates.io](https://crates.io/crates/libmake) वर प्रकाशित असून Cargo द्वारे स्थापित केले जाते:

```bash
cargo install libmake
```

किमान CLI आज्ञा सध्याच्या डिरेक्टरीमध्ये नाव दिलेली लायब्ररी तयार करते:

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

अतिरिक्त ऐच्छिक फ्लॅगमध्ये `--categories`, `--keywords`, `--homepage`, `--documentation`, `--readme`, आणि `--build` यांचा समावेश आहे.

## कॉन्फिग-फाइल पद्धत

संघातील वापरासाठी, सर्व CLI फ्लॅग एका TOML कॉन्फिग फाइलमध्ये व्यक्त करता येतात:

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

अशी चालवली जाते:

```bash
libmake --config libmake.toml
```

LibMake अनुक्रमे `--config-json`, `--config-yaml`, आणि `--config-csv` फ्लॅगद्वारे JSON, YAML, आणि CSV कॉन्फिग स्वरूपेही स्वीकारते. रिपॉझिटरीच्या मुळाशी `libmake.toml` कमिट केल्याने प्रत्येक योगदानकर्त्याला पुनरुत्पादनयोग्य स्कॅफोल्ड आधाररेखा मिळते, आणि टेम्पलेट कॉन्फिगरेशनमधील बदल Git diff मध्ये दिसतात.

## तयार होणारी प्रकल्प रचना

LibMake चालवल्याने पुढील मांडणी तयार होते:

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

तयार होणाऱ्या `src/lib.rs` मध्ये क्रेट-स्तरीय doc टिप्पणी, `#![deny(missing_docs)]`, README ला rustdoc मध्ये आणण्यासाठी `#![doc = include_str!("../README.md")]`, आणि संबंधित doc टिप्पणी असलेला स्टब सार्वजनिक टाइप यांचा समावेश असतो. या निवडी Rust API मार्गदर्शक तत्त्वांच्या त्या आवश्यकतेला अनुसरून आहेत की सर्व सार्वजनिक घटकांना दस्तऐवजीकरण असावे.

तयार होणारी `benches/lib_benchmarks.rs` [Criterion.rs](https://github.com/bheisler/criterion.rs) वापरते आणि `criterion` ला dev-dependency म्हणून जोडणे आवश्यक असते, जे LibMake आपोआप `Cargo.toml` मध्ये समाविष्ट करते.

## GitHub Actions CI वर्कफ्लो

तयार होणारी `.github/workflows/release.yml` प्रत्येक push व pull request वर पाच जॉब चालवते:

| जॉब | टूलचेन | ती काय तपासते |
|---|---|---|
| `test` | stable, beta, nightly (मॅट्रिक्स) | `cargo test --all-features` |
| `clippy` | stable | `cargo clippy -- -D warnings` |
| `fmt` | stable | `cargo fmt --check` |
| `audit` | stable | `cargo audit` (जॉबमध्ये cargo-audit स्थापित) |
| `doc` | stable | `cargo doc --no-deps` (गहाळ docs असल्यास अपयशी) |

nightly जॉबमध्ये `continue-on-error: true` असल्याने nightly रिग्रेशन merge रोखत नाही, तरीही वर्कफ्लो रनमध्ये ते अपयश समोर आणले जाते.

## Tera सह टेम्पलेटिंग

LibMake सर्व तयार होणाऱ्या फाइल्स रेंडर करण्यासाठी [Tera](https://keats.github.io/tera/) टेम्पलेट इंजिन — Rust साठी Jinja2-सदृश वाक्यरचना — वापरते. प्रत्येक टेम्पलेटला संदर्भ म्हणून संपूर्ण कॉन्फिग struct मिळते:

```
{{ name }}            → my_library
{{ author }}          → Jane Smith
{{ edition }}         → 2021
{{ description }}     → A Rust library for doing useful things
```

`--template` फ्लॅगद्वारे कस्टम टेम्पलेट डिरेक्टरींना समर्थन आहे:

```bash
libmake --config libmake.toml --template ./my_templates/
```

कस्टम डिरेक्टरीने डीफॉल्ट टेम्पलेट रचनेचे (समान फाइलनावांचे) प्रतिबिंब असणे आवश्यक आहे. कस्टम डिरेक्टरीत असलेली कोणतीही फाइल संबंधित अंगभूत टेम्पलेटला ओव्हरराइड करते; कस्टम डिरेक्टरीत नसलेल्या फाइल्स अंगभूत आवृत्तीकडे परत जातात. यामुळे आंशिक ओव्हरराइड शक्य होतात — उदाहरणार्थ, केवळ CI वर्कफ्लो टेम्पलेट बदलताना डीफॉल्ट src/lib.rs आणि Cargo.toml टेम्पलेट कायम ठेवणे.

## वारंवार विचारले जाणारे प्रश्न

**LibMake हे `cargo new --lib` पेक्षा कसे वेगळे आहे?**
`cargo new --lib` केवळ `Cargo.toml` आणि `src/lib.rs` (ज्यात एकच `#[cfg(test)]` ब्लॉक असतो) असलेला किमान प्रकल्प तयार करते. LibMake संपूर्ण रचना तयार करते — एकात्मिक चाचण्या, बेंचमार्क, CI, CONTRIBUTING.md, दुहेरी-परवाना फाइल्स, आणि योग्यरीत्या दस्तऐवजीकृत src/lib.rs — प्लेसहोल्डरऐवजी प्रकल्पाच्या प्रत्यक्ष मेटाडेटासह कॉन्फिगर केलेली.

**LibMake विद्यमान Cargo workspace सोबत वापरता येते का?**
LibMake एक स्वतंत्र क्रेट डिरेक्टरी तयार करते. तयार झालेल्या क्रेटला विद्यमान workspace मध्ये जोडण्यासाठी, आउटपुट पथ मूळ `Cargo.toml` मधील workspace `members` अ‍ॅरेमध्ये जोडा. LibMake विद्यमान workspace फाइल्समध्ये बदल करत नाही.

**प्रारंभिक निर्मितीनंतर मी स्कॅफोल्ड टेम्पलेट अद्ययावत करू शकतो का?**
LibMake फाइल्स एकदाच तयार करते; ते आधी तयार केलेल्या प्रकल्पांचा मागोवा घेत नाही किंवा त्यांना अद्ययावत करत नाही. अद्ययावत टेम्पलेट स्वीकारण्यासाठी, शिफारस केलेला मार्ग म्हणजे LibMake तात्पुरत्या डिरेक्टरीत पुन्हा चालवणे आणि निकालाचा विद्यमान क्रेटशी diff घेणे, आणि इच्छित बदल निवडकपणे लागू करणे.

**LibMake कोणत्या Rust आवृत्ती आणि MSRV मूल्यांना समर्थन देते?**
LibMake `--edition` आणि `--rustversion` साठी कोणतीही स्ट्रिंग स्वीकारते आणि ती मूल्ये थेट `Cargo.toml` मध्ये लिहिते. निर्दिष्ट केलेली आवृत्ती किंवा MSRV खरी Rust आवृत्ती आहे का याची ते पडताळणी करत नाही, त्यामुळे योग्य मूल्ये पुरवण्याची जबाबदारी कॉलरची असते.

## संदर्भ

1. Rousseau, S. *LibMake — A code generator to reduce repetitive tasks and build high-quality Rust libraries*. GitHub, 2023. https://github.com/sebastienrousseau/libmake
2. The Rust Programming Language. *Rust API Guidelines*. GitHub, 2023. https://rust-lang.github.io/api-guidelines/
3. The Cargo Book. *Package Layout*. The Rust Programming Language, 2023. https://doc.rust-lang.org/cargo/guide/project-layout.html
4. Keats, V. et al. *Tera — A template engine inspired by Jinja2 and Django templates*. GitHub, 2023. https://keats.github.io/tera/

[00]: https://github.com/sebastienrousseau/libmake "LibMake — Rust library scaffold generator"
