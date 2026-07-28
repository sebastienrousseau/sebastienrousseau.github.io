---
title: "LibMake: เครื่องมือสร้างโครงสร้างไลบรารี Rust"
subtitle: "LibMake: เครื่องมือสร้างโค้ด Rust ที่บังคับใช้แนวปฏิบัติที่ดีที่สุดตั้งแต่วันแรก"
description: "LibMake คือเครื่องมือ CLI ของ Rust ที่สร้างโครงสร้างไลบรารีแบบครบถ้วน ทั้ง Cargo.toml, src/lib.rs พร้อมเทมเพลตเอกสาร ชุดทดสอบและเบนช์มาร์ก และ CI ของ GitHub Actions จากคำสั่งเดียวหรือไฟล์คอนฟิก TOML/YAML ที่มีการกำหนดเวอร์ชัน"
date: "October 26, 2023"
language: "th-TH"
locale: "th_TH"
banner: "https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp"
banner_alt: "เสาสีขาวขนาดใหญ่"
keywords: "LibMake, เครื่องมือสร้างโค้ด Rust, โครงสร้าง cargo, เทมเพลตไลบรารี Rust, การทำเทมเพลตด้วย Tera, GitHub Actions Rust, cargo-audit, Rust API Guidelines, เครื่องมือสร้างโค้ดต้นแบบ, เวิร์กโฟลว์ CI ของ Rust"
---

![เสาสีขาวขนาดใหญ่](https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp).class=\"img-fluid clearfix\"

[**LibMake ⧉**][00] คือ CLI และไลบรารีของ Rust แบบโอเพนซอร์สที่สร้างโครงสร้างโปรเจกต์ไลบรารีแบบครบถ้วนจากการเรียกใช้เพียงครั้งเดียว โดยเติมเต็มช่องว่างระหว่าง `cargo new --lib` (ซึ่งสร้างเพียง Cargo.toml และ src/lib.rs ขั้นต่ำ) กับการตั้งค่าไลบรารีที่พร้อมใช้งานจริง (ซึ่งต้องเพิ่มคอมเมนต์เอกสาร, CI, ชุดทดสอบ, โครงสร้างเบนช์มาร์ก, CONTRIBUTING.md และไฟล์สัญญาอนุญาตด้วยตนเอง)

บทความนี้อธิบายว่า LibMake สร้างอะไรบ้าง โหมดไฟล์คอนฟิกและโหมด CLI ทำงานอย่างไร โครงสร้าง CI ที่สร้างขึ้น และระบบการทำเทมเพลต

## การติดตั้งและการใช้งานเบื้องต้น

LibMake เผยแพร่บน [crates.io](https://crates.io/crates/libmake) และติดตั้งผ่าน Cargo:

```bash
cargo install libmake
```

การเรียกใช้ CLI ขั้นต่ำจะสร้างไลบรารีตามชื่อที่กำหนดในไดเรกทอรีปัจจุบัน:

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

แฟล็กเสริมเพิ่มเติมได้แก่ `--categories`, `--keywords`, `--homepage`, `--documentation`, `--readme` และ `--build`

## โหมดไฟล์คอนฟิก

สำหรับการใช้งานเป็นทีม แฟล็ก CLI ทั้งหมดสามารถระบุในไฟล์คอนฟิก TOML ได้:

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

เรียกใช้ดังนี้:

```bash
libmake --config libmake.toml
```

LibMake ยังรองรับรูปแบบคอนฟิก JSON, YAML และ CSV ผ่านแฟล็ก `--config-json`, `--config-yaml` และ `--config-csv` ตามลำดับ การคอมมิต `libmake.toml` ไว้ที่รากของที่เก็บโค้ดทำให้ผู้ร่วมพัฒนาทุกคนมีฐานโครงสร้างที่ทำซ้ำได้เหมือนกัน และการเปลี่ยนแปลงในการตั้งค่าเทมเพลตจะปรากฏใน Git diff

## โครงสร้างโปรเจกต์ที่สร้างขึ้น

การเรียกใช้ LibMake หนึ่งครั้งจะสร้างโครงสร้างดังต่อไปนี้:

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

ไฟล์ `src/lib.rs` ที่สร้างขึ้นมีคอมเมนต์เอกสารระดับเครต, `#![deny(missing_docs)]`, `#![doc = include_str!("../README.md")]` เพื่อดึง README เข้าสู่ rustdoc และไทป์สาธารณะแบบโครงร่างพร้อมคอมเมนต์เอกสารที่เกี่ยวข้อง ตัวเลือกเหล่านี้เป็นไปตามข้อกำหนดของ Rust API Guidelines ที่ว่าไอเท็มสาธารณะทุกรายการต้องมีเอกสารกำกับ

ไฟล์ `benches/lib_benchmarks.rs` ที่สร้างขึ้นใช้ [Criterion.rs](https://github.com/bheisler/criterion.rs) และต้องเพิ่ม `criterion` เป็น dev-dependency ซึ่ง LibMake จะแทรกลงใน `Cargo.toml` ให้โดยอัตโนมัติ

## เวิร์กโฟลว์ CI ของ GitHub Actions

ไฟล์ `.github/workflows/release.yml` ที่สร้างขึ้นจะรันงานห้ารายการในทุกครั้งที่ push และ pull request:

| งาน | ทูลเชน | ตรวจสอบอะไร |
|---|---|---|
| `test` | stable, beta, nightly (เมทริกซ์) | `cargo test --all-features` |
| `clippy` | stable | `cargo clippy -- -D warnings` |
| `fmt` | stable | `cargo fmt --check` |
| `audit` | stable | `cargo audit` (ติดตั้ง cargo-audit ในงาน) |
| `doc` | stable | `cargo doc --no-deps` (ล้มเหลวเมื่อขาดเอกสาร) |

งาน nightly มี `continue-on-error: true` เพื่อไม่ให้การถดถอยใน nightly ขวางการรวมโค้ด แต่ยังคงแสดงความล้มเหลวในการรันเวิร์กโฟลว์

## การทำเทมเพลตด้วย Tera

LibMake ใช้เอนจินเทมเพลต [Tera](https://keats.github.io/tera/) ซึ่งเป็นไวยากรณ์คล้าย Jinja2 สำหรับ Rust ในการเรนเดอร์ไฟล์ที่สร้างขึ้นทั้งหมด แต่ละเทมเพลตจะได้รับสตรัคต์คอนฟิกทั้งหมดเป็นบริบท:

```
{{ name }}            → my_library
{{ author }}          → Jane Smith
{{ edition }}         → 2021
{{ description }}     → A Rust library for doing useful things
```

รองรับไดเรกทอรีเทมเพลตที่กำหนดเองผ่านแฟล็ก `--template`:

```bash
libmake --config libmake.toml --template ./my_templates/
```

ไดเรกทอรีที่กำหนดเองต้องมีโครงสร้างตรงกับโครงสร้างเทมเพลตเริ่มต้น (ใช้ชื่อไฟล์เดียวกัน) ไฟล์ใดก็ตามที่มีอยู่ในไดเรกทอรีที่กำหนดเองจะแทนที่เทมเพลตในตัวที่ตรงกัน ส่วนไฟล์ที่ไม่มีอยู่ในไดเรกทอรีที่กำหนดเองจะย้อนกลับไปใช้เวอร์ชันในตัว วิธีนี้อนุญาตให้แทนที่เพียงบางส่วนได้ เช่น การแทนที่เฉพาะเทมเพลตเวิร์กโฟลว์ CI ในขณะที่ยังคงใช้เทมเพลต src/lib.rs และ Cargo.toml เริ่มต้น

## คำถามที่พบบ่อย

**LibMake แตกต่างจาก `cargo new --lib` อย่างไร?**
`cargo new --lib` สร้างโปรเจกต์ขั้นต่ำที่มีเพียง `Cargo.toml` และ `src/lib.rs` (ซึ่งมีบล็อก `#[cfg(test)]` เพียงบล็อกเดียว) ส่วน LibMake สร้างโครงสร้างแบบครบถ้วน ทั้งการทดสอบแบบบูรณาการ, เบนช์มาร์ก, CI, CONTRIBUTING.md, ไฟล์สัญญาอนุญาตแบบคู่ และ src/lib.rs ที่มีเอกสารกำกับอย่างเหมาะสม โดยตั้งค่าด้วยเมทาดาทาจริงของโปรเจกต์แทนที่จะเป็นค่าตัวอย่าง

**ใช้ LibMake กับ Cargo workspace ที่มีอยู่แล้วได้หรือไม่?**
LibMake สร้างไดเรกทอรีเครตแบบสแตนด์อโลน หากต้องการเพิ่มเครตที่สร้างขึ้นเข้าสู่ workspace ที่มีอยู่ ให้เพิ่มพาธเอาต์พุตลงในอาร์เรย์ `members` ของ workspace ใน `Cargo.toml` ที่ราก LibMake จะไม่แก้ไขไฟล์ workspace ที่มีอยู่

**สามารถอัปเดตเทมเพลตโครงสร้างหลังจากสร้างครั้งแรกได้หรือไม่?**
LibMake สร้างไฟล์เพียงครั้งเดียว และไม่ติดตามหรืออัปเดตโปรเจกต์ที่สร้างไว้ก่อนหน้า หากต้องการนำเทมเพลตที่อัปเดตมาใช้ แนวทางที่แนะนำคือการรัน LibMake ใหม่ลงในไดเรกทอรีชั่วคราว แล้วเปรียบเทียบผลลัพธ์กับเครตที่มีอยู่ จากนั้นนำการเปลี่ยนแปลงที่ต้องการมาใช้อย่างเลือกสรร

**LibMake รองรับ Rust edition และค่า MSRV ใดบ้าง?**
LibMake รับสตริงใดก็ได้สำหรับ `--edition` และ `--rustversion` และเขียนค่าเหล่านั้นลงใน `Cargo.toml` โดยตรง มันไม่ได้ตรวจสอบว่า edition หรือ MSRV ที่ระบุเป็นเวอร์ชัน Rust จริงหรือไม่ ดังนั้นผู้เรียกใช้จึงมีหน้าที่ระบุค่าที่ถูกต้อง

## เอกสารอ้างอิง

1. Rousseau, S. *LibMake — A code generator to reduce repetitive tasks and build high-quality Rust libraries*. GitHub, 2023. https://github.com/sebastienrousseau/libmake
2. The Rust Programming Language. *Rust API Guidelines*. GitHub, 2023. https://rust-lang.github.io/api-guidelines/
3. The Cargo Book. *Package Layout*. The Rust Programming Language, 2023. https://doc.rust-lang.org/cargo/guide/project-layout.html
4. Keats, V. et al. *Tera — A template engine inspired by Jinja2 and Django templates*. GitHub, 2023. https://keats.github.io/tera/

[00]: https://github.com/sebastienrousseau/libmake "LibMake เครื่องมือสร้างโครงสร้างไลบรารี Rust"
